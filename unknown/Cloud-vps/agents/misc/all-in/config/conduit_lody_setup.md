# Lody / Conduit 手機端填入指南（內網文件）

> ⚠️ 本檔含 Tailscale 內網位址（100.x.x.x 屬 CGNAT 保留段，無法從公網路由）。
> 僅供私有 repo 使用；若 repo 轉公開，請先移除內網 IP 與任何真實 Key。

## Provider 設定
- Provider type: OpenAI-compatible
- Base URL: http://100.x.x.x:8642/v1
- API Key: 從 .env 讀取 HERMES_API_KEY（嚴禁寫死在文檔或程式碼）
- Connection name: Hermes Manager

## Hermes Agent 區塊
- Hermes connection mode: Responses API
- Server URL: http://100.x.x.x:8642
- API Key: HERMES_API_KEY
- Memory key: （自訂）

## MCP Servers
- 加入 Streamable HTTP: http://100.x.x.x:8642/mcp
