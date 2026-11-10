"""
Project 27 — Desert Dunes
Part 1: Nature Scenes
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

Smooth, curving sand dunes built from sums of Gaussian bumps (instead of
the jagged fractal ridges used for mountains) — Gaussians naturally give
the soft, rounded profile real dunes have.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, add_sun_or_moon

# ---- Change these parameters to create your own variation ----
SEED = 23
N_DUNES = 4
SKY_TOP = (120, 160, 210)
SKY_HORIZON = (255, 214, 160)
SUN_COLOR = (255, 244, 214)
# ------------------------------------------------------------------


def gaussian_dune(x, bumps):
    y = np.zeros_like(x)
    for center, width, height in bumps:
        y += height * np.exp(-((x - center) ** 2) / (2 * width ** 2))
    return y


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (-1, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    add_sun_or_moon(ax, (0.45, 0.55), 0.11, np.array(SUN_COLOR) / 255, glow=True, glow_layers=5, zorder=1)

    x = np.linspace(-1.2, 1.2, 400)
    base_ys = np.linspace(0.05, -0.65, N_DUNES)
    sand_light = np.array([237, 201, 150]) / 255
    sand_dark = np.array([170, 120, 80]) / 255

    for i, base_y in enumerate(base_ys):
        n_bumps = rng.integers(2, 4)
        bumps = [(rng.uniform(-1, 1), rng.uniform(0.25, 0.55), rng.uniform(0.08, 0.18))
                 for _ in range(n_bumps)]
        y = base_y + gaussian_dune(x, bumps)
        shade = 1 - i / N_DUNES
        color = sand_light * shade + sand_dark * (1 - shade)
        pts = list(zip(x, y)) + [(1.2, -1), (-1.2, -1)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=i))

        # fine ridge line + light stipple texture for sand grain
        ax.plot(x, y, color=color * 0.85, linewidth=0.8, zorder=i + 0.5)
        grain_x = rng.uniform(-1, 1, 250)
        grain_y_offset = rng.uniform(-0.02, 0.1, 250)
        grain_y = base_y + gaussian_dune(grain_x, bumps) - grain_y_offset
        ax.scatter(grain_x, grain_y, s=0.3, color=color * 0.7, alpha=0.3, zorder=i + 0.6)

    out_path = out_dir / "013_desert_dunes.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
