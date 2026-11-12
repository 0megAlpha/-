# AI Agent Skills — 共用能力庫

本目錄是跨 Agent 共用的能力資產來源，不是另一個 Agent Runtime。它保存可重用的 Skills、工具、MCP 元件、Plugin adapter、工作流程與文件，供 OpenHands、Hermes、Claude Code、OpenCode、Cline、Aider 等既有 Agent 按需整合。

## 單一來源與目錄歸屬

遵守「一個 Agent 一個專屬目錄」：

- Agent 本體、專屬設定與專屬執行程式只放在對應的 `agents/<agent-id>/` 或既有頂層 Agent 目錄。
- OpenHands 專屬能力歸入 `openhands/`；Hermes 專屬能力歸入 `hermes/`。
- 跨框架可共用的能力只保留一份，放在本目錄的 `skills/`、`plugins/`、`mcp-servers/`、`tools/` 或 `workflows/`。
- 各 Agent 目錄只保留 adapter、manifest 或安裝引用，不再複製一份相同的 Skill／Plugin 原始碼。
- 同名或近似目錄先做完整檔案樹、Git 歷史、來源與功能比較；未證實等價前不得刪除或合併。

## 資產類別

| 路徑 | 責任 |
|---|---|
| `agents/` | Agent 定義、角色提示、能力設定與代理協作規格 |
| `skills/` | 可被多個 Agent 載入的 Skill bundles 與流程知識 |
| `.claude-plugins/` | Claude Code 相容 Plugin adapter／marketplace 定義 |
| `.cline/` | Cline 相容設定與 Plugin adapter |
| `mcp-servers/` | MCP server 來源、啟動規格、工具與資源契約 |
| `plugins/` | 可重用 Plugin 實作與掛載設定 |
| `tools/`、`scripts/` | 可獨立測試的工具與維運輔助程式 |
| `workflows/`、`multi-agent-orchestrator/` | 多 Agent 任務拆分、狀態流轉、檢查與交付流程 |
| `references/`、`docs/` | 上游來源、版本、License、整合與驗證紀錄 |
| `memory/` | 可移植的記憶格式與 adapter；不得放入即時 session、憑證或使用者秘密 |

## 已盤點的能力範圍

VPS 上可讀取的同名來源目錄包含以下能力集合；這些是來源盤點項目，不代表每個套件都已安裝、已載入或通過執行測試：

- Skills：`skills/` 下的通用開發、Code Review、Security、Research、Frontend、Kubernetes、Docker、GitHub、Vercel、Notion、Superpowers、GStack、Kiro Powers 等項目。
- Plugin adapters：Claude 相容 Plugin 集合、Browser Use、Code Review、MCP Bridge、Filesystem、Test Coverage、Task Runner、Frontend Design、Google Workspace 等。
- MCP 元件：AWS、Deno、Docker、Fetch、Filesystem、GitHub、Jupyter、Kubernetes、NPM、PostgreSQL、SQLite、UV、Technical Writing 等。
- Framework adapters：Claude Code、OpenCode、Devin、OpenClaw、Open WebUI、Hermes 與多 Agent 編排定義。
- Workflow／工具：任務拆分、記憶、研究、部署、協作監控、依賴檢查、品質檢查與文件產出。

來源清單與實際可執行狀態必須分開記錄。若一個項目只有 stub、範例或連結，不能標記為已安裝的完整 MCP server／Plugin。

## OpenHands 整合契約

OpenHands 是主要程式實作 Agent。整合採用既有 OpenHands Runtime 與 Docker sandbox，不另建立第二套 OpenHands 核心。

- OpenHands 專屬 Skills／Plugins 放在 `openhands/` 的唯一對應位置。
- 通用 Skills 由本目錄維護單一來源，再透過 OpenHands adapter 掛載。
- Aider 用於多檔案程式碼編輯；LangGraph 用於可觀測、可重試的工作流狀態管理。
- Playwright 用於瀏覽器端到端測試；測試結果、截圖與 Console／Network 錯誤應回傳工作流進行修正。
- Dify 可作為視覺化 Workflow／模型工具管理層；避免再部署第二套功能重疊的總控服務。
- Coolify 僅保留 API adapter／部署工作流定義；只有在 Coolify Server 與 API Token 已配置並驗證後，才宣告可部署。
- 反覆修正需設定最大重試數、超時、成本上限、差異檢查與人工升級條件；不得使用無上限迴圈。

## Skill 與 Plugin 安裝規範

1. 每一項資產先確認來源 Repository、License、版本、依賴、安裝方式與維護狀態。
2. 安裝前檢查同名／同功能資產是否已存在；可共用則引用既有唯一來源。
3. 先以隔離環境執行單元測試、型別／Lint、MCP initialize/list_tools 或 Plugin manifest 驗證。
4. 再安裝到對應 Agent 的 adapter／registry；不得把全域依賴清單直接灌入所有 Agent。
5. 更新後記錄版本、來源 Commit、測試結果、必要環境變數名稱（不包含其值）與回復方式。

## 去敏與禁止提交項目

禁止提交 `.env`、`.env.*`、Token、API Key、Cookie、Authorization header、私鑰、憑證庫、SSH material、資料庫傾印、使用者 session、即時記憶資料庫、含秘密的 Log、私有模型權重及未審查的備份。

範例設定只能使用明確假值，並且在提交前對工作樹與將提交的內容執行秘密掃描。若 Repository 可見性為 Public，不得加入可定位實際主機、服務入口或內部網路的未去敏維運資料。

## 目前狀態與限制

- 本文件已整理原有衝突 README 的兩套說明；舊 README 的 Git merge-conflict markers 已移除。
- 來源目錄的實際安裝腳本尚未完成權限與內容審核；不能僅因檔案存在就執行。
- Skills／Plugins／MCP 清單是待逐項核實的來源盤點，不代表全部已完成部署。
- OpenHands、Dify、LiteLLM 與相關服務的實際版本、Volume、掛載、健康狀態和端口屬於獨立部署盤點；不可由本文件推定。
- 完整 VPS root-only 掃描、舊帳號私有 Repository 讀取、Runtime 更新與快取清理，必須在權限及來源可讀取後另行驗證。

## 來源與維護

每個新增或更新的第三方能力，必須在 `docs/SOURCES.md` 記錄原始 URL、版本／Commit、License、檢查日期、整合位置與驗證結果。保留上游 LICENSE／NOTICE，不把第三方程式碼誤標成自有實作。
