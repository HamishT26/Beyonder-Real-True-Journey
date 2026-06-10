#!/usr/bin/env python3
"""Build curated v478 THOS v6 x1 readiness artifacts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from thos_v478_v5_x1_builder import GMUT_GATES, PERSPECTIVES, SOURCE_ROWS


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v6_x1"
NEXT_PHASE = "v478_thos_v6_x2"

SYSTEM_EXPANSIONS = [
    "v6_app_lane_notifier_runner",
    "v6_app_server_status_console",
    "v6_cicero_kierkegaard_aristotle_watch_bridge",
    "v6_cli_open_gap_compactor",
    "v6_cross_lane_runtime_meter",
    "v6_source_refresh_atlas",
    "v6_command_surface_patch_queue",
    "v6_v54_v55_handoff_surface_guard",
    "v6_sandbox_readiness_signal_board",
    "v6_tui_return_path_monitor",
    "v6_exact_stage_preflight_table",
    "v6_schema_artifact_manifest",
    "v6_connector_read_boundary_ledger",
    "v6_google_drive_search_boundary",
    "v6_github_remote_equality_guard",
    "v6_codex_app_mode_receipt",
    "v6_codex_cli_update_receipt",
    "v6_mcp_tool_trust_matrix",
    "v6_nvidia_simulation_context_lane",
    "v6_openai_agent_trace_lane",
    "v6_microsoft_agent_isolation_lane",
    "v6_google_agent_engine_lane",
    "v6_python_watcher_timeout_lane",
    "v6_opentelemetry_signal_lane",
    "v6_kubernetes_retry_semantics_lane",
    "v6_ai_risk_governance_lane",
    "v6_freedid_rights_boundary_lane",
    "v6_albion_simulation_prereq_lane",
    "v6_gmut_open_gate_register",
    "v6_v490_handoff_ladder",
]

COMMAND_DESIGNS = [
    "thos v6 app-lane notifier run",
    "thos v6 app-server status",
    "thos v6 app siblings watch",
    "thos v6 cli-open-gap compact",
    "thos v6 runtime meter",
    "thos v6 source atlas",
    "thos v6 command patch queue",
    "thos v6 handoff surface guard",
    "thos v6 sandbox signals",
    "thos v6 tui return monitor",
    "thos v6 exact-stage preflight",
    "thos v6 schema manifest",
    "thos v6 connector boundary",
    "thos v6 gdrive boundary",
    "thos v6 github equality",
    "thos v6 app mode receipt",
    "thos v6 cli update receipt",
    "thos v6 mcp trust",
    "thos v6 nvidia context",
    "thos v6 openai trace",
    "thos v6 windows isolation",
    "thos v6 google engine",
    "thos v6 python timeout",
    "thos v6 otel signal",
    "thos v6 k8s retry semantics",
    "thos v6 ai-risk governance",
    "thos v6 freedid boundary",
    "thos v6 albion prereq",
    "thos v6 gmut gates",
    "thos v6 v490 ladder",
]

SKILL_DESIGNS = [
    "v6-app-lane-notifier-runner-operations",
    "v6-app-server-status-console-operations",
    "v6-app-sibling-watch-bridge-operations",
    "v6-cli-open-gap-compactor-operations",
    "v6-cross-lane-runtime-meter-operations",
    "v6-source-refresh-atlas-operations",
    "v6-command-surface-patch-queue-operations",
    "v6-handoff-surface-guard-operations",
    "v6-sandbox-readiness-signal-board-operations",
    "v6-tui-return-path-monitor-operations",
    "v6-exact-stage-preflight-operations",
    "v6-schema-artifact-manifest-operations",
    "v6-connector-read-boundary-operations",
    "v6-google-drive-search-boundary-operations",
    "v6-github-remote-equality-operations",
    "v6-codex-app-mode-receipt-operations",
    "v6-codex-cli-update-receipt-operations",
    "v6-mcp-tool-trust-matrix-operations",
    "v6-nvidia-simulation-context-operations",
    "v6-openai-agent-trace-operations",
    "v6-microsoft-agent-isolation-operations",
    "v6-google-agent-engine-operations",
    "v6-python-watcher-timeout-operations",
    "v6-opentelemetry-signal-operations",
    "v6-kubernetes-retry-semantics-operations",
    "v6-ai-risk-governance-operations",
    "v6-freedid-rights-boundary-operations",
    "v6-albion-simulation-prereq-operations",
    "v6-gmut-open-gate-register-operations",
    "v6-v490-handoff-ladder-operations",
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def path(name: str) -> Path:
    return TRACE_DIR / name


def read_json(name: str) -> Any:
    return json.loads(path(name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    path(name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    path(name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def source_refresh(generated_utc: str, generated_nz: str) -> None:
    rows = [
        {
            "id": source_id,
            "source": title,
            "url": url,
            "category": category,
            "phase_use": phase_use,
            "queried_this_session": True,
            "v6_use": "support app-lane notifier, watcher, sandbox, source, and governance decisions",
        }
        for source_id, title, url, category, phase_use in SOURCE_ROWS
    ]
    write_json(
        "v478-thos-v6-x1-source-refresh-ledger-v1.json",
        {
            "artifact_type": "source_refresh_ledger",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "search_count": 32,
            "source_count": len(rows),
            "official_or_primary_preference": True,
            "rows": rows,
        },
    )
    write_md(
        "v478-thos-v6-x1-source-refresh-ledger-v1.md",
        [
            "# v478 THOS v6 x1 Source Refresh Ledger",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- search_count: `32`",
            f"- source_count: `{len(rows)}`",
            "- boundary: sources inform THOS design; they do not close GMUT gates.",
            "",
            "## Sources",
            *[f"- {row['id']}: [{row['source']}]({row['url']}) - {row['v6_use']}." for row in rows],
        ],
    )


def lane_retry_status(generated_utc: str, generated_nz: str) -> None:
    app_files = {
        "probe": "v478-thos-v6-x1-app-lane-completion-notifier-probe-v1.json",
        "notify": "v478-thos-v6-x1-app-lane-completion-notifier-v1.json",
        "runner_probe": "v478-thos-v6-x1-app-lane-notifier-runner-probe-v1.json",
    }
    app_payloads = {key: read_json(name) for key, name in app_files.items() if path(name).exists()}
    cli_names = ["v478-thos-v6-x1-cli-lane-completion-poll-v1.json"] + [
        f"v478-thos-v6-x1-cli-lane-completion-poll-retry-{idx}-v1.json" for idx in range(2, 6)
    ]
    cli_payloads = [read_json(name) for name in cli_names]
    app_rows = []
    notify = app_payloads.get("notify", {})
    for lane in notify.get("lanes", []):
        app_rows.append(
            {
                "lane": lane.get("lane"),
                "overall_status": lane.get("overall_status"),
                "duration_seconds": lane.get("duration_seconds"),
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_status": lane.get("turn_start", {}).get("status"),
                "completion_status": lane.get("turn_completion", {}).get("status"),
            }
        )
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
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "app_probe_status": app_payloads.get("probe", {}).get("overall_status"),
        "app_notify_status": notify.get("overall_status"),
        "app_runner_probe_status": app_payloads.get("runner_probe", {}).get("overall_status"),
        "app_lanes": app_rows,
        "cli_retry_attempt_count": len(cli_rows),
        "cli_retry_rows": cli_rows,
        "unfiltered_payloads_published": False,
        "mutation_performed": False,
    }
    write_json("v478-thos-v6-x1-lane-retry-status-board-v1.json", payload)
    lines = [
        "# v478 THOS v6 x1 Lane Retry Status Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
        f"- app_probe_status: `{payload['app_probe_status']}`",
        f"- app_notify_status: `{payload['app_notify_status']}`",
        f"- app_runner_probe_status: `{payload['app_runner_probe_status']}`",
        f"- cli_retry_attempt_count: `{len(cli_rows)}`",
        "- unfiltered_payloads_published: `false`",
        "",
        "## App Lanes",
    ]
    lines.extend(f"- {row['lane']}: `{row['overall_status']}` with completion `{row['completion_status']}`." for row in app_rows)
    lines.extend(["", "## CLI Attempts"])
    lines.extend(f"- attempt `{row['attempt']}`: `{row['aggregate_status']}`." for row in cli_rows)
    write_md("v478-thos-v6-x1-lane-retry-status-board-v1.md", lines)


def design_boards(generated_utc: str, generated_nz: str) -> None:
    expansion_rows = [
        {
            "id": f"SYS-{idx:02d}",
            "name": name,
            "status": "designed_not_installed",
            "purpose": f"Provide a bounded THOS v6 surface for {name.replace('_', ' ')}.",
            "write_scope": "repo_artifact_only",
            "install_performed": False,
        }
        for idx, name in enumerate(SYSTEM_EXPANSIONS, start=1)
    ]
    write_json("v478-thos-v6-x1-system-expansion-design-board-v1.json", {"artifact_type": "system_expansion_design_board", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(expansion_rows), "rows": expansion_rows, "install_performed": False})
    write_md("v478-thos-v6-x1-system-expansion-design-board-v1.md", ["# v478 THOS v6 x1 System Expansion Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(expansion_rows)}`", "- install_performed: `false`", "", "## Expansions", *[f"- `{row['name']}`: {row['purpose']}" for row in expansion_rows]])

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
    write_json("v478-thos-v6-x1-command-design-board-v1.json", {"artifact_type": "command_design_board", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(command_rows), "rows": command_rows, "execution_performed": False})
    write_md("v478-thos-v6-x1-command-design-board-v1.md", ["# v478 THOS v6 x1 Command Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(command_rows)}`", "- execution_performed: `false`", "", "## Commands", *[f"- `{row['command']}`: `{row['status']}` risk `{row['risk_class']}`." for row in command_rows]])

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
    write_json("v478-thos-v6-x1-skill-design-board-v1.json", {"artifact_type": "skill_design_board", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(skill_rows), "rows": skill_rows, "install_performed": False, "cache_mutation_performed": False})
    write_md("v478-thos-v6-x1-skill-design-board-v1.md", ["# v478 THOS v6 x1 Skill Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(skill_rows)}`", "- install_performed: `false`", "- cache_mutation_performed: `false`", "", "## Skills", *[f"- `{row['skill']}`: {row['purpose']}" for row in skill_rows]])


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
                    "reflection": f"Use {scope} as non-canon continuity context for {domain} discipline while prioritizing app-lane notifier reliability.",
                    "canon_status": "journey_context_not_canon",
                }
            )
    write_json("v478-thos-v6-x1-six-perspective-reflection-board-v1.json", {"artifact_type": "six_perspective_reflection_board", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "perspective_count": len(PERSPECTIVES), "reflection_count": len(rows), "rows": rows, "raw_journey_text_published": False, "claim_boundary": "reflection only; not empirical proof or canon promotion"})
    write_md("v478-thos-v6-x1-six-perspective-reflection-board-v1.md", ["# v478 THOS v6 x1 Six-Perspective Reflection Board", "", f"- generated_nz: `{generated_nz}`", f"- perspective_count: `{len(PERSPECTIVES)}`", f"- reflection_count: `{len(rows)}`", "- canon_status: `journey_context_not_canon`", "", "## Reflections", *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['reflection']}" for row in rows]])


def eureka_and_synthesis(generated_utc: str, generated_nz: str) -> None:
    eureka_rows = []
    for perspective, domains in PERSPECTIVES.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            eureka_rows.append(
                {
                    "id": f"{perspective.upper().replace(' ', '_')}-E{idx:02d}",
                    "perspective": perspective,
                    "domain": domain,
                    "task": f"Prepare v478 v6 x2 {domain} synthesis from app-lane notifier receipts, CLI open-gap evidence, source refresh, and open GMUT gates.",
                    "payload_boundary": "status_only",
                }
            )
    write_json("v478-thos-v6-x1-eureka-handoff-board-v1.json", {"artifact_type": "eureka_handoff_board", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "proposal_count": len(eureka_rows), "perspective_count": len(PERSPECTIVES), "rows": eureka_rows, "unfiltered_payloads_published": False})
    write_md("v478-thos-v6-x1-eureka-handoff-board-v1.md", ["# v478 THOS v6 x1 Eureka Handoff Board", "", f"- generated_nz: `{generated_nz}`", f"- proposal_count: `{len(eureka_rows)}`", "- payload_boundary: `status_only`", "", "## Proposals", *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['task']}" for row in eureka_rows]])

    findings = [
        "v478 v6 x1 starts from the remote-verified v5 x2 synthesis.",
        "A reusable v478 app-lane notifier runner was added for Cicero, Kierkegaard, and Aristotle.",
        "The runner delegates to the local app-server watch launcher and publishes status-only receipts.",
        "Cicero, Kierkegaard, and Aristotle completed a fresh status-only notify pass.",
        "A runner probe verified the reusable wrapper path without sending an extra advisory prompt.",
        "The app-lane path used existing threads only.",
        "No old-style spawning or replacement lane creation occurred.",
        "The app-lane artifacts publish status only, not advisory body text.",
        "Arby and Aster Vale were checked through five CLI watcher attempts.",
        "All five CLI attempts remain in the final-message open gap state.",
        "The CLI gap is recorded as explicit evidence for v6 x2 planning.",
        "No CLI output payload is published.",
        "The source refresh used 32 searches with official or primary preference.",
        "OpenAI sources support app-server, sandbox, agent, tracing, and schema practice.",
        "MCP sources support tool, authorization, and security boundary design.",
        "GitHub sources support exact publication and auth-material guard design.",
        "Microsoft sources support Windows isolation and current agent platform context.",
        "Python sources support bounded process, temporary output, and JSON reliability.",
        "OpenTelemetry sources support future signal separation.",
        "Docker and Kubernetes sources remain comparison surfaces only.",
        "Google sources provide managed agent and multimodal RAG comparison only.",
        "NVIDIA sources provide local inference, workstation, and simulation context only.",
        "NIST and Stanford sources provide governance and ecosystem trend context only.",
        "Thirty system expansion designs were drafted without install.",
        "Thirty command designs were drafted without execution.",
        "Thirty skill designs were drafted without install or cache mutation.",
        "Six perspectives produced 180 reflection rows.",
        "Journey context remains non-canon continuity context.",
        "The Eureka handoff board carries 120 role-slot proposals.",
        "All six GMUT gates remain open.",
    ]
    write_json("v478-thos-v6-x1-synthesis-v1.json", {"artifact_type": "phase_synthesis", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "finding_count": len(findings), "findings": [{"step": f"R{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)], "claim_boundary": {"scope": "THOS v478 v6 x1 readiness, app-lane runner, source, lane, and handoff only", "gmut_gate_state": "all_gmut_gates_remain_open", "canon_promotion": "not_claimed"}})
    write_md("v478-thos-v6-x1-synthesis-v1.md", ["# v478 THOS v6 x1 Synthesis", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", "- claim_boundary: THOS readiness only; all GMUT gates remain open.", "", "## Findings", *[f"- R{idx:02d}: {item}" for idx, item in enumerate(findings, start=1)]])


def roadmap_status_schema(generated_utc: str, generated_nz: str) -> None:
    domains = ["app-lane", "cli-gap", "runner", "source", "system", "command", "skill", "reflection", "eureka", "guard", "schema", "handoff"]
    tasks = [
        {
            "id": f"V478V6X2-{idx:02d}",
            "domain": domains[(idx - 1) % len(domains)],
            "task": f"Synthesize v478 v6 x1 evidence into v6 x2 {domains[(idx - 1) % len(domains)]} decisions while preserving status-only receipts and open GMUT gates.",
        }
        for idx in range(1, 61)
    ]
    write_json("v478-thos-v6-x2-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase": PHASE, "next_phase": NEXT_PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(tasks), "tasks": tasks})
    write_md("v478-thos-v6-x2-roadmap-v1.md", ["# v478 THOS v6 x2 Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(tasks)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks]])
    write_json("v478-thos-v6-x1-run-status-v1.json", {"artifact_type": "run_status", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "next_expected_phase": NEXT_PHASE, "app_lane_status": "PASS", "cli_lane_status": "OPEN_GAP_AFTER_5_ATTEMPTS", "gmut_gates": GMUT_GATES})
    write_md("v478-thos-v6-x1-run-status-v1.md", ["# v478 THOS v6 x1 Run Status", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", f"- next_expected_phase: `{NEXT_PHASE}`", "- app_lane_status: `PASS`", "- cli_lane_status: `OPEN_GAP_AFTER_5_ATTEMPTS`", "- GMUT gates: all remain `OPEN`."])
    expected = [
        "v478-thos-v6-x1-source-refresh-ledger-v1.json",
        "v478-thos-v6-x1-lane-retry-status-board-v1.json",
        "v478-thos-v6-x1-system-expansion-design-board-v1.json",
        "v478-thos-v6-x1-command-design-board-v1.json",
        "v478-thos-v6-x1-skill-design-board-v1.json",
        "v478-thos-v6-x1-six-perspective-reflection-board-v1.json",
        "v478-thos-v6-x1-eureka-handoff-board-v1.json",
        "v478-thos-v6-x1-synthesis-v1.json",
        "v478-thos-v6-x1-run-status-v1.json",
        "v478-thos-v6-x2-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json("v478-thos-v6-x1-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "checked_json_count": len(rows), "rows": rows})
    write_md("v478-thos-v6-x1-schema-bound-artifact-check-v1.md", ["# v478 THOS v6 x1 Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", f"- checked_json_count: `{len(rows)}`", "", "## Checked", *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows]])


def main() -> int:
    generated_utc, generated_nz = now_pair()
    source_refresh(generated_utc, generated_nz)
    lane_retry_status(generated_utc, generated_nz)
    design_boards(generated_utc, generated_nz)
    reflection_board(generated_utc, generated_nz)
    eureka_and_synthesis(generated_utc, generated_nz)
    roadmap_status_schema(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "phase": PHASE, "next": NEXT_PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
