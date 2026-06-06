#!/usr/bin/env python3
"""Validate the current THOS wait-run policy receipts without mutating skills."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: str) -> dict[str, object]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def count_list(payload: dict[str, object], key: str) -> int:
    value = payload.get(key)
    return len(value) if isinstance(value, list) else 0


def nested(payload: dict[str, object], *keys: str) -> object:
    value: object = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def check_rows(
    framework: dict[str, object],
    source_ledger: dict[str, object],
    reflection_ledger: dict[str, object],
    cadence_gate: dict[str, object],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL_BLOCKER",
                "evidence": evidence,
            }
        )

    current_wait = nested(framework, "cadence_policy", "current_boundary_wait_mark_minutes")
    add("x2_wait_mark_at_least_15", isinstance(current_wait, int) and current_wait >= 15, f"value={current_wait!r}")

    elapsed = cadence_gate.get("elapsed_seconds")
    threshold = cadence_gate.get("threshold_seconds")
    allowed = cadence_gate.get("status_check_allowed")
    add(
        "cadence_gate_elapsed",
        isinstance(elapsed, int) and isinstance(threshold, int) and elapsed >= threshold and allowed is True,
        f"elapsed={elapsed!r}; threshold={threshold!r}; allowed={allowed!r}",
    )

    source_count = source_ledger.get("search_queries_completed")
    if source_count is None:
        source_count = nested(source_ledger, "prep_window", "search_queries_completed")
    add("web_searches_at_least_30", isinstance(source_count, int) and source_count >= 30, f"count={source_count!r}")

    draft_skills = nested(framework, "skill_policy_overlay", "draft_skill_candidates")
    draft_count = len(draft_skills) if isinstance(draft_skills, list) else 0
    add("draft_skill_candidates_at_least_10", draft_count >= 10, f"count={draft_count}")

    micro_count = count_list(reflection_ledger, "draft_skill_micro_workflows_used")
    add("draft_skill_micro_workflows_used_at_least_10", micro_count >= 10, f"count={micro_count}")

    reflections = count_list(reflection_ledger, "thirty_reflections")
    add("journey_trinity_reflections_at_least_30", reflections >= 30, f"count={reflections}")

    eureka_tasks = count_list(reflection_ledger, "twenty_x2_eureka_tasks")
    add("x2_eureka_tasks_at_least_20", eureka_tasks >= 20, f"count={eureka_tasks}")

    fix_attempts = nested(framework, "cadence_policy", "safe_fix_attempts_per_blocker")
    add("safe_fix_attempts_target_at_least_5", isinstance(fix_attempts, int) and fix_attempts >= 5, f"value={fix_attempts!r}")

    actual_skill_mutation = nested(framework, "skill_policy_overlay", "actual_user_skill_mutation_performed")
    actual_enable_disable = nested(framework, "skill_policy_overlay", "actual_enable_disable_labels_mutated")
    labels_overlay = nested(framework, "skill_policy_overlay", "labels_are_planning_overlay_only")
    add(
        "skill_labels_are_overlay_only",
        actual_skill_mutation is False and actual_enable_disable is False and labels_overlay is True,
        f"skill_mutation={actual_skill_mutation!r}; label_mutation={actual_enable_disable!r}; overlay={labels_overlay!r}",
    )

    raw_lane = nested(reflection_ledger, "claim_boundary", "raw_lane_text_published")
    raw_transport = nested(reflection_ledger, "claim_boundary", "raw_transport_published")
    add(
        "raw_lane_and_transport_not_published",
        raw_lane is False and raw_transport is False,
        f"raw_lane={raw_lane!r}; raw_transport={raw_transport!r}",
    )
    return rows


def build_report(args: argparse.Namespace) -> dict[str, object]:
    framework = load_json(args.framework_json)
    source_ledger = load_json(args.source_ledger_json)
    reflection_ledger = load_json(args.reflection_ledger_json)
    cadence_gate = load_json(args.cadence_gate_json)
    rows = check_rows(framework, source_ledger, reflection_ledger, cadence_gate)
    failed = [row for row in rows if row["status"] != "PASS"]
    return {
        "artifact_type": "thos_wait_policy_guard_report",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_WAIT_POLICY_GUARD" if not failed else "FAIL_WAIT_POLICY_BLOCKER",
        "checked_artifacts": [
            args.framework_json,
            args.source_ledger_json,
            args.reflection_ledger_json,
            args.cadence_gate_json,
        ],
        "rows": rows,
        "mutation_performed": False,
        "actual_user_skill_mutation_performed": False,
        "actual_plugin_cache_mutation_performed": False,
        "raw_lane_text_published": False,
        "raw_transport_published": False,
        "gmut_gate_state": "all_gmut_gates_remain_open",
        "canon_promotion": "not_claimed",
    }


def write_md(report: dict[str, object], path: str) -> None:
    lines = [
        f"# {report['phase_slug']} Wait Policy Guard",
        "",
        f"- Status: `{report['overall_status']}`",
        "- Mutation performed: `false`",
        "- User-skill mutation performed: `false`",
        "- Plugin-cache mutation performed: `false`",
        "",
        "## Rows",
        "",
    ]
    for row in report["rows"]:  # type: ignore[assignment]
        lines.append(f"- `{row['row_id']}`: `{row['status']}` - {row['evidence']}")
    lines.extend(
        [
            "",
            "Claim boundary: this guard validates wait-policy receipts only. It does not install skills, disable skills, mutate plugin cache, harvest raw lane text, validate GMUT, or promote canon.",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate THOS wait-run policy receipts.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--framework-json", required=True)
    parser.add_argument("--source-ledger-json", required=True)
    parser.add_argument("--reflection-ledger-json", required=True)
    parser.add_argument("--cadence-gate-json", required=True)
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    args = parser.parse_args()

    report = build_report(args)
    if args.receipt_json:
        Path(args.receipt_json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.receipt_md:
        write_md(report, args.receipt_md)
    print(json.dumps(report, indent=2))
    return 0 if report["overall_status"] == "PASS_WAIT_POLICY_GUARD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
