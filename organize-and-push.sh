#!/usr/bin/env bash
set -uo pipefail
ROOT="$HOME/oh-stack"
GH_REPO="${GH_REPO:-0megAlpha/-}"      # ← 改成你的真实 repo，- 是占位符
BRANCH="${BRANCH:-main}"
cd "$ROOT" || { echo "cd $ROOT 失败"; exit 1; }

# 1. 分类（未知 → misc）
classify() {
  case "$1" in
    code-review*|comment-cleanup|learn-from-code-review|qa-changes) echo code-review ;;
    github*|upstream-fork-sync|git-guardrails*) echo github ;;
    gitlab*) echo gitlab ;;
    bitbucket*) echo bitbucket ;;
    docker*|kubernetes*|ssh|ssh.md|uv|npm|vercel*|deno|deploy-to-vercel) echo devops ;;
    frontend-design|theme-factory|ui-ux-pro-max|web-design-guidelines|vercel-react*) echo frontend ;;
    research*|news-digest|evidence-based-citations|firecrawl*|sequential-thinking) echo research ;;
    technical-writing|plain-english-content|simplified-technical-english|prd|spec-driven-dev.md) echo writing ;;
    agent-*|setup-*|openhands-*|skill-creator|skill-optimizer|show-me|magic-word|add-*) echo agent-ops ;;
    notion|linear*|jira*|slack-*|discord|datadog|azure-devops|composio*) echo integrations ;;
    security*|ghost-goat|cochise|trinity|saml-forge|stripe-replay|race-condition|biometric|ja3-ja4|fingerprint|crack|zombie|refactor) echo security ;;
    jupyter|pdflatex*|pdf|pptx|mlops|supabase*|prisma*) echo data ;;
    swift-linux*|mobile|apple) echo mobile ;;
    *memory*|apollo-memory|engineering-memory|evolution-tree) echo memory ;;
    release-notes|release|upcoming-release|incident-retrospective) echo automation ;;
    superpowers|gstack|cc-suite|orchestrat*) echo orchestration ;;
    creative|social-media|email|smart-home) echo creative ;;
    *) echo misc ;;
  esac
}

# 2. 收集
declare -A SRC=()
for a in code-review github gitlab bitbucket devops frontend research writing agent-ops \
         integrations security data mobile memory automation orchestration creative misc; do SRC[$a]=""; done
for base in "$HOME/.openhands/skills" "$ROOT/.openhands/skills" "$ROOT/.agents/skills" "$ROOT/skills"; do
  [ -d "$base" ] || continue
  while IFS= read -r -d '' e; do
    n=$(basename "$e"); [ "$n" = ".git" ] && continue
    [ -L "$e" ] && [ ! -e "$e" ] && continue     # 断链跳过
    SRC[$(classify "$n")]+="$e"$'\n'
  done < <(find "$base" -mindepth 1 -maxdepth 1 -print0 2>/dev/null)
done

# 3. 生成（不备份；每次全新生成，幂等）
rm -rf "$ROOT/agents" "$ROOT/shared"
mkdir -p "$ROOT/agents" "$ROOT/shared"/{mcp-servers,hooks,litellm,memory}
[ -d "$ROOT/mcp-servers" ] && cp -a "$ROOT/mcp-servers/." "$ROOT/shared/mcp-servers/" 2>/dev/null || true
[ -d "$ROOT/.openhands/hooks" ] && cp -a "$ROOT/.openhands/hooks/." "$ROOT/shared/hooks/" 2>/dev/null || true

# ⚠️ 关键修复：litellm config 里实际 key → 占位符，否则 secret 扫描必挂
if [ -f "$ROOT/litellm/config.yaml" ]; then
  sed -E 's/(master_key:[[:space:]]*)"sk-[a-zA-Z0-9]+"/\1"${LITELLM_MASTER}"/' \
    "$ROOT/litellm/config.yaml" > "$ROOT/shared/litellm/config.yaml"
fi

for a in "${!SRC[@]}"; do
  [ -z "${SRC[$a]}" ] && continue
  adir="$ROOT/agents/$a"
  mkdir -p "$adir"/{skills,config,memory}
  while IFS= read -r s; do [ -z "$s" ] && continue; cp -a "$s" "$adir/skills/" 2>/dev/null || true; done <<< "${SRC[$a]}"

  python3 - "$a" "$adir" <<'PY'
import json, os, sys
agent, adir = sys.argv[1], sys.argv[2]
sd = os.path.join(adir, "skills")
skills = sorted(os.listdir(sd)) if os.path.isdir(sd) else []
json.dump({
  "agent": agent, "skills": skills, "entrypoint": "run.sh",
  "shared": {"mcp": "../../shared/mcp-servers", "hooks": "../../shared/hooks",
             "litellm": "../../shared/litellm/config.yaml", "memory": "../../shared/memory"},
  "collaboration": {"publishes": [f"{agent}.result"], "subscribes": ["shared.broadcast"]},
}, open(os.path.join(adir, "manifest.json"), "w"), indent=2, ensure_ascii=False)
PY

  # ⚠️ 关键修复：用 openhands web / serve 子命令，不再把 --skills-dir 当位置参数
  cat > "$adir/run.sh" <<RUN
#!/usr/bin/env bash
set -uo pipefail
DIR="\$(cd "\$(dirname "\$0")" && pwd)"
ROOT="\$(cd "\$DIR/../.." && pwd)"
export OPENHANDS_SKILLS_DIR="\$DIR/skills"
export OPENHANDS_MCP_CONFIG="\$DIR/config/mcp.json"
echo "[$a] skills=\$(ls "\$DIR/skills" | wc -l)  dir=\$OPENHANDS_SKILLS_DIR"
if command -v openhands >/dev/null 2>&1; then
  case "\${1:-web}" in
    web)   exec openhands web   --skills-dir "\$OPENHANDS_SKILLS_DIR" --mcp-config "\$OPENHANDS_MCP_CONFIG" ;;
    serve) exec openhands serve --skills-dir "\$OPENHANDS_SKILLS_DIR" ;;
    *) echo "用法: \$0 [web|serve]" ;;
  esac
else
  echo "OpenHands CLI 未装；在 Canvas → Settings → Skills 载入 \$OPENHANDS_SKILLS_DIR"
fi
RUN
  chmod +x "$adir/run.sh"
  echo '{"mcpServers":{}}' > "$adir/config/mcp.json"
  echo 'models: [deepseek-v4-flash, glm-5.2, qwen-plus]' > "$adir/config/models.yaml"
  echo "# $a agent" > "$adir/README.md"
done

# 4. 一次验证（结构 + JSON + shell 语法 + secret）
fail=0
for d in "$ROOT/agents"/*/; do
  [ -d "$d" ] || continue
  for f in README.md manifest.json run.sh config/mcp.json config/models.yaml; do
    [ -f "$d/$f" ] || { echo "MISSING: $d/$f"; fail=1; }
  done
  bash -n "$d/run.sh" || fail=1
  python3 -c "import json,sys;json.load(open('$d/manifest.json'))" 2>/dev/null || fail=1
done
hits=$(grep -rIE 'sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{30,}|AKIA[0-9A-Z]{16}' \
  "$ROOT/agents" "$ROOT/shared" --include='*.json' --include='*.sh' --include='*.yaml' --include='*.md' 2>/dev/null \
  | grep -v 'REDACTED' | grep -v '\${' | head -3 || true)
if [ -n "$hits" ]; then echo "SECRET:"; echo "$hits"; fail=1; fi
[ $fail -eq 0 ] || { echo "❌ 验证失败"; exit 1; }
echo "✅ 验证通过: $(ls -1 "$ROOT/agents" | wc -l) agents"

# 5. gitignore + 推送
cat > "$ROOT/.gitignore" <<'EOF'
.env
*.key
*.pem
*.log
wordlists/
data/
.aider-desk/ .augment/ .bob/ .claude/ .codeartsdoer/ .codebuddy/
.codemaker/ .codestudio/ .commandcode/ .continue/ .cortex/ .crush/
.devin/ .forge/ .fx/ .goose/ .grok/ .hermes/ .inferencesh/ .jazz/
.junie/ .iflow/ .kimchi/ .kiro/ .kode/ .lingma/ .mcpjam/ .minimax/
.vibe/ .moxby/ .mux/ .ona/ .posit/ .qoder/ .qwen/ .reasonix/
.rovodev/ .roo/ .tabnine/ .terramind/ .tinycloud/ .trae/ .windsurf/
.zcode/ .zencoder/ .neovate/ .pochi/ .adal/ .agents/ skills/
EOF

[ -d .git ] || git init -b "$BRANCH"
git add -A
git -c user.name=oh-stack -c user.email=agent@oh-stack.local \
  commit -m "organize agents ($(date -Iseconds))" 2>/dev/null || echo "no changes"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$GH_REPO.git"
git push -u origin "$BRANCH"
echo "✅ 推送完成: https://github.com/$GH_REPO/tree/$BRANCH/agents"
