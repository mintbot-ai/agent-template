"""Pytest fixtures shared across template validation tests."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Path to the template repo root (the directory containing this file's parent)."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def theme_dir(repo_root: Path) -> Path:
    return repo_root / "theme"


@pytest.fixture(scope="session")
def preview_dir(repo_root: Path) -> Path:
    return repo_root / "preview"
