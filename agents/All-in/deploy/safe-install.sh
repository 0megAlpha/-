#!/usr/bin/env bash
# Project-local skill installer. Never writes to global/shared Agent skill roots.
set -Eeuo pipefail
ROOT="${ALLIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    -h|--help)
      echo "Usage: bash deploy/safe-install.sh [--apply]"
      echo "Default is dry-run. --apply installs only missing skills into this All-in project's .openhands/skills."
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done
SOURCE="$ROOT/skills"
TARGET="$ROOT/.openhands/skills"
[[ -d "$SOURCE" ]] || { echo "ERROR: skills directory missing: $SOURCE" >&2; exit 1; }
count=0
while IFS= read -r -d '' src; do
  skill="$(basename "$(dirname "$src")")"
  dst="$TARGET/$skill/SKILL.md"
  [[ -s "$dst" ]] && continue
  count=$((count+1))
  if (( APPLY )); then
    mkdir -p "$(dirname "$dst")"
    install -m 0644 "$src" "$dst"
    echo "INSTALLED $dst"
  else
    echo "WOULD_INSTALL $dst"
  fi
done < <(find "$SOURCE" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -print0 | sort -z)
echo "Project skill definitions: $(find "$SOURCE" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | wc -l)"
echo "Missing project-local skills: $count"
if (( APPLY )); then echo "PASS: only missing All-in-local skill files were added."
else echo "DRY_RUN_ONLY: no files changed; pass --apply to install missing local skills."
fi
