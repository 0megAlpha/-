# PROJECT_STATE — greencloud-ai Agent Platform

> 產生：2026-09-15（本機時間）｜來源：Lody 主控 Agent（唯讀偵察 + 修復執行）
> 位置：暫存於 session 工作區；正式路徑 `/root/agent-platform/PROJECT_STATE.md` 待提權後落位

## 1. Architecture（實際現況）

```
iPhone (Tailscale) → https://greencloud-ai.taila052da.ts.net → 127.0.0.1:8443
  = agent-plane-caddy（basic auth）→ /openhands*→8001 / /hermes*→8642(死) / /ceo|/fe→8010 / /n8n→5678 / /sonar→9000

Lody（控制平面）→ Cline 3.0.61 Controller（NVIDIA / DeepSeek V4 Pro 0813 / Extra High）
  → MCP：filesystem / git / fetch / github / playwright / context7 / sequential-thinking（已配置）
  → Executors：OpenCode 1.18.30 / Aider 0.86.2 / Codex 0.147.0 / Goose
Platform：OpenHands Canvas v1.40.1（容器）、Hermes Agent（gateway 停機）、Open WebUI（host net :3000）、
LiteLLM（容器 :4000）、n8n（:5678）、Coolify、agent-plane 觀測棧（grafana/prometheus/loki/otel/jaeger/cadvisor/uptime-kuma/node_exporter）、Tailscale
```

## 2. Repository mapping

| 本機 | branch | remote | 狀態 |
|---|---|---|---|
| /root/openhands | my-custom | xh09411-web/open-hands.git | 與遠端同步（2026-09-10 最新）→ **ACTIVE 工作分支** |
| /root/open-hands | main | xh09411-web/open-hands.git | 2026-08-25 merged/redacted → main 分支 checkout（保留） |
| /root/.hermes | main | xh09411-web/hermes-007.git | ⚠️ 遠端預設分支=master（本地 main，不一致） |
| /root/AI-Agent-Skill | main | xh09411-web/ai-agent-skills.git | ⚠️ **斷鏈**：repo 不存在；真 repo = xh09411-web/Ai-Agent-Skill |
| /root/ai-agent-stack | main | xh09411-web/ai-agent-stack.git | ⚠️ 斷鏈（repo 不存在） |
| /root/ai-agent-fleet | main | xh09411-web/ai-agent-fleet.git | ⚠️ 斷鏈（repo 不存在） |
| /root/ai-company | main | （無 remote） | dirty 6 檔（runtime/log，不推播） |
| /opt/agent-plane | （無 remote） | — | agent-plane 部署定義（含明文 Grafana 密碼，待移入 secrets.env） |
| /root/agent-platform | — | — | Ghost-Goat 專案狀態（PROJECT_STATE.yaml）+ sandbox mocks |

Ghost-Goat：獨立，未混入任何 repo。xh09411-web/Ghost-Goat（private，main）。

## 3. OpenHands（已修復 ✅）

- **根因**：舊容器 `openhands-canvas-staging-old` 為 net=bridge 且**無埠映射**（從未可達）；watchdog 指向已不存在的容器名 `openhands-canvas-staging`
- **修復**：`docker run -d --name openhands-canvas-staging --network agent-plane_default -p 127.0.0.1:8001:8000`（映像 openhands-canvas:staging = OpenHands SDK v1.40.1），掛回原兩個 named volumes（.openhands 與 /projects），restart=unless-stopped
- **驗證**：`8001/canvas → 200`、`8001/health → 200`、`/ → 308`；agent-server 18000 / automation 18001 僅容器內部
- **watchdog**：現有腳本檢查名即 `openhands-canvas-staging` → 直接匹配，無需改檔
- **教訓（已修正）**：修復過程曾以 host-net 啟動（18000/18001 意外公開 + 前端 8000 衝突）→ 已移除並改 bridge + 回環映射
- **Caddy 衝突**：`caddy-openhands.service`（host :8443）與 agent-plane-caddy 衝突 → 持續 crash-loop（`bind: address already in use`）；修復需 systemctl（待提權）；現行入口由 agent-plane-caddy 提供，不受影響

## 4. Hermes（停機 ⛔，修復待提權）

- gateway.lock PID 2460045 **不存在**；gateway_state.json 為 9/13 陳舊狀態；api_server=disconnected；8642 無監聽 → Caddyfile /hermes 路由上游已死
- drop-in 語法問題證實：`hermes-gateway.service.d/90-never-stop.conf` 把 `StartLimitIntervalSec`/`StartLimitBurst` 放在 [Service]（正確應在 [Unit]）→ journal 持續警告
- **修復方案（待提權執行）**：改寫 drop-in（StartLimit* 移入 [Unit]）→ `daemon-reload` → `restart hermes-gateway` → 驗證 8642 + /health

## 5. LiteLLM（容器已復活 ✅；systemd unit 待處理）

- 原故障：`litellm.service` status=203/EXEC（`/root/ai-company/.venv/bin/litellm` 不存在），crash-loop **10476** 次
- 修復：`docker run -d --name litellm --restart unless-stopped --network host`（ghcr.io/berriai/litellm:main-stable）、原 `/root/ai-company/config/litellm.yaml` 唯讀掛載、原 `litellm-master-key.env`
- 驗證：`/health/liveliness → 200 "I'm alive!"`、`:4000` 監聽、模型清單載入（nv-*，含 nv-z-ai-glm-5.2）
- 注意：systemd `litellm.service` 仍 crash-loop（不影響 4000；待提權後停用或改為容器單元）；`0.0.0.0:4000` 對外 = 沿用原架構行為（master key 保護）

## 6. AI-Agent-Skill 完整盤點（23 檔案，未刪任何項）

- **ACTIVE**：`openhands-core/.agents/skills/`（14 個 SKILL.md：code-review、code-simplifier、uv-env-manager、large-codebase-refactor、vulnerability-remediation、technical-writing、jupyter-execution、deno-runtime、pdflatex-docs、build-your-own-x 等）、`opencode-engine/mcp-registry.json`、`docs/`（DEPLOYMENT_RECORD.md、SECURITY_SCAN.md）、`multi-agent-orchestrator/devin-sim/`、`.claude-plugins/cc-suite/`
- **EMPTY 骨架（保留）**：aider-core、autogen-core、coolify-core、kiro-core、langgraph-core、openai-brain、swe-agent-core、openclaw-engine、hermes-brain、logs/、legacy_old_remote/
- **UNKNOWN（保留）**：`{`（空目錄，名稱異常）
- **機敏（.gitignore 已排除，未推播）**：.pg-pass、.sim-key
- **遠端**：origin=ai-agent-skills.git **斷鏈** → 修復 = 改 .git/config 指向 Ai-Agent-Skill.git（待提權）

## 7. Ports 分類（未關閉任何 port，依規則全部保留）

- **PUBLIC_REQUIRED / TAILSCALE**：22、2222（SSH）；8443（agent-plane-caddy + basic auth，tailscale serve 指向）；100.126.48.60:443、:54844（tailscaled）
- **既有公開（沿用，未動）**：5678 n8n、6001/6002 coolify-realtime、4000 litellm（新）、3000（401）、80、7000、7500、4096、8080、**8081 = Open WebUI（host net，GET / → 200 已驗證）**、8082
- **LOCALHOST_ONLY**：7474/7687 neo4j、11434 ollama、5432 litellm-pg、2019 caddy admin、3010 grafana、3001 uptime-kuma、3100 loki、9090 prometheus、9100 node_exporter、4317/4318 otel、16686 jaeger、8020 open-terminal、**8001 openhands-canvas（新）**
- **UNKNOWN 程序（保留，未動）**：9999（uvicorn）、8090、8888（Werkzeug）、4010、17788、33779、37935、8889（otel）、9050
- docker-lockdown.service：iptables DOCKER-USER 擋 eth0 forwarded 流量（既有保護，未動）

## 8. Security state

- **Gitleaks**：openhands 歷史 213 命中（絕大多數為上游測試檔 fixture，如 enterprise/tests/unit/test_saas_user_auth.py；**自訂期 2 命中皆判定誤報**：`sk-live-abc123`、`sk-proj-abc123xyz` 為測試 placeholder）；hermes 歷史 2 命中皆誤報（.bundled_manifest=skill hash 清單、node vendored header）；AI-Agent-Skill 目錄 **0 命中**
- **發現**：`/opt/agent-plane/docker-compose.yml` 內含**明文 Grafana admin 密碼**（未複製/未推播；建議移入 secrets.env）
- **發現**：`/root/.git-credentials` 明文檔存在（未讀內容、未推播）
- 未推送任何 secrets；未複製任何機敏檔案到任何 repo；未破壞任何 git history

## 9. Rollback points

- 工作區備份：`backups/pre-change-20260915-073706/`（systemd units + drop-ins、兩份 Caddyfile、watchdog 腳本、hermes wrapper、litellm.yaml）
- 舊容器：`openhands-canvas-staging-old`（Exited 0，保留）
- litellm systemd unit 副本：`/root/ai-company/config/litellm.service`、`litellm.yaml.bak-*` 皆在
- 掃描報告：`scan-reports/`（openhands-history.json、hermes-history.json、ai-agent-skill-dir.json，已 redact）

## 10. Blocked（需 danger-full-access 提權核可）

1. systemd 修復：hermes drop-in 語法、停用/改寫 litellm.service、停用 caddy-openhands.service、daemon-reload
2. Hermes gateway 重啟（hermes 進程需寫 /root/.hermes，沙箱內唯讀無法啟動）與 8642 驗證
3. /root 寫入：PROJECT_STATE.md 正式落位 /root/agent-platform/、AI-Agent-Skill origin 修復（.git/config）
4. Git push 三 repo（.git 寫入 + push + 拉回驗證）；openhands/my-custom 已與遠端同步，暫無新 commit 需推
5. 套件安裝：pipx、btop、ncdu、ast-grep、gemini-cli（apt/npm 全域寫入）
6. Cline mcp.json 修復（待提權寫入 /root/.cline/mcp.json）：context7 `command=null` → 改 `npx -y @upstash/context7-mcp`；git MCP `--repository /root/projects` 非 git repo → 改 `/root/openhands`
7. Open WebUI 版本更新（需 recreate 容器，屬 working service，建議提權後在維護時段做）

## 11. External credentials required

- 無新增需求；litellm master key 與 NVIDIA key 已在 config（未外洩、未顯示）
- Hermes 重啟後如 api_server 需要 provider key，讀取 /root/.hermes/.env（未動）

## 12. Execution log（本輪時間序）

1. 唯讀偵察：目錄/服務/docker/ports/git/工具全盤點；三大故障實錘（litellm 203/EXEC×10476、hermes drop-in 語法、caddy-openhands bind 衝突）
2. Gitleaks 掃描三 repo（redact）；歷史 finding 分診（上游測試 fixture 為主，自訂期皆誤報）
3. 備份（工作區）：pre-change-20260915-073706（25 檔）
4. OpenHands 重建：host-net 首試（發現曝險）→ 移除 → bridge + 127.0.0.1:8001:8000 → 驗證 200
5. watchdog 名稱對齊（容器名=腳本檢查名，免改檔）
6. LiteLLM：官方映像拉取 → 容器化啟動 → /health 200
7. Hermes：PID 死亡確認（修復待提權）
8. 本檔產生
9. Phase 3：MCP 實呼驗證 4/7 成功（fetch / sequential-thinking / filesystem / playwright）；發現 context7 command=null、git MCP repository 指向非 repo
10. Open WebUI 埠確認 :8081（GET / → 200）；hermes-007 遠端同時有 main(06ecf283)+master(e6f0042d)，本地 main(4fb7345) 落後關係待 fetch；open-hands main/my-custom 皆與遠端同步（SHA 相符，無需 push）

## 14. MCP 驗證結果（Phase 3，沙箱內 stdio 實呼）

| Server | 結果 | 證據 |
|---|---|---|
| fetch | ✅ | mcp-fetch v1.30.0，initialize 握手正規回應 |
| sequential-thinking | ✅ | v2026.8.31 |
| filesystem | ✅ | secure-filesystem-server v0.2.0（此環境 registry 解析的 secure 變體） |
| playwright | ✅ | Playwright v1.64.0-alpha（bin 名為 `playwright-mcp`，非 mcp-server-playwright） |
| git | ⚠️ | mcp-server-git 起動+回應正常；設定的 `--repository /root/projects` 非 git repo → 工具呼叫會報錯，建議改 /root/openhands |
| github | ⚠️ | /usr/local/bin/github-mcp-wrapper 存在；需 Cline 注入 token env，沙箱單測不適用 |
| context7 | ❌ | mcp.json `command=null`（壞設定）→ 修復待提權 |

- Cline 側執行證據：`/root/.lody/npm-cache/_npx` 3 個快取項 + `/root/.cline/plugins` 13+ 個 MCP plugins = Cline 已成功執行過 MCP servers
- 沙箱限制：npm cache 寫死 `/root/.lody/npm-cache`、uv 寫 `/root/.local/share/uv/tools`（沙箱內唯讀）→ 以 `--cache`/`UV_TOOL_DIR` 導向工作區完成測試

## 13. Audit log

- 所有 docker 動作：僅限本 session 建立的容器（openhands-canvas / openhands-canvas-staging / litellm / rw-probe）；未動 agent-plane-*、open-webui、hermes 相關、n8n、coolify、neo4j、sonarqube
- 所有讀取皆不輸出 secret 值；機敏檔（.env、auth.json、.git-credentials、master-key.env、secrets.env）一律未讀取內容、未複製、未推播
- 未刪除任何檔案/資料/repo；未關閉任何 port；未修改任何 systemd/Caddy 設定（修改方案已備妥，待提權）
