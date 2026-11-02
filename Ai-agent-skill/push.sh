#!/usr/bin/env bash
# =============================================================================
# Ai-agent-skill 去敏推送（安全閘版）
#
# 🔧 已修復 P0 bug：舊版是 `cd "$(dirname "$0")/.."`。本檔位於**倉庫根目錄**，
#    那行會跳到「上一層目錄」（家目錄 /home/xiaye），接著 `git add -A` 會把
#    整個 home（含 .ssh、其他專案、6.1G 大檔）全部納入版控。
#    現在改成 cd 到腳本所在目錄，並加上多重保險。
#
# 閘門：git 追蹤檢查 → gitleaks/key_manager → semgrep → trivy
# 任一閘門發現問題 → 輸出 logs/security_report.md 並中止。
# 絕不 --force。
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# ── 保險 1：必須落在「看起來像本倉庫」的目錄 ──
case "$HERE" in
  */Ai-agent-skill) cd "$HERE" ;;
  *)
    echo "❌ 腳本不在 Ai-agent-skill 目錄內（目前：$HERE），拒絕執行以免掃錯目錄。"
    exit 1
    ;;
esac

MSG="${1:-feat: Ai-agent-skill 更新}"
REPORT="logs/security_report.md"
mkdir -p logs
: > "$REPORT"
FAILED=""
hr()  { printf '\n## %s\n\n' "$1" >> "$REPORT"; }
note() { printf -- '- %s\n' "$1" >> "$REPORT"; }

# ── 保險 2：必須真的有 Ai-agent-skill 的標誌檔 ──
if [ ! -d "fleet" ] && [ ! -d "skills" ] && [ ! -f "AGENTS.md" ]; then
  echo "❌ $HERE 不像 Ai-agent-skill 倉庫根目錄，拒絕執行。"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -q && git branch -M main
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ 未設定 origin。請執行："
  echo "   git remote add origin https://github.com/xh09411-web/Ai-agent-skill.git"
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"

hr "推送前安全閘報告"
note "時間：$(date -Is)"
note "訊息：$MSG"
note "目錄：$HERE"
note "分支：$BRANCH"

# ─────────────────────────── 閘門 1：敏感檔 ───────────────────────────
hr "閘門 1：敏感檔 git 追蹤檢查"
TRACKED="$(git ls-files | grep -Ei '(^|/)\.env($|\.)|\.(pem|key|p12|pfx)$|id_(rsa|ed25519)$|credentials(\.yaml|\.json)?$|\.npmrc$|\.netrc$' || true)"
if [ -n "$TRACKED" ]; then
  printf '%s\n' "$TRACKED" | sed 's/^/    ⚠️ /' >> "$REPORT"
  FAILED="${FAILED:+$FAILED | }閘門1：敏感檔已被 git 追蹤"
  echo "  ✗ 敏感檔已被 git 追蹤"
else
  note "✅ 無敏感檔被 git 追蹤"
  echo "  ✓ 敏感檔檢查通過"
fi

# ─────────────────────────── 閘門 2：密鑰 ───────────────────────────
hr "閘門 2：gitleaks / key_manager（密鑰偵測）"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks detect --no-git --redact -v >/tmp/aask_gitleaks.log 2>&1; then
    note "✅ gitleaks：無密鑰"
    echo "  ✓ gitleaks 通過"
  else
    tail -40 /tmp/aask_gitleaks.log | sed 's/^/    /' >> "$REPORT"
    FAILED="${FAILED:+$FAILED | }閘門2：gitleaks 偵測到疑似密鑰"
    echo "  ✗ gitleaks 發現疑似密鑰"
  fi
elif [ -f "$HOME/All-in/core/security/key_manager.py" ]; then
  if python3 "$HOME/All-in/core/security/key_manager.py" scan . >> "$REPORT" 2>&1; then
    note "✅ key_manager 兜底掃描通過"
    echo "  ✓ key_manager 兜底掃描通過"
  else
    FAILED="${FAILED:+$FAILED | }閘門2：key_manager 發現疑似密鑰"
    echo "  ✗ key_manager 發現疑似密鑰"
  fi
else
  note "⚠️ gitleaks 與 key_manager.py 皆不可用 → **本閘門未執行**（非通過）。請人工檢查 diff。"
  echo "  ⚠️ 密鑰掃描未執行（gitleaks / key_manager 皆不可用）"
fi

# ─────────────────────────── 閘門 3：semgrep ───────────────────────────
hr "閘門 3：semgrep（靜態分析）"
if command -v semgrep >/dev/null 2>&1; then
  if semgrep scan --config=p/python --config=p/security-audit \
        --severity=ERROR --error --quiet --exclude='.git' \
        --exclude='logs' --exclude='node_modules' . >/tmp/aask_semgrep.log 2>&1; then
    note "✅ semgrep：無 ERROR 級問題"
    echo "  ✓ semgrep 通過"
  else
    grep -E 'ERROR|error:' /tmp/aask_semgrep.log | head -30 | sed 's/^/    /' >> "$REPORT"
    FAILED="${FAILED:+$FAILED | }閘門3：semgrep 發現 ERROR 級問題"
    echo "  ✗ semgrep 發現 ERROR 級問題"
  fi
else
  note "⚠️ semgrep 未安裝 → **本閘門未執行**（非通過）。安裝：pipx install semgrep"
fi

# ─────────────────────────── 閘門 4：trivy ───────────────────────────
hr "閘門 4：trivy（漏洞掃描）"
if command -v trivy >/dev/null 2>&1; then
  if trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL \
        --exit-code 1 --no-progress --quiet --skip-dirs .git \
        --skip-dirs node_modules --ignore-unfixed . >/tmp/aask_trivy.log 2>&1; then
    note "✅ trivy：無 HIGH/CRITICAL 未修復漏洞"
    echo "  ✓ trivy 通過"
  else
    grep -Ei 'HIGH|CRITICAL|Total:' /tmp/aask_trivy.log | head -30 | sed 's/^/    /' >> "$REPORT"
    FAILED="${FAILED:+$FAILED | }閘門4：trivy 發現 HIGH/CRITICAL 漏洞"
    echo "  ✗ trivy 發現 HIGH/CRITICAL 漏洞"
  fi
else
  note "⚠️ trivy 未安裝 → **本閘門未執行**（非通過）"
fi

# ─────────────────────────── 閘門 5：大檔 ───────────────────────────
hr "閘門 5：大檔防護（>100MB 不進 git）"
BIG="$(git ls-files -z 2>/dev/null | tr '\0' '\n' | while read -r f; do
         [ -f "$f" ] && [ "$(stat -c%s "$f" 2>/dev/null || echo 0)" -gt 104857600 ] && echo "$f"
       done | head -20)"
if [ -n "$BIG" ]; then
  printf '%s\n' "$BIG" | sed 's/^/    ⚠️ /' >> "$REPORT"
  FAILED="${FAILED:+$FAILED | }閘門5：>100MB 大檔已被 git 追蹤"
  echo "  ✗ 發現 >100MB 大檔被追蹤"
else
  note "✅ 無 >100MB 大檔被追蹤"
  echo "  ✓ 大檔檢查通過"
fi

hr "結論"
if [ -n "$FAILED" ]; then
  echo "❌ 安全閘未通過 → **中止推送**"
  printf -- '- ❌ %s\n' "$FAILED" >> "$REPORT"
  printf -- '\n完整報告：`%s`\n' "$REPORT" >> "$REPORT"
  echo "   完整報告：$REPORT"
  exit 1
fi

printf -- '- ✅ 安全閘通過（未安裝的工具已明確標記為「未執行」，非「通過」）\n' >> "$REPORT"
printf -- '\n完整報告：`%s`\n' "$REPORT" >> "$REPORT"
echo "  ✓ 安全閘通過，報告：$REPORT"

git add -A
git commit -q -m "$MSG" || echo "（無新變更）"
if ! git push -u origin "$BRANCH"; then
  echo "❌ 推送被拒（可能非 fast-forward）。請先：git pull --rebase origin $BRANCH"
  echo "   依 P0 規則，本腳本絕不使用 --force。"
  exit 1
fi
echo "✅ 推送完成，commit hash：$(git rev-parse HEAD)"
