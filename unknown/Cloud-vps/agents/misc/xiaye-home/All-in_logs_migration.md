# 大檔遷移說明（2026-10-01 02:13:30）

- 來源：/root/ai-company /root/dsh
- 備份檔：/tmp/ai-migration/ai-company-backup.tar.gz（4.6G）
- SHA256：a551233ce24322aef5d0178a681f36de47ed99776470ad0caf9003d2d96703c7
- 下載連結：http://100.126.48.60:9999/ai-company-backup.tar.gz
- scp 指令：scp root@100.126.48.60:/tmp/ai-migration/ai-company-backup.tar.gz ./ai-company-backup.tar.gz
- 下載後驗證：echo "a551233ce24322aef5d0178a681f36de47ed99776470ad0caf9003d2d96703c7  ai-company-backup.tar.gz" | sha256sum -c
- ⚠️ 此服務無鑒權，僅限 Tailscale 內網使用；傳輸完成後請立即關閉：
  kill $(cat /tmp/migration-http.pid)

## Docker volumes（openwebui 等）
不要直接 tar /var/lib/docker/volumes（live 狀態易損壞）。建議：
  docker run --rm -v <volume_name>:/src -v /tmp/ai-migration:/dst alpine     tar czf /dst/<volume_name>.tar.gz -C /src .
之後一併放入 /tmp/ai-migration 由同一個 HTTP 服務下載。
