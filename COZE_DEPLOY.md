# Coze平台部署指南

## 🚀 部署到Coze平台

### 前置条件

✅ **已完成：**
- 代码已提交到Git仓库
- 项目已配置Coze部署配置（.coze文件）
- 依赖已安装（pyproject.toml）

## 📋 部署步骤

### 步骤1：准备Git仓库

确保你的代码已推送到远程仓库（GitHub/GitLab/Gitee等）

```bash
# 查看当前状态
git status

# 如果有未提交的更改，先提交
git add .
git commit -m "准备部署到Coze平台"
git push
```

### 步骤2：在Coze平台创建项目

1. **登录Coze平台**
   - 访问你的Coze工作台

2. **创建新应用**
   - 点击"创建应用"或"New Application"
   - 选择应用类型：`工作流` 或 `Bot`
   - 应用名称：`AI分镜师工作流`
   - 应用描述：`将剧本转化为Seedance视频提示词的AI工作流`

3. **配置基本信息**
   - 编程语言：`Python`
   - 运行环境：`Python 3.12`
   - 入口文件：`src/main.py`

### 步骤3：关联Git仓库

**方法A：通过Coze界面关联（推荐）**

1. 在应用设置中找到"代码管理"或"Git仓库"
2. 点击"关联仓库"
3. 选择你的Git平台（GitHub/GitLab/Gitee）
4. 授权Coze访问你的仓库
5. 选择要关联的仓库分支（通常是 `main`）

**方法B：通过Coze CLI部署**

如果你有Coze CLI工具：

```bash
# 安装Coze CLI（如果还没安装）
npm install -g @coze/cli

# 登录Coze
coze login

# 部署当前项目
coze deploy
```

### 步骤4：配置部署参数

在Coze平台配置以下参数：

#### 环境变量（如果需要）
```
COZE_WORKSPACE_PATH=/workspace/projects
PORT=5000
LOG_LEVEL=INFO
```

#### 依赖管理
Coze会自动从 `pyproject.toml` 读取依赖：
```toml
[project]
requires = ["python-3.12"]
```

#### 构建配置
- 构建命令：`bash scripts/setup.sh`
- 运行命令：`bash scripts/http_run.sh -p 5000`

### 步骤5：触发部署

**方式1：手动部署**
1. 在Coze平台点击"部署"或"Deploy"
2. 选择要部署的分支（main）
3. 点击"开始部署"

**方式2：自动部署（推荐）**
1. 在Coze配置Webhook
2. 关联GitHub仓库的push事件
3. 每次推送代码自动触发部署

### 步骤6：监控部署过程

部署过程中，你会看到：

```
✅ 检出代码
✅ 安装依赖
✅ 构建项目
✅ 启动服务
✅ 健康检查
```

## 🔧 部署配置说明

### .coze 文件解析

```ini
[project]
entrypoint = "src/main.py"      # 应用入口
requires = ["python-3.12"]      # Python版本要求

[deploy]
build = ["bash", "scripts/setup.sh"]         # 构建命令
run = ["bash", "/workspace/projects/scripts/http_run.sh", "-p 5000"]  # 运行命令
deps = ["git"]                                  # 系统依赖
```

### 构建流程

1. **环境准备**
   - 安装Python 3.12
   - 安装git

2. **构建阶段（build）**
   ```bash
   bash scripts/setup.sh
   ```
   - 安装项目依赖
   - 初始化数据库（如果有）
   - 下载模型资源（如果有）

3. **运行阶段（run）**
   ```bash
   bash scripts/http_run.sh -p 5000
   ```
   - 启动HTTP服务
   - 监听5000端口
   - 等待请求

## 🌐 部署完成后

### 1. 获取访问地址

部署成功后，Coze会提供：
- **API地址**：`https://your-app.coze.run`
- **WebSocket地址**：`wss://your-app.coze.run`
- **测试地址**：Coze平台提供的在线测试页面

### 2. 测试API

```bash
# 测试健康检查
curl https://your-app.coze.run/health

# 测试工作流
curl -X POST https://your-app.coze.run/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "你的剧本内容",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

### 3. 配置域名（可选）

在Coze平台配置自定义域名：
1. 在应用设置中找到"域名管理"
2. 添加你的域名（如 `workflow.yourdomain.com`）
3. 配置DNS解析
4. 启用HTTPS证书

## 🔄 更新部署

### 代码更新流程

1. **本地修改代码**
```bash
# 修改代码后提交
git add .
git commit -m "更新功能"
git push
```

2. **触发部署**
   - 如果配置了自动部署：自动触发
   - 如果是手动部署：在Coze平台点击"部署"

3. **验证更新**
```bash
curl https://your-app.coze.run/health
```

## 📊 监控和日志

### 查看部署日志

在Coze平台可以查看：
- **构建日志**：依赖安装、构建过程
- **运行日志**：应用运行时的日志
- **错误日志**：异常和错误信息

### 本地日志位置

```bash
# 查看应用日志
cat /app/work/logs/bypass/app.log

# 查看最新日志
tail -n 50 /app/work/logs/bypass/app.log
```

## ⚙️ 高级配置

### 配置数据库

如果需要数据库支持：

1. 在Coze平台申请数据库资源
2. 获取数据库连接信息
3. 配置环境变量：
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

### 配置对象存储

如果需要存储生成的文件：

1. 在Coze平台申请OSS资源
2. 获取访问密钥
3. 配置环境变量：
   ```
   OSS_ACCESS_KEY=your_access_key
   OSS_SECRET_KEY=your_secret_key
   OSS_BUCKET=your_bucket
   ```

### 配置大模型API

工作流已集成 `doubao-seed-2-0-pro-260215`，如果需要切换模型：

1. 在Coze平台配置模型API密钥
2. 修改 `config/*.json` 中的 `model` 字段
3. 重新部署

## 🔐 安全配置

### API密钥管理

1. 在Coze平台配置环境变量
2. 修改代码从环境变量读取密钥：
   ```python
   import os
   api_key = os.getenv("API_KEY")
   ```

### 访问控制

在Coze平台配置：
- API访问白名单
- 限流策略
- 认证方式

## 🐛 常见问题

### Q1: 部署失败 - 依赖安装错误
**A:** 检查 `pyproject.toml` 中的依赖是否正确，使用 `uv add` 而不是 `pip install`

### Q2: 部署成功但无法访问
**A:**
- 检查端口配置（.coze文件中的PORT）
- 检查健康检查端点是否正常
- 查看部署日志中的错误信息

### Q3: 运行时错误 - 模块找不到
**A:** 确保所有依赖都已声明在 `pyproject.toml` 中

### Q4: 性能问题 - 响应慢
**A:**
- 检查大模型API调用是否优化
- 考虑增加缓存机制
- 优化剧本处理逻辑

## 📞 获取帮助

- Coze平台文档
- Coze技术支持
- 项目日志：`/app/work/logs/bypass/app.log`

---

## ✅ 部署检查清单

部署前请确认：

- [ ] 代码已提交到Git仓库
- [ ] .coze 配置文件正确
- [ ] pyproject.toml 依赖完整
- [ ] 入口文件 `src/main.py` 存在
- [ ] 启动脚本 `scripts/http_run.sh` 存在
- [ ] 构建脚本 `scripts/setup.sh` 存在
- [ ] 环境变量已配置（如果需要）
- [ ] 数据库连接已配置（如果需要）

部署后请验证：

- [ ] 应用成功启动
- [ ] 健康检查端点正常
- [ ] API调用成功
- [ ] 日志正常输出
- [ ] 无错误和异常

---

准备就绪后，按照上述步骤在Coze平台部署你的AI分镜师工作流！
