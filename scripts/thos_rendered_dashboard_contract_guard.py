#!/usr/bin/env python3
"""Guard a THOS rendered-dashboard artifact bundle as one contract."""

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


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def row(row_id: str, status: str, message: str, evidence: object = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def row_statuses(payload: dict[str, Any]) -> list[str]:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        return []
    return [item.get("status") for item in rows if isinstance(item, dict) and isinstance(item.get("status"), str)]


def build_contract(
    html_text: str,
    rendered_assertion: dict[str, Any],
    negative_self_test: dict[str, Any],
    visual_readiness: dict[str, Any],
    phase_slug: str,
    require_browser_visual: bool,
) -> dict[str, Any]:
    visual_status = visual_readiness.get("aggregate_status")
    browser_tool_status = visual_readiness.get("browser_tool_status")
    report_rows = [
        row(
            "rendered_assertion_required",
            "PASS_SHAPE_ONLY" if rendered_assertion.get("aggregate_status") == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
            "rendered artifact assertion is present and green",
            {
                "aggregate_status": rendered_assertion.get("aggregate_status"),
                "row_statuses": row_statuses(rendered_assertion),
            },
        ),
        row(
            "negative_self_test_required",
            "PASS_SHAPE_ONLY" if negative_self_test.get("aggregate_status") == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER",
            "negative rendered-artifact self-test is present and green",
            {
                "aggregate_status": negative_self_test.get("aggregate_status"),
                "negative_self_test": negative_self_test.get("negative_self_test"),
                "row_statuses": row_statuses(negative_self_test),
            },
        ),
        row(
            "visual_readiness_required",
            "PASS_SHAPE_ONLY" if visual_status in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else "FAIL_BLOCKER",
            "visual readiness artifact is present and non-blocking",
            {
                "aggregate_status": visual_status,
                "browser_tool_status": browser_tool_status,
                "row_statuses": row_statuses(visual_readiness),
            },
        ),
        row(
            "browser_visual_requirement",
            "FAIL_BLOCKER" if require_browser_visual and browser_tool_status != "used" else "OPEN_GAP"
            if browser_tool_status == "not_exposed"
            else "PASS_SHAPE_ONLY",
            "browser visual inspection requirement status is explicit",
            {
                "browser_tool_status": browser_tool_status,
                "require_browser_visual": require_browser_visual,
            },
        ),
        row(
            "html_artifact_required",
            "PASS_SHAPE_ONLY" if "THOS Reason Dashboard" in html_text and '<main data-phase-slug=' in html_text else "FAIL_BLOCKER",
            "rendered HTML artifact contains the expected dashboard shell",
            {"html_length": len(html_text)},
        ),
        row(
            "forbidden_claim_guard",
            "PASS_SHAPE_ONLY" if not FORBIDDEN_CLAIM_RE.search(html_text) else "FAIL_BLOCKER",
            "rendered dashboard bundle avoids forbidden claim wording",
        ),
        row(
            "credential_shape_guard",
            "PASS_SHAPE_ONLY" if not SECRET_RE.search(html_text) else "FAIL_BLOCKER",
            "rendered dashboard bundle avoids credential-shaped content",
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
        "connector_write_performed": False,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rendered_dashboard_contract": "v1",
        "require_browser_visual": require_browser_visual,
        "rows": report_rows,
        "validator_mode": "local_non_mutating_rendered_dashboard_contract",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Guard a rendered THOS dashboard artifact bundle.")
    parser.add_argument("--html", required=True)
    parser.add_argument("--rendered-assertion", required=True)
    parser.add_argument("--negative-self-test", required=True)
    parser.add_argument("--visual-readiness", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--require-browser-visual", action="store_true")
    args = parser.parse_args()

    report = build_contract(
        Path(args.html).read_text(encoding="utf-8"),
        read_json_object(Path(args.rendered_assertion)),
        read_json_object(Path(args.negative_self_test)),
        read_json_object(Path(args.visual_readiness)),
        args.phase_slug,
        args.require_browser_visual,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
