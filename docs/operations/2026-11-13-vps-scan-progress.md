# VPS 全境掃描進度 — 2026-11-13

狀態：部分盤點完成，非最終驗收；只記錄本輪實測。

## 主機與容量
- Ubuntu 26.04 / kernel 7.0.0-38-generic；Docker 29.1.3、Compose v5.6.0、Podman 5.7.0。
- 根磁碟 332.1 GB，已用 296.7 GB，可用 35.4 GB，90%。
- /home/xiaye 約 39.88 GB；vps-mirror-workspace 27.46 GB；CKA-Agent 5.20 GB；hermes-007 2.76 GB；agent-os-portable 1.47 GB；ai-agent-fleet 1.08 GB。
- /usr/local/lib/node_modules 9.22 GB；Python 3.14 8.10 GB；Hermes 3.26 GB；Ollama 2.21 GB；/var/lib/docker 4.99 GB。
- 未刪除資料；先核對依賴、使用狀態與備份。

## 執行環境
- 30 containers、24 images、32 volumes；349 systemd service unit files；failed units 查詢 0。
- 已發現 OpenHands、Hermes/LiteLLM、Open WebUI、Dify、Redis、Qdrant、PostgreSQL、Mem0、New API、Coolify、exa-mcp、mcp-proxy 等容器。
- 已辨識 agent-throne-file-center、dsh-agent、eni-harbor、frps、hermes-api、hermes-gateway、litellm、llama-agent、nginx、redis-server、sentinelx-cloud-core、termalin-agent 等 unit；尚未逐一驗證 running/HTTP health。
- Gateway listener 查詢 handler 回傳 invalid structured result；監聽埠未驗證。

## Git 狀態
- /home/xiaye/vps-mirror-workspace：vps-mirror/full-tree，clean，HEAD 0a325b3f1fce4f89744fae0fcf21c520e6a8595c。
- Ai-agent-skill：main，ahead 1 / behind 24，2 modified、7 untracked。
- CKA-Agent：main，2 modified、1 untracked。
- Claude-code：main，1 modified。
- hermes-007：master，behind 22；1 staged deletion 與同名 untracked .env.example，1 modified。
- openhands-extensions：main，1 modified。
- Google-AI：main，2,563 staged、1 modified；submodule/gitlink 語意未核清，不提交。
- agent-os-portable：41 untracked，含 home dotfiles、SSH/config/cache/logs，不可整包加入 Git。
- /opt/agents/-：main，ahead 1，2 modified、21 untracked。
- /opt/agent-plane：3 modified、8 untracked。
- /opt/openhands-upstream-build-v1.25.0：detached HEAD，1 staged、1 modified。
- /opt/sentinelx-cloud-core：2 untracked（.local、venv backup）。

## 去敏與遠端
- /opt/agents/- 的 origin URL 曾含 URL-embedded credential；已改為無憑證 SSH URL git@github.com:0megAlpha/-.git，讀回確認清除。此 clone 尚未推送，credential rotation 未完成。
- GitHub 登入 0megAlpha；目標 repo 0megAlpha/- 有管理及推送權限，visibility Public，default branch vps-mirror/full-tree，約 2.08 GB。
- vps-mirror-workspace 有 .ai-agent-skill-mirror.tar.gz（23,835,564 bytes）；尚未解包／掃描，public repo 風險優先。
- /opt/agent-integration/staging 有大量 nested Git checkout，且發現 .env/.envrc 檔案；未確認內容，不可整個 staging 推送。

## 外部整合
- Shellway greencloud-ai offline。
- SentinelX hosts=0，Free plan 1 個空位。
- Vercel 使用者 xavideo777-9021，Hobby plan，team list 空；projects 未完成檢查。
- Termalin host list 未重新讀取，online 未驗證。

## 未完成驗收
tarball 解包與 secret scan、staging tree/size、nested repos 去重、Docker images/volumes 使用狀態、systemd runtime health、listener/HTTP checks、逐 Agent 去敏/推送/安裝/啟動/二次驗證、Vercel projects、Shellway online、SentinelX enrollment、Termalin connectivity、Notion 更新均未完成。
