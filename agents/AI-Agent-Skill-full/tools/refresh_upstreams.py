#!/usr/bin/env python3
"""Refresh upstream source lock metadata for integrated runtimes/packages."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled in CI/runtime
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def parse_github(remote: str) -> tuple[str, str] | None:
    patterns = [
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?/?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, remote)
        if match:
            return match.group("owner"), match.group("repo")
    return None


def request_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def resolve_git_head(remote: str, branch: str, github_token: str | None) -> tuple[str | None, str | None]:
    parsed = parse_github(remote)
    if not parsed:
        return None, f"unsupported_git_remote:{remote}"
    owner, repo = parsed
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ai-agent-skill-sync"}
    if github_token:
        headers["Authorization"] = "token " + github_token
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{urllib.parse.quote(branch, safe='')}"
    api_error: str | None = None
    try:
        payload = request_json(url, headers=headers)
        sha = payload.get("sha")
        if isinstance(sha, str) and sha:
            return sha, None
        api_error = "github_commit_sha_missing"
    except urllib.error.HTTPError as exc:
        api_error = f"github_http_{exc.code}"
    except Exception as exc:  # pragma: no cover - network failure path
        api_error = f"github_error_{type(exc).__name__}"

    # Private repositories may be readable through the host's existing Git/SSH
    # credentials even when the unauthenticated GitHub REST API returns 404.
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", remote, f"refs/heads/{branch}"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                fields = line.split()
                if len(fields) == 2 and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", fields[0]):
                    return fields[0], None
        return None, f"{api_error};git_ls_remote_exit_{result.returncode}"
    except Exception as exc:  # pragma: no cover - network failure path
        return None, f"{api_error};git_ls_remote_error_{type(exc).__name__}"


def resolve_npm_latest(package: str) -> tuple[str | None, str | None]:
    encoded = urllib.parse.quote(package, safe="@/")
    url = f"https://registry.npmjs.org/{encoded}"
    try:
        payload = request_json(url, headers={"Accept": "application/json", "User-Agent": "ai-agent-skill-sync"})
        latest = payload.get("dist-tags", {}).get("latest")
        if not isinstance(latest, str) or not latest:
            return None, "npm_latest_missing"
        return latest, None
    except urllib.error.HTTPError as exc:
        return None, f"npm_http_{exc.code}"
    except Exception as exc:  # pragma: no cover - network failure path
        return None, f"npm_error_{type(exc).__name__}"


def numeric_version_tuple(value: Any) -> tuple[int, ...] | None:
    """Parse simple numeric dotted versions; leave prerelease formats untouched."""
    if not isinstance(value, str) or not re.fullmatch(r"\d+(?:\.\d+)*", value.strip()):
        return None
    try:
        return tuple(int(part) for part in value.strip().split("."))
    except ValueError:
        return None


def refresh(inventory: dict[str, Any], previous_lock: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    previous_sources = {item.get("id"): item for item in previous_lock.get("sources", []) if isinstance(item, dict)}
    refreshed_sources: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    github_token = os.environ.get("GITHUB_TOKEN")

    for source in inventory.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("id", "")).strip()
        kind = str(source.get("kind", "")).strip()
        if not source_id or not kind:
            continue

        previous_entry = previous_sources.get(source_id, {})
        previous_resolved = previous_entry.get("resolved")
        resolved: str | None = None
        error: str | None = None
        tracked = None

        if kind == "git":
            remote = str(source.get("remote", "")).strip()
            branch = str(source.get("branch", "main")).strip() or "main"
            tracked = branch
            if remote:
                resolved, error = resolve_git_head(remote, branch, github_token)
            else:
                error = "missing_git_remote"
        elif kind == "npm":
            package = str(source.get("package", "")).strip()
            tracked = source.get("version")
            if package:
                resolved, error = resolve_npm_latest(package)
                tracked_tuple = numeric_version_tuple(tracked)
                resolved_tuple = numeric_version_tuple(resolved)
                if resolved and tracked_tuple and resolved_tuple and resolved_tuple < tracked_tuple:
                    error = f"npm_version_downgrade_detected:{tracked}->{resolved}"
                    previous_tuple = numeric_version_tuple(previous_resolved)
                    resolved = previous_resolved if previous_tuple and previous_tuple >= tracked_tuple else str(tracked)
            else:
                error = "missing_npm_package"
        else:
            error = f"unsupported_kind:{kind}"

        if not resolved and isinstance(previous_resolved, str) and previous_resolved:
            resolved = previous_resolved

        entry = {
            "id": source_id,
            "kind": kind,
            "tracked": tracked,
            "resolved": resolved,
            "required": bool(source.get("required", False)),
            "status": "ok" if error is None else "degraded",
            "error": error,
            "checked_at": utc_now(),
        }
        refreshed_sources.append(entry)

        if error:
            failures.append({"id": source_id, "error": error, "required": bool(source.get("required", False))})

        if previous_resolved and resolved and previous_resolved != resolved:
            changes.append({"id": source_id, "from": previous_resolved, "to": resolved})
        elif not previous_resolved and resolved:
            changes.append({"id": source_id, "from": None, "to": resolved})

    lock_payload = {
        "generated_at": utc_now(),
        "inventory_version": inventory.get("version"),
        "sources": refreshed_sources,
        "summary": {
            "total": len(refreshed_sources),
            "updated": len(changes),
            "failed": len(failures),
        },
    }
    report_payload = {
        "generated_at": utc_now(),
        "changes": changes,
        "failures": failures,
        "requires_manual_attention": any(item.get("required") for item in failures),
    }
    return lock_payload, report_payload


def apply_upgrades_to_runtime_sources(lock_payload: dict[str, Any], runtime_sources_path: Path) -> tuple[int, int]:
    runtime_sources = load_yaml(runtime_sources_path)
    entries = runtime_sources.get("runtimes", {})
    if not isinstance(entries, dict):
        return 0, 0

    lock_index = {item.get("id"): item for item in lock_payload.get("sources", []) if isinstance(item, dict)}
    updated = 0
    examined = 0
    for source_id, lock_entry in lock_index.items():
        target = entries.get(source_id)
        if not isinstance(target, dict):
            continue
        examined += 1
        resolved = lock_entry.get("resolved")
        if not resolved:
            continue
        if lock_entry.get("kind") == "git":
            before = target.get("commit")
            if before != resolved:
                target["commit"] = resolved
                updated += 1
        elif lock_entry.get("kind") == "npm":
            # The npm package version and the product/runtime version are not
            # necessarily the same (e.g. @cline/cli package 0.0.13 vs Cline 3.0.62).
            version_field = "package_version" if "package_version" in target else "version"
            before = target.get(version_field)
            if before != resolved:
                target[version_field] = resolved
                updated += 1

    if updated:
        write_yaml(runtime_sources_path, runtime_sources)
    return examined, updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        default=str(ROOT / "integrations" / "agent-registry" / "integration-inventory.yaml"),
    )
    parser.add_argument("--lock", default=str(ROOT / "integrations" / "agent-registry" / "runtime-sources.lock.json"))
    parser.add_argument("--report", default=str(ROOT / "integrations" / "agent-registry" / "upstream-refresh-report.json"))
    parser.add_argument(
        "--runtime-sources",
        default=str(ROOT / "runtimes" / "runtime-sources.yaml"),
        help="Path to runtime-sources.yaml for automatic version/commit upgrades.",
    )
    parser.add_argument(
        "--apply-upgrades",
        action="store_true",
        help="Apply resolved versions/commits into runtime-sources.yaml.",
    )
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    lock_path = Path(args.lock)
    report_path = Path(args.report)

    inventory = load_yaml(inventory_path)
    previous_lock = load_json(lock_path)

    lock_payload, report_payload = refresh(inventory, previous_lock)

    if args.apply_upgrades:
        examined, updated = apply_upgrades_to_runtime_sources(lock_payload, Path(args.runtime_sources))
        report_payload["runtime_sources_upgrade"] = {
            "examined": examined,
            "updated": updated,
            "path": args.runtime_sources,
        }

    write_json(lock_path, lock_payload)
    write_json(report_path, report_payload)

    failed_required = [f for f in report_payload["failures"] if f.get("required")]
    print(f"Refreshed {lock_payload['summary']['total']} sources; updates={lock_payload['summary']['updated']} failed={lock_payload['summary']['failed']}")
    if failed_required:
        print(f"Required source failures: {len(failed_required)}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
