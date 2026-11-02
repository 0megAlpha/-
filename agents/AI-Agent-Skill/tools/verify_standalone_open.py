#!/usr/bin/env python3
"""Config-level verification that each integrated component is individually openable."""
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_path(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        default=str(ROOT / "integrations" / "agent-registry" / "integration-inventory.yaml"),
    )
    parser.add_argument("--lock", default=str(ROOT / "integrations" / "agent-registry" / "runtime-sources.lock.json"))
    parser.add_argument(
        "--output",
        default=str(ROOT / "integrations" / "agent-registry" / "standalone-open-report.json"),
    )
    args = parser.parse_args()

    inventory = load_yaml(Path(args.inventory))
    lock = load_json(Path(args.lock))
    lock_index = {item.get("id"): item for item in lock.get("sources", []) if isinstance(item, dict)}
    source_index = {item.get("id"): item for item in inventory.get("sources", []) if isinstance(item, dict)}

    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    for binding in inventory.get("agent_bindings", []):
        if not isinstance(binding, dict):
            continue
        agent = str(binding.get("agent", "")).strip()
        source = str(binding.get("source", "")).strip()
        mode = str(binding.get("mode", "")).strip()
        if not agent:
            continue

        adapter_path = f"agents/{agent}/adapter.yaml"
        adapter_ok = check_path(adapter_path)
        result = {
            "agent": agent,
            "source": source,
            "mode": mode,
            "adapter_path": adapter_path,
            "adapter_exists": adapter_ok,
            "runtime_entry_exists": source in source_index if source else False,
            "lock_resolved": bool(lock_index.get(source, {}).get("resolved")) if source else False,
            "runtime_readme_exists": check_path(f"runtimes/{source}/README.md") if source else False,
            "status": "ok",
        }

        if not adapter_ok:
            result["status"] = "fail"
            failures.append(f"{agent}: missing adapter at {adapter_path}")
        elif source and mode != "external-independent":
            src = source_index.get(source, {})
            kind = src.get("kind")
            if source not in source_index:
                result["status"] = "fail"
                failures.append(f"{agent}: source {source} not found in inventory")
            elif source in lock_index and not lock_index[source].get("resolved"):
                result["status"] = "fail"
                failures.append(f"{agent}: source {source} unresolved in LOCK.json")
            elif kind == "git" and not result["runtime_readme_exists"]:
                result["status"] = "fail"
                failures.append(f"{agent}: runtimes/{source}/README.md missing")

        checks.append(result)

    report = {
        "generated_at": utc_now(),
        "summary": {"total": len(checks), "failed": len(failures)},
        "failures": failures,
        "components": checks,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Standalone-open verification: total={len(checks)} failed={len(failures)}")
    if failures:
        for item in failures:
            print("FAIL", item)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
