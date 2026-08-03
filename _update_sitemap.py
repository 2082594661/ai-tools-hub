# -*- coding: utf-8 -*-
"""更新 sitemap.xml + sitemap.html，加入 12 个新工具页"""
import io, os, re

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"
TODAY = "2026-08-03"

NEW_TOOLS = [
    ("word-count", "🔤 字数统计"),
    ("json-formatter", "🧩 JSON 格式化"),
    ("base64-convert", "🔐 Base64 编解码"),
    ("url-encode", "🔗 URL 编解码"),
    ("timestamp-convert", "⏰ 时间戳转换"),
    ("password-generator", "🎲 随机密码生成器"),
    ("uuid-generator", "🆔 UUID 生成器"),
    ("md5-hash", "🔏 MD5 加密"),
    ("zh-convert", "🀄 简体繁体转换"),
    ("md-to-html", "📝 Markdown 转 HTML"),
    ("image-convert", "🔄 图片格式转换"),
    ("age-calc", "🎂 年龄计算器"),
]

# 1) sitemap.xml
xml_path = os.path.join(ROOT, "sitemap.xml")
xml = io.open(xml_path, encoding="utf-8").read()
blocks = []
for slug, _ in NEW_TOOLS:
    blocks.append("""  <url>
    <loc>https://aifunnyplay.cn/tools/%s.html</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>""" % (slug, TODAY))
insert = "\n" + "\n".join(blocks) + "\n"
assert "</urlset>" in xml
xml = xml.replace("</urlset>", insert + "</urlset>")
io.open(xml_path, "w", encoding="utf-8").write(xml)
print("sitemap.xml: 新增 %d 条, 共 %d 条" % (len(NEW_TOOLS), xml.count("<loc>")))

# 2) sitemap.html
html_path = os.path.join(ROOT, "sitemap.html")
html = io.open(html_path, encoding="utf-8").read()
lis = []
for slug, label in NEW_TOOLS:
    lis.append('                    <li><a href="tools/%s.html">%s</a></li>' % (slug, label))
# 在 </ul> 前插入（小工具 section 的最后一个 </ul>）
marker = "                    </ul>"
idx = html.rfind(marker)
assert idx != -1
insert_html = "\n".join(lis) + "\n" + marker
html = html[:idx] + insert_html + html[idx + len(marker):]
io.open(html_path, "w", encoding="utf-8").write(html)
print("sitemap.html: 已追加 %d 个工具链接" % len(NEW_TOOLS))
