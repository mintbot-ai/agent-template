"""Reject obviously dangerous JavaScript patterns in theme.js.

This is a STATIC sanity check, not a full sandbox — mintbot does
additional checks at deploy time. The goal here is to catch common
mistakes early in CI.
"""
from __future__ import annotations

import re
from pathlib import Path

# Each rule: (regex, human-readable reason).
FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\beval\s*\(", "eval() is not allowed"),
    (r"\bnew\s+Function\s*\(", "new Function() is not allowed"),
    (r"document\.write\s*\(", "document.write() is not allowed"),
    (r"\.innerHTML\s*=", "Assigning to .innerHTML is not allowed (use textContent)"),
    (r"\.outerHTML\s*=", "Assigning to .outerHTML is not allowed"),
    (r"document\.createElement\s*\(\s*['\"]script['\"]\s*\)", "Dynamic <script> injection is not allowed"),
    (r"\bimport\s*\(", "Dynamic import() is not allowed"),
)


def test_theme_js_no_unsafe_patterns(theme_dir: Path) -> None:
    js_path = theme_dir / "theme.js"
    if not js_path.exists():
        return  # theme.js is optional

    src = js_path.read_text(encoding="utf-8", errors="replace")
    findings: list[str] = []
    for pattern, reason in FORBIDDEN_PATTERNS:
        for match in re.finditer(pattern, src):
            line = src.count("\n", 0, match.start()) + 1
            findings.append(f"L{line}: {reason} (matched `{match.group(0)}`)")
    assert not findings, "theme.js contains unsafe patterns:\n  " + "\n  ".join(findings)
