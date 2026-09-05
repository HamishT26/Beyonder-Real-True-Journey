"""Synthetic clock-offset, custody-window, and embargo contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MAX_TICK = 2_000_000


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate_member")
        value[key] = item
    return value


def read_strict(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def _tick(value: Any) -> bool:
    return type(value) is int and abs(value) <= MAX_TICK


def clock_offset(data: dict[str, Any]) -> dict[str, Any]:
    observed, reference = data.get("observed"), data.get("reference")
    if type(observed) is not int or type(reference) is not int:
        return {"error": "invalid_tick"}
    if max(abs(observed), abs(reference)) > MAX_TICK:
        return {"error": "tick_budget_exceeded"}
    return {"offset_ticks": observed - reference, "physical_clock_verified": False}


def _window(row: dict[str, Any]) -> bool:
    return _tick(row.get("lo")) and _tick(row.get("hi")) and row["lo"] < row["hi"]


def custody_at(data: dict[str, Any]) -> dict[str, Any]:
    records, tick = data.get("records"), data.get("tick")
    if not isinstance(records, list) or not _tick(tick):
        return {"error": "invalid_input"}
    holders: list[str] = []
    for row in records:
        if not isinstance(row, dict) or not _window(row) or not isinstance(row.get("holder"), str) or not row["holder"]:
            return {"error": "invalid_custody_record"}
        if row["lo"] <= tick < row["hi"]:
            holders.append(row["holder"])
    return {"active_holders": sorted(holders), "real_custody": False}


def custody_overlap(data: dict[str, Any]) -> dict[str, Any]:
    records = data.get("records")
    if not isinstance(records, list):
        return {"error": "invalid_input"}
    checked: list[dict[str, Any]] = []
    labels: set[str] = set()
    for row in records:
        if not isinstance(row, dict) or not _window(row) or not isinstance(row.get("record"), str) or not row["record"] or not isinstance(row.get("asset"), str) or not row["asset"]:
            return {"error": "invalid_custody_record"}
        if row["record"] in labels:
            return {"error": "duplicate_record"}
        labels.add(row["record"])
        checked.append(row)
    pairs: list[list[str]] = []
    for index, left in enumerate(checked):
        for right in checked[index + 1 :]:
            if left["asset"] == right["asset"] and max(left["lo"], right["lo"]) < min(left["hi"], right["hi"]):
                pairs.append(sorted([left["record"], right["record"]]))
    return {"pairs": sorted(pairs), "real_custody": False}


def embargo_state(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("synthetic") is not True:
        return {"error": "synthetic_required"}
    now, lo, hi = data.get("now"), data.get("lo"), data.get("hi")
    if any(type(value) is not int for value in (now, lo, hi)):
        return {"error": "invalid_tick"}
    if max(abs(now), abs(lo), abs(hi)) > MAX_TICK:
        return {"error": "tick_budget_exceeded"}
    if lo >= hi:
        return {"error": "invalid_window"}
    state = "not_yet_active" if now < lo else "withheld" if now < hi else "released_by_fixture"
    return {"state": state, "real_authority": False}


OPERATIONS = {
    "clock_offset": clock_offset,
    "custody_at": custody_at,
    "custody_overlap": custody_overlap,
    "embargo_state": embargo_state,
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
