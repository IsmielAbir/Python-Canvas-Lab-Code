"""
Project 23 — Fractal Mountains
Part 1: Nature Scenes
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

Layered mountain ridges built with the classic midpoint-displacement
fractal algorithm (the same technique behind old-school "plasma terrain"
generators), with a soft mist band fading between each layer.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, mountain_layer

# ---- Change these parameters to create your own variation ----
SEED = 12
SKY_TOP = (173, 196, 219)
SKY_HORIZON = (235, 220, 200)
N_LAYERS = 5
ROUGHNESS = 0.58
MIST_COLOR = (255, 255, 255)
# ------------------------------------------------------------------


def main():
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (-1, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)

    base_grays = np.linspace(0.55, 0.12, N_LAYERS)
    base_ys = np.linspace(0.35, -0.5, N_LAYERS)
    mist_color = np.array(MIST_COLOR) / 255
    for i in range(N_LAYERS):
        tint = base_grays[i]
        color = (tint * 0.85, tint * 0.9, tint * 1.05)
        color = tuple(min(1.0, max(0.0, c)) for c in color)
        x, y = mountain_layer(ax, (-1, 1), base_ys[i], 0.55 - i * 0.03, SEED + i * 7,
                               color, roughness=ROUGHNESS, zorder=i)

        # soft mist pooling in the valleys at the foot of each ridge — capped
        # at the ridge line itself so it never bleeds up over distant peaks
        mist_height = 0.08
        mist_ceiling = np.minimum(y, base_ys[i] + mist_height)
        for k in range(5):
            level = base_ys[i] + mist_height * (k + 1) / 5
            ax.fill_between(x, base_ys[i], np.minimum(mist_ceiling, level),
                             color=mist_color, alpha=0.06, zorder=i + 0.5, linewidth=0)

    # foreground ground
    ax.axhspan(-1, -0.55, color=(0.08, 0.1, 0.07), zorder=N_LAYERS + 1)

    out_path = out_dir / "10_fractal_mountains.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
