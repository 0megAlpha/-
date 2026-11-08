#!/usr/bin/env bash
set -uo pipefail
ROOT="$HOME/oh-stack"
GH_REPO="${GH_REPO:-0megAlpha/-}"
BRANCH="main"
cd "$ROOT" || { echo "cd $ROOT 失败"; exit 1; }

echo "════════ 阶段 1/5: 全境扫描 ════════"
MANIFEST=(
  agents shared
  mcp-servers litellm redteam astra scripts repos reverse-apis skills-external workspace
  .openhands
  emat_kernel.py start-all.sh
  openwebui_plugins.txt mobile_setup.md schedule.json skills-lock.json organize-and-push.sh
)
for item in "${MANIFEST[@]}"; do
  if [ -e "$item" ]; then
    if [ -d "$item" ]; then
      printf "  ✓ %-30s %5d files\n" "$item/" "$(find "$item" -type f 2>/dev/null | wc -l)"
    else
      printf "  ✓ %-30s (file)\n" "$item"
    fi
  else
    printf "  - %-30s (不存在)\n" "$item"
  fi
done

echo ""
echo "════════ 阶段 2/5: .gitignore ════════"
cat > .gitignore <<'EOF'
# 敏感
*.key
*.pem
*.log
.env
.env.*
credentials*.json
auth.json
litellm/proxy.log
# 运行时
node_modules/
__pycache__/
.venv/
venv/
*.pyc
.pytest_cache/
.ruff_cache/
# 本地数据
wordlists/
data/
logs/
backups/
# npx 撒的重复分发（已归入 agents/）
.aider-desk/ .augment/ .bob/ .claude/ .codeartsdoer/ .codebuddy/
.codemaker/ .codestudio/ .commandcode/ .continue/ .cortex/ .crush/
.devin/ .forge/ .fx/ .goose/ .grok/ .hermes/ .inferencesh/ .jazz/
.junie/ .iflow/ .kimchi/ .kiro/ .kode/ .lingma/ .mcpjam/ .minimax/
.vibe/ .moxby/ .mux/ .ona/ .posit/ .qoder/ .qwen/ .reasonix/
.rovodev/ .roo/ .tabnine/ .terramind/ .tinycloud/ .trae/ .windsurf/
.zcode/ .zencoder/ .neovate/ .pochi/ .adal/ .agents/ skills/
# 断链源（内容已在 agents/*/skills/）
.openhands/skills/
# 系统
.DS_Store
Thumbs.db
EOF
echo "  ✓ .gitignore 已更新"

echo ""
echo "════════ 阶段 3/5: 秘钥扫描 ════════"
HITS=$(grep -rIE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH) PRIVATE' \
  --include='*.md' --include='*.json' --include='*.yaml' --include='*.yml' --include='*.sh' --include='*.py' --include='*.js' --include='*.ts' \
  agents shared mcp-servers litellm astra scripts .openhands workspace \
  2>/dev/null | grep -vE '\$\{|\{\{|placeholder|<[A-Z_]+>|REDACTED|example' | head -10 || true)
if [ -n "$HITS" ]; then
  echo "  ⚠ 疑似秘钥："
  echo "$HITS"
fi
if [ -f litellm/config.yaml ]; then
  sed -i -E 's/(master_key:[[:space:]]*)"sk-[a-zA-Z0-9]+"/\1"${LITELLM_MASTER}"/' litellm/config.yaml && \
    echo "  ✓ litellm/config.yaml 的 master_key 占位符化"
fi

echo ""
echo "════════ 阶段 4/5: Git 提交 ════════"
[ -d .git ] || git init -b "$BRANCH"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GH_REPO.git"
git add -A 2>&1 | tail -2
echo "  已暂存 $(git diff --cached --name-only 2>/dev/null | wc -l) 个文件"
git -c user.name="oh-stack" -c user.email="agent@oh-stack.local" \
  commit -m "full deploy: all agents + MCP + configs ($(date -Iseconds))" 2>&1 | tail -3 || echo "  无变更"

echo ""
echo "════════ 阶段 5/5: 推送 ════════"
echo "  remote: https://github.com/$GH_REPO"
git ls-remote --heads "https://github.com/$GH_REPO.git" >/dev/null 2>&1 \
  || { echo "❌ 无法访问 remote，检查 repo 名或凭证"; exit 1; }

push_ok=0
if git push -u origin "$BRANCH" 2>&1; then
  push_ok=1
else
  echo ""
  echo "⚠ 首次推送被拒，尝试 pull --rebase ..."
  if git pull --rebase origin "$BRANCH" 2>&1 | tail -5; then
    if git push -u origin "$BRANCH" 2>&1; then
      push_ok=1
    fi
  else
    echo "⚠ rebase 冲突，改用强制推送（本地为权威源）"
    git rebase --abort 2>/dev/null || true
    if git push --force-with-lease origin "$BRANCH" 2>&1; then
      push_ok=1
    fi
  fi
fi

echo ""
if [ "$push_ok" = "1" ]; then
  echo "════════ ✅ 推送成功 ════════"
  echo "  https://github.com/$GH_REPO/tree/$BRANCH"
  echo "  提交: $(git log --oneline -1)"
  echo "  已推文件: $(git ls-files | wc -l)"
  echo "  submodule: $(git submodule status 2>/dev/null | wc -l) 个（clone 用 --recursive 拉内容）"
else
  echo "════════ ❌ 推送失败 ════════"
  echo "  排查:"
  echo "    1. repo 名是否正确: $GH_REPO"
  echo "    2. 凭证: git config credential.helper（HTTPS 需 token）"
  echo "    3. 手动: cd ~/oh-stack && git push --force-with-lease origin main"
  exit 1
fi
