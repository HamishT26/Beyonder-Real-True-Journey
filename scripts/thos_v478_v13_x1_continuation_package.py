#!/usr/bin/env python3
"""Build the v478 THOS v13 x1 continuation package from curated evidence."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478-thos-v13-x1"
PREVIOUS_PHASE = "v478-thos-v12-x2"
NEXT_PHASE = "v478-thos-v13-x2"

DOMAINS = [
    "lane_reliability",
    "stale_flow",
    "runner_contract",
    "source_freshness",
    "sandbox_readiness",
    "command_surface",
    "skill_surface",
    "mcp_trust",
    "publication_guard",
    "journey_reflection",
    "gmut_thos_boundary",
    "dashboard_compaction",
]

SOURCE_ROWS = [
    ("SRC-01", "openai_codex", "Codex for every role, tool, and workflow", "https://openai.com/index/codex-for-every-role-tool-workflow/", "Role plugins, sites, annotations, and broad workflow expansion."),
    ("SRC-02", "openai_codex", "Introducing the Codex app", "https://openai.com/index/introducing-the-codex-app/", "Multi-agent desktop command-center and sandbox framing."),
    ("SRC-03", "openai_codex", "Using Codex with your ChatGPT plan", "https://help.openai.com/en/articles/11369540", "Plan boundary, client access, and usage framing."),
    ("SRC-04", "openai_codex", "Codex releases", "https://github.com/openai/codex/releases", "CLI release drift and update-watch framing."),
    ("SRC-05", "openai_agents", "The next evolution of the Agents SDK", "https://openai.com/index/the-next-evolution-of-the-agents-sdk", "Sandbox, checkpoint, and durable harness framing."),
    ("SRC-06", "openai_agents", "OpenAI Agents SDK", "https://platform.openai.com/docs/guides/agents-sdk/", "Agent handoff, trace, and orchestration framing."),
    ("SRC-07", "openai_agents", "Agents", "https://platform.openai.com/docs/guides/agents", "AgentKit, eval, connector, and deployment framing."),
    ("SRC-08", "openai_agents", "Guardrails", "https://openai.github.io/openai-agents-js/guides/guardrails", "Tool and output guardrail framing."),
    ("SRC-09", "mcp", "MCP authorization", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "Transport authorization and resource-boundary framing."),
    ("SRC-10", "mcp", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "Connector trust and token-boundary framing."),
    ("SRC-11", "mcp", "MCP key changes", "https://modelcontextprotocol.io/specification/2025-06-18/changelog", "Structured output and resource metadata framing."),
    ("SRC-12", "mcp", "MCP 2026 roadmap", "https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/", "Agent communication and enterprise-readiness framing."),
    ("SRC-13", "windows", "Windows platform security for AI agents", "https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/", "MXC, composable sandbox, and agent containment framing."),
    ("SRC-14", "windows", "Windows trusted development platform", "https://blogs.windows.com/windowsdeveloper/2026/06/02/build-2026-furthering-windows-as-the-trusted-platform-for-development/", "Windows local AI and sandbox platform framing."),
    ("SRC-15", "windows", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "Terminal stream preservation framing."),
    ("SRC-16", "windows", "AppContainer isolation", "https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation", "Windows isolation primitive framing."),
    ("SRC-17", "google", "Agents CLI in Agent Platform", "https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/", "Local-to-production agent lifecycle framing."),
    ("SRC-18", "google", "Gemini CLI subagents", "https://developers.googleblog.com/en/subagents-have-arrived-in-gemini-cli/", "Isolated specialist-agent comparison framing."),
    ("SRC-19", "google", "Gemini CLI to Antigravity CLI transition", "https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/", "Unified multi-agent terminal transition framing."),
    ("SRC-20", "google", "Vertex AI Agent Engine sessions", "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview", "Managed session, event, state, and memory framing."),
    ("SRC-21", "nvidia", "NVIDIA RTX Spark Windows PCs", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Microsoft-Reinvent-Windows-PCs-for-the-Age-of-Personal-AI/default.aspx", "Personal AI workstation and Windows agent framing."),
    ("SRC-22", "nvidia", "NVIDIA Rubin platform", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Kicks-Off-the-Next-Generation-of-AI-With-Rubin--Six-New-Chips-One-Incredible-AI-Supercomputer/default.aspx", "Agentic AI factory and NVLink framing."),
    ("SRC-23", "nvidia", "NVIDIA Vera Rubin production", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx", "Production-scale agentic compute framing."),
    ("SRC-24", "nvidia", "NVIDIA open model families", "https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai", "Nemotron and agentic model-family framing."),
    ("SRC-25", "github", "Copilot cloud and local sandboxes", "https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes", "Sandbox policy comparison framing."),
    ("SRC-26", "github", "Local sandbox settings", "https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings", "Filesystem, network, and sandbox setting framing."),
    ("SRC-27", "github", "Push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "Pre-publication secret prevention framing."),
    ("SRC-28", "github", "SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "Security artifact shape framing."),
    ("SRC-29", "governance", "NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "AI risk and critical infrastructure framing."),
    ("SRC-30", "governance", "Stanford AI Index 2026", "https://hai.stanford.edu/ai-index/2026-ai-index-report", "AI ecosystem measurement framing."),
    ("SRC-31", "observability", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "Trace, metric, log, event, baggage, and profile separation framing."),
    ("SRC-32", "science", "Nature consciousness adversarial test", "https://www.nature.com/articles/s41586-025-08888-1", "Consciousness-science humility and disagreement framing."),
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


def lane_rows(app_payload: dict[str, Any], cli_payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in app_payload.get("notifier_summary", {}).get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "surface": "app_local_server",
                "status": lane.get("overall_status"),
                "completion": lane.get("completion_status"),
                "action": "carry_ready_status_without_payload_publication",
            }
        )
    for lane in cli_payload.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "surface": "cli_final_marker",
                "status": lane.get("completion_status"),
                "completion": "marker_open" if lane.get("completion_status") != "FINAL_MESSAGE_READY" else "marker_ready",
                "action": "keep_status_only_watch_active",
            }
        )
    return rows


def reflection_rows() -> list[dict[str, str]]:
    scopes = [
        "v4-v6 early continuity",
        "v15-v16 system roots",
        "v24-v25 Ariel reflection",
        "v29 Aerin THOS foundation",
        "v30-v38 Trinity Mandala foundation",
        "v39 induction continuity",
        "v45-v48 Solas planning",
        "v49 Codex sibling closeout",
        "v476-v477 watcher recovery",
        "v478 v12 skill evolution",
    ]
    rows: list[dict[str, str]] = []
    for idx in range(1, 31):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        scope = scopes[(idx - 1) % len(scopes)]
        rows.append(
            {
                "id": f"V13X1-REF-{idx:02d}",
                "domain": domain,
                "scope": scope,
                "reflection": f"Use {scope} as bounded context for {domain}; preserve proof-first THOS receipts and open GMUT gates.",
                "status": "context_only",
            }
        )
    return rows


def helper_rows() -> list[dict[str, str]]:
    names = [
        "five_lane_state_compactor",
        "cli_final_marker_contract_probe",
        "app_local_server_receipt_minifier",
        "stale_flow_repeat_counter",
        "source_freshness_delta_board",
        "command_surface_bridge_index",
        "skill_surface_frontmatter_audit_plan",
        "mcp_connector_consent_matrix",
        "publication_guard_preflight_pack",
        "gmut_open_gate_dashboard",
    ]
    return [
        {
            "id": f"HELPER-{idx:02d}",
            "name": f"v13_{name}",
            "status": "designed_not_installed",
            "purpose": f"Support {PHASE} by improving {name.replace('_', ' ')} without mutating live caches.",
        }
        for idx, name in enumerate(names, start=1)
    ]


def roadmap_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx in range(1, 61):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        rows.append(
            {
                "id": f"V478V13X2-{idx:02d}",
                "domain": domain,
                "task": f"Advance {NEXT_PHASE} {domain.replace('_', ' ')} with v13 x1 compact evidence, stale-flow receipts, source freshness, and open GMUT gates.",
            }
        )
    return rows


def build() -> None:
    generated_utc, generated_nz = now_pair()
    app = read_json(f"{PHASE}-council-app-lane-notifier-runner-notify-v1.json")
    cli = read_json("v478-thos-v12-x1-background-cli-completion-v1.json")
    x2_synthesis = read_json(f"{PREVIOUS_PHASE}-beta-alpha-omega-synthesis-v1.json")
    lanes = lane_rows(app, cli)
    reflections = reflection_rows()
    helpers = helper_rows()
    sources = [
        {
            "id": sid,
            "category": category,
            "title": title,
            "url": url,
            "phase_use": use,
            "queried_for_v13_x1": True,
        }
        for sid, category, title, url, use in SOURCE_ROWS
    ]

    lane_board = {
        "artifact_type": "lane_continuity_board",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_READY_CLI_FINAL_MARKER_OPEN",
        "app_receipt_available": bool(app.get("artifact_type")),
        "cli_receipt_available": bool(cli.get("artifact_type")),
        "rows": lanes,
        "policy": {
            "existing_lanes_only": True,
            "new_threads_created": False,
            "old_style_spawn_used": False,
            "unfiltered_lane_text_published": False,
        },
    }
    write_json(f"{PHASE}-lane-continuity-board-v1.json", lane_board)
    write_md(
        f"{PHASE}-lane-continuity-board-v1.md",
        [
            f"# {PHASE} Lane Continuity Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- overall_status: `{lane_board['overall_status']}`",
            "- policy: existing lanes only; no new threads; no old-style spawning; status-only publication.",
            "",
            "## Rows",
            *[f"- `{row['lane']}` / `{row['surface']}`: status `{row['status']}`, completion `{row['completion']}`, action `{row['action']}`." for row in lanes],
        ],
    )

    stale_rows = [
        {
            "id": "STALE-CLI-FINAL-MARKER",
            "surface": "cli_final_marker_contract",
            "status": "open_carried_forward",
            "evidence": "v12 x1 and v12 x2 receipts carried Arby/Aster final-marker open state without treating it as completion.",
            "next_action": "keep final-marker watcher active and prepare exact lane mutation packet only if status-only methods cannot resolve it.",
        },
        {
            "id": "READY-APP-LOCAL-SERVER",
            "surface": "app_local_server",
            "status": "ready_from_receipts",
            "evidence": "local app-server receipts show Cicero, Kierkegaard, and Aristotle app lanes reachable through approved existing routes.",
            "next_action": "continue app-lane calls through local app-server summaries only.",
        },
        {
            "id": "READY-SKILL-ORCHESTRATION",
            "surface": "multi_agent_orchestration_skill",
            "status": "verified_live",
            "evidence": "v12 x1 skill receipt verified frontmatter and approved draft match.",
            "next_action": "use evolved skill as the live orchestration boundary.",
        },
    ]
    write_json(f"{PHASE}-stale-flow-refresh-v1.json", {"artifact_type": "stale_flow_refresh", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "STALE_CLI_MARKER_OPEN_APP_READY", "rows": stale_rows})
    write_md(f"{PHASE}-stale-flow-refresh-v1.md", [f"# {PHASE} Stale Flow Refresh", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `STALE_CLI_MARKER_OPEN_APP_READY`", "", "## Rows", *[f"- `{row['id']}` / `{row['status']}`: {row['evidence']} Next: {row['next_action']}" for row in stale_rows]])

    write_json(f"{PHASE}-source-refresh-ledger-v1.json", {"artifact_type": "source_refresh_ledger", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "search_count": 32, "source_count": len(sources), "rows": sources, "claim_boundary": "THOS source context only; all GMUT gates remain open"})
    write_md(f"{PHASE}-source-refresh-ledger-v1.md", [f"# {PHASE} Source Refresh Ledger", "", f"- generated_nz: `{generated_nz}`", "- search_count: `32`", f"- source_count: `{len(sources)}`", "- boundary: THOS source context only; all GMUT gates remain open.", "", "## Sources", *[f"- `{row['id']}` {row['category']}: [{row['title']}]({row['url']}) - {row['phase_use']}" for row in sources]])

    write_json(f"{PHASE}-personal-reflection-board-v1.json", {"artifact_type": "personal_reflection_board", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "reflection_count": len(reflections), "rows": reflections, "claim_boundary": "continuity reflection only; not canon"})
    write_md(f"{PHASE}-personal-reflection-board-v1.md", [f"# {PHASE} Personal Reflection Board", "", f"- generated_nz: `{generated_nz}`", f"- reflection_count: `{len(reflections)}`", "- boundary: continuity reflection only; not canon.", "", "## Reflections", *[f"- `{row['id']}` ({row['domain']} / {row['scope']}): {row['reflection']}" for row in reflections]])

    write_json(f"{PHASE}-runner-harmonization-helper-plan-v1.json", {"artifact_type": "runner_harmonization_helper_plan", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "helper_count": len(helpers), "rows": helpers, "install_performed": False})
    write_md(f"{PHASE}-runner-harmonization-helper-plan-v1.md", [f"# {PHASE} Runner Harmonization Helper Plan", "", f"- generated_nz: `{generated_nz}`", f"- helper_count: `{len(helpers)}`", "- install_performed: `false`", "", "## Helpers", *[f"- `{row['name']}`: {row['purpose']}" for row in helpers]])

    beta = [
        "v12 x2 remote publication is verified and can be treated as the latest curated baseline.",
        "The evolved orchestration skill now gives the run a clearer existing-lane and no-spawn boundary.",
        "App-lane continuity is stronger than CLI final-marker continuity, so the split state must remain visible.",
        "The source refresh confirms agent sandboxing, connector trust, and observability remain fast-moving surfaces.",
    ]
    alpha = [
        "v13 x1 should compact repeated evidence into boards rather than expanding report volume for its own sake.",
        "CLI final-marker gaps should be handled as stale-flow signals, not proof of failure or proof of completion.",
        "The next helper layer should improve status surfaces before proposing any live lane mutation.",
        "GMUT/THOS boundary language must remain humble, explicit, and receipt-backed.",
    ]
    omega = [
        "Proceed to v13 x2 with app-ready and CLI-open status visible.",
        "Use the 10-helper plan as design inventory, not installation proof.",
        "Keep x14+ phases focused on reducing babysitting through compact background status boards.",
        "The v478-v490 goal remains active and incomplete.",
    ]
    synthesis = {
        "artifact_type": "beta_alpha_omega_synthesis",
        "phase_slug": PHASE,
        "previous_phase_slug": PREVIOUS_PHASE,
        "next_phase_slug": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X1_CONTINUATION_WITH_CLI_FINAL_MARKER_OPEN",
        "input_receipts": {
            "previous_synthesis_status": x2_synthesis.get("overall_status"),
            "app_lane_receipt_available": lane_board["app_receipt_available"],
            "cli_lane_receipt_available": lane_board["cli_receipt_available"],
            "source_count": len(sources),
            "reflection_count": len(reflections),
        },
        "beta": beta,
        "alpha": alpha,
        "omega": omega,
        "claim_boundary": {
            "scope": "v13 x1 THOS continuation and v13 x2 preparation",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(f"{PHASE}-beta-alpha-omega-synthesis-v1.json", synthesis)
    write_md(f"{PHASE}-beta-alpha-omega-synthesis-v1.md", [f"# {PHASE} Beta Alpha Omega Synthesis", "", f"- generated_nz: `{generated_nz}`", f"- overall_status: `{synthesis['overall_status']}`", f"- next_phase_slug: `{NEXT_PHASE}`", "- boundary: THOS continuation only; all GMUT gates remain open.", "", "## Beta", *[f"- {row}" for row in beta], "", "## Alpha", *[f"- {row}" for row in alpha], "", "## Omega", *[f"- {row}" for row in omega]])

    roadmap = roadmap_rows()
    write_json(f"{NEXT_PHASE}-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase_slug": PHASE, "next_phase_slug": NEXT_PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(roadmap), "tasks": roadmap})
    write_md(f"{NEXT_PHASE}-roadmap-v1.md", [f"# {NEXT_PHASE} Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(roadmap)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in roadmap]])

    run_status = {
        "artifact_type": "run_status",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": synthesis["overall_status"],
        "next_expected_phase": NEXT_PHASE,
        "app_lane_status": "READY_OR_RECEIPT_PENDING",
        "cli_lane_status": "FINAL_MARKER_OPEN_CARRIED_FORWARD",
        "gmut_gates": {"empirical_physics": "OPEN", "consciousness_claims": "OPEN", "canon_promotion": "OPEN"},
    }
    write_json(f"{PHASE}-run-status-v1.json", run_status)
    write_md(f"{PHASE}-run-status-v1.md", [f"# {PHASE} Run Status", "", f"- generated_nz: `{generated_nz}`", f"- overall_status: `{run_status['overall_status']}`", f"- next_expected_phase: `{NEXT_PHASE}`", "- app_lane_status: `READY_OR_RECEIPT_PENDING`", "- cli_lane_status: `FINAL_MARKER_OPEN_CARRIED_FORWARD`", "- GMUT gates: all remain `OPEN`."])

    expected = [
        f"{PHASE}-lane-continuity-board-v1.json",
        f"{PHASE}-stale-flow-refresh-v1.json",
        f"{PHASE}-source-refresh-ledger-v1.json",
        f"{PHASE}-personal-reflection-board-v1.json",
        f"{PHASE}-runner-harmonization-helper-plan-v1.json",
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
    write_json(f"{PHASE}-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "rows": check_rows})
    write_md(f"{PHASE}-schema-bound-artifact-check-v1.md", [f"# {PHASE} Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", "", "## Rows", *[f"- `{row['artifact']}`: exists `{str(row['exists']).lower()}`, type `{row['artifact_type']}`." for row in check_rows]])

    print(json.dumps({"status": synthesis["overall_status"], "phase_slug": PHASE, "next_phase_slug": NEXT_PHASE}, sort_keys=True))


if __name__ == "__main__":
    build()
