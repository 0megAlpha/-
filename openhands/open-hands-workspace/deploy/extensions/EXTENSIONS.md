# OpenHands 熱門擴充套件清單（官方 + 安全社群）

來源: 官方 marketplace = `github.com/OpenHands/extensions.git`（本機 clone 在
`/home/xiaye/openhands-extensions`）。安裝透過 UI: **Settings → Marketplace**，
或把 `deploy/settings.json.example` 的 `registered_marketplaces` 寫入
`~/.openhands/settings.json` 後重啟 app。

## 一、官方 Plugins（編程/終端優化優先）
| Plugin | 用途 |
|---|---|
| **pr-review** | PR 自動審查（code review 最佳化） |
| **qa-changes** | 變更品質驗證 / QA 檢查 |
| **magic-test** | 自動產生與執行測試 |
| **issue-duplicate-checker** | issue 重複偵測 |
| **vulnerability-remediation** | 漏洞修補建議（安全） |
| **release-notes** | 自動產生 release notes |
| **migration-scoring** | 遷移難度評分 |
| **cobol-modernization** | 老碼現代化 |
| **city-weather** | 天氣工具 |
| **onboarding** | 入門引導 |
| **openhands** | OpenHands 核心整合 |

## 二、官方 Automations（自動化）
| Automation | 用途 |
|---|---|
| **github-pr-reviewer** | 自動 PR reviewer |
| **github-repo-monitor** | repo 健康監控 |
| **upstream-fork-sync** | 上游 fork 同步（搭配本 repo 的 update 流程） |
| **jira-issue-to-pr** | Jira issue → PR |
| **linear-triage-assistant** | Linear 分派 |
| **slack-channel-monitor / standup-digest** | Slack 監控/摘要 |
| **incident-retrospective-drafter** | 事後檢討草稿 |
| **research-brief-writer** | 研究簡報產生 |

## 三、Skills（官方）
| Skill | 用途 |
|---|---|
| custom-codereview-guide | 自訂 code review 準則 |

## 四、熱門 MCP 工具（可選，UI 或 mcp_config 設定）
| MCP | 用途 |
|---|---|
| GitHub MCP | repo/issue/PR 操作 |
| Docker MCP | 容器管理 |
| Kubernetes MCP | k8s 操作 |
| Postgres MCP | 資料庫查詢 |
| Brave Search | 網頁搜尋 |

## 安裝步驟
1. 開啟 openhands UI（本機 :3000）→ **Settings → Marketplace**
2. 確認 "openhands-official" 已註冊（或貼上 `https://github.com/OpenHands/extensions.git`）
3. 勾選要啟用的 plugin / automation / skill → 一鍵啟用
4. 也可直接編輯 `~/.openhands/settings.json`（先備份）重啟 app

⚠️ 社群 marketplace 安裝前先看 stars/權限；本清單只列官方與安全熱門。
