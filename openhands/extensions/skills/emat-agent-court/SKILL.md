---
name: emat-agent-court
description: Run a three-role Breaker/Builder/Magistrate engineering loop with sealed plans, adversarial tests, independent verification, and append-only verdict evidence.
---

# EMAT Agent Court

Use this workflow for non-trivial code changes, migrations, bug fixes, security hardening, and agent self-improvement tasks. It is an OpenHands capability, not a shared generic skill.

## Roles

- **Breaker**: works from the sealed requirements and current baseline. Produces counterexamples, edge cases, threat cases, and regression tests. It must not edit Builder implementation files after the Builder starts.
- **Builder**: receives the sealed plan and Breaker findings; implements the smallest complete fix in its own branch/worktree. It cannot edit the sealed plan, Breaker evidence, or Magistrate verdicts.
- **Magistrate**: operates from a fresh checkout of the candidate commit. It independently runs the sealed test commands, checks coverage of Breaker counterexamples, reviews the diff and policy constraints, and records PASS, FAIL, or INCONCLUSIVE. It does not implement fixes.

## Mandatory sequence

1. Write a versioned plan containing objective, acceptance criteria, allowed paths, forbidden paths, baseline revision, test commands (argv arrays, not shell strings), timeout, and rollback point.
2. Seal the plan with `scripts/emat.py seal`. Never edit a sealed plan; create a new version and seal it again when requirements change.
3. Breaker creates `breaker.json` with named counterexamples and test references. Store it outside Builder's writable tree or make it read-only.
4. Builder implements on a separate branch/worktree and emits `builder.json` containing candidate commit, changed paths, and summary.
5. Magistrate checks out the exact candidate in a clean worktree, executes each sealed test command, and writes `tests.json` with exit codes and captured evidence.
6. Magistrate runs `scripts/emat.py judge`. PASS requires a valid sealed plan, a candidate commit, all required tests passing, and zero unresolved Breaker counterexamples. Missing or inconsistent evidence is INCONCLUSIVE; a failing test or unresolved counterexample is FAIL.
7. Append verdicts to `verdicts.jsonl`; never rewrite prior verdicts. Each record links to the previous record hash.
8. Only a PASS can be proposed for merge. The workflow must still run the repository's normal CI and human-required deployment gates. No role may directly overwrite production or auto-deploy.

## Evidence contract

- `plan.json`: immutable source plan.
- `sealed-plan.json`: canonical plan plus SHA-256.
- `breaker.json`: counterexamples and test references.
- `builder.json`: candidate commit and changed paths.
- `tests.json`: independently executed test results.
- `verdicts.jsonl`: append-only hash-chained Magistrate records.

Example commands:

```bash
python3 scripts/emat.py seal --plan plan.json --out evidence/sealed-plan.json
python3 scripts/emat.py judge \
  --seal evidence/sealed-plan.json \
  --breaker evidence/breaker.json \
  --builder evidence/builder.json \
  --tests evidence/tests.json \
  --ledger evidence/verdicts.jsonl
python3 scripts/emat.py verify-ledger --ledger evidence/verdicts.jsonl
```

Do not mark work complete from a Builder's self-report. A PASS is a test-backed verdict for the exact candidate commit and sealed plan only.
