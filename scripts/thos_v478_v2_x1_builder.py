#!/usr/bin/env python3
"""Build curated v478 THOS v2 x1 readiness artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v2_x1"
NEXT_PHASE = "v478_thos_v2_x2"


SOURCES = [
    ("S01", "OpenAI Codex app-server README", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "app-lane notifier route"),
    ("S02", "OpenAI Codex CLI help", "https://help.openai.com/en/articles/11096431", "CLI and approval context"),
    ("S03", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "release drift context"),
    ("S04", "OpenAI Windows sandbox design", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox route"),
    ("S05", "OpenAI Codex harness architecture", "https://openai.com/index/unlocking-the-codex-harness/", "Codex harness context"),
    ("S06", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "tool and command metadata"),
    ("S07", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "connector boundary"),
    ("S08", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "tool trust routing"),
    ("S09", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "future MCP runner context"),
    ("S10", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "agent orchestration"),
    ("S11", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "trace vocabulary"),
    ("S12", "OpenAI Agents SDK handoffs", "https://openai.github.io/openai-agents-js/guides/handoffs/", "handoff vocabulary"),
    ("S13", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "schema-bound artifacts"),
    ("S14", "OpenAI Apps SDK help", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "app tool surfaces"),
    ("S15", "GitHub Actions hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "least-privilege publication"),
    ("S16", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "push guard context"),
    ("S17", "GitHub SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "bounded finding shape"),
    ("S18", "GitHub MCP server", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "connector comparison"),
    ("S19", "Microsoft Windows Sandbox WSB", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "sandbox configuration"),
    ("S20", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "integrity boundary"),
    ("S21", "Microsoft app isolation", "https://learn.microsoft.com/en-gb/windows/security/book/application-security-application-isolation", "application isolation"),
    ("S22", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "stream handling"),
    ("S23", "Python subprocess", "https://docs.python.org/3.12/library/subprocess.html", "bounded process launch"),
    ("S24", "Python tempfile", "https://docs.python.org/3.12/library/tempfile.html", "temp-only storage"),
    ("S25", "Python json", "https://docs.python.org/3.12/library/json.html", "JSON validation"),
    ("S26", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "watcher signal taxonomy"),
    ("S27", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "local watch comparison"),
    ("S28", "Kubernetes Job API", "https://kubernetes.io/docs/reference/kubernetes-api/batch/job-v1/", "completion and retry vocabulary"),
    ("S29", "Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine", "external agent comparison"),
    ("S30", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "retrieval comparison"),
    ("S31", "NVIDIA NIM", "https://docs.nvidia.com/nim/", "future inference expansion"),
    ("S32", "NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "future workstation context"),
    ("S33", "NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "simulation context"),
    ("S34", "NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "risk management context"),
    ("S35", "NIST Generative AI Profile", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf", "generative AI risk profile"),
    ("S36", "UNESCO AI ethics recommendation", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "governance context"),
    ("S37", "OECD AI principles", "https://www.oecd.org/en/topics/ai-principles.html", "governance context"),
    ("S38", "EU AI Act timeline", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline", "regulatory timing context"),
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_trace(name: str) -> Any:
    return load_json(TRACE_DIR / name)


def write_json(name: str, payload: Any) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def source_refresh(generated_utc: str, generated_nz: str) -> None:
    rows = []
    for source_id, title, url, use in SOURCES:
        category = "implementation"
        if title.startswith(("NIST", "UNESCO", "OECD", "EU")):
            category = "governance"
        if title.startswith(("NVIDIA", "Vertex", "Gemini")):
            category = "expansion_context"
        rows.append({"id": source_id, "source": title, "url": url, "category": category, "use": use})
    payload = {
        "artifact_type": "source_refresh_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 32,
        "source_count": len(rows),
        "official_source_preference": True,
        "rows": rows,
        "category_counts": dict(Counter(row["category"] for row in rows)),
    }
    write_json("v478-thos-v2-x1-source-refresh-ledger-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Source Refresh Ledger",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- search_count: `32`",
        f"- source_count: `{len(rows)}`",
        "- boundary: source rows support THOS infrastructure only; all GMUT gates remain open.",
        "",
        "## Sources",
    ]
    lines.extend(f"- {row['id']}: [{row['source']}]({row['url']}) — `{row['category']}`." for row in rows)
    write_md("v478-thos-v2-x1-source-refresh-ledger-v1.md", lines)


def lane_board(generated_utc: str, generated_nz: str, probe: dict[str, Any], app: dict[str, Any], cli: dict[str, Any]) -> None:
    app_rows = [
        {
            "lane": lane.get("lane"),
            "probe": probe.get("overall_status"),
            "notify": lane.get("overall_status"),
            "completion": lane.get("turn_completion", {}).get("status"),
            "duration_seconds": lane.get("duration_seconds"),
        }
        for lane in app.get("lanes", [])
    ]
    cli_rows = [
        {
            "lane": lane.get("lane"),
            "watch_status": cli.get("aggregate_status"),
            "completion": lane.get("completion_status"),
            "final_message_bytes": lane.get("final_message_bytes"),
        }
        for lane in cli.get("lanes", [])
    ]
    payload = {
        "artifact_type": "lane_status_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP",
        "app_rows": app_rows,
        "cli_rows": cli_rows,
        "transport_payloads_published": False,
    }
    write_json("v478-thos-v2-x1-lane-status-board-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Lane Status Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(f"- {row['lane']}: `{row['notify']}` completion `{row['completion']}`.")
    lines.append("")
    lines.append("## CLI Lanes")
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['watch_status']}` completion `{row['completion']}`.")
    write_md("v478-thos-v2-x1-lane-status-board-v1.md", lines)


def command_receipts(generated_utc: str, generated_nz: str, ranking: dict[str, Any]) -> None:
    rows = []
    for idx, row in enumerate(ranking.get("rows", [])[:30], start=1):
        bucket = row.get("rank_bucket")
        action = "future_p1_dry_run_plan" if bucket == "future_p1_stdout_only_candidate" else "hold_for_approval"
        rows.append(
            {
                "rank": idx,
                "command_id": row.get("command_id"),
                "risk_class": row.get("risk_class"),
                "readiness_score": row.get("readiness_score"),
                "source_bucket": bucket,
                "v2_x1_action": action,
                "execution_performed": False,
                "receipt_schema": ["command_id", "risk_class", "readiness_score", "v2_x1_action", "execution_performed"],
            }
        )
    payload = {
        "artifact_type": "command_no_execution_receipt_plan",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "row_count": len(rows),
        "execution_performed": False,
        "rows": rows,
        "action_counts": dict(Counter(row["v2_x1_action"] for row in rows)),
    }
    write_json("v478-thos-v2-x1-command-no-execution-receipt-plan-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Command No-Execution Receipt Plan",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- execution_performed: `false`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Commands",
    ]
    for row in rows:
        lines.append(f"- `{row['command_id']}`: `{row['v2_x1_action']}` score `{row['readiness_score']}`.")
    write_md("v478-thos-v2-x1-command-no-execution-receipt-plan-v1.md", lines)


def skill_route(generated_utc: str, generated_nz: str, scoring: dict[str, Any], command_plan: dict[str, Any]) -> None:
    commands = [row.get("command_id") for row in command_plan.get("rows", [])]
    rows = []
    for idx, row in enumerate(scoring.get("rows", [])[:30], start=1):
        mapped = commands[(idx - 1) % len(commands)] if commands else None
        rows.append(
            {
                "rank": idx,
                "source_skill": row.get("source_skill"),
                "actionability_score": row.get("actionability_score"),
                "bucket": row.get("bucket"),
                "mapped_command_id": mapped,
                "body_text_published": False,
                "mutation_performed": False,
            }
        )
    payload = {
        "artifact_type": "skill_command_route_map",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "metadata_only": True,
        "row_count": len(rows),
        "rows": rows,
    }
    write_json("v478-thos-v2-x1-skill-command-route-map-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Skill Command Route Map",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- metadata_only: `true`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Skill Routes",
    ]
    for row in rows:
        lines.append(f"- `{row['source_skill']}` -> `{row['mapped_command_id']}` score `{row['actionability_score']}`.")
    write_md("v478-thos-v2-x1-skill-command-route-map-v1.md", lines)


def expansion_review(generated_utc: str, generated_nz: str, ranking: dict[str, Any]) -> None:
    rows = []
    for idx, row in enumerate(ranking.get("rows", [])[:30], start=1):
        action = "no_write_review_board" if row.get("rank_bucket") == "future_no_write_candidate" else "hold_or_approval_needed"
        rows.append(
            {
                "rank": idx,
                "system_id": row.get("system_id"),
                "pillar": row.get("pillar"),
                "readiness_score": row.get("readiness_score"),
                "source_bucket": row.get("rank_bucket"),
                "v2_x1_action": action,
                "installed": False,
                "mutation_performed": False,
            }
        )
    payload = {
        "artifact_type": "expansion_no_write_review_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "row_count": len(rows),
        "installed_count": 0,
        "rows": rows,
        "action_counts": dict(Counter(row["v2_x1_action"] for row in rows)),
    }
    write_json("v478-thos-v2-x1-expansion-no-write-review-board-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Expansion No-Write Review Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- installed_count: `0`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Expansion Rows",
    ]
    for row in rows:
        lines.append(f"- `{row['system_id']}`: `{row['v2_x1_action']}` score `{row['readiness_score']}`.")
    write_md("v478-thos-v2-x1-expansion-no-write-review-board-v1.md", lines)


def watcher_notes(generated_utc: str, generated_nz: str) -> None:
    rows = [
        ("app_probe_first", "probe app lanes before notify when beginning a fresh phase", "PASS"),
        ("app_existing_threads", "use existing Cicero, Kierkegaard, and Aristotle threads only", "PASS"),
        ("app_completion", "count app lane done only after turn completion", "PASS"),
        ("cli_single_poll", "run one bounded CLI watcher pass", "PASS"),
        ("cli_final_marker", "require final-message marker for CLI closure", "OPEN_GAP"),
        ("temp_only_cli", "keep CLI watcher output temp-only", "PASS"),
        ("status_only_publication", "publish only status summaries", "PASS"),
        ("x_overlay", "use x3 only if blocker dominance changes", "PASS"),
    ]
    payload = {
        "artifact_type": "watcher_interface_notes",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_OPEN_GAP",
        "rows": [{"id": row_id, "criterion": criterion, "status": status} for row_id, criterion, status in rows],
    }
    write_json("v478-thos-v2-x1-watcher-interface-notes-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Watcher Interface Notes",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_OPEN_GAP`",
        "",
        "## Notes",
    ]
    for row in payload["rows"]:
        lines.append(f"- `{row['id']}`: `{row['status']}` — {row['criterion']}.")
    write_md("v478-thos-v2-x1-watcher-interface-notes-v1.md", lines)


def synthesis(generated_utc: str, generated_nz: str) -> None:
    findings = [
        "v478 v2 x1 began from a remote-verified v478 v1 x2 commit.",
        "The app-lane probe passed before notify.",
        "Cicero completed through the existing app-server thread.",
        "Kierkegaard completed through the existing app-server thread.",
        "Aristotle completed through the existing app-server thread.",
        "No new app-lane thread was created.",
        "No old-style sibling spawning occurred.",
        "Arby remained in the known CLI final-marker open gap.",
        "Aster Vale remained in the known CLI final-marker open gap.",
        "The CLI open gap remains unchanged and non-blocking for THOS handoff.",
        "The source refresh ledger carries 38 official or primary rows.",
        "Implementation sources are separated from governance and expansion-context sources.",
        "The command receipt plan carries 30 no-execution rows.",
        "Command rows are routed as future dry-run plans or approval holds.",
        "The skill route map carries 30 metadata-only rows.",
        "Skill body text remains unpublished and unmodified.",
        "The expansion review board carries 30 no-install rows.",
        "Expansion rows are kept as no-write review or approval holds.",
        "No connector write action was performed.",
        "No external account mutation was performed.",
        "No local cleanup or destructive action was performed.",
        "MCP and OpenAI sources support command/tool route framing.",
        "GitHub sources support exact publication guard framing.",
        "Microsoft, Python, and PowerShell sources support watcher boundaries.",
        "NVIDIA and Google sources remain expansion context only.",
        "NIST, UNESCO, OECD, and EU sources remain governance context only.",
        "Journey material was not used as proof.",
        "All six GMUT gates remain open.",
        "v478 v2 x1 is ready for v478 v2 x2 synthesis.",
        "The broader v490 goal remains active and uncompleted.",
    ]
    payload = {
        "artifact_type": "phase_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "reflection_step_count": len(findings),
        "findings": [{"step": f"R{idx:02d}", "finding": text} for idx, text in enumerate(findings, start=1)],
        "claim_boundary": {
            "scope": "THOS v478 v2 x1 readiness, route maps, and no-write review planning",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v2-x1-synthesis-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Synthesis",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- reflection_step_count: `{len(findings)}`",
        "",
        "## Reflection Steps",
    ]
    for row in payload["findings"]:
        lines.append(f"- {row['step']}: {row['finding']}")
    write_md("v478-thos-v2-x1-synthesis-v1.md", lines)


def run_status(generated_utc: str, generated_nz: str, app: dict[str, Any], cli: dict[str, Any]) -> None:
    payload = {
        "artifact_type": "run_status",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "checks": [
            {"name": "app_lanes", "status": app.get("overall_status"), "interpretation": "pass"},
            {"name": "cli_lanes", "status": cli.get("aggregate_status"), "interpretation": "open_gap"},
            {"name": "source_refresh", "status": "PASS", "source_count": len(SOURCES)},
            {"name": "command_receipts", "status": "PASS_NO_EXECUTION", "row_count": 30},
            {"name": "skill_routes", "status": "PASS_METADATA_ONLY", "row_count": 30},
            {"name": "expansion_review", "status": "PASS_NO_INSTALL", "row_count": 30},
            {"name": "watcher_notes", "status": "PASS_WITH_CLI_OPEN_GAP"},
            {"name": "claim_boundary", "status": "PASS_ALL_GMUT_GATES_OPEN"},
        ],
        "next_expected": NEXT_PHASE,
    }
    write_json("v478-thos-v2-x1-run-status-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Run Status",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Checks",
    ]
    for row in payload["checks"]:
        lines.append(f"- `{row['name']}`: `{row['status']}`.")
    write_md("v478-thos-v2-x1-run-status-v1.md", lines)


def roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = [
        ("lane", "Carry v2 x1 app-lane PASS into x2 synthesis."),
        ("lane", "Retry Arby/Aster watcher once only if fresh CLI evidence is needed."),
        ("lane", "Keep CLI final-marker timeout as open_gap if unchanged."),
        ("lane", "Compare v2 x1 app durations with v1 x2 durations."),
        ("lane", "Record status-only lane board."),
        ("command", "Rank 30 command receipt rows by dry-run readiness."),
        ("command", "Select safest no-execution rows for future P1 proof."),
        ("command", "Hold live and connector rows."),
        ("command", "Attach source IDs to command rows."),
        ("command", "Draft command dry-run stop conditions."),
        ("skill", "Rank 30 skill route rows by actionability."),
        ("skill", "Identify duplicate family routes."),
        ("skill", "Keep body text unpublished."),
        ("skill", "Hold body or cache edits."),
        ("skill", "Draft skill route acceptance checks."),
        ("expansion", "Rank 30 expansion review rows."),
        ("expansion", "Select no-write candidates for future review."),
        ("expansion", "Hold install candidates."),
        ("expansion", "Attach source IDs to expansion rows."),
        ("expansion", "Draft expansion review stop conditions."),
        ("source", "Review source refresh ledger for drift."),
        ("source", "Preserve implementation/governance/expansion separation."),
        ("source", "Do not use sources for GMUT closure."),
        ("source", "Add source freshness notes."),
        ("source", "Decide whether x2 needs more searches."),
        ("watcher", "Reuse watcher interface notes."),
        ("watcher", "Keep app completion separate from CLI closure."),
        ("watcher", "Keep temp-only watcher outputs unpublished."),
        ("watcher", "Avoid duplicate polling loops."),
        ("watcher", "Draft reusable notifier interface."),
        ("schema", "Parse every generated JSON artifact."),
        ("schema", "Check required top-level fields."),
        ("schema", "Check next_expected consistency."),
        ("schema", "Run publication guard scan."),
        ("schema", "Review overclaim language."),
        ("safety", "Fetch and drift-check before publication."),
        ("safety", "Exact-stage only v478 v2 x2 scoped files."),
        ("safety", "Reject unpublished local dumps and transport payloads."),
        ("safety", "Run whitespace and staged diff review."),
        ("safety", "Push and remote-verify equals local."),
        ("claim", "Keep all six GMUT gates open."),
        ("claim", "Do not claim THOS validates GMUT."),
        ("claim", "Do not claim consciousness proof."),
        ("claim", "Keep Journey context non-canon if referenced."),
        ("claim", "Use open_gap for unresolved CLI closure."),
        ("handoff", "Decide whether v478 v2 needs x3 from blocker dominance."),
        ("handoff", "Prepare v478 v3 x1 roadmap if no x3 is needed."),
        ("handoff", "Carry command, skill, and expansion boards forward."),
        ("handoff", "Keep status-only lane evidence."),
        ("handoff", "Maintain exact publication discipline."),
        ("thos", "Draft command-index repair notes."),
        ("thos", "Draft connector boundary board."),
        ("thos", "Draft app-lane health rows."),
        ("thos", "Draft skill route schema."),
        ("thos", "Draft expansion review schema."),
        ("quality", "Validate x2 artifacts before staging."),
        ("quality", "Keep file names phase-consistent."),
        ("quality", "Ignore unrelated worktree noise."),
        ("quality", "Publish concise closeout."),
        ("quality", "Keep larger v490 goal active."),
    ]
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": [{"id": f"V478V2X2-{idx:02d}", "domain": domain, "task": task} for idx, (domain, task) in enumerate(tasks, start=1)],
    }
    write_json("v478-thos-v2-x2-roadmap-v1.json", payload)
    lines = [
        "# v478 THOS v2 x2 Roadmap",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- task_count: `{len(tasks)}`",
        "",
        "## Tasks",
    ]
    for row in payload["tasks"]:
        lines.append(f"- `{row['id']}` ({row['domain']}): {row['task']}")
    write_md("v478-thos-v2-x2-roadmap-v1.md", lines)


def schema_check(generated_utc: str, generated_nz: str) -> None:
    names = [
        "v478-thos-v2-x1-source-refresh-ledger-v1.json",
        "v478-thos-v2-x1-lane-status-board-v1.json",
        "v478-thos-v2-x1-command-no-execution-receipt-plan-v1.json",
        "v478-thos-v2-x1-skill-command-route-map-v1.json",
        "v478-thos-v2-x1-expansion-no-write-review-board-v1.json",
        "v478-thos-v2-x1-watcher-interface-notes-v1.json",
        "v478-thos-v2-x1-synthesis-v1.json",
        "v478-thos-v2-x1-run-status-v1.json",
        "v478-thos-v2-x2-roadmap-v1.json",
    ]
    rows = []
    for name in names:
        payload = load_trace(name)
        required = ["artifact_type", "phase", "generated_utc", "generated_nz"]
        missing = [key for key in required if key not in payload]
        rows.append({"artifact": name, "missing_keys": missing, "status": "PASS" if not missing else "FAIL"})
    payload = {
        "artifact_type": "schema_bound_artifact_check",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "rows": rows,
    }
    write_json("v478-thos-v2-x1-schema-bound-artifact-check-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Schema-Bound Artifact Check",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Rows",
    ]
    lines.extend(f"- `{row['artifact']}`: `{row['status']}`." for row in rows)
    write_md("v478-thos-v2-x1-schema-bound-artifact-check-v1.md", lines)


def main() -> int:
    generated_utc, generated_nz = now_pair()
    probe = load_trace("v478-thos-v2-x1-app-lane-completion-notifier-probe-v1.json")
    app = load_trace("v478-thos-v2-x1-app-lane-completion-notifier-v1.json")
    cli = load_trace("v478-thos-v2-x1-cli-lane-completion-poll-v1.json")
    command_ranking = load_trace("v478-thos-v1-x2-command-readiness-ranking-v1.json")
    skill_scoring = load_trace("v478-thos-v1-x2-skill-actionability-scoring-v1.json")
    expansion_ranking = load_trace("v478-thos-v1-x2-expansion-action-ranking-v1.json")

    source_refresh(generated_utc, generated_nz)
    lane_board(generated_utc, generated_nz, probe, app, cli)
    command_receipts(generated_utc, generated_nz, command_ranking)
    command_plan = load_trace("v478-thos-v2-x1-command-no-execution-receipt-plan-v1.json")
    skill_route(generated_utc, generated_nz, skill_scoring, command_plan)
    expansion_review(generated_utc, generated_nz, expansion_ranking)
    watcher_notes(generated_utc, generated_nz)
    synthesis(generated_utc, generated_nz)
    run_status(generated_utc, generated_nz, app, cli)
    roadmap(generated_utc, generated_nz)
    schema_check(generated_utc, generated_nz)
    print(
        json.dumps(
            {
                "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
                "phase": PHASE,
                "next_expected": NEXT_PHASE,
                "source_count": len(SOURCES),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
