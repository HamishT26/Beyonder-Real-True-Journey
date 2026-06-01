#!/usr/bin/env python3
"""Validate THOS phase-manifest examples against a JSON Schema contract."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing json file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json file: {path}: {exc}") from exc


def _parse_case(raw: str) -> tuple[str, bool, Path]:
    parts = raw.split(":", 2)
    if len(parts) != 3:
        raise SystemExit("case must use name:pass|fail:path")
    name, expected, path = parts
    if not name:
        raise SystemExit("case name must be non-empty")
    if expected not in {"pass", "fail"}:
        raise SystemExit("case expectation must be pass or fail")
    return name, expected == "pass", Path(path)


def _jsonschema_module():
    try:
        import jsonschema  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "jsonschema is not installed; keep schema as documentation or install an approved validator."
        ) from exc
    return jsonschema


def main() -> int:
    parser = argparse.ArgumentParser(description="Run THOS JSON Schema fixture checks.")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    jsonschema = _jsonschema_module()
    schema = _load_json(args.schema)
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)

    cases = [_parse_case(raw) for raw in args.case]
    if not cases:
        raise SystemExit("at least one --case is required")

    results: list[dict[str, Any]] = []
    for name, expected_pass, path in cases:
        instance = _load_json(path)
        errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
        actual_pass = not errors
        results.append(
            {
                "case": name,
                "path": path.as_posix(),
                "expected": "pass" if expected_pass else "fail",
                "actual": "pass" if actual_pass else "fail",
                "matched": expected_pass == actual_pass,
                "error_count": len(errors),
                "errors": [error.message for error in errors[:5]],
            }
        )

    status = "PASS" if all(result["matched"] for result in results) else "FAIL"
    report = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "schema": args.schema.as_posix(),
        "status": status,
        "validator": "jsonschema.Draft202012Validator",
        "cases": results,
    }
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"THOS_PHASE_SCHEMA_FIXTURES_{status} {args.schema.as_posix()}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
