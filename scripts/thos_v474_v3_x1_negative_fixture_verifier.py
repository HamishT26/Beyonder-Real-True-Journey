#!/usr/bin/env python3
"""Verify v474 THOS receipt-classifier hardening with executable negative fixtures."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v3-x1"
SOURCE_PHASE = "v474-thos-v2-x2"
NEXT_PHASE = "v474-thos-v3-x2"
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

STATUS_PRECEDENCE = [
    "FAIL_BLOCKER",
    "REVIEW_REQUIRED",
    "OPEN_GAP",
    "PASS_SHAPE_ONLY",
    "NOT_RUN",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def derive_status(receipt: dict[str, Any]) -> tuple[str, str]:
    if receipt.get("raw_text_published") is True:
        return "FAIL_BLOCKER", "raw text was marked as published"
    if receipt.get("hard_credential_marker") is True:
        return "FAIL_BLOCKER", "hard credential marker is present"
    if receipt.get("gmUT_gate_effect") != "none_open_not_tested":
        return "FAIL_BLOCKER", "GMUT gate effect drift is present"
    if receipt.get("malformed_json") is True:
        return "FAIL_BLOCKER", "receipt metadata is malformed"
    if receipt.get("duplicate_receipt_id") is True:
        return "FAIL_BLOCKER", "duplicate receipt id is present"
    if receipt.get("lane_run_mismatch") is True:
        return "FAIL_BLOCKER", "lane/run mismatch is present"
    if receipt.get("derived_status") == "PASS":
        return "FAIL_BLOCKER", "generic PASS is not a deterministic derived status"
    if receipt.get("summary_ready") is True and receipt.get("marker_review_status") != "passed":
        return "FAIL_BLOCKER", "summary readiness contradicts missing marker-review pass"
    if receipt.get("credential_like_marker") is True:
        return "REVIEW_REQUIRED", "credential-like marker needs marker review"
    if receipt.get("final_message_status") != "ready":
        return "OPEN_GAP", "final message is missing or not ready"
    if receipt.get("marker_review_status") != "passed":
        return "OPEN_GAP", "marker review has not passed"
    if receipt.get("redaction_status") != "confirmed":
        return "OPEN_GAP", "redaction metadata is incomplete"
    if receipt.get("planned_only") is True:
        return "NOT_RUN", "receipt is planned only"
    return "PASS_SHAPE_ONLY", "receipt metadata is summary-ready and bounded"


def fixture(case_id: str, expected: str, **overrides: Any) -> dict[str, Any]:
    base = {
        "blocked_claims": ["gmUT_validation", "final_physics", "consciousness_proof"],
        "derived_status": "UNSET",
        "final_message_status": "ready",
        "gmUT_gate_effect": "none_open_not_tested",
        "lane": "fixture_lane",
        "marker_review_status": "passed",
        "phase_ref": PHASE,
        "raw_text_published": False,
        "receipt_id": case_id,
        "redaction_status": "confirmed",
        "run_id": f"{case_id}-run",
        "source_artifact_ref": "<repo_artifact_ref>",
        "summary_ready": False,
    }
    base.update(overrides)
    observed, reason = derive_status(base)
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "reason": reason,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("raw_text_published", "FAIL_BLOCKER", raw_text_published=True),
        fixture("hard_credential_marker", "FAIL_BLOCKER", hard_credential_marker=True),
        fixture("credential_like_review_required", "REVIEW_REQUIRED", credential_like_marker=True),
        fixture("missing_final_message", "OPEN_GAP", final_message_status="missing"),
        fixture("missing_marker_review", "OPEN_GAP", marker_review_status="pending"),
        fixture("generic_pass_without_derivation", "FAIL_BLOCKER", derived_status="PASS"),
        fixture("gmUT_gate_effect_drift", "FAIL_BLOCKER", gmUT_gate_effect="claimed_closed"),
        fixture("malformed_json", "FAIL_BLOCKER", malformed_json=True),
        fixture("duplicate_receipt_id", "FAIL_BLOCKER", duplicate_receipt_id=True),
        fixture("lane_run_mismatch", "FAIL_BLOCKER", lane_run_mismatch=True),
        fixture("summary_ready_contradicts_open_gap", "FAIL_BLOCKER", marker_review_status="pending", summary_ready=True),
        fixture("clean_summary_ready", "PASS_SHAPE_ONLY"),
    ]


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    hardening = read_json(ARTIFACT_ROOT / f"{SOURCE_PHASE}-classifier-hardening-v1.json")
    fixtures = build_fixtures()
    mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    verifier_status = "PASS_SHAPE_ONLY" if not mismatches else "FAIL_BLOCKER"
    rows = [
        row(
            "source_hardening",
            "PASS_SHAPE_ONLY" if hardening else "OPEN_GAP_SOURCE_HARDENING_MISSING",
            "v2 x2 hardening artifact is available.",
            {"source_status": hardening.get("aggregate_status", "MISSING")},
        ),
        row(
            "negative_fixtures",
            verifier_status,
            "Executable negative fixtures were evaluated.",
            {"fixture_count": len(fixtures), "mismatch_count": len(mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Verifier checks THOS receipt metadata only; it does not test or close GMUT gates.",
        ),
    ]
    verifier = {
        "aggregate_status": "OPEN_GAP" if any(item["status"].startswith("OPEN_GAP") for item in rows) else verifier_status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "status_precedence": STATUS_PRECEDENCE,
    }
    run_status = {
        "aggregate_status": verifier["aggregate_status"],
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    verifier_json = ARTIFACT_ROOT / f"{PHASE}-negative-fixture-verifier-v1.json"
    write_json(verifier_json, verifier)
    written.append(verifier_json)
    verifier_md = ARTIFACT_ROOT / f"{PHASE}-negative-fixture-verifier-v1.md"
    write_md(
        verifier_md,
        f"""
# v474 THOS v3 x1 Negative Fixture Verifier

Generated UTC: `{generated_at}`

Status: `{verifier['aggregate_status']}`

Executable fixture results: `{len(fixtures) - len(mismatches)}` confirmed, `{len(mismatches)}` mismatched.

The verifier blocks raw-output publication, hard credential markers, generic PASS states, GMUT gate-effect drift, duplicate receipt IDs, lane/run mismatches, and summary-ready contradictions.

All six GMUT gates remain open.
""",
    )
    written.append(verifier_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v3 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v3 x1 implements executable negative-fixture checks for the v2 x2 classifier hardening map.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    for path in build_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
