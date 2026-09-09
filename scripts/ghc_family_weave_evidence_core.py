#!/usr/bin/env python3
"""Finite synthetic weave-evidence contracts for Elaren v689-v4 x2.

This module transforms only the frozen synthetic case profile.  It performs no
network ingestion, real textile work, rights decision, or authority action.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OPERATIONS = (
    "liftplan_from_tieup",
    "tieup_from_liftplan",
    "drawdown_difference",
    "block_substitution",
    "draft_digest",
    "correction_chain",
    "accessibility_projection",
    "rights_reservation",
    "source_adapter",
    "authority_reservation",
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
    if operation == "liftplan_from_tieup":
        return {
            "liftplan": [[1 + item % 4] for item in range(number)],
            "pick_count": number,
            "source_tieup_retained": True,
        }
    if operation == "tieup_from_liftplan":
        return {
            "lossless_for_lift_sets": True,
            "treadle_count": number,
            "treadling": list(range(1, number + 1)),
        }
    if operation == "drawdown_difference":
        return {
            "difference_count": index,
            "different_cells": [[item, item] for item in range(index)],
            "same_shape": True,
        }
    if operation == "block_substitution":
        block_columns = 1 + index % 3
        return {
            "block_columns": block_columns,
            "block_rows": number,
            "expanded_cells": 4 * number * block_columns,
            "tile_columns": 2,
            "tile_rows": 2,
        }
    if operation == "draft_digest":
        raw = _canonical({"case": number, "draft": "synthetic"})
        return {
            "canonical_bytes": len(raw),
            "correspondence_only": True,
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    if operation == "correction_chain":
        return {
            "event_count": index,
            "final_revision": index,
            "nonerasing": True,
            "real_draft_changed": False,
        }
    if operation == "accessibility_projection":
        return {
            "manual_assistive_review": False,
            "row_count": number,
            "structural_projection": True,
            "text_token": f"pick-{number}-state-explicit",
        }
    if operation == "rights_reservation":
        return {
            "artifact": f"SYN-DRAFT-{number:02d}",
            "cultural_review": ("absent", "reserved", "required")[index % 3],
            "release_authorized": False,
            "rights_status": ("unknown", "declared_unverified", "reserved")[index % 3],
        }
    if operation == "source_adapter":
        live = index >= 5
        return {
            "ingested_rows": 0,
            "live_network_calls": 0,
            "missing_authority_or_schema": live,
            "mode": "live_ingest" if live else "zero_row",
        }
    if operation == "authority_reservation":
        actions = (
            "loom_operation",
            "textile_safety_decision",
            "rights_release",
            "cultural_interpretation",
            "maori_authority_decision",
        )
        requested = index >= 5
        return {
            "action": actions[index % 5],
            "disposition": "exact_gate" if requested else "not_requested",
            "executed": False,
            "requested": requested,
        }
    raise KeyError(operation)


def evaluate(request: Any) -> dict[str, Any]:
    """Return one complete envelope for a frozen x2 request."""
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
    if operation not in {
        "accessibility_projection",
        "rights_reservation",
        "source_adapter",
        "authority_reservation",
    } and index >= 6:
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
