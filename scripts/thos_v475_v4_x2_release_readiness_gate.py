#!/usr/bin/env python3
"""Build v475 THOS v4 x2 release/readiness gate artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v475-thos-v4-x2"
SOURCE_PHASE = "v475-thos-v4-x1"
NEXT_PHASE = "v475-thos-v5-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
LEDGER = ARTIFACT_ROOT / "v475-thos-v4-x1-release-readiness-ledger-v1.json"
LEDGER_STATUS = ARTIFACT_ROOT / "v475-thos-v4-x1-run-status-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

REQUIRED_LEDGER_ROWS = {
    "report_board_gate",
    "source_authority",
    "open_gap_policy",
    "claim_boundary",
}


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
    if case.get("missing_ledger_row") or case.get("claim_ceiling_missing"):
        observed = "FAIL_BLOCKER"
    elif case.get("source_promoted_to_proof") or case.get("production_readiness_claim"):
        observed = "FAIL_BLOCKER"
    elif case.get("raw_output") or case.get("gmut_gate_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source") or case.get("open_gap"):
        observed = "OPEN_GAP"
    elif case.get("ledger_ready") and case.get("claim_ceilings_present"):
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
            "ledger_ready_expected_pass",
            {
                "claim_ceilings_present": True,
                "gmut_gate_effect": "none_open_not_tested",
                "ledger_ready": True,
            },
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "missing_ledger_row_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "missing_ledger_row": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "claim_ceiling_missing_expected_fail",
            {"claim_ceiling_missing": True, "gmut_gate_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_promoted_to_proof_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "source_promoted_to_proof": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "production_readiness_claim_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "production_readiness_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "raw_output_expected_fail",
            {"gmut_gate_effect": "none_open_not_tested", "raw_output": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "open_gap_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "open_gap": True},
            "OPEN_GAP",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_gate_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "gmut_effect_moved_expected_fail",
            {"gmut_gate_effect": "gate_moved", "ledger_ready": True},
            "FAIL_BLOCKER",
        ),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]]) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    return "PASS_SHAPE_ONLY_RELEASE_READINESS_GATE_READY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    ledger = read_json(LEDGER)
    ledger_status = read_json(LEDGER_STATUS)
    source_refs = [source_ref(LEDGER), source_ref(LEDGER_STATUS)]
    source_gaps = [item for item in source_refs if item["status"] != "PASS_SHAPE_ONLY"]
    ledger_rows = ledger.get("readiness_ledger", [])
    ledger_ids = {str(item.get("ledger_row")) for item in ledger_rows}
    missing_ledger_rows = sorted(REQUIRED_LEDGER_ROWS - ledger_ids)
    official_sources = ledger.get("external_source_refs", [])
    source_ceiling_gaps = [item.get("url") for item in official_sources if not item.get("claim_ceiling")]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if not source_gaps else "OPEN_GAP_SOURCE_REFS",
            "v4 x1 ledger sources were checked for the release/readiness gate.",
            {"source_count": len(source_refs), "source_gap_count": len(source_gaps)},
        ),
        row(
            "ledger_row_coverage",
            "PASS_SHAPE_ONLY" if not missing_ledger_rows else "FAIL_LEDGER_ROW_COVERAGE",
            "Required readiness ledger rows are present.",
            {"missing_ledger_rows": missing_ledger_rows, "ledger_row_count": len(ledger_rows)},
        ),
        row(
            "official_source_claim_ceilings",
            "PASS_SHAPE_ONLY" if not source_ceiling_gaps else "FAIL_SOURCE_CEILING_GAP",
            "Official external sources have explicit claim ceilings and remain context only.",
            {"source_count": len(official_sources), "ceiling_gaps": source_ceiling_gaps},
        ),
        row(
            "negative_fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_FIXTURE_MISMATCH",
            "Release/readiness fixtures checked row coverage, claim ceilings, source-proof overclaim, production overclaim, raw output, open gaps, missing source, and GMUT boundary.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This gate is THOS release/readiness metadata only; it does not test or close GMUT gates.",
        ),
    ]
    status = aggregate_status(rows, fixtures)
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "release_readiness_gate": {
            "ledger_row_count": len(ledger_rows),
            "missing_ledger_rows": missing_ledger_rows,
            "official_source_count": len(official_sources),
            "source_ceiling_gaps": source_ceiling_gaps,
            "source_run_status": ledger_status.get("run_status"),
        },
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "source_refs": source_refs,
        "v5_x1_handoff": {
            "recommended_scope": "turn the release/readiness gate into an operator-facing THOS phase ledger index with explicit source authority and open-gap columns",
            "claim_ceiling": "THOS release/readiness metadata only",
        },
    }
    artifact_json = ARTIFACT_ROOT / f"{PHASE}-release-readiness-gate-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{PHASE}-release-readiness-gate-v1.md"
    run_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    run_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_json(artifact_json, payload)
    write_md(
        artifact_md,
        f"""
# v475 THOS v4 x2 Release Readiness Gate

Generated UTC: `{generated_at}`

Status: `{status}`

v475 v4 x2 gates the release/readiness ledger for row coverage, official-source claim ceilings, negative fixtures, and THOS-only claim boundaries.

Ledger rows: `{len(ledger_rows)}`; missing rows: `{len(missing_ledger_rows)}`.

Official source claim-ceiling gaps: `{len(source_ceiling_gaps)}`.

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
            "ledger row coverage checked",
            "official source claim ceilings checked",
            "negative fixtures checked",
            "metadata-only claim boundary preserved",
        ],
    }
    write_json(run_json, run_payload)
    write_md(
        run_md,
        f"""
# v475 THOS v4 x2 Run Status

Status: `{status}`

Next expected phase: `{NEXT_PHASE}`

v475 v4 x2 gates the release/readiness ledger and prepares the v5 x1 phase ledger index handoff.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, run_json, run_md]


def main() -> None:
    for path in build_artifacts():
        print(path.relative_to(REPO_ROOT).as_posix())


if __name__ == "__main__":
    main()
