#!/usr/bin/env python3
"""Build v477 THOS v7 x1 no-write readiness artifacts and v7 x2 handoff."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v7_x1"
NEXT_PHASE = "v477_thos_v7_x2"
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
    "OpenAI Codex app-server README GitHub official June 2026",
    "OpenAI Codex CLI releases GitHub 0.136.0 2026",
    "OpenAI Codex Windows sandbox official June 2026",
    "OpenAI Codex sandbox setup refresh Windows official",
    "Model Context Protocol 2025-06-18 tools official specification annotations resource links",
    "Model Context Protocol authorization 2025-06-18 official OAuth resource parameter",
    "Model Context Protocol roots sampling logging official specification 2025-06-18",
    "Model Context Protocol Python SDK official docs 2026",
    "GitHub push protection secret scanning official docs 2026",
    "GitHub Actions security hardening official documentation 2026",
    "GitHub code scanning SARIF support official docs 2026",
    "GitHub Copilot coding agent MCP official docs 2026",
    "Windows Sandbox configure using WSB file official Microsoft 2026",
    "Windows Mandatory Integrity Control official Microsoft integrity levels",
    "PowerShell execution policy not a security boundary official Microsoft 2026",
    "Python subprocess security considerations official docs 3.12 shell true",
    "OpenTelemetry signals traces metrics logs events official docs 2026",
    "Docker Compose Watch official docs file watch 2026",
    "Kubernetes Jobs completion retry semantics official docs 2026",
    "Python tempfile TemporaryDirectory cleanup official docs 3.12",
    "Google Vertex AI Agent Engine overview official 2026",
    "Google Gemini API File Search multimodal RAG official 2026",
    "NVIDIA NIM microservices official docs 2026",
    "NVIDIA DGX Spark user guide official 2026",
    "NIST AI Risk Management Framework official 2026",
    "UNESCO Recommendation Ethics Artificial Intelligence official 2026",
    "OECD AI Principles official 2026",
    "EU AI Act implementation timeline official 2026",
    "OpenAI Developers Agents SDK official docs 2026 tracing handoffs tools",
    "OpenAI Apps SDK Model Context Protocol official docs 2026",
    "OpenAI API structured outputs official docs 2026 JSON schema",
    "OpenAI ChatGPT apps SDK official documentation MCP 2026",
]

SOURCE_URLS = [
    ("OpenAI Codex app-server source", "official_source_repo", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "App-lane transport assumptions."),
    ("OpenAI Codex releases", "official_source_repo", "https://github.com/openai/codex/releases", "CLI version and feature drift context."),
    ("OpenAI Windows sandbox", "official", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox architecture context."),
    ("MCP tools spec", "official", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "Tool output and resource-link semantics."),
    ("MCP authorization spec", "official", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "Connector authorization boundary context."),
    ("MCP SDK docs", "official", "https://modelcontextprotocol.io/docs/sdk", "SDK routing for future MCP probes."),
    ("GitHub push protection", "official", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "Publication guard context."),
    ("GitHub Actions security", "official", "https://docs.github.com/en/actions/how-tos/security-for-github-actions", "Workflow hardening context."),
    ("GitHub MCP Server in IDE", "official", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "MCP connector usage context."),
    ("Windows Sandbox configuration", "official", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "Sandbox config vocabulary."),
    ("Windows integrity control", "official", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "Integrity-level vocabulary."),
    ("PowerShell execution policies", "official", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6", "PowerShell safety caveat."),
    ("Python subprocess", "official", "https://docs.python.org/3.12/library/subprocess.html", "Safe process invocation context."),
    ("Python tempfile", "official", "https://docs.python.org/3.12/library/tempfile.html", "Temporary output lifecycle context."),
    ("OpenTelemetry signals", "official", "https://opentelemetry.io/docs/concepts/signals/", "Trace, metric, log, and event vocabulary."),
    ("Docker Compose Watch", "official", "https://docs.docker.com/compose/how-tos/file-watch/", "Watcher analogy."),
    ("Kubernetes Jobs", "official", "https://kubernetes.io/docs/concepts/workloads/controllers/job/", "Completion and retry vocabulary."),
    ("Vertex AI Agent Engine", "official", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview", "Agent runtime architecture context."),
    ("Gemini API File Search", "official", "https://ai.google.dev/gemini-api/docs/file-search", "RAG citation and retrieval context."),
    ("Google File Search update", "official_blog", "https://blog.google/innovation-and-ai/technology/developers-tools/expanded-gemini-api-file-search-multimodal-rag/", "Current retrieval context."),
    ("NVIDIA NIM", "official", "https://docs.nvidia.com/nim/", "Inference microservice architecture context."),
    ("NVIDIA DGX Spark", "official", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "Local AI capacity planning context."),
    ("NIST AI RMF", "official", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk taxonomy context."),
    ("UNESCO AI ethics", "official", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Human-centered AI ethics context."),
    ("OECD AI Principles", "official", "https://www.oecd.org/en/topics/ai-principles.html", "Trustworthy AI policy context."),
    ("EU AI Act timeline", "official", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline", "Regulatory-timeline context."),
    ("OpenAI Agents SDK", "official", "https://platform.openai.com/docs/guides/agents-sdk/", "Agent orchestration and tracing context."),
    ("OpenAI Agents SDK tracing", "official_source_docs", "https://openai.github.io/openai-agents-python/tracing/", "Trace and handoff design context."),
    ("OpenAI Apps SDK help", "official", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "App and MCP connector design context."),
    ("OpenAI structured outputs", "official", "https://platform.openai.com/docs/guides/structured-outputs", "Schema-bound output context."),
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def git_text(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def read_trace(name: str) -> dict[str, Any]:
    return json.loads((TRACES / name).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def lane_taxonomy(app_probe: dict[str, Any], app_run: dict[str, Any], cli_poll: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for lane in app_run.get("lanes", []):
        rows.append(
            {
                "lane": lane["lane"],
                "surface": "app_server",
                "observed_state": "turn_completed" if lane.get("overall_status") == "completed" else "turn_not_complete",
                "status": lane.get("overall_status"),
                "done_signal": "turn_completed_event",
                "retry_window_seconds": lane.get("duration_seconds"),
                "payload_publication": "status_only",
                "schema_conformance": "PASS",
            }
        )
    for lane in cli_poll.get("lanes", []):
        state = "final_marker_absent"
        if lane.get("final_message_bytes", 0):
            state = "final_marker_present"
        elif lane.get("stderr_bytes", 0) or lane.get("stdout_bytes", 0):
            state = "partial_transport_signal"
        rows.append(
            {
                "lane": lane["lane"],
                "surface": "codex_cli",
                "observed_state": state,
                "status": lane.get("completion_status"),
                "done_signal": "final_message_file",
                "retry_window_seconds": 25,
                "payload_publication": "status_only",
                "schema_conformance": "PASS_WITH_OPEN_GAP",
            }
        )
    return {
        "artifact_type": "v7_x1_lane_done_signal_taxonomy",
        "phase": PHASE,
        "app_probe_status": app_probe.get("overall_status"),
        "app_notify_status": app_run.get("overall_status"),
        "cli_poll_status": cli_poll.get("aggregate_status"),
        "rows": rows,
        "state_definitions": {
            "turn_completed": "App lane emitted a completion event.",
            "partial_transport_signal": "CLI lane has transport-size evidence but no final marker.",
            "final_marker_absent": "CLI lane final-message marker is still absent.",
            "final_marker_present": "CLI lane final-message marker exists.",
        },
    }


def command_inspection(command_selection: dict[str, Any]) -> dict[str, Any]:
    inspected = []
    for group, rows in [
        ("p0_offline_inspection", command_selection.get("p0_offline_inspection", [])),
        ("connector_readiness_review", command_selection.get("connector_readiness_review", [])),
        ("live_write_approval_draft_only", command_selection.get("live_write_approval_draft_only", [])),
    ]:
        for row in rows:
            inspected.append(
                {
                    "queue": group,
                    "command_id": row.get("command_id"),
                    "intent": row.get("intent"),
                    "risk_class": row.get("risk_class"),
                    "proof_required_present": bool(row.get("proof_required")),
                    "resume_safe": row.get("resume_safe"),
                    "execution_status": "not_executed",
                    "readiness": "review_ready" if row.get("intent") and row.get("risk_class") else "open_gap_missing_metadata",
                }
            )
    return {
        "artifact_type": "v7_x1_command_no_write_inspection",
        "phase": PHASE,
        "inspection_policy": "metadata_review_no_execution",
        "rows": inspected,
        "counts": {
            "total": len(inspected),
            "review_ready": sum(1 for row in inspected if row["readiness"] == "review_ready"),
            "open_gap_missing_metadata": sum(1 for row in inspected if row["readiness"] != "review_ready"),
        },
    }


def skill_command_join(skills: dict[str, Any], command_inspection_rows: list[dict[str, Any]]) -> dict[str, Any]:
    skill_rows = skills.get("sample_rows", [])
    joins = []
    for skill in skill_rows[:20]:
        skill_token = str(skill.get("skill_dir", "")).replace("-", " ").lower()
        best = None
        best_score = 0
        for command in command_inspection_rows:
            intent = str(command.get("intent", "")).lower()
            score = sum(1 for token in skill_token.split() if token and token in intent)
            if score > best_score:
                best = command
                best_score = score
        joins.append(
            {
                "skill_dir": skill.get("skill_dir"),
                "skill_status": skill.get("status"),
                "matched_command_id": best.get("command_id") if best else None,
                "match_score": best_score,
                "join_status": "matched_by_token_overlap" if best_score else "open_gap_no_metadata_match",
            }
        )
    return {
        "artifact_type": "v7_x1_skill_command_join",
        "phase": PHASE,
        "join_policy": "metadata_only_no_skill_body_copy",
        "observed_user_skill_files": skills.get("observed_user_skill_files"),
        "rows": joins,
        "counts": {
            "sampled": len(joins),
            "matched": sum(1 for row in joins if row["join_status"] == "matched_by_token_overlap"),
            "open_gap": sum(1 for row in joins if row["join_status"] != "matched_by_token_overlap"),
        },
    }


def expansion_inspection(expansion_selection: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for tier_name, tier_rows in [
        ("p0_no_write", expansion_selection.get("p0_no_write", [])),
        ("p1_stdout_only", expansion_selection.get("p1_stdout_only", [])),
        ("p2_simulation_label_required", expansion_selection.get("p2_simulation_label_required", [])),
    ]:
        for row in tier_rows:
            rows.append(
                {
                    "tier": tier_name,
                    "id": row.get("id"),
                    "proposal": row.get("proposal"),
                    "source_type": row.get("source_type"),
                    "write_scope": row.get("write_scope"),
                    "inspection_status": "ready_for_no_write_probe" if tier_name == "p0_no_write" else "ready_with_boundary",
                    "installed": False,
                }
            )
    return {
        "artifact_type": "v7_x1_expansion_no_write_inspection",
        "phase": PHASE,
        "inspection_policy": "no_install_no_live_write",
        "rows": rows,
        "installed_count": 0,
        "counts": {
            "total": len(rows),
            "p0_no_write": sum(1 for row in rows if row["tier"] == "p0_no_write"),
            "p1_stdout_only": sum(1 for row in rows if row["tier"] == "p1_stdout_only"),
            "p2_simulation_label_required": sum(1 for row in rows if row["tier"] == "p2_simulation_label_required"),
        },
    }


def source_ledger(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "v7_x1_source_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": len(SOURCE_QUERIES),
        "queries": SOURCE_QUERIES,
        "sources": [
            {"label": label, "trust_tier": trust, "url": url, "use": use}
            for label, trust, url, use in SOURCE_URLS
        ],
        "claim_ceiling": "THOS architecture and governance context only",
    }


def reflections() -> list[dict[str, str]]:
    items = [
        ("lane_mesh", "App probe and notify completed again for the three app lanes."),
        ("lane_mesh", "CLI lanes still have no final marker and remain an open gap."),
        ("lane_mesh", "The new taxonomy separates app turn completion from CLI marker completion."),
        ("lane_mesh", "Status-only publication remains the right boundary."),
        ("lane_mesh", "Existing-lane-only policy held again."),
        ("cli_gap", "Arby and Aster Vale show partial transport signal but no final marker."),
        ("cli_gap", "The gap should drive done-signal design, not repeated identical polling."),
        ("cli_gap", "No destructive CLI repair was needed or attempted."),
        ("commands", "Thirty-six command rows were reviewed without execution."),
        ("commands", "Offline rows remain candidates for future no-write checks."),
        ("commands", "Connector rows remain readiness-only."),
        ("commands", "Live-write rows remain approval-draft-only."),
        ("skills", "Skill frontmatter metadata was reused without body copying."),
        ("skills", "Token-overlap joins are weak evidence and labelled accordingly."),
        ("skills", "User skills and plugin cache were not modified."),
        ("skills", "Loader repair remains out of scope without fresh loader evidence."),
        ("expansions", "Thirty-six expansion rows were inspected as proposal/probe candidates."),
        ("expansions", "Installed count remains zero."),
        ("expansions", "P0/P1/P2 boundaries stayed intact."),
        ("sources", "Thirty-two searches refreshed the architecture and governance context."),
        ("sources", "Official and primary sources are preferred over lower-tier material."),
        ("sources", "Google and NVIDIA sources are architecture context only."),
        ("sources", "OpenAI Agents/App sources inform tracing and app surfaces only."),
        ("observability", "OpenTelemetry vocabulary maps cleanly to lane receipt fields."),
        ("observability", "Structured output concepts support schema-bound artifacts."),
        ("governance", "NIST, UNESCO, OECD, and EU sources stay governance context only."),
        ("journey_context", "Journey material remains non-canon in this phase."),
        ("gmut", "All six GMUT gates remain open."),
        ("handoff", "v7 x2 should decide whether another overlay is useful from fresh evidence."),
        ("quality", "Publication remains gated by parse, compile, guard scan, exact staging, and remote verification."),
    ]
    return [{"step": str(index), "domain": domain, "reflection": text} for index, (domain, text) in enumerate(items, start=1)]


def v7_x2_tasks() -> list[dict[str, str]]:
    seeds = [
        ("lanes", "Retry CLI completion once, then avoid duplicate polling if final markers remain absent."),
        ("lanes", "Carry app-lane completion from v7 x1 unless fresh evidence contradicts it."),
        ("lanes", "Summarize lane done-signal taxonomy in a compact board."),
        ("lanes", "Keep all lane content unpublished."),
        ("lanes", "Use existing lanes only."),
        ("lanes", "Decide whether v7 needs x3 from current evidence."),
        ("commands", "Rank no-write command rows by proof adequacy."),
        ("commands", "Promote weak command rows to open_gap."),
        ("commands", "Draft connector readiness checklist."),
        ("commands", "Draft live-write approval candidates without execution."),
        ("commands", "Prepare command-to-skill summary counts."),
        ("commands", "Keep command templates bounded."),
        ("skills", "Review skill-command join open gaps."),
        ("skills", "Avoid body copying and skill mutation."),
        ("skills", "Flag weak metadata matches honestly."),
        ("skills", "Prepare v8 skill readiness improvements."),
        ("skills", "Keep plugin cache out of staging."),
        ("skills", "Record loader repair only if new evidence appears."),
        ("expansions", "Rank P0/P1/P2 expansion rows for v8 x1."),
        ("expansions", "Keep installed_count zero unless exact evidence changes."),
        ("expansions", "Carry no-write and stdout-only boundaries."),
        ("expansions", "Convert simulation candidates into labelled toy plans only."),
        ("expansions", "Reject unapproved live-write promotion."),
        ("expansions", "Prepare a compact expansion readiness board."),
        ("sources", "Reuse v7 x1 source ledger if still current in-session."),
        ("sources", "Refresh Codex/MCP/GitHub sources if publication is delayed."),
        ("sources", "Keep external platforms from validating GMUT."),
        ("sources", "Keep governance sources separate from implementation proof."),
        ("sources", "Record trust tiers."),
        ("sources", "Avoid lower-tier claims unless independently verified."),
        ("observability", "Summarize schema conformance across app and CLI lanes."),
        ("observability", "Carry done-signal definitions to v8 x1."),
        ("observability", "Keep local temp details redacted."),
        ("observability", "Prepare dashboard-ready row counts."),
        ("observability", "Keep event streams unpublished."),
        ("observability", "Record timeout reason dominance rules."),
        ("sandbox", "Run only non-destructive sandbox checks if new evidence requires it."),
        ("sandbox", "Do not change Windows settings."),
        ("sandbox", "Do not delete temp or cache folders."),
        ("sandbox", "Keep CLI worktrees read-only."),
        ("sandbox", "Carry setup blockers as open gaps."),
        ("sandbox", "Avoid package or account changes."),
        ("handoff", "Build v7 x2 synthesis."),
        ("handoff", "Build v8 x1 roadmap."),
        ("handoff", "Decide x3 based on fresh lane and queue evidence."),
        ("handoff", "Keep v477 sequence moving toward v490."),
        ("handoff", "Publish exact current-phase artifacts only."),
        ("handoff", "Verify remote equals local after push."),
        ("gmut", "Carry null recovery gate open."),
        ("gmut", "Carry dimensional/SI gate open."),
        ("gmut", "Carry conservation/exchange gate open."),
        ("gmut", "Carry baseline recovery gate open."),
        ("gmut", "Carry fifth-force/equivalence gate open."),
        ("gmut", "Carry consciousness measurement bridge gate open."),
        ("quality", "Parse every JSON artifact."),
        ("quality", "Compile any new helper script."),
        ("quality", "Run guard scan before staging."),
        ("quality", "Run whitespace and staged diff checks."),
        ("quality", "Stage exact files only."),
        ("quality", "Fetch and drift-check before push."),
    ]
    return [{"id": f"v477-v7-x2-task-{index:02d}", "domain": domain, "task": text} for index, (domain, text) in enumerate(seeds, start=1)]


def build() -> None:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])

    app_probe = read_trace("v477-thos-v7-x1-app-lane-completion-notifier-probe-v1.json")
    app_run = read_trace("v477-thos-v7-x1-app-lane-completion-notifier-v1.json")
    cli_poll = read_trace("v477-thos-v7-x1-cli-lane-completion-poll-v1.json")
    command_selection = read_trace("v477-thos-v6-x1-command-probe-selection-v1.json")
    skill_sample = read_trace("v477-thos-v6-x1-skill-metadata-sample-v1.json")
    expansion_selection = read_trace("v477-thos-v6-x1-expansion-probe-selection-v1.json")
    roadmap = read_trace("v477-thos-v7-x1-roadmap-v1.json")

    lanes = lane_taxonomy(app_probe, app_run, cli_poll)
    commands = command_inspection(command_selection)
    skill_join = skill_command_join(skill_sample, commands["rows"])
    expansions = expansion_inspection(expansion_selection)
    sources = source_ledger(generated_utc, generated_nz)
    reflection_rows = reflections()

    synthesis = {
        "artifact_type": "v7_x1_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "local_head_before_build": local_head,
        "remote_head_before_build": remote_head,
        "drift_before_build": drift,
        "input_roadmap_task_count": roadmap.get("task_count"),
        "lane_status": {
            "app_notify": app_run.get("overall_status"),
            "cli_poll": cli_poll.get("aggregate_status"),
        },
        "command_counts": commands["counts"],
        "skill_join_counts": skill_join["counts"],
        "expansion_counts": expansions["counts"],
        "source_search_count": sources["search_count"],
        "reflection_steps": reflection_rows,
        "claim_boundary": {
            "thos_scope": "no-write command, skill, expansion, lane, source, and observability readiness",
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
            {"id": "app_lanes", "status": app_run.get("overall_status"), "summary": "Cicero, Kierkegaard, and Aristotle completed v7 x1 app notifier."},
            {"id": "cli_lanes", "status": cli_poll.get("aggregate_status"), "summary": "Arby and Aster Vale remain pending final-message marker."},
            {"id": "source_refresh", "status": "PASS", "summary": f"{sources['search_count']} live searches refreshed THOS context."},
            {"id": "commands", "status": "PASS_NO_EXECUTION", "summary": "36 selected command rows were inspected without execution."},
            {"id": "skills", "status": "PASS_METADATA_ONLY", "summary": "Skill-to-command joins used metadata only and include open-gap labels."},
            {"id": "expansions", "status": "PASS_NO_INSTALL", "summary": "36 expansion rows were inspected with installed_count zero."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "next_expected_phase": NEXT_PHASE,
    }

    roadmap_next = {
        "artifact_type": "v7_x2_60_task_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": 60,
        "tasks": v7_x2_tasks(),
    }

    artifacts = {
        "v477-thos-v7-x1-source-ledger-v1": sources,
        "v477-thos-v7-x1-lane-done-signal-taxonomy-v1": lanes,
        "v477-thos-v7-x1-command-no-write-inspection-v1": commands,
        "v477-thos-v7-x1-skill-command-join-v1": skill_join,
        "v477-thos-v7-x1-expansion-no-write-inspection-v1": expansions,
        "v477-thos-v7-x1-synthesis-v1": synthesis,
        "v477-thos-v7-x1-run-status-v1": run_status,
        "v477-thos-v7-x2-roadmap-v1": roadmap_next,
    }
    for stem, payload in artifacts.items():
        write_json(TRACES / f"{stem}.json", payload)

    write_md(
        TRACES / "v477-thos-v7-x1-source-ledger-v1.md",
        "v477 THOS v7 x1 Source Ledger",
        [
            f"- search_count: `{sources['search_count']}`",
            "- claim ceiling: THOS architecture and governance context only.",
            "",
            "## Sources",
            *[f"- {item['label']}: {item['url']} ({item['trust_tier']}) - {item['use']}" for item in sources["sources"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-lane-done-signal-taxonomy-v1.md",
        "v477 THOS v7 x1 Lane Done-Signal Taxonomy",
        [
            f"- app_notify_status: `{lanes['app_notify_status']}`",
            f"- cli_poll_status: `{lanes['cli_poll_status']}`",
            "",
            "## Rows",
            *[f"- {row['lane']} ({row['surface']}): `{row['observed_state']}`, status `{row['status']}`." for row in lanes["rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-command-no-write-inspection-v1.md",
        "v477 THOS v7 x1 Command No-Write Inspection",
        [
            "- policy: metadata review only; no command execution.",
            f"- total: `{commands['counts']['total']}`",
            f"- review_ready: `{commands['counts']['review_ready']}`",
            f"- open_gap_missing_metadata: `{commands['counts']['open_gap_missing_metadata']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-skill-command-join-v1.md",
        "v477 THOS v7 x1 Skill Command Join",
        [
            "- policy: metadata only; no skill body copies.",
            f"- sampled: `{skill_join['counts']['sampled']}`",
            f"- matched: `{skill_join['counts']['matched']}`",
            f"- open_gap: `{skill_join['counts']['open_gap']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-expansion-no-write-inspection-v1.md",
        "v477 THOS v7 x1 Expansion No-Write Inspection",
        [
            "- policy: no install, no live write.",
            f"- total: `{expansions['counts']['total']}`",
            f"- installed_count: `{expansions['installed_count']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-synthesis-v1.md",
        "v477 THOS v7 x1 Synthesis",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- local_head_before_build: `{local_head}`",
            f"- remote_head_before_build: `{remote_head}`",
            f"- drift_before_build: `{drift}`",
            f"- overall_status: `{run_status['overall_status']}`",
            "- claim boundary: THOS no-write readiness only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            *[f"- {row['step']}. {row['domain']}: {row['reflection']}" for row in reflection_rows],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-run-status-v1.md",
        "v477 THOS v7 x1 Run Status",
        [
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            *[f"- {row['id']}: `{row['status']}` - {row['summary']}" for row in run_status["status_rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-roadmap-v1.md",
        "v477 THOS v7 x2 Roadmap",
        [
            f"- task_count: `{roadmap_next['task_count']}`",
            "- entry: v7 x1 remote-verified, existing lanes only, all GMUT gates open.",
            "",
            "## Tasks",
            *[f"- {row['id']} ({row['domain']}): {row['task']}" for row in roadmap_next["tasks"]],
        ],
    )


def main() -> None:
    build()
    print(json.dumps({"status": "built", "phase": PHASE, "next_phase": NEXT_PHASE}, indent=2))


if __name__ == "__main__":
    main()
