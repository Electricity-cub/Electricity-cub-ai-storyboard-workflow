#!/bin/bash

# AI分镜师后端服务 - 启动脚本

echo "========================================="
echo "   AI分镜师 - 后端服务启动"
echo "========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 启动服务
echo ""
echo "========================================="
echo "🚀 启动后端服务..."
echo "========================================="
echo ""
echo "服务地址: http://localhost:5000"
echo "健康检查: http://localhost:5000/health"
echo "API接口: http://localhost:5000/api/v1/generate"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python app.py
