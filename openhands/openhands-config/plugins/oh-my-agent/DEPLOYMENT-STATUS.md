# oh-my-agent deployment status

- Source: private repository xh09411-web/open-hands main, merge commit 474194b435c06df40c7c164fd8ec3c575fc3164d.
- Plugin source deployed into the active OpenHands Canvas persistent volume at /home/openhands/.openhands/plugins/oh-my-agent.
- Registered in /home/openhands/.openhands/settings.json under agent_settings.mcp_config as an enabled stdio server. Total configured MCP servers: 11; the prior 10 were preserved.
- A mode-0600 rollback backup was created at /home/openhands/.openhands/settings.json.bak-oh-my-agent-20261011.
- OpenHands SDK v1.40.1 MCP client successfully connected and discovered all 8 plugin tools. Independent stdio initialize, tools/list, and system_status smoke tests passed.
- No credentials were copied into the plugin. provider_probe requires LLM_BASE_URL plus LLM_API_KEY/OPENAI_API_KEY; memory_search/store require MEM0_URL and optionally MEM0_API_KEY. These tools return explicit unavailable/not-configured responses until secrets and endpoints are configured through the supported secret store.
- Skill drafts are written only under the plugin's drafts directory, which is mode 0700; created draft files are mode 0600. Promotion remains manual-only and fail-closed.

## Web access
- Tailscale Serve names: https://greencloud-ai.taila052da.ts.net/ and https://xiaye.taila052da.ts.net/ (tailnet only, proxy to localhost:8443).
- OpenHands route: https://greencloud-ai.taila052da.ts.net/openhands/ . Local Caddy returns HTTP 401, consistent with authentication protection.
- The VPS could not resolve its own Tailscale MagicDNS hostname during this check, so HTTPS reachability from the VPS itself was not confirmed. The URL must be tested from a connected tailnet device. The iPhone peer was offline at last check.
- Public-IP access has not been validated; do not treat 1.2.3.4 as a real server address.

## Validation
- VPS main branch: 15 unit tests passed; compileall passed; git diff --check passed.
- OpenHands SDK: MCP client connected and listed 8 tools.
- Resource sample after cleanup: 25 GiB memory available, 55 GiB disk available (83% used).
- Temporary clone /tmp/oh-my-agent-secure and /tmp/ohma-installed were removed. Pip cache was purged. The dated 4.9 GB migration backup and shared browser/tool caches were preserved as potentially useful data.

## Follow-up verification (2026-10-11)
- Reconnected to the primary Remote Desktop Commander device; ping passed. Two older registered devices remain offline.
- Re-ran `python -m unittest discover -s tests -p 'test_oh_my_agent.py' -v`: all 15 tests passed.
- OpenHands SDK v1.40.1 MCP client connected and discovered all 8 tools. Direct MCP `system_status` and `skills_list` calls succeeded; promotion check rejects missing evidence as expected.
- Temporary draft-create path was exercised and the test draft was removed after verifying its mode.
- Current runtime status is explicitly partial: no provider base URL/key and no Mem0 URL are configured. Those tools report unavailable rather than simulating success.
- Local `/canvas/` returned 200; Caddy `/openhands/` returned 401 Basic-auth challenge. Tailnet browser and new-conversation UI visibility remain unverified.
- See `INTEGRATION-INVENTORY.md` for the connected-provider/resource audit and outstanding blockers. No service restart was performed.
