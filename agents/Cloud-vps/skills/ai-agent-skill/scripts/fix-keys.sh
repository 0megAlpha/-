#!/usr/bin/env bash
set -u
echo '=== 1) openhands override gitignore ==='
cd /root/openhands
if git check-ignore docker-compose.override.yml >/dev/null 2>&1; then
  echo 'already ignored'
else
  grep -q 'docker-compose.override.yml' .gitignore 2>/dev/null || echo 'docker-compose.override.yml' >> .gitignore
  echo 'added to .gitignore:'
  tail -3 .gitignore
  git check-ignore docker-compose.override.yml && echo 'OK: now ignored'
fi

echo '=== 2) scan committed secrets in openhands (tracked files only) ==='
git grep -lE 'sk-[A-Za-z0-9]{30,}|nvapi-|github_pat_|gsk_[A-Za-z0-9]{30,}' HEAD -- 2>/dev/null | head -5 || echo 'none found'

echo '=== 3) openhands tracked files containing LLM_API_KEY ==='
git grep -lE 'LLM_API_KEY|LLM_BASE_URL|LITELLM' HEAD -- 2>/dev/null | head -5 || echo 'none'

echo '=== 4) clean ai-company remote token ==='
cd /root/ai-company
git remote get-url origin | sed -E 's#https://[^@]+@#https://#' | tee /tmp/new-remote-url.txt
NEWURL=$(cat /tmp/new-remote-url.txt)
if [ "$NEWURL" != "$(git remote get-url origin)" ]; then
  git remote set-url origin "$NEWURL"
  echo 'remote cleaned:'
  git remote -v
else
  echo 'no token embedded, unchanged'
fi

echo '=== 5) litellm chat with CORRECT master key (value after =) ==='
MKFILE=/root/ai-company/config/litellm-master-key.env
MK=$(grep -m1 '^MASTER_KEY=' "$MKFILE" | cut -d= -f2-)
if [ -z "$MK" ]; then MK=$(grep -v '^#' "$MKFILE" | head -1); fi
echo "key length: ${#MK}"
curl -s --max-time 30 -H "Authorization: Bearer $MK" -H 'Content-Type: application/json' \
  -d '{"model":"glm-5.2","messages":[{"role":"user","content":"ping"}],"max_tokens":8}' \
  http://127.0.0.1:4000/v1/chat/completions \
  | head -c 500
echo ''
