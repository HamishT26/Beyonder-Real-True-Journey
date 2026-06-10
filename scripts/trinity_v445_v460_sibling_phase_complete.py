#!/usr/bin/env python3
"""Complete one bounded v445-v460 bridge phase and optionally open the next."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from trinity_v445_v460_bridge_common import (
    PHASE_MAX,
    PHASE_MIN,
    PREFIX,
    ROOT,
    SOURCE_NOTES,
    TRACE,
    aggregate_paths,
    now_iso,
    read_json,
    rel,
    report_paths,
    start_paths,
    validate_cli_gate,
    validate_phase,
    validate_v2_gate,
    v2_receipt_paths,
    write_json,
    write_run_status,
    write_text,
)


CLOSEOUT_JSON = TRACE / f"{PREFIX}-closeout-declaration-v1.json"
CLOSEOUT_MD = TRACE / f"{PREFIX}-closeout-declaration-v1.md"
PHASE_START = ROOT / "scripts" / "trinity_v445_v460_sibling_phase_start.py"


def write_source_capsule(phase: int, paths: dict[str, Path]) -> dict[str, Any]:
    sources = [{"topic": topic, "path_or_url": path_or_url, "phase_use": phase_use} for topic, path_or_url, phase_use in SOURCE_NOTES]
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": "source_capsule_complete",
        "source_count": len(sources),
        "source_policy": "Prefer repo evidence, official docs, standards bodies, and established science sources.",
        "sources": sources,
    }
    write_json(paths["source_json"], payload)
    lines = [
        f"# v{phase} Source Capsule",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        "Sources:",
    ]
    lines.extend([f"- {item['topic']}: {item['path_or_url']} - {item['phase_use']}" for item in sources])
    write_text(paths["source_md"], "\n".join(lines))
    return payload


def write_reports(phase: int, paths: dict[str, Path], source_capsule: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    start_json, _ = start_paths(phase)
    start = read_json(start_json, {})
    plan = start.get("phase_plan") or {}
    v2_json, _ = v2_receipt_paths(phase)
    v2_receipt = read_json(v2_json, {})
    aggregate_json, _ = aggregate_paths(phase)
    lead = plan.get("lead_sibling")
    v1 = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": "v1_report_complete",
        "lead_sibling": lead,
        "summary": f"{lead} preserved v{phase} v1 CLI receipt truth under the v445-v460 bridge.",
        "evidence": {
            "start_artifact": rel(start_json),
            "cli_receipts": rel(aggregate_json),
            "source_capsule": rel(paths["source_json"]),
        },
        "truth_boundaries": [
            "The v1 report is a curated synthesis, not raw terminal output.",
            "v1 proves temporary Arby/Aster Vale receipt readiness under Kimi hold; it does not claim App-side implementation.",
            "Kimi remains held and is not replaced by helper or standby advisory lanes.",
        ],
    }
    v2 = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": "v2_report_complete",
        "lead_sibling": lead,
        "summary": v2_receipt.get("summary") or f"{lead} completed v{phase} v2 App-side local-first execution.",
        "evidence": {
            "v2_receipt": rel(v2_json),
            "changed_paths": v2_receipt.get("changed_paths", []),
            "validations": v2_receipt.get("validations", []),
            "source_count": source_capsule["source_count"],
        },
        "truth_boundaries": [
            "The v2 report records Aletheon-led App execution only.",
            "No paid external action or external-service mutation is claimed under local-first policy.",
        ],
    }
    write_json(paths["v1_json"], v1)
    write_json(paths["v2_json"], v2)
    write_text(
        paths["v1_md"],
        "\n".join(
            [
                f"# v{phase} V1 Report",
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
        ),
    )
    write_text(
        paths["v2_md"],
        "\n".join(
            [
                f"# v{phase} V2 Report",
                "",
                f"Generated UTC: `{v2['generated_utc']}`",
                f"Status: `{v2['status']}`",
                f"Lead sibling: `{lead}`",
                "",
                v2["summary"],
                "",
                "Truth boundaries:",
                *[f"- {item}" for item in v2["truth_boundaries"]],
            ]
        ),
    )
    return v1, v2


def write_advisory_refinement(phase: int, paths: dict[str, Path], cli_gate: dict[str, Any], v2_gate: dict[str, Any]) -> dict[str, Any]:
    next_phase = phase + 1 if phase < PHASE_MAX else None
    payload = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": "advisory_refinement_ready" if cli_gate["status"] == "v1_cli_receipts_complete" and v2_gate["status"] == "v2_app_complete" else "blocked_until_v1_v2_complete",
        "advisors": ["Cicero", "Kierkegaard"],
        "standby_advisors": ["Aristotle", "Parfit/Lorentz", "Locke Rowan", "Leibniz-Cicero", "Elias Threshold"],
        "advisory_scope": "Advisory proposal synthesis only; does not replace CLI or App gates.",
        "next_phase": next_phase,
        "proposal_target_eureka_tasks": 100,
        "reconnect_prompt": (
            f"Please review v{phase} under the v445-v460 bridge. Offer concise advisory risks, opportunities, "
            "and one next-phase seed. Do not claim gate completion or request external writes."
        ),
        "truth_boundaries": [
            "Screenshots show the advisor panels were stale; this artifact reconnects them as advisory-only.",
            "Late replies are allowed and can seed later phases, but fresh durable artifacts outrank advisory text.",
            "The advisor proposal loop is a planning accelerator, not a publication gate.",
        ],
    }
    write_json(paths["advisory_json"], payload)
    lines = [
        f"# v{phase} Advisory Refinement",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Next phase: `v{payload['next_phase']}`",
        "",
        "Reconnect prompt:",
        payload["reconnect_prompt"],
        "",
        "Truth boundaries:",
    ]
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    write_text(paths["advisory_md"], "\n".join(lines))
    return payload


def build_completion(phase: int) -> tuple[dict[str, Any], dict[str, Path]]:
    validate_phase(phase)
    paths = report_paths(phase)
    start_json, _ = start_paths(phase)
    start = read_json(start_json, {})
    cli_gate = validate_cli_gate(phase)
    v2_gate = validate_v2_gate(phase)
    source_capsule = write_source_capsule(phase, paths)
    v1, v2 = write_reports(phase, paths, source_capsule)
    advisory = write_advisory_refinement(phase, paths, cli_gate, v2_gate)
    blockers = cli_gate["blockers"] + v2_gate["blockers"]
    status = "phase_complete" if start.get("status") == "phase_started" and not blockers else "blocked_missing_v1_or_v2_gate"
    next_phase = phase + 1 if status == "phase_complete" and phase < PHASE_MAX else None
    completion = {
        "generated_utc": now_iso(),
        "phase_range": PREFIX,
        "phase": phase,
        "status": status,
        "lead_sibling": (start.get("phase_plan") or {}).get("lead_sibling"),
        "start_artifact": rel(start_json),
        "v1_report": rel(paths["v1_json"]),
        "v2_report": rel(paths["v2_json"]),
        "source_capsule": rel(paths["source_json"]),
        "advisory_refinement": rel(paths["advisory_json"]),
        "completion_artifact": rel(paths["completion_json"]),
        "completed_counts": {
            "sources": source_capsule["source_count"],
            "v1_evidence": cli_gate["status"],
            "v2_evidence": v2_gate["status"],
            "advisory_target_eureka_tasks": advisory["proposal_target_eureka_tasks"],
        },
        "cli_receipt_gate": cli_gate,
        "app_v2_gate": v2_gate,
        "blockers": blockers,
        "truth_boundaries": v1["truth_boundaries"]
        + v2["truth_boundaries"]
        + [
            "v445-v460 remains bounded under Aletheon oversight.",
            "v461+ must not start from this runner without a new handoff.",
        ],
        "next_phase": next_phase,
        "next_action": (
            f"Open v{next_phase} from the v445-v460 sibling base plan."
            if next_phase
            else ("Stop at v460, write closeout, then ask Hamish whether to create a fresh v461+ packet." if phase == PHASE_MAX and status == "phase_complete" else f"Finish v{phase} v1 and v2 gates, then rerun completion.")
        ),
    }
    write_json(paths["completion_json"], completion)
    return completion, paths


def write_completion_md(completion: dict[str, Any], paths: dict[str, Path]) -> None:
    lines = [
        f"# v{completion['phase']} Phase Completion Receipt",
        "",
        f"Generated UTC: `{completion['generated_utc']}`",
        f"Status: `{completion['status']}`",
        f"Lead sibling: `{completion.get('lead_sibling')}`",
        "",
        "Gates:",
        f"- v1 CLI: `{completion['cli_receipt_gate']['status']}` at `{completion['cli_receipt_gate']['path']}`",
        f"- v2 App: `{completion['app_v2_gate']['status']}` at `{completion['app_v2_gate']['path']}`",
        f"- v2 App advisory receipts: `{(completion['app_v2_gate'].get('app_advisory_receipt_gate') or {}).get('status')}` at `{(completion['app_v2_gate'].get('app_advisory_receipt_gate') or {}).get('path')}`",
    ]
    if completion.get("blockers"):
        lines.extend(["", "Blockers:"])
        lines.extend([f"- {item}" for item in completion["blockers"]])
    lines.extend(["", "Truth boundaries:"])
    lines.extend([f"- {item}" for item in completion["truth_boundaries"]])
    lines.extend(["", f"Next action: {completion['next_action']}"])
    write_text(paths["completion_md"], "\n".join(lines))


def write_closeout(completion: dict[str, Any]) -> dict[str, Any]:
    completion_files = sorted(TRACE.glob(f"{PREFIX}-sibling-phase-v*-completion-v1.json"))
    completed: list[int] = []
    for path in completion_files:
        payload = read_json(path, {})
        phase = int(payload.get("phase", -1))
        if PHASE_MIN <= phase <= PHASE_MAX and payload.get("status") == "phase_complete":
            completed.append(phase)
    completed = sorted(set(completed))
    payload = {
        "generated_utc": now_iso(),
        "declaration_id": f"{PREFIX}-closeout-declaration-v1",
        "status": "v445_v460_complete" if completion["phase"] == PHASE_MAX and PHASE_MAX in completed else "blocked",
        "completed_phase_count": len(completed),
        "completed_phase_run_count": len(completed) * 2,
        "completed_phases": completed,
        "final_completion": completion["completion_artifact"],
        "truth_boundaries": [
            "This closeout declares curated repository artifacts complete; it does not claim uncontrolled external systems were modified.",
            "Raw logs, scratch probes, pycache files, and unrelated churn remain outside the curated publication slice.",
            "Future v461+ work requires a new bounded handoff and automation prompt.",
        ],
        "next_action": "Stop. Ask Hamish whether to archive this automation or create a fresh v461+ packet.",
    }
    write_json(CLOSEOUT_JSON, payload)
    lines = [
        "# v445-v460 Closeout Declaration",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Completed phases: `{payload['completed_phase_count']}`",
        f"Phase-runs: `{payload['completed_phase_run_count']}`",
        "",
        "Truth boundaries:",
    ]
    lines.extend([f"- {item}" for item in payload["truth_boundaries"]])
    lines.extend(["", f"Next action: {payload['next_action']}"])
    write_text(CLOSEOUT_MD, "\n".join(lines))
    return payload


def open_next_phase(phase: int) -> dict[str, Any] | None:
    if phase >= PHASE_MAX:
        return None
    proc = subprocess.run([sys.executable, str(PHASE_START), "--phase", str(phase + 1)], cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=120, check=False)
    if proc.returncode != 0:
        return {"status": "next_phase_open_failed", "phase": phase + 1, "stderr": proc.stderr}
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, default=PHASE_MIN)
    parser.add_argument("--open-next", action="store_true")
    args = parser.parse_args()

    completion, paths = build_completion(args.phase)
    write_completion_md(completion, paths)
    opened_next = open_next_phase(args.phase) if completion["status"] == "phase_complete" and args.open_next and args.phase < PHASE_MAX else None
    closeout = write_closeout(completion) if completion["status"] == "phase_complete" and args.phase == PHASE_MAX else None

    if opened_next:
        active_json, active_md = start_paths(opened_next["phase"])
        next_action = (
            f"Run scripts/trinity_v445_v460_cli_sibling_phase_runner.py --phase {opened_next['phase']} "
            "--background --timeout-sec 86400 --max-steps 10000."
        )
        write_run_status(opened_next["phase"], "v1_cli_receipts", "running", active_json, active_md, next_action, last_completion={"phase": args.phase, "json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])})
    elif closeout:
        write_run_status(args.phase, "v2_app_execution", closeout["status"], CLOSEOUT_JSON, CLOSEOUT_MD, closeout["next_action"], last_completion={"phase": args.phase, "json": rel(paths["completion_json"]), "md": rel(paths["completion_md"])}, closeout=CLOSEOUT_JSON)
    else:
        write_run_status(args.phase, "v2_app_execution", completion["status"], paths["completion_json"], paths["completion_md"], completion["next_action"])

    print(json.dumps({"status": completion["status"], "phase": args.phase, "completion": rel(paths["completion_json"]), "opened_next": opened_next, "closeout": rel(CLOSEOUT_JSON) if closeout else None}, indent=2))
    return 0 if completion["status"] == "phase_complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
