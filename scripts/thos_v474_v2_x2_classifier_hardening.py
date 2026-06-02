#!/usr/bin/env python3
"""Build v474 THOS v2 x2 classifier hardening synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v2-x2"
SOURCE_PHASE = "v474-thos-v2-x1"
NEXT_PHASE = "v474-thos-v3-x1"
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

APP_HARDENING_INPUTS = [
    {
        "lane": "Cicero",
        "received": True,
        "hardening_points": [
            "avoid complete unless marker-reviewed curated receipt is ready",
            "process exit without final message is not success",
            "unresolved credential-like marker is not success",
            "retry loops require bounded reason codes",
            "THOS runtime success must not imply GMUT validation",
        ],
    },
    {
        "lane": "Kierkegaard",
        "received": True,
        "hardening_points": [
            "classify durable artifacts, not raw temp lane text",
            "wait while lane is healthy; retry only transport or malformed invocation",
            "carry open gap for privacy hold or incomplete marker review",
            "do not retry for tone preference",
            "classifier improves publication hygiene only",
        ],
    },
    {
        "lane": "Aristotle",
        "received": True,
        "hardening_points": [
            "add receipt_id and source_artifact_ref",
            "deterministic precedence must be reproducible",
            "raw text publication is a fail blocker",
            "include negative fixtures for duplicates and contradictions",
            "exact staging must remain repo-only and summary-only",
        ],
    },
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


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    classifier = read_json(ARTIFACT_ROOT / f"{SOURCE_PHASE}-receipt-classifier-v1.json")
    classifier_status = classifier.get("aggregate_status", "MISSING")
    lane_count = len(classifier.get("lane_classifications", []))

    hardening_schema = {
        "required_receipt_fields": [
            "receipt_id",
            "phase_ref",
            "lane",
            "run_id",
            "source_artifact_ref",
            "raw_text_published",
            "marker_review_status",
            "final_message_status",
            "exit_status",
            "redaction_status",
            "summary_ready",
            "blocked_claims",
            "derived_status",
            "gmUT_gate_effect",
        ],
        "status_precedence": [
            "FAIL_BLOCKER",
            "REVIEW_REQUIRED",
            "OPEN_GAP",
            "PASS_SHAPE_ONLY",
            "NOT_RUN",
        ],
        "retry_reason_codes": [
            "transport_timeout",
            "no_final_message",
            "wrapper_exit_mismatch",
            "marker_review_blocked",
            "stale_process_state",
            "operator_requested_retry",
            "malformed_invocation",
        ],
    }
    negative_fixtures = [
        "raw_text_published",
        "hard_credential_marker",
        "credential_like_review_required",
        "missing_final_message",
        "missing_marker_review",
        "generic_pass_without_derivation",
        "gmUT_gate_effect_drift",
        "malformed_json",
        "duplicate_receipt_id",
        "lane_run_mismatch",
        "summary_ready_contradicts_open_gap",
    ]
    rows = [
        row(
            "source_classifier",
            "PASS_SHAPE_ONLY" if classifier else "OPEN_GAP_SOURCE_CLASSIFIER_MISSING",
            "v2 x1 classifier artifact is present and can be hardened.",
            {"classifier_status": classifier_status, "lane_count": lane_count},
        ),
        row(
            "app_hardening_inputs",
            "PASS_SHAPE_ONLY",
            "Three app advisories returned and are distilled into classifier hardening points.",
            {"advisory_count": len(APP_HARDENING_INPUTS)},
        ),
        row(
            "negative_fixtures",
            "OPEN_GAP_IMPLEMENTATION_PENDING",
            "Negative fixture list is specified but not yet implemented as an executable verifier.",
            {"fixture_count": len(negative_fixtures)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Classifier hardening affects THOS publication hygiene only; GMUT gates remain open.",
        ),
    ]
    synthesis = {
        "aggregate_status": "OPEN_GAP",
        "app_hardening_inputs": APP_HARDENING_INPUTS,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "hardening_schema": hardening_schema,
        "negative_fixtures_to_implement": negative_fixtures,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_v3_x1_tasks": [
            "Implement executable negative-fixture verifier for the hardening schema.",
            "Add receipt_id/source_artifact_ref derivation without exposing raw temp paths.",
            "Split REVIEW_REQUIRED from OPEN_GAP in classifier output.",
            "Add a publication guard that fails on generic PASS or GMUT gate-effect drift.",
        ],
        "rows": rows,
        "source_classifier_status": classifier_status,
        "source_phase": SOURCE_PHASE,
    }
    run_status = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    synthesis_json = ARTIFACT_ROOT / f"{PHASE}-classifier-hardening-v1.json"
    write_json(synthesis_json, synthesis)
    written.append(synthesis_json)
    synthesis_md = ARTIFACT_ROOT / f"{PHASE}-classifier-hardening-v1.md"
    write_md(
        synthesis_md,
        f"""
# v474 THOS v2 x2 Classifier Hardening

Generated UTC: `{generated_at}`

Status: `OPEN_GAP`

v2 x2 incorporates Cicero, Kierkegaard, and Aristotle advisories into a harder receipt-classifier plan: stronger required fields, deterministic status precedence, bounded retry reason codes, and explicit negative fixtures.

Implementation remains pending for `v474-thos-v3-x1`.

All six GMUT gates remain open.
""",
    )
    written.append(synthesis_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v2 x2 Run Status

Status: `OPEN_GAP`

Next expected phase: `{NEXT_PHASE}`

v2 x2 turns the app advisories into a concrete hardening map. The executable negative-fixture verifier is intentionally deferred to v3 x1.

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
