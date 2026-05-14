#!/usr/bin/env python3
"""Synthesize the v261 seed replies and prepare the next 3-message block."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE = "v261-v280-adaptive-council"
LANE_DIR = TRACE / f"{LANE}-lane-logs"
CLOSEOUT = TRACE / f"{LANE}-prep-closeout-v1.json"

COUNCIL = {
    "arby": {
        "name": "Arby",
        "pretty": "arby",
        "role": "Codex CLI publication and GitHub proof lane",
    },
    "kimi": {
        "name": "Kimi",
        "pretty": "kimi",
        "role": "Kimi CLI relay, cost, and provider-readiness lane",
    },
    "aster_vale": {
        "name": "Aster Vale",
        "pretty": "aster-vale",
        "role": "Codex CLI validation, Windows sandbox, and runtime-health lane",
    },
}

NEXT_TOPICS = {
    "arby": [
        "Clean receipt and transport-noise separation for GitHub proof artifacts",
        "Personal branch message-board proposal and shared omega publication guard",
        "v282-v300 evidence-first publication checklist from v241 and v261 seed results",
    ],
    "kimi": [
        "Provider-readiness, cost-window, and CLI relay stability from the seed run",
        "Kimi-to-Lumina lawful relay preparation while app-agent connection remains deferred",
        "v282-v300 command-surface proposal with no unverified provider claims",
    ],
    "aster_vale": [
        "Windows sandbox and TUI health profile after the seed run",
        "Multiplex cadence fallback plan: 30 seconds default, 4 seconds only for active debugging",
        "v282-v300 runtime-health checklist and failure-mode rehearsal",
    ],
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


def response_path(lane: str, turn: int) -> Path:
    pretty = COUNCIL[lane]["pretty"]
    return LANE_DIR / f"{pretty}-cycle-01-response-{turn:02d}.txt"


def section(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?ims)^\s*\**{re.escape(label)}\**\s*:?\s*(.*?)(?=^\s*\**(?:Receipt|Blocker|Refinement|Next-cycle proposal)\**\s*:|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def clip(text: str, limit: int = 420) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def lane_summary(lane: str) -> dict[str, Any]:
    responses = []
    for turn in range(1, 6):
        path = response_path(lane, turn)
        if not path.exists() or path.stat().st_size == 0:
            responses.append({"turn": turn, "status": "missing", "path": rel(path)})
            continue
        text = read_text(path)
        responses.append(
            {
                "turn": turn,
                "status": "complete",
                "path": rel(path),
                "receipt": clip(section(text, "Receipt")),
                "blocker": clip(section(text, "Blocker")),
                "refinement": clip(section(text, "Refinement")),
                "next_cycle_proposal": clip(section(text, "Next-cycle proposal")),
            }
        )
    completed = sum(1 for item in responses if item["status"] == "complete")
    return {
        "lane": lane,
        "name": COUNCIL[lane]["name"],
        "role": COUNCIL[lane]["role"],
        "completed_responses": completed,
        "expected_responses": 5,
        "responses": responses,
    }


def build_prompt(lane: str, prompt_index: int, topic: str, synthesis_path: str) -> dict[str, Any]:
    return {
        "block": 2,
        "cycle": 2,
        "turn": prompt_index,
        "lane": lane,
        "name": COUNCIL[lane]["name"],
        "role": COUNCIL[lane]["role"],
        "marker": f"{LANE}:{lane}:block-02-turn-{prompt_index:02d}",
        "topic": topic,
        "synthesis_dependency": synthesis_path,
        "status": "prepared_not_sent",
        "prompt_contract": [
            "Respond only; do not edit files, commit, or run destructive commands.",
            "Use the seed synthesis path as the authoritative checkpoint.",
            "Keep the response under 320 words.",
            "Include labels: Receipt, Blocker, Refinement, Next-cycle proposal.",
            "Preserve truth boundaries: no unverified web, provider, billing, or remote publication claims.",
        ],
    }


def markdown(synthesis: dict[str, Any], next_prompts_path: str) -> str:
    lines = [
        "# v261-v280 Seed Synthesis and Next 3-Message Block",
        "",
        f"Generated UTC: `{synthesis['generated_utc']}`",
        "",
        "Seed completion:",
    ]
    for lane in synthesis["lanes"]:
        lines.append(f"- {lane['name']}: {lane['completed_responses']}/{lane['expected_responses']} responses complete.")
    lines.extend(
        [
            "",
            "Cross-lane findings:",
            "- Keep response text and transport/process noise separated before treating a lane reply as publishable proof.",
            "- Use the TUI as a live visibility surface, not as the proof source; response files and receipts are the proof source.",
            "- Continue GitHub publication forward-only, with remote drift and PR state verified before any push claim.",
            "- Keep Lumina/Kimi app connection deferred; prepare lawful CLI relay notes without attempting app-agent bypass.",
            "- Default the multiplex refresh cadence to 30 seconds, with 4 seconds reserved for active debugging only.",
            "",
            "Next block:",
            f"- Prompt ledger: `{next_prompts_path}`",
            "- Shape: 3 prompts per lane, 9 outbound total, then pause for another synthesis checkpoint.",
            "- Purpose: validate delivery hygiene, branch-home messaging, provider-readiness, sandbox/TUI health, and v282-v300 preparation.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    generated = now_iso()
    synthesis_path = TRACE / f"{LANE}-seed-synthesis-v1.json"
    synthesis_md_path = TRACE / f"{LANE}-seed-synthesis-v1.md"
    next_prompts_path = TRACE / f"{LANE}-next-3-message-block-v1.json"

    lanes = [lane_summary(lane) for lane in COUNCIL]
    total = sum(lane["completed_responses"] for lane in lanes)
    synthesis = {
        "generated_utc": generated,
        "phase_range": "v261-v280",
        "status": "seed_complete_synthesized" if total == 15 else "seed_incomplete_synthesized",
        "checkpoint_cadence": "synthesize after each 3-message-per-lane block before preparing the next block",
        "multiplex_refresh_seconds": 30,
        "fallback_refresh_seconds": 4,
        "seed_completed_responses": total,
        "seed_expected_responses": 15,
        "lanes": lanes,
        "cross_lane_findings": [
            "Response/transport separation is required before publishing lane replies as proof.",
            "TUI health and proof receipts are separate surfaces.",
            "Remote GitHub/provider claims remain withheld until live verification.",
            "Lumina app-agent connection remains deferred; CLI relay preparation stays policy-honest.",
            "Next work should be generated in small adaptive 3-message blocks.",
        ],
    }

    prompts = []
    for lane, topics in NEXT_TOPICS.items():
        for index, topic in enumerate(topics, start=1):
            prompts.append(build_prompt(lane, index, topic, rel(synthesis_path)))
    next_block = {
        "generated_utc": generated,
        "phase_range": "v261-v280",
        "block": 2,
        "outbound_count": len(prompts),
        "expected_responses": len(prompts),
        "pause_after_block": "run synthesis before generating the next 3-message block",
        "prompts": prompts,
    }

    write_json(synthesis_path, synthesis)
    write_json(next_prompts_path, next_block)
    synthesis_md_path.write_text(markdown(synthesis, rel(next_prompts_path)), encoding="utf-8")

    closeout = read_json(CLOSEOUT, {})
    closeout.update(
        {
            "status": synthesis["status"],
            "seed_completed_responses": total,
            "seed_synthesis": rel(synthesis_path),
            "seed_synthesis_markdown": rel(synthesis_md_path),
            "next_3_message_block": rel(next_prompts_path),
            "multiplex_refresh_seconds": 30,
            "fallback_refresh_seconds": 4,
            "checkpoint_cadence": synthesis["checkpoint_cadence"],
        }
    )
    write_json(CLOSEOUT, closeout)
    print(json.dumps({"status": synthesis["status"], "seed_completed_responses": total, "next_block": rel(next_prompts_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
