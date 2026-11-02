# Agent Skill Source and Portability Manifest

Generated from the VPS checkout on 2026-10-11. This manifest records evidence found locally; it does not infer authorship or a license from a folder name. Skills without source/license evidence remain private until reviewed. Shared symlinks are not committed as absolute paths; scripts/link-shared-skills.sh recreates them from the pinned canonical repository.

## Setup

After cloning this repository, run `./scripts/link-shared-skills.sh`. It validates the pinned Ai-Agent-Skill checkout and creates only missing links. It refuses to overwrite a non-symlink destination or use a modified/wrong-version source checkout. GitHub credentials are supplied by the user through normal Git configuration; no tokens are embedded.

Canonical shared source: `https://github.com/xh09411-web/Ai-Agent-Skill` at commit `39112117be17b67b40944681e753ac9ed7dd5091`.

Then run `python ./scripts/sync-agent-catalog.py` to verify that `.agents/skill-registry.json` still matches local `skills/` and `extensions/plugins/`. Use `--apply` when you intentionally added/removed skills or plugins and want the registry auto-repaired.

Private-only overlays should stay under `.private/`, `.agents/private/`, or `.agents/skills-private/` so they are not committed upstream while your private fork still receives automated dependency and workflow update PRs via Dependabot.

| Skill path | Local state | Source evidence | License evidence |
|---|---|---|---|
| BrowserGym | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| CI-CD-Watcher | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| DB-Schema-Grapher | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| Docker-Sandbox-Plus | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| Git-Flow-Manager | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| OSWorld-Core | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| Pytest-AutoHealing | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| Slack-Notifier-Agent | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| SonarQube-Linter | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| add-javadoc | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| add-skill | local files: 7 | https://github.com/OpenHands/extensions; https://github.com/owner/repo | NOT FOUND — provenance/license not established from local files |
| agent-canvas-environment | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| agent-creator | local files: 7 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| agent-memory | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| agent-readiness-report | local files: 8 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| agent-sdk-builder | local files: 6 | https://github.com/OpenHands/software-agent-sdk; https://github.com/OpenHands/docs; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| agent-skills | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/agent-skills | not vendored here; source license follows canonical repository |
| api-compatibility | local files: 1 | local VPS addition; source/author evidence not stated; keep private until verified | NOT FOUND — provenance/license not established from local files |
| api-integration | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| apollo-memory | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/apollo-memory | not vendored here; source license follows canonical repository |
| auth-security | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| automated-ui-asset-generator | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| azure-devops | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| bitbucket | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| bitbucket-cloud | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| bitbucket-data-center | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| build-your-own-x | local files: 1 | https://github.com/codecrafters-io/build-your-own-x.git | NOT FOUND — provenance/license not established from local files |
| canvas-extension-api | local files: 14 | https://github.com/OpenHands/software-agent-sdk; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| cc-suite-bridge | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| ci-cd-pipeline | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| cluster-load-balancer | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| code-review | local files: 9 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| code-simplifier | local files: 9 | https://github.com/anthropics/claude-plugins-official; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| composio | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/composio | not vendored here; source license follows canonical repository |
| composio-tool-integration | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/composio-tool-integration | not vendored here; source license follows canonical repository |
| cross-repo-testing | local files: 1 | https://github.com/OpenHands/software-agent-sdk; https://github.com/OpenHands/OpenHands; https://github.com/OpenHands/deploy | NOT FOUND — provenance/license not established from local files |
| datadog | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| db-migrate | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| deep-packet-inspector | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| define-to-ship | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/define-to-ship | not vendored here; source license follows canonical repository |
| deno | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| dependency-resolver | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| discord | local files: 16 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| docker | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| docker-orchestration | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| documentation-gen | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| ecc | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/ecc | not vendored here; source license follows canonical repository |
| engineering-memory | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/engineering-memory | not vendored here; source license follows canonical repository |
| env-verifier | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| evidence-based-citations | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| evolution-tree | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| ffmpeg-media-matrix | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| firecrawl | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/firecrawl | not vendored here; source license follows canonical repository |
| firecrawl-web-research | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/firecrawl-web-research | not vendored here; source license follows canonical repository |
| flarglebargle | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| frontend-design | local files: 6 | https://github.com/OpenHands/extensions | LICENSE.txt |
| full-cycle-mobile-dev | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/full-cycle-mobile-dev | not vendored here; source license follows canonical repository |
| git-commander | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| github | local files: 10 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-actions | local files: 5 | https://github.com/nektos/act; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-agents-md-maintainer | local files: 11 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-delivery-watchdog | local files: 10 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| github-issue-to-pr | local files: 15 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-issue-triage | local files: 12 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| github-pr-review | local files: 7 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-pr-reviewer | local files: 20 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-repo-monitor | local files: 15 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| github-stale-ci-pr-closer | local files: 10 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| gitlab | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| gitlab-issue-to-mr | local files: 9 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| go-microservices-generator | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| harness-evolution | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/harness-evolution | not vendored here; source license follows canonical repository |
| improve-agent-readiness | local files: 3 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| incident-retrospective | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| iterate | local files: 11 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| jira-issue-to-pr | local files: 8 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| jupyter | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| kubernetes | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| large-codebase | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| learn-from-code-review | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| linear | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| linear-triage | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| log-analyzer | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| magic-word | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| memory-leak-plugger | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| multimodal-mcp-adapter | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| news-digest | local files: 9 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| notion | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| npm | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| npm-conflict-resolver | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| obra-superpowers | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/obra-superpowers | not vendored here; source license follows canonical repository |
| openhands-api | local files: 12 | https://github.com/jpshackelford/.openhands; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| openhands-automation | local files: 10 | https://github.com/OpenHands/extensions; https://github.com/owner/repo.git; https://github.com/owner/repo | NOT FOUND — provenance/license not established from local files |
| openhands-enterprise-troubleshooting | local files: 9 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| openhands-sdk | local files: 6 | https://github.com/OpenHands/software-agent-sdk; https://github.com/OpenHands/docs; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| package-cleaner | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| pdflatex | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| performance-tuner | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| plain-english-content | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| plan-once-verify-always | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/plan-once-verify-always | not vendored here; source license follows canonical repository |
| prd | local files: 6 | https://github.com/snarktank/ralph; https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| python-bytecode-optimizer | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| qa-changes | local files: 3 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| recovered-from-freebuff | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/recovered-from-freebuff | not vendored here; source license follows canonical repository |
| release-notes | local files: 3 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| research-brief | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| rust-wasm-compiler | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| security | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| self-evolving-engineer | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| sesm-engine | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/sesm-engine | not vendored here; source license follows canonical repository |
| setup-agents-md | local files: 2 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| setup-openhands | local files: 2 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| setup-pr-review | local files: 2 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| skill-creator | local files: 13 | https://github.com/OpenHands/extensions | LICENSE.txt |
| skill-optimizer | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/skill-optimizer | not vendored here; source license follows canonical repository |
| slack-channel-monitor | local files: 11 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| slack-standup-digest | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| spark-version-upgrade | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| ssh | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| swift-linux | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| technical-writing | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| theme-factory | local files: 17 | https://github.com/OpenHands/extensions | LICENSE.txt |
| ticket-to-code-change | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| understand-anything | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/understand-anything | not vendored here; source license follows canonical repository |
| unit-testing | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| upcoming-release | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| update-sdk | local files: 3 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| upstream-fork-sync | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| uv | local files: 6 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| vercel | local files: 5 | https://github.com/OpenHands/extensions | NOT FOUND — provenance/license not established from local files |
| vps-bridge | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/vps-bridge | not vendored here; source license follows canonical repository |
| vulnerability-remediation | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |
| zero-knowledge-proof-auth | local files: 1 | NOT STATED IN LOCAL FILES — verify source before redistribution | NOT FOUND — provenance/license not established from local files |

| evolution-tree/evolution-tree | shared symlink | source repo xh09411-web/Ai-Agent-Skill at pinned commit 39112117be17b67b40944681e753ac9ed7dd5091; path skills/evolution-tree | not vendored here; source license follows canonical repository |

## Publishing rule

Do not publish a skill publicly unless its origin and redistribution license are verified. This repository is private, but the manifest deliberately flags missing provenance so a future public release does not accidentally redistribute unverified content.
