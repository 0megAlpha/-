# Spec-Driven Development Skill

## 用途
快速從需求 → 完整 spec (API/DB/架構/測試清單)

## 觸發提示詞
"根據這個需求產出完整 spec：[用戶需求]
格式：Markdown + YAML + OpenAPI 3.0"

## 工作流
1. 需求解析（提問澄清）
2. 架構設計（Mermaid 圖）
3. API 規格 (OpenAPI YAML)
4. 資料庫 Schema
5. 測試案例（BDD 格式）
6. 部署清單

## 輸出格式
```yaml
spec:
  version: 1.0
  project: [名稱]
  architecture: [Mermaid 圖]
  api: [OpenAPI YAML]
  database: [Schema SQL]
  tests: [BDD 列表]
  deployment: [檢查清單]
```
