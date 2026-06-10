#!/usr/bin/env python3
"""Build v476 THOS v4 x2 candidate preflight gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v4-x2"
SOURCE_PHASE = "v476-thos-v4-x1"
NEXT_PHASE = "v476-thos-v5-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
CROSSWALK = ARTIFACT_ROOT / "v476-thos-v4-x1-candidate-preflight-crosswalk-v1.json"
CROSSWALK_STATUS = ARTIFACT_ROOT / "v476-thos-v4-x1-run-status-v1.json"
CLI_COMPLETION = ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_FAMILY_COUNTS = {
    "command": 30,
    "skill": 30,
    "system_expansion": 30,
}

REQUIRED_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "candidate_label",
    "source_ref",
    "source_hash_required",
    "approval_required_for_live_write",
    "preflight_state",
    "materialization_state",
    "allowed_probe_levels",
    "blocked_publication_classes",
    "raw_material_boundary",
    "next_action",
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
        "status": "CARRIED_FROM_V476_V3",
        "points": [
            "materialize only with curated evidence refs, required fields, guard status, source authority, and no blocked publication classes",
            "notifier rows observe; they do not publish, certify, or complete a gate",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "CARRIED_FROM_V476_V3",
        "points": [
            "handoff and crosswalk artifacts are metadata continuity only",
            "open gaps should be preserved rather than erased",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "CARRIED_FROM_V476_V3",
        "points": [
            "gate contract order, source hashes, notifier completeness, negative fixtures, and publication boundaries",
            "generic pass labels and aggregate-child contradictions remain invalid",
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
    if case.get("missing_source") or case.get("marker_review"):
        observed = "OPEN_GAP"
    elif case.get("missing_candidate") or case.get("missing_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_hash_not_required") or case.get("approval_false"):
        observed = "FAIL_BLOCKER"
    elif case.get("installed_candidate") or case.get("raw_material_published") or case.get("missing_block_class"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
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
        fixture("gate_ready_expected_pass", {"gate_ready": True, "gmut_gate_effect": "none_open_not_tested", "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "missing_source": True}, "OPEN_GAP"),
        fixture("marker_review_expected_open_gap", {"gmut_gate_effect": "none_open_not_tested", "marker_review": True}, "OPEN_GAP"),
        fixture("missing_candidate_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_candidate": True}, "FAIL_BLOCKER"),
        fixture("missing_column_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_column": True}, "FAIL_BLOCKER"),
        fixture("source_hash_not_required_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "source_hash_not_required": True}, "FAIL_BLOCKER"),
        fixture("approval_false_expected_fail", {"approval_false": True, "gmut_gate_effect": "none_open_not_tested"}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "installed_candidate": True}, "FAIL_BLOCKER"),
        fixture("raw_material_publication_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "raw_material_published": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"gmut_gate_effect": "none_open_not_tested", "missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"gate_ready": True, "gmut_gate_effect": "gate_moved", "metadata_only": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "optional_cli_marker_review"):
        return "OPEN_GAP_CANDIDATE_PREFLIGHT_GATE_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    crosswalk = read_json(CROSSWALK)
    crosswalk_status = read_json(CROSSWALK_STATUS)
    completion = read_json(CLI_COMPLETION)
    source_refs = [source_ref(CROSSWALK), source_ref(CROSSWALK_STATUS), source_ref(CLI_COMPLETION, optional=True)]
    required_source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY" and not item.get("optional")]
    rows_in = crosswalk.get("candidate_crosswalk", [])
    family_counts = {
        family: len([item for item in rows_in if item.get("candidate_family") == family])
        for family in REQUIRED_FAMILY_COUNTS
    }
    missing_family_counts = {
        family: {"expected": expected, "observed": family_counts.get(family, 0)}
        for family, expected in REQUIRED_FAMILY_COUNTS.items()
        if family_counts.get(family, 0) != expected
    }
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in rows_in)
        }
    )
    source_hash_missing = [item.get("candidate_id") for item in rows_in if item.get("source_hash_required") is not True]
    approval_false = [item.get("candidate_id") for item in rows_in if item.get("approval_required_for_live_write") is not True]
    installed_candidates = [item.get("candidate_id") for item in rows_in if item.get("materialization_state") != "candidate_only_not_installed"]
    missing_block_classes = sorted(
        {
            block
            for block in REQUIRED_BLOCK_CLASSES
            if any(block not in item.get("blocked_publication_classes", []) for item in rows_in)
        }
    )
    raw_boundary_mismatch = [
        item.get("candidate_id")
        for item in rows_in
        if "published" not in str(item.get("raw_material_boundary", "")).lower()
    ]
    gate_effect_moved = [item.get("candidate_id") for item in rows_in if item.get("gmut_gate_effect") != "none_open_not_tested"]
    completion_status = completion.get("aggregate_status", "OPEN_GAP_NOT_YET_WRITTEN")
    fixtures = build_fixtures()
    preflight_rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not required_source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v4 x1 crosswalk, v4 x1 status, and optional v3 CLI completion notice were checked.",
            {"required_source_gap_count": len(required_source_gaps), "source_count": len(source_refs)},
        ),
        row(
            "crosswalk_status",
            "PASS_SHAPE_ONLY" if crosswalk.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_CROSSWALK_READY" and crosswalk_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_CROSSWALK_READY" else "OPEN_GAP_CROSSWALK_NOT_READY",
            "The x1 candidate preflight crosswalk must be ready before x2 gate publication.",
            {"crosswalk_status": crosswalk.get("aggregate_status"), "run_status": crosswalk_status.get("aggregate_status")},
        ),
        row(
            "family_counts",
            "PASS_SHAPE_ONLY" if not missing_family_counts else "FAIL_FAMILY_COUNTS",
            "All three candidate families must carry 30 rows.",
            {"family_counts": family_counts, "missing_family_counts": missing_family_counts},
        ),
        row(
            "required_columns",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_COLUMNS",
            "All candidate rows must carry required columns.",
            {"missing_columns": missing_columns},
        ),
        row(
            "source_hash_required",
            "PASS_SHAPE_ONLY" if not source_hash_missing else "FAIL_SOURCE_HASH_REQUIRED",
            "Every candidate row requires source-hash carry-forward.",
            {"source_hash_missing": source_hash_missing},
        ),
        row(
            "approval_boundary",
            "PASS_SHAPE_ONLY" if not approval_false else "FAIL_APPROVAL_BOUNDARY",
            "Every candidate live-write path remains approval-bound.",
            {"approval_false": approval_false},
        ),
        row(
            "candidate_materialization_state",
            "PASS_SHAPE_ONLY" if not installed_candidates else "FAIL_CANDIDATE_INSTALLED",
            "No candidate is installed or promoted in v476 v4.",
            {"installed_candidates": installed_candidates},
        ),
        row(
            "blocked_publication_classes",
            "PASS_SHAPE_ONLY" if not missing_block_classes else "FAIL_BLOCKED_CLASS_COVERAGE",
            "All candidate rows carry required blocked publication classes.",
            {"missing_block_classes": missing_block_classes},
        ),
        row(
            "raw_material_boundary",
            "PASS_SHAPE_ONLY" if not raw_boundary_mismatch else "FAIL_RAW_BOUNDARY",
            "Raw runtime and sibling material remain unpublished.",
            {"raw_boundary_mismatch": raw_boundary_mismatch},
        ),
        row(
            "optional_cli_marker_review",
            "OPEN_GAP_CLI_MARKER_REVIEW_PENDING" if completion_status == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "PASS_SHAPE_ONLY",
            "CLI marker review remains a carried optional open gap until a separate reviewer classifies it.",
            {"completion_status": completion_status},
        ),
        row(
            "app_advisory_boundary",
            "PASS_SHAPE_ONLY",
            "v476 v3 app advisory guidance was carried as sanitized metadata only.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY" if not gate_effect_moved else "FAIL_GMUT_GATE_MOVED",
            "Candidate preflight work does not move or close GMUT gates.",
            {"gate_effect_moved": gate_effect_moved, "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(preflight_rows, fixtures)
    next_roadmap = [
        {
            "task_id": f"v476-v5-task-{index:02d}",
            "task": task,
            "claim_ceiling": "roadmap item only; no live materialization or production claim",
        }
        for index, task in enumerate(
            [
                "Build a dry-run materialization rehearsal for command candidates.",
                "Build a body-preserving frontmatter rehearsal for skill candidates.",
                "Build a registry naming rehearsal for system-expansion candidates.",
                "Add source-hash drift checks for every crosswalk source.",
                "Add optional lane marker reviewer rows that never publish final messages.",
                "Define a freshness window for no-rush CLI completion receipts.",
                "Gate candidate promotion against explicit approval packet references.",
                "Gate connector and cloud writes as denied until separate approval exists.",
                "Gate all raw runtime material as unpublished.",
                "Carry GMUT gates open into v476 v5.",
            ],
            start=1,
        )
    ]
    payload = {
        "aggregate_status": status,
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "family_counts": family_counts,
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
    gate_json = ARTIFACT_ROOT / f"{PHASE}-candidate-preflight-gate-v1.json"
    gate_md = ARTIFACT_ROOT / f"{PHASE}-candidate-preflight-gate-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(gate_json, payload)
    written.append(gate_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in preflight_rows)
    roadmap_lines = "\n".join(f"- `{item['task_id']}`: {item['task']}" for item in next_roadmap)
    write_md(
        gate_md,
        f"""
# v476 THOS v4 x2 Candidate Preflight Gate

Generated UTC: `{generated_at}`

Status: `{status}`

Rows:

{row_lines}

v476 v5 roadmap:

{roadmap_lines}

All candidate rows remain candidate-only and approval-bound. The optional CLI marker-review open gap is carried without publishing raw lane content.

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
# v476 THOS v4 x2 Run Status

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
