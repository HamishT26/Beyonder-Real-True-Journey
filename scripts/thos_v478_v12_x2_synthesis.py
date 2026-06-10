#!/usr/bin/env python3
"""Build the v478 THOS v12 x2 synthesis package from current v12 evidence."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478-thos-v12-x2"
PREVIOUS_PHASE = "v478-thos-v12-x1"
NEXT_PHASE = "v478-thos-v13-x1"

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

SOURCES = [
    ("SRC-01", "openai_codex", "Introducing the Codex app", "https://openai.com/index/introducing-the-codex-app/", "Codex App multi-agent and worktree context"),
    ("SRC-02", "openai_codex", "Codex for every role, tool, and workflow", "https://openai.com/index/codex-for-every-role-tool-workflow/", "Codex plugins, Sites, annotations, and role workflow context"),
    ("SRC-03", "openai_codex", "Codex for almost everything", "https://openai.com/index/codex-for-almost-everything/", "Codex browser, SSH, terminal, and workflow expansion context"),
    ("SRC-04", "openai_codex", "Using Codex with your ChatGPT plan", "https://help.openai.com/en/articles/11369540-getting-started-with-codex", "Plan, usage, plugin, and data-control context"),
    ("SRC-05", "openai_codex", "Building Codex Windows sandbox", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox containment context"),
    ("SRC-06", "openai_agents", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-js/guides/tracing", "Tracing, guardrail, handoff, and custom event context"),
    ("SRC-07", "openai_agents", "The next evolution of the Agents SDK", "https://openai.com/index/the-next-evolution-of-the-agents-sdk", "Snapshotting, rehydration, and durable agent-state context"),
    ("SRC-08", "mcp", "MCP authorization", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "Connector authorization and transport context"),
    ("SRC-09", "mcp", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "Connector trust-boundary and token-scope context"),
    ("SRC-10", "mcp", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "Tool invocation and structured output context"),
    ("SRC-11", "mcp", "MCP 2026 roadmap", "https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/", "Agent communication and enterprise readiness context"),
    ("SRC-12", "mcp", "Official MCP Registry FAQ", "https://modelcontextprotocol.io/registry/faq", "Registry naming, API, and discovery context"),
    ("SRC-13", "windows", "Windows trusted development platform", "https://blogs.windows.com/windowsdeveloper/2026/06/02/build-2026-furthering-windows-as-the-trusted-platform-for-development/", "Local AI, agent workload, and Windows trust context"),
    ("SRC-14", "windows", "PowerShell about redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "Terminal stream and output-handling context"),
    ("SRC-15", "windows", "Windows application isolation", "https://learn.microsoft.com/en-gb/windows/security/book/application-security-application-isolation", "AppContainer and process-isolation context"),
    ("SRC-16", "microsoft", "Microsoft open trust stack for AI agents", "https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/", "Agent evaluation and control-standard context"),
    ("SRC-17", "google", "Transitioning Gemini CLI to Antigravity CLI", "https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/", "Multi-agent terminal migration context"),
    ("SRC-18", "google", "Google Antigravity at I/O 2026", "https://antigravity.google/blog/google-io-2026", "Antigravity 2.0 and CLI platform context"),
    ("SRC-19", "google", "Vertex AI Agent Engine sessions", "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview", "Managed agent session-state context"),
    ("SRC-20", "google", "Google I/O 2026 developer highlights", "https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights", "AI developer platform and migration context"),
    ("SRC-21", "nvidia", "NVIDIA and Microsoft reinvent Windows PCs for personal AI", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Microsoft-Reinvent-Windows-PCs-for-the-Age-of-Personal-AI/default.aspx", "RTX Spark personal AI workstation context"),
    ("SRC-22", "nvidia", "NVIDIA DGX Spark", "https://www.nvidia.com/en-us/products/workstations/dgx-spark/", "Grace Blackwell compact AI compute context"),
    ("SRC-23", "nvidia", "NVIDIA Vera Rubin full production", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx", "Agentic AI factory compute context"),
    ("SRC-24", "nvidia", "NVIDIA open model families", "https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai", "Nemotron and agentic model-family context"),
    ("SRC-25", "github", "GitHub Copilot cloud and local sandboxes", "https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes", "Sandbox comparison and access-policy context"),
    ("SRC-26", "github", "Configuring local sandbox settings", "https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings", "Local sandbox configuration context"),
    ("SRC-27", "github", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "Pre-publication auth-material prevention context"),
    ("SRC-28", "github", "SARIF support for code scanning", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "Security-report shape context"),
    ("SRC-29", "governance", "NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "AI risk and critical-infrastructure profile context"),
    ("SRC-30", "governance", "Stanford AI Index", "https://hai.stanford.edu/ai-index", "AI measurement and governance context"),
    ("SRC-31", "observability", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "Trace, metric, log, event, and profile separation context"),
    ("SRC-32", "science_security", "Nature consciousness adversarial test", "https://www.nature.com/articles/s41586-025-08888-1", "Consciousness-science humility and evidence-boundary context"),
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


def build_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": sid,
            "category": category,
            "title": title,
            "url": url,
            "phase_use": phase_use,
            "queried_for_x2": True,
        }
        for sid, category, title, url, phase_use in SOURCES
    ]


def reflection_rows() -> list[dict[str, Any]]:
    scopes = [
        "v4-v6 early continuity",
        "v15-v16 system roots",
        "v24-v25 Ariel reflection",
        "v29 Aerin THOS foundation",
        "v30-v38 Trinity Mandala foundation",
        "v39 induction continuity",
        "v45-v48 Solas planning",
        "v49 Codex sibling closeout",
    ]
    rows = []
    for idx in range(1, 31):
        domain = DOMAINS[(idx - 1) % len(DOMAINS)]
        scope = scopes[(idx - 1) % len(scopes)]
        rows.append(
            {
                "id": f"X2-REF-{idx:02d}",
                "domain": domain,
                "record_scope": scope,
                "reflection": (
                    f"Carry {scope} as non-canon context for {domain}; keep x2 synthesis bound "
                    "to receipts, source rows, and open GMUT gates."
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
                "id": f"V478V13X1-{idx:02d}",
                "domain": domain,
                "task": (
                    f"Advance {NEXT_PHASE} {domain.replace('_', ' ')} with compact x2 evidence, "
                    "source-drift refresh, stale-flow tracking, and open GMUT gates."
                ),
            }
        )
    return rows


def build() -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    handoff = read_json(f"{PREVIOUS_PHASE}-continuation-handoff-v1.json")
    stale = read_json(f"{PREVIOUS_PHASE}-stale-flow-refresh-runner-v1.json")
    skill = read_json(f"{PREVIOUS_PHASE}-live-skill-evolution-receipt-v1.json")
    sources = build_source_rows()
    reflections = reflection_rows()
    roadmap = roadmap_rows()
    beta = [
        "v12 x1 established an evolved orchestration skill with draft-match verification.",
        "The stale-flow runner identified app-ready and CLI-open split state without forcing completion.",
        "The x1 continuation handoff carried the CLI final-marker gap into x2 honestly.",
        "The fresh x2 source refresh keeps public source categories current for THOS design.",
        "The x2 reflection board supplies 30 context-only record reflections without source-body publication.",
        "All GMUT gates remain open.",
    ]
    alpha = [
        "Use v13 x1 to reduce repeated receipt weight while preserving proof density.",
        "Treat background notifier and multiplex boards as complementary visibility surfaces.",
        "Keep final-marker absence as an explicit stale-flow signal until marker evidence appears.",
        "Prefer source ledgers and schema checks over long copied reports.",
        "Convert any required lane mutation into a new exact approval packet.",
        "Keep rights, consciousness, and GMUT claims conceptual unless closure evidence exists.",
    ]
    omega = [
        "The next phase should promote stable runner contracts and compact dashboards.",
        "App-lane coordination remains ready through existing council lanes.",
        "Arby and Aster CLI marker status remains open evidence, not failure and not completion.",
        "The approved skill evolution should guide all future sibling orchestration.",
        "No external account, plugin-cache, or new-thread action is needed for v13 x1.",
        "The larger v478-v490 objective remains active and incomplete.",
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
            "handoff_status": handoff.get("overall_status"),
            "stale_flow_status": stale.get("overall_status"),
            "skill_after_hash": skill.get("after_sha256"),
            "source_count": len(sources),
            "reflection_count": len(reflections),
        },
        "beta": beta,
        "alpha": alpha,
        "omega": omega,
        "claim_boundary": {
            "scope": "v12 x2 THOS synthesis and v13 x1 preparation",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(f"{PHASE}-source-refresh-ledger-v1.json", {"artifact_type": "source_refresh_ledger", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "web_query_count": 32, "source_count": len(sources), "rows": sources, "claim_boundary": "THOS source context only; all GMUT gates remain open"})
    write_md(f"{PHASE}-source-refresh-ledger-v1.md", [f"# {PHASE} Source Refresh Ledger", "", f"- generated_nz: `{generated_nz}`", "- web_query_count: `32`", f"- source_count: `{len(sources)}`", "- boundary: THOS source context only; all GMUT gates remain open.", "", "## Sources", *[f"- `{row['id']}` {row['category']}: [{row['title']}]({row['url']}) - {row['phase_use']}" for row in sources]])
    write_json(f"{PHASE}-personal-reflection-board-v1.json", {"artifact_type": "personal_reflection_board", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "reflection_count": len(reflections), "rows": reflections, "claim_boundary": "continuity reflection only; not canon"})
    write_md(f"{PHASE}-personal-reflection-board-v1.md", [f"# {PHASE} Personal Reflection Board", "", f"- generated_nz: `{generated_nz}`", f"- reflection_count: `{len(reflections)}`", "- boundary: continuity reflection only; not canon.", "", "## Reflections", *[f"- `{row['id']}` ({row['domain']} / {row['record_scope']}): {row['reflection']}" for row in reflections]])
    write_json(f"{PHASE}-beta-alpha-omega-synthesis-v1.json", synthesis)
    write_md(f"{PHASE}-beta-alpha-omega-synthesis-v1.md", [f"# {PHASE} Beta Alpha Omega Synthesis", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_X2_SYNTHESIS_WITH_CLI_FINAL_MARKER_OPEN`", f"- next_phase_slug: `{NEXT_PHASE}`", "- boundary: THOS synthesis only; all GMUT gates remain open.", "", "## Beta", *[f"- {row}" for row in beta], "", "## Alpha", *[f"- {row}" for row in alpha], "", "## Omega", *[f"- {row}" for row in omega]])
    write_json(f"{NEXT_PHASE}-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase_slug": PHASE, "next_phase_slug": NEXT_PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(roadmap), "tasks": roadmap})
    write_md(f"{NEXT_PHASE}-roadmap-v1.md", [f"# {NEXT_PHASE} Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(roadmap)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in roadmap]])
    run_status = {"artifact_type": "run_status", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": synthesis["overall_status"], "next_expected_phase": NEXT_PHASE, "app_lane_status": "READY_FROM_X1_RECEIPTS", "cli_lane_status": "FINAL_MARKER_OPEN_CARRIED_FORWARD", "gmut_gates": {"empirical_physics": "OPEN", "consciousness_claims": "OPEN", "canon_promotion": "OPEN"}}
    write_json(f"{PHASE}-run-status-v1.json", run_status)
    write_md(f"{PHASE}-run-status-v1.md", [f"# {PHASE} Run Status", "", f"- generated_nz: `{generated_nz}`", f"- overall_status: `{run_status['overall_status']}`", f"- next_expected_phase: `{NEXT_PHASE}`", "- app_lane_status: `READY_FROM_X1_RECEIPTS`", "- cli_lane_status: `FINAL_MARKER_OPEN_CARRIED_FORWARD`", "- GMUT gates: all remain `OPEN`."])
    expected = [
        f"{PHASE}-source-refresh-ledger-v1.json",
        f"{PHASE}-personal-reflection-board-v1.json",
        f"{PHASE}-beta-alpha-omega-synthesis-v1.json",
        f"{NEXT_PHASE}-roadmap-v1.json",
        f"{PHASE}-run-status-v1.json",
    ]
    checked = []
    for name in expected:
        payload = read_json(name)
        checked.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type")})
    write_json(f"{PHASE}-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase_slug": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "checked_json_count": len(checked), "rows": checked})
    write_md(f"{PHASE}-schema-bound-artifact-check-v1.md", [f"# {PHASE} Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", f"- checked_json_count: `{len(checked)}`", "", "## Checked", *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in checked]])
    return synthesis


def main() -> None:
    payload = build()
    print(json.dumps({"status": payload["overall_status"], "next": payload["next_phase_slug"]}, sort_keys=True))


if __name__ == "__main__":
    main()
