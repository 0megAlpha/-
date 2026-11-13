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


## Additional runtime frameworks discovered in the full-tree inventory

| Framework | Adapter path | Native integration | State |
|---|---|---|---|
| mini-SWE-agent | `agents/mini-swe-agent/providers` | LiteLLM, OpenAI-compatible, Anthropic, OpenRouter, Portkey | Template installed |
| SWE-agent | `agents/SWE-agent/providers` | LiteLLM with explicit api_base/api_key | Template installed |
| DGM | `agents/DGM/providers` | OpenAI SDK, Anthropic SDK, DeepSeek, OpenRouter | Template installed; custom base URL is limited to the OpenAI SDK branch |
| HyperAgents | `agents/HyperAgents/providers` | LiteLLM | Template installed |
| FuzzingBrain / DARPA-AIxCC | `agents/DARPA-AIxCC/providers` | OpenAI, Anthropic, Google, xAI | Template installed; current LLMConfig does not expose a general api_base field |
| Agent System | `agents/agent-system/providers` | Existing generic LiteLLM base URL/key/model contract | Template installed |

## OpenHands capabilities installed in the live workspace

- EMAT court + adaptive evolution: 8/8 unit tests pass in the live Canvas container. Branch ranking requires complete test evidence, topology validation keeps Magistrate read-only, feedback retries are bounded to three, and law/topology changes remain proposal-only.
- Quality gates: Playwright 1.65.0 + Chromium (2/2 browser tests pass), Biome 2.6.7, ESLint 10.14.0, SonarScanner wrapper 5.1.0, Semgrep 1.185.0 and Trivy 0.73.0.
- Sonar analysis is not yet live because no SonarQube/SonarCloud endpoint or token is configured.
- Semgrep smoke checks on one Python and one JavaScript file each returned zero findings; this is a smoke test, not a full repository security clearance.
- The OpenHands runtime intentionally cannot access the host Docker socket directly. Container lifecycle stays under the OpenHands Docker runtime control plane.


## Additional provider-enabled runtime and orchestration bundle

- Oh My Agent: canonical path `agents/oh-my-agent`; existing ProviderMatrix and `config/providers.env.example` cover LiteLLM, OpenAI, Anthropic, Google, Azure, AWS, DeepSeek, Qwen, Mistral, xAI, Groq, Together, Fireworks, OpenRouter and Ollama. The hyphen-wrapped sibling is a retained alias, not a second deployment.
- All-in: canonical path `agents/All-in`; orchestration bundle with OpenAI, DeepSeek, Moonshot, OpenRouter and LiteLLM endpoint variables. Its child agents retain their own provider adapters.
- Duplicate policy: do not deploy both `agents/oh-my-agent` and `agents/-oh-my-agent-`; do not deploy both `agents/DARPA-AIxCC` and its marker-only sibling; retain the divergent `afc-crs`/FuzzingBrain snapshots for review only; `All-in-root` is a divergent historical snapshot and is not deployed beside canonical All-in.
- StateM is a workflow engine and XAttacker is a security testing tool; they are not standalone LLM runtimes requiring a generic model-provider adapter.
