#!/usr/bin/env python3
"""Build v474 THOS v4 x2 combined publication preflight artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v4-x2"
SOURCE_GUARD_PHASE = "v474-thos-v3-x2"
SOURCE_ALLOWLIST_PHASE = "v474-thos-v4-x1"
NEXT_PHASE = "v474-thos-v5-x1"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_PREFLIGHT_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "preflight row ordering must start with phase identity and drift checks",
            "exact-stage proof supports only staged-set matching, not publication authority",
            "raw runtime material in staged artifacts is a blocker",
            "marker review pending without raw leak remains open gap",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "combined preflight is a narrow permission check, not a pressure machine",
            "wait and open-gap-carried must remain valid outcomes",
            "privacy and marker-review holds dominate allowlist membership",
            "allowlist completion must not imply unresolved matters are done",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "candidate refs, expected refs, and allowlist refs should match as sets",
            "status precedence must be deterministic",
            "expected-fail confirmation is fixture-only",
            "generic pass status is invalid",
        ],
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"].startswith("OPEN_GAP") for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    guard = read_json(ARTIFACT_ROOT / f"{SOURCE_GUARD_PHASE}-publication-guard-v1.json")
    allowlist = read_json(ARTIFACT_ROOT / f"{SOURCE_ALLOWLIST_PHASE}-staged-allowlist-validator-v1.json")
    guard_status = guard.get("aggregate_status", "MISSING")
    allowlist_status = allowlist.get("aggregate_status", "MISSING")
    blocking_lanes = guard.get("blocking_lanes", [])

    preflight_steps = [
        "record phase identity, local head, expected remote head, and branch context",
        "confirm local and remote heads match before staging",
        "derive exact current-phase allowlist before any add operation",
        "stage only current-phase allowlisted paths",
        "run JSON parse and script compile checks",
        "run path, credential-pattern, raw-output, visual-capture, and session-material guard scans",
        "run staged diff review and whitespace check",
        "block combined publication while any lane remains marker-review required",
        "commit and push only after drift remains zero",
        "verify remote equals local after push",
    ]
    deterministic_schema = {
        "required_inputs": [
            "phase_ref",
            "publication_guard_ref",
            "staged_allowlist_ref",
            "candidate_artifact_refs",
            "expected_artifact_refs",
            "checksum_refs",
            "raw_text_published_false",
            "broad_status_scan_performed_false",
            "gmUT_gate_effect_none_open_not_tested",
        ],
        "status_precedence": [
            "FAIL_BLOCKER",
            "REVIEW_REQUIRED",
            "OPEN_GAP",
            "PASS_SHAPE_ONLY",
            "NOT_RUN",
        ],
        "carry_forward_statuses": [
            "marker_review_pending",
            "privacy_hold",
            "open_gap_carried",
            "wait_no_rush",
            "blocked_exact_scope",
        ],
    }
    rows = [
        row(
            "publication_guard",
            guard_status,
            "v3 x2 publication guard remains authoritative for lane publication status.",
            {"blocking_lane_count": len(blocking_lanes)},
        ),
        row(
            "staged_allowlist",
            allowlist_status,
            "v4 x1 staged allowlist validator confirms exact current-phase package checking.",
            {"fixture_count": len(allowlist.get("fixtures", []))},
        ),
        row(
            "app_advisories",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into this preflight synthesis.",
            {"advisory_count": len(APP_PREFLIGHT_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Combined preflight governs THOS publication hygiene only; GMUT gates remain open.",
        ),
    ]
    preflight = {
        "aggregate_status": aggregate(rows),
        "app_preflight_advisories": APP_PREFLIGHT_ADVISORIES,
        "deterministic_schema": deterministic_schema,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "preflight_steps": preflight_steps,
        "rows": rows,
        "source_allowlist_phase": SOURCE_ALLOWLIST_PHASE,
        "source_guard_phase": SOURCE_GUARD_PHASE,
    }
    run_status = {
        "aggregate_status": preflight["aggregate_status"],
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    preflight_json = ARTIFACT_ROOT / f"{PHASE}-combined-preflight-synthesis-v1.json"
    write_json(preflight_json, preflight)
    written.append(preflight_json)
    preflight_md = ARTIFACT_ROOT / f"{PHASE}-combined-preflight-synthesis-v1.md"
    write_md(
        preflight_md,
        f"""
# v474 THOS v4 x2 Combined Publication Preflight

Generated UTC: `{generated_at}`

Status: `{preflight['aggregate_status']}`

The combined preflight synthesizes the v3 x2 publication guard with the v4 x1 staged-allowlist validator. It preserves the marker-review hold: Arby remains blocked, while Aster Vale remains metadata-only.

App advisory status: `ADVISORY_RECEIVED`

All six GMUT gates remain open.
""",
    )
    written.append(preflight_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v4 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v4 x2 combines the publication guard and staged-allowlist validator into a reusable preflight sequence. App advisories were received and folded in as summary-only guard design constraints.

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
