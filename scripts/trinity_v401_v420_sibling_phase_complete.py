#!/usr/bin/env python3
"""Complete one bounded v401-v420 sibling phase and optionally open the next."""

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
RUN_STATUS_JSON = TRACE / "v401-v420-sibling-run-status-v1.json"
RUN_STATUS_MD = TRACE / "v401-v420-sibling-run-status-v1.md"
PHASE_START = ROOT / "scripts" / "trinity_v401_v420_sibling_phase_start.py"
CLOSEOUT_JSON = TRACE / "v401-v420-closeout-declaration-v1.json"
CLOSEOUT_MD = TRACE / "v401-v420-closeout-declaration-v1.md"

PHASE_MIN = 401
PHASE_MAX = 420
PHASE_RANGE = "v401-v420"
REQUIRED_CLI_LANES = {"Arby": "Codex CLI", "Kimi": "Kimi CLI", "Aster Vale": "Codex CLI"}

SOURCE_NOTES = [
    ("v281-v360 closeout", "docs/trinity-live-traces/v281-v360-closeout-declaration-v1.json", "Use completed packet truth as the floor."),
    ("v361-v370 closeout", "docs/trinity-live-traces/v361-v370-closeout-declaration-v1.json", "Use the predecessor packet truth as inherited context."),
    ("v371-v400 closeout", "docs/trinity-live-traces/v371-v400-closeout-declaration-v1.json", "Use the latest completed packet as the direct predecessor."),
    ("v401-v420 final handoff", "docs/trinity-live-traces/v401-v420-final-handoff-v1.json", "Use bounded successor packet rules."),
    ("OpenAI Codex docs", "https://developers.openai.com/codex/", "Keep Codex automation and CLI claims tied to official docs."),
    ("Model Context Protocol", "https://modelcontextprotocol.io/", "Keep MCP expansion inside explicit trust boundaries."),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Govern, map, measure, and manage risk."),
    ("UNESCO AI ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Keep dignity, rights, and human flourishing visible."),
    ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "Preserve risk-based governance language."),
    ("W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model/", "Anchor Freed ID portability discussions."),
    ("CERN Standard Model", "https://home.cern/science/physics/standard-model", "Separate established physics from exploratory GMUT framing."),
    ("NASA dark matter and dark energy", "https://science.nasa.gov/universe/dark-matter-dark-energy/", "Keep cosmology unknowns honest."),
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
    stem = f"v401-v420-sibling-phase-v{phase}"
    return {
        "start_json": TRACE / f"{stem}-start-v1.json",
        "completion_json": TRACE / f"{stem}-completion-v1.json",
        "completion_md": TRACE / f"{stem}-completion-v1.md",
        "v1_json": TRACE / f"{stem}-v1-report-v1.json",
        "v1_md": TRACE / f"{stem}-v1-report-v1.md",
        "v2_json": TRACE / f"{stem}-v2-report-v1.json",
        "v2_md": TRACE / f"{stem}-v2-report-v1.md",
        "source_json": TRACE / f"v401-v420-sibling-source-capsule-v{phase}-v1.json",
        "source_md": TRACE / f"v401-v420-sibling-source-capsule-v{phase}-v1.md",
        "cli_receipts_json": TRACE / f"{stem}-cli-receipts-v1.json",
        "cli_receipts_md": TRACE / f"{stem}-cli-receipts-v1.md",
    }


def validate_cli_receipts(phase: int, paths: dict[str, Path]) -> dict[str, Any]:
    gate = {"required": True, "path": rel(paths["cli_receipts_json"]), "status": "blocked_missing_cli_receipts", "blockers": []}
    if not paths["cli_receipts_json"].exists():
        gate["blockers"].append(f"Run scripts/trinity_v401_v420_cli_sibling_phase_runner.py --phase {phase} --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000 before completion.")
        return gate
    payload = read_json(paths["cli_receipts_json"], {})
    gate["status"] = payload.get("status") or "blocked_unreadable_cli_receipts"
    if payload.get("status") != "cli_receipts_complete":
        gate["blockers"].append("CLI receipt aggregate is not complete.")
    receipts = payload.get("lane_receipts") or []
    for lane, expected_surface in REQUIRED_CLI_LANES.items():
        receipt = next((item for item in receipts if item.get("lane") == lane), None)
        if not receipt:
            gate["blockers"].append(f"Missing {lane} CLI receipt.")
            continue
        if receipt.get("surface") != expected_surface:
            gate["blockers"].append(f"{lane} receipt is from {receipt.get('surface')} instead of {expected_surface}.")
        if receipt.get("receipt_status") != "valid_cli_receipt" or not receipt.get("valid"):
            gate["blockers"].append(f"{lane} receipt is not valid: {receipt.get('receipt_status')}.")
        if int(receipt.get("requested_max_steps") or receipt.get("max_steps") or 0) < 10000:
            gate["blockers"].append(f"{lane} did not record the requested 10000 max useful steps.")
        receipt_path = receipt.get("receipt_path")
        if receipt_path and not (ROOT / receipt_path).exists():
            gate["blockers"].append(f"{lane} receipt path does not exist: {receipt_path}.")
    gate["status"] = "blocked_missing_cli_receipts" if gate["blockers"] else "cli_receipts_complete"
    return gate


def write_source_capsule(phase: int, paths: dict[str, Path]) -> dict[str, Any]:
    sources = [{"topic": topic, "path_or_url": path_or_url, "phase_use": phase_use} for topic, path_or_url, phase_use in SOURCE_NOTES]
    payload = {"generated_utc": now_iso(), "phase": phase, "status": "source_capsule_complete", "source_count": len(sources), "source_policy": "Prefer repo evidence, official docs, standards bodies, and established science sources.", "sources": sources}
    write_json(paths["source_json"], payload)
    lines = [f"# v{phase} Sibling Source Capsule", "", f"Generated UTC: `{payload['generated_utc']}`", f"Status: `{payload['status']}`", f"Source count: `{payload['source_count']}`", "", f"Source policy: {payload['source_policy']}", "", "Sources:"]
    lines.extend([f"- {item['topic']}: {item['path_or_url']} - {item['phase_use']}" for item in sources])
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
        "summary": f"{lead} preserved v401-v420 handoff truth and mapped v{phase} into bounded CLI receipt evidence.",
        "evidence": {"start_artifact": rel(paths["start_json"]), "source_capsule": rel(paths["source_json"]), "sources": len(source_capsule["sources"])},
        "truth_boundaries": [
            "The v1 report is a curated synthesis, not raw terminal output.",
            "No claim is made that paid/cloud providers were touched without explicit scope and credentials.",
            "Speculative science, GMUT, and frontier AI synthesis are framed as exploratory unless independently validated.",
        ],
    }
    v2 = {
        "generated_utc": now_iso(),
        "phase": phase,
        "status": "v2_report_complete",
        "lead_sibling": lead,
        "summary": f"{lead} converted v{phase} receipt evidence into next-phase readiness and publication hygiene.",
        "readiness": {"app_heartbeat_minutes": 30, "max_steps_requested": 10000, "stage_raw_logs": False, "next_phase_upper_bound": PHASE_MAX},
        "handoff_notes": [
            "Keep one active phase at a time.",
            "Before commit or push, fetch and verify branch drift.",
            "At v420, stop, write the v401-v420 closeout declaration, and ask Hamish whether to archive or update automation.",
        ],
    }
    write_json(paths["v1_json"], v1)
    write_json(paths["v2_json"], v2)
    paths["v1_md"].write_text("\n".join([f"# v{phase} Sibling V1 Report", "", f"Generated UTC: `{v1['generated_utc']}`", f"Status: `{v1['status']}`", f"Lead sibling: `{lead}`", "", v1["summary"], "", "Truth boundaries:", *[f"- {item}" for item in v1["truth_boundaries"]]]) + "\n", encoding="utf-8")
    paths["v2_md"].write_text("\n".join([f"# v{phase} Sibling V2 Report", "", f"Generated UTC: `{v2['generated_utc']}`", f"Status: `{v2['status']}`", f"Lead sibling: `{lead}`", "", v2["summary"], "", "Handoff notes:", *[f"- {item}" for item in v2["handoff_notes"]]]) + "\n", encoding="utf-8")
    return v1, v2


def write_closeout_declaration(completion: dict[str, Any]) -> dict[str, Any]:
    completions = sorted(TRACE.glob("v401-v420-sibling-phase-v*-completion-v1.json"))
    phase_numbers: list[int] = []
    for item in completions:
        try:
            phase_numbers.append(int(item.name.split("-phase-v", 1)[1].split("-", 1)[0]))
        except (IndexError, ValueError):
            continue
    phase_numbers = sorted(set(phase_numbers))
    payload = {
        "generated_utc": now_iso(),
        "declaration_id": "v401-v420-closeout-declaration-v1",
        "status": "v401_v420_complete" if completion["phase"] == PHASE_MAX and completion["status"] == "phase_complete" else "blocked",
        "completed_ranges": {
            "v281_v360": "complete",
            "v361_v370": "complete",
            "v371_v400": "complete",
            "v401_v420": "complete_through_v420" if PHASE_MAX in phase_numbers else "incomplete",
        },
        "v401_v420_completion_count": len([phase for phase in phase_numbers if PHASE_MIN <= phase <= PHASE_MAX]),
        "v401_v420_completed_phases": [phase for phase in phase_numbers if PHASE_MIN <= phase <= PHASE_MAX],
        "final_completion": {"phase": completion["phase"], "json": completion["completion_artifact"], "md": completion["completion_artifact"].replace(".json", ".md")},
        "truth_boundaries": [
            "This closeout declares curated repository artifacts complete; it does not claim uncontrolled external systems were modified.",
            "Raw logs, scratch probes, pycache files, and unrelated churn remain outside the curated publication slice.",
            "Future v421+ work requires a new bounded handoff or explicit operator automation update.",
        ],
        "next_action": "Ask Hamish whether to archive this automation or update it for the next packet.",
    }
    write_json(CLOSEOUT_JSON, payload)
    lines = ["# v401-v420 Closeout Declaration", "", f"Generated UTC: `{payload['generated_utc']}`", f"Status: `{payload['status']}`", "", "Completed ranges:"]
    lines.extend([f"- `{key}`: `{value}`" for key, value in payload["completed_ranges"].items()])
    lines.extend(["", f"v401-v420 completion count: `{payload['v401_v420_completion_count']}`", "", "Truth boundaries:", *[f"- {item}" for item in payload["truth_boundaries"]], "", f"Next action: {payload['next_action']}"])
    CLOSEOUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def build_completion(phase: int, open_next: bool) -> tuple[dict[str, Any], dict[str, Path]]:
    validate_phase(phase)
    paths = paths_for_phase(phase)
    start = read_json(paths["start_json"], {})
    plan = start.get("phase_plan") or {}
    cli_gate = validate_cli_receipts(phase, paths)
    source_capsule = write_source_capsule(phase, paths)
    v1, _v2 = write_reports(phase, start, paths, source_capsule)
    status = "phase_complete" if start.get("status") == "phase_started" else "blocked_missing_phase_start"
    if status == "phase_complete" and cli_gate["blockers"]:
        status = "blocked_missing_cli_receipts"
    next_phase = phase + 1 if open_next and phase < PHASE_MAX and status == "phase_complete" else None
    next_action = f"Open v{next_phase} from the v401-v420 sibling base plan." if next_phase else ("Stop at v420, write closeout, then ask Hamish whether to archive or update the automation." if phase == PHASE_MAX and status == "phase_complete" else f"Run scripts/trinity_v401_v420_cli_sibling_phase_runner.py --phase {phase} --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000, then rerun completion after receipts complete.")
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
        "completed_counts": {"sources": len(source_capsule["sources"]), "system_expansions": len(plan.get("system_expansions", [])), "commands": len(plan.get("commands", [])), "skills": len(plan.get("skills", [])), "eureka_proposals": len(plan.get("eureka_proposals", []))},
        "cli_receipt_gate": cli_gate,
        "blockers": cli_gate["blockers"] if cli_gate["blockers"] else [],
        "truth_boundaries": v1["truth_boundaries"] + ["v401-v420 remains bounded under Aletheon oversight.", "v421+ must not start from this runner without a new handoff."],
        "next_phase": next_phase,
        "next_action": next_action,
    }
    write_json(paths["completion_json"], completion)
    return completion, paths


def write_completion_md(completion: dict[str, Any], paths: dict[str, Path]) -> None:
    gate = completion.get("cli_receipt_gate") or {}
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
        "CLI receipt gate:",
        f"- Required: `{gate.get('required')}`",
        f"- Status: `{gate.get('status')}`",
        f"- Artifact: `{gate.get('path')}`",
    ]
    if completion.get("blockers"):
        lines.extend(["", "Blockers:", *[f"- {item}" for item in completion["blockers"]]])
    lines.extend(["", "Truth boundaries:", *[f"- {item}" for item in completion["truth_boundaries"]], "", f"Next action: {completion['next_action']}"])
    paths["completion_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_next_phase(phase: int) -> dict[str, Any] | None:
    if phase >= PHASE_MAX:
        return None
    proc = subprocess.run([sys.executable, str(PHASE_START), "--phase", str(phase + 1)], cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=120, check=False)
    if proc.returncode != 0:
        return {"status": "next_phase_open_failed", "phase": phase + 1, "stderr": proc.stderr}
    return json.loads(proc.stdout)


def update_run_status(completion: dict[str, Any], paths: dict[str, Path], opened_next: dict[str, Any] | None, closeout: dict[str, Any] | None) -> None:
    if opened_next:
        status = "running"
        active_phase = opened_next["phase"]
        active_status = opened_next["status"]
        artifacts = {"json": opened_next["phase_artifact"], "md": opened_next["phase_artifact"].replace(".json", ".md")}
        next_action = f"Run scripts/trinity_v401_v420_cli_sibling_phase_runner.py --phase {active_phase} --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000."
    elif closeout:
        status = closeout["status"]
        active_phase = completion["phase"]
        active_status = completion["status"]
        artifacts = {"json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])}
        next_action = closeout["next_action"]
    else:
        status = "phase_complete_waiting" if completion["status"] == "phase_complete" else completion["status"]
        active_phase = completion["phase"]
        active_status = completion["status"]
        artifacts = {"json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])}
        next_action = completion["next_action"]
    payload = {"generated_utc": now_iso(), "phase_range": completion["phase_range"], "status": status, "active_phase": active_phase, "active_phase_status": active_status, "active_phase_artifacts": artifacts, "last_completion": {"phase": completion["phase"], "json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])} if completion["status"] == "phase_complete" else None, "closeout_declaration": rel(CLOSEOUT_JSON) if closeout else None, "next_action": next_action}
    write_json(RUN_STATUS_JSON, payload)
    lines = ["# v401-v420 Sibling Run Status", "", f"Generated UTC: `{payload['generated_utc']}`", f"Status: `{payload['status']}`", f"Active phase: `v{payload['active_phase']}`", f"Active phase status: `{payload['active_phase_status']}`", "", "Active artifacts:", f"- `{payload['active_phase_artifacts']['json']}`", f"- `{payload['active_phase_artifacts']['md']}`", ""]
    if payload.get("last_completion"):
        lines.extend(["Last completion:", f"- `v{payload['last_completion']['phase']}`", f"- `{payload['last_completion']['json']}`", f"- `{payload['last_completion']['md']}`", ""])
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
