#!/usr/bin/env python3
"""Copy the bundled entry.png image to the make.fun output directory.

The image (a child's cardboard chair with a handwritten note) lives
beside this script as ``entry.png``. The program streams it to a
temporary file in the output directory, flushes and fsyncs it, then
atomically renames it onto ``entry.png`` there, so the grader always
sees a complete file. It prints nothing on success.
"""

import os
import shutil
import sys
from pathlib import Path

ASSET_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> int:
    asset = Path(__file__).resolve().parent / ASSET_NAME
    if not asset.is_file():
        print(f"error: bundled asset not found: {asset}", file=sys.stderr)
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    output_dir.mkdir(parents=True, exist_ok=True)

    tmp_path = output_dir / (ASSET_NAME + ".tmp")
    target_path = output_dir / ASSET_NAME

    with asset.open("rb") as src, tmp_path.open("wb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024)
        dst.flush()
        os.fsync(dst.fileno())

    if tmp_path.stat().st_size != asset.stat().st_size:
        print(
            f"error: copied size {tmp_path.stat().st_size} does not match "
            f"asset size {asset.stat().st_size}",
            file=sys.stderr,
        )
        return 1

    os.replace(tmp_path, target_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
