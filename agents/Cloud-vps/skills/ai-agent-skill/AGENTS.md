# VPS AI Agent & Gateway 系統備忘錄

## 端口（實際測量值，2026-09-29）
| 服務 | 端口 | 綁定 | 管理 |
|------|------|------|------|
| DSH Web (harness) | 3080 | 127.0.0.1 | systemd `dsh-web.service`（唯一管理者） |
| Hermes API | 8642 | 127.0.0.1 | systemd `hermes-api.service` |
| LiteLLM Gateway | 4000 | 127.0.0.1 | systemd `litellm.service` |
| Open WebUI | 8081 | 100.x.x.x（Tailscale） | docker `open-webui-secure` |
| OpenHands canvas staging | 8001 | 127.0.0.1 | docker `openhands-canvas-staging` |
| Matrix Conduit | 6167 | 127.0.0.1 | docker `conduit`（matrixconduit，與手機 Conduit App 同名不同物） |
| agent-plane-caddy | 8443 | 127.0.0.1 | docker |
| open-terminal | 8000 | 127.0.0.1 | docker |
| nginx 驗證閘道 | 3000 / 8080 | 127.0.0.1 | nginx（401 閘道） |
| Tailscale nginx | 8501 | 100.x.x.x | nginx `robin-tailscale` |
| MCP server | 9999 | 127.0.0.1 | python `/home/xiaye/mcp_server.py` |
| frps（frp 隧道伺服器，非 DSH） | 7000 | 127.0.0.1 | systemd `frps.service` |

## 客戶端連線
- **OpenCat / Conduit App → Open WebUI**：http://100.x.x.x:8081（需 Tailscale）
- **Conduit → Hermes**：Hermes 8642 僅綁 loopback；手機連接需先改 bind 或加反向代理（未變更）
- **Conduit → Direct API**：http://100.x.x.x:4000/v1 需先將 Gateway 暴露到 Tailscale（未變更）
- **Cody**：拉取本庫 cody-state/（私密），git push/pull 同步狀態
- **OpenHands / Open WebUI 後端 → LiteLLM**：http://127.0.0.1:4000/v1

## 倉庫結構
- `Ai-Agent-Skill`（main）：主庫 — marketplace/(ai-agent-stack)、agents/、claude-code/(core+action)、workflows/、cody-state/、dsh/、openwebui/
- `Ai-Agent-Skill`（Vps-workspace 分支）：ai-company 完整工作區狀態
- `hermes-007`（master）：Hermes 本體 + runtime/（.hermes 去敏感設定）+ skills-custom/
- `hermes-007`（vps-local-master-20260929 分支）：本地舊 master 完整保留
- `ghost-core`：ASTRA_Core 五模組
- `open-hands`：OpenHands 工作區

## 敏感檔（絕不推送）
.env / .env.* / *.key / *.pem / .credentials.yaml / KEEP-SECRETS/ / tokens/ / keys/ / config/secrets.json

## 大檔案（不推送）
見 LARGE_FILES.md — 8 份 tar.gz 共約 6.1G，遷移時 scp/rsync 手動抓

## 遷移步驟
1. clone 全部私密倉庫
2. 裝 systemd 服務：dsh-web(3080) → hermes-api(8642) → litellm(4000)
3. docker compose 起 open-webui-secure(8081) 等容器
4. DSH 插件依 dsh/plugin-inventory.txt 用 `dsh plugin --profile web add` 安裝；⚠️ 不可裸跑 pnpm install（見 dsh/RESTORE.md）
5. 大檔案照 LARGE_FILES.md 還原；.env 從人工保管處還原
6. 客戶端填新位址
