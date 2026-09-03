# -*- coding: utf-8 -*-
"""
デモ用のプレースホルダ画像（SVG）を作る。

写真は一切使わない。すべてこのスクリプトが図形として描くので、
著作権の心配なくGitHubなどに公開できる。
本番では、ここを実際に撮影した写真に差し替える。
"""
import os, io, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "img")

PALETTES = {
    "grain":  ["#1B4E8E", "#2F6FB5", "#5A93CE", "#9CBFE3", "#003399", "#7FA8D6"],
    "lattice": ["#003399", "#2F6FB5", "#8FB3D9"],
    "layers": ["#00246B", "#003399", "#2F6FB5", "#5A93CE", "#B9CBEC"],
}


def grain_map(path, w=760, h=428, seed=7, cells=52):
    """結晶粒マップ風。ボロノイ図で塗り分けたPNGを書き出す（SVGだと重いため）。"""
    from PIL import Image, ImageDraw
    rnd = random.Random(seed)
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(cells)]
    pal = [(27, 78, 142), (47, 111, 181), (90, 147, 206), (156, 191, 227),
           (0, 51, 153), (127, 168, 214), (63, 96, 160), (110, 170, 220)]
    im = Image.new("RGB", (w, h), (11, 31, 63))
    px = im.load()
    for gx in range(w):
        for gy in range(h):
            best, bi = 1e18, 0
            for i, (ax, ay) in enumerate(pts):
                d = (ax - gx) ** 2 + (ay - gy) ** 2
                if d < best:
                    best, bi = d, i
            px[gx, gy] = pal[bi % len(pal)]
    ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=(200, 214, 236))
    im.save(path, "PNG", optimize=True)
    return path


def lattice(w=760, h=428):
    """格子構造の模式図。金属積層造形のラティスをイメージ。"""
    pal = PALETTES["lattice"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="格子構造の模式図">',
           f'<rect width="{w}" height="{h}" fill="#F2F6FC"/>']
    cell, ox, oy, dx, dy = 62, 70, 60, 26, -20
    for r in range(5):
        for c in range(9):
            x = ox + c * cell + r * dx
            y = oy + r * cell + r * dy % 1
            y = oy + r * (cell * 0.62)
            x = ox + c * cell + r * dx
            op = 0.30 + 0.14 * r
            col = pal[(r + c) % len(pal)]
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell-16}" height="{cell-16}" '
                       f'fill="none" stroke="{col}" stroke-width="2" opacity="{op:.2f}" rx="2"/>')
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{col}" opacity="{min(op+0.25,1):.2f}"/>')
    out.append('</svg>')
    return "".join(out)


def layers(w=760, h=428):
    """積層方向の異方性をイメージした層状の図。"""
    pal = PALETTES["layers"]
    rnd = random.Random(3)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="積層構造の模式図">',
           f'<rect width="{w}" height="{h}" fill="#0A1730"/>']
    y = 18
    i = 0
    while y < h - 10:
        t = rnd.uniform(9, 26)
        col = pal[i % len(pal)]
        out.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{t:.0f}" fill="{col}" opacity="{rnd.uniform(.35,.95):.2f}"/>')
        for _ in range(int(w / 90)):
            cx = rnd.uniform(0, w)
            out.append(f'<rect x="{cx:.0f}" y="{y:.0f}" width="{rnd.uniform(20,70):.0f}" height="{t:.0f}" '
                       f'fill="#FFFFFF" opacity="{rnd.uniform(.04,.16):.2f}"/>')
        y += t + rnd.uniform(2, 7)
        i += 1
    out.append(f'<rect width="{w}" height="{h}" fill="none" stroke="rgba(255,255,255,.12)"/>')
    out.append('</svg>')
    return "".join(out)


def portrait(initial, w=260, h=347, tint="#EAF1FF", fg="#3584BB"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="人物写真のプレースホルダ">'
            f'<rect width="{w}" height="{h}" fill="{tint}"/>'
            f'<circle cx="{w/2:.0f}" cy="{h*0.40:.0f}" r="{w*0.20:.0f}" fill="{fg}" opacity=".28"/>'
            f'<path d="M {w*0.18:.0f} {h} a {w*0.32:.0f} {h*0.30:.0f} 0 0 1 {w*0.64:.0f} 0 Z" fill="{fg}" opacity=".28"/>'
            f'<text x="{w/2:.0f}" y="{h*0.47:.0f}" text-anchor="middle" font-family="sans-serif" '
            f'font-size="{w*0.20:.0f}" font-weight="700" fill="#FFFFFF">{initial}</text>'
            f'</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    grain_map(os.path.join(OUT, "fig-grain.png"))
    print("   fig-grain.png")
    files = {
        "fig-lattice.svg": lattice(),
        "fig-layers.svg": layers(),
    }
    for i, ini in enumerate(["A", "B", "C", "D", "E"], 1):
        files[f"person-{i}.svg"] = portrait(ini)
    for name, svg in files.items():
        with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("  ", name, len(svg) // 1024, "KB")
    print("完了：", len(files), "個の図版を生成しました")


if __name__ == "__main__":
    main()
