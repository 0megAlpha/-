# 📋 FINAL_ENTRY — 最終填入清單（Ai-agent-skill / All-in）

> 產生時間：2026-08-16
> 密鑰**一律不在本文件**。本文件只寫「欄位 → 變數名 → 從哪讀」。

---

## 0. 三個檔案的分工（先搞清楚再填）

| 檔案 | 內容 | 權限 | 是否入 git |
|---|---|---|---|
| `~/.ai-company/.env` | 系統層：服務 URL、Tailscale IP、面板設定 | 600 | ❌ 永不 |
| `~/All-in/.env` | 引擎層：模型 API Key、Qdrant、OpenRouter… | 600 | ❌ 永不 |
| `~/.hermes/.env` | Hermes 層：`API_SERVER_*`、密鑰 | 600 | ❌ 永不 |

產生範本（不填真值也能建檔）：

```bash
mkdir -p ~/.ai-company && chmod 700 ~/.ai-company
cat > ~/.ai-company/.env <<'EOF'
TAILSCALE_IP=100.126.48.60
WEB_PORT=8080
API_PORT=8765
HERMES_API_URL=http://100.126.48.60:8642
ORCH_API_URL=http://100.126.48.60:8765
QDRANT_URL=http://100.126.48.60:6333
OPENWEBUI_URL=http://100.126.48.60:3000
HERMES_API_KEY=<在這裡貼上，之後 chmod 600>
EOF
chmod 600 ~/.ai-company/.env
```

---

## 1. Conduit（Lody）填入

| 欄位 | 值 |
|---|---|
| Provider type | `OpenAI-compatible` |
| Base URL | `http://100.126.48.60:8642/v1`（Hermes 不在線時改用 `http://100.126.48.60:8765`） |
| API Key | `~/.ai-company/.env` → `HERMES_API_KEY` |
| Model | 依 Hermes 實際掛載的模型；先用 `/v1/models` 查 |
| MCP Server URL | `http://100.126.48.60:8642/mcp` |

連線前先驗證（回應 200 才算通）：

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://100.126.48.60:8642/health
curl -s http://100.126.48.60:8642/v1/models | head -c 400
```

### 關於 MCP 自動掛載

我**沒有**替你自動掛 MCP server 到 Lody workspace —— 那會改動你所有 session 共用的 catalog，
必須由你在 Lody 的 UI 裡親自確認。要掛的話：

1. 先啟動 Orchestrator：`python3 ~/All-in/core/orchestrator.py --serve`
2. 在 Lody UI 新增 stdio 或 HTTP MCP server，command 用上面那支 python
3. 在 trusted UI 裡**親自選取**它（agent 建立的項目預設不會自動生效）

---

## 2. Open WebUI 填入

| 欄位 | 值 |
|---|---|
| API URL | `http://host.docker.internal:8642/v1`（Docker 內）<br>`http://100.126.48.60:8642/v1`（瀏覽器直接填） |
| API Key | `~/.ai-company/.env` → `HERMES_API_KEY` |
| Model | `/v1/models` 查到的第一個 |

容器內連宿主機的兩種做法（二選一）：

```yaml
# docker-compose.yml
services:
  open-webui:
    extra_hosts:
      - "host.docker.internal:host-gateway"   # Linux 需要這行
```

驗證容器看得到宿主機：

```bash
docker exec -it open-webui sh -c 'curl -s -o /dev/null -w "%{http_code}\n" http://host.docker.internal:8642/health'
```

---

## 3. 密鑰來源對照

| 變數 | 放在哪 | 誰在讀 |
|---|---|---|
| `HERMES_API_KEY` | `~/.ai-company/.env` | Conduit / Open WebUI / 面板 |
| `OPENROUTER_API_KEY` | `~/All-in/.env` | `core/sesm_engine.py` |
| `DEEPSEEK_API_KEY` | `~/All-in/.env` | `core/sesm_engine.py`（故障轉移備援） |
| `MOONSHOT_API_KEY` | `~/All-in/.env` | `core/sesm_engine.py`（故障轉移備援） |
| `QDRANT_API_KEY` | `~/All-in/.env` | Qdrant + 記憶面板 |
| `API_SERVER_KEY` | `~/.hermes/.env` | Hermes gateway |
| `TAILSCALE_IP` | `~/.ai-company/.env` | 全部前端腳本 |

---

## 4. 安全鐵律（每次提交前複誦一次）

1. `git ls-files | grep -E '\.env$|\.pem$|\.key$'` **必須是空的**
2. 推送一律走 `~/All-in/deploy/push.sh`（內含 gitleaks → semgrep → trivy 三道閘）
3. **絕不 `git push --force`**；被拒就 `git pull --rebase`
4. 8080 / 8642 / 8765 **只綁 Tailscale**，不對公網開放
5. API Key 不要貼進任何截圖、對話、issue
6. 服務沒驗證過就說「沒驗證過」——不要寫「已完成」

---

## 5. 驗收清單（逐項打勾）

- [ ] `curl http://100.126.48.60:8765/health` → `{"status":"ok"}`
- [ ] `python3 ~/All-in/core/orchestrator.py --agents` → 列出 12 崗位的真實探測結果
- [ ] `bash ~/All-in/deploy/scan.sh` → 產生 `logs/full_scan_report.md`
- [ ] 面板四個網址都能開，且顯示的是真實資料或誠實的 offline
- [ ] `crontab -l | grep harness-evolution` → 有 03:00 那條
- [ ] `git -C ~/All-in log -1 --oneline` → 有真實 commit hash
- [ ] `git -C ~/Ai-agent-skill log -1 --oneline` → 有真實 commit hash