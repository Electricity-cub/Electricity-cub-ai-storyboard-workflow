# AI分镜师工作流

将剧本转化为专业分镜脚本的智能系统。

## 🚀 快速开始

### 方式1：Coze Web SDK（推荐，最简单）

1. 下载 `index_cozeweb.html`
2. 获取Coze API Token（在Coze工作流页面）
3. 打开文件，替换第223行的API Token
4. 在浏览器中打开使用

**部署到线上：**
- 上传到Vercel/GitHub Pages/Netlify
- 无需后端，2分钟上线

---

### 方式2：后端版本（更安全）

1. 克隆仓库
2. 配置环境变量：
   ```bash
   API_TOKEN=你的Coze_API_Token
   COZE_API_URL=https://3b7j5mjhsz.coze.site/workflow_run
   ```
3. 运行：
   ```bash
   pip install -r requirements_web.txt
   python app.py
   ```

**部署到Railway：**
1. 访问 railway.app
2. 连接GitHub仓库
3. 配置环境变量
4. 点击部署

---

## 📖 使用说明

### 输入参数

- **剧本内容**：待分镜的剧本文本
- **集数**：ep01, ep02等（默认ep01）
- **视觉风格**：写实、3D CG、国漫、日漫
- **项目类型**：国内短剧、海外短剧、国内动漫剧、海外动漫剧

### 输出结果

- 导演讲戏本
- 人物设计提示词
- 场景设计提示词
- 分镜头脚本
- Seedance视频提示词

---

## 🌐 项目地址

- GitHub: https://github.com/Electricity-cub/Electricity-cub-ai-storyboard-workflow

---

## 📄 文件说明

- `index_cozeweb.html` - Coze Web SDK版本（推荐）
- `app.py` - Flask后端服务
- `templates/index.html` - 前端页面
- `requirements_web.txt` - Python依赖
- `Procfile` - Railway部署配置

---

## ⚠️ 注意事项

- Coze Web SDK版本：API Token暴露在前端，适合测试/内部项目
- 后端版本：API Token在后端，适合公开项目
- 请妥善保管API Token，不要泄露

---

## 📝 许可证

MIT
