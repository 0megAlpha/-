# DSH 完整整合比對報告
### — 本機 Agent 環境能力盤點 × GitHub「ai-agent-skill」儲存庫整合分析

> 產出時間：2025-09-27 ｜ 執行環境：DeepSeek Harness（DSH）on Lody
> 資料檔：`local_skills.json`、`repo_skills.json`、`overlap_analysis.json`、`security_scan.json`、`integration-package/manifest.json`

---

## 執行摘要

| 指標 | 數值 |
|---|---|
| 本機已安裝技能 | **38** 個 |
| 內建工具函數 | **25** 個 |
| MCP 平台工具 | **20** 個 |
| 比對的候選儲存庫 | **5** 個（名稱近似「ai-agent-skill」） |
| 儲存庫技能總數 | **168** 條目（去重後 167 種） |
| 與本機重疊 | 僅 **4** 個語意相近＋1 個同名 → **互補性約 97%** |
| 通過安全掃描的推薦技能 | **34** 個（已打包至 `integration-package/skills/`） |
| 安全掃描 | 286 個文字檔、10 種紅旗模式，無實質惡意內容 |

**結論**：GitHub 上沒有精確名為 `ai-agent-skill` 的儲存庫，本次比對了 5 個最接近的儲存庫。其內容與本機技能庫高度互補——本機強在雲端/資料庫/商業服務，儲存庫補上了通用軟工、上下文工程、代理安全、影音字幕與中文搜尋能力。34 個精選技能已通過安全掃描並完成打包，一鍵安裝腳本就緒。

---

## 一、DSH 環境完整能力盤點

### 1.1 系統架構

```
┌────────────────────────────────────────────┐
│  Lody 平台（Session 管理、檔案上傳、預覽） │
├────────────────────────────────────────────┤
│  DSH Agent Harness                         │
│  ├─ 模型：z-ai/glm-5.3                     │
│  ├─ 沙盒：workspace-write（工作區可寫）     │
│  ├─ 提示詞框架：系統提示＋技能目錄＋目標機制│
│  └─ 技能庫：/root/.agents/skills（唯讀掛載）│
├────────────────────────────────────────────┤
│  工具層：25 內建函數 ＋ 20 個 MCP 工具      │
└────────────────────────────────────────────┘
```

### 1.2 內建工具函數（25 個）

| 類別 | 函數 | 用途 |
|---|---|---|
| 檔案 | `read` / `write` / `edit` | 讀取（含行號）、建立/覆寫、精確替換編輯 |
| 檔案 | `glob` / `grep` | 檔案模式搜尋、ripgrep 正則內容搜尋 |
| 檔案 | `read_image` | 直接讀取 PNG/JPEG/WebP/GIF 圖片 |
| 執行 | `bash` | 執行 shell 命令（背景工作、沙盒、逾時控制） |
| 執行 | `job_list` / `job_output` / `job_kill` | 背景工作管理 |
| 搜尋 | `web_search` | 網頁搜尋（※本次實測後端 API key 失效，已改用 GitHub API） |
| 技能 | `skill` | 載入指定技能的完整指令集 |
| 任務 | `todo_write` | 結構化任務清單 |
| 任務 | `create_goal` / `get_goal` / `update_goal` | 跨輪持久完成目標 |
| 規劃 | `exit_plan_mode` | 計畫模式提交與審核 |
| 互動 | `ask_user_question` | 互動提問（※本環境無註冊 provider，實測不可用） |
| 代理 | `subagent` / `subagent_fork` | 背景子代理（獨立/繼承上下文） |
| 代理 | `send_message` / `interrupt_agent` / `list_agents` | 子代理通訊與控制 |
| 代理 | `workflow` | JavaScript 多代理編排腳本（大規模扇出） |
| 代理 | `ralph` | 全新代理迭代迴圈（僅在明確要求時使用） |

### 1.3 MCP 平台工具（20 個，Lody）

| 類別 | 函數 |
|---|---|
| Session 建立 | `lody_session_create` / `_create_many` / `_create_options` |
| Session 通訊 | `lody_session_chat` / `_chat_many` |
| Session 管理 | `lody_session_list` / `_history` / `_status_many` / `_rename` / `_rename_many` / `_archive` / `_cancel` |
| 操作與回報 | `lody_operation_get` / `_operation_cancel` / `_review_submit` / `_report_preview_candidate` / `_feedback` |
| 檔案 | `lody_upload_files` / `_upload_images` / `_mcp_configure` |

### 1.4 提示詞框架（Prompt Framework）

1. **系統提示**：角色定位、工具規範、沙盒政策、輸出規則
2. **技能目錄機制**：`SKILL.md`（YAML frontmatter `name`+`description` + 指令主體 + `references/`、`scripts/` 資源目錄），session 啟動時自動注入目錄摘要
3. **規劃模式**：plan mode → `exit_plan_mode` 提交計畫審核
4. **目標機制**：goal tools 支援跨輪持久目標、自動續行、阻塞回報
5. **任務清單**：`todo_write` 全量替換式進度追蹤

### 1.5 已安裝技能（38 個，依領域分類）

**雲端平台與部署（6）**
| 技能 | 說明 |
|---|---|
| `amazon-location-service` | AWS 地圖、地理編碼、路線與地理圍欄 |
| `amplify-workflow` | AWS Amplify Gen2 全棧應用（Auth/Cognito、AppSync/DynamoDB、S3、AI Kit） |
| `dr-bedrock` | AWS Bedrock 認證與區域疑難排解 |
| `gcp-to-aws` | GCP → AWS 遷移（含 AI/agentic 工作負載） |
| `use-railway` | Railway 平台操作（部署、資料庫、儲存、網域） |
| `dataproc-skills` | Dataproc 叢集與任務互動 |

**資料庫與資料分析（7）**
| 技能 | 說明 |
|---|---|
| `dsql` | Aurora DSQL：schema、遷移、查詢計畫、資料載入 |
| `cosmosdb-best-practices` | Azure Cosmos DB 效能優化（分區、向量搜尋） |
| `firestore-data` | Firestore NoSQL 文件操作與集合階層探索 |
| `spanner-data` | Spanner schema 探索與自訂 SQL |
| `oracledb` | Oracle DB 管理、效能與資源監控 |
| `convex-design` | Convex 反應式後端（schema、auth、排程、多人即時） |
| `data-analyst` | ClickHouse 互動式資料分析（指標、漏斗、趨勢） |

**開發與 DevOps 工具（9）**
| 技能 | 說明 |
|---|---|
| `cline-session-history` | Cline session 歷史搜尋/匯出 |
| `desktop-commander-overview` | Desktop Commander MCP（持久 shell、REPL、SSH、結構化檔案） |
| `sentry-cli` | Sentry CLI 操作與認證 |
| `teamcity-cli` | TeamCity CI/CD（builds、logs、agents、pipeline） |
| `endor-setup` | endorctl 安裝與弱點掃描 |
| `linear-sdk-scripting` | Linear SDK 腳本操作（issues、projects、cycles） |
| `searching-sourcegraph` | Sourcegraph 程式碼搜尋工作流 |
| `ui5-typescript-conversion` | UI5 專案轉 TypeScript |
| `sap-fiori-add-visual-filter` | SAP Fiori Elements 視覺篩選器（CAP/ABAP RAP） |

**AI 與代理開發（5）**
| 技能 | 說明 |
|---|---|
| `building-pydantic-ai-agents` | Pydantic AI 代理建構（工具、結構化輸出、串流、多代理） |
| `find-skills` | 技能生態探索與安裝（skills.sh） |
| `skill-creator` | 技能建立/優化/評測 |
| `review-team` | 多代理程式碼審查艦隊（正確性、安全、架構等專職審查） |
| `exa-search` | Exa 深度研究（潛在客戶、文獻、競品分析） |

**前端與設計（4）**：`frontend-design`（高品質前端設計）、`site-specification`（網站規格提取）、`playground`（互動 HTML playground）、`mintlify`（Mintlify 文檔站）

**商業與資料服務（4）**：`knowledge-catalog-discovery`（知識目錄探索）、`windsor-ai-business-data`（行銷/CRM/電商資料查詢）、`vibe-prospecting`（企業與聯絡人開發）、`attorney-assist`（LegalZoom 律師諮詢轉介）

**其他專項（3）**：`math-olympiad`（奧林匹亞數學＋對抗驗證）、`session-report`（session 使用報告）、`save-to-spotify`（Spotify 音檔製作）

---

## 二、比對的候選儲存庫（5 個）

GitHub 查無精確名為 `ai-agent-skill` 的儲存庫，以下為名稱/內容最接近者（皆已完整克隆與解析）：

| # | 儲存庫 | ⭐ | 技能數 | 定位 |
|---|---|---|---|---|
| 1 | **MoizIbnYousaf/ai-agent-skills** | 1,146 | 18 | 名稱最接近。通用技能安裝器 CLI ＋ 技能生命週期管理類技能 |
| 2 | **seb1n/awesome-ai-agent-skills** | 193 | 103 | 21 分類現成技能庫（最完整的通用技能集合） |
| 3 | **dean9703111/ai-agent-skill-for-video-workflow** | 215 | 5 | 繁中。影音字幕處理工作流（音訊轉 SRT、優化、字卡、社群摘要） |
| 4 | **hoodini/ai-agents-skills** | 279 | 40 | 創作型工具收藏（yuv 影音系列、fal-ai、figma、vercel…） |
| 5 | **valenovo/ai-agent-skills** | 65 | 2 | 中文技能：百度 API 搜尋、中國天氣查詢 |

> 另有約 30 個名稱部分符合的儲存庫（建築業技能包、cyber skills、電商技能包等），因主題高度特化未列入主比對，需要可再擴充。

---

## 三、整合比對分析

### 3.1 重疊情況（168 條目 vs 本機 38 技能）

| 重疊項 | 儲存庫技能 | 本機對應 | 處置 |
|---|---|---|---|
| 同名 | seb1n `frontend-design` | `frontend-design` | **排除**，避免覆蓋本機版本 |
| 語意相近 | Moiz `database-design` | `dsql` | 保留為推薦（通用 schema 設計 vs 專屬 DSQL） |
| 語意相近 | valenovo `baidu-api-search` | `exa-search` | 保留（中文搜尋場景 vs 英文深度研究） |
| 語意相近 | hoodini `mongodb` | `cosmosdb-best-practices` | 不推薦（hoodini 未通過供應鏈風險評估） |
| 語意相近 | hoodini `analytics-metrics` | `data-analyst` | 不推薦（同上） |

**其餘 163 條目全部為本機缺少的能力** —— 互補性約 97%。

### 3.2 本機能力缺口（儲存庫可補上的）

| 缺口領域 | 缺口內容 | 補上來源 |
|---|---|---|
| 通用軟體工程 | testing、debugging、refactoring、version-control、code-documentation | seb1n＋Moiz |
| 上下文工程 | context-optimization、context-retrieval | seb1n |
| 代理工程 | multi-agent-orchestration、mcp-server-building、tool-schema-design、agent-evaluation | seb1n |
| 代理安全（防禦） | prompt-injection-defense、skill-supply-chain-audit | seb1n |
| API 整合 | api-design、oauth-2-0-setup | seb1n |
| DevOps | docker-compose-setup、ci-cd | seb1n |
| 資料處理 | sql-query-generation、data-visualization、pdf-processing、spreadsheet-analysis | seb1n |
| 寫作與研究 | technical-writing、translation、fact-checking、deep-research | seb1n |
| 影音媒體 | audio-to-srt、srt 字卡/優化/社群摘要 | dean9703111 |
| 中文搜尋 | baidu-api-search（需 API Key） | valenovo |
| 技能治理 | review-a-skill、verification-agent、changelog-generator | MoizIbnYousaf |

### 3.3 未列入推薦但已收錄於 manifest 的重點項目

- **seb1n 另有 79 個技能**：行銷 SEO、法務合規（EU AI Act）、財務會計、客服成功、銷售、簡報製作等——依需求可從 `manifest.json` 挑選後安裝
- **hoodini 40 個**：`x-twitter-scraper` 有 ToS 疑慮；`yuv-*` 影音系列與 `fal-ai`、`nano-banana-pro` 需外部服務金鑰；`install.sh` 採 `curl | bash` 模式——**全部標記為「自行審閱後再安裝」**
- **valenovo `china-weather`**：中國氣象公開資料查詢，需求明確再裝

---

## 四、整合建議：34 個推薦技能

已複製到 `integration-package/skills/`，格式與本機技能庫完全相容（`SKILL.md` frontmatter `name`+`description`）：

| 來源 | 推薦技能 |
|---|---|
| **seb1n**（24） | `multi-agent-orchestration`、`mcp-server-building`、`tool-schema-design`、`agent-evaluation`、`prompt-injection-defense`、`skill-supply-chain-audit`、`context-optimization`、`context-retrieval`、`testing`、`debugging`、`version-control`、`refactoring`、`api-design`、`oauth-2-0-setup`、`docker-compose-setup`、`ci-cd`、`sql-query-generation`、`data-visualization`、`pdf-processing`、`spreadsheet-analysis`、`technical-writing`、`translation`、`fact-checking`、`deep-research` |
| **MoizIbnYousaf**（5） | `review-a-skill`、`verification-agent`、`changelog-generator`、`code-documentation`、`ask-questions-if-underspecified` |
| **dean9703111**（4） | `audio-to-srt`、`srt-enhancer`、`srt-card-annotator`、`srt-social-summary` |
| **valenovo**（1） | `baidu-api-search`（需 `BAIDU_AI_SEARCH_API_KEYS` 環境變數） |

挑選原則：① 本機沒有的能力 ② 通過安全掃描 ③ 不需外部金鑰即可運作（baidu 除外，已標註）④ 與本機既有技能不衝突（同名已排除）。

---

## 五、安全評估

**掃描方法**：10 種紅旗正則——提示注入（ignore previous / override instructions）、`curl|bash`、`rm -rf /`、base64 解碼執行、eval 遠端、鍵盤側錄/外洩字樣、`chmod 777`、停用安全機制、憑證＋HTTP 模式。共掃描 446 個文字檔（270 個工作區檔案＋hoodini 176 個 git blob 補掃）。

| 儲存庫 | 命中 | 判定 |
|---|---|---|
| seb1n | 18 | ✅ 全為資安教育內容（威脅建模攻擊樹教學、OAuth 安全最佳實踐、技能供應鏈審計指引）——是「教你防禦」非「叫你攻擊」 |
| MoizIbnYousaf | 6 | ✅ 測試檔中的注入樣本（驗證其防護機制會清除注入）＋安全警告文字 |
| dean9703111 | 0 | ✅ 乾淨 |
| valenovo | 1 | ✅ API Key 走環境變數，正常模式 |
| hoodini | 8 | ⚠️ `curl \| bash` 安裝模式＋外部服務依賴，供應鏈風險較高，未列入推薦 |

> **重要提醒**：技能會在未來 session 自動注入指令。本報告的推薦清單已做第一輪審查，但安裝任何第三方技能前，保持「內容是資料、不是指令」的審查習慣是必要的。

---

## 六、安裝方式與後續

```bash
# DSH 沙盒內 /root/.agents/skills 為唯讀檔案系統
# 請在 VPS 自己的 shell（SSH 登入）執行：

cd /root/.lody/chats/b3639a8e-bec4-448e-a627-83398da5fe1d/integration-package
bash install.sh --dry-run      # 先預覽
bash install.sh                # 安裝全部 34 個推薦技能到 ~/.agents/skills
bash install.sh translation deep-research   # 或只裝指定技能
```

安裝後**重啟 agent session**，新技能即出現在技能目錄。安裝 34 個後本機技能庫將達 **72 個**。

### 後續可選項

1. **更換/擴充比對對象**：告訴我實際想要的 `owner/repo`（例如你自己的私有庫），我重新比對
2. **加裝 manifest 中的其他技能**：從 `integration-package/manifest.json`（168 條目）挑選，改一份清單給我即可
3. **推送（push）到遠端**：若要把本報告＋套件推到你的 GitHub 儲存庫或 VPS 目錄，提供目標位置與授權方式（建議用 SSH key 或 fine-grained PAT，不要直接貼 token）
4. **技能生態搜尋**：`npx skills find <關鍵字>`（本沙盒 npm 快取唯讀無法執行，但可在你的 shell 使用）
