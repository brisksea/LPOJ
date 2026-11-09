#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "  LPOJ 开发环境状态"
echo "════════════════════════════════════════════════════"
echo ""

# 检查Docker
echo "🐳 Docker 容器状态:"
docker-compose -f docker-compose-dev.yml ps
echo ""

# 检查后端进程
echo "🔧 Backend 进程:"
pgrep -f "python.*manage.py runserver" > /dev/null && echo "  ✅ 运行中 (PID: $(pgrep -f 'python.*manage.py runserver'))" || echo "  ❌ 未运行"
echo ""

# 检查前端进程
echo "🌐 Frontend 进程:"
FRONTEND_PIDS=$(pgrep -f "npm run dev" | head -1)
if [ -n "$FRONTEND_PIDS" ]; then
    echo "  ✅ 运行中 (PID: $FRONTEND_PIDS)"
else
    echo "  ❌ 未运行"
fi
echo ""

# 检查数据库连接
echo "📦 数据库连接:"
if docker exec $(docker-compose -f docker-compose-dev.yml ps -q db 2>/dev/null) mysqladmin ping -u root -plpojdatabase &> /dev/null; then
    echo "  ✅ 已连接"
    echo "    地址: 127.0.0.1:3306"
    echo "    用户: root"
else
    echo "  ❌ 无法连接"
fi
echo ""

# 检查端口
echo "🔌 端口状态:"
lsof -i :8080 &>/dev/null && echo "  ✅ 8080 (Frontend) 正在使用" || echo "  ⚠️  8080 (Frontend) 未使用"
lsof -i :8081 &>/dev/null && echo "  ✅ 8081 (Mobile) 正在使用" || echo "  ⚠️  8081 (Mobile) 未使用"
lsof -i :9003 &>/dev/null && echo "  ✅ 9003 (Backend) 正在使用" || echo "  ⚠️  9003 (Backend) 未使用"
lsof -i :3306 &>/dev/null && echo "  ✅ 3306 (MySQL) 正在使用" || echo "  ⚠️  3306 (MySQL) 未使用"
echo ""

echo "════════════════════════════════════════════════════"
echo ""
echo "🌐 服务访问:"
echo "  Frontend:  http://localhost:8080"
echo "  Mobile:    http://localhost:8081"
echo "  Admin:     http://localhost:9003/admin"
echo ""
echo "📝 命令:"
echo "  启动:      bash dev-start.sh"
echo "  停止:      bash dev-stop.sh"
echo "  查看日志:  docker-compose -f docker-compose-dev.yml logs -f db"
echo ""
