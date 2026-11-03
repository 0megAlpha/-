# Integration inventory and verification

Checked: 2026-10-11 (VPS local time). This file distinguishes successful connection tests from accounts that lack deployable resources.

## OpenHands / oh-my-agent

- Repository `xh09411-web/open-hands`, branch `main`, commit `474194b435c06df40c7c164fd8ec3c575fc3164d`.
- PR #45 and PR #46 are merged. GitHub's commit-workflow query returned no PR-triggered workflow runs for the merge commit; this is not evidence of CI success or failure.
- VPS unit tests: `python -m unittest discover -s tests -p 'test_oh_my_agent.py' -v` — 15 passed. `compileall` and `git diff --check` had passed in the earlier validation run.
- Plugin installed at `/home/openhands/.openhands/plugins/oh-my-agent` in `openhands-canvas-staging` persistent volume.
- Active settings file `/home/openhands/.openhands/settings.json` is valid JSON, mode 0600, and contains 11 MCP entries. `oh-my-agent` is enabled with stdio transport. The pre-change rollback backup exists at `/home/openhands/.openhands/settings.json.bak-oh-my-agent-20261011`.
- OpenHands SDK v1.40.1 MCP client connected and discovered all 8 tools: `system_status`, `provider_probe`, `skills_list`, `skill_draft_create`, `memory_search`, `memory_store`, `upstream_status`, `promotion_check`.
- Raw MCP JSON-RPC `initialize`, `tools/list`, `system_status`, and `skills_list` succeeded. `promotion_check` rejected missing evidence fields as expected (fail-closed). A temporary draft was created with `draft_not_installed` status and then removed after checking its permissions; no test artifact remains.
- `system_status` reports `provider_configured=false`, `provider_base_url_set=false`, and Mem0 `not_configured`. `provider_probe` reports `provider_base_url_not_configured`; `memory_search` reports `MEM0_URL_not_configured`. The OpenHands `agent_settings.llm` object does contain a base URL and API key, but those values are not inherited by the plugin MCP environment; I did not copy or expose the existing key. To activate provider probing, the provider settings need an explicit, deliberate mapping into the plugin environment or a supported secret reference. The existing `memory` MCP entry is the generic `@modelcontextprotocol/server-memory`, not a Mem0 REST endpoint, so `oh-my-agent` memory_search/store remain unavailable until an adapter or Mem0 endpoint is configured.
- Local Canvas UI route `/canvas/` returned HTTP 200. Caddy `/openhands/` returned HTTP 401 with a Basic-auth challenge; that is consistent with a protected route, but authenticated browser/new-conversation visibility has not been verified from an online tailnet client. VPS-side MagicDNS lookup was not confirmed.
- Existing untracked `/root/open-hands/.agents/skills/*` were preserved; no production container restart was performed.

## Connected provider/resource inventory

- GitHub: connected; PR #45 and #46 merged.
- Remote Desktop Commander: primary `greencloud-ai` device online and ping successful; two older registered devices offline.
- Vercel: connection responds, but project and deployment lists are both empty. No deployment target exists in this account scope.
- Base44: one existing app named `Remote Desktop Commander`; left unchanged.
- ProductOS: no projects in granted organizations.
- Val Town: authenticated handle has zero vals.
- BasicDeploy: authenticated Free account, zero containers.
- Gateway: zero servers.
- SentinelX: zero enrolled hosts; no remote host operations possible until enrollment.
- Pethost: no machine/plan is configured.
- Brainbase: one personal organization and default General team, but zero managed agents.
- aictrl.dev: one personal organization, zero published workflows.
- Codex Tasks: zero registered environments and zero recent durable tasks.
- Codelit: public planning-template catalog is available; it does not expose account-specific drafts or execute deployments.

## Not yet integrated / blockers

The labels Founder Pulse, Develoop, Smart Model Router, Plugin Autopilot, Codex Engineering Guardrails, ECZ-ID API Trust, Vibe Coder, Runpod (Official), Blog Generator, Modal, Voice Notify for Codex, SQL Expert, and PR Completion did not map to callable connector namespaces in this session. Some may be product labels or ChatGPT-side workflows rather than installable VPS services. No unsupported adapters, accounts, credentials, or projects were fabricated.

Remaining external checks: authenticate from a connected tailnet browser, open a new OpenHands conversation and confirm tool visibility, configure provider/Mem0 endpoints if desired, and create/authorize actual deployment targets before deploying to Vercel/other hosting accounts.
