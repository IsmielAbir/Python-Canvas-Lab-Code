"""
Shared drawing primitives for the "Illustrated Scenes" chapters
(projects 22-51). Every scene script imports what it needs from here
instead of re-deriving the same sky gradient / fractal ridge / star field
math thirty times.
"""
import numpy as np
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import LineCollection


# ---------------------------------------------------------------- sky / atmosphere

def add_sky(ax, xlim, ylim, top_color, bottom_color, n=200, zorder=-100):
    """Vertical gradient drawn as a fine stack of filled bands across a
    sub-region (ylim) of the axes. Does NOT touch the axes' own view
    limits — set ax.set_xlim/set_ylim yourself once, before or after
    calling this (possibly more than once for sky+sea)."""
    y = np.linspace(ylim[0], ylim[1], n + 1)
    top = np.array(top_color, dtype=float)
    bottom = np.array(bottom_color, dtype=float)
    for i in range(n):
        t = i / (n - 1)
        color = top + (bottom - top) * t
        ax.fill_between(xlim, y[i], y[i + 1], color=color, zorder=zorder, linewidth=0)


def add_sun_or_moon(ax, center, radius, color, glow=True, glow_layers=4, glow_color=None, zorder=5):
    glow_color = glow_color or color
    if glow:
        for i in range(glow_layers, 0, -1):
            r = radius * (1 + i * 0.35)
            ax.add_patch(Circle(center, r, color=glow_color, alpha=0.06, zorder=zorder - 1, linewidth=0))
    ax.add_patch(Circle(center, radius, color=color, zorder=zorder, linewidth=0))


def scatter_stars(ax, n, rng, xlim, ylim, color="white", size_range=(0.5, 3.0), alpha_range=(0.4, 1.0), zorder=1):
    xs = rng.uniform(*xlim, n)
    ys = rng.uniform(*ylim, n)
    sizes = rng.uniform(*size_range, n)
    alphas = rng.uniform(*alpha_range, n)
    ax.scatter(xs, ys, s=sizes, color=color, alpha=alphas, linewidths=0, zorder=zorder)
    return xs, ys


# ---------------------------------------------------------------- fractal terrain

def midpoint_displacement(length_pow2, roughness, rng, start=0.0, end=0.0):
    """Classic 1D fractal ridge line (plasma / fractal-mountain algorithm)."""
    n = 2 ** length_pow2
    y = np.zeros(n + 1)
    y[0], y[-1] = start, end
    step = n
    scale = 1.0
    while step > 1:
        half = step // 2
        for i in range(half, n, step):
            avg = (y[i - half] + y[i + half]) / 2
            y[i] = avg + rng.uniform(-1, 1) * scale
        scale *= roughness
        step = half
    return y


def mountain_layer(ax, xlim, base_y, height_scale, seed, color, roughness=0.55, zorder=0):
    rng = np.random.default_rng(seed)
    ridge = midpoint_displacement(8, roughness, rng)
    ridge = (ridge - ridge.min()) / (ridge.max() - ridge.min() + 1e-9)
    x = np.linspace(xlim[0], xlim[1], len(ridge))
    y = base_y + ridge * height_scale
    pts = list(zip(x, y)) + [(xlim[1], base_y - height_scale * 0.1), (xlim[0], base_y - height_scale * 0.1)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=zorder))
    return x, y


# ---------------------------------------------------------------- value noise (fBm)

def value_noise(size, grid_res, rng):
    g = rng.uniform(-1, 1, (grid_res + 1, grid_res + 1))
    coords = np.linspace(0, grid_res, size, endpoint=False)
    idx = np.floor(coords).astype(int)
    frac = coords - idx
    smooth = frac * frac * (3 - 2 * frac)
    xi, yi = np.meshgrid(idx, idx)
    u, v = np.meshgrid(smooth, smooth)
    tl, tr = g[yi, xi], g[yi, xi + 1]
    bl, br = g[yi + 1, xi], g[yi + 1, xi + 1]
    top = tl + u * (tr - tl)
    bottom = bl + u * (br - bl)
    return top + v * (bottom - top)


def fbm_noise(size, octaves, persistence, rng, start_res=3):
    total = np.zeros((size, size))
    amp, max_amp, res = 1.0, 0.0, start_res
    for _ in range(octaves):
        total += value_noise(size, res, rng) * amp
        max_amp += amp
        amp *= persistence
        res *= 2
    return total / max_amp


# ---------------------------------------------------------------- waves

def wave_sum(x, components):
    """components: list of (amplitude, frequency, phase)."""
    y = np.zeros_like(x)
    for amp, freq, phase in components:
        y = y + amp * np.sin(freq * x + phase)
    return y


# ---------------------------------------------------------------- L-systems / turtle

def l_system_expand(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(ch, ch) for ch in s)
    return s


def turtle_segments(instructions, angle_deg, step, start_heading=90.0, angle_jitter=0.0, rng=None):
    pos = np.array([0.0, 0.0])
    heading = start_heading
    stack = []
    segments = []
    for ch in instructions:
        if ch == "F":
            jitter = rng.uniform(-angle_jitter, angle_jitter) if (rng is not None and angle_jitter) else 0.0
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


# ---------------------------------------------------------------- points / curves

def chaos_game(n_points, corners, ratio, rng):
    corners = np.array(corners)
    point = corners.mean(axis=0)
    pts = np.empty((n_points, 2))
    choices = rng.integers(0, len(corners), size=n_points)
    for i in range(n_points):
        point = point + (corners[choices[i]] - point) * ratio
        pts[i] = point
    return pts, choices


def golden_angle_points(n, scale=1.0):
    """Phyllotaxis / sunflower-seed placement using the golden angle."""
    golden_angle = np.pi * (3 - np.sqrt(5))
    i = np.arange(n)
    r = scale * np.sqrt(i / n)
    theta = i * golden_angle
    return r * np.cos(theta), r * np.sin(theta)


def rose_curve(k, n_points=500, scale=1.0, phase=0.0):
    theta = np.linspace(0, 2 * np.pi, n_points)
    r = scale * np.cos(k * theta + phase)
    return r * np.cos(theta), r * np.sin(theta)


def catenary(x, a, x0=0.0, y0=0.0):
    return a * np.cosh((x - x0) / a) + (y0 - a)


def nearest_seed_raster(height, width, seeds):
    yy, xx = np.mgrid[0:height, 0:width]
    best_dist = np.full((height, width), np.inf)
    second_dist = np.full((height, width), np.inf)
    nearest = np.zeros((height, width), dtype=int)
    for i, (sx, sy) in enumerate(seeds):
        d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)
        closer = d < best_dist
        second_dist = np.where(closer, best_dist, np.minimum(second_dist, d))
        best_dist = np.where(closer, d, best_dist)
        nearest = np.where(closer, i, nearest)
    return nearest, best_dist, second_dist
