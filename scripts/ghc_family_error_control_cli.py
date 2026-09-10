"""File or inline JSON CLI for Lyren's bounded error-control operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x1 import run as run_x1


def run(request):
    return run_x1(request)


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--request-json")
    source.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = run(request)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
