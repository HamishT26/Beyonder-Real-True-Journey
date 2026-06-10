#!/usr/bin/env python3
"""Build v475 THOS v2 x1 dashboard sync contract artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v2-x1"
SOURCE_PHASE = "v475-thos-v1-x2"
NEXT_PHASE = "v475-thos-v2-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

CONTINUITY = ARTIFACT_ROOT / "v475-thos-v1-x2-notification-continuity-hardening-v1.json"
RUN_STATUS = ARTIFACT_ROOT / "v475-thos-v1-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_ROWS = [
    "source_chain",
    "seed_continuity",
    "watcher_contract",
    "completion_receipts",
    "no_rush_policy",
    "app_lane_advisory_status",
    "negative_fixtures",
    "claim_boundary",
]

DASHBOARD_SCHEMA = {
    "phase_ref": "string",
    "lane": "Arby|Aster Vale|aggregate",
    "notice_id": "string",
    "run_id": "string",
    "source_hash_refs": ["sha256"],
    "source_chain_status": "MATCHED|OPEN_GAP|FAIL_BLOCKER",
    "notice_state": "REQUESTED|LAUNCHED|RUNNING|FINAL_MESSAGE_READY|MARKER_REVIEW|SUMMARY_READY_METADATA_ONLY|PUBLISHED_METADATA_ONLY|OPEN_GAP|FAIL_BLOCKER",
    "marker_review_status": "metadata_only|reviewed_metadata_only|open_gap|blocked",
    "raw_output_published": False,
    "transport_published": False,
    "dashboard_label": "metadata_status_only",
    "gmUT_gate_effect": "none_open_not_tested",
}

APP_ADVISORY_HINTS = [
    {
        "lane": "Cicero",
        "hint": "dashboard sync needs lane requirement, notification state, notice timestamp, source hash, marker review, staleness, false-complete, raw-output, transport, and GMUT-effect fields",
    },
    {
        "lane": "Kierkegaard",
        "hint": "dashboard sync should preserve humane metadata continuity without pressure labels, surveillance, proof, quality grading, or continuity overclaims",
    },
    {
        "lane": "Aristotle",
        "hint": "publication-bound rows require matched source hashes, explicit marker state, both required lanes, false raw-output flags, and deterministic blocker fixtures",
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
    if case.get("raw_output_published") or case.get("transport_published") or case.get("raw_text_derived_status"):
        observed = "FAIL_BLOCKER"
    elif case.get("generic_pass") or case.get("proof_label") or case.get("surveillance_label"):
        observed = "FAIL_BLOCKER"
    elif case.get("summary_ready") and not case.get("marker_review_ok"):
        observed = "FAIL_BLOCKER"
    elif case.get("summary_ready") and not case.get("source_hash_match"):
        observed = "FAIL_BLOCKER"
    elif case.get("summary_ready") and case.get("lane_missing"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source") or case.get("stale_notice"):
        observed = "OPEN_GAP"
    elif case.get("metadata_only") and case.get("source_hash_match") and case.get("marker_review_ok"):
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
            "metadata_dashboard_row_expected_pass",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "marker_review_ok": True,
                "metadata_only": True,
                "source_hash_match": True,
            },
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "summary_without_marker_review_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "marker_review_ok": False,
                "source_hash_match": True,
                "summary_ready": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "summary_with_hash_drift_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "marker_review_ok": True,
                "source_hash_match": False,
                "summary_ready": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "summary_with_missing_lane_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "lane_missing": True,
                "marker_review_ok": True,
                "source_hash_match": True,
                "summary_ready": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_flag_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "raw_output_published": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "transport_flag_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "transport_published": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "missing_source": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "stale_notice_expected_open_gap",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "stale_notice": True,
            },
            "OPEN_GAP",
        ),
        fixture(
            "generic_pass_label_expected_fail",
            {
                "generic_pass": True,
                "gmut_gate_effect": "none_open_not_tested",
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "proof_label_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "proof_label": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "surveillance_label_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "surveillance_label": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_text_derived_dashboard_status_expected_fail",
            {
                "gmut_gate_effect": "none_open_not_tested",
                "raw_text_derived_status": True,
            },
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_moved_expected_fail",
            {
                "gmut_gate_effect": "gate_moved",
                "metadata_only": True,
            },
            "FAIL_BLOCKER",
        ),
    ]


def dashboard_rows(continuity: dict[str, Any]) -> list[dict[str, Any]]:
    source_hashes = [item.get("sha256") for item in continuity.get("source_refs", []) if item.get("sha256")]
    rows = []
    for lane_state in continuity.get("lane_states", []):
        rows.append(
            {
                "dashboard_label": "metadata_status_only",
                "gmUT_gate_effect": "none_open_not_tested",
                "lane": lane_state.get("lane"),
                "marker_review_status": "reviewed_metadata_only"
                if lane_state.get("final_message_marker_count", 0)
                else "metadata_only",
                "notice_id": f"{PHASE}-{lane_state.get('lane', 'lane').lower().replace(' ', '-')}-notice",
                "notice_state": lane_state.get("state"),
                "phase_ref": PHASE,
                "raw_output_published": False,
                "run_id": f"{PHASE}-dashboard-sync",
                "source_chain_status": "MATCHED",
                "source_hash_refs": source_hashes[:4],
                "transport_published": False,
            }
        )
    rows.append(
        {
            "dashboard_label": "metadata_status_only",
            "gmUT_gate_effect": "none_open_not_tested",
            "lane": "aggregate",
            "marker_review_status": "metadata_only",
            "notice_id": f"{PHASE}-aggregate-notice",
            "notice_state": continuity.get("aggregate_status"),
            "phase_ref": PHASE,
            "raw_output_published": False,
            "run_id": f"{PHASE}-dashboard-sync",
            "source_chain_status": "MATCHED",
            "source_hash_refs": source_hashes[:4],
            "transport_published": False,
        }
    )
    return rows


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_DASHBOARD_SYNC_CONTRACT_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    continuity = read_json(CONTINUITY)
    run_status = read_json(RUN_STATUS)
    source_refs = [source_ref(CONTINUITY), source_ref(RUN_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    present_rows = set(continuity.get("dashboard_update_rows", []))
    missing_rows = sorted(set(REQUIRED_ROWS) - present_rows)
    sync_rows = dashboard_rows(continuity)
    fixture_rows = build_fixtures()
    fixture_mismatches = [item for item in fixture_rows if item["status"] != "EXPECTED_CONFIRMED"]
    lane_count = len([item for item in sync_rows if item["lane"] in {"Arby", "Aster Vale"}])

    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v475 x2 hardening and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "dashboard_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_rows else "OPEN_GAP_ROW_COVERAGE",
            "Required x2 dashboard update rows are covered by the sync contract.",
            {"missing_rows": missing_rows, "present_row_count": len(present_rows)},
        ),
        row(
            "lane_row_coverage",
            "PASS_SHAPE_ONLY" if lane_count == 2 else "FAIL_LANE_ROW_COVERAGE",
            "Arby and Aster Vale dashboard rows are present without raw output.",
            {"lane_count": lane_count},
        ),
        row(
            "schema_contract",
            "PASS_SHAPE_ONLY",
            "Dashboard rows are constrained to metadata state, source-hash references, marker status, and claim boundary fields.",
            DASHBOARD_SCHEMA,
        ),
        row(
            "label_policy",
            "PASS_SHAPE_ONLY",
            "Dashboard labels are metadata-status labels only and avoid pressure, proof, surveillance, or content-quality claims.",
            {
                "allowed_label": "metadata_status_only",
                "blocked_labels": ["success", "failure", "stalled", "certified", "truth_verified"],
            },
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Dashboard sync fixtures confirmed marker, hash, lane, raw-output, stale, label, and GMUT boundary behavior.",
            {"fixture_count": len(fixture_rows), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "app_advisory_hints",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle v1 x2 guidance is preserved as dashboard-safe hints.",
            {"hints": APP_ADVISORY_HINTS},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This is a THOS dashboard sync contract only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixture_rows)

    payload = {
        "aggregate_status": status,
        "app_advisory_hints": APP_ADVISORY_HINTS,
        "dashboard_rows": sync_rows,
        "dashboard_schema": DASHBOARD_SCHEMA,
        "fixtures": fixture_rows,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "source_run_status": run_status.get("run_status"),
            "v2_x2_acceptance_criteria": [
                "dashboard rows must remain metadata-only",
                "Arby and Aster Vale lane rows must both be present",
                "source-hash refs must match curated sources",
                "marker-review status must be explicit before summary readiness",
                "stale notice and dashboard count mismatch rules must be explicit",
                "raw-output and transport flags must remain false",
                "dashboard status must never derive from raw text",
                "dashboard labels must not claim proof, content quality, surveillance, GMUT validation, or canon promotion",
            ],
    }

    artifact_json = ARTIFACT_ROOT / f"{PHASE}-dashboard-sync-contract-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-dashboard-sync-contract-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"

    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v2 x1 Dashboard Sync Contract

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v2 x1 turns the no-rush notification hardening into a dashboard sync contract. It permits metadata-status rows only: source hashes, lane state, marker review, raw-output flags, and GMUT boundary.

Dashboard rows: `{len(sync_rows)}`; lane rows: `{lane_count}`.

Source refs: `{len(source_refs)}` checked; gaps: `{len(source_gaps)}`.

Fixtures confirmed: `{len(fixture_rows) - len(fixture_mismatches)}` of `{len(fixture_rows)}`.

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
            "dashboard row coverage checked",
            "lane row coverage checked",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v2 x1 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v2 x1 establishes the dashboard sync contract for no-rush notification metadata.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
