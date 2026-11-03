#!/usr/bin/env bash
set -euo pipefail

echo "🚀 启动 Hermes Ultimate 2026..."
echo ""

if [ ! -f docker-compose.yml ]; then
  echo "❌ 错误: docker-compose.yml 不存在"
  exit 1
fi

echo "启动容器..."
docker-compose up -d

echo ""
sleep 5

echo "✅ 服务已启动"
echo ""
echo "📱 访问地址:"
echo "   Hermes UI:     http://localhost:8787"
echo "   OpenHands:     http://localhost:3000"
echo ""

docker-compose ps

echo ""
echo "💡 提示: 使用 'bash auto_verify_update.sh' 验证系统状态"
