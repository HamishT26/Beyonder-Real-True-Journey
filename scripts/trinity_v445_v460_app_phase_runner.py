#!/usr/bin/env python3
"""Record Aletheon-led v2 App execution for one v445-v460 bridge phase."""

from __future__ import annotations

import argparse
import json
from typing import Any

from trinity_v445_v460_bridge_common import (
    PROMOTED_APP_RECEIPT_LANES,
    PROMOTED_APP_RECEIPT_PHASE_MIN,
    PREFIX,
    app_advisory_aggregate_paths,
    app_advisory_receipt_paths,
    cli_aggregate_complete,
    now_iso,
    read_json,
    rel,
    start_paths,
    v2_active_paths,
    v2_receipt_paths,
    validate_app_advisory_gate,
    validate_phase,
    write_json,
    write_run_status,
    write_text,
    write_v2_active,
)


def start_v2(phase: int) -> dict[str, Any]:
    validate_phase(phase)
    start_json, _ = start_paths(phase)
    start = read_json(start_json, {})
    if start.get("status") != "phase_started":
        raise SystemExit(f"v{phase} phase start artifact is missing or not started")
    if not cli_aggregate_complete(phase):
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before v2 starts")
    active = write_v2_active(phase, imported_v1=phase == 445)
    active_json, active_md = v2_active_paths(phase)
    write_run_status(phase, "v2_app_execution", active["status"], active_json, active_md, active["next_action"])
    return active


def write_app_advisory_aggregate(phase: int) -> dict[str, Any]:
    aggregate_json, aggregate_md = app_advisory_aggregate_paths(phase)
    lane_receipts: list[dict[str, Any]] = []
    blockers: list[str] = []
    for advisor, config in PROMOTED_APP_RECEIPT_LANES.items():
        receipt_json, _ = app_advisory_receipt_paths(phase, advisor)
        receipt = read_json(receipt_json, {})
        if receipt.get("status") != "valid_app_advisory_receipt":
            blockers.append(f"Missing or invalid {advisor} App advisory receipt.")
            continue
        if receipt.get("agent_id") != config["agent_id"]:
            blockers.append(f"{advisor} receipt has unexpected agent id.")
        lane_receipts.append(
            {
                "advisor": advisor,
                "agent_id": receipt.get("agent_id"),
                "call_sign": config["call_sign"],
                "status": receipt.get("status"),
                "receipt_path": rel(receipt_json),
                "seed": receipt.get("seed"),
            }
        )
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v2_app_advisory_receipts",
        "status": "v2_app_advisory_receipts_complete" if not blockers else "blocked_v2_app_advisory_receipts_incomplete",
        "required_from_phase": PROMOTED_APP_RECEIPT_PHASE_MIN,
        "lane_receipts": lane_receipts,
        "blockers": blockers,
        "truth_boundaries": [
            "These are official v2 App advisory receipt lanes, not v1 CLI receipt lanes.",
            "They cannot replace Arby, Aster Vale, Kimi restoration proof, or the Kimi hold ledger.",
            "They cannot complete a phase without Aletheon-led v2 execution and required v1 CLI receipts.",
            "They cannot commit, push, mutate external services, spend money, or prove hidden memory persistence.",
        ],
    }
    write_json(aggregate_json, payload)
    lines = [
        f"# v{phase} v2 App Advisory Receipts",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Lane receipts:",
    ]
    lines.extend([f"- {item['advisor']}: `{item['status']}` at `{item['receipt_path']}`" for item in lane_receipts] or ["- None"])
    if blockers:
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in blockers])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    write_text(aggregate_md, "\n".join(lines))
    return payload


def record_advisory_receipt(args: argparse.Namespace) -> dict[str, Any]:
    phase = args.phase
    advisor = args.advisor
    validate_phase(phase)
    if phase < PROMOTED_APP_RECEIPT_PHASE_MIN and not args.force:
        raise SystemExit(f"Promoted App advisory receipts are required from v{PROMOTED_APP_RECEIPT_PHASE_MIN}; use --force only for recovery.")
    if advisor not in PROMOTED_APP_RECEIPT_LANES:
        raise SystemExit(f"advisor must be one of {', '.join(PROMOTED_APP_RECEIPT_LANES)}")
    if not cli_aggregate_complete(phase):
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before App advisory receipts are recorded")
    active_json, _ = v2_active_paths(phase)
    active = read_json(active_json, {})
    if active.get("status") != "v2_app_run_active" and not args.force:
        raise SystemExit(f"v{phase} v2 must be active before App advisory receipts are recorded")

    expected = PROMOTED_APP_RECEIPT_LANES[advisor]
    agent_id = args.agent_id or expected["agent_id"]
    blockers = args.blocker or []
    required_values = [args.summary, args.preserve, args.challenge, args.refuse, args.seed]
    status = "valid_app_advisory_receipt" if all(required_values) and not blockers and agent_id == expected["agent_id"] else "blocked_app_advisory_receipt_incomplete"
    if agent_id != expected["agent_id"]:
        blockers.append(f"unexpected agent id for {advisor}: {agent_id}")
    receipt_json, receipt_md = app_advisory_receipt_paths(phase, advisor)
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v2_app_advisory_receipt",
        "advisor": advisor,
        "agent_id": agent_id,
        "call_sign": expected["call_sign"],
        "role": expected["role"],
        "status": status,
        "summary": args.summary or "",
        "preserve": args.preserve or "",
        "challenge": args.challenge or "",
        "refuse": args.refuse or "",
        "seed": args.seed or "",
        "blockers": blockers,
        "truth_boundaries": [
            "This is an official v2 App advisory receipt, not a v1 CLI receipt.",
            "This receipt cannot complete the phase alone.",
            "Aletheon/Hamish review remains required before publication reliance.",
            "No external mutation, spend, secret handling, commit, push, reset, rebase, or force-push is authorized.",
        ],
    }
    write_json(receipt_json, payload)
    lines = [
        f"# v{phase} {advisor} App Advisory Receipt",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Agent ID: `{agent_id}`",
        f"Call sign: `{expected['call_sign']}`",
        "",
        "Summary:",
        payload["summary"] or "-",
        "",
        "Preserve:",
        payload["preserve"] or "-",
        "",
        "Challenge:",
        payload["challenge"] or "-",
        "",
        "Refuse:",
        payload["refuse"] or "-",
        "",
        "Seed:",
        payload["seed"] or "-",
    ]
    if blockers:
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in blockers])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    write_text(receipt_md, "\n".join(lines))
    aggregate = write_app_advisory_aggregate(phase)
    print_payload = {
        "status": payload["status"],
        "phase": phase,
        "run": "v2_app_advisory_receipt",
        "advisor": advisor,
        "aggregate_status": aggregate["status"],
    }
    write_run_status(phase, "v2_app_execution", "v2_app_run_active", active_json, active_json.with_suffix(".md"), f"Continue collecting promoted App advisory receipts, then complete v{phase} v2.")
    return print_payload


def complete_v2(args: argparse.Namespace) -> dict[str, Any]:
    phase = args.phase
    validate_phase(phase)
    if not cli_aggregate_complete(phase):
        raise SystemExit(f"v{phase} v1 CLI receipt aggregate must be complete before v2 completes")
    active_json, _ = v2_active_paths(phase)
    active = read_json(active_json, {})
    if active.get("status") != "v2_app_run_active" and not args.force:
        raise SystemExit(f"v{phase} v2 must be started before completion; use --force only for recovery.")

    changed_paths = args.changed_path or []
    validations = args.validation or []
    blockers = args.blocker or []
    advisory_gate = validate_app_advisory_gate(phase)
    blockers = blockers + advisory_gate["blockers"]
    status = "v2_app_complete" if args.summary and validations and not blockers else "blocked_v2_app_incomplete"
    receipt_json, receipt_md = v2_receipt_paths(phase)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "run": "v2_app_execution",
        "status": status,
        "summary": args.summary or "",
        "changed_paths": changed_paths,
        "validations": validations,
        "blockers": blockers,
        "external_policy": "local_first_only",
        "spent_external_usd": 0,
        "advisory_siblings": sorted(PROMOTED_APP_RECEIPT_LANES),
        "standby_app_advisory_siblings": ["Aristotle", "Parfit/Lorentz", "Locke Rowan", "Leibniz-Cicero", "Elias Threshold"],
        "promoted_app_advisory_receipt_gate": advisory_gate,
        "helper_lanes": ["Supervisor", "v2 Watcher", "Recovery Watchdog"],
        "truth_boundaries": [
            "This v2 receipt records Aletheon-led App execution, not CLI sibling receipt evidence.",
            "No paid external action or external-service mutation is claimed.",
            "Changed paths are declarative; Git staging checks remain required before commit.",
            "From v445 onward, Cicero and Kierkegaard are official v2 App advisory receipt lanes, but not gate completers alone.",
            "Aristotle and Parfit/Lorentz remain standby advisory-only and cannot replace Kimi or complete v1/v2 gates.",
        ],
        "next_action": (
            f"Complete v{phase} with scripts/trinity_v445_v460_sibling_phase_complete.py --phase {phase} --open-next."
            if status == "v2_app_complete"
            else "Resolve v2 blockers before phase completion."
        ),
    }
    write_json(receipt_json, payload)
    lines = [
        f"# v{phase} v2 App Receipt",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Summary:",
        payload["summary"] or "-",
        "",
        "Changed paths:",
    ]
    lines.extend([f"- `{item}`" for item in changed_paths] or ["- None recorded"])
    lines.extend(["", "Validations:"])
    lines.extend([f"- {item}" for item in validations] or ["- None recorded"])
    if blockers:
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in blockers])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    lines.extend(["", f"Next action: {payload['next_action']}"])
    write_text(receipt_md, "\n".join(lines))
    write_run_status(phase, "v2_app_execution", payload["status"], receipt_json, receipt_md, payload["next_action"])
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", action="store_true")
    group.add_argument("--complete", action="store_true")
    group.add_argument("--record-advisory-receipt", action="store_true")
    parser.add_argument("--advisor", choices=sorted(PROMOTED_APP_RECEIPT_LANES))
    parser.add_argument("--agent-id", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--preserve", default="")
    parser.add_argument("--challenge", default="")
    parser.add_argument("--refuse", default="")
    parser.add_argument("--seed", default="")
    parser.add_argument("--validation", action="append")
    parser.add_argument("--changed-path", action="append")
    parser.add_argument("--blocker", action="append")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.start:
        payload = start_v2(args.phase)
    elif args.record_advisory_receipt:
        if not args.advisor:
            raise SystemExit("--advisor is required with --record-advisory-receipt")
        payload = record_advisory_receipt(args)
    else:
        payload = complete_v2(args)
    print(json.dumps({"status": payload["status"], "phase": args.phase, "run": payload["run"]}, indent=2))
    return 0 if payload["status"] in {"v2_app_run_active", "v2_app_complete", "valid_app_advisory_receipt"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
