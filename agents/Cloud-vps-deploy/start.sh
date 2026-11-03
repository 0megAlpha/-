#!/usr/bin/env bash
set -euo pipefail
 
echo "🚀 启动 AI Agent Factory..."
 
# 验证配置
if [ ! -f .env.prod ]; then
  echo "❌ 错误: .env.prod 不存在"
  exit 1
fi
 
# 加载配置
source .env.prod
 
echo "📋 配置已加载"
echo "   默认 Model Provider: $DEFAULT_MODEL_PROVIDER"
echo "   默认 Model: $DEFAULT_MODEL"
 
if [ "$LODY_ENABLED" = "true" ]; then
  echo "   Lody 已启用: $LODY_SERVER"
fi
 
if [ "$CONDUIT_ENABLED" = "true" ]; then
  echo "   Conduit 已启用: $CONDUIT_SERVER"
fi
 
echo ""
echo "启动服务..."
docker-compose up -d
 
echo ""
sleep 3
 
echo "✅ 服务已启动"
echo ""
echo "📱 访问地址:"
echo "   OpenHands: http://localhost:3000"
echo ""
docker-compose ps
