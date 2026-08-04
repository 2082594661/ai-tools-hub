#!/usr/bin/env python3
"""Batch update all article HTML files with new Chinese header/footer."""
import os
import re
import glob

SITE_DIR = r'C:\Users\龙潜\seo-website'

# Pages to skip (non-article pages)
SKIP_FILES = {
    'index.html', 'about.html', 'contact.html', 'privacy.html',
    'disclaimer.html', 'links.html', '404.html'
}

NEW_HEADER = '''    <header class="site-header">
        <div class="container">
            <a href="/" class="site-title">AI工具箱</a>
            <nav>
                <a href="/">首页</a>
                <a href="/about.html">关于本站</a>
                <a href="/links.html">友情链接</a>
                <a href="/contact.html">联系我</a>
            </nav>
        </div>
    </header>'''

NEW_FOOTER = '''    <footer class="site-footer">
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
                        <li><a href="#">AI写作工具</a></li>
                        <li><a href="#">AI图像处理</a></li>
                        <li><a href="#">AI视频编辑</a></li>
                        <li><a href="#">AI编程辅助</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>相关说明</h4>
                    <ul>
                        <li><a href="/privacy.html">隐私政策</a></li>
                        <li><a href="/disclaimer.html">免责声明</a></li>
                        <li><a href="/sitemap.xml">站点地图</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 AI工具箱 | 个人维护的非商业网站</p>
                <p class="beian"><a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow" class="beian">粤ICP备XXXXXXXX号-1</a>（备案申请中）</p>
            </div>
        </div>
    </footer>'''

BAIDU_META = '    <meta name="baidu_union_verify" content="12c06fb585923e45afa002468feead30">'

def update_file(filepath):
    """Update a single HTML file with new header/footer."""
    filename = os.path.basename(filepath)
    if filename in SKIP_FILES:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Fix lang attribute
    content = content.replace('<html lang="en">', '<html lang="zh-CN">')
    if '<html lang="zh-CN">' in content and '<html lang="en">' not in content:
        modified = True

    # 2. Add baidu_union_verify meta if missing
    if 'baidu_union_verify' not in content:
        content = content.replace(
            '<link rel="stylesheet" href="/assets/css/style.css">',
            BAIDU_META + '\n    <link rel="stylesheet" href="/assets/css/style.css">'
        )
        modified = True

    # 3. Replace author meta
    content = re.sub(
        r'<meta name="author" content="[^"]*">',
        '<meta name="author" content="AI工具箱站长">',
        content
    )

    # 4. Replace header section
    old_header_pat = r'<header class="site-header">.*?</header>'
    new_header = NEW_HEADER
    if re.search(old_header_pat, content, re.DOTALL):
        content = re.sub(old_header_pat, new_header, content, flags=re.DOTALL)
        modified = True

    # 5. Replace footer section
    old_footer_pat = r'<footer class="site-footer">.*?</footer>'
    if re.search(old_footer_pat, content, re.DOTALL):
        content = re.sub(old_footer_pat, NEW_FOOTER, content, flags=re.DOTALL)
        modified = True

    # 6. Fix Open Graph URL (replace yourusername.github.io with ai-tools-hub.surge.sh)
    content = content.replace('https://yourusername.github.io', 'https://ai-tools-hub.surge.sh')

    # 7. Replace site title in og and twitter tags
    content = content.replace('AI Tools Hub', 'AI工具箱')
    content = content.replace('content="AI Tools Hub"', 'content="AI工具箱"')

    # 8. Fix author in schema
    content = content.replace('"Organization"', '"Person"')
    content = content.replace('"name": "AI Tools Hub"', '"name": "AI工具箱站长"')

    # 9. Replace the post class with article-content for consistency
    content = content.replace('<article class="post">', '<article class="article-content">')
    content = content.replace('<header class="post-header">', '<div class="post-header">')
    content = content.replace('</header>', '</div>', 1)  # only the first one (post-header)

    # 10. Fix the post-content class
    content = content.replace('<div class="post-content">', '<div class="post-content">')  # keep as is

    # 11. Fix footer inside article - remove old post-footer if present
    content = re.sub(
        r'<footer class="post-footer">.*?</footer>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 12. Remove old sidebar if present
    content = re.sub(
        r'<aside class="sidebar">.*?</aside>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filename}")
        return True
    else:
        print(f"  Skipped (no changes): {filename}")
        return False


def main():
    html_files = glob.glob(os.path.join(SITE_DIR, '*.html'))
    article_files = [f for f in html_files if os.path.basename(f) not in SKIP_FILES]

    print(f"Found {len(article_files)} article files to update\n")

    updated = 0
    for f in sorted(article_files):
        if update_file(f):
            updated += 1

    print(f"\nUpdated {updated} of {len(article_files)} article files.")


if __name__ == '__main__':
    main()
