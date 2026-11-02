# cc-suite — Claude Code / Codex / OpenHands 雙向 MCP 橋接層

> 已安裝：`cc-suite@1.0.5`（npm 全域，2026-08-13）

## 用途
統一管理 Claude Code / OpenAI Codex / OpenHands / Cline 之間的 MCP 授權與跨主機代理：
- 單一源頭設定 MCP 伺服器清單（見 `opencode-engine/mcp-registry.json`）
- 跨 agent 共用同一組工具與憑證
- 異步代理：一個 agent 的任務可轉交另一個 agent 執行

## 本機整合點
| Agent | 設定檔 | 說明 |
|---|---|---|
| OpenCode | `/root/.config/opencode/opencode.json` | mcp 區塊已註冊 9 個 MCP 伺服器 |
| Claude Code | `/root/.claude-plugins/` | 本目錄為插件掛載點 |
| Codex CLI | `/root/.codex/config.toml` | 指向 LiteLLM 閘道（4000） |
| OpenHands | `http://localhost:18000` | 網頁畫布介面 |

## MCP 統一註冊表
```json
// /root/AI-Agent-Skill/opencode-engine/mcp-registry.json
{
  "filesystem": "mcp-server-filesystem",
  "github": "mcp-server-github",
  "postgres": "mcp-server-postgres",
  "kubernetes": "mcp-server-kubernetes",
  "sqlite": "mcp-server-sqlite",
  "fetch": "mcp-server-fetch",
  "docker": "docker-mcp",
  "aws": "aws-mcp",
  "npm": "npm-mcp-server"
}
```

## 規則
- 憑證一律從環境變數讀取，不寫入本目錄
- 跨主機代理前確認目標 agent 的授權範圍
