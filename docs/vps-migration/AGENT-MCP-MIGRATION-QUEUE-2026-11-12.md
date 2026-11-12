# Agent / MCP migration queue — 2026-11-12

Destination for all sanitized, verified deliverables: 0megAlpha/- (branch vps-mirror/full-tree). Do not restore or depend on any former GitHub account. Do not create listeners or publish new ports.

## Migration order

| Priority | Source | Current condition | Required gate before import |
|---|---|---|---|
| P0 | /home/xiaye/agent-os-portable | Portable core merged into destination | CI run, real LiteLLM integration test |
| P1 | /home/xiaye/Ai-agent-skill | Dirty tree; previous Gitleaks findings | Classify 36 findings; verify remotes; test; redact |
| P1 | /home/xiaye/openhands-extensions | Git reports bad object HEAD | Recover source from working files/upstream; validate 0 findings; preserve origin history where possible |
| P1 | /home/xiaye/hermes-007 | 22 commits behind at prior inspection; staged/unstaged/untracked docs | Reconcile upstream; classify 816 scanner findings; protect .env and credentials; run tests |
| P1 | /home/xiaye/CKA-Agent | Dirty config and backup; 3 scanner findings | Review config and backup; remove real credentials from staged content; tests |
| P1 | /home/xiaye/Claude-code | Dirty .gitignore; 3 scanner findings | Review test fixtures vs live secrets; verify project origin and tests |
| P1 | /home/xiaye/repository/Google-AI | Nested repo/submodule, staged additions/deletions, 6 findings | Reconcile .gitmodules, nested OpenHands core, deletions and secret findings |
| P1 | /opt/agent-plane | Root-owned/dirty compose and Caddy files | Inspect as owner; redact configs; validate Compose; no live reconfigure |
| P1 | /opt/agents/- | ~14 GB deployment tree; dirty compose/config; .env present | Export only source/config templates; exclude volumes, .env, databases and model files |
| P1 | /opt/ai-stack | Git index inaccessible to SSH user; .env present | Inspect with proper file ownership; exclude .env; test |
| P2 | /home/xiaye/ai-agent-fleet | ~1.1 GB; project identity pending | Classify project structure, scan secrets, determine nested repos |
| P2 | /home/xiaye/All-in | ~912 KB; .env present; staged .env.example deletion | Restore intended template from safe source; verify placeholder-only; scan and test |
| P2 | /opt/dify | Upstream source; existing production deployment | Keep upstream source separate from local config/secrets; do not alter runtime |
| P2 | /opt/llama.cpp | Upstream source; staged vocabulary deletions reported | Reconcile staged deletions; exclude model weights and generated artifacts |
| P2 | /opt/openhands-upstream-build-v1.25.0 | Upstream build; staged sample deletion and .gitignore changes | Reconcile sample/config; scan and test |
| P2 | /usr/local/lib/hermes-agent | Installed source tree; root-owned | Export verified source/patches only; preserve installed runtime |
| P3 | freebuff-project, bot, game, result, /opt/openwebui-plugins, /opt/sentinelx-python, /opt/agent-throne-file-center, /opt/dsh-sandbox, /opt/free-api, /opt/frp, /opt/eni-register, /opt/*-sandbox | Additional projects | Classify, inventory dependencies, scan secrets, test, then migrate |

## Exclusions

Never commit: .env files, private keys, access tokens, cookies, user databases, runtime volumes, model weights, caches, virtualenvs, node_modules, logs, backups, generated binaries or unreviewed archives. Preserve original project history and do not force-push. For each migrated project, record source, destination path, branch, commit SHA, excluded paths, scanner output, test command/result and remote SHA verification.

## Runtime remediation queue

- Dify agent_backend and local_sandbox restart loops.
- Exa MCP restart loop.
- SentinelX Core, THRONE HUD, llama-agent and llama-agent-fast systemd restart loops.
- LiteLLM health endpoint connection reset.
- Lody device authorization and iOS Conduit pairing.
- Shellway host offline; SentinelX enrollment not yet completed.
- Vercel team scope requires renewed team consent; Termalin host operations require Pro.
