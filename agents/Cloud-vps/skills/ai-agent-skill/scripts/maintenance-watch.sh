#!/usr/bin/env bash
# 容量監控：磁碟/資料庫/日誌超過門檻時寫入提醒檔（供使用者查看清理）
set -u
REPORT=/root/ai-company/reports/CAPACITY-REMINDER.txt
mkdir -p "$(dirname "$REPORT")"

THRESH_DISK=80          # 磁碟使用率 % 
THRESH_OPENCODE=200     # opencode db MB
THRESH_WEBUI=500        # openwebui db MB
THRESH_LOG=200          # 單一日誌 MB

TODAY=$(date '+%Y-%m-%d %H:%M')
touch "$REPORT"
{
  echo "===== 容量檢查 $TODAY ====="
  df -h / | tail -1
  du -sm /root/.local/share/opencode/opencode.db 2>/dev/null | awk '{print "opencode.db: "$1" MB"}'
  du -sm /root/ai-company/open-webui/webui.db 2>/dev/null | awk '{print "openwebui webui.db: "$1" MB"}'
  du -sm /root/ai-company/logs 2>/dev/null | awk '{print "ai-company/logs: "$1" MB"}'
  echo "-----"
} >> "$REPORT"

DISK=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
OC=$(du -sm /root/.local/share/opencode/opencode.db 2>/dev/null | cut -f1)
WUI=$(du -sm /root/ai-company/open-webui/webui.db 2>/dev/null | cut -f1)
LOG=$(du -sm /root/ai-company/logs 2>/dev/null | cut -f1)

ALERT=0
if [ "${DISK:-0}" -ge "$THRESH_DISK" ]; then ALERT=1; fi
if [ "${OC:-0}" -ge "$THRESH_OPENCODE" ]; then ALERT=1; fi
if [ "${WUI:-0}" -ge "$THRESH_WEBUI" ]; then ALERT=1; fi
if [ "${LOG:-0}" -ge "$THRESH_LOG" ]; then ALERT=1; fi

if [ "$ALERT" -eq 1 ]; then
  {
    echo "⚠️  ⚠️  建議清理！門檻：磁碟>${THRESH_DISK}% / opencode db>${THRESH_OPENCODE}MB / webui db>${THRESH_WEBUI}MB / logs>${THRESH_LOG}MB"
    echo "清理建議："
    echo "  - opencode 舊 session：opencode web 刪除舊對話，或清 /root/.local/share/opencode/opencode.db"
    echo "  - OpenWebUI 舊聊天：在 UI 刪除舊對話（資料存 /root/ai-company/open-webui）"
    echo "  - 快取：rm -rf /root/.cache/pip /root/.cache/uv /tmp/pip-*"
    echo "  - 舊備份：ls -lh /root/ai-company/backups | tail"
    echo "===== 提醒結束 ====="
  } >> "$REPORT"
fi
