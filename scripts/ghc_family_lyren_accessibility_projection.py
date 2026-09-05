"""Bitemporal and accessible chronology projections for synthetic records."""

from __future__ import annotations

import argparse
import json
import re
from datetime import timezone
from pathlib import Path
from typing import Any

from dateutil import parser as date_parser


OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


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
    return type(value) is int and abs(value) <= 2_000_000


def recorded_asof(data: dict[str, Any]) -> Any:
    records, recorded_cut, valid_tick = data.get("records"), data.get("recorded_cut"), data.get("valid_tick")
    if not isinstance(records, list) or not _tick(recorded_cut) or not _tick(valid_tick):
        return {"error": "invalid_input"}
    selected: list[str] = []
    for row in records:
        required = (row.get("record"), row.get("recorded"), row.get("valid_lo"), row.get("valid_hi")) if isinstance(row, dict) else (None, None, None, None)
        if not isinstance(required[0], str) or not all(_tick(value) for value in required[1:]) or required[2] >= required[3]:
            return {"error": "invalid_record"}
        if row["recorded"] <= recorded_cut and row["valid_lo"] <= valid_tick < row["valid_hi"]:
            selected.append(row["record"])
    return sorted(selected)


def _parents(records: Any) -> tuple[dict[str, str | None] | None, dict[str, str] | None]:
    if not isinstance(records, list):
        return None, {"error": "invalid_input"}
    parents: dict[str, str | None] = {}
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("record"), str) or not row["record"]:
            return None, {"error": "invalid_record"}
        label, parent = row["record"], row.get("parent")
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


def supersession_chain(data: dict[str, Any]) -> Any:
    parents, error = _parents(data.get("records"))
    if error:
        return error
    tip = data.get("tip")
    if not isinstance(tip, str) or tip not in parents:
        return {"error": "unknown_tip"}
    chain: list[str] = []
    cursor: str | None = tip
    while cursor is not None:
        chain.append(cursor)
        cursor = parents[cursor]
    return list(reversed(chain))


def _normalize(value: Any) -> str | None:
    if not isinstance(value, str) or re.search(r":60(?:[.,]|Z|[+-]|$)", value, re.IGNORECASE):
        return None
    try:
        parsed = date_parser.isoparse(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    converted = parsed.astimezone(timezone.utc)
    timespec = "microseconds" if converted.microsecond else "seconds"
    return converted.isoformat(timespec=timespec).replace("+00:00", "Z")


def accessible_chronology(data: dict[str, Any]) -> Any:
    records = data.get("records")
    if not isinstance(records, list):
        return {"error": "invalid_input"}
    rows: list[tuple[str, str, str]] = []
    labels: set[str] = set()
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("record"), str) or not row["record"]:
            return {"error": "invalid_record"}
        if row["record"] in labels:
            return {"error": "duplicate_record"}
        labels.add(row["record"])
        if row.get("outcome") not in OUTCOMES:
            return {"error": "invalid_outcome"}
        instant = _normalize(row.get("instant"))
        if instant is None:
            return {"error": "invalid_timestamp"}
        rows.append((instant, row["record"], row["outcome"]))
    rendered = [f"{label} | {instant} | {outcome}" for instant, label, outcome in sorted(rows)]
    return {"rows": rendered, "manual_review_reserved": True, "real_authority": False}


def duration_phrase(data: dict[str, Any]) -> Any:
    seconds = data.get("seconds")
    if type(seconds) is not int:
        return {"error": "invalid_duration"}
    if seconds < 0:
        return {"error": "negative_duration"}
    remaining = seconds
    values = []
    for unit, size in (("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)):
        count, remaining = divmod(remaining, size)
        if count:
            values.append(f"{count} {unit}{'' if count == 1 else 's'}")
    return {"text": ", ".join(values) if values else "0 seconds", "manual_review_reserved": True}


OPERATIONS = {
    "recorded_asof": recorded_asof,
    "supersession_chain": supersession_chain,
    "accessible_chronology": accessible_chronology,
    "duration_phrase": duration_phrase,
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
