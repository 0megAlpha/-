---
name: plan-once-verify-always
description: 任何代碼提交前必須通過 DGM 沙箱驗證；計畫一次，驗證永遠。
version: "1.0.0"
owner: "All-in"
---
# 驗證規則（merge gate）
- pytest 覆蓋率 >= 80%
- semgrep 掃描無高風險
- 驗證通過率 >= 95%（連續 20 次試次）

# 規則
- 驗證失敗 → 回到 CODE_STAGE，不得帶病前進
- 驗證數據寫回 SESM metrics.trials / success_rate，供 DGM 升版判斷
- 與 SESM 的 MIN_TRIALS=20 對齊
