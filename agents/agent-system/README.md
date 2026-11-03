# agent-system — 多 Agent 協作框架

多 Agent 資料鏈接（Pipeline）框架，透過 LiteLLM 閘道串接 LLM，全部敏感參數環境變數隔離。

## 架構
```
├── .env.example            # 環境變數範例（無真實金鑰，值皆為佔位符）
├── .gitignore              # 屏蔽 .env / *.pem / keys/ / 執行期資料
├── config/settings.json    # 全局設定 + Agent 註冊 + 管線定義（無 secret）
├── agents/                 # 8 個 Agent 模組
│   ├── base_agent.py       # 基礎類別（env 讀取 / redact / LLM 客戶端 / mock）
│   ├── researcher.py       # 網路/文件檢索
│   ├── scraper.py          # 網頁抓取（白名單 + 禁內部位址）
│   ├── processor.py        # 資料清洗（自動拔 secret）
│   ├── planner.py          # 任務規劃拆解（JSON）
│   ├── coder.py            # 程式碼生成（sandbox workspace）
│   ├── verifier.py         # 驗證執行（指令白名單）
│   ├── memory.py           # 記憶/狀態（gitignore 目錄）
│   └── notifier.py         # Telegram 通知（env token）
├── workflows/
│   ├── main_pipeline.py    # 主控調度（資料鏈接 + 平行 + 產物存檔）
│   └── tasks/              # 子任務包裝
└── scripts/                # setup / run / smoke / health / protect
```

## 安全規則（本專案紅線）
1. **零 hardcode**：金鑰/token/密碼一律 `os.getenv()`；預設只允許 `localhost` / 佔位符。
2. **零真實位址**：所有 code/JSON/shell 不允許出現真實 IP；掃描器會檢查 `205.*` 等樣式。
3. **redact 強制**：日誌與產物自動遮罩 `sk-` / `ghp_` / `alv2_` / bot token 樣式。
4. **沙箱輸出**：coder 只寫入 `workflows/state/workspace`；verifier 只跑白名單指令。
5. **gitignore 屏蔽**：`.env`、`*.pem`、`keys/`、`workflows/data|state/`、`logs/`。

## 快速開始
```bash
bash scripts/setup.sh          # venv + .env + 語法檢查
bash scripts/smoke_test.sh     # mock 驗證整條管線（不需金鑰）
bash scripts/run_pipeline.sh --pipeline default --query "你的任務"   # 真實執行（需 .env 金鑰）
bash scripts/healthcheck.sh    # 健康檢查
```

## 管線（default）
`research → scrape → process → plan → code → verify → notify`，每個 stage 輸出自動鏈接到下一 stage 輸入（`stage_id.key` 引用語法），支援 `parallel` 平行階段。

## 環境變數
見 `.env.example`（LITELLM_MASTER_KEY / LITELLM_BASE_URL / TELEGRAM_BOT_TOKEN / SEARCH_API_URL …）。
