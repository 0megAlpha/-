# VPS / OpenHands execution tracker — 2026-10-12

Scope: deduplicated execution register derived from the two uploaded audit/transcript files (文字 48.txt and 文字 49.txt), this project's available history, and live checks performed on 2026-10-12. The source files repeat several audit lists, so counts below are work packages after deduplication, not a claim that every historical message has been recovered.

## Summary
- 30 deduplicated work packages tracked: 10 verified complete, 20 open or partial.
- Primary runtime is running, but the production container is an older `ai-agent-snapshots/openhands-pre-api:20261009-053318`, build `0.14.3`. It has no `openhands.sdk`, no `openhands mcp` CLI, and no settings file at `/home/openhands/.openhands/settings.json`.
- The 8-tool MCP registration was verified in `openhands-canvas-staging` using SDK 1.40.1 only. This is not production-agent integration.
- PR #49 is marked ready for review and remains open/unmerged. Latest pushed head: `04a5fb0ca8cb5c1b2d237ecbae01bf22a90959ec`; it includes optional `GITHUB_TOKEN` support for upstream metadata probes and Bearer-token redaction in skill drafts.
- No GitHub Actions workflow runs were returned for the current PR #49 head. Copilot review reported quota exhaustion; this is not a successful code review.

## Verified complete (10)
1. OpenHands PR #47 workflow fix merged; merge commit `5d7d6c9d56e58fae9bc59d10a720196f94c5933e`.
2. OpenHands PR #48 shared-skill portability merged; merge commit `51a8bbcf5dcdcaba10baccf9a38f8b304f89d2d4`.
3. OpenHands PR #50 agent/plugin catalog automation merged; merge commit `8005c85103d9d18d76eb7999b2b631bcf8924602`.
4. OpenHands PR #49 plugin code is pushed and marked ready for review; branch includes latest main.
5. PR #49 isolated unit tests passed: 17/17 on Python 3.10, Python 3.13, and host Python 3.14; compileall passed on 3.10/3.13, git diff --check passed, and Gitleaks found no leaks in the plugin directory.
6. Staging SDK discovered all 8 oh-my-agent MCP tools; system_status, skills_list, and fail-closed promotion checks were exercised.
7. VPS watchdog dry-run repair passed syntax, dry-run, and single-run exit-code checks; original script backup retained.
8. System journal retention was bounded to 700 MB / 14 days; vacuum and apt cache cleanup were performed.
9. Live Docker container inventory and disk capacity were rechecked; root filesystem is 310 GB total, 264 GB used, 47 GB free (86%).
10. Aider CLI startup was repaired at pinned version 0.86.2; version/help/import checks passed. This does not mean provider inference works.

## Open / partial (20)
1. **P0 — Production OpenHands MCP:** identify a supported upgrade/migration path from build 0.14.3 to a supported MCP-capable runtime. Do not mutate/restart production until configuration, data persistence, backup and rollback are mapped.
2. **P0 — Production end-to-end:** from an authenticated Tailnet browser, sign in, create a conversation, verify tool visibility, invoke tools, generate a model response, edit a disposable test repo, and prove rollback.
3. **P0 — Provider:** Aider's local-model request is still failing/timing out; verify the intended provider/base URL and real completion path.
4. **P0 — Mem0:** configure a supported endpoint/adapter and test persistent memory search/store; the generic MCP memory server is not automatically a Mem0 REST endpoint.
5. **P0 — Secret exposure:** rotate potentially exposed API/session credentials through supported service procedures; do not paste values into reports or command-line arguments.
6. **P0 — Network boundary:** investigate Docker-published ports 3001 and 33601 (bound to all interfaces); verify host/cloud firewall and external reachability before changing rules.
7. **P0 — PR #49 CI/review:** GitHub Actions returned no runs for current head; Copilot reviewer quota was exhausted. Obtain actual CI evidence and a real review before merge.
8. **P1 — ai-agent-stack PR #3:** still open; inventory/rebuild documentation is not a completed clean rebuild.
9. **P1 — All-in PR #4:** still open; its historical workflow status was action_required and needs a fresh check.
10. **P1 — Ai-Agent-Skill PR #5:** merged, but historical Agent Fleet Verification failed on a PEM-placeholder example; confirm whether fixed and whether current CI passes.
11. **P1 — All-in PR #5:** merged, but historical Orchestrator quality failed on Ruff F401; confirm current main CI and fix if still present.
12. **P1 — Skill source inventory:** audit the 19 untracked skill directories in `/root/open-hands/.agents/skills` for origin, license, version, secrets, compatibility and test results before committing/pushing them. Preserve all untracked content.
13. **P1 — Full repository security scan:** scan worktrees, Git index and history; verify ignore rules and record exceptions without exposing secret values.
14. **P1 — Backup evidence:** checksum critical backups and test a restore into an isolated location; preserve the 4.9 GB migration backup and all rollback assets.
15. **P1 — Clean Linux rebuild:** execute the documented rebuild in isolation, restore persistent data, and run smoke tests; currently unverified.
16. **P1 — Tailscale/iPhone:** verify MagicDNS, TLS, Basic Auth and the OpenHands/Canvas routes from an online Tailnet client; mobile-to-VPS task execution is not yet accepted.
17. **P1 — Documentation truthfulness:** correct older deployment notes that claimed the primary container had a settings file/MCP registration; live inspection found those paths absent in the primary container.
18. **P2 — Disk/Docker cleanup:** inspect reclaimable images/volumes and large temporary files, but do not prune unknown images/volumes or delete backups without a restore and dependency check.
19. **P2 — Connector resource inventory:** Gateway currently exposes zero servers; Val Town has zero vals; Render requires a user-selected workspace. Base44 README initialization errored due missing project-owner metadata. Hostinger Connector, Develoop, PR Completion, Voice Notify for Codex and Vibe Coder did not expose callable namespaces in this session; do not fabricate deployments.
20. **P2 — Update notifications:** implement and verify release/commit notifications only after the source repositories and notification destination are explicitly identified.

## Other live repository status
- `xh09411-web/open-hands`: PR #47, #48, #50 merged; PR #49 open, ready for review, not merged.
- `xh09411-web/ai-agent-stack`: PR #3 open, latest pushed head `4c14c816a55a654136b576a7f418758e3d281ffc`.
- `xh09411-web/Ai-Agent-Skill`: PR #5 and #6 merged.
- `xh09411-web/All-in`: PR #4 open; PR #5 merged with historical CI failure to recheck.

## Safety boundaries
- No production OpenHands restart/upgrade, firewall change, credential rotation, volume/image prune, destructive cleanup, or PR merge was performed in this batch.
- Keep the primary service, persistent state, untracked skills, backups, and rollback image intact until the side-by-side upgrade path passes tests.

## Addendum — additional verification on 2026-10-12
- PR #49 tests passed on Python 3.10 and 3.13 containers (17/17 each), plus host Python 3.14; compileall passed on 3.10/3.13 and Gitleaks on the plugin directory found no leaks. The GitHub metadata probe now accepts an optional `GITHUB_TOKEN`, and Bearer tokens are redacted from draft text; both focused tests were observed failing before their fixes and passing afterward.
- Attempted read-only manifest inspection of the official OpenHands 1.25.0 image. The VPS could not resolve `docker.all-hands.dev` (`lookup docker.all-hands.dev ... no such host`), so the image could not be verified/pulled. No production image was changed.

- UFW is active. It explicitly allows SSH 22/2222 and web 80/443, has explicit denies for 3000 and 8000, and allows 8081 from Anywhere. Docker still publishes 3001 and 33601 on all interfaces; UFW output does not settle whether Docker rules permit external reachability. No firewall rules were changed; external reachability remains unverified.

- A side-by-side OpenHands CLI canary was prepared under `/root/openhands-canary-home` (separate mode-0700 home; config mode 0600) using PyPI `openhands-ai` CLI 1.16.0. Its enabled `oh-my-agent` stdio config is recognized by `openhands mcp list`; an isolated web UI bound only to `127.0.0.1:3002` returned HTTP 200. No Tailscale/public route was added.
- Using that CLI environment's SDK, the canary loaded all 8 MCP tools and successfully called `system_status`, `skills_list` (5 read-only skill directories when `OHMA_SKILL_ROOTS=/root/workspace/.agents/skills` was set), and `upstream_status`. Provider remains unconfigured, Mem0 remains not configured, and upstream GitHub metadata calls returned HTTP 403. This is a local canary, not a production rollout or authenticated end-to-end coding test.


## Addendum — official Agent Canvas 1.25.0 canary, 2026-10-12
- Pulled the official `ghcr.io/openhands/agent-canvas:1.25.0` image from GHCR after the legacy `docker.all-hands.dev` hostname failed DNS resolution.
- Started `openhands-canvas-canary-20261012` on host loopback `127.0.0.1:8003`, with isolated state and projects directories, the plugin source mounted read-only, skills mounted read-only, telemetry disabled, no Docker socket, and no production state or provider credentials mounted.
- Root, health/readiness probes returned HTTP 200. Authenticated `/api/settings` confirmed the canary settings include the `oh-my-agent` MCP configuration.
- Direct SDK integration test inside the official image (SDK 1.53.0) discovered all 8 MCP tools and successfully called `system_status`, `skills_list` (5 entries), `memory_search` (reports unconfigured Mem0), and `promotion_check` (still fail-closed).
- Important limitation: `/api/tools/catalog` did not expose the MCP tools, so this does not yet prove they appear in a real Agent Canvas conversation. The dedicated `/api/mcp/test` endpoint validation was blocked by the tool safety checker; no request was sent. No Tailscale/Caddy route was added.
- The older temporary CLI 1.16.0 canary was stopped; the official 1.25.0 canary remains loopback-only. Production `openhands` remains unchanged.


## Addendum — local model and gateway integration repair, 2026-10-13

- Downloaded official `Qwen/Qwen3-4B-GGUF` `Qwen3-4B-Q4_K_M.gguf` (Apache-2.0; observed file size 2,497,280,256 bytes) into `/opt/qwen3-4b-runtime/`. The observed SHA-256 is recorded in `deploy/local-qwen-fast/model.lock`; it is not represented as an independently published upstream checksum.
- Added and enabled `llama-agent-fast.service` on `127.0.0.1:8089`, with `--api-key-file` and a generated key stored only in `/etc/llama-agent-fast/api-keys` and `/root/.agent.env`, both restrictive permissions. Unauthenticated model catalog returns HTTP 401; authenticated completion returns HTTP 200.
- Backed up the active LiteLLM config and `.agent.env` before changing them. The active `my-model` alias now routes to `qwen3-4b-local`; `my-model-slow` preserves the original 27B Q8 route. `extra_body.chat_template_kwargs.enable_thinking=false` fixed the empty-final-content issue caused by reasoning-only output.
- Fresh verification passed: `All-in/tests/verify_agent_api_compat.sh` tested live generation, required function-tool emission, and continuation after a simulated tool result through both LiteLLM (`127.0.0.1:4000`) and the OpenHands bridge (`10.0.0.1:4001`). `test_refresh_upstreams.py` (3/3), `test_verify_repo_patterns.py` (3/3), integration matrix (blocking=0, warnings=0), standalone-open (8/8), repository verifier (21 skills; 297 JSON and 63 YAML), skill-fleet verifier (21 skills, 7 agent targets), Gitleaks, and `git diff --check` all passed.
- Limitations still open: this validates model/API and tool-call protocol, not an actual OpenHands browser conversation invoking its terminal tool, not Hermes/DSH/Lody task completion, and not mobile-to-Git end-to-end. The 27B model is slow on 4 CPU cores and remains as fallback. Root filesystem is now about 87% used (267 GB of 310 GB, 44 GB free); no bulk cleanup was performed.
- Codex CLI remains `Not logged in`; its `sim` provider still lacks `SIM_API_KEY` and port `4010` has no listener. NVIDIA and DeepSeek env values have non-ASCII placeholder-like content and are identical; real provider credentials were not guessed or printed.
- `Ai-Agent-Skill` PR #8 adds the live inference/tool-round-trip regression test and remains open; no GitHub Actions runs were returned for its head at last check. `ai-agent-stack` PR #3 is being updated with the sanitized deployment manifest; neither PR is represented as merged.


## Addendum — Hermes and Lody follow-up, 2026-10-13

- Hermes `config.yaml` was migrated from unrecognized `litellm.*` fields to the current custom-provider schema: `model_provider: local-litellm`, `model: my-model`, `providers.local-litellm.api: http://127.0.0.1:4000/v1`, `key_env: OPENAI_API_KEY`. LiteLLM's `my-model` alias now has per-model `drop_params: true`, so Hermes' `reasoning.effort` field no longer causes `UnsupportedParamsError`.
- Verified Hermes one-shot only in a fresh temporary home with the existing root-owned env file, `--ignore-rules`, and `-t terminal`: returned `HERMES-OK`. The default/full toolset remains unverified and currently fails context admission: llama-server logs requests of 18,511 and 32,943 tokens against an 8,192-token context. A full-context local Hermes task would be slow even if context were increased; do not claim Hermes gateway is complete.
- The active `hermes-gateway.service` does not load `/root/.agent.env`; it was not restarted or given all environment secrets because that would widen secret exposure. Its end-to-end task path still needs a least-privilege provider credential injection and a viable context/toolset strategy.
- `lody agent-config list` reports ten agent configs as available (including Claude Code, Codex, Hermes, DeepSeek Harness, Cline, OpenCode, Kimi Code CLI, Goose, Grok, and Kimi Code). This is catalog availability only, not runtime verification. No secret was uploaded to Lody's cloud-backed agent config.


## Addendum — bounded disk cleanup, 2026-10-13

- Removed only this session's temporary Hermes test home (`/tmp/hermes-e2e-home`, 432 MB), empty test workspace, small test response/status files, and cleared npm download cache (`/root/.npm/_cacache`, about 312 MB). The active `_npx` CLI installation cache (about 1.2 GB) was retained.
- Reduced systemd journal retention to a 200 MB target; 100.9 MB of archived journals were removed. Current journal usage is about 177.5 MB.
- Filesystem moved from 267 GB used / 44 GB free (87%) to 266 GB used / 44 GB free (86%). This is a bounded cleanup, not a full disk cleanup.
- Preserved `/tmp/ai-migration` (about 4.6 GB), other prior agent test artifacts, Docker images (about 33.65 GB reported reclaimable), and Docker volumes (about 3.73 GB reported reclaimable) because ownership/dependencies are not yet proven. No Docker prune or model deletion was performed.


## Addendum — current CLI refresh and Codex verification, 2026-10-13

- Backed up the pre-update global npm package inventory and `/root/.codex/config.toml` under `/var/backups/agent-integration/20261013-pre-cli-update/`, with SHA-256 checksums. The previous `/usr/local/bin` symlink targets were also recorded for rollback.
- Updated the active PATH commands for Codex CLI to `0.162.1`, Claude Code to `2.1.296`, OpenCode to `1.19.0`, and Biome to `2.5.15`. The `skills` npm package `1.7.2` is installed under `/usr/lib/node_modules`, but the active `/usr/local/bin/skills` remains the distinct pre-existing `skills-cli` package; it was intentionally not replaced with a different package. Other globally outdated packages remain inventoried and are not upgraded blindly because several have major-version jumps or unclear production consumers.
- LiteLLM Responses API non-streaming and streaming smoke tests both returned HTTP 200 with expected text. Codex CLI is still not logged in, and its previous device-auth request returned HTTP 403. A Codex CLI task through the local model has not yet completed; the local 8K-context model is too slow for the full Codex prompt within the initial test window, so no end-to-end success is claimed.
- A custom-provider CLI test is running after the Codex CLI refresh. Do not change the production Codex config or claim integration success until this test completes and the command result is captured.
- Git remotes were fetched with `git fetch --all --prune`. Clean `/root/AI-Agent-Skill`, `/root/ai-agent-stack`, and `/root/hermes-007` checkouts match their tracked upstreams. Dirty `/root/.hermes`, `/root/open-hands`, and `/root/ai-company` working trees were preserved; no pull, reset, clean, or overwrite was applied to them.


## Addendum — Codex tool execution and progress timer, 2026-10-13

- Codex CLI `0.162.1` successfully ran through the local LiteLLM Responses API using an isolated temporary home and the `my-model` alias. A real `workspace-write` test created `CODEX-E2E.txt`, read it back, and verified `CODEX-WRITE-OK`; command exit code 0. This proves one local Codex tool-execution path works, not that the default root Codex profile or mobile Remote Control is complete.
- Added a root-only, read-only systemd timer (`agent-integration-progress-report.timer`) running every 30 minutes. It writes `/var/lib/agent-integration/progress-latest.md` with disk, CLI, service, HTTP health, and local Git worktree status. It does not delete files, restart services, commit, push, or send messages to ChatGPT.
- The default root Codex config remains on the old `sim` provider and is still not logged in. The successful task used a clean isolated home to keep the local model prompt within its context budget. Production Codex profile switching and phone-to-VPS remote control remain open.
- Lody's `Claude Code` agent-config currently has no environment entries. LiteLLM virtual-key creation is unavailable because its proxy has no connected database (`/key/info` returns HTTP 500, `Database not connected`). A direct Anthropic Messages authentication probe was blocked by the tool safety check, so no credential was copied into Lody's cloud config. Lody API wiring remains blocked until a safe scoped credential path is available.
- The all-in-one Agent Skill test suite completed with exit code 0: gateway and OpenHands bridge tool round-trips, 3+3 Python tests, integration matrix (0 blocking/0 warnings/4 isolated), standalone-open (8/8), repository/skill structure checks (21 skills, 7 targets), config syntax checks (297 JSON and 63 YAML), and Gitleaks (no leaks). Generated report files changed only their timestamps and were restored to avoid committing timestamp-only noise.


## Addendum — Claude Code local route failure, 2026-10-13

- Tested Claude Code `2.1.296` against the local Anthropic Messages-compatible LiteLLM route with the configured `my-model` alias. It rejected the alias as unknown to its built-in model catalog, then the API request failed because the prompt was 17,869 tokens against the local model's 8,192-token context. A reduced built-in toolset test timed out after 70 seconds without creating the test file. Claude Code is therefore not end-to-end working on the current local 4B model.
- The configured `ANTHROPIC_AUTH_TOKEN`, `OPENAI_API_KEY`, `LITELLM_API_KEY`, and `LITELLM_MASTER_KEY` are the same gateway master credential. LiteLLM virtual-key endpoints return `Database not connected`; I did not copy that full-privilege key into Lody's cloud-backed agent config. The direct credentialed API probe was blocked by the tool safety check.
- Safe next route: either provision a genuine external Claude-compatible API credential through the user's chosen provider, or build and benchmark a dedicated local model route with adequate context and a scoped key before configuring Lody. Do not mark Lody/Claude Code complete based on the current API compatibility tests.


## Addendum — root-only Codex wrapper and 30-minute progress timer, 2026-10-13

- Installed `/usr/local/sbin/codex-local` (mode 0700) which reads the existing root-only `/root/.agent.env`, uses isolated Codex home `/var/lib/agent-integration/codex-home`, routes to LiteLLM `my-model` over the Responses API, and runs ephemeral tasks in the workspace-write sandbox. Tested successfully: one-shot response `WRAPPER-OK` and a real file create/read round-trip returning `WRAPPER-WRITE-OK`. The custom model metadata warning remains; the default `/root/.codex/config.toml` was not overwritten and remains unauthenticated on the `sim` provider.
- Installed and enabled `agent-integration-progress-report.timer`, refreshing every 30 minutes. It writes a root-only, read-only snapshot to `/var/lib/agent-integration/progress-latest.md`. It does not automatically send messages to ChatGPT.
- Claude Code and Lody remain blocked on the local 8K-context model; a real Claude Code task exceeded the context limit and a limited-tool attempt timed out. No gateway master credential was copied to Lody's cloud config.

## Addendum — PR #4 merged and live regression, 2026-10-13

- PR #4 merged by squash into `portable-20260924`: merge commit `e2d9d3c1270487ceb43556bac2625f3bd15dfc84`.
- Installed `codex-local` wrapper hash matches tracked source (`37d251f58cc213cd98e451e972f02a8a9e22282925da07f9ecddc42260296bb2`). The wrapper exports only `OPENAI_API_KEY`, uses the isolated Codex home, and rejects caller attempts to override sandbox/provider configuration.
- Live local Codex inference returned `LOCAL-CODEX-REGRESSION-OK`; workspace-write test returned `WRAPPER-WRITE-OK`. The warning about custom model alias `my-model` metadata remains non-fatal.
- Progress snapshot service is active through `agent-integration-progress-report.timer`; oneshot service returned `Result=success`, `ExecMainStatus=0`. Snapshot file is root-only mode 0600. Tracked and installed script hashes match (`c55d7d73a65b54f9129526af26fcc2d681d637e4377e8e29c92789a47d8babea`).
- Live health probes: LiteLLM HTTP 200; Qwen-fast HTTP 200; OpenHands bridge `10.0.0.1:4001/health/readiness` HTTP 200. Bridge response reports `db: Not connected`; DB-backed features remain unverified.
- `bash -n`, `git diff --check`, and Gitleaks on `deploy/local-qwen-fast` passed; no leaks found.
- Global npm package directories now report Crush 0.98.1 and Kilo CLI 7.8.8, but executable `crush` still reports 0.89.0 and `kilo`/`kilocode` report 7.4.21 because postinstall scripts were blocked. Do not claim these CLI upgrades are complete; repair the binary installers separately.
- Remaining blockers: default Codex profile is still logged out on `sim`; Claude Code/Lody full end-to-end workflow still blocked by custom model alias and 8,192-token context; disk is ~87% used (~41 GB free); npm packages 9router, freebuff, npm, oh-my-opencode, root remain outdated and need isolated impact analysis. Desktop Commander online/ping verified. Exact plugin names Voice Notify for Codex and NVIDIA Skills were not found in plugin search; SQL search found Supabase installed, but no exact SQL Expert plugin match.

## Addendum — repair Crush/Kilo CLI launchers, 2026-10-13

- Root cause confirmed: npm updated the package directories, but the Crush and Kilo postinstall hooks had not run, leaving their cached/native launcher binaries stale.
- Backed up both global package directories and executable symlinks under `/var/backups/agent-integration/20261013-crush-kilo-repair` before repair.
- Re-ran the package-specific installers only: `node /usr/lib/node_modules/@kilocode/cli/postinstall.mjs`; Crush's 0.98.1 package contains and runs its bundled launcher. Verified live executables now report `crush 0.98.1`, `kilo 7.8.8`, and `kilocode 7.8.8`.
- n8n 2.42.7, Promptfoo 0.124.1, and TweakCC 4.4.0 version commands match package metadata. n8n systemd service is inactive; it is installed but not running.

## Addendum — reconcile duplicate npm global prefixes, 2026-10-13

- Found two separate global package trees: `/usr/lib/node_modules` contained updated Crush 0.98.1 and Kilo 7.8.8, while PATH-resolved `/usr/local/lib/node_modules` still contained Crush 0.89.0 and Kilo 7.4.21. This explained why the CLI version checks stayed old after npm update.
- Backups of original `/usr/lib` packages and command symlinks are under `/var/backups/agent-integration/20261013-crush-kilo-repair`.
- Copied the verified new Crush native binary and Kilo `.kilo` binary into the corresponding PATH-resolved `/usr/local` package trees without deleting the old package metadata. Live commands now report `crush 0.98.1`, `kilo 7.8.8`, `kilocode 7.8.8`.
- Note: `/usr/local` package.json metadata remains older (Crush 0.89.0, Kilo 7.4.21), while the executable payloads are updated. Runtime `--version` is correct; reconcile npm prefix/package metadata separately during a controlled reinstall to avoid overwriting working launchers.

## Addendum — safe cache cleanup and remaining service blockers, 2026-10-13

- Saved a pre-cleanup inventory at `/var/backups/agent-integration/20261013-safe-cache-cleanup/inventory.txt`; cleared npm's download cache and removed only temporary files created by the Codex wrapper regression tests. Root disk use changed from about 88% (40 GB free) to about 87% (43 GB free); no Docker images, volumes, model files, or skill directories were deleted.
- Confirmed `n8n` is installed at 2.42.7 but `n8n.service` is inactive and no 5678/5679 listener is present; treat it as installed, not deployed/available.
- Confirmed the host reports `System restart required`, with uptime about 2 weeks. No reboot was performed because it could interrupt the running agents and services.
- Current key services remain active: LiteLLM, OpenHands bridge, Hermes API/gateway, Lody agent, DSH agent, and progress timer. Bridge readiness returns HTTP 200 but its own health payload still says `db: Not connected`.
- Remaining global npm updates: 9router 0.5.95→0.5.99, freebuff 0.0.137→0.2.27, npm 11.19.0→12.2.0, oh-my-opencode 4.19.4→5.1.32, root 1.0.0→3.2.0. These remain untouched because major-version/runtime impact and service ownership have not been established.

## Addendum — Claude Code/Lody context and integration follow-up, 2026-10-13

- Backed up the active llama-agent-fast.service, LiteLLM config, and Claude settings under /var/backups/agent-integration/20261013-claude-context/.
- Changed the Qwen3-4B local inference service context from 8,192 to 32,768 tokens via a systemd drop-in. Fresh verification: service active; authenticated /v1/models returns qwen3-4b-local.
- Claude Code 2.1.296 through the existing local LiteLLM route successfully completed a real shell-tool create/read test in /tmp/claude-lody-final, returning CLAUDE-LODY-FINAL-OK. The command used CLAUDE_CODE_SIMPLE=1 and an explicit restricted Bash allowlist.
- Updated the Lody cloud-backed Claude Code agent config with non-secret environment values only: ANTHROPIC_BASE_URL=http://127.0.0.1:4000, ANTHROPIC_MODEL=my-model, CLAUDE_CODE_SIMPLE=1. Refreshed ACP capabilities successfully; custom model my-model is listed.
- Registered /root/ai-agent-stack as a local project in the Lody workspace (local-project-4dd27ae44d58855fe070774b).
- Full Lody ACP session execution remains unverified/blocked: two read-only session tests timed out without an assistant response. Both were cancelled. Process inspection confirmed the ACP child received the three non-secret environment variables. LiteLLM logs showed successful /v1/messages calls, but the Lody turn did not finish within 65/75 seconds; latency/tool-context overhead remains to diagnose.
- Direct Claude Code with the full default configuration exceeded context at 55,916 tokens when the model context was 32,768. CLAUDE_CODE_SIMPLE=1 reduced the direct CLI path enough for one-shot and restricted-tool tests, but did not establish that the full Lody ACP toolset completes.
- A temporary isolated LiteLLM proxy was tested for an Anthropic Messages API request and an unauthenticated request returned HTTP 401 after its runtime was corrected. The temporary proxy was stopped and its configuration/key files removed; the Lody cloud config was verified without an ANTHROPIC_AUTH_TOKEN entry. No gateway master key was copied to Lody.
- Remaining: make Lody ACP complete a real read-only tool call within an acceptable time; remove/resolve the custom-model warning; test from the Lody app UI and validate the mobile-to-Git workflow. Do not claim end-to-end integration until this passes.
