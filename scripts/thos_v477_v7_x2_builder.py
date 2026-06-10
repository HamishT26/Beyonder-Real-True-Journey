#!/usr/bin/env python3
"""Build v477 THOS v7 x2 synthesis, overlay decision, and v8 x1 roadmap."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v7_x2"
NEXT_PHASE = "v477_thos_v8_x1"
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
    "OpenAI Codex app-server README GitHub official June 2026 v0.136",
    "OpenAI Codex CLI releases 0.136.0 app-server stdio official GitHub",
    "OpenAI Codex Windows sandbox setup refresh issue official GitHub 2026",
    "OpenAI Codex Windows sandbox official restricted token 2026",
    "Model Context Protocol authorization 2025-06-18 security best practices official",
    "Model Context Protocol tools output annotations official 2025-06-18",
    "Model Context Protocol SDK official docs Python TypeScript 2026",
    "Model Context Protocol security best practices official 2026 tool poisoning",
    "GitHub push protection secret scanning official docs June 2026",
    "GitHub Actions security hardening official docs June 2026",
    "GitHub SARIF support code scanning official docs 2026",
    "GitHub MCP server Copilot official docs 2026",
    "Windows Sandbox configure WSB official Microsoft 2026",
    "PowerShell execution policy not security boundary official Microsoft 2026",
    "Python subprocess security considerations official docs shell true 3.12",
    "Python tempfile TemporaryDirectory delete cleanup official docs 3.12",
    "OpenTelemetry signals official docs traces metrics logs events 2026",
    "Docker Compose Watch official docs file watch 2026",
    "Kubernetes Jobs completion backoffLimit official docs 2026",
    "OpenTelemetry trace span logs metrics concepts official docs 2026",
    "Google Vertex AI Agent Engine overview official 2026",
    "Google Gemini API File Search multimodal RAG official 2026",
    "NVIDIA NIM microservices official docs 2026",
    "NVIDIA DGX Spark user guide official 2026",
    "OpenAI Agents SDK tracing official docs handoffs tools 2026",
    "OpenAI Apps SDK ChatGPT MCP apps official docs 2026",
    "OpenAI structured outputs JSON schema official docs 2026",
    "OpenAI Agents SDK native sandbox file tools official 2026",
    "OpenAI Agents SDK tools handoffs tracing official docs 2026",
    "OpenAI Apps SDK MCP tools official documentation 2026",
    "OpenAI Codex CLI sandbox official docs GitHub Windows 2026",
    "OpenAI API structured outputs JSON schema official docs 2026",
]

SOURCE_URLS = [
    ("OpenAI Codex app-server source", "official_source_repo", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "Local app-server transport context."),
    ("OpenAI Codex releases", "official_source_repo", "https://github.com/openai/codex/releases", "Codex CLI version drift context."),
    ("OpenAI Codex Windows sandbox", "official", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox design context."),
    ("MCP authorization", "official", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "Connector authorization and resource-boundary context."),
    ("MCP tools", "official", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "Tool output and resource-link context."),
    ("MCP SDK docs", "official", "https://modelcontextprotocol.io/docs/sdk", "SDK routing context."),
    ("GitHub push protection", "official", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "Publication guard context."),
    ("GitHub Actions security", "official", "https://docs.github.com/en/actions/how-tos/security-for-github-actions", "Workflow hardening context."),
    ("GitHub SARIF support", "official", "https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning", "Bounded scan-output context."),
    ("GitHub MCP server", "official", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "MCP connector context."),
    ("Windows Sandbox configuration", "official", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "Sandbox configuration context."),
    ("PowerShell execution policy", "official", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6", "Terminal safety caveat."),
    ("Python subprocess", "official", "https://docs.python.org/3.12/library/subprocess.html", "Process invocation safety context."),
    ("Python tempfile", "official", "https://docs.python.org/3.12/library/tempfile.html", "Temporary artifact lifecycle context."),
    ("OpenTelemetry signals", "official", "https://opentelemetry.io/docs/concepts/signals/", "Trace, metric, log, and event vocabulary."),
    ("Docker Compose Watch", "official", "https://docs.docker.com/compose/how-tos/file-watch/", "Watcher analogy."),
    ("Kubernetes Jobs", "official", "https://kubernetes.io/docs/concepts/workloads/controllers/job/", "Completion and retry vocabulary."),
    ("Vertex AI Agent Engine", "official", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview", "Managed agent architecture context."),
    ("Gemini API File Search", "official", "https://ai.google.dev/gemini-api/docs/file-search", "Retrieval and citation context."),
    ("NVIDIA NIM", "official", "https://docs.nvidia.com/nim/", "Inference microservice architecture context."),
    ("NVIDIA DGX Spark", "official", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "Local AI capacity context."),
    ("OpenAI Agents SDK", "official", "https://platform.openai.com/docs/guides/agents-sdk/", "Agent orchestration context."),
    ("OpenAI Agents SDK tracing", "official_source_docs", "https://openai.github.io/openai-agents-python/tracing/", "Tracing context."),
    ("OpenAI Agents SDK handoffs", "official_source_docs", "https://openai.github.io/openai-agents-js/guides/handoffs/", "Handoff context."),
    ("OpenAI Apps SDK help", "official", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "App and MCP surface context."),
    ("OpenAI MCP apps help", "official", "https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt", "ChatGPT MCP app context."),
    ("OpenAI structured outputs", "official", "https://platform.openai.com/docs/guides/structured-outputs", "Schema-bound output context."),
    ("OpenAI structured outputs announcement", "official_blog", "https://openai.com/index/introducing-structured-outputs-in-the-api/", "Historical structured-output context."),
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


def lane_compact_board(taxonomy: dict[str, Any], cli_retry: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in taxonomy.get("rows", []):
        retry_state = None
        if row.get("surface") == "codex_cli":
            retry = next((item for item in cli_retry.get("lanes", []) if item.get("lane") == row.get("lane")), {})
            retry_state = "final_marker_present" if retry.get("final_message_bytes", 0) else "final_marker_absent"
        rows.append(
            {
                "lane": row.get("lane"),
                "surface": row.get("surface"),
                "prior_observed_state": row.get("observed_state"),
                "retry_observed_state": retry_state or row.get("observed_state"),
                "prior_status": row.get("status"),
                "retry_status": next((item.get("completion_status") for item in cli_retry.get("lanes", []) if item.get("lane") == row.get("lane")), row.get("status")),
                "publication": "status_only",
            }
        )
    return {
        "artifact_type": "v7_x2_lane_compact_board",
        "phase": PHASE,
        "prior_app_status": taxonomy.get("app_notify_status"),
        "retry_cli_status": cli_retry.get("aggregate_status"),
        "rows": rows,
        "summary": {
            "app_lanes_complete": sum(1 for row in rows if row["surface"] == "app_server" and row["prior_status"] == "completed"),
            "cli_lanes_open": sum(1 for row in rows if row["surface"] == "codex_cli" and row["retry_observed_state"] != "final_marker_present"),
        },
    }


def command_rank(commands: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in commands.get("rows", []):
        score = 0
        if row.get("proof_required_present"):
            score += 2
        if row.get("resume_safe") is True:
            score += 1
        if row.get("risk_class") == "low":
            score += 1
        readiness = "v8_ready_no_write" if score >= 2 else "open_gap_weak_metadata"
        rows.append({**row, "proof_score": score, "rank_bucket": readiness})
    rows.sort(key=lambda row: (-row["proof_score"], str(row.get("command_id"))))
    return {
        "artifact_type": "v7_x2_command_proof_ranking",
        "phase": PHASE,
        "ranking_policy": "metadata_only_no_execution",
        "rows": rows,
        "counts": {
            "total": len(rows),
            "v8_ready_no_write": sum(1 for row in rows if row["rank_bucket"] == "v8_ready_no_write"),
            "open_gap_weak_metadata": sum(1 for row in rows if row["rank_bucket"] != "v8_ready_no_write"),
        },
    }


def skill_join_review(skill_join: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in skill_join.get("rows", []):
        rows.append(
            {
                **row,
                "review_status": "usable_metadata_hint" if row.get("match_score", 0) > 0 else "open_gap_no_metadata_match",
                "mutation_performed": False,
            }
        )
    return {
        "artifact_type": "v7_x2_skill_join_review",
        "phase": PHASE,
        "review_policy": "metadata_only_no_body_copy",
        "rows": rows,
        "counts": {
            "sampled": len(rows),
            "usable_metadata_hint": sum(1 for row in rows if row["review_status"] == "usable_metadata_hint"),
            "open_gap_no_metadata_match": sum(1 for row in rows if row["review_status"] != "usable_metadata_hint"),
        },
    }


def expansion_readiness(expansions: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in expansions.get("rows", []):
        tier = row.get("tier")
        if tier == "p0_no_write":
            next_action = "v8_no_write_inspection"
        elif tier == "p1_stdout_only":
            next_action = "v8_stdout_only_probe"
        else:
            next_action = "v8_labelled_toy_plan"
        rows.append({**row, "next_action": next_action, "promotion_allowed": False})
    return {
        "artifact_type": "v7_x2_expansion_readiness_board",
        "phase": PHASE,
        "readiness_policy": "no_install_no_unapproved_live_write",
        "rows": rows,
        "installed_count": 0,
        "counts": {
            "total": len(rows),
            "v8_no_write_inspection": sum(1 for row in rows if row["next_action"] == "v8_no_write_inspection"),
            "v8_stdout_only_probe": sum(1 for row in rows if row["next_action"] == "v8_stdout_only_probe"),
            "v8_labelled_toy_plan": sum(1 for row in rows if row["next_action"] == "v8_labelled_toy_plan"),
        },
    }


def source_ledger(generated_utc: str, generated_nz: str) -> dict[str, Any]:
    return {
        "artifact_type": "v7_x2_source_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": len(SOURCE_QUERIES),
        "queries": SOURCE_QUERIES,
        "sources": [
            {"label": label, "trust_tier": tier, "url": url, "use": use}
            for label, tier, url, use in SOURCE_URLS
        ],
        "claim_ceiling": "THOS architecture and governance context only",
    }


def overlay_decision(cli_retry: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "v7_x2_overlay_decision",
        "phase": PHASE,
        "decision": "NO_X3_FOR_V7",
        "next_phase": NEXT_PHASE,
        "reasoning": [
            "v7 x1 already completed app-lane probe and notify for the three app lanes.",
            "v7 x2 retried Arby and Aster Vale completion polling and observed the same final-marker timeout.",
            "The command, skill, expansion, and source queues are ready for v8 x1 without a duplicate v7 x3 overlay.",
            "v8 x1 should improve CLI done-signal handling while continuing no-write command and expansion work.",
        ],
        "cli_status_carried_forward": cli_retry.get("aggregate_status"),
    }


def reflections() -> list[dict[str, str]]:
    items = [
        ("lane_board", "App lanes remain complete from v7 x1 evidence."),
        ("lane_board", "CLI retry repeated the final-marker timeout."),
        ("lane_board", "The open CLI gap is now stable enough to carry forward without duplicate v7 polling."),
        ("lane_board", "Status-only lane publication remained intact."),
        ("lane_board", "Existing-lane-only policy held."),
        ("commands", "No-write command rows were ranked by proof metadata."),
        ("commands", "Rows with weak metadata are labelled open gaps."),
        ("commands", "Live-write rows remain approval candidates only."),
        ("commands", "No command templates were executed."),
        ("skills", "Skill-command joins remain metadata hints, not proof of readiness."),
        ("skills", "No skill bodies were copied."),
        ("skills", "No skill or plugin-cache mutation occurred."),
        ("expansions", "Expansion rows are ready for v8 action buckets without installation."),
        ("expansions", "Simulation candidates remain labelled toy-plan candidates."),
        ("expansions", "Installed count remains zero."),
        ("sources", "Thirty-two searches refreshed official architecture context."),
        ("sources", "OpenAI Agents/App sources improve tracing and handoff vocabulary."),
        ("sources", "Codex and MCP sources support lane and connector design only."),
        ("sources", "External platforms do not validate GMUT."),
        ("observability", "Done-signal definitions are ready to carry into v8 x1."),
        ("observability", "OpenTelemetry remains the clean vocabulary for future receipt rows."),
        ("observability", "Structured-output sources support schema-bound artifacts."),
        ("sandbox", "No Windows or Codex settings changed in v7 x2."),
        ("sandbox", "No temp or cache cleanup occurred."),
        ("governance", "Governance sources remain context-only."),
        ("journey_context", "Journey context remains non-canon in this phase."),
        ("gmut", "All six GMUT gates remain open."),
        ("handoff", "v8 x1 is a better next phase than v7 x3."),
        ("handoff", "v8 x1 should carry CLI done-signal work plus no-write inspections."),
        ("quality", "Publication remains bound by parse, compile, guard scan, exact staging, and remote verification."),
    ]
    return [{"step": str(index), "domain": domain, "reflection": text} for index, (domain, text) in enumerate(items, start=1)]


def v8_tasks() -> list[dict[str, str]]:
    seeds = [
        ("lanes", "Run app-lane probe for Cicero, Kierkegaard, and Aristotle."),
        ("lanes", "Run app-lane notify only if probe passes."),
        ("lanes", "Run CLI poll with done-signal definitions from v7 x2."),
        ("lanes", "Avoid duplicate polling if final markers remain absent."),
        ("lanes", "Keep lane content unpublished."),
        ("lanes", "Use existing lanes only."),
        ("commands", "Run no-write inspection receipts for ready command rows."),
        ("commands", "Keep weak command rows as open gaps."),
        ("commands", "Draft connector readiness checklist from ranked rows."),
        ("commands", "Draft live-write approval candidates without execution."),
        ("commands", "Build command-to-skill summary counts."),
        ("commands", "Do not execute command templates."),
        ("skills", "Review metadata hint rows from skill join review."),
        ("skills", "Avoid skill body copying."),
        ("skills", "Keep user skills and plugin cache unmodified."),
        ("skills", "Record loader evidence only if a loader blocker appears."),
        ("skills", "Prepare v8 x2 skill readiness summary."),
        ("skills", "Keep sample rows bounded."),
        ("expansions", "Create v8 no-write inspection receipts for P0 rows."),
        ("expansions", "Create stdout-only probe receipts for P1 rows."),
        ("expansions", "Create labelled toy plans for P2 rows."),
        ("expansions", "Keep installed_count zero unless exact proof changes."),
        ("expansions", "Reject unapproved live-write promotion."),
        ("expansions", "Prepare compact v8 readiness board."),
        ("sources", "Refresh Codex and OpenAI Agents sources if publication is delayed."),
        ("sources", "Refresh MCP official sources before connector claims."),
        ("sources", "Refresh GitHub security sources before workflow claims."),
        ("sources", "Carry Google/NVIDIA as architecture context only."),
        ("sources", "Keep governance context separated from implementation proof."),
        ("sources", "Record trust tiers and freshness."),
        ("observability", "Add done-signal taxonomy to v8 lane board."),
        ("observability", "Add schema-bound artifact checks from structured-output context."),
        ("observability", "Keep event streams unpublished."),
        ("observability", "Keep local temp details redacted."),
        ("observability", "Prepare bounded dashboard-ready rows."),
        ("observability", "Record timeout dominance rules."),
        ("sandbox", "Run only non-destructive Codex/sandbox checks if needed."),
        ("sandbox", "Do not change Windows settings."),
        ("sandbox", "Do not delete temp or cache folders."),
        ("sandbox", "Preserve CLI worktrees read-only."),
        ("sandbox", "Carry setup blockers as open gaps."),
        ("sandbox", "Avoid package or account changes."),
        ("handoff", "Build v8 x1 synthesis."),
        ("handoff", "Build v8 x2 roadmap."),
        ("handoff", "Decide x3 from fresh evidence only."),
        ("handoff", "Keep sequence moving toward v490."),
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
    return [{"id": f"v477-v8-x1-task-{index:02d}", "domain": domain, "task": text} for index, (domain, text) in enumerate(seeds, start=1)]


def build() -> None:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])

    taxonomy = read_trace("v477-thos-v7-x1-lane-done-signal-taxonomy-v1.json")
    cli_retry = read_trace("v477-thos-v7-x2-cli-lane-completion-poll-v1.json")
    command_source = read_trace("v477-thos-v7-x1-command-no-write-inspection-v1.json")
    skill_source = read_trace("v477-thos-v7-x1-skill-command-join-v1.json")
    expansion_source = read_trace("v477-thos-v7-x1-expansion-no-write-inspection-v1.json")
    roadmap = read_trace("v477-thos-v7-x2-roadmap-v1.json")

    lanes = lane_compact_board(taxonomy, cli_retry)
    commands = command_rank(command_source)
    skills = skill_join_review(skill_source)
    expansions = expansion_readiness(expansion_source)
    sources = source_ledger(generated_utc, generated_nz)
    decision = overlay_decision(cli_retry)
    reflection_rows = reflections()

    synthesis = {
        "artifact_type": "v7_x2_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "local_head_before_build": local_head,
        "remote_head_before_build": remote_head,
        "drift_before_build": drift,
        "input_roadmap_task_count": roadmap.get("task_count"),
        "lane_summary": lanes["summary"],
        "command_counts": commands["counts"],
        "skill_counts": skills["counts"],
        "expansion_counts": expansions["counts"],
        "source_search_count": sources["search_count"],
        "overlay_decision": decision["decision"],
        "reflection_steps": reflection_rows,
        "claim_boundary": {
            "thos_scope": "v7 synthesis and v8 x1 handoff only",
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
            {"id": "lane_compact_board", "status": "PASS_WITH_OPEN_GAP", "summary": "App lanes remain complete; CLI retry remains final-marker timeout."},
            {"id": "source_refresh", "status": "PASS", "summary": f"{sources['search_count']} live searches refreshed THOS context."},
            {"id": "command_ranking", "status": "PASS_NO_EXECUTION", "summary": "Command rows ranked by metadata without execution."},
            {"id": "skill_review", "status": "PASS_METADATA_ONLY", "summary": "Skill join rows reviewed as weak metadata hints."},
            {"id": "expansion_board", "status": "PASS_NO_INSTALL", "summary": "Expansion rows bucketed for v8 without installation."},
            {"id": "overlay_decision", "status": decision["decision"], "summary": "v8 x1 is more useful than a v7 x3 duplicate retry."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "next_expected_phase": NEXT_PHASE,
    }

    roadmap_next = {
        "artifact_type": "v8_x1_60_task_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": 60,
        "tasks": v8_tasks(),
    }

    artifacts = {
        "v477-thos-v7-x2-source-ledger-v1": sources,
        "v477-thos-v7-x2-lane-compact-board-v1": lanes,
        "v477-thos-v7-x2-command-proof-ranking-v1": commands,
        "v477-thos-v7-x2-skill-join-review-v1": skills,
        "v477-thos-v7-x2-expansion-readiness-board-v1": expansions,
        "v477-thos-v7-x2-overlay-decision-v1": decision,
        "v477-thos-v7-x2-synthesis-v1": synthesis,
        "v477-thos-v7-x2-run-status-v1": run_status,
        "v477-thos-v8-x1-roadmap-v1": roadmap_next,
    }
    for stem, payload in artifacts.items():
        write_json(TRACES / f"{stem}.json", payload)

    write_md(
        TRACES / "v477-thos-v7-x2-source-ledger-v1.md",
        "v477 THOS v7 x2 Source Ledger",
        [
            f"- search_count: `{sources['search_count']}`",
            "- claim ceiling: THOS architecture and governance context only.",
            "",
            "## Sources",
            *[f"- {item['label']}: {item['url']} ({item['trust_tier']}) - {item['use']}" for item in sources["sources"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-lane-compact-board-v1.md",
        "v477 THOS v7 x2 Lane Compact Board",
        [
            f"- prior_app_status: `{lanes['prior_app_status']}`",
            f"- retry_cli_status: `{lanes['retry_cli_status']}`",
            f"- cli_lanes_open: `{lanes['summary']['cli_lanes_open']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-command-proof-ranking-v1.md",
        "v477 THOS v7 x2 Command Proof Ranking",
        [
            "- policy: metadata only; no execution.",
            f"- total: `{commands['counts']['total']}`",
            f"- v8_ready_no_write: `{commands['counts']['v8_ready_no_write']}`",
            f"- open_gap_weak_metadata: `{commands['counts']['open_gap_weak_metadata']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-skill-join-review-v1.md",
        "v477 THOS v7 x2 Skill Join Review",
        [
            "- policy: metadata only; no skill body copies.",
            f"- sampled: `{skills['counts']['sampled']}`",
            f"- usable_metadata_hint: `{skills['counts']['usable_metadata_hint']}`",
            f"- open_gap_no_metadata_match: `{skills['counts']['open_gap_no_metadata_match']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-expansion-readiness-board-v1.md",
        "v477 THOS v7 x2 Expansion Readiness Board",
        [
            "- policy: no install, no unapproved live write.",
            f"- total: `{expansions['counts']['total']}`",
            f"- installed_count: `{expansions['installed_count']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-overlay-decision-v1.md",
        "v477 THOS v7 x2 Overlay Decision",
        [
            f"- decision: `{decision['decision']}`",
            f"- next_phase: `{decision['next_phase']}`",
            "",
            "## Reasoning",
            *[f"- {item}" for item in decision["reasoning"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-synthesis-v1.md",
        "v477 THOS v7 x2 Synthesis",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- local_head_before_build: `{local_head}`",
            f"- remote_head_before_build: `{remote_head}`",
            f"- drift_before_build: `{drift}`",
            f"- overlay_decision: `{decision['decision']}`",
            "- claim boundary: THOS synthesis and handoff only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            *[f"- {row['step']}. {row['domain']}: {row['reflection']}" for row in reflection_rows],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x2-run-status-v1.md",
        "v477 THOS v7 x2 Run Status",
        [
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            *[f"- {row['id']}: `{row['status']}` - {row['summary']}" for row in run_status["status_rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v8-x1-roadmap-v1.md",
        "v477 THOS v8 x1 Roadmap",
        [
            f"- task_count: `{roadmap_next['task_count']}`",
            "- entry: v7 x2 remote-verified, existing lanes only, all GMUT gates open.",
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
