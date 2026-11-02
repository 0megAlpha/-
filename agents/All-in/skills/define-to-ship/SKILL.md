---
name: define-to-ship
description: 強制執行從需求定義到上線的完整生命週期，任何階段不得跳過。
version: "1.0.0"
owner: "All-in"
---
# 工作流（硬性順序）
1. 需求澄清 → 2. 技術選型 → 3. 代碼編寫 → 4. 單元測試 → 5. 自動部署 → 6. 產出文檔

# 閘門
- 每階段產出必須寫入 artifacts，缺件不得進入下一階段
- 部署前必須通過 plan-once-verify-always 的驗證閘
- 上線後回寫 engineering-memory（決策 + 結果）
