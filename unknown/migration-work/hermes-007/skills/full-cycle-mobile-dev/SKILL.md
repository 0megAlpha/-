# 終極全端開發與手機協作矩陣 (Master Skill)

## 1. 手機端編程痛點與終極解決方案
### A. Termux 環境極致優化 (解決螢幕小、輸入難)
- **快捷鍵擴展**：編輯 `~/.termux/termux.properties` 加入 `extra-keys = [['ESC','/','~','UP','HOME','PGUP','DEL'],['TAB','CTRL','LEFT','DOWN','RIGHT','PGDN','BKSP']]`
- **SSH 防斷線**：在 `~/.ssh/config` 強制加入 `ServerAliveInterval 60` 與 `ServerAliveCountMax 3`。
- **環境秒開**：將常用 alias 寫入 `~/.bashrc`，如 `alias v='nvim'`, `alias g='git'`, `alias py='python'`。

### B. Acode / Spck Editor SFTP 無縫同步
- **痛點**：手機編輯器無法直接運行後端代碼。
- **解法**：使用 Acode 的 FTP/SFTP 插件，配置 VPS IP、Port 22、User root、SSH Key。開啟 "Auto Save & Upload"，實現手機打字，VPS 即時運行。

## 2. Agent 協作與 SDLC 全流程
### A. 需求與架構 (PRD & Mermaid)
- 強制使用 Mermaid.js 繪製架構圖，確保 Agent 能解析並生成對應代碼骨架。
### B. 自動化測試與 CI/CD
- 整合 PyTest/Jest，要求 Coverage > 80%。
- 產出 `.github/workflows/deploy.yml`，Push 到 main 自動觸發 Docker Build 並 SSH 部署到 VPS。

## 3. 必備熱門套件矩陣 (Agent 自動安裝)
- **後端**：FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **前端**：React, TailwindCSS, Zustand
- **DevOps**：Docker, GitHub Actions, Nginx Proxy Manager
- **AI 整合**：LangChain, LiteLLM, Open WebUI
