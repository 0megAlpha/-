# Agent / Skill 三大 Repository 整理報告

> 產出日期：2026-09-17 ｜ 執行原則：不刪能力、不破壞環境、不新增第四個 Repository、敏感資訊不入 git、來源一律保留。

---

## 1. OpenHands

### 正式 Repository
- **本機路徑**：`/root/open-hands`（完整版：Python core + frontend + openhands-ui + openhands-extensions + enterprise/tests）
- **GitHub**：`xh09411-web/open-hands`（main 分支，HEAD `a22efddf20`）
- 另有舊 checkout `/root/openhands`（my-custom 分支，remote 相同，未動）

### 發現什麼
- `skills/`：27 個 OpenHands 原生 skills（agent-builder、code-review、github、gitlab、kubernetes、ssh 等，README 完整）
- `.agents/skills/`：5 個已追蹤自訂 skills（cross-repo-testing、custom-codereview-guide、release、upcoming-release、update-sdk）
- `openhands-extensions/`：完整擴展專案（含 plugins：vulnerability-remediation、skill-optimizer 等）
- 未提交變更 216 個（多為上游測試/同步檔案，未動）

### 新增什麼
- （本次**未新增**：發現 `Google-ai/openhands-core/.agents/skills/` 有 41 個 OpenHands 原生自訂 skills（BrowserGym、CI-CD-Watcher、Docker-Sandbox-Plus、SonarQube-Linter、zero-knowledge-proof-auth 等，遠端 identical e295baf），擬整合進正式 repo — **審批被取消，列「待確認」**，未動 open-hands 內容）

### 保留 / 優化
- OpenHands 全部能力保留，未刪任何檔案
- openhands service 雖停止，但 repo/資產完整，未因 service 停止而動任何東西

### Skill / Agent / Plugin / MCP / Runtime
- Skill：27 個原生 skills 完好；.agents/skills 5 個自訂完好
- Agent：Agent Canvas/microagents 於 `.agents/`、`openhands/` core 完好
- Plugin：openhands-extensions/plugins 完好
- MCP：OpenHands core 內建 MCP 支援（未改動）
- Runtime：openhands CLI 未安裝（僅 repo）；不因 service 停止刪除資產

### 驗證結果
- [x] Repo git 完整性（HEAD a22efddf20，remote 對應 open-hands）
- [x] 27 個原生 skills 存在且有 README
- [x] `.agents/skills/` 5 個自訂均已追蹤（1 個有本地修改，保留）

---

## 2. Hermes

### 正式 Repository
- **本機路徑**：`/root/.hermes`（Hermes runtime + git repo）
- **GitHub**：`xh09411-web/hermes-007`（HEAD `4fb7345`）
- Hermes service 已停止（`.clean_shutdown`），但 repo/資產完整 — 未刪除任何資產

### 發現什麼
- `skills/`：33 個類別（71 個 SKILL.md），含 autonomous-ai-agents、creative、research、vps-bridge、software-development 等
- runtime 資產：config.yaml、SOUL.md、moa.yaml、apollo/memory_core.py、bin/（tirith、uv、uvx）、platforms/、kanban.db、state.db（gitignore 已涵蓋 db/logs）
- `.skills_prompt_snapshot.json`：70 個 skills 快照（Hermes 可載入索引）
- hermes CLI：`/usr/local/bin/hermes` 正常（--help 可用）

### 新增什麼（本次整理 ✅）
- **`core/skills/`：30 個 Hermes core skills（skill.py 格式）**，從 `Google-ai/hermes-007/core/skills` 複製整合（來源：hermes-007 repo commit `c42ef45`）
  - 清單：cross-repo-dependency-mapper、hyperparameter-auto-tuner、architecture-boundary-reviewer、multi-tenant-isolation-guard、continuous-compliance-auditor、meta-prompt-generator、predictive-resource-scaler、context-window-sliding-controller、backup-redundancy-trigger、concurrency-deadlock-resolver、legal-open-source-license-checker、semantic-drift-detector、strategic-task-decomposer、sandbox-security-audit 等 30 個
- **`CORE-SKILLS-SOURCES.md`**：來源紀錄（來源 URL、commit、驗證狀態）
- 已 staged（git add），**commit/push 待批准**

### 保留 / 優化
- 原有 33 類 skills 全部保留
- 新增的 core/skills 以普通檔案追蹤（30 個 skill.py，無 gitlink）
- 來源 `/root/Google-ai/hermes-007` 未刪

### Skill / Agent / Plugin / MCP / ACP / Runtime
- Skill：33 類 + 新增 30 個 core skills = 71+ SKILL.md + 30 skill.py
- Agent：Hermes 本體 agent 完好（config/soul 未動）
- Plugin：platforms/pairing 等未動
- MCP：native-mcp 文件於 skills 內（未動）
- ACP：未動
- Runtime：node/、bin/ 未動

### 驗證結果
- [x] hermes CLI 可執行、--help 正常
- [x] 71 個 SKILL.md 存在
- [x] 30 個 core skill.py 已追蹤（staged）
- [x] config.yaml 解析正常（skills 設定節存在）
- [x] 無敏感資訊入 git

---

## 3. AI-Agent-Skill

### 正式 Repository
- **本機路徑**：`/root/AI-Agent-Skill` ｜ **GitHub**：`xh09411-web/Ai-Agent-Skill`（HEAD `2edbc7e`）

### 新增哪些 Skill
- 本次**補齊追蹤** 5 個 bundle 的完整內容（原本是 gitlink/submodule 殘留，clone 後內容會是空的）：
  - addyosmani-agent-skills（addyosmani/agent-skills）
  - awesome-claude-code-toolkit（rohitg00/awesome-claude-code-toolkit）
  - claude-forge（immacualate/claude-forge，含 cc-chips）
  - gstack（garrytan/gstack）
  - superpowers（obra/superpowers）
  - 共 **3538 個檔案**改為普通檔案完整追蹤（179 個 SKILL.md 涵蓋在內）
- **README.md**（原本缺失）：新增，說明目錄結構、8 套 bundle 來源、維護契約
- **docs/SOURCES.md**：完整來源紀錄（URL、原始 HEAD、驗證狀態）

### 新增哪些 Agent capability
- multi-agent-orchestrator/：18 個 JSON agent 編排組態（既有，保留）
- opencode-engine/plugins、openai-brain/sdk_configs（既有，保留）
- hermes-brain/core/skills 9 個（既有，保留；30 個 core skills 已歸入 Hermes repo）

### 新增哪些 Plugin / MCP / ACP
- Plugin：.claude-plugins/ 33 個（既有，保留）；.cline/plugins（既有）
- MCP：mcp-servers/ 14 個 stub（既有；已驗證對應全局 runtime 套件：docker→docker-mcp、kubernetes→mcp-server-kubernetes、npm→npm-mcp-server 等；stub 僅清單，實作以官方/全局套件為準，標註於 SOURCES.md）

### 哪些來自 Google-AI / OpenHands / Hermes / 昨天新增
- 來自 Google-ai：mcp-servers、kiro-powers、devin-sandbox、cc-suite 等（既有副本，來源紀錄於 SOURCES.md）
- 來自 OpenHands：openhands-core/.agents/skills（本 repo 內 gitignore，正式來源為 open-hands repo）
- 來自 Hermes：hermes-brain（9 個通用 skills）；30 個 core skills 已正確歸入 Hermes repo
- 昨天（9/14 後）新增：gitlink 修復 + README + SOURCES.md（本次）

### 去除哪些重複
- **移除 5 個懸空 gitlink**（submodule 模式 160000 但無 .gitmodules）：修復為內嵌檔案追蹤，消除「clone 後內容缺失」缺陷
- 6 個嵌套 .git 元資料移至 repo 內 `.embedded-git/`（gitignored、不刪除、可回滾）
- 未刪除任何能力

### 驗證結果
- [x] gitlink = 0（完全修復）
- [x] 179 個 SKILL.md 存在於 skills/
- [x] 3886 個檔案追蹤（原 352 個 → 3886）
- [x] 18 個指定 skills 全部存在且 SKILL.md OK（見第 4 節）
- [x] 敏感掃描通過（僅發現 regex/範例文字，無真實金鑰）
- [x] 安全：無 .env/.pg-pass/.sim-key/auth.json 追蹤

---

## 4. 昨天 2026-09-14 00:00 後安裝內容（完整清單）

### npm 全局套件（依安裝時間）
| 時間 | 套件 | 版本 | 最終歸屬 |
|---|---|---|---|
| 09-14 02:20 | opencode-ai | 1.18.30 | Agent runtime（保留原位） |
| 09-15 02:03 | dsh-hermes-memory | 1.1.10 | Hermes 記憶擴展（runtime） |
| 09-15 21:53 | ghost-blog | — | 一般套件（保留原位） |
| 09-16 10:30 | @deepseek-ai/dsh | 0.1.5-rc.1 | DSH（保留原位，不動核心） |
| 09-16 19:29~50 | opencode-*（16 個：oh-my-opencode, caveman, data-agent, daytona, github, handoff, helicone-session, linear, marketing-agent, obsidian, ocx, sales-agent, sentry-monitor, slack, superpowers, wakatime） | 0.0.1~4.19.4 | Agent runtime 插件（保留原位） |
| 09-16 19:30 | cline | 3.0.62 | Agent runtime（保留原位） |
| 09-16 19:30 | @openai/codex、@openai/agents | 0.154.0 / 0.17.0 | Agent runtime（保留原位） |
| 09-16 19:32-19:50 | skills-cli、skillswitch、cc-suite、uipro-cli、coding-agent-adapters、roo-cli、mcporter、gitnexus、qmd、firecrawl、firebase-tools/firebase-mcp-server、@ast-grep/cli、@upstash/context7-mcp、mcp-server-semgrep、pm2、biome、eslint、prettier、pnpm、yarn、bun、typescript、tsx、ts-node、claude-code-reviewer、playwright-*、semantic-release 系列、@memberjunction/ai-cerebras、@modelcontextprotocol/* | 多版本 | 基礎工具鏈/CLI（保留 package/runtime 管理方式） |
| 09-16 19:37 | @anthropic-ai/claude-code | 2.1.273 | Agent runtime（保留原位） |

### Skill / Agent / Plugin
- `/root/.agents/skills/`：38 個（.skill-lock.json v3）
  - **18 個指定 skills 全部已安裝且可發現**（building-pydantic-ai-agents、sentry-cli、teamcity-cli、use-railway、gcp-to-aws、cosmosdb-best-practices、firestore-data、spanner-data、convex-design、amplify-workflow、frontend-design、exa-search、searching-sourcegraph、knowledge-catalog-discovery、find-skills、cline-session-history、review-team、playground）
  - 其餘 20 個（save-to-spotify、attorney-assist 等）：既有安裝，屬通用 skill 庫，按「不刪能力」原則保留原位（未裝新、未卸載）
- `~/.claude/skills/`：14 個、`~/.claude-plugins`、`.config/opencode/skills`、`.codex/skills` 等（既有的 agent runtime 技能安裝位，保留）

### 最終歸屬說明
- 凡 Agent runtime/CLI（DSH、OpenCode、Cline、Claude Code、Codex 等）：**保留原本安裝位置與管理方式**（任務原則四）
- 通用 Skill 能力 → AI-Agent-Skill / skill 庫
- OpenHands/Hermes 專屬 → 對應 repo（Hermes core skills 本次已歸位）
- **一律未塞入 Google-AI**

---

## 5. 無法分類項目（真正待確認）

| 項目 | 位置 | 原因 |
|---|---|---|
| openhands-core 41 個 skills 整合 | Google-ai/openhands-core/.agents/skills | 明確屬 OpenHands，但整合複製的審批被取消 → **待你確認後執行** |
| Google-ai 內其餘未追蹤項（deepseek-harness/、lody/、tasks/、portal/、research/、build-your-own-x-ref/、terminal-bench/、deploy-docs/） | /root/Google-ai | remote 指錯（open-hands）+ 混合內容，多為設定/研究/部署文件，不屬三大 repo 能力資產 → **列待確認，未動** |
| agent-platform（第四個 repo，legacy remote） | /root/agent-platform | 非本次三大 repo 範圍，保留原位不歸類 |
| ai-agent-workflows / ai-company（副本目錄） | /root | 舊副本（remote=Ai-Agent-Skill），保留不刪、不歸類 |
| ghost-blog | npm 全局 | 用途不明的一般套件，待確認 |

---

## 6. 已完成的優化

1. **AI-Agent-Skill gitlink 修復**（核心）：5 個 skills bundle 由懸空 submodule(gitlink) 改為內嵌檔案完整追蹤（+3538 檔案），消除「clone 後 skills 內容為空」的 Repository 不完整缺陷；6 個嵌套 .git 元資料集中至 `.embedded-git/`（gitignored、可回滾）
2. **AI-Agent-Skill README**：新增（原本缺失），統一結構說明 + 維護契約
3. **AI-Agent-Skill docs/SOURCES.md**：新增完整來源紀錄（8 bundle + 各資產來源 URL/HEAD）
4. **Hermes core/skills 整合**：30 個 Hermes core skills 由 Google-ai 副本歸入正式 Hermes repo + CORE-SKILLS-SOURCES.md 來源紀錄
5. **gitignore 補強**：`.embedded-git/`（AI-Agent-Skill）
6. **安全掃描**：三大 repo 敏感資訊掃描（真實金鑰 0 筆）
7. 未刪除任何能力、未修改任何 agent 核心配置（Lody/DSH/OpenCode/Cline/Codex/Google-AI 均未動）

---

## 7. 驗證（逐項）

| 項目 | 結果 |
|---|---|
| Agent 可載入 | hermes CLI ✓（--help OK）；opencode 1.18.30 ✓；cline 3.0.62 ✓；claude-code 2.1.273 ✓；codex 0.154.0 ✓；dsh 0.1.5-rc.1 ✓；skills CLI ✓ |
| Skill 可發現 | 18 個指定 skills ✓（/root/.agents/skills 全數 SKILL.md OK，lock 註冊 18/18）；AI-Agent-Skill 179 SKILL.md ✓；Hermes 71 SKILL.md + 30 skill.py ✓ |
| Plugin 可載入 | openhands-extensions/plugins、.claude-plugins/33、opencode-engine/plugins 結構完好 ✓（未嘗試載入，避免副作用） |
| MCP 正常 | 14 stub 對應全局 runtime ✓（docker→docker-mcp、kubernetes→mcp-server-kubernetes、npm→npm-mcp-server、filesystem/github/postgres→@modelcontextprotocol/server-* 已全局安裝） |
| ACP 正常 | 未發現獨立 ACP 元件需驗證（Hermes/OpenHands 支援保留） |
| dependency 正常 | mcp-servers 無 node_modules（stub 清單，非缺失）；Hermes node/ 完整（4749 tracked）；AI-Agent-Skill 無未安裝依賴阻塞 |
| Repository 完整 | AI-Agent-Skill：gitlink 0、3886 檔追蹤 ✓；Hermes：core/skills 30 追蹤 ✓；open-hands：完整 ✓ |

---

## 8. 尚未完成（真正待完成）

1. **Commit + Push 三 repo**（AI-Agent-Skill、Hermes）：整理內容已 staged，但 commit 審批被取消 → 待你批准後我執行 `git commit` + `git push`（AI-Agent-Skill、hermes-007 兩個 remote）
2. **OpenHands 41 個 skills 整合**（選做）：確認後我再把 `Google-ai/openhands-core/.agents/skills` 41 個 skills 複製進 `/root/open-hands/.agents/skills` 並 commit/push
3. mcp-servers stub → 正式實作安裝（屬後續部署，非本次，待你指示）

---

## 9. 後續部署（只列，不執行）

- mcp-servers stub 補實作（以官方套件 npm install 於對應目錄）
- OpenHands service / Hermes service 重啟與驗證
- 其他你之後指示的部署項目

---

## ⚠️ 需要你批准的行動（審批兩次被取消，我已停止）

1. **`git commit` + `git push`**：AI-Agent-Skill（gitlink 修復 + README + SOURCES）與 hermes-007（30 core skills + 來源紀錄）— 內容已 staged，一鍵可完成，commit message 已擬好
2. **（選做）openhands 41 skills 整合**：明確屬 OpenHands 的能力，複製進正式 repo

請回覆「批准 commit/push」或指示其他範圍，我再繼續。未批准前我不會再對三大 repo 寫入。