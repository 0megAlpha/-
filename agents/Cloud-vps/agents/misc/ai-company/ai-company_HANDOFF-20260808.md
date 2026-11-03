# AI Company Handoff — 2026-08-08

## 1. Full Integration 失敗步驟已銷帳 ✅
- 失敗步驟：`CHECK HERMES CLI`（安裝程式在互動式提示卡住被判 FAIL）
- 現況：`hermes --version` → **Hermes Agent v0.20.0 (2026.8.3)**，已安裝於 `/usr/local/bin/hermes`
- 結論：該步驟已完成，無需重跑

## 2. OpenCode Web（port 4096）✅ 可正常運作
- 根因：opencode server 開啟 **Basic Auth**（無帳密回 HTTP 401）
- 驗證：以正確帳密連 `http://127.0.0.1:4096/` → HTTP 200，正常輸出 OpenCode Web UI
- 帳密存放：`/root/.config/opencode/server.env`（包含帳號與密碼兩個欄位）
- systemd：`opencode-server.service` active，firewall 4096/tcp 已放行
- 使用者從瀏覽器開啟 `http://<IP>:4096` 時，需輸入上述帳密（值在本機檔案中，未寫入此文件）

## 3. GitHub 權限調查 ⚠️（需要升級 token 才能完成）
| Repo | 可見性 | 說明 |
|---|---|---|
| xh09411-web/openhands | **PUBLIC** | 使用者要求改 private，但 API PATCH 回 403 |
| xh09411-web/hermes-007 | private | — |
| xh09411-web/Ai-Agent-Skill | private | — |

- 現有 token（git 憑證檔內）：fine-grained PAT，**可讀但無 Administration 權限**
  - 修改 openhands 可見性為 private → **403** "Resource not accessible by personal access token"
  - 建立 ai-company 新 repo → **403** 相同錯誤
- 結論：這正是「權限不夠」的具體證明。需要：
  - fine-grained token 加上 **Administration: Read and write**，或
  - classic token 含 `repo` scope
- 未完成項目：openhands 改 private、ai-company 建立 repo + push

## 4. Pre-push Sanitize Audit
- 結果：ATTENTION（7 個警示），但逐項審查後全部為**誤報**：
  - `$GITHUB_TOKEN` 環境變數範本（文件/skill 內容）
  - `secrets_router.py`、`api_keys.py` 等「功能檔名」（非真密鑰）
- 先前 secret audit（11:19）亦確認無真實 secret 洩漏

## 5. OpenWebUI
- **尚未安裝**（無 pip 套件、無 docker container、無 port）
- 需另行安裝（pip 或 Docker）

## 6. 附註
- `/root/ai-company` 已是 git repo，狀態 clean，尚未設定 remote
- OpenCode 模型供應商：僅 NVIDIA NIM（auth.json），NVIDIA 免費額度為每日重置

---

## 7. 更新（16:30）— opencode web 已驗證可用 ✅
- 登入帳密：`/root/.config/opencode/server.env`（HTTP Basic Auth）
- 新增工作區方法：Add project → 在 Search folders 輸入完整路徑（如 `/root/ai-agent-workflows`）→ Enter → 側邊欄出現專案 → New session
- 已知怪癖：`/find/file?dirs=true&directory=/root`（home 目錄）回傳空 → picker 初始顯示 "No folders found"，這是誤導；用路徑輸入即可繞過
- E2E 實測：新增專案 → New session（預設模型 GLM-5.2）→ 送訊息 → 正常串流回覆，無 401/403
- NVIDIA key 當下驗證：/v1/models 與 chat completion 皆 200 正常

## 8. OpenWebUI ✅ 已安裝
- http://205.189.160.125:8080 （首次造訪請註冊管理員帳號）
- 串接：NVIDIA NIM（OpenAI 相容）+ Ollama（localhost:11434，目前 0 模型）
- 容器：open-webui（restart=unless-stopped），資料於 /root/ai-company/open-webui
- 防火牆：8080/tcp 已放行

## 9. openhands 瀏覽器模式 ⏳ 建置中
- docker-compose.yml：本機建置 openhands:latest（containers/app/Dockerfile），port 3000
- 背景 tmux `ohbuild` 執行 `docker compose build openhands`
- 完成後：`cd /root/openhands && docker compose up -d` → http://205.189.160.125:3000
- 注意：runtime sandbox 需掛載 /var/run/docker.sock（compose 已設定）

## 10. 端口審計 + 清理 ✅
- frps（:7000, dashboard :7500）：FRP 內網穿透基礎設施，保留（ufw 未對外開放 7000/7500）
- 允許對外：22, 80, 443, 4096, 8080
- 清理：pip/uv/electron/node-gyp 快取 + /tmp 暫存（約 2.3GB）
- 保留：ms-playwright（測試用）、.venv、backups、git repos

---

## 11. 更新（17:00）— LiteLLM 閘道 + 三 UI 全上線

### LiteLLM API 閘道 ✅（核心架構）
- 位置：systemd `litellm.service`（開機自啟、當機重啟），port **4000**
- 設定：`/root/ai-company/config/litellm.yaml`
- master key：`/root/ai-company/config/litellm-master-key.env`（勿外洩）
- 路由：`nvidia/*` 萬用（任何 NVIDIA 模型皆可用）+ glm-5.2 + llama-3.1-8b + deepseek-r1 + qwen3-32b
- 實測：/v1/models 與 chat（glm-5.2→NVIDIA）皆 200
- 注意：litellm 1.95 需 fastapi 0.127（metadata 寫 >=0.136 是 bug）；不支援 sqlite database_url
- 加 API key：在 litellm.yaml model_list 加一筆即可

### 三個 UI 全部上線 ✅
| UI | URL | 說明 |
|---|---|---|
| opencode | http://205.189.160.125:4096 | 已接 litellm（provider + auth key） |
| OpenWebUI | http://205.189.160.125:8080 | host network，首次註冊管理員；OpenAI 連線指向 litellm |
| openhands | http://205.189.160.125:3000 | 本機建置映像 + host network，restart=unless-stopped |

### 重要經驗：本 VPS docker port 發布與 ufw 衝突
- docker-proxy 有監聽但 docker0 轉發被封 → 對外連不上
- 解法：docker 服務一律用 **--network host**（或 compose override `network_mode: host`）
- `docker-compose.override.yml` 已建立於 /root/openhands

### 其他
- cc-switch 5.10.1（CLI）已裝於 /usr/local/bin/cc-switch（Claude Code/Codex/OpenCode provider 切換）
- 提示詞專案已拉取：/root/ai-company/projects/prompts/{awesome-chatgpt-prompts, awesome-chatgpt-prompts-zh}
- 待辦：openhands 首次啟動需在 UI 設定模型（LiteLLM: http://localhost:4000/v1）

---

## 12. 更新（17:20）— 多供應商整合 + openhands 接閘道 + 容量監控

### 供應商整合（litellm.yaml，gitignored）
| 供應商 | 狀態 | 說明 |
|---|---|---|
| NVIDIA ×2 key | ✅ | 負載平衡；萬用 nvidia/* 路由 |
| OpenRouter | ✅ | key 有效（部分模型有區域限制） |
| Groq | ⚠️ 403 | key 被拒，需用戶確認 |
| Moonshot | ⚠️ 401 | key 無效（.cn/.ai 都拒） |
| d_... / key_... 兩把 | ❓ | 無法辨識供應商，需要 base URL |
- 閘道共 566 個模型可選；加 key：`bash /root/ai-company/scripts/add-key.sh <provider> <key>`

### openhands ✅ 已接 LiteLLM
- docker-compose.override.yml：LLM_BASE_URL=http://localhost:4000/v1、LLM_API_KEY=master key、LLM_MODEL=openai/glm-5.2
- :3000 HTTP 200

### 容量監控 ✅
- /root/ai-company/scripts/maintenance-watch.sh + systemd timer（每天 08:00）
- 門檻：磁碟>80% / opencode db>200MB / webui db>500MB / logs>200MB → 寫入 reports/CAPACITY-REMINDER.txt
- 目前狀態：磁碟 14%，全部正常

---

## 13. 更新（18:10）— 身份切換 / 遷移 / 清理 / 常駐助手 / GitHub 現況

### 身份切換（Termius 適用）✅
- `switch`（顯示目前身份與用途說明）、root 紅 / xiaye 綠（一般）/ game 黃（測試）
- PS1 已改彩色身份標示（/etc/profile.d/ai-prompt.sh）；game 用戶已建立（uid 1002, sudo）

### 敏感資訊防護 ✅
- 全域 pre-push hook：/root/.git-hooks/pre-push（推送前掃描 key/token/私鑰，命中即擋下；強制例外 GIT_ALLOW_SECRETS=1）
- litellm.yaml + master-key 已 gitignored；所有 provider keys 已移除（留空，用 add-key.sh 自行加入）
- opencode auth.json 的 nvidia key 已移除；本機備份 auth.json.bak-*（600 權限，僅 root 可讀）

### 遷移 /root → /home/xiaye ✅（系統服務不受影響）
- 已移動：hermes-007、Claude-code、openhands-extensions、freebuff-project、ai-agent-fleet
- 保留：ai-company（全部服務）、openhands（docker compose）、ai-agent-workflows（opencode WorkingDirectory）
- ollama.service PATH 已更新指向 /home/xiaye/ai-agent-fleet/bin

### 清理 ✅
- 舊 tmux session 11 個已清除（剩 assistant）；記憶體 27Gi 可用
- git 歷史重寫：.git 671MB → 2.3MB（無 remote，安全）；秘密掃描通過；commit eb099dd

### 常駐 AI 助手（Termius 用）✅
- 指令：`ai` 或 `assistant`（attach）；離開：Ctrl+B 再按 D；`tmux ls` 查看
- systemd ai-assistant.service：監督者迴圈（session 掛了自動重建），開機自啟
- 內容：opencode TUI（已接 litellm 閘道）

### GitHub 現況 ⚠️（等你提供 Classic PAT）
- 目前 token 是 fine-grained 僅讀取 → 建 repo / 改私人 / 刪 repo 全部 403
- 待辦（拿到 Classic PAT repo scope 後）：①建私有 ai-company + push（本機 commit eb099dd 就緒）②openhands 改 private（目前 public）③刪除 -AI-AI--LLM
- 加 API key 用法：`bash /root/ai-company/scripts/add-key.sh <provider> <key>`（provider: nvidia/openrouter/groq/moonshot）
