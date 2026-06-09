#!/usr/bin/env python3
"""Generate a status-only x2 implementation bundle and next x1 handoff.

The bundle translates an x1 closeout, x2 prep-start, source ledger, runner map,
and continuity index into concrete build/use receipts without reading raw
sibling output or claiming GMUT/canon closure.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


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
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def source_rows(source_ledger: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for row in source_ledger.get("sources", []):
        if isinstance(row, dict):
            rows.append(
                {
                    "label": str(row.get("label", "")),
                    "url": str(row.get("url", "")),
                    "phase_use": str(row.get("phase_use", "")),
                }
            )
    return rows


def build_items(prep: dict[str, Any]) -> list[str]:
    queue = prep.get("build_queue")
    if isinstance(queue, list):
        return [str(item) for item in queue]
    return []


def build_implementation(args: argparse.Namespace, receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    queue = build_items(receipts["prep"])
    sources = source_rows(receipts["source"])
    missing = [name for name, payload in receipts.items() if not payload.get("_available")]
    status_gaps = [
        f"{name}:{status(payload)}"
        for name, payload in receipts.items()
        if payload.get("_available")
        and name in {"closeout", "prep", "source", "runner_map", "continuity"}
        and not status(payload).startswith("PASS_")
    ]
    coverage = [
        {
            "build_item": "valid_cadence_status_board_consolidation",
            "implementation": "Require cadence receipt, app gate, CLI quality, marker review, five-lane normalizer, classifier, exposure, phase advance, and dashboard receipts before phase advance.",
            "evidence": "phase_advance_and_dashboard_receipts",
        },
        {
            "build_item": "app_redaction_dependency_gate",
            "implementation": "Require app receipt thread redaction before app completion receipts feed publication or phase advance.",
            "evidence": "app_thread_redaction_receipts",
        },
        {
            "build_item": "cli_long_form_carryover_quality_gate",
            "implementation": "Use strict CLI completion, elaboration quality, and marker review as the accepted long-form CLI gate.",
            "evidence": "cli_quality_and_marker_review_receipts",
        },
        {
            "build_item": "source_ledger_to_ipc_mapping",
            "implementation": "Map official OpenAI, MCP, OWASP, NVIDIA, and Google source notes into status-only IPC event vocabulary.",
            "evidence": "current_source_ledger",
        },
        {
            "build_item": "omega_v2_fast_read_pack",
            "implementation": "Use continuity index sections and current phase dashboard as the fast-read surface for phase starts and compact refreshes.",
            "evidence": "omega_v2_continuity_index",
        },
        {
            "build_item": "no_babysitting_watcher_audit",
            "implementation": "Treat premature probes as stale-flow learning and require scheduled cadence receipts for status harvests.",
            "evidence": "productive_wait_plan_and_cadence_receipts",
        },
        {
            "build_item": "latest_essential_helper_pruning_map",
            "implementation": "Prefer current app, CLI, cadence, publication, IPC, and continuity helpers over older versioned helpers without deleting legacy files.",
            "evidence": "latest_essential_runner_map",
        },
        {
            "build_item": "trinity_mandala_boundary_refresh",
            "implementation": "Keep GMUT mind, THOS body, and Freed ID/CBR heart language open-gated and evidence-led.",
            "evidence": "claim_boundary_fields",
        },
        {
            "build_item": "phase_runtime_foothold_ledger",
            "implementation": "Record durations and word counts as footholds only, never as completion proof.",
            "evidence": "five_lane_status_and_closeout",
        },
        {
            "build_item": "v504_v7_x1_launch_handoff",
            "implementation": "Generate a next x1 handoff with existing-lane-only routing, Node entrypoint first, and five-minute cadence.",
            "evidence": "next_handoff_generated_by_this_bundle",
        },
    ]
    return {
        "artifact_type": "x2_implementation_ledger",
        "phase_slug": args.phase_slug,
        "next_phase_slug": args.next_phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_IMPLEMENTATION_LEDGER"
        if not missing and not status_gaps
        else "OPEN_GAP_X2_IMPLEMENTATION_LEDGER",
        "missing_inputs": missing,
        "status_gaps": status_gaps,
        "source_count": len(sources),
        "build_queue": queue,
        "implementation_coverage": coverage,
        "use_results": [
            "Current-source ledger is converted into IPC-safe design language.",
            "Valid cadence is promoted from guidance into a phase-advance dependency.",
            "App thread redaction is promoted from cleanup into a publication precondition.",
            "CLI long-form quality is captured by word count, heading coverage, marker review, and hash-only evidence.",
            "Omega v2 continuity is treated as a curated fast-read surface rather than a raw archive copy.",
            "Next x1 launch remains existing-lane-only with Node entrypoint first for CLI lanes.",
        ],
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "prompt_body_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "session_streams_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
            "duration_is_completion_proof": False,
        },
    }


def build_source_ipc(args: argparse.Namespace, source: dict[str, Any]) -> dict[str, Any]:
    mappings = [
        {
            "source_family": row["label"],
            "ipc_event_use": "source_ledger",
            "guardrail": row["phase_use"],
        }
        for row in source_rows(source)
    ]
    return {
        "artifact_type": "source_ledger_to_ipc_mapping",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_SOURCE_LEDGER_TO_IPC_MAPPING",
        "mappings": mappings,
        "ipc_event_contract": {
            "required_fields": [
                "message_type",
                "phase_slug",
                "generated_utc",
                "status",
                "summary",
                "evidence_receipts",
                "raw_boundary",
            ],
            "forbidden_payloads": [
                "raw_webpage_text",
                "private_connector_payload",
                "credentials",
                "screenshots",
                "session_streams",
                "raw_lane_text",
            ],
        },
        "publication_boundary": {
            "status_only": True,
            "raw_webpage_text_published": False,
            "private_connector_payload_published": False,
            "credentials_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def build_fast_read(args: argparse.Namespace, continuity: dict[str, Any], runner_map: dict[str, Any]) -> dict[str, Any]:
    sections = continuity.get("sections") if isinstance(continuity.get("sections"), dict) else {}
    runner_groups = runner_map.get("runner_groups") if isinstance(runner_map.get("runner_groups"), dict) else {}
    return {
        "artifact_type": "omega_v2_fast_read_pack",
        "phase_slug": args.phase_slug,
        "next_phase_slug": args.next_phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_OMEGA_V2_FAST_READ_PACK",
        "read_order": [
            "latest_phase_dashboard",
            "latest_closeout",
            "latest_x2_prep",
            "current_source_ledger",
            "latest_essential_runner_map",
            "omega_v2_continuity_index",
            "next_x1_handoff",
        ],
        "continuity_section_counts": {name: len(rows) if isinstance(rows, list) else 0 for name, rows in sections.items()},
        "runner_group_counts": {name: len(rows) if isinstance(rows, list) else 0 for name, rows in runner_groups.items()},
        "selection_boundary": {
            "curated_fast_read_only": True,
            "raw_archive_copy": False,
            "history_rewrite": False,
            "deletion": False,
        },
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "credentials_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def build_watcher_audit(args: argparse.Namespace, prep: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "no_babysitting_watcher_audit",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_NO_BABYSITTING_WATCHER_AUDIT",
        "audit_rules": [
            "Harvest only at valid cadence marks unless an explicit blocker requires repair.",
            "Treat premature probes as stale-flow learning and do not use them as phase evidence.",
            "Continue x2 build/use work while app and CLI lanes run under watchers.",
            "Phase advance requires all five lanes or curated blocker receipts.",
            "Duration remains a foothold, not completion proof.",
        ],
        "prep_contract": prep.get("contract", {}),
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "session_streams_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def build_runtime_foothold(args: argparse.Namespace, closeout: dict[str, Any]) -> dict[str, Any]:
    cli = closeout.get("lane_summary", {}).get("cli_lanes", {})
    app = closeout.get("lane_summary", {}).get("app_lanes", {})
    return {
        "artifact_type": "phase_runtime_foothold_ledger",
        "phase_slug": args.phase_slug,
        "source_phase": closeout.get("phase_slug"),
        "generated_utc": utc_now(),
        "overall_status": "PASS_PHASE_RUNTIME_FOOTHOLD_LEDGER",
        "footholds": {
            "app_lanes": app.get("lanes", []),
            "cli_lanes": cli.get("lanes", []),
            "arby_word_count": cli.get("arby_word_count"),
            "aster_vale_word_count": cli.get("aster_vale_word_count"),
            "five_lane_status": closeout.get("lane_summary", {}).get("five_lane_status"),
        },
        "interpretation": {
            "word_counts_are_quality_evidence": True,
            "duration_is_completion_proof": False,
            "hashes_and_counts_replace_raw_publication": True,
        },
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "credentials_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def build_handoff(args: argparse.Namespace, implementation: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "next_x1_launch_handoff",
        "phase_slug": args.next_phase_slug,
        "source_phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_NEXT_X1_HANDOFF_READY"
        if implementation["overall_status"].startswith("PASS")
        else "OPEN_GAP_NEXT_X1_HANDOFF",
        "lane_contract": {
            "lanes_required": ["Arby", "Aster Vale", "Cicero", "Kierkegaard", "Aristotle"],
            "existing_lanes_only": True,
            "minimum_lane_work_minutes": 4,
            "manual_check_cadence_minutes": 5,
            "node_entrypoint_first_for_cli": True,
            "duration_is_completion_proof": False,
        },
        "launch_focus": [
            "Use x1 for source review, reflection, design, and eureka task proposals.",
            "Use watchers and notifiers for status; do not babysit between cadence marks.",
            "Keep all raw lane text private and publish only curated receipts.",
            "Carry v504 v6 x2 build results into the next x1 prompt contract.",
            "Keep GMUT, canon, consciousness, and final-physics gates open.",
        ],
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "credentials_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    title = payload["artifact_type"].replace("_", " ").title()
    lines = [
        f"# {payload['phase_slug']} {title}",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- overall_status: `{payload['overall_status']}`",
    ]
    if payload.get("next_phase_slug"):
        lines.append(f"- next_phase_slug: `{payload['next_phase_slug']}`")
    if payload.get("source_phase_slug"):
        lines.append(f"- source_phase_slug: `{payload['source_phase_slug']}`")
    for key in [
        "implementation_coverage",
        "use_results",
        "mappings",
        "read_order",
        "audit_rules",
        "footholds",
        "launch_focus",
    ]:
        if key not in payload:
            continue
        lines.extend(["", f"## {key.replace('_', ' ').title()}"])
        value = payload[key]
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    label = item.get("build_item") or item.get("source_family") or item.get("id") or "item"
                    detail = item.get("implementation") or item.get("guardrail") or item.get("scope") or item
                    lines.append(f"- {label}: {detail}")
                else:
                    lines.append(f"- {item}")
        elif isinstance(value, dict):
            for item_key, item_value in value.items():
                lines.append(f"- {item_key}: `{item_value}`")
    lines.extend(
        [
            "",
            "Boundary: status-only bundle; no raw lane text, raw logs, prompt bodies, screenshots, credentials, session streams, private connector payloads, or local absolute paths.",
            "",
            "GMUT, canon, consciousness, and final-physics gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_pair(prefix: str, payload: dict[str, Any]) -> None:
    write_json(REPO_ROOT / f"{prefix}.json", payload)
    write_md(REPO_ROOT / f"{prefix}.md", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-phase-slug", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--prep-json", required=True)
    parser.add_argument("--source-ledger-json", required=True)
    parser.add_argument("--runner-map-json", required=True)
    parser.add_argument("--continuity-index-json", required=True)
    parser.add_argument("--output-prefix", required=True)
    args = parser.parse_args()

    receipts = {
        "closeout": read_json(args.closeout_json),
        "prep": read_json(args.prep_json),
        "source": read_json(args.source_ledger_json),
        "runner_map": read_json(args.runner_map_json),
        "continuity": read_json(args.continuity_index_json),
    }
    output_prefix = args.output_prefix.rstrip(".")
    implementation = build_implementation(args, receipts)
    source_ipc = build_source_ipc(args, receipts["source"])
    fast_read = build_fast_read(args, receipts["continuity"], receipts["runner_map"])
    watcher_audit = build_watcher_audit(args, receipts["prep"])
    runtime_foothold = build_runtime_foothold(args, receipts["closeout"])
    handoff = build_handoff(args, implementation)

    outputs = {
        "implementation-ledger": implementation,
        "source-ledger-to-ipc-mapping": source_ipc,
        "omega-v2-fast-read-pack": fast_read,
        "no-babysitting-watcher-audit": watcher_audit,
        "phase-runtime-foothold-ledger": runtime_foothold,
        "launch-handoff": handoff,
    }
    for suffix, payload in outputs.items():
        emit_pair(f"{output_prefix}-{suffix}-v1", payload)

    all_pass = all(str(payload["overall_status"]).startswith("PASS") for payload in outputs.values())
    print(
        json.dumps(
            {
                "status": "PASS_X2_IMPLEMENTATION_BUNDLE" if all_pass else "OPEN_GAP_X2_IMPLEMENTATION_BUNDLE",
                "phase_slug": args.phase_slug,
                "next_phase_slug": args.next_phase_slug,
                "outputs": list(outputs),
            },
            indent=2,
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
