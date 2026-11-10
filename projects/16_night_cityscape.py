"""
Project 31 — Night Cityscape
Part 2: City & Architecture
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

Dark building silhouettes with randomly lit windows (points), connected
to nothing but the night sky above — and the whole skyline mirrored and
wave-distorted below the waterline for a reflection.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, scatter_stars

# ---- Change these parameters to create your own variation ----
SEED = 41
N_BUILDINGS = 13
SKY_TOP = (6, 10, 28)
SKY_HORIZON = (20, 24, 48)
# ------------------------------------------------------------------


def building_layout(n_buildings, rng):
    layout = []
    x = -1.05
    for _ in range(n_buildings):
        width = rng.uniform(0.11, 0.22)
        height = rng.uniform(0.25, 0.85)
        layout.append((x, width, height))
        x += width + rng.uniform(0.0, 0.02)
    return layout


def draw_skyline(ax, layout, base_y, flip, rng, window_alpha=1.0, zorder=5):
    for x, width, height in layout:
        h = height if not flip else height
        y0 = base_y if not flip else base_y - height
        ax.add_patch(Rectangle((x, y0), width, h, facecolor=(0.05, 0.05, 0.08),
                                edgecolor="none", zorder=zorder))
        rows = max(1, int(height / 0.07))
        cols = max(1, int(width / 0.05))
        for r in range(rows):
            for c in range(cols):
                if rng.random() < 0.6:
                    continue
                wx = x + width / cols * (c + 0.5)
                wy = (base_y + 0.03 + r * 0.07) if not flip else (base_y - 0.03 - r * 0.07)
                ax.scatter([wx], [wy], s=5, color=(1.0, 0.85, 0.4), alpha=window_alpha, zorder=zorder + 0.1)


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 7), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (-1, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    scatter_stars(ax, 250, rng, (-1, 1), (0.0, 1), zorder=1)

    base_y = -0.1
    layout = building_layout(N_BUILDINGS, rng)

    # reflection first (drawn behind, below the waterline, faded + squashed)
    draw_skyline(ax, layout, base_y, flip=True, rng=np.random.default_rng(SEED), window_alpha=0.35, zorder=2)
    ax.fill_between([-1, 1], -1, base_y, color=(0.02, 0.03, 0.08), alpha=0.55, zorder=3)
    for ry in np.linspace(base_y - 0.02, -0.95, 14):
        ax.axhline(ry, color=(0.3, 0.35, 0.45), linewidth=0.4, alpha=0.15, zorder=3.5)

    # real skyline on top
    draw_skyline(ax, layout, base_y, flip=False, rng=np.random.default_rng(SEED), window_alpha=1.0, zorder=5)

    out_path = out_dir / "16_night_cityscape.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
