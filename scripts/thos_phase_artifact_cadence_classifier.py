#!/usr/bin/env python3
"""Classify THOS phase artifacts by cadence and publication role."""

from __future__ import annotations

import argparse
import glob
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROLE_RULES: list[tuple[str, str, str]] = [
    ("exposure-guard", "exposure_guard", "publish_before_staging"),
    ("launch", "launch", "publish_after_launch_guard"),
    ("productive-wait", "productive_wait", "publish_during_wait_if_guarded"),
    ("wait-plan", "productive_wait", "publish_during_wait_if_guarded"),
    ("eureka-wait-task-plan", "productive_wait", "publish_during_wait_if_guarded"),
    ("retry-wait", "productive_wait", "publish_during_wait_if_guarded"),
    ("app-receipt-thread-redactor", "redaction_guard", "publish_before_exposure_guard"),
    ("app-gate-thread-redactor", "redaction_guard", "publish_before_exposure_guard"),
    ("app-lane-probe-redactor", "redaction_guard", "publish_before_exposure_guard"),
    ("app-lane-probe-repair-diagnostic", "app_lane_probe", "publish_after_redaction_guard"),
    ("app-lane-direct-repair-success-ledger", "app_lane_repair_success", "publish_after_repair_gate"),
    ("council-app-lane-direct-repair-gate", "app_completion_gate", "publish_after_cadence_and_redaction"),
    ("15m-cadence-guard", "cadence_gate", "publish_after_threshold"),
    ("15-minute-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("10m-cadence-guard", "cadence_gate", "publish_after_threshold"),
    ("10-minute-prep-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("10-minute-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("five-minute-cadence-check", "cadence_gate", "publish_after_threshold"),
    ("status-check-cadence-guard", "cadence_gate", "publish_after_threshold"),
    ("candidate-build-backlog", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("source-and-eureka-backlog", "prebuild_backlog", "publish_during_wait_if_guarded"),
    ("repair-wait-source-refresh", "source_refresh", "publish_during_wait_if_guarded"),
    ("wider-infra-source-refresh", "source_refresh", "publish_during_wait_if_guarded"),
    ("source-and-handoff-prep-ledger", "source_handoff_prep", "publish_during_prep_if_guarded"),
    ("source-and-regression-prep-ledger", "source_regression_prep", "publish_during_prep_if_guarded"),
    ("source-and-build-prep-ledger", "source_regression_prep", "publish_during_prep_if_guarded"),
    ("temp-output-hygiene-verifier-design", "prebuild_design", "publish_during_wait_if_guarded"),
    ("handoff-surface", "phase_handoff", "publish_after_closeout"),
    ("launch-timeout-regression-prep", "source_regression_prep", "publish_during_prep_if_guarded"),
    ("x2-build-implementation-plan", "x2_build_plan", "publish_after_x2_prep_gate"),
    ("build-use-acceptance", "x2_build_use_acceptance", "publish_after_x2_build_actions"),
    ("implementation-ledger", "x2_implementation_ledger", "publish_after_x2_build_actions"),
    ("launch-handoff", "next_x1_launch_handoff", "publish_after_x2_acceptance"),
    ("x2-build-queue-seed", "x2_build_queue_seed", "publish_during_wait_if_guarded"),
    ("source-backed-x2-build-queue-update", "x2_build_queue_seed", "publish_during_wait_if_guarded"),
    ("x2-build-queue", "x2_build_queue", "publish_after_source_guard"),
    ("x2-build-funnel-draft", "prebuild_backlog", "publish_during_wait_if_guarded"),
    ("x2-design-sketch", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("watcher-trust-cadence-receipt", "watcher_trust_cadence", "publish_after_cadence"),
    ("watcher-trust-contract", "watcher_trust_contract", "publish_after_x2_build_actions"),
    ("no-babysitting-enforcement-checklist", "no_babysitting_enforcement_checklist", "publish_after_x2_build_actions"),
    ("command-surface-compatibility-queue", "command_surface_compatibility_queue", "publish_after_x2_build_actions"),
    ("cli-quality-regression-tracker", "cli_quality_regression_tracker", "publish_after_quality_gate"),
    ("source-to-system-table", "source_to_system_table", "publish_after_source_guard"),
    ("app-wrapper-stale-receipt-repair-policy", "app_wrapper_repair_policy", "publish_after_repair_gate"),
    ("helper-runner-acceptance-test-list", "helper_runner_acceptance_tests", "publish_after_x2_build_actions"),
    ("direct-app-fallback-hardening-matrix", "direct_app_fallback_matrix", "publish_after_repair_gate"),
    ("cli-long-form-reliability-ledger", "cli_reliability_ledger", "publish_after_quality_gate"),
    ("prebuild", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("prebuild-source-and-backlog", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("readiness-preflight", "readiness_preflight", "publish_after_preflight_guard"),
    ("prestart-receipt", "launch_prestart", "publish_before_launch"),
    ("prestart-positive-proof", "launch_prestart", "publish_before_launch"),
    ("heading-contract", "heading_contract_preflight", "publish_before_launch"),
    ("prompt-contract-verifier", "prompt_contract_preflight", "publish_before_launch"),
    ("launch-checklist-verifier", "launch_checklist", "publish_after_launch_guard"),
    ("phase-artifact-cadence-classifier", "phase_artifact_classifier", "publish_after_classification"),
    ("artifact-cadence-classifier", "phase_artifact_classifier", "publish_after_classification"),
    ("phase-advance-gate-design", "prebuild_design", "publish_during_wait_if_guarded"),
    ("phase-advance-gate-verifier", "phase_advance_gate", "publish_before_phase_advance"),
    ("phase-dashboard-receipt", "phase_dashboard_receipt", "publish_after_phase_advance"),
    ("no-overclaim-guard", "no_overclaim_guard", "publish_before_closeout"),
    ("completion-gate", "app_completion_gate", "publish_after_cadence_and_redaction"),
    ("completion-notifier", "completion_status", "publish_after_cadence"),
    ("app-thread-redaction", "redaction_guard", "publish_before_app_completion_publication"),
    ("app-watch-thread-redaction", "redaction_guard", "publish_before_app_watch_publication"),
    ("app-watcher-freshness-guard-design", "prebuild_design", "publish_during_wait_if_guarded"),
    ("council-app-lane-notifier-runner", "app_lane_runner_launch", "publish_after_launch_guard"),
    ("cli-r4-carryover-update", "cli_carryover_update", "publish_after_repair_launch"),
    ("cli-r3-carryover-update", "cli_carryover_update", "publish_after_repair_launch"),
    ("cli-r2-carryover-update", "cli_carryover_update", "publish_after_repair_launch"),
    ("cli-bridge-startprocess-repair", "cli_bridge_repair", "publish_after_cadence_and_exposure"),
    ("cli-bridge-repair", "cli_bridge_repair", "publish_after_cadence"),
    ("bridge-surface-repair", "cli_bridge_repair", "publish_after_cadence"),
    ("cli-repair-quality-ladder", "cli_repair_governance", "publish_after_repair_launch"),
    ("cli-live-wait-repair", "cli_live_wait_repair", "publish_after_cadence"),
    ("cli-quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("combined-elaboration-quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("marker-review-ledger", "cli_marker_review", "publish_after_quality_gate"),
    ("five-lane-status-normalizer", "five_lane_normalizer", "publish_before_closeout"),
    ("five-lane-normalized-status", "five_lane_normalizer", "publish_before_closeout"),
    ("five-lane-gratitude-handoff", "five_lane_gratitude_handoff", "publish_after_launch_guard"),
    ("closeout", "phase_closeout", "publish_after_five_lane_ready"),
    ("prep-start", "next_x2_prep_start", "publish_after_closeout"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def role_for(name: str) -> tuple[str, str]:
    for token, role, rule in ROLE_RULES:
        if token in name:
            return role, rule
    return "unclassified", "manual_review_required"


def read_status(path: Path) -> str:
    if path.suffix.lower() != ".json":
        return "non_json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return "json_parse_failed"
    return str(
        payload.get("overall_status")
        or payload.get("aggregate_status")
        or payload.get("status")
        or "status_missing"
    )


def expand_inputs(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(item) for item in glob.glob(pattern)]
        if matches:
            paths.extend(matches)
        else:
            path = Path(pattern)
            if path.exists():
                paths.append(path)
    return sorted(set(paths), key=lambda p: str(p).lower())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Phase Artifact Cadence Classifier",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- files_classified: `{payload['files_classified']}`",
        f"- unclassified_count: `{payload['unclassified_count']}`",
        "",
        "Role counts:",
    ]
    for role, count in sorted(payload["role_counts"].items()):
        lines.append(f"- {role}: `{count}`")
    lines.extend(["", "Publication rules are filename/status based and do not publish raw lane text."])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    role_counts: dict[str, int] = {}
    for path in expand_inputs(args.input):
        role, publication_rule = role_for(path.name)
        role_counts[role] = role_counts.get(role, 0) + 1
        rows.append(
            {
                "file": path.name,
                "role": role,
                "publication_rule": publication_rule,
                "status": read_status(path),
                "raw_boundary": "filename_and_status_only",
            }
        )

    unclassified_count = role_counts.get("unclassified", 0)
    payload: dict[str, Any] = {
        "artifact_type": "phase_artifact_cadence_classifier",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_ARTIFACT_CLASSIFIER" if unclassified_count == 0 else "OPEN_GAP_UNCLASSIFIED_ARTIFACTS",
        "files_classified": len(rows),
        "unclassified_count": unclassified_count,
        "role_counts": role_counts,
        "artifacts": rows,
        "claim_boundary": {
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if unclassified_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
