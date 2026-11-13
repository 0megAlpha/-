# Agent catalog classification and duplicate deployment policy

This inventory distinguishes LLM agent runtimes from orchestration platforms, workflow engines, skill libraries and security tools. A directory is not treated as a separately deployable Agent merely because its name contains "agent".

## Canonical provider-enabled runtimes

- OpenHands — primary platform and runtime.
- Codex, Claude Code, Devin, Hermes, DSH, Aider, Cline, Goose, OpenCode, DeepSeek, Open WebUI.
- mini-SWE-agent, SWE-agent, DGM, HyperAgents, FuzzingBrain / DARPA-AIxCC, Agent System.
- Oh My Agent — existing multi-provider ProviderMatrix.

Each runtime keeps its provider adapter and project-specific skills inside its own Agent directory. The shared directory contains only cross-Agent contracts, not all Agent-specific plugins.

## Orchestration bundles and platforms

- All-in — multi-agent orchestration bundle; child Agents keep their own provider adapters.
- Dify — orchestration platform, runtime health verified.
- agent-plane and ai-agent-fleet — platform/fleet orchestration, not standalone inference Agents.

## Non-LLM modules

- StateM — workflow orchestration engine; no standalone provider adapter required.
- XAttacker — security testing tool; no standalone provider adapter required.
- CKA-Agent — Kubernetes/security research project; retain its own model/config boundary rather than forcing a generic runtime template.

## Duplicate and historical snapshot policy

| Canonical path | Retained path | Relationship | Deployment rule |
|---|---|---|---|
| agents/oh-my-agent | agents/-oh-my-agent- | Only source marker differs | Deploy canonical only |
| agents/DARPA-AIxCC | agents/-DARPA-AIxCC- | Only source marker differs | Deploy canonical only |
| agents/DARPA-AIxCC | agents/afc-crs and agents/afc-crs-all-you-need-is-a-fuzzing-brain | Divergent historical forks; security/docs/SesM/venv differ | Retain for review; do not deploy in parallel |
| agents/All-in | agents/All-in-root | Divergent Compose/dashboard and additional security/deploy docs | Canonical All-in only; merge unique files by review |

No duplicate directories were deleted. The historical snapshots are retained until their unique files are merged and verified individually.
