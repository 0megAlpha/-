#!/usr/bin/env python3
"""Validate integration inventory and compatibility mappings."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install PyYAML") from exc

ROOT = Path(__file__).resolve().parents[1]
CORE_AGENTS = {"openhands", "hermes", "dsh", "opencode", "claude-code"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def validate(inventory: dict[str, Any], compatibility: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    blocking: list[str] = []
    warnings: list[str] = []
    isolated: list[str] = []

    sources = [item for item in inventory.get("sources", []) if isinstance(item, dict)]
    source_ids = {item.get("id") for item in sources if item.get("id")}
    required_ids = {item.get("id") for item in sources if item.get("required")}

    if not sources:
        blocking.append("integration inventory has no sources")

    if not isinstance(compatibility.get("agents"), dict):
        blocking.append("agent compatibility file missing agents mapping")
    else:
        compatibility_agents = set(compatibility["agents"].keys())
        for agent in CORE_AGENTS:
            if agent not in compatibility_agents:
                blocking.append(f"missing compatibility record for core agent: {agent}")
        for name, conf in compatibility["agents"].items():
            if isinstance(conf, dict):
                status = str(conf.get("status", "")).lower()
                if "manual" in status or "not-applied" in status or "never-auto-start" in status:
                    isolated.append(name)

    agent_bindings = [item for item in inventory.get("agent_bindings", []) if isinstance(item, dict)]
    for binding in agent_bindings:
        source = binding.get("source")
        if source and source not in source_ids and binding.get("mode") != "external-independent":
            warnings.append(f"binding for agent {binding.get('agent')} references unknown source {source}")

    lock_sources = {item.get("id"): item for item in lock.get("sources", []) if isinstance(item, dict)}
    for req_id in sorted(required_ids):
        if req_id not in lock_sources:
            blocking.append(f"required source {req_id} missing from lock")
            continue
        lock_entry = lock_sources[req_id]
        if lock_entry.get("status") != "ok":
            blocking.append(f"required source {req_id} has degraded refresh status")
        if not lock_entry.get("resolved"):
            blocking.append(f"required source {req_id} has no resolved version")

    for source in sources:
        if source.get("kind") == "npm":
            channel = source.get("version_channel", "latest")
            if channel not in {"latest", "minor-patch", "patch"}:
                warnings.append(f"npm source {source.get('id')} uses uncommon version_channel={channel}")

    return {
        "generated_at": utc_now(),
        "blocking_issues": blocking,
        "warnings": warnings,
        "isolated_components": sorted(set(isolated)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        default=str(ROOT / "integrations" / "agent-registry" / "integration-inventory.yaml"),
    )
    parser.add_argument(
        "--compatibility",
        default=str(ROOT / "integrations" / "provider-gateway" / "agent-compatibility.yaml"),
    )
    parser.add_argument("--lock", default=str(ROOT / "integrations" / "agent-registry" / "runtime-sources.lock.json"))
    parser.add_argument(
        "--output",
        default=str(ROOT / "integrations" / "agent-registry" / "compatibility-report.json"),
    )
    args = parser.parse_args()

    inventory = load_yaml(Path(args.inventory))
    compatibility = load_yaml(Path(args.compatibility))
    lock = load_json(Path(args.lock))
    report = validate(inventory, compatibility, lock)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        "Integration matrix:",
        f"blocking={len(report['blocking_issues'])}",
        f"warnings={len(report['warnings'])}",
        f"isolated={len(report['isolated_components'])}",
    )
    if report["blocking_issues"]:
        for issue in report["blocking_issues"]:
            print("BLOCKING", issue)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
