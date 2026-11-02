#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

overlay_files=(
  "$repo_root/overlays/private/runtime-overrides.env"
  "$repo_root/overlays/private/runtime-overrides.local.env"
)

for overlay in "${overlay_files[@]}"; do
  if [ -f "$overlay" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$overlay"
    set +a
  fi
done
