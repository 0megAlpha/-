---
name: harness-evolution
description: 整合 SWE-agent / mini-swe-agent / Self-Harness / Meta-Harness / LLM-as-a-Verifier 的進化腳手架。
version: "2.0.0"
owner: "All-in"
---
# 方案整合
- SWE-agent / mini-swe-agent：src/ 由 deploy/fix/03-install-harness-evolution.sh clone（已加入 .gitignore，不入庫）
- Self-Harness（上海AI Lab）：從失敗軌跡挖掘弱點，自動提出並驗證 Harness 修改
- Meta-Harness（Stanford 等）：自動搜索優化 Harness 代碼的外循環
- Live-SWE-agent（UIUC）：運行時自主進化腳手架
- LLM-as-a-Verifier（Stanford 等）：把粗略判分升級為細粒度核驗

# 規則
- 一律以「協同進化」為準：強模型只修正弱模型的失敗步驟，不做整軌模仿
- 所有演化結果必須過 DGM 驗證閘（試次 >= 20 且不退化才可升版）
