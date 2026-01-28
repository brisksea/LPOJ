#!/bin/bash
set -e

PROJECT_DIR="/home/zq/project/LPOJ"
cd "$PROJECT_DIR"

echo "════════════════════════════════════════════════════"
echo "  LPOJ 开发环境启动 (不构建镜像)"
echo "════════════════════════════════════════════════════"
echo ""

# 检查依赖
echo "✓ 检查依赖..."
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 需要安装 Docker"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要安装 Python 3"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 需要安装 Node.js"
    exit 1
fi

# 启动数据库
echo ""
echo "📦 启动MySQL容器..."
docker-compose -f docker-compose-dev.yml up -d
echo "⏳ 等待数据库启动..."
sleep 10

# 检查数据库连接
echo "🔍 检查数据库连接..."
while ! docker exec $(docker-compose ps -q db) mysqladmin ping -u root -plpojdatabase &> /dev/null; do
    echo "  等待数据库就绪..."
    sleep 2
done
echo "✅ 数据库已就绪"

# 启动后端
echo ""
echo "🔧 启动 Backend 服务..."
cd Backend

echo "  📥 安装Python依赖..."
pip install -r requirements.txt > /dev/null 2>&1 || pip3 install -r requirements.txt > /dev/null 2>&1

echo "  🔄 执行数据库迁移..."
python manage.py makemigrations > /dev/null 2>&1 || python3 manage.py makemigrations > /dev/null 2>&1
python manage.py makemigrations judgestatus item problem user contest board blog wiki classes > /dev/null 2>&1 || python3 manage.py makemigrations judgestatus item problem user contest board blog wiki classes > /dev/null 2>&1
python manage.py migrate > /dev/null 2>&1 || python3 manage.py migrate > /dev/null 2>&1

echo "  👤 创建管理员账户..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" > /dev/null 2>&1 || python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" > /dev/null 2>&1

echo "  🚀 启动开发服务器..."
python manage.py runserver 0.0.0.0:9003 2>&1 &
BACKEND_PID=$!
sleep 3
echo "  ✅ Backend 运行 (PID: $BACKEND_PID)"

# 启动前端 (Desktop)
echo ""
echo "🌐 启动 Frontend (Desktop)..."
cd ../Frontend

echo "  📥 安装依赖..."
npm install --legacy-peer-deps > /dev/null 2>&1

echo "  🚀 启动开发服务器 (热重载)..."
npm run dev 2>&1 &
FRONTEND_PID=$!
sleep 5
echo "  ✅ Frontend 运行 (PID: $FRONTEND_PID)"

# 启动前端 (Mobile)
echo ""
echo "📱 启动 Frontend (Mobile)..."
cd ../FrontendMobile

echo "  📥 安装依赖..."
npm install --legacy-peer-deps > /dev/null 2>&1

echo "  🚀 启动开发服务器 (热重载)..."
npm run dev 2>&1 &
MOBILE_PID=$!
sleep 5
echo "  ✅ FrontendMobile 运行 (PID: $MOBILE_PID)"

# 显示启动完成信息
echo ""
echo "════════════════════════════════════════════════════"
echo "✅ LPOJ 开发环境启动完成!"
echo "════════════════════════════════════════════════════"
echo ""
echo "📌 服务信息:"
echo ""
echo "  数据库 (MySQL 5.7):"
echo "    主机:    127.0.0.1"
echo "    端口:    3306"
echo "    用户:    root"
echo "    密码:    lpojdatabase"
echo "    数据库:  LPOJ"
echo ""
echo "🌐 访问地址:"
echo ""
echo "  🖥️  前端 (Desktop):  http://localhost:8080"
echo "  📱 前端 (Mobile):   http://localhost:8081"
echo "  🔧 后端 API:        http://localhost:9003"
echo "  👨‍💼 Admin 管理:       http://localhost:9003/admin"
echo "     账户: admin"
echo "     密码: admin"
echo ""
echo "📝 进程PID:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo "  Mobile:   $MOBILE_PID"
echo ""
echo "📋 常用命令:"
echo ""
echo "  查看数据库:    mysql -h 127.0.0.1 -u root -p"
echo "  查看Docker日志: docker-compose -f docker-compose-dev.yml logs -f db"
echo "  重置数据库:    cd Backend && python manage.py flush --no-input && python manage.py migrate"
echo "  停止所有服务:  bash dev-stop.sh"
echo ""
echo "⚠️  按 Ctrl+C 可以停止后端服务"
echo "    但前端会继续运行，可以用 dev-stop.sh 停止所有"
echo ""
echo "════════════════════════════════════════════════════"

# 保存PID到文件，方便停止
echo "$BACKEND_PID" > .dev-pids
echo "$FRONTEND_PID" >> .dev-pids
echo "$MOBILE_PID" >> .dev-pids

# 等待后端进程
wait $BACKEND_PID
