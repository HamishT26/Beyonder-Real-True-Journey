#!/usr/bin/env python3
"""Finite synthetic weave-draft contracts for Elaren v689-v4 x1.

The engine performs no loom, material, participant, identity, network, rights,
or authority action.  Its accepted domain is the frozen ten-case profile only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OPERATIONS = (
    "draft_dimensions",
    "threading_sequence",
    "tieup_matrix",
    "treadling_sequence",
    "drawdown_matrix",
    "float_profile",
    "repeat_period",
    "color_run_lengths",
    "draft_transpose",
    "draft_symmetry",
)
ERRORS = ("E_EMPTY", "E_RANGE", "E_TYPE", "E_SCHEMA")


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _value(operation: str, index: int) -> dict[str, Any]:
    number = index + 1
    if operation == "draft_dimensions":
        ends, picks = 4 + number, 6 + 2 * index
        return {
            "cells": ends * picks,
            "ends": ends,
            "picks": picks,
            "shafts": 1 + index % 6,
            "synthetic_only": True,
            "treadles": 2 + index % 7,
        }
    if operation == "threading_sequence":
        shaft_count = 1 + index % 4
        return {
            "direction": "left_to_right" if index % 2 == 0 else "right_to_left",
            "shaft_count": shaft_count,
            "threading": [1 + (item % shaft_count) for item in range(number + 2)],
        }
    if operation == "tieup_matrix":
        return {
            "active_ties": 2 + index,
            "convention": "rising" if index % 2 == 0 else "sinking",
            "shafts": 2 + index % 3,
            "treadles": 2 + index % 4,
        }
    if operation == "treadling_sequence":
        treadle_count = 2 + index % 5
        return {
            "picks": [1 + item % treadle_count for item in range(number + 1)],
            "reading": "top_to_bottom",
            "treadle_count": treadle_count,
        }
    if operation == "drawdown_matrix":
        rows, columns = 2 + index, 3 + index
        return {
            "columns": columns,
            "real_cloth": False,
            "rows": rows,
            "warp_up_cells": rows * columns // 2,
        }
    if operation == "float_profile":
        return {
            "claims_safe_to_weave": False,
            "warp_down_max": 2 + index,
            "warp_up_max": 1 + index,
            "weft_down_max": 2 + index % 2,
            "weft_up_max": 1 + index % 3,
        }
    if operation == "repeat_period":
        return {
            "period": number,
            "repeat_unit": [f"R{item + 1}" for item in range(number)],
            "sequence_length": 2 * number,
        }
    if operation == "color_run_lengths":
        return {
            "run_count": number,
            "runs": [
                {"length": item + 1, "token": f"C{item + 1}"}
                for item in range(number)
            ],
            "sequence_length": sum(range(1, number + 1)),
        }
    if operation == "draft_transpose":
        return {
            "source_columns": 2 + index,
            "source_rows": number,
            "target_columns": number,
            "target_rows": 2 + index,
        }
    if operation == "draft_symmetry":
        return {
            "horizontal_mirror": index in (0, 2, 4),
            "rotational_180": index in (0, 2),
            "vertical_mirror": index in (0, 3),
        }
    raise KeyError(operation)


def evaluate(request: Any) -> dict[str, Any]:
    """Return one complete envelope for a frozen x1 request."""
    if not isinstance(request, dict):
        return {"error": "E_SHAPE", "ok": False, "value": None}
    if set(request) != {"op", "case", "payload"}:
        return {"error": "E_FIELDS", "ok": False, "value": None}
    operation, case, payload = request["op"], request["case"], request["payload"]
    if operation not in OPERATIONS:
        return {"error": "E_OPERATION", "ok": False, "value": None}
    if not _is_int(case) or not 1 <= case <= 10:
        return {"error": "E_CASE", "ok": False, "value": None}
    if (
        not isinstance(payload, dict)
        or set(payload) != {"seed", "synthetic"}
        or not _is_int(payload["seed"])
        or payload["seed"] < 1
        or payload["synthetic"] is not True
    ):
        return {"error": "E_PAYLOAD", "ok": False, "value": None}
    index = case - 1
    if index >= 6:
        return {"error": ERRORS[index - 6], "ok": False, "value": None}
    return {"error": None, "ok": True, "value": _value(operation, index)}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.input:
        request = json.loads(
            args.input.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
    else:
        request = json.load(__import__("sys").stdin, object_pairs_hook=_unique_object)
    result = evaluate(request)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
