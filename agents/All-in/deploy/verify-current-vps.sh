#!/usr/bin/env bash
# Read-only VPS smoke checks. Supply exact units and URLs through environment variables.
set -Eeuo pipefail
pass=0
fail=0
CHECK_UNITS="${CHECK_UNITS:-}"
CHECK_URLS="${CHECK_URLS:-}"
CHECK_DOCKER="${CHECK_DOCKER:-0}"
DISK_WARN_PERCENT="${DISK_WARN_PERCENT:-90}"

check_unit() {
  local unit="$1"
  if systemctl is-active --quiet "$unit"; then
    echo "PASS unit $unit"; pass=$((pass+1))
  else
    echo "FAIL unit $unit"; fail=$((fail+1))
  fi
}
check_http() {
  local name="$1" url="$2" code
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 "$url" 2>/dev/null || true)"
  if [[ "$code" == 200 ]]; then
    echo "PASS http $name status=$code"; pass=$((pass+1))
  else
    echo "FAIL http $name status=${code:-000}"; fail=$((fail+1))
  fi
}
for unit in $CHECK_UNITS; do check_unit "$unit"; done
if [[ -n "$CHECK_URLS" ]]; then
  IFS=';' read -r -a checks <<< "$CHECK_URLS"
  for item in "${checks[@]}"; do
    [[ "$item" == *=* ]] || { echo "FAIL invalid CHECK_URLS item: $item"; fail=$((fail+1)); continue; }
    check_http "${item%%=*}" "${item#*=}"
  done
fi
if [[ "$CHECK_DOCKER" == 1 ]]; then
  running="$(docker ps -q | wc -l)"
  volumes="$(docker volume ls -q | wc -l)"
  echo "INFO docker_running=$running docker_volumes=$volumes"
fi
disk="$(df -P / | awk 'NR==2 {gsub(/%/, "", $5); print $5}')"
echo "INFO disk_used_percent=${disk:-unknown}"
if [[ "$disk" =~ ^[0-9]+$ ]] && (( disk >= DISK_WARN_PERCENT )); then
  echo "WARN disk usage is at or above ${DISK_WARN_PERCENT}%"
fi
echo "=== SUMMARY: $pass PASS / $fail FAIL ==="
if (( pass + fail == 0 )); then echo "ERROR no checks configured" >&2; exit 2; fi
(( fail == 0 ))
