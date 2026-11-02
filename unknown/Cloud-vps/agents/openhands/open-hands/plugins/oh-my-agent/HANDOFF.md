# OpenHands / oh-my-agent — recovered task handoff

Date: 2026-10-11 (VPS local time)

## Completed and verified
- PR #46 merged into feature branch feat/oh-my-agent-secure-integration-20261011.
- PR #45 merged into private repository xh09411-web/open-hands main.
- Main commit: 474194b435c06df40c7c164fd8ec3c575fc3164d.
- VPS checkout /root/open-hands fast-forwarded to main. Existing untracked .agents/skills/* were preserved and not staged.
- Plugin source deployed into active OpenHands Canvas persistent volume /home/openhands/.openhands/plugins/oh-my-agent.
- Added enabled stdio MCP entry oh-my-agent to /home/openhands/.openhands/settings.json. Total MCP server entries: 11. Existing entries preserved.
- Rollback backup: /home/openhands/.openhands/settings.json.bak-oh-my-agent-20261011 (mode 0600).
- Security fixes cover cross-origin redirects with Authorization, plaintext HTTP credential/data transport, oversized/invalid JSON responses, malformed JSON-RPC, runtime schema validation/unknown arguments, secret-like memory metadata, restrictive draft creation, and fail-closed missing promotion evidence.
- Validation on VPS main: python -m unittest discover -s tests -p test_oh_my_agent.py -v — 15 tests passed; compileall passed; git diff --check passed.
- OpenHands SDK v1.40.1 MCP client connected and discovered 8 tools. Independent initialize/tools/list/system_status smoke tests passed.
- provider_probe and memory_search/store require endpoint/credential configuration; no secrets were copied or exposed.
- Temporary clone /tmp/oh-my-agent-secure and /tmp/ohma-installed removed; pip cache purged.

## GitHub
- PR #45: https://github.com/xh09411-web/open-hands/pull/45 — merged to main.
- PR #46: https://github.com/xh09411-web/open-hands/pull/46 — merged into feature branch before PR #45 was merged.
- Main commit: https://github.com/xh09411-web/open-hands/commit/474194b435c06df40c7c164fd8ec3c575fc3164d

## Web access
- Tailscale Serve names: https://greencloud-ai.taila052da.ts.net/ and https://xiaye.taila052da.ts.net/ (tailnet only).
- OpenHands route: https://greencloud-ai.taila052da.ts.net/openhands/ . Local Caddy returns HTTP 401, consistent with authentication protection.
- VPS-side MagicDNS resolution failed during this check; validate from an online tailnet client. The iPhone peer was offline at last check. Public-IP access has not been validated; 1.2.3.4 is not confirmed as a real address.

## Cleanup decisions
- Preserved /tmp/ai-migration/ai-company-backup.tar.gz (~4.9 GB) and its SHA-256 file: dated backup, not disposable cache.
- Preserved 3.7 GB of shared tool/browser caches outside the pip cache because deleting them may break workflows or trigger large re-downloads.
- Preserved untracked .agents/skills/* in /root/open-hands; they are user/project data and were not reviewed for deletion.

## Other integrations
Remote Desktop Commander and GitHub were used for this task; web research informed OpenHands MCP setup. Code/Codex workflow, Agent Reach, Hey Terminal, and Figma are ChatGPT-side integrations and are not automatically installed into OpenHands. Each requires a supported MCP/API adapter and authorized credentials before it can be integrated into the VPS runtime. No credentials were copied or exposed.

## Remaining checks
1. Open the Tailscale URL from an online tailnet client and confirm browser access.
2. Start a new OpenHands conversation so it loads the updated MCP settings, then verify the 8 oh-my-agent tools are exposed in the UI.
3. Configure provider/Mem0 endpoints and secrets only if those optional tools are required.
4. If public-IP access is required, confirm the actual VPS public IP and establish a secured public HTTPS route rather than exposing the placeholder 1.2.3.4.

## Follow-up verification (2026-10-11)
- RDC primary device reconnected; ping passed.
- Re-ran 15 `test_oh_my_agent.py` tests: all passed. OpenHands SDK v1.40.1 connected and discovered 8 MCP tools; direct `system_status` and `skills_list` calls passed.
- The plugin MCP env does not inherit the LLM base URL/API key already present in OpenHands settings; no key was copied. Mem0 is not configured (the existing `memory` MCP is generic server-memory). Tool responses correctly report unavailable rather than pretending success. Temporary draft-create verification artifact was removed.
- `/canvas/` returns 200 locally; protected Caddy `/openhands/` returns 401 Basic-auth challenge. Authenticated tailnet browser/new-conversation visibility is still pending.
- See `INTEGRATION-INVENTORY.md` for account resource inventory. No service restart or unrelated data deletion was performed.
