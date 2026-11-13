# FuzzingBrain / DARPA AIxCC provider adapter

The bundled FuzzingBrain runtime supports OpenAI, Anthropic, Google Gemini and xAI provider keys, and uses LiteLLM for model routing in addition to native OpenAI SDK branches.

- API keys are read from `llm_config.local.yaml` or the runtime environment.
- Keep the populated local config untracked; use `llm_config.local.yaml.example` as a template.
- Model selection is through the existing provider/model registry. Do not invent provider model IDs.
- The current LLMConfig schema does not expose a general per-model `api_base` field. Native provider endpoints work through the provider SDK/LiteLLM defaults; arbitrary custom endpoints require an explicit code/config extension and a protocol test before being declared compatible.

The example contains empty credentials only. It is not a live credential setup.
