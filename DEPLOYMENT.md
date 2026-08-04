# GitHub Pages 部署指南

## 📋 你需要做的事

### 1️⃣ 创建 GitHub 账号 (如果没有)

访问 https://github.com/signup 注册

### 2️⃣ 创建新仓库

1. 打开 https://github.com/new
2. 填写:
   - **Repository name**: `ai-tools-hub`
   - **Description**: `Best AI Tools Reviews & Comparisons`
   - **Public** (免费必须选 Public)
   - **不要勾选**任何初始化选项 (不要 README, .gitignore, license)
3. 点击 **Create repository**

### 3️⃣ 连接本地仓库

创建仓库后，GitHub 会显示推送命令。复制并运行:

```bash
cd C:\Users\龙潜\seo-website
git remote add origin https://github.com/你的用户名/ai-tools-hub.git
git branch -M main
git push -u origin main
```

### 4️⃣ 启用 GitHub Pages

1. 打开你的仓库: `https://github.com/你的用户名/ai-tools-hub`
2. 点击 **Settings** (设置)
3. 左侧菜单找到 **Pages**
4. **Source** 选择 `main` 分支
5. 点击 **Save**

### 5️⃣ 等待部署

通常 1-5 分钟后，你的网站会在这里:
```
https://你的用户名.github.io/ai-tools-hub/
```

---

## 🎯 完成后你将拥有

✅ 20 篇 SEO 优化文章
✅ 专业网站设计
✅ 自动站点地图 (sitemap.xml)
✅ 搜索引擎优化
✅ 完全免费托管

---

## 📈 下一步: 自定义域名 (可选)

如果你有自己的域名:

1. 在仓库创建文件 `CNAME`，内容为你的域名
2. 在域名 DNS 设置:
   - 添加 CNAME 记录: `你的用户名.github.io`
3. 在 GitHub Pages 设置中启用 HTTPS

---

## ❓ 常见问题

**Q: 为什么选 Public?**
A: GitHub Pages 免费版必须是 Public 仓库

**Q: 能用自定义域名吗?**
A: 可以! 详见上面的自定义域名步骤

**Q: 怎么更新文章?**
A: 修改文件后:
```bash
git add .
git commit -m "Update articles"
git push
```

**Q: 怎么添加 Google Analytics?**
A: 在 HTML 模板中添加 Google Analytics 代码

---

## 🔧 本地预览

安装 Python HTTP 服务器:
```bash
cd C:\Users\龙潜\seo-website
python -m http.server 8000
```

然后打开: http://localhost:8000
