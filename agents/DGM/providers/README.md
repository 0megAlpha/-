# Darwin Gödel Machine provider adapter

DGM currently selects clients by model family:
- Anthropic SDK for Claude models
- OpenAI SDK for GPT/o-series models
- OpenAI-compatible DeepSeek and OpenRouter clients with provider-specific base URLs
- Bedrock and Vertex Anthropic clients for those model prefixes

For the OpenAI SDK branch, set `OPENAI_BASE_URL` to a compatible API root and `OPENAI_API_KEY` to a runtime secret. The selected model name must be accepted by DGM's `AVAILABLE_LLMS` list and registered as an alias at the gateway. DeepSeek/OpenRouter branches currently hard-code their provider endpoints, so do not claim arbitrary custom base URL support for those branches.

Use `dgm.env.example`; inject values from the secret store. Never commit a populated `.env`.
