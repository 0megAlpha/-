#!/usr/bin/env bash
# ============================================================
# 修復 2/4：大檔遷移（6.1G 級）
# 打包 ~/ai-company、~/openwebui、~/dsh（存在的才包）→ sha256 →
# 啟動「僅綁 Tailscale IP」的臨時 HTTP 服務 → 寫入 All-in/logs/migration.md
# ⚠️ 此 HTTP 服務無鑒權：只綁內網 IP、只serve專用目錄，傳完務必關閉！
# 額外來源可用 MIGRATION_EXTRA="~/dirA ~/dirB" 加入。
# ============================================================
set -euo pipefail
TS_IP="${TS_IP:-100.126.48.60}"
PORT="${MIGRATION_PORT:-9999}"
OUT_DIR="/tmp/ai-migration"
OUT="$OUT_DIR/ai-company-backup.tar.gz"
LOGS="$(cd "$(dirname "$0")/../.." && pwd)/logs"
mkdir -p "$LOGS" "$OUT_DIR"

ITEMS=()
for d in "$HOME/ai-company" "$HOME/openwebui" "$HOME/dsh"; do
  [ -e "$d" ] && ITEMS+=("$d")
done
for d in ${MIGRATION_EXTRA:-}; do
  [ -e "$d" ] && ITEMS+=("$d")
done

if [ ${#ITEMS[@]} -eq 0 ]; then
  echo "❌ 找不到 ~/ai-company、~/openwebui、~/dsh"
  echo "ℹ 本機 $HOME 下較大的候選目錄（自行決定要不要包進 MIGRATION_EXTRA）："
  du -sh "$HOME"/*/ 2>/dev/null | sort -h | tail -10 || true
  echo "ℹ Docker volumes 另外處理（不要直接 tar live volume，見下方註解）"
  exit 1
fi

echo "📦 打包中（來源：${ITEMS[*]}）… 可能需要數分鐘"
tar -czf "$OUT" "${ITEMS[@]}"
sha256sum "$OUT" > "$OUT.sha256"
SIZE=$(du -h "$OUT" | cut -f1)
echo "✅ 打包完成：$OUT（$SIZE）"
echo "⚠️ 打包前請確認來源目錄內沒有 .env / config.yaml 等憑證（本服務無鑒權）"

echo "🌐 啟動臨時 HTTP 服務（綁 $TS_IP:$PORT，僅 serve $OUT_DIR）..."
cd "$OUT_DIR"
nohup python3 -m http.server "$PORT" --bind "$TS_IP" > /tmp/migration-http.log 2>&1 &
echo $! > /tmp/migration-http.pid
sleep 1
kill -0 "$(cat /tmp/migration-http.pid)" 2>/dev/null || { echo "❌ HTTP 服務啟動失敗，看 /tmp/migration-http.log"; exit 1; }

SHA=$(awk '{print $1}' "$OUT.sha256")
cat > "$LOGS/migration.md" <<EOF
# 大檔遷移說明（$(date '+%F %T')）

- 來源：${ITEMS[*]}
- 備份檔：$OUT（$SIZE）
- SHA256：$SHA
- 下載連結：http://$TS_IP:$PORT/ai-company-backup.tar.gz
- scp 指令：scp ${USER}@$TS_IP:$OUT ./ai-company-backup.tar.gz
- 下載後驗證：echo "$SHA  ai-company-backup.tar.gz" | sha256sum -c
- ⚠️ 此服務無鑒權，僅限 Tailscale 內網使用；傳輸完成後請立即關閉：
  kill \$(cat /tmp/migration-http.pid)

## Docker volumes（openwebui 等）
不要直接 tar /var/lib/docker/volumes（live 狀態易損壞）。建議：
  docker run --rm -v <volume_name>:/src -v /tmp/ai-migration:/dst alpine \
    tar czf /dst/<volume_name>.tar.gz -C /src .
之後一併放入 $OUT_DIR 由同一個 HTTP 服務下載。
EOF

echo "✅ 已寫入 $LOGS/migration.md"
echo "⏳ 服務運行中（PID $(cat /tmp/migration-http.pid)）。"
echo "   下載完成後請執行：kill \$(cat /tmp/migration-http.pid)"
