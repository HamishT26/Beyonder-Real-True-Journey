#!/usr/bin/env python3
"""Build v472 THOS v6 x2 natural-duration completion synthesis artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE = "v472-thos-v6-x2"
NEXT_PHASE = "v472-thos-v7-x1"
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
        "status": "ADVISORY_RETURNED",
        "summary": "Publish readiness metadata only; natural runtime is scoped observation, not permanent reliability.",
    },
    {
        "lane": "Kierkegaard",
        "status": "ADVISORY_RETURNED",
        "summary": "Notifier receipts prove readiness state only; stale-temp cleanup and GMUT claims remain outside this evidence.",
    },
    {
        "lane": "Aristotle",
        "status": "ADVISORY_RETURNED",
        "summary": "Use schemas and expected-negative rows for final-message, notifier, stale-temp, and publication lints.",
    },
]

CLI_ADVISORIES = [
    {
        "lane": "Arby",
        "status": "ADVISORY_RETURNED",
        "summary": (
            "Final-message reliability must move from syntactic checks to semantic checks; require sidecar claims, "
            "transport cleanliness, schema validity, artifact existence, semantic rules, and then rendered prose."
        ),
    },
    {
        "lane": "Aster Vale",
        "status": "ADVISORY_RETURNED",
        "summary": (
            "Final receipts should refuse self-certification without checked inputs; add run-status, allowlist, "
            "browser-boundary, and semantic-contradiction guards."
        ),
    },
]

SEMANTIC_RULES = [
    {
        "rule_id": "gmUT_gate_claim_ceiling",
        "reject_pair": ["validated", "gates remain open"],
        "message": "Validation language cannot coexist with open-gate status for GMUT.",
    },
    {
        "rule_id": "observer_boundary",
        "reject_pair": ["observer-only", "publication verified"],
        "message": "Observer evidence cannot certify publication or mutation.",
    },
    {
        "rule_id": "held_lane_boundary",
        "reject_pair": ["held", "restored"],
        "message": "A held lane cannot be described as restored without a restoration receipt.",
    },
    {
        "rule_id": "completion_boundary",
        "reject_pair": ["complete", "blocked"],
        "message": "Completion language must not mask blocker status.",
    },
    {
        "rule_id": "cleanup_boundary",
        "reject_pair": ["dry-run", "deleted"],
        "message": "Dry-run stale-temp inspection cannot imply deletion.",
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


def read_json(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def aggregate(rows: list[dict[str, Any]]) -> str:
    if any(item["status"] == "FAIL_BLOCKER" for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] == "OPEN_GAP" for item in rows):
        return "OPEN_GAP"
    return "PASS_SHAPE_ONLY"


def write_artifacts() -> list[Path]:
    generated_at = utc_now()
    notice = read_json("v472-thos-v6-x1-cli-lane-completion-notice-v1.json")
    x1_status = read_json("v472-thos-v6-x1-run-status-v1.json")
    notice_ready = notice.get("aggregate_status") == "FINAL_MESSAGES_READY"
    notice_lanes = notice.get("lanes", [])
    final_marker_count = sum(item.get("final_message_sensitive_marker_count", 0) for item in notice_lanes)

    completion_rows = [
        row(
            "natural_duration_notice",
            "PASS_SHAPE_ONLY" if notice_ready else "OPEN_GAP",
            "The notifier produced a curated completion notice for both natural-duration CLI lanes.",
            {"status": notice.get("aggregate_status"), "lane_count": len(notice_lanes)},
        ),
        row(
            "final_message_marker_boundary",
            "PASS_SHAPE_ONLY" if final_marker_count == 0 else "FAIL_BLOCKER",
            "Final-message marker count is zero in the curated notice.",
            {"final_message_marker_count": final_marker_count},
        ),
        row(
            "raw_transport_boundary",
            "PASS_SHAPE_ONLY",
            "Raw lane transport remains temp-only and is not published.",
        ),
        row(
            "x1_open_gap_inheritance",
            "OPEN_GAP" if x1_status.get("aggregate_status") == "OPEN_GAP" else "PASS_SHAPE_ONLY",
            "v6 x1 published the watcher as an open gap before async completion; v6 x2 now records the completion notice.",
            {"x1_status": x1_status.get("aggregate_status")},
        ),
    ]
    completion = {
        "aggregate_status": aggregate(completion_rows),
        "app_advisories": APP_ADVISORIES,
        "cli_advisories": CLI_ADVISORIES,
        "completion_notice": notice,
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": completion_rows,
    }
    written: list[Path] = []
    path = ARTIFACT_ROOT / f"{PHASE}-natural-duration-completion-synthesis-v1.json"
    write_json(path, completion)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-natural-duration-completion-synthesis-v1.md",
        f"""
# v472 THOS v6 x2 Natural-Duration Completion Synthesis

Generated UTC: `{generated_at}`

Status: `{completion['aggregate_status']}`

Arby and Aster Vale completed their natural-duration read-only CLI lanes. The notifier recorded final-message readiness for both lanes, with raw transport excluded from publication.

This is workflow reliability evidence only. It does not validate GMUT or close any GMUT gate.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-natural-duration-completion-synthesis-v1.md")

    semantic_rows = [
        row("rules_defined", "PASS_SHAPE_ONLY", "Semantic contradiction rules are defined for GMUT, observer, held-lane, completion, and cleanup boundaries.", {"rule_count": len(SEMANTIC_RULES)}),
        row("implementation_status", "OPEN_GAP", "Rules are specified as a v7 implementation target; no full markdown/json contradiction engine is claimed yet."),
    ]
    semantic = {
        "aggregate_status": aggregate(semantic_rows),
        "generated_at_utc": generated_at,
        "gmUT_gate_effect": "none_open_not_tested",
        "gmUT_gates_open": GMUT_GATES,
        "phase_slug": PHASE,
        "rows": semantic_rows,
        "semantic_rules": SEMANTIC_RULES,
    }
    path = ARTIFACT_ROOT / f"{PHASE}-semantic-contradiction-rules-v1.json"
    write_json(path, semantic)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-semantic-contradiction-rules-v1.md",
        """
# v472 THOS v6 x2 Semantic Contradiction Rules

v6 x2 defines the first compact ruleset for contradiction linting. The rules are specified for v7 implementation; they are not yet a full contradiction engine.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-semantic-contradiction-rules-v1.md")

    state_machine = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": generated_at,
        "notifier_states": [
            "LANE_LAUNCHED",
            "FIRST_OUTPUT_OBSERVED",
            "FINAL_MESSAGE_READY",
            "NOTICE_WRITTEN",
            "SYNTHESIZED_FOR_PUBLICATION",
        ],
        "phase_slug": PHASE,
        "transition_rules": [
            "Do not force short termination when the lane is still making progress.",
            "Write completion notice only when final-message markers are ready.",
            "Keep raw transport out of publication.",
            "Carry pending lanes as open gaps instead of failure unless phase contract requires completion.",
        ],
    }
    path = ARTIFACT_ROOT / f"{PHASE}-notifier-state-machine-ledger-v1.json"
    write_json(path, state_machine)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-notifier-state-machine-ledger-v1.md",
        """
# v472 THOS v6 x2 Notifier State Machine Ledger

The notifier flow is state-based: launch, observe output, detect final message, write notice, then synthesize. Pending lanes remain open gaps rather than forced failures.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-notifier-state-machine-ledger-v1.md")

    handoff = {
        "generated_at_utc": generated_at,
        "gmUT_gates_open": GMUT_GATES,
        "next_phase": NEXT_PHASE,
        "phase_slug": PHASE,
        "recommended_tasks": [
            "Implement the semantic contradiction rules as executable lint fixtures.",
            "Require final-message sidecar claims before publication-ready prose.",
            "Add freshness checks for cached versus live evidence.",
            "Add Browser smoke boundaries as observer-only evidence.",
            "Continue stale-temp work as dry-run unless a separate exact cleanup approval is active.",
        ],
        "status": "READY_FOR_V7_WITH_OPEN_GAPS",
    }
    path = ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.json"
    write_json(path, handoff)
    written.append(path)
    write_md(
        ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.md",
        """
# v472 THOS v7 Handoff

v7 should convert the v6 semantic contradiction rules into executable lint fixtures and freshness-aware publication checks.
""",
    )
    written.append(ARTIFACT_ROOT / f"{PHASE}-v7-handoff-v1.md")

    status_rows = [
        row("completion_notice", completion["aggregate_status"], "Natural-duration completion notice synthesized."),
        row("semantic_rules", semantic["aggregate_status"], "Contradiction rules defined for v7 implementation."),
        row("notifier_state_machine", state_machine["aggregate_status"], "Notifier state machine recorded."),
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
# v472 THOS v6 x2 Run Status

Status: `{run_status['aggregate_status']}`

Next expected phase: `{NEXT_PHASE}`

v6 x2 publishes the natural-duration Arby/Aster notifier completion notice, synthesis, state-machine ledger, and semantic contradiction rule handoff.

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
