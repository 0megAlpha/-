#!/usr/bin/env bash
set -euo pipefail

test "$(systemctl is-active 9router.service)" = active
ss -lntp | grep -q '127.0.0.1:20128'
curl -fsS --max-time 5 http://127.0.0.1:20128/v1/models >/tmp/9router-models.json
python3 - <<'PY'
import json
d=json.load(open('/tmp/9router-models.json'))
ids={x.get('id') for x in d.get('data',[])}
assert 'groq/openai/gpt-oss-120b' in ids, 'Groq GPT-OSS 120B is not present in the catalog'
print('9ROUTER_HEALTH=PASS')
print('GROQ_GPT_OSS_120B_CATALOG=PASS')
print('MODEL_COUNT=', len(ids))
PY
rm -f /tmp/9router-models.json
