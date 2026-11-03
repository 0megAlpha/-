#!/usr/bin/env bash
set -u
# 從 opencode auth.json 備份提取 nvidia key（不顯示明文）
NVKEY=$(python3 - <<'PY'
import json
d = json.load(open('/root/.local/share/opencode/auth.json.bak-1786181604'))
c = d.get('nvidia') or {}
k = c.get('key') or ''
print(k)
PY
)
if [ -z "$NVKEY" ] || [[ "$NVKEY" != nvapi-* ]]; then
  echo 'ERROR: nvidia key not found in backup'; exit 1
fi
echo "nvidia key recovered (len ${#NVKEY})"

CFG=/root/ai-company/config/litellm.yaml
cp "$CFG" "$CFG.bak-before-restore"

# 狀態機：只有 model_name 含 nvidia 或 glm 的 entry，其 api_key 空欄位才填入
python3 - "$CFG" "$NVKEY" <<'PY'
import sys
cfg, key = sys.argv[1], sys.argv[2]
out = []
cur_entry = ''
for line in open(cfg):
    s = line.strip()
    if s.startswith('- model_name:'):
        cur_entry = s.split('"')[1] if '"' in s else s
    if s.startswith('api_key:[REDACTED_BY_GATEKEEPER]""' in line and ('nvidia' in cur_entry or cur_entry.startswith('glm') or 'nvidia' in cur_entry):
        indent = line[:len(line) - len(line.lstrip())]
        out.append(f'{indent}api_key: [REDACTED_BY_GATEKEEPER]\n')
        continue
    out.append(line)
open(cfg, 'w').writelines(out)
print('patched api_key entries for nvidia/glm')
PY

echo '=== verify yaml parses ==='
python3 -c "import yaml; d=yaml.safe_load(open('$CFG')); print('entries:', len(d.get('model_list',[])))"

echo '=== restart litellm ==='
systemctl restart litellm.service
sleep 6
systemctl is-active litellm.service

echo '=== test glm-5.2 chat ==='
MK=$(grep -m1 '^MASTER_KEY=' /root/ai-company/config/litellm-master-key.env | cut -d= -f2-)
curl -s --max-time 40 -H "Authorization: Bearer $MK" -H 'Content-Type: application/json' \
  -d '{"model":"glm-5.2","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}' \
  http://127.0.0.1:4000/v1/chat/completions \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("reply:", (d.get("choices") or [{}])[0].get("message",{}).get("content","ERROR: "+str(d.get("error"))))' 2>/dev/null || echo CHAT_FAIL
