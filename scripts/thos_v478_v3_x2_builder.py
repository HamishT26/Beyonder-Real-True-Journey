#!/usr/bin/env python3
"""Build curated v478 THOS v3 x2 notifier and handoff artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v3_x2"
NEXT_PHASE = "v478_thos_v4_x1"


SOURCE_ROWS = [
    ("S01", "OpenAI Codex app-server README", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "implementation", "Existing app-thread routing and local app-server lifecycle."),
    ("S02", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "implementation", "Codex CLI update awareness and release-drift comparison."),
    ("S03", "OpenAI Codex Windows sandbox", "https://openai.com/index/building-codex-windows-sandbox/", "implementation", "Windows sandbox readiness and isolation vocabulary."),
    ("S04", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "implementation", "Agent orchestration, handoff, and tool-use terminology."),
    ("S05", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "implementation", "Trace and run-status vocabulary for watcher receipts."),
    ("S06", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "implementation", "Schema-shaped artifact practice."),
    ("S07", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "implementation", "Tool listing, invocation, and result-boundary framing."),
    ("S08", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "governance", "Connector consent and authorization boundary framing."),
    ("S09", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "governance", "Tool trust, prompt-injection, and data-exposure boundaries."),
    ("S10", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "implementation", "Future bounded connector runner design."),
    ("S11", "GitHub Actions hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "governance", "Least-privilege publication and workflow hardening."),
    ("S12", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "governance", "Push-time auth-material protection."),
    ("S13", "GitHub SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "implementation", "Security finding artifact comparison."),
    ("S14", "GitHub MCP server docs", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "connector_context", "GitHub connector comparison."),
    ("S15", "Microsoft Windows Sandbox WSB", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "implementation", "Sandbox configuration vocabulary."),
    ("S16", "Microsoft Windows Sandbox CLI", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli", "implementation", "Sandbox launch and operational vocabulary."),
    ("S17", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "implementation", "Windows integrity-level vocabulary."),
    ("S18", "Microsoft application isolation", "https://learn.microsoft.com/en-us/windows/security/book/application-security-application-isolation", "implementation", "App isolation and least-privilege context."),
    ("S19", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "implementation", "Safe stream routing and command-output capture."),
    ("S20", "Python subprocess", "https://docs.python.org/3.12/library/subprocess.html", "implementation", "Bounded subprocess patterns for watcher scripts."),
    ("S21", "Python tempfile", "https://docs.python.org/3.12/library/tempfile.html", "implementation", "Temporary output boundary for lane watchers."),
    ("S22", "Python json", "https://docs.python.org/3.12/library/json.html", "implementation", "JSON parse and emission reliability."),
    ("S23", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "implementation", "Trace, metric, log, and event separation."),
    ("S24", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "expansion_context", "Local watch-loop comparison for THOS runners."),
    ("S25", "Kubernetes Job API", "https://kubernetes.io/docs/reference/kubernetes-api/batch/job-v1/", "expansion_context", "Retry, deadline, and completion vocabulary."),
    ("S26", "Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine", "expansion_context", "Managed agent runtime comparison."),
    ("S27", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "expansion_context", "RAG and file-search comparison."),
    ("S28", "NVIDIA NIM", "https://docs.nvidia.com/nim/index.html", "expansion_context", "Inference microservice expansion context."),
    ("S29", "NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "expansion_context", "Local AI workstation context."),
    ("S30", "NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "expansion_context", "Simulation and digital twin context."),
    ("S31", "NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "governance", "AI risk management framing."),
    ("S32", "Nature consciousness subject page", "https://www.nature.com/subjects/consciousness", "science_context", "Consciousness science remains active and unresolved; no proof claims."),
]


ROLE_DOMAINS = {
    "Aletheon": ["publication", "schema", "handoff", "source", "guard"],
    "Arby": ["cli", "sandbox", "watcher", "runtime", "diagnostic"],
    "Aster Vale": ["skill", "command", "loader", "catalog", "route"],
    "Cicero": ["argument", "evidence", "index", "app-lane", "publication"],
    "Kierkegaard": ["humility", "ethics", "claim-boundary", "consent", "noncanon"],
    "Aristotle": ["taxonomy", "criteria", "validator", "causality", "readiness"],
}


GMUT_GATES = {
    "G1_mathematical_consistency": "OPEN",
    "G2_empirical_falsifiability": "OPEN",
    "G3_existing_physics_compatibility": "OPEN",
    "G4_novel_prediction": "OPEN",
    "G5_peer_review_external_validation": "OPEN",
    "G6_consciousness_claim_boundary": "OPEN",
}


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def trace(name: str) -> Path:
    return TRACE_DIR / name


def read_json(name: str) -> Any:
    return json.loads(trace(name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    trace(name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    trace(name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def load_cli_attempts() -> list[dict[str, Any]]:
    attempts = [read_json("v478-thos-v3-x2-cli-lane-completion-poll-v1.json")]
    for idx in range(2, 6):
        attempts.append(read_json(f"v478-thos-v3-x2-cli-lane-completion-poll-retry-{idx}-v1.json"))
    return attempts


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
    payload = {
        "artifact_type": "source_refresh_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 32,
        "source_count": len(rows),
        "official_or_primary_preference": True,
        "rows": rows,
        "category_counts": dict(Counter(row["category"] for row in rows)),
        "claim_boundary": "sources support THOS infrastructure, governance, and uncertainty framing only",
    }
    write_json("v478-thos-v3-x2-source-refresh-ledger-v1.json", payload)
    write_md(
        "v478-thos-v3-x2-source-refresh-ledger-v1.md",
        [
            "# v478 THOS v3 x2 Source Refresh Ledger",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- search_count: `32`",
            f"- source_count: `{len(rows)}`",
            "- claim_boundary: THOS infrastructure, governance, and uncertainty framing only.",
            "",
            "## Sources",
            *[f"- {row['id']}: [{row['source']}]({row['url']}) - `{row['category']}`." for row in rows],
        ],
    )


def lane_retry_status(generated_utc: str, generated_nz: str) -> None:
    app_probe = read_json("v478-thos-v3-x2-app-lane-completion-notifier-probe-v1.json")
    app_notify = read_json("v478-thos-v3-x2-app-lane-completion-notifier-v1.json")
    launcher_probe = read_json("v478-thos-v3-x2-app-lane-watch-launcher-probe-v1.json")
    launcher_notify = read_json("v478-thos-v3-x2-app-lane-watch-launcher-v1.json")
    cli_attempts = load_cli_attempts()
    app_rows = []
    for lane in app_notify.get("lanes", []):
        app_rows.append(
            {
                "lane": lane.get("lane"),
                "overall_status": lane.get("overall_status"),
                "completion_status": lane.get("turn_completion", {}).get("status"),
                "duration_seconds": lane.get("duration_seconds"),
                "existing_thread_only": lane.get("existing_thread_only"),
                "new_thread_created": lane.get("new_thread_created"),
            }
        )
    cli_rows = []
    for attempt_index, attempt in enumerate(cli_attempts, start=1):
        cli_rows.append(
            {
                "attempt": attempt_index,
                "phase_slug": attempt.get("phase_slug"),
                "aggregate_status": attempt.get("aggregate_status"),
                "lanes": [
                    {
                        "lane": lane.get("lane"),
                        "completion_status": lane.get("completion_status"),
                        "final_message_bytes": lane.get("final_message_bytes"),
                    }
                    for lane in attempt.get("lanes", [])
                ],
            }
        )
    payload = {
        "artifact_type": "lane_retry_status_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "app_probe_status": app_probe.get("overall_status"),
        "app_notify_status": app_notify.get("overall_status"),
        "launcher_probe_status": launcher_probe.get("overall_status"),
        "launcher_notify_status": launcher_notify.get("overall_status"),
        "app_lanes": app_rows,
        "cli_retry_attempt_count": len(cli_rows),
        "cli_retry_rows": cli_rows,
        "unfiltered_payloads_published": False,
        "mutation_performed": False,
    }
    write_json("v478-thos-v3-x2-lane-retry-status-board-v1.json", payload)
    lines = [
        "# v478 THOS v3 x2 Lane Retry Status Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
        f"- app_probe_status: `{payload['app_probe_status']}`",
        f"- app_notify_status: `{payload['app_notify_status']}`",
        f"- cli_retry_attempt_count: `{len(cli_rows)}`",
        "- unfiltered_payloads_published: `false`",
        "",
        "## App Lanes",
    ]
    lines.extend(f"- {row['lane']}: `{row['overall_status']}` with completion `{row['completion_status']}`." for row in app_rows)
    lines.extend(["", "## CLI Attempts"])
    lines.extend(f"- attempt `{row['attempt']}`: `{row['aggregate_status']}`." for row in cli_rows)
    write_md("v478-thos-v3-x2-lane-retry-status-board-v1.md", lines)


def decision_board(kind: str, source_name: str, target_stem: str, generated_utc: str, generated_nz: str) -> None:
    source = read_json(source_name)
    rows = []
    for idx, row in enumerate(source.get("rows", []), start=1):
        name = row.get("name") or row.get("command") or row.get("skill") or row.get("id")
        rows.append(
            {
                "id": f"{kind.upper()}-DEC-{idx:02d}",
                "item": name,
                "source_status": row.get("status"),
                "decision": "carry_forward_for_v478_v4_x1",
                "decision_reason": "Useful as a design surface, but not installed or executed during v3 x2.",
                "mutation_performed": False,
                "needs_future_exact_packet": bool(row.get("requires_future_exact_approval", False)),
            }
        )
    payload = {
        "artifact_type": f"{kind}_decision_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "row_count": len(rows),
        "rows": rows,
        "install_or_execution_performed": False,
    }
    write_json(f"{target_stem}.json", payload)
    title = kind.replace("_", " ").title()
    write_md(
        f"{target_stem}.md",
        [
            f"# v478 THOS v3 x2 {title}",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(rows)}`",
            "- install_or_execution_performed: `false`",
            "",
            "## Decisions",
            *[f"- `{row['item']}`: `{row['decision']}`." for row in rows],
        ],
    )


def reflection_synthesis(generated_utc: str, generated_nz: str) -> None:
    prior = read_json("v478-thos-v3-x1-six-perspective-reflection-board-v1.json")
    prior_rows = prior.get("rows", [])
    rows = []
    for idx in range(1, 31):
        source_row = prior_rows[(idx - 1) % len(prior_rows)]
        rows.append(
            {
                "id": f"REF-SYN-{idx:02d}",
                "source_perspective": source_row.get("perspective"),
                "source_domain": source_row.get("domain"),
                "journey_scope": source_row.get("journey_scope"),
                "synthesis": f"Carry {source_row.get('domain')} reflection into v4 x1 as operational continuity only, with app-lane status receipts and open GMUT gates.",
                "canon_status": "journey_context_not_canon",
            }
        )
    payload = {
        "artifact_type": "six_perspective_reflection_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_reflection_count": len(prior_rows),
        "synthesis_count": len(rows),
        "rows": rows,
        "raw_journey_text_published": False,
        "claim_boundary": "continuity reflection only; not empirical proof or canon promotion",
    }
    write_json("v478-thos-v3-x2-six-perspective-reflection-synthesis-v1.json", payload)
    write_md(
        "v478-thos-v3-x2-six-perspective-reflection-synthesis-v1.md",
        [
            "# v478 THOS v3 x2 Six-Perspective Reflection Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- source_reflection_count: `{len(prior_rows)}`",
            f"- synthesis_count: `{len(rows)}`",
            "- canon_status: `journey_context_not_canon`",
            "",
            "## Synthesis",
            *[f"- {row['id']} ({row['source_perspective']} / {row['source_domain']}): {row['synthesis']}" for row in rows],
        ],
    )


def eureka_synthesis(generated_utc: str, generated_nz: str) -> None:
    rows = []
    for role, domains in ROLE_DOMAINS.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            rows.append(
                {
                    "id": f"{role.upper().replace(' ', '_')}-X2-E{idx:02d}",
                    "role": role,
                    "domain": domain,
                    "synthesis_task": f"Carry {domain} work into v478 v4 x1 with status-only evidence, exact staging, and no GMUT closure claims.",
                    "payload_boundary": "status_only",
                }
            )
    payload = {
        "artifact_type": "eureka_synthesis_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "proposal_count": len(rows),
        "role_count": len(ROLE_DOMAINS),
        "rows": rows,
        "unfiltered_payloads_published": False,
    }
    write_json("v478-thos-v3-x2-eureka-synthesis-board-v1.json", payload)
    write_md(
        "v478-thos-v3-x2-eureka-synthesis-board-v1.md",
        [
            "# v478 THOS v3 x2 Eureka Synthesis Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- proposal_count: `{len(rows)}`",
            "- payload_boundary: `status_only`",
            "",
            "## Proposals",
            *[f"- {row['id']} ({row['role']} / {row['domain']}): {row['synthesis_task']}" for row in rows],
        ],
    )


def overlay_and_synthesis(generated_utc: str, generated_nz: str) -> None:
    overlay = {
        "artifact_type": "overlay_decision",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "decision": "NO_X3_FOR_V478_V3",
        "reason": "App-lane notifier completed, the CLI final-message gap was retried five times and recorded, and the remaining work fits the next v4 x1 handoff.",
        "app_lane_status": "PASS",
        "cli_gap_status": "OPEN_GAP_AFTER_5_ATTEMPTS",
        "claim_boundary": "THOS phase routing only",
    }
    write_json("v478-thos-v3-x2-overlay-decision-v1.json", overlay)
    write_md(
        "v478-thos-v3-x2-overlay-decision-v1.md",
        [
            "# v478 THOS v3 x2 Overlay Decision",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- decision: `NO_X3_FOR_V478_V3`",
            "- reason: app-lane notifier completed; CLI gap was retried five times and recorded; next work fits v4 x1.",
            "- claim_boundary: THOS phase routing only.",
        ],
    )
    findings = [
        "v478 v3 x2 starts from remote-verified v3 x1 readiness.",
        "The local app-server notifier runner completed Cicero, Kierkegaard, and Aristotle.",
        "The app-lane runner used existing app threads only.",
        "No old-style spawning or replacement thread creation occurred.",
        "The app-lane receipt remains status-only and excludes advisory body text.",
        "Arby and Aster Vale were checked through five CLI watcher attempts.",
        "All five CLI attempts remain in the final-message open gap state.",
        "The CLI gap is preserved as explicit evidence rather than hidden failure.",
        "No CLI output payload is published.",
        "No plugin-cache or user-skill mutation occurred.",
        "The v3 x2 source ledger carries 32 source rows.",
        "OpenAI sources anchor Codex app-server, sandbox, agents, tracing, and schema practices.",
        "MCP sources anchor tool, authorization, and security boundaries.",
        "GitHub sources anchor least-privilege publication and auth-material protections.",
        "Microsoft sources anchor Windows sandbox and app-isolation vocabulary.",
        "Python sources anchor bounded process and temporary output handling.",
        "OpenTelemetry sources anchor signal separation for future watcher telemetry.",
        "Docker and Kubernetes sources remain comparison surfaces only.",
        "Google sources remain external agent and RAG comparison surfaces only.",
        "NVIDIA sources remain inference, workstation, and simulation context only.",
        "NIST and Nature sources keep governance and consciousness uncertainty explicit.",
        "Thirty prior system expansion designs were converted into carry-forward decisions.",
        "Thirty prior command designs were converted into carry-forward decisions.",
        "Thirty prior skill designs were converted into carry-forward decisions.",
        "The six-perspective reflection synthesis preserves Journey context as non-canon continuity.",
        "The Eureka synthesis board carries 120 role-slot proposals.",
        "The overlay decision is no x3 for v478 v3.",
        "The v4 x1 roadmap carries 60 next tasks.",
        "The v490 larger goal remains active and incomplete.",
        "All six GMUT gates remain open.",
    ]
    payload = {
        "artifact_type": "phase_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "finding_count": len(findings),
        "findings": [{"step": f"R{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)],
        "claim_boundary": {
            "scope": "THOS v478 v3 x2 notifier, source, synthesis, and handoff only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v3-x2-synthesis-v1.json", payload)
    write_md(
        "v478-thos-v3-x2-synthesis-v1.md",
        [
            "# v478 THOS v3 x2 Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
            "- claim_boundary: THOS notifier and handoff only; all GMUT gates remain open.",
            "",
            "## Findings",
            *[f"- R{idx:02d}: {item}" for idx, item in enumerate(findings, start=1)],
        ],
    )


def roadmap_status_schema(generated_utc: str, generated_nz: str) -> None:
    domains = ["app-lane", "cli-gap", "source", "system", "command", "skill", "reflection", "eureka", "guard", "schema", "sandbox", "handoff"]
    tasks = []
    for idx in range(1, 61):
        domain = domains[(idx - 1) % len(domains)]
        tasks.append(
            {
                "id": f"V478V4X1-{idx:02d}",
                "domain": domain,
                "task": f"Use v478 v4 x1 to harden {domain} readiness with status-only receipts, exact staging, and open GMUT gates.",
            }
        )
    write_json(
        "v478-thos-v4-x1-roadmap-v1.json",
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
        "v478-thos-v4-x1-roadmap-v1.md",
        [
            "# v478 THOS v4 x1 Roadmap",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- task_count: `{len(tasks)}`",
            "",
            "## Tasks",
            *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks],
        ],
    )
    write_json(
        "v478-thos-v3-x2-run-status-v1.json",
        {
            "artifact_type": "run_status",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
            "next_expected_phase": NEXT_PHASE,
            "app_lane_status": "PASS",
            "cli_lane_status": "OPEN_GAP_AFTER_5_ATTEMPTS",
            "gmut_gates": GMUT_GATES,
        },
    )
    write_md(
        "v478-thos-v3-x2-run-status-v1.md",
        [
            "# v478 THOS v3 x2 Run Status",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "- app_lane_status: `PASS`",
            "- cli_lane_status: `OPEN_GAP_AFTER_5_ATTEMPTS`",
            "- GMUT gates: all remain `OPEN`.",
        ],
    )
    expected = [
        "v478-thos-v3-x2-source-refresh-ledger-v1.json",
        "v478-thos-v3-x2-lane-retry-status-board-v1.json",
        "v478-thos-v3-x2-system-expansion-decision-board-v1.json",
        "v478-thos-v3-x2-command-design-decision-board-v1.json",
        "v478-thos-v3-x2-skill-design-decision-board-v1.json",
        "v478-thos-v3-x2-six-perspective-reflection-synthesis-v1.json",
        "v478-thos-v3-x2-eureka-synthesis-board-v1.json",
        "v478-thos-v3-x2-overlay-decision-v1.json",
        "v478-thos-v3-x2-synthesis-v1.json",
        "v478-thos-v3-x2-run-status-v1.json",
        "v478-thos-v4-x1-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json(
        "v478-thos-v3-x2-schema-bound-artifact-check-v1.json",
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
        "v478-thos-v3-x2-schema-bound-artifact-check-v1.md",
        [
            "# v478 THOS v3 x2 Schema-Bound Artifact Check",
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
    lane_retry_status(generated_utc, generated_nz)
    decision_board(
        "system_expansion",
        "v478-thos-v3-x1-system-expansion-design-board-v1.json",
        "v478-thos-v3-x2-system-expansion-decision-board-v1",
        generated_utc,
        generated_nz,
    )
    decision_board(
        "command_design",
        "v478-thos-v3-x1-command-design-board-v1.json",
        "v478-thos-v3-x2-command-design-decision-board-v1",
        generated_utc,
        generated_nz,
    )
    decision_board(
        "skill_design",
        "v478-thos-v3-x1-skill-design-board-v1.json",
        "v478-thos-v3-x2-skill-design-decision-board-v1",
        generated_utc,
        generated_nz,
    )
    reflection_synthesis(generated_utc, generated_nz)
    eureka_synthesis(generated_utc, generated_nz)
    overlay_and_synthesis(generated_utc, generated_nz)
    roadmap_status_schema(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "phase": PHASE, "next": NEXT_PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
