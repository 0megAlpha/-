# Agent System provider adapter

This project already has a generic OpenAI Chat Completions client in `BaseAgent`. It reads:
- `LITELLM_BASE_URL`
- `LITELLM_MASTER_KEY`
- `LITELLM_MODEL`
- `LLM_TIMEOUT`
- `MOCK_LLM`

Use the example environment file, inject the key through the runtime secret store, and select a model alias registered in LiteLLM. This is the cleanest generic self-hosted adapter among the imported agent projects because it has a single base URL, key and model contract.

The VPS LiteLLM key is currently a placeholder, so a real end-to-end call remains pending.
