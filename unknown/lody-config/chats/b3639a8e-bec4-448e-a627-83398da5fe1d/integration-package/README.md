# DSH 技能整合套件（ai-agent-skill 比對結果）

本套件是「ai-agent-skill 儲存庫 ↔ 本機 DSH 技能庫」完整比對後產出的整合包。

## 內容

| 項目 | 說明 |
|---|---|
| `skills/`（34 個） | 經安全掃描與重疊比對後挑選的推薦技能，格式與本機 `/root/.agents/skills` 完全相容 |
| `manifest.json` | 全部 168 個候選技能的中繼資料（名稱、分類、來源 repo、描述、是否推薦） |
| `install.sh` | 一鍵安裝腳本（支援 `--list` / `--dry-run` / 指定技能名 / `--force` / `TARGET_DIR`） |
| `../dsh-integration-report.md` | 完整比對報告（能力盤點、差異分析、安全評估） |

## 推薦技能來源分佈

| 來源儲存庫 | 數量 | 內容 |
|---|---|---|
| seb1n/awesome-ai-agent-skills | 24 | 多代理編排、MCP 建構、上下文工程、提示注入防禦、開發/DevOps/資料/寫作/研究通用品 |
| MoizIbnYousaf/ai-agent-skills | 5 | 技能生命週期管理（review-a-skill、verification-agent、changelog-generator…） |
| dean9703111/ai-agent-skill-for-video-workflow | 4 | 影音字幕工作流（audio-to-srt、srt-enhancer、字卡、社群摘要） |
| valenovo/ai-agent-skills | 1 | baidu-api-search（中文搜索，**需設定 `BAIDU_AI_SEARCH_API_KEYS` 環境變數**） |

## 安裝方式

```bash
# 先預覽
bash install.sh --dry-run

# 安裝全部推薦技能（目標 ~/.agents/skills）
bash install.sh

# 只裝部分
bash install.sh translation deep-research audio-to-srt
```

> ⚠️ DSH 沙盒內 `/root/.agents/skills` 是唯讀檔案系統，請在 VPS 自己的 shell（SSH 登入後）執行本腳本。安裝後重啟 agent session 生效。

## 注意事項

1. **hoodini/ai-agents-skills 未列入推薦**：其技能多依賴 `curl | bash` 外部安裝腳本與外部服務金鑰（fal-ai、yuv-* 系列），供應鏈風險較高。如需安裝請先自行審閱內容，完整清單見 `manifest.json`。
2. **seb1n 的 `frontend-design` 與本機技能同名，刻意排除**，避免覆蓋本機既有能力。
3. `baidu-api-search` 需要[百度 AI Search API Key](https://github.com/valenovo/baidu-search-skill)，裝了沒 Key 也不會壞，只是無法使用。
4. 全部 34 個技能皆通過紅旗模式安全掃描（提示注入、pipe-to-shell、憑證外洩等 10 種模式），掃描結果見主報告「安全評估」章節。
