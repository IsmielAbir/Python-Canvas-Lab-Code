"""
Project 06 — Recursive Polygon Spiral
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

A single polygon is drawn, then redrawn scaled down and rotated, over and
over. The simple recursive transform builds a hypnotic spiraling tunnel.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path

# ---- Change these parameters to create your own variation ----
N_SIDES = 6
N_ITERATIONS = 70
SCALE_FACTOR = 0.94
ROTATION_STEP = 9.0     # degrees
COLORMAP = "viridis"
BACKGROUND = "#060608"
# ------------------------------------------------------------------


def polygon_vertices(n_sides, radius, rotation):
    angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False) + np.radians(rotation)
    return np.column_stack([radius * np.cos(angles), radius * np.sin(angles)])


def main():
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 9), dpi=150, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)

    cmap = plt.get_cmap(COLORMAP)
    radius = 1.0
    rotation = 0.0
    for i in range(N_ITERATIONS):
        verts = polygon_vertices(N_SIDES, radius, rotation)
        color = cmap(i / N_ITERATIONS)
        ax.add_patch(Polygon(verts, closed=True, fill=False,
                              edgecolor=color, linewidth=1.1, alpha=0.9))
        radius *= SCALE_FACTOR
        rotation += ROTATION_STEP

    out_path = out_dir / "05_recursive_polygon_spiral.png"
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
