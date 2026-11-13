# Codex Provider Adapter

Codex custom model providers use the OpenAI Responses wire API. A gateway that only implements `/v1/chat/completions` is not sufficient.

- Configure `base_url` as the API root (normally ending in `/v1`); Codex appends `/responses`.
- Configure `wire_api = "responses"`.
- `env_key` is the environment variable NAME, not the key itself.
- Confirm the selected provider exposes `POST /v1/responses` and streaming `response.completed` before enabling it.

See `config.toml.example`. Current VPS LiteLLM Chat Completions routes are live for selected free providers; Responses conformance is still pending.
