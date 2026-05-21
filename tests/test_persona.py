"""Persona safety contract — covers both persona files.

The two persona files in this repo are both spliced into the agent's
SOUL.md at deploy time:

  - ``persona/system_prompt.md.j2`` — full brand persona (replaces the
    bundled mintbot persona entirely).
  - ``persona/brand_layer.md``      — optional short voice overlay
    appended at the very end.

To stop a malicious or careless template from impersonating mintbot,
hijacking the chat-completion role machinery, or hiding text inside
HTML comments, we reject any file that contains role-changing markers
or other prompt-injection patterns.

If you legitimately need to mention one of these strings (e.g. in a
code example), describe it in prose instead of pasting the literal
token — your customers see this file's content in their agent's
persona, not its raw source.

mintbot re-runs this check at deploy time. Keep it green.
"""
from __future__ import annotations

import re
from pathlib import Path

PERSONA_PATHS: tuple[str, ...] = (
    "persona/system_prompt.md.j2",
    "persona/brand_layer.md",
)

# Case-insensitive substring matches — these are markers used by LLM chat
# templates and prompt-injection attacks to flip into a different role
# or system context.
FORBIDDEN_LITERALS: tuple[str, ...] = (
    "<|system|>",
    "<|user|>",
    "<|assistant|>",
    "<|im_start|>",
    "<|im_end|>",
    "<|endoftext|>",
    "[INST]",
    "[/INST]",
    "<<SYS>>",
    "<</SYS>>",
    "### Instruction:",
    "### System:",
    "<<system>>",
    "<<user>>",
)

# Regex patterns — catch role headers at line start and HTML comments
# (we forbid HTML comments entirely so the brand layer can't smuggle
# hidden instructions past a casual reviewer).
FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("HTML comment", re.compile(r"<!--", re.IGNORECASE)),
    ("Role header at line start", re.compile(r"^\s*(system|user|assistant)\s*:", re.IGNORECASE | re.MULTILINE)),
)


def _scan_persona(path: Path, rel: str) -> list[str]:
    """Return a list of safety-rule violations for ``path`` (empty if clean)."""
    text = path.read_text(encoding="utf-8")
    hits: list[str] = []
    lowered = text.lower()
    for marker in FORBIDDEN_LITERALS:
        if marker.lower() in lowered:
            hits.append(f"{rel}: contains forbidden marker: {marker!r}")
    for label, pat in FORBIDDEN_PATTERNS:
        if pat.search(text):
            hits.append(f"{rel}: contains forbidden pattern: {label}")
    return hits


def test_persona_no_injection_markers(repo_root: Path) -> None:
    """Every persona file present must be free of prompt-injection markers."""
    hits: list[str] = []
    for rel in PERSONA_PATHS:
        path = repo_root / rel
        if not path.exists():
            # Persona files are optional — whitelist / required-files tests
            # cover existence. Brand_layer.md in particular is fully optional.
            continue
        hits.extend(_scan_persona(path, rel))
    assert not hits, (
        "Persona file(s) contain prompt-injection markers that mintbot "
        "will reject at deploy time:\n  " + "\n  ".join(hits)
    )


def test_persona_is_utf8_text(repo_root: Path) -> None:
    """Every persona file present must be plain UTF-8 — no binary, no BOM."""
    for rel in PERSONA_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), (
            f"{rel} starts with a UTF-8 BOM — strip it (most editors "
            "have a 'save without BOM' option)."
        )
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"{rel} is not valid UTF-8: {exc}") from exc


def test_persona_system_prompt_jinja_renders(repo_root: Path) -> None:
    """``system_prompt.md.j2`` must render with the deploy-time Jinja context.

    mintbot passes ``agent_id`` (int), ``panel_domain_base`` (str), and
    ``bot_handle`` (str) to this template. A typo here would not be caught
    by the safety scan above — it surfaces as a deploy crash. We render
    against the same StrictUndefined env to fail loud locally instead.
    """
    path = repo_root / "persona/system_prompt.md.j2"
    if not path.exists():
        # File is optional — partners may stick with brand_layer.md only.
        return
    try:
        from jinja2 import Environment, FileSystemLoader, StrictUndefined
    except ImportError:
        # Jinja2 is a test-only dep; skip gracefully when not installed.
        return
    env = Environment(
        loader=FileSystemLoader(str(path.parent)),
        keep_trailing_newline=True,
        undefined=StrictUndefined,
        autoescape=False,
    )
    out = env.get_template(path.name).render(
        agent_id=8061,
        panel_domain_base="example.com",
        bot_handle="@example_bot",
    )
    assert out.strip(), "system_prompt.md.j2 rendered to empty output"
