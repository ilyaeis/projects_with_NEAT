"""Record a headless replay of one sub-project as a GIF.

The game code stays unchanged. This script runs a replay function with the
SDL "dummy" video driver, grabs the screen on every pygame.display.flip()
and stops after enough frames.

Example (from the repo root):
    python tools/record_gif.py flappy_bird BestNeatBirdGame:replay docs/flappy_bird.gif
"""
import argparse
import importlib
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
from PIL import Image  # noqa: E402


class EnoughFrames(Exception):
    pass


class FastClock:
    """Replaces pygame.time.Clock so the replay does not wait in real time."""
    def tick(self, *_):
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="folder of the sub-project")
    parser.add_argument("call", help="module:function that starts the replay")
    parser.add_argument("out", help="output .gif path")
    parser.add_argument("--frames", type=int, default=300, help="frames to keep")
    parser.add_argument("--every", type=int, default=2, help="keep every Nth flip")
    parser.add_argument("--skip", type=int, default=0, help="flips to skip at the start")
    parser.add_argument("--scale", type=float, default=0.5)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    out = os.path.abspath(args.out)
    os.chdir(args.project)
    sys.path.insert(0, os.getcwd())

    frames: list[Image.Image] = []
    flips = 0
    real_flip = pygame.display.flip

    def flip():
        nonlocal flips
        real_flip()
        flips += 1
        if flips <= args.skip or (flips - args.skip) % args.every:
            return
        surface = pygame.display.get_surface()
        image = Image.frombytes("RGB", surface.get_size(), pygame.image.tobytes(surface, "RGB"))
        if args.scale != 1:
            size = (int(image.width * args.scale), int(image.height * args.scale))
            image = image.resize(size, Image.LANCZOS)
        frames.append(image.quantize(colors=64))
        if len(frames) >= args.frames:
            raise EnoughFrames

    pygame.display.flip = flip
    pygame.time.Clock = FastClock

    module_name, function_name = args.call.split(":")
    try:
        getattr(importlib.import_module(module_name), function_name)()
    except EnoughFrames:
        pass

    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=1000 // args.fps, loop=0, optimize=True)
    print(f"{out}: {len(frames)} frames, {os.path.getsize(out) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
