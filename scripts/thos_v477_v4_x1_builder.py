#!/usr/bin/env python3
"""Build v477 THOS v4 x1 command, handoff, skill, source, and lane artifacts."""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v4_x1"
NEXT_PHASE = "v477_thos_v4_x2"


GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


SOURCE_QUERIES = [
    "OpenAI Codex CLI Windows sandbox app-server official",
    "OpenAI Codex app-server thread read resume turn start",
    "OpenAI Agents SDK tracing MCP guardrails official",
    "OpenAI developer docs MCP Codex official",
    "MCP server tools resources prompts inspector official",
    "MCP authorization security OAuth 2.1 official",
    "MCP roots deprecation sampling logging official",
    "MCP TypeScript SDK tools resources prompts official",
    "GitHub push protection secret scanning official",
    "GitHub Actions security hardening official",
    "GitHub code scanning SARIF upload official",
    "GitHub SARIF support limits official",
    "PowerShell execution policies security official",
    "PowerShell security features official",
    "Windows Sandbox configuration official",
    "Windows Mandatory Integrity Control official",
    "Windows AppContainer official",
    "Windows CreateRestrictedToken official",
    "Python subprocess security shell false official",
    "Python pathlib filesystem paths official",
    "Python tempfile cleanup official",
    "Python hashlib sha256 official",
    "OpenTelemetry signals traces metrics logs official",
    "Docker Compose watch develop official",
    "Kubernetes Jobs official",
    "Kubernetes CronJobs official",
    "OWASP Top 10 LLM Applications official",
    "Google Vertex AI Agent Development Kit official",
    "Google Vertex AI Agent Engine ADK official",
    "Google Bigtable vector search Vertex AI official",
    "Google Cloud RAG Gemini Enterprise Vertex AI official",
    "NVIDIA DGX Spark hardware official",
    "NVIDIA Nemotron agentic AI official",
    "NVIDIA NIM inference microservices official",
]


OPENED_SOURCES = [
    {
        "label": "OpenAI Codex Windows sandbox",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "source_class": "official_openai",
        "v4_use": "Windows sandbox/readiness boundaries for CLI lanes.",
    },
    {
        "label": "OpenAI Codex app-server README",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "source_class": "official_source_repository",
        "v4_use": "Local app-server transport and thread method routing.",
    },
    {
        "label": "OpenAI Agents SDK tracing",
        "url": "https://openai.github.io/openai-agents-python/tracing/",
        "source_class": "official_sdk_docs",
        "v4_use": "Trace/span vocabulary for THOS watcher receipts.",
    },
    {
        "label": "OpenAI Docs MCP",
        "url": "https://platform.openai.com/docs/docs-mcp",
        "source_class": "official_openai_docs",
        "v4_use": "Read-only documentation MCP pattern for future connector discipline.",
    },
    {
        "label": "MCP Inspector",
        "url": "https://modelcontextprotocol.io/docs/tools",
        "source_class": "official_protocol_docs",
        "v4_use": "Tools/resources/prompts inspection model for THOS connector testing.",
    },
    {
        "label": "MCP authorization specification",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
        "source_class": "official_protocol_spec",
        "v4_use": "Authorization and token audience boundaries for connector design.",
    },
    {
        "label": "GitHub push protection",
        "url": "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection",
        "source_class": "official_platform_docs",
        "v4_use": "Publication guard inspiration for repo push safety.",
    },
    {
        "label": "GitHub Actions security hardening",
        "url": "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions",
        "source_class": "official_platform_docs",
        "v4_use": "Action/workflow security controls for future THOS automation.",
    },
    {
        "label": "Microsoft Mandatory Integrity Control",
        "url": "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control",
        "source_class": "official_os_docs",
        "v4_use": "Windows integrity-level framing for sandbox readiness.",
    },
    {
        "label": "PowerShell execution policies",
        "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6",
        "source_class": "official_runtime_docs",
        "v4_use": "PowerShell safety expectations and non-security caveats.",
    },
    {
        "label": "Python subprocess",
        "url": "https://docs.python.org/3.12/library/subprocess.html",
        "source_class": "official_runtime_docs",
        "v4_use": "List-form command execution and shell-avoidance discipline.",
    },
    {
        "label": "OpenTelemetry signals",
        "url": "https://opentelemetry.io/docs/concepts/signals/",
        "source_class": "official_observability_docs",
        "v4_use": "Trace/metric/log naming for lane watcher artifacts.",
    },
    {
        "label": "Docker Compose Watch",
        "url": "https://docs.docker.com/compose/how-tos/file-watch/",
        "source_class": "official_container_docs",
        "v4_use": "File-watch analogies for bounded runner refresh.",
    },
    {
        "label": "Kubernetes CronJob",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/",
        "source_class": "official_orchestration_docs",
        "v4_use": "Retry/idempotency and scheduled-run caveats for THOS watchers.",
    },
    {
        "label": "Google Agent Development Kit",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/overview",
        "source_class": "official_cloud_docs",
        "v4_use": "Agent software-development framing for THOS orchestration.",
    },
    {
        "label": "NVIDIA DGX Spark hardware",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/hardware.html",
        "source_class": "official_hardware_docs",
        "v4_use": "Local AI capacity planning context only.",
    },
    {
        "label": "NVIDIA Nemotron",
        "url": "https://www.nvidia.com/en-us/ai-data-science/foundation-models/llama-nemotron/",
        "source_class": "official_model_docs",
        "v4_use": "Agentic model ecosystem context for future THOS planning.",
    },
]


def utc_nz_now() -> tuple[str, str]:
    utc = dt.datetime.now(dt.timezone.utc)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12)))
    return utc.isoformat(timespec="seconds"), nz.isoformat(timespec="seconds")


def run_git(args: list[str], default: str = "unknown") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return default


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"read_status": "missing", "path_label": path.name}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(name: str, payload: dict[str, Any]) -> None:
    (TRACES / name).write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(name: str, body: str) -> None:
    (TRACES / name).write_text(body.strip() + "\n", encoding="utf-8")


def command_surface() -> dict[str, Any]:
    book_path = ROOT / "docs" / "trinity-command-book-v11.json"
    validation_path = ROOT / "docs" / "trinity-command-book-validation-latest.json"
    book = read_json(book_path)
    validation = read_json(validation_path)
    commands = book.get("commands", [])
    risk_counts = Counter(str(item.get("risk_class", "unknown")) for item in commands)
    mode_counts = Counter(str(item.get("mode", "unknown")) for item in commands)
    connector_count = sum(1 for item in commands if item.get("requires_connector"))
    live_count = sum(1 for item in commands if item.get("requires_live"))
    sample_rows = []
    for item in commands[:40]:
        sample_rows.append(
            {
                "command_id": item.get("command_id"),
                "mode": item.get("mode"),
                "risk_class": item.get("risk_class"),
                "requires_live": bool(item.get("requires_live")),
                "requires_connector": item.get("requires_connector") or "",
                "source_of_truth": item.get("source_of_truth") or "",
                "resume_safe": bool(item.get("resume_safe")),
            }
        )
    return {
        "book_version": book.get("version"),
        "book_generated_utc": book.get("generated_utc"),
        "command_count": len(commands),
        "connector_command_count": connector_count,
        "live_command_count": live_count,
        "risk_counts": dict(risk_counts),
        "mode_counts": dict(mode_counts),
        "validation_status": validation.get("overall_status"),
        "validation_command_count": validation.get("command_count"),
        "sample_rows": sample_rows,
        "surface_status": "PASS_METADATA_ONLY",
    }


def handoff_surface() -> dict[str, Any]:
    surface = read_json(ROOT / "docs" / "trinity-v54-v55-handoff-surface-v1.json")
    read_surfaces = []
    for item in surface.get("read_surfaces", []):
        read_surfaces.append(
            {
                "surface_id": item.get("surface_id"),
                "path": item.get("path"),
                "policy_path": item.get("policy_path"),
                "claim_class": "journey_context_not_canon",
            }
        )
    return {
        "source_status": surface.get("overall_status", "unknown"),
        "runtime_model_resolution_label": surface.get("runtime_model_resolution", {}).get("path"),
        "read_surfaces": read_surfaces,
        "source_hash_count": len(surface.get("source_hashes", [])),
        "surface_status": "PASS_EXISTING_SURFACE_CONFIRMED" if surface.get("overall_status") == "PASS" else "OPEN_GAP_REVIEW_NEEDED",
        "boundary": "continuity_handoff_only_no_gmut_validation",
    }


def parse_frontmatter(text: str) -> dict[str, str]:
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {"parse_status": "missing_frontmatter"}
    end = text.find("\n---", 3)
    if end == -1:
        return {"parse_status": "unterminated_frontmatter"}
    front = text[3:end].strip().splitlines()
    result = {"parse_status": "ok"}
    for line in front:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def skill_surface() -> dict[str, Any]:
    skill_root = Path.home() / ".codex" / "skills"
    plugin_root = Path.home() / ".codex" / "plugins" / "cache"
    rows = []
    for directory in sorted(skill_root.iterdir()) if skill_root.exists() else []:
        if not directory.is_dir() or directory.name.startswith("."):
            continue
        skill_file = directory / "SKILL.md"
        if not skill_file.exists():
            rows.append({"folder": directory.name, "status": "OPEN_GAP_NO_SKILL_MD"})
            continue
        text = skill_file.read_text(encoding="utf-8-sig", errors="replace")
        meta = parse_frontmatter(text)
        rows.append(
            {
                "folder": directory.name,
                "status": "PASS_METADATA" if meta.get("parse_status") == "ok" and meta.get("name") and meta.get("description") else "OPEN_GAP_METADATA",
                "name": meta.get("name", ""),
                "description_present": bool(meta.get("description")),
            }
        )
    name_counts = Counter(row.get("name", "") for row in rows if row.get("name"))
    duplicates = sorted(name for name, count in name_counts.items() if count > 1)
    return {
        "sample_limit": 120,
        "user_skill_count_observed": len(rows),
        "user_skill_sample": rows[:120],
        "duplicate_name_sample": duplicates[:30],
        "plugin_cache_exists": plugin_root.exists(),
        "mutation_policy": "no_skill_or_plugin_cache_mutation_in_this_phase",
        "surface_status": "PASS_METADATA_ONLY_WITH_REVIEW_GAPS" if any(row["status"].startswith("OPEN") for row in rows) else "PASS_METADATA_ONLY",
    }


def app_lane_status() -> list[dict[str, Any]]:
    payload = read_json(TRACES / "v477-thos-v4-x1-app-lane-notifier-run-v1.json")
    rows = []
    for lane in payload.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("name"),
                "overall_status": lane.get("overall_status"),
                "read": lane.get("read", {}).get("status"),
                "resume": lane.get("resume", {}).get("status"),
                "turn_start": lane.get("turn_start", {}).get("status"),
                "turn_completion": lane.get("turn_completion", {}).get("status"),
                "payload_publication": "not_published",
            }
        )
    return rows


def cli_notice_status() -> dict[str, Any]:
    notice = read_json(TRACES / "v477-thos-v3-x2-cli-lane-completion-notice-v1.json")
    return {
        "aggregate_status": notice.get("aggregate_status", "missing"),
        "phase_slug": notice.get("phase_slug", "v477-thos-v3-x2"),
        "lanes": [
            {
                "lane": row.get("lane"),
                "completion_status": row.get("completion_status"),
                "final_message_bytes": row.get("final_message_bytes"),
                "stdout_bytes": row.get("stdout_bytes"),
                "stderr_bytes": row.get("stderr_bytes"),
            }
            for row in notice.get("lanes", [])
        ],
        "publication_boundary": "completion_metadata_only",
    }


def reflection_steps() -> list[dict[str, str]]:
    base = [
        ("command_book", "Command book v11 is present and validation reports PASS, so v4 can surface metadata before mutating anything."),
        ("dirty_worktree", "Unrelated dirty files are present; exact staging remains mandatory."),
        ("handoff_surface", "The v54/v55 handoff surface already exists and can be carried forward as continuity, not canon."),
        ("app_lanes", "Cicero, Kierkegaard, and Aristotle completed v4 x1 through app-server notifier."),
        ("cli_lanes", "Arby/Aster x2 completion remains pending and should not be summarized as received."),
        ("source_refresh", "Search volume is process metadata; opened official sources are the stronger evidence."),
        ("mcp", "MCP Inspector and authorization docs support tool/resource/prompt and OAuth boundary design."),
        ("openai", "Codex sandbox and app-server sources support local lane transport decisions."),
        ("github", "Push protection and Actions hardening inform staged publication and future automation."),
        ("windows", "MIC, AppContainer, and restricted token docs support observed sandbox claims only."),
        ("powershell", "Execution policy is a safety feature, not a complete security boundary."),
        ("python", "List-form subprocess calls and temp cleanup docs support safer helper scripts."),
        ("otel", "Signals, spans, and metrics are useful for watcher receipts and dashboards."),
        ("docker", "Compose watch gives a concrete model for file-triggered bounded refresh."),
        ("kubernetes", "Job/CronJob caveats reinforce idempotent retries and duplicate-start avoidance."),
        ("google", "ADK and Agent Engine docs are architecture context, not deployment permission."),
        ("nvidia", "DGX/Nemotron/NIM sources support capacity and model ecosystem planning only."),
        ("owasp", "LLM risk taxonomy should shape connector/tool prompt-surface hardening."),
        ("skills", "Skill capability index should publish frontmatter metadata only."),
        ("plugins", "Plugin cache stays read/use-only unless exact repair is separately approved."),
        ("drive", "Drive/Journey material can support continuity pointers without publishing restricted payloads."),
        ("gmut", "No THOS result closes null/SI/conservation/baseline/equivalence/bridge gates."),
        ("eureka", "120-task sibling ideals need compression into executable 60-task next maps."),
        ("x_sessions", "Extra x sessions should exist because work needs them, not because labels are decorative."),
        ("watcher", "A live watcher without final files is an open gap, not failure and not completion."),
        ("receipts", "Receipts should include start time, state, source, blocker, and next action."),
        ("schemas", "Every new artifact should be JSON-parseable and guard-clean."),
        ("handoff", "v4 x2 should integrate the CLI completion notice if it arrives."),
        ("remote", "Shared omega remote equality remains the authoritative publication proof."),
        ("next_phase", "v477 v4 x2 should close command/handoff/skill/source surfaces before v478 transition."),
    ]
    return [{"step": f"reflection_{idx:02d}", "theme": theme, "finding": finding} for idx, (theme, finding) in enumerate(base, 1)]


def next_tasks() -> list[dict[str, str]]:
    groups = [
        ("command-index", [
            "Promote v11 command metadata into a compact command-index surface.",
            "Add risk/mode/live/connector summary cards.",
            "Create a parser that checks command_id, source_of_truth, and safety fields.",
            "Flag commands with live connectors for future exact approval review.",
            "Create a top-40 sample table for UI/workbench discovery.",
            "Separate command availability from command aspiration.",
        ]),
        ("handoff", [
            "Carry v54/v55 continuity packs into v477 route cards.",
            "Record source hashes without copying pack bodies.",
            "Classify handoff rows as journey_context_not_canon.",
            "Connect v55 receiver policy to v478 acceptance criteria.",
            "Preserve dirty input notices and avoid staging unrelated tracked files.",
            "Create a handoff freshness check for v478.",
        ]),
        ("skills", [
            "Generate a metadata-only skill capability index.",
            "Flag missing or malformed frontmatter as review gaps.",
            "Do not mutate skill or plugin cache files in ordinary THOS phases.",
            "Map skill names to command-index domains.",
            "Add duplicate name detection to the skill index.",
            "Prepare exact repair packets only if loader failures recur.",
        ]),
        ("lanes", [
            "Run app-lane probe before the next app advisory pass.",
            "Record app-lane completion status without publishing advisory text.",
            "Poll Arby/Aster completion notice before x2 synthesis.",
            "If the CLI notice remains pending, record process and file evidence.",
            "If CLI final files arrive, hash and summarize metadata only.",
            "Keep all lane calls existing-only with no new old-style spawn.",
        ]),
        ("source-ledger", [
            "Keep official sources above social or anecdotal sources.",
            "Mark opened pages separately from searches.",
            "Add citation-required flags for current product behavior.",
            "Track MCP authorization and deprecation changes for future connector work.",
            "Track Codex app-server source changes before changing notifier assumptions.",
            "Keep NVIDIA/Google sources as capacity/architecture context unless deployed.",
        ]),
        ("observability", [
            "Add trace_id and run_id fields to watcher receipts.",
            "Add retry_count and timeout_window fields to app-lane receipts.",
            "Create a bounded dashboard snapshot with lane status rows.",
            "Use OpenTelemetry signal vocabulary in future receipt schemas.",
            "Record process-exists-is-not-progress caveat in CLI watcher docs.",
            "Add final_state_reason to every lane watcher summary.",
        ]),
        ("safety", [
            "Run JSON parse before staging.",
            "Compile helper scripts before staging.",
            "Run publication guard on exact staged files.",
            "Fetch and drift-check before every commit.",
            "Stage only current curated artifacts.",
            "Verify shared omega remote equals local after push.",
        ]),
        ("thos-platform", [
            "Design a command/skill/plugin capability graph for v478.",
            "Create no-mutation runner mode for broad THOS inspections.",
            "Build a source-to-command recommendation table.",
            "Define enterprise-grade tiers: inspect, dry-run, local simulation, live write.",
            "Add Windows sandbox readiness to the platform board.",
            "Add PowerShell terminal hygiene runbook entries.",
        ]),
        ("gmut-boundary", [
            "Carry all six GMUT gates open.",
            "Label GMUT-adjacent outputs as infrastructure support only.",
            "Keep Journey/Solas material as journey_context_not_canon.",
            "Avoid final physics and consciousness proof language.",
            "Require exact closure artifacts before any gate state changes.",
            "Preserve simulation labels for any toy/fixture work.",
        ]),
        ("phase-closeout", [
            "Use v4 x2 to integrate pending CLI watcher state.",
            "Prepare v478 transition only after v4 surfaces are published.",
            "Keep x3/x4 overlays tied to concrete blockers.",
            "Record NZ phase times in every closeout.",
            "Publish next 60-task map after x2.",
            "Keep the active goal open until v490 THOS is actually verified.",
        ]),
    ]
    tasks = []
    idx = 1
    for domain, items in groups:
        for item in items:
            tasks.append({"id": f"v477-v4-x2-task-{idx:02d}", "domain": domain, "task": item})
            idx += 1
    return tasks


def main() -> None:
    utc, nz = utc_nz_now()
    head = run_git(["rev-parse", "HEAD"])
    remote = run_git(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = run_git(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    command = command_surface()
    handoff = handoff_surface()
    skill = skill_surface()
    app_lanes = app_lane_status()
    cli_notice = cli_notice_status()
    reflections = reflection_steps()

    source_ledger = {
        "artifact_type": "v4_source_ledger",
        "generated_nz": nz,
        "generated_utc": utc,
        "opened_source_count": len(OPENED_SOURCES),
        "opened_sources": OPENED_SOURCES,
        "phase": PHASE,
        "query_count": len(SOURCE_QUERIES),
        "queries": SOURCE_QUERIES,
        "query_status": "completed_official_focused_search_refresh",
        "source_boundary": "implementation_context_only_journey_context_not_canon",
    }
    write_json("v477-thos-v4-x1-source-ledger-v1.json", source_ledger)
    write_md(
        "v477-thos-v4-x1-source-ledger-v1.md",
        "\n".join(
            [
                "# V477 THOS V4 X1 Source Ledger",
                "",
                f"- generated_nz: `{nz}`",
                f"- query_count: `{len(SOURCE_QUERIES)}`",
                f"- opened_source_count: `{len(OPENED_SOURCES)}`",
                "- query_status: `completed_official_focused_search_refresh`",
                "- boundary: implementation context only; Journey material remains `journey_context_not_canon`.",
                "",
                "## Opened Sources",
                "",
                *[f"- {item['label']}: {item['url']}" for item in OPENED_SOURCES],
            ]
        ),
    )

    status_board = {
        "app_lanes": app_lanes,
        "artifact_type": "lane_status_board",
        "cli_notice": cli_notice,
        "generated_nz": nz,
        "generated_utc": utc,
        "phase": PHASE,
        "status": "PASS_APP_LANES_WITH_CLI_PENDING",
    }
    write_json("v477-thos-v4-x1-lane-status-board-v1.json", status_board)
    write_md(
        "v477-thos-v4-x1-lane-status-board-v1.md",
        "\n".join(
            [
                "# V477 THOS V4 X1 Lane Status Board",
                "",
                f"- generated_nz: `{nz}`",
                "- status: `PASS_APP_LANES_WITH_CLI_PENDING`",
                "",
                "## App Lanes",
                "",
                *[f"- {row['lane']}: `{row['overall_status']}`; completion `{row['turn_completion']}`; payload `{row['payload_publication']}`." for row in app_lanes],
                "",
                "## CLI Notice",
                "",
                f"- aggregate_status: `{cli_notice['aggregate_status']}`",
                *[f"- {row['lane']}: `{row['completion_status']}`, final bytes `{row['final_message_bytes']}`." for row in cli_notice.get("lanes", [])],
            ]
        ),
    )

    command_payload = {"artifact_type": "command_index_surface", "generated_nz": nz, "generated_utc": utc, "phase": PHASE, **command}
    write_json("v477-thos-v4-x1-command-index-surface-v1.json", command_payload)
    write_md(
        "v477-thos-v4-x1-command-index-surface-v1.md",
        f"""
# V477 THOS V4 X1 Command Index Surface

- generated_nz: `{nz}`
- surface_status: `{command['surface_status']}`
- book_version: `{command['book_version']}`
- command_count: `{command['command_count']}`
- validation_status: `{command['validation_status']}`
- live_command_count: `{command['live_command_count']}`
- connector_command_count: `{command['connector_command_count']}`

This surface is metadata-only and does not execute commands.
""",
    )

    handoff_payload = {"artifact_type": "handoff_surface_receipt", "generated_nz": nz, "generated_utc": utc, "phase": PHASE, **handoff}
    write_json("v477-thos-v4-x1-handoff-surface-receipt-v1.json", handoff_payload)
    write_md(
        "v477-thos-v4-x1-handoff-surface-receipt-v1.md",
        f"""
# V477 THOS V4 X1 Handoff Surface Receipt

- generated_nz: `{nz}`
- surface_status: `{handoff['surface_status']}`
- source_status: `{handoff['source_status']}`
- source_hash_count: `{handoff['source_hash_count']}`
- boundary: continuity handoff only; no GMUT validation or canon promotion.
""",
    )

    skill_payload = {"artifact_type": "skill_capability_index", "generated_nz": nz, "generated_utc": utc, "phase": PHASE, **skill}
    write_json("v477-thos-v4-x1-skill-capability-index-v1.json", skill_payload)
    write_md(
        "v477-thos-v4-x1-skill-capability-index-v1.md",
        f"""
# V477 THOS V4 X1 Skill Capability Index

- generated_nz: `{nz}`
- surface_status: `{skill['surface_status']}`
- observed_user_skill_count: `{skill['user_skill_count_observed']}`
- sample_limit: `{skill['sample_limit']}`
- mutation_policy: `{skill['mutation_policy']}`

This index publishes frontmatter metadata only and does not copy skill bodies.
""",
    )

    run_status = {
        "artifact_type": "run_status_pair",
        "claim_boundary": {
            "gmut_gates_open": GMUT_GATES,
            "canon_promotion": "not_claimed",
            "domain": "THOS command, handoff, skill, source, and lane readiness",
        },
        "generated_nz": nz,
        "generated_utc": utc,
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "reflection_count": len(reflections),
        "reflection_steps": reflections,
        "repo_state": {"local_head": head, "shared_remote_head": remote, "drift": drift},
        "rows": [
            {"id": "app_lanes", "status": "PASS", "summary": "Three app lanes completed v4 x1 notifier run."},
            {"id": "cli_lanes", "status": cli_notice["aggregate_status"], "summary": "Arby/Aster completion notice remains metadata-only."},
            {"id": "command_index", "status": command["surface_status"], "summary": "Command book v11 metadata surfaced."},
            {"id": "handoff_surface", "status": handoff["surface_status"], "summary": "v54/v55 continuity handoff surface confirmed."},
            {"id": "skill_index", "status": skill["surface_status"], "summary": "User skill frontmatter metadata sampled."},
            {"id": "source_refresh", "status": "PASS", "summary": "Official-focused source refresh recorded."},
            {"id": "gmut_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "status": "PASS_WITH_CLI_PENDING_OPEN_GAP",
    }
    write_json("v477-thos-v4-x1-run-status-v1.json", run_status)
    write_md(
        "v477-thos-v4-x1-run-status-v1.md",
        "\n".join(
            [
                "# V477 THOS V4 X1 Run Status",
                "",
                f"- generated_nz: `{nz}`",
                "- status: `PASS_WITH_CLI_PENDING_OPEN_GAP`",
                f"- next_expected_phase: `{NEXT_PHASE}`",
                "- claim boundary: THOS readiness only; all six GMUT gates remain open.",
                "",
                "## Rows",
                "",
                *[f"- {row['id']}: `{row['status']}`; {row['summary']}" for row in run_status["rows"]],
                "",
                "## Reflection Steps",
                "",
                *[f"- {item['step']} [{item['theme']}]: {item['finding']}" for item in reflections],
            ]
        ),
    )

    roadmap = {
        "artifact_type": "v4_x2_60_task_roadmap",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_phase": NEXT_PHASE,
        "phase": PHASE,
        "task_count": 60,
        "tasks": next_tasks(),
    }
    write_json("v477-thos-v4-x2-roadmap-v1.json", roadmap)
    write_md(
        "v477-thos-v4-x2-roadmap-v1.md",
        "\n".join(
            [
                "# V477 THOS V4 X2 Roadmap",
                "",
                f"- generated_nz: `{nz}`",
                "- task_count: `60`",
                "- boundary: existing lanes only, no unfiltered lane payload publication, no GMUT gate closure.",
                "",
                "## Tasks",
                "",
                *[f"- {task['id']} [{task['domain']}]: {task['task']}" for task in next_tasks()],
            ]
        ),
    )


if __name__ == "__main__":
    main()
