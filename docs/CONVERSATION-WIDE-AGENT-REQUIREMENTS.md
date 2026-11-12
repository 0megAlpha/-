# Conversation-wide Agent deployment requirements

Compiled: 2026-11-13
Sole GitHub destination: `https://github.com/0megAlpha/-`
Authenticated GitHub account: `0megAlpha`

This file consolidates the user's explicit instructions from the current and prior conversation context. It is a requirements record, not evidence that every integration is already installed.

## Absolute destination and repository rules

- Only use account `0megAlpha` and repository `0megAlpha/-` as the destination for this work.
- Do not restore pushes to the previous GitHub account or distribute Agent source to other repositories.
- Existing files in the target repository must be compared before creating anything. No duplicate Agent folder, no alternate "full", "workspace", "root", "backup" Agent folder without proven separate identity.
- Every distinct Agent has one canonical home. Shared Skills, Plugins, MCP servers, Tools, Functions and Workflows have one reusable source and are referenced by adapters.
- Portable source, manifests, install scripts, configuration templates, version pins, licenses, validation tests and deployment runbooks belong in the repository.
- Never publish live secrets, credentials, session state, databases, user-specific memory, logs containing sensitive data, runtime caches or binary model weights.
- Keep Git history; no force push, history rewrite, blind reset or mass replacement.
- Record exactly what was pushed and verify remote commit SHA and file content.

## User-defined meaning of deployment

"Deployment" means install and configure the capability so that the intended Agent can call it, not merely write a README, add a folder, or list a connector. A successful installation record must identify:
- Source repository and upstream version/commit
- License and dependency requirements
- Installation/configuration location
- Agent that owns the integration
- Required environment-variable names (never their values)
- Health/initialization result
- A successful representative invocation
- Test output or verifiable evidence
- Rollback method

## Primary architecture

OpenHands is the main software engineering Agent and the existing OpenHands runtime is the core. Do not deploy another OpenHands instance or another copy of the same Agent.

The target integrated architecture is:
- OpenHands: coding and execution core, existing Docker runtime/sandbox.
- Aider: multi-file editing capability integrated into the existing coding workflow.
- LangGraph: explicit stateful orchestration, checkpoints, retries and bounded loops.
- AutoGen v0.4 / Magentic-One: optional multi-agent coordination adapter where it adds non-duplicative capability.
- Dify: use the already deployed instance for visual workflow/model/tool orchestration, not a second Dify stack.
- Playwright: browser E2E, screenshot, console/network capture and regression verification.
- Puppeteer: optional only if a required use case is not covered by Playwright.
- SonarQube scanner, Biome and ESLint: quality/security gates appropriate to each codebase.
- Docker Runtime Sandbox: existing OpenHands sandbox boundary; do not grant unrestricted host access or expose Docker control unnecessarily.
- Coolify: API/deployment adapter only after existing service and credentials are verified.
- GitHub Actions: portable CI workflows, source validation, security scanning and release checks.
- MCP: central registry with per-Agent adapters and exact tool/resource contracts.
- Model routing: compatible providers including OpenRouter, LiteLLM, local llama.cpp and other OpenAI-compatible APIs; secrets remain outside Git.
- Skill Library: portable, versioned and testable skills, not unbounded self-modifying code.

## Reasoning and quality-loop requirements

The user requested whole-project scanning, deep planning, alternative evaluation, sandbox execution, error capture, correction and skill reuse. Implement this as bounded, auditable workflows:
1. Inventory source tree, manifests, dependency graph, tests and current Git state.
2. Plan and compare candidate implementations.
3. Execute in the existing isolated sandbox.
4. Run build, lint, static security scan, unit/integration tests and browser E2E as applicable.
5. Feed concrete error logs back into a bounded repair cycle.
6. Re-run all affected tests and inspect the diff.
7. Promote a reusable skill/tool only after reproducible tests and source/license review.

MCTS or reinforcement learning must not be claimed as present unless a real implementation, evaluation harness and measured evidence exist. Use bounded retry counts, timeouts and explicit stop conditions; never create infinite repair loops.

## User-requested integrations and connector inventory

The user asked to use all available, relevant integrations to help complete the work. The requested list includes:
- Vercel
- Gateway SSH
- Termalin
- Task Tool
- Hey Terminal
- Smart Model Router
- Shellway
- PR Completion
- Superpowers
- Exa
- Tavily
- Agent Skills
- Aeon
- Eggshell
- MCP Boundary
- Codex Dev Workflows
- Codex TestFlight Release
- Codex Browser Recorder
- Codex Engineering Guardrails
- Searcherries / AI SEO
- Simplified for AI
- Replit
- TinyFish
- Notion
- ButlerBrain
- Context7
- SentinelX
- Parallel
- Firecrawl
- MagicPath
- GitHub
- Lody / Conduit
- OpenHands Extensions and MCP tools

Availability in ChatGPT does not mean the service is installed on the VPS. Each must be tracked separately as connector-connected, authorized, VPS-installed, Agent-integrated, and runtime-validated. Use only integrations that actually apply to the Agent platform and current task.

## Prior source repositories and VPS projects to reconcile

The following were named or discovered in prior handovers. This is an investigation list, not a claim that each source is readable or already migrated:
- `Ai-agent-skill` / AI Agent Skills and prior pushes to other accounts
- `All-in`
- `CKA-Agent`
- `Claude-code` / AgentSys
- `hermes-007` / Hermes
- `openhands-extensions`
- `Google-AI` including nested OpenHands repositories
- `vps-mirror-workspace`
- `agent-os-portable`
- `ai-agent-fleet`
- `agent-plane`
- `sentinelx-cloud-core` and `sentinelx-python`
- `open-hands-integrated-main`
- `openhands-upstream-build-v1.25.0`
- `open-webui` and `openwebui-plugins`
- `llama.cpp`
- `dify`
- `agent-sandbox`, `hermes-sandbox`, `opencode-sandbox`, `dsh-sandbox`
- `agent-throne-file-center`
- `free-api`, `frp`, `eni-register`, `tsvps`, `omnibypass`
- Hermes user skills and OpenHands skill/plugin backups
- Root-owned and unknown Agent folders under `/root`, `/opt` and the mirror's `unknown/` tree

Historical source references include GitHub accounts/repositories under `xh09411-web`, public upstreams such as OpenHands, NousResearch and Graph-COM, and the current target `0megAlpha/-`. Previous account repositories must be read only through an authorized connection. Do not assume a 404 means the repository never existed.

## VPS operating constraints

- Keep all current services and existing connections intact unless an explicitly approved change is required.
- Do not stop, disable, restart, remove or overwrite existing production services as a side effect of scanning or integration.
- Do not create new listening ports or publish additional Docker ports. Existing mappings must be inventoried and attributed; no new mapping is allowed.
- Use the existing OpenHands/Dify/LiteLLM/Redis/PostgreSQL/Qdrant/Open WebUI infrastructure where appropriate rather than creating duplicate stacks.
- Scan all Agent-related directories, Git histories/remotes/branches, submodules, Docker containers/images/volumes, systemd units, listeners/processes, MCP configurations, model endpoints, dependency files and deployment records.
- De-duplicate by project identity and capability ownership, not just directory name.
- Preserve unique local changes and untracked source files; exclude credentials and runtime-only data.
- Only after source is safely portable, pushed, and verified twice may disposable caches, orphaned images or temporary build outputs be cleaned. Never delete source repositories, data volumes, active state or ambiguous material.

## Final 10-point acceptance checklist

1. Sole destination verified: `0megAlpha/-`.
2. One canonical directory per Agent; shared capabilities have one source.
3. Prior account pushes and VPS Agent assets reconciled against the target, with no silently omitted source.
4. OpenHands remains the single primary coding core; Aider, LangGraph/AutoGen, Dify, Playwright, quality/security tools and Coolify adapters integrated where compatible.
5. Skills, Plugins, Tools, Functions and MCP components installed and runtime-tested, not just documented.
6. All portable content sanitized and source/license/version metadata recorded.
7. No new ports or unintended production service changes.
8. Two complete verification passes, including remote SHA/content, dependency, security, Git status and runtime tests.
9. Verified backup first, then clean only confirmed disposable caches/temporary files/orphaned images.
10. Final VPS-to-GitHub reconciliation report with per-Agent path, source, commit/version, install location, test evidence, cleanup result and unresolved blockers.

## Current blocker snapshot (2026-11-13)

- GitHub authenticated user: `0megAlpha`; repository is writable.
- GitHub currently reports `0megAlpha/-` as Public, default branch `vps-mirror/full-tree`. Historical files saying Private or referring to other branches are stale.
- VPS SSH key authentication is verified. Gateway reports sudo `action_required`; root-owned paths and privileged inventory remain blocked until the Gateway sudo setup is completed.
- The host has 30 Docker containers from the latest inventory; existing OpenHands 0.47.0 and Dify 1.19.0 are running.
- Root filesystem is 90% used. The user-owned cache tree is about 7 GB; the mirror workspace is about 18 GB and `/opt/agents` about 14 GB. These include Git object packs and runtime artifacts; do not delete blindly.
- A non-privileged `ss -lntup` snapshot succeeded and shows many wildcard listeners, including listeners that do not appear in the container port list. The full process-to-listener attribution and firewall review still require privileged inventory.
- A large `/opt/vvvkey.log` (about 99.7 MB) and root-owned archive/log material require content and secret review before any removal or upload.
- Termalin reports its Pro trial ended; its remote server connector is unavailable on the current plan.
- Shellway reports the VPS device offline.
- SentinelX currently has no enrolled hosts.
- Vercel project listing returned 403 for the existing `xavideo777-9021` scope; reauthorization is required before project inventory.
- The latest non-privileged recursive size/Git/secret scans encountered root-owned permission errors. No cleanup, port changes, service restarts or privileged mutations were performed.

## Completion status

This requirements record and the related deployment reconciliation report are committed documentation. They do not constitute completion of the requested Agent migration, installation, package updates, port remediation or VPS cleanup. Only mark the acceptance checklist complete when backed by execution evidence.
