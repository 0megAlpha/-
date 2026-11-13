#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${OPENHANDS_TOOLS_DIR:-/opt/workspace_base/.openhands/tools}"
export HOME="${HOME:-$TARGET_DIR/home}"
export NPM_CONFIG_CACHE="${NPM_CONFIG_CACHE:-$TARGET_DIR/.npm-cache}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$TARGET_DIR/.pip-cache}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$TARGET_DIR/.cache}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$TARGET_DIR/ms-playwright}"
mkdir -p "$TARGET_DIR" "$HOME" "$NPM_CONFIG_CACHE" "$PIP_CACHE_DIR" "$XDG_CACHE_HOME" "$PLAYWRIGHT_BROWSERS_PATH" "$TARGET_DIR/bin" "$TARGET_DIR/.semgrep"
cp "$SCRIPT_DIR/package.json" "$TARGET_DIR/package.json"
cp "$SCRIPT_DIR/package-lock.json" "$TARGET_DIR/package-lock.json"
cp "$SCRIPT_DIR/playwright.config.mjs" "$TARGET_DIR/playwright.config.mjs"
mkdir -p "$TARGET_DIR/tests"
cp "$SCRIPT_DIR/tests/openhands-health.spec.mjs" "$TARGET_DIR/tests/openhands-health.spec.mjs"
cd "$TARGET_DIR"
npm ci --no-audit --no-fund
if [ ! -x "$TARGET_DIR/semgrep-venv/bin/semgrep" ]; then
  python3 -m venv "$TARGET_DIR/semgrep-venv"
fi
"$TARGET_DIR/semgrep-venv/bin/pip" install --upgrade pip semgrep
"$TARGET_DIR/node_modules/.bin/playwright" install chromium
if [ -n "${TRIVY_BIN:-}" ] && [ -x "$TRIVY_BIN" ]; then
  install -m 0755 "$TRIVY_BIN" "$TARGET_DIR/bin/trivy"
elif command -v trivy >/dev/null 2>&1; then
  install -m 0755 "$(command -v trivy)" "$TARGET_DIR/bin/trivy"
else
  echo "Trivy binary not found; install Trivy using the official package for this OS." >&2
fi
printf 'Installed OpenHands quality toolchain into %s\n' "$TARGET_DIR"
