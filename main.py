#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261119.

Copies the entry image (entry.png, held in this repository next to
main.py) into the output directory as entry.png. The output directory
is $MAKEFUN_OUTPUT_DIR when set, otherwise /output. Standard library
only, no network, deterministic: the bytes written are exactly the
bytes of the repository's entry.png.

The image itself is drawn by draw.py (PIL): a newspaper front page
dated Thursday, 19 November 2026, with six story panels and a footer
ticker. Regenerating it with draw.py reproduces entry.png byte for
byte on the same machine/fonts.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
