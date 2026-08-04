#!/usr/bin/env python3
"""自动部署到 Gitee Pages"""
import os
import subprocess
import requests
import json

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def main():
    print("\n" + "=" * 60)
    print("🚀 Gitee Pages 自动部署")
    print("=" * 60)

    print("\n📋 请准备:")
    print("   1. Gitee 用户名")
    print("   2. Gitee Personal Access Token")
    print("\n💡 如何获取 Token:")
    print("   1. 打开 https://gitee.com/personal_access_tokens")
    print("   2. 点击 生成新令牌")
    print("   3. 勾选 projects 权限")
    print("   4. 点击 提交")
    print("   5. 复制生成的 token\n")

    username = input("👤 Gitee 用户名: ").strip()
    token = input("🔑 Token: ").strip()

    if not username or not token:
        print("❌ 用户名和 token 不能为空")
        return

    repo_name = "ai-tools-hub"
    site_dir = r"C:\Users\龙潜\seo-website"

    # 创建仓库
    print(f"\n📦 创建仓库 {username}/{repo_name}...")
    headers = {"Content-Type": "application/json"}
    data = {
        "name": repo_name,
        "description": "Best AI Tools Reviews & Comparisons",
        "private": False,
        "auto_init": False
    }
    api_url = "https://gitee.com/api/v5/user/repos?access_token=" + token
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ 仓库创建成功!")
    elif response.status_code == 422:
        print("⚠️  仓库已存在，继续...")
    else:
        print(f"❌ 创建失败: {response.status_code}")
        print(response.json().get("message", ""))
        return

    # 配置远程仓库
    print("\n🔗 配置远程仓库...")
    run_cmd("git remote remove origin", cwd=site_dir)
    remote_url = "https://" + username + ":" + token + "@gitee.com/" + username + "/" + repo_name + ".git"
    success, output = run_cmd("git remote add origin " + remote_url, cwd=site_dir)
    if not success and "already exists" not in output:
        print(f"❌ 配置失败: {output}")
        return
    print("✅ 远程仓库已配置")

    # 推送代码
    print("\n📤 推送代码...")
    run_cmd("git branch -M main", cwd=site_dir)
    success, output = run_cmd("git push -u origin main --force", cwd=site_dir)
    if success:
        print("✅ 代码推送成功!")
    else:
        print(f"❌ 推送失败: {output}")
        return

    # 完成
    site_url = "https://" + username + ".gitee.io/" + repo_name + "/"
    print("\n" + "=" * 60)
    print("🎉 部署完成!")
    print("=" * 60)
    print(f"\n🌐 你的网站:\n   {site_url}")
    print("\n⚠️  还需要手动启用 Gitee Pages:")
    print(f"   1. 打开 https://gitee.com/{username}/{repo_name}/pages")
    print("   2. 点击 启动")
    print("   3. 选择 main 分支")
    print("   4. 点击 部署")
    print("\n⏳ 等待 1-5 分钟后即可访问")

    config = {"username": username, "repo": repo_name, "url": site_url}
    with open(os.path.join(site_dir, "deploy_config.json"), "w") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
