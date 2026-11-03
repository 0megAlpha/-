#!/usr/bin/env python3
"""Scan GitHub owners for agent-related repositories and emit discovery results."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def request_json(url: str, token: str | None) -> dict[str, Any] | list[Any]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ai-agent-skill-discovery"}
    if token:
        headers["Authorization"] = "token " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_owner_repos(owner: str, token: str | None, include_archived: bool, include_forks: bool) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{urllib.parse.quote(owner, safe='')}/repos?per_page=100&page={page}&type=all&sort=updated"
        payload = request_json(url, token)
        if not isinstance(payload, list) or not payload:
            break
        for item in payload:
            if not isinstance(item, dict):
                continue
            if not include_archived and item.get("archived"):
                continue
            if not include_forks and item.get("fork"):
                continue
            repos.append(item)
        page += 1
    return repos


def text_score(text: str, patterns: list[re.Pattern[str]]) -> int:
    return sum(1 for pattern in patterns if pattern.search(text))


def classify_repo(repo: dict[str, Any], patterns: list[re.Pattern[str]]) -> dict[str, Any]:
    name = str(repo.get("name", ""))
    full_name = str(repo.get("full_name", ""))
    desc = str(repo.get("description") or "")
    topics = repo.get("topics") or []
    joined_topics = " ".join(str(t) for t in topics)
    haystack = " ".join([name, full_name, desc, joined_topics]).lower()
    score = text_score(haystack, patterns)
    related = score > 0
    confidence = "high" if score >= 2 else ("medium" if score == 1 else "none")
    return {
        "full_name": full_name,
        "html_url": repo.get("html_url"),
        "default_branch": repo.get("default_branch"),
        "updated_at": repo.get("updated_at"),
        "archived": bool(repo.get("archived", False)),
        "fork": bool(repo.get("fork", False)),
        "topics": topics,
        "related": related,
        "confidence": confidence,
        "score": score,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        default=str(ROOT / "integrations" / "agent-registry" / "integration-inventory.yaml"),
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "integrations" / "agent-registry" / "discovered-repos.json"),
    )
    args = parser.parse_args()

    inventory = load_yaml(Path(args.inventory))
    discovery = inventory.get("discovery", {})
    owners = discovery.get("owners") or ["xh09411-web"]
    include_archived = bool(discovery.get("include_archived", False))
    include_forks = bool(discovery.get("include_forks", False))
    keywords = [str(k).strip().lower() for k in (discovery.get("keywords") or []) if str(k).strip()]
    if not keywords:
        keywords = ["agent", "skill", "plugin", "mcp", "acp"]
    patterns = [re.compile(re.escape(keyword), re.IGNORECASE) for keyword in keywords]

    token = os.environ.get("GITHUB_TOKEN")
    all_results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for owner in owners:
        owner = str(owner).strip()
        if not owner:
            continue
        try:
            repos = list_owner_repos(owner, token, include_archived, include_forks)
            for repo in repos:
                row = classify_repo(repo, patterns)
                row["owner"] = owner
                all_results.append(row)
        except urllib.error.HTTPError as exc:
            errors.append({"owner": owner, "error": f"http_{exc.code}"})
        except Exception as exc:  # pragma: no cover
            errors.append({"owner": owner, "error": type(exc).__name__})

    related = [r for r in all_results if r["related"]]
    payload = {
        "generated_at": utc_now(),
        "owners": owners,
        "keywords": keywords,
        "summary": {
            "total_scanned": len(all_results),
            "related_candidates": len(related),
            "errors": len(errors),
        },
        "errors": errors,
        "related_candidates": sorted(related, key=lambda x: (-x["score"], x["full_name"])),
        "all_scanned_repos": sorted(all_results, key=lambda x: x["full_name"]),
    }
    write_json(Path(args.output), payload)
    print(
        "Discovered repositories:",
        f"scanned={payload['summary']['total_scanned']}",
        f"related={payload['summary']['related_candidates']}",
        f"errors={payload['summary']['errors']}",
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
