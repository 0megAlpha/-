# Agent Provider Adapter Status — 2026-11-13

## Ownership rule
Each Agent owns its own provider adapters, config templates, MCP registrations, plugins and runtime instructions under its own directory. Only cross-Agent protocol contracts and shared schemas belong under `shared/`. This change does not move per-Agent plugins into a global skills-only repository.

## Canonical Agent directories
| Agent | Adapter directory | Provider protocol | State |
|---|---|---|---|
| OpenHands | `openhands/providers/` | OpenAI Chat Completions / LiteLLM / local Qwen | Canvas 1.38.0 + EMAT workspace skill verified; provider key remains placeholder |
| Codex | `codex/providers/` | OpenAI Responses | Config template installed; live Responses route returns HTTP 500 |
| Claude Code | `claude-code/providers/` | Anthropic Messages | Env example and launch wrapper installed; Messages route timed out |
| Devin | `devin/providers/` | Devin service API + MCP | Adapter template installed; no service credential available |
| Hermes | `hermes/providers/` | Native provider registry + OpenAI Chat Completions | Existing provider implementation retained; adapter guide updated |
| DSH | `dsh/providers/` | OpenAI Chat Completions | Config template installed; runtime test pending |
| Aider | `aider/providers/` | OpenAI Chat Completions | YAML and env examples installed |
| Cline | `cline/providers/` | OpenAI-compatible provider UI | Setup guide and env example installed |
| Goose | `goose/providers/` | OpenAI Chat Completions | Env example installed; runtime schema test pending |
| OpenCode | `opencode/providers/` | OpenAI-compatible provider | JSON and env examples installed and syntax-checked |
| DeepSeek | `deepseek/providers/` | DeepSeek native / OpenAI Chat Completions | Env example installed |
| Open WebUI | `openwebui/providers/` | OpenAI Chat Completions | Env example installed; container connection pending |

## OpenHands court capability
The EMAT three-role court skill is installed into the live OpenHands Canvas workspace:
- Breaker: adversarial counterexamples and failure tests.
- Builder: independent implementation and repair.
- Magistrate: independent validation and sealed verdict.
- Evidence chain: SHA-256 sealed plans and append-only verdict ledger.

The skill has two passing unit tests and is visible in the actual workspace. It is an OpenHands workspace skill, not a detached global skills-only upload.

## Self-hosted model endpoints
- LiteLLM host: `http://127.0.0.1:14000/v1`
- LiteLLM Docker service: `http://agents-litellm:4000/v1`
- Local Qwen3 0.6B host: `http://127.0.0.1:8089/v1`
- Local Qwen3 0.6B from OpenHands Docker network: `http://172.17.0.1:8089/v1`

The local Qwen model has a verified Chat Completions response from the OpenHands container. It is a small local fallback, not a replacement for the intended 4B/27B models.

## Completion gates
A provider/Agent is not marked live until:
1. Its credential is injected from the secret store.
2. Its native protocol is identified and the exact endpoint path is tested.
3. A minimal completion succeeds.
4. Tool calls, streaming and structured output are tested where supported.
5. The Agent runtime itself loads the provider configuration.
6. The result is recorded in `agent-registry.yaml`.

## External credentials and protocol blockers
- The LiteLLM master key and OpenHands model key are placeholders. A Gateway secure stored value named `litellm-master-key` is awaiting user setup.
- Gemini, Groq, Z.AI, Cerebras, OpenRouter and Abliteration routes failed authentication/permission tests.
- Codex Responses and Claude Code Anthropic Messages are not currently verified through the VPS LiteLLM.
- Devin requires a valid service API credential and repository integration.
