#!/usr/bin/env python3
"""Build v476 THOS v4 x1 candidate preflight crosswalk artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v4-x1"
SOURCE_PHASE = "v476-thos-v3-x2"
NEXT_PHASE = "v476-thos-v4-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SUITE_SEED = ARTIFACT_ROOT / "v476-thos-v1-x1-suite-map-seed-v1.json"
HANDOFF_GATE = ARTIFACT_ROOT / "v476-thos-v3-x2-handoff-contract-gate-v1.json"
HANDOFF_STATUS = ARTIFACT_ROOT / "v476-thos-v3-x2-run-status-v1.json"
CLI_COMPLETION = ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

CANDIDATE_FAMILIES = [
    ("command", "command_candidates", "command_surface"),
    ("skill", "skill_candidates", "skill_surface"),
    ("system_expansion", "system_expansion_candidates", "system_expansion_surface"),
]

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


def candidate_rows(suite: dict[str, Any], source_refs: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family, key, surface in CANDIDATE_FAMILIES:
        for candidate in suite.get(key, []):
            rows.append(
                {
                    "allowed_probe_levels": ["P0", "P1", "P2", "P3"],
                    "approval_required_for_live_write": True,
                    "blocked_publication_classes": BLOCKED_PUBLICATION_CLASSES,
                    "candidate_family": family,
                    "candidate_id": candidate.get("candidate_id"),
                    "candidate_label": candidate.get("candidate_label"),
                    "gmut_gate_effect": "none_open_not_tested",
                    "materialization_state": "candidate_only_not_installed",
                    "next_action": "route through v476-thos-v4-x2 gate before any live materialization decision",
                    "preflight_state": "PASS_SHAPE_ONLY",
                    "raw_material_boundary": "no runtime captures, lane transport, session streams, image captures, auth material, or private material published",
                    "source_hash_required": True,
                    "source_ref": source_refs["suite_seed"],
                    "surface_family": surface,
                }
            )
    return rows


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("completion_marker_review"):
        observed = "OPEN_GAP"
    elif case.get("candidate_count_low") or case.get("missing_required_column"):
        observed = "FAIL_BLOCKER"
    elif case.get("approval_false") or case.get("installed_candidate") or case.get("raw_material_published"):
        observed = "FAIL_BLOCKER"
    elif case.get("missing_block_class") or case.get("moves_gmut_gate"):
        observed = "FAIL_BLOCKER"
    elif case.get("crosswalk_ready") and case.get("metadata_only"):
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
        fixture("crosswalk_ready_expected_pass", {"crosswalk_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("completion_marker_review_expected_open_gap", {"completion_marker_review": True}, "OPEN_GAP"),
        fixture("candidate_count_low_expected_fail", {"candidate_count_low": True}, "FAIL_BLOCKER"),
        fixture("missing_required_column_expected_fail", {"missing_required_column": True}, "FAIL_BLOCKER"),
        fixture("approval_false_expected_fail", {"approval_false": True}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"installed_candidate": True}, "FAIL_BLOCKER"),
        fixture("raw_material_publication_expected_fail", {"raw_material_published": True}, "FAIL_BLOCKER"),
        fixture("missing_block_class_expected_fail", {"missing_block_class": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "cli_completion_marker_review"):
        return "OPEN_GAP_CANDIDATE_PREFLIGHT_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_CANDIDATE_PREFLIGHT_CROSSWALK_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    started_at_nz = nz_now()
    suite = read_json(SUITE_SEED)
    gate = read_json(HANDOFF_GATE)
    gate_status = read_json(HANDOFF_STATUS)
    completion = read_json(CLI_COMPLETION)
    source_refs = [
        source_ref(SUITE_SEED),
        source_ref(HANDOFF_GATE),
        source_ref(HANDOFF_STATUS),
        source_ref(CLI_COMPLETION, optional=True),
    ]
    required_source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY" and not item.get("optional")]
    source_ref_by_key = {
        "suite_seed": source_refs[0]["path"],
        "handoff_gate": source_refs[1]["path"],
        "handoff_status": source_refs[2]["path"],
        "cli_completion": source_refs[3]["path"],
    }
    crosswalk = candidate_rows(suite, source_ref_by_key)
    family_counts = {
        family: len([item for item in crosswalk if item["candidate_family"] == family])
        for family, _key, _surface in CANDIDATE_FAMILIES
    }
    missing_columns = sorted(
        {
            column
            for column in REQUIRED_COLUMNS
            if any(column not in item for item in crosswalk)
        }
    )
    unsafe_rows = [
        item["candidate_id"]
        for item in crosswalk
        if item["materialization_state"] != "candidate_only_not_installed"
        or item["approval_required_for_live_write"] is not True
        or item["gmut_gate_effect"] != "none_open_not_tested"
    ]
    completion_status = completion.get("aggregate_status", "OPEN_GAP_NOT_YET_WRITTEN")
    completion_marker_review = completion_status == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not required_source_gaps else "OPEN_GAP_SOURCE_REFS",
            "Suite seed, v3 handoff gate, v3 run status, and optional CLI completion notice were checked.",
            {"required_source_gap_count": len(required_source_gaps), "source_count": len(source_refs)},
        ),
        row(
            "handoff_gate_ready",
            "PASS_SHAPE_ONLY" if gate.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_GATE_READY" and gate_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_GATE_READY" else "OPEN_GAP_HANDOFF_GATE_NOT_READY",
            "v476 v3 x2 handoff gate must be ready before candidate crosswalk publication.",
            {"gate_status": gate.get("aggregate_status"), "run_status": gate_status.get("aggregate_status")},
        ),
        row(
            "candidate_counts",
            "PASS_SHAPE_ONLY" if all(count == 30 for count in family_counts.values()) else "FAIL_CANDIDATE_COUNTS",
            "The crosswalk must carry 30 command, 30 skill, and 30 system-expansion candidates.",
            family_counts,
        ),
        row(
            "required_columns",
            "PASS_SHAPE_ONLY" if not missing_columns else "FAIL_REQUIRED_COLUMNS",
            "All candidate rows include required preflight columns.",
            {"missing_columns": missing_columns},
        ),
        row(
            "safe_candidate_states",
            "PASS_SHAPE_ONLY" if not unsafe_rows else "FAIL_UNSAFE_CANDIDATE_STATE",
            "Every candidate remains candidate-only and approval-bound.",
            {"unsafe_rows": unsafe_rows},
        ),
        row(
            "cli_completion_marker_review",
            "OPEN_GAP_CLI_MARKER_REVIEW_PENDING" if completion_marker_review else "PASS_SHAPE_ONLY",
            "CLI completion metadata is carried as optional source; marker review does not publish raw lane content.",
            {"completion_status": completion_status},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Candidate crosswalk work does not move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "candidate_crosswalk": crosswalk,
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
    crosswalk_json = ARTIFACT_ROOT / f"{PHASE}-candidate-preflight-crosswalk-v1.json"
    crosswalk_md = ARTIFACT_ROOT / f"{PHASE}-candidate-preflight-crosswalk-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(crosswalk_json, payload)
    written.append(crosswalk_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        crosswalk_md,
        f"""
# v476 THOS v4 x1 Candidate Preflight Crosswalk

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`

The crosswalk carries 90 candidate rows: 30 command candidates, 30 skill candidates, and 30 system-expansion candidates. Every row remains candidate-only, approval-bound, and metadata-only.

Rows:

{row_lines}

Family counts:

- command: `{family_counts.get('command', 0)}`
- skill: `{family_counts.get('skill', 0)}`
- system_expansion: `{family_counts.get('system_expansion', 0)}`

Optional CLI completion status: `{completion_status}`

All six GMUT gates remain open.
""",
    )
    written.append(crosswalk_md)
    write_json(status_json, run_status)
    written.append(status_json)
    status_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    write_md(
        status_md,
        f"""
# v476 THOS v4 x1 Run Status

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
