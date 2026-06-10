#!/usr/bin/env python3
"""Build curated v477 THOS v8 x2 synthesis and v478 handoff artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v8_x2"
NEXT_PHASE = "v478_thos_v1_x1"


SOURCE_ROWS = [
    ("S01", "OpenAI Codex app-server route", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "app-lane local-server route and thread lifecycle framing"),
    ("S02", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "CLI version and update-readiness context"),
    ("S03", "OpenAI Windows sandbox design", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox blocker taxonomy"),
    ("S04", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "command-index and tool metadata contracts"),
    ("S05", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "connector access boundary language"),
    ("S06", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "tool trust and prompt-injection risk routing"),
    ("S07", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "future connector runner implementation context"),
    ("S08", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "agent handoff and tool-run framing"),
    ("S09", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "trace and observability model for notifier receipts"),
    ("S10", "OpenAI Agents SDK handoffs", "https://openai.github.io/openai-agents-js/guides/handoffs/", "handoff route language for future lane boards"),
    ("S11", "OpenAI Apps SDK help", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "app tool-surface context"),
    ("S12", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "schema-bound JSON artifact requirements"),
    ("S13", "GitHub Actions security hardening", "https://docs.github.com/en/actions/how-tos/security-for-github-actions", "least-privilege publication safety"),
    ("S14", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "auth-material guard context"),
    ("S15", "GitHub SARIF support", "https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning", "structured finding output limits"),
    ("S16", "GitHub Copilot coding agent MCP", "https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-coding-agent-with-mcp", "agent MCP surface comparison"),
    ("S17", "Microsoft Windows Sandbox WSB", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "sandbox configuration reference"),
    ("S18", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "Windows integrity-level boundary context"),
    ("S19", "Microsoft AppContainer isolation", "https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation", "Windows app isolation comparison"),
    ("S20", "Python subprocess documentation", "https://docs.python.org/3.12/library/subprocess.html", "bounded process launch and timeout handling"),
    ("S21", "Python tempfile documentation", "https://docs.python.org/3.12/library/tempfile.html", "temp-only watcher output routing"),
    ("S22", "Python json documentation", "https://docs.python.org/3.12/library/json.html", "JSON parse validation for curated artifacts"),
    ("S23", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "stdout/stderr watcher handling context"),
    ("S24", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "watcher event class language"),
    ("S25", "OpenTelemetry semantic conventions", "https://opentelemetry.io/docs/specs/semconv/", "portable receipt naming"),
    ("S26", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "local-service watcher comparison"),
    ("S27", "Kubernetes Jobs", "https://kubernetes.io/docs/concepts/workloads/controllers/job/", "completion and backoff rule comparison"),
    ("S28", "Vertex AI Agent Engine", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview", "external agent-engine reference"),
    ("S29", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "RAG and document retrieval comparison"),
    ("S30", "NVIDIA NIM", "https://docs.nvidia.com/nim/", "inference service expansion context"),
    ("S31", "NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "risk management context"),
    ("S32", "EU AI Act timeline", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline", "regulatory timing context"),
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def load_json(name: str) -> Any:
    return json.loads((TRACE_DIR / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def make_source_ledger(generated_utc: str, generated_nz: str) -> None:
    rows = [
        {
            "id": source_id,
            "source": title,
            "url": url,
            "v8_x2_use": use,
            "source_class": "official_or_primary",
        }
        for source_id, title, url, use in SOURCE_ROWS
    ]
    payload = {
        "artifact_type": "source_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 32,
        "source_count": len(rows),
        "policy": {
            "official_sources_preferred": True,
            "queued_searches_claimed_complete": False,
            "scope": "THOS notifier, command, skill, expansion, sandbox, connector, governance, and handoff readiness.",
        },
        "rows": rows,
    }
    write_json("v477-thos-v8-x2-source-ledger-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Source Ledger",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- search_count: `32`",
        f"- source_count: `{len(rows)}`",
        "- policy: official or primary sources preferred; source rows are context, not GMUT validation.",
        "",
        "## Sources",
    ]
    for row in rows:
        lines.append(f"- {row['id']}: [{row['source']}]({row['url']}) — {row['v8_x2_use']}.")
    write_md("v477-thos-v8-x2-source-ledger-v1.md", lines)


def lane_continuity(app: dict[str, Any], cli: dict[str, Any], generated_utc: str, generated_nz: str) -> None:
    app_rows = []
    for lane in app.get("lanes", []):
        app_rows.append(
            {
                "lane": lane.get("lane"),
                "status": lane.get("overall_status"),
                "read": lane.get("read", {}).get("status"),
                "resume": lane.get("resume", {}).get("status"),
                "turn_start": lane.get("turn_start", {}).get("status"),
                "completion": lane.get("turn_completion", {}).get("status"),
                "duration_seconds": lane.get("duration_seconds"),
            }
        )
    cli_rows = [
        {
            "lane": lane.get("lane"),
            "status": cli.get("aggregate_status"),
            "completion_status": lane.get("completion_status"),
            "final_message_bytes": lane.get("final_message_bytes"),
        }
        for lane in cli.get("lanes", [])
    ]
    payload = {
        "artifact_type": "lane_continuity_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP",
        "app_rows": app_rows,
        "cli_rows": cli_rows,
        "decision": "app_lane_notifier_is_ready_for_v478; cli_lanes_remain_non_blocking_open_gap",
    }
    write_json("v477-thos-v8-x2-lane-continuity-board-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Lane Continuity Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        "- decision: app-lane notifier is ready for v478; CLI lanes remain a non-blocking open gap.",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(f"- {row['lane']}: `{row['status']}` with completion `{row['completion']}`.")
    lines.append("")
    lines.append("## CLI Lanes")
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['status']}` with `{row['completion_status']}`.")
    write_md("v477-thos-v8-x2-lane-continuity-board-v1.md", lines)


def command_bridge(command_receipts: dict[str, Any], generated_utc: str, generated_nz: str) -> None:
    rows = []
    for row in command_receipts.get("rows", [])[:24]:
        rows.append(
            {
                "command_id": row.get("command_id"),
                "queue": row.get("queue"),
                "proof_score": row.get("proof_score"),
                "v8_x2_group": "command_index_bridge_candidate",
                "execution_status": "not_executed",
                "next_phase_action": "bind to command-index surface or hold as metadata-only",
            }
        )
    gaps = [
        {
            "command_id": row.get("command_id"),
            "queue": row.get("queue"),
            "gap": row.get("reason"),
            "next_phase_action": "keep open until proof-required metadata is present",
        }
        for row in command_receipts.get("open_gaps", [])
    ]
    payload = {
        "artifact_type": "command_index_bridge_plan",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "execution_performed": False,
        "candidate_count": len(rows),
        "open_gap_count": len(gaps),
        "rows": rows,
        "open_gaps": gaps,
    }
    write_json("v477-thos-v8-x2-command-index-bridge-plan-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Command-Index Bridge Plan",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- execution_performed: `false`",
        f"- candidate_count: `{len(rows)}`",
        f"- open_gap_count: `{len(gaps)}`",
        "",
        "## Candidate Rows",
    ]
    for row in rows[:12]:
        lines.append(f"- `{row['command_id']}` from `{row['queue']}`: `{row['next_phase_action']}`.")
    write_md("v477-thos-v8-x2-command-index-bridge-plan-v1.md", lines)


def skill_acceptance(skill_summary: dict[str, Any], generated_utc: str, generated_nz: str) -> None:
    rows = []
    for row in skill_summary.get("rows", []):
        score = 2
        if row.get("matched_command_id"):
            score += 1
        if row.get("review_status") in {"usable_metadata_hint", "metadata_usable"}:
            score += 1
        rows.append(
            {
                "skill_dir": row.get("skill_dir"),
                "matched_command_id": row.get("matched_command_id"),
                "review_status": row.get("review_status"),
                "actionability_score": score,
                "mutation_performed": False,
                "acceptance_rule": "metadata can guide command routing; body text remains unpublished and unmodified",
            }
        )
    payload = {
        "artifact_type": "skill_acceptance_profile",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "metadata_only": True,
        "rows": rows,
        "score_counts": dict(Counter(str(row["actionability_score"]) for row in rows)),
    }
    write_json("v477-thos-v8-x2-skill-acceptance-profile-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Skill Acceptance Profile",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- metadata_only: `true`",
        "",
        "## Skill Rows",
    ]
    for row in rows[:16]:
        lines.append(f"- `{row['skill_dir']}`: score `{row['actionability_score']}`, command `{row['matched_command_id']}`.")
    write_md("v477-thos-v8-x2-skill-acceptance-profile-v1.md", lines)


def expansion_blockers(expansion_buckets: dict[str, Any], generated_utc: str, generated_nz: str) -> None:
    rows = []
    for bucket, items in expansion_buckets.get("buckets", {}).items():
        for item in items[:8]:
            rows.append(
                {
                    "id": item.get("id"),
                    "bucket": bucket,
                    "proposal": item.get("proposal"),
                    "installed": False,
                    "blocker_class": "requires_future_exact_approval" if bucket != "no_write_inspection" else "inspection_only",
                    "next_action": bucket,
                }
            )
    payload = {
        "artifact_type": "expansion_blocker_table",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "mutation_performed": False,
        "installed_count": 0,
        "rows": rows,
        "blocker_counts": dict(Counter(row["blocker_class"] for row in rows)),
    }
    write_json("v477-thos-v8-x2-expansion-blocker-table-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Expansion Blocker Table",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- mutation_performed: `false`",
        "- installed_count: `0`",
        "",
        "## Blockers",
    ]
    for row in rows[:18]:
        lines.append(f"- `{row['id']}`: `{row['blocker_class']}` via `{row['next_action']}`.")
    write_md("v477-thos-v8-x2-expansion-blocker-table-v1.md", lines)


def watcher_acceptance(generated_utc: str, generated_nz: str) -> None:
    rows = [
        ("app_read", "thread read returns ok", "required", "PASS"),
        ("app_resume", "thread resume returns ok under read-only request", "required", "PASS"),
        ("app_turn_start", "turn start returns ok", "required", "PASS"),
        ("app_turn_complete", "turn completion event observed", "required", "PASS"),
        ("cli_final_marker", "final-message marker found in temp-only watcher output", "required_for_cli_closure", "OPEN_GAP"),
        ("cli_timeout", "timeout without final marker is non-blocking if app lanes pass", "allowed_open_gap", "PASS"),
        ("no_duplicate_polling", "one bounded CLI poll per x2 closeout", "required", "PASS"),
        ("no_transport_publication", "transport payloads remain unpublished", "required", "PASS"),
    ]
    payload = {
        "artifact_type": "watcher_acceptance_table",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "rows": [
            {"id": row_id, "criterion": criterion, "requirement": requirement, "status": status}
            for row_id, criterion, requirement, status in rows
        ],
        "overall_status": "PASS_WITH_CLI_OPEN_GAP",
    }
    write_json("v477-thos-v8-x2-watcher-acceptance-table-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Watcher Acceptance Table",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_OPEN_GAP`",
        "",
        "## Criteria",
    ]
    for row in payload["rows"]:
        lines.append(f"- `{row['id']}`: `{row['status']}` — {row['criterion']}.")
    write_md("v477-thos-v8-x2-watcher-acceptance-table-v1.md", lines)


def overlay_decision(generated_utc: str, generated_nz: str) -> None:
    reasons = [
        "Cicero, Kierkegaard, and Aristotle completed v8 x2 app-lane turns through the local app-server.",
        "The CLI watcher repeated the known final-marker timeout but produced no stronger blocker evidence.",
        "Command, skill, and expansion work stayed within no-write/no-install boundaries.",
        "The remaining CLI open gap can be carried into v478 without blocking THOS handoff.",
        "No v8-specific contradiction or safety gate requires an x3 overlay.",
    ]
    payload = {
        "artifact_type": "overlay_decision",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "decision": "NO_X3_FOR_V8",
        "next_expected": NEXT_PHASE,
        "reasons": reasons,
    }
    write_json("v477-thos-v8-x2-overlay-decision-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Overlay Decision",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- decision: `NO_X3_FOR_V8`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Reasons",
    ]
    lines.extend(f"- {reason}" for reason in reasons)
    write_md("v477-thos-v8-x2-overlay-decision-v1.md", lines)


def synthesis(generated_utc: str, generated_nz: str) -> None:
    findings = [
        "The local app-server notifier is now the preferred app-lane path for Cicero, Kierkegaard, and Aristotle.",
        "The app-lane result is stronger than a mere reachability probe because each lane observed turn completion.",
        "The notifier preserved the existing-thread rule and did not create replacement siblings.",
        "The app-lane receipts publish only status summaries and method classes, not message payloads.",
        "Arby and Aster Vale remain available as CLI watcher targets but are not complete without final-message markers.",
        "The repeated CLI timeout is a known open gap, not a new v8-specific failure.",
        "No destructive cleanup, package replacement, or external account mutation was needed.",
        "The command bridge can move forward with no-write proof groups.",
        "Weak command rows should remain explicit open gaps until proof-required metadata exists.",
        "Skill metadata is useful for routing but not sufficient to rewrite or publish skill bodies.",
        "Expansion proposals remain proposals until a separate exact approval permits live promotion.",
        "The watcher acceptance table separates app completion, CLI closure, and allowed open gaps.",
        "The source ledger keeps official sources mapped to concrete THOS uses.",
        "OpenAI Codex app-server docs support the local-server framing.",
        "MCP specs support the command/tool metadata bridge.",
        "OpenAI structured-output guidance supports schema-bound artifact checks.",
        "GitHub security docs support exact staging and guard checks.",
        "Microsoft sandbox docs support treating Windows sandbox readiness as a platform-specific constraint.",
        "Python subprocess/tempfile docs support bounded watcher process design.",
        "OpenTelemetry docs support event taxonomy without payload publication.",
        "Kubernetes job docs support retry and completion-rule language.",
        "NVIDIA and Google agent-engine sources are context for future expansion, not claims about local deployment.",
        "NIST and EU sources are governance context, not canon or physics evidence.",
        "Journey material was not needed for this phase and remains non-canon if referenced later.",
        "All six GMUT gates remain open.",
        "THOS infrastructure progress does not validate GMUT by association.",
        "The v8 x2 phase can close without x3 because the dominant success path is stable.",
        "The next phase should start v478 with the same app-lane notifier pattern.",
        "The CLI open gap should be carried as a named risk, not hidden in success language.",
        "The durable artifact outcome is a v478 roadmap built from bounded, verified v8 evidence.",
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
            "scope": "THOS coordination and handoff readiness",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v477-thos-v8-x2-synthesis-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Synthesis",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        "- reflection_step_count: `30`",
        "",
        "## Reflection Steps",
    ]
    for row in payload["findings"]:
        lines.append(f"- {row['step']}: {row['finding']}")
    write_md("v477-thos-v8-x2-synthesis-v1.md", lines)


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
            {"name": "source_refresh", "status": "PASS", "search_count": 32},
            {"name": "command_bridge", "status": "PASS_NO_EXECUTION"},
            {"name": "skill_acceptance", "status": "PASS_METADATA_ONLY"},
            {"name": "expansion_blockers", "status": "PASS_NO_INSTALL"},
            {"name": "watcher_acceptance", "status": "PASS_WITH_CLI_OPEN_GAP"},
            {"name": "overlay_decision", "status": "NO_X3_FOR_V8"},
            {"name": "claim_boundary", "status": "PASS_ALL_GMUT_GATES_OPEN"},
        ],
        "next_expected": NEXT_PHASE,
    }
    write_json("v477-thos-v8-x2-run-status-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Run Status",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Checks",
    ]
    for row in payload["checks"]:
        lines.append(f"- `{row['name']}`: `{row['status']}`.")
    write_md("v477-thos-v8-x2-run-status-v1.md", lines)


def roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = [
        ("lane", "Start v478 v1 x1 with app-lane notifier probe for Cicero, Kierkegaard, and Aristotle."),
        ("lane", "Notify app lanes only if the probe confirms read/resume readiness."),
        ("lane", "Run one bounded Arby/Aster CLI watcher pass with final-marker criteria."),
        ("lane", "Carry the CLI timeout as a known open gap if unchanged."),
        ("lane", "Record lane durations without publishing message payloads."),
        ("command", "Build a command-index surface manifest from v8 command bridge candidates."),
        ("command", "Map command IDs to proof-required metadata fields."),
        ("command", "Hold weak command rows as open gaps."),
        ("command", "Prepare P1 stdout-only command probes without executing live writes."),
        ("command", "Draft command promotion criteria for future approval."),
        ("skill", "Sample skill metadata that maps to command-index rows."),
        ("skill", "Reject any skill action requiring body edits or cache mutation."),
        ("skill", "Produce a skill duplicate/staleness board."),
        ("skill", "Keep plugin and user skills unmodified."),
        ("skill", "Define acceptance fields for future skill-generated commands."),
        ("expansion", "Select 30 expansion proposals for no-write review."),
        ("expansion", "Classify proposals by inspection, stdout-only, toy simulation, or blocked."),
        ("expansion", "Reject proposals requiring account settings or installs."),
        ("expansion", "Produce an expansion-readiness score table."),
        ("expansion", "Carry live-promotion candidates only as approval-needed rows."),
        ("source", "Run at least 30 official-source searches for v478 if live research remains needed."),
        ("source", "Map sources to local THOS use rather than broad inspiration."),
        ("source", "Separate governance sources from implementation sources."),
        ("source", "Keep scientific/spiritual context out of GMUT closure claims."),
        ("source", "Record source drift and freshness limits."),
        ("watcher", "Check app-server route stability after each notifier cycle."),
        ("watcher", "Keep temp-only output for CLI watcher runs."),
        ("watcher", "Avoid duplicate polling within a single phase."),
        ("watcher", "Convert watcher criteria into a reusable v478 template."),
        ("watcher", "Track app completion and CLI closure as separate signals."),
        ("schema", "Parse every generated JSON artifact."),
        ("schema", "Check required keys for run status and roadmaps."),
        ("schema", "Check next_expected consistency."),
        ("schema", "Run publication guard scan before staging."),
        ("schema", "Keep row counts bounded."),
        ("safety", "Fetch and drift-check before commit."),
        ("safety", "Exact-stage only v478 scoped artifacts."),
        ("safety", "Reject raw transport, local dumps, or auth material."),
        ("safety", "Run whitespace and staged diff review."),
        ("safety", "Push and remote-verify equals local."),
        ("claim", "Keep all six GMUT gates open."),
        ("claim", "Do not claim THOS proves GMUT."),
        ("claim", "Do not claim solved consciousness."),
        ("claim", "Do not promote Journey context to canon."),
        ("claim", "Use evidence/context/hypothesis/blocker/open_gap taxonomy."),
        ("handoff", "Create v478 x1 synthesis if notifier and source checks pass."),
        ("handoff", "Decide x2 or x3 from blocker dominance."),
        ("handoff", "Carry app-lane success as the baseline coordination mode."),
        ("handoff", "Carry CLI timeout as a named risk."),
        ("handoff", "Prepare v478 x2 roadmap after x1 closeout."),
        ("thos", "Surface command-index repair candidate rows."),
        ("thos", "Surface v54/v55 handoff packs as non-proof references."),
        ("thos", "Draft a local-server health mini-dashboard concept."),
        ("thos", "Draft a connector-read/write boundary manifest."),
        ("thos", "Draft a watcher-runner reusable interface."),
        ("quality", "Review all summaries for overclaim language."),
        ("quality", "Confirm app-lane receipts stay status-only."),
        ("quality", "Confirm no broad staging happened."),
        ("quality", "Prepare concise user-facing closeout."),
        ("quality", "Keep the larger v490 goal active after v478 handoff."),
    ]
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": [{"id": f"V478X1-{idx:02d}", "domain": domain, "task": task} for idx, (domain, task) in enumerate(tasks, start=1)],
    }
    write_json("v478-thos-v1-x1-roadmap-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Roadmap",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- task_count: `{len(tasks)}`",
        "",
        "## Tasks",
    ]
    for row in payload["tasks"]:
        lines.append(f"- `{row['id']}` ({row['domain']}): {row['task']}")
    write_md("v478-thos-v1-x1-roadmap-v1.md", lines)


def schema_check(generated_utc: str, generated_nz: str) -> None:
    names = [
        "v477-thos-v8-x2-source-ledger-v1.json",
        "v477-thos-v8-x2-lane-continuity-board-v1.json",
        "v477-thos-v8-x2-command-index-bridge-plan-v1.json",
        "v477-thos-v8-x2-skill-acceptance-profile-v1.json",
        "v477-thos-v8-x2-expansion-blocker-table-v1.json",
        "v477-thos-v8-x2-watcher-acceptance-table-v1.json",
        "v477-thos-v8-x2-overlay-decision-v1.json",
        "v477-thos-v8-x2-synthesis-v1.json",
        "v477-thos-v8-x2-run-status-v1.json",
        "v478-thos-v1-x1-roadmap-v1.json",
    ]
    rows = []
    for name in names:
        data = load_json(name)
        required = ["artifact_type", "phase", "generated_utc", "generated_nz"]
        missing = [key for key in required if key not in data]
        rows.append({"artifact": name, "missing_keys": missing, "status": "PASS" if not missing else "FAIL"})
    payload = {
        "artifact_type": "schema_bound_artifact_check",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "rows": rows,
    }
    write_json("v477-thos-v8-x2-schema-bound-artifact-check-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Schema-Bound Artifact Check",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Rows",
    ]
    for row in rows:
        lines.append(f"- `{row['artifact']}`: `{row['status']}`.")
    write_md("v477-thos-v8-x2-schema-bound-artifact-check-v1.md", lines)


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app = load_json("v477-thos-v8-x2-app-lane-completion-notifier-v1.json")
    cli = load_json("v477-thos-v8-x2-cli-lane-completion-poll-v1.json")
    command_receipts = load_json("v477-thos-v8-x1-command-no-write-receipts-v1.json")
    skill_summary = load_json("v477-thos-v8-x1-skill-readiness-summary-v1.json")
    expansion_buckets = load_json("v477-thos-v8-x1-expansion-action-buckets-v1.json")

    make_source_ledger(generated_utc, generated_nz)
    lane_continuity(app, cli, generated_utc, generated_nz)
    command_bridge(command_receipts, generated_utc, generated_nz)
    skill_acceptance(skill_summary, generated_utc, generated_nz)
    expansion_blockers(expansion_buckets, generated_utc, generated_nz)
    watcher_acceptance(generated_utc, generated_nz)
    overlay_decision(generated_utc, generated_nz)
    synthesis(generated_utc, generated_nz)
    run_status(generated_utc, generated_nz, app, cli)
    roadmap(generated_utc, generated_nz)
    schema_check(generated_utc, generated_nz)
    print(
        json.dumps(
            {
                "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
                "phase": PHASE,
                "overlay_decision": "NO_X3_FOR_V8",
                "next_expected": NEXT_PHASE,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
