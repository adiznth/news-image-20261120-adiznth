#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261120 bounty.

It writes the one image that sums up the world's news of Friday
20 November 2026 to the output directory. The image is drawn by
draw.py (Pillow, build time only) and shipped beside this file as
entry.png; this program only copies it, so it runs with the
standard library alone, needs no network, and writes the same
bytes on every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in
for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    source = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
