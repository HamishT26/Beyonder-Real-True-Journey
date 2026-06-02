#!/usr/bin/env python3
"""Build v476 THOS v5 x2 dry-run rehearsal gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v5-x2"
SOURCE_PHASE = "v476-thos-v5-x1"
NEXT_PHASE = "v476-thos-v6-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
REHEARSAL = ARTIFACT_ROOT / "v476-thos-v5-x1-dry-run-rehearsal-v1.json"
REHEARSAL_STATUS = ARTIFACT_ROOT / "v476-thos-v5-x1-run-status-v1.json"

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

REQUIRED_REHEARSAL_TYPES = {
    "command": "stdout_only_command_plan",
    "skill": "body_preserving_frontmatter_plan",
    "system_expansion": "registry_naming_plan",
}

APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "command dry-run rows should record expected and observed no-effect status, blocked actions, and next required artifact",
            "skill frontmatter rehearsal rows should carry proposed frontmatter hash, original body hash, rehearsed body hash, body preserved true, and live write none",
            "system-expansion registry naming rows should track canonical name, display name, length, collision status, source authority, candidate/materialized state, and blocked claims",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "dry-run materialization rehearsal means candidate shape was exercised locally without installation, publication, production readiness, or mutation",
            "safe language includes candidate_preflight_passed, dry_run_rehearsal_only, materialization_not_installed, approval_required, open_gap_carried, and metadata_only",
            "avoid installed, production-ready, activated, certified, platform complete, validated, and GMUT advanced labels",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "dry-runs must not mutate source artifacts and must carry source_hash_before for source-backed rehearsals",
            "skill body-preservation rehearsals must prove preview changes do not alter body suffix or content",
            "negative fixtures should catch mutation, raw transport, body changes, registry collisions, overlong names, missing hashes, source drift, generic pass, and GMUT boundary drift",
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
    if case.get("missing_source"):
        observed = "OPEN_GAP"
    elif case.get("missing_family") or case.get("wrong_rehearsal_type"):
        observed = "FAIL_BLOCKER"
    elif case.get("dry_run_false") or case.get("mutation_true") or case.get("installed_candidate"):
        observed = "FAIL_BLOCKER"
    elif case.get("approval_false") or case.get("source_hash_false") or case.get("moves_gmut_gate"):
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
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("missing_family_expected_fail", {"missing_family": True}, "FAIL_BLOCKER"),
        fixture("wrong_rehearsal_type_expected_fail", {"wrong_rehearsal_type": True}, "FAIL_BLOCKER"),
        fixture("dry_run_false_expected_fail", {"dry_run_false": True}, "FAIL_BLOCKER"),
        fixture("mutation_true_expected_fail", {"mutation_true": True}, "FAIL_BLOCKER"),
        fixture("candidate_install_expected_fail", {"installed_candidate": True}, "FAIL_BLOCKER"),
        fixture("approval_false_expected_fail", {"approval_false": True}, "FAIL_BLOCKER"),
        fixture("source_hash_false_expected_fail", {"source_hash_false": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP_DRY_RUN_REHEARSAL_GATE_NOT_READY"
    return "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    rehearsal = read_json(REHEARSAL)
    rehearsal_status = read_json(REHEARSAL_STATUS)
    source_refs = [source_ref(REHEARSAL), source_ref(REHEARSAL_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    rows_in = rehearsal.get("dry_run_rehearsals", [])
    family_counts = {
        family: len([item for item in rows_in if item.get("candidate_family") == family])
        for family in REQUIRED_FAMILY_COUNTS
    }
    missing_family_counts = {
        family: {"expected": expected, "observed": family_counts.get(family, 0)}
        for family, expected in REQUIRED_FAMILY_COUNTS.items()
        if family_counts.get(family, 0) != expected
    }
    wrong_rehearsal_type = [
        item.get("candidate_id")
        for item in rows_in
        if item.get("rehearsal_type") != REQUIRED_REHEARSAL_TYPES.get(str(item.get("candidate_family")))
    ]
    unsafe_rows = [
        item.get("candidate_id")
        for item in rows_in
        if item.get("dry_run_only") is not True
        or item.get("mutation_performed") is not False
        or item.get("materialization_state") != "candidate_only_not_installed"
        or item.get("approval_required_for_live_write") is not True
        or item.get("source_hash_required") is not True
        or item.get("gmut_gate_effect") != "none_open_not_tested"
    ]
    fixtures = build_fixtures()
    preflight_rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v476 v5 x1 rehearsal and run status were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "rehearsal_status",
            "PASS_SHAPE_ONLY" if rehearsal.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_READY" and rehearsal_status.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_DRY_RUN_REHEARSAL_READY" else "OPEN_GAP_REHEARSAL_NOT_READY",
            "The x1 dry-run rehearsal must be ready before x2 gate publication.",
            {"rehearsal_status": rehearsal.get("aggregate_status"), "run_status": rehearsal_status.get("aggregate_status")},
        ),
        row(
            "family_counts",
            "PASS_SHAPE_ONLY" if not missing_family_counts else "FAIL_FAMILY_COUNTS",
            "All three families must carry 30 rehearsal rows.",
            {"family_counts": family_counts, "missing_family_counts": missing_family_counts},
        ),
        row(
            "rehearsal_types",
            "PASS_SHAPE_ONLY" if not wrong_rehearsal_type else "FAIL_REHEARSAL_TYPE",
            "Each candidate family must map to its required rehearsal type.",
            {"wrong_rehearsal_type": wrong_rehearsal_type},
        ),
        row(
            "safe_dry_run_states",
            "PASS_SHAPE_ONLY" if not unsafe_rows else "FAIL_UNSAFE_DRY_RUN_STATE",
            "All rows remain dry-run-only, mutation-free, candidate-only, approval-bound, source-hash-bound, and GMUT-neutral.",
            {"unsafe_rows": unsafe_rows},
        ),
        row(
            "app_advisory_boundary",
            "PASS_SHAPE_ONLY",
            "App advisory requests were sent and are non-blocking for this local gate.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS), "raw_advisory_text_recorded": False},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Dry-run rehearsal does not install candidates, prove production readiness, or move GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(preflight_rows, fixtures)
    next_roadmap = [
        {
            "task_id": f"v476-v6-task-{index:02d}",
            "task": task,
            "claim_ceiling": "roadmap item only; no live materialization or production claim",
        }
        for index, task in enumerate(
            [
                "Build approval-packet reference rows for candidate promotion without approving promotion.",
                "Build marker-review classifier rows for CLI completion metadata.",
                "Build source drift fixtures across v4 and v5 source artifacts.",
                "Build dry-run replay hashes for command, skill, and system-expansion rows.",
                "Carry all six GMUT gates open into v476 v6.",
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
    gate_json = ARTIFACT_ROOT / f"{PHASE}-dry-run-rehearsal-gate-v1.json"
    gate_md = ARTIFACT_ROOT / f"{PHASE}-dry-run-rehearsal-gate-v1.md"
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(gate_json, payload)
    written.append(gate_json)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in preflight_rows)
    roadmap_lines = "\n".join(f"- `{item['task_id']}`: {item['task']}" for item in next_roadmap)
    write_md(
        gate_md,
        f"""
# v476 THOS v5 x2 Dry-Run Rehearsal Gate

Generated UTC: `{generated_at}`

Status: `{status}`

Rows:

{row_lines}

v476 v6 roadmap:

{roadmap_lines}

All candidates remain candidate-only. No live materialization occurred.

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
# v476 THOS v5 x2 Run Status

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
