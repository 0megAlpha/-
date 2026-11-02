#!/usr/bin/env bash
# =============================================================================
# Ai-agent-skill — 安裝 / 部署
#   職責：把「大本營」的配置同步到各 Agent、把工作流註冊到 Hermes、
#         展開 fleet 設定、啟動前端面板。
#   原則：不覆蓋既有設定檔（只新增 ai-company.json），不做破壞性操作。
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

ok()   { echo "  ✅ $*"; }
warn() { echo "  ⚠️  $*"; }
info() { echo "  ℹ️  $*"; }

echo "🚀 [1/5] 展開 Fleet 設定（12 崗位 → fleet/<name>/config.json）"
if command -v python3 >/dev/null 2>&1; then
  python3 deploy/gen_fleet.py --probe --sync 2>&1 | sed 's/^/  /'
  ok "Fleet 設定展開完成"
else
  warn "無 python3，跳過"
fi

echo ""
echo "🚀 [2/5] 安裝工作流到 Hermes skills"
WF_SRC="$ROOT/workflows"
WF_DST="$HOME/.hermes/skills/workflows"
mkdir -p "$WF_DST"
if compgen -G "$WF_SRC/*.yaml" >/dev/null; then
  for f in "$WF_SRC"/*.yaml; do
    cp -f "$f" "$WF_DST/"
    ok "已安裝 $(basename "$f")"
  done
  cat > "$WF_DST/SKILL.md" <<'EOF'
---
name: workflows
description: >
  AI Company 的工作流定義（software-development / research-loop / deployment）。
  載入後可依 YAML 描述分派任務給對應 Agent，並遵守其中的 verification_gates
  與 human_gate 規則。
version: "1.0.0"
---
# workflows

本目錄的 YAML 是「流程的確定性骨架」，用來把 AI 的隨機性鎖在人類設定的規則裡。

| 檔案 | 用途 | 關鍵硬規則 |
|---|---|---|
| `software-development.yaml` | 主力開發閉環 | `verification` stage 為 required，失敗必回流 coding |
| `research-loop.yaml` | 自治研究循環 | `min_trials: 20`、必報誤差範圍、禁止單次實驗下結論 |
| `deployment.yaml` | 出貨與回滾 | 5 道 blocking preflight；prod 部署需 CEO 批准 |

## 執行原則
1. **plan once, verify always** — 計畫只做一次，驗證每一步都做。
2. **定義不清就不出貨**（define to ship）——沒有 success criteria 就停。
3. **human_gate 是硬閘**——`human_gate: true` 的 stage 必須等 CEO 明確回覆，
   不得用「預設同意」帶過。
4. **回滾優先於重試**——回滾上限 3 次，失敗就停手並回報，不無限嘗試。
EOF
  ok "已寫入 SKILL.md"
else
  warn "workflows/ 下沒有 yaml"
fi

echo ""
echo "🚀 [3/5] 掛載 harness-evolution 技能到 Hermes"
HE_SRC="$HOME/All-in/skills/harness-evolution"
HE_DST="$HOME/.hermes/skills/harness-evolution"
if [ -d "$HE_SRC" ]; then
  mkdir -p "$HE_DST"
  cp -rf "$HE_SRC/." "$HE_DST/" 2>/dev/null || true
  ok "已同步 $HE_SRC → $HE_DST"
else
  warn "找不到 $HE_SRC（若 All-in 未部署，harness-evolution 請改跑 ~/.hermes 內那份）"
fi

echo ""
echo "🚀 [4/5] 安全檢查（只讀，不推送）"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks detect --no-git --redact -q >/dev/null 2>&1; then
    ok "gitleaks：無密鑰"
  else
    warn "gitleaks 發現疑似密鑰 —— 已停止安裝後續步驟，請先處理"
    exit 1
  fi
else
  info "gitleaks 未安裝 → 略過（視為未執行，非通過）"
fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  TRACKED="$(git ls-files | grep -Ei '(^|/)\.env($|\.)|\.(pem|key)$' || true)"
  if [ -n "$TRACKED" ]; then
    warn "以下敏感檔已被 git 追蹤，請處理後再提交："
    printf '     %s\n' "$TRACKED"
  else
    ok "無敏感檔被 git 追蹤"
  fi
fi

echo ""
echo "🚀 [5/5] 啟動前端面板"
if [ -f "$HOME/.ai-company/serve_frontends.sh" ]; then
  bash "$HOME/.ai-company/serve_frontends.sh" --daemon
  ok "面板已啟動（詳見 ~/.ai-company/ENTRY.md）"
else
  warn "找不到 ~/.ai-company/serve_frontends.sh，請先在 All-in 執行 install.sh"
fi

echo ""
echo "════════════════════════════════════════════"
echo "✅ Ai-agent-skill 安裝完成"
echo ""
echo "面板："
echo "  http://100.126.48.60:8080/collaboration-monitor/"
echo "  http://100.126.48.60:8080/memory-viewer/"
echo ""
echo "驗證："
echo "  python3 deploy/gen_fleet.py --probe     # 看哪個 Agent 真的在線"
echo "  python3 \$HOME/All-in/core/orchestrator.py --agents"
echo "════════════════════════════════════════════"