#!/usr/bin/env bash
# 拉最新上游 -> 套用本地 patches -> 不相容就回退 pinned 並回報
set -o pipefail
export GIT_TERMINAL_PROMPT=0
ROOT=$(cd "$(dirname "$0")/.." && pwd); WORK=${WORK:-/opt/upstreams}; mkdir -p "$WORK"
G=(git -c user.name=unify -c user.email=unify@localhost)
avail=$(df -BG --output=avail "$WORK" | tail -1 | tr -dc 0-9)
[ "${avail:-0}" -lt 10 ] && { echo "磁碟剩 ${avail}G，略過同步"; exit 0; }
while IFS=$'\t' read -r name url branch pinned cls; do
  [[ -z "$name" || "$name" == \#* ]] && continue
  d="$WORK/$name"
  if [ -z "$branch" ] || [ "$branch" = HEAD ]; then
    branch=$(timeout 60 git ls-remote --symref "$url" HEAD 2>/dev/null | awk '/^ref:/{sub("refs/heads/","",$2);print $2;exit}')
    [ -z "$branch" ] && { echo "[SKIP] $name 連不到上游(私有或帳號停用)"; continue; }
  fi
  [ -d "$d/.git" ] || timeout 600 "${G[@]}" clone -q --depth 50 -b "$branch" "$url" "$d" || { echo "[FAIL clone] $name"; continue; }
  timeout 300 "${G[@]}" -C "$d" fetch -q --depth 50 origin "$branch" || { echo "[FAIL fetch] $name"; continue; }
  timeout 120 "${G[@]}" -C "$d" fetch -q --depth 1 origin "$pinned" 2>/dev/null
  old=$("${G[@]}" -C "$d" rev-parse --short HEAD)
  "${G[@]}" -C "$d" checkout -q -f -B unify "origin/$branch"
  ok=1
  if ls "$ROOT/patches/$name"/0*.patch >/dev/null 2>&1; then
    "${G[@]}" -C "$d" am --3way "$ROOT"/patches/"$name"/0*.patch >/dev/null 2>&1 || { "${G[@]}" -C "$d" am --abort 2>/dev/null; ok=0; }
  fi
  if [ $ok = 1 ] && [ -f "$ROOT/patches/$name/dirty.diff" ]; then
    "${G[@]}" -C "$d" apply --3way "$ROOT/patches/$name/dirty.diff" >/dev/null 2>&1 || ok=0
  fi
  [ $ok = 1 ] && [ -f "$d/requirements.txt" ] && { python3 -m pip install --dry-run -q -r "$d/requirements.txt" >/dev/null 2>&1 || echo "[DEPS WARN] $name requirements 有衝突"; }
  if [ $ok = 0 ]; then
    "${G[@]}" -C "$d" checkout -q -f -B unify "$pinned" 2>/dev/null
    echo "[CONFLICT] $name 與最新上游不相容，已回退 $pinned，請檢查 patches/$name"
  else
    echo "[OK] $name $old -> $("${G[@]}" -C "$d" rev-parse --short HEAD)"
  fi
done < "$ROOT/upstreams.tsv"
