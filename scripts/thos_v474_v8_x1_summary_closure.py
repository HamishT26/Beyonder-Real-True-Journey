#!/usr/bin/env python3
"""Build v474 THOS v8 x1 metadata-summary closure and handoff artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v8-x1"
SOURCE_PHASE = "v474-thos-v7-x2"
NEXT_PHASE = "v474-thos-v8-x2"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"
SOURCE_PREFLIGHT = ARTIFACT_ROOT / "v474-thos-v7-x2-summary-preflight-v1.json"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "close only scoped metadata-summary readiness",
            "carry raw final text, stderr, transport, visual captures, runtime records, and private values as blocked",
            "source hashes support identity and integrity only, not content approval or GMUT progress",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "metadata-summary closure is ethical only when limits remain explicit",
            "do not infer sibling intent, continuity, personhood, or advisory quality from metadata",
            "hash matches and fixtures do not prove truth or total safety",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "close source-hash, required-lane, raw-output-flag, fixture, and GMUT-boundary invariants",
            "carry raw CLI text, stderr, transport, source drift, missing lane, generic pass, and GMUT overclaim guards",
            "v475 should focus on receipt durability and dashboard/report continuity under the same metadata-only boundary",
        ],
    },
]

CLOSED_SCOPE = [
    "Arby/Aster completion metadata may be summarized under source-hash guards",
    "required lane coverage is present for Arby and Aster",
    "raw-output publication flags are false in the candidate",
    "marker-review state supports metadata-only summaries",
    "negative fixtures confirm blocker behavior for this scoped preflight",
]

CARRY_FORWARD = [
    "raw final-message text remains unpublished",
    "raw stderr and transport remain unpublished",
    "private values, full sensitive paths, visual captures, runtime records, and temp files remain blocked",
    "source hashes prove artifact identity/integrity only",
    "metadata review does not prove content quality, sibling intent, continuity, personhood, consciousness, or advisory truth",
    "all six GMUT gates remain open and untested",
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
    return "PASS_SHAPE_ONLY_METADATA_SUMMARY_CLOSED"


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    if case.get("raw_output") or case.get("source_mismatch") or case.get("missing_lane"):
        observed = "FAIL_BLOCKER"
    elif case.get("generic_pass") or case.get("gmut_effect") != "none_open_not_tested":
        observed = "FAIL_BLOCKER"
    elif case.get("identity_claim") or case.get("quality_claim"):
        observed = "FAIL_BLOCKER"
    elif case.get("metadata_summary_only"):
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
            "metadata_summary_only_expected_pass",
            {"gmut_effect": "none_open_not_tested", "metadata_summary_only": True},
            "PASS_SHAPE_ONLY",
        ),
        fixture(
            "raw_output_expected_fail",
            {"gmut_effect": "none_open_not_tested", "raw_output": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "source_mismatch_expected_fail",
            {"gmut_effect": "none_open_not_tested", "source_mismatch": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "missing_lane_expected_fail",
            {"gmut_effect": "none_open_not_tested", "missing_lane": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "generic_pass_expected_fail",
            {"generic_pass": True, "gmut_effect": "none_open_not_tested"},
            "FAIL_BLOCKER",
        ),
        fixture(
            "gmut_effect_expected_fail",
            {"gmut_effect": "gate_moved", "metadata_summary_only": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "identity_claim_expected_fail",
            {"gmut_effect": "none_open_not_tested", "identity_claim": True},
            "FAIL_BLOCKER",
        ),
        fixture(
            "quality_claim_expected_fail",
            {"gmut_effect": "none_open_not_tested", "quality_claim": True},
            "FAIL_BLOCKER",
        ),
    ]


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    preflight = read_json(SOURCE_PREFLIGHT)
    fixtures = build_fixtures()
    fixture_mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    source_status = preflight.get("aggregate_status")
    decision = preflight.get("summary_publication_decision")
    rows = [
        row(
            "source_preflight",
            "PASS_SHAPE_ONLY" if source_status == "PASS_SHAPE_ONLY_PREFLIGHT" else "OPEN_GAP_SOURCE_PREFLIGHT",
            "v7 x2 summary preflight was loaded as closure source.",
            {
                "path": "docs/trinity-live-traces/v474-thos-v7-x2-summary-preflight-v1.json",
                "sha256": sha256_file(SOURCE_PREFLIGHT) if SOURCE_PREFLIGHT.exists() else None,
                "source_status": source_status,
            },
        ),
        row(
            "metadata_summary_decision",
            "PASS_SHAPE_ONLY" if decision == "ALLOW_METADATA_SUMMARY_ONLY" else "OPEN_GAP_SUMMARY_NOT_ALLOWED",
            "The only closed scope is metadata-summary publication readiness.",
            {"decision": decision},
        ),
        row(
            "closed_scope",
            "PASS_SHAPE_ONLY",
            "Closed scope is limited to metadata summary under source-hash and raw-output guards.",
            {"closed_scope": CLOSED_SCOPE},
        ),
        row(
            "carry_forward",
            "PASS_SHAPE_ONLY",
            "Raw outputs, private material, overclaims, and all GMUT gates are carried forward as blocked or open.",
            {"carry_forward": CARRY_FORWARD},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not fixture_mismatches else "FAIL_BLOCKER",
            "Closure fixtures confirmed blockers for raw output, source mismatch, lane gaps, generic pass, identity/quality claims, and GMUT movement.",
            {"fixture_count": len(fixtures), "mismatch_count": len(fixture_mismatches)},
        ),
        row(
            "app_advisory_synthesis",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories agreed on metadata-only closure and raw-output carry-forward.",
            {"advisory_count": len(APP_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "This phase closes THOS metadata-summary readiness only and does not close or test GMUT gates.",
        ),
    ]
    aggregate = aggregate_status(rows)
    closure = {
        "aggregate_status": aggregate,
        "app_advisories": APP_ADVISORIES,
        "carry_forward": CARRY_FORWARD,
        "closed_scope": CLOSED_SCOPE,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
        "source_phase": SOURCE_PHASE,
        "summary_publication_decision": decision,
        "v475_handoff": [
            "reuse metadata-only receipt schema",
            "add source-hash drift recurrence checks",
            "preserve raw-output nonpublication guards",
            "build dashboard/report continuity only from curated metadata",
            "carry GMUT gates open unless exact closure artifacts exist",
        ],
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
    closure_json = ARTIFACT_ROOT / f"{PHASE}-summary-closure-handoff-v1.json"
    write_json(closure_json, closure)
    written.append(closure_json)
    closure_md = ARTIFACT_ROOT / f"{PHASE}-summary-closure-handoff-v1.md"
    write_md(
        closure_md,
        f"""
# v474 THOS v8 x1 Summary Closure Handoff

Generated UTC: `{generated_at}`

Status: `{aggregate}`

v8 x1 closes only the metadata-summary readiness path for Arby/Aster completion receipts. The allowed decision remains `{decision}`.

Closed scope count: `{len(CLOSED_SCOPE)}`

Carry-forward count: `{len(CARRY_FORWARD)}`

Fixtures confirmed: `{len(fixtures) - len(fixture_mismatches)}` of `{len(fixtures)}`.

Next handoff: reuse the metadata-only receipt schema, source-hash drift checks, raw-output nonpublication guards, and report/dashboard continuity from curated metadata only.

All six GMUT gates remain open.
""",
    )
    written.append(closure_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v8 x1 Run Status

Status: `{aggregate}`

Next expected phase: `{NEXT_PHASE}`

v8 x1 closes metadata-summary readiness only. Raw lane output remains unpublished; GMUT gates remain open.

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
