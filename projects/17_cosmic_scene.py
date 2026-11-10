"""
Project 40 — Cosmic Scene
Part 4: Space & Dream Scenes
Difficulty: medium | Time: ~5-10 seconds
Libraries: numpy, matplotlib

A glowing nebula built from multi-octave fractal noise (fBm) colored with
a vivid colormap, a bright galactic core, and a scatter of stars at
varying brightness and size.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import fbm_noise, scatter_stars, add_sun_or_moon

# ---- Change these parameters to create your own variation ----
SEED = 61
GRID = 500
OCTAVES = 5
PERSISTENCE = 0.55
COLORMAP = "magma"
N_STARS = 600
# ------------------------------------------------------------------


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    nebula = fbm_noise(GRID, OCTAVES, PERSISTENCE, rng)
    nebula = (nebula - nebula.min()) / (nebula.max() - nebula.min())
    nebula = nebula ** 1.6  # push down the faint areas so it reads as wispy clouds

    fig = plt.figure(figsize=(9, 9), dpi=150, facecolor="black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    ax.imshow(nebula, cmap=COLORMAP, extent=(-1, 1, -1, 1), alpha=0.85, zorder=0, interpolation="bilinear")

    scatter_stars(ax, N_STARS, rng, (-1, 1), (-1, 1), zorder=1)
    add_sun_or_moon(ax, (0.1, -0.05), 0.05, (1.0, 0.98, 0.9), glow=True, glow_layers=8, zorder=2)

    out_path = out_dir / "017_cosmic_scene.png"
    fig.savefig(out_path, facecolor="black")
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
