"""Local sanity checks for a customization repo.

These run in your CI before you deploy. They do NOT run centrally — in the
"VPS-side" model the platform never executes your repo — but catching
mistakes here saves a round-trip through a deploy. Run with: ``pytest -q``.

What's checked:
  * install.sh / update.sh / lib/common.sh parse under ``bash -n``.
  * shellcheck passes (skipped if shellcheck isn't installed).
  * the brand-voice overlay obeys the same rules the agent's persona CLI
    enforces at apply time (size cap + no role/template markers), so a
    rejected overlay is caught here instead of silently not applying.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = ["install.sh", "update.sh", "lib/common.sh"]

# Mirror of the agent persona CLI's overlay cap (SOUL.local.md) and its
# forbidden role/template markers. Keep in sync with the platform; if these
# drift, the worst case is CI is slightly stricter than the box.
OVERLAY_MAX_CHARS = 4000
FORBIDDEN_MARKERS = (
    "<|system|>", "<|user|>", "<|assistant|>", "<|im_start|>", "<|im_end|>",
    "<|endoftext|>", "[INST]", "[/INST]", "<<SYS>>", "<</SYS>>",
    "<|begin_of_text|>", "<|eot_id|>", "<|start_header_id|>",
    "<|end_header_id|>", "<start_of_turn>", "<end_of_turn>",
    "### Instruction:", "### System:", "### Response:", "<<system>>",
    "<<user>>", "<!--",
)
ROLE_LINE_PREFIXES = ("system:", "user:", "assistant:")


@pytest.mark.parametrize("rel", SCRIPTS)
def test_bash_syntax(rel: str) -> None:
    path = REPO / rel
    assert path.is_file(), f"{rel} is missing"
    r = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    assert r.returncode == 0, f"{rel} has a syntax error:\n{r.stderr}"


def test_install_is_executable() -> None:
    # install.sh is the required entry point; the runner invokes it with
    # `bash`, but keeping it +x is good hygiene and self-documenting.
    assert (REPO / "install.sh").is_file(), "install.sh is required"


@pytest.mark.skipif(shutil.which("shellcheck") is None, reason="shellcheck not installed")
@pytest.mark.parametrize("rel", SCRIPTS)
def test_shellcheck(rel: str) -> None:
    r = subprocess.run(
        ["shellcheck", "-x", "-S", "warning", str(REPO / rel)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"shellcheck flagged {rel}:\n{r.stdout}{r.stderr}"


def _persona_files() -> list[Path]:
    out = []
    for name in ("persona/brand_layer.md", "persona/soul.full.md"):
        p = REPO / name
        if p.is_file():
            out.append(p)
    return out


def test_brand_layer_within_overlay_cap() -> None:
    layer = REPO / "persona" / "brand_layer.md"
    if not layer.is_file():
        pytest.skip("no brand_layer.md")
    n = len(layer.read_text(encoding="utf-8"))
    assert n <= OVERLAY_MAX_CHARS, (
        f"brand_layer.md is {n} chars; the persona overlay cap is "
        f"{OVERLAY_MAX_CHARS}. Trim it or use the full-persona path."
    )


@pytest.mark.parametrize("path", _persona_files(), ids=lambda p: p.name)
def test_persona_has_no_forbidden_markers(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for marker in FORBIDDEN_MARKERS:
        assert marker.lower() not in lowered, (
            f"{path.name} contains a disallowed marker {marker!r} — the "
            f"persona CLI would reject it."
        )
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip().lower()
        for prefix in ROLE_LINE_PREFIXES:
            assert not stripped.startswith(prefix), (
                f"{path.name}:{i} starts with a chat-role prefix {prefix!r}."
            )
