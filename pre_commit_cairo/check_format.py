from __future__ import annotations
from fileinput import filename

import os
import argparse
import subprocess
from typing import Sequence

from rich.console import Console


console = Console()


def _read_file(filename):
    with open(filename, "r") as f:
        file = f.readlines()
    return file


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if filename.endswith(".cairo"):
            prev_file = _read_file(filename)
            try:
                subprocess.run(
                    f"cairo-format -i {filename}",
                    shell=True,
                    universal_newlines=True,
                    check=True,
                )
            except Exception:
                console.print(f"[red]error: cannot format {filename}[/red]")
                retval = 1
            else:
                if prev_file != _read_file(filename):
                    console.print(f"reformatted contract: {filename}")
                    retval = 1

    return retval


if __name__ == "__main__":
    raise SystemExit(main())
