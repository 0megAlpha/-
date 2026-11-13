# SWE-agent provider adapter

SWE-agent's `GenericAPIModelConfig` exposes `api_base`, `api_key`, `completion_kwargs` and uses LiteLLM for model calls. A key value beginning with `$` is resolved from the named environment variable.

## Self-hosted LiteLLM

Use `swe-agent-model.yaml.example` and inject `LITELLM_MASTER_KEY` at runtime. The example uses the VPS Docker service DNS name; from the host use `http://127.0.0.1:14000/v1`.

## Native providers

The same `api_base` and `api_key` fields can be set per model config for provider-specific endpoints. Use LiteLLM's provider/model naming and do not assume all providers share the same protocol.

The VPS LiteLLM key is currently a placeholder; do not mark the adapter live until the secret is rotated and SWE-agent passes a real model completion.
