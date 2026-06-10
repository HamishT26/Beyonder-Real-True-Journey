#!/usr/bin/env python3
"""Build v472 THOS v7 x1 executable semantic contradiction lint artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


PHASE = "v472-thos-v7-x1"
NEXT_PHASE = "v472-thos-v7-x2"
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

APP_ADVISORIES = [
    {
        "lane": "Cicero",
        "submission_id": "019e88cd-703a-7bb1-933e-73c55e258bc1",
        "status": "ADVISORY_RETURNED",
        "summary": "Define claim-boundary fixtures for GMUT gates, observer evidence, held lanes, blockers, dry-run cleanup, freshness, and publication lint.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e88cd-708e-7350-b5f2-de22b68820c1",
        "status": "ADVISORY_RETURNED",
        "summary": "Carry false-positive and false-negative risk, freshness labels, authority labels, and the THOS-vs-GMUT claim ceiling.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e88cd-7096-7251-a6ae-c93674288cf7",
        "status": "ADVISORY_RETURNED",
        "summary": "Use summary-only receipts, contradiction codes, expected fixtures, blocked claims, and no raw transport publication.",
    },
]

CLI_NATURAL_LANES = [
    {"lane": "Arby", "status": "NATURAL_DURATION_LAUNCHED"},
    {"lane": "Aster Vale", "status": "NATURAL_DURATION_LAUNCHED"},
]

RULES = [
    {
        "rule_id": "gmUT_validation_with_open_gates",
        "left": r"\bvalidated\b|\bvalidation\b",
        "right": r"gates?\s+remain\s+open|GMUT\s+gates?\s+remain\s+open",
        "message": "GMUT validation language conflicts with open-gate status.",
    },
    {
        "rule_id": "observer_evidence_as_publication",
        "left": r"observer[- ]only|browser\s+smoke|image\s+capture",
        "right": r"publication\s+verified|mutation\s+verified|live\s+write\s+verified",
        "message": "Observer evidence cannot certify publication, mutation, or live write.",
    },
    {
        "rule_id": "held_lane_restored_without_receipt",
        "left": r"\bheld\b|\bstandby\b",
        "right": r"\brestored\b|\breconnected\b",
        "message": "Held or standby lanes need explicit restoration receipts before restored language.",
    },
    {
        "rule_id": "completion_masks_blocker",
        "left": r"\bcomplete\b|\bclosed\b",
        "right": r"\bblocked\b|\bopen_gap\b",
        "message": "Completion language cannot mask blocker or open-gap status.",
    },
    {
        "rule_id": "dry_run_implies_deletion",
        "left": r"dry[- ]run|inspect(?:ion)?\s+only",
        "right": r"\bdeleted\b|\bremoved\b|\bcleaned\b",
        "message": "Dry-run inspection cannot imply deletion or cleanup.",
    },
    {
        "rule_id": "cached_claims_current",
        "left": r"\bcached\b|\bhistorical\b|\bprior\b",
        "right": r"\bcurrent\b|\blive\b|\bactive\b",
        "message": "Cached or prior evidence needs freshness proof before current/live claims.",
    },
]

EXPECTED_NEGATIVES = {
    "gmUT_overclaim": "GMUT validation is complete while all GMUT gates remain open.",
    "observer_overreach": "Browser smoke is observer-only and publication verified.",
    "held_restore_conflict": "Parfit remains held but is restored for current advisory.",
    "complete_blocked_conflict": "The phase is complete while an open_gap remains.",
    "dry_run_cleanup_conflict": "Stale temp inspection only dry-run cleaned the candidates.",
    "cached_live_conflict": "Prior cached evidence proves the current live state.",
}

EXPECTED_POSITIVES = {
    "open_gap_honest": "The phase remains OPEN_GAP and carries all GMUT gates open.",
    "observer_bounded": "Browser smoke is observer-only and does not certify publication.",
    "held_bounded": "Parfit remains held and no current advisory is fabricated.",
    "dry_run_bounded": "Stale-temp dry-run inspected candidates and performed no cleanup.",
    "cached_bounded": "Prior evidence is used as historical context only.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


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
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def lint_text(text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for rule in RULES:
        left = re.search(rule["left"], text, re.IGNORECASE)
        right = re.search(rule["right"], text, re.IGNORECASE)
        if left and right:
            hits.append(
                {
                    "message": rule["message"],
                    "rule_id": rule["rule_id"],
                    "status": "CONTRADICTION_CANDIDATE",
                }
            )
    return hits


def run_fixtures() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    with TemporaryDirectory(prefix="v472-v7-semantic-lint-fixtures-") as tmp:
        root = Path(tmp)
        for name, text in EXPECTED_NEGATIVES.items():
            path = root / "negative" / f"{name}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            hits = lint_text(text)
            entries.append(
                {
                    "detected_rule_ids": [hit["rule_id"] for hit in hits],
                    "fixture": name,
                    "hash": sha256_text(text),
                    "polarity": "expected_negative",
                    "status": "EXPECTED_NEGATIVE_CAUGHT" if hits else "FAIL_EXPECTED_NEGATIVE_NOT_CAUGHT",
                    "tempdir_only": True,
                }
            )
        for name, text in EXPECTED_POSITIVES.items():
            path = root / "positive" / f"{name}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            hits = lint_text(text)
            entries.append(
                {
                    "detected_rule_ids": [hit["rule_id"] for hit in hits],
                    "fixture": name,
                    "hash": sha256_text(text),
                    "polarity": "expected_positive",
                    "status": "EXPECTED_POSITIVE_CLEAR" if not hits else "FAIL_EXPECTED_POSITIVE_FLAGGED",
                    "tempdir_only": True,
                }
            )
    failures = [
        entry
        for entry in entries
        if entry["status"] not in {"EXPECTED_NEGATIVE_CAUGHT", "EXPECTED_POSITIVE_CLEAR"}
    ]
    return {
        "entries": entries,
        "failure_count": len(failures),
        "status": "PASS_FIXTURES" if not failures else "FAIL_FIXTURES",
    }


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    fixtures = run_fixtures()
    engine_rows = [
        row("rules_loaded", "PASS_SHAPE_ONLY", "Semantic lint rule set is loaded.", {"rule_count": len(RULES)}),
        row("fixtures", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Expected-positive and expected-negative fixtures were evaluated.", {"failure_count": fixtures["failure_count"]}),
        row("scope", "OPEN_GAP", "v7 x1 proves fixture behavior only; repo-wide semantic lint integration remains a v7 x2 target."),
    ]
    engine = {
        "aggregate_status": aggregate(engine_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": engine_rows,
        "rules": RULES,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-semantic-lint-engine-v1.json"
    write_json(path, engine)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-semantic-lint-engine-v1.md",
        f"""
# v472 THOS v7 x1 Semantic Lint Engine

Generated UTC: `{generated_at}`

Status: `{engine['aggregate_status']}`

v7 x1 implements executable semantic contradiction fixtures for GMUT claim ceilings, observer evidence, held-lane boundaries, completion/blocker language, dry-run cleanup wording, and cached/current evidence. Repo-wide integration remains open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-semantic-lint-engine-v1.md")

    path = ARTIFACT_ROOT / f"{PHASE}-semantic-lint-fixture-results-v1.json"
    write_json(path, fixtures)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-semantic-lint-fixture-results-v1.md",
        f"""
# v472 THOS v7 x1 Semantic Lint Fixture Results

Status: `{fixtures['status']}`

Fixture failures: `{fixtures['failure_count']}`

All fixture text was tempdir-only. No raw lane transport or external files were published.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-semantic-lint-fixture-results-v1.md")

    integration_rows = [
        row("publication_manifest", "PASS_SHAPE_ONLY", "Future publication lints should run semantic lint against curated Markdown and JSON summaries."),
        row("raw_boundary", "PASS_SHAPE_ONLY", "Raw lane transport remains excluded; semantic lint runs on curated content."),
        row("app_advisories", "PASS_SHAPE_ONLY", "Cicero, Kierkegaard, and Aristotle returned advisory-only schema and contradiction-hunt input."),
        row("ambiguity_boundary", "OPEN_GAP", "False-positive and false-negative tuning remains a v7 x2 review target."),
        row("next_scope", "OPEN_GAP", "v7 x2 should apply the lint to the current curated phase slice before publication."),
    ]
    integration = {
        "aggregate_status": aggregate(integration_rows),
        "app_advisories": APP_ADVISORIES,
        "cli_lanes": CLI_NATURAL_LANES,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": integration_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-publication-integration-ledger-v1.json"
    write_json(path, integration)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-publication-integration-ledger-v1.md",
        """
# v472 THOS v7 x1 Publication Integration Ledger

The semantic lint is fixture-proven and should be integrated into current-slice publication checks in v7 x2.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-publication-integration-ledger-v1.md")

    handoff = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Run semantic lint over the current v7 x1 curated slice.",
            "Collect app and CLI natural-duration advisories if notifier has completed.",
            "Add current-slice lint receipts to publication guard.",
            "Keep raw transport and external cache files excluded.",
        ],
        "status": "READY_FOR_V7_X2_WITH_OPEN_GAPS",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v7-x2-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v7-x2-handoff-v1.md",
        """
# v472 THOS v7 x2 Handoff

v7 x2 should apply the semantic lint to the current curated phase slice and collect the natural-duration lane receipts if ready.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v7-x2-handoff-v1.md")

    status_rows = [
        row("semantic_engine", engine["aggregate_status"], "Semantic lint engine and fixtures generated."),
        row("fixture_results", "PASS_SHAPE_ONLY" if fixtures["failure_count"] == 0 else "FAIL_BLOCKER", "Expected fixtures passed."),
        row("publication_integration", integration["aggregate_status"], "Publication integration remains open for v7 x2."),
    ]
    run_status = {
        "aggregate_status": aggregate(status_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "next_expected_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "rows": status_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-run-status-v1.json"
    write_json(path, run_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md",
        f"""
# v472 THOS v7 x1 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v7 x1 implements fixture-backed semantic contradiction lint. Cicero, Kierkegaard, and Aristotle returned advisory-only input. Current-slice publication integration, ambiguity tuning, and natural-duration lane synthesis remain v7 x2 open gaps.

All six GMUT gates remain open.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-run-status-v1.md")
    return written


def main() -> int:
    for path in write_artifacts():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
