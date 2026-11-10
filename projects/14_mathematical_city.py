"""
Project 28 — Mathematical City
Part 2: City & Architecture
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

A full skyline built from nothing but rectangles, triangles, and
repetition: random-width building blocks, a repeated grid of windows on
each one, a few triangular rooftops, and a street with simple perspective
lane markings.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky

# ---- Change these parameters to create your own variation ----
SEED = 6
N_BUILDINGS = 11
SKY_TOP = (120, 178, 224)
SKY_HORIZON = (221, 236, 240)
# ------------------------------------------------------------------


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 6.5), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (-0.35, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    ax.fill_between([-1, 1], -1, -0.35, color=(0.3, 0.3, 0.33), zorder=5)

    x = -1.05
    grays = np.linspace(0.75, 0.25, N_BUILDINGS)
    for i in range(N_BUILDINGS):
        width = rng.uniform(0.12, 0.24)
        height = rng.uniform(0.3, 0.95)
        base_y = -0.35
        tint = grays[(i * 3) % N_BUILDINGS]
        color = (tint * 0.8, tint * 0.85, tint * 0.95)
        ax.add_patch(Rectangle((x, base_y), width, height, facecolor=color,
                                edgecolor=(0.15, 0.15, 0.18), linewidth=0.5, zorder=6))

        # repeated grid of windows
        rows = int(height / 0.09)
        cols = max(1, int(width / 0.06))
        win_w, win_h = width / cols * 0.55, 0.09 * 0.55
        for r in range(rows):
            for c in range(cols):
                if rng.random() < 0.25:
                    continue
                wx = x + width / cols * (c + 0.5) - win_w / 2
                wy = base_y + 0.05 + r * 0.09
                lit = rng.random() < 0.5
                wcolor = (1.0, 0.92, 0.55) if lit else (0.55, 0.6, 0.65)
                ax.add_patch(Rectangle((wx, wy), win_w, win_h, facecolor=wcolor,
                                        edgecolor="none", zorder=6.1))

        # occasional triangular rooftop
        if rng.random() < 0.4:
            roof_h = rng.uniform(0.05, 0.12)
            apex = (x + width / 2, base_y + height + roof_h)
            ax.add_patch(Polygon([(x, base_y + height), (x + width, base_y + height), apex],
                                  facecolor=color, edgecolor=(0.15, 0.15, 0.18), linewidth=0.5, zorder=6))

        x += width + rng.uniform(0.0, 0.03)

    # street with simple perspective lane markings
    for lx in np.linspace(-0.9, 0.9, 10):
        ax.add_patch(Rectangle((lx, -0.75), 0.12, 0.04, facecolor=(0.9, 0.9, 0.85), zorder=7))

    out_path = out_dir / "14_mathematical_city.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
