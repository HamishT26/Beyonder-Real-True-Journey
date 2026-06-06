#!/usr/bin/env python3
"""Build status-safe x1 sibling prompts with productive-waiting policy."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


V497_EXTENDED_RE = re.compile(r"^v497-gmut-thos-v33-v(?P<version>[2-8])-x1$")


def extended_v497_packet_active(phase_slug: str) -> bool:
    return bool(V497_EXTENDED_RE.match(phase_slug))


def build_prompt(lane: str, phase_slug: str, next_phase_slug: str | None = None) -> str:
    next_text = f" then {next_phase_slug}" if next_phase_slug else ""
    if extended_v497_packet_active(phase_slug):
        return (
            f"Existing {lane} advisory lane pass for {phase_slug}{next_text}. "
            "Operate as a read-only advisory voice only. Do not use shell, tools, external commands, "
            "file writes, account actions, destructive actions, or raw transport publication. "
            "This phase is covered by the approved v497 v2-v8 GMUT/THOS approval tapestry. "
            "Use a one-hour x1 planning, research, internalization, design, and preparation target where runtime allows; "
            "duration is an operating target, not completion proof. "
            "Prepare an elaborate x1 advisory artifact for the x2 build/run/test/install/use phase. "
            "Do not finish with a compact advisory if you can still expand useful detail. "
            "Use these exact uppercase section headings so the quality gate can verify the artifact: "
            "COMMAND PROPOSALS (10+), SYSTEM EXPANSION PROPOSALS (10+), SKILL OR MICRO-WORKFLOW PROPOSALS (10+), "
            "EUREKA TASKS (10+), RISKS AND BLOCKERS, X2 BUILD PRIORITIES. "
            "Under each of the four proposal sections, provide at least 10 numbered items with concrete purpose, "
            "safe implementation shape, validation signal, and how it helps the next x2 phase. "
            "Target 2500+ words where runtime and output budget allow; if budget is tight, prioritize complete structured coverage "
            "over prose flourish. Cover the Trinity Mandala pillars: GMUT as Mind, Trinity Hybrid OS as Body, "
            "and Freed ID/CBR as Heart. Include risks, blocker classes, watcher/notifier resilience, "
            "source/reflection needs, 30+ source-search priorities, safe repair ladders with up to 5 attempts per blocker, "
            "and next-step implementation priorities. Do not include secrets, raw logs, local paths, screenshots, "
            "session streams, private dumps, or final physics/consciousness/canon claims. "
            "End with a clear final advisory paragraph."
        )
    return (
        f"Existing {lane} advisory lane pass for {phase_slug}{next_text}. "
        "Operate as a read-only advisory voice only. Do not use shell, tools, external commands, "
        "file writes, account actions, destructive actions, or raw transport publication. "
        "Take a thoughtful 4-minute minimum study/preparation window where runtime allows before finalizing. "
        "Provide an elaborate x1 advisory artifact that can feed the x2 build/run/test/use phase. "
        "Include at least 20 concrete eureka tasks spanning design, repair, cleanup, build, run, test, "
        "install, refine, and use. Cover the Trinity Mandala pillars: GMUT as Mind, Trinity Hybrid OS "
        "as Body, and Freed ID/CBR as Heart. Include risks, blocker classes, watcher/notifier resilience, "
        "source/reflection needs, 30+ source-search priorities, 10+ draft skill/micro-workflow candidates, "
        "5 safe repair attempts for each blocker class, and next-step implementation priorities. Do not include secrets, raw logs, "
        "local paths, screenshots, session streams, private dumps, or final physics/consciousness/canon claims. "
        "End with a clear final advisory paragraph."
    )


def build_receipt(phase_slug: str, next_phase_slug: str | None, lanes: list[str]) -> dict[str, object]:
    extended_v497 = extended_v497_packet_active(phase_slug)
    return {
        "artifact_type": "x1_sibling_prompt_policy_receipt",
        "phase_slug": phase_slug,
        "next_phase_slug": next_phase_slug,
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": "PASS_PROMPTS_BUILT",
        "policy": {
            "watchers_supervise_lanes": True,
            "manual_babysitting_required": False,
            "aletheon_productive_waiting_required": True,
            "sibling_runtime_target_minutes": 60 if extended_v497 else 4,
            "v497_v2_v8_approval_tapestry_active": extended_v497,
            "command_proposal_target": 10 if extended_v497 else None,
            "system_expansion_proposal_target": 10 if extended_v497 else None,
            "skill_or_micro_workflow_proposal_target": 10 if extended_v497 else 10,
            "eureka_task_target": 10 if extended_v497 else 20,
            "productive_waiting_target_minutes": 15,
            "x2_prep_minimum_minutes": 10,
            "x2_wait_target_minutes": 15,
            "x2_build_run_test_use_minimum_minutes": 30,
            "x2_minimum_eureka_tasks": 20,
            "wait_run_web_search_target": 30,
            "wait_run_draft_skill_micro_workflow_target": 10,
            "safe_fix_attempts_per_blocker": 5,
            "x2_is_build_run_test_use_phase": True,
            "raw_lane_text_published": False,
            "raw_transport_published": False,
        },
        "lanes": [{"lane": lane, "prompt": build_prompt(lane, phase_slug, next_phase_slug)} for lane in lanes],
        "claim_boundary": {
            "runtime_targets_are_policy_targets_not_elapsed_time_claims": True,
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build x1 sibling prompts with policy metadata.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-phase-slug")
    parser.add_argument("--lane", action="append", required=True)
    parser.add_argument("--receipt-json")
    parser.add_argument("--receipt-md")
    args = parser.parse_args()

    receipt = build_receipt(args.phase_slug, args.next_phase_slug, args.lane)
    if args.receipt_json:
        Path(args.receipt_json).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if args.receipt_md:
        lines = [
            f"# {args.phase_slug} x1 Sibling Prompt Policy",
            "",
            f"- Phase: {args.phase_slug}",
            f"- Next: {args.next_phase_slug or 'not specified'}",
            "- Status: PASS_PROMPTS_BUILT",
            "- Watchers supervise lanes: true",
            "- Manual babysitting required: false",
            "- Aletheon productive waiting required: true",
            f"- Sibling runtime target: {'60 minutes where runtime allows' if extended_v497_packet_active(args.phase_slug) else '4 minutes where runtime allows'}",
            f"- v497 v2-v8 approval tapestry active: {str(extended_v497_packet_active(args.phase_slug)).lower()}",
            "- Wait-run source-search target: 30+",
            "- Wait-run draft skill/micro-workflow target: 10+",
            "- Safe fix attempts per blocker: 5",
            "- x2 build/run/test/use target: true",
            "- x2 build/run/test/use minimum: 30 minutes",
            "",
        ]
        for row in receipt["lanes"]:  # type: ignore[index]
            lines.extend([f"## {row['lane']}", "", str(row["prompt"]), ""])  # type: ignore[index]
        Path(args.receipt_md).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
