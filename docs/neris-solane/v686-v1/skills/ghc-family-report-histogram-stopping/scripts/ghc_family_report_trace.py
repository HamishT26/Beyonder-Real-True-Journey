"""Type-strict report tribunal for synthetic calendar, state, queue, and replay results."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import ghc_family_protocol_trace as protocol


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def evaluate(operation, data, reported):
    before = canonical(data)
    working = copy.deepcopy(data)
    computed = protocol.evaluate(operation, working)
    errors = []
    if canonical(data) != before or canonical(working) != before:
        errors.append("input_mutated")
    if canonical(computed) != canonical(reported):
        errors.append("fabricated_report")
    return {
        "accepted": not errors,
        "computed": computed,
        "errors": errors,
        "input_sha256": hashlib.sha256(before.encode("utf-8")).hexdigest(),
        "report_sha256": hashlib.sha256(canonical(computed).encode("utf-8")).hexdigest(),
        "input_unchanged": "input_mutated" not in errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        result = evaluate(fixture["operation"], fixture["input"], fixture["reported"])
    except (OSError, ValueError, KeyError, TypeError):
        result = {"accepted": False, "computed": None, "errors": ["malformed_fixture"], "input_unchanged": True}
    text = json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        with Path(args.output).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
