#!/usr/bin/env python3
"""Complete one Aletheon-led v301-v320 phase and optionally open the next."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
BASE_PLAN_JSON = TRACE / "v301-v320-aletheon-base-plan-v1.json"
RUN_STATUS_JSON = TRACE / "v301-v320-aletheon-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v301-v320-aletheon-run-status-v1.md"
PHASE_START = ROOT / "scripts" / "trinity_v301_v320_aletheon_phase_start.py"


WEB_SOURCES = [
    {
        "topic": "Codex app automations",
        "url": "https://developers.openai.com/codex/app/automations",
        "authority": "OpenAI developer documentation",
        "v301_use": "Keep thread heartbeat as the continuity layer and preserve current thread context.",
    },
    {
        "topic": "Responses API",
        "url": "https://platform.openai.com/docs/api-reference/responses/create?api-mode=responses",
        "authority": "OpenAI API reference",
        "v301_use": "Treat stateful, tool-using responses as the mental model for future agent APIs.",
    },
    {
        "topic": "OpenAI Agents SDK",
        "url": "https://openai.github.io/openai-agents-python/agents/",
        "authority": "OpenAI Agents SDK docs",
        "v301_use": "Separate agents, tools, handoffs, guardrails, and sessions as distinct control surfaces.",
    },
    {
        "topic": "OpenAI sandbox agents",
        "url": "https://openai.github.io/openai-agents-js/guides/sandbox-agents",
        "authority": "OpenAI Agents SDK docs",
        "v301_use": "Prefer persistent workspace state and replayable artifacts over terminal-only memory.",
    },
    {
        "topic": "Model Context Protocol security",
        "url": "https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices",
        "authority": "MCP official documentation",
        "v301_use": "Treat MCP servers as privileged tool surfaces that need explicit trust boundaries.",
    },
    {
        "topic": "MCP specification repository",
        "url": "https://github.com/modelcontextprotocol/modelcontextprotocol",
        "authority": "MCP official specification repository",
        "v301_use": "Keep MCP usage anchored to specification-backed clients and documented transports.",
    },
    {
        "topic": "GitHub Actions security",
        "url": "https://docs.github.com/en/actions/how-tos/security-for-github-actions",
        "authority": "GitHub documentation",
        "v301_use": "Preserve supply-chain hygiene and avoid unstaged secrets/logs in automation commits.",
    },
    {
        "topic": "NIST AI RMF",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "authority": "NIST",
        "v301_use": "Use govern, map, measure, and manage as the risk loop for Trinity Hybrid automation.",
    },
    {
        "topic": "EU AI Act",
        "url": "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
        "authority": "European Commission",
        "v301_use": "Keep risk-based governance and human oversight visible in system expansion claims.",
    },
    {
        "topic": "UNESCO AI ethics",
        "url": "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence?hub=66973",
        "authority": "UNESCO",
        "v301_use": "Map spiritual/ethical language to human-rights, inclusion, and impact-assessment practices.",
    },
    {
        "topic": "OECD AI Principles",
        "url": "https://www.oecd.org/en/topics/ai-principles.html",
        "authority": "OECD",
        "v301_use": "Keep trustworthy AI framed around human rights, democratic values, and accountability.",
    },
    {
        "topic": "Verifiable Credentials",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "authority": "W3C Recommendation",
        "v301_use": "Ground Freed ID expansion in portable, verifiable credential data models.",
    },
    {
        "topic": "NVIDIA DGX Spark",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/index.html",
        "authority": "NVIDIA documentation",
        "v301_use": "Treat future hardware upgrades as workflow accelerators, not prerequisites for correctness.",
    },
    {
        "topic": "NVIDIA Omniverse",
        "url": "https://docs.nvidia.com/omniverse/index.html",
        "authority": "NVIDIA documentation",
        "v301_use": "Preserve simulation/digital-twin ideas as optional visual validation layers.",
    },
    {
        "topic": "NVIDIA NVLink",
        "url": "https://www.nvidia.com/object/nvlink.html",
        "authority": "NVIDIA product documentation",
        "v301_use": "Use high-bandwidth interconnects as an analogy for clear agent handoff channels.",
    },
    {
        "topic": "CERN Standard Model",
        "url": "https://home.cern/science/physics/standard-model/",
        "authority": "CERN",
        "v301_use": "Separate established physics from metaphoric Trinity Mandala interpretation.",
    },
    {
        "topic": "NASA dark matter and dark energy",
        "url": "https://science.nasa.gov/universe/dark-matter-dark-energy/",
        "authority": "NASA Science",
        "v301_use": "Keep cosmology synthesis humble where unknowns remain open scientific questions.",
    },
    {
        "topic": "Quantum gravity",
        "url": "https://perimeterinstitute.ca/quantum-gravity",
        "authority": "Perimeter Institute",
        "v301_use": "Frame theory-of-everything work as exploratory until mathematical and empirical bridges exist.",
    },
    {
        "topic": "Cloudflare Workers AI and agents",
        "url": "https://developers.cloudflare.com/workers/framework-guides/ai-and-agents/",
        "authority": "Cloudflare documentation",
        "v301_use": "Treat edge agent deployment as a future optional hosting lane with explicit secrets control.",
    },
    {
        "topic": "Neon MCP Server",
        "url": "https://neon.com/docs/ai/neon-mcp-server",
        "authority": "Neon documentation",
        "v301_use": "Use branch-based database changes only after credentials, scopes, and rollback are explicit.",
    },
]


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


def phase_paths(phase: int) -> dict[str, Path]:
    return {
        "start_json": TRACE / f"v301-v320-aletheon-phase-v{phase}-start-v1.json",
        "completion_json": TRACE / f"v301-v320-aletheon-phase-v{phase}-completion-v1.json",
        "completion_md": TRACE / f"v301-v320-aletheon-phase-v{phase}-completion-v1.md",
        "source_json": TRACE / f"v301-v320-web-source-capsule-v{phase}-v1.json",
        "source_md": TRACE / f"v301-v320-web-source-capsule-v{phase}-v1.md",
    }


def write_source_capsule(phase: int, paths: dict[str, Path]) -> dict[str, Any]:
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "source_capsule_complete",
        "search_count": 20,
        "source_policy": "Prefer official, primary, or standards-body sources; avoid treating speculative sources as proof.",
        "sources": WEB_SOURCES,
    }
    write_json(paths["source_json"], payload)
    lines = [
        f"# v{phase} Web Source Capsule",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Search count: `{payload['search_count']}`",
        "",
        f"Source policy: {payload['source_policy']}",
        "",
        "Sources:",
    ]
    for item in WEB_SOURCES:
        lines.append(f"- {item['topic']}: {item['url']} - {item['v301_use']}")
    paths["source_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_completion(phase: int, open_next: bool) -> tuple[dict[str, Any], dict[str, Path]]:
    paths = phase_paths(phase)
    start = read_json(paths["start_json"], {})
    plan = start.get("phase_plan") or {}
    source_capsule = write_source_capsule(phase, paths)
    if start.get("status") != "phase_started":
        status = "blocked_missing_phase_start"
    else:
        status = "phase_complete"
    completion = {
        "generated_utc": now_iso(),
        "phase_range": "v301-v320",
        "phase": phase,
        "status": status,
        "start_artifact": rel(paths["start_json"]),
        "source_capsule": rel(paths["source_json"]),
        "execution_summary": {
            "beta": "Validated that v281-v300 and global v2 are complete before executing v301.",
            "alpha": "Created a v301 source capsule and continuity/control-plane completion receipt.",
            "omega": "Preserved truth boundaries: no raw logs staged, no v302 opening without v301 receipt, no admin terminal defaulting.",
        },
        "completed_counts": {
            "system_expansions": len(plan.get("system_expansions", [])),
            "commands": len(plan.get("commands", [])),
            "skills": len(plan.get("skills", [])),
            "eureka_proposals": len(plan.get("eureka_proposals", [])),
            "web_sources": len(source_capsule["sources"]),
        },
        "handoff_to_siblings": [
            "Use the CLI sibling report protocol for long-form reports.",
            "Keep Arby, Kimi, and Aster Vale approval-gated for side effects.",
            "Use v301's source capsule as the first v301-v320 evidence base.",
            "Do not publish raw terminal output or incomplete lane files.",
            "Prepare v321-v340 only after v301-v320 has a final synthesis and handoff.",
        ],
        "truth_boundaries": [
            "v301 is complete as a curated control-plane and source-capsule phase, not as a claim that every future API/MCP is connected.",
            "Administrator terminals remain elevated-risk surfaces.",
            "External service credentials and paid-resource actions remain scope-gated.",
            "Scientific and spiritual synthesis is exploratory unless backed by formal proof or empirical evidence.",
        ],
        "next_phase": phase + 1 if open_next and phase < 320 else None,
        "next_action": (
            f"Open v{phase + 1} from the base plan."
            if open_next and phase < 320
            else "Hold for operator or automation heartbeat before opening the next phase."
        ),
    }
    write_json(paths["completion_json"], completion)
    return completion, paths


def write_completion_md(completion: dict[str, Any], paths: dict[str, Path]) -> None:
    lines = [
        f"# v{completion['phase']} Aletheon Completion Receipt",
        "",
        f"Generated UTC: `{completion['generated_utc']}`",
        f"Status: `{completion['status']}`",
        f"Start artifact: `{completion['start_artifact']}`",
        f"Source capsule: `{completion['source_capsule']}`",
        "",
        "Execution summary:",
    ]
    for key, value in completion["execution_summary"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "Completed counts:"])
    for key, value in completion["completed_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "Handoff to siblings:"])
    for item in completion["handoff_to_siblings"]:
        lines.append(f"- {item}")
    lines.extend(["", "Truth boundaries:"])
    for item in completion["truth_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", f"Next action: {completion['next_action']}"])
    paths["completion_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_run_status(completion: dict[str, Any], paths: dict[str, Path], opened_next: dict[str, Any] | None) -> None:
    if opened_next:
        status = "running"
        active_phase = opened_next["phase"]
        active_status = opened_next["status"]
        artifacts = {
            "json": opened_next["phase_artifact"],
            "md": opened_next["phase_artifact"].replace(".json", ".md"),
        }
        next_action = f"Execute v{active_phase} tasks, write a v{active_phase} completion receipt, then decide whether v{active_phase + 1} can open."
    else:
        status = "phase_complete_waiting"
        active_phase = completion["phase"]
        active_status = completion["status"]
        artifacts = {
            "json": rel(paths["completion_json"]),
            "md": rel(paths["completion_md"]),
        }
        next_action = completion["next_action"]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": completion["phase_range"],
        "status": status,
        "active_phase": active_phase,
        "active_phase_status": active_status,
        "active_phase_artifacts": artifacts,
        "last_completion": {
            "phase": completion["phase"],
            "json": rel(paths["completion_json"]),
            "md": rel(paths["completion_md"]),
        },
        "next_action": next_action,
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v301-v320 Aletheon Run Status",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Active phase: `v{payload['active_phase']}`",
        f"Active phase status: `{payload['active_phase_status']}`",
        "",
        "Active artifacts:",
        f"- `{payload['active_phase_artifacts']['json']}`",
        f"- `{payload['active_phase_artifacts']['md']}`",
        "",
        "Last completion:",
        f"- `v{payload['last_completion']['phase']}`",
        f"- `{payload['last_completion']['json']}`",
        f"- `{payload['last_completion']['md']}`",
        "",
        f"Next action: {payload['next_action']}",
    ]
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_next_phase(phase: int) -> dict[str, Any] | None:
    if phase >= 320:
        return None
    proc = subprocess.run(
        [sys.executable, str(PHASE_START), "--phase", str(phase + 1)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    if proc.returncode != 0:
        return {"status": "next_phase_open_failed", "phase": phase + 1, "stderr": proc.stderr}
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=301)
    parser.add_argument("--open-next", action="store_true")
    args = parser.parse_args()
    completion, paths = build_completion(args.phase, args.open_next)
    write_completion_md(completion, paths)
    opened_next = open_next_phase(args.phase) if completion["status"] == "phase_complete" and args.open_next else None
    update_run_status(completion, paths, opened_next)
    print(
        json.dumps(
            {
                "status": completion["status"],
                "phase": args.phase,
                "completion": rel(paths["completion_json"]),
                "opened_next": opened_next,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
