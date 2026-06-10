#!/usr/bin/env python3
"""Textual visual-readiness checks for a local THOS reason dashboard artifact."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_TEXT_MARKERS = [
    "THOS Reason Dashboard",
    "Local non-mutating renderer",
    "Dashboard summary",
    "Reason dashboard rows",
    "Reason-code guard rows",
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
REQUIRED_STRUCTURE_MARKERS = [
    '<meta name="viewport"',
    "<main ",
    "<header>",
    "<section aria-label=",
    "<table>",
    "<caption>",
    "<thead>",
    "<tbody>",
    'id="thos-render-data"',
]
REQUIRED_STYLE_MARKERS = [
    "overflow-x: auto",
    "grid-template-columns: repeat(auto-fit",
    "position: sticky",
    "font-size: clamp",
]
FORBIDDEN_CLAIM_RE = re.compile(
    r"(GMUT\s+validated|GMUT\s+validation\s+complete|"
    r"all\s+six\s+GMUT\s+gates\s+(?:closed|passed)|all\s+gates\s+closed|"
    r"final\s+physics\s+(?:complete|validated|solved)|consciousness\s+solved|"
    r"empirical\s+spiritual\s+proof\s+achieved|fifth[- ]force\s+safety\s+confirmed|"
    r"canon\s+promoted|cleanup\s+completed\s+successfully|"
    r"connector\s+write\s+completed\s+successfully|cloud\s+mutation\s+completed\s+successfully)",
    re.IGNORECASE,
)


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def row(row_id: str, status: str, message: str, evidence: object = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def build_report(preflight: dict[str, Any], html_text: str, phase_slug: str, browser_tool_status: str) -> dict[str, Any]:
    renderer_rows = preflight.get("renderer_rows")
    if not isinstance(renderer_rows, list):
        renderer_rows = []
    clean_rows = [item for item in renderer_rows if isinstance(item, dict)]
    declared_count_match = re.search(r'data-case-count="(\d+)"', html_text)
    declared_count = int(declared_count_match.group(1)) if declared_count_match else None
    rendered_rows = len(re.findall(r"<tr data-case-id=", html_text))
    missing_text = [marker for marker in REQUIRED_TEXT_MARKERS if marker not in html_text]
    missing_structure = [marker for marker in REQUIRED_STRUCTURE_MARKERS if marker not in html_text]
    missing_style = [marker for marker in REQUIRED_STYLE_MARKERS if marker not in html_text]
    forbidden_claims = sorted({match.group(0) for match in FORBIDDEN_CLAIM_RE.finditer(html_text)})
    report_rows = [
        row(
            "browser_tool_status",
            "OPEN_GAP" if browser_tool_status == "not_exposed" else "PASS_SHAPE_ONLY",
            "browser screenshot tooling status recorded",
            browser_tool_status,
        ),
        row(
            "case_count_parity",
            "PASS_SHAPE_ONLY" if declared_count == rendered_rows == len(clean_rows) else "FAIL_BLOCKER",
            "declared, rendered, and preflight row counts agree",
            {
                "declared_case_count": declared_count,
                "preflight_row_count": len(clean_rows),
                "rendered_row_count": rendered_rows,
            },
        ),
        row(
            "required_text_markers",
            "PASS_SHAPE_ONLY" if not missing_text else "FAIL_BLOCKER",
            "required visible text markers are present",
            {"missing_text_markers": missing_text},
        ),
        row(
            "required_structure_markers",
            "PASS_SHAPE_ONLY" if not missing_structure else "FAIL_BLOCKER",
            "required HTML structure markers are present",
            {"missing_structure_markers": missing_structure},
        ),
        row(
            "required_style_markers",
            "PASS_SHAPE_ONLY" if not missing_style else "FAIL_BLOCKER",
            "basic responsive table style markers are present",
            {"missing_style_markers": missing_style},
        ),
        row(
            "forbidden_claim_guard",
            "PASS_SHAPE_ONLY" if not forbidden_claims else "FAIL_BLOCKER",
            "visual readiness artifact avoids forbidden claim wording",
            {"forbidden_claims": forbidden_claims},
        ),
    ]
    statuses = [item["status"] for item in report_rows]
    if "FAIL_BLOCKER" in statuses:
        aggregate_status = "FAIL_BLOCKER"
    elif "OPEN_GAP" in statuses:
        aggregate_status = "OPEN_GAP"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "browser_tool_status": browser_tool_status,
        "connector_write_performed": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rendered_artifact_mode": "local_static_html_textual_readiness_only",
        "rows": report_rows,
        "validator_mode": "local_non_mutating_visual_readiness",
        "visual_readiness_status": "PASS_TEXTUAL_READINESS_WITH_BROWSER_OPEN_GAP"
        if browser_tool_status == "not_exposed"
        else "PASS_TEXTUAL_READINESS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check textual visual readiness for a THOS HTML dashboard.")
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--html", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--browser-tool-status", default="not_exposed", choices=["not_exposed", "available_not_used", "used"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    html_path = Path(args.html)
    report = build_report(
        read_json_object(Path(args.preflight)),
        html_path.read_text(encoding="utf-8"),
        args.phase_slug,
        args.browser_tool_status,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
