# OpenHands Integration Status — 2026-10-12 23:xx +0800

## Status: PARTIAL — do not report complete

### Verified
- Production `openhands` container remains on `ai-agent-snapshots/openhands-pre-api:20261009-053318`; local health endpoint returns HTTP 200.
- Tailscale HTTPS route was previously verified from the VPS with HTTP 200 and valid TLS. Primary production remains running; no production container restart/upgrade was performed in this session.
- Repository `/opt/open-hands-integrated-main` is synchronized to `origin/main` at `e90a4d8febac45099a32f312b94a6557c958f793`; working tree clean.
- PR #54 was merged as `e90a4d8febac45099a32f312b94a6557c958f793`; it broadens Authorization header redaction and preserves instructions after an empty Authorization heading.
- Local OH-MY-AGENT test suite: 19/19 passed; compileall passed; `git diff --check` passed. GitHub Actions on PR #54 passed both Python 3.10 and 3.13 unit test jobs and catalog integrity jobs.
- Production workspace mount `/opt/workspace_base/.agents/skills` contains 134 skill directories, all with a root `SKILL.md`; 20 previously missing skills were copied from the pinned, clean `/root/AI-Agent-Skill` checkout (commit `39112117be17b67b40944681e753ac9ed7dd5091`) or the canonical OpenHands repository. Existing skill folders were not overwritten.
- Isolated Agent Canvas canary `openhands-canvas-canary-20261012` is running on `127.0.0.1:8003`, health HTTP 200. It has a persistent isolated settings/project mount and an enabled `oh-my-agent` stdio MCP config. The canary MCP process initializes and exposes 8 tools: `system_status`, `provider_probe`, `skills_list`, `skill_draft_create`, `memory_search`, `memory_store`, `upstream_status`, `promotion_check`. `skills_list` returns 134 skills and all listed roots have `SKILL.md`.
- Direct canary MCP calls passed for initialization, tool listing, system status, skill inventory, and fail-closed promotion check. The fail-closed tool correctly never authorizes automatic promotion/deployment.
- A fresh backup was created after the workspace skill sync; archive and configuration snapshots were checked for readability/existence. TLS private material is included in the protected backup and must not be exposed.

### Still not verified / blockers
- The current conversation's file inventory includes only `IMG_2685.png` plus generated handoff files. The image is a black mobile browser screen with the public IP in the address bar, not the two source documents described as uploaded this morning and tonight. Their contents cannot be integrated or verified until those original files are available in this conversation/VPS.
- Production OpenHands container is still the older pre-API image and does not include `openhands.sdk` or the `mcp` package. The 8-tool MCP server is verified only in the separate canary, not in the production conversation UI.
- The canary reports provider URL/key not configured in its MCP process, and Mem0 not configured. Do not claim provider probe or memory search/store end-to-end success.
- Authenticated conversation-level MCP tool visibility has not been verified; the unauthenticated tools catalog returns 401. Direct MCP stdio tests do not prove the UI agent registered the tools.
- The 134 skills are visible as files through the shared production workspace mount and to the canary inventory tool. This does not prove every skill is semantically correct, all external dependencies exist, or all separate agent runtimes can invoke them.
- The separate invariant server still publishes port 33601 on all interfaces; its access policy must be audited before claiming host-wide security.
- Backup restore rehearsal, model/provider live probe, Mem0 integration, browser login/new conversation verification, and full multi-agent handoff tests remain pending.

## Next required acceptance gates
1. Obtain and hash/parse both original user documents (morning and evening); map each requested agent/tool/skill/plugin to an installed path and test.
2. Complete authenticated canary UI test and prove MCP tools appear in an actual new conversation, not only via direct stdio.
3. Configure/verify provider in a controlled test runtime without printing credentials; configure Mem0 or explicitly mark memory integration unavailable if no endpoint exists.
4. Build a supported production upgrade/rollback plan, test persistent-state migration and restore, then roll out only after canary acceptance.
5. Run cross-agent handoff tests for every runtime the user expects to use; maintain per-runtime capability matrix (skills, MCP, plugins, model, memory, GitHub auth, permissions).
6. Review public listener/firewall policy and validate from a connected Tailnet client.
7. Final report may say complete only when all required gates pass; otherwise explicitly list blockers.
