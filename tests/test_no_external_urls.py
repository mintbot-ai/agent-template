"""Reject external network references in theme files.

The deployed panel must be self-contained — no @import from off-site CSS,
no remote fonts, no third-party JS. The base panel ships its own fonts.

Allowed exceptions:
  * `data:` URIs (inline content, no network call).
  * Relative paths (no scheme).
  * The exact host pattern listed in ALLOWED_HOSTS, if any.
"""
from __future__ import annotations

import re
from pathlib import Path

# Currently no off-site hosts are allowed. Extend with care.
ALLOWED_HOSTS: tuple[str, ...] = ()

URL_RE = re.compile(r"https?://([^\s'\"\)]+)", re.IGNORECASE)


def _scan(path: Path) -> list[tuple[int, str]]:
    """Return (line_number, offending_url) for every disallowed URL."""
    out: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in URL_RE.finditer(line):
            host_path = match.group(1)
            host = host_path.split("/", 1)[0]
            if any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
                continue
            out.append((lineno, match.group(0)))
    return out


def test_theme_css_no_external_urls(theme_dir: Path) -> None:
    findings = _scan(theme_dir / "theme.css")
    assert not findings, (
        "theme.css references external URLs (only data: URIs and relative "
        f"paths are allowed):\n  " + "\n  ".join(f"L{n}: {u}" for n, u in findings)
    )


def test_theme_js_no_external_urls(theme_dir: Path) -> None:
    js_path = theme_dir / "theme.js"
    if not js_path.exists():
        return  # theme.js is optional
    findings = _scan(js_path)
    assert not findings, (
        "theme.js references external URLs:\n  "
        + "\n  ".join(f"L{n}: {u}" for n, u in findings)
    )
