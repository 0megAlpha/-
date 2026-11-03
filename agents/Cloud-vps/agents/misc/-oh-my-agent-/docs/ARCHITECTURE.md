# Oh My Agent
Execution plane: StateM-style deterministic state, registry, MCP/A2A boundaries, memory and policy gates.
Evolution plane: HyperAgents-style meta-planning, DGM candidate generation/evaluation, symbolic reflection and harness evaluation.
The upstream projects in the upstreams directory remain independently auditable; this repository does not copy their implementation into production.
Promotion is gated by compile, unit/regression, security and rollback checks. No autonomous production self-modification, persistence, credential harvesting or external exploitation.
