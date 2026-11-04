---
name: sesm-engine
description: 2026 自進化狀態機：HyperAgents 突變 + DGM 沙箱驗證 + StateM 鎖定執行（安全版）。
version: "3.0.0"
owner: "All-in"
---
# 核心循環
外循環（HyperAgents 突變 runbook）→ DGM 驗證閘 → 內循環（StateM 鎖定執行）

# 安全閘（不可被演化移除，見 core/sesm_engine.py）
- 狀態僅能取自 ALLOWED_STATES 白名單
- TEST_STAGE / VERIFY_STAGE 永遠存在
- metrics.trials < 20 的自評分數不得升版（防 LLM 自吹自擂）
- 不做任何繞過模型安全機制的操作（無 meta-token、無越獄提示）
