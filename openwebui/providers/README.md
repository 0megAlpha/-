# Open WebUI Provider Adapter

Open WebUI is a UI/provider client, not an agent runtime equivalent to Codex or Claude Code. Configure one or more OpenAI-compatible connections under Admin → Connections, or inject the supported environment variables at container creation.

- `OPENAI_API_BASE_URLS`: comma-separated endpoint roots
- `OPENAI_API_KEYS`: corresponding runtime keys
- `DEFAULT_MODELS`: optional default model aliases

See `openwebui.env.example`. Do not place credentials in exported connection JSON or repository files.
