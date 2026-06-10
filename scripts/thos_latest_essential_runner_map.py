#!/usr/bin/env python3
"""Create a status-only map of the latest essential THOS helper stack."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

RUNNER_GROUPS: dict[str, list[dict[str, str]]] = {
    "app_lanes": [
        {"file": "scripts/thos_council_app_lane_notifier_runner.py", "role": "existing r3 app-lane notify, background-watch, and gate-only harvest"},
        {"file": "scripts/thos_app_lane_completion_notifier.py", "role": "app-lane completion receipt production"},
        {"file": "scripts/thos_app_receipt_thread_redactor.py", "role": "app thread identifier redaction before publication"},
        {"file": "scripts/thos_app_lane_direct_repair_gate.py", "role": "direct repair fallback for app completion gaps"},
    ],
    "cli_lanes": [
        {"file": "scripts/thos_cli_strict_stdin_lane_launcher.py", "role": "Node-entrypoint-first strict read-only CLI launch"},
        {"file": "scripts/thos_cli_lane_completion_notifier.py", "role": "temp-only final-message completion receipt"},
        {"file": "scripts/thos_cli_elaboration_quality_gate.py", "role": "long-form elaboration and heading quality gate"},
        {"file": "scripts/thos_cli_marker_review_ledger.py", "role": "generic marker false-positive review"},
    ],
    "cadence_and_phase": [
        {"file": "scripts/thos_status_check_cadence_guard.py", "role": "five-minute status-check cadence guard"},
        {"file": "scripts/thos_five_lane_status_normalizer.py", "role": "five-lane normalized status board"},
        {"file": "scripts/thos_phase_advance_gate_verifier.py", "role": "phase-advance dependency verifier"},
        {"file": "scripts/thos_phase_dashboard_receipt.py", "role": "phase dashboard summary from gate receipts"},
    ],
    "publication_safety": [
        {"file": "scripts/thos_status_receipt_exposure_guard.py", "role": "raw/private/sensitive exposure guard"},
        {"file": "scripts/thos_no_overclaim_guard.py", "role": "GMUT/canon/consciousness overclaim guard"},
        {"file": "scripts/thos_publication_guard.py", "role": "staged publication shape and allowlist guard"},
        {"file": "scripts/thos_phase_artifact_cadence_classifier.py", "role": "artifact role and cadence classifier"},
    ],
    "continuity_and_bus": [
        {"file": "scripts/ghc_multiplex_ipc_bus.py", "role": "GHC Multiplex IPC status-only message contract"},
        {"file": "scripts/thos_x2_build_use_acceptance_runner.py", "role": "x2 build/use acceptance and next x1 handoff"},
    ],
}

LEGACY_AVOID_PATTERNS = [
    "trinity_v*_cli_sibling_phase_runner.py",
    "trinity_v*_app_phase_runner.py",
    "thos_v477_app_lane_notifier_runner.py",
    "thos_v478_app_lane_notifier_runner.py",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def row_for(item: dict[str, str]) -> dict[str, Any]:
    path = REPO_ROOT / item["file"]
    return {
        "file": Path(item["file"]).name,
        "repo_relative": item["file"].replace("\\", "/"),
        "present": path.exists(),
        "role": item["role"],
    }


def build_payload(phase_slug: str) -> dict[str, Any]:
    groups = {
        group: [row_for(item) for item in items]
        for group, items in RUNNER_GROUPS.items()
    }
    missing = [
        f"{group}:{row['file']}"
        for group, rows in groups.items()
        for row in rows
        if not row["present"]
    ]
    return {
        "artifact_type": "latest_essential_runner_map",
        "phase_slug": phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_LATEST_ESSENTIAL_RUNNER_MAP" if not missing else "OPEN_GAP_LATEST_ESSENTIAL_RUNNER_MAP",
        "missing": missing,
        "runner_groups": groups,
        "selection_policy": {
            "use_latest_essential_helpers_first": True,
            "node_entrypoint_first_for_cli": True,
            "windows_entrypoint_fallback_allowed": True,
            "status_only_publication": True,
            "five_minute_checks": True,
            "redaction_before_app_publication": True,
        },
        "legacy_avoid_patterns": LEGACY_AVOID_PATTERNS,
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Latest Essential Runner Map",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Runner Groups",
    ]
    for group, rows in payload["runner_groups"].items():
        lines.extend(["", f"### {group}"])
        for row in rows:
            lines.append(f"- {row['file']}: present `{str(row['present']).lower()}`, role `{row['role']}`")
    lines.extend(["", "## Legacy Avoid Patterns"])
    lines.extend(f"- `{pattern}`" for pattern in payload["legacy_avoid_patterns"])
    lines.extend(["", "Open gaps:"])
    if payload["missing"]:
        lines.extend(f"- `{gap}`" for gap in payload["missing"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: status-only runner map; no raw lane text, logs, screenshots, credentials, session streams, or local absolute paths.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    payload = build_payload(args.phase_slug)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if not payload["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
