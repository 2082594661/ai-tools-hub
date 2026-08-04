import os, re, glob
root = r"C:\Users\龙潜\Desktop\AI趣味分享"

# 断链检查
broken = []
for f in glob.glob(root + "/**/*.html", recursive=True):
    html = open(f, encoding="utf-8").read()
    base = os.path.dirname(f)
    for m in re.findall(r'(?:href|src)="([^"#]+)"', html):
        if m.startswith(("http", "//", "data:", "mailto:")):
            continue
        p = os.path.normpath(os.path.join(base, m))
        if not os.path.exists(p):
            broken.append((f.replace(root, ''), m))
print("断链:", broken if broken else "无")

# title/desc/canonical 检查
issues = []
for f in glob.glob(root + "/**/*.html", recursive=True):
    htmltxt = open(f, encoding="utf-8").read()
    name = f.replace(root, '')
    t = re.search(r'<title>(.*?)</title>', htmltxt, re.S)
    d = re.search(r'name="description" content="(.*?)"', htmltxt)
    c = re.search(r'rel="canonical" href="(.*?)"', htmltxt)
    if not t:
        issues.append(name + ": 缺title")
    elif len(t.group(1)) > 65:
        issues.append(name + ": title太长(" + str(len(t.group(1))) + ")")
    if not d:
        issues.append(name + ": 缺description")
    elif len(d.group(1)) > 160:
        issues.append(name + ": desc太长(" + str(len(d.group(1))) + ")")
    if not c:
        issues.append(name + ": 缺canonical")
print("SEO问题:", issues if issues else "无")

# sitemap 一致性
pages = []
for f in glob.glob(root + "/**/*.html", recursive=True):
    p = f.replace(root + os.sep, '').replace(os.sep, '/')
    if '404' not in p and '.git' not in p:
        pages.append(p)
sm = open(os.path.join(root, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r'<loc>(.*?)</loc>', sm)
print("页面数:", len(pages), ", sitemap loc数:", len(locs))
missing = [p for p in pages if "https://aifunnyplay.cn/" + p not in locs]
extra = [l for l in locs if l.replace("https://aifunnyplay.cn/", "") not in pages]
print("sitemap缺失:", missing if missing else "无")
print("sitemap多余:", extra if extra else "无")

# sw.js 版本
sw = open(os.path.join(root, "sw.js"), encoding="utf-8").read()
ver = re.search(r"CACHE\s*=\s*['\"]([^'\"]+)", sw)
print("SW CACHE版本:", ver.group(1) if ver else "未找到")
print("SW PRECACHE 工具页数:", sw.count("tools/"))

# robots.txt
robots_path = os.path.join(root, "robots.txt")
if os.path.exists(robots_path):
    robots = open(robots_path, encoding="utf-8").read()
    print("robots.txt 含sitemap:", "Sitemap:" in robots)
else:
    print("robots.txt: 不存在!")
