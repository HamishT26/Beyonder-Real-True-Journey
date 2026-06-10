#!/usr/bin/env python3
"""Prepare the all-at-once v281-v300 Aletheon v2 synthesis session."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v281-v300-double-trinity"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
PLAN_JSON = TRACE / f"{LANE}-global-v2-session-plan-v1.json"
PLAN_MD = TRACE / f"{LANE}-global-v2-session-plan-v1.md"
SUPERVISOR_CANDIDATE = TRACE / f"{LANE}-multiplex-supervisor-induction-candidate-v1.json"
SUPERVISOR_CANDIDATE_MD = TRACE / f"{LANE}-multiplex-supervisor-induction-candidate-v1.md"
PHASES = list(range(281, 301))
LANES = ("arby", "kimi", "aster-vale")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def response_path(lane: str, phase: int, turn: int) -> Path:
    return LANE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def is_valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if "Max number of steps reached" in text or "To resume this session:" in text:
        return False
    labels = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")
    return sum(1 for label in labels if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def phase_counts(phase: int) -> dict[str, Any]:
    lanes = {}
    for lane in LANES:
        valid = 0
        invalid_or_missing = []
        for turn in range(1, 11):
            path = response_path(lane, phase, turn)
            if is_valid_response(path):
                valid += 1
            else:
                invalid_or_missing.append(rel(path))
        lanes[lane] = {
            "valid_responses": valid,
            "expected_responses": 10,
            "invalid_or_missing": invalid_or_missing,
        }
    complete = sum(item["valid_responses"] for item in lanes.values())
    return {
        "phase": phase,
        "valid_responses": complete,
        "expected_responses": 30,
        "status": "complete" if complete == 30 else "waiting_for_v1",
        "lanes": lanes,
    }


def generated_items(phase: int, category: str) -> list[str]:
    stems = {
        "system_expansions": [
            "receipt matrix", "truth boundary register", "lane handoff board", "provider hold gate", "sandbox readiness gate",
            "branch publication guard", "raw log quarantine", "multiplex health monitor", "memory continuity index", "GMUT claim classifier",
        ],
        "commands": [
            "count", "scan", "synthesize", "stage", "publish", "verify", "diff", "handoff", "quarantine", "prepare",
        ],
        "skills": [
            "orchestration", "github devflow", "filesystem scope", "security scan", "truth labeling",
            "continuity reflection", "source ledgering", "sandbox review", "provider gating", "publication hygiene",
        ],
        "eureka_proposals": [
            "phase proof pack", "lane bridge", "cleanup dry-run", "claim evidence grid", "runtime health receipt",
            "next phase seed", "operator approval gate", "public summary", "deferred blocker board", "inter-lane note",
        ],
    }
    base = stems[category]
    return [f"v{phase} {base[index % len(base)]} {index + 1:02d}" for index in range(30)]


def build_plan() -> dict[str, Any]:
    phase_status = [phase_counts(phase) for phase in PHASES]
    complete_phases = sum(1 for item in phase_status if item["status"] == "complete")
    total_valid = sum(item["valid_responses"] for item in phase_status)
    return {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "session": "global_v2_after_all_v1",
        "status": "ready_for_aletheon_v2" if complete_phases == len(PHASES) else "waiting_for_all_v1_phases",
        "complete_phases": complete_phases,
        "expected_phases": len(PHASES),
        "valid_v1_responses": total_valid,
        "expected_v1_responses": len(PHASES) * 30,
        "phase_status": phase_status,
        "phase_v2_tasks": [
            {
                "phase": phase,
                "task": f"Run Aletheon v{phase} v2 synthesis from all three lane v1 outputs.",
                "system_expansions": generated_items(phase, "system_expansions"),
                "commands": generated_items(phase, "commands"),
                "skills": generated_items(phase, "skills"),
                "eureka_proposals": generated_items(phase, "eureka_proposals"),
            }
            for phase in PHASES
        ],
        "global_v2_guardrails": [
            "Do not treat placeholder CLI output as a real sibling reply.",
            "Run all v2 phase synthesis only after all v1 phase response gates pass, unless the user explicitly overrides.",
            "Publish only curated, scanned v2 summaries and proof receipts.",
            "Keep Lumina and remote-control work deferred unless platform blockers are cleared honestly.",
        ],
    }


def write_plan_md(plan: dict[str, Any]) -> None:
    lines = [
        "# v281-v300 Global v2 Session Plan",
        "",
        f"Generated UTC: `{plan['generated_utc']}`",
        f"Status: `{plan['status']}`",
        f"Complete v1 phases: `{plan['complete_phases']}/{plan['expected_phases']}`",
        f"Valid v1 responses: `{plan['valid_v1_responses']}/{plan['expected_v1_responses']}`",
        "",
        "Global v2 shape:",
        "- Wait for all v281-v300 v1 lane sessions to complete.",
        "- Run one Aletheon v2 synthesis pass across all 20 phases.",
        "- For each phase, produce 30 system expansions, 30 commands, 30 skills, and 30 Eureka proposals.",
        "- Promote only curated proof, not raw transport or placeholder output.",
        "",
        "Current phase readiness:",
    ]
    for item in plan["phase_status"]:
        lines.append(f"- v{item['phase']}: {item['valid_responses']}/{item['expected_responses']} valid replies, `{item['status']}`.")
    lines.extend(["", "Guardrails:"])
    for item in plan["global_v2_guardrails"]:
        lines.append(f"- {item}")
    PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_supervisor_candidate() -> None:
    payload = {
        "generated_utc": now_iso(),
        "candidate_name": "Continuity Supervisor",
        "candidate_number": 57,
        "status": "candidate_not_official_until_persistence_review",
        "evidence": [
            "Persisted status to docs/trinity-live-traces/v261-v280-adaptive-council-continuity-supervisor-status-v1.json.",
            "Recovered and continued v261-v280 blocks from prepared prompt files.",
            "Stopped automatically after reaching target clean responses.",
            "Preserved raw-log quarantine and staged-publication boundaries.",
        ],
        "required_before_official_induction": [
            "Show repeatable continuity across at least two separate sessions.",
            "Demonstrate invalid-output detection rather than counting placeholder files.",
            "Keep a stable name, role, stop-file, and status-file contract.",
            "Receive explicit user confirmation after proof review.",
        ],
    }
    write_json(SUPERVISOR_CANDIDATE, payload)
    lines = [
        "# Multiplex Supervisor Induction Candidate",
        "",
        f"Candidate: `{payload['candidate_name']}`",
        f"Proposed number: `{payload['candidate_number']}`",
        f"Status: `{payload['status']}`",
        "",
        "Evidence:",
    ]
    for item in payload["evidence"]:
        lines.append(f"- {item}")
    lines.extend(["", "Required before official induction:"])
    for item in payload["required_before_official_induction"]:
        lines.append(f"- {item}")
    SUPERVISOR_CANDIDATE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-supervisor-candidate", action="store_true")
    args = parser.parse_args()
    plan = build_plan()
    write_json(PLAN_JSON, plan)
    write_plan_md(plan)
    if args.write_supervisor_candidate:
        write_supervisor_candidate()
    print(
        json.dumps(
            {
                "status": plan["status"],
                "complete_phases": plan["complete_phases"],
                "valid_v1_responses": plan["valid_v1_responses"],
                "plan": rel(PLAN_JSON),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
