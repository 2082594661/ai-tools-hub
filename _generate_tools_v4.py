# -*- coding: utf-8 -*-
"""批量生成 AI工具箱 v4 新工具页（4个）：油耗计算器 / 预产期计算器 / 随机数生成器 / 表情包制作"""
import os

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 工具定义: slug, emoji, 名称, h1描述, meta description, JSON-LD描述, title, tool-body HTML, usage HTML
TOOLS = [
    # 1 油耗计算器
    ("fuel-cost", "🚗", "油耗计算器",
     "输入里程和加油量，算出百公里油耗和每公里油费，养车开销一目了然。",
     "免费在线油耗计算器：输入行驶里程、加油升数和油价，一键算出百公里油耗、每公里油费、总油费，纯前端本地计算，数据不上传。",
     "免费在线油耗计算器，算百公里油耗、每公里油费与总油费，纯本地计算。",
     "油耗计算器 - 免费在线算百公里油耗/油费（养车必备）",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="fc-km">行驶里程（公里）</label>
         <input type="number" id="fc-km" value="500" min="0" step="1">
       </div>
       <div class="tool-field">
         <label for="fc-liters">耗油量（升）</label>
         <input type="number" id="fc-liters" value="35" min="0" step="0.1">
       </div>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="fc-price">油价（元/升，可选）</label>
         <input type="number" id="fc-price" value="7.5" min="0" step="0.01">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="fc-run" type="button">⚡ 计算油耗</button>
     </div>
     <div class="tool-field">
       <label>计算结果</label>
       <div class="fc-result" id="fc-result" aria-live="polite">
         <div class="wc-stat"><span class="wc-num" id="fc-hundred">—</span><span class="wc-label">百公里油耗</span></div>
         <div class="wc-stat"><span class="wc-num" id="fc-per-km">—</span><span class="wc-label">每公里油费</span></div>
         <div class="wc-stat"><span class="wc-num" id="fc-total">—</span><span class="wc-label">总油费</span></div>
       </div>
     </div>
     """,
     "1. 填入行驶里程和耗油量（两次加油间的数据最准）<br>2. 可选填油价算油费<br>3. 点「计算油耗」看结果"),

    # 2 预产期计算器
    ("due-date", "🤰", "预产期计算器",
     "输入末次月经日期，自动推算预产期、当前孕周和已孕天数，孕期规划更安心。",
     "免费在线预产期计算器：输入末次月经第一天，自动推算预产期（约 40 周）、当前孕周和已孕天数，纯前端本地计算，隐私安全。",
     "免费在线预产期计算器，推预产期、当前孕周与已孕天数，纯本地计算。",
     "预产期计算器 - 免费在线推算孕周与预产期",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="dd-lmp">末次月经第一天</label>
         <input type="date" id="dd-lmp">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="dd-run" type="button">⚡ 计算预产期</button>
     </div>
     <div class="tool-field">
       <label>计算结果</label>
       <div class="dd-result" id="dd-result" aria-live="polite">
         <div class="wc-stat"><span class="wc-num" id="dd-due">—</span><span class="wc-label">预产期</span></div>
         <div class="wc-stat"><span class="wc-num" id="dd-week">—</span><span class="wc-label">当前孕周</span></div>
         <div class="wc-stat"><span class="wc-num" id="dd-days">—</span><span class="wc-label">已孕天数</span></div>
         <div class="wc-stat"><span class="wc-num" id="dd-remain">—</span><span class="wc-label">距离预产期</span></div>
       </div>
     </div>
     """,
     "1. 选择末次月经第一天<br>2. 点「计算预产期」<br>3. 查看预产期（末次月经 + 280 天）和当前孕周"),

    # 3 随机数生成器
    ("random-generator", "🎲", "随机数生成器",
     "在指定范围内生成 1 到多个随机数，支持去重、排序，抽奖选题都好用。",
     "免费在线随机数生成器：自定义范围生成 1 到 100 个随机数，支持不重复、升序/降序，一键复制，纯前端本地生成。",
     "免费在线随机数生成器，范围自定、去重、排序、一键复制，纯本地生成。",
     "随机数生成器 - 免费在线随机抽数/抽奖工具",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="rg-min">最小值</label>
         <input type="number" id="rg-min" value="1" step="1">
       </div>
       <div class="tool-field">
         <label for="rg-max">最大值</label>
         <input type="number" id="rg-max" value="100" step="1">
       </div>
       <div class="tool-field">
         <label for="rg-count">生成个数</label>
         <input type="number" id="rg-count" value="5" min="1" max="100" step="1">
       </div>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="rg-unique">不重复</label>
         <select id="rg-unique">
           <option value="1" selected>是（每个数只出现一次）</option>
           <option value="0">否（允许重复）</option>
         </select>
       </div>
       <div class="tool-field">
         <label for="rg-sort">排序</label>
         <select id="rg-sort">
           <option value="none" selected>不排序</option>
           <option value="asc">升序</option>
           <option value="desc">降序</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="rg-run" type="button">🎲 生成随机数</button>
       <button class="tool-btn tool-btn-ghost" id="rg-copy" type="button">📋 复制结果</button>
     </div>
     <div class="tool-msg" id="rg-msg" aria-live="polite"></div>
     <div class="rg-output" id="rg-output" aria-live="polite"></div>
     """,
     "1. 设置范围（最小/最大）和生成个数<br>2. 可选「不重复」「排序」<br>3. 点「生成随机数」，可一键复制"),

    # 4 表情包制作
    ("meme-maker", "😂", "表情包制作",
     "上传图片，加上顶行和底行文字，一键生成专属表情包并下载。",
     "免费在线表情包制作工具：上传图片添加顶部/底部文字，实时预览，一键下载 PNG，支持调整字号和文字颜色，浏览器本地处理不上传。",
     "免费在线表情包制作，图片加顶底文字实时预览，一键下载，纯本地处理。",
     "表情包制作 - 免费在线图片加字表情包生成器",
     """
     <div class="tool-field">
       <label for="mm-file">选择图片</label>
       <input type="file" id="mm-file" accept="image/*">
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="mm-top">顶部文字</label>
         <input type="text" id="mm-top" placeholder="顶行文字…" autocomplete="off">
       </div>
       <div class="tool-field">
         <label for="mm-bottom">底部文字</label>
         <input type="text" id="mm-bottom" placeholder="底行文字…" autocomplete="off">
       </div>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="mm-size">字号（相对图片）</label>
         <input type="range" id="mm-size" min="0.06" max="0.18" step="0.01" value="0.1">
       </div>
       <div class="tool-field">
         <label for="mm-color">文字颜色</label>
         <input type="color" id="mm-color" value="#ffffff">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="mm-render" type="button">✨ 生成表情包</button>
       <button class="tool-btn tool-btn-ghost" id="mm-download" type="button">⬇️ 下载 PNG</button>
     </div>
     <div class="tool-msg" id="mm-msg" aria-live="polite"></div>
     <div class="mm-canvas-wrap" id="mm-wrap">
       <canvas id="mm-canvas" class="mm-canvas" width="800" height="600"></canvas>
     </div>
     """,
     "1. 上传一张图片<br>2. 填顶行/底行文字，可调字号和颜色<br>3. 点「生成表情包」预览，「下载 PNG」保存"),
]

HEAD_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#c45d3a">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="baidu_union_verify" content="12c06fb585923e45afa002468feead30">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="icon" href="../favicon.svg" type="image/svg+xml">
    <link rel="canonical" href="https://aifunnyplay.cn/tools/{slug}.html">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://aifunnyplay.cn/tools/{slug}.html">
    <meta property="og:image" content="https://aifunnyplay.cn/default-og.png">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "{name}",
      "description": "{ld_desc}",
      "applicationCategory": "UtilitiesApplication",
      "operatingSystem": "Any",
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "CNY" }}
    }}
    </script>
</head>
"""

BODY_HEAD = """<body>
    <a class="skip-link" href="#main">跳到主内容</a>
    <header class="site-header">
        <div class="container">
            <a href="../index.html" class="site-title">AI工具箱</a>
            <nav>
                <a href="../index.html">首页</a><a href="../index.html" class="nav-cta">🛠 小工具</a>
            </nav>
        </div>
    </header>
    <div class="ad-slot ad-top" id="ad-top"></div>
    <div class="container">
        <main id="main" class="static-page tool-page">
            <section class="tool-card" id="{slug}">
                <nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a><span class="sep" aria-hidden="true">›</span><span>{name}</span></nav>
                <div class="tool-head">
                    <span class="tool-emoji">{emoji}</span>
                    <div>
                        <h1>{name}</h1>
                        <p class="tool-desc">{h1_desc}</p>
                    </div>
                </div>
                <div class="tool-body">
{body}
                    <div class="tool-usage">
                        <strong>💡 怎么用：</strong>{usage}
                    </div>
                </div>
            </section>
        </main>
    </div>
"""

FOOT = """    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>导航</h4>
                    <ul>
                        <li><a href="../index.html">首页</a></li>
                        <li><a href="../about.html">关于本站</a></li>
                        <li><a href="../links.html">友情链接</a></li>
                        <li><a href="../contact.html">联系我</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>相关说明</h4>
                    <ul>
                        <li><a href="../privacy.html">隐私政策</a></li>
                        <li><a href="../disclaimer.html">免责声明</a></li>
                        <li><a href="../links.html">友情链接</a></li>
                        <li><a href="../sitemap.html">站点地图</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 AI工具箱 | 个人维护的非商业网站</p>
                <p class="beian"><a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow" class="beian">京ICP备2026032489号-1</a>&nbsp;&nbsp;<img width="16" height="18" src="../assets/images/gongan.png" alt="公安备案" style="width:16px;vertical-align:middle;margin-right:2px"><a href="https://beian.mps.gov.cn/#/query/webSearch?code=11011402056201" rel="noreferrer" target="_blank" class="beian">京公网安备11011402056201号</a></p>
            </div>
        </div>
        <div class="ad-slot ad-footer" id="ad-footer"></div>
    </footer>
    <script src="../assets/js/tools-v4.js" defer></script>
    <script src="../assets/js/site.js" defer></script>
</body>
</html>
"""

def build(meta):
    slug, emoji, name, h1_desc, desc, ld_desc, title, body, usage = meta
    parts = []
    parts.append(HEAD_TPL.format(
        title=title,
        desc=desc, slug=slug, og_title=name + " - 免费在线工具",
        name=name, ld_desc=ld_desc))
    parts.append(BODY_HEAD.format(slug=slug, name=name, emoji=emoji, h1_desc=h1_desc, body=body, usage=usage))
    parts.append(FOOT)
    return "".join(parts)

if __name__ == "__main__":
    tools_dir = os.path.join(ROOT, "tools")
    for meta in TOOLS:
        slug = meta[0]
        path = os.path.join(tools_dir, slug + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(meta))
        print("生成:", slug + ".html")
