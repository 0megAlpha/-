#!/usr/bin/env python3
"""Validate and optionally repair the local agent catalog registry."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    output = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()
    return Path(output)


def _dir_names(path: Path) -> list[str]:
    return sorted(
        entry.name
        for entry in path.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    )


def _load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_registry(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _print_diff(label: str, missing: set[str], extra: set[str]) -> None:
    if not missing and not extra:
        print(f"[OK] {label}: no drift detected")
        return

    print(f"[DRIFT] {label}")
    if missing:
        print("  missing from registry:")
        for item in sorted(missing):
            print(f"    + {item}")
    if extra:
        print("  no longer on disk:")
        for item in sorted(extra):
            print(f"    - {item}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check `.agents/skill-registry.json` against `.agents/skills` and "
            "`extensions/plugins`."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Repair registry lists to match current directories",
    )
    args = parser.parse_args()

    root = _repo_root()
    registry_path = root / ".agents" / "skill-registry.json"
    skills_path = root / ".agents" / "skills"
    plugins_path = root / "extensions" / "plugins"

    registry = _load_registry(registry_path)
    registry_skills = set(registry.get("skills", []))
    registry_plugins = set(registry.get("plugins", []))
    actual_skills = set(_dir_names(skills_path))
    actual_plugins = set(_dir_names(plugins_path))

    missing_skills = actual_skills - registry_skills
    extra_skills = registry_skills - actual_skills
    missing_plugins = actual_plugins - registry_plugins
    extra_plugins = registry_plugins - actual_plugins

    _print_diff("skills", missing_skills, extra_skills)
    _print_diff("plugins", missing_plugins, extra_plugins)

    has_drift = any(
        (
            missing_skills,
            extra_skills,
            missing_plugins,
            extra_plugins,
        )
    )

    if args.apply and has_drift:
        registry["skills"] = sorted(actual_skills)
        registry["plugins"] = sorted(actual_plugins)
        _write_registry(registry_path, registry)
        print("[FIXED] Registry updated.")
        return 0

    if has_drift:
        print("Run with --apply to repair the registry.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
