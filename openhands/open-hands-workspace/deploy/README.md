# open-hands — 私人部署版（PRIVATE）

本 repo 基底為 OpenHands 官方最新 main（上游），加上本機自訂部署層。
**所有自訂/部署/綁定內容一律不得公開**，此 repo 必須保持 private。

## 結構
```
├── deploy/                      ← 自訂部署層（本 repo 的私有部分）
│   ├── docker-compose.override.yml.template   ← LiteLLM 綁定範本
│   ├── update-from-upstream.sh  ← 更新上游腳本
│   ├── settings.json.example    ← 設定範本（含 marketplace 註冊）
│   └── extensions/EXTENSIONS.md ← 熱門擴充套件清單
└── (OpenHands 官方原始碼)
```

## 綁定總覽（本機 VPS）
| 項目 | 綁定 |
|---|---|
| LLM | openhands → **LiteLLM** `http://localhost:4000/v1`（模型 `openai/glm-5.2`） |
| 瀏覽器 | OpenWebUI :8080 → litellm :4000 + ollama :11434 |
| openhands UI | :3000（docker openhands:latest，network_mode=host） |
| opencode | :4096（Basic Auth 保護） |
| AI Node | :8888（127.0.0.1，token 保護） |
| Telegram Bot | @Openpisces777Bot（白名單雙 ID） |

## 隱私規則（紅線）
- `docker-compose.override.yml`（含 master key）→ **已 gitignore，永不 push**
- `*.env`、`*.key`、`settings.json`、`config/bot.env`、`credentials.json` → gitignore
- 推送前一律跑 `scripts/scan-secrets.sh`（全境掃描）
- 任何新 secret 檔先加進 `.gitignore` 再談 commit

## 更新上游（保留官方更新通道）
```bash
bash deploy/update-from-upstream.sh
```
自動: fetch upstream main → merge → docker compose build/up → 重新掃描 secret。

## 部署（本機）
```bash
cp deploy/docker-compose.override.yml.template docker-compose.override.yml
# 編輯填入真實 LLM_API_KEY
docker compose up -d --build
```
