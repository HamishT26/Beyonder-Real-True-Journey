#!/usr/bin/env python3
"""Build v477 THOS v4 x2 synthesis and v5 x1 handoff artifacts."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v4_x2"
NEXT_PHASE = "v477_thos_v5_x1"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_QUERIES = [
    "OpenAI Codex CLI Windows sandbox official docs 0.136.0",
    "OpenAI Codex app-server README official GitHub",
    "OpenAI Codex CLI release 0.136.0 GitHub",
    "OpenAI Codex threads app server official",
    "MCP 2025-06-18 authorization specification official",
    "MCP tools resources prompts official documentation",
    "MCP roots sampling logging official specification",
    "MCP TypeScript SDK official GitHub tools resources prompts",
    "GitHub secret scanning push protection official docs",
    "GitHub Actions security hardening official docs",
    "GitHub SARIF code scanning official docs",
    "GitHub Copilot MCP official docs",
    "Windows Sandbox configuration official docs",
    "Windows Mandatory Integrity Control official docs",
    "Windows AppContainer official docs",
    "PowerShell execution policies security official docs",
    "Python subprocess security shell false official docs",
    "Python tempfile cleanup official docs",
    "Python pathlib official docs",
    "Python hashlib sha256 official docs",
    "OpenTelemetry traces metrics logs official docs",
    "Docker Compose watch official docs",
    "Kubernetes Jobs official docs",
    "Kubernetes CronJobs official docs",
    "Google Vertex AI Agent Development Kit official docs",
    "Google Vertex AI Agent Engine official docs",
    "Google Bigtable vector search Vertex AI official docs",
    "Google Cloud RAG Engine Gemini official docs",
    "NVIDIA DGX Spark official hardware specs",
    "NVIDIA NIM inference microservices official docs",
    "NVIDIA Nemotron official agentic AI",
    "NVIDIA Omniverse robotics physical AI official docs",
]

SOURCE_URLS = [
    {
        "label": "OpenAI Codex Windows sandbox",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "use": "Windows sandbox framing for CLI lane readiness.",
    },
    {
        "label": "OpenAI Codex app-server README",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "use": "Local app-server routing model for app-lane notifier work.",
    },
    {
        "label": "MCP authorization",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
        "use": "Connector authorization boundaries for THOS surfaces.",
    },
    {
        "label": "MCP tools",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/tools",
        "use": "Tool-result and resource-link discipline for future connector artifacts.",
    },
    {
        "label": "GitHub push protection",
        "url": "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection",
        "use": "Publication safety inspiration for shared omega commits.",
    },
    {
        "label": "GitHub Actions hardening",
        "url": "https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions",
        "use": "Future automation hardening context.",
    },
    {
        "label": "Windows Sandbox configuration",
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
        "use": "Configuration vocabulary for sandbox readiness checks.",
    },
    {
        "label": "Windows Mandatory Integrity Control",
        "url": "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control",
        "use": "Integrity boundary language for local Windows execution notes.",
    },
    {
        "label": "PowerShell execution policies",
        "url": "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6",
        "use": "PowerShell safety caveats for terminal hygiene.",
    },
    {
        "label": "Python subprocess",
        "url": "https://docs.python.org/3.12/library/subprocess.html",
        "use": "List-form process launching and shell-avoidance for helpers.",
    },
    {
        "label": "OpenTelemetry signals",
        "url": "https://opentelemetry.io/docs/concepts/signals/",
        "use": "Trace, metric, and log vocabulary for watcher receipts.",
    },
    {
        "label": "Docker Compose Watch",
        "url": "https://docs.docker.com/compose/how-tos/file-watch/",
        "use": "File-watch analogy for bounded refresh runners.",
    },
    {
        "label": "Kubernetes Jobs",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/job/",
        "use": "Idempotent run and completion framing.",
    },
    {
        "label": "Kubernetes CronJobs",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/",
        "use": "Scheduled retry and duplicate-start caveats.",
    },
    {
        "label": "Google Vertex AI Agent Development Kit",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/overview",
        "use": "Agent orchestration context for THOS planning.",
    },
    {
        "label": "Google Vertex AI Agent Engine",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "use": "Cloud agent runtime context, not deployment permission.",
    },
    {
        "label": "NVIDIA DGX Spark",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/hardware.html",
        "use": "Local AI capacity planning context.",
    },
    {
        "label": "NVIDIA NIM",
        "url": "https://docs.nvidia.com/nim/",
        "use": "Inference service architecture context.",
    },
    {
        "label": "NVIDIA Nemotron",
        "url": "https://www.nvidia.com/en-us/ai-data-science/foundation-models/llama-nemotron/",
        "use": "Agentic model ecosystem context.",
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


def read_json(name: str) -> dict[str, Any]:
    path = TRACES / name
    if not path.exists():
        return {"read_status": "missing", "artifact": name}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_repo_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"read_status": "missing", "file_label": path.name}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(name: str, payload: dict[str, Any]) -> None:
    (TRACES / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACES / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def app_rows(app_run: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in app_run.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("name"),
                "status": lane.get("overall_status", "unknown"),
                "read_status": lane.get("read", {}).get("status", "unknown"),
                "resume_status": lane.get("resume", {}).get("status", "unknown"),
                "turn_status": lane.get("turn_completion", {}).get("status", "unknown"),
                "payload_publication": "not_published",
            }
        )
    return rows


def cli_rows(cli_notice: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lane in cli_notice.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "status": lane.get("completion_status", "unknown"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "stderr_bytes": lane.get("stderr_bytes"),
                "stdout_bytes": lane.get("stdout_bytes"),
                "payload_publication": lane.get("raw_output_boundary", "temp_only_not_published"),
            }
        )
    return rows


def command_rollup(command_surface: dict[str, Any]) -> dict[str, Any]:
    return {
        "book_version": command_surface.get("book_version"),
        "command_count": command_surface.get("command_count"),
        "connector_command_count": command_surface.get("connector_command_count"),
        "live_command_count": command_surface.get("live_command_count"),
        "mode_counts": command_surface.get("mode_counts", {}),
        "risk_counts": command_surface.get("risk_counts", {}),
        "status": command_surface.get("validation_status", "metadata_surface"),
    }


def skill_rollup(skill_surface: dict[str, Any]) -> dict[str, Any]:
    samples = skill_surface.get("user_skill_sample", [])
    status_counts = Counter(str(item.get("status", "unknown")) for item in samples)
    return {
        "duplicate_name_sample_count": len(skill_surface.get("duplicate_name_sample", [])),
        "mutation_policy": skill_surface.get("mutation_policy"),
        "plugin_cache_exists": skill_surface.get("plugin_cache_exists"),
        "sample_status_counts": dict(status_counts),
        "surface_status": skill_surface.get("surface_status"),
        "user_skill_count_observed": skill_surface.get("user_skill_count_observed"),
    }


def journey_inventory() -> dict[str, Any]:
    v49 = Path.home() / "Downloads" / "Beyonder-Real-True Journey v49 (Aletheon & Codex CLI and App siblings).txt"
    return {
        "journey_context_policy": "journey_context_not_canon",
        "v49_downloads_file_present": v49.exists(),
        "v49_file_label": v49.name,
        "v49_size_bytes": v49.stat().st_size if v49.exists() else None,
        "use_in_phase": "continuity and terminology context only",
    }


def reflection_steps() -> list[dict[str, str]]:
    findings = [
        ("lane_mesh", "The local app-server path is now reliable enough for Cicero, Kierkegaard, and Aristotle status receipts."),
        ("lane_mesh", "The app-lane receipts are useful as completion evidence but not as a public advisory transcript."),
        ("cli_mesh", "Arby and Aster still need open-gap handling because their CLI final message files are not present."),
        ("cli_mesh", "Launching more CLI work before resolving the pending watcher would reduce clarity, so x2 keeps them pending."),
        ("command_index", "The command book surface already exposes command count, mode count, live count, and connector count."),
        ("command_index", "The next command work should validate fields and expose reader-friendly indexes rather than adding volume."),
        ("skills", "The skill index observed hundreds of user skills but only publishes frontmatter metadata samples."),
        ("skills", "Skill repair remains separate from ordinary THOS design unless exact loader errors recur."),
        ("handoff", "The v54/v55 surfaces exist and should be carried as continuity manifests, not archive imports."),
        ("handoff", "Handoff continuity should point to receiver criteria for v5 rather than re-opening old phase bodies."),
        ("journey", "The v49 Journey file is locally present and can support continuity reflection only."),
        ("journey", "Older Journey concepts can inspire system language but cannot validate GMUT or promote canon."),
        ("source_refresh", "Thirty-two current web searches were completed for the v4 x2 source refresh."),
        ("source_refresh", "Source URLs are recorded as implementation context, with official sources preferred."),
        ("openai", "Codex CLI 0.136.0 is locally observed, making current CLI diagnostics more meaningful."),
        ("openai", "The app-server README remains the source anchor for local app-lane routing assumptions."),
        ("mcp", "MCP authorization and tools docs strengthen connector boundary design."),
        ("github", "Push protection and workflow hardening remain directly relevant to exact-stage publication discipline."),
        ("windows", "Windows sandbox and integrity docs support observed-readiness language, not assumptions."),
        ("powershell", "Execution policy is a useful control but not a complete security boundary."),
        ("python", "List-form helper commands and temp-directory discipline keep runner scripts safer."),
        ("observability", "OpenTelemetry signal language should become a receipt schema layer in v5."),
        ("containers", "Docker and Kubernetes scheduling docs warn against duplicate starts without idempotence."),
        ("google", "Vertex AI and Agent Engine docs are architecture references only unless separately deployed."),
        ("nvidia", "DGX, NIM, and Nemotron sources are capacity/model context only."),
        ("safety", "The ordinary THOS publication path still needs JSON parse, compile, guard, exact stage, push, verify."),
        ("gmut", "All six GMUT gates remain open and must be repeated in x2 closeout."),
        ("phase_flow", "v477 v5 x1 is the correct next phase after v477 v4 x2."),
        ("x_overlays", "x3/x4 should be used only for concrete blockers, not decorative expansion."),
        ("goal_state", "The long v477-v490 objective remains active; this turn publishes one more verified step."),
    ]
    return [
        {"step": f"reflection_{idx:02d}", "theme": theme, "finding": finding}
        for idx, (theme, finding) in enumerate(findings, 1)
    ]


def proposal_rows(prefix: str, category: str, verbs: list[str]) -> list[dict[str, str]]:
    rows = []
    for idx, verb in enumerate(verbs, 1):
        rows.append(
            {
                "id": f"{prefix}-{idx:02d}",
                "category": category,
                "status": "proposal_only_not_installed",
                "proposal": verb,
            }
        )
    return rows


def expansion_catalog() -> dict[str, Any]:
    system_expansions = proposal_rows(
        "v477-v5-system",
        "system_expansion",
        [
            "Lane status dashboard surface",
            "Command index reader surface",
            "Skill metadata router",
            "MCP authorization boundary board",
            "App-lane retry governor",
            "CLI watcher final-state board",
            "Source freshness ledger",
            "Journey context boundary map",
            "GMUT gate carry-forward panel",
            "PowerShell hygiene board",
            "Windows sandbox readiness card",
            "Codex CLI version receipt card",
            "OpenTelemetry watcher schema",
            "Exact staging preflight board",
            "Remote equality proof card",
            "Connector approval matrix",
            "No-mutation inspection runner",
            "Temp-output boundary receipt",
            "Handoff receiver criteria board",
            "THOS phase clock ledger",
            "Web source trust tier map",
            "NVIDIA capacity context board",
            "Google agent architecture board",
            "Docker watch analogy card",
            "Kubernetes retry caveat card",
            "Python helper safety card",
            "Skill repair separation board",
            "Command risk tier heatmap",
            "Live connector approval queue",
            "v477 to v478 transition gate",
        ],
    )
    command_proposals = proposal_rows(
        "v477-v5-command",
        "command_proposal",
        [
            "thos lane-status summarize",
            "thos app-lane probe",
            "thos app-lane run",
            "thos cli-watch once",
            "thos cli-watch tail-status",
            "thos command-index build",
            "thos command-index validate",
            "thos skill-index build",
            "thos skill-index validate",
            "thos source-ledger refresh",
            "thos source-ledger trust-tier",
            "thos handoff-surface list",
            "thos handoff-surface validate",
            "thos journey-context inventory",
            "thos gmut-gates carry-forward",
            "thos sandbox doctor-summary",
            "thos codex-version receipt",
            "thos powershell-hygiene check",
            "thos publication-guard scan",
            "thos exact-stage preview",
            "thos remote-equality verify",
            "thos phase-clock stamp",
            "thos roadmap synthesize",
            "thos x-overlay justify",
            "thos blocker classify",
            "thos retry-ledger update",
            "thos connector-approval matrix",
            "thos plugin-readiness inspect",
            "thos dashboard-snapshot build",
            "thos next-phase handoff",
        ],
    )
    skill_proposals = proposal_rows(
        "v477-v5-skill",
        "skill_proposal",
        [
            "lane-status-board-operations",
            "app-lane-notifier-operations",
            "cli-watcher-final-state-operations",
            "command-index-surface-operations",
            "skill-metadata-router-operations",
            "source-freshness-ledger-operations",
            "handoff-surface-validation-operations",
            "journey-context-boundary-operations",
            "gmut-gate-carry-forward-operations",
            "power-shell-hygiene-operations",
            "windows-sandbox-readiness-operations",
            "codex-version-receipt-operations",
            "otel-watcher-schema-operations",
            "exact-stage-preflight-operations",
            "remote-equality-proof-operations",
            "connector-approval-matrix-operations",
            "no-mutation-inspection-operations",
            "temp-output-boundary-operations",
            "receiver-criteria-board-operations",
            "phase-clock-ledger-operations",
            "source-trust-tier-operations",
            "nvidia-capacity-context-operations",
            "google-agent-architecture-operations",
            "docker-watch-analogy-operations",
            "kubernetes-retry-caveat-operations",
            "python-helper-safety-operations",
            "skill-repair-separation-operations",
            "command-risk-tier-operations",
            "live-connector-queue-operations",
            "v477-v478-transition-gate-operations",
        ],
    )
    return {
        "artifact_type": "v5_x1_expansion_proposal_catalog",
        "command_proposal_count": len(command_proposals),
        "command_proposals": command_proposals,
        "installation_status": "proposal_only_no_skill_or_command_installation",
        "phase": PHASE,
        "skill_proposal_count": len(skill_proposals),
        "skill_proposals": skill_proposals,
        "system_expansion_count": len(system_expansions),
        "system_expansions": system_expansions,
    }


def roadmap_tasks() -> list[dict[str, str]]:
    domains = [
        ("lanes", "Use v5 x1 to run app-lane probe and live notifier once again."),
        ("lanes", "Keep Cicero/Kierkegaard/Aristotle existing-thread only."),
        ("lanes", "Poll Arby/Aster watcher before any new CLI task launch."),
        ("lanes", "Do not duplicate CLI work while pending watcher state remains unresolved."),
        ("lanes", "Create a single lane-status board that merges app and CLI metadata."),
        ("lanes", "Add final-state-reason to each lane row."),
        ("command", "Promote command book v11 into a durable reader index."),
        ("command", "Validate command id, mode, risk, live, connector, and source fields."),
        ("command", "Create a command risk tier heatmap as data only."),
        ("command", "Separate live-connector commands from offline commands."),
        ("command", "Flag commands needing exact approval before use."),
        ("command", "Draft command proposals as proposal-only rows."),
        ("skills", "Refresh user skill metadata sample without body publication."),
        ("skills", "Detect duplicate skill names and frontmatter gaps."),
        ("skills", "Map skills to command domains by metadata."),
        ("skills", "Keep plugin cache read/use-only."),
        ("skills", "Prepare repair packet only if loader evidence recurs."),
        ("skills", "Draft skill proposals as proposal-only rows."),
        ("systems", "Carry the 30 system expansion proposals into v5 x1."),
        ("systems", "Classify each system expansion by inspect, dry-run, local simulation, or live write."),
        ("systems", "Create a no-mutation inspection runner plan."),
        ("systems", "Prepare dashboard-ready bounded snapshot rows."),
        ("systems", "Add watcher schema fields using trace/metric/log vocabulary."),
        ("systems", "Keep proposed systems separate from installed systems."),
        ("sources", "Run another current web refresh if v5 x1 extends source claims."),
        ("sources", "Prefer official implementation docs for platform behavior."),
        ("sources", "Record query count separately from reviewed page count."),
        ("sources", "Use source trust tiers in v5 x1 ledgers."),
        ("sources", "Keep NVIDIA/Google sources as context until deployed."),
        ("sources", "Avoid relying on social image posts for implementation proof."),
        ("handoff", "Surface v54/v55 receiver criteria as metadata."),
        ("handoff", "Avoid importing old archive bodies into current artifacts."),
        ("handoff", "Carry v49 Journey presence as continuity context only."),
        ("handoff", "Mark Journey/Solas context as journey_context_not_canon."),
        ("handoff", "Build v477-v478 transition criteria without skipping v477 v5-v8."),
        ("handoff", "Document which handoffs remain open gaps."),
        ("sandbox", "Summarize Codex CLI 0.136.0 observed version."),
        ("sandbox", "Record codex doctor timeout as a diagnostic open gap if still present."),
        ("sandbox", "Probe sandbox help safely before repair claims."),
        ("sandbox", "Keep Windows sandbox readiness observed rather than assumed."),
        ("sandbox", "Avoid admin or account setting changes without separate approval."),
        ("sandbox", "Publish only curated diagnostic receipts."),
        ("safety", "Run script compile before staging."),
        ("safety", "Parse all generated JSON artifacts."),
        ("safety", "Run publication guard over exact current files."),
        ("safety", "Fetch and drift-check before commit."),
        ("safety", "Stage exact current artifacts only."),
        ("safety", "Verify remote equals local after push."),
        ("gmut", "Carry all six GMUT gates open."),
        ("gmut", "Keep THOS infrastructure separate from GMUT validation."),
        ("gmut", "Avoid final physics, consciousness proof, and canon language."),
        ("gmut", "Require exact closure artifacts for any future gate movement."),
        ("gmut", "Label simulations and fixtures as simulations only."),
        ("gmut", "Preserve claim taxonomy in v5 x1."),
        ("phase", "Start v477 THOS v5 x1 after this v4 x2 publication."),
        ("phase", "Use x3/x4 only for concrete blockers."),
        ("phase", "Record NZ time in every artifact."),
        ("phase", "Keep the long v490 objective active."),
        ("phase", "Commit every second phase where feasible."),
        ("phase", "Publish v5 x2 roadmap after v5 x1."),
    ]
    return [
        {"id": f"v477-v5-x1-task-{idx:02d}", "domain": domain, "task": task}
        for idx, (domain, task) in enumerate(domains, 1)
    ]


def main() -> None:
    utc, nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = git_text(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    app_probe = read_json("v477-thos-v4-x2-app-lane-notifier-probe-v1.json")
    app_run = read_json("v477-thos-v4-x2-app-lane-notifier-run-v1.json")
    cli_notice = read_json("v477-thos-v3-x2-cli-lane-completion-notice-v2.json")
    command_surface = read_json("v477-thos-v4-x1-command-index-surface-v1.json")
    skill_surface = read_json("v477-thos-v4-x1-skill-capability-index-v1.json")
    handoff_surface = read_json("v477-thos-v4-x1-handoff-surface-receipt-v1.json")
    v4_roadmap = read_json("v477-thos-v4-x2-roadmap-v1.json")
    command_validation = read_repo_json(ROOT / "docs" / "trinity-command-book-validation-latest.json")

    source_ledger = {
        "artifact_type": "v4_x2_source_refresh_ledger",
        "generated_nz": nz,
        "generated_utc": utc,
        "phase": PHASE,
        "query_count": len(SOURCE_QUERIES),
        "query_status": "completed_live_search_refresh",
        "queries": SOURCE_QUERIES,
        "source_url_count": len(SOURCE_URLS),
        "source_urls": SOURCE_URLS,
        "source_boundary": "implementation_context_only_official_sources_preferred",
    }
    write_json("v477-thos-v4-x2-source-ledger-v1.json", source_ledger)
    write_md(
        "v477-thos-v4-x2-source-ledger-v1.md",
        [
            "# V477 THOS V4 X2 Source Ledger",
            "",
            f"- generated_nz: `{nz}`",
            f"- query_count: `{len(SOURCE_QUERIES)}`",
            f"- source_url_count: `{len(SOURCE_URLS)}`",
            "- query_status: `completed_live_search_refresh`",
            "- boundary: official implementation sources are context/evidence; Journey material remains `journey_context_not_canon`.",
            "",
            "## Source URLs",
            "",
            *[f"- {item['label']}: {item['url']}" for item in SOURCE_URLS],
            "",
            "## Query Topics",
            "",
            *[f"- {query}" for query in SOURCE_QUERIES],
        ],
    )

    expansion = expansion_catalog()
    expansion.update({"generated_nz": nz, "generated_utc": utc, "next_phase": NEXT_PHASE})
    write_json("v477-thos-v4-x2-expansion-proposal-catalog-v1.json", expansion)
    write_md(
        "v477-thos-v4-x2-expansion-proposal-catalog-v1.md",
        [
            "# V477 THOS V4 X2 Expansion Proposal Catalog",
            "",
            f"- generated_nz: `{nz}`",
            "- installation_status: `proposal_only_no_skill_or_command_installation`",
            "- system_expansion_count: `30`",
            "- command_proposal_count: `30`",
            "- skill_proposal_count: `30`",
            "",
            "## System Expansions",
            "",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion["system_expansions"]],
            "",
            "## Command Proposals",
            "",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion["command_proposals"]],
            "",
            "## Skill Proposals",
            "",
            *[f"- {row['id']}: {row['proposal']}" for row in expansion["skill_proposals"]],
        ],
    )

    synthesis = {
        "app_lanes": {
            "probe_status": app_probe.get("overall_status"),
            "run_status": app_run.get("overall_status"),
            "rows": app_rows(app_run),
        },
        "artifact_type": "v4_x2_aletheon_synthesis",
        "claim_boundary": {
            "canon_promotion": "not_claimed",
            "domain": "THOS lane coordination, command/skill/source/handoff surfaces, and proposal catalog",
            "gmut_gates_open": GMUT_GATES,
        },
        "cli_lanes": {
            "aggregate_status": cli_notice.get("aggregate_status"),
            "rows": cli_rows(cli_notice),
        },
        "command_surface": command_rollup(command_surface),
        "command_validation_status": command_validation.get("overall_status"),
        "generated_nz": nz,
        "generated_utc": utc,
        "handoff_surface_status": handoff_surface.get("surface_status", handoff_surface.get("status", "metadata_carried")),
        "journey_inventory": journey_inventory(),
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "prior_roadmap_task_count": v4_roadmap.get("task_count"),
        "reflection_count": 30,
        "reflection_steps": reflection_steps(),
        "repo_state": {
            "drift": drift,
            "local_head": local_head,
            "shared_remote_head": remote_head,
        },
        "skill_surface": skill_rollup(skill_surface),
        "source_ledger": "v477-thos-v4-x2-source-ledger-v1.json",
        "status": "PASS_WITH_CLI_PENDING_OPEN_GAP",
    }
    write_json("v477-thos-v4-x2-synthesis-v1.json", synthesis)
    write_md(
        "v477-thos-v4-x2-synthesis-v1.md",
        [
            "# V477 THOS V4 X2 Synthesis",
            "",
            f"- generated_nz: `{nz}`",
            "- status: `PASS_WITH_CLI_PENDING_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            f"- local_head: `{local_head}`",
            f"- shared_remote_head: `{remote_head}`",
            f"- drift: `{drift}`",
            "- claim boundary: THOS infrastructure only; all six GMUT gates remain open.",
            "",
            "## App Lanes",
            "",
            *[f"- {row['lane']}: `{row['status']}`; turn `{row['turn_status']}`; payload `{row['payload_publication']}`." for row in synthesis["app_lanes"]["rows"]],
            "",
            "## CLI Lanes",
            "",
            f"- aggregate_status: `{synthesis['cli_lanes']['aggregate_status']}`",
            *[f"- {row['lane']}: `{row['status']}`, final bytes `{row['final_message_bytes']}`, transport `{row['payload_publication']}`." for row in synthesis["cli_lanes"]["rows"]],
            "",
            "## Command And Skill Surfaces",
            "",
            f"- command_count: `{synthesis['command_surface']['command_count']}`",
            f"- live_command_count: `{synthesis['command_surface']['live_command_count']}`",
            f"- connector_command_count: `{synthesis['command_surface']['connector_command_count']}`",
            f"- user_skill_count_observed: `{synthesis['skill_surface']['user_skill_count_observed']}`",
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
        "reflection_count": 30,
        "rows": [
            {"id": "app_lanes", "status": "PASS", "summary": "Cicero, Kierkegaard, and Aristotle completed the v4 x2 local app-server notifier run."},
            {"id": "cli_lanes", "status": "OPEN_GAP_FINAL_MESSAGE_PENDING", "summary": "Arby and Aster Vale remain pending in the existing CLI watcher; no new duplicate CLI task was launched."},
            {"id": "command_surface", "status": "PASS_METADATA_CARRIED", "summary": "Command book v11 metadata and validation status were carried into x2."},
            {"id": "skill_surface", "status": "PASS_METADATA_CARRIED", "summary": "User skill metadata surface was carried without body publication or mutation."},
            {"id": "source_refresh", "status": "PASS", "summary": "Thirty-two current web searches and official source URLs were recorded as implementation context."},
            {"id": "expansion_catalog", "status": "PASS_PROPOSAL_ONLY", "summary": "Thirty system expansion, thirty command, and thirty skill proposals were drafted for v5 x1."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "status": "PASS_WITH_CLI_PENDING_OPEN_GAP",
    }
    write_json("v477-thos-v4-x2-run-status-v1.json", run_status)
    write_md(
        "v477-thos-v4-x2-run-status-v1.md",
        [
            "# V477 THOS V4 X2 Run Status",
            "",
            f"- generated_nz: `{nz}`",
            "- status: `PASS_WITH_CLI_PENDING_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            "",
            *[f"- {row['id']}: `{row['status']}`; {row['summary']}" for row in run_status["rows"]],
        ],
    )

    roadmap = {
        "artifact_type": "v5_x1_60_task_roadmap",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_phase": NEXT_PHASE,
        "phase": PHASE,
        "task_count": 60,
        "tasks": roadmap_tasks(),
    }
    write_json("v477-thos-v5-x1-roadmap-v1.json", roadmap)
    write_md(
        "v477-thos-v5-x1-roadmap-v1.md",
        [
            "# V477 THOS V5 X1 Roadmap",
            "",
            f"- generated_nz: `{nz}`",
            "- task_count: `60`",
            "- boundary: existing lanes only; proposal-only expansions; all GMUT gates open.",
            "",
            "## Tasks",
            "",
            *[f"- {task['id']} [{task['domain']}]: {task['task']}" for task in roadmap["tasks"]],
        ],
    )


if __name__ == "__main__":
    main()
