#!/bin/bash

# 上传到GitHub的自动化脚本

echo "========================================="
echo "   AI分镜师工作流 - 上传到GitHub"
echo "========================================="
echo ""

# 检查是否已配置远程仓库
if git remote get-url origin &>/dev/null; then
    echo "⚠️  已存在远程仓库"
    REMOTE_URL=$(git remote get-url origin)
    echo "   当前远程地址: $REMOTE_URL"
    echo ""
    read -p "是否要更换远程仓库？(y/n): " CHANGE_REMOTE

    if [ "$CHANGE_REMOTE" = "y" ]; then
        read -p "请输入新的GitHub仓库URL: " NEW_URL
        git remote set-url origin "$NEW_URL"
        echo "✅ 远程仓库已更新"
    fi
else
    echo "📝 需要配置GitHub仓库"
    echo ""
    echo "请先在GitHub创建一个新仓库："
    echo "1. 访问 https://github.com/new"
    echo "2. 创建新仓库（例如：ai-storyboard-workflow）"
    echo "3. 不要初始化README"
    echo ""
    read -p "请输入GitHub仓库URL（例如：https://github.com/username/repo.git）: " REPO_URL
    git remote add origin "$REPO_URL"
    echo "✅ 远程仓库已配置"
fi

echo ""
echo "📦 开始推送代码..."
echo ""

# 添加所有文件
git add .

# 提交
git commit -m "feat: 实现AI分镜师工作流

- 完成剧本到Seedance视频提示词的全流程
- 实现5个核心节点：导演讲戏、人物设计、场景设计、分镜头脚本、视频提示词
- 支持中英双版提示词生成
- 集成大语言模型doubao-seed-2-0-pro-260215
- 提供HTTP API服务和测试脚本
"

# 推送到GitHub
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 上传成功！"
    echo ""
    echo "🌐 你的仓库地址: $(git remote get-url origin | sed 's/\.git$//')"
    echo ""
    echo "💡 后续更新代码只需执行："
    echo "   git add ."
    echo "   git commit -m '你的更新说明'"
    echo "   git push"
else
    echo ""
    echo "❌ 上传失败"
    echo ""
    echo "可能的原因："
    echo "1. GitHub URL不正确"
    echo "2. 需要配置GitHub Token"
    echo ""
    echo "请检查后重试"
fi
