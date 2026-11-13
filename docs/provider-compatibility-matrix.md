# Agent API Provider Compatibility

LiteLLM is the common model gateway where an agent supports a documented protocol adapter. The VPS host endpoint is http://127.0.0.1:14000; containers on the OpenHands Compose network use http://agents-litellm:4000.

## Protocol contracts

| Protocol | Wire contract | Typical consumers | Notes |
|---|---|---|---|
| OpenAI Chat Completions | /v1/chat/completions | Aider, OpenCode, Open WebUI, many OpenAI-compatible clients | Custom base URLs are supported where the client exposes one. |
| OpenAI Responses | /v1/responses | Codex custom provider | Codex custom providers use the Responses wire API; Chat Completions is not interchangeable. |
| Anthropic Messages | /v1/messages | Claude Code custom endpoint | Claude Code expects Anthropic Messages semantics, not merely an OpenAI-compatible endpoint. |
| Gemini API | Google Generative Language API | Gemini-native clients | Use the native endpoint or a gateway adapter implementing Gemini semantics. |
| MCP | stdio / Streamable HTTP | Tool access for OpenHands, Claude Code, Codex and MCP-capable clients | MCP connects tools/resources; it is not an inference API. |
| ACP | Agent Client Protocol | OpenHands and compatible agent clients | ACP connects agent runtimes; it does not automatically add an inference provider. |

## Per-agent connection model

- OpenHands: use LiteLLM as its configured LLM endpoint; MCP and ACP are separate tool/agent integration layers.
- Codex CLI: use a custom provider with wire_api = responses and an OpenAI-compatible Responses endpoint. Verify /v1/responses before selecting a model.
- Claude Code: use ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN against an Anthropic Messages-compatible endpoint. A generic OpenAI Chat Completions endpoint is not sufficient.
- Aider: use its OpenAI-compatible model provider and OPENAI_API_BASE.
- Cline: select the OpenAI-compatible provider and set the custom base URL, model ID and key in Cline provider settings.
- Goose: use its OpenAI provider with a custom OpenAI host.
- OpenCode: define a provider with baseURL and a model ID in its provider configuration.
- Hermes: configure a supported OpenAI-compatible/LiteLLM provider in Hermes model configuration; use MCP separately for tools.
- DSH: configure the active DSH model provider using its supported OpenAI-compatible endpoint; DSH plugins remain inside the DSH agent directory.
- Open WebUI: configure an OpenAI-compatible connection to LiteLLM; it is a UI/provider client, not an agent runtime equivalent to Codex or Claude Code.
- Devin: Devin is a hosted agent service. Its public API/MCP integrations expose task and workspace operations; that is not the same as selecting a custom inference base URL. Do not claim arbitrary model-provider routing unless the Devin product contract explicitly supports it.
- DeepSeek: use the native DeepSeek API or an OpenAI-compatible gateway route.

## Environment contract

Use these environment variable names only; inject real values through the runtime secret store, never commit populated .env files:
- LITELLM_MASTER_KEY
- OPENAI_BASE_URL / OPENAI_API_KEY
- ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN
- DEVIN_API_KEY (Devin service API, not model inference)
- Provider-specific keys such as DEEPSEEK_API_KEY, GEMINI_API_KEY, OPENROUTER_API_KEY, and NVIDIA_API_KEY.

Current VPS observations on 2026-11-13: LiteLLM /v1/models returned 11 model IDs and its readiness endpoint returned HTTP 200. This proves route discovery and service readiness, not successful inference for every provider. Provider-specific credentials in .env were empty or placeholders at the time of inspection, so routes requiring those keys are not verified for live inference.
