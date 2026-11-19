#!/usr/bin/env python3
"""Deterministic entry builder for make.fun news-image-20261119 (v1).

Copies the pre-rendered front page (entry.png, built by build_image.py
from 30 verified stories) to the harness output directory as entry.png.

Reads MAKEFUN_OUTPUT_DIR when set, otherwise writes to /output.
Standard library only; no network access.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a valid PNG file", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Byte-identical copy check: the output must match the source exactly,
    # so repeated runs are deterministic.
    if open(src, "rb").read() != open(dst, "rb").read():
        print("error: output bytes differ from entry.png", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
