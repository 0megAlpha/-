# Lody Claude Code to local LiteLLM to Qwen3-4B

## Current configuration

The Lody workspace's Claude Code agent config is set to these non-secret values:

- ANTHROPIC_BASE_URL=http://127.0.0.1:4000
- ANTHROPIC_MODEL=my-model
- CLAUDE_CODE_SIMPLE=1

The Anthropic auth credential is deliberately not stored in Lody's cloud-backed agent config. Claude Code reads the existing VPS-local /root/.claude/settings.json configuration. Do not copy the shared LiteLLM gateway master credential into Lody's remote agent config.

The active Qwen3-4B llama-server systemd drop-in raises its context from 8,192 to 32,768 tokens. The server listens on 127.0.0.1:8089; the main LiteLLM proxy exposes the Anthropic-compatible route at 127.0.0.1:4000.

## Deployment

Install the systemd override as /etc/systemd/system/llama-agent-fast.service.d/20-context-32768.conf, then run:

    systemd-analyze verify /etc/systemd/system/llama-agent-fast.service
    systemctl daemon-reload
    systemctl restart llama-agent-fast.service
    systemctl is-active llama-agent-fast.service

Set the three non-secret variables above on the Lody Claude Code agent config using the Lody agent-config environment settings. Do not add a credential to that remote config.

## Verification status (2026-10-13)

- Direct Claude Code one-shot request through the local LiteLLM route: passed.
- Direct Claude Code shell-tool test creating and reading a file in a temporary directory: passed with CLAUDE_CODE_SIMPLE=1 and a restricted tool allowlist.
- Lody agent config capability refresh: succeeded; model my-model appears as a custom model.
- Full Lody ACP session test: not passed. Two read-only sessions timed out before returning an assistant message; both were cancelled. The Lody daemon did receive the new environment values. Investigate ACP latency/context/tool overhead before declaring Lody end-to-end complete.
- Claude Code emits a non-fatal unrecognized_model warning for custom alias my-model; LiteLLM still returns successful API responses.
- A temporary isolated proxy used during testing was stopped and its configuration/key files removed. The remote Lody config was verified to have no ANTHROPIC_AUTH_TOKEN entry.

## Rollback

Remove the context drop-in, then run systemctl daemon-reload and systemctl restart llama-agent-fast.service. The original unit remains unchanged in /etc/systemd/system/llama-agent-fast.service.
