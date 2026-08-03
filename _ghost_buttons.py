# -*- coding: utf-8 -*-
"""批量把工具页的次级按钮（清空/复制/切换方向）改为 tool-btn-ghost"""
import io, os, re, glob

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"
GHOST_KEYWORDS = ["清空", "复制", "切换方向", "清除"]

changed = 0
for f in glob.glob(os.path.join(ROOT, "tools", "*.html")):
    html = io.open(f, encoding="utf-8").read()
    orig = html
    # 匹配 <button class="tool-btn" ...>...</button>，若按钮文本含关键词则 class 加 ghost
    def repl(m):
        global changed
        full = m.group(0)
        if any(k in full for k in GHOST_KEYWORDS):
            if "tool-btn-ghost" not in full:
                changed += 1
                return full.replace('class="tool-btn"', 'class="tool-btn tool-btn-ghost"', 1)
        return full
    html = re.sub(r'<button class="tool-btn"[^>]*>.*?</button>', repl, html, flags=re.S)
    if html != orig:
        io.open(f, "w", encoding="utf-8").write(html)
        print("✓", os.path.basename(f))
print(f"\n共修改 {changed} 个按钮")
