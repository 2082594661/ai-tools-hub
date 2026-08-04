# -*- coding: utf-8 -*-
"""统一全站导航栏：首页/全部工具/更新日志/关于 + 当前页高亮。
根目录页用 ./ 前缀，tools/ 页用 ../ 前缀。
"""
import os, re, glob

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

def nav_for(page_path, current):
    """current: 当前页文件名（如 index.html / tools/qrcode.html）"""
    prefix = "../" if page_path.startswith("tools/") else ""
    def active(href, target):
        # href 是去掉前缀后的相对路径；target 是当前页的 文件名 或 目录页
        if target == "index.html" and href == "index.html":
            return ' class="active"'
        if href == target:
            return ' class="active"'
        return ""
    cur = current
    items = [
        ('index.html', '首页'),
        ('tools.html', '全部工具'),
        ('changelog.html', '更新日志'),
        ('about.html', '关于'),
    ]
    parts = []
    for href, label in items:
        parts.append('<a href="{p}{h}"{a}>{l}</a>'.format(p=prefix, h=href, a=active(href, cur), l=label))
    return '<nav>\n                ' + '\n                '.join(parts) + '\n            </nav>'

# 旧导航模式：<a href="../index.html">首页</a><a href="../index.html" class="nav-cta">🛠 小工具</a>
OLD_RE = re.compile(
    r'<nav>\s*<a href="(\.\./)?index\.html">首页</a><a href="(\.\./)?index\.html" class="nav-cta">🛠 小工具</a>\s*</nav>'
)

files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "tools", "*.html"))
changed = []
for f in files:
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    html = open(f, encoding="utf-8").read()
    if 'nav-cta' not in html:
        continue  # 已经新版导航（index/tools/changelog）
    m = OLD_RE.search(html)
    if not m:
        print("跳过(未匹配旧导航):", rel)
        continue
    new_nav = nav_for(rel, rel.split("/")[-1])
    html = OLD_RE.sub(lambda mm: new_nav, html, count=1)
    open(f, "w", encoding="utf-8").write(html)
    changed.append(rel)
    print("更新:", rel)

print("\n共更新", len(changed), "个页面")
