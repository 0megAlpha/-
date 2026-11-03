# OH-MY-AGENT MCP end-to-end verification — 2026-10-12

## Verified runtime
- Runtime checked: `openhands-canvas-staging`.
- MCP settings file: `/home/openhands/.openhands/settings.json` inside that container.
- OpenHands SDK version: 1.40.1.
- `create_mcp_tools` loaded the configured `oh-my-agent` server and reported `Created 8 MCP tools`.
- Tool names observed: `system_status`, `provider_probe`, `skills_list`, `skill_draft_create`, `memory_search`, `memory_store`, `upstream_status`, `promotion_check`.

## SDK call results
- `system_status`: PASS. Plugin `oh-my-agent`, version `0.1.0`, `draft_only=true`, `automatic_promotion=false`, `provider_configured=false`.
- `skills_list` with limit 5: PASS; returned 5 skill entries.
- `promotion_check` with all supplied evidence flags set true: tool call succeeded but `allowed=false`, consistent with fail-closed promotion gating.

## Not verified / blockers
- Provider probe is not configured: the MCP subprocess does not receive `LLM_BASE_URL` / `LLM_API_KEY`; no secret was copied into the plugin environment.
- Mem0 endpoint is not configured, so `memory_search` / `memory_store` are not yet proven against a persistent Mem0 service.
- This proves SDK tool registration and calls inside `openhands-canvas-staging`, not inside the separate primary `openhands` container.
- The primary `openhands` container's expected `/home/openhands/.openhands/settings.json` was absent in earlier checks; its live MCP settings source remains unidentified. Do not copy settings or restart the primary container until its configuration and rollback path are confirmed.
- Main OpenHands health endpoint returned HTTP 200; its container port is bound to loopback. The authenticated reverse-proxy route returned HTTP 401, consistent with an auth gate.

## Safety posture
- No automatic skill installation, promotion, GitHub merge, deployment, container restart, or firewall change was performed as part of this verification.
- A separate live port audit remains open for Docker-published ports 3001 (new-api) and 33601 (openhands-invariant-server), which are bound to all IPv4/IPv6 interfaces. External reachability was not independently verified.