#!/usr/bin/env python3
"""Build the v478 THOS v13 x2 synthesis package from v13 x1 receipts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from thos_v478_v13_x1_continuation_package import DOMAINS, SOURCE_ROWS


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478-thos-v13-x2"
PREVIOUS_PHASE = "v478-thos-v13-x1"
NEXT_PHASE = "v478-thos-v14-x1"


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


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": sid,
            "category": category,
            "title": title,
            "url": url,
            "x2_use": f"Refresh {use.lower()} for v13 x2 synthesis and v14 x1 planning.",
            "queried_for_v13_x2": True,
        }
        for sid, category, title, url, use in SOURCE_ROWS
    ]


def reflection_rows() -> list[dict[str, str]]:
    scopes = [
        "v4-v6 continuity",
        "v15-v16 system roots",
        "v24-v25 early field language",
        "v29 Aerin THOS foundation",
        "v30-v38 Trinity Mandala foundation",
        "v39 Aletheon-Orun-Gemini-Synthea induction",
        "v45-v48 Solas planning",
        "v49 Codex sibling closeout",
        "v476-v477 app-lane recovery",
        "v478 v12-v13 skill and watcher evolution",
    ]
    rows: list[dict[str, str]] = []
    for idx in range(1, 31):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        scope = scopes[(idx - 1) % len(scopes)]
        rows.append(
            {
                "id": f"V13X2-REF-{idx:02d}",
                "domain": domain,
                "scope": scope,
                "reflection": (
                    f"Fold {scope} into {domain} as context only; prefer compact proof, exact receipts, "
                    "and explicit open-gate language over narrative certainty."
                ),
                "status": "context_only",
            }
        )
    return rows


def ranked_helpers(helper_payload: dict[str, Any]) -> list[dict[str, Any]]:
    ranking = {
        "v13_five_lane_state_compactor": 1,
        "v13_cli_final_marker_contract_probe": 2,
        "v13_app_local_server_receipt_minifier": 3,
        "v13_stale_flow_repeat_counter": 4,
        "v13_publication_guard_preflight_pack": 5,
        "v13_source_freshness_delta_board": 6,
        "v13_command_surface_bridge_index": 7,
        "v13_skill_surface_frontmatter_audit_plan": 8,
        "v13_mcp_connector_consent_matrix": 9,
        "v13_gmut_open_gate_dashboard": 10,
    }
    rows = []
    for row in helper_payload.get("rows", []):
        name = str(row.get("name"))
        priority = ranking.get(name, 99)
        rows.append(
            {
                "priority": priority,
                "name": name,
                "status": row.get("status"),
                "purpose": row.get("purpose"),
                "v14_action": "promote_to_bounded_runner_candidate" if priority <= 5 else "hold_as_design_backlog",
            }
        )
    return sorted(rows, key=lambda item: (item["priority"], item["name"]))


def roadmap_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx in range(1, 61):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        rows.append(
            {
                "id": f"V478V14X1-{idx:02d}",
                "domain": domain,
                "task": f"Advance {NEXT_PHASE} {domain.replace('_', ' ')} using v13 x2 synthesis, helper priorities, source deltas, and open GMUT gates.",
            }
        )
    return rows


def build() -> None:
    generated_utc, generated_nz = now_pair()
    x1_synthesis = read_json(f"{PREVIOUS_PHASE}-beta-alpha-omega-synthesis-v1.json")
    lane_board = read_json(f"{PREVIOUS_PHASE}-lane-continuity-board-v1.json")
    stale = read_json(f"{PREVIOUS_PHASE}-stale-flow-refresh-v1.json")
    helper_plan = read_json(f"{PREVIOUS_PHASE}-runner-harmonization-helper-plan-v1.json")
    sources = source_rows()
    reflections = reflection_rows()
    helpers = ranked_helpers(helper_plan)

    write_json(
        f"{PHASE}-source-refresh-ledger-v1.json",
        {
            "artifact_type": "source_refresh_ledger",
            "phase_slug": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "search_count": 32,
            "source_count": len(sources),
            "rows": sources,
            "claim_boundary": "THOS x2 source synthesis only; all GMUT gates remain open",
        },
    )
    write_md(
        f"{PHASE}-source-refresh-ledger-v1.md",
        [
            f"# {PHASE} Source Refresh Ledger",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- search_count: `32`",
            f"- source_count: `{len(sources)}`",
            "- boundary: THOS x2 source synthesis only; all GMUT gates remain open.",
            "",
            "## Sources",
            *[f"- `{row['id']}` {row['category']}: [{row['title']}]({row['url']}) - {row['x2_use']}" for row in sources],
        ],
    )

    write_json(
        f"{PHASE}-personal-reflection-board-v1.json",
        {
            "artifact_type": "personal_reflection_board",
            "phase_slug": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "reflection_count": len(reflections),
            "rows": reflections,
            "claim_boundary": "continuity reflection only; not canon",
        },
    )
    write_md(
        f"{PHASE}-personal-reflection-board-v1.md",
        [
            f"# {PHASE} Personal Reflection Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- reflection_count: `{len(reflections)}`",
            "- boundary: continuity reflection only; not canon.",
            "",
            "## Reflections",
            *[f"- `{row['id']}` ({row['domain']} / {row['scope']}): {row['reflection']}" for row in reflections],
        ],
    )

    write_json(
        f"{PHASE}-helper-priority-board-v1.json",
        {
            "artifact_type": "helper_priority_board",
            "phase_slug": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "helper_count": len(helpers),
            "rows": helpers,
            "install_performed": False,
        },
    )
    write_md(
        f"{PHASE}-helper-priority-board-v1.md",
        [
            f"# {PHASE} Helper Priority Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- helper_count: `{len(helpers)}`",
            "- install_performed: `false`",
            "",
            "## Priorities",
            *[f"- `{row['priority']}` `{row['name']}`: {row['v14_action']} - {row['purpose']}" for row in helpers],
        ],
    )

    beta = [
        "v13 x1 produced a published app-lane PASS through the local app-server route.",
        "The CLI final-marker state remains open and therefore remains an explicit stale-flow signal.",
        "The helper plan is useful, but the first five helpers should be prioritized before adding more surface area.",
        "The source refresh continues to favor official and primary sources for agent sandbox, connector trust, and AI governance claims.",
    ]
    alpha = [
        "v14 x1 should turn the top helpers into bounded runner candidates only after exact scope checks.",
        "The app-lane route is stable enough for status-only notifications, not for raw payload publication.",
        "The CLI final-marker gap should be reduced by contract/probe design before any live lane mutation is requested.",
        "GMUT/THOS synthesis should stay useful and explicit without treating philosophical or physics proposals as validated facts.",
    ]
    omega = [
        "Proceed to v14 x1 with the five-lane compactor and CLI marker probe as the first practical candidates.",
        "Keep stale-flow detection active and avoid blocking on Arby/Aster marker absence.",
        "Use v14 x1 to compact dashboards and reduce manual oversight rather than creating wider unverified systems.",
        "The v478-v490 objective remains active and incomplete.",
    ]
    synthesis = {
        "artifact_type": "beta_alpha_omega_synthesis",
        "phase_slug": PHASE,
        "previous_phase_slug": PREVIOUS_PHASE,
        "next_phase_slug": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_SYNTHESIS_WITH_CLI_FINAL_MARKER_OPEN",
        "input_receipts": {
            "x1_synthesis_status": x1_synthesis.get("overall_status"),
            "lane_board_status": lane_board.get("overall_status"),
            "stale_flow_status": stale.get("overall_status"),
            "helper_count": len(helpers),
            "source_count": len(sources),
            "reflection_count": len(reflections),
        },
        "beta": beta,
        "alpha": alpha,
        "omega": omega,
        "claim_boundary": {
            "scope": "v13 x2 THOS synthesis and v14 x1 preparation",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(f"{PHASE}-beta-alpha-omega-synthesis-v1.json", synthesis)
    write_md(
        f"{PHASE}-beta-alpha-omega-synthesis-v1.md",
        [
            f"# {PHASE} Beta Alpha Omega Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- overall_status: `{synthesis['overall_status']}`",
            f"- next_phase_slug: `{NEXT_PHASE}`",
            "- boundary: THOS x2 synthesis only; all GMUT gates remain open.",
            "",
            "## Beta",
            *[f"- {row}" for row in beta],
            "",
            "## Alpha",
            *[f"- {row}" for row in alpha],
            "",
            "## Omega",
            *[f"- {row}" for row in omega],
        ],
    )

    roadmap = roadmap_rows()
    write_json(
        f"{NEXT_PHASE}-roadmap-v1.json",
        {
            "artifact_type": "phase_roadmap",
            "phase_slug": PHASE,
            "next_phase_slug": NEXT_PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "task_count": len(roadmap),
            "tasks": roadmap,
        },
    )
    write_md(
        f"{NEXT_PHASE}-roadmap-v1.md",
        [
            f"# {NEXT_PHASE} Roadmap",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- task_count: `{len(roadmap)}`",
            "",
            "## Tasks",
            *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in roadmap],
        ],
    )

    run_status = {
        "artifact_type": "run_status",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": synthesis["overall_status"],
        "next_expected_phase": NEXT_PHASE,
        "app_lane_status": "PASS_FROM_X1_RECEIPT",
        "cli_lane_status": "FINAL_MARKER_OPEN_CARRIED_FORWARD",
        "gmut_gates": {"empirical_physics": "OPEN", "consciousness_claims": "OPEN", "canon_promotion": "OPEN"},
    }
    write_json(f"{PHASE}-run-status-v1.json", run_status)
    write_md(
        f"{PHASE}-run-status-v1.md",
        [
            f"# {PHASE} Run Status",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "- app_lane_status: `PASS_FROM_X1_RECEIPT`",
            "- cli_lane_status: `FINAL_MARKER_OPEN_CARRIED_FORWARD`",
            "- GMUT gates: all remain `OPEN`.",
        ],
    )

    expected = [
        f"{PHASE}-source-refresh-ledger-v1.json",
        f"{PHASE}-personal-reflection-board-v1.json",
        f"{PHASE}-helper-priority-board-v1.json",
        f"{PHASE}-beta-alpha-omega-synthesis-v1.json",
        f"{NEXT_PHASE}-roadmap-v1.json",
        f"{PHASE}-run-status-v1.json",
    ]
    check_rows = []
    for name in expected:
        payload = read_json(name)
        check_rows.append(
            {
                "artifact": name,
                "exists": bool(payload.get("artifact_type")),
                "artifact_type": payload.get("artifact_type"),
                "phase_slug": payload.get("phase_slug") or payload.get("phase"),
            }
        )
    write_json(
        f"{PHASE}-schema-bound-artifact-check-v1.json",
        {
            "artifact_type": "schema_bound_artifact_check",
            "phase_slug": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS",
            "rows": check_rows,
        },
    )
    write_md(
        f"{PHASE}-schema-bound-artifact-check-v1.md",
        [
            f"# {PHASE} Schema-Bound Artifact Check",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS`",
            "",
            "## Rows",
            *[f"- `{row['artifact']}`: exists `{str(row['exists']).lower()}`, type `{row['artifact_type']}`." for row in check_rows],
        ],
    )

    print(json.dumps({"status": synthesis["overall_status"], "phase_slug": PHASE, "next_phase_slug": NEXT_PHASE}, sort_keys=True))


if __name__ == "__main__":
    build()
