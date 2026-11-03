#!/usr/bin/env bash
set -u
echo '=== backups dir ==='
ls -la /root/ai-company/backups/ 2>/dev/null
echo '=== tar contents (config-related) ==='
for t in /root/ai-company/backups/*.tar.gz; do
  [ -f "$t" ] || continue
  echo "--- $t ---"
  tar tzf "$t" 2>/dev/null | grep -iE 'litellm|auth|fleet.env|master-key|config/' | head -20
done
echo '=== bash history key patterns (masked) ==='
for h in /root/.bash_history /home/xiaye/.bash_history; do
  [ -f "$h" ] || continue
  echo "--- $h ---"
  grep -oE '(add-key\.sh [a-z]+ [A-Za-z0-9_-]{8,})|(nvapi-[A-Za-z0-9]{10,})|(sk-or-v1-[A-Za-z0-9]{10,})|(gsk_[A-Za-z0-9]{10,})|(sk-[A-Za-z0-9]{10,})' "$h" 2>/dev/null | sed -E 's/(.{14}).*/\1.../' | sort -u | head -10
done
echo '=== auth.json backups anywhere ==='
find /root /home/xiaye -maxdepth 4 -name 'auth.json*' -not -path '*/.git/*' 2>/dev/null | head
echo '=== grep litellm.yaml copies in tar ==='
for t in /root/ai-company/backups/*.tar.gz; do
  [ -f "$t" ] || continue
  tar xzf "$t" -O 2>/dev/null | grep -lE 'api_key' >/dev/null 2>&1 && echo "$t contains something" 
done
echo '=== extract litellm.yaml from backup if present ==='
mkdir -p /tmp/keyrestore
for t in /root/ai-company/backups/*.tar.gz; do
  [ -f "$t" ] || continue
  tar tzf "$t" 2>/dev/null | grep -qE 'litellm\.ya?ml$|config/litellm' && {
    echo "found in $t:"
    tar tzf "$t" 2>/dev/null | grep -E 'litellm\.ya?ml$|config/litellm' | head -3
  }
done
