# Claude Code Provider Adapter

Claude Code uses Anthropic Messages semantics. Configure a native Anthropic endpoint, a compatible gateway, or the LiteLLM Anthropic-format endpoint. Do not point Claude Code at a Chat Completions-only URL.

- `ANTHROPIC_BASE_URL`: provider root (for LiteLLM, normally the proxy root; pass-through can use `/anthropic`)
- `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`: runtime credential
- `ANTHROPIC_MODEL`: provider model alias
- `CLAUDE_CODE_USE_BEDROCK` / `CLAUDE_CODE_USE_VERTEX`: only for their respective native cloud modes

See `claude-code.env.example`. Inject values through the secret store, then run `claude doctor` and a minimal `claude -p` request.
