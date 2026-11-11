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
