#!/usr/bin/env python3
"""Small, deterministic evidence helper for the EMAT Agent Court workflow."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: str, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_bytes(value)
    with target.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def seal(args: argparse.Namespace) -> int:
    plan = load_json(args.plan)
    required = ("objective", "baseline_revision", "acceptance_criteria", "allowed_paths", "forbidden_paths", "test_commands")
    missing = [key for key in required if key not in plan]
    if missing:
        raise ValueError("plan missing required keys: " + ", ".join(missing))
    if not isinstance(plan["test_commands"], list) or not plan["test_commands"]:
        raise ValueError("test_commands must be a non-empty list of argv arrays")
    for command in plan["test_commands"]:
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            raise ValueError("each test command must be a non-empty argv array of strings")
    envelope = {"schema": "emat.sealed-plan.v1", "plan": plan, "plan_sha256": sha256_bytes(canonical_bytes(plan))}
    write_json(args.out, envelope)
    print(envelope["plan_sha256"])
    return 0


def check_seal(envelope: dict[str, Any]) -> tuple[bool, str]:
    if envelope.get("schema") != "emat.sealed-plan.v1" or not isinstance(envelope.get("plan"), dict):
        return False, "invalid sealed-plan schema"
    actual = sha256_bytes(canonical_bytes(envelope["plan"]))
    return actual == envelope.get("plan_sha256"), actual


def judge(args: argparse.Namespace) -> int:
    envelope = load_json(args.seal)
    valid, digest = check_seal(envelope)
    if not valid:
        status, reasons = "INCONCLUSIVE", ["sealed plan hash/schema invalid"]
    else:
        breaker = load_json(args.breaker)
        builder = load_json(args.builder)
        tests = load_json(args.tests)
        reasons: list[str] = []
        if not builder.get("candidate_commit"):
            reasons.append("builder evidence has no candidate_commit")
        counterexamples = breaker.get("counterexamples")
        if not isinstance(counterexamples, list):
            reasons.append("breaker counterexamples missing or invalid")
        unresolved = [item for item in (counterexamples or []) if item.get("status") != "addressed"]
        test_results = tests.get("results")
        if not isinstance(test_results, list) or not test_results:
            reasons.append("independent test results missing")
        elif any(item.get("exit_code") != 0 for item in test_results):
            reasons.append("one or more independent tests failed")
        if unresolved:
            reasons.append(f"{len(unresolved)} Breaker counterexample(s) unresolved")
        if any("failed" in reason or "unresolved" in reason for reason in reasons):
            status = "FAIL"
        elif reasons:
            status = "INCONCLUSIVE"
        else:
            status = "PASS"
    ledger = Path(args.ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    previous = "0" * 64
    if ledger.exists():
        lines = [line for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            previous = json.loads(lines[-1])["record_sha256"]
    record = {
        "schema": "emat.verdict.v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "plan_sha256": envelope.get("plan_sha256"),
        "candidate_commit": load_json(args.builder).get("candidate_commit") if valid else None,
        "reasons": reasons,
        "previous_record_sha256": previous,
    }
    record["record_sha256"] = sha256_bytes(canonical_bytes(record))
    with ledger.open("a", encoding="utf-8") as stream:
        stream.write(canonical_bytes(record).decode())
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


def verify_ledger(args: argparse.Namespace) -> int:
    path = Path(args.ledger)
    previous = "0" * 64
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        supplied = record.pop("record_sha256", None)
        if record.get("previous_record_sha256") != previous:
            raise ValueError(f"ledger chain broken at line {number}")
        actual = sha256_bytes(canonical_bytes(record))
        if supplied != actual:
            raise ValueError(f"ledger hash mismatch at line {number}")
        previous = supplied
    print(f"OK: ledger verified; last hash {previous}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)
    seal_parser = sub.add_parser("seal")
    seal_parser.add_argument("--plan", required=True)
    seal_parser.add_argument("--out", required=True)
    seal_parser.set_defaults(func=seal)
    judge_parser = sub.add_parser("judge")
    for name in ("seal", "breaker", "builder", "tests", "ledger"):
        judge_parser.add_argument("--" + name, required=True)
    judge_parser.set_defaults(func=judge)
    ledger_parser = sub.add_parser("verify-ledger")
    ledger_parser.add_argument("--ledger", required=True)
    ledger_parser.set_defaults(func=verify_ledger)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"emat: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
