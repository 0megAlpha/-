# 大檔案清單（不推送，遷移時手動抓）
| 檔案 | 大小 | 內容 |
|------|------|------|
| /root/ai-company-backup-20260918-181827.tar.gz | 1.8G | ai-company 完整備份 |
| /root/backups/openwebui-data-20260919-070711.tar.gz | 967M | Open WebUI 資料 |
| /root/OPENWEBUI_FINAL_20260919.tar.gz | 805M | Open WebUI 最終備份 |
| /root/openwebui_verified_20260919_054004.tar.gz | 805M | Open WebUI 驗證備份 |
| /root/ai-company/backups/hermes-007-pre-merge-20260815-220218.tar.gz | 763M | hermes-007 合併前備份 |
| /root/backups/dsh-full-20260919-070711.tar.gz | 469M | DSH 完整備份 |
| /root/backups/dsh-integrated-20260919-115415.tar.gz | 353M | DSH 整合備份 |
| /root/ai-company/backups/Ai-Agent-Skill-final-backup-20260816-062948.tar.gz | 130M | Ai-Agent-Skill 備份 |
| /root/.hermes（目錄） | 280M | 已由 hermes-007 repo 的 runtime/ 取代 |
| /root/.dsh（目錄） | 3.0G | node_modules 為主；設定已存 dsh/，資料屬敏感不備份 |
遷移時用 scp/rsync 從舊 VPS 抓，不經 git。
