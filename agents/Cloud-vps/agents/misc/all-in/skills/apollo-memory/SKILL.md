---
name: apollo-memory
description: Nous Research 長期記憶引擎介面：跨會話記憶、實體提取、用戶畫像、自動摘要、衝突解決。
version: "2.0.0"
owner: "All-in"
---
# 記憶類型
fact / preference / code / decision / error / task

# 自動規則
1. 對話結束自動摘要（寫入 sessions 表）
2. 偵測偏好自動提取並存為 preference
3. 代碼模式自動保存（供 engineering-memory 召回）
4. 錯誤上下文自動記錄（供 ecc 召回）
5. 記憶衝突以時間戳 + 重要度裁決
