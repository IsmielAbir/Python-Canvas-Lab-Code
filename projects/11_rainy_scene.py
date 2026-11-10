"""
Project 25 — Rainy Scene
Part 1: Nature Scenes
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

Clouds built from overlapping soft ellipses, rain drawn as fast
falling-particle streaks, and splash ripples at the bottom modeled as
small parabolic arcs plus expanding circles on the puddle.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky

# ---- Change these parameters to create your own variation ----
SEED = 19
N_RAINDROPS = 220
WIND = -0.08
SKY_TOP = (90, 98, 110)
SKY_HORIZON = (160, 165, 170)
PUDDLE_COLOR = (70, 80, 92)
# ------------------------------------------------------------------


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 9), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (-0.35, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)

    # clouds: clusters of overlapping soft gray ellipses
    for _ in range(6):
        cx, cy = rng.uniform(-0.9, 0.9), rng.uniform(0.35, 0.85)
        for _ in range(6):
            dx, dy = rng.uniform(-0.18, 0.18), rng.uniform(-0.05, 0.05)
            w, h = rng.uniform(0.18, 0.34), rng.uniform(0.08, 0.14)
            ax.add_patch(Ellipse((cx + dx, cy + dy), w, h, color=(0.4, 0.42, 0.46), alpha=0.5, zorder=1))

    # puddle at the bottom
    ax.axhspan(-1, -0.35, color=np.array(PUDDLE_COLOR) / 255, zorder=1)

    # falling rain: straight streaks with a wind-driven slant
    starts_x = rng.uniform(-1, 1, N_RAINDROPS)
    starts_y = rng.uniform(-0.3, 1, N_RAINDROPS)
    lengths = rng.uniform(0.05, 0.12, N_RAINDROPS)
    for x0, y0, length in zip(starts_x, starts_y, lengths):
        x1 = x0 + WIND * length
        y1 = y0 - length
        ax.plot([x0, x1], [y0, y1], color=(0.75, 0.82, 0.9), linewidth=0.7, alpha=0.5, zorder=2)

    # splash arcs + ripples where raindrops are hitting the puddle — a
    # small parabolic arc that starts and ends right at the puddle line
    n_splashes = 24
    splash_x = rng.uniform(-1, 1, n_splashes)
    for sx in splash_x:
        sy0 = -0.35
        t = np.linspace(0, 1, 15)
        for side in (-1, 1):
            spread = side * rng.uniform(0.015, 0.035)
            peak = rng.uniform(0.02, 0.05)
            x = sx + spread * t
            y = sy0 + peak * (1 - (2 * t - 1) ** 2)
            ax.plot(x, y, color=(0.85, 0.9, 0.95), linewidth=0.8, alpha=0.6, zorder=3)
        ripple_r = rng.uniform(0.01, 0.04)
        ax.add_patch(Circle((sx, sy0), ripple_r, fill=False, edgecolor=(0.85, 0.9, 0.95),
                             linewidth=0.6, alpha=0.4, zorder=3))

    out_path = out_dir / "11_rainy_scene.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
