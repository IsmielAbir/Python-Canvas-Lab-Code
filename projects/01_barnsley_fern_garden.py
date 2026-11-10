"""
Project 01 — Barnsley Fern Garden
Difficulty: easy | Time: a few seconds
Libraries: numpy, matplotlib

Four simple affine transformations, each picked with a different
probability, build a photorealistic fern leaf out of pure chance.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---- Change these parameters to create your own variation ----
SEED = 42
N_POINTS = 150_000
LEAF_COLOR = "#39ff6a"
BACKGROUND = "#050806"
# ------------------------------------------------------------------

TRANSFORMS = [
    # (a, b, c, d, e, f, probability)
    (0.00, 0.00, 0.00, 0.16, 0.00, 0.00, 0.01),
    (0.85, 0.04, -0.04, 0.85, 0.00, 1.60, 0.85),
    (0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07),
    (-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07),
]


def barnsley_fern(n_points, seed):
    rng = np.random.default_rng(seed)
    probs = [t[6] for t in TRANSFORMS]
    choices = rng.choice(len(TRANSFORMS), size=n_points, p=probs)

    x, y = 0.0, 0.0
    pts = np.empty((n_points, 2))
    for i, idx in enumerate(choices):
        a, b, c, d, e, f, _ = TRANSFORMS[idx]
        x, y = a * x + b * y + e, c * x + d * y + f
        pts[i] = (x, y)
    return pts


def main():
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    pts = barnsley_fern(N_POINTS, SEED)

    fig = plt.figure(figsize=(7, 10), dpi=150, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.scatter(pts[:, 0], pts[:, 1], s=0.15, color=LEAF_COLOR, alpha=0.55, linewidths=0)

    out_path = out_dir / "01_barnsley_fern_garden.png"
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
