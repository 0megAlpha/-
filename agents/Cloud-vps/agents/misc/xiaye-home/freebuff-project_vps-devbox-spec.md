# VPS AI 開發環境建置 Spec（vps-devbox-spec）

> 狀態：**草稿（draft）** — 尚未進行任何實作
> 建立日期：2026-08-04
> 來源：4 輪使用者訪談 + VPS 唯讀盤點（未修改任何檔案）
> 角色：Buffy（Freebuff）代為規劃；最終決策與高風險操作均需使用者確認

---

## 1. 需求摘要（使用者原始目標）

1. Freebuff 協助管理與開發 VPS 上的各專案。
2. VPS 未來會安裝許多開發工具、AI Agent、CLI、Web 服務與專案（OpenHands、OpenCode、Codex、LiteLLM、Open WebUI、Hermes、Cline…），**不預設它們已存在**。
3. **禁止**把系統檔案、密碼、SSH 金鑰、API Key、Token、Cookie、.env、資料庫密碼等敏感資訊提交到 GitHub。
4. 建立清楚的專案與 Git 管理結構，各專案各自有獨立 Git repository。
5. 可從 GitHub clone / pull，有權限時 commit / push 自己的修改。
6. 可拉取其他公開或授權的 repository 用於研究、整合或開發。
7. Git 操作必須保護敏感資訊：合理的 .gitignore、避免 .env / SSH 私鑰 / API 金鑰 / Token / 憑證 / secrets。
8. **不要把整個 VPS root filesystem 變成一個 Git repository。**
9. 先檢查 VPS 現況（OS、Git、Node、npm、Python、Docker、目錄結構、磁碟空間、既有專案/服務）。
10. 現階段只做檢查與規劃，**不刪除、重裝、覆蓋或破壞**現有東西。
11. 執行命令前先說明目的；高風險操作（刪除、覆蓋、權限變更、git reset、force push、credentials）需先取得確認。
12. 最後提出適合此 VPS 的 GitHub + Freebuff 開發架構與建置順序。

---

## 2. VPS 現況盤點（2026-08-04，唯讀檢查）

### 2.1 硬體與系統

| 項目 | 數值 |
|---|---|
| OS | Ubuntu 26.04 LTS (Resolute Raccoon) |
| Kernel | 7.0.0-15-generic x86_64 |
| Hostname | `greencloud-ai` |
| CPU | 4 vCPU |
| RAM | 31 GiB（可用約 30 GiB） |
| Swap | 2 GiB（未使用） |
| 磁碟 | /dev/vda1 310G，使用 6.0G，可用 **304G**（2%） |

### 2.2 工具鏈

| 工具 | 版本 | 狀態 |
|---|---|---|
| git | 2.53.0 | ✅ 已安裝 |
| node | v24.18.1 | ✅ 已安裝 |
| npm | 11.16.0 | ✅ 已安裝 |
| python3 | 3.14.4 | ✅ 已安裝 |
| pip3 | 25.1.1 | ✅ 已安裝 |
| docker | 29.7.1（daemon 運行中） | ✅ 已安裝，0 容器 |
| docker-compose | — | ❌ 未找到 binary（`docker compose` plugin 待驗證） |
| gh (GitHub CLI) | — | ❌ 未安裝 |
| curl / jq | 8.18.0 / 1.8.1 | ✅ 已安裝 |
| zsh | — | ❌ 未安裝（維持 bash） |

Docker 環境：storage driver `overlayfs`、cgroup v2（systemd driver）。

### 2.3 現有狀態（乾淨的起點）

- **無任何 Git repository**（已掃描 /root、/home、/srv、/opt、/var/www，depth 4）。
- **無 git 全域設定**（無 user.name / user.email）。
- **/root/.ssh/authorized_keys 為空**（0 bytes）——無已配置的登入金鑰。
- **對外監聽**：僅 port 22 (sshd)；其餘為本機 DNS (127.0.0.53:53)。
- **運行中服務**：系統基礎服務（ssh、docker、containerd、chrony、cron、unattended-upgrades、qemu-guest-agent 等），無自架應用服務。
- **目錄現況**：
  - `/root`：.bashrc、.bash_history、.profile、.cache、.config/manicode、.local/share、.npm、.ssh、`freebuff-project`（空，Freebuff 工作目錄）
  - `/home/xiaye`：`drwxr-x--- xiaye:xiaye`，內有 .bashrc、.bash_history、.cache、.profile、.ssh（存在但空）
  - `/srv`：空；`/opt`：僅 containerd 資料
- **npm 全域套件**：corepack、freebuff@0.0.137、npm。

---

## 3. 已確認決策（訪談結論）

| 主題 | 決策 |
|---|---|
| 使用者 | **單一使用者**（xiaye），保留 `/home/xiaye` |
| Shell | **bash**（維持現狀） |
| 專案目錄 | `/home/xiaye/repository/` = 正式 GitHub 專案；`/home/xiaye/game/` = 臨時測試與實驗；`/home/xiaye/bot/` = 長駐服務 |
| Repo 命名 | repository/ 內各專案**各自管理 Git，不固定 repo 命名** |
| GitHub 認證 | **全新專用 SSH key**（推薦方案） |
| Repo 種類 | 自己的 repo **預設全部 private** |
| Git 身分 | user.name / user.email **由使用者之後提供** |
| dotfiles repo | **之後再決定** |
| 機密存放 | **混合方案**：專案 secrets 用各自 .env（gitignored）；AI 工具（LiteLLM/OpenHands 等）API key 集中管理、由 Freebuff 代管 |
| .gitignore | **雙層**：每專案 .gitignore + git 全域 `core.excludesFile` |
| Secret 掃描 | **由 Freebuff 決定 → 建議 gitleaks**（pre-commit hook），待使用者確認後安裝 |
| 開發身分 | 日常開發用 **xiaye** 身分；Freebuff/root 僅在需要時介入代管 |
| 部署方式 | 長駐服務用 **Docker Compose**（需先驗證 compose plugin） |
| 反向代理 | **Caddy**（自動 HTTPS） |
| 備份 | **Git push 為主 + 定期 rsync/tar 打包** |
| 對外服務 | 會公開 Web 服務（Open WebUI、LiteLLM、agents 等），**清單持續增加、不設限** |
| 工具優先 | OpenCode、Codex、LiteLLM、OpenHands、Open WebUI、Cline、Hermes，及**之後新增的 AI Agent / CLI / 模型工具**（開放清單） |

---

## 4. 目錄與專案結構規劃

```
/home/xiaye/
├── repository/          # 正式 GitHub 專案（每個專案 = 獨立 git repo）
│   ├── <專案A>/
│   │   ├── .git/
│   │   ├── .gitignore
│   │   └── ...
│   └── <專案B>/
├── game/                # 臨時測試、實驗、sandbox（可不管理 git）
└── bot/                 # 長駐服務（每個服務一個子目錄 + docker-compose.yml）
    ├── open-webui/
    ├── litellm/
    ├── openhands/
    └── ...
```

### 結構規則

- **禁止**對 `/`、`/home`、`/home/xiaye`、`/root` 做 `git init`——repository/ 底下才允許出現 repo。
- repository/ 內每一層資料夾即一個獨立 repo，命名不設限（使用者習慣）。
- game/ 為實驗區，允許暫時沒有 git；若需要版本化再個別 init。
- bot/ 內每個服務獨立資料夾，各自可為獨立 repo（**僅含設定檔與 compose 檔，不含 secrets**）。
- Freebuff 工作目錄 `/root/freebuff-project/` 存放本 spec 與規劃文件（可另以私有 repo 版本化，待定）。

---

## 5. Git 與 GitHub 架構

### 5.1 認證（SSH key，以 xiaye 身分）

1. 以 **xiaye** 身分產生專用 key：`~xiaye/.ssh/github_ed25519`（`ed25519`、`chmod 600`、`~xiaye/.ssh` 權限 700）。
2. 設定 `~xiaye/.ssh/config` 指向 GitHub 使用此 key。
3. **需要使用者**：將 public key 加入 GitHub 帳號（`Settings → SSH and GPG keys`），並提供 GitHub username。
4. 驗證：`ssh -T git@github.com`。

### 5.2 全域 git 設定（xiaye 身分）

- `user.name` / `user.email`（待使用者提供；建議 GitHub noreply email）
- `init.defaultBranch = main`
- `push.default = simple`
- `core.excludesfile = ~/.gitignore_global`（全域忽略清單，見 §6.1）
- 可選：`commit.gpgsign`（待定）

### 5.3 工作流

- 新建專案：GitHub 建立 private repo → clone → 開發 → commit → push（僅限自己的 repo）。
- 研究用 repo：以 clone / pull 為主（read-only），除非有權限與需求才 push。
- 每個 repo 先有 .gitignore 才允許第一次 commit（搭配 gitleaks 把關）。

---

## 6. 敏感資訊防護設計

### 6.1 全域忽略清單（`~xiaye/.gitignore_global` 草案）

```gitignore
# 環境與機密
.env
.env.*
*.env
!.env.example

# 金鑰與憑證
*.pem
*.key
*.p12
*.pfx
*.crt
*.cer
id_rsa*
id_ed25519*
*.pem
service-account*.json
credentials*.json

# Secrets / token
.secrets/
*secret*
*token*
*credential*

# 常見開發暫存
node_modules/
__pycache__/
*.pyc
.DS_Store
*.log
```

> 註：`core.excludesFile` 只保護「忘了寫 .gitignore」的意外；**不取代**專案內 .gitignore。

### 6.2 防護類別清單（使用者確認）

`.env*`、`*.pem`、`*.key`、`*.p12`、`*.pfx`、SSH 私鑰、API keys、Access tokens、OAuth credentials、Cloud credentials、Service-account JSON、資料庫密碼 / connection strings、JWT secrets、Cookie/session secrets、TLS 憑證與私鑰、以及 `/root/.secrets/`（或集中 secrets 目錄）內含 credentials / secrets / passwords 的檔案。

### 6.3 機密存放（混合方案）

- **專案層**：各專案自己的 `.env`（gitignored、權限 600）。
- **集中層**：AI 工具所需 API key 集中管理，建議 `~xiaye/.secrets/`（`chmod 700`），由 Freebuff 代管；實際路徑待使用者確認（`/home/xiaye/.secrets` vs `/root/.secrets`）。
- 工具設定檔（LiteLLM config 等）若含 key，必須指向環境變數或集中目錄，**不直接寫死**進設定檔。

### 6.4 Secret 掃描（建議：gitleaks）

- 安裝 gitleaks（single binary），以 pre-commit hook 方式在 commit 前掃描。
- 全域層級或每 repo 層級皆可；建議先全域 pre-commit，之後再視情況細化。
- **待使用者確認後才安裝。**

### 6.5 Shell 歷史衛生

- 避免在命令列直接帶入 key / password（改用讀檔或互動輸入）。
- `.bash_history` 本身不進 git；若之後 dotfiles repo 建立，需明確排除。

---

## 7. 身分與權限

- 日常開發：**xiaye**（非 root），GitHub SSH key、專案檔案皆屬 xiaye。
- Freebuff / root：僅在需要系統層級維護（Docker、服務、防火牆）時介入，操作前先說明。
- `/home/xiaye` 目前權限 `drwxr-x---`（xiaye:xiaye）；repository/game/bot 建立後維持 xiaye 所有權。
- sudo 原則：xiaye 是否賦予 sudo 待使用者決定（規劃上建議最小權限、需要時才授權）。

---

## 8. 部署與服務架構（Docker Compose + Caddy）

- **前置**：驗證 `docker compose` plugin 是否可用（未找到 `docker-compose` binary；Docker 29.x 通常內建 plugin，需確認）。
- bot/ 下每個服務一個資料夾，內含 `docker-compose.yml` 與非敏感設定；**secrets 一律以 `.env` 或 compose `env_file` 引入**，檔案 gitignored。
- 對外服務統一由 **Caddy** 反向代理：自動 HTTPS（Let's Encrypt）、多服務 subdomain 路由。
- 防火牆：UFW（開放 22、80、443；服務間內部網路不開放對外）。
- 每服務附 systemd（或 compose restart policy）確保開機自啟。

### 候選服務藍圖（開放清單，不設限）

| 工具 | 型態 | 安裝/部署 | Secrets 注意 |
|---|---|---|---|
| OpenCode | CLI agent | npm（xiaye） | API key 走集中管理 |
| Codex | CLI agent | 官方安裝 | API key 走集中管理 |
| LiteLLM | LLM gateway | Docker Compose（bot/） | 設定檔不含 key，走 env |
| OpenHands | agent 平台 | Docker Compose | 設定走 env |
| Open WebUI | Web 介面 | Docker Compose | 登入/DB secrets 走 env |
| Cline | VSCode 外掛/CLI | 依官方方式 | key 不落 repo |
| Hermes | agent | 待確認 | 同前 |
| 其他未來工具 | — | 開放 | 一律遵守 §6 |

---

## 9. 備份策略

- **第一層**：所有 repository/ 專案 push 到 GitHub（GitHub 即備份）。
- **第二層**：cron 定期執行 `tar` / `rsync`，打包：
  - repository/game/bot 的非 git 檔案（如 `.env.example`、設定、dump）
  - 集中 secrets（建議加密後才送外部）
  - 排除：`node_modules`、`.git`、Docker volumes（視需求另備份 volumes）
- 備份目的位置（本機外接、另一台機器、物件儲存）**待使用者確認**。

---

## 10. 實作順序（建議 roadmap）

> 每個高風險步驟前會先向使用者說明並取得確認。

| Phase | 內容 | 需要確認？ |
|---|---|---|
| **P0** | 盤點完成（本文件）；取得 GitHub username、git 身分、gitleaks 同意 | ✅ 需要 |
| **P1** | 建立目錄結構 `/home/xiaye/{repository,game,bot}`（`mkdir`，低風險） | 建立前告知 |
| **P2** | xiaye 身分設定 git 全域設定 + 建立 `~xiaye/.gitignore_global` | 內容審閱 |
| **P3** | 產生 GitHub SSH key（xiaye）、ssh config、`ssh -T` 驗證 | ✅ 需要（pub key 需使用者加入 GitHub） |
| **P4** | 安裝 gitleaks + pre-commit hook | ✅ 需要同意 |
| **P5** | 第一個私有 repo 試作（建立、clone、push 驗證流程） | ✅ 需要（GitHub 建 repo） |
| **P6** | 安裝優先工具：OpenCode / Codex（CLI）→ LiteLLM / Open WebUI / OpenHands（Docker Compose） | 各工具安裝前確認 |
| **P7** | Caddy 反向代理 + UFW 防火牆 + HTTPS | ✅ 需要（domain 資訊） |
| **P8** | 備份 cron + rsync 設定 | ✅ 需要（目的位置） |
| **P9** | dotfiles repo（之後決定） | 之後 |

---

## 11. 尚未確認 / 待使用者提供（Open Questions）

1. **GitHub username**（SSH key 註冊需要）。
2. **git user.name / user.email**（建議 GitHub noreply）。
3. **gitleaks 安裝同意**（建議：要）。
4. **集中 secrets 目錄位置**：`/home/xiaye/.secrets`（推薦）還是 `/root/.secrets`。
5. **Docker compose plugin** 驗證結果（P1 前先檢查 `docker compose version`）。
6. **xiaye 是否需要 sudo**。
7. **Caddy 的 domain**（已有網域？何時啟用對外？）。
8. **備份目的位置**（外部機器 / 物件儲存）。
9. **dotfiles repo** 的最終決定。
10. **OpenHands / Hermes / Cline 的具體用途**（研究或正式使用）。

---

## 12. 安全與操作原則（鐵則）

1. 不把 `/`、`/home`、`/root` 變成 Git repository。
2. 不 commit 任何 secrets（§6.2 清單）。
3. 高風險操作（刪除、覆蓋、權限變更、`git reset`、`--force` push、credentials 處理）**一律先取得使用者確認**。
4. 執行任何命令前先說明目的。
5. 不預設未安裝的工具存在；安裝前先確認安裝方式與來源。
6. 現階段（spec 確認前）**不做任何修改**。

---

## 13. 附錄：盤點原始輸出重點

- `uname -a` → Linux greencloud-ai 7.0.0-15-generic x86_64
- `df -h /` → /dev/vda1 310G / 6.0G used / 304G avail
- `free -h` → 31Gi total / 27Gi free；`nproc` → 4
- 工具版本：git 2.53.0 / node v24.18.1 / npm 11.16.0 / python 3.14.4 / pip 25.1.1 / docker 29.7.1
- `find ... -name .git` → 無結果（全系統無 git repo）
- `ss -tlnp` → 僅 22 (sshd) 與 127.0.0.53:53 監聽
- `/root/.ssh/authorized_keys` → 0 bytes（空）
- npm -g：corepack@0.35.0、freebuff@0.0.137、npm@11.16.0
