#!/bin/bash
cd /root/AI-Agent-Skill/media-studio/backend
if [ -f /root/AI-Agent-Skill/media-studio/media_studio.pid ]; then
  OLD_PID=$(cat /root/AI-Agent-Skill/media-studio/media_studio.pid)
  if kill -0 "$OLD_PID" 2>/dev/null; then
    kill "$OLD_PID" 2>/dev/null || true
    sleep 1
  fi
fi
nohup python3 app.py > /root/AI-Agent-Skill/logs/media_studio.log 2>&1 &
echo $! > /root/AI-Agent-Skill/media-studio/media_studio.pid
