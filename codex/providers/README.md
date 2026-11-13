# Codex provider adapter

Copy config.toml.example into the user's Codex configuration only after confirming that the selected LiteLLM model route supports /v1/responses. Set LITELLM_MASTER_KEY in the Codex process environment through the secret manager.

Do not point Codex at a Chat Completions-only endpoint: Codex custom providers use the Responses wire API. This template is committed but is not installed into a user's home directory automatically.
