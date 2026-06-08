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
    ("retry-wait", "productive_wait", "publish_during_wait_if_guarded"),
    ("15m-cadence-guard", "cadence_gate", "publish_after_threshold"),
    ("15-minute-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("10m-cadence-guard", "cadence_gate", "publish_after_threshold"),
    ("10-minute-prep-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("10-minute-cadence-gate", "cadence_gate", "publish_after_threshold"),
    ("candidate-build-backlog", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("source-and-regression-prep-ledger", "source_regression_prep", "publish_during_prep_if_guarded"),
    ("launch-timeout-regression-prep", "source_regression_prep", "publish_during_prep_if_guarded"),
    ("x2-design-sketch", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("watcher-trust-cadence-receipt", "watcher_trust_cadence", "publish_after_cadence"),
    ("prebuild", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("prebuild-source-and-backlog", "prebuild_backlog", "publish_during_prep_if_guarded"),
    ("readiness-preflight", "readiness_preflight", "publish_after_preflight_guard"),
    ("phase-artifact-cadence-classifier", "phase_artifact_classifier", "publish_after_classification"),
    ("artifact-cadence-classifier", "phase_artifact_classifier", "publish_after_classification"),
    ("completion-gate", "app_completion_gate", "publish_after_cadence_and_redaction"),
    ("completion-notifier", "completion_status", "publish_after_cadence"),
    ("app-thread-redaction", "redaction_guard", "publish_before_app_completion_publication"),
    ("app-watch-thread-redaction", "redaction_guard", "publish_before_app_watch_publication"),
    ("council-app-lane-notifier-runner", "app_lane_runner_launch", "publish_after_launch_guard"),
    ("cli-bridge-repair", "cli_bridge_repair", "publish_after_cadence"),
    ("bridge-surface-repair", "cli_bridge_repair", "publish_after_cadence"),
    ("cli-quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("combined-elaboration-quality-gate", "cli_quality_gate", "publish_after_final_message_surface"),
    ("marker-review-ledger", "cli_marker_review", "publish_after_quality_gate"),
    ("five-lane-status-normalizer", "five_lane_normalizer", "publish_before_closeout"),
    ("five-lane-normalized-status", "five_lane_normalizer", "publish_before_closeout"),
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
