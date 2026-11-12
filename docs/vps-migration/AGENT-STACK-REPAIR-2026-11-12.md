# Agent stack repair — 2026-11-12

## Fixed

- LiteLLM compose bind mount previously pointed to /opt/agents/-/openhands/gateway/litellm/config.yaml, which was a directory. The actual configuration is the regular file /opt/agents/-/openhands/litellm/config.yaml.
- Applied a Compose override mounting the existing regular config file at /app/config.yaml, retaining the existing host port 14000 -> container 4000.
- Recreated only the LiteLLM container. It is running with restart count 0.
- LiteLLM /health/liveliness and /health/readiness returned HTTP 200 from inside the container and host loopback.
- Authenticated /v1/models returned 11 model aliases: pollinations-free, kilo-free, llm7-free, abliteration-glm53-uncensored, groq-llama, gemini-flash, zai-glm-flash, cerebras-llama, openrouter-free, deepseek-chat, qwen-plus.
- One configured model entry (refuseless/glm-5.3-abliterated) is rejected by LiteLLM because its provider prefix is missing; LiteLLM logs the invalid deployment and continues loading the other aliases. The source config contains provider credentials and was not copied into Git.
- Dify agent_backend and local_sandbox previously failed because DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN was empty. Generated a random 256-bit token into /home/xiaye/.config/xiaye-agent-os/dify-runtime.env (mode 0600, outside Git), supplied it as an env-file override, and recreated only those two services.
- Dify agent_backend now runs; local_sandbox reports healthy and /healthz returned HTTP 200.
- OpenHands /health returned OK.

## Deployment artifacts

- Portable Compose override and helper script are in agent-os-portable/deploy/.
- The Dify runtime token is intentionally not stored in Git. The example file contains only a placeholder.
- The helper recreates only the existing LiteLLM and Dify agent_backend/local_sandbox services.

## Unchanged

- No new port, listener, Docker published port, NAT, firewall or reverse-proxy rule was added.
- Existing host port 14000 remains unchanged.
- No database, Redis, OpenHands, Dify API/web or other container was recreated.
- No .env or provider API key was committed.

## Remaining

- Fix the single LiteLLM model alias provider prefix after verifying the intended provider/API compatibility.
- Run an authenticated completion request against one free model alias; model catalog listing is verified, inference is not yet verified.
- Repair Exa MCP restart loop, systemd 203/200 failures, and finish project-by-project secret scan and migration.
