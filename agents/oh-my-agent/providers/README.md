# Oh My Agent provider matrix

Canonical project path: `agents/oh-my-agent`. The sibling `agents/-oh-my-agent-` is a retained duplicate snapshot and is not deployed separately.

The project already provides `config/providers.env.example` and a ProviderMatrix abstraction. It supports:
- LiteLLM gateway via `LITELLM_BASE_URL`
- OpenAI, Anthropic, Google, Azure OpenAI
- AWS, DeepSeek, Qwen, Mistral, xAI, Groq, Together, Fireworks and OpenRouter
- Ollama via `OLLAMA_BASE_URL`

For this VPS, use `http://agents-litellm:4000` from the OpenHands Docker network or `http://127.0.0.1:14000` from the host. Inject provider keys through the runtime secret store. The LiteLLM master key is currently a placeholder, so the gateway route is not marked live until a real key is configured and an end-to-end call passes.

Do not create a second Oh My Agent deployment from the duplicate hyphenated directory.
