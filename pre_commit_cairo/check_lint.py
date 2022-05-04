from __future__ import annotations

import argparse
import subprocess
import json
from typing import Sequence
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def _build_summary(info, filename):
    table_result = Table(title=filename, expand=True)
    table_result.add_column("ruleId")
    table_result.add_column("level")
    table_result.add_column("message")

    table_result.add_row(
        str(info["ruleId"]), str(info["level"]), str(info["message"]["text"])
    )

    console.print(table_result)

    table_location = Table(title="locations", expand=True)
    table_location.add_column("uri")
    table_location.add_column("location_line")
    table_location.add_column("location_column_start")
    table_location.add_column("location_column_end")

    for location in info["locations"]:
        table_location.add_row(
            str(location["physicalLocation"]["artifactLocation"]["uri"]),
            str(location["physicalLocation"]["region"]["startLine"]),
            str(location["physicalLocation"]["region"]["startColumn"]),
            str(location["physicalLocation"]["region"]["endColumn"]),
        )

    console.print(table_location)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if filename.endswith(".cairo"):
            subprocess.run(
                f'amarna {filename} -o {filename.replace(".cairo", ".sarif")}',
                shell=True,
                universal_newlines=True,
                check=True,
            )
            path = Path(filename.replace(".cairo", ".sarif"))

            if path.is_file():
                console.print(
                    f"[red][bold]{filename}: failed linting check[/bold][/red]"
                )
                with open(str(path.resolve()), "r") as f:
                    summary = json.load(f)
                for run in summary["runs"]:
                    for result in run["results"]:
                        # Remove output and hook error if arithmetic warning.
                        # The arithmetic rule only warns of operands usage
                        if "arithmetic" not in result["ruleId"]:
                            _build_summary(result, filename)
                            retval = 1

    return retval


if __name__ == "__main__":
    raise SystemExit(main())
