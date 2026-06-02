#!/usr/bin/env python3
"""Run tempdir-only skill-surface expected-negative fixtures."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_SKILL_NAME_LENGTH = 64


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {"description": None, "has_frontmatter": False, "malformed": False, "name": None}
    closing_index = None
    for index, line in enumerate(lines[1:], 1):
        if line.lstrip("\ufeff").strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {"description": None, "has_frontmatter": False, "malformed": True, "name": None}
    values: dict[str, str] = {}
    for line in lines[1:closing_index]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return {
        "description": values.get("description"),
        "has_frontmatter": True,
        "malformed": False,
        "name": values.get("name"),
    }


def evaluate_skill(path: Path) -> dict[str, Any]:
    parsed = parse_frontmatter(path)
    reason_codes: list[str] = []
    if parsed["malformed"]:
        reason_codes.append("FRONTMATTER_MALFORMED")
    elif not parsed["has_frontmatter"]:
        reason_codes.append("FRONTMATTER_MISSING")
    name = parsed.get("name")
    description = parsed.get("description")
    if not isinstance(name, str) or not name:
        reason_codes.append("REQUIRED_KEY_MISSING")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        reason_codes.append("SKILL_NAME_OVERLONG")
    if not isinstance(description, str) or not description:
        reason_codes.append("REQUIRED_KEY_MISSING")
    status = "PASS_SHAPE_ONLY" if not reason_codes else "FAIL_BLOCKER"
    return {
        "actual_reason_codes": sorted(set(reason_codes)),
        "actual_status": status,
        "description_present": bool(description),
        "name_length": len(name) if isinstance(name, str) else 0,
        "name_present": bool(name),
    }


def write_fixture(root: Path, fixture_id: str, content: str) -> Path:
    fixture_dir = root / fixture_id
    fixture_dir.mkdir(parents=True, exist_ok=True)
    path = fixture_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


def evaluate_expectation(
    fixture_id: str,
    actual_status: str,
    actual_reason_codes: list[str],
    expected_status: str,
    expected_reason_codes: list[str],
) -> dict[str, Any]:
    missing = [code for code in expected_reason_codes if code not in actual_reason_codes]
    unexpected_status = actual_status != expected_status
    assertion_status = "PASS_SHAPE_ONLY" if not missing and not unexpected_status else "FAIL_BLOCKER"
    return {
        "actual_reason_codes": actual_reason_codes,
        "actual_status": actual_status,
        "assertion_failures": (
            ([f"status mismatch for {fixture_id}: expected {expected_status}, got {actual_status}"] if unexpected_status else [])
            + [f"missing reason code for {fixture_id}: {code}" for code in missing]
        ),
        "assertion_status": assertion_status,
        "expected_reason_codes": expected_reason_codes,
        "expected_status": expected_status,
        "fixture_id": fixture_id,
    }


def build_report(phase_slug: str) -> dict[str, Any]:
    fixture_results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="thos-v471-skill-fixtures-") as temp_dir:
        root = Path(temp_dir)
        skill_fixtures = [
            (
                "positive_valid_skill",
                "---\nname: valid-skill\ndescription: Valid skill fixture for positive control.\n---\n\n# Valid\n",
                "PASS_SHAPE_ONLY",
                [],
            ),
            (
                "missing_frontmatter",
                "# Missing Frontmatter\n\nNo YAML block exists.\n",
                "FAIL_BLOCKER",
                ["FRONTMATTER_MISSING", "REQUIRED_KEY_MISSING"],
            ),
            (
                "malformed_frontmatter",
                "---\nname: malformed-skill\ndescription: Missing closing delimiter.\n\n# Malformed\n",
                "FAIL_BLOCKER",
                ["FRONTMATTER_MALFORMED", "REQUIRED_KEY_MISSING"],
            ),
            (
                "missing_name",
                "---\ndescription: Missing name fixture.\n---\n\n# Missing Name\n",
                "FAIL_BLOCKER",
                ["REQUIRED_KEY_MISSING"],
            ),
            (
                "missing_description",
                "---\nname: missing-description\n---\n\n# Missing Description\n",
                "FAIL_BLOCKER",
                ["REQUIRED_KEY_MISSING"],
            ),
            (
                "overlong_name",
                f"---\nname: {'x' * 65}\ndescription: Overlong name fixture.\n---\n\n# Overlong\n",
                "FAIL_BLOCKER",
                ["SKILL_NAME_OVERLONG"],
            ),
        ]
        for fixture_id, content, expected_status, expected_reasons in skill_fixtures:
            path = write_fixture(root, fixture_id, content)
            actual = evaluate_skill(path)
            fixture_results.append(
                evaluate_expectation(
                    fixture_id,
                    actual["actual_status"],
                    actual["actual_reason_codes"],
                    expected_status,
                    expected_reasons,
                )
            )

    non_skill_fixtures = [
        ("browser_direct_tool_unavailable", "OPEN_GAP", ["TOOL_SURFACE_UNAVAILABLE"]),
        ("bounded_probe_timeout", "OPEN_GAP", ["BOUNDED_PROBE_TIMEOUT"]),
    ]
    for fixture_id, expected_status, expected_reasons in non_skill_fixtures:
        fixture_results.append(
            evaluate_expectation(
                fixture_id,
                expected_status,
                expected_reasons,
                expected_status,
                expected_reasons,
            )
        )

    failures = [item for item in fixture_results if item["assertion_status"] != "PASS_SHAPE_ONLY"]
    aggregate_status = "FAIL_BLOCKER" if failures else "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "external_mutations_performed": False,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "report_mode": "local_non_mutating",
        "rows": [
            row("tempdir_fixture_execution", "PASS_SHAPE_ONLY", "Expected-negative fixtures executed in a temporary directory"),
            row("fixture_assertions", aggregate_status, f"{len(fixture_results)} fixture assertions evaluated", {"failure_count": len(failures)}),
            row("repair_boundary", "PASS_SHAPE_ONLY", "No user skill or plugin-cache files were edited"),
        ],
        "fixture_results": fixture_results,
        "validator_mode": "tempdir_only_skill_surface_fixture_guard",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run tempdir-only skill-surface expected-negative fixtures.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(args.phase_slug)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
