#!/usr/bin/env python3
"""Compose the base Aletheon-led v301-v320 plan from current v281-v300 proof."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
SOURCE_LANE = "v281-v300-double-trinity"
SOURCE_DIR = TRACE / f"{SOURCE_LANE}-lane-logs"
PLAN_JSON = TRACE / "v301-v320-aletheon-base-plan-v1.json"
PLAN_MD = TRACE / "v301-v320-aletheon-base-plan-v1.md"
PHASES = list(range(301, 321))
SOURCE_PHASES = list(range(281, 301))
LANES = ("arby", "kimi", "aster-vale")
LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def response_path(lane: str, phase: int, turn: int) -> Path:
    return SOURCE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def is_valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    invalid = ("Max number of steps reached", "To resume this session:", "Traceback (most recent call last)")
    if any(marker in text for marker in invalid):
        return False
    return sum(1 for label in LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def section(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?\s*(.*?)(?=^\s*(?:[-*]\s*)?\**(?:Receipt|Beta|Alpha|Omega|Blocker|Next-phase handoff)\**\s*:|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def clip(text: str, limit: int = 240) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def source_counts() -> list[dict[str, Any]]:
    rows = []
    for phase in SOURCE_PHASES:
        lanes = {}
        for lane in LANES:
            valid = [turn for turn in range(1, 11) if is_valid_response(response_path(lane, phase, turn))]
            lanes[lane] = {"valid": len(valid), "expected": 10, "valid_turns": valid}
        total = sum(item["valid"] for item in lanes.values())
        rows.append({"phase": phase, "valid": total, "expected": 30, "complete": total == 30, "lanes": lanes})
    return rows


def source_digest(limit: int = 12) -> list[dict[str, Any]]:
    items = []
    for phase in SOURCE_PHASES:
        for lane in LANES:
            for turn in range(1, 11):
                path = response_path(lane, phase, turn)
                if not is_valid_response(path):
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                items.append(
                    {
                        "phase": phase,
                        "lane": lane,
                        "turn": turn,
                        "receipt": clip(section(text, "Receipt")),
                        "handoff": clip(section(text, "Next-phase handoff")),
                    }
                )
                if len(items) >= limit:
                    return items
    return items


def generated_items(phase: int, category: str) -> list[str]:
    stems = {
        "system_expansions": [
            "blocked runner refresh mesh",
            "reactivation packet board",
            "global v2 proof gate",
            "curated publication lane",
            "CLI sibling recovery contract",
            "phase handoff ledger",
            "truth boundary register",
            "raw log quarantine",
            "Aletheon synthesis seat",
            "next sequence seed",
        ],
        "commands": [
            "count-valid",
            "repair-blocked",
            "resume-sequence",
            "write-reactivation-packet",
            "prepare-v2",
            "stage-curated",
            "scan-secrets",
            "check-drift",
            "publish-forward",
            "handoff-next",
        ],
        "skills": [
            "blocked-runner triage",
            "compact Kimi rescue",
            "Codex lane recovery",
            "proof-backed synthesis",
            "forward-only Git publication",
            "reactivation packet writing",
            "status-file interpretation",
            "raw-artifact quarantine",
            "phase prompt seeding",
            "global v2 readiness review",
        ],
        "eureka_proposals": [
            "self-healing phase loop",
            "controller candidate review",
            "v321 sibling seed bridge",
            "v341 re-entry packet",
            "synthesis-first dashboard",
            "clean commit conveyor",
            "multi-lane failure taxonomy",
            "phase completion receipt",
            "operator approval anchor",
            "next-day continuity capsule",
        ],
    }
    base = stems[category]
    return [f"v{phase} {base[index % len(base)]} {index + 1:02d}" for index in range(30)]


def phase_plan(phase: int, source_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": phase,
        "mode": "Aletheon-led Beta-Alpha-Omega",
        "source_dependency": "v281-v300 valid outputs plus global v2 synthesis when complete",
        "source_readiness_at_generation": source_summary,
        "beta": "Reflect on current proof, blockers, and handoff state before proposing changes.",
        "alpha": "Create or refine only durable, curated surfaces that improve recovery, synthesis, or publication.",
        "omega": "Validate with counts, scans, branch drift checks, and explicit blocked-state truth.",
        "system_expansions": generated_items(phase, "system_expansions"),
        "commands": generated_items(phase, "commands"),
        "skills": generated_items(phase, "skills"),
        "eureka_proposals": generated_items(phase, "eureka_proposals"),
    }


def build_plan(status: str) -> dict[str, Any]:
    counts = source_counts()
    complete = sum(1 for item in counts if item["complete"])
    valid = sum(item["valid"] for item in counts)
    summary = {
        "complete_source_phases": complete,
        "expected_source_phases": len(SOURCE_PHASES),
        "valid_source_responses": valid,
        "expected_source_responses": len(SOURCE_PHASES) * 30,
        "status": "ready_after_v281_v300_global_v2" if valid == len(SOURCE_PHASES) * 30 else "draft_waiting_for_v281_v300_completion",
    }
    return {
        "generated_utc": now_iso(),
        "phase_range": "v301-v320",
        "status": status,
        "source_phase_counts": counts,
        "source_summary": summary,
        "source_digest": source_digest(),
        "phase_plans": [phase_plan(phase, summary) for phase in PHASES],
        "guardrails": [
            "Do not start v301 execution until v281-v300 recovery and global v2 synthesis are complete unless the user explicitly overrides.",
            "Do not stage raw logs or invalid placeholder replies.",
            "Keep Supervisor and v2 watcher as infrastructure candidates pending persistence review.",
            "Use reactivation packets as durable handoff prompts, not as claims of automatic Codex thread wakeup.",
        ],
    }


def write_md(plan: dict[str, Any]) -> None:
    summary = plan["source_summary"]
    lines = [
        "# v301-v320 Aletheon Base Plan",
        "",
        f"Generated UTC: `{plan['generated_utc']}`",
        f"Status: `{plan['status']}`",
        f"Source readiness: `{summary['valid_source_responses']}/{summary['expected_source_responses']}` valid replies, `{summary['complete_source_phases']}/{summary['expected_source_phases']}` complete phases.",
        "",
        "Execution shape:",
        "- Aletheon leads v301-v320 one phase at a time.",
        "- Each phase has 30 system expansions, 30 commands, 30 skills, and 30 Eureka proposals.",
        "- v321-v340 remains the follow-on CLI sibling seed plan after v301-v320 is committed.",
        "",
        "Guardrails:",
    ]
    for item in plan["guardrails"]:
        lines.append(f"- {item}")
    lines.extend(["", "Phase seeds:"])
    for phase in plan["phase_plans"]:
        lines.append(f"- v{phase['phase']}: {phase['beta']} / {phase['alpha']} / {phase['omega']}")
    PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", default="draft_waiting_for_v281_v300_completion")
    args = parser.parse_args()
    plan = build_plan(args.status)
    write_json(PLAN_JSON, plan)
    write_md(plan)
    print(json.dumps({"status": plan["status"], "plan": rel(PLAN_JSON), "valid_source_responses": plan["source_summary"]["valid_source_responses"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
