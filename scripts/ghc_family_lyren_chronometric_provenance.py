"""Bounded synthetic chronometric provenance contracts for Lyren v686-v5."""

from __future__ import annotations

import argparse
import json
import math
import re
from datetime import timedelta, timezone
from pathlib import Path
from typing import Any

import isodate
from dateutil import parser as date_parser


MAX_TICK = 2_000_000


class DuplicateMember(ValueError):
    """Raised when a JSON object repeats a member name."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateMember(key)
        result[key] = value
    return result


def read_strict(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def _instant(value: Any) -> tuple[Any | None, dict[str, str] | None]:
    if not isinstance(value, str):
        return None, {"error": "invalid_timestamp"}
    if re.search(r":60(?:[.,]|Z|[+-]|$)", value, flags=re.IGNORECASE):
        return None, {"error": "leap_second_unverified"}
    try:
        parsed = date_parser.isoparse(value)
    except (TypeError, ValueError, OverflowError):
        return None, {"error": "invalid_timestamp"}
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None, {"error": "offset_required"}
    return parsed, None


def _utc_text(value: Any) -> dict[str, Any]:
    parsed, error = _instant(value)
    if error:
        return error
    converted = parsed.astimezone(timezone.utc)
    timespec = "microseconds" if converted.microsecond else "seconds"
    return {
        "normalized_utc": converted.isoformat(timespec=timespec).replace("+00:00", "Z"),
        "physical_clock_verified": False,
    }


def _seconds(value: float) -> int | float:
    return int(value) if float(value).is_integer() else float(value)


def instant_normalize(data: dict[str, Any]) -> dict[str, Any]:
    return _utc_text(data.get("value"))


def duration_seconds(data: dict[str, Any]) -> dict[str, Any]:
    start, start_error = _instant(data.get("start"))
    end, end_error = _instant(data.get("end"))
    if start_error:
        return start_error
    if end_error:
        return end_error
    seconds = (end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds()
    if seconds < 0:
        return {"error": "reversed_duration"}
    return {"seconds": _seconds(seconds), "physical_duration_verified": False}


def duration_parse(data: dict[str, Any]) -> dict[str, Any]:
    value = data.get("value")
    if not isinstance(value, str):
        return {"error": "invalid_duration"}
    if value.startswith("-"):
        return {"error": "negative_duration"}
    try:
        parsed = isodate.parse_duration(value)
    except (TypeError, ValueError, OverflowError, isodate.ISO8601Error):
        return {"error": "invalid_duration"}
    if isinstance(parsed, isodate.duration.Duration):
        if parsed.years or parsed.months:
            return {"error": "nonfixed_duration"}
        parsed = parsed.totimedelta(start=None)
    if not isinstance(parsed, timedelta):
        return {"error": "invalid_duration"}
    seconds = parsed.total_seconds()
    if not math.isfinite(seconds):
        return {"error": "invalid_duration"}
    if seconds < 0:
        return {"error": "negative_duration"}
    return {"seconds": _seconds(seconds), "physical_duration_verified": False}


def uncertainty_envelope(data: dict[str, Any]) -> dict[str, Any]:
    center = data.get("center")
    minus = data.get("minus")
    plus = data.get("plus")
    if any(type(value) is not int for value in (center, minus, plus)):
        return {"error": "invalid_tick"}
    if minus < 0 or plus < 0:
        return {"error": "invalid_uncertainty"}
    if max(abs(center), minus, plus) > MAX_TICK:
        return {"error": "tick_budget_exceeded"}
    return {"lower": center - minus, "upper": center + plus, "unit": "synthetic_ticks"}


OPERATIONS = {
    "instant_normalize": instant_normalize,
    "duration_seconds": duration_seconds,
    "duration_parse": duration_parse,
    "uncertainty_envelope": uncertainty_envelope,
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
