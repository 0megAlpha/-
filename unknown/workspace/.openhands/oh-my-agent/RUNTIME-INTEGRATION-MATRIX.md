# Runtime Integration Matrix — 2026-10-13

## Executive status

**PARTIAL — do not report complete.** Production OpenHands remains on the legacy `ai-agent-snapshots/openhands-pre-api:20261009-053318` image. An isolated Agent Canvas Canary now proves the MCP server's JSON-RPC initialize, 8-tool inventory, provider probe, and system status. The real UI new-conversation tool invocation, Mem0, complete plugin/skill validation, restore rehearsal, and production upgrade remain open.

## Current verified state

- Termalin host `greencloud-ai` is online; Remote Desktop Commander device ping succeeds.
- Ubuntu 26.04.1 LTS; root disk 310 GB total, ~263 GB used, ~47 GB free (about 85% used).
- Repo `/opt/open-hands-integrated-main` is clean on `main` at `486cac2e783d10a181486e2ea97c3c9548313c0f`.
- PR #56 merged. Fix permits sensitive HTTP only to loopback or explicitly allowlisted hosts and bypasses environment/system proxies for sensitive plaintext requests. Unit tests 22/22 pass; Python 3.10 and 3.13 CI plus catalog-integrity CI pass.
- PR #47, #48, #50, #56 in `open-hands` and PR #6 in `Ai-Agent-Skill` are merged. `All-in` PR #6 is also merged after fixing an unused import and pytest import-path failure (CI green). `All-in` PR #4 and `ai-agent-stack` PR #3 remain open.
- Production OpenHands health HTTP 200; Canvas staging 8001 HTTP 200; original Canary 8003 HTTP 200; isolated MCP Canary 8004 HTTP 200. Production was not restarted/upgraded.
- Production provider `/models` endpoint responds HTTP 200 and returns 5 models; configured model is present.
- Isolated MCP Canary `openhands-canvas-mcp-canary-20261013` is loopback-only at `127.0.0.1:8004`, uses copied state/projects, and has provider env injected only into this isolated test container.
- Direct MCP JSON-RPC: initialize succeeds; tools/list returns `system_status`, `provider_probe`, `skills_list`, `skill_draft_create`, `memory_search`, `memory_store`, `upstream_status`, `promotion_check`. Provider probe HTTP 200, 5 models. `promotion_check` remains fail-closed; no automatic promotion/deployment.
- Shared workspace contains 134 skill directories; all have a non-empty root `SKILL.md`. A static quality inventory found 94 with YAML-style frontmatter, 40 without frontmatter, 57 under 500 bytes, 71 with README files, and 132 directory names mentioned in `SOURCES.md`. This does not prove correctness, licensing, dependencies, or executability. Audit file: `/root/workspace/.openhands/oh-my-agent/SKILL-QUALITY-AUDIT-20261013.md`.
- Repo has 12 plugin directories; these are not 12 proven runtime-installed plugins. `oh-my-agent` is the verified Python stdio MCP implementation.
- Qdrant responds HTTP 200. No `MEM0_URL`/`MEM0_API_KEY` or running Mem0 service was found; Mem0 search/store is not verified.
- Pethost reports no machine/plan for this account, so its deployment operations are unavailable. Brainbase has an organization and General team, but no managed agents or orchestrations currently listed.
- Tailscale HTTPS `https://xiaye.taila052da.ts.net:8444/` returns HTTP 200 with TLS verification result 0; nginx is active and `nginx -t` passes. Docker publishes `new-api` on 0.0.0.0/[::]:3001 and the Invariant server on 0.0.0.0/[::]:33601; matching IPv4 and IPv6 `DOCKER-USER` rules drop new inbound connections arriving on `ens3` to these ports (counters show drops). These services still listen on wildcard interfaces, so keep firewall rules under monitoring; do not claim the listeners are loopback-bound.
- Existing backup archive is readable; an isolated restore rehearsal is not complete.

## Uploaded attachment audit

- `文字 48(1).txt`: 612,102 characters, 4,473 lines. It is a deployment audit emphasizing evidence-based statuses and separating merged source from deployed runtime.
- `文字 49(1).txt`: 29,637 characters, 1,068 lines. It claims 270 entries (Hermes 70, DSH 70, OpenWebUI 70, OpenHands 60), but the actual supplied text does not provide a verifiable, complete 270-item unique install catalog with per-item official source, pinned ref, compatibility, test and rollback evidence. Treat 270 as the document's claim, not a verified install count. Do not execute every name blindly; first build a source/provenance/compatibility matrix. The OpenHands package command line itself includes both `open-handhands-ai` and a comment saying `openhands-ai`, so that command requires upstream verification before use.

## Remaining acceptance gates

1. Verify MCP tools are available and callable in a real new UI conversation; current success is JSON-RPC/process-level, not full conversation E2E.
2. Configure/verify a supported Mem0 backend or formally select and test a compatible alternative; Qdrant alone is not proof of Mem0 API compatibility.
3. Build a 270-candidate manifest with official URLs, unique item names, version/SHA, license, dependencies, target platform, installation, tests, permissions and rollback. Reject unverified candidates from production.
4. Validate each of the 12 plugin directories and each skill's provenance/content/dependencies; do not equate directory presence with installation.
5. Run cross-agent handoff tests for each intended runtime.
6. Perform isolated backup restore and validate persistence.
7. Prepare supported production image upgrade/state migration/rollback; deploy only after Canary acceptance.
8. Reassess disk capacity before pulling large images/models; do not perform indiscriminate cleanup.
9. Pethost remains blocked by account machine/plan; Brainbase currently has no agents/orchestration to connect.

## Completion rule

Do not report “all integrated” until production MCP UI invocation, provider inference, persistent memory, cross-agent handoffs, restore rehearsal, plugin/skill validation, and supported production rollout all pass. No production restart or upgrade has been performed in this audit.
