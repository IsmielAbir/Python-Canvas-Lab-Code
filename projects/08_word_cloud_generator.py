"""
Project 18 — Word Cloud Generator
Difficulty: medium | Time: ~5-10 seconds
Libraries: numpy, matplotlib (no external "wordcloud" package needed)

A hand-rolled version of the classic word-cloud tool: count word
frequency, size each word by how often it appears, then place words
outward along a spiral from the center until they stop overlapping.
Replace SOURCE_TEXT with your own speech, resume, or article text.
"""
import re
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ---- Replace this with YOUR text ----
SOURCE_TEXT = """
Python is a readable, expressive language that turns an idea into a working
program fast. Creative coding takes that same language and points it at
pictures instead of spreadsheets: generative art, procedural patterns,
animation, data visualization, interactive design. A single script can
become a fractal, a flowing particle swarm, a seamless pattern, or a
poster-ready chart. The best part of creative coding is iteration: change
one parameter, rerun the script, and watch a completely different piece of
art appear. Python makes that loop short enough to stay playful. Generative
art rewards curiosity far more than it rewards perfect planning, and small
experiments compound into a real visual style over time.
"""
N_WORDS = 45
CANVAS_W, CANVAS_H = 1000, 700
MIN_SIZE, MAX_SIZE = 14, 92
COLORMAP = "viridis"
BACKGROUND = "#101014"
STOPWORDS = {
    "the", "and", "a", "an", "of", "to", "in", "is", "it", "that", "this",
    "for", "on", "with", "as", "are", "be", "or", "its", "into", "than",
    "more", "far", "one", "can", "each", "same", "over", "time", "into",
}
# ------------------------------------------------------------------


def word_frequencies(text, n_words):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    words = [w for w in words if len(w) > 2 and w not in STOPWORDS]
    counts = Counter(words)
    return counts.most_common(n_words)


def find_spot(occupancy, w, h, cx, cy, canvas_w, canvas_h, rng):
    angle = rng.uniform(0, 2 * np.pi)
    radius = 0.0
    max_radius = 1.4 * max(canvas_w, canvas_h)
    while radius < max_radius:
        x = cx + radius * np.cos(angle) - w / 2
        y = cy + radius * np.sin(angle) - h / 2
        xi, yi = int(x), int(y)
        if 0 <= xi and xi + w < canvas_w and 0 <= yi and yi + h < canvas_h:
            if not occupancy[yi:yi + h, xi:xi + w].any():
                return xi, yi
        angle += 0.45
        radius += 3.0
    return None


def main():
    rng = np.random.default_rng(2)
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    ranked = word_frequencies(SOURCE_TEXT, N_WORDS)
    if not ranked:
        raise ValueError("No words survived filtering — check SOURCE_TEXT/STOPWORDS.")

    freqs = np.array([c for _, c in ranked], dtype=float)
    fmin, fmax = freqs.min(), freqs.max()
    sizes = MIN_SIZE + (MAX_SIZE - MIN_SIZE) * (freqs - fmin) / (fmax - fmin + 1e-9)

    occupancy = np.zeros((CANVAS_H, CANVAS_W), dtype=bool)
    cx, cy = CANVAS_W / 2, CANVAS_H / 2
    cmap = plt.get_cmap(COLORMAP)

    placements = []
    for i, ((word, freq), fontsize) in enumerate(zip(ranked, sizes)):
        rotate = rng.random() < 0.15
        px_per_pt = 100 / 72  # dpi=100
        font_px = fontsize * px_per_pt
        w = int(len(word) * font_px * 0.62) + 6
        h = int(font_px * 1.15) + 6
        if rotate:
            w, h = h, w
        spot = find_spot(occupancy, w, h, cx, cy, CANVAS_W, CANVAS_H, rng)
        if spot is None:
            continue
        xi, yi = spot
        occupancy[yi:yi + h, xi:xi + w] = True
        placements.append((word, fontsize, xi + w / 2, yi + h / 2, rotate, i))

    fig = plt.figure(figsize=(CANVAS_W / 100, CANVAS_H / 100), dpi=100, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, CANVAS_W)
    ax.set_ylim(0, CANVAS_H)
    ax.invert_yaxis()
    ax.axis("off")

    for word, fontsize, x, y, rotate, rank in placements:
        color = cmap(rank / max(1, len(placements) - 1))
        ax.text(x, y, word, fontsize=fontsize, color=color, ha="center", va="center",
                rotation=90 if rotate else 0, fontweight="bold", family="sans-serif")

    out_path = out_dir / "08_word_cloud_generator.png"
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)
    print(f"Saved {out_path}  ({len(placements)}/{len(ranked)} words placed)")


if __name__ == "__main__":
    main()
