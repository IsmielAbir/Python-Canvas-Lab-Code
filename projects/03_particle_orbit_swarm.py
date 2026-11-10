"""
Project 04 — Particle Orbit Swarm
Difficulty: medium | Time: ~10 seconds
Libraries: numpy, matplotlib

A handful of fixed "gravity wells" pull a swarm of particles around them.
Each particle's full path is drawn as a thin trail, building up a woven
orbital portrait.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path

# ---- Change these parameters to create your own variation ----
SEED = 9
N_WELLS = 3
N_PARTICLES = 220
STEPS = 500
DT = 0.02
G = 0.9
COLORMAP = "plasma"
BACKGROUND = "#05040a"
# ------------------------------------------------------------------


def simulate(wells, well_masses, starts, steps, dt, g):
    pos = starts.copy()
    vel = np.zeros_like(pos)
    trails = np.empty((steps, *pos.shape))
    for s in range(steps):
        acc = np.zeros_like(pos)
        for w, m in zip(wells, well_masses):
            diff = w - pos
            dist2 = (diff ** 2).sum(axis=1) + 0.05
            strength = g * m / dist2
            direction = diff / np.sqrt(dist2)[:, None]
            acc += direction * strength[:, None]
        vel += acc * dt
        pos += vel * dt
        trails[s] = pos
    return trails


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    wells = rng.uniform(-1.2, 1.2, (N_WELLS, 2))
    well_masses = rng.uniform(0.6, 1.4, N_WELLS)
    starts = rng.uniform(-1.5, 1.5, (N_PARTICLES, 2))

    trails = simulate(wells, well_masses, starts, STEPS, DT, G)

    fig = plt.figure(figsize=(9, 9), dpi=150, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)

    cmap = plt.get_cmap(COLORMAP)
    for p in range(N_PARTICLES):
        path = trails[:, p, :]
        segs = np.stack([path[:-1], path[1:]], axis=1)
        color = cmap(p / N_PARTICLES)
        lc = LineCollection(segs, colors=[color] * len(segs), linewidths=0.4, alpha=0.5)
        ax.add_collection(lc)

    ax.scatter(wells[:, 0], wells[:, 1], color="white", s=60, zorder=5)

    out_path = out_dir / "03_particle_orbit_swarm.png"
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
