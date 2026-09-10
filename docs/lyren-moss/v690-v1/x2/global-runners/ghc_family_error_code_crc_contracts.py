"""Public bounded dispatcher for ghc-family-error-code-crc-contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x1 import run as run_x1
from ghc_family_error_control_x2 import run as run_x2

ALLOWED = ['gf2_division_remainder', 'crc_remainder', 'crc_append', 'crc_verify']


def dispatch(request):
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        return {"ok": False, "error": "operation_outside_group", "original_success_credit": 0}
    result = run_x2(request)
    return run_x1(request) if result.get("error") == "unknown_operation" else result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    if bool(args.request_json) == bool(args.input):
        raise SystemExit("provide exactly one request source")
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = dispatch(request)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
