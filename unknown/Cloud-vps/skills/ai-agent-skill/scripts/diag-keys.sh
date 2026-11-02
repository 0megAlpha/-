#!/usr/bin/env bash
set -u
echo '=== openhands test file sk- usage (first 3 matches context) ==='
cd /root/openhands
git grep -n -E 'sk-[A-Za-z0-9]{30,}' HEAD -- frontend/__tests__/components/features/conversation/conversation-tabs.test.tsx 2>/dev/null | head -3
git grep -n -E 'sk-[A-Za-z0-9]{30,}' HEAD -- frontend/__tests__/hooks/query/use-batch-app-conversations.test.tsx 2>/dev/null | head -3

echo '=== opencode auth.json backups ==='
ls -la /root/.config/opencode/ 2>/dev/null | grep -E 'auth|bak'

echo '=== nvidia key in auth backups? (masked) ==='
for f in /root/.config/opencode/auth.json.bak-*; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -oE '"key"\s*:\s*"[A-Za-z0-9_-]{8,}"' "$f" 2>/dev/null | sed -E 's/(.{12}).*/\1.../'
  grep -c 'nvapi-' "$f" 2>/dev/null
done

echo '=== fleet.env provider keys (masked names only) ==='
grep -oE '^[A-Z_]+=' /root/ai-company/config/fleet.env 2>/dev/null

echo '=== litellm.yaml all model entries with key status ==='
grep -E 'model_name|api_key' /root/ai-company/config/litellm.yaml | grep -v '^#' | sed -E 's/(api_key:).*(.{4})$/\1 <present len=??>/' | head -20

echo '=== add-key.sh usage ==='
head -30 /root/ai-company/scripts/add-key.sh 2>/dev/null
