# Claude Code provider adapter

Claude Code's custom endpoint must implement Anthropic Messages semantics. Set ANTHROPIC_BASE_URL to an Anthropic-compatible gateway, ANTHROPIC_AUTH_TOKEN to the gateway credential, and select a model exposed by that gateway.

The included example uses the local LiteLLM service URL. It is a configuration template only: verify the gateway's /v1/messages route and a real completion before applying it to a live Claude Code profile. MCP tool servers are configured separately.
