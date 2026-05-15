"""Validate theme.json shape and contents."""
from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED_TOP_LEVEL = ("name", "version", "author", "description", "entry")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.\-]+)?$")


def _load(theme_dir: Path) -> dict:
    return json.loads((theme_dir / "theme.json").read_text(encoding="utf-8"))


def test_theme_json_parses(theme_dir: Path) -> None:
    data = _load(theme_dir)
    assert isinstance(data, dict), "theme.json must be a JSON object"


def test_required_fields_present(theme_dir: Path) -> None:
    data = _load(theme_dir)
    missing = [k for k in REQUIRED_TOP_LEVEL if k not in data]
    assert not missing, f"theme.json is missing required fields: {missing}"


def test_version_is_semver(theme_dir: Path) -> None:
    data = _load(theme_dir)
    version = data.get("version", "")
    assert SEMVER_RE.match(version), (
        f"theme.json `version` must be semver (e.g. 1.0.0), got: {version!r}"
    )


def test_entry_paths_exist(theme_dir: Path, repo_root: Path) -> None:
    data = _load(theme_dir)
    entry = data.get("entry", {})

    css_rel = entry.get("css")
    assert css_rel, "theme.json `entry.css` is required"
    assert (repo_root / css_rel).exists(), f"entry.css path does not exist: {css_rel}"

    js_rel = entry.get("js")
    if js_rel:
        assert (repo_root / js_rel).exists(), f"entry.js path does not exist: {js_rel}"


def test_name_is_reasonable(theme_dir: Path) -> None:
    data = _load(theme_dir)
    name = data.get("name", "")
    assert 1 <= len(name) <= 60, "theme.json `name` must be 1–60 chars"
    assert "\n" not in name, "theme.json `name` must be a single line"
