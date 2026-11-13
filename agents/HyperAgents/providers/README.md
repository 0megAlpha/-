# HyperAgents provider adapter

HyperAgents uses LiteLLM's `completion()` API and accepts a model ID at the call boundary. It already includes model families for Anthropic, OpenAI and Gemini.

For a self-hosted OpenAI-compatible endpoint, choose a model alias registered at the gateway and set the LiteLLM/OpenAI provider base URL and API key in the runtime environment. Keep the provider prefix in the model ID consistent with LiteLLM's routing rules.

- VPS host endpoint: `http://127.0.0.1:14000/v1`
- Docker service endpoint: `http://agents-litellm:4000/v1`
- Credential: `OPENAI_API_KEY` (Gateway secret injection)
- Model: gateway alias exposed as an OpenAI-compatible model

For native providers, inject `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GEMINI_API_KEY` as appropriate. No credential is stored in this directory.
