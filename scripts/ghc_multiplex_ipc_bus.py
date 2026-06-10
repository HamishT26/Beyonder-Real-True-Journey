#!/usr/bin/env python3
"""Create a status-only GHC Multiplex IPC bus manifest.

The bus is a repo-scoped coordination contract, not a daemon. It defines the
safe message shapes used by app lanes, CLI lanes, watchers, repair helpers,
phase gates, vision cards, and approval packets without reading or publishing
raw sibling text.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MESSAGE_TYPES = [
    "phase_start",
    "compact_refresh",
    "app_lane_event",
    "cli_lane_event",
    "watcher_status",
    "repair_status",
    "gate_status",
    "approval_packet",
    "branch_plan",
    "source_ledger",
    "vision_card",
]

FORBIDDEN_FIELDS = [
    "raw_lane_text",
    "raw_transport",
    "session_stream",
    "screenshot",
    "credential",
    "private_dump",
    "local_absolute_path",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text_if_present(path: str | None) -> str | None:
    if not path:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    return candidate.name


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "ghc_multiplex_ipc_bus_manifest",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_GHC_MULTIPLEX_IPC_BUS_SCAFFOLD",
        "bus_scope": {
            "repo_scoped": True,
            "daemon_started": False,
            "external_account_mutation": False,
            "public_deployment": False,
            "status_only": True,
        },
        "preferred_routes": {
            "cli": "node_codex_entrypoint_first_then_windows_fallback",
            "app": "background_watch_then_gate_only_harvest_then_direct_repair",
            "phase": "five_minute_blocker_checks_with_all_five_lane_closeout",
            "continuity": "vision_card_at_phase_start_and_compact_refresh",
        },
        "message_types": MESSAGE_TYPES,
        "message_contract": {
            "required_fields": [
                "message_type",
                "phase_slug",
                "generated_utc",
                "status",
                "summary",
                "evidence_receipts",
                "raw_boundary",
            ],
            "forbidden_fields": FORBIDDEN_FIELDS,
            "raw_boundary_required_values": [
                "status_only",
                "temp_only_not_published",
                "redacted",
            ],
        },
        "cadence_policy": {
            "blocker_check_minutes": 5,
            "x1_carryover_minutes": 15,
            "x2_prep_minimum_minutes": 10,
            "duration_is_completion_proof": False,
            "phase_advance_requires_all_five_lanes_or_blocker_receipts": True,
        },
        "continuity_inputs": {
            "vision_card": read_text_if_present(args.vision_md),
            "compact_refresh_required": True,
            "journey_v49_reference": "docs/journey-context/Beyonder-Real-True Journey v49 (Aletheon & Codex CLI and App siblings).txt",
        },
        "guardrails": {
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "session_streams_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
            "plugin_cache_mutation": False,
            "user_skill_mutation": False,
            "new_threads_created": False,
            "old_style_subagents_spawned": False,
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
        f"# {payload['phase_slug']} GHC Multiplex IPC Bus Manifest",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "- daemon_started: `false`",
        "- publication: `status_only`",
        "",
        "## Preferred Routes",
    ]
    for key, value in payload["preferred_routes"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Message Types"])
    for item in payload["message_types"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Cadence Policy",
            f"- blocker_check_minutes: `{payload['cadence_policy']['blocker_check_minutes']}`",
            f"- x1_carryover_minutes: `{payload['cadence_policy']['x1_carryover_minutes']}`",
            f"- x2_prep_minimum_minutes: `{payload['cadence_policy']['x2_prep_minimum_minutes']}`",
            "- duration_is_completion_proof: `false`",
            "- phase_advance_requires_all_five_lanes_or_blocker_receipts: `true`",
            "",
            "## Boundary",
            "",
            "This manifest defines a status-only coordination contract. It does not start a daemon, read raw sibling output, publish raw logs, mutate accounts, create new threads, spawn old-style subagents, or claim GMUT/canon closure.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--vision-md")
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    manifest = build_manifest(args)
    write_json(Path(args.receipt_json), manifest)
    write_md(Path(args.receipt_md), manifest)
    print(json.dumps({"status": manifest["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
