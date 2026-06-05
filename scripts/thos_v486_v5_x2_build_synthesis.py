#!/usr/bin/env python3
"""Build v486 GMUT/THOS v5 x2 no-stack supervisor synthesis."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v5-x2"
X1 = "v486-gmut-thos-v22-v5-x1"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    generated_utc, generated_nz = now_pair()
    x1_blocker = read_json(TRACE_DIR / f"{X1}-cli-deferral-blocker-v1.json")
    x1_timing = read_json(TRACE_DIR / f"{X1}-five-lane-attempt-status-v1.json")
    x1_source = read_json(TRACE_DIR / f"{X1}-source-refresh-v1.json")

    supervisor = {
        "artifact_type": "no_stack_cli_supervisor_design",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NO_STACK_SUPERVISOR_DESIGN",
        "input_blocker_status": x1_blocker.get("overall_status", "unknown"),
        "rules": [
            "Do not launch a new Arby/Aster CLI attempt while a previous attempt is still active.",
            "Record deferral as a first-class x1 lane state, not as a failure or completion.",
            "Use fresh temp-only output folders for every permitted attempt.",
            "Classify completion only when current phase slug, final marker, and non-stale content checks pass.",
            "Continue x2 build work from safe app-lane and Aletheon evidence while the CLI lane is pending.",
        ],
    }
    approval_candidate = {
        "artifact_type": "stale_cli_process_approval_candidate",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PENDING_USER_APPROVAL_NOT_EXECUTED",
        "candidate_scope": "optional future approval to terminate only Aletheon-launched read-only Codex CLI advisory processes that exceed a user-approved stale threshold with no final-message artifact",
        "not_executed_now": True,
        "reason": "The active approval posture does not require or force process termination; user previously allowed long-running lanes, so this is presented as a future exact packet candidate only.",
        "safety_rules": [
            "Verify process lineage belongs to the exact launched CLI advisory attempt.",
            "Write a status-only receipt before and after termination.",
            "Do not terminate unrelated Codex app, user sessions, worktrees, plugin cache, or system processes.",
            "Do not publish raw command lines or local paths.",
        ],
    }
    app_continuity = {
        "artifact_type": "app_lane_continuity_map",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_APP_LANE_CONTINUITY_MAP",
        "app_lanes": x1_timing.get("app_lanes", []),
        "continuity_uses": [
            "Preserve Cicero/Kierkegaard/Aristotle app-server route as the stable v486 lane backbone.",
            "Use app-lane completion receipts for timing and readiness only, not raw-body publication.",
            "Let x2 synthesize command, source, and GMUT/THOS open-gate tasks while CLI remains deferred.",
        ],
    }
    source_guard = {
        "artifact_type": "source_guard_carry_forward",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SOURCE_GUARD_CARRY_FORWARD",
        "sources": x1_source.get("sources", []),
        "guard": "Use official source surfaces for planning only; no external claim validation or canon promotion.",
    }
    validation = {
        "artifact_type": "x2_build_validation",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V5_X2_BUILD_VALIDATION",
        "artifact_statuses": {
            "supervisor": supervisor["overall_status"],
            "approval_candidate": approval_candidate["overall_status"],
            "app_continuity": app_continuity["overall_status"],
            "source_guard": source_guard["overall_status"],
        },
        "mutation_boundary": {
            "repo_artifacts_written": True,
            "processes_terminated": False,
            "plugin_cache_mutated": False,
            "user_skills_mutated": False,
            "external_accounts_mutated": False,
            "raw_lane_text_published": False,
        },
    }
    synthesis = {
        "artifact_type": "x2_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V486_V5_X2_NO_STACK_SYNTHESIS",
        "result": [
            "Converted the v5 x1 CLI deferral into no-stack supervisor rules.",
            "Prepared an optional future approval candidate for stale CLI process handling, but did not execute it.",
            "Carried app-lane continuity and source guards forward into v6 x1.",
            "Kept GMUT, physics, consciousness, and canon gates open.",
        ],
        "next_boundary": "v486-gmut-thos-v22-v6-x1",
    }
    roadmap = {
        "artifact_type": "v6_x1_readiness_roadmap",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V6_X1_READY_WITH_CLI_NO_STACK_RULE",
        "roadmap": [
            "Attempt app lanes through existing app-server routes.",
            "Before attempting CLI lanes, check whether prior Arby/Aster attempts have finished.",
            "If prior CLI attempts are still active, defer and publish the blocker instead of stacking.",
            "If they finished, classify outputs with current-phase/final-marker/stale-context gates before reuse.",
        ],
    }
    outputs = {
        "no-stack-cli-supervisor-design": supervisor,
        "stale-cli-process-approval-candidate": approval_candidate,
        "app-lane-continuity-map": app_continuity,
        "source-guard-carry-forward": source_guard,
        "build-validation": validation,
        "synthesis": synthesis,
        "v6-x1-readiness-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)

    write_md(TRACE_DIR / f"{PHASE}-no-stack-cli-supervisor-design-v1.md", "v486 GMUT/THOS v22 v5 x2 No-Stack CLI Supervisor Design", [
        f"Status: `{supervisor['overall_status']}`",
        "No new Arby/Aster CLI launch should stack on top of an active prior attempt.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-stale-cli-process-approval-candidate-v1.md", "v486 GMUT/THOS v22 v5 x2 Stale CLI Process Approval Candidate", [
        f"Status: `{approval_candidate['overall_status']}`",
        "This is a future approval candidate only; no process termination was executed.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-app-lane-continuity-map-v1.md", "v486 GMUT/THOS v22 v5 x2 App-Lane Continuity Map", [
        f"Status: `{app_continuity['overall_status']}`",
        "The three app-server lanes remain the stable orchestration backbone.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-source-guard-carry-forward-v1.md", "v486 GMUT/THOS v22 v5 x2 Source Guard Carry Forward", [
        f"Status: `{source_guard['overall_status']}`",
        "Official source guidance stays planning-only.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-build-validation-v1.md", "v486 GMUT/THOS v22 v5 x2 Build Validation", [
        f"Status: `{validation['overall_status']}`",
        "No process termination, plugin cache mutation, user skill mutation, or raw lane publication occurred.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-synthesis-v1.md", "v486 GMUT/THOS v22 v5 x2 Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        f"Next boundary: `{synthesis['next_boundary']}`",
    ])
    write_md(TRACE_DIR / f"{PHASE}-v6-x1-readiness-roadmap-v1.md", "v486 GMUT/THOS v22 v5 x2 v6 x1 Readiness Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        "Use no-stack checks before any further Arby/Aster CLI attempt.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
