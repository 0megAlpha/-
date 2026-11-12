# VPS Runtime Service Snapshot — 2026-11-12

This is a read-only snapshot from the live host. No services were restarted, disabled, stopped, reconfigured, or removed. No ports were added.

## Containers

Observed running:
- exa-mcp — restarting
- mcp-proxy — running, published 5700
- open-webui — healthy, published 3000
- qdrant — running, loopback-only 6333–6334
- mimocode2api — healthy, published 8080
- openhands-canvas — running, published 8000
- coolify-db / coolify-redis — healthy
- Dify API / worker / websocket / plugin daemon / web / PostgreSQL / Redis / sandbox / Weaviate — most running; agent_backend and local_sandbox restarting
- OpenHands runtime and web — running; web published 13000
- agents stack: LiteLLM, PostgreSQL, Redis, Qdrant, Mem0, New API — running

## systemd

Running at inspection:
- agent-throne-file-center.service
- docker.service
- dsh-agent.service
- eni-freeapi-watchdog.service
- eni-harbor.service
- freeride-relay.service
- frps.service
- hermes-api.service
- hermes-gateway.service
- litellm.service
- lody-agent.service
- redis-server.service
- tailscaled.service
- termalin-agent.service

## Remediation queue (not executed)

- exa-mcp container restarting.
- Dify agent_backend container restarting.
- Dify local_sandbox container restarting.
- Root filesystem at 88% usage (38 GB available at scan).
- Existing exposed listeners were observed on several interfaces. They were not created or changed by this task. User explicitly prohibited opening ports; no port/firewall changes were made.
- Vercel connector returned no teams / linked Git projects.
- SentinelX connector returned no enrolled hosts; account plan Free with one available host slot.
- Termalin connector previously returned Free plan after Pro trial expiry; host listing is unavailable under current plan.
- Shellway reports one online Linux device named greencloud-ai.

## Migration and credential hygiene status

- A repository inventory was committed to `0megAlpha/-` at `docs/vps-migration/VPS-AGENT-MCP-INVENTORY-2026-11-12.md` on branch `vps-mirror/full-tree`.
- That repository is currently Public.
- A full multi-project Gitleaks scan was attempted but timed out (exit 143); therefore no claim of a clean secret scan can be made.
- Exact local `.env` files exist in `/home/xiaye/All-in`, `/opt/agents/-`, `/opt/ai-stack`, and `/opt/dify/docker`. Their contents were not read or uploaded.
- Further content-level secret scanning and repository-by-repository migration are still required.
- No project source code was broadly staged or pushed in this pass; dirty worktrees, staged deletions, broken Git metadata, nested repositories, root-owned files and low disk headroom must be reconciled individually first.


## Agent OS portable deployment — 2026-11-12 09:xx Asia/Taipei

- PR #4 was squash-merged into this repository's default branch.
- Merge commit: 05e72a7e327f35add8b4fd9735d3ff302a66de51.
- Portable package path: agent-os-portable/.
- Local validation: pytest 3 passed; Ruff check passed; Ruff format check passed (18 files).
- OpenHands health: existing loopback endpoint 127.0.0.1:13000 returned OK.
- LiteLLM liveliness probe at 127.0.0.1:14000 returned TCP connection reset; no config or service change made.
- No new inbound port, published Docker port, NAT or firewall rule was created.

## Updated host findings — 2026-11-12

- Root filesystem: 310 GB total, 275 GB used, 35 GB free (89%).
- Confirmed local Git repositories include home projects Ai-agent-skill, All-in, CKA-Agent, Claude-code, hermes-007, openhands-extensions, repository/Google-AI, vps-mirror-workspace; system projects agent-plane, agents/-, ai-stack, dify, llama.cpp, openhands-upstream-build-v1.25.0, and /usr/local/lib/hermes-agent.
- Important project sizes: /opt/agents ~14 GB; /home/xiaye/ai-agent-fleet ~1.1 GB; /home/xiaye/hermes-007 ~2.6 GB; /home/xiaye/CKA-Agent ~4.9 GB; /home/xiaye/vps-mirror-workspace ~18 GB.
- Containers restarting: exa-mcp, Dify agent_backend, Dify local_sandbox.
- systemd auto-restart/activating: ai-agent-throne, llama-agent, llama-agent-fast, sentinelx-cloud-core.
- Existing listeners were enumerated; no port changes were performed.
- Shellway latest check reported greencloud-ai offline.
- Lody CLI is installed but not authenticated; device authorization command has been started and awaits browser approval. No credential is written to this repository.

## Migration status (not complete)

- Full project migration is still pending. Dirty worktrees, root-owned files, invalid Git metadata, nested repositories, submodules, old/unavailable remotes and Gitleaks findings remain to be reconciled project by project.
- The /home/xiaye umbrella Git directory has no commits and contains personal home/configuration material; do not push it wholesale.
- Known local .env paths and unclassified secret findings remain excluded from Git until sanitized.
- No old GitHub account was restored or accessed. The only destination remains 0megAlpha/-.
- Current GitHub repository visibility is Public.


## Agent stack repair completed — 2026-11-12 09:43 Asia/Taipei

- LiteLLM bind mount corrected through a Compose overlay. Existing port 14000:4000 retained.
- LiteLLM container recreated only; running with restart count 0. Authenticated model catalog returned 11 aliases. Health/liveliness and readiness both HTTP 200.
- Dify agent_backend and local_sandbox received a generated 256-bit shared runtime auth token through a local-only mode-0600 env file outside Git. Only these two services were recreated; backend is running and local_sandbox is healthy.
- OpenHands /health returned OK.
- No new listener, published port, NAT, firewall or reverse-proxy rule was created.
- LiteLLM logs still report one invalid model alias missing provider prefix; other 11 aliases loaded. Real inference test remains pending.
- Exa MCP and several systemd agents remain in remediation queue.
