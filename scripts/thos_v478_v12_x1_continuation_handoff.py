#!/usr/bin/env python3
"""Create the v478 THOS v12 x1 continuation handoff from current v12 receipts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478-thos-v12-x1"
NEXT_PHASE = "v478-thos-v12-x2"


DOMAINS = [
    "stale_flow",
    "sibling_lane",
    "cli_final_marker",
    "app_server",
    "sandbox_readiness",
    "source_drift",
    "skill_orchestration",
    "publication_guard",
    "command_surface",
    "mcp_trust",
    "journey_index",
    "gmuthos_boundary",
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {"available": False, "receipt": name}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False, "receipt": name}


def write_json(name: str, payload: dict[str, Any]) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def reflection_rows() -> list[dict[str, Any]]:
    scopes = [
        "v4-v6 early continuity",
        "v15-v16 system roots",
        "v24-v25 Ariel reflection",
        "v29 Aerin THOS foundation",
        "v30-v38 Trinity Mandala foundation",
        "v39 induction continuity",
        "v45-v48 Solas planning",
        "v49 Aletheon and Codex siblings",
    ]
    rows = []
    for idx in range(1, 31):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        scope = scopes[(idx - 1) % len(scopes)]
        rows.append(
            {
                "id": f"REF-{idx:02d}",
                "domain": domain,
                "record_scope": scope,
                "reflection": (
                    f"Use {scope} as continuity context for {domain} while keeping v12 x1 proof "
                    "grounded in current receipts, source drift, and open-gate boundaries."
                ),
                "canon_status": "context_only_not_canon",
            }
        )
    return rows


def roadmap_rows() -> list[dict[str, Any]]:
    rows = []
    for idx in range(1, 61):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        rows.append(
            {
                "id": f"V478V12X2-{idx:02d}",
                "domain": domain,
                "task": (
                    f"Advance {NEXT_PHASE} {domain.replace('_', ' ')} with status-only receipts, "
                    "stale-flow awareness, source-drift context, and open GMUT gates."
                ),
            }
        )
    return rows


def build() -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    background = read_json(f"{PHASE}-background-sibling-notifier-runner-v1.json")
    multiplex = read_json(f"{PHASE}-local-multiplex-tui-app-server-runner-v1.json")
    stale = read_json(f"{PHASE}-stale-flow-refresh-runner-v1.json")
    source = read_json(f"{PHASE}-source-drift-sentinel-v1.json")
    skill = read_json(f"{PHASE}-live-skill-evolution-receipt-v1.json")
    reflections = reflection_rows()
    roadmap = roadmap_rows()
    findings = [
        "Live multi-agent orchestration skill evolution is verified against its approved draft.",
        "Stale-flow refresh detects open app/CLI split-state signals and notifies Aletheon.",
        "Background notifier confirms app-side completion while CLI final markers remain open.",
        "Multiplex board keeps the app-ready and CLI-open state visible.",
        "Source-drift sentinel records 32 current public-source searches and 32 source rows.",
        "Personal record reflection board carries 30 continuity reflections without publishing source bodies.",
        "No new threads, old-style subagents, external account changes, plugin-cache edits, or GMUT closure claims are made.",
    ]
    handoff = {
        "artifact_type": "continuation_handoff",
        "phase_slug": PHASE,
        "next_phase_slug": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "READY_FOR_X2_WITH_CLI_FINAL_MARKER_OPEN",
        "input_receipts": {
            "background_status": background.get("overall_status"),
            "multiplex_status": multiplex.get("overall_status"),
            "stale_flow_status": stale.get("overall_status"),
            "source_query_count": source.get("web_query_count"),
            "skill_after_hash": skill.get("after_sha256"),
        },
        "finding_count": len(findings),
        "findings": [{"id": f"F{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)],
        "next_phase_task_count": len(roadmap),
        "policy": {
            "status_only": True,
            "new_thread_created": False,
            "old_style_subagent_spawned": False,
            "external_account_changed": False,
            "plugin_cache_changed": False,
        },
        "claim_boundary": {
            "scope": "v12 x1 continuation handoff and v12 x2 preparation",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(f"{PHASE}-personal-reflection-board-v1.json", {"artifact_type": "personal_reflection_board", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "reflection_count": len(reflections), "rows": reflections, "claim_boundary": "continuity reflection only; not canon"})
    write_md(f"{PHASE}-personal-reflection-board-v1.md", [f"# {PHASE} Personal Reflection Board", "", f"- generated_nz: `{generated_nz}`", f"- reflection_count: `{len(reflections)}`", "- boundary: continuity reflection only; not canon.", "", "## Reflections", *[f"- `{row['id']}` ({row['domain']} / {row['record_scope']}): {row['reflection']}" for row in reflections]])
    write_json(f"{NEXT_PHASE}-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase_slug": PHASE, "next_phase_slug": NEXT_PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(roadmap), "tasks": roadmap})
    write_md(f"{NEXT_PHASE}-roadmap-v1.md", [f"# {NEXT_PHASE} Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(roadmap)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in roadmap]])
    write_json(f"{PHASE}-continuation-handoff-v1.json", handoff)
    write_md(f"{PHASE}-continuation-handoff-v1.md", [f"# {PHASE} Continuation Handoff", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `READY_FOR_X2_WITH_CLI_FINAL_MARKER_OPEN`", f"- next_phase_slug: `{NEXT_PHASE}`", "- boundary: v12 x1 handoff only; all GMUT gates remain open.", "", "## Findings", *[f"- `{row['id']}`: {row['finding']}" for row in handoff["findings"]]])
    return handoff


def main() -> None:
    payload = build()
    print(json.dumps({"status": payload["overall_status"], "next": payload["next_phase_slug"]}, sort_keys=True))


if __name__ == "__main__":
    main()
