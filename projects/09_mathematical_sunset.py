"""
Project 22 — Mathematical Sunset
Part 1: Nature Scenes
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

A complete sunset: a gradient sky built from linear interpolation, a
glowing sun drawn as concentric circles, and a rolling sea built from
stacked sine waves — including the sun's sine-wavy reflection on the
water.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.scene_helpers import add_sky, add_sun_or_moon, wave_sum

# ---- Change these parameters to create your own variation ----
SEED = 4
SKY_TOP = (40, 24, 74)
SKY_HORIZON = (255, 140, 110)
SEA_TOP = (255, 170, 120)
SEA_DEEP = (20, 18, 48)
SUN_COLOR = (255, 232, 170)
N_WAVE_LINES = 40
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

    add_sky(ax, (-1, 1), (0, 1), np.array(SKY_TOP) / 255, np.array(SKY_HORIZON) / 255)
    add_sky(ax, (-1, 1), (-1, 0), np.array(SEA_TOP) / 255, np.array(SEA_DEEP) / 255)

    sun_center = (0.0, 0.08)
    add_sun_or_moon(ax, sun_center, 0.16, np.array(SUN_COLOR) / 255, glow=True, glow_layers=6, zorder=2)

    # sun reflection: a vertical sine-wavy band of warm color on the water
    depths = np.linspace(-0.02, -0.95, 60)
    for d in depths:
        width = 0.22 * (1 - (-d) * 0.55)
        wobble = 0.03 * np.sin(d * 40 + rng.uniform(0, 1))
        cx = sun_center[0] + wobble
        alpha = max(0, 0.5 * (1 + d * 0.9))
        ax.plot([cx - width / 2, cx + width / 2], [d, d], color=np.array(SUN_COLOR) / 255,
                linewidth=2.0, alpha=alpha, solid_capstyle="round", zorder=1)

    # rolling sea surface: several stacked sine-wave horizon lines
    x = np.linspace(-1, 1, 400)
    components_base = [(0.012, 6, 0.0), (0.006, 11, 1.3), (0.003, 19, 2.7)]
    for i, base_y in enumerate(np.linspace(-0.02, -0.8, N_WAVE_LINES)):
        phase_shift = i * 0.35
        comps = [(a, f, p + phase_shift) for a, f, p in components_base]
        y = base_y + wave_sum(x, comps) * (1 - i / N_WAVE_LINES * 0.6)
        shade = 1 - i / N_WAVE_LINES
        color = np.array(SEA_TOP) / 255 * shade + np.array(SEA_DEEP) / 255 * (1 - shade)
        ax.plot(x, y, color=color, linewidth=0.8, alpha=0.7, zorder=1)

    out_path = out_dir / "09_mathematical_sunset.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
