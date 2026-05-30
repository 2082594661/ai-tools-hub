#!/bin/bash
# GitHub Pages 推送脚本
# 使用前请确保已创建 GitHub 仓库

echo "=========================================="
echo "🚀 GitHub Pages 推送脚本"
echo "=========================================="

# 检查是否已配置远程仓库
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "⚠️  还未配置远程仓库"
    echo ""
    echo "请先在 GitHub 创建仓库:"
    echo "1. 打开 https://github.com/new"
    echo "2. 仓库名: ai-tools-hub (或你喜欢的名字)"
    echo "3. 选择 Public"
    echo "4. 不要勾选任何初始化选项"
    echo "5. 点击 Create repository"
    echo ""
    echo "然后运行:"
    echo "git remote add origin https://github.com/你的用户名/ai-tools-hub.git"
    echo ""
    exit 1
fi

echo ""
echo "📤 推送到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功!"
    echo ""
    echo "📋 下一步: 启用 GitHub Pages"
    echo "1. 打开你的仓库页面"
    echo "2. 点击 Settings"
    echo "3. 左侧菜单找到 Pages"
    echo "4. Source 选择 'main' 分支"
    echo "5. 点击 Save"
    echo ""
    echo "🌐 几分钟后，你的网站将在以下地址可用:"
    echo "https://你的用户名.github.io/仓库名/"
else
    echo ""
    echo "❌ 推送失败"
    echo "请检查网络连接和仓库权限"
fi
