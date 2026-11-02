# 共享 References（~/.agents/references/）

放「跨技能共享」的長文檔，避免一份內容隨多個技能重複維護：

- `prompts/`：通用 prompt 模板
- `configs/`：各 Agent 的 config 範例（不含真實 Key）
- `sops/`：標準作業程序
- `vendors/`：服務商 API 摘要（OpenAI / Anthropic / DeepSeek / Moonshot / OpenRouter…）

## 規則
1. 技能包內不放 references 內容，只放指到這裡的路徑
2. 本目錄可由多個 Agent 共享（one pack many agents 的落地點）
3. 含憑證的檔案一律不放這裡；改用各 Agent 自己的 secret 機制（環境變數）
