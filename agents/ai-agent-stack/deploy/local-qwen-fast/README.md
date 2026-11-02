# Local Qwen3 Fast Agent Model

This deployment adds a small local model endpoint for Agent workloads on CPU-only VPS hosts. It is a separate service and does not replace the existing 27B model process.

## Deployed contract (2026-10-13)

- Upstream: `Qwen/Qwen3-4B-GGUF`, file `Qwen3-4B-Q4_K_M.gguf`, Apache-2.0 license.
- Endpoint: `127.0.0.1:8089`; never bind it to `0.0.0.0` or expose it publicly.
- API alias: `qwen3-4b-local`.
- LiteLLM alias `my-model` routes to the 4B service; `my-model-slow` preserves the prior 27B Q8 endpoint at `127.0.0.1:8088` as a slow fallback.
- Qwen thinking is disabled in the LiteLLM `extra_body` (`chat_template_kwargs.enable_thinking=false`). Without this, short requests can return only `reasoning_content` and an empty `content` field.
- The fast model server requires an API key file at `/etc/llama-agent-fast/api-keys` (mode `0600`). The same value is supplied to LiteLLM through `LOCAL_MODEL_API_KEY` in the root-owned `/root/.agent.env` (mode `0600`). Never commit either value.
- The service uses four CPU threads and an 8,192-token context. Adjust only after benchmarking the host.
- `hermes-provider.fragment.yaml` records the current custom-provider schema for Hermes. The one-shot test only passed with a reduced prompt/toolset (`--ignore-rules -t terminal`); the default Hermes full-toolset prompt exceeds the current context and is not considered complete. Do not restart the production gateway on this model until the full prompt/context path is verified.

## Artifact lock

`model.lock` records the observed file size and SHA-256 from the VPS download. The checksum is an integrity record for that downloaded artifact, not a claim that Hugging Face publishes the same checksum.

## Installation / merge

1. Download the exact file from the `source_url` in `model.lock` into `/opt/qwen3-4b-runtime/`.
2. Verify the size and compute `sha256sum`; compare with the recorded snapshot hash when reproducing this exact artifact.
3. Create `/etc/llama-agent-fast/` with mode `0700`, generate a random API key, write it to `api-keys` with mode `0600`, and put the same value in `LOCAL_MODEL_API_KEY` in `/root/.agent.env` with mode `0600`.
4. Install this service file as `/etc/systemd/system/llama-agent-fast.service`, then run `systemctl daemon-reload` and `systemctl enable --now llama-agent-fast.service`.
5. Merge `litellm-model-list.fragment.yaml` entries into the existing `/root/litellm_config.yaml`; do not overwrite the rest of that file. Preserve a timestamped backup first.
6. Restart LiteLLM, then test `/health/readiness`, authenticated `/v1/models`, a text completion, and a required function-tool call through both `127.0.0.1:4000` and the OpenHands bridge `10.0.0.1:4001`.
7. Run `All-in/tests/verify_agent_api_compat.sh` from the Ai-Agent-Skill checkout. A model catalog response alone is not an inference test.

## Rollback

1. Restore the timestamped LiteLLM config backup and restart `litellm.service`.
2. Stop/disable `llama-agent-fast.service` if the new model fails health or tool-call tests.
3. Keep the downloaded model and key backup until the previous route is verified; do not prune the original 27B model or Docker volumes as part of this rollback.

## Observed verification

- Unauthenticated direct `/v1/models` on port 8089 returned HTTP 401; authenticated completion returned HTTP 200 and non-empty content.
- The 4B model produced a short response in about 1.6 seconds on this VPS; a required function-tool call was returned in about 9 seconds in a direct test.
- The compatibility test exercised generation, tool-call emission, and continuation after a tool result through both LiteLLM and the OpenHands bridge.
- This validates the model/gateway interface, not every production Agent UI or mobile-to-Git workflow.

## Codex local entrypoint and progress snapshots

The VPS has a root-only `codex-local` wrapper for running Codex tasks against the local LiteLLM Responses API (`my-model`). It reads only `OPENAI_API_KEY` from the existing root-only `/root/.agent.env` (other root environment secrets are not exported to Codex tools), rejects caller options that could override the fixed sandbox/provider configuration, uses an isolated writable Codex home at `/var/lib/agent-integration/codex-home`, disables user/project Codex configuration loading, and runs non-interactive tasks with the `workspace-write` sandbox. The wrapper is installed as `/usr/local/sbin/codex-local` with mode `0700`; do not make it world-readable or copy credentials into its source. This path passed a live local inference test and a real one-file write/read task. The model-metadata warning remains because `my-model` is a custom alias.

The read-only progress snapshot consists of `systemd/agent-integration-progress-report.sh`, `.service`, and `.timer`. Install the script to `/usr/local/sbin/agent-integration-progress-report.sh` (mode `0700`), the units to `/etc/systemd/system/` (mode `0644`), then create the root-only state directory with `install -d -m 700 /var/lib/agent-integration /var/lib/agent-integration/codex-home`, then run `systemctl daemon-reload`, `systemctl enable --now agent-integration-progress-report.timer`, and `systemctl start agent-integration-progress-report.service`. The service also declares `StateDirectory=agent-integration` so systemd provisions its state directory on supported hosts. The latest snapshot is written to `/var/lib/agent-integration/progress-latest.md` (mode `0600`). The timer refreshes every 30 minutes and does not install packages, delete files, restart application services, commit/push, or send chat messages.

This local Codex route is not a replacement for external Claude credentials. Claude Code 2.1.296 currently rejects the custom model alias and its full prompt exceeds the 8,192-token local model context; the Lody/Claude end-to-end path remains blocked. The default root Codex profile also remains unauthenticated and configured for the unavailable `sim` endpoint; use the explicit `codex-local` wrapper for the tested local route.
