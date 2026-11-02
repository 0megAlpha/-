# SOURCES — 資產來源紀錄（2026-09-17）

本文件紀錄 AI-Agent-Skill 內資產的來源，符合「複製/整理 → 建立來源紀錄 → 驗證」原則。原始來源一律保留，本 repo 僅收錄可重用的副本/整理結果。

## Skills bundle 來源

| Bundle | 來源 URL | 原始 HEAD（移入 .embedded-git 前） | 備註 |
|---|---|---|---|
| addyosmani-agent-skills | https://github.com/addyosmani/agent-skills.git | be4e44a Merge #553 | 完整內容以普通檔案追蹤 |
| awesome-claude-code-toolkit | https://github.com/rohitg00/awesome-claude-code-toolkit.git | ebdf1d5 Merge PR #387 | 同上 |
| claude-forge | https://github.com/immacualate/claude-forge.git | 5ba60b6 | 含 cc-chips（roger-me/CC-CHIPS, 6f73fc6） |
| gstack | https://github.com/garrytan/gstack.git | a6b3a57 v1.87.4.0 | 同上 |
| superpowers | https://github.com/obra/superpowers.git | b36e082 Release v6.3.0 | 同上 |
| ghost-goat | （見 skills/ghost-goat 內附） | — | — |
| kiro-powers | （多雲能力包，原為 Google-ai/kiro-powers 副本） | — | — |
| cc-suite | npm cc-suite@1.0.5 | — | config.json |

## 其他資產來源

| 資產 | 來源 | 備註 |
|---|---|---|
| openhands-core/.agents/skills | Google-ai/openhands-core（remote=xh09411-web/open-hands） | 本 repo 內 gitignore；正式資產歸 open-hands repo |
| hermes-brain/core/skills | Google-ai/hermes-brain | 9 個通用技能，Hermes 相容 |
| opencode-engine/plugins | Google-ai/opencode-engine 副本 | OpenCode 引擎 plugins |
| openai-brain/sdk_configs | Google-ai/openai-brain | OpenAI SDK 組態 |
| mcp-servers/* | 官方 MCP servers（@modelcontextprotocol/* 等） | stub 清單；實作以全局 npm 套件為準 |
| multi-agent-orchestrator/*.json | 自建（一人軟體公司） | 18 個多 Agent 編排組態 |
| devin-sandbox | Google-ai/devin-sandbox 副本 | tasks 目錄 |
| deployment/automation 資產 | 自建部署紀錄 | 見 docs/DEPLOYMENT_RECORD.md |

## 驗證狀態

- [x] skills/ 8 bundle 內容完整性（3538 檔追蹤，無 gitlink）
- [x] SECURITY_SCAN.md（既有）
- [x] .gitignore 涵蓋敏感檔（.env*/.pg-pass/.sim-key/auth.json/*.pem）
- [ ] mcp-servers 實作補齊（stub → 正式，待後續部署時以官方套件安裝）