# VPS Runtime Snapshot — 2026-11-13

## Host and capacity
- Host: agent-vps / Ubuntu 26.04 / 4 vCPU AMD EPYC / ~31 GiB RAM / ~320 GiB filesystem.
- Root filesystem: 332,057,387,008 bytes total; 303,958,630,400 bytes used; 28,081,979,392 bytes free; 92% used.
- Inodes: 18% used.
- Reboot required: yes (package update marker present). No reboot was initiated.
- Docker: 29 running containers, 30 total containers, 32 named/anonymous volumes.
- systemd: 88 active services; `systemctl --failed` reports 0 failed units, but several units are in repeated auto-restart loops (see below).

## Completed repairs and verified runtime
- OpenHands main container: `ghcr.io/all-hands-ai/openhands:0.47.0`, running on host port 13000.
- OpenHands Agent Canvas: `ghcr.io/openhands/agent-canvas:1.38.0`, running on port 8000; `/health` returns `{"status":"ok"}`.
- EMAT Agent Court skill copied into the live Canvas workspace at `/projects/.openhands/skills/emat-agent-court`; 112 skill files are visible in the workspace; two unit tests pass.
- Agent-Throne service: corrected its systemd working directory and entry point to the existing `/root/AI-Agent-Skill/portal/server.py`; `/api/health` returns `{"ok":true,"service":"agent-throne"}`.
- Local Qwen3 fast model: `llama-agent-fast.service` now runs the cached Qwen3 0.6B GGUF via `/usr/local/lib/ollama/llama-server`. The API is bound only to Docker bridge gateway `172.17.0.1:8089`, not a public interface. OpenHands container can reach it and a Chat Completions request returned `OK.`. The model has thinking disabled by default for short responses.
- Removed only the superseded stopped Canvas 1.37.0 backup container and its old image after verifying Canvas 1.38.0 health. The pre-upgrade inspect JSON remains at `/root/openhands-canvas-pre-1.38.0.inspect.json` (mode 0600).

## Model gateway validation
LiteLLM 1.108.0 is running as `agents-litellm` on host port 14000 (container port 4000). The configured `LITELLM_MASTER_KEY` and OpenHands `LLM_API_KEY` are placeholders, not production secrets. A Gateway stored value named `litellm-master-key` has been requested but not yet supplied.

OpenAI Chat Completions inference tests:
- PASS: `pollinations-free`
- PASS: `kilo-free`
- PASS: `refuseless-glm53-uncensored`
- PASS: `deepseek-chat`
- PASS: `qwen-plus`
- FAIL: `llm7-free` (400 invalid request/model)
- FAIL: `abliteration-glm53-uncensored` (401 authentication)
- FAIL: `groq-llama` (403 permission)
- FAIL: `gemini-flash` (401 authentication)
- FAIL: `zai-glm-flash` (401 authentication)
- FAIL: `cerebras-llama` (403 permission/edge challenge)
- FAIL: `openrouter-free` (401 missing/invalid auth)

Protocol-specific tests:
- LiteLLM `POST /v1/responses` returned HTTP 500; Codex Responses compatibility is not verified.
- LiteLLM `POST /v1/messages` timed out; Anthropic Messages compatibility is not verified.
- Local Qwen3 endpoint is OpenAI Chat Completions-compatible; it is not a verified Responses or Anthropic Messages endpoint.

## systemd exceptions requiring follow-up
- `llama-agent.service`: restart loop (approximately 79k historical restarts); configured executable `/opt/llama.cpp/build/bin/llama-server` is missing and configured 27B model file under `/opt/qwen38-runtime/` is absent. No replacement 27B weights were found in the scanned model directories.
- `llama-agent-fast.service`: repaired and now active with zero restarts since the repair; currently serves Qwen3 0.6B, not the original 4B model.
- `lody-agent.service`: repeatedly exits with `Worker authentication failed; run lody login`; service has approximately 13k historical restarts. Requires an authenticated Lody login.
- `nginx.service`: inactive. No Caddy service was active during this snapshot.
- Exa MCP container exited with code 0; Exa's ChatGPT connector is available. The container may be a stdio-launched MCP process rather than a persistent daemon; verify its MCP proxy launch configuration before treating it as a failure.
- Package reboot marker is present; reboot was not performed.

## TCP/UDP listeners
Socket bindings are recorded below. A bind to `0.0.0.0` or `::` means the process listens on all host interfaces; actual internet reachability depends on firewall rules, which were not fully proven in this snapshot.

### Public-interface binds (0.0.0.0 / ::)
- TCP 22 — SSH administration.
- TCP 631 — CUPS printing service.
- TCP 2222, 6080, 8081, 26357 — additional host processes; process-to-port ownership still needs a dedicated map.
- TCP 3000 — Open WebUI.
- TCP 5003 — Dify plugin daemon.
- TCP 5700 — Docker MCP Proxy.
- TCP 8000 — OpenHands Agent Canvas.
- TCP 8080 — MimoCode2API.
- TCP 8743 — ENI Harbor service.
- TCP 11344 — FRP relay.
- TCP 13000 — OpenHands main UI/API.
- TCP 13001 — NewAPI.
- TCP 14000 — LiteLLM proxy.
- TCP 15432 — agents PostgreSQL.
- TCP 16333/16334 — agents Qdrant HTTP/gRPC.
- TCP 16379 — agents Redis.
- TCP 18080 — agents Mem0.
- UDP 41641 — Tailscale WireGuard.

### Tailscale-interface binds
- TCP 443 and TCP 35539 on the Tailscale interface.

### Loopback-only binds
- TCP 3080 — DSH service.
- TCP 4000 — LiteLLM internal listener.
- TCP 6333/6334 — local Qdrant.
- TCP 6379 — local Redis.
- TCP 7000/7500 — FRP control/management.
- TCP 8642/8643 — Hermes API/Gateway.
- TCP 8787 — Agent-Throne API.
- TCP 8890 — Agent-Throne File Center.
- TCP 9050 — Tor SOCKS.
- TCP 9999 — mcp-vps service.
- TCP 11343 — FRP local listener.
- TCP 20128 — 9router.
- TCP 47937 — Hermes internal listener.
- UDP 323 — chrony.

## Storage and cleanup
- A separate full-tree Git worktree at `/opt/agent-vps-worktrees/0megalpha-full-tree` occupies approximately 21.6 GB; the source checkout at `/opt/agents/-` occupies approximately 20.6 GB. The worktree is a temporary duplicate created for safe branch work. After the new commit is pushed and verified, remove only that clean worktree to reclaim its checkout space; preserve the source checkout and all named Docker volumes.
- 32 Docker volumes were inventoried. No volume was deleted because ownership and data retention have not been established.
- Do not run blanket Docker volume pruning.

## Remaining deployment blockers
1. Supply `litellm-master-key` in Gateway's secure stored-value UI, then apply it to LiteLLM and OpenHands and disable placeholder credentials.
2. Supply/refresh provider credentials for the failed Gemini, Groq, Z.AI, Cerebras, OpenRouter and Abliteration routes.
3. Restore the original Qwen3 4B and Qwen3.8 27B model weights or approve an explicit quantization/model replacement.
4. Complete Lody authentication with `lody login`.
5. Verify Codex Responses and Claude Code Anthropic Messages routes with protocol-conformant providers.
6. Finish GitHub repository visibility change to Private; current `0megAlpha/-` visibility remains Public.
7. Complete Vercel team authorization and re-run project/team/deployment discovery.
