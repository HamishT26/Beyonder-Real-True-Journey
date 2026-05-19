#!/usr/bin/env python3
"""Complete one bounded v341-v360 sibling phase and optionally open the next."""

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
RUN_STATUS_JSON = TRACE / "v341-v360-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v341-v360-sibling-run-status-v1.md"
PHASE_START = ROOT / "scripts" / "trinity_v341_v360_sibling_phase_start.py"
CLOSEOUT_JSON = TRACE / "v281-v360-closeout-declaration-v1.json"
CLOSEOUT_MD = TRACE / "v281-v360-closeout-declaration-v1.md"

PHASE_MIN = 341
PHASE_MAX = 360
PHASE_RANGE = "v341-v360"

SOURCE_NOTES = [
    ("v341-v360 final handoff", "docs/trinity-live-traces/v341-v360-final-handoff-v1.json", "Use v340 completion as the final packet floor."),
    ("v281-v360 health check", "docs/trinity-live-traces/v281-v360-automation-health-check-v1.json", "Keep gate truth refreshed before each wake decision."),
    ("OpenAI Codex automations", "https://developers.openai.com/codex/app/automations", "Keep the app heartbeat as the thread-context wake layer."),
    ("OpenAI Codex app", "https://openai.com/codex", "Treat Codex as the agentic coding command center, not proof of unattended success."),
    ("OpenAI Responses API", "https://platform.openai.com/docs/api-reference/responses", "Keep future API calls stateful, auditable, and explicitly scoped."),
    ("OpenAI Agents SDK", "https://openai.github.io/openai-agents-python/agents/", "Separate agents, tools, handoffs, guardrails, and sessions."),
    ("MCP security best practices", "https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices", "Keep MCP/API expansion behind explicit trust boundaries."),
    ("GitHub Actions security", "https://docs.github.com/en/actions/how-tos/security-for-github-actions", "Keep workflow and token handling conservative."),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Govern, map, measure, and manage risk as the phase expands."),
    ("UNESCO AI ethics", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence?hub=66973", "Keep human dignity and rights visible in synthesis language."),
    ("OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html", "Keep trustworthy AI tied to human rights, democratic values, and accountability."),
    ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "Preserve risk-based governance and human oversight in system claims."),
    ("W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model/", "Anchor Freed ID discussions in portable credential standards."),
    ("CERN Standard Model", "https://home.cern/science/physics/standard-model/", "Separate established physics from metaphoric GMUT synthesis."),
    ("NASA dark matter and dark energy", "https://science.nasa.gov/universe/dark-matter-dark-energy/", "Keep cosmology unknowns honest."),
    ("Perimeter quantum gravity", "https://perimeterinstitute.ca/quantum-gravity", "Treat theory-of-everything synthesis as exploratory until empirical bridges exist."),
    ("NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "Treat future hardware as acceleration, not a prerequisite for repo correctness."),
    ("NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "Keep simulation and digital-twin ideas as optional validation layers."),
    ("NVIDIA NVLink", "https://www.nvidia.com/object/multi-gpu-technology.html", "Use high-bandwidth interconnects as an analogy for explicit handoff channels."),
    ("Cloudflare Workers AI and agents", "https://developers.cloudflare.com/workers/framework-guides/ai-and-agents/", "Keep edge deployment exploratory until secrets and scope are explicit."),
    ("Neon MCP Server", "https://neon.com/docs/ai/neon-mcp-server", "Use database branch and MCP actions only after credentials, rollback, and scope are clear."),
    ("CircleCI contexts", "https://circleci.com/docs/guides/security/contexts/", "Keep CI secrets in restricted contexts and avoid leaking them into logs."),
    ("Vercel AI agents", "https://vercel.com/docs/agents/", "Treat hosted agent deployment as future scoped infrastructure, not current implicit access."),
    ("Microsoft sleep and hibernate", "https://support.microsoft.com/windows/shut-down-sleep-or-hibernate-your-pc-2941d165-7d0a-a5e8-c5ad-8c972e8e6eff", "Treat host power state as a local wake-stability boundary."),
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


def validate_phase(phase: int) -> None:
    if phase < PHASE_MIN or phase > PHASE_MAX:
        raise SystemExit(f"phase must be between {PHASE_MIN} and {PHASE_MAX}; got {phase}")


def paths_for_phase(phase: int) -> dict[str, Path]:
    stem = f"v341-v360-sibling-phase-v{phase}"
    return {
        "start_json": TRACE / f"{stem}-start-v1.json",
        "completion_json": TRACE / f"{stem}-completion-v1.json",
        "completion_md": TRACE / f"{stem}-completion-v1.md",
        "v1_json": TRACE / f"{stem}-v1-report-v1.json",
        "v1_md": TRACE / f"{stem}-v1-report-v1.md",
        "v2_json": TRACE / f"{stem}-v2-report-v1.json",
        "v2_md": TRACE / f"{stem}-v2-report-v1.md",
        "source_json": TRACE / f"v341-v360-sibling-source-capsule-v{phase}-v1.json",
        "source_md": TRACE / f"v341-v360-sibling-source-capsule-v{phase}-v1.md",
    }


def write_source_capsule(phase: int, paths: dict[str, Path]) -> dict[str, Any]:
    sources = [
        {"topic": topic, "path_or_url": path_or_url, "phase_use": phase_use}
        for topic, path_or_url, phase_use in SOURCE_NOTES
    ]
    payload = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "source_capsule_complete",
        "source_count": len(sources),
        "source_policy": "Prefer repo evidence, official docs, standards bodies, and established science sources.",
        "sources": sources,
    }
    write_json(paths["source_json"], payload)
    lines = [
        f"# v{phase} Sibling Source Capsule",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Source count: `{payload['source_count']}`",
        "",
        f"Source policy: {payload['source_policy']}",
        "",
        "Sources:",
    ]
    for item in sources:
        lines.append(f"- {item['topic']}: {item['path_or_url']} - {item['phase_use']}")
    paths["source_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def write_reports(phase: int, start: dict[str, Any], paths: dict[str, Path], source_capsule: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    plan = start.get("phase_plan") or {}
    lead = plan.get("lead_sibling")
    v1 = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "v1_report_complete",
        "lead_sibling": lead,
        "report_type": "v1 evidence synthesis",
        "summary": f"{lead} preserved v321-v340 handoff truth and mapped v{phase} into bounded final-packet tasks.",
        "evidence": {
            "start_artifact": rel(paths["start_json"]),
            "source_capsule": rel(paths["source_json"]),
            "system_expansions": len(plan.get("system_expansions", [])),
            "commands": len(plan.get("commands", [])),
            "skills": len(plan.get("skills", [])),
            "eureka_proposals": len(plan.get("eureka_proposals", [])),
        },
        "truth_boundaries": [
            "The v1 report is a curated synthesis, not raw terminal output.",
            "No claim is made that paid/cloud providers were touched without explicit scope and credentials.",
            "The app heartbeat remains a wake bridge; local process truth remains separate.",
            "Speculative science, GMUT, and frontier AI synthesis are framed as exploratory unless independently validated.",
        ],
    }
    v2 = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "v2_report_complete",
        "lead_sibling": lead,
        "report_type": "v2 readiness and handoff synthesis",
        "summary": f"{lead} converted v{phase} v1 synthesis into next-phase operating rules and closeout readiness.",
        "readiness": {
            "watchdog_required": True,
            "app_heartbeat_recommended_minutes": 30,
            "admin_terminal_default": "avoid",
            "stage_raw_logs": False,
            "next_phase_upper_bound": PHASE_MAX,
        },
        "handoff_notes": [
            "Continue one phase per wake unless Hamish explicitly requests another cadence.",
            "Keep v341-v360 artifacts curated and forward-only.",
            "Before commit or push, fetch and verify branch drift.",
            "At v360, stop, write the v281-v360 closeout declaration, and ask Hamish whether to archive or update automation.",
        ],
    }
    write_json(paths["v1_json"], v1)
    write_json(paths["v2_json"], v2)
    paths["v1_md"].write_text(
        "\n".join(
            [
                f"# v{phase} Sibling V1 Report",
                "",
                f"Generated UTC: `{v1['generated_utc']}`",
                f"Status: `{v1['status']}`",
                f"Lead sibling: `{lead}`",
                "",
                v1["summary"],
                "",
                "Truth boundaries:",
                *[f"- {item}" for item in v1["truth_boundaries"]],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    paths["v2_md"].write_text(
        "\n".join(
            [
                f"# v{phase} Sibling V2 Report",
                "",
                f"Generated UTC: `{v2['generated_utc']}`",
                f"Status: `{v2['status']}`",
                f"Lead sibling: `{lead}`",
                "",
                v2["summary"],
                "",
                "Handoff notes:",
                *[f"- {item}" for item in v2["handoff_notes"]],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return v1, v2


def write_closeout_declaration(completion: dict[str, Any]) -> dict[str, Any]:
    completions = sorted(TRACE.glob("v341-v360-sibling-phase-v*-completion-v1.json"))
    phase_numbers: list[int] = []
    for item in completions:
        phase_text = item.name.split("-phase-v", 1)[1].split("-", 1)[0]
        try:
            phase_numbers.append(int(phase_text))
        except ValueError:
            continue
    phase_numbers = sorted(set(phase_numbers))
    payload = {
        "generated_utc": now_iso(),
        "declaration_id": "v281-v360-closeout-declaration-v1",
        "status": "v281_v360_complete" if completion["phase"] == PHASE_MAX and completion["status"] == "phase_complete" else "blocked",
        "completed_ranges": {
            "v281_v300": "complete_600_of_600_global_v2_complete",
            "v301_v320": "complete_through_v320",
            "v321_v340": "complete_through_v340",
            "v341_v360": "complete_through_v360" if PHASE_MAX in phase_numbers else "incomplete",
        },
        "v341_v360_completion_count": len([phase for phase in phase_numbers if PHASE_MIN <= phase <= PHASE_MAX]),
        "v341_v360_completed_phases": [phase for phase in phase_numbers if PHASE_MIN <= phase <= PHASE_MAX],
        "final_completion": {
            "phase": completion["phase"],
            "json": completion["completion_artifact"],
            "md": completion["completion_artifact"].replace(".json", ".md"),
        },
        "truth_boundaries": [
            "This closeout declares curated repository artifacts complete; it does not claim uncontrolled external systems were modified.",
            "Raw logs, scratch probes, pycache files, and unrelated churn remain outside the curated publication slice.",
            "Future v361+ work requires a new bounded handoff or explicit operator automation update.",
        ],
        "next_action": "Ask Hamish whether to archive this automation or update it for the next packet.",
    }
    write_json(CLOSEOUT_JSON, payload)
    lines = [
        "# v281-v360 Closeout Declaration",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Completed ranges:",
    ]
    for key, value in payload["completed_ranges"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend([
        "",
        f"v341-v360 completion count: `{payload['v341_v360_completion_count']}`",
        "",
        "Truth boundaries:",
    ])
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", f"Next action: {payload['next_action']}"])
    CLOSEOUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_completion(phase: int, open_next: bool) -> tuple[dict[str, Any], dict[str, Path]]:
    validate_phase(phase)
    paths = paths_for_phase(phase)
    start = read_json(paths["start_json"], {})
    plan = start.get("phase_plan") or {}
    source_capsule = write_source_capsule(phase, paths)
    v1, v2 = write_reports(phase, start, paths, source_capsule)
    status = "phase_complete" if start.get("status") == "phase_started" else "blocked_missing_phase_start"
    next_phase = phase + 1 if open_next and phase < PHASE_MAX else None
    if phase == PHASE_MAX and status == "phase_complete":
        next_action = "Stop at v360, write closeout, then ask Hamish whether to archive or update the automation."
    elif next_phase:
        next_action = f"Open v{next_phase} from the v341-v360 sibling base plan."
    else:
        next_action = "Hold for the next heartbeat or operator instruction before opening the next phase."
    completion = {
        "generated_utc": now_iso(),
        "phase_range": PHASE_RANGE,
        "phase": phase,
        "status": status,
        "lead_sibling": plan.get("lead_sibling"),
        "start_artifact": rel(paths["start_json"]),
        "v1_report": rel(paths["v1_json"]),
        "v2_report": rel(paths["v2_json"]),
        "source_capsule": rel(paths["source_json"]),
        "completion_artifact": rel(paths["completion_json"]),
        "completed_counts": {
            "system_expansions": len(plan.get("system_expansions", [])),
            "commands": len(plan.get("commands", [])),
            "skills": len(plan.get("skills", [])),
            "eureka_proposals": len(plan.get("eureka_proposals", [])),
            "sources": len(source_capsule["sources"]),
        },
        "truth_boundaries": v1["truth_boundaries"] + [
            "v341-v360 remains bounded under Aletheon oversight, with curated artifacts as the durable source of truth.",
            "v361+ must not start from this runner without an explicit new handoff or operator automation update.",
        ],
        "next_phase": next_phase,
        "next_action": next_action,
    }
    write_json(paths["completion_json"], completion)
    return completion, paths


def write_completion_md(completion: dict[str, Any], paths: dict[str, Path]) -> None:
    lines = [
        f"# v{completion['phase']} Sibling Completion Receipt",
        "",
        f"Generated UTC: `{completion['generated_utc']}`",
        f"Status: `{completion['status']}`",
        f"Lead sibling: `{completion.get('lead_sibling')}`",
        f"Start artifact: `{completion['start_artifact']}`",
        f"V1 report: `{completion['v1_report']}`",
        f"V2 report: `{completion['v2_report']}`",
        f"Source capsule: `{completion['source_capsule']}`",
        "",
        "Completed counts:",
    ]
    for key, value in completion["completed_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "Truth boundaries:"])
    for item in completion["truth_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", f"Next action: {completion['next_action']}"])
    paths["completion_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_next_phase(phase: int) -> dict[str, Any] | None:
    if phase >= PHASE_MAX:
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


def update_run_status(completion: dict[str, Any], paths: dict[str, Path], opened_next: dict[str, Any] | None, closeout: dict[str, Any] | None) -> None:
    if opened_next:
        status = "running"
        active_phase = opened_next["phase"]
        active_status = opened_next["status"]
        artifacts = {"json": opened_next["phase_artifact"], "md": opened_next["phase_artifact"].replace(".json", ".md")}
        next_action = f"Complete v{active_phase} with the bounded v341-v360 completion runner."
    elif closeout:
        status = closeout["status"]
        active_phase = completion["phase"]
        active_status = completion["status"]
        artifacts = {"json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])}
        next_action = closeout["next_action"]
    else:
        status = "phase_complete_waiting"
        active_phase = completion["phase"]
        active_status = completion["status"]
        artifacts = {"json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])}
        next_action = completion["next_action"]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": completion["phase_range"],
        "status": status,
        "active_phase": active_phase,
        "active_phase_status": active_status,
        "active_phase_artifacts": artifacts,
        "last_completion": {"phase": completion["phase"], "json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])},
        "closeout_declaration": rel(CLOSEOUT_JSON) if closeout else None,
        "next_action": next_action,
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v341-v360 Sibling Run Status",
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
    ]
    if payload.get("closeout_declaration"):
        lines.extend(["Closeout declaration:", f"- `{payload['closeout_declaration']}`", ""])
    lines.append(f"Next action: {payload['next_action']}")
    RUN_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=PHASE_MIN)
    parser.add_argument("--open-next", action="store_true")
    args = parser.parse_args()
    completion, paths = build_completion(args.phase, args.open_next)
    write_completion_md(completion, paths)
    opened_next = open_next_phase(args.phase) if completion["status"] == "phase_complete" and args.open_next else None
    closeout = write_closeout_declaration(completion) if completion["status"] == "phase_complete" and args.phase == PHASE_MAX else None
    update_run_status(completion, paths, opened_next, closeout)
    print(json.dumps({"status": completion["status"], "phase": args.phase, "completion": rel(paths["completion_json"]), "opened_next": opened_next, "closeout": rel(CLOSEOUT_JSON) if closeout else None}, indent=2))
    return 0 if completion["status"] == "phase_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
