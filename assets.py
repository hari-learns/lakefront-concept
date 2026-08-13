"""Resize source photography into web assets for the static build.

Source JPEGs are expected in build_src/img/ (not committed — see README).
Run: python3 assets.py
"""
import os
from PIL import Image, ImageOps

SRC = "build_src/img"
OUT = "assets"

# name -> (source file stem, target width, aspect (w,h) or None for no-crop, quality)
SPEC = {
    "hero":     ("hero_0593", 1650, (16, 9), 56),
    "facade":   ("facade_0901", 1150, (4, 3), 62),
    "corridor": ("corridor_0611", 1500, (16, 7), 60),

    "rm_family":    ("rm_family_0855", 820, (4, 3), 60),
    "rm_honeymoon": ("rm_honeymoon_0793", 820, (4, 3), 60),
    "rm_deluxe":    ("rm_deluxe_0861", 820, (4, 3), 60),
    "rm_premium":   ("rm_premium_0751", 820, (4, 3), 60),
    "rm_economy":   ("rm_economy_0667", 820, (4, 3), 60),
    "rm_mini":      ("rm_mini_0711", 820, (4, 3), 60),

    "g1": ("g1_0658", 660, (3, 4), 58),
    "g2": ("g2_0690", 660, (4, 3), 58),
    "g3": ("g3_0832", 660, (4, 3), 58),
    "g4": ("g4_0734", 660, (3, 4), 58),
    "g5": ("g5_0870", 660, (4, 3), 58),
    "g6": ("g6_0913", 660, (4, 3), 58),

    "t_boating":   ("t_boating", 780, (3, 2), 54),
    "t_mudumalai": ("t_mudumalai", 780, (3, 2), 54),
    "t_coonoor":   ("t_coonoor", 780, (3, 2), 54),
    "t_pine":      ("t_pine", 780, (3, 2), 54),
    "t_kodanad":   ("t_kodanad", 780, (3, 2), 54),
    "t_ooty":      ("t_ooty", 780, (3, 2), 54),

    # newly sourced — gallery page + room-detail companion shots
    "n_0584": ("n_0584", 900, (4, 3), 58),
    "n_0617": ("n_0617", 900, (3, 4), 58),
    "n_0632": ("n_0632", 900, (4, 3), 58),
    "n_0663": ("n_0663", 900, (4, 3), 58),
    "n_0674": ("n_0674", 900, (4, 3), 58),
    "n_0686": ("n_0686", 900, (4, 3), 58),
    "n_0702": ("n_0702", 900, (3, 4), 58),
    "n_0741": ("n_0741", 900, (4, 3), 58),
    "n_0756": ("n_0756", 900, (4, 3), 58),
    "n_0785": ("n_0785", 900, (4, 3), 58),
    "n_0817": ("n_0817", 900, (4, 3), 58),
    "n_0838": ("n_0838", 900, (4, 3), 58),
    "n_0883": ("n_0883", 900, (4, 3), 58),
    "n_0906": ("n_0906", 900, (3, 4), 58),
    "n_0919": ("n_0919", 900, (4, 3), 58),
    "n_0923": ("n_0923", 900, (3, 4), 58),
    "n_0925": ("n_0925", 900, (4, 3), 58),
    "n_0933": ("n_0933", 900, (4, 3), 58),
    "n_0958": ("n_0958", 900, (4, 3), 58),
    "n_roommini1": ("n_roommini1", 900, (4, 3), 58),
    "n_roommini2": ("n_roommini2", 900, (3, 4), 58),
}


def build():
    os.makedirs(OUT, exist_ok=True)
    missing = []
    total = 0
    for name, (stem, w, aspect, q) in SPEC.items():
        src_path = None
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            p = os.path.join(SRC, stem + ext)
            if os.path.exists(p):
                src_path = p
                break
        if not src_path:
            missing.append(stem)
            continue
        im = ImageOps.exif_transpose(Image.open(src_path).convert("RGB"))
        if aspect:
            im = ImageOps.fit(im, (w, round(w * aspect[1] / aspect[0])), Image.LANCZOS, centering=(0.5, 0.4))
        else:
            im.thumbnail((w, w * 3), Image.LANCZOS)
        out_path = os.path.join(OUT, name + ".webp")
        im.save(out_path, "WEBP", quality=q, method=6)
        total += os.path.getsize(out_path)
    print(f"built {len(SPEC) - len(missing)}/{len(SPEC)} images, {total/1_048_576:.2f} MB")
    if missing:
        print("MISSING source files (place in build_src/img/):", missing)


if __name__ == "__main__":
    build()
