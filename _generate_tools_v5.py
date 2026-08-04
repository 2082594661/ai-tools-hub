# -*- coding: utf-8 -*-
"""批量生成 AI工具箱 v5 新工具页（4个）：图片像素化 / 证件照尺寸 / 亲戚称呼计算器 / 节气查询"""
import os

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 工具定义: slug, emoji, 名称, h1描述, meta description, JSON-LD描述, title, tool-body HTML, usage HTML
TOOLS = [
    # 1 图片像素化
    ("image-pixelate", "👾", "图片像素化",
     "上传图片一键转成像素风，支持调节像素块大小，生成复古游戏感图片。",
     "免费在线图片像素化工具：上传图片一键转像素风，可调节像素块大小实时预览，复古游戏风格，支持下载 PNG，浏览器本地处理不上传。",
     "免费在线图片像素化，调节像素块大小实时预览，下载 PNG，纯本地处理。",
     "图片像素化 - 免费在线像素风图片生成器（复古游戏风）",
     """
     <div class="tool-field">
       <label for="ip-file">选择图片</label>
       <input type="file" id="ip-file" accept="image/*">
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="ip-block">像素块大小</label>
         <input type="range" id="ip-block" min="2" max="32" step="1" value="10">
         <span class="tool-range-val" id="ip-block-val">10px</span>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ip-render" type="button">✨ 像素化</button>
       <button class="tool-btn tool-btn-ghost" id="ip-download" type="button">⬇️ 下载 PNG</button>
     </div>
     <div class="tool-msg" id="ip-msg" aria-live="polite"></div>
     <div class="mm-canvas-wrap" id="ip-wrap">
       <canvas id="ip-canvas" class="mm-canvas" width="600" height="400"></canvas>
     </div>
     """,
     "1. 上传一张图片<br>2. 拖动滑块调节像素块大小<br>3. 点「像素化」实时预览，「下载 PNG」保存"),

    # 2 证件照尺寸
    ("id-photo", "🪪", "证件照尺寸",
     "一键生成一寸、二寸、小一寸等标准证件照尺寸，按底色要求输出，报名考试够用。",
     "免费在线证件照尺寸工具：一键裁剪生成一寸（295x413）、二寸（413x579）、小一寸等标准尺寸证件照，可选红蓝白底色，下载 PNG，本地处理不上传。",
     "免费在线证件照尺寸，一键生成一寸二寸等标准尺寸，可选底色，纯本地处理。",
     "证件照尺寸 - 免费在线一寸二寸证件照生成器",
     """
     <div class="tool-field">
       <label for="idp-file">选择照片</label>
       <input type="file" id="idp-file" accept="image/*">
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="idp-type">证件照类型</label>
         <select id="idp-type">
           <option value="1inch" selected>一寸 295×413px（25×35mm）</option>
           <option value="small1">小一寸 260×378px（22×32mm）</option>
           <option value="2inch">二寸 413×579px（35×49mm）</option>
           <option value="small2">小二寸 390×567px（33×48mm）</option>
           <option value="passport">护照 390×567px（33×48mm）</option>
         </select>
       </div>
       <div class="tool-field">
         <label for="idp-bg">背景色</label>
         <select id="idp-bg">
           <option value="keep" selected>保持原背景</option>
           <option value="#d92b2b">红色</option>
           <option value="#2b6bd9">蓝色</option>
           <option value="#ffffff">白色</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="idp-render" type="button">✨ 生成证件照</button>
       <button class="tool-btn tool-btn-ghost" id="idp-download" type="button">⬇️ 下载 PNG</button>
     </div>
     <div class="tool-msg" id="idp-msg" aria-live="polite"></div>
     <div class="mm-canvas-wrap" id="idp-wrap">
       <canvas id="idp-canvas" class="mm-canvas" width="295" height="413"></canvas>
     </div>
     """,
     "1. 上传正面照片（人脸居中最佳）<br>2. 选证件照类型和背景色<br>3. 点「生成证件照」预览，「下载 PNG」保存"),

    # 3 亲戚称呼计算器
    ("relative-calc", "👪", "亲戚称呼计算器",
     "输入你和亲戚的关系链，比如「爸爸的爸爸」，一键算出该叫什么，过年串门不再尴尬。",
     "免费在线亲戚称呼计算器：输入关系链如「爸爸的爸爸」「妈妈的哥哥」，自动算出对应称呼，覆盖常见亲戚关系，纯前端本地计算。",
     "免费在线亲戚称呼计算器，关系链输入自动算称呼，纯本地计算。",
     "亲戚称呼计算器 - 免费在线亲戚关系称呼查询",
     """
     <div class="tool-field">
       <label for="rc-a">我的（称谓方）</label>
       <select id="rc-a">
         <option value="self" selected>我（男）</option>
         <option value="self-f">我（女）</option>
       </select>
     </div>
     <div class="tool-field">
       <label for="rc-rel">亲戚关系链（从近到远依次选）</label>
       <div id="rc-chips" class="rc-chips"></div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="rc-add" type="button">➕ 添加一步关系</button>
       <button class="tool-btn tool-btn-ghost" id="rc-clear" type="button">🗑 清空</button>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="rc-run" type="button">⚡ 计算称呼</button>
     </div>
     <div class="tool-msg" id="rc-msg" aria-live="polite"></div>
     <div class="tool-field">
       <label>结果</label>
       <div class="rc-result" id="rc-result" aria-live="polite"></div>
     </div>
     """,
     "1. 选择你的性别<br>2. 点「添加一步关系」，依次选如「爸爸」「的爸爸」<br>3. 点「计算称呼」得到结果"),

    # 4 节气查询
    ("solar-term", "🌿", "节气查询",
     "查询 2025–2030 年二十四节气具体日期，看看今天离下一个节气还有几天。",
     "免费在线节气查询工具：查询 2025-2030 年二十四节气日期，支持指定年份，显示今天到下一个节气的天数，纯前端本地计算。",
     "免费在线节气查询，2025-2030 年二十四节气日期速查，纯本地计算。",
     "节气查询 - 免费在线二十四节气日期查询",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="st-year">年份</label>
         <select id="st-year"></select>
       </div>
       <div class="tool-field">
         <label for="st-term">节气（可选）</label>
         <select id="st-term">
           <option value="" selected>全部</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="st-run" type="button">🔍 查询节气</button>
       <button class="tool-btn tool-btn-ghost" id="st-next" type="button">⏳ 下一个节气</button>
     </div>
     <div class="tool-msg" id="st-msg" aria-live="polite"></div>
     <div class="st-list" id="st-list" aria-live="polite"></div>
     """,
     "1. 选择年份（2025-2030）<br>2. 可选只看某个节气<br>3. 点「查询节气」看日期表，或「下一个节气」看今天距离"),
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
    <script src="../assets/js/tools-v5.js" defer></script>
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
