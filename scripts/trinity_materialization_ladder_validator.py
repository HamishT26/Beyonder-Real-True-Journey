#!/usr/bin/env python3
"""Validate the Trinity materialization ladder."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = {
    "level_id",
    "desired_state",
    "actual_state",
    "write_scope",
    "target_class",
    "promotion_requirements",
    "rollback_requirements",
    "blockers",
    "proof_artifacts",
}
EXPECTED_LEVELS = [
    "l1_disposable_staging",
    "l2_persistent_dev",
    "l3_uat_preprod",
    "l4_standard_prod",
    "l5_ha_prod",
]


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Trinity Materialization Ladder Validation",
            "",
            f"- generated_utc: `{payload['generated_utc']}`",
            f"- overall_status: **{payload['overall_status']}**",
            f"- level_count: `{payload['level_count']}`",
            "",
            "## Failures",
            *([f"- {item}" for item in payload["failures"]] or ["- none"]),
            "",
            "## Warnings",
            *([f"- {item}" for item in payload["warnings"]] or ["- none"]),
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Trinity materialization ladder.")
    parser.add_argument("--ladder", default="docs/trinity-materialization-ladder-v2.json")
    parser.add_argument("--reports-dir", default="docs/trinity-materialization-ladder-runs")
    parser.add_argument("--latest-json", default="docs/trinity-materialization-ladder-validation-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-materialization-ladder-validation-latest.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    payload = json.loads(_repo_path(args.ladder).read_text(encoding="utf-8"))
    if str(payload.get("default_materialize_level") or "") != "l2_persistent_dev":
        failures.append("default_materialize_level must be l2_persistent_dev")
    levels = payload.get("levels", [])
    if not isinstance(levels, list):
        failures.append("levels must be a list")
        levels = []
    if len(levels) != 5:
        failures.append(f"expected 5 levels, found {len(levels)}")

    seen: list[str] = []
    for index, row in enumerate(levels):
        label = f"levels[{index}]"
        if not isinstance(row, dict):
            failures.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            failures.append(f"{label} missing fields: {missing}")
        level_id = str(row.get("level_id") or "").strip()
        seen.append(level_id)
        for field in ("promotion_requirements", "rollback_requirements", "blockers", "proof_artifacts"):
            if not isinstance(row.get(field), list):
                failures.append(f"{level_id or label} {field} must be a list")
    if seen != EXPECTED_LEVELS:
        failures.append(f"unexpected level ordering: {seen}")
    for level_id in ("l3_uat_preprod", "l4_standard_prod", "l5_ha_prod"):
        row = next((item for item in levels if isinstance(item, dict) and item.get("level_id") == level_id), {})
        actual_state = str(row.get("actual_state") or "")
        proofs = row.get("proof_artifacts", [])
        if actual_state == "readiness_only":
            continue
        if not proofs:
            failures.append(f"{level_id} live promotion requires proof_artifacts")

    result = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": _status(failures, warnings),
        "level_count": len(levels),
        "failures": failures,
        "warnings": warnings,
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }
    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    (reports_dir / f"{stamp}-trinity-materialization-ladder-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (reports_dir / f"{stamp}-trinity-materialization-ladder-validation.md").write_text(_markdown(result), encoding="utf-8")
    latest_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(_markdown(result), encoding="utf-8")
    print(f"overall_status={result['overall_status']}")
    print(f"effective_success={result['effective_success']}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")
    return 0 if result["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
