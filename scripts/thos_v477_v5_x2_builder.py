#!/usr/bin/env python3
"""Build v477 THOS v5 x2 synthesis artifacts and the v6 x1 handoff."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v5_x2"
NEXT_PHASE = "v477_thos_v6_x1"
SHARED_REMOTE = "origin/codex/GHC-Family/beyonder-shared-omega-line"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_QUERIES = [
    "OpenAI Codex app-server README GitHub official 2026",
    "OpenAI Codex Windows sandbox official app setup refresh 2026",
    "OpenAI Codex CLI releases 0.136.0 GitHub official",
    "OpenAI Codex safe sandbox official documentation",
    "Model Context Protocol authorization official specification 2025-06-18 tools resources prompts",
    "Model Context Protocol tools output annotations resource links official specification 2025-06-18",
    "Model Context Protocol SDK official docs TypeScript Python 2026",
    "MCP OAuth resource parameter RFC 9728 official specification",
    "GitHub secret scanning push protection official docs 2026",
    "GitHub Actions security hardening official docs 2026",
    "GitHub SARIF upload limits official docs 2026",
    "GitHub Copilot coding agent MCP official docs 2026",
    "Windows Sandbox configure WSB official Microsoft 2026",
    "Windows AppContainer low integrity process official Microsoft security boundary",
    "Windows Mandatory Integrity Control official Win32 integrity levels",
    "PowerShell execution policy not security boundary official Microsoft",
    "Python subprocess security considerations official docs 3.12",
    "Python tempfile TemporaryDirectory cleanup official docs 3.12",
    "OpenTelemetry signals traces metrics logs events official docs 2026",
    "Docker Compose Watch official docs file watch 2026",
    "Google Vertex AI Agent Engine official overview 2026",
    "Google Vertex AI RAG Engine API official 2026",
    "Google Bigtable vector search official docs 2026",
    "Google Gemini API File Search multimodal RAG official 2026",
    "site:cloud.google.com/vertex-ai/generative-ai/docs/agent-engine overview Agent Engine official 2026",
    "site:cloud.google.com/bigtable/docs vector search official Bigtable 2026",
    "site:cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit official 2026",
    "site:cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy official 2026",
    "NVIDIA NIM microservices official docs 2026",
    "NVIDIA DGX Spark user guide official 2026",
    "NVIDIA Nemotron open models agentic AI official 2026",
    "NVIDIA Omniverse physical AI robotics official docs 2026",
]

SOURCE_URLS = [
    {
        "label": "OpenAI Codex Windows sandbox",
        "trust_tier": "official",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "use": "Codex Windows sandbox framing for CLI lane reliability.",
    },
    {
        "label": "OpenAI Codex app-server source",
        "trust_tier": "official_source_repo",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "use": "Local app-server transport assumptions for app lanes.",
    },
    {
        "label": "OpenAI Codex releases",
        "trust_tier": "official_source_repo",
        "url": "https://github.com/openai/codex/releases",
        "use": "CLI release surface context for version tracking.",
    },
    {
        "label": "MCP authorization specification",
        "trust_tier": "official",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
        "use": "Connector authorization and resource-boundary design.",
    },
    {
        "label": "MCP tools specification",
        "trust_tier": "official",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/tools",
        "use": "Tool output, annotations, and resource-link design.",
    },
    {
        "label": "MCP SDK index",
        "trust_tier": "official",
        "url": "https://modelcontextprotocol.io/docs/sdk",
        "use": "SDK routing for future MCP test surfaces.",
    },
    {
        "label": "GitHub push protection",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection",
        "use": "Publication guard inspiration for auth-material prevention.",
    },
    {
        "label": "GitHub Actions hardening",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions",
        "use": "Future workflow hardening context.",
    },
    {
        "label": "GitHub SARIF support",
        "trust_tier": "official",
        "url": "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning",
        "use": "Bounded report-size thinking for future security outputs.",
    },
    {
        "label": "Windows Sandbox configuration",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
        "use": "Sandbox configuration vocabulary.",
    },
    {
        "label": "Windows integrity control",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control",
        "use": "Integrity-level vocabulary for sandbox receipts.",
    },
    {
        "label": "PowerShell execution policies",
        "trust_tier": "official",
        "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6",
        "use": "Terminal safety caveat for script-running assumptions.",
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
        "use": "Temporary-output lifecycle design.",
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
        "label": "Vertex AI Agent Engine",
        "trust_tier": "official",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "use": "Managed agent runtime architecture context only.",
    },
    {
        "label": "Vertex AI Agent Engine deploy",
        "trust_tier": "official",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy",
        "use": "Deploy and permission boundary context only.",
    },
    {
        "label": "Vertex AI ADK overview",
        "trust_tier": "official",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/overview",
        "use": "Agent-development pattern context only.",
    },
    {
        "label": "Vertex AI RAG Engine API",
        "trust_tier": "official",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api",
        "use": "RAG API context only.",
    },
    {
        "label": "Gemini API File Search",
        "trust_tier": "official",
        "url": "https://ai.google.dev/gemini-api/docs/file-search",
        "use": "RAG citation and retrieval context only.",
    },
    {
        "label": "Google File Search update",
        "trust_tier": "official_blog",
        "url": "https://blog.google/innovation-and-ai/technology/developers-tools/expanded-gemini-api-file-search-multimodal-rag/",
        "use": "Current multimodal retrieval context only.",
    },
    {
        "label": "NVIDIA NIM",
        "trust_tier": "official",
        "url": "https://docs.nvidia.com/nim/",
        "use": "Inference microservice architecture context only.",
    },
    {
        "label": "NVIDIA NIM product",
        "trust_tier": "official",
        "url": "https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/",
        "use": "Deployment surface context only.",
    },
    {
        "label": "NVIDIA DGX Spark",
        "trust_tier": "official",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/index.html",
        "use": "Local AI capacity planning context only.",
    },
    {
        "label": "NVIDIA Nemotron 3",
        "trust_tier": "official_newsroom",
        "url": "https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models",
        "use": "Agentic model ecosystem context only.",
    },
    {
        "label": "NVIDIA physical AI tools",
        "trust_tier": "official_newsroom",
        "url": "https://nvidianews.nvidia.com/news/nvidia-releases-major-collection-of-open-source-agent-tools-and-skills-for-physical-ai",
        "use": "Simulation and physical-AI context only.",
    },
    {
        "label": "NIST AI RMF",
        "trust_tier": "official",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "use": "Governance-risk taxonomy context.",
    },
    {
        "label": "UNESCO AI ethics",
        "trust_tier": "official",
        "url": "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
        "use": "Human-centered AI ethics context.",
    },
    {
        "label": "OECD AI principles",
        "trust_tier": "official",
        "url": "https://www.oecd.org/en/topics/ai-principles.html",
        "use": "Trustworthy AI policy context.",
    },
    {
        "label": "EU AI Act timeline",
        "trust_tier": "official",
        "url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline",
        "use": "Regulatory-timeline context.",
    },
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_trace(name: str) -> dict[str, Any]:
    return json.loads((TRACES / name).read_text(encoding="utf-8"))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def git_text(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def command_rows() -> list[dict[str, Any]]:
    book = read_json(ROOT / "docs" / "trinity-command-book-v11.json")
    rows = []
    for command in book["commands"]:
        rows.append(
            {
                "command_id": command.get("command_id"),
                "intent": command.get("intent"),
                "mode": command.get("mode"),
                "risk_class": command.get("risk_class"),
                "requires_live": bool(command.get("requires_live")),
                "requires_connector": bool(command.get("requires_connector")),
                "resume_safe": command.get("resume_safe"),
                "proof_required": command.get("proof_required"),
            }
        )
    return rows


def lane_board(app_run: dict[str, Any], cli_poll: dict[str, Any]) -> dict[str, Any]:
    app_rows = []
    for lane in app_run.get("lanes", []):
        app_rows.append(
            {
                "lane": lane["lane"],
                "platform": "codex_app",
                "status": lane.get("overall_status"),
                "final_state_reason": "app_server_turn_completed"
                if lane.get("overall_status") == "completed"
                else "app_server_turn_not_complete",
                "duration_seconds": lane.get("duration_seconds"),
                "retry_window": lane.get("turn_completion", {}).get("attempt") or lane.get("read", {}).get("attempt"),
                "payload_publication": "status_only",
                "trace_id": f"{PHASE}:{lane['lane']}:app",
            }
        )
    cli_rows = []
    for lane in cli_poll.get("lanes", []):
        cli_rows.append(
            {
                "lane": lane["lane"],
                "platform": "codex_cli",
                "status": lane.get("completion_status"),
                "final_state_reason": "watch_timeout_no_final_message",
                "final_message_bytes": lane.get("final_message_bytes"),
                "stderr_bytes": lane.get("stderr_bytes"),
                "stdout_bytes": lane.get("stdout_bytes"),
                "payload_publication": "status_only",
                "trace_id": f"{PHASE}:{lane['lane']}:cli",
            }
        )
    return {
        "artifact_type": "lane_final_state_board",
        "phase": PHASE,
        "app_lane_status": app_run.get("overall_status"),
        "cli_lane_status": cli_poll.get("aggregate_status"),
        "lanes": app_rows + cli_rows,
        "summary": {
            "completed_app_lanes": sum(1 for row in app_rows if row["status"] == "completed"),
            "waiting_cli_lanes": sum(1 for row in cli_rows if row["status"] != "FINAL_MESSAGE_READY"),
            "unfiltered_transport_published": False,
        },
    }


def command_approval_queues(commands: list[dict[str, Any]]) -> dict[str, Any]:
    live = [row for row in commands if row["requires_live"]]
    connector = [row for row in commands if row["requires_connector"]]
    offline_low = [row for row in commands if not row["requires_live"] and not row["requires_connector"] and row["risk_class"] == "low"]
    risk_mode = Counter((row["mode"], row["risk_class"]) for row in commands)
    heatmap = [
        {"mode": mode, "risk_class": risk, "count": count}
        for (mode, risk), count in sorted(risk_mode.items(), key=lambda item: (str(item[0][0]), str(item[0][1])))
    ]
    return {
        "artifact_type": "command_approval_queues",
        "phase": PHASE,
        "command_count": len(commands),
        "queues": {
            "live_write_approval_required": live[:30],
            "connector_approval_required": connector[:30],
            "offline_low_risk_candidate_sample": offline_low[:30],
        },
        "queue_counts": {
            "live_write_approval_required": len(live),
            "connector_approval_required": len(connector),
            "offline_low_risk_candidate": len(offline_low),
        },
        "risk_mode_heatmap": heatmap,
        "execution_policy": "metadata_only_no_command_execution",
    }


def expansion_ranked_queue(matrix: dict[str, Any]) -> dict[str, Any]:
    rows = matrix.get("rows", [])
    tier_order = {
        "P0_inspect_only": 0,
        "P1_dry_run_guard_probe": 1,
        "P2_bounded_local_simulation": 2,
    }
    ranked = sorted(rows, key=lambda row: (tier_order.get(row.get("suggested_probe_tier"), 9), row.get("source_type", ""), row.get("id", "")))
    for index, row in enumerate(ranked, start=1):
        row["rank"] = index
        row["promotion_gate"] = "exact_approval_required_before_live_write" if row.get("suggested_probe_tier") == "P2_bounded_local_simulation" else "safe_probe_only"
    return {
        "artifact_type": "expansion_ranked_queue",
        "phase": PHASE,
        "proposal_count": len(ranked),
        "tier_counts": matrix.get("tier_counts", {}),
        "installed_count": 0,
        "top_p0": [row for row in ranked if row.get("suggested_probe_tier") == "P0_inspect_only"][:15],
        "top_p1": [row for row in ranked if row.get("suggested_probe_tier") == "P1_dry_run_guard_probe"][:15],
        "top_p2": [row for row in ranked if row.get("suggested_probe_tier") == "P2_bounded_local_simulation"][:15],
        "ranked_all": ranked,
        "claim_boundary": "proposal_and_probe_queue_only",
    }


def observability_schema() -> dict[str, Any]:
    fields = [
        {"field": "phase", "reason": "ties a receipt to one phase-version session"},
        {"field": "lane", "reason": "identifies advisory lane without publishing message text"},
        {"field": "run_id", "reason": "links start, watcher, and completion receipts"},
        {"field": "trace_id", "reason": "stable row-level correlation key"},
        {"field": "generated_utc", "reason": "unambiguous clock source"},
        {"field": "status", "reason": "machine-readable final state"},
        {"field": "final_state_reason", "reason": "explains completion or open gap"},
        {"field": "retry_window_seconds", "reason": "records patience budget"},
        {"field": "timeout_reason", "reason": "separates no-signal, partial-signal, and active-turn blockers"},
        {"field": "payload_publication", "reason": "documents status-only publication boundary"},
        {"field": "gmut_gate_state", "reason": "keeps physics-claim gates visibly open"},
    ]
    return {
        "artifact_type": "observability_schema",
        "phase": PHASE,
        "fields": fields,
        "invariants": [
            "No unfiltered event stream is published.",
            "No local machine-specific filesystem address is required in reader-facing artifacts.",
            "Existing lanes only; no replacement agent creation.",
            "All GMUT gates stay open unless exact closure artifacts exist.",
        ],
        "recommended_next_probe": "add the same schema keys to the next app and CLI notifier receipts",
    }


def source_ledger(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "source_refresh_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": len(SOURCE_QUERIES),
        "queries": SOURCE_QUERIES,
        "sources": SOURCE_URLS,
        "source_policy": {
            "preferred_tiers": ["official", "official_source_repo", "official_blog", "official_newsroom"],
            "lower_tier_material": "context_only_unless_independently_verified",
            "claim_ceiling": "technology_and_governance_context_only",
        },
    }


def x3_decision(cli_poll: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "x3_decision",
        "phase": PHASE,
        "decision": "NO_X3_FOR_V5",
        "next_phase": NEXT_PHASE,
        "reasoning": [
            "The three app lanes completed in the refreshed app-server notifier run.",
            "The two CLI lanes still show a watcher timeout with no final-message marker.",
            "Another v5 x3 overlay would mostly duplicate the same CLI polling evidence.",
            "The open CLI gap is better carried into v6 x1 with a clearer watcher schema and a fresh non-ephemeral launch check.",
        ],
        "cli_status_carried_forward": cli_poll.get("aggregate_status"),
        "open_gap": "Arby and Aster Vale final-message marker still pending in this receipt.",
    }


def reflections() -> list[dict[str, str]]:
    items = [
        ("lane_mesh", "App-server route now has both probe and notify PASS receipts for three app lanes."),
        ("lane_mesh", "CLI route remains useful but needs a richer done-signal than final-message file presence."),
        ("lane_mesh", "Five-lane status is mixed: app completed, CLI waiting."),
        ("lane_mesh", "Existing-lane policy held; no replacement lanes were created."),
        ("notifier", "The app notifier is reusable across future v477-v490 THOS passes."),
        ("notifier", "The notifier should gain timeout taxonomy fields in v6."),
        ("notifier", "Status-only publication is the correct boundary for advisory lanes."),
        ("notifier", "Probe-only mode is useful before notify mode after app updates."),
        ("command_graph", "The command book remains metadata-rich enough for approval queue generation."),
        ("command_graph", "Live commands require explicit approval queues rather than silent execution."),
        ("command_graph", "Connector commands should stay read/use-only until separate write approval exists."),
        ("command_graph", "Offline low-risk commands are the safest candidates for v6 dry-run rehearsal."),
        ("skill_graph", "The 701-skill observation is metadata, not a claim that all skills are ready."),
        ("skill_graph", "No skill or plugin-cache mutation belongs in v5 x2."),
        ("skill_graph", "Frontmatter repair can be reopened only with fresh loader evidence."),
        ("expansion_queue", "All 90 proposal rows remain proposal/probe candidates."),
        ("expansion_queue", "Installed count remains zero because v5 x2 did not install expansions."),
        ("expansion_queue", "P0 rows should drive v6 no-write inspections."),
        ("source_refresh", "Official documentation is enough for architecture context but not for GMUT validation."),
        ("source_refresh", "NVIDIA and Google agent stacks are useful THOS design references only."),
        ("source_refresh", "OpenTelemetry is the cleanest vocabulary for runner receipt design."),
        ("source_refresh", "GitHub security docs reinforce exact staging and guard scans."),
        ("sandbox", "Windows sandbox sources support bounded diagnosis, not destructive repair."),
        ("sandbox", "PowerShell execution policy should not be treated as a security boundary."),
        ("governance", "NIST, UNESCO, OECD, and EU sources map to governance vocabulary for THOS."),
        ("governance", "Ethics and policy sources do not promote Journey context into canon."),
        ("journey_context", "Journey material remains context-only unless separately cited and bounded."),
        ("gmut", "All six GMUT gates remain open in this THOS phase."),
        ("handoff", "v6 x1 should convert metadata queues into first bounded probes."),
        ("handoff", "v6 x1 should preserve app-lane notifier cadence while retrying CLI completion carefully."),
    ]
    return [{"step": str(index), "domain": domain, "reflection": text} for index, (domain, text) in enumerate(items, start=1)]


def v6_tasks() -> list[dict[str, str]]:
    seeds = [
        ("lanes", "Run app-lane notifier probe before any v6 x1 notification pass."),
        ("lanes", "Run app-lane notifier notify pass for Cicero, Kierkegaard, and Aristotle if probe passes."),
        ("lanes", "Run a fresh Arby/Aster completion watcher using the new observability fields."),
        ("lanes", "Record active-turn, no-signal, partial-signal, and timeout categories separately."),
        ("lanes", "Keep all lane message content unpublished unless separately approved."),
        ("lanes", "Record no old-style spawn and existing-lane-only proof."),
        ("command_queue", "Select 12 offline low-risk command rows for P0 inspection."),
        ("command_queue", "Select 12 connector command rows for read-only connector readiness review."),
        ("command_queue", "Select 12 live-write command rows for approval-packet drafting only."),
        ("command_queue", "Add a command-to-skill domain join without skill body copying."),
        ("command_queue", "Add proof-required summaries for selected commands."),
        ("command_queue", "Reject any command with unclear rollback as not ready."),
        ("skills", "Sample user-skill metadata without editing skill files."),
        ("skills", "Run a duplicate-name scan as stdout-only evidence."),
        ("skills", "Create a skill-readiness queue from metadata only."),
        ("skills", "Keep plugin cache and user skills out of repo staging."),
        ("skills", "Draft exact repair approval only if a loader failure recurs."),
        ("skills", "Add skill-to-command graph edge examples."),
        ("expansions", "Run P0 no-write inspections for top system expansion rows."),
        ("expansions", "Run P1 stdout-only guard probes for top command rows."),
        ("expansions", "Keep P2 toy simulations labelled as simulation only."),
        ("expansions", "Keep installed_count at zero unless exact install proof exists."),
        ("expansions", "Promote failed probes into open_gap, not failure inflation."),
        ("expansions", "Draft a 30/30/30 proposal status board for v6 x1."),
        ("sources", "Refresh Codex app-server and CLI release sources before v6 publication."),
        ("sources", "Refresh MCP authorization/tool docs before connector planning."),
        ("sources", "Refresh GitHub security docs before any workflow proposal."),
        ("sources", "Refresh Google/NVIDIA sources as architecture context only."),
        ("sources", "Keep spiritual/Journey material context-only and locally cited if used."),
        ("sources", "Distinguish official, official repo, official blog, and lower-tier material."),
        ("observability", "Add run_id and trace_id to every v6 lane receipt."),
        ("observability", "Add retry_window_seconds to every v6 watcher receipt."),
        ("observability", "Add timeout_reason values to CLI and app receipts."),
        ("observability", "Add payload_publication value to every lane row."),
        ("observability", "Add gmut_gate_state field to every run-status pair."),
        ("observability", "Prepare dashboard-ready rows with bounded payload size."),
        ("sandbox", "Run non-destructive Codex version and sandbox readiness checks."),
        ("sandbox", "Record Windows sandbox blocker class without changing system policy."),
        ("sandbox", "Avoid package/cache deletion unless exact separate approval exists."),
        ("sandbox", "Keep PowerShell settings unchanged unless exact safety need exists."),
        ("sandbox", "Retain CLI lane worktrees as read-only advisory surfaces."),
        ("sandbox", "Add CLI done-signal alternatives for future Arby/Aster waits."),
        ("handoff", "Write v6 x1 synthesis after lane and command probes finish."),
        ("handoff", "Generate v6 x2 60-task roadmap from v6 x1 evidence."),
        ("handoff", "Decide whether v6 x2 needs x3 overlay from fresh evidence only."),
        ("handoff", "Publish every second phase where feasible with exact staging."),
        ("handoff", "Keep current v477 sequence moving toward v490 without narrowing the goal."),
        ("handoff", "Record remote-equals-local proof after each push."),
        ("gmut", "Carry all six GMUT gates open."),
        ("gmut", "Keep THOS artifacts from validating GMUT by association."),
        ("gmut", "Keep consciousness bridge as protocol requirement, not solved claim."),
        ("gmut", "Keep fifth-force/equivalence constraints open."),
        ("gmut", "Keep Journey context out of canon proof."),
        ("gmut", "Keep source dependencies explicitly separated by claim taxonomy."),
        ("quality", "Run JSON parse on every generated v6 artifact."),
        ("quality", "Run script compile for any new helper script."),
        ("quality", "Run staged whitespace check before publication."),
        ("quality", "Run scoped guard scan before publication."),
        ("quality", "Review staged names before commit."),
        ("quality", "Push only if drift remains zero or a forward-only merge is safely completed."),
    ]
    return [{"id": f"v477-v6-x1-task-{index:02d}", "domain": domain, "task": text} for index, (domain, text) in enumerate(seeds, start=1)]


def build() -> None:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])
    app_run = read_trace("v477-thos-v5-x2-app-lane-completion-notifier-v1.json")
    cli_poll = read_trace("v477-thos-v5-x2-cli-lane-completion-poll-v1.json")
    capability = read_trace("v477-thos-v5-x1-command-skill-capability-graph-v1.json")
    matrix = read_trace("v477-thos-v5-x1-expansion-readiness-matrix-v1.json")
    roadmap = read_trace("v477-thos-v5-x2-roadmap-v1.json")
    commands = command_rows()

    source = source_ledger(generated_utc, generated_nz)
    lanes = lane_board(app_run, cli_poll)
    command_queue = command_approval_queues(commands)
    expansion_queue = expansion_ranked_queue(matrix)
    observability = observability_schema()
    decision = x3_decision(cli_poll)
    reflection_rows = reflections()

    synthesis = {
        "artifact_type": "v5_x2_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "local_head_before_build": local_head,
        "remote_head_before_build": remote_head,
        "drift_before_build": drift,
        "inputs": {
            "roadmap_task_count": roadmap.get("task_count"),
            "app_lane_status": app_run.get("overall_status"),
            "cli_lane_status": cli_poll.get("aggregate_status"),
            "command_count": capability.get("command_count"),
            "user_skill_count_observed": capability.get("user_skill_count_observed"),
            "proposal_count": matrix.get("proposal_count"),
            "source_search_count": source["search_count"],
        },
        "reflection_steps": reflection_rows,
        "outputs": {
            "lane_board": "v477-thos-v5-x2-lane-final-state-board-v1",
            "command_approval_queues": "v477-thos-v5-x2-command-approval-queues-v1",
            "expansion_ranked_queue": "v477-thos-v5-x2-expansion-ranked-queue-v1",
            "observability_schema": "v477-thos-v5-x2-observability-schema-v1",
            "x3_decision": "v477-thos-v5-x2-x3-decision-v1",
            "next_roadmap": "v477-thos-v6-x1-roadmap-v1",
        },
        "claim_boundary": {
            "thos_scope": "lane, command, expansion, source, and observability coordination",
            "gmut_gates": {gate: "open" for gate in GMUT_GATES},
            "canon_promotion": "not_claimed",
        },
    }

    run_status = {
        "artifact_type": "run_status_pair",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "status_rows": [
            {"id": "app_lanes", "status": "PASS", "summary": "Cicero, Kierkegaard, and Aristotle completed the app-server notifier run."},
            {"id": "cli_lanes", "status": cli_poll.get("aggregate_status"), "summary": "Arby and Aster Vale remain pending final-message marker in this watcher receipt."},
            {"id": "source_refresh", "status": "PASS", "summary": f"{source['search_count']} live searches refreshed the official-source ledger."},
            {"id": "command_queues", "status": "PASS_METADATA_ONLY", "summary": "Command approval queues were generated from existing command metadata."},
            {"id": "expansion_queue", "status": "PASS_PROPOSAL_ONLY", "summary": "All 90 expansion proposals remain proposal/probe candidates; no install occurred."},
            {"id": "observability_schema", "status": "PASS", "summary": "Next watcher schema fields were specified."},
            {"id": "x3_decision", "status": "NO_X3_FOR_V5", "summary": "The open CLI gap is carried into v6 x1 rather than duplicating v5 x3."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "next_expected_phase": NEXT_PHASE,
    }

    v6 = {
        "artifact_type": "v6_x1_60_task_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": 60,
        "tasks": v6_tasks(),
        "entry_conditions": [
            "Fetch and drift-check before any publication.",
            "Use existing app and CLI lanes only.",
            "Run no-write probes before any live-write request.",
            "Keep all GMUT gates open.",
        ],
    }

    artifacts = {
        "v477-thos-v5-x2-source-ledger-v1": source,
        "v477-thos-v5-x2-lane-final-state-board-v1": lanes,
        "v477-thos-v5-x2-command-approval-queues-v1": command_queue,
        "v477-thos-v5-x2-expansion-ranked-queue-v1": expansion_queue,
        "v477-thos-v5-x2-observability-schema-v1": observability,
        "v477-thos-v5-x2-x3-decision-v1": decision,
        "v477-thos-v5-x2-synthesis-v1": synthesis,
        "v477-thos-v5-x2-run-status-v1": run_status,
        "v477-thos-v6-x1-roadmap-v1": v6,
    }

    for stem, payload in artifacts.items():
        write_json(TRACES / f"{stem}.json", payload)

    write_md(
        TRACES / "v477-thos-v5-x2-source-ledger-v1.md",
        "v477 THOS v5 x2 Source Ledger",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- search_count: `{source['search_count']}`",
            "- source policy: official and primary sources preferred; lower-tier material is context-only.",
            "",
            "## Sources",
            *[f"- {item['label']}: {item['url']} ({item['trust_tier']}) - {item['use']}" for item in source["sources"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-lane-final-state-board-v1.md",
        "v477 THOS v5 x2 Lane Final-State Board",
        [
            f"- app_lane_status: `{lanes['app_lane_status']}`",
            f"- cli_lane_status: `{lanes['cli_lane_status']}`",
            "- publication: status-only lane receipts.",
            "",
            "## Lanes",
            *[f"- {row['lane']} ({row['platform']}): `{row['status']}` - {row['final_state_reason']}." for row in lanes["lanes"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-command-approval-queues-v1.md",
        "v477 THOS v5 x2 Command Approval Queues",
        [
            f"- command_count: `{command_queue['command_count']}`",
            f"- live_write_approval_required: `{command_queue['queue_counts']['live_write_approval_required']}`",
            f"- connector_approval_required: `{command_queue['queue_counts']['connector_approval_required']}`",
            f"- offline_low_risk_candidate: `{command_queue['queue_counts']['offline_low_risk_candidate']}`",
            "- execution_policy: metadata-only; no command execution.",
            "",
            "## Live Approval Queue Sample",
            *[f"- {row['command_id']}: {row['intent']}" for row in command_queue["queues"]["live_write_approval_required"][:12]],
            "",
            "## Connector Queue Sample",
            *[f"- {row['command_id']}: {row['intent']}" for row in command_queue["queues"]["connector_approval_required"][:12]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-expansion-ranked-queue-v1.md",
        "v477 THOS v5 x2 Expansion Ranked Queue",
        [
            f"- proposal_count: `{expansion_queue['proposal_count']}`",
            "- installed_count: `0`",
            "- claim boundary: proposal and probe queue only.",
            "",
            "## Top P0",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion_queue["top_p0"][:10]],
            "",
            "## Top P1",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion_queue["top_p1"][:10]],
            "",
            "## Top P2",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion_queue["top_p2"][:10]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-observability-schema-v1.md",
        "v477 THOS v5 x2 Observability Schema",
        [
            "- purpose: standardize future app and CLI watcher receipts.",
            "",
            "## Fields",
            *[f"- {row['field']}: {row['reason']}" for row in observability["fields"]],
            "",
            "## Invariants",
            *[f"- {item}" for item in observability["invariants"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-x3-decision-v1.md",
        "v477 THOS v5 x2 x3 Decision",
        [
            f"- decision: `{decision['decision']}`",
            f"- next_phase: `{decision['next_phase']}`",
            f"- cli_status_carried_forward: `{decision['cli_status_carried_forward']}`",
            "",
            "## Reasoning",
            *[f"- {item}" for item in decision["reasoning"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-synthesis-v1.md",
        "v477 THOS v5 x2 Synthesis",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- local_head_before_build: `{local_head}`",
            f"- remote_head_before_build: `{remote_head}`",
            f"- drift_before_build: `{drift}`",
            f"- app_lane_status: `{app_run.get('overall_status')}`",
            f"- cli_lane_status: `{cli_poll.get('aggregate_status')}`",
            f"- command_count: `{capability.get('command_count')}`",
            f"- user_skill_count_observed: `{capability.get('user_skill_count_observed')}`",
            f"- source_search_count: `{source['search_count']}`",
            "- claim boundary: THOS coordination only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            *[f"- {row['step']}. {row['domain']}: {row['reflection']}" for row in reflection_rows],
        ],
    )
    write_md(
        TRACES / "v477-thos-v5-x2-run-status-v1.md",
        "v477 THOS v5 x2 Run Status",
        [
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            *[f"- {row['id']}: `{row['status']}` - {row['summary']}" for row in run_status["status_rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-roadmap-v1.md",
        "v477 THOS v6 x1 Roadmap",
        [
            f"- task_count: `{v6['task_count']}`",
            "- entry: existing lanes only, no unapproved live writes, all GMUT gates open.",
            "",
            "## Tasks",
            *[f"- {row['id']} ({row['domain']}): {row['task']}" for row in v6["tasks"]],
        ],
    )


def main() -> None:
    build()
    print(json.dumps({"status": "built", "phase": PHASE, "next_phase": NEXT_PHASE}, indent=2))


if __name__ == "__main__":
    main()
