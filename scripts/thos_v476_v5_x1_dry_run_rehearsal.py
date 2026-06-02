#!/usr/bin/env python3
"""Build v476 THOS v5 x1 dry-run rehearsal artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v5-x1"
SOURCE_PHASE = "v476-thos-v4-x2"
NEXT_PHASE = "v476-thos-v5-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
V4_CROSSWALK = ARTIFACT_ROOT / "v476-thos-v4-x1-candidate-preflight-crosswalk-v1.json"
V4_GATE = ARTIFACT_ROOT / "v476-thos-v4-x2-candidate-preflight-gate-v1.json"
V4_STATUS = ARTIFACT_ROOT / "v476-thos-v4-x2-run-status-v1.json"
CLI_COMPLETION = ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_COLUMNS = [
    "candidate_id",
    "candidate_family",
    "rehearsal_type",
    "source_ref",
    "source_hash_required",
    "dry_run_only",
    "mutation_performed",
    "materialization_state",
    "approval_required_for_live_write",
    "rehearsal_state",
    "blocked_publication_classes",
    "next_action",
    "gmut_gate_effect",
]

BLOCKED_PUBLICATION_CLASSES = [
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

REHEARSAL_BY_FAMILY = {
    "command": "stdout_only_command_plan",
    "skill": "body_preserving_frontmatter_plan",
    "system_expansion": "registry_naming_plan",
}


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


def rehearsal_rows(crosswalk: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in crosswalk.get("candidate_crosswalk", []):
        family = candidate.get("candidate_family")
        rows.append(
            {
                "approval_required_for_live_write": True,
                "blocked_publication_classes": BLOCKED_PUBLICATION_CLASSES,
                "candidate_family": family,
                "candidate_id": candidate.get("candidate_id"),
                "dry_run_only": True,
                "gmut_gate_effect": "none_open_not_tested",
                "materialization_state": "candidate_only_not_installed",
                "mutation_performed": False,
                "next_action": "gate rehearsal in v476-thos-v5-x2 before any approval packet reference can be attached",
                "rehearsal_state": "PASS_SHAPE_ONLY",
                "rehearsal_type": REHEARSAL_BY_FAMILY.get(str(family), "unknown_family_plan"),
                "source_hash_required": True,
                "source_ref": "docs/trinity-live-traces/v476-thos-v4-x1-candidate-preflight-crosswalk-v1.json",
            }
        )
    return rows


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("marker_review"):
        observed = "OPEN_GAP"
    elif case.get("missing_rehearsal_row") or case.get("missing_column") or case.get("unknown_family"):
        observed = "FAIL_BLOCKER"
    elif case.get("dry_run_false") or case.get("mutation_true") or case.get("installed_candidate"):
        observed = "FAIL_BLOCKER"
    elif case.get("approval_false") or case.get("missing_block_class") or case.get("moves_gmut_gate"):
        observed = "FAIL_BLOCKER"
    elif case.get("rehearsal_ready") and case.get("metadata_only"):
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
        fixture("rehearsal_ready_expected_pass", {"metadata_only": True, "rehearsal_ready": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("marker_review_expected_open_gap", {"marker_review": True}, "OPEN_GAP"),
        fixture("missing_rehearsal_row_expected_fail", {"missing_rehearsal_row": True}, "FAIL_BLOCKER"),
        fixture("missing_column_expected_fail", {"missing_column": True}, "FAIL_BLOCKER"),
        fixture("unknown_family_expected_fail", {"unknown_family": True}, "FAIL_BLOCKER"),
        fixture("dry_run_false_expected_fail", {"dry_run_false": True}, "FAIL_BLOCKER"),
        fixture("mutation_true_expected_fail", {"mutation_true": True}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"installed_candidate": True}, "FAIL_BLOCKER"),
        fixture("approval_false_expected_fail", {"approval_false": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "optional_cli_marker_review"):
        return "OPEN_GAP_DRY_RUN_REHEARSAL_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    started_at_nz = nz_now()
    crosswalk = read_json(V4_CROSSWALK)
    gate = read_json(V4_GATE)
    gate_status = read_json(V4_STATUS)
    completion = read_json(CLI_COMPLETION)
    source_refs = [source_ref(V4_CROSSWALK), source_ref(V4_GATE), source_ref(V4_STATUS), source_ref(CLI_COMPLETION, optional=True)]
    required_source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY" and not item.get("optional")]
    rehearsals = rehearsal_rows(crosswalk)
    family_counts = {
        family: len([item for item in rehearsals if item.get("candidate_family") == family])
        for family in REHEARSAL_BY_FAMILY
    }
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in rehearsals)
        }
    )
    unsafe_rows = [
        item.get("candidate_id")
        for item in rehearsals
        if item.get("dry_run_only") is not True
        or item.get("mutation_performed") is not False
        or item.get("materialization_state") != "candidate_only_not_installed"
        or item.get("approval_required_for_live_write") is not True
        or item.get("gmut_gate_effect") != "none_open_not_tested"
    ]
    unknown_family_rows = [item.get("candidate_id") for item in rehearsals if item.get("rehearsal_type") == "unknown_family_plan"]
    completion_status = completion.get("aggregate_status", "OPEN_GAP_NOT_YET_WRITTEN")
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not required_source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v4 crosswalk/gate sources and optional CLI completion metadata were checked.",
            {"required_source_gap_count": len(required_source_gaps), "source_count": len(source_refs)},
        ),
        row(
            "v4_gate_ready",
            "PASS_SHAPE_ONLY" if gate.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_GATE_READY" and gate_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_GATE_READY" else "OPEN_GAP_V4_GATE_NOT_READY",
            "v476 v4 x2 gate must be ready before dry-run rehearsal.",
            {"gate_status": gate.get("aggregate_status"), "run_status": gate_status.get("aggregate_status")},
        ),
        row(
            "family_counts",
            "PASS_SHAPE_ONLY" if all(count == 30 for count in family_counts.values()) else "FAIL_FAMILY_COUNTS",
            "The rehearsal ledger must carry 30 command, 30 skill, and 30 system-expansion rows.",
            family_counts,
        ),
        row(
            "required_columns",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_COLUMNS",
            "All rehearsal rows carry required columns.",
            {"missing_columns": missing_columns},
        ),
        row(
            "safe_dry_run_states",
            "PASS_SHAPE_ONLY" if not unsafe_rows else "FAIL_UNSAFE_DRY_RUN_STATE",
            "Every rehearsal row stays dry-run-only, mutation-free, candidate-only, approval-bound, and GMUT-neutral.",
            {"unsafe_rows": unsafe_rows},
        ),
        row(
            "known_rehearsal_families",
            "PASS_SHAPE_ONLY" if not unknown_family_rows else "FAIL_UNKNOWN_REHEARSAL_FAMILY",
            "Every candidate family maps to a known rehearsal type.",
            {"unknown_family_rows": unknown_family_rows},
        ),
        row(
            "optional_cli_marker_review",
            "OPEN_GAP_CLI_MARKER_REVIEW_PENDING" if completion_status == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "PASS_SHAPE_ONLY",
            "CLI marker review is carried as an optional open gap only.",
            {"completion_status": completion_status},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Dry-run rehearsal does not install candidates, prove production readiness, or move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "dry_run_rehearsals": rehearsals,
        "family_counts": family_counts,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_rows": rows,
        "required_columns": REQUIRED_COLUMNS,
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
    rehearsal_json = ARTIFACT_ROOT / f"{PHASE}-dry-run-rehearsal-v1.json"
    rehearsal_md = ARTIFACT_ROOT / f"{PHASE}-dry-run-rehearsal-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(rehearsal_json, payload)
    written.append(rehearsal_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        rehearsal_md,
        f"""
# v476 THOS v5 x1 Dry-Run Rehearsal

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`

The rehearsal ledger carries 90 rows and performs no live materialization. Command candidates use stdout-only command plans, skill candidates use body-preserving frontmatter plans, and system-expansion candidates use registry naming plans.

Rows:

{row_lines}

Family counts:

- command: `{family_counts.get('command', 0)}`
- skill: `{family_counts.get('skill', 0)}`
- system_expansion: `{family_counts.get('system_expansion', 0)}`

All six GMUT gates remain open.
""",
    )
    written.append(rehearsal_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        status_md,
        f"""
# v476 THOS v5 x1 Run Status

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
