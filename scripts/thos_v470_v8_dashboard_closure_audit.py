#!/usr/bin/env python3
"""Audit the v470 THOS v8 dashboard guard lane closure state."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_ARTIFACTS = [
    "docs/trinity-live-traces/v470-thos-v8-x4-renderer-preflight-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x4-renderer-input-map-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x5-reason-dashboard-render-v1.html",
    "docs/trinity-live-traces/v470-thos-v8-x5-rendered-artifact-check-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x5-renderer-design-brief-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x6-rendered-artifact-check-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x6-render-negative-self-test-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x6-visual-readiness-v1.json",
    "docs/trinity-live-traces/v470-thos-v8-x7-rendered-dashboard-contract-v1.json",
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


def row(row_id: str, status: str, message: str, evidence: object = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object")
    return payload


def build_audit(repo_root: Path, phase_slug: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    missing = [path for path in EXPECTED_ARTIFACTS if not (repo_root / path).exists()]
    rows.append(
        row(
            "expected_artifact_presence",
            "PASS_SHAPE_ONLY" if not missing else "FAIL_BLOCKER",
            "expected v8 x4-x7 dashboard artifacts are present",
            {"missing": missing, "expected_count": len(EXPECTED_ARTIFACTS)},
        )
    )
    json_failures: list[str] = []
    parsed: dict[str, dict[str, Any]] = {}
    for artifact in EXPECTED_ARTIFACTS:
        if not artifact.endswith(".json"):
            continue
        try:
            parsed[artifact] = read_json(repo_root / artifact)
        except Exception as exc:
            json_failures.append(f"{artifact}: {exc}")
    rows.append(
        row(
            "json_parse",
            "PASS_SHAPE_ONLY" if not json_failures else "FAIL_BLOCKER",
            "expected JSON artifacts parse as objects",
            {"json_failures": json_failures},
        )
    )
    status_mismatches = {
        artifact: payload.get("aggregate_status")
        for artifact, payload in parsed.items()
        if artifact.endswith(("renderer-preflight-v1.json", "rendered-artifact-check-v1.json", "render-negative-self-test-v1.json"))
        and payload.get("aggregate_status") != "PASS_SHAPE_ONLY"
    }
    rows.append(
        row(
            "green_assertion_chain",
            "PASS_SHAPE_ONLY" if not status_mismatches else "FAIL_BLOCKER",
            "preflight, rendered assertions, and negative self-test are green",
            {"status_mismatches": status_mismatches},
        )
    )
    visual = parsed.get("docs/trinity-live-traces/v470-thos-v8-x6-visual-readiness-v1.json", {})
    contract = parsed.get("docs/trinity-live-traces/v470-thos-v8-x7-rendered-dashboard-contract-v1.json", {})
    rows.append(
        row(
            "browser_visual_gap",
            "OPEN_GAP" if visual.get("browser_tool_status") == "not_exposed" else "PASS_SHAPE_ONLY",
            "browser visual inspection status is explicitly classified",
            {
                "browser_tool_status": visual.get("browser_tool_status"),
                "visual_readiness_status": visual.get("visual_readiness_status"),
            },
        )
    )
    rows.append(
        row(
            "dashboard_contract_gap",
            "OPEN_GAP" if contract.get("aggregate_status") == "OPEN_GAP" else "PASS_SHAPE_ONLY",
            "dashboard contract carries browser gap without blocking local artifact chain",
            {"contract_aggregate_status": contract.get("aggregate_status")},
        )
    )
    claim_hits: list[str] = []
    for artifact in EXPECTED_ARTIFACTS:
        text = (repo_root / artifact).read_text(encoding="utf-8")
        match = FORBIDDEN_CLAIM_RE.search(text)
        if match:
            claim_hits.append(f"{artifact}: {match.group(0)}")
    rows.append(
        row(
            "forbidden_claim_guard",
            "PASS_SHAPE_ONLY" if not claim_hits else "FAIL_BLOCKER",
            "dashboard lane artifacts avoid forbidden claim wording",
            {"claim_hits": claim_hits},
        )
    )
    rows.append(
        row(
            "gmut_gate_status",
            "OPEN_GAP",
            "all six GMUT gates remain open and are not moved by this THOS lane",
            {
                "null_recovery": "open",
                "dimensional_si_consistency": "open",
                "conservation_or_exchange_law": "open",
                "baseline_recovery": "open",
                "fifth_force_equivalence_constraints": "open",
                "consciousness_measurement_bridge": "open",
            },
        )
    )
    statuses = [item["status"] for item in rows]
    if "FAIL_BLOCKER" in statuses:
        aggregate_status = "FAIL_BLOCKER"
    elif "OPEN_GAP" in statuses:
        aggregate_status = "OPEN_GAP"
    else:
        aggregate_status = "PASS_SHAPE_ONLY"
    return {
        "aggregate_status": aggregate_status,
        "connector_write_performed": False,
        "expected_artifacts": EXPECTED_ARTIFACTS,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": phase_slug,
        "rows": rows,
        "validator_mode": "local_non_mutating_v470_v8_closure_audit",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit v470 THOS v8 dashboard guard lane closure.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_audit(Path.cwd(), args.phase_slug)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_status"] in {"PASS_SHAPE_ONLY", "OPEN_GAP"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
