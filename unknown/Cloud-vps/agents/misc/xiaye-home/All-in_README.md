# 🏢 All-in — AI Software Company 部署包

CEO（人）→ Hermes（AI Manager）→ Orchestrator → Agent Fleet → 驗證 → 記憶 → CEO

> ⚠️ **誠實狀態聲明**：本包由 DSH Agent 以「檔案寫入」方式產生。
> 產生者 session **沒有 shell**，所以 `systemctl`、`curl`、`git push` 都寫成可執行腳本，
> 但**尚未執行**。本包不偽造 commit hash、不假造服務狀態。
> 請依下方手冊執行後，以**實際輸出**為準。

---

## 1️⃣ 怎麼打開監控面板

先啟動（一次就夠，之後重開機再跑）：

```bash
bash ~/.ai-company/serve_frontends.sh --daemon
```

| 面板 | URL |
|---|---|
| 🏠 **All-in Dashboard**（總覽，推薦先看這個） | `http://100.126.48.60:8080/all-in-dashboard/` |
| 📊 **Agent Monitor** | `http://100.126.48.60:8080/agent-monitor/` |
| 🤝 **Collaboration Monitor** | `http://100.126.48.60:8080/collaboration-monitor/` |
| 🧠 **Memory Viewer** | `http://100.126.48.60:8080/memory-viewer/` |

面板右上角「⚙ 連線設定」填：

| 欄位 | 值 |
|---|---|
| Hermes / Orchestrator Base | `http://100.126.48.60:8765`（Hermes 在線則 `http://100.126.48.60:8642`） |
| Qdrant Base | `http://100.126.48.60:6333` |
| API Key | `~/.ai-company/.env` 的 `HERMES_API_KEY` |

> 面板顯示 `offline` / `unknown` 是**正常且誠實**的 —— 代表那個端點真的沒開。
> 本包沒有任何 `Math.random()` 假資料。

---

## 2️⃣ 怎麼填 Conduit / Open WebUI

### Conduit（Lody）

| 欄位 | 值 |
|---|---|
| Provider type | `OpenAI-compatible` |
| Base URL | `http://100.126.48.60:8642/v1` |
| API Key | `~/.ai-company/.env` → `HERMES_API_KEY` |
| MCP Server | `http://100.126.48.60:8642/mcp` |

### Open WebUI

| 欄位 | 值 |
|---|---|
| API URL（容器內） | `http://host.docker.internal:8642/v1` |
| API URL（瀏覽器） | `http://100.126.48.60:8642/v1` |
| API Key | 同上 `HERMES_API_KEY` |

Linux 容器要能連到宿主機，`docker-compose.yml` 需要：

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

完整填入清單見 `~/Ai-agent-skill/FINAL_ENTRY.md`。

---

## 3️⃣ 怎麼驗證服務活著

```bash
# A. 一次性總檢查
bash ~/All-in/deploy/verify.sh

# B. 服務狀態
systemctl --failed --no-pager        # systemd（應無 failed）
pm2 status                           # pm2（有裝的話）
ss -tlnp | grep -E '8080|8765|8642|6333|3000|8000|18000|8743'

# C. 逐一探活（000 = 不通）
for p in 8080 8765 8642 6333 3000 8000 18000 8743 4000 5678; do
  printf '%-6s %s\n' "$p" "$(curl -s -o /dev/null -m 3 -w '%{http_code}' http://127.0.0.1:$p/)"
done

# D. Agent 真相（哪個真的裝了、在線）
python3 ~/All-in/core/orchestrator.py --agents
```

**只要輸出是 200 / `"status":"ok"`，才算活著。** 其他一律當沒活。

---

## 4️⃣ 完整 Runbook（從零到上線）

```bash
cd ~/All-in
cp .env.example .env && nano .env                # 填 Key（.env 永不進 git）
bash deploy/install.sh                           # 安裝 skills + 引擎 + compose
bash deploy/fix/01-fix-hermes-binding.sh         # 修復 1：8642 綁定
bash deploy/fix/02-migrate-large-files.sh        # 修復 2：大檔打包（不刪原檔）
bash deploy/fix/03-install-harness-evolution.sh  # 修復 3：harness 源碼
bash deploy/scan.sh                              # 全境掃描 → logs/full_scan_report.md

python3 core/orchestrator.py --serve &           # 啟動狀態 API（面板資料來源）
bash ~/.ai-company/serve_frontends.sh --daemon    # 啟動面板
bash ~/.hermes/skills/harness-evolution/install_cron.sh  # 掛每日 03:00 巡檢

bash deploy/verify.sh                            # 驗證
bash deploy/push.sh "feat: All-in 最終強化與全境掃描"
```

---

## 5️⃣ 目錄

```
All-in/
├── core/
│   ├── orchestrator.py      動態選 Agent + 真實狀態 API（純 stdlib）
│   ├── sesm_engine.py       狀態機演化引擎（白名單 + 不可移除驗證閘）
│   ├── agent_registry.json  12 崗位註冊表（scan.sh 會回寫真實路徑）
│   ├── state/               執行期狀態（metrics / tasks / runbook / whitelist）
│   └── security/            key_manager + firewall_rules
├── skills/                  9 個 SKILL.md
├── config/                  conduit / openwebui / mcp_servers 設定指南
├── frontend/
│   ├── all-in-dashboard/    總覽面板（真實 fetch）
│   └── agent-monitor/       Agent 監控（真實 fetch）
├── deploy/
│   ├── install.sh  verify.sh  scan.sh
│   ├── push.sh              5 道安全閘：追蹤/gitleaks/semgrep/trivy/compose
│   └── fix/01~03            修復腳本
└── logs/                    deploy_log / migration / full_scan_report / security_report
```

---

## 6️⃣ 這套設計的三條底線

1. **真實數據優先**。探不到就是 `offline`/`unknown`；不生成假狀態、不填假記憶。
2. **安全閘不可繞過**。`push.sh` 任一閘門不通就中止；語意過關的 code review 才是有效的。
3. **狀態機可演化，但閘門不可被演化移除**。`TEST_STAGE`/`VERIFY_STAGE` 恆存；
   `trials < 20` 的自評數據不採信 —— 這是「協同進化」而非「自我欺騙」。

### 明確不做的事

- ❌ 不做未經同意的訪客算力利用（分散式運算必須明示同意 + 可退出）
- ❌ 不硬編碼任何憑證
- ❌ 不 `git push --force`
- ❌ 不刪除未確認的 repository 或服務
- ❌ 不在未驗證時宣稱完成

---

## 7️⃣ 服務端口

| 服務 | Port | 綁定 |
|---|---|---|
| 前端面板 | 8080 | Tailscale only |
| Orchestrator API | 8765 | Tailscale only |
| Hermes | 8642 | Tailscale only |
| Qdrant | 6333 | Tailscale only |
| Open WebUI | 3000 | Tailscale only |
| Mem0 | 8000 | Tailscale only |
| OpenHands | 18000 | Tailscale only |
| OpenCode | 8743 | Tailscale only |
| LiteLLM | 4000 | Tailscale only |
| Ollama | 11434 | **僅 127.0.0.1** |
| n8n | 5678 | Tailscale only |

ufw：`sudo ufw default deny incoming && sudo ufw allow 22/tcp && sudo ufw allow in on tailscale0`
