#!/bin/bash
# 完整的中文编码修复部署脚本
# 在远程服务器 10.188.2.252 上执行

set -e

echo "================================================"
echo " LPOJ Python 中文输出编码修复"
echo "================================================"
echo ""

cd /home/lzc/LPOJ

echo "步骤 1/4: 停止 judger 服务..."
sudo docker-compose stop judger

echo ""
echo "步骤 2/4: 检查修复内容..."
echo "- encoding='utf-8' 数量:"
grep -c "encoding='utf-8'" Judger/main.py || echo "0"
echo "- PYTHONIOENCODING 设置:"
grep -c "PYTHONIOENCODING=utf-8" Judger/main.py || echo "0（需要至少2处）"

echo ""
echo "步骤 3/4: 重新构建 judger 镜像（不使用缓存）..."
sudo docker-compose -f docker-compose-build.yml build --no-cache judger

echo ""
echo "步骤 4/4: 启动 judger 服务（3个实例）..."
sudo docker-compose -f docker-compose-build.yml up -d --scale judger=3

echo ""
echo "================================================"
echo " 部署完成！"
echo "================================================"
echo ""

echo "容器状态:"
sudo docker-compose ps judger

echo ""
echo "验证环境变量设置："
sudo docker-compose exec judger python3 -c "import os; print('PYTHONIOENCODING:', os.environ.get('PYTHONIOENCODING', 'NOT SET'))"

echo ""
echo "测试中文输出:"
sudo docker-compose exec judger bash -c 'echo "你好" | PYTHONIOENCODING=utf-8 python3 -c "print(input())"'

echo ""
echo "========================================="
echo "现在可以提交以下代码到 683 题测试:"
echo ""
echo "input()"
echo "print(\"你好\")"
echo ""
echo "应该显示 Accepted"
echo "========================================="
