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
            try:
                subprocess.run(
                    f'amarna {filename} -o {filename.replace(".cairo", ".sarif")}',
                    shell=True,
                    universal_newlines=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                console.print(
                    f"[red][bold]{filename}]: failed linting check[/bold][/red]"
                )
                console.print_exception()
                retval = 1

    return retval


if __name__ == "__main__":
    raise SystemExit(main())
