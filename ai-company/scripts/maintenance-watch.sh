#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

HOST="$(hostname -s 2>/dev/null || hostname)"
STAMP="$(date --iso-8601=seconds)"
LOAD="$(awk '{print $1" "$2" "$3}' /proc/loadavg)"
MEM_TOTAL="$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)"
MEM_AVAIL="$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)"
MEM_USED_PCT=0
if [[ "${MEM_TOTAL:-0}" =~ ^[0-9]+$ && "${MEM_AVAIL:-0}" =~ ^[0-9]+$ && "$MEM_TOTAL" -gt 0 ]]; then
  MEM_USED_PCT=$(( (MEM_TOTAL - MEM_AVAIL) * 100 / MEM_TOTAL ))
fi
ROOT_USED_PCT="$(df -P / | awk 'NR==2 {gsub(/%/,"",$5); print $5}')"
ROOT_AVAIL="$(df -hP / | awk 'NR==2 {print $4}')"
SWAP_TOTAL="$(awk '/^SwapTotal:/ {print $2}' /proc/meminfo)"
SWAP_FREE="$(awk '/^SwapFree:/ {print $2}' /proc/meminfo)"
SWAP_USED_PCT=0
if [[ "${SWAP_TOTAL:-0}" =~ ^[0-9]+$ && "${SWAP_FREE:-0}" =~ ^[0-9]+$ && "$SWAP_TOTAL" -gt 0 ]]; then
  SWAP_USED_PCT=$(( (SWAP_TOTAL - SWAP_FREE) * 100 / SWAP_TOTAL ))
fi

SUMMARY="host=$HOST at=$STAMP load=$LOAD memory_used=${MEM_USED_PCT}% root_disk_used=${ROOT_USED_PCT}% root_available=$ROOT_AVAIL swap_used=${SWAP_USED_PCT}%"
logger -t ai-company-capacity-watch -- "$SUMMARY"
printf '%s\n' "$SUMMARY"

if (( MEM_USED_PCT >= 90 )); then
  logger -p daemon.warning -t ai-company-capacity-watch -- "WARNING memory usage is at least 90 percent: $SUMMARY"
fi
if [[ "$ROOT_USED_PCT" =~ ^[0-9]+$ ]] && (( ROOT_USED_PCT >= 90 )); then
  logger -p daemon.warning -t ai-company-capacity-watch -- "WARNING root filesystem usage is at least 90 percent: $SUMMARY"
fi
if (( SWAP_USED_PCT >= 90 )); then
  logger -p daemon.warning -t ai-company-capacity-watch -- "WARNING swap usage is at least 90 percent: $SUMMARY"
fi
