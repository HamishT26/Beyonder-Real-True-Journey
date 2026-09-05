"""Synthetic disclosure, custody-transfer, and immutable correction contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from immutables import Map


MAX_TICK = 2_000_000


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_member")
        result[key] = value
    return result


def read_strict(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def _tick(value: Any) -> bool:
    return type(value) is int and abs(value) <= MAX_TICK


def disclosure_slice(data: dict[str, Any]) -> dict[str, Any]:
    records, now = data.get("records"), data.get("now")
    if not isinstance(records, list) or not _tick(now):
        return {"error": "invalid_input"}
    visible: list[str] = []
    labels: set[str] = set()
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("record"), str) or not row["record"]:
            return {"error": "invalid_record"}
        if row["record"] in labels:
            return {"error": "duplicate_record"}
        labels.add(row["record"])
        if type(row.get("public")) is not bool:
            return {"error": "invalid_public_flag"}
        if not _tick(row.get("lo")) or not _tick(row.get("hi")) or row["lo"] >= row["hi"]:
            return {"error": "invalid_window"}
        if row["public"] and row["lo"] <= now < row["hi"]:
            visible.append(row["record"])
    return {"records": sorted(visible), "real_disclosure": False}


def transfer_sequence(data: dict[str, Any]) -> dict[str, Any]:
    transfers = data.get("transfers")
    if not isinstance(transfers, list) or not transfers:
        return {"error": "missing_origin"}
    current: str | None = None
    for index, row in enumerate(transfers):
        if not isinstance(row, dict):
            return {"error": "invalid_transfer"}
        prior, next_holder = row.get("from"), row.get("to")
        if not isinstance(next_holder, str) or not next_holder:
            return {"error": "invalid_holder"}
        if prior is not None and (not isinstance(prior, str) or not prior):
            return {"error": "invalid_holder"}
        if index == 0:
            if prior is not None:
                return {"error": "missing_origin"}
        elif prior is None:
            return {"error": "multiple_origins"}
        elif prior != current:
            return {"error": "broken_transfer"}
        current = next_holder
    return {"holder": current, "real_custody": False, "valid": True}


def immutable_append(data: dict[str, Any]) -> dict[str, Any]:
    prior, key = data.get("prior"), data.get("key")
    if not isinstance(prior, dict) or not isinstance(key, str) or not key:
        return {"error": "invalid_input"}
    before = json.loads(json.dumps(prior, ensure_ascii=False, allow_nan=False))
    persistent = Map(prior)
    next_map = persistent.set(key, data.get("value"))
    return {
        "prior": before,
        "next": dict(next_map),
        "prior_unchanged": prior == before and dict(persistent) == before,
    }


def _graph(records: Any) -> tuple[dict[str, str | None] | None, dict[str, str] | None]:
    if not isinstance(records, list):
        return None, {"error": "invalid_input"}
    parents: dict[str, str | None] = {}
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("record"), str) or not row["record"]:
            return None, {"error": "invalid_record"}
        label = row["record"]
        parent = row.get("parent")
        if label in parents:
            return None, {"error": "duplicate_record"}
        if parent is not None and (not isinstance(parent, str) or not parent):
            return None, {"error": "invalid_parent"}
        parents[label] = parent
    for parent in parents.values():
        if parent is not None and parent not in parents:
            return None, {"error": "missing_parent"}
    for label in parents:
        seen: set[str] = set()
        cursor: str | None = label
        while cursor is not None:
            if cursor in seen:
                return None, {"error": "cycle"}
            seen.add(cursor)
            cursor = parents[cursor]
    return parents, None


def correction_tips(data: dict[str, Any]) -> Any:
    parents, error = _graph(data.get("records"))
    if error:
        return error
    referenced = {parent for parent in parents.values() if parent is not None}
    return sorted(set(parents) - referenced)


OPERATIONS = {
    "disclosure_slice": disclosure_slice,
    "transfer_sequence": transfer_sequence,
    "immutable_append": immutable_append,
    "correction_tips": correction_tips,
}


def run(operation: str, data: Any) -> Any:
    if operation not in OPERATIONS:
        return {"error": "unknown_operation"}
    if not isinstance(data, dict):
        return {"error": "invalid_input"}
    return OPERATIONS[operation](data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("output exists; exclusive-write refusal")
    try:
        payload = read_strict(args.input)
        result = run(payload.get("operation"), payload.get("input")) if isinstance(payload, dict) else {"error": "invalid_input"}
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        result = {"error": "invalid_json"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
