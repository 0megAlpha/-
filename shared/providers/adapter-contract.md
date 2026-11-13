# Cross-Agent Provider Adapter Contract

This is the shared interface contract only. Provider implementation, configuration, plugins and credentials remain in each Agent's own canonical directory.

## Required fields
- `provider_id`: stable identifier
- `protocol`: exact wire protocol (OpenAI Responses, OpenAI Chat Completions, Anthropic Messages, Gemini native, MCP, ACP, or vendor REST)
- `base_url`: provider root, without a duplicated endpoint suffix
- `model_id`: provider model identifier
- `credential_env`: environment variable name; never a populated secret
- `capabilities`: streaming, tools, structured output, vision, embeddings, reasoning, batch
- `health_check`: safe non-billable endpoint where available
- `conformance_tests`: protocol-specific model listing and minimal completion checks

## Protocol rules
- Do not treat Chat Completions, Responses, Anthropic Messages, Gemini, MCP and ACP as interchangeable.
- Codex custom providers require the Responses wire API.
- Claude Code uses Anthropic Messages semantics or a compatible LiteLLM Anthropic endpoint.
- Devin's service API/MCP controls Devin sessions and workspaces; it is not a custom inference endpoint.
- MCP provides tools/resources; ACP provides external-agent execution. Neither is a model inference API.
- Credentials are injected at runtime from a secret store. Never commit .env files with populated values.
- A route is `verified` only after an actual minimal completion succeeds using that Agent's native protocol.

## Canonical ownership
Agent-specific adapters and settings belong under `<agent>/providers/`. Only this protocol contract and cross-agent schemas belong in `shared/providers/`.
