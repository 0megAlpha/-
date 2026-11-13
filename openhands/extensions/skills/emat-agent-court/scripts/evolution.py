#!/usr/bin/env python3
"""Evidence-gated helpers for bounded EMAT branch and topology evolution."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_INVARIANTS = {"magistrate_read_only", "sealed_plan", "no_auto_deploy"}
_FORBIDDEN_PERMISSIONS = {"write_production", "deploy", "merge", "force_push", "admin"}


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value.lower()))


def rank_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank sealed candidate branches; eligibility requires complete independent evidence."""
    ranked: list[dict[str, Any]] = []
    for item in candidates:
        tests_total = item.get("tests_total", 0)
        tests_passed = item.get("tests_passed", 0)
        risk = item.get("risk_score", 1.0)
        complexity = item.get("complexity", 1.0)
        breaker_resolved = item.get("breaker_resolved") is True
        numeric = (
            isinstance(tests_total, int) and not isinstance(tests_total, bool) and tests_total > 0
            and isinstance(tests_passed, int) and not isinstance(tests_passed, bool)
            and 0 <= tests_passed <= tests_total
            and isinstance(risk, (int, float)) and not isinstance(risk, bool) and 0 <= risk <= 1
            and isinstance(complexity, (int, float)) and not isinstance(complexity, bool) and 0 <= complexity <= 1
        )
        complete = numeric and tests_passed == tests_total and breaker_resolved and _valid_hash(item.get("evidence_sha256"))
        pass_rate = tests_passed / tests_total if numeric else 0.0
        score = round(60 * pass_rate + 25 * int(breaker_resolved) + 10 * (1 - risk if numeric else 0) + 5 * (1 - complexity if numeric else 0), 2)
        ranked.append({
            "id": str(item.get("id", "")),
            "eligible": bool(complete),
            "score": score,
            "tests_passed": tests_passed if numeric else 0,
            "tests_total": tests_total if numeric else 0,
            "breaker_resolved": breaker_resolved,
            "evidence_sha256": item.get("evidence_sha256") if _valid_hash(item.get("evidence_sha256")) else None,
        })
    return sorted(ranked, key=lambda x: (x["eligible"], x["score"], x["id"]), reverse=True)


def validate_topology(topology: list[dict[str, Any]], max_agents: int = 8) -> dict[str, Any]:
    """Validate a proposed agent graph without applying or mutating a live topology."""
    errors: list[str] = []
    if not isinstance(topology, list) or not topology:
        return {"valid": False, "errors": ["topology must be a non-empty list"], "status": "proposal_only"}
    if len(topology) > max_agents:
        errors.append(f"topology exceeds max_agents={max_agents}")
    ids = [x.get("id") for x in topology if isinstance(x, dict)]
    if len(ids) != len(topology) or any(not isinstance(x, str) or not x for x in ids):
        errors.append("every agent must have a non-empty string id")
    if len(set(ids)) != len(ids):
        errors.append("agent ids must be unique")
    roles = [x.get("role") for x in topology if isinstance(x, dict)]
    for role in ("breaker", "builder", "magistrate"):
        if roles.count(role) != 1:
            errors.append(f"topology must contain exactly one {role}")
    for agent in topology:
        if not isinstance(agent, dict):
            continue
        agent_id = str(agent.get("id", "<unknown>"))
        permissions = set(agent.get("permissions", []))
        if agent.get("sandboxed") is not True:
            errors.append(f"{agent_id} must be sandboxed")
        if permissions & _FORBIDDEN_PERMISSIONS:
            errors.append(f"{agent_id} has forbidden permissions: {sorted(permissions & _FORBIDDEN_PERMISSIONS)}")
        if agent.get("role") in {"breaker", "magistrate"} and permissions & {"write", "write_branch", "write_workspace"}:
            errors.append(f"{agent_id} ({agent.get('role')}) must be read-only")
    return {"valid": not errors, "errors": errors, "status": "proposal_only"}


def feedback_decision(attempt: int, max_attempts: int, passed: bool) -> str:
    """Return a bounded next action; never produce an unbounded retry."""
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or not 1 <= max_attempts <= 10:
        raise ValueError("max_attempts must be an integer between 1 and 10")
    if not isinstance(attempt, int) or isinstance(attempt, bool) or not 1 <= attempt <= max_attempts:
        raise ValueError("attempt must be between 1 and max_attempts")
    if passed:
        return "complete"
    return "repair" if attempt < max_attempts else "escalate"


def validate_law_proposal(current: dict[str, Any], proposed: dict[str, Any]) -> dict[str, Any]:
    """Validate a new law version; changes are proposals and never auto-applied."""
    errors: list[str] = []
    old_version, new_version = current.get("version"), proposed.get("version")
    if not isinstance(old_version, int) or not isinstance(new_version, int) or new_version != old_version + 1:
        errors.append("law version must increment by exactly one")
    old_rules = set(current.get("invariants", []))
    new_rules = set(proposed.get("invariants", []))
    missing = _REQUIRED_INVARIANTS - new_rules
    removed = old_rules - new_rules
    if missing:
        errors.append(f"required invariants missing: {sorted(missing)}")
    if removed:
        errors.append(f"existing invariants cannot be removed: {sorted(removed)}")
    if not _valid_hash(proposed.get("evidence_sha256")):
        errors.append("law proposal requires a valid evidence_sha256")
    return {"valid": not errors, "errors": errors, "status": "proposal_only", "apply": False}


def _read(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: str, data: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("rank-candidates", "validate-topology", "validate-law-proposal"):
        p = sub.add_parser(name)
        p.add_argument("--input", required=True)
        p.add_argument("--output")
    feedback = sub.add_parser("feedback-decision")
    feedback.add_argument("--attempt", type=int, required=True)
    feedback.add_argument("--max-attempts", type=int, default=3)
    feedback.add_argument("--passed", action="store_true")
    args = parser.parse_args()

    if args.command == "feedback-decision":
        print(json.dumps({"decision": feedback_decision(args.attempt, args.max_attempts, args.passed)}))
        return 0
    data = _read(args.input)
    if args.command == "rank-candidates":
        result = rank_candidates(data)
    elif args.command == "validate-topology":
        result = validate_topology(data)
    else:
        result = validate_law_proposal(data["current"], data["proposed"])
    if args.output:
        _write(args.output, result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if (result.get("valid", True) if isinstance(result, dict) else True) else 2


if __name__ == "__main__":
    raise SystemExit(main())
