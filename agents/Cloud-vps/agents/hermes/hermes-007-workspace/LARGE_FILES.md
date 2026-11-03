# 大檔案（不推送，遷移時手動抓）
| 檔案 | 大小 | 說明 |
|------|------|------|
| /root/ai-company/backups/hermes-007-pre-merge-20260815-220218.tar.gz | 763M | hermes-007 合併前完整備份 |
| /root/.hermes（280M 運行中安裝）| 280M | 以本 repo 的 runtime/（設定+程式，排除 venv/金鑰/日誌）取代 |
遷移時用 scp/rsync 從舊 VPS 抓，不經 git。
