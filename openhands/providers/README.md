# OpenHands Provider Adapter

OpenHands is the primary orchestration platform. Use LiteLLM for model routing, MCP for tools/resources, and ACP for external coding-agent runtimes. These are distinct integration layers.

- Docker-network LiteLLM base: `http://agents-litellm:4000`
- Local Qwen3 0.6B Chat Completions endpoint (Docker bridge only): `http://172.17.0.1:8089/v1`
- OpenAI-compatible model route: `/v1`
- Anthropic-compatible route: configure LiteLLM's Anthropic endpoint separately when an Anthropic provider is configured.
- Model name: `litellm_proxy/<registered-model-alias>`
- Credential: inject the actual gateway key through the runtime secret store.

The current LiteLLM master key and OpenHands LLM_API_KEY were detected as placeholders, not production credentials. Two keyless Chat Completions routes passed live inference; remaining provider routes and Responses/Anthropic conformance are pending.
