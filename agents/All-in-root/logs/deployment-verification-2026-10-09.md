# Deployment verification report — 2026-10-09

## Scope and evidence

This report records checks executed against the existing `greencloud-ai` VPS and the private repositories. It is an evidence snapshot, not a claim that every possible agent tool-use workflow has been exercised.

## Repository state

The following GitHub repositories were checked and confirmed private:
- `xh09411-web/Ai-Agent-Skill` — `main`
- `xh09411-web/All-in` — `main`
- `xh09411-web/ai-agent-stack` — `portable-20260924`
- `xh09411-web/ai-agent-fleet` — `main`

Merged pull requests:
- Ai-Agent-Skill #3 — secure multi-agent workflow skill: https://github.com/xh09411-web/Ai-Agent-Skill/pull/3
- All-in #1 — VPS recovery, private mobile access, and Qdrant loopback binding: https://github.com/xh09411-web/All-in/pull/1
- ai-agent-stack #1 — safe VPS recovery: https://github.com/xh09411-web/ai-agent-stack/pull/1

The first three working trees were clean and synchronized with their tracked remote branches. The existing `ai-agent-fleet` worktree contains an uncommitted deletion of the `swe-agent-src` gitlink. It was deliberately preserved; no reset, checkout-overwrite, or forced push was used. Inspect and resolve that missing submodule/worktree before publishing changes from that repository.

## Verification results

### Repository and skills
- `tools/verify_repo.py`: PASS — no high-confidence credential patterns found in scanned text files.
- Canonical skill structure: PASS — 21 `SKILL.md` definitions.
- Configuration syntax: PASS — 20 JSON and 43 YAML files parsed.
- Skill-fleet verification: PASS — all 21 required skills exist in all seven target roots; generated manifest contains 21 skills and 7 agent targets; LangGraph import available; workflow Python syntax passes.
- Independent sandbox verification: PASS — OpenHands, DSH, OpenCode, and Hermes sandbox images exist; OpenHands Python and OpenCode Node smoke tests pass; required sandbox configuration/plugin files are present.
- `git diff --check`: PASS for Ai-Agent-Skill, All-in, and ai-agent-stack.

### Agent API compatibility
`All-in/tests/verify_agent_api_compat.sh`: PASS.
- Authenticated LiteLLM gateway and OpenHands bridge model catalogs returned HTTP 200 with five expected aliases.
- Unauthenticated model-catalog requests were rejected.
- Hermes, DSH, OpenHands, OpenCode, and Claude Code settings match the intended gateway/bridge configuration.
- OpenHands live container has the expected model/base URL/key configuration and can reach the bridge.
- Cline's existing OpenAI-compatible provider remains configured.
- OpenWebUI's 14 existing provider connections remain intact.
- The duplicate Docker LiteLLM proxy remains stopped; the systemd LiteLLM gateway is canonical.
- This test does not by itself prove successful model generation or agent tool use.

### Real inference and tool use
A separate authenticated `/v1/chat/completions` request through `my-model` returned HTTP 200 and the expected answer after increasing `max_tokens` to 128. Runtime was approximately 46 seconds. The initial 8-token probe returned an empty content field with finish reason `length`; the follow-up probe passed. This demonstrates generation, but the latency is a performance item to investigate.

A follow-up function/tool-calling E2E probe was started against a harmless local addition tool, but it did not produce output within the bounded observation window and was terminated to avoid leaving a long-running test process. Tool-call execution therefore remains unverified; do not treat model-catalog success or ordinary text generation as proof that agent tools work.

### VPS services and endpoints
`deploy/verify-current-vps.sh`: PASS — 9 checks passed, 0 failed.
- `litellm.service`
- `openhands-litellm-bridge.service`
- `hermes-api.service`
- `dsh-agent.service`
- `agent-docker-port-guard.service`
- LiteLLM readiness, OpenHands local UI, and Qdrant health returned HTTP 200.
- 21 canonical skill definitions detected.

### Network exposure and cleanup
- `agent-docker-port-guard.service` is enabled and active; systemd logs report rules applied on public interface `ens3` for new TCP connections to Docker original destination ports 3000, 3001, and 33601. External-network reachability was not tested, so public blocking is not yet independently proven.
- Qdrant Compose ports 6333/6334 are bound to loopback for future Compose recreations; existing containers were not recreated by the repository change.
- Docker builder cache cleanup completed and reclaimed 4.456 GB. Root filesystem improved from 87% used / 42 GB free to 86% used / 46 GB free.
- Remaining reclaimable Docker images (about 36 GB) and volumes (about 3.73 GB) were intentionally retained because they may contain rollback/sandbox images or persistent data. No broad image/volume prune was performed.

## Remaining verification gates

1. Complete one bounded agent tool-use task through the normal agent interface and capture a successful tool result.
2. Test the public interface from an external network to confirm the Docker port guard blocks 3000/3001/33601 while Tailscale access remains functional.
3. Investigate the `my-model` inference latency (~46 seconds).
4. Resolve the pre-existing `ai-agent-fleet` `swe-agent-src` gitlink deletion only after confirming whether the submodule should be restored; preserve its current worktree until then.
5. Reassess reclaimable images/volumes individually before deleting any of them.

No provider secrets are recorded in this report.
