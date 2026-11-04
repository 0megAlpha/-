# Agent / Skill 三大 Repository 盤點 Inventory（2026-09-17）

## 0. 三大正式 Repository 判定
| Repo | 本機路徑 | GitHub Remote | 分支 | HEAD |
|---|---|---|---|---|
| OpenHands | /root/open-hands（完整版） | xh09411-web/open-hands | main | a22efddf20 (initial commit of merged and redacted openhands core custom assets) |
| OpenHands（舊 checkout） | /root/openhands | 同 open-hands | my-custom | 4bb0cd1df |
| Hermes | /root/.hermes | xh09411-web/hermes-007 | (detached/working) | 4fb7345 |
| AI-Agent-Skill | /root/AI-Agent-Skill | xh09411-web/Ai-Agent-Skill | (working) | 2edbc7e |

## 1. OpenHands（/root/open-hands）
- skills/：27 個 .md skill（add_agent, agent-builder, agent_memory, code-review, github, gitlab, kubernetes, ssh, docker 等）
- .agents/skills/：cross-repo-testing, custom-codereview-guide.md, upcoming-release, update-sdk（未追蹤）
- openhands-extensions/：完整 OpenHands 擴展專案
- openhands-ui/, openhands/（Python core）, enterprise/, frontend/, tests/
- 未提交變更 216 個（多為測試/上游同步檔案）
- openhands CLI 未安裝（MISSING）；服務停止

## 2. Hermes（/root/.hermes）
- skills/：30 個類別（apollo-memory, autonomous-ai-agents, creative, media, research, vps-bridge 等），git 追蹤 11 個變更
- apollo/memory_core.py, bin/（tirith, uv, uvx）, platforms/pairing, cron/, state.db, kanban.db
- config.yaml, SOUL.md, moa.yaml（Hermes 本體設定）
- hermes CLI：/usr/local/bin/hermes 存在
- Hermes service 已停止（.clean_shutdown）

## 3. AI-Agent-Skill（/root/AI-Agent-Skill）
- skills/ 8 個 bundle：addyosmani-agent-skills, awesome-claude-code-toolkit, cc-suite, claude-forge, ghost-goat, gstack, kiro-powers, superpowers
- mcp-servers/ 14 個 stub（僅 package.json，無實作、無 node_modules）：aws deno docker fetch filesystem github jupyter kubernetes npm pdflatex postgres sqlite technical-writing uv
- .claude-plugins/ 33 個 plugin 目錄
- .claude/skills/, .cline/plugins/, scripts/（n8n_workflow_importer.json, v6_orchestrator.py）
- openhands-core/（.agents/skills）, hermes-brain/（core/skills 9 個 + config.json）
- 其他：aider-core, autogen-core, coolify-core, kiro-core, langgraph-core, swe-agent-core, openai-brain, openclaw-engine, opencode-engine, devin-sandbox, multi-agent-orchestrator（18 個 json agent 定義）, media-studio, automation-center, models/, memory/, security/
- 無 README.md；有 docs/DEPLOYMENT_RECORD.md, docs/SECURITY_SCAN.md
- git：4 commits，4 個未提交變更（submodule 型，skills 內嵌 git repo）

## 4. Google-ai（/root/Google-ai）— remote 錯誤指向 open-hands
- hermes-007/core/skills/：30 個 skill.py（cross-repo-dependency-mapper, hyperparameter-auto-tuner, architecture-boundary-reviewer, multi-tenant-isolation-guard, continuous-compliance-auditor, meta-prompt-generator, predictive-resource-scaler, context-window-sliding-controller, backup-redundancy-trigger, concurrency-deadlock-resolver, legal-open-source-license-checker, semantic-drift-detector, iphone-ui-viewport-adapter, strategic-task-decomposer, sandbox-security-audit, agent-race-consensus-manager, api-breaking-change-detector, automated-patch-reviewer, autonomous-refactor-planner, code-smell-identifier, cost-token-optimizer, cross-model-token-saver, dynamic-topology-orchestrator, episodic-memory-writer, error-recovery-fallback-strategy, failure-mode-simulation, failure-root-cause-analyzer, graph-database-sync, ...）
- openhands-core/（.agents/skills）
- openhands-cloud/（OpenHands cloud 部署層：charts, terraform, replicated, scripts）
- kiro-powers/（10+ 能力：aws-lambda-managed, aws-transform-agent, datadog-monitoring, discord-webhook, elevenlabs-tts, exa-web-search, figma-design, firebase-integration, github-actions-cicd, hashicorp-terraform...）
- cc-suite/（README only）, devin-sandbox/（tasks）, terminal-bench/, build-your-own-x-ref/, deploy-docs/, research/, portal/, tasks/
- mcp-servers/ 58 個 stub（僅 package.json，無實作）— 含 cerebras-* 系列、playwright-* 系列
- deepseek-harness/config.json, lody/config.json（基礎設施設定 → 不動）
- agent-command-center.html, server.mjs, index.html

## 5. Skill 安裝庫（agent runtime 技能，保留原位）
- /root/.agents/skills/：38 個（.skill-lock.json v3 註冊；18 個指定 + 20 個非指定）— 由 skills-cli 管理
- /root/.claude/skills/：14 個（agentic-tdd, antigravity, browser-use, claude-token-saver, code-reviewer, excalidraw-diagram, frontend-design, google-workspace, improve-codebase-architecture, planetscale-db, remotion, remotion-video, shannon, valyu）
- /root/.config/opencode/skills/, /root/.codex/skills/, /root/.cline/skills/, /root/.grok/bundled/skills/
- ~/.hermes/skills/（見上）

## 6. 2026-09-14 00:00 後全局安裝（npm，依 mtime）
- 09-14 02:20 opencode-ai@1.18.30
- 09-15 02:03 dsh-hermes-memory@1.1.10
- 09-15 21:53 ghost-blog
- 09-16 10:30 @deepseek-ai/dsh@0.1.5-rc.1
- 09-16 19:29~19:50 大批：opencode-* 套件（oh-my-opencode, opencode-caveman/handoff/data-agent/daytona/github/helicone-session/linear/marketing-agent/obsidian/ocx/sales-agent/sentry-monitor/slack/superpowers/wakatime）, cline@3.0.62, @openai/codex@0.154.0, @anthropic-ai/claude-code@2.1.273, skills-cli@0.1.3, skillswitch@0.2.0, cc-suite@1.0.5, uipro-cli@2.2.3, coding-agent-adapters@0.17.0, roo-cli@0.2.17, mcporter@0.9.0, gitnexus@1.6.12, qmd, firecrawl, firebase-tools/firebase-mcp-server, @ast-grep/cli, @upstash/context7-mcp, mcp-server-semgrep, pm2@7.0.4, biome, eslint, prettier, pnpm, yarn, bun, typescript, tsx, ts-node, claude-code-reviewer, playwright-* 系列, semantic-release 系列, @memberjunction/ai-cerebras, @modelcontextprotocol/* 系列

## 7. 備份/其他副本（不屬三大 repo，保留不動）
- /root/ai-agent-workflows（remote=Ai-Agent-Skill）, /root/ai-company（local git）, /root/agent-platform（remote=agent-platform-legacy）
- /root/opencode-backup-20260914-022614, /root/cline-acp-upgrade-backup-20260913-180724, /root/lody-cline-acp-backup-*, /root/prompt-backup-*, /root/ai-company-backups, /root/_audit/
- .dsh.bak.* / .dsh.backup.* / .dsh.broken.*（DSH 守護備份 → 絕不動）

## 8. 已確認不可動
- Lody / DSH 核心配置、OpenCode/Cline/Codex 核心配置、Google-ai 前後端（agent-command-center.html/server.mjs）
- iptables 備份僅為檔案（本任務不改防火牆）
- ASTRA/REALM 腳本（玩具 stub，不使用）