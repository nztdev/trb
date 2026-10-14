"""Regenerates every TRB icon and iOS splash image.

Usage (from the repo root):   python tools/make_icons.py
Needs:                        pip install pillow numpy
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def radial(S, cx, cy, r, stops):
    """RGB image (S x S) with a radial gradient. stops = [(t, (r, g, b)), ...] with t in 0..1."""
    y, x = np.mgrid[0:S, 0:S]
    d = np.clip(np.hypot(x - cx, y - cy) / r, 0, 1)
    out = np.zeros((S, S, 3), np.float32)
    for c in range(3):
        out[..., c] = np.interp(d, [s[0] for s in stops], [s[1][c] for s in stops])
    return Image.fromarray(out.astype(np.uint8), "RGB")


def disc(S, cx, cy, r):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    return m


def button(size, scale, bg=True):
    """The red button seen from above, as a size x size RGBA image.

    scale = outer radius as a fraction of the image size
    bg    = paint the dark spotlit background (False = transparent, used for splash screens)
    """
    S = size * 2  # supersample, downscaled at the end for smooth edges
    cx, cy, Ro = S / 2, S * 0.52, S * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    if bg:
        base = radial(S, S * .5, S * .40, S * .75,
                      [(0, (30, 37, 43)), (.6, (10, 13, 16)), (1, (3, 4, 6))]).convert("RGBA")
        cone = Image.new("L", (S, S), 0)
        ImageDraw.Draw(cone).polygon([(S * .40, 0), (S * .60, 0), (S * .92, S), (S * .08, S)], fill=70)
        cone = cone.filter(ImageFilter.GaussianBlur(S * .04))
        light = Image.new("RGBA", (S, S), (255, 236, 210, 255))
        base.paste(light, (0, 0), cone.point(lambda v: int(v * .35)))
        img.alpha_composite(base)

    # red glow behind the button
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((cx - Ro * 1.04, cy - Ro * 1.04, cx + Ro * 1.04, cy + Ro * 1.04),
                                 fill=(255, 40, 20, 150))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(S * .035)))

    # metal housing
    hous = radial(S, cx - Ro * .2, cy - Ro * .25, Ro * 1.5,
                  [(0, (96, 104, 112)), (.55, (52, 58, 64)), (1, (18, 21, 24))]).convert("RGBA")
    hous.putalpha(disc(S, cx, cy, Ro))
    img.alpha_composite(hous)
    d = ImageDraw.Draw(img)
    d.ellipse((cx - Ro, cy - Ro, cx + Ro, cy + Ro), outline=(150, 158, 166, 255), width=max(2, int(S * .004)))

    # yellow / black hazard ring
    n, r1, r2 = 32, Ro * .80, Ro * .93
    step = 360 / n
    skew = math.radians(step * .55)
    for i in range(n):
        a0, a1 = math.radians(i * step), math.radians((i + 1) * step)
        pts = [(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)),
               (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)),
               (cx + r2 * math.cos(a1 + skew), cy + r2 * math.sin(a1 + skew)),
               (cx + r2 * math.cos(a0 + skew), cy + r2 * math.sin(a0 + skew))]
        d.polygon(pts, fill=(236, 184, 0, 255) if i % 2 == 0 else (14, 14, 14, 255))
    for rr in (r1, r2):
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(20, 22, 24, 255), width=max(2, int(S * .004)))

    # chrome collar and bolts
    col = radial(S, cx - Ro * .2, cy - Ro * .25, Ro * .8,
                 [(0, (236, 240, 244)), (.5, (150, 158, 166)), (1, (70, 76, 82))]).convert("RGBA")
    m = disc(S, cx, cy, Ro * .70)
    ImageDraw.Draw(m).ellipse((cx - Ro * .61, cy - Ro * .61, cx + Ro * .61, cy + Ro * .61), fill=0)
    col.putalpha(m)
    img.alpha_composite(col)
    d = ImageDraw.Draw(img)
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        bx, by, br = cx + Ro * .745 * math.cos(a), cy + Ro * .745 * math.sin(a), Ro * .025
        d.ellipse((bx - br, by - br, bx + br, by + br), fill=(210, 216, 222, 255), outline=(40, 44, 48, 255))

    # glossy red cap
    Rc = Ro * .60
    cap = radial(S, cx - Rc * .28, cy - Rc * .34, Rc * 1.35,
                 [(0, (255, 104, 80)), (.25, (228, 40, 28)), (.7, (176, 12, 10)), (1, (96, 4, 6))]).convert("RGBA")
    cap.putalpha(disc(S, cx, cy, Rc))
    img.alpha_composite(cap)
    rim = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(rim).ellipse((cx - Rc, cy - Rc, cx + Rc, cy + Rc), outline=(60, 0, 0, 150), width=int(S * .012))
    img.alpha_composite(rim.filter(ImageFilter.GaussianBlur(S * .004)))
    hl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse((cx - Rc * .62, cy - Rc * .72, cx - Rc * .02, cy - Rc * .22), fill=(255, 255, 255, 170))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(S * .018)))
    dot = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(dot).ellipse((cx - Rc * .52, cy - Rc * .6, cx - Rc * .3, cy - Rc * .42), fill=(255, 255, 255, 235))
    img.alpha_composite(dot.filter(ImageFilter.GaussianBlur(S * .006)))

    return img.resize((size, size), Image.LANCZOS)


def simple(size):
    """Hazard-free version of the button for tiny sizes (favicons)."""
    S = size * 8
    cx = cy = S / 2
    img = Image.new("RGBA", (S, S), (7, 10, 12, 255))
    d = ImageDraw.Draw(img)
    d.ellipse((cx - S * .47, cy - S * .47, cx + S * .47, cy + S * .47), fill=(58, 64, 70, 255), outline=(150, 158, 166, 255), width=int(S * .03))
    d.ellipse((cx - S * .38, cy - S * .38, cx + S * .38, cy + S * .38), fill=(236, 184, 0, 255))
    cap = radial(S, cx - S * .1, cy - S * .12, S * .5, [(0, (255, 104, 80)), (.3, (228, 40, 28)), (.8, (150, 8, 8)), (1, (96, 4, 6))]).convert("RGBA")
    cap.putalpha(disc(S, cx, cy, S * .31))
    img.alpha_composite(cap)
    hl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse((cx - S * .2, cy - S * .24, cx - S * .02, cy - S * .08), fill=(255, 255, 255, 190))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(S * .02)))
    return img.resize((size, size), Image.LANCZOS)


def save(img, path, flat=False):
    """Save as PNG. flat=True removes transparency (required for the iOS home-screen icon)."""
    if flat:
        bg = Image.new("RGB", img.size, (7, 10, 12))
        bg.paste(img, (0, 0), img)
        img = bg
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)


def main():
    icons = os.path.join(ROOT, "icons")
    for size in (192, 512):
        save(button(size, .44), os.path.join(icons, f"icon-{size}.png"), flat=True)
    # maskable: artwork kept inside the central 80% "safe zone" so Android can crop it to any shape
    save(button(512, .33), os.path.join(icons, "icon-maskable-512.png"), flat=True)
    save(button(180, .44), os.path.join(icons, "apple-touch-icon.png"), flat=True)
    save(simple(32), os.path.join(icons, "favicon-32.png"), flat=True)

    # iOS launch screens (portrait): pure black with the button in the middle
    for w, h in ((1290, 2796), (1179, 2556), (1170, 2532), (1125, 2436),
                 (1242, 2688), (1242, 2208), (828, 1792), (750, 1334)):
        sp = Image.new("RGB", (w, h), (0, 0, 0))
        b = button(int(w * .46), .44, bg=False)
        sp.paste(b, ((w - b.width) // 2, int(h * .5 - b.height * .5)), b)
        save(sp, os.path.join(ROOT, "splash", f"splash-{w}x{h}.png"))
    print("icons done")


if __name__ == "__main__":
    main()
