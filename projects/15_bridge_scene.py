"""
Project 30 — Bridge Scene
Part 2: City & Architecture
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

A suspension bridge built on real physics: the main cables follow a
catenary curve (a*cosh(x/a)) between the two towers, with evenly spaced
vertical suspender lines down to the deck — plus a river and a couple of
small boats.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, catenary, wave_sum

# ---- Change these parameters to create your own variation ----
SEED = 3
SKY_TOP = (160, 200, 230)
SKY_HORIZON = (235, 235, 220)
RIVER_TOP = (90, 140, 160)
RIVER_DEEP = (25, 55, 70)
TOWER_X = 0.55
TOWER_HEIGHT = 0.55
DECK_Y = -0.1
CATENARY_A = 0.9
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

    add_sky(ax, (-1, 1), (DECK_Y, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    add_sky(ax, (-1, 1), (-1, DECK_Y), np.array(RIVER_TOP) / 255, np.array(RIVER_DEEP) / 255)

    for tx in (-TOWER_X, TOWER_X):
        ax.add_patch(Rectangle((tx - 0.03, DECK_Y), 0.06, TOWER_HEIGHT,
                                facecolor=(0.25, 0.22, 0.24), zorder=5))

    # main cable: a catenary between the two towers
    x = np.linspace(-TOWER_X, TOWER_X, 200)
    y0 = catenary(np.array([-TOWER_X]), CATENARY_A)[0]
    y = catenary(x, CATENARY_A) - y0 + DECK_Y + TOWER_HEIGHT
    ax.plot(x, y, color=(0.2, 0.18, 0.2), linewidth=2, zorder=4)

    # side spans running down to the ground at each end
    for side, tx in ((-1, -TOWER_X), (1, TOWER_X)):
        ex = tx + side * 0.35
        ax.plot([tx, ex], [DECK_Y + TOWER_HEIGHT, DECK_Y], color=(0.2, 0.18, 0.2), linewidth=2, zorder=4)

    # vertical suspenders down to the deck
    for sx in np.linspace(-TOWER_X + 0.04, TOWER_X - 0.04, 24):
        cable_y = np.interp(sx, x, y)
        ax.plot([sx, sx], [cable_y, DECK_Y], color=(0.35, 0.32, 0.3), linewidth=0.6, alpha=0.8, zorder=3)

    # deck
    ax.add_patch(Rectangle((-1, DECK_Y - 0.025), 2, 0.025, facecolor=(0.3, 0.27, 0.25), zorder=6))

    # river surface ripples
    rx = np.linspace(-1, 1, 400)
    for i, depth in enumerate(np.linspace(-0.02, -0.75, 18)):
        ry = depth + wave_sum(rx, [(0.015, 6, i * 0.4), (0.008, 13, i)])
        shade = 1 - i / 18
        color = np.array(RIVER_TOP) / 255 * shade + np.array(RIVER_DEEP) / 255 * (1 - shade)
        ax.plot(rx, ry, color=color, linewidth=0.7, alpha=0.6, zorder=1)

    # a couple of small boats
    for bx in (-0.4, 0.15):
        by = -0.25 + rng.uniform(-0.02, 0.02)
        hull = [(bx - 0.08, by), (bx + 0.08, by), (bx + 0.05, by - 0.035), (bx - 0.05, by - 0.035)]
        ax.add_patch(Polygon(hull, closed=True, facecolor=(0.25, 0.2, 0.18), zorder=7))
        ax.plot([bx, bx], [by, by + 0.08], color=(0.2, 0.15, 0.12), linewidth=1, zorder=7)
        ax.add_patch(Polygon([(bx, by + 0.08), (bx, by + 0.02), (bx + 0.05, by + 0.04)],
                              facecolor=(0.95, 0.95, 0.9), zorder=7))

    out_path = out_dir / "15_bridge_scene.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
