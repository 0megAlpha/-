# Recovery / Tool Audit — 2026-10-03

## Disk conclusion
The 246G used on / is not simply Agent source code.

Large verified areas:
- /opt/qwen38-runtime: 27G — local Qwen model/runtime assets.
- /opt/army: 6.3G — Agent/skill/free-api/Hermes/red-team/venv collection.
- /opt/ai-arsenal: 6.1G — Python environment/tool arsenal.
- /root/opencode: 2.7G.
- /root/flowise-LLM: 2.7G.
- /root/-cuga-agent-: 2.6G.
- /root/hermes-007: 2.0G.
- /root/.dsh: 1.5G.
- /root/.cache: 7.1G.
- /root/.local: 8.6G.
- /root/.npm: 1.2G.
- /tmp: 4.6G.
- /var/lib/docker: 3.7G.
- /opt: 41G total.
- /usr/local: 19G total.

No individual file larger than 1G was found under /root by the large-file scan.

## Recovered Freebuff material
The old Freebuff bootstrap and archive still exist as recovery evidence. The active freebuff-daemon.service was disabled and stopped; its files were not blindly deleted.

Useful workflow material recovered:
- spec-driven development
- multi-model routing
- security audit
- dependency update
- agent orchestration

These are now provider-neutral skills under skills/recovered-from-freebuff/.

## Deleted-history review
Intentional deletion categories found in Git history:
- embedded gitlinks/sub-repositories
- OpenHands source separation
- red-team bundles excluded for sanitization
- vendor-policy plugin removals
- stale session/harness artifacts

They were not blindly restored.

## Upstream integration snapshot review
The remote integration snapshot contained three substantial OpenWebUI plugins that passed source-level review and compile checks:
- multi_model_council.py
- parallel_tools.py
- sub_agent.py

Six other snapshot paths contained literal 404: Not Found placeholder content and were excluded.

A separate NVIDIA test file contained a hard-coded API credential and was deliberately not imported. The current tree passes the local secret-pattern scan.

## Runtime inventory
Present:
- OpenCode
- Goose
- Aider
- Kilo / KiloCode
- Crush
- Ollama
- Continue
- DSH
- OpenHands
- Hermes
- Lody
- Cline
- OpenWebUI
- Conduit

Not present as global commands:
- mini
- sweagent

They are documented rather than silently installed into the production runtime.

## Security changes
- AGENT//THRONE is localhost-only on 127.0.0.1:8787.
- Its bridge exposes only read-only observations plus an optional provider adapter.
- The service is systemd-managed with filesystem/network/capability hardening.
- Generic public UFW access to OpenHands port 3000 was removed; the existing Tailscale interface allowance remains.
- Generic UFW rules for unused 4000 and 8888 were removed.
- No hidden persistence or anti-defense behavior was added.
