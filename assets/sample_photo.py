"""
Shared demo asset — a synthetic "sample photo" (sunset over layered
mountains) used by every photo-filter project in this book.

Every filter script imports `ensure_sample_photo()` and runs it on this
image by default. To try a filter on your OWN photo, just change the
IMAGE_PATH constant near the top of that script to point at any JPG/PNG.
"""
import numpy as np
from PIL import Image, ImageDraw


def _sky_gradient(width, height, top_color, bottom_color):
    t = np.linspace(0, 1, height)[:, None]
    top = np.array(top_color, dtype=float)
    bottom = np.array(bottom_color, dtype=float)
    gradient = top + (bottom - top) * t
    return np.repeat(gradient[:, None, :], width, axis=1)


def _mountain_silhouette(draw, width, base_y, peak_height, seed, color):
    rng = np.random.default_rng(seed)
    n_points = 10
    xs = np.linspace(-20, width + 20, n_points)
    ys = base_y - rng.uniform(0.2, 1.0, n_points) * peak_height
    points = list(zip(xs, ys)) + [(width + 20, base_y + 50), (-20, base_y + 50)]
    draw.polygon(points, fill=color)


def _cloud_texture(width, height, seed):
    """Soft streaky cloud bands — gives gradient-based filters something
    to pick up on besides flat color (otherwise pencil-sketch/edge filters
    have almost nothing to work with)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:height, 0:width]
    texture = np.zeros((height, width))
    for _ in range(5):
        fx = rng.uniform(1.5, 5.0)
        fy = rng.uniform(0.3, 1.2)
        phase = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.3, 1.0)
        texture += amp * np.sin(2 * np.pi * (fx * xx / width + fy * yy / height) + phase)
    texture = (texture - texture.min()) / (texture.max() - texture.min())
    return texture


def generate_sample_photo(width=900, height=650, seed=7):
    sky = _sky_gradient(width, height, (255, 191, 120), (255, 94, 98)).astype(np.uint8)
    img = Image.fromarray(sky, mode="RGB")
    draw = ImageDraw.Draw(img)

    # sun
    sun_r = 70
    draw.ellipse((width * 0.5 - sun_r, height * 0.32 - sun_r,
                  width * 0.5 + sun_r, height * 0.32 + sun_r), fill=(255, 244, 214))

    # three layered mountain ranges, back to front
    _mountain_silhouette(draw, width, height * 0.72, height * 0.30, 1, (120, 90, 110))
    _mountain_silhouette(draw, width, height * 0.80, height * 0.26, 2, (80, 60, 90))
    _mountain_silhouette(draw, width, height * 0.90, height * 0.22, 3, (40, 32, 58))

    # subtle cloud streaks (mostly visible in the sky) + photographic grain —
    # without this the image is near-flat color, which starves edge/texture
    # based filters (pencil sketch, ASCII art) of anything to render.
    rng = np.random.default_rng(seed)
    arr = np.array(img).astype(float)
    clouds = _cloud_texture(width, height, seed) - 0.5
    sky_mask = np.linspace(1, 0, height)[:, None] ** 0.5
    arr += (clouds * 18)[:, :, None] * sky_mask[:, :, None]
    arr += rng.normal(0, 7, (height, width, 1))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    return img


def ensure_sample_photo(path):
    """Create assets/sample_photo.png if it doesn't already exist."""
    path = str(path)
    import os
    if not os.path.exists(path):
        generate_sample_photo().save(path)
    return path


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parent / "sample_photo.png"
    generate_sample_photo().save(out)
    print(f"Saved {out}")
