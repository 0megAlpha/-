#!/bin/bash
PID_FILE="/tmp/$(basename $0 .sh).pid"
LOG_FILE="/tmp/$(basename $0 .sh).log"
trap 'rm -f $PID_FILE; exit' INT TERM
echo "$$" > "$PID_FILE"
while true; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') heartbeat" >> "$LOG_FILE"
    sleep 60
done
