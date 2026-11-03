# Ai-agent-skill 協作面板說明

## 快速啟動
直接用瀏覽器開啟 `index.html`（或放到任何靜態伺服器）。
右上設定填入 Hermes / Qdrant 位址後按「儲存並刷新」。

## 資料來源（全部真實 fetch）
| 面板區塊 | 端點 | 用途 |
|---|---|---|
| Agent 協作狀態 | Hermes `/v1/agents/status` | 各 Agent 狀態與目前工作 |
| 記憶庫統計 | Qdrant `/collections`、`/collections/{name}` | collections / points / 狀態 |
| 記憶檢索 | Qdrant `POST /collections/{name}/points/scroll` | 最新 20 筆記憶 + 關鍵詞過濾 |

## CORS
瀏覽器直連 Hermes/Qdrant 需要服務端允許跨網域；
未開 CORS 時面板如實顯示 offline，不會假造數據。

## 注意
- API Key 只存在瀏覽器 localStorage（本機可見），請勿在共用裝置使用。
- Hermes 若尚未實作 `/v1/agents/status`，面板會顯示不可用（正常），
  等 Hermes 端補上該端點後面板自動顯示真實狀態。
