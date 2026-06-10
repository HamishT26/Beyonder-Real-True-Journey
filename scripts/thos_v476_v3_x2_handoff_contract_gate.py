#!/usr/bin/env python3
"""Build v476 THOS v3 x2 handoff contract gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v3-x2"
SOURCE_PHASE = "v476-thos-v3-x1"
NEXT_PHASE = "v476-thos-v4-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
CONTRACT = ARTIFACT_ROOT / "v476-thos-v3-x1-handoff-contract-v1.json"
CONTRACT_STATUS = ARTIFACT_ROOT / "v476-thos-v3-x1-run-status-v1.json"
COMPLETION_NOTICE = ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_ROWS = [
    "command_candidate_contract",
    "skill_candidate_contract",
    "system_expansion_candidate_contract",
    "script_inventory_contract",
    "connector_plugin_boundary_contract",
    "dashboard_sync_contract",
    "receipt_freshness_contract",
    "publication_guard_contract",
    "negative_fixture_contract",
    "source_hash_chain_contract",
    "async_cli_lane_contract",
    "gmut_open_boundary_contract",
]

REQUIRED_COLUMNS = [
    "row_id",
    "surface_family",
    "source_ref",
    "contract_state",
    "materialization_state",
    "approval_required_for_live_write",
    "raw_material_boundary",
    "allowed_next_action",
    "blocked_publication_classes",
    "validation_gate",
    "claim_ceiling",
    "gmut_gate_effect",
]

REQUIRED_BLOCK_CLASSES = [
    "runtime_capture_publication",
    "transport_body_publication",
    "private_material_publication",
    "unapproved_connector_write",
    "destructive_cleanup",
    "candidate_installation_without_preflight",
    "production_readiness_claim",
    "gmut_validation_claim",
    "canon_promotion_claim",
]

APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "handoff rows should include phase/source refs, suite-map status, required-row gate status, materialization/candidate-only status, receipt freshness, async notifier status, supervisor guard status, blocked publication classes, next artifact, and GMUT open effect",
            "materialize only with curated evidence refs, required fields, guard status, source authority, and no blocked publication classes; otherwise keep candidate-only",
            "async notifier rows observe lane presence, freshness, marker-review state, metadata-only receipt status, and raw-output block status; notifier metadata does not certify or publish lane content",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "safe claim label is handoff_contract_metadata_only",
            "the contract may record bounded metadata continuity and open-gap preservation, but cannot authorize mutation, connector writes, cleanup, quality certification, GMUT validation, consciousness proof, or gate closure",
            "asynchronous Arby/Aster completion may arrive under no-rush handling; publication should wait for curated metadata or carry an open gap",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "ordered sections should include source hash chain, required-row matrix, suite-map summary, publication guard, async lane notifier, negative fixture summary, handoff risk ledger, and GMUT boundary",
            "validation invariants include one occurrence per ordered section, source hash refs, boundary flags, no generic PASS, no aggregate-child contradiction, and GMUT effect none_open_not_tested",
            "v476 v4 should gate contract order, source hashes, notifier completeness, negative fixtures, and publication boundaries while remaining metadata-only",
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


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("optional_completion_pending"):
        observed = "OPEN_GAP"
    elif case.get("missing_source"):
        observed = "OPEN_GAP"
    elif case.get("missing_required_row") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_block_class") or case.get("unsafe_materialization"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_material_published") or case.get("approval_false") or case.get("source_hash_drift"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("contract_gate_ready") and case.get("metadata_only"):
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
        fixture("contract_gate_ready_expected_pass", {"contract_gate_ready": True, "gmut_gate_effect": "none_open_not_tested", "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "missing_source": True}, "OPEN_GAP"),
        fixture("optional_completion_pending_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "optional_completion_pending": True}, "OPEN_GAP"),
        fixture("missing_required_row_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_row": True}, "FAIL_BLOCKER"),
        fixture("missing_required_column_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_required_column": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("unsafe_materialization_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "unsafe_materialization": True}, "FAIL_BLOCKER"),
        fixture("raw_material_publication_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "raw_material_published": True}, "FAIL_BLOCKER"),
        fixture("approval_false_expected_fail", {"approval_false": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("source_hash_drift_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "source_hash_drift": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"contract_gate_ready": True, "gmut_gate_effect": "gate_moved", "metadata_only": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "optional_cli_completion_notice"):
        return "OPEN_GAP_CONTRACT_GATE_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_GATE_READY"


def safe_materialization_state(state: str) -> bool:
    return state in {
        "candidate_only_not_installed",
        "evidence_contract_only",
        "async_advisory_lane_temp_transport_only",
    }


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    contract = read_json(CONTRACT)
    contract_status = read_json(CONTRACT_STATUS)
    completion = read_json(COMPLETION_NOTICE)
    source_refs = [source_ref(CONTRACT), source_ref(CONTRACT_STATUS), source_ref(COMPLETION_NOTICE, optional=True)]
    required_source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY" and not item.get("optional")]
    contract_rows = contract.get("contract_rows", [])
    present_rows = sorted(item.get("row_id") for item in contract_rows if item.get("row_id"))
    missing_rows = sorted(set(REQUIRED_ROWS) - set(present_rows))
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in contract_rows)
        }
    )
    not_ready_rows = [item.get("row_id") for item in contract_rows if item.get("contract_state") != "PASS_SHAPE_ONLY"]
    unsafe_materialization = [
        item.get("row_id")
        for item in contract_rows
        if not safe_materialization_state(str(item.get("materialization_state", "")))
    ]
    approval_false = [item.get("row_id") for item in contract_rows if item.get("approval_required_for_live_write") is not True]
    missing_block_classes = sorted(
        {
            block
            for block in REQUIRED_BLOCK_CLASSES
            if any(block not in item.get("blocked_publication_classes", []) for item in contract_rows)
        }
    )
    raw_boundary_mismatch = [
        item.get("row_id")
        for item in contract_rows
        if "raw" not in str(item.get("raw_material_boundary", "")).lower()
        or "published" not in str(item.get("raw_material_boundary", "")).lower()
    ]
    gate_effect_moved = [item.get("row_id") for item in contract_rows if item.get("gmut_gate_effect") != "none_open_not_tested"]
    completion_status = completion.get("aggregate_status", "OPEN_GAP_NOT_YET_WRITTEN")
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not required_source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v3 x1 contract and run status sources were checked.",
            {"required_source_gap_count": len(required_source_gaps), "source_count": len(source_refs)},
        ),
        row(
            "contract_status",
            "PASS_SHAPE_ONLY" if contract.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_READY" and contract_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_READY" else "OPEN_GAP_CONTRACT_NOT_READY",
            "The x1 handoff contract must be ready before x2 gate publication.",
            {"contract_status": contract.get("aggregate_status"), "run_status": contract_status.get("aggregate_status")},
        ),
        row(
            "required_contract_rows",
            "PASS_SHAPE_ONLY" if not missing_rows else "FAIL_REQUIRED_CONTRACT_ROWS",
            "All required contract rows must be present.",
            {"missing_rows": missing_rows},
        ),
        row(
            "required_contract_columns",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_CONTRACT_COLUMNS",
            "All required contract columns must be present.",
            {"missing_columns": missing_columns},
        ),
        row(
            "contract_row_states",
            "PASS_SHAPE_ONLY" if not not_ready_rows else "OPEN_GAP_CONTRACT_ROW_NOT_READY",
            "All contract rows must be shape-ready.",
            {"not_ready_rows": not_ready_rows},
        ),
        row(
            "safe_materialization_states",
            "PASS_SHAPE_ONLY" if not unsafe_materialization else "FAIL_UNSAFE_MATERIALIZATION_STATE",
            "x2 permits candidate/evidence/async metadata states only.",
            {"unsafe_materialization": unsafe_materialization},
        ),
        row(
            "approval_boundary",
            "PASS_SHAPE_ONLY" if not approval_false else "FAIL_APPROVAL_BOUNDARY",
            "Every live-write path must still require approval.",
            {"approval_false": approval_false},
        ),
        row(
            "blocked_publication_classes",
            "PASS_SHAPE_ONLY" if not missing_block_classes else "FAIL_BLOCKED_CLASS_COVERAGE",
            "All contract rows carry the required blocked publication classes.",
            {"missing_block_classes": missing_block_classes},
        ),
        row(
            "raw_material_boundary",
            "PASS_SHAPE_ONLY" if not raw_boundary_mismatch else "FAIL_RAW_BOUNDARY_MISMATCH",
            "Raw transport and private material remain unpublished.",
            {"raw_boundary_mismatch": raw_boundary_mismatch},
        ),
        row(
            "optional_cli_completion_notice",
            "PASS_SHAPE_ONLY" if completion_status in {"FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"} else "OPEN_GAP_ASYNC_COMPLETION_PENDING",
            "Arby/Aster completion notice is useful but not required for the handoff contract gate.",
            {"completion_status": completion_status},
        ),
        row(
            "app_advisory_boundary",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle requests were sent but are not blocking this local gate.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS), "raw_advisory_text_recorded": False},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY" if not gate_effect_moved else "FAIL_GMUT_GATE_MOVED",
            "THOS contract work does not move or close GMUT gates.",
            {"gate_effect_moved": gate_effect_moved, "gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures)
    next_roadmap = [
        {
            "task_id": f"v476-v4-task-{index:02d}",
            "task": task,
            "claim_ceiling": "roadmap item only; no live write or production claim",
        }
        for index, task in enumerate(
            [
                "Build a candidate-to-preflight crosswalk for the 30 command candidates.",
                "Build a candidate-to-preflight crosswalk for the 30 skill candidates.",
                "Build a candidate-to-preflight crosswalk for the 30 system-expansion candidates.",
                "Gate each candidate against explicit approval and raw-material boundaries.",
                "Add source-hash carry-forward rows for suite-map, matrix, contract, and completion notice sources.",
                "Define a no-rush lane completion receipt freshness rule.",
                "Keep optional Arby/Aster final text local and publish metadata only.",
                "Map launcher failure modes into retry classes without destructive cleanup.",
                "Map watcher timeout states into open-gap states instead of failures.",
                "Add a command-surface dry-run-only materialization rehearsal plan.",
                "Add a skill-surface frontmatter and body-preservation rehearsal plan.",
                "Add a system-expansion registry naming rehearsal plan.",
                "Add connector/plugin mutation denial rows until separate connector approval exists.",
                "Add dashboard sync rows that use counts and hashes only.",
                "Add app-lane advisory receipt rows that never publish raw advisory text.",
                "Add sibling lane budget and no-rush policy rows.",
                "Add negative fixtures for missing source, hash drift, unsafe state, and raw transport publication.",
                "Add GMUT claim-denial fixtures to prevent THOS association overclaim.",
                "Add exact-stage publication guard rows for every v476 v4 artifact.",
                "Carry all six GMUT gates open into v476 v4.",
            ],
            start=1,
        )
    ]
    payload = {
        "aggregate_status": status,
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "next_phase_roadmap": next_roadmap,
        "phase_slug": PHASE,
        "preflight_rows": rows,
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
        "rows": rows,
    }
    written: list[Path] = []
    gate_json = ARTIFACT_ROOT / f"{PHASE}-handoff-contract-gate-v1.json"
    gate_md = ARTIFACT_ROOT / f"{PHASE}-handoff-contract-gate-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(gate_json, payload)
    written.append(gate_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    roadmap_lines = "\n".join(f"- `{item['task_id']}`: {item['task']}" for item in next_roadmap)
    write_md(
        gate_md,
        f"""
# v476 THOS v3 x2 Handoff Contract Gate

Generated UTC: `{generated_at}`

Status: `{status}`

The v3 x2 gate checks the x1 handoff contract for required rows, required columns, safe materialization states, approval boundaries, blocked publication classes, raw-material boundaries, optional async completion metadata, and GMUT claim boundaries.

Rows:

{row_lines}

v476 v4 roadmap:

{roadmap_lines}

Arby/Aster completion is allowed to remain pending. Pending completion is an open-gap notification state, not a failure and not a reason to publish raw transport.

All six GMUT gates remain open.
""",
    )
    written.append(gate_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        status_md,
        f"""
# v476 THOS v3 x2 Run Status

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
