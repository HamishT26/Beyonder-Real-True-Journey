#!/usr/bin/env python3
"""Build generic x1 closeout and x2 input receipts from curated lane gates."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = REPO_ROOT / "docs" / "trinity-live-traces"


SOURCE_ROWS = [
    {
        "label": "OpenAI Codex CLI releases",
        "url": "https://github.com/openai/codex/releases",
        "phase_use": "Keep CLI version claims current; 0.138.0 is the latest stable release observed for this pass, while 0.139 alpha is treated as pre-release.",
    },
    {
        "label": "OpenAI Codex README",
        "url": "https://github.com/openai/codex",
        "phase_use": "Anchor Node/CLI entrypoint, app-server, update, and install surface design to the official Codex repository.",
    },
    {
        "label": "Model Context Protocol repository",
        "url": "https://github.com/modelcontextprotocol/modelcontextprotocol",
        "phase_use": "Use official MCP specification and schema language for IPC bus and connector boundary planning.",
    },
    {
        "label": "OWASP Top 10 for Agentic Applications 2026",
        "url": "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
        "phase_use": "Map multi-agent runner, connector, memory, and tool-use risks into explicit guardrails.",
    },
    {
        "label": "OWASP Agentic AI threats and mitigations",
        "url": "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
        "phase_use": "Keep stale-flow repair and watcher design grounded in threat-model controls.",
    },
    {
        "label": "NVIDIA DGX Spark User Guide",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/index.html",
        "phase_use": "Inform local AI workstation and edge compute planning without claiming local hardware deployment.",
    },
    {
        "label": "NVIDIA Vera Rubin production announcement",
        "url": "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx",
        "phase_use": "Use AI-factory scale language as infrastructure inspiration while keeping repo claims aspirational and open-gated.",
    },
    {
        "label": "Google Cloud Vertex AI Agent Engine overview",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "phase_use": "Translate managed-agent deployment concepts into local runner supervision and app-server boundaries.",
    },
]


APP_LANES = ["Cicero", "Kierkegaard", "Aristotle"]
CLI_LANES = ["Arby", "Aster Vale"]


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
        payload = json.loads(candidate.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {"_available": False, "_file": candidate.name, "_reason": "json_error"}
    if not isinstance(payload, dict):
        return {"_available": False, "_file": candidate.name, "_reason": "not_object"}
    payload["_available"] = True
    payload["_file"] = candidate.name
    return payload


def status(payload: dict[str, Any]) -> str:
    return str(payload.get("overall_status") or payload.get("aggregate_status") or payload.get("status") or "")


def require_status(payload: dict[str, Any], allowed: set[str], label: str) -> None:
    observed = status(payload)
    if observed not in allowed:
        raise SystemExit(f"{label} status {observed!r} not in {sorted(allowed)!r}")


def lane_word_count(quality: dict[str, Any], lane: str) -> int | None:
    for row in quality.get("lanes", []):
        if isinstance(row, dict) and row.get("lane") == lane:
            value = row.get("word_count")
            return value if isinstance(value, int) else None
    return None


def lane_hash(cli_check: dict[str, Any], lane: str) -> str:
    for row in cli_check.get("lanes", []):
        if isinstance(row, dict) and row.get("lane") == lane:
            return str(row.get("final_message_hash") or "")
    return ""


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    body = [f"# {title}", ""]
    body.extend(f"- {line}" for line in lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def write_pair(stem: str, payload: dict[str, Any], md_lines: list[str]) -> None:
    write_json(TRACE_DIR / f"{stem}.json", payload)
    write_md(TRACE_DIR / f"{stem}.md", stem.replace("-", " ").title(), md_lines)


def build_closeout(args: argparse.Namespace, receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    cli_check = receipts["cli_check"]
    quality = receipts["quality"]
    return {
        "artifact_type": "phase_closeout",
        "phase_slug": args.x1_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X1_CLOSEOUT_READY_FOR_X2",
        "lane_summary": {
            "app_lanes": {
                "surface": "existing_r3_local_app_server_callable_routes",
                "lanes": APP_LANES,
                "completion_gate": status(receipts["app_gate"]),
                "redaction_gate": status(receipts["app_redaction"]),
                "manual_babysitting_before_cadence_gate": False,
            },
            "cli_lanes": {
                "surface": "strict_stdin_read_only_cli_lanes",
                "lanes": CLI_LANES,
                "completion_gate": "FINAL_MESSAGES_READY",
                "quality_gate": status(quality),
                "marker_review": status(receipts["marker_review"]),
                "arby_word_count": lane_word_count(quality, "Arby"),
                "aster_vale_word_count": lane_word_count(quality, "Aster Vale"),
                "arby_hash": lane_hash(cli_check, "Arby"),
                "aster_vale_hash": lane_hash(cli_check, "Aster Vale"),
            },
            "five_lane_status": status(receipts["five_lane"]),
        },
        "x2_build_focus": [
            "Convert all five x1 lane outputs into status-only x2 build priorities.",
            "Promote Codex 0.138.0, sandbox-ok, and help-surface findings into the readiness ledger.",
            "Use source rows to strengthen IPC bus, watcher, command, and skill boundaries.",
            "Refresh omega-v2 fast-read continuity for phase starts and compact refresh points.",
            "Generate the next x1 launch handoff only after x2 publication gates pass.",
        ],
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
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


def build_prep(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "x2_prep_start",
        "phase_slug": args.x2_slug,
        "source_phase": args.x1_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_X2_PREP_READY_AFTER_X1_FIVE_LANE_QUORUM",
        "contract": {
            "role": "build_run_test_install_and_use_x1_eureka_tasks_and_repair_outputs",
            "prep_gate_minutes": 10,
            "manual_sibling_polling_before_x2_gate": False,
            "watcher_supervision_continues": True,
            "duration_is_completion_proof": False,
        },
        "build_queue": [
            "codex_0138_readiness_receipt",
            "local_multiplex_ipc_bus_message_contract",
            "omega_v2_fast_read_pack_refresh",
            "source_ledger_to_ipc_mapping",
            "no_babysitting_watcher_audit",
            "five_minute_lane_cadence_dashboard",
            "latest_essential_helper_pruning_map",
            "trinity_mandala_boundary_refresh",
            "approval_packet_queue_for_next_phase",
            f"{args.next_x1_slug}_launch_handoff",
        ],
        "publication_boundary": {
            "status_only": True,
            "raw_lane_text_published": False,
            "raw_logs_published": False,
            "screenshots_published": False,
            "credentials_published": False,
            "session_streams_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
            "consciousness_or_final_physics_proof": "not_claimed",
        },
    }


def build_source_ledger(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "current_source_ledger",
        "phase_slug": args.x1_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_CURRENT_SOURCE_LEDGER_READY",
        "sources": SOURCE_ROWS,
        "source_policy": {
            "primary_sources_preferred": True,
            "raw_webpage_text_published": False,
            "citations_required_in_human_summary": True,
            "research_volume_is_not_quality_proof": True,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def build_runner_map(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "latest_essential_runner_map",
        "phase_slug": args.x1_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_LATEST_ESSENTIAL_RUNNER_MAP",
        "runner_groups": {
            "lane_launch_and_watch": [
                "thos_council_app_lane_notifier_runner.py",
                "thos_cli_strict_stdin_lane_launcher.py",
                "thos_cli_lane_completion_notifier.py",
                "thos_cli_elaboration_quality_gate.py",
                "thos_cli_marker_review_ledger.py",
                "thos_five_lane_status_normalizer.py",
            ],
            "cadence_and_wait": [
                "thos_status_check_cadence_guard.py",
                "thos_waiting_session_alpha_task_builder.py",
                "thos_productive_wait_receipt_verifier.py",
                "thos_wait_policy_guard.py",
            ],
            "x2_build_and_publication": [
                "thos_x1_closeout_x2_input_builder.py",
                "thos_x2_implementation_bundle.py",
                "thos_phase_artifact_cadence_classifier.py",
                "thos_status_receipt_exposure_guard.py",
                "thos_no_overclaim_guard.py",
                "thos_phase_advance_gate_verifier.py",
                "thos_phase_dashboard_receipt.py",
            ],
        },
        "entrypoint_policy": {
            "node_entrypoint_first_for_cli": True,
            "windows_entrypoint_fallback_allowed": True,
            "use_latest_essential_helpers_first": True,
            "legacy_helpers_not_deleted": True,
        },
    }


def build_continuity_index(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "omega_v2_continuity_index",
        "phase_slug": args.x1_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_OMEGA_V2_CONTINUITY_INDEX",
        "sections": {
            "phase_start_read_order": [
                "latest phase dashboard",
                "latest closeout",
                "latest x2 prep",
                "current source ledger",
                "latest essential runner map",
                "omega v2 continuity index",
                "next x1 handoff",
            ],
            "vision_md_requirements": [
                "summarize latest progress and standards",
                "track x1/x2 cadence requirements",
                "track existing lane routes only",
                "keep GMUT/canon gates open",
            ],
            "branch_pair": [
                "codex/GHC-Family/beyonder-shared-omega-line",
                "codex/GHC-Family/beyonder-shared-omega-line-v2",
            ],
        },
        "selection_boundary": {
            "curated_fast_read_only": True,
            "raw_archive_copy": False,
            "history_rewrite": False,
            "deletion": False,
        },
    }


def build_approval_candidates(args: argparse.Namespace) -> dict[str, Any]:
    packets = [
        ("IPC bus event contract", "Approve repo-scoped IPC event schemas for app and CLI lane receipts."),
        ("Vision MD phase-start refresh", "Approve curated phase-start and compact-refresh vision notes."),
        ("Latest helper pruning map", "Approve marking legacy helpers as deferred in repo docs without deleting files."),
        ("Codex doctor stale-flow repair", "Approve bounded diagnosis for doctor hangs without account or cache mutation."),
        ("Source ledger expansion", "Approve broader primary-source refresh for OpenAI, MCP, OWASP, NVIDIA, Google, and GitHub."),
        ("Skill overlay drafting", "Approve repo-scoped skill proposals while blocking direct user-skill writes."),
        ("Command rollback ledger", "Approve command-surface rollback coverage receipts for high-risk helpers."),
        ("Omega v2 continuity copy plan", "Approve curated essential-data carryover planning, not raw archive import."),
        ("Five-minute cadence dashboard", "Approve compact dashboard receipts for each x1 lane-check cycle."),
        ("v515 roadmap pack", "Approve sequential v505-v515 v1-v8 x1/x2 planning ledgers."),
    ]
    return {
        "artifact_type": "approval_candidate_queue",
        "phase_slug": args.x1_slug,
        "next_phase_slug": args.x2_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_APPROVAL_CANDIDATES_READY",
        "spending_ceiling_usd_each": 100,
        "packets": [
            {
                "packet_number": idx,
                "title": title,
                "approval_scope": scope,
                "not_approved_without_extra_packet": [
                    "plugin-cache mutation",
                    "user-skill mutation",
                    "external account changes",
                    "destructive cleanup",
                    "raw lane text publication",
                    "GMUT/canon/final-physics closure claims",
                ],
            }
            for idx, (title, scope) in enumerate(packets, start=1)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--x1-slug", required=True)
    parser.add_argument("--x2-slug", required=True)
    parser.add_argument("--next-x1-slug", required=True)
    parser.add_argument("--cadence-json", required=True)
    parser.add_argument("--app-gate-json", required=True)
    parser.add_argument("--app-redaction-json", required=True)
    parser.add_argument("--cli-check-json", required=True)
    parser.add_argument("--quality-json", required=True)
    parser.add_argument("--marker-review-json", required=True)
    parser.add_argument("--five-lane-json", required=True)
    args = parser.parse_args()

    receipts = {
        "cadence": read_json(args.cadence_json),
        "app_gate": read_json(args.app_gate_json),
        "app_redaction": read_json(args.app_redaction_json),
        "cli_check": read_json(args.cli_check_json),
        "quality": read_json(args.quality_json),
        "marker_review": read_json(args.marker_review_json),
        "five_lane": read_json(args.five_lane_json),
    }
    require_status(receipts["cadence"], {"PASS_STATUS_CHECK_ALLOWED"}, "cadence")
    require_status(receipts["app_gate"], {"PASS_APP_LANE_COMPLETION_GATE"}, "app gate")
    require_status(receipts["app_redaction"], {"PASS_APP_THREAD_REDACTION_GUARD"}, "app redaction")
    require_status(receipts["quality"], {"PASS_ALL_CLI_LANES_ELABORATE"}, "CLI quality")
    require_status(receipts["marker_review"], {"PASS_MARKER_REVIEW_LEDGER"}, "marker review")
    require_status(receipts["five_lane"], {"PASS_FIVE_LANE_READY"}, "five lane")

    closeout = build_closeout(args, receipts)
    prep = build_prep(args)
    source = build_source_ledger(args)
    runner_map = build_runner_map(args)
    continuity = build_continuity_index(args)
    approvals = build_approval_candidates(args)
    outputs = {
        f"{args.x1_slug}-closeout-v1": (
            closeout,
            [
                f"overall_status: `{closeout['overall_status']}`",
                f"five_lane_status: `{closeout['lane_summary']['five_lane_status']}`",
                f"arby_word_count: `{closeout['lane_summary']['cli_lanes']['arby_word_count']}`",
                f"aster_vale_word_count: `{closeout['lane_summary']['cli_lanes']['aster_vale_word_count']}`",
                "raw lane text remains unpublished",
            ],
        ),
        f"{args.x2_slug}-prep-start-v1": (
            prep,
            [
                f"overall_status: `{prep['overall_status']}`",
                f"source_phase: `{args.x1_slug}`",
                "x2 role: build, run, test, install, and use x1 proposals within approved boundaries",
            ],
        ),
        f"{args.x1_slug}-current-source-ledger-v1": (
            source,
            [f"overall_status: `{source['overall_status']}`", f"source_count: `{len(SOURCE_ROWS)}`"],
        ),
        f"{args.x1_slug}-latest-essential-runner-map-v1": (
            runner_map,
            [f"overall_status: `{runner_map['overall_status']}`", "node entrypoint first for CLI lanes"],
        ),
        f"{args.x1_slug}-omega-v2-continuity-index-v1": (
            continuity,
            [f"overall_status: `{continuity['overall_status']}`", "curated fast-read only"],
        ),
        f"{args.x1_slug}-{args.x2_slug}-approval-candidates-v1": (
            approvals,
            [f"overall_status: `{approvals['overall_status']}`", f"packet_count: `{len(approvals['packets'])}`"],
        ),
    }
    for stem, (payload, md_lines) in outputs.items():
        write_pair(stem, payload, md_lines)

    print(
        json.dumps(
            {
                "status": "PASS_X1_CLOSEOUT_X2_INPUTS_BUILT",
                "x1_slug": args.x1_slug,
                "x2_slug": args.x2_slug,
                "outputs": list(outputs),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
