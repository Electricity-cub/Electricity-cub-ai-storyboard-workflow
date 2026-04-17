#!/bin/bash

# AI分镜师 - 一键启动脚本

echo "========================================="
echo "   AI分镜师 - 一键启动"
echo "========================================="
echo ""

# 检查后端目录
if [ ! -d "backend" ]; then
    echo "❌ 未找到backend目录"
    exit 1
fi

# 检查HTML文件
if [ ! -f "index_new.html" ]; then
    echo "❌ 未找到index_new.html文件"
    exit 1
fi

echo "✅ 项目结构检查完成"
echo ""

# 启动后端服务
echo "🚀 正在启动后端服务..."
echo ""

cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -q -r requirements.txt

# 检查Token配置
if grep -q "你的Coze_API_Token" app.py; then
    echo ""
    echo "⚠️  警告：API Token未配置！"
    echo ""
    echo "请打开 backend/app.py 文件"
    echo "找到第22行，将 \"你的Coze_API_Token\" 替换成你实际的Coze API Token"
    echo ""
    read -p "是否继续启动（会失败）？(y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo "已取消启动"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "✅ 后端服务启动成功！"
echo "========================================="
echo ""
echo "📍 后端地址: http://localhost:5000"
echo "📍 健康检查: http://localhost:5000/health"
echo "📍 API接口: http://localhost:5000/api/v1/generate"
echo ""
echo "💡 下一步："
echo "   1. 在浏览器中打开 index_new.html 文件"
echo "   2. 输入剧本内容"
echo "   3. 点击 \"生成分镜\""
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动Flask应用
python app.py
