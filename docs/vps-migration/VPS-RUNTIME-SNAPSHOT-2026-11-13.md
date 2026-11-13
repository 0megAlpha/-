# VPS Runtime Snapshot — 2026-11-13

## Host and capacity
- Host: agent-vps / Ubuntu 26.04 / 4 vCPU AMD EPYC / ~31 GiB RAM / ~320 GiB filesystem.
- After removing the verified clean duplicate Git worktree, root filesystem: 332,057,387,008 bytes total; approximately 263 GB used; 47 GB free; 86% used.
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

## Network exposure

- Detailed TCP/UDP listener inventory is retained in the private VPS maintenance record in Notion; it is intentionally not published in this public GitHub repository.
- Several services bind to all host interfaces; actual internet reachability depends on firewall rules. No firewall or published-port changes were made in this pass.

## Storage and cleanup
- The temporary full-tree Git worktree was removed only after confirming it was clean and its HEAD exactly matched the remote branch SHA. Approximately 21.6 GB was reclaimed. The source checkout at `/opt/agents/-` and all Docker volumes were preserved.
- 32 Docker volumes were inventoried. No volume was deleted because ownership and data retention have not been established.
- Do not run blanket Docker volume pruning.
- The original source checkout `/opt/agents/-` remains on `main`, ahead 3 / behind 2, with existing modified and untracked files. It was not reset, cleaned, switched or overwritten.

## Remaining deployment blockers
1. Supply `litellm-master-key` in Gateway's secure stored-value UI, then apply it to LiteLLM and OpenHands and disable placeholder credentials.
2. Supply/refresh provider credentials for the failed Gemini, Groq, Z.AI, Cerebras, OpenRouter and Abliteration routes.
3. Restore the original Qwen3 4B and Qwen3.8 27B model weights or approve an explicit quantization/model replacement.
4. Complete Lody authentication with `lody login`.
5. Verify Codex Responses and Claude Code Anthropic Messages routes with protocol-conformant providers.
6. Finish GitHub repository visibility change to Private; current `0megAlpha/-` visibility remains Public.
7. Complete Vercel team authorization and re-run project/team/deployment discovery.
