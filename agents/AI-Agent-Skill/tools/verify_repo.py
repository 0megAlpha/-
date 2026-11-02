#!/usr/bin/env python3
"""Portable, non-destructive repository checks for the agent skill fleet."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills"
SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
TEXT_SUFFIXES = {
    ".py", ".sh", ".yaml", ".yml", ".json", ".toml", ".ini", ".conf",
    ".env", ".example", ".md", ".txt", ".js", ".ts", ".tsx", ".jsx",
    ".html", ".css", ".sql", ".service",
}
SECRET_PATTERNS = {
    "OpenAI-style API key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    "NVIDIA API key": re.compile(r"\bnvapi-[A-Za-z0-9_-]{30,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "Private key block": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE\x20KEY-----\s*"
        r"[A-Za-z0-9+/=\r\n]{100,}"
        r"-----END (?:RSA |EC |OPENSSH )?PRIVATE\x20KEY-----"
    ),
}

def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue
        yield path

def scan_secrets():
    findings = []
    for path in iter_files():
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".env", ".env.example"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(content):
                number = content.count("\n", 0, match.start()) + 1
                findings.append((path.relative_to(ROOT), number, label))
    if findings:
        for path, number, label in findings:
            print(f"FAIL possible {label}: {path}:{number}")
        return False
    print("PASS no high-confidence credential patterns in scanned text files")
    return True

def verify_structure():
    skills = sorted(SKILL_ROOT.glob("*/SKILL.md")) if SKILL_ROOT.exists() else []
    errors = []
    if not skills:
        errors.append("No skills/*/SKILL.md definitions found")
    for path in skills:
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError:
            errors.append(f"Unreadable skill definition: {path.relative_to(ROOT)}")
            continue
        if len(text) < 80:
            errors.append(f"Skill definition is unexpectedly short: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print("FAIL " + error)
        return False
    print(f"PASS skill structure: {len(skills)} SKILL.md definitions")
    return True

def verify_configs():
    try:
        import yaml
    except ImportError:
        print("FAIL PyYAML is required for YAML validation")
        return False
    class PortableSafeLoader(yaml.SafeLoader):
        pass
    def construct_unknown_tag(loader, tag_suffix, node):
        # Custom tags are parsed as inert data; they are never evaluated.
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        if isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node, deep=True)
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node, deep=True)
        return None
    PortableSafeLoader.add_multi_constructor("", construct_unknown_tag)
    json_files, yaml_files, errors = [], [], []
    for path in iter_files():
        if path.suffix.lower() == ".json":
            json_files.append(path)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            yaml_files.append(path)
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({type(exc).__name__})")
    for path in yaml_files:
        try:
            list(yaml.load_all(path.read_text(encoding="utf-8"), Loader=PortableSafeLoader))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML ({type(exc).__name__})")
    if errors:
        for error in errors:
            print("FAIL " + error)
        return False
    print(f"PASS config syntax: {len(json_files)} JSON and {len(yaml_files)} YAML files")
    return True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--secrets-only", action="store_true")
    args = parser.parse_args()
    checks = [scan_secrets()]
    if not args.secrets_only:
        checks += [verify_structure(), verify_configs()]
    return 0 if all(checks) else 1

if __name__ == "__main__":
    sys.exit(main())
