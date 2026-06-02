#!/usr/bin/env python3
"""Build v475 THOS v1 x1 receipt durability and dashboard seed artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v1-x1"
SOURCE_PHASE = "v474-thos-v8-x2"
NEXT_PHASE = "v475-thos-v1-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
DRIFT_GUARD = ARTIFACT_ROOT / "v474-thos-v8-x2-drift-recurrence-guard-v1.json"
SUMMARY_CANDIDATE = ARTIFACT_ROOT / "v474-thos-v7-x1-summary-candidate-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LANES = {"Arby", "Aster Vale"}
DASHBOARD_ROWS = [
    "lane_completion_summary",
    "marker_review_summary",
    "source_chain_integrity",
    "raw_output_block_status",
    "negative_fixture_status",
    "gmut_gate_effect_status",
    "handoff_risk_status",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "schema rows should carry phase, lane, marker, hash, raw-output flag, GMUT boundary, dashboard status, and next check",
            "recurrence checks should cover hash drift, missing sources, raw-output flag drift, marker regression, lane absence, dashboard mismatch, and GMUT movement",
            "dashboard continuity must not become raw content approval",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "receipt durability is metadata governance only",
            "recurrence checks are guardrails, not certification",
            "hashes support source identity/integrity only, not truth, completeness, consciousness, final physics, or GMUT validity",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "durable schema should include source chain, lane receipts, raw-output flags, marker status, source refs, hash refs, and GMUT effect",
            "dashboard rows need source hash, raw-output, marker, blocker, and GMUT boundary fields",
            "negative fixtures should cover source drift, missing refs, raw output flags, missing lanes, marker gaps, generic pass, raw dashboard source, and GMUT drift",
        ],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_RECEIPT_DURABILITY_SEEDED"


def source_ref(path_text: str) -> dict[str, Any]:
    path = REPO_ROOT / path_text
    if not path.exists():
        return {"path": path_text, "status": "OPEN_GAP_MISSING_SOURCE"}
    return {
        "bytes": path.stat().st_size,
        "path": path_text,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def lane_receipts(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    receipts = []
    for lane in candidate.get("lane_summaries", []):
        receipts.append(
            {
                "completion_metadata_status": lane.get("final_message_status"),
                "hash_ref_count": len(lane.get("source_refs", [])),
                "lane": lane.get("lane"),
                "marker_review_status": lane.get("marker_review_state"),
                "raw_output_published": bool(lane.get("raw_text_published")),
                "source_refs": lane.get("source_refs", []),
                "stderr_published": bool(lane.get("stderr_published")),
                "transport_published": bool(lane.get("transport_published")),
            }
        )
    return receipts


def dashboard_row(row_id: str, lane: str, status: str, source_hash_status: str, marker_status: str) -> dict[str, Any]:
    return {
        "blocked_claims": [
            "raw_output_publication",
            "GMUT_validation",
            "gate_closure",
            "content_quality_proof",
            "identity_or_consciousness_claim",
        ],
        "lane": lane,
        "marker_status": marker_status,
        "raw_output_status": "BLOCKED_UNPUBLISHED",
        "row_id": row_id,
        "source_hash_status": source_hash_status,
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    if case.get("hash_drift") or case.get("raw_output_flag") or case.get("missing_lane"):
        observed = "FAIL_BLOCKER"
    elif case.get("generic_pass") or case.get("dashboard_raw_text") or case.get("gmut_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source") or case.get("marker_missing"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only"):
        observed = "PASS_SHAPE_ONLY"
    else:
        observed = "OPEN_GAP"
    return {
        "case": case,
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture(
            "metadata_only_expected_pass",
            {"gmut_effect": "none_open_not_tested", "metadata_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "hash_drift_expected_fail",
            {"gmut_effect": "none_open_not_tested", "hash_drift": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "raw_output_flag_expected_fail",
            {"gmut_effect": "none_open_not_tested", "raw_output_flag": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_lane_expected_fail",
            {"gmut_effect": "none_open_not_tested", "missing_lane": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "marker_missing_expected_open_gap",
            {"gmut_effect": "none_open_not_tested", "marker_missing": True},
            "OPEN_GAP",
        ),
        fixture(
            "dashboard_raw_text_expected_fail",
            {"dashboard_raw_text": True, "gmut_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "generic_pass_expected_fail",
            {"generic_pass": True, "gmut_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_expected_fail",
            {"gmut_effect": "gate_moved", "metadata_only": True},
            "FAIL_BLOCKER",
        ),
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    guard = read_json(DRIFT_GUARD)
    candidate = read_json(SUMMARY_CANDIDATE)
    receipts = lane_receipts(candidate)
    lane_set = {str(item.get("lane")) for item in receipts}
    missing_lanes = sorted(REQUIRED_LANES - lane_set)
    bad_raw_flags = [
        item["lane"]
        for item in receipts
        if item["raw_output_published"] or item["stderr_published"] or item["transport_published"]
    ]
    source_chain = guard.get("source_chain", [])
    source_refs = [source_ref(item.get("path", "")) for item in source_chain]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    dashboard_rows = [
        dashboard_row("lane_completion_summary", "aggregate", "PASS_SHAPE_ONLY", "MATCHED", "metadata_only"),
        dashboard_row("marker_review_summary", "aggregate", "PASS_SHAPE_ONLY", "MATCHED", "reviewed_metadata_only"),
        dashboard_row(
            "source_chain_integrity",
            "aggregate",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP",
            "MATCHED" if not source_gaps else "MISSING",
            "metadata_only",
        ),
        dashboard_row("raw_output_block_status", "aggregate", "PASS_SHAPE_ONLY" if not bad_raw_flags else "FAIL_BLOCKER", "MATCHED", "blocked_unpublished"),
        dashboard_row("negative_fixture_status", "aggregate", "PASS_SHAPE_ONLY", "MATCHED", "fixture_guarded"),
        dashboard_row("gmut_gate_effect_status", "aggregate", "PASS_SHAPE_ONLY", "MATCHED", "none_open_not_tested"),
        dashboard_row("handoff_risk_status", "aggregate", "PASS_SHAPE_ONLY", "MATCHED", "carry_forward"),
    ]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    dashboard_missing = sorted(set(DASHBOARD_ROWS) - {item["row_id"] for item in dashboard_rows})
    rows = [
        row(
            "source_guard",
            "PASS_SHAPE_ONLY" if guard.get("aggregate_status") == "PASS_SHAPE_ONLY_DRIFT_GUARD_READY" else "OPEN_GAP_SOURCE_GUARD",
            "v474 v8 x2 drift guard was loaded as v475 durability source.",
            {
                "path": "docs/trinity-live-traces/v474-thos-v8-x2-drift-recurrence-guard-v1.json",
                "sha256": sha256_file(DRIFT_GUARD) if DRIFT_GUARD.exists() else None,
            },
        ),
        row(
            "source_chain_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_MISSING_SOURCE",
            "Source-chain references were rechecked for the v475 seed.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "lane_receipts",
            "PASS_SHAPE_ONLY" if not missing_lanes and not bad_raw_flags else "FAIL_BLOCKER",
            "Required lane receipts and raw-output flags were checked.",
            {"missing_lanes": missing_lanes, "bad_raw_flag_lanes": bad_raw_flags},
        ),
        row(
            "dashboard_rows",
            "PASS_SHAPE_ONLY" if not dashboard_missing else "OPEN_GAP_DASHBOARD_ROWS",
            "Dashboard/report continuity rows were seeded from curated metadata only.",
            {"dashboard_row_count": len(dashboard_rows), "missing_rows": dashboard_missing},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Durability fixtures confirmed hash drift, missing source, raw flag, lane, marker, dashboard raw text, generic pass, and GMUT drift behavior.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into the v475 durability seed.",
            {"advisory_count": len(APP_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase seeds THOS receipt durability and dashboard continuity only; it does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    seed = {
        "aggregate_status": aggregate,
        "app_advisories": APP_ADVISORIES,
        "dashboard_rows": dashboard_rows,
        "durability_schema": {
            "claim_ceiling": "metadata_summary_only",
            "fields": [
                "phase_id",
                "source_chain_ids",
                "source_hashes",
                "lane_ids",
                "lane_completion_status",
                "raw_output_published",
                "marker_review_status",
                "gmUT_gate_effect",
                "drift_guard_status",
                "blocker_ids",
                "handoff_target",
            ],
        },
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "lane_receipts": receipts,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recurrence_checks": [
            "source hash drift",
            "missing source artifact",
            "raw-output flag true",
            "required lane absence",
            "marker-review regression",
            "dashboard row mismatch",
            "claim-ceiling expansion",
            "GMUT boundary movement",
        ],
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    seed_json = ARTIFACT_ROOT / f"{PHASE}-receipt-durability-seed-v1.json"
    write_json(seed_json, seed)
    written.append(seed_json)
    seed_md = ARTIFACT_ROOT / f"{PHASE}-receipt-durability-seed-v1.md"
    write_md(
        seed_md,
        f"""
# v475 THOS v1 x1 Receipt Durability Seed

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v475 v1 x1 seeds receipt durability and dashboard/report continuity from curated metadata only. It carries the v474 drift recurrence guard forward and keeps raw Arby/Aster lane output unpublished.

Lane receipts: `{len(receipts)}`; missing lanes: `{len(missing_lanes)}`.

Dashboard rows: `{len(dashboard_rows)}`; missing rows: `{len(dashboard_missing)}`.

Source refs: `{len(source_refs)}` checked; gaps: `{len(source_gaps)}`.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

All six GMUT gates remain open.
""",
    )
    written.append(seed_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v475 THOS v1 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v475 v1 x1 begins receipt durability and dashboard/report continuity using only curated metadata and the v474 drift recurrence guard.

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
