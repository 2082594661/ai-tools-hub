# -*- coding: utf-8 -*-
"""批量生成 AI工具箱 v2 新工具页（12个），基于 qrcode.html 模板结构。"""
import os, io

ROOT = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 工具定义: slug, emoji, 名称, h1描述, meta description, JSON-LD描述, tool-body HTML, usage HTML
TOOLS = [
    # 1 字数统计
    ("word-count", "🔤", "字数统计",
     "实时统计文本的字数、字符数、行数、段落数和阅读时间，中文英文都准确。",
     "免费在线字数统计工具：实时统计中文字数、英文字数、字符数、行数、段落数和预计阅读时间，支持复制粘贴，全程浏览器本地运行，不上传任何文本。",
     "免费在线统计文本字数、字符数、行数、段落数，实时计算阅读时间，纯本地运行。",
     """
     <div class="tool-field">
       <label for="wc-input">输入要统计的文本（直接粘贴即可，实时统计）</label>
       <textarea id="wc-input" rows="8" placeholder="在这里粘贴或输入文字，下方会实时显示统计结果…"></textarea>
     </div>
     <div class="wc-stats" id="wc-stats" aria-live="polite">
       <div class="wc-stat"><span class="wc-num" id="wc-words">0</span><span class="wc-label">字数</span></div>
       <div class="wc-stat"><span class="wc-num" id="wc-chars">0</span><span class="wc-label">字符数（含空格）</span></div>
       <div class="wc-stat"><span class="wc-num" id="wc-chars-no">0</span><span class="wc-label">字符数（不含空格）</span></div>
       <div class="wc-stat"><span class="wc-num" id="wc-lines">0</span><span class="wc-label">行数</span></div>
       <div class="wc-stat"><span class="wc-num" id="wc-paras">0</span><span class="wc-label">段落数</span></div>
       <div class="wc-stat"><span class="wc-num" id="wc-readtime">0分钟</span><span class="wc-label">预计阅读时间</span></div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="wc-clear" type="button">🗑 清空</button>
     </div>
     """,
     "1. 在输入框粘贴或输入任意文字\n2. 统计结果实时更新\n3. 点「清空」一键重置"),

    # 2 JSON 格式化
    ("json-formatter", "🧩", "JSON 格式化",
     "一键格式化、压缩和校验 JSON 数据，错误位置高亮提示，开发者必备。",
     "免费在线 JSON 格式化工具：格式化、压缩、校验 JSON，实时显示解析错误及位置，支持大段数据粘贴，浏览器本地处理，不上传数据。",
     "免费在线格式化、压缩和校验 JSON，解析错误带位置提示，纯本地运行。",
     """
     <div class="tool-field">
       <label for="jf-input">输入 JSON 内容</label>
       <textarea id="jf-input" rows="8" placeholder='{"name": "AI工具箱", "tools": ["字数统计", "JSON格式化"]}'></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="jf-format" type="button">✨ 格式化</button>
       <button class="tool-btn" id="jf-minify" type="button">📦 压缩</button>
       <button class="tool-btn" id="jf-validate" type="button">✅ 校验</button>
     </div>
     <div class="tool-field">
       <label for="jf-output">结果（只读）</label>
       <textarea id="jf-output" rows="8" readonly placeholder="格式化/压缩后的结果会显示在这里"></textarea>
     </div>
     <div class="tool-field">
       <button class="tool-btn" id="jf-copy" type="button">📋 复制结果</button>
     </div>
     <div class="tool-msg" id="jf-msg" aria-live="polite"></div>
     """,
     "1. 粘贴 JSON 数据\n2. 点「格式化」排版或「压缩」去空格\n3. 点「校验」检查语法，错误会提示位置"),

    # 3 Base64 编解码
    ("base64-convert", "🔐", "Base64 编解码",
     "文本与 Base64 互转，支持中文、UTF-8，一键编码解码，本地处理安全。",
     "免费在线 Base64 编解码工具：文本转 Base64、Base64 转文本，完美支持中文和 UTF-8，一键复制结果，浏览器本地处理，数据不上传。",
     "免费在线 Base64 编码解码，支持中文 UTF-8，一键互转，纯本地运行。",
     """
     <div class="tool-field">
       <label for="b64-mode">转换方向</label>
       <select id="b64-mode">
         <option value="encode" selected>文本 → Base64 编码</option>
         <option value="decode">Base64 → 文本 解码</option>
       </select>
     </div>
     <div class="tool-field">
       <label for="b64-input">输入内容</label>
       <textarea id="b64-input" rows="6" placeholder="输入要编码的文本，或要解码的 Base64 字符串"></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="b64-run" type="button">⚡ 转换</button>
       <button class="tool-btn" id="b64-swap" type="button">🔄 切换方向</button>
     </div>
     <div class="tool-field">
       <label for="b64-output">结果（只读）</label>
       <textarea id="b64-output" rows="6" readonly placeholder="转换结果会显示在这里"></textarea>
     </div>
     <div class="tool-field">
       <button class="tool-btn" id="b64-copy" type="button">📋 复制结果</button>
     </div>
     <div class="tool-msg" id="b64-msg" aria-live="polite"></div>
     """,
     "1. 选择「编码」或「解码」方向\n2. 输入文本或 Base64\n3. 点「转换」，结果自动出现在下方"),

    # 4 URL 编解码
    ("url-encode", "🔗", "URL 编解码",
     "URL 编码与解码，支持中文和特殊字符，解决乱码问题，一键转换。",
     "免费在线 URL 编解码工具：中文、空格、特殊字符一键 URL 编码或解码，解决链接乱码问题，支持完整编码模式，浏览器本地处理。",
     "免费在线 URL 编码解码，中文特殊字符一键转换，纯本地运行。",
     """
     <div class="tool-field">
       <label for="ue-mode">转换方向</label>
       <select id="ue-mode">
         <option value="encode" selected>文本 → URL 编码</option>
         <option value="decode">URL → 文本 解码</option>
       </select>
     </div>
     <div class="tool-field">
       <label for="ue-input">输入内容</label>
       <textarea id="ue-input" rows="6" placeholder="例如：https://aifunnyplay.cn/?q=中文 空格 测试"></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ue-run" type="button">⚡ 转换</button>
       <button class="tool-btn" id="ue-swap" type="button">🔄 切换方向</button>
     </div>
     <div class="tool-field">
       <label for="ue-output">结果（只读）</label>
       <textarea id="ue-output" rows="6" readonly placeholder="转换结果会显示在这里"></textarea>
     </div>
     <div class="tool-field">
       <button class="tool-btn" id="ue-copy" type="button">📋 复制结果</button>
     </div>
     <div class="tool-msg" id="ue-msg" aria-live="polite"></div>
     """,
     "1. 选择「编码」或「解码」\n2. 输入内容\n3. 点「转换」，结果自动出现并可复制"),

    # 5 时间戳转换
    ("timestamp-convert", "⏰", "时间戳转换",
     "Unix 时间戳与日期时间互转，支持秒和毫秒，多种格式显示，程序员神器。",
     "免费在线时间戳转换工具：Unix 时间戳秒/毫秒与日期时间互转，支持本地时间和 UTC 显示，一键获取当前时间戳，浏览器本地运行。",
     "免费在线 Unix 时间戳与日期互转，支持秒/毫秒，多种格式，纯本地运行。",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="ts-input">时间戳</label>
         <input type="number" id="ts-input" placeholder="例如 1754208000">
       </div>
       <div class="tool-field">
         <label for="ts-unit">单位</label>
         <select id="ts-unit">
           <option value="s" selected>秒（10位）</option>
           <option value="ms">毫秒（13位）</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ts-convert" type="button">⚡ 转日期</button>
       <button class="tool-btn" id="ts-now" type="button">🕐 当前时间戳</button>
     </div>
     <div class="tool-field">
       <label for="ts-output">转换结果（只读）</label>
       <textarea id="ts-output" rows="5" readonly placeholder="日期时间、UTC、ISO 格式会显示在这里"></textarea>
     </div>
     """,
     "1. 输入时间戳数字，选择秒或毫秒\n2. 点「转日期」查看多种格式\n3. 点「当前时间戳」获取现在的时间"),

    # 6 随机密码生成
    ("password-generator", "🎲", "随机密码生成器",
     "生成高强度随机密码，自定义长度和字符集，实时显示强度，一键复制。",
     "免费在线随机密码生成器：自定义长度、大写小写数字符号任意组合，实时密码强度检测，一键复制，浏览器本地生成，不经过任何服务器。",
     "免费在线生成高强度随机密码，自定义字符集与长度，实时强度检测，纯本地生成。",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="pg-length">密码长度：<span id="pg-length-val">16</span></label>
         <input type="range" id="pg-length" min="4" max="64" value="16">
       </div>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label><input type="checkbox" id="pg-upper" checked> 大写字母 A-Z</label>
         <label><input type="checkbox" id="pg-lower" checked> 小写字母 a-z</label>
         <label><input type="checkbox" id="pg-digit" checked> 数字 0-9</label>
         <label><input type="checkbox" id="pg-symbol" checked> 符号 !@#$%</label>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="pg-gen" type="button">⚡ 生成密码</button>
       <button class="tool-btn" id="pg-copy" type="button">📋 复制</button>
     </div>
     <div class="tool-field">
       <label for="pg-output">生成的密码（只读）</label>
       <input type="text" id="pg-output" readonly placeholder="点击生成">
     </div>
     <div class="tool-msg" id="pg-strength" aria-live="polite"></div>
     """,
     "1. 拖动滑块设置密码长度\n2. 勾选需要的字符类型\n3. 点「生成密码」，看强度提示后复制"),

    # 7 UUID 生成器
    ("uuid-generator", "🆔", "UUID 生成器",
     "批量生成 UUID v4 唯一标识符，支持多种格式，一键复制全部。",
     "免费在线 UUID 生成器：批量生成 UUID v4，支持带横线/不带横线/大写格式，最多一次生成 100 个，一键复制全部，浏览器本地生成。",
     "免费在线批量生成 UUID v4，多种格式可选，一键复制，纯本地生成。",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="ug-count">生成数量：<span id="ug-count-val">5</span></label>
         <input type="range" id="ug-count" min="1" max="100" value="5">
       </div>
       <div class="tool-field">
         <label for="ug-format">格式</label>
         <select id="ug-format">
           <option value="std" selected>标准（带横线）</option>
           <option value="plain">无横线</option>
           <option value="upper">大写</option>
           <option value="braces">花括号</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ug-gen" type="button">⚡ 生成 UUID</button>
       <button class="tool-btn" id="ug-copy" type="button">📋 复制全部</button>
     </div>
     <div class="tool-field">
       <label for="ug-output">生成的 UUID（只读）</label>
       <textarea id="ug-output" rows="6" readonly placeholder="生成的 UUID 列表会显示在这里"></textarea>
     </div>
     """,
     "1. 拖动滑块设置生成数量\n2. 选择输出格式\n3. 点「生成 UUID」，可一键复制全部"),

    # 8 MD5 哈希
    ("md5-hash", "🔏", "MD5 加密",
     "在线计算文本 MD5 哈希值，支持 32 位/16 位、大小写输出，本地计算安全。",
     "免费在线 MD5 加密工具：计算文本 MD5 哈希值，支持 32 位小写、32 位大写、16 位输出，全程浏览器本地计算，不上传任何内容。",
     "免费在线计算文本 MD5 哈希，32位/16位、大小写可选，纯本地计算。",
     """
     <div class="tool-field">
       <label for="md5-input">输入文本</label>
       <textarea id="md5-input" rows="6" placeholder="输入要计算 MD5 的文本…"></textarea>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="md5-format">输出格式</label>
         <select id="md5-format">
           <option value="32lower" selected>32 位小写</option>
           <option value="32upper">32 位大写</option>
           <option value="16lower">16 位小写</option>
           <option value="16upper">16 位大写</option>
         </select>
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="md5-run" type="button">⚡ 计算 MD5</button>
       <button class="tool-btn" id="md5-copy" type="button">📋 复制</button>
     </div>
     <div class="tool-field">
       <label for="md5-output">MD5 结果（只读）</label>
       <input type="text" id="md5-output" readonly placeholder="计算结果会显示在这里">
     </div>
     """,
     "1. 输入任意文本\n2. 选择输出格式\n3. 点「计算 MD5」获取哈希值"),

    # 9 繁体简体转换
    ("zh-convert", "🀄", "简体繁体转换",
     "简体中文与繁体中文一键互转，常用词组精准转换，支持批量文本。",
     "免费在线简体繁体转换工具：简体转繁体、繁体转简体一键完成，常用词组精准转换，支持长文本批量处理，浏览器本地运行。",
     "免费在线简繁互转工具，词组级精准转换，批量处理长文本，纯本地运行。",
     """
     <div class="tool-field">
       <label for="zh-mode">转换方向</label>
       <select id="zh-mode">
         <option value="s2t" selected>简体 → 繁体</option>
         <option value="t2s">繁体 → 简体</option>
       </select>
     </div>
     <div class="tool-field">
       <label for="zh-input">输入文本</label>
       <textarea id="zh-input" rows="8" placeholder="输入要转换的中文文本…"></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="zh-run" type="button">⚡ 转换</button>
       <button class="tool-btn" id="zh-swap" type="button">🔄 切换方向</button>
     </div>
     <div class="tool-field">
       <label for="zh-output">结果（只读）</label>
       <textarea id="zh-output" rows="8" readonly placeholder="转换结果会显示在这里"></textarea>
     </div>
     <div class="tool-field">
       <button class="tool-btn" id="zh-copy" type="button">📋 复制结果</button>
     </div>
     """,
     "1. 选择「简体转繁体」或「繁体转简体」\n2. 粘贴文本\n3. 点「转换」并复制结果"),

    # 10 Markdown 转 HTML
    ("md-to-html", "📝", "Markdown 转 HTML",
     "Markdown 实时转 HTML，支持标题、列表、代码块、表格，双栏预览。",
     "免费在线 Markdown 转 HTML 工具：支持标题、粗体、链接、列表、代码块、引用、表格等语法，实时预览，一键复制 HTML 源码，本地转换。",
     "免费在线 Markdown 转 HTML，支持常用语法与表格，实时预览，纯本地转换。",
     """
     <div class="tool-field">
       <label for="md-input">Markdown 内容（输入后自动转换）</label>
       <textarea id="md-input" rows="10" placeholder="# 标题&#10;&#10;支持 **粗体**、*斜体*、[链接](https://aifunnyplay.cn)、列表、代码块等"></textarea>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="md-copy-html" type="button">📋 复制 HTML</button>
       <button class="tool-btn" id="md-copy-md" type="button">🗑 清空</button>
     </div>
     <div class="tool-field">
       <label for="md-output">生成的 HTML（只读）</label>
       <textarea id="md-output" rows="8" readonly placeholder="转换出的 HTML 源码会显示在这里"></textarea>
     </div>
     <div class="tool-field">
       <label>实时预览</label>
       <div class="md-preview" id="md-preview"></div>
     </div>
     """,
     "1. 左侧输入 Markdown，自动实时转换\n2. 上方查看 HTML 源码\n3. 下方是渲染后的预览效果"),

    # 11 图片格式转换
    ("image-convert", "🔄", "图片格式转换",
     "PNG、JPG、WebP 互转，可调质量，批量预览下载，本地转换不压缩画质。",
     "免费在线图片格式转换工具：PNG、JPG、WebP 一键互转，可调节图片质量，支持批量上传，浏览器本地转换，图片不上传服务器。",
     "免费在线 PNG/JPG/WebP 图片格式互转，可调质量，支持批量，纯本地转换。",
     """
     <div class="tool-field">
       <label for="ic-file">选择图片（支持 PNG / JPG / WebP，可多选）</label>
       <div class="ic-drop" id="ic-drop" role="button" tabindex="0" aria-label="点击或拖拽上传图片">
         <p>📁 点击选择或拖拽图片到这里</p>
       </div>
       <input type="file" id="ic-file" accept="image/*" multiple hidden>
     </div>
     <div class="tool-row">
       <div class="tool-field">
         <label for="ic-format">输出格式</label>
         <select id="ic-format">
           <option value="image/png">PNG（无损）</option>
           <option value="image/jpeg">JPG（有损）</option>
           <option value="image/webp">WebP（推荐）</option>
         </select>
       </div>
       <div class="tool-field">
         <label for="ic-quality">质量：<span id="ic-quality-val">90</span></label>
         <input type="range" id="ic-quality" min="10" max="100" value="90">
       </div>
     </div>
     <div class="tool-msg" id="ic-msg" aria-live="polite"></div>
     <div class="ic-list" id="ic-list"></div>
     """,
     "1. 点击或拖拽上传图片（可多选）\n2. 选择输出格式和质量\n3. 每张图显示转换预览，点击即可下载"),

    # 12 年龄计算器
    ("age-calc", "🎂", "年龄计算器",
     "输入出生日期，精确计算周岁、虚岁、生肖、星座和已活天数。",
     "免费在线年龄计算器：输入出生日期即可精确计算周岁、虚岁、已活天数，同时显示生肖和星座，结果实时更新，浏览器本地计算。",
     "免费在线年龄计算器，算周岁虚岁、已活天数、生肖星座，纯本地计算。",
     """
     <div class="tool-row">
       <div class="tool-field">
         <label for="ac-date">出生日期</label>
         <input type="date" id="ac-date" value="1995-06-15">
       </div>
     </div>
     <div class="tool-row">
       <button class="tool-btn" id="ac-run" type="button">⚡ 计算年龄</button>
     </div>
     <div class="tool-field">
       <label>计算结果</label>
       <div class="ac-result" id="ac-result" aria-live="polite">
         <div class="wc-stat"><span class="wc-num" id="ac-age">—</span><span class="wc-label">周岁</span></div>
         <div class="wc-stat"><span class="wc-num" id="ac-xu">—</span><span class="wc-label">虚岁</span></div>
         <div class="wc-stat"><span class="wc-num" id="ac-days">—</span><span class="wc-label">已活天数</span></div>
         <div class="wc-stat"><span class="wc-num" id="ac-zodiac">—</span><span class="wc-label">生肖</span></div>
         <div class="wc-stat"><span class="wc-num" id="ac-constellation">—</span><span class="wc-label">星座</span></div>
       </div>
     </div>
     """,
     "1. 选择出生日期\n2. 点「计算年龄」\n3. 查看周岁、虚岁、天数、生肖和星座"),
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
    <script src="../assets/js/tools-v2.js" defer></script>
    <script src="../assets/js/site.js" defer></script>
</body>
</html>
"""

def build(meta):
    slug, emoji, name, h1_desc, desc, ld_desc, body, usage = meta
    parts = []
    parts.append(HEAD_TPL.format(
        title=f"{name} - 免费在线{name}工具（本地运行·不上传数据）" if len(name) <= 4 else f"{name} - 免费在线工具（本地运行）",
        desc=desc, slug=slug, og_title=f"{name} - 免费在线工具",
        name=name, ld_desc=ld_desc))
    parts.append(BODY_HEAD.format(slug=slug, name=name, emoji=emoji, h1_desc=h1_desc, body=body, usage=usage))
    parts.append(FOOT)
    return "".join(parts)

if __name__ == "__main__":
    for meta in TOOLS:
        slug = meta[0]
        html = build(meta)
        path = os.path.join(ROOT, "tools", f"{slug}.html")
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ {slug}.html  ({len(html)} bytes)")
    print(f"\n共生成 {len(TOOLS)} 个工具页")
