"""
Project 02 — L-System Tree Forest
Difficulty: medium | Time: a few seconds
Libraries: numpy, matplotlib

A Lindenmayer system rewrites a short string into a long one, then a
"turtle" reads the string as draw/turn/branch commands. A handful of trees
with randomized angles become a small forest.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path

# ---- Change these parameters to create your own variation ----
SEED = 11
AXIOM = "F"
RULES = {"F": "FF+[+F-F-F]-[-F+F+F]"}
ITERATIONS = 4
BASE_ANGLE = 22.5       # degrees
N_TREES = 5
COLORMAP = "YlGn"
# ------------------------------------------------------------------


def expand(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(ch, ch) for ch in s)
    return s


def turtle_segments(instructions, angle_deg, angle_jitter, step, rng):
    pos = np.array([0.0, 0.0])
    heading = 90.0
    stack = []
    segments = []
    for ch in instructions:
        if ch == "F":
            jitter = rng.uniform(-angle_jitter, angle_jitter)
            rad = np.radians(heading + jitter)
            new_pos = pos + step * np.array([np.cos(rad), np.sin(rad)])
            segments.append((pos.copy(), new_pos.copy()))
            pos = new_pos
        elif ch == "+":
            heading += angle_deg
        elif ch == "-":
            heading -= angle_deg
        elif ch == "[":
            stack.append((pos.copy(), heading))
        elif ch == "]":
            pos, heading = stack.pop()
    return segments


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    instructions = expand(AXIOM, RULES, ITERATIONS)
    cmap = plt.get_cmap(COLORMAP)

    # Build every tree's segments first so we know the true bounding box
    # before sizing the figure — otherwise a wide-but-short canopy gets
    # padded into a square frame and drowns in empty margin.
    spacing = 1.9
    offsets = np.linspace(-(N_TREES - 1) * spacing / 2, (N_TREES - 1) * spacing / 2, N_TREES)
    trees = []
    all_points = []
    for ox in offsets:
        segs = turtle_segments(instructions, BASE_ANGLE, 4.0, 0.035, rng)
        segs = [(p1 + [ox, 0], p2 + [ox, 0]) for p1, p2 in segs]
        trees.append(segs)
        all_points.extend(p for seg in segs for p in seg)

    all_points = np.array(all_points)
    margin = 0.1
    x_min, y_min = all_points.min(axis=0)
    x_max, y_max = all_points.max(axis=0)
    x_span, y_span = x_max - x_min, y_max - y_min
    x_min, x_max = x_min - margin * x_span, x_max + margin * x_span
    y_min, y_max = y_min - margin * y_span, y_max + margin * y_span

    long_side = 10.0
    aspect = (y_max - y_min) / (x_max - x_min)
    figsize = (long_side, max(2.5, long_side * aspect)) if aspect <= 1 else (max(2.5, long_side / aspect), long_side)

    fig = plt.figure(figsize=figsize, dpi=150, facecolor="#eaf3ea")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    for segs in trees:
        depth = np.array([abs(p1[1]) for p1, _ in segs])
        norm_depth = depth / (depth.max() + 1e-9)
        colors = cmap(0.3 + 0.7 * norm_depth)
        lc = LineCollection(segs, colors=colors, linewidths=0.9)
        ax.add_collection(lc)

    out_path = out_dir / "02_lsystem_tree_forest.png"
    fig.savefig(out_path, facecolor="#eaf3ea")
    plt.close(fig)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
