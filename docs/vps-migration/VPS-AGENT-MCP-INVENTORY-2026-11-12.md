# VPS Agent / MCP / Deployment Inventory — 2026-11-12

> Snapshot captured from read-only inspection. This report is an inventory, not a declaration that migration or deployment is complete. No service was stopped, restarted, disabled, or deleted. No listener or firewall port was added.

## GitHub destination

- Authenticated owner: `0megAlpha`
- Destination repository: `0megAlpha/-`
- Destination branch: `vps-mirror/full-tree`
- Visibility at inspection: **Public**
- Existing repository is large; do not treat this repository as private.
- Only one repository was returned in the authenticated account's first 100-item listing.
- Old remotes were found in local working trees. The old account's private repositories and permissions have not been independently verified.

## Host and storage snapshot

- Hostname: `greencloud-ai`
- OS: Ubuntu 26.04, x86_64
- Docker: 29.1.3; Podman 5.7.0; Docker Compose v5.6.0
- Root filesystem: 310 GB total, 273 GB used, 38 GB available (88%)
- Inspection user: `xiaye`
- No service changes were made.

## Project roots discovered

### Home projects

- `/home/xiaye/Ai-agent-skill` — agent skills, plugins, MCP server definitions, OpenCode MCP registry; local modifications in `.gitignore` and `push.sh`; remote points to old account.
- `/home/xiaye/All-in` — orchestrator / compose deployment; several tracked modifications and `.env.example` deletion staged; remote points to old account.
- `/home/xiaye/CKA-Agent` — Kubernetes agent/security project; modified `.gitignore` and `config/config.yml`; untracked `config/config.yml.bak`; remote points to Graph-COM.
- `/home/xiaye/Claude-code` — AgentSys collaboration project; modified `.gitignore`; remote points to old account.
- `/home/xiaye/hermes-007` — Hermes CLI/TUI / messaging integration; branch master was 22 commits behind origin at inspection; `.env.example` had staged deletion and untracked replacement; secrets documentation directories untracked; remote points to old account, upstream is NousResearch.
- `/home/xiaye/openhands-extensions` — OpenHands extensions; remote `0megAlpha/openhands-extensions` exists in config, but local Git reports `fatal: bad object HEAD`; cannot safely commit/push until repository metadata is repaired.
- `/home/xiaye/repository/Google-AI` — large Google-AI/OpenHands aggregate with nested `openhands-core` and submodule metadata; thousands of staged/removed paths were reported in prior inventory; remote points to old account. Do not bulk-push until submodule and staged deletion intent is reconciled.
- `/home/xiaye/vps-mirror-workspace` — full-tree mirror workspace; branch `vps-mirror/full-tree`; remotes point to this destination repository. Nested files include a large duplicated/archived collection and some paths are unreadable to the SSH user.
- `/home/xiaye/ai-agent-fleet` — 1.1 GB; repository/project identity still requires classification.
- `/home/xiaye/freebuff-project`, `bot`, `game`, `result` — require project classification before migration.
- `/home/xiaye` itself contains a Git repository with no commits and many untracked personal/configuration paths; it must not be committed as a whole.

### System projects

- `/opt/agent-plane` — Git repository; local modifications include `.gitignore`, `caddy/Caddyfile`, and `docker-compose.yml`.
- `/opt/agents/-` — Git repository for deployed stack; modified LiteLLM and OpenHands compose/config files; remote points to destination repo.
- `/opt/ai-stack` — Git repository, but the SSH user cannot read its Git index.
- `/opt/dify` — upstream Dify repository.
- `/opt/llama.cpp` — upstream llama.cpp repository; model vocabulary files show staged deletions in status output; do not commit those changes without reconciliation.
- `/opt/openhands-upstream-build-v1.25.0` — OpenHands upstream build; staged deletion of `.env.sample` and modified `.gitignore`.
- `/opt/hermes-agent-v0.22.5` and `/usr/local/lib/hermes-agent` — Hermes installation/source trees.
- `/opt/open-hands-integrated-main` — OpenHands integrated tree.
- `/opt/open-webui`, `/opt/openwebui-plugins` — Open WebUI and plugin tree.
- `/opt/sentinelx-cloud-core`, `/opt/sentinelx-python` — SentinelX components; a prior version backup exists under `/opt/.sentinelx-prev.*`.
- `/opt/agent-throne-file-center`, `/opt/dsh-sandbox`, `/opt/free-api`, `/opt/frp`, `/opt/eni-register`, `/opt/agent-sandbox`, `/opt/hermes-sandbox`, `/opt/openhands-sandbox`, `/opt/opencode-sandbox` — additional service or sandbox trees.
- Several trees are root-owned and not fully inspectable by the unprivileged SSH account.

## Running containers observed

Container status and published ports are copied as observed; this report does not modify them.

- `exa-mcp` — restarting
- `mcp-proxy` — running; published 5700
- `open-webui` — healthy; published 3000
- `qdrant` — running; bound to loopback 6333–6334
- `mimocode2api` — healthy; published 8080
- `openhands-canvas` — running; published 8000
- `coolify-db`, `coolify-redis` — healthy
- Dify API / worker / websocket / plugin daemon / web / PostgreSQL / Redis / sandbox / Weaviate components — most running; `agent_backend` and `local_sandbox` restarting
- OpenHands runtime and web — running; web published 13000
- Agents stack: LiteLLM, PostgreSQL, Redis, Qdrant, Mem0, New API — running

## Running systemd services observed

- `agent-throne-file-center.service`
- `docker.service`
- `dsh-agent.service`
- `eni-freeapi-watchdog.service`
- `eni-harbor.service`
- `freeride-relay.service`
- `frps.service`
- `hermes-api.service`
- `hermes-gateway.service`
- `litellm.service`
- `lody-agent.service`
- `redis-server.service`
- `tailscaled.service`
- `termalin-agent.service`

## MCP / plugin ecosystem evidence

- Global Node packages include: `claude-code`, `cline`, `codex`, `context7-mcp`, `desktop-commander`, `dsh`, `gemini-cli`, `mcp-cli`, `notion-mcp-server`, `oh-my-opencode`, `opencode-ai`, `semgrep`, `skills`, `server-filesystem`, `server-github`, `server-memory`, `server-postgres`, `server-puppeteer`, `server-sequential-thinking`, `server-slack`, and others.
- MCP configuration files were found in the agent skills tree and the full-tree mirror, including OpenCode registry and Claude/Cursor plugin definitions.
- Configuration values and credentials were not copied into this report.

## Issues requiring follow-up before safe migration

1. Disk usage is 88%; avoid copying full 14 GB and 18 GB trees without a deduplication plan.
2. Multiple repos point to old account `xh09411-web`; current account authentication is `0megAlpha`.
3. OpenHands extensions has invalid Git HEAD metadata.
4. Google-AI has substantial staged changes, nested repository/submodule content and apparent deletions.
5. Hermes local branch is behind upstream/origin and contains mixed staged/unstaged/untracked changes.
6. CKA-Agent and All-in contain unreviewed local configuration changes.
7. `/home/xiaye` itself is an uncommitted umbrella Git tree and contains private home-directory files; never push it wholesale.
8. Root-owned directories prevented complete inventory under the current SSH identity.
9. No broad credential scan was run against file contents; secret-like file names were observed. A proper content-level secret scan with exclusion rules is still required before any bulk push.
10. Several containers were restarting at inspection. No restart or repair was attempted.

## Migration rules for subsequent work

- Preserve source history and working trees; no force push, history rewrite, destructive clean, or recursive deletion.
- Create a separate destination repository per independent project when appropriate; do not place unrelated projects into one repository.
- Exclude credentials, private keys, tokens, local `.env` files, caches, virtual environments, model weights, build artifacts, logs, backups and runtime databases from Git.
- Keep safe templates such as `.env.example` only after verifying that they contain placeholders, not real credentials.
- Fetch source remotes, compare commit ancestry, reconcile staged/unstaged changes and submodules, run project tests, then push normally.
- Record the source remote, destination repository, branch, commit SHA, excluded paths, validation result and push verification for every project.
- Do not add listeners, publish new ports, alter firewall rules, or restart services during this migration.
