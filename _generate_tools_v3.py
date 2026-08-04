# -*- coding: utf-8 -*-
"""批量生成 AI工具箱 v3 新工具页（4个），基于 _generate_tools_v2.py 模板结构。
九宫格切图 / 正则表达式测试 / 个税计算器 / 时区转换
"""
import os

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 工具定义: slug, emoji, 名称, h1描述, meta description, JSON-LD描述, title, tool-body HTML, usage HTML
TOOLS = [
    # 1 九宫格切图
    ("nine-grid", "🔲", "九宫格切图",
     "上传一张图片，一键切成 3×3 九张，发朋友圈直接凑齐九宫格，张张清晰。",
     "免费在线九宫格切图工具：上传图片一键切成 3×3 九张，适配朋友圈九宫格发图。支持单张下载和一键下载全部，浏览器本地处理，图片不上传。",
     "免费在线九宫格切图，一键切成 3x3 九张，适配朋友圈发图，纯本地处理。",
     "九宫格切图 - 免费在线图片九宫格切割（朋友圈发图神器）",
     """
     <div class="tool-field">
       <label for="ng-file">选择图片（建议使用正方形图片，效果最佳）</label>
       <input type="file" id="ng-file" accept="image/*">
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ng-crop" type="button">🔲 切成九宫格</button>
       <button class="tool-btn tool-btn-ghost" id="ng-clear" type="button">🗑 清除</button>
     </div>
     <div class="tool-msg" id="ng-msg" aria-live="polite"></div>
     <div class="ng-grid" id="ng-grid"></div>
     <div class="tool-row" id="ng-actions" style="display:none">
       <button class="tool-btn" id="ng-download-all" type="button">⬇️ 下载全部 9 张</button>
     </div>
     """,
     "1. 点击或拖拽选择一张图片\\n2. 点「切成九宫格」自动切为 3×3\\n3. 点任意小图单独下载，或「下载全部 9 张」"),

    # 2 正则表达式测试
    ("regex-tester", "🧪", "正则表达式测试",
     "输入正则和测试文本，实时高亮所有匹配项，匹配数量、结果列表一目了然。",
     "免费在线正则表达式测试工具：输入正则和测试文本，实时高亮所有匹配项，显示匹配数量与结果列表，支持 g/i/m/s 修饰符，浏览器本地运行。",
     "免费在线正则表达式测试，实时高亮匹配项，显示匹配数量与结果列表，纯本地运行。",
     "正则表达式测试 - 免费在线正则匹配测试工具（regex tester）",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="rt-pattern">正则表达式</label>
         <input type="text" id="rt-pattern" placeholder="例如：\\d+ 或 [a-z]+" autocomplete="off">
       </div>
       <div class="tool-field">
         <label for="rt-flags">修饰符（可选）</label>
         <input type="text" id="rt-flags" placeholder="g i m s" value="g" autocomplete="off">
       </div>
     </div>
     <div class="tool-field">
       <label for="rt-input">测试文本</label>
       <textarea id="rt-input" rows="7" placeholder="在这里粘贴要匹配的文本…"></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="rt-run" type="button">⚡ 测试匹配</button>
       <button class="tool-btn tool-btn-ghost" id="rt-clear" type="button">🗑 清空</button>
     </div>
     <div class="tool-msg" id="rt-msg" aria-live="polite"></div>
     <div class="tool-field">
       <label>匹配结果</label>
       <div id="rt-output" class="rt-output" aria-live="polite"></div>
     </div>
     """,
     "1. 输入正则表达式，如 \\\\d+ 匹配数字\\n2. 粘贴测试文本，点「测试匹配」\\n3. 匹配项自动高亮，下方显示结果列表"),

    # 3 个税计算器
    ("tax-calc", "🧾", "个税计算器",
     "输入税前月薪、五险一金和专项附加扣除，快速估算每月个税与税后工资。",
     "免费在线个税计算器：输入税前月薪、五险一金个人缴纳和专项附加扣除，快速估算每月应缴个税与税后工资，支持年终奖单独计税，纯本地计算。",
     "免费在线个税计算器，估算每月个税、税后工资与年缴税额，支持年终奖，纯本地计算。",
     "个税计算器 - 免费在线个人所得税计算（税率表）",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="tc-salary">税前月薪（元）</label>
         <input type="number" id="tc-salary" value="15000" min="0" step="100">
       </div>
       <div class="tool-field">
         <label for="tc-insurance">五险一金个人缴纳（元/月）</label>
         <input type="number" id="tc-insurance" value="2500" min="0" step="100">
       </div>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="tc-deduction">专项附加扣除（元/月）</label>
         <input type="number" id="tc-deduction" value="0" min="0" step="100">
       </div>
       <div class="tool-field">
         <label for="tc-bonus">年终奖/其他（元/年）</label>
         <input type="number" id="tc-bonus" value="0" min="0" step="100">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="tc-run" type="button">⚡ 计算个税</button>
     </div>
     <div class="tool-field">
       <label>计算结果（按月预扣预缴估算）</label>
       <div class="tc-result" id="tc-result" aria-live="polite">
         <div class="wc-stat"><span class="wc-num" id="tc-tax">—</span><span class="wc-label">每月个税</span></div>
         <div class="wc-stat"><span class="wc-num" id="tc-net">—</span><span class="wc-label">税后月薪</span></div>
         <div class="wc-stat"><span class="wc-num" id="tc-rate">—</span><span class="wc-label">实际税率</span></div>
         <div class="wc-stat"><span class="wc-num" id="tc-year">—</span><span class="wc-label">年缴个税</span></div>
       </div>
     </div>
     """,
     "1. 填入税前月薪、五险一金和专项附加扣除\\n2. 有年终奖就填「年终奖」一栏\\n3. 点「计算个税」查看每月个税和税后工资"),

    # 4 时区转换
    ("timezone-convert", "🌍", "时区转换",
     "输入一个时间，一键换算北京、东京、伦敦、纽约等 14 个城市的时间，跨时区开会不再算错。",
     "免费在线时区转换工具：输入时间一键换算北京、东京、伦敦、纽约等 14 个城市时间，支持指定任意时间，浏览器本地运行，无需安装。",
     "免费在线时区转换，一键换算 14 个城市时间，支持任意时间，纯本地运行。",
     "时区转换 - 免费在线世界时间时区换算（多城市）",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="tz-datetime">要转换的时间</label>
         <input type="datetime-local" id="tz-datetime">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="tz-run" type="button">⚡ 转换时区</button>
       <button class="tool-btn tool-btn-ghost" id="tz-now" type="button">🕐 使用当前时间</button>
     </div>
     <div class="tool-field">
       <label>世界各城市时间</label>
       <div id="tz-list" class="tz-list" aria-live="polite"></div>
     </div>
     """,
     "1. 选择要转换的时间（默认当前时间）\\n2. 点「转换时区」或「使用当前时间」\\n3. 14 个城市的时间一目了然"),
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
    <script src="../assets/js/tools-v3.js" defer></script>
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
