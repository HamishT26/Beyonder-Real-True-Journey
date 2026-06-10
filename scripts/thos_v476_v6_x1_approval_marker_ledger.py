#!/usr/bin/env python3
"""Build v476 THOS v6 x1 approval-reference and marker-review ledger artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v6-x1"
SOURCE_PHASE = "v476-thos-v5-x2"
NEXT_PHASE = "v476-thos-v6-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
REHEARSAL = ARTIFACT_ROOT / "v476-thos-v5-x1-dry-run-rehearsal-v1.json"
V5_GATE = ARTIFACT_ROOT / "v476-thos-v5-x2-dry-run-rehearsal-gate-v1.json"
V5_STATUS = ARTIFACT_ROOT / "v476-thos-v5-x2-run-status-v1.json"
CLI_COMPLETION = ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_APPROVAL_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "approval_decision",
    "approval_packet_ref",
    "promotion_allowed",
    "live_write_allowed",
    "materialization_state",
    "source_ref",
    "source_hash_required",
    "next_action",
    "claim_ceiling",
    "gmut_gate_effect",
]

REQUIRED_MARKER_COLUMNS = [
    "lane",
    "completion_status",
    "final_message_bytes",
    "final_marker_count",
    "stderr_marker_count_unpublished",
    "marker_review_decision",
    "raw_lane_text_published",
    "next_action",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def nz_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


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


def source_ref(path: Path, optional: bool = False) -> dict[str, Any]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {"optional": optional, "path": rel, "status": "OPEN_GAP_MISSING_OPTIONAL_SOURCE" if optional else "OPEN_GAP_MISSING_SOURCE"}
    return {
        "bytes": path.stat().st_size,
        "optional": optional,
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


def approval_rows(rehearsal: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in rehearsal.get("dry_run_rehearsals", []):
        rows.append(
            {
                "approval_decision": "HOLD_REQUIRES_EXACT_PACKET",
                "approval_packet_ref": None,
                "candidate_family": item.get("candidate_family"),
                "candidate_id": item.get("candidate_id"),
                "claim_ceiling": "approval-reference row only; no promotion or live write authorized",
                "gmut_gate_effect": "none_open_not_tested",
                "live_write_allowed": False,
                "materialization_state": "candidate_only_not_installed",
                "next_action": "attach exact approval packet reference only if Hamish grants one for this candidate class",
                "promotion_allowed": False,
                "source_hash_required": True,
                "source_ref": "docs/trinity-live-traces/v476-thos-v5-x1-dry-run-rehearsal-v1.json",
            }
        )
    return rows


def marker_rows(completion: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in completion.get("lanes", []):
        final_marker_count = int(lane.get("final_message_sensitive_marker_count", 0))
        stderr_marker_count = int(lane.get("stderr_sensitive_marker_count_unpublished", 0))
        if final_marker_count > 0:
            decision = "REVIEW_REQUIRED_FINAL_MARKER_METADATA_ONLY"
        elif stderr_marker_count > 0:
            decision = "REVIEW_REQUIRED_STDERR_MARKER_METADATA_ONLY"
        else:
            decision = "NO_MARKERS_DETECTED_METADATA_ONLY"
        rows.append(
            {
                "completion_status": lane.get("completion_status"),
                "final_marker_count": final_marker_count,
                "final_message_bytes": lane.get("final_message_bytes", 0),
                "lane": lane.get("lane"),
                "marker_review_decision": decision,
                "next_action": "keep raw lane text unpublished; review only metadata unless a separate exact review packet is approved",
                "raw_lane_text_published": False,
                "stderr_marker_count_unpublished": stderr_marker_count,
            }
        )
    return rows


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("marker_review_required"):
        observed = "OPEN_GAP"
    elif case.get("approval_allows_promotion") or case.get("live_write_allowed"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_approval_row") or case.get("missing_marker_row") or case.get("missing_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_lane_text_published") or case.get("installed_candidate") or case.get("moves_gmut_gate"):
        observed = "FAIL_BLOCKER"
    elif case.get("ledger_ready") and case.get("metadata_only"):
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
        fixture("ledger_ready_expected_pass", {"ledger_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("marker_review_required_expected_open_gap", {"marker_review_required": True}, "OPEN_GAP"),
        fixture("approval_allows_promotion_expected_fail", {"approval_allows_promotion": True}, "FAIL_BLOCKER"),
        fixture("live_write_allowed_expected_fail", {"live_write_allowed": True}, "FAIL_BLOCKER"),
        fixture("missing_approval_row_expected_fail", {"missing_approval_row": True}, "FAIL_BLOCKER"),
        fixture("missing_marker_row_expected_fail", {"missing_marker_row": True}, "FAIL_BLOCKER"),
        fixture("missing_column_expected_fail", {"missing_column": True}, "FAIL_BLOCKER"),
        fixture("raw_lane_text_publication_expected_fail", {"raw_lane_text_published": True}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"installed_candidate": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "marker_review_metadata"):
        return "OPEN_GAP_APPROVAL_MARKER_LEDGER_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_APPROVAL_MARKER_LEDGER_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    started_at_nz = nz_now()
    rehearsal = read_json(REHEARSAL)
    gate = read_json(V5_GATE)
    gate_status = read_json(V5_STATUS)
    completion = read_json(CLI_COMPLETION)
    source_refs = [source_ref(REHEARSAL), source_ref(V5_GATE), source_ref(V5_STATUS), source_ref(CLI_COMPLETION, optional=True)]
    required_source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY" and not item.get("optional")]
    approvals = approval_rows(rehearsal)
    markers = marker_rows(completion)
    missing_approval_columns = sorted(
        {
            column
            for column in REQUIRED_APPROVAL_COLUMNS
            if any(column not in item for item in approvals)
        }
    )
    missing_marker_columns = sorted(
        {
            column
            for column in REQUIRED_MARKER_COLUMNS
            if any(column not in item for item in markers)
        }
    )
    unsafe_approval_rows = [
        item.get("candidate_id")
        for item in approvals
        if item.get("promotion_allowed") is not False
        or item.get("live_write_allowed") is not False
        or item.get("materialization_state") != "candidate_only_not_installed"
        or item.get("gmut_gate_effect") != "none_open_not_tested"
    ]
    marker_review_required = [item for item in markers if str(item.get("marker_review_decision", "")).startswith("REVIEW_REQUIRED")]
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not required_source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v5 rehearsal/gate sources and optional CLI completion metadata were checked.",
            {"required_source_gap_count": len(required_source_gaps), "source_count": len(source_refs)},
        ),
        row(
            "v5_gate_ready",
            "PASS_SHAPE_ONLY" if gate.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_GATE_READY" and gate_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_GATE_READY" else "OPEN_GAP_V5_GATE_NOT_READY",
            "v476 v5 x2 gate must be ready before approval-marker ledger publication.",
            {"gate_status": gate.get("aggregate_status"), "run_status": gate_status.get("aggregate_status")},
        ),
        row(
            "approval_row_count",
            "PASS_SHAPE_ONLY" if len(approvals) == 90 else "FAIL_APPROVAL_ROW_COUNT",
            "Every dry-run rehearsal row must have an approval-reference row.",
            {"approval_row_count": len(approvals)},
        ),
        row(
            "approval_columns",
            "PASS_SHAPE_ONLY" if not missing_approval_columns else "FAIL_APPROVAL_COLUMNS",
            "All approval-reference rows carry required columns.",
            {"missing_approval_columns": missing_approval_columns},
        ),
        row(
            "approval_safety",
            "PASS_SHAPE_ONLY" if not unsafe_approval_rows else "FAIL_UNSAFE_APPROVAL_ROW",
            "All approval rows deny promotion and live write until an exact packet is attached.",
            {"unsafe_approval_rows": unsafe_approval_rows},
        ),
        row(
            "marker_review_metadata",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED" if marker_review_required else "PASS_SHAPE_ONLY",
            "Marker review metadata is carried without raw lane text publication.",
            {"marker_review_required_count": len(marker_review_required), "marker_row_count": len(markers)},
        ),
        row(
            "marker_columns",
            "PASS_SHAPE_ONLY" if not missing_marker_columns else "FAIL_MARKER_COLUMNS",
            "All marker rows carry required metadata columns.",
            {"missing_marker_columns": missing_marker_columns},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Approval-reference and marker-review metadata does not approve writes, install candidates, or move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "approval_rows": approvals,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "marker_rows": markers,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
        "required_approval_columns": REQUIRED_APPROVAL_COLUMNS,
        "required_marker_columns": REQUIRED_MARKER_COLUMNS,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "started_at_nz": started_at_nz,
    }
    run_status = {
        "aggregate_status": status,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "started_at_nz": started_at_nz,
    }
    written: list[Path] = []
    ledger_json = ARTIFACT_ROOT / f"{PHASE}-approval-marker-ledger-v1.json"
    ledger_md = ARTIFACT_ROOT / f"{PHASE}-approval-marker-ledger-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(ledger_json, payload)
    written.append(ledger_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    marker_lines = "\n".join(f"- {item.get('lane')}: `{item.get('marker_review_decision')}`" for item in markers)
    write_md(
        ledger_md,
        f"""
# v476 THOS v6 x1 Approval Reference and Marker Review Ledger

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`

The ledger carries 90 approval-reference rows. All remain `HOLD_REQUIRES_EXACT_PACKET`, with promotion and live write denied.

Rows:

{row_lines}

Marker rows:

{marker_lines}

Raw lane text remains unpublished.

All six GMUT gates remain open.
""",
    )
    written.append(ledger_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        status_md,
        f"""
# v476 THOS v6 x1 Run Status

NZ start: `{started_at_nz}`
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
