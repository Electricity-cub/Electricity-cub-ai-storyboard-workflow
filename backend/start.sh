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

echo "✅ Python3 已安装: $(python3 --version)"

# 检查依赖
echo "🔧 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 安装Flask..."
    pip install -q flask requests
fi

if ! python3 -c "import requests" 2>/dev/null; then
    echo "📥 安装Requests..."
    pip install -q flask requests
fi

echo "✅ 依赖已安装"

# 检查Token配置
if grep -q '"你的Coze_API_Token"' app.py; then
    echo ""
    echo "⚠️  警告：API Token 未配置！"
    echo "请编辑 app.py，将第22行的 \"你的Coze_API_Token\" 替换为实际Token"
    echo ""
    read -p "是否继续启动？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

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
echo "⏱️  提示：工作流执行可能需要较长时间（2-10分钟），请耐心等待"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
