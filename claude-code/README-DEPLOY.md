# Claude Code 部署说明

1. 启动 LiteLLM：
   bash litellm/start.sh

2. 载入环境（Claude Code 通过 Anthropic 兼容端点路由）：
   export ANTHROPIC_BASE_URL="http://127.0.0.1:4000"
   export ANTHROPIC_API_KEY="sk-anything"

3. MCP 配置：
   cp mcp-configs/mcp.json ~/.claude/mcp_settings.json

4. 启动：
   claude
