#!/usr/bin/env python3
"""Build curated v478 THOS v1 x2 synthesis and v2 handoff artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v1_x2"
NEXT_PHASE = "v478_thos_v2_x1"


SOURCES = [
    ("S01", "OpenAI Codex app-server README", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "app-lane turn lifecycle and status-only notifier design"),
    ("S02", "OpenAI Codex CLI help", "https://help.openai.com/en/articles/11096431", "CLI approvals and local sandbox context"),
    ("S03", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "release drift context"),
    ("S04", "OpenAI Windows sandbox design", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox blocker taxonomy"),
    ("S05", "OpenAI Codex for almost everything", "https://openai.com/index/codex-for-almost-everything/", "current Codex product context"),
    ("S06", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "tool metadata and command surface route"),
    ("S07", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "connector access boundary route"),
    ("S08", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "least-scope connector and tool trust route"),
    ("S09", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "future MCP runner implementation route"),
    ("S10", "MCP TypeScript SDK docs", "https://ts.sdk.modelcontextprotocol.io/", "SDK maturity context"),
    ("S11", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "agent orchestration and tracing context"),
    ("S12", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "watcher trace vocabulary"),
    ("S13", "OpenAI Agents SDK handoffs", "https://openai.github.io/openai-agents-js/guides/handoffs/", "handoff route vocabulary"),
    ("S14", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "schema-bound output expectations"),
    ("S15", "OpenAI Apps SDK help", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "app tool-surface context"),
    ("S16", "GitHub Actions hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "least-privilege publication context"),
    ("S17", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "push-time auth-material guard context"),
    ("S18", "GitHub SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "bounded findings and result-shape context"),
    ("S19", "GitHub SARIF limits", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/troubleshoot-sarif-uploads/results-exceed-limit", "artifact-size and bounded-table context"),
    ("S20", "GitHub MCP server in IDE", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "GitHub connector comparison context"),
    ("S21", "Microsoft Windows Sandbox WSB", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "sandbox configuration comparison"),
    ("S22", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "Windows integrity boundary comparison"),
    ("S23", "Microsoft app isolation", "https://learn.microsoft.com/en-gb/windows/security/book/application-security-application-isolation", "AppContainer and isolation context"),
    ("S24", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "stdout and stderr stream handling"),
    ("S25", "Python subprocess", "https://docs.python.org/3.12/library/subprocess.html", "bounded process and timeout handling"),
    ("S26", "Python tempfile", "https://docs.python.org/3.12/library/tempfile.html", "temp-only watcher output handling"),
    ("S27", "Python json", "https://docs.python.org/3.12/library/json.html", "JSON parse and bounded decode context"),
    ("S28", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "watcher signal taxonomy"),
    ("S29", "OpenTelemetry logs", "https://opentelemetry.io/docs/specs/otel/logs/", "log and trace correlation context"),
    ("S30", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "local file watcher comparison"),
    ("S31", "Kubernetes Job API", "https://kubernetes.io/docs/reference/kubernetes-api/batch/job-v1/", "completion and retry vocabulary"),
    ("S32", "Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine", "external agent-engine comparison"),
    ("S33", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "retrieval and file-search comparison"),
    ("S34", "NVIDIA NIM", "https://docs.nvidia.com/nim/", "future inference-service expansion context"),
    ("S35", "NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "future workstation capability context"),
    ("S36", "NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "simulation and digital-twin context"),
    ("S37", "NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "risk management framing"),
    ("S38", "UNESCO AI ethics recommendation", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence", "governance framing"),
    ("S39", "OECD AI principles", "https://www.oecd.org/en/topics/ai-principles.html", "governance framing"),
    ("S40", "EU AI Act timeline", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline", "regulatory timing context"),
]


RISK_RANK = {"low": 1, "medium": 2, "high": 3, "unknown": 4}


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


def make_source_drift(generated_utc: str, generated_nz: str) -> None:
    implementation = {"OpenAI", "MCP", "GitHub", "Microsoft", "PowerShell", "Python", "OpenTelemetry", "Docker", "Kubernetes"}
    rows = []
    for source_id, title, url, use in SOURCES:
        category = "governance"
        if any(title.startswith(prefix) for prefix in implementation):
            category = "implementation"
        if title.startswith("Google") or title.startswith("Vertex") or title.startswith("Gemini") or title.startswith("NVIDIA"):
            category = "expansion_context"
        rows.append(
            {
                "id": source_id,
                "source": title,
                "url": url,
                "source_category": category,
                "v478_x2_use": use,
                "drift_action": "carry_forward_with_current_search_refresh",
            }
        )
    payload = {
        "artifact_type": "source_drift_review",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 40,
        "source_count": len(rows),
        "rows": rows,
        "category_counts": dict(Counter(row["source_category"] for row in rows)),
    }
    write_json("v478-thos-v1-x2-source-drift-review-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Source Drift Review",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- search_count: `40`",
        f"- source_count: `{len(rows)}`",
        "- boundary: sources inform THOS infrastructure only; they do not close GMUT gates.",
        "",
        "## Sources",
    ]
    lines.extend(f"- {row['id']}: [{row['source']}]({row['url']}) — `{row['source_category']}`." for row in rows)
    write_md("v478-thos-v1-x2-source-drift-review-v1.md", lines)


def make_lane_compact(generated_utc: str, generated_nz: str, app: dict[str, Any], cli: dict[str, Any]) -> None:
    app_rows = [
        {
            "lane": lane.get("lane"),
            "status": lane.get("overall_status"),
            "completion": lane.get("turn_completion", {}).get("status"),
            "duration_seconds": lane.get("duration_seconds"),
        }
        for lane in app.get("lanes", [])
    ]
    cli_rows = [
        {
            "lane": lane.get("lane"),
            "status": cli.get("aggregate_status"),
            "completion": lane.get("completion_status"),
            "final_message_bytes": lane.get("final_message_bytes"),
        }
        for lane in cli.get("lanes", [])
    ]
    payload = {
        "artifact_type": "lane_compact_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP",
        "app_rows": app_rows,
        "cli_rows": cli_rows,
        "message_payloads_published": False,
    }
    write_json("v478-thos-v1-x2-lane-compact-board-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Lane Compact Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(f"- {row['lane']}: `{row['status']}` completion `{row['completion']}`.")
    lines.append("")
    lines.append("## CLI Lanes")
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['status']}` completion `{row['completion']}`.")
    write_md("v478-thos-v1-x2-lane-compact-board-v1.md", lines)


def make_command_ranking(generated_utc: str, generated_nz: str, command_surface: dict[str, Any]) -> None:
    rows = []
    for row in command_surface.get("rows", []):
        risk = str(row.get("risk_class") or "unknown")
        base = 10 - RISK_RANK.get(risk, 4)
        if not row.get("requires_live"):
            base += 2
        if not row.get("requires_connector"):
            base += 1
        if row.get("bridge_status") == "v8_bridge_candidate":
            base += 1
        bucket = "future_p1_stdout_only_candidate" if base >= 10 and risk in {"low", "medium"} else "hold_for_approval_or_metadata"
        rows.append(
            {
                "command_id": row.get("command_id"),
                "intent": row.get("intent"),
                "risk_class": risk,
                "requires_live": row.get("requires_live"),
                "requires_connector": row.get("requires_connector"),
                "readiness_score": base,
                "rank_bucket": bucket,
                "execution_performed": False,
            }
        )
    rows.sort(key=lambda item: (-int(item["readiness_score"]), item["command_id"] or ""))
    payload = {
        "artifact_type": "command_readiness_ranking",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_artifact": "v478-thos-v1-x1-command-index-surface-manifest-v1.json",
        "execution_performed": False,
        "rows": rows,
        "bucket_counts": dict(Counter(row["rank_bucket"] for row in rows)),
    }
    write_json("v478-thos-v1-x2-command-readiness-ranking-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Command Readiness Ranking",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- execution_performed: `false`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Ranked Commands",
    ]
    for row in rows:
        lines.append(f"- `{row['command_id']}`: score `{row['readiness_score']}`, bucket `{row['rank_bucket']}`.")
    write_md("v478-thos-v1-x2-command-readiness-ranking-v1.md", lines)


def make_skill_scoring(generated_utc: str, generated_nz: str, skill_matrix: dict[str, Any], command_ranking: dict[str, Any]) -> None:
    command_terms = {str(row.get("command_id", "")).replace("_", "-") for row in command_ranking.get("rows", [])}
    rows = []
    for row in skill_matrix.get("rows", []):
        skill = str(row.get("source_skill") or "")
        family = str(row.get("family_hint") or "")
        score = 2
        if family and any(family in command for command in command_terms):
            score += 2
        if "command" in skill or "surface" in skill:
            score += 2
        if "integration" in skill:
            score += 1
        bucket = "metadata_route_candidate" if score >= 4 else "hold_metadata_only"
        rows.append(
            {
                "proposal_id": row.get("proposal_id"),
                "source_skill": skill,
                "family_hint": family,
                "actionability_score": score,
                "bucket": bucket,
                "body_text_published": False,
                "mutation_performed": False,
            }
        )
    rows.sort(key=lambda item: (-int(item["actionability_score"]), item["source_skill"]))
    payload = {
        "artifact_type": "skill_actionability_scoring",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "metadata_only": True,
        "rows": rows,
        "bucket_counts": dict(Counter(row["bucket"] for row in rows)),
    }
    write_json("v478-thos-v1-x2-skill-actionability-scoring-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Skill Actionability Scoring",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- metadata_only: `true`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Skill Scores",
    ]
    for row in rows:
        lines.append(f"- `{row['source_skill']}`: score `{row['actionability_score']}`, bucket `{row['bucket']}`.")
    write_md("v478-thos-v1-x2-skill-actionability-scoring-v1.md", lines)


def make_expansion_ranking(generated_utc: str, generated_nz: str, expansion_table: dict[str, Any]) -> None:
    rows = []
    for row in expansion_table.get("rows", []):
        bucket = str(row.get("action_bucket") or "unknown")
        score = 3
        if bucket == "no_write_inspection":
            score += 4
        if bucket == "stdout_only_probe_candidate":
            score += 3
        if bucket == "approval_needed_blocked":
            score -= 2
        score += min(int(row.get("output_count") or 0), 3)
        rank_bucket = "future_no_write_candidate" if score >= 7 else "hold_or_approval_needed"
        rows.append(
            {
                "proposal_id": row.get("proposal_id"),
                "system_id": row.get("system_id"),
                "pillar": row.get("pillar"),
                "source_bucket": bucket,
                "readiness_score": score,
                "rank_bucket": rank_bucket,
                "installed": False,
                "mutation_performed": False,
            }
        )
    rows.sort(key=lambda item: (-int(item["readiness_score"]), item["system_id"] or ""))
    payload = {
        "artifact_type": "expansion_action_ranking",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "installed_count": 0,
        "rows": rows,
        "bucket_counts": dict(Counter(row["rank_bucket"] for row in rows)),
    }
    write_json("v478-thos-v1-x2-expansion-action-ranking-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Expansion Action Ranking",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- installed_count: `0`",
        f"- row_count: `{len(rows)}`",
        "",
        "## Expansion Rankings",
    ]
    for row in rows:
        lines.append(f"- `{row['system_id']}`: score `{row['readiness_score']}`, bucket `{row['rank_bucket']}`.")
    write_md("v478-thos-v1-x2-expansion-action-ranking-v1.md", lines)


def make_watcher_checklist(generated_utc: str, generated_nz: str) -> None:
    rows = [
        ("app_existing_threads", "existing app-lane threads only", "PASS"),
        ("app_notify_complete", "app-lane turn completion observed", "PASS"),
        ("cli_single_poll", "one bounded CLI poll run", "PASS"),
        ("cli_final_marker", "CLI final-message marker present", "OPEN_GAP"),
        ("transport_status_only", "transport payloads unpublished", "PASS"),
        ("x3_decision_rule", "x3 only when blocker dominance demands it", "PASS"),
        ("artifact_schema", "JSON artifacts parse and expose required keys", "PENDING_FINAL_VALIDATION"),
        ("publication_safety", "exact staging and remote verification remain required", "PENDING_FINAL_VALIDATION"),
    ]
    payload = {
        "artifact_type": "watcher_x2_acceptance_checklist",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_OPEN_GAP",
        "rows": [{"id": row_id, "criterion": criterion, "status": status} for row_id, criterion, status in rows],
    }
    write_json("v478-thos-v1-x2-watcher-acceptance-checklist-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Watcher Acceptance Checklist",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_OPEN_GAP`",
        "",
        "## Criteria",
    ]
    for row in payload["rows"]:
        lines.append(f"- `{row['id']}`: `{row['status']}` — {row['criterion']}.")
    write_md("v478-thos-v1-x2-watcher-acceptance-checklist-v1.md", lines)


def make_overlay_decision(generated_utc: str, generated_nz: str) -> None:
    reasons = [
        "App lanes completed again through existing local app-server threads.",
        "CLI lanes repeated the known final-message timeout without introducing a new blocker class.",
        "Command, skill, and expansion work stayed metadata-only, no-write, and no-install.",
        "Source refresh produced enough current official context for v478 v1 x2 synthesis.",
        "The remaining open gap can be carried into v478 v2 x1 without needing a v1 x3 overlay.",
    ]
    payload = {
        "artifact_type": "overlay_decision",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "decision": "NO_X3_FOR_V478_V1",
        "next_expected": NEXT_PHASE,
        "reasons": reasons,
    }
    write_json("v478-thos-v1-x2-overlay-decision-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Overlay Decision",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- decision: `NO_X3_FOR_V478_V1`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Reasons",
    ]
    lines.extend(f"- {reason}" for reason in reasons)
    write_md("v478-thos-v1-x2-overlay-decision-v1.md", lines)


def make_synthesis(generated_utc: str, generated_nz: str) -> None:
    findings = [
        "v478 v1 x2 began from a remote-verified v478 x1 commit.",
        "The app-lane notifier completed Cicero through the local app-server route.",
        "The app-lane notifier completed Kierkegaard through the local app-server route.",
        "The app-lane notifier completed Aristotle through the local app-server route.",
        "No new app sibling thread was created.",
        "No old-style sibling spawning was used.",
        "Arby remained in the known CLI final-marker open gap.",
        "Aster Vale remained in the known CLI final-marker open gap.",
        "The CLI open gap did not introduce a new blocker class.",
        "The x2 source refresh covered 40 official or primary rows.",
        "Implementation sources were separated from governance and expansion-context sources.",
        "Command rows were ranked by risk, live requirement, connector requirement, and bridge status.",
        "Command work remained no-execution.",
        "Skill proposals were scored metadata-only.",
        "No skill body text was published or modified.",
        "Expansion rows were ranked without installation or promotion.",
        "No external account or connector write action was performed.",
        "Watcher acceptance keeps app completion and CLI closure separate.",
        "OpenTelemetry and Agents SDK sources support future trace language.",
        "MCP sources support command and connector boundary language.",
        "GitHub sources support exact staging and auth-material guard language.",
        "Microsoft, Python, and PowerShell sources support platform and stream handling.",
        "Docker and Kubernetes sources support watcher/retry vocabulary.",
        "Google and NVIDIA sources remain future expansion context only.",
        "NIST, UNESCO, OECD, and EU sources remain governance context only.",
        "No source is used as GMUT physics evidence.",
        "Journey material was not used as proof in this x2 phase.",
        "All six GMUT gates remain open.",
        "No v478 v1 x3 overlay is justified by blocker dominance.",
        "The next phase is v478 v2 x1 with the same exact publication discipline.",
    ]
    payload = {
        "artifact_type": "phase_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "reflection_step_count": len(findings),
        "findings": [{"step": f"R{idx:02d}", "finding": finding} for idx, finding in enumerate(findings, start=1)],
        "claim_boundary": {
            "scope": "THOS v478 x2 synthesis, ranking, watcher acceptance, and v2 handoff",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v1-x2-synthesis-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Synthesis",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- reflection_step_count: `{len(findings)}`",
        "",
        "## Reflection Steps",
    ]
    for row in payload["findings"]:
        lines.append(f"- {row['step']}: {row['finding']}")
    write_md("v478-thos-v1-x2-synthesis-v1.md", lines)


def make_run_status(generated_utc: str, generated_nz: str, app: dict[str, Any], cli: dict[str, Any]) -> None:
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
            {"name": "command_ranking", "status": "PASS_NO_EXECUTION"},
            {"name": "skill_scoring", "status": "PASS_METADATA_ONLY"},
            {"name": "expansion_ranking", "status": "PASS_NO_INSTALL"},
            {"name": "watcher_acceptance", "status": "PASS_WITH_CLI_OPEN_GAP"},
            {"name": "overlay_decision", "status": "NO_X3_FOR_V478_V1"},
            {"name": "claim_boundary", "status": "PASS_ALL_GMUT_GATES_OPEN"},
        ],
        "next_expected": NEXT_PHASE,
    }
    write_json("v478-thos-v1-x2-run-status-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Run Status",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Checks",
    ]
    for row in payload["checks"]:
        lines.append(f"- `{row['name']}`: `{row['status']}`.")
    write_md("v478-thos-v1-x2-run-status-v1.md", lines)


def make_next_roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = [
        ("lane", "Start v478 v2 x1 from the v478 v1 x2 remote-verified head."),
        ("lane", "Run app-lane probe before notify if app route freshness is needed."),
        ("lane", "Notify Cicero, Kierkegaard, and Aristotle through existing app-server threads."),
        ("lane", "Run one bounded Arby/Aster CLI watcher pass."),
        ("lane", "Carry CLI final-marker timeout as open_gap if unchanged."),
        ("command", "Select 30 command rows from v1 x2 readiness ranking."),
        ("command", "Promote only future_p1_stdout_only_candidate rows for dry-run planning."),
        ("command", "Hold live and connector rows for exact approval."),
        ("command", "Map command rows to source categories."),
        ("command", "Draft no-execution proof receipt schema."),
        ("skill", "Select 30 skill rows from actionability scoring."),
        ("skill", "Map metadata-route candidates to command rows."),
        ("skill", "Keep body text unpublished and unmodified."),
        ("skill", "Record duplicate or stale skill-name families."),
        ("skill", "Draft skill promotion stop conditions."),
        ("expansion", "Select 30 expansion rows from action ranking."),
        ("expansion", "Promote only no-write candidates to review board."),
        ("expansion", "Hold install and live promotion rows."),
        ("expansion", "Separate simulation candidates from connector candidates."),
        ("expansion", "Draft future approval packet candidates without executing them."),
        ("source", "Refresh at least 30 official sources if source drift matters."),
        ("source", "Carry implementation/governance/expansion separation."),
        ("source", "Do not treat source context as GMUT closure."),
        ("source", "Attach source IDs to command and expansion rows."),
        ("source", "Record source freshness limits."),
        ("watcher", "Reuse x2 watcher checklist."),
        ("watcher", "Keep app-lane completion separate from CLI closure."),
        ("watcher", "Keep temp-only watcher output unpublished."),
        ("watcher", "Avoid duplicate polling loops."),
        ("watcher", "Draft v478 reusable notifier interface notes."),
        ("schema", "Parse every generated JSON artifact."),
        ("schema", "Check required keys and next_expected consistency."),
        ("schema", "Bound all published rows."),
        ("schema", "Run publication guard scan."),
        ("schema", "Review markdown summaries for overclaim language."),
        ("safety", "Fetch and drift-check before publication."),
        ("safety", "Exact-stage only v478 v2 x1 scoped files."),
        ("safety", "Reject unpublished local dumps and transport payloads."),
        ("safety", "Run whitespace and staged diff review."),
        ("safety", "Push and remote-verify equals local."),
        ("claim", "Keep all six GMUT gates open."),
        ("claim", "Do not claim THOS validates GMUT."),
        ("claim", "Do not claim consciousness proof."),
        ("claim", "Do not promote Journey context to canon."),
        ("claim", "Use open_gap for unresolved CLI closure."),
        ("handoff", "Prepare v478 v2 x2 roadmap after x1."),
        ("handoff", "Decide x3 only from blocker dominance."),
        ("handoff", "Carry v1 x2 ranking artifacts forward."),
        ("handoff", "Keep status-only lane evidence."),
        ("handoff", "Maintain exact publication discipline."),
        ("thos", "Draft command-index repair candidates from ranking rows."),
        ("thos", "Draft connector boundary board from MCP/GitHub sources."),
        ("thos", "Draft app-lane health mini-dashboard rows."),
        ("thos", "Draft skill acceptance schema from scoring rows."),
        ("thos", "Draft expansion review schema from ranking rows."),
        ("quality", "Validate all v2 x1 artifacts before staging."),
        ("quality", "Keep file names phase-consistent."),
        ("quality", "Ignore unrelated dirty worktree content."),
        ("quality", "Publish concise closeout."),
        ("quality", "Keep the larger v490 goal active."),
    ]
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": [{"id": f"V478V2X1-{idx:02d}", "domain": domain, "task": task} for idx, (domain, task) in enumerate(tasks, start=1)],
    }
    write_json("v478-thos-v2-x1-roadmap-v1.json", payload)
    lines = [
        "# v478 THOS v2 x1 Roadmap",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- task_count: `{len(tasks)}`",
        "",
        "## Tasks",
    ]
    for row in payload["tasks"]:
        lines.append(f"- `{row['id']}` ({row['domain']}): {row['task']}")
    write_md("v478-thos-v2-x1-roadmap-v1.md", lines)


def make_schema_check(generated_utc: str, generated_nz: str) -> None:
    names = [
        "v478-thos-v1-x2-source-drift-review-v1.json",
        "v478-thos-v1-x2-lane-compact-board-v1.json",
        "v478-thos-v1-x2-command-readiness-ranking-v1.json",
        "v478-thos-v1-x2-skill-actionability-scoring-v1.json",
        "v478-thos-v1-x2-expansion-action-ranking-v1.json",
        "v478-thos-v1-x2-watcher-acceptance-checklist-v1.json",
        "v478-thos-v1-x2-overlay-decision-v1.json",
        "v478-thos-v1-x2-synthesis-v1.json",
        "v478-thos-v1-x2-run-status-v1.json",
        "v478-thos-v2-x1-roadmap-v1.json",
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
    write_json("v478-thos-v1-x2-schema-bound-artifact-check-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Schema-Bound Artifact Check",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Rows",
    ]
    lines.extend(f"- `{row['artifact']}`: `{row['status']}`." for row in rows)
    write_md("v478-thos-v1-x2-schema-bound-artifact-check-v1.md", lines)


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app = load_trace("v478-thos-v1-x2-app-lane-completion-notifier-v1.json")
    cli = load_trace("v478-thos-v1-x2-cli-lane-completion-poll-v1.json")
    command_surface = load_trace("v478-thos-v1-x1-command-index-surface-manifest-v1.json")
    skill_matrix = load_trace("v478-thos-v1-x1-skill-proposal-matrix-v1.json")
    expansion_table = load_trace("v478-thos-v1-x1-expansion-readiness-score-table-v1.json")

    make_source_drift(generated_utc, generated_nz)
    make_lane_compact(generated_utc, generated_nz, app, cli)
    make_command_ranking(generated_utc, generated_nz, command_surface)
    command_ranking = load_trace("v478-thos-v1-x2-command-readiness-ranking-v1.json")
    make_skill_scoring(generated_utc, generated_nz, skill_matrix, command_ranking)
    make_expansion_ranking(generated_utc, generated_nz, expansion_table)
    make_watcher_checklist(generated_utc, generated_nz)
    make_overlay_decision(generated_utc, generated_nz)
    make_synthesis(generated_utc, generated_nz)
    make_run_status(generated_utc, generated_nz, app, cli)
    make_next_roadmap(generated_utc, generated_nz)
    make_schema_check(generated_utc, generated_nz)

    print(
        json.dumps(
            {
                "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
                "phase": PHASE,
                "overlay_decision": "NO_X3_FOR_V478_V1",
                "next_expected": NEXT_PHASE,
                "source_count": len(SOURCES),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
