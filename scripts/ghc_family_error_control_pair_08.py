"""Bounded Lyren error-control pair 08: row_deinterleave, erasure_inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x2 import run

ALLOWED = ['row_deinterleave', 'erasure_inventory']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    if bool(args.request_json) == bool(args.input):
        raise SystemExit("provide exactly one request source")
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = run(request) if request.get("operation") in ALLOWED else {"ok": False, "error": "operation_outside_pair", "original_success_credit": 0}
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
