#!/usr/bin/env python3
"""Validate a rendered local THOS reason dashboard artifact."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORBIDDEN_CLAIM_RE = re.compile(
    r"(GMUT\s+validated|GMUT\s+validation\s+complete|"
    r"all\s+six\s+GMUT\s+gates\s+(?:closed|passed)|all\s+gates\s+closed|"
    r"final\s+physics\s+(?:complete|validated|solved)|consciousness\s+solved|"
    r"empirical\s+spiritual\s+proof\s+achieved|fifth[- ]force\s+safety\s+confirmed|"
    r"canon\s+promoted|cleanup\s+completed\s+successfully|"
    r"connector\s+write\s+completed\s+successfully|cloud\s+mutation\s+completed\s+successfully)",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|"
    r"gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|"
    r"(api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^\s\"']{8,})",
    re.IGNORECASE,
)
REQUIRED_LABELS = [
    "THOS Reason Dashboard",
    "Local non-mutating renderer",
    "Case ID",
    "Row Status",
    "Guard Status",
    "Guard Decision",
    "Dominant Reason",
    "Reason Codes",
    "Required Codes",
    "Missing Required",
    "Allowed Extras",
    "Unexpected Extras",
    "All six GMUT gates remain open",
]


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def row(row_id: str, status: str, message: str, evidence: object = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def assert_render(preflight: dict[str, Any], html_text: str, phase_slug: str) -> dict[str, Any]:
    rows = preflight.get("renderer_rows")
    if not isinstance(rows, list):
        rows = []
    clean_rows = [item for item in rows if isinstance(item, dict)]
    report_rows: list[dict[str, Any]] = []

    report_rows.append(
        row(
            "preflight_status",
            "PASS_SHAPE_ONLY" if preflight.get("aggregate_status") == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
            "preflight aggregate status is green",
            preflight.get("aggregate_status"),
        )
    )
    declared_count_match = re.search(r'data-case-count="(\d+)"', html_text)
    declared_count = int(declared_count_match.group(1)) if declared_count_match else None
    report_rows.append(
        row(
            "case_count_parity",
            "PASS_SHAPE_ONLY" if declared_count == len(clean_rows) else "FAIL_BLOCKER",
            "rendered artifact case count matches preflight renderer_rows",
            {"declared_case_count": declared_count, "preflight_case_count": len(clean_rows)},
        )
    )
    rendered_row_count = len(re.findall(r"<tr data-case-id=", html_text))
    report_rows.append(
        row(
            "row_count_parity",
            "PASS_SHAPE_ONLY" if rendered_row_count == len(clean_rows) else "FAIL_BLOCKER",
            "rendered table row count matches preflight renderer_rows",
            {"rendered_row_count": rendered_row_count, "preflight_row_count": len(clean_rows)},
        )
    )
    missing_labels = [label for label in REQUIRED_LABELS if label not in html_text]
    report_rows.append(
        row(
            "required_labels",
            "PASS_SHAPE_ONLY" if not missing_labels else "FAIL_BLOCKER",
            "required visible labels are present",
            {"missing_labels": missing_labels},
        )
    )
    missing_case_ids = [
        str(item.get("case_id"))
        for item in clean_rows
        if item.get("case_id") is not None and str(item.get("case_id")) not in html_text
    ]
    report_rows.append(
        row(
            "case_id_presence",
            "PASS_SHAPE_ONLY" if not missing_case_ids else "FAIL_BLOCKER",
            "every preflight case id is present in rendered artifact",
            {"missing_case_ids": missing_case_ids},
        )
    )
    forbidden_claims = sorted({match.group(0) for match in FORBIDDEN_CLAIM_RE.finditer(html_text)})
    report_rows.append(
        row(
            "forbidden_claim_guard",
            "PASS_SHAPE_ONLY" if not forbidden_claims else "FAIL_BLOCKER",
            "rendered artifact avoids forbidden claim wording",
            {"forbidden_claims": forbidden_claims},
        )
    )
    secret_shapes = sorted({match.group(0) for match in SECRET_RE.finditer(html_text)})
    report_rows.append(
        row(
            "credential_shape_guard",
            "PASS_SHAPE_ONLY" if not secret_shapes else "FAIL_BLOCKER",
            "rendered artifact avoids credential-shaped content",
            {"secret_shape_count": len(secret_shapes)},
        )
    )
    statuses = [item["status"] for item in report_rows]
    aggregate_status = "FAIL_BLOCKER" if "FAIL_BLOCKER" in statuses else "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rendered_artifact_checked": True,
        "rows": report_rows,
        "validator_mode": "local_non_mutating_render_assertion",
    }


def remove_first_render_row(html_text: str) -> str:
    return re.sub(r"\n\s*<tr data-case-id=.*?</tr>", "", html_text, count=1, flags=re.DOTALL)


def self_test_negative(preflight: dict[str, Any], html_text: str, phase_slug: str) -> dict[str, Any]:
    cases = [
        ("missing_required_label", html_text.replace("Case ID", "Case Identity", 1), "required_labels"),
        ("case_count_mismatch", re.sub(r'data-case-count="\d+"', 'data-case-count="0"', html_text, count=1), "case_count_parity"),
        ("row_count_mismatch", remove_first_render_row(html_text), "row_count_parity"),
    ]
    report_rows: list[dict[str, Any]] = []
    for case_id, mutated_html, expected_failing_row in cases:
        negative_report = assert_render(preflight, mutated_html, f"{phase_slug}-{case_id}")
        observed_failures = [
            item["row_id"]
            for item in negative_report["rows"]
            if item.get("status") == "FAIL_BLOCKER"
        ]
        passed = negative_report["aggregate_status"] == "FAIL_BLOCKER" and expected_failing_row in observed_failures
        report_rows.append(
            row(
                case_id,
                "PASS_SHAPE_ONLY" if passed else "FAIL_BLOCKER",
                "negative rendered-artifact mutation fails as expected",
                {
                    "expected_failing_row": expected_failing_row,
                    "observed_aggregate_status": negative_report["aggregate_status"],
                    "observed_failures": observed_failures,
                },
            )
        )
    aggregate_status = "FAIL_BLOCKER" if any(item["status"] == "FAIL_BLOCKER" for item in report_rows) else "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "negative_self_test": True,
        "phase_slug": phase_slug,
        "rows": report_rows,
        "validator_mode": "local_non_mutating_render_negative_self_test",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assert a rendered THOS reason dashboard artifact.")
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--html", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--self-test-negative", action="store_true")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        raise FileNotFoundError(args.html)
    preflight = read_json_object(Path(args.preflight))
    html_text = html_path.read_text(encoding="utf-8")
    if args.self_test_negative:
        report = self_test_negative(preflight, html_text, args.phase_slug)
    else:
        report = assert_render(preflight, html_text, args.phase_slug)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] == "PASS_SHAPE_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
