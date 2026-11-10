"""
Project 05 — Starfield Galaxy Spiral
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

Stars scattered along logarithmic spiral arms, plus a scattered background
field, rendered as glowing points on black to suggest a spiral galaxy.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---- Change these parameters to create your own variation ----
SEED = 88
N_ARMS = 3
STARS_PER_ARM = 2500
BACKGROUND_STARS = 1500
SPIRAL_TIGHTNESS = 1.3
COLORMAP = "Blues_r"
# ------------------------------------------------------------------


def spiral_arm(n_stars, arm_offset, tightness, rng):
    t = rng.uniform(0, 2.2 * np.pi, n_stars)
    r = t * 0.22
    jitter_r = rng.normal(0, 0.015 + 0.01 * t, n_stars)
    jitter_a = rng.normal(0, 0.06, n_stars)
    angle = t / tightness + arm_offset + jitter_a
    radius = r + jitter_r
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y, r


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    fig = plt.figure(figsize=(9, 9), dpi=150, facecolor="black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_facecolor("black")

    cmap = plt.get_cmap(COLORMAP)
    for arm in range(N_ARMS):
        offset = arm * (2 * np.pi / N_ARMS)
        x, y, r = spiral_arm(STARS_PER_ARM, offset, SPIRAL_TIGHTNESS, rng)
        colors = cmap(1 - r / r.max())
        sizes = rng.uniform(0.3, 3.0, STARS_PER_ARM)
        ax.scatter(x, y, s=sizes, c=colors, linewidths=0, alpha=0.85)

    bx = rng.uniform(-2.2, 2.2, BACKGROUND_STARS)
    by = rng.uniform(-2.2, 2.2, BACKGROUND_STARS)
    ax.scatter(bx, by, s=rng.uniform(0.1, 0.8, BACKGROUND_STARS),
               color="white", alpha=0.4, linewidths=0)

    # bright galactic core
    ax.scatter([0], [0], s=1200, color="white", alpha=0.25, linewidths=0)
    ax.scatter([0], [0], s=300, color="white", alpha=0.6, linewidths=0)

    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)

    out_path = out_dir / "04_starfield_galaxy_spiral.png"
    fig.savefig(out_path, facecolor="black")
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
