#!/usr/bin/env python3
"""自动部署到 GitHub Pages"""
import os
import sys
import subprocess
import requests
import json

def run_cmd(cmd, cwd=None):
    """运行命令并返回结果"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def main():
    print("\n" + "="*60)
    print("🚀 GitHub Pages 自动部署")
    print("="*60)
    
    # 获取用户信息
    print("\n📋 请准备:")
    print("   1. GitHub 用户名")
    print("   2. GitHub Personal Access Token")
    print("\n💡 如何获取 Token:")
    print("   1. 打开 https://github.com/settings/tokens")
    print("   2. 点击 'Generate new token (classic)'")
    print("   3. 勾选 'repo' 权限")
    print("   4. 点击 'Generate token'")
    print("   5. 复制生成的 token")
    print()
    
    username = input("👤 GitHub 用户名: ").strip()
    token = input("🔑 Token: ").strip()
    
    if not username or not token:
        print("❌ 用户名和 token 不能为空")
        return
    
    repo_name = "ai-tools-hub"
    site_dir = r"C:\Users\龙潜\seo-website"
    
    # 第一步: 创建仓库
    print(f"\n📦 创建仓库 {username}/{repo_name}...")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo_name,
        "description": "Best AI Tools Reviews & Comparisons",
        "private": False,
        "auto_init": False
    }
    
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ 仓库创建成功!")
    elif response.status_code == 422:
        print(f"⚠️  仓库已存在，继续...")
    else:
        print(f"❌ 创建失败: {response.status_code}")
        print(response.json().get("message", ""))
        return
    
    # 第二步: 配置远程仓库
    print(f"\n🔗 配置远程仓库...")
    
    # 删除现有 remote
    run_cmd("git remote remove origin", cwd=site_dir)
    
    # 添加新的 remote (带 token 认证)
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    success, output = run_cmd(f"git remote add origin {remote_url}", cwd=site_dir)
    
    if not success and "already exists" not in output:
        print(f"❌ 配置失败: {output}")
        return
    
    print(f"✅ 远程仓库已配置")
    
    # 第三步: 推送代码
    print(f"\n📤 推送代码...")
    
    # 确保在 main 分支
    run_cmd("git branch -M main", cwd=site_dir)
    
    # 推送
    success, output = run_cmd("git push -u origin main --force", cwd=site_dir)
    
    if success:
        print(f"✅ 代码推送成功!")
    else:
        print(f"❌ 推送失败: {output}")
        return
    
    # 第四步: 启用 GitHub Pages
    print(f"\n🌐 启用 GitHub Pages...")
    
    pages_data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    
    response = requests.put(
        f"https://api.github.com/repos/{username}/{repo_name}/pages",
        headers=headers,
        json=pages_data
    )
    
    if response.status_code in [201, 204]:
        print(f"✅ GitHub Pages 已启用!")
    else:
        print(f"⚠️  请手动启用 Pages:")
        print(f"   1. 打开 https://github.com/{username}/{repo_name}/settings/pages")
        print(f"   2. Source 选择 'main' 分支")
        print(f"   3. 点击 Save")
    
    # 完成
    site_url = f"https://{username}.github.io/{repo_name}/"
    
    print(f"\n{'='*60}")
    print(f"🎉 部署完成!")
    print(f"{'='*60}")
    print(f"\n🌐 你的网站:")
    print(f"   {site_url}")
    print(f"\n⏳ 请等待 1-5 分钟让 GitHub 完成部署")
    print(f"\n📊 包含:")
    print(f"   ✅ 20 篇 SEO 文章")
    print(f"   ✅ 专业网站设计")
    print(f"   ✅ 站点地图 (sitemap.xml)")
    print(f"   ✅ 搜索引擎优化")
    
    # 保存配置
    config = {
        "username": username,
        "repo": repo_name,
        "url": site_url
    }
    
    config_file = os.path.join(site_dir, "deploy_config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n📁 配置已保存到: {config_file}")

if __name__ == "__main__":
    main()
