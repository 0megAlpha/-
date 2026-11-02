---
name: ecc
description: 錯誤檢測與自動修補（Error Correction Cycle）：靜態分析、邊界檢查、安全掃描、自動補丁。
version: "1.0.0"
owner: "All-in"
---
# 能力
- static-analysis（semgrep / ruff / mypy）
- boundary-check（輸入邊界、空值、併發競態）
- security-scan（gitleaks / trivy / 依賴漏洞）
- auto-patch（修補後必須重跑 plan-once-verify-always 驗證閘）

# 觸發時機
CODE_STAGE 結束後與 VERIFY_STAGE 失敗時自動啟動。
