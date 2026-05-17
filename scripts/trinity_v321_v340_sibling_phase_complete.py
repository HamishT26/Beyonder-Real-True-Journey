#!/usr/bin/env python3
"""Complete one v321-v340 sibling phase and optionally open the next."""

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
RUN_STATUS_JSON = TRACE / "v321-v340-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v321-v340-sibling-run-status-v1.md"
PHASE_START = ROOT / "scripts" / "trinity_v321_v340_sibling_phase_start.py"

SOURCE_NOTES = [
    ("v301-v320 closeout", "docs/trinity-live-traces/v301-v320-aletheon-run-status-v1.json", "Use v320 completion as the handoff floor."),
    ("v321-v340 handoff", "docs/trinity-live-traces/v321-v340-sibling-handoff-v1.json", "Use sibling rules, watcher state, and staging boundaries."),
    ("OpenAI Codex automations", "https://developers.openai.com/codex/app/automations", "Keep the app heartbeat as the thread-context wake layer."),
    ("Microsoft laptop lid power behavior", "https://support.microsoft.com/windows/shut-down-sleep-or-hibernate-your-pc-2941d165-7d0a-a5e8-c5ad-8c972e8e6eff", "Treat partial lid closure as a host power-state risk before blaming repo automation."),
    ("MCP security best practices", "https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices", "Keep MCP/API expansion behind explicit trust boundaries."),
    ("GitHub Actions security", "https://docs.github.com/en/actions/how-tos/security-for-github-actions", "Keep workflow and token handling conservative."),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Govern, map, measure, and manage risk as the phase expands."),
    ("UNESCO AI ethics", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence?hub=66973", "Keep human dignity and rights visible in synthesis language."),
    ("W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model/", "Anchor Freed ID discussions in portable credential standards."),
    ("CERN Standard Model", "https://home.cern/science/physics/standard-model/", "Separate established physics from metaphoric GMUT synthesis."),
    ("NASA dark matter and dark energy", "https://science.nasa.gov/universe/dark-matter-dark-energy/", "Keep cosmology unknowns honest."),
    ("OpenAI Codex app", "https://openai.com/codex", "Treat Codex as the agentic coding command center, not as proof of unattended success."),
    ("OpenAI Responses API", "https://platform.openai.com/docs/api-reference/responses", "Keep future API calls stateful, auditable, and explicitly scoped."),
    ("OpenAI Agents SDK", "https://openai.github.io/openai-agents-python/agents/", "Separate agents, tools, handoffs, guardrails, and sessions."),
    ("OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html", "Keep trustworthy AI tied to human rights, democratic values, and accountability."),
    ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "Preserve risk-based governance and human oversight in system claims."),
    ("Perimeter quantum gravity", "https://perimeterinstitute.ca/quantum-gravity", "Treat theory-of-everything synthesis as exploratory until mathematical and empirical bridges exist."),
    ("NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "Treat future hardware as acceleration, not a prerequisite for repo correctness."),
    ("NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "Keep simulation and digital-twin ideas as optional validation layers."),
    ("NVIDIA NVLink", "https://www.nvidia.com/object/multi-gpu-technology.html", "Use high-bandwidth interconnects as an analogy for explicit handoff channels."),
    ("Cloudflare Workers AI and agents", "https://developers.cloudflare.com/workers/framework-guides/ai-and-agents/", "Keep edge deployment exploratory until secrets and scope are explicit."),
    ("Neon MCP Server", "https://neon.com/docs/ai/neon-mcp-server", "Use database branch and MCP actions only after credentials, rollback, and scope are clear."),
    ("CircleCI contexts", "https://circleci.com/docs/guides/security/contexts/", "Keep CI secrets in restricted contexts and avoid leaking them into logs."),
    ("Vercel AI agents", "https://vercel.com/docs/agents/", "Treat hosted agent deployment as future scoped infrastructure, not current implicit access."),
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


def paths_for_phase(phase: int) -> dict[str, Path]:
    return {
        "start_json": TRACE / f"v321-v340-sibling-phase-v{phase}-start-v1.json",
        "completion_json": TRACE / f"v321-v340-sibling-phase-v{phase}-completion-v1.json",
        "completion_md": TRACE / f"v321-v340-sibling-phase-v{phase}-completion-v1.md",
        "v1_json": TRACE / f"v321-v340-sibling-phase-v{phase}-v1-report-v1.json",
        "v1_md": TRACE / f"v321-v340-sibling-phase-v{phase}-v1-report-v1.md",
        "v2_json": TRACE / f"v321-v340-sibling-phase-v{phase}-v2-report-v1.json",
        "v2_md": TRACE / f"v321-v340-sibling-phase-v{phase}-v2-report-v1.md",
        "source_json": TRACE / f"v321-v340-sibling-source-capsule-v{phase}-v1.json",
        "source_md": TRACE / f"v321-v340-sibling-source-capsule-v{phase}-v1.md",
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
        "summary": f"{lead} preserved v301-v320 evidence and mapped the active v321-v340 work into sibling-operable tasks.",
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
            "Laptop lid/sleep disruption is treated as a local wake-stability risk, not a repo failure.",
        ],
    }
    v2 = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "v2_report_complete",
        "lead_sibling": lead,
        "report_type": "v2 readiness and handoff synthesis",
        "summary": f"{lead} converted v1 synthesis into next-phase operating rules and v341-v360 preparation notes.",
        "readiness": {
            "watchdog_required": True,
            "app_heartbeat_recommended_minutes": 30,
            "local_watchdog_recommended_minutes": 5,
            "admin_terminal_default": "avoid",
            "stage_raw_logs": False,
        },
        "handoff_notes": [
            "Continue one phase per wake unless the operator asks for a diagnostic burst.",
            "Keep v321-v340 sibling reports in worktree artifacts.",
            "Prepare v341-v360 only after v321-v340 has complete receipts and a final handoff.",
            "If the laptop lid is partly closed, treat automation stalls as host power-state issues first.",
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


def build_completion(phase: int, open_next: bool) -> tuple[dict[str, Any], dict[str, Path]]:
    paths = paths_for_phase(phase)
    start = read_json(paths["start_json"], {})
    plan = start.get("phase_plan") or {}
    source_capsule = write_source_capsule(phase, paths)
    v1, v2 = write_reports(phase, start, paths, source_capsule)
    status = "phase_complete" if start.get("status") == "phase_started" else "blocked_missing_phase_start"
    completion = {
        "generated_utc": now_iso(),
        "phase_range": "v321-v340",
        "phase": phase,
        "status": status,
        "lead_sibling": plan.get("lead_sibling"),
        "start_artifact": rel(paths["start_json"]),
        "v1_report": rel(paths["v1_json"]),
        "v2_report": rel(paths["v2_json"]),
        "source_capsule": rel(paths["source_json"]),
        "completed_counts": {
            "system_expansions": len(plan.get("system_expansions", [])),
            "commands": len(plan.get("commands", [])),
            "skills": len(plan.get("skills", [])),
            "eureka_proposals": len(plan.get("eureka_proposals", [])),
            "sources": len(source_capsule["sources"]),
        },
        "truth_boundaries": v1["truth_boundaries"] + [
            "v321-v340 remains sibling-led under Aletheon oversight, with curated artifacts as the durable source of truth.",
            "v341-v360 should not start until v321-v340 has complete receipts and a final handoff.",
        ],
        "next_phase": phase + 1 if open_next and phase < 340 else None,
        "next_action": (
            f"Open v{phase + 1} from the sibling base plan."
            if open_next and phase < 340
            else "Hold for the next heartbeat or operator instruction before opening the next phase."
        ),
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
    if phase >= 340:
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


def update_run_status(completion: dict[str, Any], paths: dict[str, Path], opened_next: dict[str, Any] | None) -> None:
    if opened_next:
        status = "running"
        active_phase = opened_next["phase"]
        active_status = opened_next["status"]
        artifacts = {"json": opened_next["phase_artifact"], "md": opened_next["phase_artifact"].replace(".json", ".md")}
        next_action = f"Execute v{active_phase} sibling tasks, write v1/v2 reports, complete v{active_phase}, then decide whether v{active_phase + 1} can open."
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
        "next_action": next_action,
    }
    write_json(RUN_STATUS_JSON, payload)
    lines = [
        "# v321-v340 Sibling Run Status",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=321)
    parser.add_argument("--open-next", action="store_true")
    args = parser.parse_args()
    completion, paths = build_completion(args.phase, args.open_next)
    write_completion_md(completion, paths)
    opened_next = open_next_phase(args.phase) if completion["status"] == "phase_complete" and args.open_next else None
    update_run_status(completion, paths, opened_next)
    print(json.dumps({"status": completion["status"], "phase": args.phase, "completion": rel(paths["completion_json"]), "opened_next": opened_next}, indent=2))
    return 0 if completion["status"] == "phase_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
