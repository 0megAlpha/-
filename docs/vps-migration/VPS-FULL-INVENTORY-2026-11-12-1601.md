# VPS full-scope inventory — 2026-11-12 16:01 Asia/Taipei

## Scope and safety
- Canonical destination: `0megAlpha/-`, branch `vps-mirror/full-tree`. No old GitHub account was accessed or restored.
- VPS: Gateway server `agent-vps` / hostname `greencloud-ai`, Ubuntu 26.04, SSH user `xiaye`.
- This snapshot is read-only. No listener, firewall, NAT, reverse proxy, service, container, volume, or repository was changed by this inventory.
- No new port was opened.
- Proactive Gateway file scanning is disabled by account preference (0/5 scans used); therefore no special file-scanner scan was started. This does not certify the contents of unreviewed files.

## GitHub destination verification
- Authenticated GitHub account: `0megAlpha`.
- Repository: `0megAlpha/-`; admin/push permission confirmed.
- Default branch: `vps-mirror/full-tree`.
- Visibility: **PUBLIC** (not private).
- Repository reported size: 2,080,313 KB (GitHub repository size field).
- Latest observed commit at snapshot time: `b455915cec9a2c145402155ab36f36df0ae1e347` — `fix(agent-stack): repair LiteLLM and Dify runtime integrations`.
- PR #4 merged; merge commit `05e72a7e327f35add8b4fd9735d3ff302a66de51`.
- Portable Agent OS and prior migration queue are already in this repository. This file records the new host-side snapshot; it is not a claim that all legacy repositories have been migrated.

## Host health
- Root filesystem: 310G total, 276G used, 34G free, 90% used.
- Memory: 33.6 GB total, 20.3 GB available, 13.3 GB used.
- Swap: 2.15 GB total, 2.08 GB used (about 97%); investigate memory pressure before installing further large packages.
- Load average: 0.75 / 1.30 / 1.40.
- Uptime: 1,253,397 seconds at check.
- Failed systemd units count from Gateway health snapshot: 0; several named units below nevertheless show activating/restart-loop states in systemd's unit listing.
- Gateway sudo status: action required; non-root inspection was possible. Root-only inventory and cleanup are blocked until sudo is authorized in Gateway.

## Disk attribution observed (du, one filesystem)
- `/home`: 30G; `/home/xiaye`: 30G.
- `/opt`: 18G; `/opt/agents`: 14G.
- `/usr/local`: 22G; `/usr/local/lib`: 22G.
- `/opt/open-webui`: 933M; `/opt/dify`: 892M; `/opt/hermes-agent-v0.22.5`: 609M; `/opt/litellm-venv`: 546M; `/opt/agent-plane`: 393M; `/opt/llama.cpp`: 326M.
- `/opt/openhands-upstream-build-v1.25.0`: 33M; `/opt/open-hands-integrated-main`: 7.5M.
- Docker reports: 24 images / 40.92GB; 30 containers / 1.324GB; 32 volumes / 4.92GB (3.682GB reported reclaimable); build cache 357.2MB (122.9KB reclaimable).
- Docker's image reclaimable field says 100% despite 30 containers being active; do not interpret this alone as safe-to-prune. No prune was run.
- Largest unattributed areas still require a deeper, permission-aware du pass: /home/xiaye, /usr/local/lib and Docker's actual data root.

## Docker containers observed
Running / restarting containers (names as reported):
- Dify: `docker-local_sandbox-1` (healthy), `docker-agent_backend-1`, `docker-api-1` (healthy), `docker-worker-1`, `docker-worker_beat-1`, `docker-api_websocket-1`, `docker-plugin_daemon-1`, `docker-agent_ssrf_proxy-1`, `docker-web-1`, `docker-db_postgres-1`, `docker-redis-1`, `docker-sandbox-1` (healthy), `docker-ssrf_proxy-1`, `docker-weaviate-1`.
- OpenHands: `openhands-canvas` (Agent Canvas image, published host port 8000); `openhands` (0.47.0, published host port 13000); `oh-runtime`.
- Agent stack: `agents-litellm` (published 14000), `agents-postgres` (15432), `agents-redis` (16379), `agents-qdrant` (16333/16334), `agents-mem0` (18080), `agents-newapi` (13001).
- Other: `open-webui` (healthy, published 3000), `mimocode2api` (healthy, published 8080), `mcp-proxy` (published 5700), `exa-mcp` (restarting), `qdrant` (loopback 6333/6334), `coolify-db` (healthy), `coolify-redis` (healthy).
- Docker reports 30 active containers. The listing above is the portion returned in the bounded output; verify full `docker ps -a` before any lifecycle action.

## Existing listening TCP sockets
No port was added during this audit. The following listeners were already present at observation time:
- All-interface / wildcard: 22, 2222, 3000, 5003, 5700, 631, 8000, 8080, 8081, 8743, 11344, 13000, 13001, 14000, 15432, 16333, 16334, 16379, 18080, 26357.
- Loopback only: 3080, 4000, 47937, 6379, 7000, 7500, 8642, 8643, 8890, 9050, 9999, 11343, 20128, 6333, 6334.
- Tailscale interface: 443, 35539.
- Existing wildcard-bound listeners are not evidence that firewall exposure is intended. Each must be mapped to its owning service and ingress policy before changing anything. The user's instruction remains: do not open additional ports.

## systemd units observed
Active/running: `agent-throne-file-center.service`, `dsh-agent.service`, `hermes-api.service`, `hermes-gateway.service`, `litellm.service`, `lody-agent.service`, `redis-server.service`, `tailscaled.service`, `termalin-agent.service`.
Restarting / activating: `ai-agent-throne.service`, `llama-agent-fast.service`, `llama-agent.service`, `sentinelx-cloud-core.service`.
Inactive/dead (do not assume disposable): `agent-docker-port-guard.service`, `agent-integration-progress-report.service`, `ai-agent-upstream-check.service`, `litellm-agent.service`, `nginx.service`, `openhands-litellm-bridge.service`, `openhands-watchdog.service`, `termalin-agent-update.service`.
- Nginx is listed inactive even though many direct container host ports are bound. This needs review; do not start/reload it as part of inventory.

## Local Git working trees discovered
- `/home/xiaye/Ai-agent-skill`
- `/home/xiaye/All-in`
- `/home/xiaye/CKA-Agent`
- `/home/xiaye/Claude-code`
- `/home/xiaye/hermes-007`
- `/home/xiaye/openhands-extensions`
- `/home/xiaye/repository/Google-AI`
- `/home/xiaye/vps-mirror-workspace`
- `/opt/.sentinelx-prev.20261112020440`
- `/opt/agent-plane`
- `/opt/agents/-`
- `/opt/ai-stack`
- `/opt/dify`
- `/opt/llama.cpp`
- `/opt/openhands-upstream-build-v1.25.0`
- `/usr/local/lib/hermes-agent`

The earlier inventory additionally recorded /root/openhands-deploy and several /opt projects. This read-only find did not return /root/openhands-deploy, which may be a stale path or inaccessible under current permissions. Reconcile before concluding it is absent.

## Integrations and account state
- GitHub connector authenticated as `0megAlpha`, destination repository push/admin rights confirmed.
- Gateway SSH connected and read-only host commands succeeded.
- Shellway lists `greencloud-ai` as **offline**; no Shellway remote execution possible.
- Termalin previously reported the Pro trial expired; its AI server access is not currently usable on the Free plan.
- SentinelX currently has no connected host (previous host enrollment requires installation/handshake); current host service restart-loop observed.
- Vercel deployment context returns no linked teams; listing projects fails 403 because connector is scoped to old team `xavideo777-9021`. Do not authorize or restore that old team; Vercel requires selecting the correct current team/account through its own account scope before project actions.
- Lody runtime systemd service is active, but the external mobile/device authorization is separate and still pending. Generate any device authorization code only after all host-side preparation is finished.
- Conduit mobile pairing is still pending; no evidence of a successful iOS pairing in this audit.
- Notion connector had previously authenticated successfully; current page update was not attempted in this snapshot.

## Immediate remediation queue
1. Resolve disk usage by identifying top-level consumers and exact duplicate/cache candidates. Do not run `docker system prune`, volume prune, image prune, apt autoremove, or blanket cache deletion. Confirm image/container/volume references first.
2. Inspect the four restarting systemd units and `exa-mcp` logs, unit files, executable paths, restart policies and dependencies. Fix only after collecting evidence and preserving rollback.
3. Map every existing wildcard listener to container/systemd owner and ingress path. No new listener; no automatic closure of existing listeners until dependency/owner mapping is proven.
4. Perform project-by-project Git status, remotes, branch ancestry, staged/unstaged/untracked/ignored files, submodule/LFS inventory and duplicate comparison for every local tree above.
5. Exclude real secrets, private keys, cookies, auth databases, model weights, caches, runtime state and unreviewed suspicious tooling from Git. Keep sanitized templates and provenance.
6. The user-uploaded historical notes include tools described as encoding/obfuscating requests to evade upstream security filters (e.g. JBFuzz, Ghost Gateway, REALM Decomposer, Outbound Cloaker, MetaCipher). Do not install these into the portable Agent OS or treat their bypass claims as normal coding capabilities. Preserve the original document only in a restricted/private archive after review; the target repository is PUBLIC.
7. Finish the project migration by adding verified, sanitized source files/submodules to the canonical repository, preserving upstream history and source attribution; then verify each commit and remote file content.
8. Complete runtime end-to-end tests: OpenHands UI/API, Agent Server, workspace persistence, LLM inference via LiteLLM, MCP tool invocation, Playwright, Dify agent workflow, GitHub PR workflow and Conduit mobile client.
9. Only after all host-side setup and tests, generate fresh Lody / other one-time authorization links or codes.

## Blocking prerequisites
- Gateway sudo is currently `action_required`; setup link: https://trygateway.sh/app/servers/srv_01M691XRH300JR2KZND0ZJPF3S/sudo . This is needed for root-owned paths and full system-level disk/agent inventory. Do not enter passwords in chat.
- Proactive Gateway file scanning preference is disabled (0 of 5 daily scans used). No proactive file scan was started.
- This snapshot does not claim full migration, all project comparisons, or all integrations complete.
