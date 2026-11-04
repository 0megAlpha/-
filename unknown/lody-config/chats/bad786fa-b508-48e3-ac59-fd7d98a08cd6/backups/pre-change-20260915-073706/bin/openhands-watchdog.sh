#!/usr/bin/env bash
set -uo pipefail
LOGFILE="/root/ai-company/logs/watchdog.log"
notify(){ local m="$1"; echo "$(date '+%F %T') $m" >> "$LOGFILE"
  command -v hermes >/dev/null 2>&1 && hermes send "$m" >/dev/null 2>&1 || true; }

docker ps --format '{{.Names}}' | grep -q "^openhands-canvas-staging$" || { notify "⚠️ OpenHands停止，自動拉起"; docker start openhands-canvas-staging; notify "✅ 已恢復"; }
docker ps --format '{{.Names}}' | grep -q "^agent-plane-caddy$" || { notify "⚠️ Caddy停止，自動拉起"; docker start agent-plane-caddy; notify "✅ 已恢復"; }
systemctl is-active --quiet tailscaled || { notify "⚠️ tailscaled停止，重啟中"; systemctl restart tailscaled; notify "✅ 已恢復"; }
tailscale serve status 2>/dev/null | grep -q "127.0.0.1:8443" || { notify "⚠️ serve轉發不是8443，重建中"; tailscale serve --bg --https=443 http://127.0.0.1:8443; notify "✅ 已恢復指向8443"; }
