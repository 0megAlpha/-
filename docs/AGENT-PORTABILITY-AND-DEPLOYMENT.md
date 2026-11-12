# Agent Portability, Deployment and VPS Reconciliation

Last inspected: 2026-11-12
Target repository: `0megAlpha/-`
Target branch: `vps-mirror/full-tree`

## User's acceptance requirements

1. This repository under GitHub account `0megAlpha` is the sole destination for portable Agent source, skills, plugins, tools, MCP servers, functions, workflows, manifests and deployment documentation.
2. Each distinct Agent has exactly one canonical directory. Do not create another folder for an Agent that already has a canonical location. Before consolidation, compare source identity, Git history, versions, manifests, checksums, licenses and local changes.
3. Preserve all useful portable material from VPS directories, prior GitHub pushes and previously used repositories. Do not assume a prior push means the current repository contains the same files.
4. Treat OpenHands as the primary software-engineering Agent. Integrate shared capabilities through a single reusable registry and per-Agent adapters; do not deploy a second OpenHands core.
5. Install means configure and make usable on the existing VPS deployment, not merely copy documentation or create folders in GitHub.
6. Do not publish credentials, tokens, cookies, private keys, .env files, database dumps, runtime sessions, private model weights, user memory stores, sensitive logs or infrastructure secrets. Use placeholders and document variable names only.
7. Do not open or add listening ports. Preserve existing service configuration unless a separately reviewed change is explicitly approved. Prefer loopback-only or internal container networking for future integrations.
8. Update upstream packages and source only after recording current version, source URL, license, local modifications, dependency compatibility, backup and rollback path.
9. Verify each integration twice: (a) source/manifest/dependency/security validation; (b) runtime invocation, health check or MCP initialize/list_tools test. Mark unavailable or unverified capabilities honestly.
10. After a verified portable backup and two successful checks, remove only confirmed disposable caches, temporary build artifacts and orphaned images. Never delete source, data volumes, active runtime state or ambiguous files.
11. At completion, reconcile VPS and GitHub manifests, verify the target branch head and clean Git status, then produce a per-Agent install and validation report.

## Canonical ownership model

- `openhands/`: OpenHands core, runtime configuration, extensions and OpenHands-specific adapters.
- `hermes/`: Hermes Agent source and Hermes-specific adapters.
- `agents/<agent-id>/`: one directory for each distinct standalone Agent not already represented by a top-level canonical directory.
- `agents/Ai-agent-skill/`: shared, framework-neutral skills, plugins, MCP adapters, reusable tools, workflows and capability manifests. This is a shared capability library, not a second Agent runtime.
- Other existing top-level Agent directories (for example `aider/`, `claude-code/`, `cline/`, `continue/`, `crush/`, `deepseek/`, `devin/`, `goose/`, `opencode/`, `openwebui/`, `swe-agent/`) remain canonical unless source inspection proves they are duplicates.
- A per-Agent adapter may reference shared capability IDs; it must not vendor a second copy of the same source.

## Capability integration targets

| Capability | Intended integration | Verification required |
|---|---|---|
| OpenHands Runtime / Docker sandbox | Existing OpenHands core | Runtime health, sandbox create/execute, no new host listener |
| Aider | OpenHands coding adapter / shared tool registry | Multi-file edit and test in isolated workspace |
| LangGraph | Workflow orchestration layer | State persistence, retries, checkpoint and bounded loop |
| AutoGen / Magentic-One | Optional multi-agent orchestration adapter | Agent handoff, termination and trace |
| Dify | Existing workflow UI and model/tool integration | Workflow run and API/tool invocation |
| Playwright | Browser QA tool | Browser launch, navigation, assertion, screenshot and console capture |
| Puppeteer | Optional browser adapter only if non-overlapping | Smoke test and explicit reason not to use Playwright alone |
| SonarQube scanner | Quality/security gate | Scanner run and report; do not invent a 95% score |
| Biome / ESLint | Language-specific lint adapters | Lint on representative projects |
| GitHub API / Actions | Repository and CI integration | Least-privilege access, workflow run and artifact verification |
| Coolify API | Deployment adapter only | API auth and dry-run/target inspection; do not publish ports |
| MCP servers | Shared MCP registry plus adapters | initialize, list_tools, invoke one safe read-only tool |
| Exa / Tavily / Firecrawl / Parallel | Research adapters | Auth state, minimal query and source output |
| Context7 | Documentation lookup adapter | Resolve library and retrieve docs |
| Notion / ButlerBrain | Knowledge capture adapters | Read/write test in designated workspace |
| Vercel | Existing account/team integration | Correct team authorization, project listing and repository binding |
| Shellway / Gateway / Termalin / SentinelX | Host operations connectors, not duplicate Agents | Connection status and bounded read-only inventory |

Do not claim that a capability is installed because its connector is available in ChatGPT. Connector availability and VPS installation are separate states.

## Current VPS evidence (2026-11-12)

- Host OS capability probe: Ubuntu 26.04, systemd, Docker 29.1.3, Compose v5.6.0, Podman 5.7.0.
- Existing Docker inventory: 30 containers returned. Existing OpenHands 0.47.0 and Runtime 0.47.0 are running. Existing Dify 1.19.0 components, LiteLLM, Open WebUI, Qdrant, PostgreSQL and Redis services are present.
- Existing Compose/container port mappings were observed. No new listener or port mapping was created by this reconciliation.
- Root filesystem usage reported 90%; approximately 296.7 GB used of 332.1 GB. Inode usage reported 18%.
- A large log file was observed under `/opt`; it must be attributed to its owning process, checked for secrets and active writes, and backed up/rotated before any truncation or deletion.
- `/home/xiaye/vps-mirror-workspace` has fetch and push remotes that both point to `0megAlpha/-`. Git status cannot be completed under the current SSH user because parts of the mirror are root-owned.
- Several directories under `/home/xiaye` and `/opt` are root-owned or contain unreadable paths. Full recursive size and Git scans therefore remain incomplete.
- Gateway reports the managed SSH key as verified, but sudo access is still `action_required`; the server capability probe reports password/policy-required privilege escalation. No sudo command was retried after that state.
- A bounded network-listener operation returned an invalid structured result. The Docker container inventory exposes published port mappings, but it is not a complete host socket/process listener report.
- Termalin host access is unavailable because its Pro trial ended. Shellway reports the VPS device offline. SentinelX has no enrolled hosts.
- Vercel project listing returned 403 for scope `xavideo777-9021`; that scope needs reauthorization before project inventory can be completed.
- GitHub authenticated identity is `0megAlpha`; target repository is writable by the current connection. GitHub metadata reports repository visibility as Public and default branch as `vps-mirror/full-tree`. Older repository documents incorrectly describe it as Private and refer to another branch; these must be reconciled before publishing sensitive operational detail.

## Duplicate-folder warning

The target repository currently contains several overlapping skill-library candidates:
`agents/AI-Agent-Skill`, `agents/AI-Agent-Skill-full`, `agents/Ai-Agent-Skill-workspace`, `agents/Ai-agent-skill`, `agents/agent-skills`, `agents/skills` and `agents/public-skills`.
It also contains multiple OpenHands snapshots under `openhands/`. Their names alone do not prove they are duplicates. Do not create more skill-library folders or remove existing ones until full file-tree, Git history, source remote, license and content comparisons are completed.

## Blockers and next actions

1. Complete Gateway sudo authorization through the Gateway server page, then repeat read-only root inventory and permission-aware Git status. Never send passwords or tokens in chat.
2. Re-run network listener/process inventory and disk attribution with privilege; identify every published port, owning container/process, service dependency and firewall exposure. Do not change or open ports.
3. Compare all root-owned VPS Agent trees and prior-account repositories against this target branch. Retrieve private source only through an authorized connected GitHub account or connector.
4. Resolve the skill-library duplicates and OpenHands snapshots by evidence; create a canonical manifest and keep one copy of each capability.
5. Perform staged updates in isolated worktrees/containers, test compatibility, and deploy to the existing Agent integration points without starting duplicate cores.
6. Reconcile Vercel authorization and connector status. Do not treat an app connector as a VPS-installed plugin.
7. Back up before cleanup. Clean only attributable caches, orphaned images and temporary build output after verifying no active dependency.
8. Run the two validation passes and update this report with exact versions, commit SHAs, tests and remaining exceptions.

## Status vocabulary

- `inventoried`: path or service was observed.
- `source-reviewed`: source, license, version and local diff were reviewed.
- `portable`: credentials and runtime-only data were removed; clean checkout is reproducible.
- `installed`: configured in the intended runtime.
- `validated`: both source and runtime checks passed.
- `blocked`: access, permissions, authorization or compatibility prevented completion.

Never promote a row to a later status without evidence.
