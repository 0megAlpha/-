# AI Agent Skills — 共用能力庫

本目錄是跨 Agent 共用的能力資產來源，不是另一個 Agent Runtime。只保存已確認可由多個 Agent／Framework 共用的 Skills、工具、MCP 元件、Plugin adapters、工作流程與文件。

## 單一來源與歸屬規則
- Agent 本體、專屬設定、專屬工具、Skills、Plugins、MCP adapter 和執行工作流，必須放在該 Agent 的唯一 canonical 目錄。
- OpenHands 專屬能力放在 openhands/；Hermes 專屬能力放在 hermes/；DSH 專屬能力放在 dsh/；Open WebUI 專屬能力放在 openwebui/。
- 其他獨立 Agent 的專屬資產放在 agents/<agent-id>/。
- 本目錄 skills/、plugins/、mcp-servers/、tools/、workflows/ 僅保存 framework-neutral、可被多個 Agent 重用的單一來源。
- Agent 專屬套件不得只放在共用庫，否則單獨拉取 Agent 目錄會缺能力。
- 若共用資產需要 Agent-specific adapter，adapter 放在 Agent 目錄，核心實作仍只保留一份在共用庫。

## 資產分類
| 路徑 | 責任 |
|---|---|
| agents/ | Agent 定義、角色提示、能力設定與協作規格 |
| skills/ | 多 Agent 可重用的 Skill bundles |
| .claude-plugins/ | Claude Code 相容 Plugin／marketplace |
| .cline/ | Cline 相容設定與 Plugin adapter |
| mcp-servers/ | 通用 MCP server 來源、啟動規格、工具與資源契約 |
| plugins/ | 多 Agent 可重用 Plugin 實作 |
| tools/、scripts/ | 可獨立測試的通用工具 |
| workflows/、multi-agent-orchestrator/ | 跨 Agent 任務拆分、狀態流轉、檢查與交付流程 |
| references/、docs/ | 上游來源、版本、License、整合與驗證紀錄 |
| memory/ | 可移植記憶格式與 adapter；不得放即時 session、憑證或私人對話資料 |

## 已盤點來源
VPS 同名來源目錄包含通用開發、Code Review、安全、Research、Frontend、Kubernetes、Docker、GitHub、Vercel、Notion、Superpowers、GStack、Kiro Powers、Claude/Cline/OpenCode adapters、多 Agent 編排、MCP bridge、Filesystem、Browser automation、測試與部署能力。來源目錄存在不代表已安裝、已載入或通過執行測試；stub、範例和連結必須標示為 stub/reference，不得冒充完整實作。

## 整合與驗收
1. 記錄來源 Repository、License、版本／Commit、依賴和目標 Agent。
2. 檢查同名／同功能資產，先比較內容、歷史、授權與測試，再決定共用或保留專屬副本。
3. 安裝前執行秘密掃描、依賴檢查與隔離測試。
4. 通用資產放本庫；專屬資產直接隨所屬 Agent 完整目錄保存。
5. 驗證 Skill frontmatter、Plugin manifest、MCP initialize/list_tools、工具真實呼叫及 Agent 啟動流程。
6. 記錄來源、版本、安裝位置、測試結果、必要環境變數名稱（不包含值）和回復方式。

## 去敏
禁止提交 .env、Token、API Key、Cookie、Authorization header、私鑰、憑證庫、SSH material、資料庫傾印、使用者 session、即時記憶資料庫、含秘密的 Log、私有模型權重及未審查備份。Public repository 也不得包含可定位實際主機的內部 port map、IP 或私有部署 endpoint。

## 狀態
這是共用能力資產庫，不是部署完成聲明。各 Agent 的專屬能力仍需按 canonical folder 完成比對、安裝、載入與功能驗證。來源記錄放在 docs/SOURCES.md；沒有來源、授權或測試證據的項目不得標記為已完成。
