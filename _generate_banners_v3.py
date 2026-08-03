#!/usr/bin/env python3
"""
AI工具箱 · 横幅图片生成器 v3 — 杂志编辑级设计（增强版）
========================================================
v2 的基础上增强：
- 每张图保证足够视觉密度，杜绝空旷
- 增加光晕/辉光效果提升质感
- 更丰富的色彩层次和对比度
- 细腻的噪点纹理增加胶片感
- 所有构图都经过精心调配的参数
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter

OUT_DIR = r"C:\Users\龙潜\Desktop\AI趣味分享\assets\images\banners"
W, H = 800, 400

# ── 精心调配的分类配色 ──
PALETTES = {
    "writing": {
        "dark": (180, 75, 45),      # 深珊瑚
        "mid":  (220, 130, 70),      # 暖琥珀
        "light": (255, 235, 215),    # 暖奶油
        "glow": (255, 200, 160),     # 辉光
        "accent": (200, 80, 50),
        "name": "暖琥珀",
    },
    "image": {
        "dark": (30, 95, 78),        # 深青绿
        "mid":  (55, 140, 115),      # 明青绿
        "light": (230, 248, 242),    # 薄荷白
        "glow": (180, 235, 210),     # 青辉光
        "accent": (45, 160, 125),
        "name": "青绿",
    },
    "video": {
        "dark": (65, 45, 110),       # 深靛蓝
        "mid":  (105, 75, 170),      # 亮靛紫
        "light": (238, 235, 250),    # 薰衣草白
        "glow": (200, 190, 240),     # 紫辉光
        "accent": (140, 100, 200),
        "name": "靛紫",
    },
    "office": {
        "dark": (35, 78, 62),        # 深森林绿
        "mid":  (60, 125, 98),       # 明绿色
        "light": (238, 248, 242),    # 绿白
        "glow": (190, 232, 212),     # 绿辉光
        "accent": (70, 155, 120),
        "name": "深绿",
    },
    "marketing": {
        "dark": (130, 55, 72),       # 深玫红
        "mid":  (185, 85, 105),      # 亮玫瑰
        "light": (253, 242, 245),    # 玫瑰白
        "glow": (245, 210, 220),     # 粉辉光
        "accent": (200, 80, 105),
        "name": "玫红",
    },
    "review": {
        "dark": (55, 50, 62),        # 深炭灰
        "mid":  (90, 82, 105),       # 灰紫
        "light": (244, 243, 248),    # 冷灰白
        "glow": (215, 210, 230),     # 灰辉光
        "accent": (120, 105, 150),
        "name": "炭灰",
    },
    "brand": {
        "dark": (195, 80, 42),       # 品牌深橙
        "mid":  (235, 135, 60),      # 品牌亮橙
        "light": (255, 248, 240),    # 暖白
        "glow": (255, 225, 195),     # 橙辉光
        "accent": (196, 93, 58),
        "name": "品牌",
    },
}


def hc(c):
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, c[0])),
        max(0, min(255, c[1])),
        max(0, min(255, c[2]))
    )


def lerp(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def add_glow(img, cx, cy, radius, color, intensity=60):
    """在指定位置添加柔和辉光"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -3):
        alpha = int(intensity * (r / radius) ** 2)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(color[0], color[1], color[2], alpha))
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0,0,0,0)), overlay), (0,0), overlay)
    return img


def add_noise(img, seed, level=4):
    rng = random.Random(seed + 77777)
    pixels = img.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            n = rng.randint(-level, level)
            p = img.getpixel((x, y))
            if len(p) == 3:
                pixels[x, y] = tuple(max(0, min(255, c + n)) for c in p)
            else:
                pixels[x, y] = p[:3] + (p[3],)
    return img


def radial_gradient_bg(palette):
    """创建径向渐变背景"""
    img = Image.new("RGB", (W, H), palette["light"])
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    max_d = math.sqrt(cx**2 + cy**2)
    for y in range(H):
        for x in range(W):
            d = math.sqrt((x - cx)**2 + (y - cy)**2) / max_d
            c = lerp(palette["light"], palette["mid"], d * 0.7)
            img.putpixel((x, y), c)
    return img


# ════════════════════════════════════
# 8 种构图风格
# ════════════════════════════════════

def style_blob_layers(palette, seed=0):
    """A: 有机 blob 层叠 — 流动、温暖、丰富层次"""
    rng = random.Random(seed)
    bg = radial_gradient_bg(palette)

    # 叠加多个有机形状层
    for i in range(6):
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)

        bx = rng.randint(-int(W*0.35), int(W*0.65))
        by = rng.randint(-int(H*0.35), int(H*0.55))
        bw = rng.randint(int(W*0.5), int(W*1.15))
        bh = rng.randint(int(H*0.55), int(H*1.25))

        points = []
        npts = rng.randint(10, 16)
        for j in range(npts):
            angle = 2 * math.pi * j / npts + rng.uniform(-0.15, 0.15)
            rx = bw // 2 + rng.randint(-bw//5, bw//5)
            ry = bh // 2 + rng.randint(-bh//5, bh//5)
            points.append((int(bw//2 + rx * math.cos(angle)),
                          int(bh//2 + ry * math.sin(angle))))

        ci = [palette["dark"], palette["mid"], palette["accent"],
              (*[max(0, c-20) for c in palette["dark"]],)][i % 4]
        alpha = rng.randint(35, 85)
        od.polygon(points, fill=(ci[0], ci[1], ci[2], alpha))

        blob = overlay.resize((bw, bh), Image.Resampling.LANCZOS)
        bg.paste(Image.alpha_composite(Image.new("RGBA", bg.size), overlay), (0, 0), overlay)

    # 高光弧线装饰
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hld = ImageDraw.Draw(hl)
    ac = palette["accent"]
    gl = palette["glow"]
    hld.arc([-60, -120, W+120, int(H*0.55)], 200, 340,
            fill=(gl[0], gl[1], gl[2], 50), width=4)
    hld.arc([int(W*0.3), -int(H*0.3), int(W*1.1), int(H*0.8)], 120, 280,
            fill=(ac[0], ac[1], ac[2], 35), width=2)
    bg = Image.alpha_composite(bg.convert("RGBA"), hl).convert("RGB")

    # 散布小圆点
    dot_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dld = ImageDraw.Draw(dot_layer)
    for _ in range(rng.randint(8, 16)):
        dx, dy = rng.randint(0, W), rng.randint(0, H)
        dr = rng.randint(2, 8)
        dalpha = rng.randint(30, 80)
        dld.ellipse([dx-dr, dy-dr, dx+dr, dy+dr],
                    fill=(palette["glow"][0], palette["glow"][1], palette["glow"][2], dalpha))
    bg = Image.alpha_composite(bg.convert("RGBA"), dot_layer).convert("RGB")

    return add_noise(bg, seed)


def style_diagonal_split(palette, seed=0):
    """B: 对角分割 — 大胆、有力、杂志封面感"""
    rng = random.Random(seed)

    # 主色块
    img = Image.new("RGB", (W, H), palette["dark"])
    draw = ImageDraw.Draw(img)

    angle = rng.choice([22, -28, 18, -24, 32, -18])
    if angle > 0:
        poly1 = [(0, int(H*0.28)), (int(W*0.52), 0), (W, int(H*0.55)), (W, H), (0, H)]
        poly2 = [(0, int(H*0.28)), (int(W*0.52), 0), (W, 0), (W, int(H*0.55))]
    else:
        poly1 = [(0, int(H*0.72)), (int(W*0.48), H), (W, int(H*0.42)), (W, 0), (0, 0)]
        poly2 = [(0, int(H*0.72)), (int(W*0.48), H), (W, H), (W, int(H*0.42))]

    draw.polygon(poly1, fill=hc(palette["light"]))
    draw.polygon(poly2, fill=hc((*[min(255, c+18) for c in palette["mid"]],)))

    # 第二条细分割线
    offset = rng.randint(35, 90)
    ac = palette["accent"]
    poly3 = [(p[0] + (offset if angle > 0 else -offset),
              p[1] + (offset if angle < 0 else -offset)) for p in poly1]
    draw.polygon(poly3, fill=hc((*[max(0, c-25) for c in palette["dark"]],)))

    # 圆形装饰元素
    for _ in range(rng.randint(3, 6)):
        cx = rng.randint(0, W)
        cy = rng.randint(0, H)
        cr = rng.randint(25, 85)
        ci = rng.choice([palette["accent"], palette["mid"], palette["glow"]])
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        old = ImageDraw.Draw(ol)
        old.ellipse([cx-cr, cy-cr, cx+cr, cy+cr],
                    fill=(ci[0], ci[1], ci[2], rng.randint(40, 100)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 细线网格纹理
    step = rng.randint(50, 90)
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=hc((*[min(255, c+20) for c in palette["light"]],)), width=1)

    return add_noise(img, seed)


def style_arc_composition(palette, seed=0):
    """C: 圆弧构成 — 技术、精密、现代"""
    rng = random.Random(seed)
    img = radial_gradient_bg(palette)
    draw = ImageDraw.Draw(img)

    centers = [
        (rng.randint(int(W*0.15), int(W*0.85)),
         rng.randint(int(H*0.1), int(H*0.9)))
        for _ in range(rng.randint(3, 5))
    ]

    # 多层圆弧
    arc_colors = [palette["dark"], palette["mid"], palette["accent"],
                  (*[min(255, c+30) for c in palette["mid"]],)]

    for ci_idx, (cx, cy) in enumerate(centers):
        base_r = rng.randint(70, 220)
        n_arcs = rng.randint(3, 5)
        for j in range(n_arcs):
            r = base_r + j * rng.randint(35, 80)
            col = arc_colors[(ci_idx + j) % len(arc_colors)]
            sw = rng.randint(4, 16)
            start = rng.randint(0, 180)
            end = start + rng.randint(90, 270)
            draw.arc([cx-r, cy-r, cx+r, cy-r], start, end,
                     fill=hc(col), width=sw)

    # 实心圆点填充
    for _ in range(rng.randint(5, 12)):
        cx = rng.randint(0, W)
        cy = rng.randint(0, H)
        cr = rng.randint(6, 32)
        ci = rng.choice([palette["dark"], palette["accent"], palette["mid"]])
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        old = ImageDraw.Draw(ol)
        old.ellipse([cx-cr, cy-cr, cx+cr, cy+cr],
                    fill=(ci[0], ci[1], ci[2], rng.randint(45, 130)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 辉光点
    gx, gy = rng.randint(int(W*0.2), int(W*0.8)), rng.randint(int(H*0.2), int(H*0.8))
    img = add_glow(img, gx, gy, rng.randint(80, 150), palette["glow"], 40)

    return add_noise(img, seed)


def style_mesh_gradient(palette, seed=0):
    """D: 不规则色块编织 — 丰富层次、现代艺术感"""
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), palette["light"])

    grid_cols = rng.randint(4, 6)
    grid_rows = rng.randint(3, 5)
    cell_w = W / grid_cols
    cell_h = H / grid_rows

    colors_pool = [palette["dark"], palette["mid"], palette["accent"],
                   palette["light"], palette["glow"],
                   (*[min(255, c+15) for c in palette["mid"]],),
                   (*[max(0, c-15) for c in palette["dark"]],)]

    for gy in range(grid_rows):
        for gx in range(grid_cols):
            x0 = gx * cell_w + rng.uniform(-cell_w*0.2, cell_w*0.2)
            y0 = gy * cell_h + rng.uniform(-cell_h*0.15, cell_h*0.15)
            x1 = (gx + 1) * cell_w + rng.uniform(-cell_w*0.2, cell_w*0.2)
            y1 = (gy + 1) * cell_h + rng.uniform(-cell_h*0.15, cell_h*0.15)

            overlay = Image.new("RGBA", (W, H), (0,0,0,0))
            odraw = ImageDraw.Draw(overlay)
            ci = rng.choice(colors_pool)
            odraw.rectangle([int(x0), int(y0), int(x1), int(y1)],
                        fill=(ci[0], ci[1], ci[2], rng.randint(110, 210)))
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # 粗切割线
    draw = ImageDraw.Draw(img)
    ac = palette["accent"]
    for _ in range(rng.randint(2, 4)):
        y = rng.randint(int(H*0.2), int(H*0.8))
        draw.line([(0, y), (W, y + rng.randint(-30, 30))],
                  fill=hc(ac), width=rng.randint(2, 5))

    # 角落小方块点缀
    for corner in [(rng.randint(0, 30), rng.randint(0, 30)),
                   (W - rng.randint(0, 30), rng.randint(0, 30)),
                   (rng.randint(0, 30), H - rng.randint(0, 30)),
                   (W - rng.randint(0, 30), H - rng.randint(0, 30))]:
        sz = rng.randint(12, 30)
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        odm = ImageDraw.Draw(ol)
        odm.rectangle([corner[0], corner[1], corner[0]+sz, corner[1]+sz],
                     fill=(ac[0], ac[1], ac[2], rng.randint(50, 120)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    return add_noise(img, seed)


def style_wave_organic(palette, seed=0):
    """E: 波浪流体 — 自然、创意、流动感"""
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), palette["light"])
    draw = ImageDraw.Draw(img)

    # 底部渐变
    for y in range(H):
        t = y / H
        c = lerp(palette["light"], palette["glow"], t * 0.5)
        draw.line([(0, y), (W, y)], fill=hc(c))

    num_waves = rng.randint(4, 7)
    wave_colors = [palette["dark"], palette["mid"], palette["accent"],
                   (*[max(0, c-18) for c in palette["dark"]],),
                   palette["mid"]]

    for i in range(num_waves):
        points = [(0, H)]
        amp = rng.randint(35, 85)
        freq = rng.uniform(0.009, 0.022)
        phase = rng.uniform(0, math.pi * 2)
        base_y = int(H * (0.15 + 0.14 * i))

        for x in range(0, W + 1, 4):
            y = base_y + int(amp * math.sin(x * freq + phase) +
                             amp * 0.4 * math.sin(x * freq * 2.3 + phase * 1.7))
            points.append((x, max(0, min(H, y))))
        points.append((W, H))

        ci = wave_colors[i % len(wave_colors)]
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        od.polygon(points, fill=(ci[0], ci[1], ci[2], rng.randint(100, 185)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 气泡点缀
    bubble_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    bld = ImageDraw.Draw(bubble_layer)
    gl = palette["glow"]
    for _ in range(rng.randint(6, 14)):
        bx = rng.randint(0, W)
        by = rng.randint(0, int(H*0.7))
        br = rng.randint(3, 12)
        bld.ellipse([bx-br, by-br, bx+br, by+br],
                    fill=(gl[0], gl[1], gl[2], rng.randint(40, 100)))
    img = Image.alpha_composite(img.convert("RGBA"), bubble_layer).convert("RGB")

    return add_noise(img, seed)


def style_brutalist_blocks(palette, seed=0):
    """F: 粗野主义色块 — 大胆结构、力量感"""
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H), palette["light"])
    draw = ImageDraw.Draw(img)

    # 微底纹
    for y in range(H):
        t = y / H
        c = lerp(palette["light"], palette["glow"], t * 0.3)
        draw.line([(0, y), (W, y)], fill=hc(c))

    blocks = []
    for _ in range(rng.randint(5, 8)):
        bw = rng.randint(int(W*0.18), int(W*0.65))
        bh = rng.randint(int(H*0.25), int(H*0.75))
        bx = rng.randint(-int(bw*0.25), int(W*0.82))
        by = rng.randint(-int(bh*0.25), int(H*0.75))
        ci = rng.choice([palette["dark"], palette["mid"], palette["accent"],
                         (*[min(255, c+12) for c in palette["dark"]],)])
        blocks.append((bx, by, bx+bw, by+bh, ci))

    for (x0, y0, x1, y1, ci) in blocks:
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        od.rectangle([int(x0), int(y0), int(x1), int(y1)],
                     fill=(ci[0], ci[1], ci[2], rng.randint(160, 240)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 细网格叠加
    step = rng.randint(35, 65)
    grid_color = (*[min(255, c+25) for c in palette["light"]],)
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=hc(grid_color), width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=hc(grid_color), width=1)

    # 数字标注装饰（类似建筑蓝图）
    font_size_label = rng.choice(["01", "02", "03", "04", "05", "06", "07"])
    label_x = rng.randint(int(W*0.05), int(W*0.15))
    label_y = rng.randint(int(H*0.08), int(H*0.2))
    draw.text((label_x, label_y), font_size_label,
              fill=hc(palette["accent"]), font_size=rng.randint(36, 56))

    return add_noise(img, seed)


def style_minimal_focus(palette, seed=0):
    """G: 焦点构图 — 一个主视觉焦点 + 丰富的背景层次"""
    rng = random.Random(seed)

    # 背景：微妙的径向渐变
    img = radial_gradient_bg(palette)
    draw = ImageDraw.Draw(img)

    ac = palette["accent"]
    dk = palette["dark"]
    md = palette["mid"]
    gl = palette["glow"]

    # 选择焦点类型
    ftype = rng.choice(["large_circle", "concentric_rings", "offset_arc",
                         "dual_shape", "layered_rect"])

    fx = rng.randint(int(W*0.25), int(W*0.75))
    fy = rng.randint(int(H*0.2), int(H*0.75))
    fs = rng.randint(90, 200)

    if ftype == "large_circle":
        # 大圆形焦点，带内部层次
        for r_delta in range(4, 0, -1):
            r = fs - r_delta * 18
            if r <= 0:
                continue
            ci = [dk, md, ac, gl][r_delta - 1]
            alpha = [160, 120, 80, 50][r_delta - 1]
            ol = Image.new("RGBA", (W, H), (0,0,0,0))
            od = ImageDraw.Draw(ol)
            od.ellipse([fx-r, fy-r, fx+r, fy+r],
                       fill=(ci[0], ci[1], ci[2], alpha))
            img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")
        # 外圈光环
        draw.ellipse([fx-fs-10, fy-fs-10, fx+fs+10, fy+fs+10],
                     outline=hc(gl), width=2)

    elif ftype == "concentric_rings":
        for ri in range(rng.randint(4, 7)):
            r = fs - ri * 22
            if r <= 10:
                continue
            sw = rng.randint(5, 14)
            ci = [ac, dk, md, gl][ri % 4]
            draw.ellipse([fx-r, fy-r, fx+r, fy+r],
                        outline=hc(ci), width=sw)
        # 中心淡填充
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        inner = max(fs - 120, 20)
        od.ellipse([fx-inner, fy-inner, fx+inner, fy+inner],
                   fill=(md[0], md[1], md[2], 45))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    elif ftype == "offset_arc":
        # 大弧形
        draw.arc([fx-fs, fy-int(fs*0.6), fx+fs, fy+int(fs*0.6)],
                 rng.randint(0, 60), rng.randint(200, 320),
                 fill=hc(ac), width=rng.randint(10, 22))
        # 第二道弧
        draw.arc([fx-int(fs*0.7), fy-int(fs*0.4), fx+int(fs*0.7), fy+int(fs*0.4)],
                 rng.randint(30, 90), rng.randint(240, 300),
                 fill=hc(dk), width=rng.randint(4, 10))
        # 填充扇区
        ol2 = Image.new("RGBA", (W, H), (0,0,0,0))
        od2 = ImageDraw.Draw(ol2)
        pts = [(fx, fy), (fx+fs, fy-int(fs*0.5)), (fx+int(fs*0.8), fy+int(fs*0.4))]
        od2.polygon(pts, fill=(md[0], md[1], md[2], 60))
        img = Image.alpha_composite(img.convert("RGBA"), ol2).convert("RGB")

    elif ftype == "dual_shape":
        # 双图形组合：一个实心 + 一个轮廓
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        od.rounded_rectangle([fx-fs//2, fy-fs//3, fx+fs//2, fy+fs//3],
                             radius=20, fill=(dk[0], dk[1], dk[2], 140))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")
        draw.rounded_rectangle([fx-fs//2+20, fy-fs//3-20, fx+fs//2+20, fy+fs//3-20],
                               radius=12, outline=hc(ac), width=3)

    elif ftype == "layered_rect":
        # 多层错位矩形
        for li in range(5):
            off = li * rng.randint(12, 22)
            rw, rh = fs - li * 25, int(fs * 0.55) - li * 12
            if rw < 20 or rh < 10:
                continue
            ci = [dk, ac, md, (*[min(255, c+20) for c in palette["mid"]],), gl][li % 5]
            ol_l = Image.new("RGBA", (W, H), (0,0,0,0))
            od_l = ImageDraw.Draw(ol_l)
            od_l.rounded_rectangle([fx-rw//2-off, fy-rh//2-off//2,
                                 fx+rw//2-off, fy+rh//2-off//2],
                                radius=rng.randint(3, 12),
                                fill=(ci[0], ci[1], ci[2], 100-li*15))
            img = Image.alpha_composite(img.convert("RGBA"), ol_l).convert("RGB")

    # 散布装饰点（确保不空旷）
    for _ in range(rng.randint(10, 20)):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        dr = rng.randint(2, 10)
        dci = rng.choice([ac, gl, dk])
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        od.ellipse([dx-dr, dy-dr, dx+dr, dy+dr],
                   fill=(dci[0], dci[1], dci[2], rng.randint(30, 80)))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 细线条装饰
    for _ in range(rng.randint(2, 4)):
        x1 = rng.randint(0, W)
        y1 = rng.randint(0, H)
        x2 = x1 + rng.randint(-150, 150)
        y2 = y1 + rng.randint(-80, 80)
        draw.line([(x1, y1), (x2, y2)], fill=hc(gl), width=1)

    return add_noise(img, seed)


def style_duotone_texture(palette, seed=0):
    """H: 双色调纹理 — 高端克制、精致质感"""
    rng = random.Random(seed)
    dk = palette["dark"]
    lt = palette["light"]
    md = palette["mid"]
    ac = palette["accent"]
    gl = palette["glow"]

    img = Image.new("RGB", (W, H), lt)
    draw = ImageDraw.Draw(img)

    shape = rng.choice(["wedge", "curved_wedge", "corner_fill",
                        "organic_block", "stripe_field"])

    if shape == "wedge":
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        pts = [(int(W*0.55), 0), (W, 0), (W, H),
               (int(W*0.35), H), (int(W*0.15), int(H*0.6))]
        od.polygon(pts, fill=(dk[0], dk[1], dk[2], 175))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")
        # 内部浅区
        ol2 = Image.new("RGBA", (W, H), (0,0,0,0))
        od2 = ImageDraw.Draw(ol2)
        pts2 = [(int(W*0.7), 0), (W, 0), (W, int(H*0.4)),
                (int(W*0.5), int(H*0.4))]
        od2.polygon(pts2, fill=(md[0], md[1], md[2], 80))
        img = Image.alpha_composite(img.convert("RGBA"), ol2).convert("RGB")

    elif shape == "curved_wedge":
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        pts = []
        for i in range(20):
            x = int(W * i / 19)
            y = int(H * 0.5 + H * 0.35 * math.sin(math.pi * i / 19) +
                  rng.randint(-8, 8))
            pts.append((x, y))
        pts = [(0, 0)] + pts + [(W, H), (0, H)]
        od.polygon(pts, fill=(dk[0], dk[1], dk[2], 165))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    elif shape == "corner_fill":
        corners = rng.choice(["br", "tr", "bl", "tl"])
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        if corners == "br":
            pts = [(int(W*0.5), H), (W, H), (W, int(H*0.3)), (int(W*0.3), int(H*0.5))]
        elif corners == "tr":
            pts = [(int(W*0.5), 0), (W, 0), (W, int(H*0.7)), (int(W*0.3), int(H*0.5))]
        elif corners == "bl":
            pts = [(0, int(H*0.5)), (int(W*0.3), int(H*0.7)), (int(W*0.5), H), (0, H)]
        else:
            pts = [(0, int(H*0.5)), (int(W*0.3), int(H*0.3)), (int(W*0.5), 0), (0, 0)]
        od.polygon(pts, fill=(dk[0], dk[1], dk[2], 170))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    elif shape == "organic_block":
        ol = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ol)
        cx, cy = W * 0.62, H * 0.5
        npts = 14
        pts = []
        for j in range(npts):
            angle = 2 * math.pi * j / npts + rng.uniform(-0.2, 0.2)
            rx = rng.randint(int(W*0.28), int(W*0.48))
            ry = rng.randint(int(H*0.28), int(H*0.48))
            pts.append((int(cx + rx * math.cos(angle)),
                       int(cy + ry * math.sin(angle))))
        od.polygon(pts, fill=(dk[0], dk[1], dk[2], 175))
        img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    elif shape == "stripe_field":
        stripe_w = rng.randint(35, 65)
        for si in range(-1, W // stripe_w + 3):
            x = si * stripe_w + rng.randint(-8, 8)
            if si % 3 == 0:
                ol = Image.new("RGBA", (W, H), (0,0,0,0))
                od = ImageDraw.Draw(ol)
                od.rectangle([x, 0, x + int(stripe_w*1.5), H],
                            fill=(dk[0], dk[1], dk[2], rng.randint(70, 145)))
                img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")
            elif si % 3 == 1:
                ol = Image.new("RGBA", (W, H), (0,0,0,0))
                od = ImageDraw.Draw(ol)
                od.rectangle([x, 0, x + int(stripe_w*0.6), H],
                            fill=(md[0], md[1], md[2], rng.randint(40, 90)))
                img = Image.alpha_composite(img.convert("RGBA"), ol).convert("RGB")

    # 点阵纹理覆盖全图
    dot_step = 7
    for y in range(dot_step//2, H, dot_step):
        for x in range(dot_step//2, W, dot_step):
            if rng.random() > 0.55:
                dv = rng.randint(-10, 10)
                c = lt
                draw.point((x, y), fill=hc((max(0,c[0]+dv), max(0,c[1]+dv), max(0,c[2]+dv))))

    # 一条醒目分割线
    ly = rng.randint(int(H*0.35), int(H*0.65))
    draw.line([(0, ly), (W, ly + rng.randint(-20, 20))],
              fill=hc(ac), width=rng.randint(1, 3))

    return add_noise(img, seed, level=3)


# ── 风格列表 ──
ALL_STYLES = [
    style_blob_layers,         # A
    style_diagonal_split,      # B
    style_arc_composition,     # C
    style_mesh_gradient,       # D
    style_wave_organic,        # E
    style_brutalist_blocks,    # F
    style_minimal_focus,       # G
    style_duotone_texture,     # H
]


# ── 文章→分类映射 ──
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

STATIC_CATEGORY = {
    "index":     "brand",
    "about":     "brand",
    "contact":   "brand",
    "links":     "office",
    "privacy":   "review",
    "disclaimer":"review",
    "sitemap":   "office",
}


def pick_style(filename, idx):
    hash_val = sum(ord(c) for c in filename)
    return ALL_STYLES[(hash_val + idx * 11) % len(ALL_STYLES)]


def generate_banner(filename, category_key, index=0):
    palette = PALETTES.get(category_key, PALETTES["brand"])
    style_fn = pick_style(filename, index)
    seed = (hash(filename) & 0xFFFFFF) + index * 31

    img = style_fn(palette, seed=seed)
    out_path = os.path.join(OUT_DIR, filename + ".png")
    img.save(out_path, "PNG", optimize=True)
    style_name = style_fn.__doc__.split("—")[0].strip() if style_fn.__doc__ else "?"
    print(f"  OK {filename}.png [{palette['name']}] {style_name}")
    return out_path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"输出目录: {OUT_DIR}  尺寸: {W}x{H}")
    print("=" * 60)

    all_files = []
    for fname, cat in ARTICLE_CATEGORY.items():
        all_files.append((fname, cat))
    for fname, cat in STATIC_CATEGORY.items():
        all_files.append((fname, cat))

    print(f"共 {len(all_files)} 张横幅\n")

    for i, (fname, cat) in enumerate(all_files):
        generate_banner(fname, cat, index=i)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
