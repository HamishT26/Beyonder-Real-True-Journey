#!/usr/bin/env python3
"""Build v475 THOS v2 x2 dashboard sync aggregation artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v2-x2"
SOURCE_PHASE = "v475-thos-v2-x1"
NEXT_PHASE = "v475-thos-v3-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

CONTRACT = ARTIFACT_ROOT / "v475-thos-v2-x1-dashboard-sync-contract-v1.json"
CONTRACT_STATUS = ARTIFACT_ROOT / "v475-thos-v2-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LANES = {"Arby", "Aster Vale"}
ALLOWED_DASHBOARD_LABELS = {"metadata_status_only"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(path: Path) -> dict[str, Any]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {"path": rel, "status": "OPEN_GAP_MISSING_SOURCE"}
    return {
        "bytes": path.stat().st_size,
        "path": rel,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("raw_output_published") or case.get("transport_published"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_hash_drift") or case.get("dashboard_count_mismatch"):
        observed = "FAIL_BLOCKER"
    elif case.get("summary_ready") and case.get("marker_review_status") not in {
        "metadata_only",
        "reviewed_metadata_only",
    }:
        observed = "FAIL_BLOCKER"
    elif case.get("summary_ready") and case.get("missing_required_lane"):
        observed = "FAIL_BLOCKER"
    elif case.get("dashboard_label") not in ALLOWED_DASHBOARD_LABELS:
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source") or case.get("stale_notice"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only") and case.get("source_hash_match") and not case.get("missing_required_lane"):
        observed = "PASS_SHAPE_ONLY"
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
            "metadata_dashboard_sync_expected_pass",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "metadata_only": True,
                "source_hash_match": True,
            },
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "dashboard_count_mismatch_expected_fail",
            {
                "dashboard_count_mismatch": True,
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_hash_drift_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "source_hash_drift": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "marker_pending_summary_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "marker_review_status": "open_gap",
                "summary_ready": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_required_lane_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "missing_required_lane": True,
                "summary_ready": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_published_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "raw_output_published": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "transport_published_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "transport_published": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "stale_notice_expected_open_gap",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "stale_notice": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "none_open_not_tested",
                "missing_source": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "pressure_label_expected_fail",
            {
                "dashboard_label": "certified",
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_moved_expected_fail",
            {
                "dashboard_label": "metadata_status_only",
                "gmut_gate_effect": "gate_moved",
                "metadata_only": True,
            },
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_lane_rows(contract: dict[str, Any]) -> dict[str, Any]:
    lane_rows = [
        item
        for item in contract.get("dashboard_rows", [])
        if item.get("lane") in REQUIRED_LANES
    ]
    lane_names = {str(item.get("lane")) for item in lane_rows}
    missing_lanes = sorted(REQUIRED_LANES - lane_names)
    raw_flag_rows = [
        item.get("lane")
        for item in lane_rows
        if item.get("raw_output_published") or item.get("transport_published")
    ]
    bad_labels = [
        item.get("lane")
        for item in lane_rows
        if item.get("dashboard_label") not in ALLOWED_DASHBOARD_LABELS
    ]
    source_hash_ref_gaps = [
        item.get("lane")
        for item in lane_rows
        if not item.get("source_hash_refs")
    ]
    return {
        "bad_labels": bad_labels,
        "lane_count": len(lane_rows),
        "lane_names": sorted(lane_names),
        "missing_lanes": missing_lanes,
        "raw_flag_rows": raw_flag_rows,
        "source_hash_ref_gaps": source_hash_ref_gaps,
    }


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_DASHBOARD_SYNC_AGGREGATOR_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    contract = read_json(CONTRACT)
    contract_status = read_json(CONTRACT_STATUS)
    source_refs = [source_ref(CONTRACT), source_ref(CONTRACT_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    lane_aggregate = aggregate_lane_rows(contract)
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    dashboard_count_mismatch = lane_aggregate["lane_count"] != 2
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v2 x1 contract sources were checked for x2 aggregation.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "lane_count_reconciliation",
            "PASS_SHAPE_ONLY" if not dashboard_count_mismatch else "FAIL_DASHBOARD_COUNT_MISMATCH",
            "Dashboard lane count was reconciled against required Arby/Aster rows.",
            lane_aggregate,
        ),
        row(
            "raw_output_reconciliation",
            "PASS_SHAPE_ONLY" if not lane_aggregate["raw_flag_rows"] else "FAIL_RAW_OUTPUT_FLAG",
            "Raw-output and transport publication flags remain false for lane rows.",
            {"flagged_lanes": lane_aggregate["raw_flag_rows"]},
        ),
        row(
            "source_hash_refs",
            "PASS_SHAPE_ONLY" if not lane_aggregate["source_hash_ref_gaps"] else "OPEN_GAP_SOURCE_HASH_REFS",
            "Lane rows include source-hash references for metadata integrity only.",
            {"gaps": lane_aggregate["source_hash_ref_gaps"]},
        ),
        row(
            "label_policy",
            "PASS_SHAPE_ONLY" if not lane_aggregate["bad_labels"] else "FAIL_LABEL_POLICY",
            "Dashboard labels remain metadata-status only.",
            {"bad_label_lanes": lane_aggregate["bad_labels"], "allowed_labels": sorted(ALLOWED_DASHBOARD_LABELS)},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Aggregator fixtures checked count mismatch, hash drift, marker pending, lane absence, raw output, stale notice, source gap, label drift, and GMUT boundary.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This aggregator is THOS dashboard metadata only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "contract_run_status": contract_status.get("run_status"),
        "dashboard_aggregation": lane_aggregate,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "v3_x1_handoff": {
            "recommended_scope": "derive a concise dashboard-ready report board from the v2 sync contract and aggregator",
            "required_boundaries": [
                "metadata-only lane rows",
                "raw-output and transport flags false",
                "source-hash refs used only for artifact integrity",
                "stale or missing notices remain open gaps",
                "count/hash/raw/label/GMUT drift remain blockers",
            ],
        },
    }

    artifact_json = ARTIFACT_ROOT / f"{PHASE}-dashboard-sync-aggregator-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-dashboard-sync-aggregator-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v2 x2 Dashboard Sync Aggregator

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v2 x2 aggregates the dashboard sync contract into lane-count, raw-output, source-hash, label-policy, fixture, and handoff checks.

Required lane rows: `{lane_aggregate["lane_count"]}`; missing lanes: `{len(lane_aggregate["missing_lanes"])}`.

Source refs: `{len(source_refs)}` checked; gaps: `{len(source_gaps)}`.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Next expected phase: `{NEXT_PHASE}`.

All six GMUT gates remain open.
""",
    )
    run_payload = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "published_artifacts": [artifact_json.relative_to(REPO_ROOT).as_posix(), artifact_md.relative_to(REPO_ROOT).as_posix()],
        "run_status": status,
        "validation": [
            "source refs checked",
            "lane count reconciled",
            "raw-output flags checked",
            "source-hash refs checked",
            "dashboard label policy checked",
            "negative fixtures checked",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v2 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v2 x2 aggregates dashboard sync contract checks and prepares the v3 x1 report-board handoff.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
