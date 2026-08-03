#!/usr/bin/env python3
"""
AI工具箱 · 横幅图片生成器 v2 — 杂志编辑级设计
==========================================
摒弃 v1 的 emoji+渐变+文字标签简陋方案，
改用抽象几何构图 + 精心调配的配色 + 层次叠加 + 微纹理，
达到现代编辑杂志的视觉品质。

每张图 800×400，按文章分类差异化配色与构图风格。
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter

# ── 输出目录 ──
OUT_DIR = r"C:\Users\龙潜\Desktop\AI趣味分享\assets\images\banners"
W, H = 800, 400

# ── 配色方案（按分类，使用 oklch 风格的和谐色组）─────────────
PALETTES = {
    "writing": {   # AI 写作 / 阅读
        "colors": [(232, 148, 58), (196, 93, 58), (163, 61, 28), (255, 243, 230), (250, 220, 195)],
        "accent": (200, 80, 50),
        "name": "暖琥珀写作系",
    },
    "image": {     # AI 图像 / 设计
        "colors": [(45, 107, 90), (30, 80, 68), (20, 60, 50), (235, 248, 243), (200, 230, 215)],
        "accent": (55, 140, 110),
        "name": "青绿图像系",
    },
    "video": {     # 音视频 / 音乐 / 转录
        "colors": [(75, 55, 115), (100, 70, 150), (55, 40, 90), (240, 238, 250), (210, 205, 235)],
        "accent": (130, 100, 190),
        "name": "靛紫音视频系",
    },
    "office": {     # 办公 / 数据 / 编程 / 简历
        "colors": [(40, 85, 70), (55, 110, 90), (28, 60, 50), (240, 247, 243), (212, 232, 222)],
        "accent": (80, 150, 120),
        "name": "深绿办公系",
    },
    "marketing": {  # 营销 / 客服
        "colors": [(140, 60, 75), (180, 80, 95), (100, 45, 55), (252, 240, 243), (235, 210, 218)],
        "accent": (190, 90, 110),
        "name": "玫红营销系",
    },
    "review": {     # 检测 / 其他
        "colors": [(60, 55, 65), (90, 82, 95), (42, 38, 48), (245, 244, 247), (220, 215, 225)],
        "accent": (120, 110, 140),
        "name": "炭灰检测系",
    },
    "brand": {      # 品牌主色（首页/about等）
        "colors": [(238, 148, 58), (224, 106, 53), (201, 74, 40), (255, 248, 240), (255, 225, 195)],
        "accent": (196, 93, 58),
        "name": "品牌主色系",
    },
}


# ── 文章 → 分类映射 ──
ARTICLE_CATEGORY = {
    "best-ai-writing-tools-for-bloggers-2025":          "writing",
    "ai-data-analysis-tool-for-excel-beginners":         "office",
    "ai-transcription-software-for-podcasters-comparison": "video",
    "ai-resume-builder-with-ats-optimization":           "office",
    "ai-chatbot-for-small-business-customer-service":    "marketing",
    "ai-music-generator-royalty-free-commercial-use":     "video",
    "free-ai-video-editor-no-watermark":                  "video",
    "ai-code-assistant-vs-github-copilot-alternative":    "office",
    "ai-image-generator-for-ecommerce-product-photo":     "image",
    "ai-pdf-summarizer-for-research-papers":              "writing",
    "ai-background-remover-api-for-developers":           "image",
    "ai-email-writer-chrome-extension-gmail":             "writing",
    "ai-image-upscaler-for-old-photos":                   "image",
    "ai-logo-maker-for-startups-free-trial":              "image",
    "ai-music-generator-for-videos":                      "video",
    "ai-paraphrasing-tool-to-avoid-plagiarism":           "writing",
    "ai-pdf-to-ppt-converter-free":                       "office",
    "ai-presentation-maker-with-templates":               "office",
    "ai-presentation-maker-templates-guide":              "office",
    "ai-seo-tool-for-keyword-research-affiliate":          "marketing",
    "ai-text-to-speech-narration-tool":                   "video",
    "ai-translation-app-for-travel":                      "writing",
    "best-ai-photo-enhancer-for-real-estate":             "image",
    "best-ai-voice-generator-for-youtube-videos":         "video",
    "cheap-ai-content-detector-for-teachers":             "review",
}

# ── 静态页映射 ──
STATIC_CATEGORY = {
    "index":     "brand",
    "about":     "brand",
    "contact":   "brand",
    "links":     "office",
    "privacy":   "review",
    "disclaimer":"review",
    "sitemap":   "office",
}


def hex_color(c):
    """Return '#rrggbb' from (r,g,b) tuple."""
    return "#{:02x}{:02x}{:02x}".format(*c)


def lerp(c1, c2, t):
    """Linear interpolation between two colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def make_gradient(draw, w, h, colors, direction="vertical"):
    """Fill image with a multi-stop gradient."""
    n = len(colors)
    if direction == "vertical":
        for y in range(h):
            t = y / max(h - 1, 1)
            seg = t * (n - 1)
            i = min(int(seg), n - 2)
            local_t = seg - i
            c = lerp(colors[i], colors[i + 1], local_t)
            draw.line([(0, y), (w, y)], fill=hex_color(c))
    elif direction == "horizontal":
        for x in range(w):
            t = x / max(w - 1, 1)
            seg = t * (n - 1)
            i = min(int(seg), n - 2)
            local_t = seg - i
            c = lerp(colors[i], colors[i + 1], local_t)
            draw.line([(x, 0), (x, h)], fill=hex_color(c))
    elif direction == "diagonal":
        # Diagonal from top-left to bottom-right
        for y in range(h):
            for x in range(w):
                t = (x / max(w - 1, 1) + y / max(h - 1, 1)) / 2
                seg = t * (n - 1)
                i = min(int(seg), n - 2)
                local_t = seg - i
                c = lerp(colors[i], colors[i + 1], local_t)
                draw.point((x, y), fill=hex_color(c))
    elif direction == "radial":
        # Radial from center
        cx, cy = w // 2, h // 2
        max_dist = math.sqrt(cx**2 + cy**2)
        img_temp = Image.new("RGB", (w, h))
        for y in range(h):
            for x in range(w):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                t = dist / max_dist
                seg = t * (n - 1)
                i = min(int(seg), n - 2)
                local_t = seg - i
                c = lerp(colors[i], colors[i + 1], local_t)
                img_temp.putpixel((x, y), c)
        return img_temp
    return None


# ════════════════════════════════════════
# 构图风格函数（每个返回一张 800×400 的 Image）
# ════════════════════════════════════════

def style_blob_layers(palette, seed=0):
    """风格A：有机 blob 叠加层 — 流动、温暖、有深度"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])  # 浅底
    draw = ImageDraw.Draw(bg)

    # 底层大渐变
    make_gradient(draw, W, H, [colors[3], colors[4]], "vertical")

    # 叠加 3-5 个有机 blob
    for i in range(5):
        bx = rng.randint(-int(W*0.3), int(W*0.7))
        by = rng.randint(-int(H*0.3), int(H*0.5))
        bw = rng.randint(int(W*0.5), int(W*1.1))
        bh = rng.randint(int(H*0.6), int(H*1.2))
        opacity = rng.randint(30, 80)

        blob = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(blob)
        # 用多边形模拟 organic shape
        points = []
        num_pts = 12
        for j in range(num_pts):
            angle = 2 * math.pi * j / num_pts
            rx = bw // 2 + rng.randint(-bw//6, bw//6)
            ry = bh // 2 + rng.randint(-bh//6, bh//6)
            points.append((bw//2 + int(rx * math.cos(angle)), bh//2 + int(ry * math.sin(angle))))
        ci = colors[rng.randint(0, 2)]
        bdraw.polygon(points, fill=(ci[0], ci[1], ci[2], opacity))

        blob = blob.resize((bw, bh), Image.Resampling.LANCZOS)
        bg.paste(blob, (bx, by), blob)

    # 加一层高光弧形
    highlight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(highlight)
    ac = palette["accent"]
    hdraw.ellipse([-50, -100, W+100, H//2], outline=(ac[0], ac[1], ac[2], 40), width=3)
    bg.paste(highlight, (0, 0), highlight)

    return _add_noise(bg, seed)


def style_diagonal_split(palette, seed=0):
    """风格B：对角分割 — 大胆、有力、杂志封面感"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[0])
    draw = ImageDraw.Draw(bg)

    # 主对角切分
    angle = rng.choice([25, -30, 15, -20, 35])
    rad = math.radians(angle)
    split_points = []
    if angle > 0:
        split_points = [
            (0, int(H * 0.3)),
            (int(W * 0.5), 0),
            (W, int(H * 0.6)),
            (W, H),
            (0, H),
        ]
    else:
        split_points = [
            (0, int(H * 0.7)),
            (int(W * 0.5), H),
            (W, int(H * 0.35)),
            (W, 0),
            (0, 0),
        ]
    draw.polygon(split_points, fill=hex_color(colors[3]))

    # 第二条细对角线装饰
    off = rng.randint(40, 100)
    pts2 = [(p[0] + off, p[1] - off) for p in split_points]
    ac = palette["accent"]
    draw.polygon(pts2, fill=hex_color((*[max(0, c-20) for c in ac],)))

    # 圆形点缀
    for _ in range(rng.randint(2, 5)):
        cx = rng.randint(0, W)
        cy = rng.randint(0, H)
        cr = rng.randint(20, 80)
        ci_idx = rng.choice([2, 4, 3])
        draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr],
                     fill=hex_color(colors[ci_idx]))

    return _add_noise(bg, seed)


def style_arc_composition(palette, seed=0):
    """风格C：圆弧构成 — 技术、精密、现代"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])
    draw = ImageDraw.Draw(bg)

    # 轻微背景渐变
    make_gradient(draw, W, H, [colors[3], colors[4]], "diagonal" if rng.random() > 0.5 else "vertical")

    # 多个同心/偏心圆弧
    centers = [
        (rng.randint(int(W*0.2), int(W*0.8)), rng.randint(int(H*0.1), int(H*0.9)))
        for _ in range(rng.randint(2, 4))
    ]

    for i, (cx, cy) in enumerate(centers):
        base_r = rng.randint(80, 250)
        for j in range(rng.randint(2, 4)):
            r = base_r + j * rng.randint(40, 90)
            ci = colors[min(i + j, len(colors)-1)]
            sw = rng.randint(3, 18)
            # 画不完整的圆弧（通过 start/end angle）
            start = rng.randint(0, 180)
            end = start + rng.randint(90, 270)
            draw.arc([cx-r, cy-r, cx+r, cy+r], start, end,
                     fill=hex_color(ci), width=sw)

    # 填充一些实心小圆
    for _ in range(rng.randint(3, 7)):
        cx = rng.randint(0, W)
        cy = rng.randint(0, H)
        cr = rng.randint(8, 35)
        ci = rng.choice(colors[:3])
        alpha_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        adraw = ImageDraw.Draw(alpha_layer)
        adraw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(ci[0], ci[1], ci[2], rng.randint(40, 120)))
        bg.paste(alpha_layer, (0, 0), alpha_layer)

    return _add_noise(bg, seed)


def style_mesh_gradient(palette, seed=0):
    """风格D：网格渐变块 — 编织感、丰富层次"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])

    # 划分成不规则网格，每格不同颜色
    grid_w = rng.randint(3, 5)
    grid_h = rng.randint(2, 4)
    cell_w = W // grid_w
    cell_h = H // grid_h

    draw = ImageDraw.Draw(bg)
    for gy in range(grid_h):
        for gx in range(grid_w):
            x0 = gx * cell_w + rng.randint(-15, 15)
            y0 = gy * cell_h + rng.randint(-10, 10)
            x1 = (gx + 1) * cell_w + rng.randint(-15, 15)
            y1 = (gy + 1) * cell_h + rng.randint(-10, 10)
            ci = colors[rng.randint(0, len(colors)-1)]
            # 使用带透明度的填充
            overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            odraw.rectangle([x0, y0, x1, y1], fill=(ci[0], ci[1], ci[2], rng.randint(100, 200)))
            bg.paste(overlay, (0, 0), overlay)

    # 叠加几条粗线条切割
    ac = palette["accent"]
    for _ in range(rng.randint(1, 3)):
        y = rng.randint(0, H)
        draw.line([(0, y), (W, y + rng.randint(-40, 40))],
                  fill=hex_color(ac), width=rng.randint(2, 6))

    return _add_noise(bg, seed)


def style_wave_organic(palette, seed=0):
    """风格E：波浪流体 — 自然、创意、流动感"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])
    draw = ImageDraw.Draw(bg)

    # 背景渐变
    make_gradient(draw, W, H, [colors[3], colors[4]], "vertical")

    # 多层波浪
    num_waves = rng.randint(3, 6)
    for i in range(num_waves):
        points = []
        amplitude = rng.randint(30, 80)
        frequency = rng.uniform(0.008, 0.02)
        phase = rng.uniform(0, math.pi * 2)
        base_y = int(H * (0.2 + 0.15 * i))

        points.append((0, H))
        for x in range(0, W + 1, 5):
            y = base_y + int(amplitude * math.sin(x * frequency + phase))
            points.append((x, y))
        points.append((W, H))

        ci = colors[min(i % 3, 2)]
        wave_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        wdraw = ImageDraw.Draw(wave_img)
        wdraw.polygon(points, fill=(ci[0], ci[1], ci[2], rng.randint(100, 180)))
        bg.paste(wave_img, (0, 0), wave_img)

    return _add_noise(bg, seed)


def style_brutalist_blocks(palette, seed=0):
    """风格F：粗野主义方块 — 大胆、结构化、有力量感"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])
    draw = ImageDraw.Draw(bg)

    # 底色
    draw.rectangle([0, 0, W, H], fill=hex_color(colors[4]))

    # 大色块偏移堆叠
    blocks = []
    for i in range(rng.randint(4, 7)):
        bw = rng.randint(int(W*0.2), int(W*0.7))
        bh = rng.randint(int(H*0.3), int(H*0.8))
        bx = rng.randint(-int(bw*0.2), int(W*0.8))
        by = rng.randint(-int(bh*0.2), int(H*0.7))
        blocks.append((bx, by, bx+bw, by+bh, colors[rng.randint(0, 2)]))

    for (x0, y0, x1, y1, ci) in blocks:
        draw.rectangle([x0, y0, x1, y1], fill=hex_color(ci))

    # 细线网格叠加
    ac = palette["accent"]
    step = rng.randint(40, 80)
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(*[min(255, c+30) for c in colors[3]],), width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(*[min(255, c+30) for c in colors[3]],), width=1)

    return _add_noise(bg, seed)


def style_minimal_focus(palette, seed=0):
    """风格G：极简焦点 — 大面积留白+一个视觉焦点"""
    rng = random.Random(seed)
    colors = palette["colors"]
    bg = Image.new("RGB", (W, H), colors[3])
    draw = ImageDraw.Draw(bg)

    # 几乎纯色底，微渐变
    make_gradient(draw, W, H, [colors[3], colors[4]], "vertical")

    # 一个大的焦点形状（偏移位置）
    focus_type = rng.choice(["circle", "ring", "rect", "arc"])
    fx = rng.randint(int(W*0.3), int(W*0.7))
    fy = rng.randint(int(H*0.2), int(H*0.7))
    fsize = rng.randint(80, 200)
    ac = palette["accent"]

    if focus_type == "circle":
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse([fx-fsize, fy-fsize, fx+fsize, fy+fsize],
                       fill=(ac[0], ac[1], ac[2], rng.randint(50, 130)))
        bg.paste(overlay, (0, 0), overlay)
    elif focus_type == "ring":
        draw.ellipse([fx-fsize, fy-fsize, fx+fsize, fy+fsize],
                     outline=hex_color(ac), width=rng.randint(4, 12))
        # 内部淡填充
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        inner = fsize - 15
        odraw.ellipse([fx-inner, fy-inner, fx+inner, fy+inner],
                       fill=(colors[0][0], colors[0][1], colors[0][2], 30))
        bg.paste(overlay, (0, 0), overlay)
    elif focus_type == "rect":
        angle = rng.randint(-25, 25)
        rad = math.radians(angle)
        pts = [
            (fx - fsize, fy - int(fsize*0.6)),
            (fx + fsize, fy - int(fsize*0.6)),
            (fx + int(fsize*0.8), fy + int(fsize*0.6)),
            (fx - int(fsize*0.8), fy + int(fsize*0.6)),
        ]
        draw.polygon(pts, fill=hex_color((*[max(0, c-15) for c in ac],)))
    elif focus_type == "arc":
        draw.arc([fx-fsize, fy-fsize, fx+fsize, fy+fsize],
                 rng.randint(0, 90), rng.randint(180, 360),
                 fill=hex_color(ac), width=rng.randint(8, 20))

    # 小点缀
    for _ in range(rng.randint(2, 4)):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        dr = rng.randint(3, 10)
        draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=hex_color(ac))

    return _add_noise(bg, seed)


def style_duotone_texture(palette, seed=0):
    """风格H：双色调纹理 — 高端、克制、质感"""
    rng = random.Random(seed)
    colors = palette["colors"]
    # 取最深和最浅两色
    dark = colors[0]
    light = colors[3]
    bg = Image.new("RGB", (W, H), light)
    draw = ImageDraw.Draw(bg)

    # 大型抽象形状用深色
    shape_type = rng.choice(["blob", "wedge", "stripes"])
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    if shape_type == "blob":
        points = []
        cx, cy = W * 0.65, H * 0.5
        for j in range(16):
            angle = 2 * math.pi * j / 16
            rx = rng.randint(int(W*0.25), int(W*0.45))
            ry = rng.randint(int(H*0.25), int(H*0.45))
            points.append((int(cx + rx * math.cos(angle)), int(cy + ry * math.sin(angle))))
        odraw.polygon(points, fill=(*dark, 180))

    elif shape_type == "wedge":
        wedge_pts = [
            (rng.randint(int(W*0.4), W), 0),
            (W, 0), (W, H),
            (rng.randint(int(W*0.3), int(W*0.7)), H),
            (rng.randint(0, int(W*0.3)), rng.randint(int(H*0.3), int(H*0.7))),
        ]
        odraw.polygon(wedge_pts, fill=(*dark, 160))

    elif shape_type == "stripes":
        stripe_w = rng.randint(30, 70)
        for i in range(-1, W // stripe_w + 2):
            x = i * stripe_w + rng.randint(-10, 10)
            if i % 2 == 0:
                odraw.rectangle([x, 0, x + stripe_w, H], fill=(*dark, rng.randint(60, 140)))

    bg.paste(overlay, (0, 0), overlay)

    # 细腻点状纹理
    ac = palette["accent"]
    dot_step = 8
    for y in range(0, H, dot_step):
        for x in range(0, W, dot_step):
            if rng.random() > 0.6:
                draw.point((x + rng.randint(-2, 2), y + rng.randint(-2, 2)),
                           fill=(*[min(255, c + rng.randint(-15, 15)) for c in light],))

    return _add_noise(bg, seed, intensity=3)


# ── 所有可用风格 ──
ALL_STYLES = [
    style_blob_layers,
    style_diagonal_split,
    style_arc_composition,
    style_mesh_gradient,
    style_wave_organic,
    style_brutalist_blocks,
    style_minimal_focus,
    style_duotone_texture,
]


def _add_noise(img, seed, intensity=5):
    """添加极微妙的噪点纹理，增加胶片质感"""
    rng = random.Random(seed + 99999)
    pixels = img.load()
    for y in range(0, H, 2):  # 隔行采样提升性能
        for x in range(0, W, 2):
            n = rng.randint(-intensity, intensity)
            r, g, b = img.getpixel((x, y))
            pixels[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n))
            )
    return img


# ── 文件名→风格分配（确保相邻文章不重复）──
def pick_style(filename, idx):
    """根据文件名哈希选择风格，确保分布均匀但确定性。"""
    hash_val = sum(ord(c) for c in filename)
    style_idx = (hash_val + idx * 7) % len(ALL_STYLES)
    return ALL_STYLES[style_idx]


def generate_banner(filename, category_key, index=0):
    """为指定文件名生成横幅图片"""
    palette = PALETTES.get(category_key, PALETTES["brand"])
    style_fn = pick_style(filename, index)
    seed = hash(filename) & 0xFFFFFFF

    img = style_fn(palette, seed=seed)
    out_path = os.path.join(OUT_DIR, filename + ".png")
    img.save(out_path, "PNG", optimize=True)
    print(f"  OK: {filename}.png [{palette['name']} | {style_fn.__doc__.split('—')[0].strip() if style_fn.__doc__ else '?'}]")
    return out_path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"输出目录: {OUT_DIR}")
    print(f"尺寸: {W}×{H}")
    print("=" * 60)

    all_files = []

    # 文章横幅
    for fname, cat in ARTICLE_CATEGORY.items():
        all_files.append((fname, cat))

    # 静态页横幅
    for fname, cat in STATIC_CATEGORY.items():
        all_files.append((fname, cat))

    print(f"共 {len(all_files)} 张横幅待生成\n")

    for i, (fname, cat) in enumerate(all_files):
        generate_banner(fname, cat, index=i)

    print("\n" + "=" * 60)
    print("全部完成！")


if __name__ == "__main__":
    main()
