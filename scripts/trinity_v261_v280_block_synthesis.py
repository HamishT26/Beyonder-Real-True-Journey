#!/usr/bin/env python3
"""Synthesize a completed v261-v280 block and prepare the next 3-message block."""

from __future__ import annotations

import argparse
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
    "arby": ("Arby", "arby", "Codex CLI publication and GitHub proof lane"),
    "kimi": ("Kimi", "kimi", "Kimi CLI relay, cost, and provider-readiness lane"),
    "aster_vale": ("Aster Vale", "aster-vale", "Codex CLI validation, Windows sandbox, and runtime-health lane"),
}

NEXT_TOPIC_ROTATION = {
    "arby": [
        "Remote drift check design and forward-only publication receipt",
        "Sanitized artifact allowlist for shared omega publication",
        "Branch-home message board protocol for inter-lane notes",
    ],
    "kimi": [
        "Provider-health evidence without overclaiming billing or app access",
        "Cost-window and CLI relay guardrails for the next active run",
        "Lumina relay preparation as a deferred, policy-honest handoff",
    ],
    "aster_vale": [
        "TUI latency telemetry and lane liveness scoring",
        "Windows sandbox readiness checklist and WSB candidate profile",
        "Failure recovery drills for stalled, noisy, or truncated lane replies",
    ],
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


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


def response_path(lane: str, block: int, turn: int) -> Path:
    pretty = COUNCIL[lane][1]
    return LANE_DIR / f"{pretty}-block-{block:02d}-response-{turn:02d}.txt"


def lane_summary(lane: str, block: int) -> dict[str, Any]:
    name, _, role = COUNCIL[lane]
    responses = []
    for turn in range(1, 4):
        path = response_path(lane, block, turn)
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
    return {
        "lane": lane,
        "name": name,
        "role": role,
        "completed_responses": sum(1 for item in responses if item["status"] == "complete"),
        "expected_responses": 3,
        "responses": responses,
    }


def build_next_prompt(lane: str, block: int, turn: int, topic: str, dependency: str) -> dict[str, Any]:
    name, _, role = COUNCIL[lane]
    return {
        "block": block,
        "cycle": block,
        "turn": turn,
        "lane": lane,
        "name": name,
        "role": role,
        "marker": f"{LANE}:{lane}:block-{block:02d}-turn-{turn:02d}",
        "topic": topic,
        "synthesis_dependency": dependency,
        "status": "prepared_not_sent",
        "prompt_contract": [
            "Respond only; do not edit files, commit, or run destructive commands.",
            "Use the prior block synthesis as the authoritative checkpoint.",
            "Keep the response under 320 words.",
            "Include labels: Receipt, Blocker, Refinement, Next-cycle proposal.",
            "Preserve truth boundaries and avoid unverified provider or publication claims.",
        ],
    }


def write_md(path: Path, synthesis: dict[str, Any], next_block_path: Path | None) -> None:
    lines = [
        f"# v261-v280 Block {synthesis['block']:02d} Synthesis",
        "",
        f"Generated UTC: `{synthesis['generated_utc']}`",
        "",
        "Completion:",
    ]
    for lane in synthesis["lanes"]:
        lines.append(f"- {lane['name']}: {lane['completed_responses']}/{lane['expected_responses']} replies.")
    lines.extend(["", "Checkpoint decisions:"])
    for decision in synthesis["checkpoint_decisions"]:
        lines.append(f"- {decision}")
    if next_block_path:
        lines.extend(["", f"Next prompt block: `{rel(next_block_path)}`"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int, required=True)
    parser.add_argument("--prepare-next", action="store_true")
    args = parser.parse_args()

    generated = now_iso()
    lanes = [lane_summary(lane, args.block) for lane in COUNCIL]
    completed = sum(lane["completed_responses"] for lane in lanes)
    synthesis_path = TRACE / f"{LANE}-block-{args.block:02d}-synthesis-v1.json"
    synthesis_md_path = TRACE / f"{LANE}-block-{args.block:02d}-synthesis-v1.md"
    next_block_path = TRACE / f"{LANE}-block-{args.block + 1:02d}-prompts-v1.json"

    synthesis = {
        "generated_utc": generated,
        "phase_range": "v261-v280",
        "block": args.block,
        "status": "complete_synthesized" if completed == 9 else "incomplete_synthesized",
        "completed_responses": completed,
        "expected_responses": 9,
        "multiplex_refresh_seconds": 30,
        "fallback_refresh_seconds": 4,
        "lanes": lanes,
        "checkpoint_decisions": [
            "Continue adaptive 3-message blocks only when the previous block has response receipts or explicit blockers.",
            "Keep transport noise separated from response proof.",
            "Keep remote-control and Lumina app-agent work deferred until platform blockers are explicitly cleared.",
            "Use v282-v300 prep as the next-day strategic landing surface.",
        ],
    }
    write_json(synthesis_path, synthesis)

    next_prompts = None
    if args.prepare_next and completed == 9:
        prompts = []
        for lane, topics in NEXT_TOPIC_ROTATION.items():
            for index, topic in enumerate(topics, start=1):
                prompts.append(build_next_prompt(lane, args.block + 1, index, topic, rel(synthesis_path)))
        next_prompts = {
            "generated_utc": generated,
            "phase_range": "v261-v280",
            "block": args.block + 1,
            "outbound_count": len(prompts),
            "expected_responses": len(prompts),
            "pause_after_block": "run synthesis before generating the next 3-message block",
            "prompts": prompts,
        }
        write_json(next_block_path, next_prompts)
    else:
        next_block_path = None

    write_md(synthesis_md_path, synthesis, next_block_path)
    closeout = read_json(CLOSEOUT, {})
    closeout[f"block_{args.block:02d}_synthesis"] = rel(synthesis_path)
    closeout[f"block_{args.block:02d}_synthesis_markdown"] = rel(synthesis_md_path)
    closeout[f"block_{args.block:02d}_completed_responses"] = completed
    closeout[f"block_{args.block:02d}_status"] = synthesis["status"]
    if next_block_path:
        closeout[f"block_{args.block + 1:02d}_prompt_file"] = rel(next_block_path)
    write_json(CLOSEOUT, closeout)
    print(json.dumps({"status": synthesis["status"], "completed_responses": completed, "next_block": rel(next_block_path) if next_block_path else None}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
