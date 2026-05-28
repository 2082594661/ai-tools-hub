#!/usr/bin/env python3
"""Generate GitHub Pages site from SEO articles."""
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
    'title': 'AI Tools Hub - Best AI Software Reviews & Comparisons',
    'description': 'Comprehensive reviews and comparisons of the best AI tools for writing, video editing, image generation, and more.',
    'url': 'https://yourusername.github.io',  # Update after creating repo
    'author': 'AI Tools Hub',
    'language': 'en',
}

# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Tools Hub</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="AI Tools Hub">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{meta_description}">
    
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
            "@type": "Organization",
            "name": "AI Tools Hub"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "AI Tools Hub"
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
            <a href="/" class="site-title">AI Tools Hub</a>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
            </nav>
        </div>
    </header>
    
    <main class="container">
        <article class="post">
            <header class="post-header">
                <h1>{title}</h1>
                <div class="post-meta">
                    <time datetime="{date}">{date_formatted}</time>
                    <span class="reading-time">{reading_time} min read</span>
                </div>
            </header>
            
            <div class="post-content">
                {content}
            </div>
            
            <footer class="post-footer">
                <div class="post-tags">
                    {tags}
                </div>
                
                <div class="post-share">
                    <span>Share this article:</span>
                    <a href="https://twitter.com/intent/tweet?text={title}&url={url}" target="_blank">Twitter</a>
                    <a href="https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}" target="_blank">LinkedIn</a>
                </div>
            </footer>
        </article>
        
        <aside class="sidebar">
            <div class="widget">
                <h3>Related Articles</h3>
                <ul class="related-posts">
                    {related_posts}
                </ul>
            </div>
        </aside>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2026 AI Tools Hub. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''

# Index template
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="site-title">AI Tools Hub</a>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
            </nav>
        </div>
    </header>
    
    <main class="container">
        <section class="hero">
            <h1>Best AI Tools Reviews & Comparisons</h1>
            <p>Comprehensive guides to help you choose the right AI tools for your needs.</p>
        </section>
        
        <section class="posts-grid">
            {posts_list}
        </section>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2026 AI Tools Hub. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''


def extract_meta_info(md_content):
    """Extract title and meta description from markdown."""
    # Get H1 title
    h1_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else "Untitled"
    
    # Get meta description
    meta_match = re.search(r'Meta Description:\s*(.+)$', md_content, re.MULTILINE)
    meta_desc = meta_match.group(1).strip() if meta_match else ""
    
    # Get keywords from title
    keywords = ', '.join(title.lower().split()[:10])
    
    return title, meta_desc, keywords


def md_to_html(md_content):
    """Convert markdown to HTML."""
    import markdown
    
    # Remove YAML frontmatter
    md_content = re.sub(r'^---\n.*?\n---\n', '', md_content, flags=re.DOTALL)
    
    # Remove meta description line
    md_content = re.sub(r'Meta Description:.*\n', '', md_content)
    
    # Convert to HTML
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Clean up code blocks
    html = re.sub(r'<pre><code>.*?</code></pre>', '', html, flags=re.DOTALL)
    
    return html


def calculate_reading_time(text):
    """Calculate reading time in minutes."""
    words = len(text.split())
    return max(1, round(words / 200))


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
    
    # Sort by relevance and return top N
    related.sort(key=lambda x: len(set(create_slug(x['file']).split('-')) & current_keywords), reverse=True)
    return related[:count]


def generate_tags(title):
    """Generate tags from title."""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'best', 'top', '2025', '2026'}
    words = title.lower().split()
    tags = [w for w in words if w not in stop_words and len(w) > 2]
    return tags[:5]


def process_article(md_file, all_posts):
    """Process a single article."""
    filepath = os.path.join(ARTICLES_DIR, md_file)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extract info
    title, meta_desc, keywords = extract_meta_info(md_content)
    html_content = md_to_html(md_content)
    reading_time = calculate_reading_time(md_content)
    
    # Create slug and date
    slug = create_slug(title)
    date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate tags
    tags = generate_tags(title)
    tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in tags])
    
    # Get related posts
    related = get_related_posts(md_file, all_posts)
    related_html = ''.join([
        f'<li><a href="/{create_slug(r["title"])}">{r["title"]}</a></li>'
        for r in related
    ])
    
    # Create URL
    url = f"{SITE_CONFIG['url']}/{slug}"
    
    # Fill template
    html = HTML_TEMPLATE.format(
        title=title,
        meta_description=meta_desc,
        keywords=keywords,
        url=url,
        date=date,
        date_formatted=datetime.now().strftime('%B %d, %Y'),
        reading_time=reading_time,
        content=html_content,
        tags=tags_html,
        related_posts=related_html
    )
    
    return {
        'file': md_file,
        'title': title,
        'slug': slug,
        'html': html,
        'meta_desc': meta_desc,
        'date': date,
        'tags': tags
    }


def generate_index(all_posts):
    """Generate index page."""
    posts_html = ''
    
    for post in sorted(all_posts, key=lambda x: x['date'], reverse=True):
        posts_html += f'''
        <article class="post-card">
            <h2><a href="/{post['slug']}">{post['title']}</a></h2>
            <p>{post['meta_desc'][:150]}...</p>
            <div class="post-meta">
                <time>{post['date']}</time>
                <div class="tags">
                    {' '.join([f'<span class="tag">{t}</span>' for t in post['tags'][:3]])}
                </div>
            </div>
        </article>
        '''
    
    return INDEX_TEMPLATE.format(
        title=SITE_CONFIG['title'],
        description=SITE_CONFIG['description'],
        posts_list=posts_html
    )


def create_css():
    """Create CSS stylesheet."""
    return '''
/* Reset and Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.site-header {
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.site-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.site-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2563eb;
    text-decoration: none;
}

nav a {
    margin-left: 2rem;
    text-decoration: none;
    color: #666;
}

nav a:hover {
    color: #2563eb;
}

/* Hero */
.hero {
    text-align: center;
    padding: 4rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin: 2rem 0;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Posts Grid */
.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
    padding: 2rem 0;
}

.post-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.post-card:hover {
    transform: translateY(-5px);
}

.post-card h2 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.post-card h2 a {
    color: #1a1a1a;
    text-decoration: none;
}

.post-card h2 a:hover {
    color: #2563eb;
}

.post-card p {
    color: #666;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}

.post-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: #888;
}

.tags {
    display: flex;
    gap: 0.5rem;
}

.tag {
    background: #e0e7ff;
    color: #2563eb;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
}

/* Article Page */
.post {
    background: white;
    border-radius: 10px;
    padding: 3rem;
    margin: 2rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-header {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #eee;
}

.post-header h1 {
    font-size: 2rem;
    color: #1a1a1a;
    line-height: 1.3;
}

.post-content h2 {
    font-size: 1.5rem;
    color: #1a1a1a;
    margin: 2rem 0 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
}

.post-content h3 {
    font-size: 1.2rem;
    color: #333;
    margin: 1.5rem 0 0.75rem;
}

.post-content p {
    margin-bottom: 1rem;
    line-height: 1.8;
}

.post-content ul, .post-content ol {
    margin-bottom: 1rem;
    padding-left: 2rem;
}

.post-content li {
    margin-bottom: 0.5rem;
}

.post-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
}

.post-content th, .post-content td {
    padding: 0.75rem;
    border: 1px solid #ddd;
    text-align: left;
}

.post-content th {
    background: #f8f9fa;
    font-weight: 600;
}

.post-footer {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid #eee;
}

.post-share {
    margin-top: 1rem;
}

.post-share a {
    margin-left: 1rem;
    color: #2563eb;
    text-decoration: none;
}

/* Sidebar */
.sidebar {
    padding: 2rem 0;
}

.widget {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.widget h3 {
    margin-bottom: 1rem;
    color: #1a1a1a;
}

.related-posts li {
    margin-bottom: 0.5rem;
}

.related-posts a {
    color: #2563eb;
    text-decoration: none;
}

/* Footer */
.site-footer {
    background: #1a1a1a;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 1.8rem;
    }
    
    .posts-grid {
        grid-template-columns: 1fr;
    }
    
    .post {
        padding: 1.5rem;
    }
    
    .post-header h1 {
        font-size: 1.5rem;
    }
}
'''


def create_sitemap(all_posts):
    """Generate sitemap.xml."""
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add homepage
    sitemap += f'  <url>\n'
    sitemap += f'    <loc>{SITE_CONFIG["url"]}/</loc>\n'
    sitemap += f'    <changefreq>daily</changefreq>\n'
    sitemap += f'    <priority>1.0</priority>\n'
    sitemap += f'  </url>\n'
    
    # Add posts
    for post in all_posts:
        sitemap += f'  <url>\n'
        sitemap += f'    <loc>{SITE_CONFIG["url"]}/{post["slug"]}</loc>\n'
        sitemap += f'    <lastmod>{post["date"]}</lastmod>\n'
        sitemap += f'    <changefreq>monthly</changefreq>\n'
        sitemap += f'    <priority>0.8</priority>\n'
        sitemap += f'  </url>\n'
    
    sitemap += '</urlset>'
    return sitemap


def create_robots_txt():
    """Generate robots.txt."""
    return '''User-agent: *
Allow: /

Sitemap: https://yourusername.github.io/sitemap.xml
'''


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("🚀 生成 GitHub Pages 网站")
    print("="*60)
    
    # Get all markdown files
    md_files = sorted([f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')])
    
    # First pass: collect all post info
    all_posts = []
    for md_file in md_files:
        filepath = os.path.join(ARTICLES_DIR, md_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        title, meta_desc, _ = extract_meta_info(content)
        slug = create_slug(title)
        all_posts.append({
            'file': md_file,
            'title': title,
            'slug': slug,
            'meta_desc': meta_desc,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': generate_tags(title)
        })
    
    # Process each article
    print(f"\n📝 处理 {len(md_files)} 篇文章...")
    
    for md_file in md_files:
        result = process_article(md_file, all_posts)
        
        # Save HTML file
        html_path = os.path.join(SITE_DIR, f"{result['slug']}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(result['html'])
        
        print(f"✅ {result['title'][:50]}...")
    
    # Generate index page
    print(f"\n📄 生成首页...")
    index_html = generate_index(all_posts)
    with open(os.path.join(SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Generate CSS
    print(f"🎨 生成样式表...")
    with open(os.path.join(ASSETS_DIR, 'css', 'style.css'), 'w', encoding='utf-8') as f:
        f.write(create_css())
    
    # Generate sitemap
    print(f"🗺️  生成站点地图...")
    with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(create_sitemap(all_posts))
    
    # Generate robots.txt
    print(f"🤖 生成 robots.txt...")
    with open(os.path.join(SITE_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(create_robots_txt())
    
    print(f"\n{'='*60}")
    print(f"✅ 网站生成完成!")
    print(f"📁 文件位置: {SITE_DIR}")
    print(f"📊 文章数量: {len(md_files)}")
    print(f"{'='*60}")
    
    print(f"\n📋 下一步:")
    print(f"1. 创建 GitHub 仓库")
    print(f"2. 推送代码")
    print(f"3. 启用 GitHub Pages")


if __name__ == '__main__':
    main()
