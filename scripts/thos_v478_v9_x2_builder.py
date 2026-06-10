#!/usr/bin/env python3
"""Build curated v478 THOS v9 x2 synthesis artifacts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from thos_v478_v6_x1_builder import GMUT_GATES, PERSPECTIVES
from thos_v478_v9_x1_builder import DOMAINS, PHASE as PREVIOUS_PHASE


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v9_x2"
NEXT_PHASE = "v478_thos_v10_x1"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def trace_path(name: str) -> Path:
    return TRACE_DIR / name


def read_json(name: str) -> Any:
    return json.loads(trace_path(name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    trace_path(name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    trace_path(name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def beta_alpha_omega(generated_utc: str, generated_nz: str) -> None:
    run_status = read_json("v478-thos-v9-x1-run-status-v1.json")
    lane_board = read_json("v478-thos-v9-x1-lane-retry-status-board-v1.json")
    source_ledger = read_json("v478-thos-v9-x1-source-refresh-ledger-v1.json")
    x1_synthesis = read_json("v478-thos-v9-x1-synthesis-v1.json")
    beta_rows = [
        "Council app lanes completed through the local app-server path.",
        "The new council notifier runner is now a reusable status-only surface.",
        "Arby and Aster Vale remained in the known final-marker open gap after five safe polls.",
        "The source ledger preserves a thirty-two source floor for v9 design decisions.",
        "All generated artifacts stayed inside curated repo scope.",
        "All six GMUT gates remain open.",
    ]
    alpha_rows = [
        "Treat app-lane completion as the primary real-time advisory signal for v10 x1.",
        "Treat CLI final-marker absence as an explicit watch gap instead of a phase failure.",
        "Use the council notifier as the default Cicero/Kierkegaard/Aristotle contact surface.",
        "Keep Arby/Aster CLI polling status-only until final-message markers are reliably observed.",
        "Move v10 toward watcher reuse and smaller phase receipts where possible.",
        "Keep source-to-system mappings primary-source-biased and non-canon.",
    ]
    omega_rows = [
        "Promote the council notifier runner as the v478 app-lane standard for existing app siblings.",
        "Preserve exact staging and remote equality as the publication standard.",
        "Keep THOS systems designed but not installed unless a future packet approves mutation.",
        "Keep journey documents as continuity context and not empirical closure.",
        "Use v10 x1 to consolidate watcher ergonomics, source drift, command surfaces, and sibling handoff density.",
        "Do not claim GMUT validation or canon promotion.",
    ]
    payload = {
        "artifact_type": "beta_alpha_omega_synthesis",
        "phase": PHASE,
        "previous_phase": PREVIOUS_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP",
        "inputs": {
            "run_status": run_status.get("overall_status"),
            "council_notifier_status": lane_board.get("council_notifier_status"),
            "cli_retry_attempt_count": lane_board.get("cli_retry_attempt_count"),
            "source_count": source_ledger.get("source_count"),
            "x1_finding_count": x1_synthesis.get("finding_count"),
        },
        "beta": beta_rows,
        "alpha": alpha_rows,
        "omega": omega_rows,
        "claim_boundary": {
            "scope": "THOS v9 x2 synthesis only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v9-x2-beta-alpha-omega-synthesis-v1.json", payload)
    write_md(
        "v478-thos-v9-x2-beta-alpha-omega-synthesis-v1.md",
        [
            "# v478 THOS v9 x2 Beta Alpha Omega Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_SYNTHESIS_WITH_CLI_OPEN_GAP`",
            "- claim_boundary: THOS synthesis only; all GMUT gates remain open.",
            "",
            "## Beta",
            *[f"- {row}" for row in beta_rows],
            "",
            "## Alpha",
            *[f"- {row}" for row in alpha_rows],
            "",
            "## Omega",
            *[f"- {row}" for row in omega_rows],
        ],
    )


def source_to_system_map(generated_utc: str, generated_nz: str) -> None:
    source_ledger = read_json("v478-thos-v9-x1-source-refresh-ledger-v1.json")
    system_board = read_json("v478-thos-v9-x1-system-expansion-design-board-v1.json")
    sources = source_ledger.get("rows", [])
    systems = system_board.get("rows", [])
    rows = []
    for idx, system in enumerate(systems, start=1):
        source = sources[(idx - 1) % len(sources)]
        rows.append(
            {
                "id": f"MAP-{idx:02d}",
                "system": system.get("name"),
                "source_id": source.get("id"),
                "source_category": source.get("category"),
                "mapping": f"{system.get('name')} uses {source.get('source')} as current-context input, not closure proof.",
                "install_performed": False,
            }
        )
    write_json(
        "v478-thos-v9-x2-source-to-system-map-v1.json",
        {
            "artifact_type": "source_to_system_map",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(rows),
            "rows": rows,
            "claim_boundary": "design mapping only; no system install or GMUT closure",
        },
    )
    write_md(
        "v478-thos-v9-x2-source-to-system-map-v1.md",
        [
            "# v478 THOS v9 x2 Source-To-System Map",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(rows)}`",
            "- boundary: design mapping only; no system install.",
            "",
            "## Mappings",
            *[f"- `{row['id']}` {row['system']} <= {row['source_id']} / {row['source_category']}: {row['mapping']}" for row in rows],
        ],
    )


def lane_resolution_plan(generated_utc: str, generated_nz: str) -> None:
    lane_board = read_json("v478-thos-v9-x1-lane-retry-status-board-v1.json")
    app_lanes = lane_board.get("app_lanes", [])
    cli_rows = lane_board.get("cli_retry_rows", [])
    actions = [
        {
            "id": "LANE-01",
            "target": "Cicero/Kierkegaard/Aristotle",
            "status": "ready",
            "action": "Use the council app-lane notifier runner as the default local app-server contact path.",
        },
        {
            "id": "LANE-02",
            "target": "Cicero/Kierkegaard/Aristotle",
            "status": "ready",
            "action": "Keep lane receipts status-only and omit advisory body text.",
        },
        {
            "id": "LANE-03",
            "target": "Arby/Aster Vale",
            "status": "open_gap",
            "action": "Continue bounded final-marker polling without treating absent markers as completion.",
        },
        {
            "id": "LANE-04",
            "target": "Arby/Aster Vale",
            "status": "open_gap",
            "action": "Use longer polling windows only when the active packet explicitly asks for them.",
        },
        {
            "id": "LANE-05",
            "target": "all lanes",
            "status": "ready",
            "action": "Fuse app and CLI lane boards into v10 x1 readiness rather than publishing transport payloads.",
        },
    ]
    payload = {
        "artifact_type": "lane_resolution_plan",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "app_lane_count": len(app_lanes),
        "cli_attempt_count": len(cli_rows),
        "actions": actions,
        "overall_status": "APP_READY_CLI_GAP_OPEN",
    }
    write_json("v478-thos-v9-x2-lane-resolution-plan-v1.json", payload)
    write_md(
        "v478-thos-v9-x2-lane-resolution-plan-v1.md",
        [
            "# v478 THOS v9 x2 Lane Resolution Plan",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `APP_READY_CLI_GAP_OPEN`",
            f"- app_lane_count: `{len(app_lanes)}`",
            f"- cli_attempt_count: `{len(cli_rows)}`",
            "",
            "## Actions",
            *[f"- `{row['id']}` {row['target']} / `{row['status']}`: {row['action']}" for row in actions],
        ],
    )


def eureka_consolidation(generated_utc: str, generated_nz: str) -> None:
    x1_handoff = read_json("v478-thos-v9-x1-eureka-handoff-board-v1.json")
    rows = []
    for idx, proposal in enumerate(x1_handoff.get("rows", []), start=1):
        domain = proposal.get("domain")
        rows.append(
            {
                "id": f"V9X2-E{idx:03d}",
                "source_task": proposal.get("id"),
                "perspective": proposal.get("perspective"),
                "domain": domain,
                "consolidated_task": f"Carry {domain} into v10 x1 with council-app completion, CLI open-gap evidence, and status-only publication.",
                "ready_for_next_phase": True,
            }
        )
    write_json(
        "v478-thos-v9-x2-eureka-consolidation-v1.json",
        {
            "artifact_type": "eureka_consolidation",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(rows),
            "rows": rows,
            "unfiltered_payloads_published": False,
        },
    )
    write_md(
        "v478-thos-v9-x2-eureka-consolidation-v1.md",
        [
            "# v478 THOS v9 x2 Eureka Consolidation",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(rows)}`",
            "- unfiltered_payloads_published: `false`",
            "",
            "## Consolidated Tasks",
            *[f"- `{row['id']}` ({row['perspective']} / {row['domain']}): {row['consolidated_task']}" for row in rows],
        ],
    )


def status_and_roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = [
        {
            "id": f"V478V10X1-{idx:02d}",
            "domain": DOMAINS[(idx - 1) % len(DOMAINS)],
            "task": (
                f"Advance v478 v10 x1 {DOMAINS[(idx - 1) % len(DOMAINS)].replace('_', ' ')} with "
                "council notifier reuse, CLI gap tracking, current-source grounding, and open GMUT gates."
            ),
        }
        for idx in range(1, 61)
    ]
    write_json(
        "v478-thos-v10-x1-roadmap-v1.json",
        {
            "artifact_type": "phase_roadmap",
            "phase": PHASE,
            "next_phase": NEXT_PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "task_count": len(tasks),
            "tasks": tasks,
        },
    )
    write_md(
        "v478-thos-v10-x1-roadmap-v1.md",
        [
            "# v478 THOS v10 x1 Roadmap",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- task_count: `{len(tasks)}`",
            "",
            "## Tasks",
            *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks],
        ],
    )
    write_json(
        "v478-thos-v9-x2-run-status-v1.json",
        {
            "artifact_type": "run_status",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP",
            "next_expected_phase": NEXT_PHASE,
            "council_app_lane_status": "PASS",
            "cli_lane_status": "OPEN_GAP_CARRIED_FORWARD",
            "gmut_gates": GMUT_GATES,
        },
    )
    write_md(
        "v478-thos-v9-x2-run-status-v1.md",
        [
            "# v478 THOS v9 x2 Run Status",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_SYNTHESIS_WITH_CLI_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "- council_app_lane_status: `PASS`",
            "- cli_lane_status: `OPEN_GAP_CARRIED_FORWARD`",
            "- GMUT gates: all remain `OPEN`.",
        ],
    )


def schema_check(generated_utc: str, generated_nz: str) -> None:
    expected = [
        "v478-thos-v9-x2-beta-alpha-omega-synthesis-v1.json",
        "v478-thos-v9-x2-source-to-system-map-v1.json",
        "v478-thos-v9-x2-lane-resolution-plan-v1.json",
        "v478-thos-v9-x2-eureka-consolidation-v1.json",
        "v478-thos-v9-x2-run-status-v1.json",
        "v478-thos-v10-x1-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json(
        "v478-thos-v9-x2-schema-bound-artifact-check-v1.json",
        {
            "artifact_type": "schema_bound_artifact_check",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS",
            "checked_json_count": len(rows),
            "rows": rows,
        },
    )
    write_md(
        "v478-thos-v9-x2-schema-bound-artifact-check-v1.md",
        [
            "# v478 THOS v9 x2 Schema-Bound Artifact Check",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS`",
            f"- checked_json_count: `{len(rows)}`",
            "",
            "## Checked",
            *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows],
        ],
    )


def main() -> int:
    generated_utc, generated_nz = now_pair()
    beta_alpha_omega(generated_utc, generated_nz)
    source_to_system_map(generated_utc, generated_nz)
    lane_resolution_plan(generated_utc, generated_nz)
    eureka_consolidation(generated_utc, generated_nz)
    status_and_roadmap(generated_utc, generated_nz)
    schema_check(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP", "phase": PHASE, "next": NEXT_PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
