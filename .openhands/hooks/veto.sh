#!/usr/bin/env bash
CMD=$(cat | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
for pat in "rm -rf /" "rm -rf ~" "mkfs" "dd if=" ":(){:|:&};:"; do
  echo "$CMD" | grep -qF "$pat" && { echo '{"decision":"deny","reason":"Blocked by veto."}'; exit 2; }
done
echo '{"decision":"allow"}'; exit 0
