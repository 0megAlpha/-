# Claude Code 整合層
- core/   : Claude Code 主體（plugins/agents/skills）
- action/ : GitHub Action 觸發層
- 獨立調用：claude-code/core
- 協作模式：action 觸發 → core 執行 → skills 應用
