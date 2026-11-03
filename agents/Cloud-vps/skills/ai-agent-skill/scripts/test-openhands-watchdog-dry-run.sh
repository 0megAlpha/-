#!/usr/bin/env bash
set -euo pipefail

SOURCE="${1:-/usr/local/bin/openhands-watchdog.sh}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
CALLS="$TMP/calls"
: > "$CALLS"

# Run a disposable copy so the pre-fix behavior can be tested without touching
# the real watchdog log or invoking real service-management commands.
sed "s|^LOGFILE=.*|LOGFILE=\"$TMP/watchdog.log\"|" "$SOURCE" > "$TMP/watchdog.sh"
chmod +x "$TMP/watchdog.sh"

cat > "$TMP/bin/docker" <<'STUB'
#!/usr/bin/env bash
printf 'docker %s\n' "$*" >> "$CALLS"
exit 0
STUB
cat > "$TMP/bin/systemctl" <<'STUB'
#!/usr/bin/env bash
printf 'systemctl %s\n' "$*" >> "$CALLS"
if [[ "${1:-}" == "is-active" ]]; then exit 1; fi
exit 0
STUB
cat > "$TMP/bin/tailscale" <<'STUB'
#!/usr/bin/env bash
printf 'tailscale %s\n' "$*" >> "$CALLS"
if [[ "${1:-}" == "serve" && "${2:-}" == "status" ]]; then
  printf 'No serve config\n'
fi
exit 0
STUB
cat > "$TMP/bin/hermes" <<'STUB'
#!/usr/bin/env bash
printf 'hermes %s\n' "$*" >> "$CALLS"
exit 0
STUB
chmod +x "$TMP/bin/"*

export CALLS PATH="$TMP/bin:$PATH"
set +e
"$TMP/watchdog.sh" --dry-run > "$TMP/output.txt" 2>&1
RC=$?
set -e

if (( RC != 0 )); then
  echo "FAIL: --dry-run exited $RC"
  cat "$TMP/output.txt"
  exit 1
fi
if grep -Eq '^(docker start|systemctl restart|tailscale serve --bg)' "$CALLS"; then
  echo "FAIL: dry-run executed a mutating command"
  cat "$CALLS"
  exit 1
fi
if [[ -e "$TMP/watchdog.log" ]]; then
  echo "FAIL: dry-run wrote the watchdog log"
  exit 1
fi
if ! grep -q '\[DRY-RUN\]' "$TMP/output.txt"; then
  echo "FAIL: dry-run did not describe planned actions"
  cat "$TMP/output.txt"
  exit 1
fi

echo "PASS: dry-run reports recovery actions without invoking them or writing logs"
