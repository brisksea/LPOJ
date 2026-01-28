#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "  停止 LPOJ 开发环境"
echo "════════════════════════════════════════════════════"
echo ""

# 停止后端
echo "🛑 停止后端服务..."
pkill -f "python.*manage.py runserver" || true
pkill -f "python3.*manage.py runserver" || true

# 停止前端
echo "🛑 停止前端服务..."
pkill -f "npm run dev" || true

# 停止数据库容器
echo "🛑 停止MySQL容器..."
docker-compose -f docker-compose-dev.yml down

# 清理PID文件
rm -f .dev-pids

echo ""
echo "✅ 所有开发服务已停止"
echo ""
echo "💡 要重新启动: bash dev-start.sh"
echo ""
echo "════════════════════════════════════════════════════"
