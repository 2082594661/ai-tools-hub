# -*- coding: utf-8 -*-
"""给 35 个工具页添加"相关推荐"区块（同分类其他工具），插在 </main> 前。
工具页结构：<section class="tool-card" id="slug">...</section>\n        </main>
在 section 结束后、</main> 前插入推荐。
"""
import os, re, json

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 每个分类的工具列表 (slug, emoji, 名称)
GROUPS = {
    "图片处理": [
        ("qrcode", "🔳", "二维码生成器"),
        ("image-compress", "🖼️", "图片智能压缩"),
        ("watermark", "💧", "图片加水印"),
        ("art-text", "🎨", "艺术字生成器"),
        ("image-convert", "🔄", "图片格式转换"),
        ("nine-grid", "🔲", "九宫格切图"),
        ("meme-maker", "😂", "表情包制作"),
        ("image-pixelate", "👾", "图片像素化"),
        ("id-photo", "🪪", "证件照尺寸"),
    ],
    "文字处理": [
        ("word-count", "🔤", "字数统计"),
        ("text-diff", "🔍", "文本对比"),
        ("zh-convert", "🀄", "简体繁体转换"),
        ("md-to-html", "📝", "Markdown 转 HTML"),
        ("base64-convert", "🔐", "Base64 编解码"),
        ("url-encode", "🔗", "URL 编解码"),
    ],
    "开发工具": [
        ("json-formatter", "🧩", "JSON 格式化"),
        ("timestamp-convert", "⏰", "时间戳转换"),
        ("password-generator", "🎲", "随机密码生成器"),
        ("uuid-generator", "🆔", "UUID 生成器"),
        ("md5-hash", "🔏", "MD5 加密"),
        ("base-convert", "🔢", "进制转换"),
        ("regex-tester", "🧪", "正则表达式测试"),
        ("random-generator", "🎲", "随机数生成器"),
    ],
    "生活计算": [
        ("date-calc", "📅", "日期计算器"),
        ("unit-convert", "📐", "单位换算"),
        ("color-convert", "🌈", "颜色转换"),
        ("mortgage", "🏠", "房贷月供计算器"),
        ("bmi", "⚖️", "BMI 计算器"),
        ("age-calc", "🎂", "年龄计算器"),
        ("tax-calc", "🧾", "个税计算器"),
        ("timezone-convert", "🌍", "时区转换"),
        ("fuel-cost", "🚗", "油耗计算器"),
        ("due-date", "🤰", "预产期计算器"),
        ("relative-calc", "👪", "亲戚称呼计算器"),
        ("solar-term", "🌿", "节气查询"),
    ],
}

# slug -> (分类, 名称)
SLUG_GROUP = {}
SLUG_NAME = {}
for g, items in GROUPS.items():
    for slug, emoji, name in items:
        SLUG_GROUP[slug] = g
        SLUG_NAME[slug] = name

def rec_block(current_slug):
    group = SLUG_GROUP.get(current_slug)
    if not group:
        return ""
    items = GROUPS[group]
    others = [it for it in items if it[0] != current_slug]
    # 最多推荐 4 个同分类（取当前工具后面 4 个，循环）
    idx = [i for i, it in enumerate(items) if it[0] == current_slug][0]
    picks = []
    for k in range(1, len(others) + 1):
        nxt = items[(idx + k) % len(items)]
        if nxt[0] != current_slug:
            picks.append(nxt)
        if len(picks) >= 4:
            break
    links = "\n".join(
        '                    <a class="rel-card" href="{slug}.html"><span class="rc-emoji">{emoji}</span><span class="rc-name">{name}</span></a>'.format(
            slug=s, emoji=e, name=n) for s, e, n in picks
    )
    return (
        '            <section class="tool-related" aria-label="相关推荐">\n'
        '                <h2 class="tool-related-title">🧭 你可能还想用</h2>\n'
        '                <div class="rel-grid">\n' + links + '\n'
        '                </div>\n'
        '            </section>\n'
    )

tools_dir = os.path.join(ROOT, "tools")
count = 0
for slug in SLUG_GROUP:
    path = os.path.join(tools_dir, slug + ".html")
    if not os.path.exists(path):
        print("缺失:", slug)
        continue
    html = open(path, encoding="utf-8").read()
    if "tool-related" in html:
        continue  # 已有
    block = rec_block(slug)
    if not block:
        continue
    # 在 </main> 前插入（该文件只有一个 </main>）
    if "</main>" not in html:
        print("跳过(无main):", slug)
        continue
    html = html.replace("        </main>", block + "        </main>", 1)
    open(path, "w", encoding="utf-8").write(html)
    count += 1
    print("添加推荐:", slug)

print("\n共处理", count, "个工具页")
