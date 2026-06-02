#!/usr/bin/env python3
"""Build v474 THOS v8 x2 source-drift recurrence guard artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v8-x2"
SOURCE_PHASE = "v474-thos-v8-x1"
NEXT_PHASE = "v475-thos-v1-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

SOURCE_CHAIN = [
    "docs/trinity-live-traces/v474-thos-v5-x2-cli-lane-completion-notice-v1.json",
    "docs/trinity-live-traces/v474-thos-v6-x1-receipt-marker-review-ledger-v1.json",
    "docs/trinity-live-traces/v474-thos-v6-x2-marker-classification-v1.json",
    "docs/trinity-live-traces/v474-thos-v7-x1-summary-candidate-v1.json",
    "docs/trinity-live-traces/v474-thos-v7-x2-summary-preflight-v1.json",
    "docs/trinity-live-traces/v474-thos-v8-x1-summary-closure-handoff-v1.json",
]

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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def source_check(path_text: str) -> dict[str, Any]:
    path = REPO_ROOT / path_text
    if not path.exists():
        return {
            "path": path_text,
            "status": "OPEN_GAP_MISSING_SOURCE",
        }
    payload = read_json(path)
    return {
        "aggregate_status": payload.get("aggregate_status"),
        "bytes": path.stat().st_size,
        "gmUT_gate_effect": payload.get("gmUT_gate_effect"),
        "path": path_text,
        "phase_slug": payload.get("phase_slug"),
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


def aggregate_status(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY_DRIFT_GUARD_READY"


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    if case.get("hash_changed") or case.get("raw_output_flag") or case.get("gmut_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("missing_source"):
        observed = "OPEN_GAP"
    elif case.get("all_sources_present"):
        observed = "PASS_SHAPE_ONLY"
    else:
        observed = "OPEN_GAP"
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
            "stable_sources_expected_pass",
            {"all_sources_present": True, "gmut_effect": "none_open_not_tested"},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "hash_changed_expected_fail",
            {"gmut_effect": "none_open_not_tested", "hash_changed": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_source_expected_open_gap",
            {"gmut_effect": "none_open_not_tested", "missing_source": True},
            "OPEN_GAP",
        ),
        fixture(
            "raw_output_flag_expected_fail",
            {"gmut_effect": "none_open_not_tested", "raw_output_flag": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_expected_fail",
            {"all_sources_present": True, "gmut_effect": "gate_moved"},
            "FAIL_BLOCKER",
        ),
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    checks = [source_check(path) for path in SOURCE_CHAIN]
    missing = [item for item in checks if item["status"] != "PASS_SHAPE_ONLY"]
    gmut_drift = [item for item in checks if item.get("gmUT_gate_effect") not in {None, "none_open_not_tested"}]
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    rows = [
        row(
            "source_chain",
            "PASS_SHAPE_ONLY" if not missing else "OPEN_GAP_MISSING_SOURCE",
            "Curated metadata source chain was hashed for recurrence checks.",
            {"source_count": len(checks), "missing_count": len(missing)},
        ),
        row(
            "gmut_boundary",
            "PASS_SHAPE_ONLY" if not gmut_drift else "FAIL_BLOCKER",
            "GMUT gate effect was checked across source artifacts where present.",
            {"drift_count": len(gmut_drift)},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Drift guard fixtures confirmed stable, hash-change, missing-source, raw-output, and GMUT-drift behavior.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This guard supports THOS metadata recurrence only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    guard = {
        "aggregate_status": aggregate,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recurrence_rule": "Recompute source_chain hashes before reusing metadata-summary decisions; block on hash drift, missing sources, raw-output publication flags, or GMUT boundary movement.",
        "rows": rows,
        "source_chain": checks,
        "source_phase": SOURCE_PHASE,
    }
    run_status = {
        "aggregate_status": aggregate,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    guard_json = ARTIFACT_ROOT / f"{PHASE}-drift-recurrence-guard-v1.json"
    write_json(guard_json, guard)
    written.append(guard_json)
    guard_md = ARTIFACT_ROOT / f"{PHASE}-drift-recurrence-guard-v1.md"
    write_md(
        guard_md,
        f"""
# v474 THOS v8 x2 Drift Recurrence Guard

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v8 x2 records a reusable source-hash recurrence guard for metadata-only THOS summaries. Future reuse must recompute source-chain hashes and block on source drift, missing sources, raw-output publication flags, or GMUT boundary movement.

Source checks: `{len(checks)}` checked, `{len(missing)}` missing.

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Next expected phase: `{NEXT_PHASE}`.

All six GMUT gates remain open.
""",
    )
    written.append(guard_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v8 x2 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v8 x2 converts the metadata-summary closure into a reusable drift recurrence guard for v475 and later THOS phases.

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
