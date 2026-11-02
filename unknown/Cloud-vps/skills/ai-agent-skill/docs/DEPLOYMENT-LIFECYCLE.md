# Deployment Lifecycle
## Initial
The VPS accumulated Agent runtimes, skills, plugins, workspaces, exports and duplicate Ai-Agent-Skill checkouts.

## Repair rule
Ai-Agent-Skill is not a source-repository merger. OpenHands, Hermes, DSH, OpenCode and other source repos remain independent.

## Deleted-data audit
Git deletion history was inspected. Removed paths included embedded gitlinks, separated OpenHands content, red-team bundles excluded for sanitization, vendor-policy plugin removals and stale session/harness artifacts.

These are not blindly restored. A deleted path is recovered only if its function is useful, compatible with current boundaries and safe to track.

## Freebuff recovery
The legacy Freebuff bootstrap contained useful generic workflows: spec-driven development, multi-model routing, security audit, dependency update and agent orchestration. Those were rewritten under skills/recovered-from-freebuff/ without Freebuff-specific commands or hidden runtime assumptions.

The old watcher mainly emitted heartbeat/security-scan logs. It is not promoted as a hidden persistent Agent. Observability now belongs to named, stoppable services and AGENT//THRONE.

## Final chain
source repos -> adapters -> skills/tools/MCP/ACP -> isolated workspace/session -> workflows -> AGENT//THRONE -> human acceptance.

## Reproducibility
No secrets in Git. Provider/model choices are configuration. Background jobs are observable and stoppable. No anti-defense behavior.## Recovered deployment inventory
The archived fleet bootstrap also identified useful coding/tooling components:
- OpenCode, Goose, Aider, Kilo/KiloCode, Crush, Ollama, Continue
- mini-SWE-agent and SWE-agent
- CrewAI + LangGraph
- Superpowers skills

Current quick availability check: OpenCode, Goose, Aider, Kilo, Crush, Ollama, Continue and KiloCode are present. mini and sweagent are not currently installed as global commands. Their absence is recorded rather than silently installing new production runtimes.

The archived Freebuff watcher is not re-enabled. Its useful workflow documents were recovered into provider-neutral skills.

## Browser / mobile access
AGENT//THRONE binds to 127.0.0.1:8787. Use an SSH tunnel for mobile:
ssh -L 8787:127.0.0.1:8787 <user>@<vps>
then open http://127.0.0.1:8787/.

OpenHands currently listens through its existing container on port 3000. Public UFW access to 3000 was removed; the existing Tailscale interface rule remains. This keeps the runtime available through the private overlay without leaving the port generally exposed.

The systemd unit is reproducible at deploy/systemd/ai-agent-throne.service.
