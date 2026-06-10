#!/usr/bin/env python3
"""Build v476 THOS v1 x1 suite-map seed artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v476-thos-v1-x1"
SOURCE_PHASE = "v475-thos-v8-x2"
NEXT_PHASE = "v476-thos-v1-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
HANDOFF = ARTIFACT_ROOT / "v475-thos-v8-x2-v476-handoff-ledger-v1.json"
HANDOFF_STATUS = ARTIFACT_ROOT / "v475-thos-v8-x2-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SURFACE_SPECS = [
    {
        "claim_ceiling": "repo-local Python script count only",
        "surface_id": "repo_scripts",
        "surface_type": "script_surface",
    },
    {
        "claim_ceiling": "repo-local command-book file count only",
        "surface_id": "command_books",
        "surface_type": "command_surface",
    },
    {
        "claim_ceiling": "repo-local API-book file count only",
        "surface_id": "api_books",
        "surface_type": "api_surface",
    },
    {
        "claim_ceiling": "user skill manifest count only",
        "surface_id": "user_skill_manifests",
        "surface_type": "skill_surface",
    },
    {
        "claim_ceiling": "plugin skill manifest count only",
        "surface_id": "plugin_skill_manifests",
        "surface_type": "plugin_skill_surface",
    },
    {
        "claim_ceiling": "repo-local expansion artifact count only",
        "surface_id": "trinity_expansion_docs",
        "surface_type": "system_expansion_surface",
    },
    {
        "claim_ceiling": "repo-local live trace count only",
        "surface_id": "trinity_live_traces",
        "surface_type": "receipt_surface",
    },
    {
        "claim_ceiling": "repo-local dashboard data count only",
        "surface_id": "dashboard_data_files",
        "surface_type": "dashboard_surface",
    },
]

APP_ADVISORY_SYNTHESIS = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "suite-map rows should include surface identity, type, scope, source authority, freshness, guard requirements, negative fixtures, and GMUT effect",
            "safe evidence is curated metadata counts, receipt IDs, source hashes, remote-verified commits, manifest refs, checker statuses, dashboard row counts, and guard verdicts",
            "blocked material includes lane transport, runtime text, temp transport, session streams, image captures, private auth material, sensitive paths, unreviewed cache bodies, and connector write payloads",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "suite-map language should frame orientation and readiness context, not mastery or production completion",
            "counts are inventory evidence only and do not imply safe commands, approved connector writes, production dashboards, truth, quality, or publication clearance",
            "open gaps include connector authority, destructive cleanup authority, skill safety, freshness uncertainty, and raw sibling output nonpublication",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "required rows include command registry, skill loader health, script inventory, connector/plugin boundary, dashboard sync, receipt freshness, publication guard, negative fixture coverage, source-hash chain, and GMUT-open boundary",
            "validation should require source hashes, metadata-only scan mode, false raw-output flags, false mutation flags, and explicit blocked claims",
            "v1 x2 should harden required-row matrix, surface-family enums, source-hash checks, freshness checks, fixture report, and handoff risk ledger",
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


def count_files(root: Path, pattern: str = "*") -> int:
    if not root.exists():
        return 0
    return sum(1 for item in root.rglob(pattern) if item.is_file())


def scan_surface_counts() -> dict[str, int]:
    docs = REPO_ROOT / "docs"
    codex_root = Path.home() / ".codex"
    return {
        "api_books": len(list(docs.glob("trinity-api-book-v*.json"))),
        "command_books": len(list(docs.glob("trinity-command-book-v*.json"))),
        "dashboard_data_files": count_files(REPO_ROOT / "control-plane", "*.json"),
        "plugin_skill_manifests": count_files(codex_root / "plugins" / "cache", "SKILL.md"),
        "repo_scripts": len(list((REPO_ROOT / "scripts").glob("*.py"))),
        "trinity_expansion_docs": count_files(docs / "trinity-expansion"),
        "trinity_live_traces": count_files(docs / "trinity-live-traces"),
        "user_skill_manifests": count_files(codex_root / "skills", "SKILL.md"),
    }


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def candidate_rows(prefix: str, label: str, count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, count + 1):
        rows.append(
            {
                "candidate_id": f"{prefix}-{index:02d}",
                "candidate_label": f"{label} {index:02d}",
                "claim_ceiling": "candidate planning row only; not installed or promoted",
                "materialization_state": "candidate_only_not_installed",
                "next_action": "preflight in v476-thos-v1-x2 before any live materialization",
                "raw_material_boundary": "no runtime captures, transport bodies, session streams, or private material",
            }
        )
    return rows


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("candidate_count_low"):
        observed = "OPEN_GAP"
    elif case.get("raw_material") or case.get("installed_without_preflight") or case.get("broad_stage"):
        observed = "FAIL_BLOCKER"
    elif case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("suite_map_ready") and case.get("candidate_only"):
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
            "suite_map_candidate_expected_pass",
            {"candidate_only": True, "gmut_gate_effect": "none_open_not_tested", "suite_map_ready": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "candidate_count_low_expected_open_gap",
            {"candidate_count_low": True, "gmut_gate_effect": "none_open_not_tested"},
            "OPEN_GAP",
        ),
        fixture(
            "raw_material_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_material": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "installed_without_preflight_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "installed_without_preflight": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "broad_stage_expected_fail",
            {"broad_stage": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_gate_move_expected_fail",
            {"candidate_only": True, "gmut_gate_effect": "gate_moved", "suite_map_ready": True},
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_V476_SUITE_MAP_SEED_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    handoff = read_json(HANDOFF)
    handoff_status = read_json(HANDOFF_STATUS)
    source_refs = [source_ref(HANDOFF), source_ref(HANDOFF_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    counts = scan_surface_counts()
    surface_rows = [
        {
            **surface,
            "observed_count": counts.get(surface["surface_id"], 0),
            "status": "PASS_SHAPE_ONLY" if counts.get(surface["surface_id"], 0) > 0 else "OPEN_GAP_EMPTY_SURFACE",
        }
        for surface in SURFACE_SPECS
    ]
    expansions = candidate_rows("expansion", "THOS System Expansion Candidate", 30)
    commands = candidate_rows("command", "THOS Command Candidate", 30)
    skills = candidate_rows("skill", "THOS Skill Candidate", 30)
    candidate_totals = {
        "command_candidates": len(commands),
        "skill_candidates": len(skills),
        "system_expansion_candidates": len(expansions),
    }
    count_gaps = {key: value for key, value in candidate_totals.items() if value < 30}
    fixtures = build_fixtures()
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v475 handoff and run-status sources were checked.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "handoff_ready",
            "PASS_SHAPE_ONLY" if handoff.get("aggregate_status") == "PASS_SHAPE_ONLY_V476_HANDOFF_READY" else "OPEN_GAP_HANDOFF_NOT_READY",
            "v475 must hand off cleanly before v476 suite-map seeding.",
            {"handoff_status": handoff.get("aggregate_status"), "run_status": handoff_status.get("aggregate_status")},
        ),
        row(
            "surface_counts",
            "PASS_SHAPE_ONLY" if all(item["observed_count"] > 0 for item in surface_rows) else "OPEN_GAP_EMPTY_SURFACE",
            "Core THOS surfaces were counted as metadata only.",
            {"surface_count": len(surface_rows), "empty_surface_count": sum(1 for item in surface_rows if item["observed_count"] == 0)},
        ),
        row(
            "candidate_counts",
            "PASS_SHAPE_ONLY" if not count_gaps else "OPEN_GAP_CANDIDATE_COUNTS",
            "v476 x1 includes 30 candidate rows each for expansions, commands, and skills.",
            candidate_totals,
        ),
        row(
            "materialization_boundary",
            "PASS_SHAPE_ONLY",
            "Candidate rows are not installed, downloaded, or promoted until a later preflight authorizes exact materialization.",
            {"candidate_only": True, "installed_now": False},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "THOS suite-map counts and candidates do not validate GMUT or close GMUT gates.",
            {"gmut_gate_effect": "none_open_not_tested", "gmut_gates_open": GMUT_GATES},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded as sanitized metadata-only guidance.",
            {"advisory_count": len(APP_ADVISORY_SYNTHESIS), "raw_advisory_text_recorded": False},
        ),
    ]
    aggregate = aggregate_status(rows, fixtures)
    suite_map = {
        "aggregate_status": aggregate,
        "app_advisory_synthesis": APP_ADVISORY_SYNTHESIS,
        "candidate_totals": candidate_totals,
        "command_candidates": commands,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "skill_candidates": skills,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "surface_counts": counts,
        "surface_rows": surface_rows,
        "system_expansion_candidates": expansions,
        "v475_handoff_tasks": handoff.get("v476_handoff_tasks", []),
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }
    written: list[Path] = []
    suite_json = ARTIFACT_ROOT / f"{PHASE}-suite-map-seed-v1.json"
    write_json(suite_json, suite_map)
    written.append(suite_json)
    suite_md = ARTIFACT_ROOT / f"{PHASE}-suite-map-seed-v1.md"
    surface_lines = "\n".join(
        f"- {item['surface_id']}: `{item['observed_count']}` ({item['surface_type']})"
        for item in surface_rows
    )
    write_md(
        suite_md,
        f"""
# v476 THOS v1 x1 Suite-Map Seed

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v476 starts with a safe metadata-only suite map. It counts existing THOS surfaces and seeds candidate-only rows for future preflight, without installing skills, creating commands, publishing transport, or promoting capability claims.

Surface counts:

{surface_lines}

Candidate rows:

- System expansion candidates: `{len(expansions)}`
- Command candidates: `{len(commands)}`
- Skill candidates: `{len(skills)}`

App advisories folded: `{len(APP_ADVISORY_SYNTHESIS)}`

Next expected phase: `{NEXT_PHASE}`

All six GMUT gates remain open.
""",
    )
    written.append(suite_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v476 THOS v1 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v476 v1 x1 seeds a THOS suite map across scripts, command/API books, user/plugin skills, expansion docs, live traces, and dashboard data. Candidate expansion/command/skill rows are planning-only and not installed.

Cicero, Kierkegaard, and Aristotle advisories were folded as sanitized metadata-only guidance.

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
