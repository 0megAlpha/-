---
name: engineering-memory
description: 工程決策記憶，對接 Qdrant，記錄架構決策、Bug 修復、成功模式，跨專案自動召回。
version: "2.0.0"
owner: "All-in"
---
# 核心能力
- memory.add：記錄決策與結果（含環境、版本、代碼片段）
- memory.search：檢索相似情境（語意 + 標籤）
- memory.update：更新已知案例的成功率與適用範圍

# 自動規則
1. 任務開始前：先檢索歷史相似案例，命中則優先採用已驗證解法
2. 任務結束後：寫入決策、Bug、解法、代碼片段與驗證結果
3. 跨專案自動召回；檢索結果必須標註來源任務與置信度

# 對接
Qdrant collection: sesm_experience / apollo_memories（見 core/sesm_engine.py）
