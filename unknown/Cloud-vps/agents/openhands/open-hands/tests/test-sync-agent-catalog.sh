#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
SOURCE_SCRIPT="$ROOT/scripts/sync-agent-catalog.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

REPO="$TMP/open-hands"
mkdir -p "$REPO/.agents/skills" "$REPO/extensions/plugins" "$REPO/scripts"
git -C "$REPO" init -q
cp "$SOURCE_SCRIPT" "$REPO/scripts/sync-agent-catalog.py"
chmod +x "$REPO/scripts/sync-agent-catalog.py"

mkdir -p "$REPO/.agents/skills/alpha" "$REPO/.agents/skills/beta"
mkdir -p "$REPO/extensions/plugins/p1" "$REPO/extensions/plugins/p2"

cat > "$REPO/.agents/skill-registry.json" <<'JSON'
{
  "schema_version": 1,
  "skills": ["alpha"],
  "plugins": ["p1", "ghost"]
}
JSON

if (cd "$REPO" && ./scripts/sync-agent-catalog.py); then
  echo "FAIL: expected drift detection failure" >&2
  exit 1
fi

(cd "$REPO" && ./scripts/sync-agent-catalog.py --apply >/dev/null)

python - <<'PY' "$REPO/.agents/skill-registry.json"
import json
import sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
assert data["skills"] == ["alpha", "beta"], data["skills"]
assert data["plugins"] == ["p1", "p2"], data["plugins"]
print("PASS: repaired registry lists")
PY
