---
name: custom-codereview-guide
description: open-hands 專案的自訂程式碼審核指南
triggers:
  - /codereview
---
# open-hands 程式碼審核指南
## 核心原則
1. **安全性優先**：所有輸入必須驗證，所有認證必須檢查
2. **測試覆蓋**：新功能必須包含測試
3. **程式碼簡潔**：避免不必要的複雜性
## 檢查項目
- 輸入驗證與 Sanitization
- API 端點認證檢查
- 參數化查詢 (防 SQL 注入)
- 輸出編碼 (防 XSS)
- 禁止硬編碼敏感資訊
