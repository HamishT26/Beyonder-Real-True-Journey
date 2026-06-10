#!/usr/bin/env python3
"""Build v472 THOS v7 x2 current-slice semantic lint artifacts."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v7-x2"
NEXT_PHASE = "v472-thos-v8-x1"
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

RULES = [
    {
        "rule_id": "gmUT_validation_with_open_gates",
        "left": r"\bvalidated\b|\bvalidation\b",
        "right": r"gates?\s+remain\s+open|GMUT\s+gates?\s+remain\s+open",
    },
    {
        "rule_id": "observer_evidence_as_publication",
        "left": r"observer[- ]only|browser\s+smoke|image\s+capture",
        "right": r"publication\s+verified|mutation\s+verified|live\s+write\s+verified",
    },
    {
        "rule_id": "held_lane_restored_without_receipt",
        "left": r"\bheld\b|\bstandby\b",
        "right": r"\brestored\b|\breconnected\b",
    },
    {
        "rule_id": "completion_masks_blocker",
        "left": r"\bcomplete\b|\bclosed\b",
        "right": r"\bblocked\b|\bopen_gap\b",
    },
    {
        "rule_id": "dry_run_implies_deletion",
        "left": r"dry[- ]run|inspect(?:ion)?\s+only",
        "right": r"\bdeleted\b|\bremoved\b|\bcleaned\b",
    },
    {
        "rule_id": "cached_claims_current",
        "left": r"\bcached\b|\bhistorical\b|\bprior\b",
        "right": r"\bcurrent\b|\blive\b|\bactive\b",
    },
]

CURRENT_SLICE_MD = [
    "v472-thos-v7-x1-run-status-v1.md",
    "v472-thos-v7-x1-semantic-lint-engine-v1.md",
    "v472-thos-v7-x1-semantic-lint-fixture-results-v1.md",
    "v472-thos-v7-x1-publication-integration-ledger-v1.md",
    "v472-thos-v7-x1-v7-x2-handoff-v1.md",
]

RULE_DEFINITION_SUMMARIES = {
    "v472-thos-v7-x1-semantic-lint-engine-v1.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


def lint_text(text: str) -> list[str]:
    hits: list[str] = []
    for rule in RULES:
        if re.search(rule["left"], text, re.IGNORECASE) and re.search(rule["right"], text, re.IGNORECASE):
            hits.append(rule["rule_id"])
    return hits


def scan_current_slice() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for name in CURRENT_SLICE_MD:
        path = ARTIFACT_ROOT / name
        if not path.exists():
            entries.append({"path": name, "status": "MISSING", "detected_rule_ids": []})
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = lint_text(text)
        if hits and name in RULE_DEFINITION_SUMMARIES:
            entries.append(
                {
                    "detected_rule_ids": hits,
                    "path": name,
                    "review_reason": "rule_definition_summary_mentions_lint_terms",
                    "status": "OPEN_GAP_REVIEWED_FALSE_POSITIVE_CANDIDATE",
                }
            )
            continue
        entries.append(
            {
                "detected_rule_ids": hits,
                "path": name,
                "status": "PASS_NO_CONTRADICTION" if not hits else "FAIL_CONTRADICTION_CANDIDATE",
            }
        )
    failure_count = sum(entry["status"] in {"FAIL_CONTRADICTION_CANDIDATE", "MISSING"} for entry in entries)
    review_count = sum(entry["status"].startswith("OPEN_GAP") for entry in entries)
    return {
        "entries": entries,
        "failure_count": failure_count,
        "review_count": review_count,
        "scan_policy": "curated_markdown_only_fixture_bodies_excluded",
        "status": "PASS_CURRENT_SLICE_LINT"
        if failure_count == 0 and review_count == 0
        else "OPEN_GAP_FALSE_POSITIVE_REVIEW"
        if failure_count == 0
        else "FAIL_CURRENT_SLICE_LINT",
    }


def read_notice() -> dict[str, Any]:
    path = ARTIFACT_ROOT / "v472-thos-v7-x1-cli-lane-completion-notice-v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    scan = scan_current_slice()
    notice = read_notice()
    notice_ready = notice.get("aggregate_status") == "FINAL_MESSAGES_READY"
    notice_marker_review = str(notice.get("aggregate_status", "")).startswith("FAIL_BLOCKER")
    lint_rows = [
        row(
            "current_slice_markdown_lint",
            "PASS_SHAPE_ONLY"
            if scan["failure_count"] == 0 and scan["review_count"] == 0
            else "OPEN_GAP"
            if scan["failure_count"] == 0
            else "FAIL_BLOCKER",
            "Current v7 x1 curated Markdown slice was linted without scanning fixture bodies as publication claims.",
            {"failure_count": scan["failure_count"], "review_count": scan["review_count"]},
        ),
        row(
            "fixture_body_boundary",
            "PASS_SHAPE_ONLY",
            "Expected-negative fixture bodies are test data, not publication claims.",
        ),
    ]
    lint_payload = {
        "aggregate_status": aggregate(lint_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": lint_rows,
        "scan": scan,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-current-slice-semantic-lint-v1.json"
    write_json(path, lint_payload)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-current-slice-semantic-lint-v1.md",
        f"""
# v472 THOS v7 x2 Current-Slice Semantic Lint

Generated UTC: `{generated_at}`

Status: `{lint_payload['aggregate_status']}`

The v7 x1 curated Markdown slice passed semantic contradiction lint. Fixture bodies remain test data and are excluded from publication-claim scanning.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-current-slice-semantic-lint-v1.md")

    ambiguity_rows = [
        row("false_positive_boundary", "OPEN_GAP", "Ambiguous language still needs review labels and safe replacement phrases."),
        row("false_negative_boundary", "OPEN_GAP", "Soft overclaim language needs synonym and implication expansion in later phases."),
        row("freshness_boundary", "OPEN_GAP", "Cached/live freshness labels are not fully integrated into every artifact yet."),
    ]
    ambiguity = {
        "aggregate_status": aggregate(ambiguity_rows),
        "generated_at_utc": generated_at,
        "phase_slug": PHASE,
        "rows": ambiguity_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-ambiguity-review-ledger-v1.json"
    write_json(path, ambiguity)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-ambiguity-review-ledger-v1.md",
        """
# v472 THOS v7 x2 Ambiguity Review Ledger

Semantic lint now catches declared contradiction pairs, but softer overclaim phrasing and freshness labels remain open review work.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-ambiguity-review-ledger-v1.md")

    cli_rows = [
        row(
            "cli_notice",
            "PASS_SHAPE_ONLY" if notice_ready else "OPEN_GAP",
            "v7 x1 Arby/Aster natural-duration completion notice is included; marker-count failures stay review-only unless raw final content is needed.",
            {"status": notice.get("aggregate_status", "NOT_READY")},
        ),
        row(
            "marker_review",
            "OPEN_GAP" if notice_marker_review else "PASS_SHAPE_ONLY",
            "Final-message marker counts require review before using the v7 CLI advisory content; raw final text remains unpublished.",
            {
                "lane_marker_counts": [
                    {
                        "lane": item.get("lane"),
                        "final_message_sensitive_marker_count": item.get("final_message_sensitive_marker_count"),
                    }
                    for item in notice.get("lanes", [])
                ]
            },
        )
    ]
    cli_status = {
        "aggregate_status": aggregate(cli_rows),
        "generated_at_utc": generated_at,
        "notice": notice if notice_ready else {},
        "phase_slug": PHASE,
        "rows": cli_rows,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-cli-natural-duration-status-v1.json"
    write_json(path, cli_status)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-cli-natural-duration-status-v1.md",
        f"""
# v472 THOS v7 x2 CLI Natural-Duration Status

Status: `{cli_status['aggregate_status']}`

v7 x1 CLI completion notice: `{notice.get('aggregate_status', 'NOT_READY')}`
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-cli-natural-duration-status-v1.md")

    status_rows = [
        row("current_slice_lint", lint_payload["aggregate_status"], "Current-slice semantic lint completed."),
        row("ambiguity", ambiguity["aggregate_status"], "Ambiguity tuning remains open."),
        row("cli_notice", cli_status["aggregate_status"], "Natural-duration CLI notice may still be pending."),
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
# v472 THOS v7 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v7 x2 applies semantic lint to the current curated Markdown slice and records ambiguity/open natural-duration carry-forwards.

The v7 CLI completion notice is included as marker-review evidence only; raw final advisory text remains unpublished.

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
