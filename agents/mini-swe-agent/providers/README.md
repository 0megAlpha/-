# mini-SWE-agent provider adapter

The checked-in runtime already uses LiteLLM and supports local OpenAI-compatible models through `model_kwargs.custom_llm_provider` and `model_kwargs.api_base`. It also has native model classes for Anthropic, OpenAI, OpenRouter and Portkey.

## Self-hosted LiteLLM example

Copy `mini-swe-agent.yaml.example` into a task config and inject `OPENAI_API_KEY` from the runtime secret store. Do not put the populated key in YAML or Git.

- Model alias: `pollinations-free` (must exist in the LiteLLM proxy model list)
- API base: `http://agents-litellm:4000/v1` from the Docker network, or `http://127.0.0.1:14000/v1` on the VPS host
- Model class: `litellm`
- Provider: `openai`

The current LiteLLM master key on the VPS is a placeholder, so this template is not marked live until a real Gateway-stored key is applied and the agent's own completion test passes.

## Other providers

Use the native model class and corresponding runtime secret variables: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, or `PORTKEY_API_KEY`. The exact model ID must match the selected provider.
