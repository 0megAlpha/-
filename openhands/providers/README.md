# OpenHands model and agent adapters

The OpenHands stack uses LiteLLM for model routing and MCP/ACP for tool and agent interoperability.

Host process:
- LLM_BASE_URL=http://127.0.0.1:14000
- LLM_API_KEY must be injected from the LiteLLM secret.

Container process on the OpenHands network:
- LLM_BASE_URL=http://agents-litellm:4000
- LLM_API_KEY must be injected from the LiteLLM secret.

Do not hard-code a gateway key in config.toml. Keep model routing, MCP server definitions and ACP agent connections as separate configuration layers.
