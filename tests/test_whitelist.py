"""agent-template whitelist contract.

Only files listed in ALLOWED_PATTERNS may exist in the repo (excluding
the `.git/` directory and the `tests/` folder itself). This keeps the
deploy surface tiny and predictable — mintbot copies the matching
files into your agent at deploy time and rejects anything else.

Run with: pytest tests/test_whitelist.py
"""
from __future__ import annotations

import fnmatch
from pathlib import Path

# Each entry is a glob relative to the repo root.
ALLOWED_PATTERNS: tuple[str, ...] = (
    "README.md",
    "LICENSE",
    ".gitignore",
    ".github/workflows/*.yml",
    "theme/theme.css",
    "theme/theme.js",
    "theme/theme.json",
    "preview/index.html",
    "preview/base.css",
    "preview/README.md",
    "tests/*.py",
    "tests/README.md",
    "docs/*.md",
    "docs/*.json",
)

# Paths we silently ignore (housekeeping, never deployed).
IGNORE_PATTERNS: tuple[str, ...] = (
    ".git/*",
    "__pycache__/*",
    "*/__pycache__/*",
    ".pytest_cache/*",
    "*.pyc",
)


def _iter_repo_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, pat) for pat in IGNORE_PATTERNS):
            continue
        out.append(path)
    return out


def test_no_unknown_files(repo_root: Path) -> None:
    """Every file in the repo must match at least one allowed pattern."""
    unknown: list[str] = []
    for path in _iter_repo_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        if not any(fnmatch.fnmatch(rel, pat) for pat in ALLOWED_PATTERNS):
            unknown.append(rel)
    assert not unknown, (
        "These files are not in the allowed whitelist and will be rejected "
        "by mintbot at deploy time:\n  " + "\n  ".join(sorted(unknown))
    )


def test_required_files_present(repo_root: Path) -> None:
    """The minimum set of files must exist."""
    required = ("theme/theme.css", "theme/theme.json", "README.md", "LICENSE")
    missing = [p for p in required if not (repo_root / p).exists()]
    assert not missing, f"Required files are missing: {missing}"
