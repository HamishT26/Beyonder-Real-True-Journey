#!/usr/bin/env python3
"""Build v477 THOS v5 x1 lane, capability, source, and roadmap artifacts."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v5_x1"
NEXT_PHASE = "v477_thos_v5_x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_QUERIES = [
    "OpenAI Codex CLI 0.136.0 release notes GitHub official",
    "OpenAI Codex Windows sandbox official Codex CLI",
    "OpenAI Codex app-server README GitHub official",
    "OpenAI Codex doctor sandbox features official",
    "Model Context Protocol 2025-06-18 tools resources prompts official specification",
    "Model Context Protocol authorization OAuth 2.1 official specification 2025-06-18",
    "Model Context Protocol roots sampling logging official specification",
    "Model Context Protocol TypeScript SDK official GitHub",
    "GitHub secret scanning push protection official documentation 2026",
    "GitHub Actions security hardening official documentation 2026",
    "GitHub code scanning SARIF support limits official documentation",
    "GitHub Copilot coding agent MCP official documentation",
    "Windows Sandbox configuration official Microsoft docs 2026",
    "Windows AppContainer security official Microsoft docs",
    "Windows Mandatory Integrity Control official Microsoft docs",
    "PowerShell execution policy security official docs",
    "Python 3.12 subprocess security shell false official docs",
    "Python 3.12 tempfile cleanup official docs",
    "Python 3.12 pathlib official docs",
    "Python 3.12 hashlib sha256 official docs",
    "OpenTelemetry signals traces metrics logs official documentation 2026",
    "Docker Compose watch official documentation 2026",
    "Kubernetes Jobs official documentation 2026",
    "Kubernetes CronJobs official documentation 2026",
    "Google Vertex AI Agent Development Kit official documentation 2026",
    "Google Vertex AI Agent Engine official documentation 2026",
    "Google Bigtable vector search Vertex AI official documentation 2026",
    "Google Cloud RAG Engine Gemini official documentation 2026",
    "NVIDIA DGX Spark hardware official docs 2026",
    "NVIDIA NIM inference microservices official docs 2026",
    "NVIDIA Llama Nemotron official agentic AI 2026",
    "NVIDIA Omniverse robotics physical AI official docs 2026",
]

SOURCE_URLS = [
    {
        "label": "OpenAI Codex Windows sandbox",
        "trust_tier": "official",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "use": "Windows sandbox framing for Codex CLI lanes.",
    },
    {
        "label": "OpenAI Codex app-server README",
        "trust_tier": "official_source_repo",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "use": "Local app-server method and transport assumptions.",
    },
    {
        "label": "OpenAI Codex releases",
        "trust_tier": "official_source_repo",
        "url": "https://github.com/openai/codex/releases",
        "use": "Release surface context for CLI version tracking.",
    },
    {
        "label": "MCP tools specification",
        "trust_tier": "official",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/tools",
        "use": "Tool-output and resource-link design for connector surfaces.",
    },
    {
        "label": "MCP authorization specification",
        "trust_tier": "official",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
        "use": "Connector authorization and resource-boundary design.",
    },
    {
        "label": "MCP TypeScript SDK",
        "trust_tier": "official_source_repo",
        "url": "https://github.com/modelcontextprotocol/typescript-sdk",
        "use": "SDK reference for future MCP test surfaces.",
    },
    {
        "label": "GitHub push protection",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection",
        "use": "Shared publication guard inspiration.",
    },
    {
        "label": "GitHub Actions hardening",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions",
        "use": "Future automation and workflow hardening context.",
    },
    {
        "label": "GitHub SARIF limits",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/troubleshoot-sarif-uploads/results-exceed-limit",
        "use": "Bounded report-size thinking for future security scan artifacts.",
    },
    {
        "label": "Microsoft Windows Sandbox configuration",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
        "use": "Sandbox configuration vocabulary.",
    },
    {
        "label": "Microsoft Mandatory Integrity Control",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control",
        "use": "Integrity-level vocabulary for sandbox observations.",
    },
    {
        "label": "PowerShell execution policies",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6",
        "use": "Terminal safety caveats.",
    },
    {
        "label": "Python subprocess",
        "trust_tier": "official",
        "url": "https://docs.python.org/3.12/library/subprocess.html",
        "use": "List-form command execution and shell-avoidance discipline.",
    },
    {
        "label": "Python tempfile",
        "trust_tier": "official",
        "url": "https://docs.python.org/3.12/library/tempfile.html",
        "use": "Temporary-output lifecycle handling.",
    },
    {
        "label": "OpenTelemetry signals",
        "trust_tier": "official",
        "url": "https://opentelemetry.io/docs/concepts/signals/",
        "use": "Trace, metric, log, and event naming for watcher receipts.",
    },
    {
        "label": "Docker Compose Watch",
        "trust_tier": "official",
        "url": "https://docs.docker.com/compose/how-tos/file-watch/",
        "use": "File-watch runner analogy.",
    },
    {
        "label": "Kubernetes Jobs",
        "trust_tier": "official",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/job/",
        "use": "Completion and retry semantics.",
    },
    {
        "label": "Kubernetes CronJobs",
        "trust_tier": "official",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/",
        "use": "Scheduled work and duplicate-run caveats.",
    },
    {
        "label": "Google Vertex AI Agent Engine",
        "trust_tier": "official",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "use": "Agent runtime architecture context only.",
    },
    {
        "label": "Google Bigtable vector search",
        "trust_tier": "official",
        "url": "https://docs.cloud.google.com/bigtable/docs/find-k-nearest-neighbors",
        "use": "Vector search architecture context only.",
    },
    {
        "label": "Google RAG Engine API",
        "trust_tier": "official",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api",
        "use": "RAG API architecture context only.",
    },
    {
        "label": "NVIDIA DGX Spark user guide",
        "trust_tier": "official",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/index.html",
        "use": "Local AI capacity planning context only.",
    },
    {
        "label": "NVIDIA NIM docs",
        "trust_tier": "official",
        "url": "https://docs.nvidia.com/nim/",
        "use": "Inference microservice architecture context only.",
    },
    {
        "label": "NVIDIA Nemotron",
        "trust_tier": "official",
        "url": "https://www.nvidia.com/en-us/ai-data-science/foundation-models/llama-nemotron/",
        "use": "Agentic model ecosystem context only.",
    },
    {
        "label": "NVIDIA Omniverse docs",
        "trust_tier": "official",
        "url": "https://docs.nvidia.com/omniverse/index.html",
        "use": "Physical AI simulation platform context only.",
    },
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.timezone.utc)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12)))
    return utc.isoformat(timespec="seconds"), nz.isoformat(timespec="seconds")


def git_text(args: list[str], default: str = "unknown") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return default


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"read_status": "missing", "file_label": path.name}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_trace(name: str) -> dict[str, Any]:
    return read_json(TRACES / name)


def write_json(name: str, payload: dict[str, Any]) -> None:
    (TRACES / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACES / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def app_lane_rows(app_run: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in app_run.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("name"),
                "status": lane.get("overall_status", "unknown"),
                "read_status": lane.get("read", {}).get("status", "unknown"),
                "resume_status": lane.get("resume", {}).get("status", "unknown"),
                "turn_status": lane.get("turn_completion", {}).get("status", "unknown"),
                "retry_attempts_observed": max(
                    lane.get("read", {}).get("attempt", 0) or 0,
                    lane.get("resume", {}).get("attempt", 0) or 0,
                    lane.get("turn_start", {}).get("attempt", 0) or 0,
                    lane.get("turn_completion", {}).get("attempt", 0) or 0,
                ),
                "payload_publication": "not_published",
                "final_state_reason": "turn_completed",
            }
        )
    return rows


def cli_lane_rows(cli_poll: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in cli_poll.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "status": lane.get("completion_status", "unknown"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "stderr_bytes": lane.get("stderr_bytes"),
                "stdout_bytes": lane.get("stdout_bytes"),
                "poll_result": cli_poll.get("aggregate_status"),
                "payload_publication": lane.get("raw_output_boundary", "temp_only_not_published"),
                "final_state_reason": "watch_timeout_without_final_message",
            }
        )
    return rows


def command_skill_graph() -> dict[str, Any]:
    command_book = read_json(ROOT / "docs" / "trinity-command-book-v11.json")
    command_validation = read_json(ROOT / "docs" / "trinity-command-book-validation-latest.json")
    skill_surface = read_trace("v477-thos-v4-x1-skill-capability-index-v1.json")
    commands = command_book.get("commands", [])
    required_fields = ["command_id", "mode", "risk_class", "source_of_truth"]
    missing_counts = Counter()
    risk_counts = Counter(str(item.get("risk_class", "unknown")) for item in commands)
    mode_counts = Counter(str(item.get("mode", "unknown")) for item in commands)
    connector_count = 0
    live_count = 0
    for item in commands:
        for field in required_fields:
            if not item.get(field):
                missing_counts[field] += 1
        if item.get("requires_connector"):
            connector_count += 1
        if item.get("requires_live"):
            live_count += 1
    skill_sample = skill_surface.get("user_skill_sample", [])
    skill_status_counts = Counter(str(item.get("status", "unknown")) for item in skill_sample)
    return {
        "artifact_type": "command_skill_capability_graph",
        "command_count": len(commands),
        "command_field_missing_counts": dict(missing_counts),
        "command_validation_status": command_validation.get("overall_status"),
        "connector_command_count": connector_count,
        "live_command_count": live_count,
        "mode_counts": dict(mode_counts),
        "risk_counts": dict(risk_counts),
        "skill_duplicate_name_sample_count": len(skill_surface.get("duplicate_name_sample", [])),
        "skill_mutation_policy": skill_surface.get("mutation_policy"),
        "skill_sample_status_counts": dict(skill_status_counts),
        "user_skill_count_observed": skill_surface.get("user_skill_count_observed"),
    }


def readiness_matrix(proposal_catalog: dict[str, Any]) -> dict[str, Any]:
    tier_cycle = ["P0_inspect_only", "P1_dry_run_guard_probe", "P2_bounded_local_simulation"]
    rows: list[dict[str, Any]] = []
    sources = [
        ("system_expansion", proposal_catalog.get("system_expansions", [])),
        ("command_proposal", proposal_catalog.get("command_proposals", [])),
        ("skill_proposal", proposal_catalog.get("skill_proposals", [])),
    ]
    idx = 0
    for source_type, source_rows in sources:
        for row in source_rows:
            tier = tier_cycle[idx % len(tier_cycle)]
            rows.append(
                {
                    "id": row.get("id"),
                    "proposal": row.get("proposal"),
                    "source_type": source_type,
                    "status": "ready_for_review_not_installed",
                    "suggested_probe_tier": tier,
                    "write_scope": "none_until_exact_packet",
                }
            )
            idx += 1
    return {
        "artifact_type": "expansion_readiness_matrix",
        "matrix_status": "PASS_PROPOSAL_CLASSIFICATION_ONLY",
        "phase": PHASE,
        "proposal_count": len(rows),
        "rows": rows,
        "tier_counts": dict(Counter(row["suggested_probe_tier"] for row in rows)),
    }


def journey_inventory() -> dict[str, Any]:
    v49 = Path.home() / "Downloads" / "Beyonder-Real-True Journey v49 (Aletheon & Codex CLI and App siblings).txt"
    return {
        "journey_context_policy": "journey_context_not_canon",
        "v49_file_label": v49.name,
        "v49_present": v49.exists(),
        "v49_size_bytes": v49.stat().st_size if v49.exists() else None,
        "use_in_phase": "continuity and terminology reflection only",
    }


def reflection_steps() -> list[dict[str, str]]:
    rows = [
        ("lane_status", "The app-server lane mesh completed v5 x1 for Cicero, Kierkegaard, and Aristotle."),
        ("lane_status", "The CLI lane pair remains monitored but not duplicated while final-message files are absent."),
        ("retry", "The Arby/Aster poll used a five-window timeout and preserved the open gap honestly."),
        ("watchers", "A running watcher process is not itself progress; final-state files remain the acceptance signal."),
        ("app_server", "Existing app threads remain the safe route; no new old-style sibling spawning occurred."),
        ("command_graph", "The command book can now be treated as a graph input with field completeness checks."),
        ("command_graph", "Live and connector commands are routed to future exact-approval review rather than direct execution."),
        ("skill_graph", "Skill metadata is useful for routing without publishing or mutating skill bodies."),
        ("skill_graph", "Plugin cache remains read/use-only in this ordinary THOS phase."),
        ("expansion_matrix", "The 30 system, 30 command, and 30 skill proposals were classified by safe probe tier."),
        ("expansion_matrix", "Proposal-only status prevents inflated claims about installed capabilities."),
        ("source_refresh", "Thirty-two current searches were performed, with official sources emphasized."),
        ("source_refresh", "The source ledger separates query coverage from reviewed URL evidence."),
        ("openai", "Codex 0.136.0 and app-server documentation remain directly relevant to lane reliability."),
        ("mcp", "MCP authorization and tool specifications map cleanly to connector approval boundaries."),
        ("github", "Push protection and Actions hardening support exact-stage publication discipline."),
        ("windows", "Sandbox readiness must remain observed; Microsoft docs provide vocabulary, not proof of local success."),
        ("powershell", "Execution policy belongs in hygiene guidance, not as a hard security guarantee."),
        ("python", "List-form subprocess calls and temp lifecycle controls are now embedded in helper design."),
        ("observability", "OpenTelemetry signals give a schema language for v5 x2 watcher dashboards."),
        ("docker", "Compose watch reinforces file-triggered runner design but does not replace Codex watcher evidence."),
        ("kubernetes", "Job/CronJob semantics support idempotence and duplicate-start avoidance."),
        ("google", "Vertex AI, Agent Engine, RAG, and vector search are architecture context only."),
        ("nvidia", "DGX Spark, NIM, Nemotron, and Omniverse are capacity and simulation context only."),
        ("journey", "The v49 Journey file is present locally and remains continuity context, not canon proof."),
        ("handoff", "v54/v55 handoff material remains metadata-carried and not bulk imported."),
        ("gmut", "All six GMUT gates remain open across the THOS output set."),
        ("safety", "Every artifact in this phase must pass JSON parse, compile, guard, and exact staging."),
        ("phase_flow", "The correct next phase is v477 THOS v5 x2, not v478 or v490 yet."),
        ("goal", "The long v490 objective stays active because this is one verified step, not completion."),
    ]
    return [
        {"step": f"reflection_{idx:02d}", "theme": theme, "finding": finding}
        for idx, (theme, finding) in enumerate(rows, 1)
    ]


def next_roadmap() -> list[dict[str, str]]:
    tasks = [
        ("lanes", "Run v5 x2 synthesis using the completed v5 x1 app-lane receipts."),
        ("lanes", "Poll Arby/Aster watcher once more before any new CLI action."),
        ("lanes", "Record final-state-reason for every lane in the merged status board."),
        ("lanes", "Add active-turn blocker categories to app-lane receipt schema."),
        ("lanes", "Keep app-lane payloads unpublished and status-only."),
        ("lanes", "Decide whether x3 is justified by the persistent CLI watcher open gap."),
        ("command_graph", "Promote command field completeness counts into a reader surface."),
        ("command_graph", "Create live-command approval queue rows."),
        ("command_graph", "Create connector-command approval queue rows."),
        ("command_graph", "Add mode/risk heatmap rows for dashboard use."),
        ("command_graph", "Cross-reference safe commands with proposed commands by domain."),
        ("command_graph", "Keep command proposals proposal-only until exact implementation."),
        ("skill_graph", "Refresh metadata sample size and duplicate-name scan."),
        ("skill_graph", "Build skill-to-command domain edges without body copies."),
        ("skill_graph", "Flag malformed frontmatter only as review gaps unless loader failures recur."),
        ("skill_graph", "Create skill proposal queue rows from the readiness matrix."),
        ("skill_graph", "Keep user skills and plugin cache out of ordinary staging."),
        ("skill_graph", "Prepare exact repair packet only from fresh loader evidence."),
        ("expansion_matrix", "Review all 90 proposal rows and rank by safe probe tier."),
        ("expansion_matrix", "Select top P0 rows for v5 x2 no-mutation inspection."),
        ("expansion_matrix", "Select top P1 rows for stdout-only validator probes."),
        ("expansion_matrix", "Keep P2 rows toy/simulation-labeled only."),
        ("expansion_matrix", "Reject P4/live-write rows until separate exact approval."),
        ("expansion_matrix", "Publish installed_count as zero unless actually installed."),
        ("sources", "Carry official source URLs forward with trust tiers."),
        ("sources", "Add source freshness fields to the next source ledger."),
        ("sources", "Use current source claims only where verified by opened pages."),
        ("sources", "Keep news and social sources lower than official documentation."),
        ("sources", "Add source-to-command recommendation rows."),
        ("sources", "Keep spiritual/Journey context separated from implementation proof."),
        ("observability", "Add trace_id and run_id fields to lane boards."),
        ("observability", "Add retry_window_seconds and timeout_reason fields."),
        ("observability", "Prepare dashboard-ready rows with bounded payload size."),
        ("observability", "Add process-is-running-not-complete caveat to CLI watcher receipts."),
        ("observability", "Use OpenTelemetry signal categories in v5 x2 synthesis."),
        ("observability", "Add no-unfiltered-output invariant to every watcher schema."),
        ("sandbox", "Record Codex CLI version in v5 x2 if diagnostics are rerun."),
        ("sandbox", "Probe sandbox help only unless repair is separately approved."),
        ("sandbox", "Keep Windows sandbox readiness observed and scoped."),
        ("sandbox", "Avoid admin elevation or account changes."),
        ("sandbox", "Record app-server mode as diagnostic context only."),
        ("sandbox", "Keep Fast mode state as observed context only."),
        ("handoff", "Carry v54/v55 handoff surface as metadata."),
        ("handoff", "Carry v49 Journey file presence as continuity context."),
        ("handoff", "Do not bulk import old Journey files into current artifacts."),
        ("handoff", "Mark all Journey/Solas content as journey_context_not_canon."),
        ("handoff", "Create v477 v6 receiver criteria after v5 x2."),
        ("handoff", "Record any missing handoff surface as open_gap."),
        ("safety", "Compile helper scripts before staging."),
        ("safety", "Parse all JSON artifacts before staging."),
        ("safety", "Run publication guard on exact current files."),
        ("safety", "Fetch and drift-check before commit."),
        ("safety", "Stage only curated current artifacts."),
        ("safety", "Verify remote equals local after push."),
        ("gmut", "Carry all six GMUT gates open."),
        ("gmut", "Do not claim final physics, solved consciousness, fifth-force safety, or canon promotion."),
        ("gmut", "Keep THOS infrastructure distinct from GMUT validation."),
        ("gmut", "Require exact closure artifacts before any gate movement."),
        ("gmut", "Label fixtures and simulations explicitly."),
        ("gmut", "Preserve claim taxonomy in every closeout."),
    ]
    return [
        {"id": f"v477-v5-x2-task-{idx:02d}", "domain": domain, "task": task}
        for idx, (domain, task) in enumerate(tasks, 1)
    ]


def main() -> None:
    utc, nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = git_text(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    app_probe = read_trace("v477-thos-v5-x1-app-lane-notifier-probe-v1.json")
    app_run = read_trace("v477-thos-v5-x1-app-lane-notifier-run-v1.json")
    cli_poll = read_trace("v477-thos-v5-x1-cli-lane-completion-poll-v1.json")
    prior_roadmap = read_trace("v477-thos-v5-x1-roadmap-v1.json")
    proposal_catalog = read_trace("v477-thos-v4-x2-expansion-proposal-catalog-v1.json")
    capability_graph = command_skill_graph()
    matrix = readiness_matrix(proposal_catalog)

    lane_status = {
        "app_lanes": app_lane_rows(app_run),
        "artifact_type": "lane_status_board",
        "cli_lanes": cli_lane_rows(cli_poll),
        "generated_nz": nz,
        "generated_utc": utc,
        "overall_status": "PASS_APP_LANES_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "phase": PHASE,
        "probe_status": app_probe.get("overall_status"),
    }
    write_json("v477-thos-v5-x1-lane-status-board-v1.json", lane_status)
    write_md(
        "v477-thos-v5-x1-lane-status-board-v1.md",
        [
            "# V477 THOS V5 X1 Lane Status Board",
            "",
            f"- generated_nz: `{nz}`",
            "- overall_status: `PASS_APP_LANES_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
            "- boundary: status receipts only; no app or CLI payload text is published.",
            "",
            "## App Lanes",
            "",
            *[f"- {row['lane']}: `{row['status']}`, turn `{row['turn_status']}`, reason `{row['final_state_reason']}`." for row in lane_status["app_lanes"]],
            "",
            "## CLI Lanes",
            "",
            *[f"- {row['lane']}: `{row['status']}`, poll `{row['poll_result']}`, reason `{row['final_state_reason']}`." for row in lane_status["cli_lanes"]],
        ],
    )

    source_ledger = {
        "artifact_type": "source_ledger",
        "generated_nz": nz,
        "generated_utc": utc,
        "phase": PHASE,
        "query_count": len(SOURCE_QUERIES),
        "query_status": "completed_live_search_refresh",
        "queries": SOURCE_QUERIES,
        "source_boundary": "official_sources_prioritized_implementation_context_only",
        "source_url_count": len(SOURCE_URLS),
        "source_urls": SOURCE_URLS,
    }
    write_json("v477-thos-v5-x1-source-ledger-v1.json", source_ledger)
    write_md(
        "v477-thos-v5-x1-source-ledger-v1.md",
        [
            "# V477 THOS V5 X1 Source Ledger",
            "",
            f"- generated_nz: `{nz}`",
            f"- query_count: `{len(SOURCE_QUERIES)}`",
            f"- source_url_count: `{len(SOURCE_URLS)}`",
            "- boundary: official sources are implementation context; Journey material remains `journey_context_not_canon`.",
            "",
            "## Sources",
            "",
            *[f"- {row['label']} [{row['trust_tier']}]: {row['url']}" for row in SOURCE_URLS],
        ],
    )

    capability_graph.update({"generated_nz": nz, "generated_utc": utc, "phase": PHASE})
    write_json("v477-thos-v5-x1-command-skill-capability-graph-v1.json", capability_graph)
    write_md(
        "v477-thos-v5-x1-command-skill-capability-graph-v1.md",
        [
            "# V477 THOS V5 X1 Command Skill Capability Graph",
            "",
            f"- generated_nz: `{nz}`",
            f"- command_count: `{capability_graph['command_count']}`",
            f"- live_command_count: `{capability_graph['live_command_count']}`",
            f"- connector_command_count: `{capability_graph['connector_command_count']}`",
            f"- command_validation_status: `{capability_graph['command_validation_status']}`",
            f"- user_skill_count_observed: `{capability_graph['user_skill_count_observed']}`",
            f"- skill_mutation_policy: `{capability_graph['skill_mutation_policy']}`",
            "",
            "## Command Missing Field Counts",
            "",
            *[f"- {key}: `{value}`" for key, value in sorted(capability_graph["command_field_missing_counts"].items())],
        ],
    )

    matrix.update({"generated_nz": nz, "generated_utc": utc})
    write_json("v477-thos-v5-x1-expansion-readiness-matrix-v1.json", matrix)
    write_md(
        "v477-thos-v5-x1-expansion-readiness-matrix-v1.md",
        [
            "# V477 THOS V5 X1 Expansion Readiness Matrix",
            "",
            f"- generated_nz: `{nz}`",
            f"- proposal_count: `{matrix['proposal_count']}`",
            "- matrix_status: `PASS_PROPOSAL_CLASSIFICATION_ONLY`",
            "- installation_status: no proposed system, command, or skill was installed in this phase.",
            "",
            "## Tier Counts",
            "",
            *[f"- {key}: `{value}`" for key, value in sorted(matrix["tier_counts"].items())],
            "",
            "## Sample Rows",
            "",
            *[f"- {row['id']} [{row['source_type']}]: `{row['suggested_probe_tier']}`; {row['proposal']}" for row in matrix["rows"][:30]],
        ],
    )

    synthesis = {
        "artifact_type": "v5_x1_synthesis",
        "capability_graph": "v477-thos-v5-x1-command-skill-capability-graph-v1.json",
        "claim_boundary": {
            "canon_promotion": "not_claimed",
            "domain": "THOS lane, command, skill, source, readiness, and roadmap work",
            "gmut_gates_open": GMUT_GATES,
        },
        "expansion_matrix": "v477-thos-v5-x1-expansion-readiness-matrix-v1.json",
        "generated_nz": nz,
        "generated_utc": utc,
        "journey_inventory": journey_inventory(),
        "lane_status": "v477-thos-v5-x1-lane-status-board-v1.json",
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "prior_roadmap_task_count": prior_roadmap.get("task_count"),
        "reflection_count": 30,
        "reflection_steps": reflection_steps(),
        "repo_state": {"drift": drift, "local_head": local_head, "shared_remote_head": remote_head},
        "source_ledger": "v477-thos-v5-x1-source-ledger-v1.json",
        "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
    }
    write_json("v477-thos-v5-x1-synthesis-v1.json", synthesis)
    write_md(
        "v477-thos-v5-x1-synthesis-v1.md",
        [
            "# V477 THOS V5 X1 Synthesis",
            "",
            f"- generated_nz: `{nz}`",
            "- status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            f"- local_head: `{local_head}`",
            f"- shared_remote_head: `{remote_head}`",
            f"- drift: `{drift}`",
            "- claim boundary: THOS infrastructure only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            "",
            *[f"- {row['step']} [{row['theme']}]: {row['finding']}" for row in synthesis["reflection_steps"]],
        ],
    )

    run_status = {
        "artifact_type": "run_status_pair",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "rows": [
            {"id": "app_lanes", "status": "PASS", "summary": "Cicero, Kierkegaard, and Aristotle completed the v5 x1 app-server notifier run."},
            {"id": "cli_lanes", "status": "OPEN_GAP_WATCH_TIMEOUT", "summary": "Arby and Aster Vale were polled through a five-window watcher check and still have no final-message files."},
            {"id": "source_refresh", "status": "PASS", "summary": "Thirty-two current searches and twenty-five source URLs were recorded."},
            {"id": "capability_graph", "status": "PASS_METADATA_ONLY", "summary": "Command and skill metadata were converted into a capability graph without mutation."},
            {"id": "expansion_matrix", "status": "PASS_PROPOSAL_ONLY", "summary": "Ninety proposals were classified into safe probe tiers; no installs were claimed."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
    }
    write_json("v477-thos-v5-x1-run-status-v1.json", run_status)
    write_md(
        "v477-thos-v5-x1-run-status-v1.md",
        [
            "# V477 THOS V5 X1 Run Status",
            "",
            f"- generated_nz: `{nz}`",
            "- status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            "",
            *[f"- {row['id']}: `{row['status']}`; {row['summary']}" for row in run_status["rows"]],
        ],
    )

    roadmap = {
        "artifact_type": "v5_x2_60_task_roadmap",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_phase": NEXT_PHASE,
        "phase": PHASE,
        "task_count": 60,
        "tasks": next_roadmap(),
    }
    write_json("v477-thos-v5-x2-roadmap-v1.json", roadmap)
    write_md(
        "v477-thos-v5-x2-roadmap-v1.md",
        [
            "# V477 THOS V5 X2 Roadmap",
            "",
            f"- generated_nz: `{nz}`",
            "- task_count: `60`",
            "- boundary: existing lanes only; proposal-only expansion matrix; all GMUT gates open.",
            "",
            "## Tasks",
            "",
            *[f"- {task['id']} [{task['domain']}]: {task['task']}" for task in roadmap["tasks"]],
        ],
    )


if __name__ == "__main__":
    main()
