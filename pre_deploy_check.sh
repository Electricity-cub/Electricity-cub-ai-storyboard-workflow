#!/bin/bash

# Coze平台部署前检查脚本

echo "========================================="
echo "   Coze平台部署 - 部署前检查"
echo "========================================="
echo ""

# 检查1：Git仓库状态
echo "📝 检查1: Git仓库状态"
if [ -d ".git" ]; then
    echo "✅ Git仓库存在"
    BRANCH=$(git branch --show-current)
    echo "   当前分支: $BRANCH"

    # 检查是否有未提交的更改
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  检测到未提交的更改"
        git status --short
        echo ""
        read -p "是否要提交这些更改？(y/n): " COMMIT_CHANGES
        if [ "$COMMIT_CHANGES" = "y" ]; then
            git add .
            read -p "请输入提交信息: " COMMIT_MSG
            git commit -m "$COMMIT_MSG"
            echo "✅ 更改已提交"
        fi
    else
        echo "✅ 工作区干净，无未提交更改"
    fi
else
    echo "❌ 不是Git仓库，请先初始化Git仓库"
    exit 1
fi

echo ""

# 检查2：远程仓库
echo "📝 检查2: 远程仓库配置"
if git remote get-url origin &>/dev/null; then
    echo "✅ 远程仓库已配置"
    REMOTE_URL=$(git remote get-url origin)
    echo "   远程地址: $REMOTE_URL"

    # 检查是否已推送
    LOCAL_COMMIT=$(git rev-parse HEAD)
    REMOTE_COMMIT=$(git ls-remote origin main 2>/dev/null | awk '{print $1}')

    if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
        echo "⚠️  本地有未推送的提交"
        read -p "是否要推送到远程仓库？(y/n): " PUSH_CODE
        if [ "$PUSH_CODE" = "y" ]; then
            echo "📤 推送代码到远程仓库..."
            git push origin $BRANCH
            if [ $? -eq 0 ]; then
                echo "✅ 代码已推送"
            else
                echo "❌ 推送失败，请检查网络或认证信息"
                exit 1
            fi
        fi
    else
        echo "✅ 代码已与远程同步"
    fi
else
    echo "❌ 未配置远程仓库"
    echo ""
    echo "请先配置远程仓库："
    echo "1. 在GitHub/GitLab/Gitee创建新仓库"
    echo "2. 运行: git remote add origin <仓库URL>"
    echo "3. 运行: git push -u origin main"
    exit 1
fi

echo ""

# 检查3：配置文件
echo "📝 检查3: 配置文件"
CONFIG_FILES=(
    ".coze"
    "pyproject.toml"
    "src/main.py"
    "scripts/setup.sh"
    "scripts/http_run.sh"
)

ALL_EXIST=true
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    echo ""
    echo "❌ 缺少必要的配置文件，部署可能失败"
    read -p "是否继续？(y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        exit 1
    fi
fi

echo ""

# 检查4：依赖文件
echo "📝 检查4: 依赖管理"
if [ -f "pyproject.toml" ]; then
    echo "✅ pyproject.toml 存在"
    echo "   检查依赖..."
    if [ -f "requirements.txt" ]; then
        DEP_COUNT=$(wc -l < requirements.txt)
        echo "   requirements.txt 包含 $DEP_COUNT 个依赖"
    else
        echo "⚠️  requirements.txt 不存在，建议生成"
        read -p "是否生成requirements.txt？(y/n): " GEN_REQ
        if [ "$GEN_REQ" = "y" ]; then
            if command -v uv &>/dev/null; then
                uv export --frozen --no-hashes --no-dev | grep -v "^#" | grep -v "^$" | grep -v "^    " | sed 's/ ;.*//' > requirements.txt
            else
                pip freeze --exclude watchdog > requirements.txt
            fi
            echo "✅ requirements.txt 已生成"
        fi
    fi
fi

echo ""

# 检查5：工作流文件
echo "📝 检查5: 工作流文件"
WORKFLOW_FILES=(
    "src/graphs/state.py"
    "src/graphs/graph.py"
    "src/graphs/nodes/director_notes_node.py"
    "src/graphs/nodes/character_design_node.py"
    "src/graphs/nodes/scene_design_node.py"
    "src/graphs/nodes/storyboard_node.py"
    "src/graphs/nodes/seedance_prompts_node.py"
)

WORKFLOW_OK=true
for file in "${WORKFLOW_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file 不存在"
        WORKFLOW_OK=false
    fi
done

if [ "$WORKFLOW_OK" = false ]; then
    echo ""
    echo "❌ 工作流文件不完整"
    exit 1
fi

echo ""

# 检查6：配置文件
echo "📝 检查6: 大模型配置"
CONFIG_COUNT=$(ls -1 config/*.json 2>/dev/null | wc -l)
echo "✅ 找到 $CONFIG_COUNT 个配置文件"
ls config/*.json 2>/dev/null | while read file; do
    echo "   - $(basename $file)"
done

echo ""

# 总结
echo "========================================="
echo "   检查完成"
echo "========================================="
echo ""
echo "✅ 所有检查通过！"
echo ""
echo "📋 下一步操作："
echo ""
echo "1️⃣  在Coze平台创建新应用"
echo "   - 访问你的Coze工作台"
echo "   - 创建工作流/Bot应用"
echo "   - 配置基本信息"
echo ""
echo "2️⃣  关联Git仓库"
echo "   - 在应用设置中关联Git仓库"
echo "   - 选择当前仓库和分支"
echo "   - 授权Coze访问权限"
echo ""
echo "3️⃣  配置部署参数"
echo "   - 确认入口文件: src/main.py"
echo "   - 确认运行环境: Python 3.12"
echo "   - 配置环境变量（如果需要）"
echo ""
echo "4️⃣  触发部署"
echo "   - 点击\"部署\"按钮"
echo "   - 选择要部署的分支"
echo "   - 等待部署完成"
echo ""
echo "5️⃣  验证部署"
echo "   - 获取API地址"
echo "   - 测试健康检查"
echo "   - 测试工作流调用"
echo ""
echo "📖 详细文档: 查看 COZE_DEPLOY.md"
echo ""
echo "💡 需要帮助？"
echo "   - 查看部署日志"
echo "   - 检查 /app/work/logs/bypass/app.log"
echo "   - 联系Coze技术支持"
echo ""
