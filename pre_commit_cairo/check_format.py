from __future__ import annotations

import argparse
import subprocess
from typing import Sequence

from rich.console import Console


console = Console()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if filename.endswith(".cairo"):
            console.print(f"Formatting contract: {filename}")
            try:
                subprocess.run(
                    f"cairo-format -i {filename}",
                    shell=True,
                    universal_newlines=True,
                    check=True,
                )
            except Exception:
                console.print(f"[red]Failed formatting in file {filename}[/red]")
                retval = 1
                break

    return retval


if __name__ == "__main__":
    raise SystemExit(main())
