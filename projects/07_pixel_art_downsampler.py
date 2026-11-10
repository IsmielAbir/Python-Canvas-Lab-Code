"""
Project 11 — Pixel Art Downsampler
Difficulty: easy | Time: a few seconds
Libraries: numpy, Pillow

Shrinks a photo down to a tiny grid, limits it to a small color palette,
then blows it back up with hard edges — the classic retro / 8-bit game
sprite look, popular for stylized avatars and game assets.

Run this on your OWN photo: just change IMAGE_PATH below.
"""
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assets.sample_photo import ensure_sample_photo

# ---- Change these parameters to create your own variation ----
IMAGE_PATH = Path(__file__).resolve().parent.parent / "assets" / "sample_photo.png"
PIXEL_WIDTH = 72          # how many "pixels" wide the final art is
N_COLORS = 16             # limited retro-style palette
UPSCALE = 10              # final image = PIXEL_WIDTH * UPSCALE pixels wide
# ------------------------------------------------------------------


def main():
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)

    ensure_sample_photo(IMAGE_PATH)
    img = Image.open(IMAGE_PATH).convert("RGB")
    pixel_height = max(1, round(PIXEL_WIDTH * img.height / img.width))

    small = img.resize((PIXEL_WIDTH, pixel_height), Image.BOX)
    quantized = small.quantize(colors=N_COLORS).convert("RGB")
    final = quantized.resize((PIXEL_WIDTH * UPSCALE, pixel_height * UPSCALE), Image.NEAREST)

    out_path = out_dir / "07_pixel_art_downsampler.png"
    final.save(out_path)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
