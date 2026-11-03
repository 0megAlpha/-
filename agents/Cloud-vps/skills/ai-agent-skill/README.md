# AI-Agent-Skill

通用 Agent / Skill 能力資產庫 — 非專屬 OpenHands 或 Hermes，可被多個 Agent / Framework 重複使用的 Skills、Agent capabilities、reusable tools、plugins、MCP/ACP 元件、Agent modules 與 scripts。

> 維護方針：三大 Repository（OpenHands / Hermes / AI-Agent-Skill）之一。本 repo 只收**通用**能力；凡明確屬於 OpenHands 或 Hermes 的資產，分別歸入對應 Repository。

## 目錄結構

| 路徑 | 內容 |
|---|---|
| `skills/` | 通用 Skill bundle（8 套，均為內嵌檔案追蹤，clone 後即完整可用） |
| `mcp-servers/` | 通用 MCP server 元件（14 個；stub 清單，實作以官方/全局套件為準） |
| `.claude-plugins/` | 33 個 Claude 相容 plugin 目錄 |
| `.claude/skills/` | Claude skills |
| `.cline/plugins/` | Cline 插件配置 |
| `opencode-engine/` | OpenCode 引擎 plugins（vulnerability-remediation, skill-optimizer, css-tailwind-purger, uv-env-manager, dotenv-secret-scanner 等） |
| `openai-brain/` | OpenAI SDK configs（mcp-resource-subscription-manager, adaptive-thread-manager 等） |
| `hermes-brain/` | Hermes 相容 core（9 個通用 skills + config） |
| `openhands-core/` | OpenHands 相容 core（.agents/skills；本目錄於 git 忽略，正式來源為 open-hands repo） |
| `multi-agent-orchestrator/` | 多 Agent 編排定義（18 個 JSON agent 組態） |
| `devin-sandbox/`, `kiro-core/`, `langgraph-core/`, `autogen-core/`, `swe-agent-core/`, `coolify-core/`, `aider-core/`, `openai-brain/` | 各框架 core 參考/能力 |
| `scripts/` | 可重用腳本（v6_orchestrator.py, n8n_workflow_importer.json） |
| `docs/` | DEPLOYMENT_RECORD.md, SECURITY_SCAN.md, SOURCES.md |
| `media-studio/`, `automation-center/`, `models/`, `memory/`, `security/`, `bookmarks/`, `dictionary/`, `portal/`, `notebook/` | 輔助資產 |

## Skills（8 套通用 bundle）

| Bundle | 來源（GitHub） | 說明 |
|---|---|---|
| addyosmani-agent-skills | addyosmani/agent-skills | agents/commands/docs 通用技能包（.claude-plugin marketplace 格式） |
| awesome-claude-code-toolkit | rohitg00/awesome-claude-code-toolkit | Claude Code 工具包集合 |
| claude-forge | immacualate/claude-forge（含 CC-CHIPS） | Claude Code 插件/能力（cc-chips） |
| ghost-goat | (見 skills/ghost-goat) | ghost-goat skills：agent-evaluation, code-review, mcp-development, red-team-testing 等 |
| gstack | garrytan/gstack | Claude Code 工作流 stack（AGENTS.md/CLAUDE.md） |
| kiro-powers | (見 skills/kiro-powers) | 多雲能力：aws-transform-toolkit, datadog-monitoring, figma-design, firebase-integration, exa-web-search 等 |
| cc-suite | (npx cc-suite) | cc-suite@1.0.5 工具鏈組態 |
| superpowers | obra/superpowers | superpowers v6.3.0（Devin CLI / Hermes Agent 支援） |

## 長期維護契約

1. 通用能力進 `skills/`、`mcp-servers/`、`.claude-plugins/` 等；OpenHands 專屬進 open-hands repo；Hermes 專屬進 hermes-007 repo。
2. 新增能力時：在 `docs/SOURCES.md` 記錄來源 URL 與檢核狀態。
3. 敏感檔案（`.env*`、`.sim-key`、`.pg-pass`、`auth.json`、`*.pem`、`*.key`）一律禁止 commit（見 .gitignore）。
4. 嵌套 repo 的 `.git` 元資料統一放 `.embedded-git/`（gitignore），確保 clone 後內容完整。