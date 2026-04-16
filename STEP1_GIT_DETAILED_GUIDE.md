# 📖 手动部署步骤2详解：配置并推送代码到GitHub

## 这一步的目标
把本地电脑上的代码，上传到GitHub网站上，这样Coze平台才能访问到这些代码进行部署。

---

## 🤔 基础概念解释

### 什么是Git？
Git是一个**版本控制工具**，就像代码的"时间机器"，可以记录每次修改的历史。

### 什么是远程仓库（Remote Repository）？
- **本地仓库**：在你电脑上的代码库
- **远程仓库**：在GitHub网站上的代码库
- **目的**：把本地代码上传到GitHub，这样：
  - 可以从任何地方访问代码
  - 可以和别人协作
  - 可以备份代码
  - Coze平台可以从GitHub获取代码部署

### 什么是Origin？
- `origin` 是远程仓库的**默认别名**
- 就像给你的GitHub仓库起个昵叫，叫"origin"
- 以后推送代码时，不用输入完整的URL，只要说"推送到origin"就行

---

## 📝 三个命令详解

### 命令1：git remote add origin [URL]

```
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
```

#### 逐词解释：
- `git`：Git命令行工具
- `remote`：操作远程仓库
- `add`：添加一个新的远程仓库
- `origin`：给这个远程仓库起的名字（约定俗成叫origin）
- `https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git`：GitHub仓库的网址

#### 翻译成人话：
"告诉Git，有一个远程仓库，名字叫origin，地址是这个GitHub网址"

#### 需要替换的内容：
- `YOUR_USERNAME` → 你的GitHub用户名

#### 举例：
如果你的GitHub用户名是 `zhangsan`，那么：
```
git remote add origin https://github.com/zhangsan/ai-storyboard-workflow.git
```

---

### 命令2：git branch -M main

```
git branch -M main
```

#### 逐词解释：
- `git`：Git命令行工具
- `branch`：操作分支
- `-M`：移动或重命名分支（相当于 --move --force）
- `main`：目标分支名称

#### 翻译成人话：
"把当前分支改名为main"

#### 为什么要这样做？
- Git以前的默认分支名是 `master`
- 现在改成了 `main`（更现代、更包容的命名）
- 这个命令确保你的分支名是 `main`

#### 注意：
如果你的分支已经是 `main`，这个命令不会有任何问题，相当于确认一下。

---

### 命令3：git push -u origin main

```
git push -u origin main
```

#### 逐词解释：
- `git`：Git命令行工具
- `push`：推送代码
- `-u`：设置上游分支（相当于 --set-upstream）
- `origin`：推送到名为origin的远程仓库
- `main`：推送本地的main分支

#### 翻译成人话：
"把本地的main分支，推送到origin这个远程仓库，并记住这个关联关系"

#### 详细解释：
1. **推送代码**：把本地main分支的所有提交，上传到GitHub
2. **-u参数的作用**：以后推送代码时，只需要输入 `git push`，Git就会自动推送到origin的main分支，不用每次都输入 `git push origin main`

#### 执行时会发生什么：
1. Git会连接GitHub
2. 如果需要认证，会提示输入用户名和密码（或Token）
3. 上传代码到GitHub
4. 显示推送成功信息

---

## 🔑 什么是GitHub Token？

### 为什么需要Token？

#### 方式1：用户名+密码（已废弃）
- 以前可以用GitHub用户名和密码推送代码
- 2021年开始，GitHub**不再支持**密码认证
- 必须使用Token

#### 方式2：SSH密钥（推荐长期使用）
- 生成一对密钥（公钥+私钥）
- 把公钥添加到GitHub
- 以后推送不需要输入密码
- 更安全，但配置稍微复杂

#### 方式3：个人访问令牌（Personal Access Token，推荐快速上手）
- 类似一个"临时密码"
- 由你生成和管理
- 有权限限制（可以控制这个Token能做什么）
- 使用简单，复制粘贴即可

### Token是什么？
- 一个长长的随机字符串，例如：
  ```
  ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- 这个字符串就是你的"新密码"
- 每次推送代码时，都要输入这个Token

---

## 🛠️ 如何创建GitHub Token？

### 详细步骤：

#### 第1步：登录GitHub
访问：https://github.com/
确保你已经登录

#### 第2步：进入设置页面
- 点击右上角的**头像**
- 在下拉菜单中，点击**"Settings"（设置）**

#### 第3步：找到Token设置
- 在左侧菜单中，向下滚动
- 找到**"Developer settings"（开发者设置）**
- 点击进入

#### 第4步：选择个人访问令牌
在开发者设置页面：
- 找到**"Personal access tokens"（个人访问令牌）**
- 点击**"Tokens (classic)"（令牌（经典））**
  - 注意：有两个选项，选择"Tokens (classic)"

#### 第5步：创建新Token
点击**"Generate new token"（生成新令牌）**按钮

#### 第6步：填写Token信息

**Note（备注）：**
- 必填项
- 填写：`AI分镜师工作流部署`
- 说明：用来区分不同的Token，方便管理

**Expiration（过期时间）：**
- 选择：`No expiration`（永不过期）或 `90 days`（90天）
- 建议：选择 `No expiration`，这样不会过期
- 如果选择过期时间，到期后需要重新创建

**Select scopes（选择权限）：**
- 勾选：`repo`（整个仓库权限）
- 这个权限包括：
  - ✅ repo:status
  - ✅ repo_deployment
  - ✅ public_repo
  - ✅ repo:invite
  - ✅ security_events

#### 第7步：生成Token
- 向下滚动到页面底部
- 点击**"Generate token"（生成令牌）**按钮

#### 第8步：复制Token（重要！）
- 生成后，你会看到一个长长的字符串
- 这是**唯一一次**显示完整的Token
- **必须立即复制！**
- 关闭页面后，就看不到了

#### ⚠️ 重要提示：
- 把Token复制到安全的地方（记事本、密码管理器等）
- 不要分享给任何人
- 不要提交到代码仓库

---

## 🚀 如何使用Token推送代码？

### 方法1：在推送时输入Token

执行命令：
```bash
git push -u origin main
```

然后会提示：
```
Username: [你的GitHub用户名]
Password: [粘贴你的Token]
```

**注意：**
- Username输入你的GitHub用户名（不是邮箱）
- **Password输入你的Token**（不是你的GitHub密码）

---

### 方法2：在URL中包含Token（推荐）

修改远程仓库URL：
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/ai-storyboard-workflow.git
```

**示例：**
- 你的GitHub用户名：`zhangsan`
- 你的Token：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

命令：
```bash
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/zhangsan/ai-storyboard-workflow.git
```

**然后再推送：**
```bash
git push -u origin main
```

这样就不需要每次都输入Token了。

---

## 📋 完整操作步骤（推荐方式）

### 假设你的GitHub用户名是 `zhangsan`

#### 步骤1：创建GitHub仓库
- 访问：https://github.com/new
- 仓库名：`ai-storyboard-workflow`
- 点击"Create repository"

#### 步骤2：配置远程仓库
```bash
git remote add origin https://github.com/zhangsan/ai-storyboard-workflow.git
```

#### 步骤3：确保分支名是main
```bash
git branch -M main
```

#### 步骤4：创建Token（如果还没有）
按照上面的详细步骤创建Token，并复制

#### 步骤5：设置Token（方法2推荐）
```bash
# 替换成你自己的Token和用户名
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/zhangsan/ai-storyboard-workflow.git
```

#### 步骤6：推送代码
```bash
git push -u origin main
```

---

## ⚠️ 常见问题

### Q1: 提示"Permission denied"（权限被拒绝）
**原因：**
- Token输入错误
- Token已过期
- Token没有正确的权限

**解决：**
- 检查Token是否正确复制
- 重新创建Token
- 确保勾选了`repo`权限

---

### Q2: 提示"remote origin already exists"（远程仓库已存在）
**原因：**
- 已经配置过origin了

**解决：**
```bash
# 查看现有的远程仓库
git remote -v

# 如果需要，先删除旧的
git remote remove origin

# 重新添加
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
```

---

### Q3: 提示"Authentication failed"（认证失败）
**原因：**
- 用户名或Token错误

**解决：**
- 确保用户名是GitHub用户名（不是邮箱）
- 确保Token正确复制
- 检查Token是否过期

---

### Q4: 提示"branch 'main' does not exist"（分支不存在）
**原因：**
- 本地没有main分支

**解决：**
```bash
# 查看当前分支
git branch

# 如果是其他分支，切换或创建main
git checkout -b main
```

---

## ✅ 成功的标志

推送成功后，你会看到：
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads.
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), done.
Total XX (delta X), reused X (delta X)
To https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
 * [new branch]      main -> main
```

然后在浏览器访问你的GitHub仓库：
```
https://github.com/YOUR_USERNAME/ai-storyboard-workflow
```

你应该能看到所有的代码文件！

---

## 📊 快速参考

| 命令 | 作用 | 需要替换 |
|------|------|---------|
| `git remote add origin [URL]` | 添加远程仓库 | YOUR_USERNAME |
| `git branch -M main` | 重命名分支为main | 无 |
| `git push -u origin main` | 推送代码到GitHub | 无 |

| 变量 | 说明 | 示例 |
|------|------|------|
| YOUR_USERNAME | GitHub用户名 | zhangsan |
| YOUR_TOKEN | GitHub个人访问令牌 | ghp_xxx... |

---

## 🎯 总结

### 这一步要做什么？
1. 把本地代码和GitHub仓库连接起来（`git remote add`）
2. 确保分支名是main（`git branch -M main`）
3. 推送代码到GitHub（`git push`）

### 关键点
- 先创建GitHub仓库
- 再配置远程仓库
- 创建Token用于认证
- 推送代码

### 预计时间
- 第一次：3-5分钟（包括创建Token）
- 以后每次：30秒-1分钟

---

## 🎉 完成！

这一步完成后，你的代码就上传到GitHub了！

**下一步：在Coze平台创建应用**

详细说明请查看：[STEP2_DETAILED_GUIDE.md](STEP2_DETAILED_GUIDE.md)

---

**预计时间：3-5分钟**
**难度：⭐⭐☆☆☆**

🎉 **完成这一步后，你的代码就在GitHub上了！**
