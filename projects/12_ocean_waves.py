"""
Project 26 — Ocean Waves
Part 1: Nature Scenes
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

The rolling surface of the sea, built entirely from several sine waves of
different frequency and amplitude added together — plus a scatter of
white foam right at each wave's crest.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, wave_sum

# ---- Change these parameters to create your own variation ----
SEED = 15
N_BANDS = 26
SKY_TOP = (120, 180, 220)
SKY_HORIZON = (200, 230, 235)
SEA_TOP = (30, 120, 150)
SEA_DEEP = (5, 30, 55)
# ------------------------------------------------------------------


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 7), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    add_sky(ax, (-1, 1), (0.15, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    add_sky(ax, (-1, 1), (-1, 0.15), np.array(SEA_TOP) / 255, np.array(SEA_DEEP) / 255)

    x = np.linspace(-1, 1, 500)
    components = [(0.04, 4.5, 0.0), (0.02, 8.0, 1.1), (0.01, 15.0, 2.4)]

    for i, base_y in enumerate(np.linspace(0.12, -0.95, N_BANDS)):
        depth_t = i / N_BANDS
        comps = [(a * (1 - depth_t * 0.15), f, p + i * 0.5) for a, f, p in components]
        y = base_y + wave_sum(x, comps)
        # a cyclical band-to-band shade (so crests stay visible at any depth)
        # multiplied by an overall depth darkening (so it still reads as deep water)
        band_shade = 0.5 + 0.5 * np.cos(i * 0.9)
        depth_dark = 1 - 0.55 * depth_t
        color = (np.array(SEA_TOP) / 255 * band_shade + np.array(SEA_DEEP) / 255 * (1 - band_shade)) * depth_dark
        shade = band_shade * depth_dark
        ax.fill_between(x, y, base_y - 0.05, color=color, zorder=i, linewidth=0)

        if i % 3 == 0:
            crest_mask = np.gradient(y) > 0.0008
            ax.scatter(x[crest_mask][::6], y[crest_mask][::6], s=2, color="white",
                       alpha=0.5 * shade + 0.2, zorder=i + 0.5)

    out_path = out_dir / "12_ocean_waves.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
