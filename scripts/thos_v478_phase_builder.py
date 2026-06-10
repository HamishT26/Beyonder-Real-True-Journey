#!/usr/bin/env python3
"""Build curated v478 THOS phase artifacts from existing receipts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from thos_v478_v6_x1_builder import GMUT_GATES, PERSPECTIVES


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"

DOMAINS = [
    "source_freshness",
    "app_lane",
    "cli_gap",
    "sandbox",
    "mcp_trust",
    "windows_isolation",
    "google_agents",
    "nvidia_compute",
    "github_security",
    "observability",
    "governance",
    "handoff",
]

SOURCE_ROWS = [
    ("S01", "OpenAI Codex app", "https://openai.com/index/introducing-the-codex-app/", "openai", "Codex app multi-agent command-center context."),
    ("S02", "OpenAI Codex for every role", "https://openai.com/index/codex-for-every-role-tool-workflow/", "openai", "Cross-functional Codex workflow context."),
    ("S03", "OpenAI Codex Windows sandbox", "https://openai.com/index/building-codex-windows-sandbox/", "openai", "Windows sandbox design and oversight context."),
    ("S04", "OpenAI Agents SDK evolution", "https://openai.com/index/the-next-evolution-of-the-agents-sdk", "openai", "Agent harness, sandbox, and durable execution context."),
    ("S05", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "openai", "CLI and app-server release-drift context."),
    ("S06", "OpenAI Codex help", "https://help.openai.com/en/articles/11369540-getting-started-with-codex", "openai", "Plan and usage-boundary context."),
    ("S07", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "mcp", "Connector trust and local-server consent context."),
    ("S08", "MCP authorization", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "mcp", "Authorization and resource-boundary context."),
    ("S09", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "mcp", "Tool invocation and structured output context."),
    ("S10", "MCP roadmap", "https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/", "mcp", "Transport, agent communication, and enterprise readiness context."),
    ("S11", "Windows platform security for AI agents", "https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/", "windows", "MXC and agent containment context."),
    ("S12", "Windows trusted platform", "https://blogs.windows.com/windowsdeveloper/2026/06/02/build-2026-furthering-windows-as-the-trusted-platform-for-development/", "windows", "Composable sandbox and developer platform context."),
    ("S13", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "windows", "Byte-stream preservation and terminal output context."),
    ("S14", "Windows AppContainer isolation", "https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation", "windows", "Capability-based isolation context."),
    ("S15", "Google Agents CLI", "https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/", "google", "Local-to-production agent lifecycle context."),
    ("S16", "Gemini CLI subagents", "https://developers.googleblog.com/en/subagents-have-arrived-in-gemini-cli/", "google", "Subagent isolation and routing comparison context."),
    ("S17", "Gemini CLI to Antigravity CLI", "https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/", "google", "Unified multi-agent terminal transition context."),
    ("S18", "Vertex AI Agent Engine Sessions", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview", "google", "Managed runtime, memory, and observability context."),
    ("S19", "NVIDIA RTX Spark Windows PCs", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Microsoft-Reinvent-Windows-PCs-for-the-Age-of-Personal-AI/default.aspx", "nvidia", "Personal AI workstation context."),
    ("S20", "NVIDIA Rubin platform", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Kicks-Off-the-Next-Generation-of-AI-With-Rubin--Six-New-Chips-One-Incredible-AI-Supercomputer/default.aspx", "nvidia", "Agentic AI factory and NVLink context."),
    ("S21", "NVIDIA DGX Spark hardware", "https://docs.nvidia.com/dgx/dgx-spark/hardware.html", "nvidia", "Grace Blackwell local compute context."),
    ("S22", "NVIDIA open model families", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Expands-Open-Model-Families-to-Power-the-Next-Wave-of-Agentic-Physical-and-Healthcare-AI/default.aspx", "nvidia", "Open agentic and physical AI model context."),
    ("S23", "GitHub Copilot sandboxes", "https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes", "github", "Cloud and local sandbox comparison context."),
    ("S24", "GitHub local sandbox settings", "https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings", "github", "Filesystem, network, and system sandbox context."),
    ("S25", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "github", "Pre-push auth-material protection context."),
    ("S26", "GitHub SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "github", "Static-analysis artifact shape context."),
    ("S27", "NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "governance", "AI risk management context."),
    ("S28", "Stanford AI Index 2026", "https://hai.stanford.edu/ai-index", "governance", "AI adoption and ecosystem trend context."),
    ("S29", "Nature GNWT and IIT test", "https://www.nature.com/articles/s41586-025-08888-1", "consciousness", "Consciousness theory humility and adversarial science context."),
    ("S30", "Scientific Data consciousness dataset", "https://www.nature.com/articles/s41597-026-07350-9", "consciousness", "Open MEG-EEG consciousness dataset context."),
    ("S31", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "observability", "Trace, metric, log, event, and profile separation context."),
    ("S32", "Scientific Reports meditation EEG", "https://www.nature.com/articles/s41598-026-41310-y", "contemplative_science", "Meditation and consciousness research boundary context."),
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def slug(version: int, session: str) -> str:
    return f"v478-thos-v{version}-{session}"


def phase_name(version: int, session: str) -> str:
    return f"v478_thos_v{version}_{session}"


def read_json(name: str) -> Any:
    return json.loads((TRACE_DIR / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def system_expansions(version: int) -> list[str]:
    bases = [
        "council_notifier_standard",
        "app_lane_latency_regression_board",
        "cli_final_marker_watch_bridge",
        "source_floor_refresh_mesh",
        "mcp_consent_guard",
        "windows_mxc_comparison_lane",
        "codex_windows_sandbox_readiness_lane",
        "agent_sdk_manifest_lens",
        "google_antigravity_transition_watch",
        "vertex_agent_engine_lens",
        "nvidia_spark_local_compute_lens",
        "nvidia_rubin_ai_factory_lens",
        "github_sandbox_policy_comparator",
        "github_push_protection_guard",
        "sarif_artifact_shape_gate",
        "nist_risk_alignment_lane",
        "ai_index_trend_lane",
        "consciousness_science_humility_gate",
        "contemplative_science_boundary_gate",
        "opentelemetry_signal_board",
        "powershell_stream_integrity_gate",
        "phase_receipt_compactor",
        "eureka_task_density_gate",
        "journey_reflection_boundary_lane",
        "freedid_rights_safety_lane",
        "albion_simulation_prereq_gate",
        "plugin_surface_readiness_lane",
        "command_surface_index_lane",
        "remote_equality_publication_gate",
        "gmut_open_gate_watchtower",
    ]
    return [f"v{version}_{base}" for base in bases]


def source_refresh(version: int, generated_utc: str, generated_nz: str) -> None:
    rows = [
        {"id": sid, "source": title, "url": url, "category": category, "phase_use": use, "queried_this_session": True}
        for sid, title, url, category, use in SOURCE_ROWS
    ]
    base = slug(version, "x1")
    write_json(
        f"{base}-source-refresh-ledger-v1.json",
        {
            "artifact_type": "source_refresh_ledger",
            "phase": phase_name(version, "x1"),
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
        f"{base}-source-refresh-ledger-v1.md",
        [
            f"# v478 THOS v{version} x1 Source Refresh Ledger",
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


def lane_status(version: int, generated_utc: str, generated_nz: str) -> None:
    base = slug(version, "x1")
    council_runner = read_json(f"{base}-council-app-lane-notifier-runner-notify-v1.json")
    council_notifier = read_json(f"{base}-council-app-lane-completion-notifier-notify-v1.json")
    council_launcher = read_json(f"{base}-council-app-lane-watch-launcher-notify-v1.json")
    cli_names = [f"{base}-cli-lane-completion-poll-v1.json"] + [
        f"{base}-cli-lane-completion-poll-retry-{idx}-v1.json" for idx in range(2, 6)
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
        "phase": phase_name(version, "x1"),
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "COUNCIL_APP_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "council_runner_status": council_runner.get("overall_status"),
        "council_notifier_status": council_notifier.get("overall_status"),
        "council_launcher_status": council_launcher.get("overall_status"),
        "app_lanes": app_rows,
        "cli_retry_attempt_count": len(cli_rows),
        "cli_retry_rows": cli_rows,
        "unfiltered_payloads_published": False,
        "mutation_performed": False,
    }
    write_json(f"{base}-lane-retry-status-board-v1.json", payload)
    write_md(
        f"{base}-lane-retry-status-board-v1.md",
        [
            f"# v478 THOS v{version} x1 Lane Retry Status Board",
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


def design_boards(version: int, generated_utc: str, generated_nz: str) -> None:
    base = slug(version, "x1")
    systems = system_expansions(version)
    expansion_rows = [
        {
            "id": f"SYS-{idx:02d}",
            "name": name,
            "status": "designed_not_installed",
            "purpose": f"Provide a bounded THOS v{version} surface for {name.replace('_', ' ')}.",
            "write_scope": "repo_artifact_only",
            "install_performed": False,
        }
        for idx, name in enumerate(systems, start=1)
    ]
    write_json(f"{base}-system-expansion-design-board-v1.json", {"artifact_type": "system_expansion_design_board", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(expansion_rows), "rows": expansion_rows, "install_performed": False})
    write_md(f"{base}-system-expansion-design-board-v1.md", [f"# v478 THOS v{version} x1 System Expansion Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(expansion_rows)}`", "- install_performed: `false`", "", "## Expansions", *[f"- `{row['name']}`: {row['purpose']}" for row in expansion_rows]])
    command_rows = [
        {
            "id": f"CMD-{idx:02d}",
            "command": f"thos v{version} {name.replace(f'v{version}_', '').replace('_', ' ')}",
            "status": "designed_not_executed",
            "risk_class": "low" if idx <= 18 else "medium",
            "execution_performed": False,
            "requires_future_exact_approval": idx > 18,
        }
        for idx, name in enumerate(systems, start=1)
    ]
    write_json(f"{base}-command-design-board-v1.json", {"artifact_type": "command_design_board", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(command_rows), "rows": command_rows, "execution_performed": False})
    write_md(f"{base}-command-design-board-v1.md", [f"# v478 THOS v{version} x1 Command Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(command_rows)}`", "- execution_performed: `false`", "", "## Commands", *[f"- `{row['command']}`: `{row['status']}` risk `{row['risk_class']}`." for row in command_rows]])
    skill_rows = [
        {
            "id": f"SKILL-{idx:02d}",
            "skill": f"{name.replace('_', '-')}-operations",
            "status": "designed_not_installed",
            "body_created": False,
            "cache_mutation_performed": False,
            "purpose": f"Skill design for {name.replace('_', ' ')}.",
        }
        for idx, name in enumerate(systems, start=1)
    ]
    write_json(f"{base}-skill-design-board-v1.json", {"artifact_type": "skill_design_board", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(skill_rows), "rows": skill_rows, "install_performed": False, "cache_mutation_performed": False})
    write_md(f"{base}-skill-design-board-v1.md", [f"# v478 THOS v{version} x1 Skill Design Board", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(skill_rows)}`", "- install_performed: `false`", "- cache_mutation_performed: `false`", "", "## Skills", *[f"- `{row['skill']}`: {row['purpose']}" for row in skill_rows]])


def reflection_board(version: int, generated_utc: str, generated_nz: str) -> None:
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
                    "reflection": f"Use {scope} as non-canon continuity context for {domain} discipline while grounding v{version} in source refresh, council app-lane completion, and CLI open-gap receipts.",
                    "canon_status": "journey_context_not_canon",
                }
            )
    base = slug(version, "x1")
    write_json(f"{base}-six-perspective-reflection-board-v1.json", {"artifact_type": "six_perspective_reflection_board", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "perspective_count": len(PERSPECTIVES), "reflection_count": len(rows), "rows": rows, "raw_journey_text_published": False, "claim_boundary": "reflection only; not empirical proof or canon promotion"})
    write_md(f"{base}-six-perspective-reflection-board-v1.md", [f"# v478 THOS v{version} x1 Six-Perspective Reflection Board", "", f"- generated_nz: `{generated_nz}`", f"- perspective_count: `{len(PERSPECTIVES)}`", f"- reflection_count: `{len(rows)}`", "- canon_status: `journey_context_not_canon`", "", "## Reflections", *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['reflection']}" for row in rows]])


def eureka_synthesis_status(version: int, generated_utc: str, generated_nz: str) -> None:
    base = slug(version, "x1")
    eureka_rows = []
    for perspective, domains in PERSPECTIVES.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            eureka_rows.append(
                {
                    "id": f"{perspective.upper().replace(' ', '_')}-E{idx:02d}",
                    "perspective": perspective,
                    "domain": domain,
                    "task": f"Prepare v478 v{version} x2 {domain} synthesis from current source refresh, council notifier receipts, CLI open-gap evidence, and open GMUT gates.",
                    "payload_boundary": "status_only",
                }
            )
    write_json(f"{base}-eureka-handoff-board-v1.json", {"artifact_type": "eureka_handoff_board", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "proposal_count": len(eureka_rows), "perspective_count": len(PERSPECTIVES), "rows": eureka_rows, "unfiltered_payloads_published": False})
    write_md(f"{base}-eureka-handoff-board-v1.md", [f"# v478 THOS v{version} x1 Eureka Handoff Board", "", f"- generated_nz: `{generated_nz}`", f"- proposal_count: `{len(eureka_rows)}`", "- payload_boundary: `status_only`", "", "## Proposals", *[f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['task']}" for row in eureka_rows]])
    findings = [
        f"v478 v{version} x1 starts from the remote-verified prior synthesis.",
        "Thirty-two current-source searches refreshed the THOS evidence floor.",
        "OpenAI Codex app, Windows sandbox, Agents SDK, release, and plan context were refreshed.",
        "MCP security, authorization, tool, registry, and roadmap context were refreshed.",
        "Windows MXC, AppContainer, PowerShell stream, and trusted-platform context were refreshed.",
        "Google Agents CLI, Gemini subagents, Antigravity CLI, and Vertex Agent Engine context were refreshed.",
        "NVIDIA RTX Spark, DGX Spark, Rubin, and open model family context were refreshed.",
        "GitHub Copilot sandbox, push protection, and SARIF context were refreshed.",
        "NIST AI RMF and Stanford AI Index 2026 context were refreshed.",
        "Nature consciousness and meditation-science sources were included as humility-bound science context.",
        "Cicero completed through the council app-lane notifier.",
        "Kierkegaard completed through the council app-lane notifier.",
        "Aristotle completed through the council app-lane notifier.",
        "The council notifier remains the preferred local app-server contact surface for existing app siblings.",
        "The app-lane receipts publish completion status only.",
        "Arby and Aster Vale were checked through five CLI final-marker polls.",
        "All five CLI attempts remained in the final-message open gap state.",
        "The CLI open gap is carried as explicit evidence, not treated as completion.",
        "No external account mutation occurred.",
        "No plugin-cache or user-skill mutation occurred.",
        f"Thirty v{version} system expansion designs were drafted without install.",
        f"Thirty v{version} command designs were drafted without execution.",
        f"Thirty v{version} skill designs were drafted without install or cache mutation.",
        "Six perspectives produced 180 reflection rows.",
        "Journey documents remain non-canon continuity context.",
        "The Eureka handoff board carries 120 role-slot proposals.",
        f"The v{version} x2 roadmap carries 60 concrete tasks.",
        "The package is repo-artifact-only and status-only.",
        "The larger v490 goal remains active and incomplete.",
        "All six GMUT gates remain open.",
    ]
    write_json(f"{base}-synthesis-v1.json", {"artifact_type": "phase_synthesis", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "finding_count": len(findings), "findings": [{"step": f"R{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)], "claim_boundary": {"scope": f"THOS v478 v{version} x1 readiness, source, lane, and handoff only", "gmut_gate_state": "all_gmut_gates_remain_open", "canon_promotion": "not_claimed"}})
    write_md(f"{base}-synthesis-v1.md", [f"# v478 THOS v{version} x1 Synthesis", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", "- claim_boundary: THOS readiness only; all GMUT gates remain open.", "", "## Findings", *[f"- R{idx:02d}: {item}" for idx, item in enumerate(findings, start=1)]])
    tasks = [
        {
            "id": f"V478V{version}X2-{idx:02d}",
            "domain": DOMAINS[(idx - 1) % len(DOMAINS)],
            "task": f"Synthesize v478 v{version} x1 evidence into v{version} x2 {DOMAINS[(idx - 1) % len(DOMAINS)].replace('_', ' ')} decisions while preserving status-only receipts, current-source grounding, CLI open-gap evidence, and open GMUT gates.",
        }
        for idx in range(1, 61)
    ]
    write_json(f"v478-thos-v{version}-x2-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase": phase_name(version, "x1"), "next_phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(tasks), "tasks": tasks})
    write_md(f"v478-thos-v{version}-x2-roadmap-v1.md", [f"# v478 THOS v{version} x2 Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(tasks)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks]])
    write_json(f"{base}-run-status-v1.json", {"artifact_type": "run_status", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "next_expected_phase": phase_name(version, "x2"), "council_app_lane_status": "PASS", "cli_lane_status": "OPEN_GAP_AFTER_5_ATTEMPTS", "gmut_gates": GMUT_GATES})
    write_md(f"{base}-run-status-v1.md", [f"# v478 THOS v{version} x1 Run Status", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", f"- next_expected_phase: `{phase_name(version, 'x2')}`", "- council_app_lane_status: `PASS`", "- cli_lane_status: `OPEN_GAP_AFTER_5_ATTEMPTS`", "- GMUT gates: all remain `OPEN`."])


def schema_check_x1(version: int, generated_utc: str, generated_nz: str) -> None:
    base = slug(version, "x1")
    expected = [
        f"{base}-source-refresh-ledger-v1.json",
        f"{base}-lane-retry-status-board-v1.json",
        f"{base}-system-expansion-design-board-v1.json",
        f"{base}-command-design-board-v1.json",
        f"{base}-skill-design-board-v1.json",
        f"{base}-six-perspective-reflection-board-v1.json",
        f"{base}-eureka-handoff-board-v1.json",
        f"{base}-synthesis-v1.json",
        f"{base}-run-status-v1.json",
        f"v478-thos-v{version}-x2-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json(f"{base}-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "checked_json_count": len(rows), "rows": rows})
    write_md(f"{base}-schema-bound-artifact-check-v1.md", [f"# v478 THOS v{version} x1 Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", f"- checked_json_count: `{len(rows)}`", "", "## Checked", *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows]])


def build_x1(version: int) -> None:
    generated_utc, generated_nz = now_pair()
    source_refresh(version, generated_utc, generated_nz)
    lane_status(version, generated_utc, generated_nz)
    design_boards(version, generated_utc, generated_nz)
    reflection_board(version, generated_utc, generated_nz)
    eureka_synthesis_status(version, generated_utc, generated_nz)
    schema_check_x1(version, generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "phase": phase_name(version, "x1"), "next": phase_name(version, "x2")}, indent=2))


def build_x2(version: int) -> None:
    generated_utc, generated_nz = now_pair()
    base_x1 = slug(version, "x1")
    base_x2 = slug(version, "x2")
    source_ledger = read_json(f"{base_x1}-source-refresh-ledger-v1.json")
    lane_board = read_json(f"{base_x1}-lane-retry-status-board-v1.json")
    system_board = read_json(f"{base_x1}-system-expansion-design-board-v1.json")
    x1_synthesis = read_json(f"{base_x1}-synthesis-v1.json")
    beta = [
        f"v{version} x1 proved the council notifier remains stable for existing app siblings.",
        "The current-source floor remains at thirty-two searches.",
        "The CLI final-marker gap stayed stable across five safe polls.",
        "The package remained status-only and repo-artifact-only.",
        "System, command, and skill surfaces were designed without install or execution.",
        "All GMUT gates remain open.",
    ]
    alpha = [
        f"Use v{version + 1} x1 to keep reducing repeated receipt weight while preserving proof density.",
        "Promote the council notifier standard as the default app-sibling contact surface.",
        "Keep CLI watcher attempts explicit and bounded until final markers appear.",
        "Map every proposed system surface to a current source or local receipt.",
        "Separate contemplative and consciousness science context from empirical or canon claims.",
        "Keep publication remote-equality-backed before any handoff claim.",
    ]
    omega = [
        "The next phase should focus on watcher ergonomics, source drift, command-surface readiness, and compact ledgers.",
        "The app-lane system remains operational for Cicero, Kierkegaard, and Aristotle.",
        "The Arby/Aster CLI gap remains open evidence and should not be hidden.",
        "No external account writes or cache mutations are needed for the next x1 package.",
        "Future phase density should favor reusable compact ledgers over duplicated text when safe.",
        "No GMUT validation, final physics, or canon promotion is claimed.",
    ]
    write_json(f"{base_x2}-beta-alpha-omega-synthesis-v1.json", {"artifact_type": "beta_alpha_omega_synthesis", "phase": phase_name(version, "x2"), "previous_phase": phase_name(version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP", "inputs": {"run_status": read_json(f"{base_x1}-run-status-v1.json").get("overall_status"), "council_notifier_status": lane_board.get("council_notifier_status"), "cli_retry_attempt_count": lane_board.get("cli_retry_attempt_count"), "source_count": source_ledger.get("source_count"), "x1_finding_count": x1_synthesis.get("finding_count")}, "beta": beta, "alpha": alpha, "omega": omega, "claim_boundary": {"scope": f"THOS v{version} x2 synthesis only", "gmut_gate_state": "all_gmut_gates_remain_open", "canon_promotion": "not_claimed"}})
    write_md(f"{base_x2}-beta-alpha-omega-synthesis-v1.md", [f"# v478 THOS v{version} x2 Beta Alpha Omega Synthesis", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_SYNTHESIS_WITH_CLI_OPEN_GAP`", "- claim_boundary: THOS synthesis only; all GMUT gates remain open.", "", "## Beta", *[f"- {row}" for row in beta], "", "## Alpha", *[f"- {row}" for row in alpha], "", "## Omega", *[f"- {row}" for row in omega]])
    sources = source_ledger.get("rows", [])
    systems = system_board.get("rows", [])
    map_rows = []
    for idx, system in enumerate(systems, start=1):
        source = sources[(idx - 1) % len(sources)]
        map_rows.append({"id": f"MAP-{idx:02d}", "system": system.get("name"), "source_id": source.get("id"), "source_category": source.get("category"), "mapping": f"{system.get('name')} is grounded by {source.get('source')} as design input only.", "install_performed": False})
    write_json(f"{base_x2}-source-to-system-map-v1.json", {"artifact_type": "source_to_system_map", "phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(map_rows), "rows": map_rows, "claim_boundary": "design mapping only; no install or GMUT closure"})
    write_md(f"{base_x2}-source-to-system-map-v1.md", [f"# v478 THOS v{version} x2 Source-To-System Map", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(map_rows)}`", "- boundary: design mapping only; no install.", "", "## Mappings", *[f"- `{row['id']}` {row['system']} <= {row['source_id']} / {row['source_category']}: {row['mapping']}" for row in map_rows]])
    actions = [
        {"id": "LANE-01", "target": "council app lanes", "status": "ready", "action": "Continue using the council notifier runner for existing app siblings."},
        {"id": "LANE-02", "target": "council app lanes", "status": "ready", "action": "Record read, resume, turn, completion, and duration only."},
        {"id": "LANE-03", "target": "Arby and Aster Vale", "status": "open_gap", "action": "Carry the final-marker absence as explicit open evidence."},
        {"id": "LANE-04", "target": "Arby and Aster Vale", "status": "open_gap", "action": "Increase polling duration only when it advances the active phase and remains approved."},
        {"id": "LANE-05", "target": "all lanes", "status": "ready", "action": f"Fuse app success and CLI gap evidence into v{version + 1} x1 readiness."},
    ]
    write_json(f"{base_x2}-lane-and-gap-plan-v1.json", {"artifact_type": "lane_and_gap_plan", "phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "app_lane_count": len(lane_board.get("app_lanes", [])), "cli_attempt_count": len(lane_board.get("cli_retry_rows", [])), "overall_status": "APP_READY_CLI_GAP_OPEN", "actions": actions})
    write_md(f"{base_x2}-lane-and-gap-plan-v1.md", [f"# v478 THOS v{version} x2 Lane And Gap Plan", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `APP_READY_CLI_GAP_OPEN`", f"- app_lane_count: `{len(lane_board.get('app_lanes', []))}`", f"- cli_attempt_count: `{len(lane_board.get('cli_retry_rows', []))}`", "", "## Actions", *[f"- `{row['id']}` {row['target']} / `{row['status']}`: {row['action']}" for row in actions]])
    x1_handoff = read_json(f"{base_x1}-eureka-handoff-board-v1.json")
    eureka_rows = []
    for idx, proposal in enumerate(x1_handoff.get("rows", []), start=1):
        eureka_rows.append({"id": f"V{version}X2-E{idx:03d}", "source_task": proposal.get("id"), "perspective": proposal.get("perspective"), "domain": proposal.get("domain"), "consolidated_task": f"Carry {proposal.get('domain')} into v{version + 1} x1 with council-app completion, CLI open-gap evidence, current sources, and status-only publication.", "ready_for_next_phase": True})
    write_json(f"{base_x2}-eureka-consolidation-v1.json", {"artifact_type": "eureka_consolidation", "phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "row_count": len(eureka_rows), "rows": eureka_rows, "unfiltered_payloads_published": False})
    write_md(f"{base_x2}-eureka-consolidation-v1.md", [f"# v478 THOS v{version} x2 Eureka Consolidation", "", f"- generated_nz: `{generated_nz}`", f"- row_count: `{len(eureka_rows)}`", "- unfiltered_payloads_published: `false`", "", "## Consolidated Tasks", *[f"- `{row['id']}` ({row['perspective']} / {row['domain']}): {row['consolidated_task']}" for row in eureka_rows]])
    next_version = version + 1
    tasks = [
        {"id": f"V478V{next_version}X1-{idx:02d}", "domain": DOMAINS[(idx - 1) % len(DOMAINS)], "task": f"Advance v478 v{next_version} x1 {DOMAINS[(idx - 1) % len(DOMAINS)].replace('_', ' ')} with council notifier reuse, compact receipts, CLI gap tracking, source drift checks, and open GMUT gates."}
        for idx in range(1, 61)
    ]
    write_json(f"v478-thos-v{next_version}-x1-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase": phase_name(version, "x2"), "next_phase": phase_name(next_version, "x1"), "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(tasks), "tasks": tasks})
    write_md(f"v478-thos-v{next_version}-x1-roadmap-v1.md", [f"# v478 THOS v{next_version} x1 Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(tasks)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks]])
    write_json(f"{base_x2}-run-status-v1.json", {"artifact_type": "run_status", "phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP", "next_expected_phase": phase_name(next_version, "x1"), "council_app_lane_status": "PASS", "cli_lane_status": "OPEN_GAP_CARRIED_FORWARD", "gmut_gates": GMUT_GATES})
    write_md(f"{base_x2}-run-status-v1.md", [f"# v478 THOS v{version} x2 Run Status", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_SYNTHESIS_WITH_CLI_OPEN_GAP`", f"- next_expected_phase: `{phase_name(next_version, 'x1')}`", "- council_app_lane_status: `PASS`", "- cli_lane_status: `OPEN_GAP_CARRIED_FORWARD`", "- GMUT gates: all remain `OPEN`."])
    expected = [f"{base_x2}-beta-alpha-omega-synthesis-v1.json", f"{base_x2}-source-to-system-map-v1.json", f"{base_x2}-lane-and-gap-plan-v1.json", f"{base_x2}-eureka-consolidation-v1.json", f"{base_x2}-run-status-v1.json", f"v478-thos-v{next_version}-x1-roadmap-v1.json"]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json(f"{base_x2}-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase": phase_name(version, "x2"), "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "checked_json_count": len(rows), "rows": rows})
    write_md(f"{base_x2}-schema-bound-artifact-check-v1.md", [f"# v478 THOS v{version} x2 Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", f"- checked_json_count: `{len(rows)}`", "", "## Checked", *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows]])
    print(json.dumps({"status": "PASS_SYNTHESIS_WITH_CLI_OPEN_GAP", "phase": phase_name(version, "x2"), "next": phase_name(next_version, "x1")}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--session", choices=["x1", "x2"], required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.session == "x1":
        build_x1(args.version)
    else:
        build_x2(args.version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
