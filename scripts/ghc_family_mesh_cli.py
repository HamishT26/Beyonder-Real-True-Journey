"""Strict JSON file/stdin interface for one declared pair of synthetic operations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("E_DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def parse_json(text: str):
    if len(text.encode("utf-8")) > 200_000:
        raise ValueError("E_INPUT_CAPACITY")
    return json.loads(text, object_pairs_hook=unique_pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("E_NONFINITE")))


def main(evaluator, operations) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        request = parse_json(args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read())
        if type(request) is dict and request.get("op") not in operations:
            result = {"ok": False, "value": None, "error": "E_RUNNER_SCOPE"}
        else:
            result = evaluator(request)
    except (ValueError, UnicodeError) as error:
        result = {"ok": False, "value": None, "error": str(error)}
    data = (json.dumps(result, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    if args.output:
        with args.output.open("xb") as stream:
            stream.write(data)
    else:
        sys.stdout.buffer.write(data)
    return 0 if result["ok"] else 2
