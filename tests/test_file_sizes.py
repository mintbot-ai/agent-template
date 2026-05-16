"""Enforce per-file size budgets.

A bloated theme makes the panel slow to load. mintbot enforces the same
limits at deploy time — keep them in sync if you change the numbers.
"""
from __future__ import annotations

from pathlib import Path

# (relative path, max size in KB)
SIZE_BUDGETS: tuple[tuple[str, int], ...] = (
    ("theme/theme.css", 64),
    ("theme/theme.js",  32),
    ("theme/theme.json", 8),
    # Persona overlay is injected into SOUL.md on every turn — keep it
    # tight so it doesn't push capabilities/persona past Hermes's context
    # file truncation budget (~14 KB head + 4 KB tail).
    ("persona/brand_layer.md", 8),
)


def test_file_sizes_within_budget(repo_root: Path) -> None:
    overruns: list[str] = []
    for rel, max_kb in SIZE_BUDGETS:
        path = repo_root / rel
        if not path.exists():
            continue  # whitelist + required-files tests cover existence
        size_kb = path.stat().st_size / 1024
        if size_kb > max_kb:
            overruns.append(f"{rel}: {size_kb:.1f} KB > {max_kb} KB budget")
    assert not overruns, "Files exceed size budget:\n  " + "\n  ".join(overruns)
