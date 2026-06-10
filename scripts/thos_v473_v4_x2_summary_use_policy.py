#!/usr/bin/env python3
"""Build v473 THOS v4 x2 summary-use policy artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v473-thos-v4-x2"
NEXT_PHASE = "v473-thos-v5-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def lane_decision(review: dict[str, Any]) -> dict[str, Any]:
    status = review.get("review_status")
    if status == "PASS_NO_MARKER":
        action = "ALLOW_METADATA_SUMMARY"
        gate_status = "PASS_SHAPE_ONLY"
    elif status == "OPEN_GAP_MARKER_REVIEW_REQUIRED":
        action = "HOLD_RAW_TEXT_AND_SUMMARY"
        gate_status = "OPEN_GAP"
    else:
        action = "HOLD_PENDING_COMPLETION"
        gate_status = "OPEN_GAP"
    return {
        "action": action,
        "final_message_hash": review.get("final_message_hash"),
        "gate_status": gate_status,
        "lane": review.get("lane"),
        "marker_count": review.get("marker_count"),
        "raw_output_boundary": review.get("raw_output_boundary"),
        "review_status": status,
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    marker_review = read_json("v473-thos-v4-x1-receipt-marker-review-v1.json")
    app_cli = read_json("v473-thos-v4-x1-app-cli-integration-ledger-v1.json")
    decisions = [lane_decision(review) for review in marker_review.get("lane_reviews", [])]
    held_lanes = [item["lane"] for item in decisions if item["action"] != "ALLOW_METADATA_SUMMARY"]
    allowed_lanes = [item["lane"] for item in decisions if item["action"] == "ALLOW_METADATA_SUMMARY"]

    policy_rows = [
        row(
            "policy_defined",
            "PASS_SHAPE_ONLY",
            "Summary-use policy is defined over receipt-level review decisions only.",
            {"decision_count": len(decisions)},
        ),
        row(
            "allowed_lanes",
            "PASS_SHAPE_ONLY",
            "Lanes with no receipt marker count may be summarized from metadata only.",
            {"lanes": allowed_lanes},
        ),
        row(
            "held_lanes",
            "OPEN_GAP" if held_lanes else "PASS_SHAPE_ONLY",
            "Lanes with marker review still open remain held for raw-text and advisory-summary use.",
            {"lanes": held_lanes},
        ),
        row(
            "raw_boundary",
            "PASS_SHAPE_ONLY",
            "No raw final advisory body is used or published by this policy.",
        ),
    ]
    policy = {
        "aggregate_status": aggregate(policy_rows),
        "decisions": decisions,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "policy_rules": [
            "PASS_NO_MARKER permits metadata-only summary.",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED holds raw text and advisory summary.",
            "OPEN_GAP_FINAL_MESSAGE_PENDING holds all summary use.",
            "No THOS receipt can validate GMUT physics claims.",
        ],
        "rows": policy_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-summary-use-policy-v1.json"
    write_json(path, policy)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-summary-use-policy-v1.md",
        f"""
# v473 THOS v4 x2 Summary-Use Policy

Generated UTC: `{generated_at}`

Status: `{policy['aggregate_status']}`

Allowed metadata-only lanes: `{', '.join(allowed_lanes) if allowed_lanes else 'none'}`

Held lanes: `{', '.join(held_lanes) if held_lanes else 'none'}`

Raw final advisory text remains unpublished.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-summary-use-policy-v1.md")

    verifier_rows = [
        row("metadata_source", marker_review.get("aggregate_status", "OPEN_GAP"), "Verifier input is the v4 x1 receipt-level review artifact."),
        row("app_payloads", "OPEN_GAP", "App-lane payloads remain unavailable and are not used."),
        row("decision_policy", policy["aggregate_status"], "Policy decisions are generated for every lane review row."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "Policy does not affect GMUT gate status."),
    ]
    verifier = {
        "aggregate_status": aggregate(verifier_rows),
        "app_cli_status": app_cli.get("aggregate_status"),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": verifier_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-summary-use-verifier-v1.json"
    write_json(path, verifier)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-summary-use-verifier-v1.md",
        """
# v473 THOS v4 x2 Summary-Use Verifier

The verifier applies the summary-use policy to receipt-level marker-review rows only. App-lane payloads are still open and not claimed.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-summary-use-verifier-v1.md")

    handoff_rows = [
        row("policy", policy["aggregate_status"], "Summary-use policy is ready for v5 wrapper cycle reuse."),
        row("verifier", verifier["aggregate_status"], "Verifier carries app-lane payloads as open."),
        row("claim_boundary", "PASS_SHAPE_ONLY", "All six GMUT gates remain open."),
    ]
    handoff = {
        "aggregate_status": aggregate(handoff_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Launch v5 x1 with wrapper-backed Arby/Aster lanes and apply summary-use policy after receipt.",
            "Use metadata-only summaries for allowed lanes; keep held lanes unpublished until separately reviewed.",
            "Record any returned app-lane payloads as advisory-only in a later integration artifact.",
            "Keep THOS workflow reliability separate from GMUT validation claims.",
        ],
        "rows": handoff_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v5-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v5-handoff-v1.md",
        f"""
# v473 THOS v4 x2 to v5 Handoff

Status: `{handoff['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v5 should reuse the wrapper-backed lane cycle and apply the summary-use policy after the receipt lands.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v5-handoff-v1.md")

    status_rows = [
        row("policy", policy["aggregate_status"], "Summary-use policy published."),
        row("verifier", verifier["aggregate_status"], "Summary-use verifier published."),
        row("handoff", handoff["aggregate_status"], "v5 handoff published."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v473 THOS v4 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v4 x2 publishes summary-use policy for wrapper completion receipts.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
