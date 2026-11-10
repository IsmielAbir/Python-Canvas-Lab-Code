"""
Project 41 — Planetary Orbits
Part 4: Space & Dream Scenes
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

A sun, several planets, and their elliptical orbital paths — drawn with
real ellipse geometry (each orbit tilted slightly for a sense of
perspective), each planet placed at its own angle along its path.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import scatter_stars, add_sun_or_moon

# ---- Change these parameters to create your own variation ----
SEED = 2
N_PLANETS = 6
PLANET_COLORS = ["#b5b5b5", "#e0c27a", "#6fb3e0", "#d9604a", "#d8b27a", "#9ec7d9"]
# ------------------------------------------------------------------


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 9), dpi=150, facecolor="black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    scatter_stars(ax, 300, rng, (-1, 1), (-1, 1), zorder=0)
    add_sun_or_moon(ax, (0, 0), 0.09, (1.0, 0.85, 0.3), glow=True, glow_layers=7, zorder=5)

    radii = np.linspace(0.18, 0.92, N_PLANETS)
    for i, r in enumerate(radii):
        tilt = 18 - i * 1.5
        ax.add_patch(Ellipse((0, 0), r * 2, r * 2 * 0.42, angle=tilt, fill=False,
                              edgecolor=(0.5, 0.5, 0.55), linewidth=0.7, alpha=0.6, zorder=1))

        theta = rng.uniform(0, 2 * np.pi)
        a, b = r, r * 0.42
        ex = a * np.cos(theta)
        ey = b * np.sin(theta)
        rad = np.radians(tilt)
        px = ex * np.cos(rad) - ey * np.sin(rad)
        py = ex * np.sin(rad) + ey * np.cos(rad)

        planet_r = rng.uniform(0.02, 0.045)
        ax.add_patch(plt.Circle((px, py), planet_r, facecolor=PLANET_COLORS[i % len(PLANET_COLORS)], zorder=4))
        if rng.random() < 0.3:
            ax.add_patch(Ellipse((px, py), planet_r * 3.2, planet_r * 0.6, angle=tilt + 90,
                                  fill=False, edgecolor=PLANET_COLORS[i % len(PLANET_COLORS)],
                                  linewidth=1.2, alpha=0.8, zorder=4.1))

    out_path = out_dir / "18_planetary_orbits.png"
    fig.savefig(out_path, facecolor="black")
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
