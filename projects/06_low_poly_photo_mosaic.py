"""
Project 07 — Low-Poly Photo Mosaic
Difficulty: medium | Time: ~10-20 seconds
Libraries: numpy, Pillow

A real, widely-used photo effect (the "crystallize" / low-poly art look
seen in posters and app icons): sample more seed points along strong
edges, give every pixel to its nearest seed, and color each cell with the
average color of the photo underneath it.

Run this on your OWN photo: just change IMAGE_PATH below.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.sample_photo import ensure_sample_photo

# ---- Change these parameters to create your own variation ----
IMAGE_PATH = Path(__file__).resolve().parent.parent / "assets" / "sample_photo.png"
SEED = 3
N_CELLS = 500
WORK_WIDTH = 480          # internal computation width (speed/quality trade-off)
UPSCALE = 2               # final image = WORK_WIDTH * UPSCALE pixels wide
EDGE_DARKEN = 0.25
# ------------------------------------------------------------------


def nearest_seed_raster(height, width, seeds):
    yy, xx = np.mgrid[0:height, 0:width]
    best_dist = np.full((height, width), np.inf)
    second_dist = np.full((height, width), np.inf)
    nearest = np.zeros((height, width), dtype=int)
    for i, (sx, sy) in enumerate(seeds):
        d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)
        closer = d < best_dist
        second_dist = np.where(closer, best_dist, np.minimum(second_dist, d))
        best_dist = np.where(closer, d, best_dist)
        nearest = np.where(closer, i, nearest)
    return nearest, best_dist, second_dist


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    ensure_sample_photo(IMAGE_PATH)
    img = Image.open(IMAGE_PATH).convert("RGB")
    work_h = round(WORK_WIDTH * img.height / img.width)
    work = img.resize((WORK_WIDTH, work_h))
    arr = np.array(work).astype(float)

    gray = arr.mean(axis=2)
    gy, gx = np.gradient(gray)
    grad_mag = np.sqrt(gx ** 2 + gy ** 2)
    prob = grad_mag + grad_mag.mean() * 0.35
    prob = prob.ravel()
    prob /= prob.sum()

    flat_idx = rng.choice(work_h * WORK_WIDTH, size=N_CELLS, replace=False, p=prob)
    seed_y, seed_x = np.unravel_index(flat_idx, (work_h, WORK_WIDTH))
    seeds = list(zip(seed_x.tolist(), seed_y.tolist()))

    nearest, best_dist, second_dist = nearest_seed_raster(work_h, WORK_WIDTH, seeds)

    colors = np.zeros((N_CELLS, 3))
    for i in range(N_CELLS):
        mask = nearest == i
        if mask.any():
            colors[i] = arr[mask].mean(axis=0)
        else:
            colors[i] = arr[seed_y[i], seed_x[i]]

    mosaic = colors[nearest]
    edges = (second_dist - best_dist) < 1.2
    mosaic[edges] *= EDGE_DARKEN

    final = Image.fromarray(np.clip(mosaic, 0, 255).astype(np.uint8))
    final = final.resize((WORK_WIDTH * UPSCALE, work_h * UPSCALE), Image.NEAREST)

    out_path = out_dir / "006_low_poly_photo_mosaic.png"
    final.save(out_path)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
