#!/usr/bin/env python3
"""Build v476 THOS v6 x2 approval-reference and marker-review gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v6-x2"
SOURCE_PHASE = "v476-thos-v6-x1"
NEXT_PHASE = "v476-thos-v7-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
LEDGER = ARTIFACT_ROOT / "v476-thos-v6-x1-approval-marker-ledger-v1.json"
LEDGER_STATUS = ARTIFACT_ROOT / "v476-thos-v6-x1-run-status-v1.json"

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
    if case.get("missing_source") or case.get("marker_review_required"):
        observed = "OPEN_GAP"
    elif case.get("approval_row_missing") or case.get("promotion_allowed") or case.get("live_write_allowed"):
        observed = "FAIL_BLOCKER"
    elif case.get("packet_ref_present_without_scope") or case.get("raw_lane_text_published") or case.get("moves_gmut_gate"):
        observed = "FAIL_BLOCKER"
    elif case.get("gate_ready") and case.get("metadata_only"):
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
        fixture("gate_ready_expected_pass", {"gate_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("marker_review_required_expected_open_gap", {"marker_review_required": True}, "OPEN_GAP"),
        fixture("approval_row_missing_expected_fail", {"approval_row_missing": True}, "FAIL_BLOCKER"),
        fixture("promotion_allowed_expected_fail", {"promotion_allowed": True}, "FAIL_BLOCKER"),
        fixture("live_write_allowed_expected_fail", {"live_write_allowed": True}, "FAIL_BLOCKER"),
        fixture("packet_ref_present_without_scope_expected_fail", {"packet_ref_present_without_scope": True}, "FAIL_BLOCKER"),
        fixture("raw_lane_text_publication_expected_fail", {"raw_lane_text_published": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "marker_review_required"):
        return "OPEN_GAP_APPROVAL_MARKER_GATE_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_APPROVAL_MARKER_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    ledger = read_json(LEDGER)
    ledger_status = read_json(LEDGER_STATUS)
    source_refs = [source_ref(LEDGER), source_ref(LEDGER_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    approvals = ledger.get("approval_rows", [])
    markers = ledger.get("marker_rows", [])
    unsafe_approvals = [
        item.get("candidate_id")
        for item in approvals
        if item.get("approval_decision") != "HOLD_REQUIRES_EXACT_PACKET"
        or item.get("approval_packet_ref") is not None
        or item.get("promotion_allowed") is not False
        or item.get("live_write_allowed") is not False
        or item.get("materialization_state") != "candidate_only_not_installed"
        or item.get("gmut_gate_effect") != "none_open_not_tested"
    ]
    marker_review_required = [item for item in markers if str(item.get("marker_review_decision", "")).startswith("REVIEW_REQUIRED")]
    raw_lane_publication = [item.get("lane") for item in markers if item.get("raw_lane_text_published") is not False]
    gate_effect_moved = [item.get("candidate_id") for item in approvals if item.get("gmut_gate_effect") != "none_open_not_tested"]
    fixtures = build_fixtures()
    preflight_rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v6 x1 ledger and run status were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "ledger_status",
            "PASS_SHAPE_ONLY" if ledger.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_APPROVAL_MARKER_LEDGER_READY" and ledger_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_APPROVAL_MARKER_LEDGER_READY" else "OPEN_GAP_LEDGER_NOT_READY",
            "The x1 approval-marker ledger must be ready before x2 gate publication.",
            {"ledger_status": ledger.get("aggregate_status"), "run_status": ledger_status.get("aggregate_status")},
        ),
        row(
            "approval_row_count",
            "PASS_SHAPE_ONLY" if len(approvals) == 90 else "FAIL_APPROVAL_ROW_COUNT",
            "All 90 rehearsal candidates must have approval-reference rows.",
            {"approval_row_count": len(approvals)},
        ),
        row(
            "approval_denial_boundary",
            "PASS_SHAPE_ONLY" if not unsafe_approvals else "FAIL_UNSAFE_APPROVAL_BOUNDARY",
            "All approval rows must deny promotion and live write until exact packet scope exists.",
            {"unsafe_approvals": unsafe_approvals},
        ),
        row(
            "marker_review_required",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED" if marker_review_required else "PASS_SHAPE_ONLY",
            "Marker review remains open when marker metadata is present.",
            {"marker_review_required_count": len(marker_review_required), "marker_row_count": len(markers)},
        ),
        row(
            "raw_lane_publication",
            "PASS_SHAPE_ONLY" if not raw_lane_publication else "FAIL_RAW_LANE_PUBLICATION",
            "No marker row publishes raw lane text.",
            {"raw_lane_publication": raw_lane_publication},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY" if not gate_effect_moved else "FAIL_GMUT_GATE_MOVED",
            "Approval-marker gate does not approve writes, install candidates, or move GMUT gates.",
            {"gate_effect_moved": gate_effect_moved, "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(preflight_rows, fixtures)
    next_roadmap = [
        {
            "task_id": f"v476-v7-task-{index:02d}",
            "task": task,
            "claim_ceiling": "roadmap item only; no live materialization or production claim",
        }
        for index, task in enumerate(
            [
                "Build marker-review resolution options without raw text publication.",
                "Build exact approval packet template rows for future candidate classes.",
                "Build source-drift replay checks for v4-v6 artifacts.",
                "Build v476 closure ledger for v7/v8 handoff.",
                "Carry all six GMUT gates open into v476 v7.",
            ],
            start=1,
        )
    ]
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "next_phase_roadmap": next_roadmap,
        "phase_slug": PHASE,
        "preflight_rows": preflight_rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
    }
    run_status = {
        "aggregate_status": status,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": preflight_rows,
    }
    written: list[Path] = []
    gate_json = ARTIFACT_ROOT / f"{PHASE}-approval-marker-gate-v1.json"
    gate_md = ARTIFACT_ROOT / f"{PHASE}-approval-marker-gate-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(gate_json, payload)
    written.append(gate_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in preflight_rows)
    roadmap_lines = "\n".join(f"- `{item['task_id']}`: {item['task']}" for item in next_roadmap)
    write_md(
        gate_md,
        f"""
# v476 THOS v6 x2 Approval Marker Gate

Generated UTC: `{generated_at}`

Status: `{status}`

Rows:

{row_lines}

v476 v7 roadmap:

{roadmap_lines}

Marker review remains metadata-only and open where required. All candidates remain held until exact approval packet scope exists.

All six GMUT gates remain open.
""",
    )
    written.append(gate_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in preflight_rows)
    write_md(
        status_md,
        f"""
# v476 THOS v6 x2 Run Status

Generated UTC: `{generated_at}`

Status: `{status}`
Next expected phase: `{NEXT_PHASE}`

Rows:

{status_lines}

No runtime transport, session streams, image captures, auth material, plugin-cache bodies, user-skill bodies, or raw sibling transport are published.

All six GMUT gates remain open.
""",
    )
    written.append(status_md)
    return written


def main() -> int:
    written = build_artifacts()
    print(json.dumps({"written": [str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in written]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
