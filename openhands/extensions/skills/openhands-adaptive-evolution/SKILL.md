---
name: openhands-adaptive-evolution
description: Orchestrate evidence-gated multi-branch planning, EMAT adjudication, bounded error correction, skill hardening, and agent-topology evolution inside OpenHands.
---

# OpenHands Adaptive Evolution Engine

Use this skill when a task requires more than a single-pass implementation: architecture choices, complex debugging, multi-agent collaboration, repository migrations, reusable skill creation, or improving the agent workflow itself.

This skill composes the installed `emat-agent-court`, `harness-evolution`, `sesm-engine`, `agent-memory`, `agent-creator`, `skill-optimizer`, `qa-changes`, `code-review`, `security`, and `plan-once-verify-always` skills. Do not duplicate their responsibilities.

## 1. Full-context scan

Before choosing a design:
1. Inventory the repository, tracked/untracked files, branches, remotes, submodules, LFS and build manifests.
2. Map runtime boundaries: Docker Compose, systemd, listeners, reverse proxies, databases, MCP servers, model providers and environment variables (names only; never values).
3. Build a dependency map from entry points, imports, package manifests, Compose links and systemd dependencies.
4. Read the relevant AGENTS.md, skills, prior evidence and test commands.
5. Record unknowns as unknowns. Never infer a service or feature is installed merely because a README mentions it.

## 2. Multi-branch planning (Tree Search)

For a difficult task, generate at least three materially different candidate plans. Each candidate must contain:
- intended outcome and changed paths;
- dependencies and model/provider assumptions;
- test commands as argv arrays;
- failure modes and rollback point;
- security and production-impact assessment.

Run the cheapest discriminating tests first. Eliminate a candidate when its assumptions fail. Do not reveal private chain-of-thought; provide concise decision summaries, evidence, trade-offs and the selected plan.

When branch evidence is available, use:
`python3 <emat-agent-court>/scripts/evolution.py rank-candidates --input candidates.json`
Only candidates with all required tests passing, resolved Breaker counterexamples and a valid SHA-256 evidence hash are eligible.

## 3. EMAT court

Use `emat-agent-court` for the independent roles:
- Breaker: adversarial tests and counterexamples; read-only against Builder changes.
- Builder: implementation in its own branch/worktree.
- Magistrate: independent clean-checkout verification; read-only and no implementation.
- Keep the plan sealed, evidence hash-linked and verdict ledger append-only.

A Builder's self-report is never proof. A Magistrate PASS applies only to the exact candidate commit and sealed plan.

## 4. Bounded error-feedback loop

Use the following cycle:
1. Run the sealed tests and capture stdout/stderr, exit codes and elapsed time.
2. If a test fails, classify the error, map it to a changed path and ask Builder to produce one minimal repair.
3. Run the same focused test plus relevant regression tests.
4. Use `feedback-decision --attempt N --max-attempts 3` to determine whether to repair, complete or escalate.
5. After three unsuccessful attempts, stop the loop and produce an escalation report. Never run an infinite repair loop.

## 5. Self-evolving laws

The Magistrate may propose new rules or revisions based on repeated evidence. It must not silently change active rules.

- Store law versions as YAML with monotonically increasing versions.
- Preserve immutable invariants: `magistrate_read_only`, `sealed_plan`, `no_auto_deploy`, `no_force_push`, and explicit approval for production changes.
- Validate proposals with `validate-law-proposal`; attach a SHA-256 evidence hash.
- New laws remain proposals until independently reviewed and explicitly approved.
- Never lower a test gate merely to make a candidate pass.

## 6. Agent topology mutation

When the current team cannot solve a task, propose a new role or topology rather than mutating the running team:
1. State the bottleneck and evidence.
2. Propose the smallest topology change (e.g. memory specialist, performance reviewer, independent security reviewer).
3. Define each agent's role, sandbox, readable/writable paths and tools.
4. Validate with `validate-topology`.
5. Keep Breaker and Magistrate read-only; only Builder may write to its branch.
6. Run a sandbox tournament and compare its evidence against the baseline.
7. Record the proposed topology and result. Never hot-reload production topology automatically.

## 7. Skill hardening and durable learning

When discovering a reusable capability:
1. Research its official documentation and pin the source/version.
2. Create a new skill in a project-local `.openhands/skills/<skill-name>/` directory or the canonical OpenHands extension directory, according to repository ownership.
3. Include explicit inputs, outputs, prerequisites, failure modes and rollback.
4. Add unit/integration tests and a runnable example.
5. Run tests in the isolated workspace; compute SHA-256 hashes for the skill files and evidence.
6. Record the source, version, tests and hash in a manifest.
7. Use `skill-optimizer` to improve only from observed failures.
8. Keep the original skill until the replacement passes independent review.
9. Never write a project-specific plugin into a global shared skills repository. Store it with the owning Agent or project; shared libraries contain only truly cross-Agent contracts.

## 8. Output contract

Every run ends with:
- Baseline and scope scanned;
- Candidate plans considered and selected plan;
- Roles and topology used;
- Changed paths and candidate commit;
- Tests, exact exit codes and evidence hashes;
- Breaker counterexamples resolved/unresolved;
- Magistrate verdict;
- Law/topology/skill proposals (if any);
- Rollback point and remaining blockers.

No result is called complete until the candidate is independently verified and the repository's normal CI/deployment gates pass.
