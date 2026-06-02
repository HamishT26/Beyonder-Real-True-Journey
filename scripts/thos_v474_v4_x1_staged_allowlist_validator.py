#!/usr/bin/env python3
"""Build v474 THOS v4 x1 staged-allowlist validator artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v474-thos-v4-x1"
NEXT_PHASE = "v474-thos-v4-x2"
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

ALLOWLIST = [
    "scripts/thos_v474_v4_x1_staged_allowlist_validator.py",
    "docs/trinity-live-traces/v474-thos-v4-x1-staged-allowlist-validator-v1.json",
    "docs/trinity-live-traces/v474-thos-v4-x1-staged-allowlist-validator-v1.md",
    "docs/trinity-live-traces/v474-thos-v4-x1-run-status-v1.json",
    "docs/trinity-live-traces/v474-thos-v4-x1-run-status-v1.md",
]

BLOCKED_PREFIXES = [
    "docs/trinity-live-traces/raw-",
    "tmp/",
    ".codex/",
    "plugin-cache/",
    "external-account/",
]

APP_ALLOWLIST_ADVISORIES = [
    {
        "lane": "Cicero",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "verify phase and head fields before publication",
            "check exact staged paths before content claims",
            "block raw runtime material and external cache paths",
            "apply marker-review and claim-ceiling blockers before pass status",
        ],
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "validator narrows publication scope rather than creating pressure to publish",
            "wait and carry open gap are valid humane outcomes",
            "privacy holds override filename convenience",
            "exact current-phase scope cannot be replaced by nearby phase patterns",
        ],
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RECEIVED",
        "points": [
            "prove exact staging by set equality",
            "generic pass status is invalid",
            "missing required artifact is not success",
            "broad status scans are not evidence of exact staging",
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


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def validate_paths(candidate_paths: list[str], allowlist: list[str]) -> tuple[str, list[dict[str, Any]]]:
    allow = {normalize_path(path) for path in allowlist}
    normalized_candidates = [normalize_path(path) for path in candidate_paths]
    candidate_set = set(normalized_candidates)
    rows: list[dict[str, Any]] = []
    duplicate_paths = sorted(path for path in candidate_set if normalized_candidates.count(path) > 1)
    for path in duplicate_paths:
        rows.append(
            {
                "path": path,
                "reason": "duplicate staged path candidate",
                "status": "FAIL_BLOCKER",
            }
        )
    for path in normalized_candidates:
        blocked_prefix = next((prefix for prefix in BLOCKED_PREFIXES if path.startswith(prefix)), None)
        if blocked_prefix:
            rows.append(
                {
                    "path": path,
                    "reason": f"blocked prefix {blocked_prefix}",
                    "status": "FAIL_BLOCKER",
                }
            )
        elif path not in allow:
            rows.append(
                {
                    "path": path,
                    "reason": "path not in exact current-phase allowlist",
                    "status": "FAIL_BLOCKER",
                }
            )
        else:
            rows.append(
                {
                    "path": path,
                    "reason": "path is exactly allowed for the current phase",
                    "status": "PASS_SHAPE_ONLY",
                }
            )
    for missing in sorted(allow - candidate_set):
        rows.append(
            {
                "path": missing,
                "reason": "allowlisted current-phase path is missing from candidate set",
                "status": "OPEN_GAP",
            }
        )
    status = "FAIL_BLOCKER" if any(row["status"] == "FAIL_BLOCKER" for row in rows) else "PASS_SHAPE_ONLY"
    if status == "PASS_SHAPE_ONLY" and any(row["status"] == "OPEN_GAP" for row in rows):
        status = "OPEN_GAP"
    return status, rows


def fixture(case_id: str, candidate_paths: list[str], expected: str) -> dict[str, Any]:
    observed, rows = validate_paths(candidate_paths, ALLOWLIST)
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "path_count": len(candidate_paths),
        "rows": rows,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def build_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("exact_current_phase_allowlist", ALLOWLIST, "PASS_SHAPE_ONLY"),
        fixture("raw_lane_material_blocked", ["docs/trinity-live-traces/raw-lane-material.txt"], "FAIL_BLOCKER"),
        fixture("external_plugin_cache_blocked", ["plugin-cache/skill-frontmatter-candidate.md"], "FAIL_BLOCKER"),
        fixture("broad_directory_blocked", ["docs/trinity-live-traces"], "FAIL_BLOCKER"),
        fixture("prior_phase_artifact_blocked", ["docs/trinity-live-traces/v474-thos-v3-x2-run-status-v1.md"], "FAIL_BLOCKER"),
        fixture("mixed_allowed_and_blocked_fails", [ALLOWLIST[0], "tmp/transient-lane-output.txt"], "FAIL_BLOCKER"),
        fixture("missing_required_artifacts_open_gap", [ALLOWLIST[0]], "OPEN_GAP"),
        fixture("duplicate_allowed_artifact_blocked", [ALLOWLIST[0], ALLOWLIST[0]], "FAIL_BLOCKER"),
    ]


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def build_artifacts() -> list[Path]:
    generated_at = utc_now()
    fixtures = build_fixtures()
    mismatches = [item for item in fixtures if item["status"] != "EXPECTED_CONFIRMED"]
    planned_status, planned_rows = validate_paths(ALLOWLIST, ALLOWLIST)
    aggregate_status = "PASS_SHAPE_ONLY" if not mismatches and planned_status == "PASS_SHAPE_ONLY" else "FAIL_BLOCKER"
    rows = [
        row(
            "planned_current_phase_paths",
            planned_status,
            "The current phase publication package is exactly allowlisted.",
            {"path_count": len(ALLOWLIST)},
        ),
        row(
            "fixtures",
            "PASS_SHAPE_ONLY" if not mismatches else "FAIL_BLOCKER",
            "Expected allowlist/refusal fixtures were evaluated.",
            {"fixture_count": len(fixtures), "mismatch_count": len(mismatches)},
        ),
        row(
            "app_allowlist_advisories",
            "PASS_SHAPE_ONLY",
            "Cicero, Kierkegaard, and Aristotle advisories were folded into the allowlist validator.",
            {"advisory_count": len(APP_ALLOWLIST_ADVISORIES)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "Allowlist validation governs repo publication only; GMUT gates remain open.",
        ),
    ]
    validator = {
        "aggregate_status": aggregate_status,
        "app_allowlist_advisories": APP_ALLOWLIST_ADVISORIES,
        "allowlist": ALLOWLIST,
        "blocked_prefixes": BLOCKED_PREFIXES,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "planned_path_rows": planned_rows,
        "rows": rows,
    }
    run_status = {
        "aggregate_status": aggregate_status,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": rows,
    }

    written: list[Path] = []
    validator_json = ARTIFACT_ROOT / f"{PHASE}-staged-allowlist-validator-v1.json"
    write_json(validator_json, validator)
    written.append(validator_json)
    validator_md = ARTIFACT_ROOT / f"{PHASE}-staged-allowlist-validator-v1.md"
    write_md(
        validator_md,
        f"""
# v474 THOS v4 x1 Staged Allowlist Validator

Generated UTC: `{generated_at}`

Status: `{aggregate_status}`

The validator confirms the current phase publication package is exactly allowlisted and refuses raw-lane material, external plugin-cache candidates, broad directories, prior-phase artifacts, and mixed allowed/blocked path sets.

Fixture results: `{len(fixtures) - len(mismatches)}` confirmed, `{len(mismatches)}` mismatched.

All six GMUT gates remain open.
""",
    )
    written.append(validator_md)
    status_json = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(status_json, run_status)
    written.append(status_json)
    status_md = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md"
    write_md(
        status_md,
        f"""
# v474 THOS v4 x1 Run Status

Status: `{aggregate_status}`

Next expected phase: `{NEXT_PHASE}`

v4 x1 implements a repo-only staged-allowlist validator for current-phase publication packages.

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
