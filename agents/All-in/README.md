# 🏢 All-in — AI Software Company 一鍵部署包（2026.08.16 Final + 4 點強化）

CEO（人類）→ Hermes（長駐 AI Manager）→ Agent Fleet → Verification → Memory → CEO。

> ⚠️ **誠實狀態聲明**：本包由 DSH Agent 於 `greencloud-ai` 主機以「檔案寫入」方式生成。
> 本 session 的工具集**只有檔案讀寫，沒有 shell**，因此 `systemctl restart`、`curl` 驗證、
> `tar` 打包、`git clone`、`git push` 都已寫成可一鍵執行的腳本，但**尚未執行**。
> 本包不偽造任何 commit hash 或服務狀態（遵守專案 P0：❌ 未驗證就宣稱完成）。

## 目錄結構
```
All-in/
├── README.md / .env.example / .gitignore / docker-compose.yml / requirements.txt
├── core/            sesm_engine.py, orchestrator.py, agent_registry.json, security/
├── skills/          9 個 SKILL.md（engineering-memory, define-to-ship, plan-once-verify-always,
│                    agent-skills, ecc, vps-bridge, apollo-memory, sesm-engine, harness-evolution）
├── config/          conduit_lody_setup.md, openwebui_hermes_setup.md, mcp_servers.json
├── frontend/        all-in-dashboard/（index.html + dashboard.js）, agent-monitor/（index.html + monitor.js）
├── deploy/          install.sh, verify.sh, push.sh, fix/01~03（4 大修復的可執行腳本）
└── logs/            deploy_log.txt, migration.md（由 fix/02 生成）
```

## Runbook（在 VPS 上以 xiaye 身分執行）
```bash
cd ~/All-in
cp .env.example .env && nano .env          # 1. 填真實 Key（.env 已被 .gitignore 排除，絕不入庫）
bash deploy/install.sh                     # 2. 安裝 skills + SESM + docker 基礎服務
bash deploy/fix/01-fix-hermes-binding.sh   # 3. 修復1：8642 對 Tailscale 可達（備份→sed→重啟→驗證→nginx 備案）
bash deploy/fix/02-migrate-large-files.sh  # 4. 修復2：大檔打包 + 臨時 HTTP 下載 + 寫 logs/migration.md
bash deploy/fix/03-install-harness-evolution.sh # 5. 修復3：clone SWE-agent / mini-swe-agent 進 harness-evolution
bash deploy/verify.sh                      # 6. 全服務健康驗證（只回報事實）
bash deploy/push.sh "feat: All-in 完整部署包 + 4 點強化"  # 7. 去敏掃描後推送（絕不 --force）
```
修復 4（面板接真實數據）已直接寫在 `frontend/all-in-dashboard/dashboard.js`
與 `~/Ai-agent-skill/frontend/collaboration-monitor/monitor.js`。

## 相較原稿的安全強化（務必閱讀）
1. **SESM meta-prompt 已移除 meta-token／越獄指令**。自我突變被鎖進 `ALLOWED_STATES` 白名單，
   `TEST_STAGE`/`VERIFY_STAGE` 驗證閘不可被演化移除，`metrics.trials < 20` 的自評分數不得升版
   ——這才是 StateM「鐵軌鎖定」精神的真正實作，而不是靠繞過模型安全機制。
2. **未收錄**「寄生式瀏覽器算力／偽裝層」程式碼：在訪客不知情下使用其 CPU/GPU 屬於
   未經授權的資源取用。若要做分散式算力，請改用「明示同意」的志願運算（頁面清楚聲明並提供退出）。
3. `deploy/push.sh` **不使用 `--force`**（遵守本專案 P0 規則）；推送前先跑 gitleaks
   （沒有則用 `core/security/key_manager.py` 陽春掃描），一偵測到密鑰立即中止。
4. 全包**零硬編碼憑證**；docker-compose 一律 `${VAR}` 引用 .env。
5. 8642 綁 `0.0.0.0` 務必搭配 `core/security/firewall_rules.md` 的 ufw 規則（僅放行 tailscale0）。
6. 面板跨網域呼叫 Hermes/Qdrant 需開 CORS；`dashboard.js` 內建離線降級，端點不存在時顯示 unknown，不假造數據。

## 各崗位 Top 5 工作流套件（skill 推薦，可選裝）
| 崗位 | 推薦 Top 5 |
|---|---|
| Hermes（經理） | apollo-memory, vps-bridge, opencode-bridge, grill-me, handoff |
| OpenHands（深度工程） | browser 工具, docker 沙箱, define-to-ship, ecc, engineering-memory |
| OpenCode（日常編碼） | obra-superpowers, firecrawl, understand-anything, composio, skill-optimizer |
| Kilo Code（架構/偵錯） | plan-once-verify-always, grill-me, engineering-memory, ecc, sesm-engine |
| mini-SWE / SWE-agent（修 Issue） | harness-evolution, ecc, engineering-memory, define-to-ship, vps-bridge |

## 服務端口約定
8642 Hermes ／ 6333 Qdrant ／ 3000 Open WebUI ／ 8000 Mem0 ／ 18000 OpenHands ／
8743 OpenCode ／ 4000 LiteLLM ／ 11434 Ollama（僅本機）／ 5678 n8n
