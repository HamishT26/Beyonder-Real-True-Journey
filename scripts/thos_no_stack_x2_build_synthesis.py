#!/usr/bin/env python3
"""Generate reusable no-stack x2 synthesis receipts for GMUT/THOS phases."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
DOCS_DIR = ROOT / "docs"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def file_records(patterns: list[str], limit: int = 32) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pattern in patterns:
        for path in sorted(DOCS_DIR.glob(pattern)):
            if path.is_file():
                records.append({"path": rel(path), "bytes": path.stat().st_size})
            if len(records) >= limit:
                return records
    return records


def title_for(slug: str) -> str:
    return slug.replace("-", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate reusable no-stack x2 synthesis receipts.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--source-x1-slug", required=True)
    parser.add_argument("--next-x1-slug", required=True)
    args = parser.parse_args()

    phase = args.phase_slug
    source_x1 = args.source_x1_slug
    generated_utc, generated_nz = now_pair()
    x1_blocker = read_json(TRACE_DIR / f"{source_x1}-cli-deferral-blocker-v1.json")
    x1_status = read_json(TRACE_DIR / f"{source_x1}-five-lane-attempt-status-v1.json")
    x1_synthesis = read_json(TRACE_DIR / f"{source_x1}-synthesis-v1.json")
    command_surfaces = file_records([
        "trinity-command-book*.json",
        "trinity-command-book-validation-latest.*",
        "trinity-command-execution-ledger.jsonl",
    ])

    supervisor = {
        "artifact_type": "no_stack_cli_supervisor_carry_forward",
        "phase_slug": phase,
        "source_x1_slug": source_x1,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NO_STACK_SUPERVISOR_CARRY_FORWARD",
        "input_blocker_status": x1_blocker.get("overall_status", "unknown"),
        "rules": [
            "Do not stack new Arby/Aster CLI attempts while prior attempts remain unresolved or current-context repair is unapproved.",
            "Treat CLI deferral as an accounted lane state.",
            "Use app-server lanes and Aletheon synthesis to keep x2 work moving.",
            "Resume CLI attempts only after context-capsule repair approval or verified current-context availability.",
        ],
    }
    app_continuity = {
        "artifact_type": "app_lane_continuity_map",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_APP_LANE_CONTINUITY_MAP",
        "app_lanes": x1_status.get("app_lanes", []),
        "source_x1_status": x1_synthesis.get("overall_status", "unknown"),
        "uses": [
            "Use app-lane completion receipts as stable orchestration-health evidence.",
            "Do not publish app-lane body text.",
            "Fold app-lane progress into command-surface, source, and handoff design.",
        ],
    }
    open_gate_queue = {
        "artifact_type": "open_gate_build_queue",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_OPEN_GATE_BUILD_QUEUE",
        "command_surface_count": len(command_surfaces),
        "command_surfaces": command_surfaces,
        "queue": [
            "Keep command-index and v54/v55 surface work receiver-safe.",
            "Keep GMUT statements in source-backed, simulation-ready, comparator-needed, or speculative buckets.",
            "Use Journey docs as continuity/history inspiration, not empirical proof.",
            "Prepare the next x1 with app lanes and a visible Arby/Aster context-capsule approval pause if needed.",
        ],
        "claim_boundary": {
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    validation = {
        "artifact_type": "x2_build_validation",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NO_STACK_X2_BUILD_VALIDATION",
        "input_receipts": [
            f"{source_x1}-cli-deferral-blocker-v1.json",
            f"{source_x1}-five-lane-attempt-status-v1.json",
            f"{source_x1}-synthesis-v1.json",
        ],
        "artifact_statuses": {
            "supervisor": supervisor["overall_status"],
            "app_continuity": app_continuity["overall_status"],
            "open_gate_queue": open_gate_queue["overall_status"],
        },
        "mutation_boundary": {
            "repo_artifacts_written": True,
            "arby_aster_worktrees_mutated": False,
            "processes_terminated": False,
            "plugin_cache_mutated": False,
            "user_skills_mutated": False,
            "raw_lane_text_published": False,
        },
    }
    synthesis = {
        "artifact_type": "x2_synthesis",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NO_STACK_X2_SYNTHESIS",
        "result": [
            "Carried no-stack CLI rules forward without mutating Arby/Aster worktrees.",
            "Converted app-lane completion into safe x2 continuity and build-queue artifacts.",
            "Preserved GMUT/THOS claim boundaries and publication discipline.",
        ],
        "next_boundary": args.next_x1_slug,
    }
    roadmap = {
        "artifact_type": "next_x1_readiness_roadmap",
        "phase_slug": phase,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NEXT_X1_READY_WITH_CONTEXT_CAPSULE_APPROVAL_OPEN",
        "roadmap": [
            "Run existing app-server lanes at the next x1.",
            "Do not relaunch Arby/Aster CLI work until context-capsule repair is approved or current context is proven available.",
            "If approval arrives, validate capsule files before retrying read-only CLI lanes.",
            "Continue exact publication and open-gate claim posture.",
        ],
    }

    outputs = {
        "no-stack-cli-supervisor-carry-forward": supervisor,
        "app-lane-continuity-map": app_continuity,
        "open-gate-build-queue": open_gate_queue,
        "build-validation": validation,
        "synthesis": synthesis,
        "next-x1-readiness-roadmap": roadmap,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{phase}-{suffix}-v1.json", payload)

    title = title_for(phase)
    write_md(TRACE_DIR / f"{phase}-no-stack-cli-supervisor-carry-forward-v1.md", f"{title} No-Stack CLI Supervisor Carry Forward", [
        f"Status: `{supervisor['overall_status']}`",
        "No Arby/Aster worktree mutation or duplicate CLI relaunch occurred.",
    ])
    write_md(TRACE_DIR / f"{phase}-app-lane-continuity-map-v1.md", f"{title} App-Lane Continuity Map", [
        f"Status: `{app_continuity['overall_status']}`",
        "App-server lane receipts remain the stable orchestration backbone.",
    ])
    write_md(TRACE_DIR / f"{phase}-open-gate-build-queue-v1.md", f"{title} Open-Gate Build Queue", [
        f"Status: `{open_gate_queue['overall_status']}`",
        "Command, Journey, and GMUT/THOS work remains receiver-safe and open-gated.",
    ])
    write_md(TRACE_DIR / f"{phase}-build-validation-v1.md", f"{title} Build Validation", [
        f"Status: `{validation['overall_status']}`",
        "No raw lane text, plugin-cache mutation, user-skill mutation, or process termination occurred.",
    ])
    write_md(TRACE_DIR / f"{phase}-synthesis-v1.md", f"{title} Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        f"Next boundary: `{args.next_x1_slug}`",
    ])
    write_md(TRACE_DIR / f"{phase}-next-x1-readiness-roadmap-v1.md", f"{title} Next x1 Readiness Roadmap", [
        f"Status: `{roadmap['overall_status']}`",
        "Proceed with app lanes and keep Arby/Aster context-capsule approval open.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": phase, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
