from __future__ import annotations

import os
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
    reformatted_count = 0
    unchanged_count = 0
    failed_count = 0
    for filename in args.filenames:
        if filename.endswith(".cairo"):
            prev_timestamp = os.path.getmtime(filename)

            try:
                subprocess.run(
                    f"cairo-format -i {filename}",
                    shell=True,
                    universal_newlines=True,
                    check=True,
                )
            except Exception:
                failed_count += 1
                console.print(f"[red]error: cannot format {filename}[/red]")
                retval = 1
            else:
                if prev_timestamp != os.path.getmtime(filename):
                    reformatted_count += 1
                    console.print(f"reformatted contract: {filename}")
                    retval = 1
                else:
                    unchanged_count += 1

    console.print("All done! :sparkles: :cake: :sparkles:")
    final_output = []
    if reformatted_count > 0:
        if reformatted_count > 1:
            final_output.append(f"{reformatted_count} files reformatted")
        else:
            final_output.append(f"{reformatted_count} file reformatted")
    if unchanged_count > 0:
        if unchanged_count > 1:
            final_output.append(f"{reformatted_count} files left unchanged")
        else:
            final_output.append(f"{reformatted_count} file left unchanged")
    if failed_count > 0:
        if failed_count > 1:
            final_output.append(f"{failed_count} files failed to reformat")
        else:
            final_output.append(f"{failed_count} file failed to reformat")
    console.print(", ".join(final_output))

    return retval


if __name__ == "__main__":
    raise SystemExit(main())
