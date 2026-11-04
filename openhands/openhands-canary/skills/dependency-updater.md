# Dependency Updater Skill

## 支持語言
- Python (pip, poetry, uv)
- JavaScript (npm, pnpm, yarn)
- Go (go.mod)
- Rust (Cargo.toml)

## 工作流
1. 掃描 lock 檔案
2. 檢查更新
3. 篩選安全/功能更新（Skip 重大版本除非明確要求）
4. 執行測試
5. 生成 PR 描述
6. 自動提交 PR（待人工審查）

## 觸發
- 手動：`freebuff update dependencies <repo>`
- 自動（Cron）：`0 0 * * 0 freebuff update --auto --pr-only`
