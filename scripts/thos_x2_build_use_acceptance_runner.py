#!/usr/bin/env python3
"""Build a status-only x2 acceptance receipt and next x1 launch handoff.

This runner connects the v504 x2 build queue to the verified receipt layer. It
does not read raw sibling output, start background daemons, or create threads.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

ESSENTIAL_SCRIPTS = [
    "scripts/thos_cli_strict_stdin_lane_launcher.py",
    "scripts/thos_cli_lane_completion_notifier.py",
    "scripts/thos_cli_elaboration_quality_gate.py",
    "scripts/thos_cli_marker_review_ledger.py",
    "scripts/thos_council_app_lane_notifier_runner.py",
    "scripts/thos_app_lane_completion_notifier.py",
    "scripts/thos_app_lane_direct_repair_gate.py",
    "scripts/thos_five_lane_status_normalizer.py",
    "scripts/thos_phase_advance_gate_verifier.py",
    "scripts/thos_status_check_cadence_guard.py",
    "scripts/ghc_multiplex_ipc_bus.py",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def read_json(path: str) -> dict[str, Any]:
    candidate = resolve(path)
    if not candidate.exists():
        return {"_available": False, "_file": candidate.name, "_reason": "missing"}
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_available": False, "_file": candidate.name, "_reason": "json_error"}
    if not isinstance(payload, dict):
        return {"_available": False, "_file": candidate.name, "_reason": "not_object"}
    payload["_available"] = True
    payload["_file"] = candidate.name
    return payload


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("status") or payload.get("aggregate_status") or "")


def script_rows() -> list[dict[str, Any]]:
    rows = []
    for script in ESSENTIAL_SCRIPTS:
        rows.append(
            {
                "script": Path(script).name,
                "present": (REPO_ROOT / script).exists(),
                "role": role_for(script),
            }
        )
    return rows


def role_for(script: str) -> str:
    if "strict_stdin" in script:
        return "cli_node_entrypoint_first_policy_anchor"
    if "completion_notifier" in script:
        return "completion_status_receipt_anchor"
    if "elaboration_quality" in script:
        return "cli_final_message_quality_gate"
    if "marker_review" in script:
        return "cli_marker_false_positive_review"
    if "council_app_lane" in script:
        return "app_lane_notify_and_watch_anchor"
    if "direct_repair" in script:
        return "app_background_watch_direct_repair_anchor"
    if "five_lane_status" in script:
        return "five_lane_status_board_anchor"
    if "phase_advance" in script:
        return "phase_dependency_gate_anchor"
    if "cadence" in script:
        return "five_minute_check_cadence_anchor"
    if "multiplex" in script:
        return "ipc_bus_contract_anchor"
    return "supporting_helper"


def build_dependency_graph(receipts: dict[str, dict[str, Any]], next_phase_slug: str) -> list[dict[str, Any]]:
    return [
        {
            "node": "v504_v4_x1_five_lane_quorum",
            "receipt": receipts["x1_closeout"].get("_file"),
            "status": status(receipts["x1_closeout"]),
            "required_for": "x2_build_use",
        },
        {
            "node": "v504_v4_x2_prep_contract",
            "receipt": receipts["x2_prep"].get("_file"),
            "status": status(receipts["x2_prep"]),
            "required_for": "x2_build_use",
        },
        {
            "node": "codex_cli_0_138_readiness",
            "receipt": receipts["cli_update"].get("_file"),
            "status": status(receipts["cli_update"]),
            "required_for": "node_entrypoint_first_policy",
        },
        {
            "node": "ghc_multiplex_ipc_contract",
            "receipt": receipts["ipc"].get("_file"),
            "status": status(receipts["ipc"]),
            "required_for": "app_cli_status_bus",
        },
        {
            "node": "vision_compact_refresh_continuity",
            "receipt": receipts["vision"].get("_file"),
            "status": status(receipts["vision"]),
            "required_for": "phase_start_and_compact_refresh",
        },
        {
            "node": "omega_line_v2_branch",
            "receipt": receipts["branch"].get("_file"),
            "status": status(receipts["branch"]),
            "required_for": "cleaner_future_phase_surface",
        },
        {
            "node": f"{next_phase_slug}_handoff",
            "receipt": "generated_by_this_runner",
            "status": "READY_TO_WRITE",
            "required_for": "next_x1_launch",
        },
    ]


def build_acceptance(args: argparse.Namespace, receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    scripts = script_rows()
    graph = build_dependency_graph(receipts, args.next_phase_slug)
    required_statuses = {
        "x1_closeout": status(receipts["x1_closeout"]).startswith("PASS_"),
        "x2_prep": status(receipts["x2_prep"]).startswith("PASS_"),
        "cli_update": status(receipts["cli_update"]) == "PASS_CODEX_CLI_0_138_0_UPDATED",
        "ipc": status(receipts["ipc"]) == "PASS_GHC_MULTIPLEX_IPC_BUS_SCAFFOLD",
        "vision": status(receipts["vision"]) == "PASS_PHASE_START_AND_COMPACT_REFRESH_VISION_CARD_READY",
        "branch": status(receipts["branch"]) == "PASS_OMEGA_LINE_V2_BRANCH_CREATED",
        "essential_scripts": all(row["present"] for row in scripts),
    }
    open_gaps = [name for name, passed in required_statuses.items() if not passed]
    return {
        "artifact_type": "x2_build_use_acceptance_receipt",
        "phase_slug": args.phase_slug,
        "next_phase_slug": args.next_phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_BUILD_USE_ACCEPTANCE_READY" if not open_gaps else "OPEN_GAP_X2_BUILD_USE_ACCEPTANCE",
        "open_gaps": open_gaps,
        "build_queue_coverage": [
            {
                "item": "gate_aware_background_supervision_dashboard",
                "outcome": "covered_by_five_lane_status_normalizer_and_ipc_status_board",
            },
            {
                "item": "strict_stdin_first_policy",
                "outcome": "covered_by_cli_strict_stdin_launcher_and_cli_update_receipt",
            },
            {
                "item": "app_background_watch_then_direct_repair_policy",
                "outcome": "covered_by_app_lane_notifier_and_direct_repair_gate",
            },
            {
                "item": "combined_receipt_generator",
                "outcome": "covered_by_this_x2_acceptance_runner",
            },
            {
                "item": "phase_advance_dependency_graph",
                "outcome": "embedded_in_dependency_graph",
            },
            {
                "item": "x2_build_use_acceptance_receipt",
                "outcome": "generated_by_this_runner",
            },
            {
                "item": "v504_v5_x1_launch_handoff",
                "outcome": "generated_as_companion_handoff",
            },
        ],
        "dependency_graph": graph,
        "essential_script_rows": scripts,
        "phase_policy": {
            "node_entrypoint_first": True,
            "windows_entrypoint_fallback_allowed": True,
            "five_minute_blocker_checks": True,
            "duration_is_completion_proof": False,
            "x1_requires_all_five_lane_receipts_or_blocker_receipts": True,
            "x2_uses_x1_tasks_for_build_run_test_install_use": True,
        },
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


def build_handoff(args: argparse.Namespace, acceptance: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "next_x1_launch_handoff",
        "phase_slug": args.next_phase_slug,
        "source_phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_NEXT_X1_HANDOFF_READY" if not acceptance["open_gaps"] else "OPEN_GAP_NEXT_X1_HANDOFF",
        "lane_contract": {
            "lanes_required": ["Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle"],
            "existing_lanes_only": True,
            "minimum_lane_work_minutes": 4,
            "manual_check_cadence_minutes": 5,
            "carryover_after_minutes": 15,
            "duration_is_completion_proof": False,
        },
        "launch_message_contract": [
            "Use existing lanes only; do not create replacement siblings, new old-style subagents, or new threads.",
            "Use x1 for research, reflection, design, source review, repair planning, and at least 20 eureka task proposals.",
            "Keep raw lane output private; publish only status receipts, hashes, counts, and curated summaries.",
            "Use Node entrypoint first for CLI launchers; fall back to Windows entrypoint only when the Node route is blocked.",
            "Check blockers every five minutes through watchers/notifiers; do not babysit lanes between scheduled checks.",
            "Carry unresolved long-running CLI work into x2 only with status receipts or explicit blocker receipts.",
            "Keep GMUT, canon, consciousness, and final-physics gates open unless exact future evidence closes them.",
        ],
        "x1_focus": [
            "Validate the GHC Multiplex IPC bus contract against the five-lane workflow.",
            "Prepare the first v2-branch continuity pass using the vision card and latest phase receipts.",
            "Refine command, skill, runner, and watcher inventory toward latest-essential-only usage.",
            "Generate implementation-ready tasks for the next x2 build/use phase.",
            "Advance Trinity Hybrid OS body tooling while preserving GMUT and Freed ID/CBR boundaries.",
        ],
        "handoff_inputs": {
            "acceptance_status": acceptance["overall_status"],
            "source_phase": args.phase_slug,
            "next_phase": args.next_phase_slug,
        },
        "publication_boundary": acceptance["publication_boundary"],
        "claim_boundary": acceptance["claim_boundary"],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md_acceptance(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} x2 Build/Use Acceptance Receipt",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- next_phase_slug: `{payload['next_phase_slug']}`",
        "",
        "## Build Queue Coverage",
    ]
    for row in payload["build_queue_coverage"]:
        lines.append(f"- {row['item']}: `{row['outcome']}`")
    lines.extend(["", "## Dependency Graph"])
    for row in payload["dependency_graph"]:
        lines.append(
            f"- {row['node']}: `{row['status']}` via `{row['receipt']}`; required for `{row['required_for']}`"
        )
    lines.extend(["", "## Essential Scripts"])
    for row in payload["essential_script_rows"]:
        lines.append(f"- {row['script']}: present `{str(row['present']).lower()}`, role `{row['role']}`")
    lines.extend(["", "Open gaps:"])
    if payload["open_gaps"]:
        lines.extend(f"- `{gap}`" for gap in payload["open_gaps"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Boundary: status-only receipts; no raw lane text, raw logs, session streams, screenshots, credentials, private dumps, or local absolute paths are published.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_md_handoff(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Launch Handoff",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- source_phase_slug: `{payload['source_phase_slug']}`",
        "",
        "## Lane Contract",
    ]
    contract = payload["lane_contract"]
    for key, value in contract.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Launch Message Contract"])
    lines.extend(f"- {item}" for item in payload["launch_message_contract"])
    lines.extend(["", "## x1 Focus"])
    lines.extend(f"- {item}" for item in payload["x1_focus"])
    lines.extend(
        [
            "",
            "Boundary: existing lanes only; status receipts only; no raw publication, no new threads, no old-style subagent spawning, and no GMUT/canon closure claim.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-phase-slug", required=True)
    parser.add_argument("--x1-closeout-json", required=True)
    parser.add_argument("--x2-prep-json", required=True)
    parser.add_argument("--cli-update-json", required=True)
    parser.add_argument("--ipc-json", required=True)
    parser.add_argument("--vision-json", required=True)
    parser.add_argument("--branch-json", required=True)
    parser.add_argument("--acceptance-json", required=True)
    parser.add_argument("--acceptance-md", required=True)
    parser.add_argument("--handoff-json", required=True)
    parser.add_argument("--handoff-md", required=True)
    args = parser.parse_args()

    receipts = {
        "x1_closeout": read_json(args.x1_closeout_json),
        "x2_prep": read_json(args.x2_prep_json),
        "cli_update": read_json(args.cli_update_json),
        "ipc": read_json(args.ipc_json),
        "vision": read_json(args.vision_json),
        "branch": read_json(args.branch_json),
    }
    acceptance = build_acceptance(args, receipts)
    handoff = build_handoff(args, acceptance)
    write_json(resolve(args.acceptance_json), acceptance)
    write_md_acceptance(resolve(args.acceptance_md), acceptance)
    write_json(resolve(args.handoff_json), handoff)
    write_md_handoff(resolve(args.handoff_md), handoff)
    print(
        json.dumps(
            {
                "status": acceptance["overall_status"],
                "handoff_status": handoff["overall_status"],
                "phase_slug": args.phase_slug,
                "next_phase_slug": args.next_phase_slug,
            },
            indent=2,
        )
    )
    return 0 if not acceptance["open_gaps"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
