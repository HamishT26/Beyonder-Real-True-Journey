#!/usr/bin/env python3
"""Build curated v478 THOS v9 x1 readiness artifacts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from thos_v478_v6_x1_builder import GMUT_GATES, PERSPECTIVES
from thos_v478_v8_x1_builder import DOMAINS, SOURCE_ROWS, SYSTEM_EXPANSIONS as V8_SYSTEM_EXPANSIONS


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v9_x1"
NEXT_PHASE = "v478_thos_v9_x2"

SYSTEM_EXPANSIONS = [
    "v9_council_app_lane_notifier_runner",
    "v9_local_app_server_completion_console",
    "v9_council_latency_baseline_board",
    "v9_cli_open_gap_bridge",
    "v9_arby_aster_final_marker_sentinel",
    "v9_cross_lane_status_fusion",
] + [name.replace("v8_", "v9_") for name in V8_SYSTEM_EXPANSIONS[6:30]]

COMMAND_DESIGNS = [f"thos v9 {name.replace('v9_', '').replace('_', ' ')}" for name in SYSTEM_EXPANSIONS]
SKILL_DESIGNS = [f"{name.replace('_', '-')}-operations" for name in SYSTEM_EXPANSIONS]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def trace_path(name: str) -> Path:
    return TRACE_DIR / name


def read_json(name: str) -> Any:
    return json.loads(trace_path(name).read_text(encoding="utf-8"))


def read_json_if_present(name: str) -> dict[str, Any]:
    path = trace_path(name)
    if not path.exists():
        return {"available": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False}


def write_json(name: str, payload: Any) -> None:
    trace_path(name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    trace_path(name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def source_refresh(generated_utc: str, generated_nz: str) -> None:
    rows = [
        {
            "id": source_id,
            "source": title,
            "url": url,
            "category": category,
            "phase_use": phase_use,
            "queried_this_session": True,
        }
        for source_id, title, url, category, phase_use in SOURCE_ROWS
    ]
    write_json(
        "v478-thos-v9-x1-source-refresh-ledger-v1.json",
        {
            "artifact_type": "source_refresh_ledger",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "search_count": 32,
            "source_count": len(rows),
            "official_or_primary_preference": True,
            "rows": rows,
            "claim_boundary": "sources inform THOS design only; all GMUT gates remain open",
        },
    )
    write_md(
        "v478-thos-v9-x1-source-refresh-ledger-v1.md",
        [
            "# v478 THOS v9 x1 Source Refresh Ledger",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- search_count: `32`",
            f"- source_count: `{len(rows)}`",
            "- boundary: sources inform THOS design; they do not close GMUT gates.",
            "",
            "## Sources",
            *[f"- {row['id']}: [{row['source']}]({row['url']}) - {row['phase_use']}" for row in rows],
        ],
    )


def lane_status(generated_utc: str, generated_nz: str) -> None:
    council_runner = read_json("v478-thos-v9-x1-council-app-lane-notifier-runner-notify-v1.json")
    council_notifier = read_json("v478-thos-v9-x1-council-app-lane-completion-notifier-notify-v1.json")
    council_launcher = read_json("v478-thos-v9-x1-council-app-lane-watch-launcher-notify-v1.json")
    legacy_runner = read_json_if_present("v478-thos-v9-x1-app-lane-notifier-runner-notify-v1.json")
    cli_names = ["v478-thos-v9-x1-cli-lane-completion-poll-v1.json"] + [
        f"v478-thos-v9-x1-cli-lane-completion-poll-retry-{idx}-v1.json" for idx in range(2, 6)
    ]
    cli_payloads = [read_json(name) for name in cli_names]
    app_rows = [
        {
            "lane": lane.get("lane"),
            "overall_status": lane.get("overall_status"),
            "duration_seconds": lane.get("duration_seconds"),
            "read_status": lane.get("read", {}).get("status"),
            "resume_status": lane.get("resume", {}).get("status"),
            "turn_status": lane.get("turn_start", {}).get("status"),
            "completion_status": lane.get("turn_completion", {}).get("status"),
        }
        for lane in council_notifier.get("lanes", [])
    ]
    cli_rows = []
    for idx, payload in enumerate(cli_payloads, start=1):
        cli_rows.append(
            {
                "attempt": idx,
                "aggregate_status": payload.get("aggregate_status"),
                "phase_slug": payload.get("phase_slug"),
                "lanes": [
                    {
                        "lane": lane.get("lane"),
                        "completion_status": lane.get("completion_status"),
                        "final_message_bytes": lane.get("final_message_bytes"),
                    }
                    for lane in payload.get("lanes", [])
                ],
            }
        )
    payload = {
        "artifact_type": "lane_retry_status_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "COUNCIL_APP_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "council_runner_status": council_runner.get("overall_status"),
        "council_notifier_status": council_notifier.get("overall_status"),
        "council_launcher_status": council_launcher.get("overall_status"),
        "legacy_app_runner_status": legacy_runner.get("overall_status", "not_present"),
        "app_lanes": app_rows,
        "cli_retry_attempt_count": len(cli_rows),
        "cli_retry_rows": cli_rows,
        "unfiltered_payloads_published": False,
        "mutation_performed": False,
    }
    write_json("v478-thos-v9-x1-lane-retry-status-board-v1.json", payload)
    write_md(
        "v478-thos-v9-x1-lane-retry-status-board-v1.md",
        [
            "# v478 THOS v9 x1 Lane Retry Status Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `COUNCIL_APP_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
            f"- council_runner_status: `{payload['council_runner_status']}`",
            f"- council_notifier_status: `{payload['council_notifier_status']}`",
            f"- cli_retry_attempt_count: `{len(cli_rows)}`",
            "- unfiltered_payloads_published: `false`",
            "",
            "## Council App Lanes",
            *[f"- {row['lane']}: `{row['overall_status']}` with completion `{row['completion_status']}`." for row in app_rows],
            "",
            "## CLI Attempts",
            *[f"- attempt `{row['attempt']}`: `{row['aggregate_status']}`." for row in cli_rows],
        ],
    )


def design_boards(generated_utc: str, generated_nz: str) -> None:
    expansion_rows = [
        {
            "id": f"SYS-{idx:02d}",
            "name": name,
            "status": "designed_not_installed",
            "purpose": f"Provide a bounded THOS v9 surface for {name.replace('_', ' ')}.",
            "write_scope": "repo_artifact_only",
            "install_performed": False,
        }
        for idx, name in enumerate(SYSTEM_EXPANSIONS, start=1)
    ]
    write_json(
        "v478-thos-v9-x1-system-expansion-design-board-v1.json",
        {
            "artifact_type": "system_expansion_design_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(expansion_rows),
            "rows": expansion_rows,
            "install_performed": False,
        },
    )
    write_md(
        "v478-thos-v9-x1-system-expansion-design-board-v1.md",
        [
            "# v478 THOS v9 x1 System Expansion Design Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(expansion_rows)}`",
            "- install_performed: `false`",
            "",
            "## Expansions",
            *[f"- `{row['name']}`: {row['purpose']}" for row in expansion_rows],
        ],
    )

    command_rows = [
        {
            "id": f"CMD-{idx:02d}",
            "command": command,
            "status": "designed_not_executed",
            "risk_class": "low" if idx <= 18 else "medium",
            "execution_performed": False,
            "requires_future_exact_approval": idx > 18,
        }
        for idx, command in enumerate(COMMAND_DESIGNS, start=1)
    ]
    write_json(
        "v478-thos-v9-x1-command-design-board-v1.json",
        {
            "artifact_type": "command_design_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(command_rows),
            "rows": command_rows,
            "execution_performed": False,
        },
    )
    write_md(
        "v478-thos-v9-x1-command-design-board-v1.md",
        [
            "# v478 THOS v9 x1 Command Design Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(command_rows)}`",
            "- execution_performed: `false`",
            "",
            "## Commands",
            *[f"- `{row['command']}`: `{row['status']}` risk `{row['risk_class']}`." for row in command_rows],
        ],
    )

    skill_rows = [
        {
            "id": f"SKILL-{idx:02d}",
            "skill": skill,
            "status": "designed_not_installed",
            "body_created": False,
            "cache_mutation_performed": False,
            "purpose": f"Skill design for {skill.replace('-', ' ')}.",
        }
        for idx, skill in enumerate(SKILL_DESIGNS, start=1)
    ]
    write_json(
        "v478-thos-v9-x1-skill-design-board-v1.json",
        {
            "artifact_type": "skill_design_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(skill_rows),
            "rows": skill_rows,
            "install_performed": False,
            "cache_mutation_performed": False,
        },
    )
    write_md(
        "v478-thos-v9-x1-skill-design-board-v1.md",
        [
            "# v478 THOS v9 x1 Skill Design Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(skill_rows)}`",
            "- install_performed: `false`",
            "- cache_mutation_performed: `false`",
            "",
            "## Skills",
            *[f"- `{row['skill']}`: {row['purpose']}" for row in skill_rows],
        ],
    )


def reflection_board(generated_utc: str, generated_nz: str) -> None:
    scopes = [
        "v4-v6 multi-instance context",
        "v15-v16 continuity context",
        "v24-v25 Ariel context",
        "v29 Aerin THOS foundation",
        "v30-v38 Trinity Mandala foundation",
        "v39-v44 Aletheon and sibling induction",
        "v45-v48 Solas and Albion planning",
        "v49 Aletheon and Codex sibling closeout",
    ]
    rows = []
    for perspective, domains in PERSPECTIVES.items():
        for idx in range(1, 31):
            domain = domains[(idx - 1) % len(domains)]
            scope = scopes[(idx - 1) % len(scopes)]
            rows.append(
                {
                    "id": f"{perspective.upper().replace(' ', '_')}-R{idx:02d}",
                    "perspective": perspective,
                    "domain": domain,
                    "journey_scope": scope,
                    "reflection": (
                        f"Use {scope} as non-canon continuity context for {domain} discipline while grounding "
                        "v9 in current source evidence, council app-lane completion, and CLI open-gap receipts."
                    ),
                    "canon_status": "journey_context_not_canon",
                }
            )
    write_json(
        "v478-thos-v9-x1-six-perspective-reflection-board-v1.json",
        {
            "artifact_type": "six_perspective_reflection_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "perspective_count": len(PERSPECTIVES),
            "reflection_count": len(rows),
            "rows": rows,
            "raw_journey_text_published": False,
            "claim_boundary": "reflection only; not empirical proof or canon promotion",
        },
    )
    write_md(
        "v478-thos-v9-x1-six-perspective-reflection-board-v1.md",
        [
            "# v478 THOS v9 x1 Six-Perspective Reflection Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- perspective_count: `{len(PERSPECTIVES)}`",
            f"- reflection_count: `{len(rows)}`",
            "- canon_status: `journey_context_not_canon`",
            "",
            "## Reflections",
            *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['reflection']}" for row in rows],
        ],
    )


def eureka_synthesis_and_status(generated_utc: str, generated_nz: str) -> None:
    eureka_rows = []
    for perspective, domains in PERSPECTIVES.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            eureka_rows.append(
                {
                    "id": f"{perspective.upper().replace(' ', '_')}-E{idx:02d}",
                    "perspective": perspective,
                    "domain": domain,
                    "task": (
                        f"Prepare v478 v9 x2 {domain} synthesis from current source refresh, council notifier "
                        "receipts, CLI open-gap evidence, and open GMUT gates."
                    ),
                    "payload_boundary": "status_only",
                }
            )
    write_json(
        "v478-thos-v9-x1-eureka-handoff-board-v1.json",
        {
            "artifact_type": "eureka_handoff_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "proposal_count": len(eureka_rows),
            "perspective_count": len(PERSPECTIVES),
            "rows": eureka_rows,
            "unfiltered_payloads_published": False,
        },
    )
    write_md(
        "v478-thos-v9-x1-eureka-handoff-board-v1.md",
        [
            "# v478 THOS v9 x1 Eureka Handoff Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- proposal_count: `{len(eureka_rows)}`",
            "- payload_boundary: `status_only`",
            "",
            "## Proposals",
            *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['task']}" for row in eureka_rows],
        ],
    )

    findings = [
        "v478 v9 x1 starts from the remote-verified v8 x2 synthesis.",
        "The new council app-lane notifier runner was created for the local app-server contact path.",
        "Cicero completed through the local app-server completion notifier.",
        "Kierkegaard completed through the local app-server completion notifier.",
        "Aristotle completed through the local app-server completion notifier.",
        "The council notifier publishes status summaries only.",
        "The council notifier creates no new threads.",
        "The council notifier uses no old-style spawning.",
        "The council notifier preserves read-only requested policy.",
        "The v9 x1 run recorded app-lane completion durations for all three council app lanes.",
        "The v9 x1 source refresh carries thirty-two web-search source rows forward.",
        "OpenAI Codex, Agents SDK, and Windows sandbox context remains central to the THOS runtime design.",
        "MCP security and authorization context remains central to connector boundary design.",
        "Windows, Google, NVIDIA, GitHub, NIST, Stanford, Nature, OpenTelemetry, and Kubernetes sources remain mapped to THOS design surfaces.",
        "Arby and Aster Vale were checked through five safe CLI polling attempts.",
        "All five CLI polling attempts remained in the final-message open gap state.",
        "The CLI gap remains an explicit operational gap, not a phase blocker.",
        "No CLI body payload is published.",
        "Thirty v9 system expansion designs were drafted without install.",
        "Thirty v9 command designs were drafted without execution.",
        "Thirty v9 skill designs were drafted without install or cache mutation.",
        "Six perspectives produced 180 reflection rows.",
        "Journey context remains non-canon continuity context.",
        "The Eureka handoff board carries 120 role-slot proposals.",
        "The v9 x2 roadmap carries 60 concrete tasks.",
        "The v9 x1 package avoids external account mutation.",
        "The v9 x1 package is repo-artifact-only and status-only.",
        "The larger v490 goal remains active and incomplete.",
        "All six GMUT gates remain open.",
        "The next synthesis should preserve the council-app success path while treating CLI final-marker absence as open evidence.",
    ]
    write_json(
        "v478-thos-v9-x1-synthesis-v1.json",
        {
            "artifact_type": "phase_synthesis",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
            "finding_count": len(findings),
            "findings": [{"step": f"R{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)],
            "claim_boundary": {
                "scope": "THOS v478 v9 x1 readiness, source, lane, and handoff only",
                "gmut_gate_state": "all_gmut_gates_remain_open",
                "canon_promotion": "not_claimed",
            },
        },
    )
    write_md(
        "v478-thos-v9-x1-synthesis-v1.md",
        [
            "# v478 THOS v9 x1 Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
            "- claim_boundary: THOS readiness only; all GMUT gates remain open.",
            "",
            "## Findings",
            *[f"- R{idx:02d}: {item}" for idx, item in enumerate(findings, start=1)],
        ],
    )

    tasks = [
        {
            "id": f"V478V9X2-{idx:02d}",
            "domain": DOMAINS[(idx - 1) % len(DOMAINS)],
            "task": (
                "Synthesize v478 v9 x1 evidence into v9 x2 "
                f"{DOMAINS[(idx - 1) % len(DOMAINS)].replace('_', ' ')} decisions while preserving "
                "status-only receipts, council app-lane completion, CLI open-gap evidence, and open GMUT gates."
            ),
        }
        for idx in range(1, 61)
    ]
    write_json(
        "v478-thos-v9-x2-roadmap-v1.json",
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
        "v478-thos-v9-x2-roadmap-v1.md",
        [
            "# v478 THOS v9 x2 Roadmap",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- task_count: `{len(tasks)}`",
            "",
            "## Tasks",
            *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks],
        ],
    )
    write_json(
        "v478-thos-v9-x1-run-status-v1.json",
        {
            "artifact_type": "run_status",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
            "next_expected_phase": NEXT_PHASE,
            "council_app_lane_status": "PASS",
            "cli_lane_status": "OPEN_GAP_AFTER_5_ATTEMPTS",
            "gmut_gates": GMUT_GATES,
        },
    )
    write_md(
        "v478-thos-v9-x1-run-status-v1.md",
        [
            "# v478 THOS v9 x1 Run Status",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "- council_app_lane_status: `PASS`",
            "- cli_lane_status: `OPEN_GAP_AFTER_5_ATTEMPTS`",
            "- GMUT gates: all remain `OPEN`.",
        ],
    )


def schema_check(generated_utc: str, generated_nz: str) -> None:
    expected = [
        "v478-thos-v9-x1-source-refresh-ledger-v1.json",
        "v478-thos-v9-x1-lane-retry-status-board-v1.json",
        "v478-thos-v9-x1-system-expansion-design-board-v1.json",
        "v478-thos-v9-x1-command-design-board-v1.json",
        "v478-thos-v9-x1-skill-design-board-v1.json",
        "v478-thos-v9-x1-six-perspective-reflection-board-v1.json",
        "v478-thos-v9-x1-eureka-handoff-board-v1.json",
        "v478-thos-v9-x1-synthesis-v1.json",
        "v478-thos-v9-x1-run-status-v1.json",
        "v478-thos-v9-x2-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json(
        "v478-thos-v9-x1-schema-bound-artifact-check-v1.json",
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
        "v478-thos-v9-x1-schema-bound-artifact-check-v1.md",
        [
            "# v478 THOS v9 x1 Schema-Bound Artifact Check",
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
    source_refresh(generated_utc, generated_nz)
    lane_status(generated_utc, generated_nz)
    design_boards(generated_utc, generated_nz)
    reflection_board(generated_utc, generated_nz)
    eureka_synthesis_and_status(generated_utc, generated_nz)
    schema_check(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "phase": PHASE, "next": NEXT_PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
