"""Copy the pre-rendered front page to the output directory.

Self-contained: standard library only, no local imports, so it runs
under `python3 -P -s` in the grader sandbox.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    print(f"{dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
