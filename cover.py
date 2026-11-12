#!/usr/bin/env python3
"""画一张封面：深海底的渐变 + 一条鲸鱼剪影 + 标题。不依赖任何外部素材。"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 750
img = Image.new("RGB", (W, H), (8, 18, 30))
d = ImageDraw.Draw(img)

# 纵向渐变：上浅下深
top = (18, 46, 72)
bottom = (5, 10, 18)
for y in range(H):
    t = y / (H - 1)
    c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# 几缕从水面落下来的光
for i, x0 in enumerate((180, 420, 760, 980)):
    alpha = 14 + i * 3
    for k in range(70):
        x = x0 + k * 1.6
        d.line([(x, 0), (x + 120, H * 0.85)], fill=(
            min(255, top[0] + alpha), min(255, top[1] + alpha), min(255, top[2] + alpha)))

# 鲸鱼剪影（身体 + 尾 + 鳍），用极坐标画
def whale(cx, cy, s, color):
    # 身体：一组椭圆叠加
    d.ellipse([cx - 300 * s, cy - 120 * s, cx + 210 * s, cy + 120 * s], fill=color)
    # 头
    d.ellipse([cx - 340 * s, cy - 95 * s, cx - 140 * s, cy + 95 * s], fill=color)
    # 尾巴
    tail = [
        (cx + 190 * s, cy),
        (cx + 330 * s, cy - 130 * s),
        (cx + 300 * s, cy - 40 * s),
        (cx + 380 * s, cy - 10 * s),
        (cx + 300 * s, cy + 40 * s),
        (cx + 330 * s, cy + 130 * s),
    ]
    d.polygon(tail, fill=color)
    # 下面的鳍
    d.polygon([(cx - 40 * s, cy + 80 * s), (cx + 60 * s, cy + 230 * s), (cx + 120 * s, cy + 70 * s)], fill=color)

whale(560, 430, 1.0, (16, 34, 54))

# 标题
def font(size, bold=False):
    path = "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc"
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

d.text((90, 120), "海里的日子", font=font(86, True), fill=(226, 238, 248))
d.text((94, 232), "十来天的日记里挑出来的几段", font=font(30), fill=(140, 178, 208))
d.text((94, H - 96), "困困", font=font(28), fill=(110, 150, 180))

img.save("第一篇/cover.png")
print("封面生成：第一篇/cover.png")
