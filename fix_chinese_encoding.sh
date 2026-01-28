#!/bin/bash
# 修复 LPOJ Judger 中文编码问题并重新部署

set -e  # 遇到错误立即退出

echo "================================================"
echo "LPOJ Judger 中文编码修复脚本"
echo "================================================"

# 1. 检查当前目录
if [ ! -f "docker-compose.yml" ]; then
    echo "错误: 请在 LPOJ 项目根目录执行此脚本"
    exit 1
fi

echo ""
echo "步骤 1/4: 停止 judger 服务..."
sudo docker-compose stop judger

echo ""
echo "步骤 2/4: 检查 main.py 中的编码修复..."
grep -n "encoding='utf-8'" Judger/main.py | head -5
if [ $? -eq 0 ]; then
    echo "✓ 编码修复已应用到 main.py"
else
    echo "✗ 警告: main.py 中未找到 encoding='utf-8'"
fi

echo ""
echo "步骤 3/4: 重新构建 judger 镜像..."
sudo docker-compose -f docker-compose-build.yml build judger

echo ""
echo "步骤 4/4: 启动 judger 服务（3个实例）..."
sudo docker-compose -f docker-compose-build.yml up -d --scale judger=3

echo ""
echo "================================================"
echo "部署完成！正在检查服务状态..."
echo "================================================"
sudo docker-compose ps judger

echo ""
echo "查看最近的日志（按 Ctrl+C 退出）："
echo "sudo docker-compose logs -f judger"
echo ""
echo "测试建议："
echo "1. 提交一个包含中文输入/输出的测试题目"
echo "2. 查看评测结果是否正常"
echo ""
