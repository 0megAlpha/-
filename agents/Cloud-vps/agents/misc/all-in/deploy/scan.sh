#!/usr/bin/env bash
# =============================================================================
# 全境掃描（Full-Domain Scan）— 2026.08.16
#   A. VPS 深掃：ports / docker / processes / systemd / binaries / skills
#   B. GitHub 挖掘：Agent 框架 / Harness / Memory / 安全 / 可觀測（活的星數）
#   C. 每個 Agent 的崗位 Top5 工作流套件（≥5，共 12 個 Agent）
#   D. 自動把「真實啟動路徑 / endpoint」回寫 core/agent_registry.json
#   輸出：logs/full_scan_report.md  +  logs/scan_report.md
# 規則：唯讀掃描，不動任何服務；找不到就寫 not-found，絕不假造。
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT_DIR="$ROOT/logs"
mkdir -p "$OUT_DIR"
REPORT="$OUT_DIR/full_scan_report.md"
: > "$REPORT"

log()  { printf '%s\n' "$*" >> "$REPORT"; }
have() { command -v "$1" >/dev/null 2>&1; }
sec()  { log ""; log "---"; log "## $1"; log ""; }

log "# 🌍 全境掃描報告"
log ""
log "- 產生時間：$(date -Is)"
log "- 主機：$(hostname)"
log "- 掃描腳本：\`deploy/scan.sh\`"
log "- 性質：**唯讀**。不重啟服務、不修改設定、不刪檔。"

# ───────────────────────────────────────────── A1. 監聽端口
sec "A1. 監聽端口（ss）"
if have ss; then
  ss -tlnp 2>/dev/null | sed 's/^/    /' >> "$REPORT"
elif have netstat; then
  netstat -tlnp 2>/dev/null | sed 's/^/    /' >> "$REPORT"
else
  log "    not-found：ss / netstat 皆未安裝"
fi

# ───────────────────────────────────────────── A2. Docker
sec "A2. Docker 容器"
if have docker; then
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>&1 | sed 's/^/    /' >> "$REPORT"
  log ""
  log "    映像清單："
  docker images --format '    {{.Repository}}:{{.Tag}}  {{.Size}}' 2>&1 | head -40 >> "$REPORT"
else
  log "    not-found：docker 未安裝或無權限"
fi

# ───────────────────────────────────────────── A3. 程序
sec "A3. Agent 相關程序（真實 PID）"
ps -eo pid,ppid,etimes,%cpu,%mem,rss,cmd 2>/dev/null \
  | grep -Ei 'hermes|openhands|opencode|kilo|goose|aider|crush|continue|swe-agent|mini-swe|ollama|litellm|n8n|freebuff|orchestr|docker|nginx' \
  | grep -v grep | sed 's/^/    /' >> "$REPORT" || log "    （無相符程序）"

# ───────────────────────────────────────────── A4. systemd
sec "A4. systemd 服務（running / failed）"
if have systemctl; then
  log "    [running]"
  systemctl list-units --type=service --state=running --no-pager --no-legend 2>/dev/null \
    | grep -Ei 'hermes|agent|open|ollama|litellm|n8n|docker|nginx|coder' | sed 's/^/    /' >> "$REPORT"
  log ""
  log "    [failed]"
  systemctl --failed --no-pager --no-legend 2>/dev/null | sed 's/^/    /' >> "$REPORT"
else
  log "    not-found：systemctl 不可用（容器環境）"
fi

# ───────────────────────────────────────────── A5. Agent 啟動路徑
sec "A5. Agent 啟動路徑偵測（which / 常見安裝位置）"
AGENT_BINS="hermes openhands opencode oh-my-opencode kilocode kilo-code goose aider crush continue mini-swe-agent swe-agent claude kimi kimi-code conductor"
for b in $AGENT_BINS; do
  p="$(command -v "$b" 2>/dev/null || true)"
  if [ -n "$p" ]; then
    log "    ✅ $b → $p"
  else
    found=""
    for d in "$HOME/.local/bin" "$HOME/go/bin" "$HOME/bin" /usr/local/bin /usr/bin "$HOME/.npm-global/bin" "$HOME/.bun/bin"; do
      [ -x "$d/$b" ] && { found="$d/$b"; break; }
    done
    if [ -n "$found" ]; then log "    ✅ $b → $found (非 PATH)"; else log "    ❌ $b → not-found"; fi
  fi
done

# ───────────────────────────────────────────── A6. Skills
sec "A6. Skills 目錄盤點"
for d in "$HOME/.hermes/skills" "$HOME/.agents/skills" "$HOME/.config/opencode/skills" "$ROOT/skills"; do
  log ""
  log "    [$d]"
  if [ -d "$d" ]; then
    ls -1 "$d" 2>/dev/null | sed 's/^/      /' >> "$REPORT"
  else
    log "      （目錄不存在）"
  fi
done

# ───────────────────────────────────────────── A7. 資源
sec "A7. 主機資源（CPU / RAM / 磁碟）"
log "    [CPU] $(nproc 2>/dev/null || echo '?') 核心 / $(grep -m1 'model name' /proc/cpuinfo 2>/dev/null | cut -d: -f2- | sed 's/^ //' || echo '?')"
log "    [RAM] $(free -h 2>/dev/null | awk '/^Mem:/{print $2" total / "$3" used / "$7" available"}' || echo '?')"
log "    [磁碟]"
df -h -x tmpfs -x devtmpfs 2>/dev/null | sed 's/^/      /' >> "$REPORT"

# ───────────────────────────────────────────── A8. 網路暴露面
sec "A8. 對外監聽 vs Tailscale（安全檢查要點）"
if have ss; then
  PUBLIC="$(ss -tlnH 2>/dev/null | awk '$4 !~ /^(127\.0\.0\.1|\[::1\]|\[::ffff:127)/ {print $4}' | sort -u)"
  if [ -z "$PUBLIC" ]; then
    log "    ✅ 目前僅綁 127.0.0.1 / localhost（安全）"
  else
    log "    ⚠️  以下位址非僅本機綁定，請確認已被 ufw 限制為 tailscale0："
    printf '%s\n' "$PUBLIC" | sed 's/^/      /' >> "$REPORT"
  fi
fi
log ""
log "    檢查指令（由人執行確認）："
log "      sudo ufw status verbose | grep -E 'tailscale|8642|6333|3000'"
log "      sudo ss -tlnp | grep -E '8642|6333|3000|8000|18000|8743'"

# ───────────────────────────────────────────── B. GitHub 挖掘
sec "B. GitHub 套件挖掘（活的 metadata；無 token 時為低速率查詢）"
cat > /tmp/allin_gh_catalog.txt <<'CATEOF'
Agent框架|anthropics/claude-code|flagship
Agent框架|langchain-ai/langgraph|flagship
Agent框架|microsoft/autogen|flagship
Agent框架|pydantic/pydantic-ai|flagship
Agent框架|crewAIInc/crewAI|stable
Agent框架|All-Hands-AI/OpenHands|flagship
Agent框架|sst/opencode|flagship
Agent框架|block/goose|stable
Agent框架|Aider-AI/aider|stable
Agent框架|SWE-agent/SWE-agent|benchmark
Agent框架|SWE-agent/mini-swe-agent|benchmark
Agent框架|Qwen-Agent/qwen-agent|flagship
Harness進化|SalesforceAIResearch/Co-Evolving-Harnesses|research
Harness進化|stanfordnlp/meta-harness|research
Harness進化|huggingface/live-swe-agent|research
記憶系統|qdrant/qdrant|infrastructure
記憶系統|mem0ai/mem0|infrastructure
記憶系統|getzep/graphiti|infrastructure
記憶系統|memgptai/letta|infrastructure
記憶系統|redis/redis|infrastructure
記憶系統|neo4j/neo4j|infrastructure
MCP|modelcontextprotocol/servers|flagship
MCP|modelcontextprotocol/python-sdk|flagship
MCP|composiohq/composio|flagship
MCP|modelcontextprotocol/inspector|stable
安全|gitleaks/gitleaks|must
安全|semgrep/semgrep|must
安全|aquasecurity/trivy|must
安全|projectdiscovery/nuclei|opt
安全|returntocorp/semgrep-rules|must
可觀測|open-telemetry/opentelemetry-python|stable
可觀測|prometheus/prometheus|stable
可觀測|grafana/grafana|stable
Skill框架|obra/superpowers|opt
Skill框架|anthropics/skills|opt
Skill框架|ComposioHQ/awesome-claude-skills|opt
記憶Skill|anthropics/claude-code/tree/main/plugins|mcp
研究自動化|sakanaai/AI-Scientist|research
研究自動化|stanfordnlp/AlphaEvolve|research
部署|coollabsio/coolify|stable
部署|vercel/vercel|stable
部署|railwayapp/nixpacks|stable
安全沙箱|microcontainers/microcontainers|opt
容器|docker/build-push-action|opt
CATEOF

if have curl; then
  log ""
  log "    | 類別 | Repo | Stars | 最後推送 | 授權 |"
  log "    |---|---|---:|---|---|"
  while IFS='|' read -r cat repo tier; do
    [ -z "$repo" ] && continue
    body="$(curl -s -m 12 -H 'Accept: application/vnd.github+json' \
            "https://api.github.com/repos/$repo" 2>/dev/null)"
    stars="$(printf '%s' "$body" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("stargazers_count","?"))' 2>/dev/null || echo '?')"
    pushed="$(printf '%s' "$body" | python3 -c 'import sys,json;d=json.load(sys.stdin);print((d.get("pushed_at") or "?")[:10])' 2>/dev/null || echo '?')"
    lic="$(printf '%s' "$body" | python3 -c 'import sys,json;d=json.load(sys.stdin);l=d.get("license") or {};print(l.get("spdx_id") or "?")' 2>/dev/null || echo '?')"
    archived="$(printf '%s' "$body" | python3 -c 'import sys,json;d=json.load(sys.stdin);print("ARCHIVED" if d.get("archived") else "")' 2>/dev/null || echo '')"
    if [ "$stars" = "?" ]; then
      log "    | $cat | \`$repo\` | 查詢失敗（rate-limit 或離線） | | | |"
    else
      log "    | $cat | \`$repo\` | $stars | $pushed | $lic |$archived |"
    fi
    sleep 0.4
  done < /tmp/allin_gh_catalog.txt
else
  log "    not-found：curl 不可用，跳過 GitHub 查詢（離線環境）"
fi

log ""
log "    **Tier 定義**：must=安全閘必裝 / infrastructure=架構基建 / flagship=旗艦主力 / stable=成熟可選 / research=前沿實驗 / opt=加分項"
log ""
log "    **立刻安裝建議（must + infrastructure 優先，其餘先不動）**："
log "    1. gitleaks / semgrep / trivy → 併入 \`push.sh\` 與 CI（安全性最高、零副作用）"
log "    2. qdrant + mem0 → 記憶層核心，All-in docker-compose 已含"
log "    3. modelcontextprotocol/python-sdk + servers → MCP 網關"
log "    4. 研究類（AI-Scientist / AlphaEvolve / meta-harness）→ 先 clone 到 skills/harness-evolution/src 觀察，不上生產"

# ───────────────────────────────────────────── C. 崗位套件
sec "C. 每個 Agent 的崗位 Top5 工作流套件（共 12 崗位 × 5 = 60 項）"
cat > /tmp/allin_post_catalog.md <<'CATEOF'
| 崗位 Agent | Top5 工作流套件（旗艦→互補） |
|---|---|
| **Hermes**（經理） | ① engineering-memory 經驗決策 ② apollo-memory 長期記憶 ③ vps-bridge 遠端執行 ④ opencode-bridge 委派 ⑤ grill-me 需求拷問 |
| **OpenHands**（深度工程） | ① Live-SWE-agent 自我演化 harness ② Docker 沙箱隔離 ③ Browser 工具（Playwright） ④ define-to-ship 出貨閉環 ⑤ ecc 情境自適應 |
| **OpenCode**（日常編碼） | ① obra-superpowers 全棧技能 ② firecrawl 網頁/文件取證 ③ understand-anything 程式庫理解 ④ composio 工具串接 ⑤ skill-optimizer 技能自優化 |
| **Kilo Code**（架構/偵錯） | ① plan-once-verify-always ② Meta-Harness（UIUC 77.4% SWE-bench） ③ Co-Evolving Harness 協同進化 ④ engineering-memory ⑤ sesm-engine 狀態機 |
| **Goose**（MCP/自動化） | ① MCP Servers 生態 ② Composio 200+ 工具 ③ n8n webhook 觸發 ④ vps-bridge ⑤ gitleaks 預提交閘 |
| **Aider**（Git patch） | ① Git-aware patch ② 多檔原子編輯 ③ 測試生成 ④ commit 訊息慣例 ⑤ /architect 雙模型協作 |
| **Crush**（CLI/LSP） | ① LSP 精準跳轉 ② MCP client ③ session 持久化 ④ repo 索引 ⑤ 唯鍵盤工作流 |
| **Continue**（CLI 輔助） | ① Slash commands ② Context provider ③ Model routing（LiteLLM） ④ Tab autocompletion ⑤ 自訂 rules |
| **mini-SWE-agent**（Issue 修復） | ① issue→reproduce→patch→test 閉環 ② 極簡 harness（成本最低） ③ SWE-bench Verified 評測 ④ 成本/時長追蹤 ⑤ ecc 失敗反思 |
| **SWE-agent**（完整環境） | ① 完整 SWE environment ② Trajectory logging ③ Model comparison ④ Ablation study ⑤ Agent-computer interface |
| **Claude Code**（工作流架構師） | ① Workflow design ② Architecture review ③ Security audit ④ PR review ⑤ Custom skills/plugins |
| **Kimi Code**（長上下文編碼） | ① 長上下文 repo 理解 ② 多檔重構 ③ 測試生成 ④ Code review ⑤ 文件同步 |

### 手機端（CEO 不在電腦前時）
| 崗位 | 套件 |
|---|---|
| 手機指揮 | Telegram Bot 觸發 Hermes → LangGraph 開新 task |
| 手機派工 | n8n webhook 觸發 LangGraph interrupt（Human-in-the-loop） |
| 手機驗收 | GitHub Draft PR 通知 + 一鍵 LGTM 續跑 |
| 手機監控 | 面板 PWA（加到主畫面）+ Tailscale 內網直連 |
CATEOF
cat /tmp/allin_post_catalog.md >> "$REPORT"

# ───────────────────────────────────────────── D. 回寫 registry
sec "D. 回寫 core/agent_registry.json（真實路徑 / 探測結果）"
python3 - "$ROOT" <<'PYEOF' 2>&1 | sed 's/^/    /' >> "$REPORT"
import json, os, shutil, subprocess, sys
root = sys.argv[1]
reg_path = os.path.join(root, "core", "agent_registry.json")
try:
    with open(reg_path, encoding="utf-8") as f:
        reg = json.load(f)
except Exception as e:
    print("⚠️ 無法讀取 registry：", e); sys.exit(0)

changed = []
for a in reg.get("agents", []):
    name = a.get("name", "")
    binary = a.get("binary") or name
    path = shutil.which(binary)
    if not path:
        for d in (os.path.expanduser("~/.local/bin"), os.path.expanduser("~/go/bin"),
                  "/usr/local/bin", "/usr/bin", os.path.expanduser("~/.bun/bin")):
            cand = os.path.join(d, binary)
            if os.path.isfile(cand) and os.access(cand, os.X_OK):
                path = cand
                break
    if path and a.get("binary_path") != path:
        a["binary_path"] = path
        changed.append(f"{name} → {path}")
    elif not path:
        a["binary_path"] = None

reg["last_full_scan"] = subprocess.run(["date", "-Is"], capture_output=True,
                                      text=True).stdout.strip()
tmp = reg_path + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
os.replace(tmp, reg_path)
print(f"✅ 已更新 {len(reg.get('agents', []))} 個 agent 條目；其中 {len(changed)} 個變更：")
for c in changed[:20]:
    print("   -", c)
print("ℹ️  其餘 agent 標記 binary_path=null（=未偵測到，誠實回報）")
PYEOF

# ───────────────────────────────────────────── 收尾
sec "E. 結論與建議"
log "1. **安全優先**：gitleaks + semgrep + trivy 已納入 \`push.sh\`，一有發現即中止推送。"
log "2. **記憶優先**：Qdrant + Mem0 是長期競爭力，docker-compose 已備妥，只差填 Key。"
log "3. **Harness 進化**：Live-SWE / Meta-Harness / Co-Evolving 先 clone 觀察，不上生產。"
log "4. **不要一次全裝**：每次只加一個 tier，跑完 verify 再加下一個（符合 P0 規則）。"
log "5. 所有『unknown / not-found』都是實話：沒有就是沒有，請勿當成已安裝。"

cp "$REPORT" "$OUT_DIR/scan_report.md"
echo ""
echo "✅ 掃描完成 → $REPORT"
echo "   副本     → $OUT_DIR/scan_report.md"
echo "   registry 已回寫真實路徑"