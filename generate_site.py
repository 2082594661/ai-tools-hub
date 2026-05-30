#!/usr/bin/env python3
"""Generate static site from SEO articles (Chinese version)."""
import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = r'C:\Users\龙潜'
ARTICLES_DIR = os.path.join(BASE_DIR, 'seo-articles')
SITE_DIR = os.path.join(BASE_DIR, 'seo-website')
POSTS_DIR = os.path.join(SITE_DIR, '_posts')
ASSETS_DIR = os.path.join(SITE_DIR, 'assets')

# Site settings
SITE_CONFIG = {
    'title': 'AI工具箱 - 实用AI工具推荐与使用心得',
    'description': '分享我实际使用过的AI工具，不吹不黑，只说真实体验。涵盖AI写作、AI图片处理、AI视频编辑、AI编程辅助等各类工具。',
    'url': 'https://ai-tools-hub.surge.sh',
    'author': 'AI工具箱',
    'language': 'zh-CN',
}

# HTML Template for articles
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI工具箱</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="AI工具箱站长">
    <meta name="baidu_union_verify" content="12c06fb585923e45afa002468feead30">

    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">

    <!-- Canonical URL -->
    <link rel="canonical" href="{url}">

    <!-- Stylesheet -->
    <link rel="stylesheet" href="/assets/css/style.css">

    <!-- Schema.org Article Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{meta_description}",
        "author": {{
            "@type": "Person",
            "name": "AI工具箱站长"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "AI工具箱"
        }},
        "datePublished": "{date}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{url}"
        }}
    }}
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="site-title">AI工具箱</a>
            <nav>
                <a href="/">首页</a>
                <a href="/about.html">关于本站</a>
                <a href="/links.html">友情链接</a>
                <a href="/contact.html">联系我</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <article class="article-content">
            <h1>{title}</h1>
            <div class="article-meta">
                <span>发布于 <time datetime="{date}">{date_formatted}</time></span>
                <span>阅读约{reading_time}分钟</span>
                <span>分类：{category}</span>
            </div>

            <div class="post-content">
                {content}
            </div>

            <footer class="article-footer">
                <p>声明：本文为原创内容，基于作者实际使用体验撰写。文中涉及的AI工具可能已更新，请以官方最新信息为准。如需转载，请注明出处。</p>
                <p style="margin-top:0.8rem">标签：{tags}</p>
            </footer>
        </article>

        <aside class="sidebar-col" style="width:100%;margin-top:2rem">
            <div class="sidebar-widget">
                <h3>相关文章</h3>
                <ul class="related-posts">
                    {related_posts}
                </ul>
            </div>
        </aside>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>导航</h4>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/about.html">关于本站</a></li>
                        <li><a href="/links.html">友情链接</a></li>
                        <li><a href="/contact.html">联系我</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>文章分类</h4>
                    <ul>
                        <li><a href="/category/ai-writing.html">AI写作工具</a></li>
                        <li><a href="/category/ai-image.html">AI图像处理</a></li>
                        <li><a href="/category/ai-video-audio.html">AI音视频</a></li>
                        <li><a href="/category/ai-office.html">AI办公效率</a></li>
                        <li><a href="/category/ai-marketing.html">AI营销客服</a></li>
                        <li><a href="/category/ai-coding.html">AI编程辅助</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>相关说明</h4>
                    <ul>
                        <li><a href="/privacy.html">隐私政策</a></li>
                        <li><a href="/disclaimer.html">免责声明</a></li>
                        <li><a href="/links.html">友情链接</a></li>
                        <li><a href="/sitemap.html">站点地图</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 AI工具箱 | 个人维护的非商业网站</p>
                <p class="beian"><a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow" class="beian">粤ICP备XXXXXXXX号-1</a>（备案申请中）</p>
            </div>
        </div>
    </footer>
</body>
</html>'''


def strip_markdown(text):
    """Strip markdown formatting characters from text."""
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'__', '', text)
    text = re.sub(r'_', '', text)
    text = re.sub(r'`', '', text)
    text = re.sub(r'~~', '', text)
    text = re.sub(r'#', '', text)
    return text.strip()


def extract_meta_info(md_content):
    """Extract title and meta description from markdown."""
    h1_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else "Untitled"

    meta_match = re.search(r'\*{0,2}Meta Description:\*{0,2}\s*(.+)$', md_content, re.MULTILINE)
    meta_desc = meta_match.group(1).strip() if meta_match else ""
    meta_desc = strip_markdown(meta_desc)

    # Clean title: remove markdown, punctuation for keyword extraction
    clean_title = strip_markdown(title)
    stop_words = {'the','a','an','and','or','but','in','on','at','to','for','of','with','by',
                  'best','top','2025','2026','your','how','what','why','is','it','its','this',
                  'that','are','you','we','they','can','will','guide','complete','comparison',
                  'vs','use','using','not','no','more','our','all','from','has','been'}
    words = [w.strip(':,.-!?()') for w in clean_title.lower().split()]
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    # Add Chinese category keywords
    cat = guess_category(title)
    zh_keywords_map = {
        'AI写作工具': 'AI写作,写作软件,内容创作',
        'AI图像处理': 'AI图像,图片处理,修图工具',
        'AI视频编辑': 'AI视频,视频剪辑,视频制作',
        'AI编程辅助': 'AI编程,代码助手,开发工具',
        'AI音频工具': 'AI音频,语音转文字,音乐生成',
        'AI数据分析': 'AI数据,数据分析,Excel工具',
        'AI营销工具': 'AI营销,SEO工具,关键词研究',
        'AI学术工具': 'AI学术,论文,PDF总结',
        'AI客服': 'AI客服,聊天机器人,客户服务',
        'AI求职工具': 'AI简历,求职,面试',
        'AI邮件工具': 'AI邮件,邮件助手,Gmail',
        'AI演示文稿': 'AI演示,PPT,幻灯片',
        'AI检测工具': 'AI检测,内容检测,查重',
        'AI工具评测': 'AI工具,AI软件,工具推荐',
    }
    zh_kw = zh_keywords_map.get(cat, 'AI工具')
    keywords = ', '.join(keywords[:8]) + ', ' + zh_kw

    return title, meta_desc, keywords


def md_to_html(md_content):
    """Convert markdown to HTML."""
    import markdown

    # Remove YAML-style frontmatter
    md_content = re.sub(r'^---\n.*?\n---\n', '', md_content, flags=re.DOTALL)
    # Remove Meta Description line (may have ** markers)
    md_content = re.sub(r'\*{0,2}Meta Description:\*{0,2}.*\n', '', md_content)
    # Clean up leftover markdown markers on blank lines
    md_content = re.sub(r'^\*{1,2}\s*$', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^_{1,2}\s*$', '', md_content, flags=re.MULTILINE)

    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    html = re.sub(r'<pre><code>.*?</code></pre>', '', html, flags=re.DOTALL)
    # Remove empty heading tags left from cleanup
    html = re.sub(r'<h[1-6]>\s*</h[1-6]>', '', html)
    html = re.sub(r'<h[1-6]>\*{1,2}</h[1-6]>', '', html)

    return html


def calculate_reading_time(text):
    """Calculate reading time in minutes (Chinese: ~400 chars/min)."""
    chars = len(text)
    return max(1, round(chars / 400))


def create_slug(title):
    """Create URL slug from title."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug[:80].strip('-')


def get_related_posts(current_file, all_posts, count=3):
    """Get related posts based on keywords."""
    related = []
    current_keywords = set(create_slug(current_file).split('-'))

    for post in all_posts:
        if post['file'] != current_file:
            post_keywords = set(create_slug(post['file']).split('-'))
            common = len(current_keywords & post_keywords)
            if common > 0:
                related.append(post)

    related.sort(key=lambda x: len(set(create_slug(x['file']).split('-')) & current_keywords), reverse=True)
    return related[:count]


def category_to_slug(category_name):
    """Convert Chinese category name to URL slug."""
    slug_map = {
        'AI写作工具': 'ai-writing',
        'AI图像处理': 'ai-image',
        'AI视频编辑': 'ai-video',
        'AI编程辅助': 'ai-coding',
        'AI音频工具': 'ai-audio',
        'AI数据分析': 'ai-data',
        'AI营销工具': 'ai-marketing',
        'AI学术工具': 'ai-academic',
        'AI客服': 'ai-customer-service',
        'AI求职工具': 'ai-resume',
        'AI邮件工具': 'ai-email',
        'AI演示文稿': 'ai-presentation',
        'AI检测工具': 'ai-detection',
        'AI工具评测': 'ai-review',
    }
    return slug_map.get(category_name, 'ai-review')


def generate_tags(title):
    """Generate Chinese+English tags from title."""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
                  'with', 'by', 'best', 'top', '2025', '2026', 'your', 'how', 'what', 'why'}
    words = title.lower().split()
    tags = [w.strip(':,.-!?()') for w in words if w not in stop_words and len(w) > 2]
    # Add category-based Chinese tag
    cat = guess_category(title)
    return list(dict.fromkeys(tags))[:6], cat  # Return both tags and category


def guess_category(title):
    """Guess category from title keywords."""
    title_lower = title.lower()
    if any(k in title_lower for k in ['writing', 'writing tools', 'paraphrasing', 'plagiarism']):
        return 'AI写作工具'
    if any(k in title_lower for k in ['image', 'photo', 'logo', 'background', 'picture', 'design']):
        return 'AI图像处理'
    if any(k in title_lower for k in ['video', 'editor', 'editing']):
        return 'AI视频编辑'
    if any(k in title_lower for k in ['code', 'copilot', 'programming', 'developer']):
        return 'AI编程辅助'
    if any(k in title_lower for k in ['chatbot', 'customer service', '客服']):
        return 'AI客服'
    if any(k in title_lower for k in ['transcription', 'voice', 'audio', 'music', 'podcast']):
        return 'AI音频工具'
    if any(k in title_lower for k in ['data', 'excel', 'analysis']):
        return 'AI数据分析'
    if any(k in title_lower for k in ['resume', 'job', 'hired']):
        return 'AI求职工具'
    if any(k in title_lower for k in ['seo', 'keyword', 'marketing']):
        return 'AI营销工具'
    if any(k in title_lower for k in ['email', 'gmail', 'mail']):
        return 'AI邮件工具'
    if any(k in title_lower for k in ['presentation', 'slide', 'ppt']):
        return 'AI演示文稿'
    if any(k in title_lower for k in ['pdf', 'summariz', 'research', 'paper']):
        return 'AI学术工具'
    if any(k in title_lower for k in ['detector', 'content detect']):
        return 'AI检测工具'
    return 'AI工具评测'


def process_article(md_file, all_posts):
    """Process a single article."""
    filepath = os.path.join(ARTICLES_DIR, md_file)

    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    title, meta_desc, keywords = extract_meta_info(md_content)
    html_content = md_to_html(md_content)
    reading_time = calculate_reading_time(md_content)
    # Use filename for slug since Chinese titles don't produce good slugs
    slug = os.path.splitext(md_file)[0]
    # Remove leading numbers like "01-", "13-" etc.
    slug = re.sub(r'^\d+-', '', slug)
    date = datetime.now().strftime('%Y-%m-%d')

    tags, category = generate_tags(title)
    cat_slug = category_to_slug(category)
    tags_html = ', '.join([
        f'<a href="/tag/{cat_slug}.html" style="color:#8b7355;font-size:0.8rem;">#{tag}</a>'
        for tag in tags
    ])

    related = get_related_posts(md_file, all_posts)
    related_html = ''.join([
        f'<li><a href="/{r["slug"]}.html">{r.get("zh_title", r["title"])[:50]}</a></li>'
        for r in related
    ])

    url = f"{SITE_CONFIG['url']}/{slug}"

    html = HTML_TEMPLATE.format(
        title=title,
        meta_description=meta_desc,
        keywords=keywords,
        url=url,
        date=date,
        date_formatted=datetime.now().strftime('%Y年%m月%d日'),
        reading_time=reading_time,
        content=html_content,
        tags=tags_html,
        related_posts=related_html,
        category=f'<a href="/category/{cat_slug}.html">{category}</a>'
    )

    return {
        'file': md_file,
        'title': title,
        'slug': slug,
        'html': html,
        'meta_desc': meta_desc,
        'date': date,
        'tags': tags,
        'category': category,
        'category_slug': cat_slug,
    }


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("生成 AI工具箱 静态网站")
    print("="*60)

    md_files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')])

    all_posts = []
    for md_file in md_files:
        filepath = os.path.join(ARTICLES_DIR, md_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        title, meta_desc, _ = extract_meta_info(content)
        tags, category = generate_tags(title)
        # Use filename for slug
        slug = os.path.splitext(md_file)[0]
        slug = re.sub(r'^\d+-', '', slug)
        all_posts.append({
            'file': md_file,
            'title': title,
            'slug': slug,
            'meta_desc': meta_desc,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': tags,
            'category': category,
            'category_slug': category_to_slug(category),
        })

    print(f"\n处理 {len(md_files)} 篇文章...")

    for md_file in md_files:
        result = process_article(md_file, all_posts)

        html_path = os.path.join(SITE_DIR, f"{result['slug']}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(result['html'])

        print(f"  {result['title'][:50]}...")

    print(f"\n{'='*60}")
    print(f"网站生成完成!")
    print(f"文件位置: {SITE_DIR}")
    print(f"文章数量: {len(md_files)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
