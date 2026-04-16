#!/bin/bash

# AI分镜师工作流 - 完整自动化部署脚本

echo "========================================="
echo "   AI分镜师工作流 - 自动化部署"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 步骤1：检查Git仓库状态
echo -e "${BLUE}步骤1: 检查Git仓库状态${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✅ Git仓库存在${NC}"
    BRANCH=$(git branch --show-current)
    echo "   当前分支: $BRANCH"
else
    echo -e "${RED}❌ 不是Git仓库${NC}"
    exit 1
fi
echo ""

# 步骤2：配置远程仓库
echo -e "${BLUE}步骤2: 配置远程仓库${NC}"

if git remote get-url origin &>/dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo -e "${YELLOW}⚠️  已存在远程仓库: $REMOTE_URL${NC}"
    read -p "是否要更换远程仓库？(y/n): " CHANGE_REMOTE
    if [ "$CHANGE_REMOTE" = "y" ]; then
        read -p "请输入新的远程仓库URL: " NEW_URL
        git remote set-url origin "$NEW_URL"
        echo -e "${GREEN}✅ 远程仓库已更新${NC}"
    fi
else
    echo ""
    echo "请选择一个Git平台："
    echo "  1) GitHub (推荐，国际通用)"
    echo "  2) GitLab (企业级)"
    echo "  3) Gitee (码云，国内访问最快)"
    echo ""
    read -p "请选择 (1/2/3): " PLATFORM

    case $PLATFORM in
        1)
            echo ""
            echo -e "${BLUE}配置GitHub仓库${NC}"
            echo ""
            echo "请先在GitHub创建一个新仓库："
            echo "1. 访问 https://github.com/new"
            echo "2. 仓库名: ai-storyboard-workflow"
            echo "3. 设为公开或私有"
            echo "4. 不要初始化README"
            echo "5. 点击创建"
            echo ""
            read -p "请输入GitHub仓库URL: " REPO_URL
            ;;
        2)
            echo ""
            echo -e "${BLUE}配置GitLab仓库${NC}"
            echo ""
            echo "请先在GitLab创建一个新仓库："
            echo "1. 访问 https://gitlab.com/projects/new"
            echo "2. 仓库名: ai-storyboard-workflow"
            echo "3. 设为公开或私有"
            echo "4. 点击创建"
            echo ""
            read -p "请输入GitLab仓库URL: " REPO_URL
            ;;
        3)
            echo ""
            echo -e "${BLUE}配置Gitee仓库${NC}"
            echo ""
            echo "请先在Gitee创建一个新仓库："
            echo "1. 访问 https://gitee.com/projects/new"
            echo "2. 仓库名: ai-storyboard-workflow"
            echo "3. 设为公开或私有"
            echo "4. 点击创建"
            echo ""
            read -p "请输入Gitee仓库URL: " REPO_URL
            ;;
        *)
            echo -e "${RED}❌ 无效选择${NC}"
            exit 1
            ;;
    esac

    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✅ 远程仓库已配置: $REPO_URL${NC}"
fi
echo ""

# 步骤3：推送代码到远程仓库
echo -e "${BLUE}步骤3: 推送代码到远程仓库${NC}"
echo "正在推送代码到远程仓库..."
echo ""

# 先拉取远程分支信息（如果有）
git fetch origin main 2>/dev/null || true

# 推送代码
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 代码已成功推送到远程仓库${NC}"
else
    echo -e "${RED}❌ 推送失败${NC}"
    echo ""
    echo "可能的原因："
    echo "1. 仓库URL不正确"
    echo "2. 需要配置Git认证（GitHub Token或SSH密钥）"
    echo ""
    echo "请检查后重试"
    exit 1
fi
echo ""

# 步骤4：生成部署配置文件
echo -e "${BLUE}步骤4: 生成部署配置${NC}"

# 检查.coze文件是否存在
if [ -f ".coze" ]; then
    echo -e "${GREEN}✅ .coze配置文件存在${NC}"
else
    echo -e "${YELLOW}⚠️  .coze配置文件不存在${NC}"
    echo "正在创建默认配置..."
    cat > .coze << 'EOF'
[project]
entrypoint = "src/main.py"
requires = ["python-3.12"]

[dev]
build = ["bash", "scripts/setup.sh"]
run = ["bash", "/workspace/projects/scripts/http_run.sh", "-p 5000"]
pack = ["bash", "/workspace/projects/scripts/pack.sh"]
deps = ["git"]

[deploy]
build = ["bash", "scripts/setup.sh"]
run = ["bash", "/workspace/projects/scripts/http_run.sh", "-p 5000"]
deps = ["git"]
EOF
    echo -e "${GREEN}✅ .coze配置文件已创建${NC}"
fi

# 检查pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo -e "${GREEN}✅ pyproject.toml存在${NC}"
else
    echo -e "${RED}❌ pyproject.toml不存在${NC}"
    exit 1
fi

# 检查requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "生成requirements.txt..."
    if command -v uv &>/dev/null; then
        uv export --frozen --no-hashes --no-dev | grep -v "^#" | grep -v "^$" | grep -v "^    " | sed 's/ ;.*//' > requirements.txt
    else
        pip freeze --exclude watchdog > requirements.txt
    fi
    echo -e "${GREEN}✅ requirements.txt已生成${NC}"
fi
echo ""

# 步骤5：生成部署文档
echo -e "${BLUE}步骤5: 生成部署文档${NC}"

# 检查是否已有部署文档
if [ -f "DEPLOY_GUIDE.md" ]; then
    echo -e "${GREEN}✅ 部署文档已存在${NC}"
else
    echo "生成部署文档..."
    cat > DEPLOY_GUIDE.md << 'EOF'
# 快速部署指南

## 1. 在Coze平台创建应用

1. 登录Coze平台
2. 点击"创建应用" → 选择"工作流"
3. 应用名称：`AI分镜师工作流`
4. 配置基本信息：
   - 编程语言：Python
   - 运行环境：Python 3.12
   - 入口文件：src/main.py

## 2. 关联Git仓库

1. 在应用设置中找到"代码管理"
2. 点击"关联仓库"
3. 选择你的Git平台
4. 选择仓库：ai-storyboard-workflow
5. 选择分支：main
6. 点击"关联"

## 3. 配置部署参数

### 构建配置
```
构建命令: bash scripts/setup.sh
运行命令: bash scripts/http_run.sh -p 5000
```

### 环境变量（可选）
```
PORT=5000
LOG_LEVEL=INFO
```

## 4. 触发部署

1. 点击"部署"按钮
2. 选择分支：main
3. 点击"开始部署"

## 5. 验证部署

### 测试健康检查
```bash
curl https://your-app.coze.run/health
```

### 测试API
```bash
curl -X POST https://your-app.coze.run/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "测试剧本",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

## 6. 获取访问地址

部署成功后，Coze会提供：
- API地址
- 在线测试页面
- 日志查看入口

## 常见问题

### 认证失败
配置GitHub Token或SSH密钥

### 依赖安装失败
检查pyproject.toml中的依赖配置

### 启动失败
查看Coze平台的部署日志

---

详细文档请查看：
- COZE_DEPLOY.md - 完整部署指南
- USAGE.md - 使用指南
- README.md - 项目介绍
EOF
    echo -e "${GREEN}✅ 部署文档已生成${NC}"
fi
echo ""

# 步骤6：提交部署相关文件
echo -e "${BLUE}步骤6: 提交部署相关文件${NC}"

if [ -n "$(git status --porcelain)" ]; then
    echo "检测到新文件，正在提交..."
    git add .
    git commit -m "chore: 添加部署配置和文档"
    git push
    echo -e "${GREEN}✅ 部署文件已提交并推送${NC}"
else
    echo -e "${GREEN}✅ 没有需要提交的文件${NC}"
fi
echo ""

# 步骤7：生成下一步操作指南
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}✅ 自动化部署准备完成！${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "${YELLOW}📋 下一步操作：${NC}"
echo ""
echo -e "${BLUE}1️⃣  在Coze平台创建应用${NC}"
echo "   - 访问你的Coze工作台"
echo "   - 创建工作流/Bot应用"
echo "   - 应用名称：AI分镜师工作流"
echo ""
echo -e "${BLUE}2️⃣  关联Git仓库${NC}"
echo "   - 仓库URL: $(git remote get-url origin)"
echo "   - 分支：main"
echo ""
echo -e "${BLUE}3️⃣  配置部署参数${NC}"
echo "   - 构建命令：bash scripts/setup.sh"
echo "   - 运行命令：bash scripts/http_run.sh -p 5000"
echo ""
echo -e "${BLUE}4️⃣  触发部署${NC}"
echo "   - 点击\"部署\"按钮"
echo "   - 选择分支：main"
echo "   - 等待部署完成"
echo ""
echo -e "${BLUE}5️⃣  验证部署${NC}"
echo "   - 测试API调用"
echo "   - 查看日志"
echo ""
echo -e "${YELLOW}📚 详细文档：${NC}"
echo "   - 部署指南: DEPLOY_GUIDE.md"
echo "   - 完整指南: COZE_DEPLOY.md"
echo "   - 使用手册: USAGE.md"
echo "   - 项目介绍: README.md"
echo ""
echo -e "${GREEN}🎉 准备工作已完成，现在可以在Coze平台开始部署了！${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "   如果需要GitHub Token，请访问："
echo "   https://github.com/settings/tokens"
echo ""
