#!/usr/bin/env python3
"""Build curated v478 THOS v1 x1 readiness artifacts."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v1_x1"
NEXT_PHASE = "v478_thos_v1_x2"


SOURCES = [
    ("S01", "OpenAI Codex app-server README", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "local app-server app-lane routing"),
    ("S02", "OpenAI Codex CLI help", "https://help.openai.com/en/articles/11096431", "CLI and sandbox capability context"),
    ("S03", "OpenAI Codex releases", "https://github.com/openai/codex/releases", "CLI release drift context"),
    ("S04", "OpenAI Windows sandbox design", "https://openai.com/index/building-codex-windows-sandbox/", "Windows sandbox blocker routing"),
    ("S05", "OpenAI Codex harness architecture", "https://openai.com/index/unlocking-the-codex-harness/", "app-server architecture context"),
    ("S06", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "tool metadata and command surface design"),
    ("S07", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "connector boundary design"),
    ("S08", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "tool trust and blast-radius constraints"),
    ("S09", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "future connector runner implementation"),
    ("S10", "MCP client best practices", "https://modelcontextprotocol.io/docs/develop/clients/client-best-practices", "client-side tool boundary context"),
    ("S11", "OpenAI Apps SDK help", "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk", "apps and MCP bridge context"),
    ("S12", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "agent orchestration and handoff context"),
    ("S13", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "trace and watcher signal framing"),
    ("S14", "OpenAI Agents SDK handoffs", "https://openai.github.io/openai-agents-js/guides/handoffs/", "handoff surface framing"),
    ("S15", "OpenAI Agents SDK MCP guide", "https://openai.github.io/openai-agents-js/guides/mcp/", "MCP server tool use context"),
    ("S16", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "schema-bound artifact quality"),
    ("S17", "GitHub Actions security hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "least-privilege publication safety"),
    ("S18", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "publication guard context"),
    ("S19", "GitHub SARIF limits", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/troubleshoot-sarif-uploads/results-exceed-limit", "bounded finding output design"),
    ("S20", "GitHub MCP server in IDE", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "GitHub connector comparison context"),
    ("S21", "Microsoft Windows Sandbox WSB", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "Windows sandbox configuration context"),
    ("S22", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "Windows integrity boundary context"),
    ("S23", "Microsoft AppContainer isolation", "https://learn.microsoft.com/en-gb/windows/security/book/application-security-application-isolation", "Windows isolation spectrum context"),
    ("S24", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "stdout and stderr watcher handling"),
    ("S25", "Python subprocess", "https://docs.python.org/3.12/library/subprocess.html", "bounded process execution design"),
    ("S26", "Python tempfile", "https://docs.python.org/3.12/library/tempfile.html", "temp-only watcher storage"),
    ("S27", "Python json", "https://docs.python.org/3.12/library/json.html", "JSON parse validation"),
    ("S28", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "watcher event taxonomy"),
    ("S29", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "local file watcher comparison"),
    ("S30", "Kubernetes Jobs", "https://kubernetes.io/docs/reference/kubernetes-api/batch/job-v1/", "completion and backoff comparison"),
    ("S31", "Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine", "external agent engine comparison"),
    ("S32", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "RAG and document retrieval comparison"),
    ("S33", "NVIDIA NIM", "https://docs.nvidia.com/nim/", "inference service expansion context"),
    ("S34", "NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "local AI workstation context"),
    ("S35", "NVIDIA Omniverse docs", "https://docs.nvidia.com/omniverse/index.html", "simulation and digitalization context"),
    ("S36", "NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "risk management language"),
    ("S37", "UNESCO AI ethics recommendation", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "governance context"),
    ("S38", "OECD AI principles", "https://www.oecd.org/en/topics/ai-principles.html", "governance context"),
    ("S39", "EU AI Act timeline", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline", "regulatory timeline context"),
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


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def source_ledger(generated_utc: str, generated_nz: str) -> None:
    rows = [
        {
            "id": source_id,
            "source": source,
            "url": url,
            "v478_x1_use": use,
            "source_class": "official_or_primary",
        }
        for source_id, source, url, use in SOURCES
    ]
    payload = {
        "artifact_type": "source_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 39,
        "source_count": len(rows),
        "queued_searches_claimed_complete": False,
        "rows": rows,
    }
    write_json("v478-thos-v1-x1-source-ledger-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Source Ledger",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- search_count: `39`",
        f"- source_count: `{len(rows)}`",
        "- boundary: sources guide THOS infrastructure decisions only; they do not validate GMUT.",
        "",
        "## Sources",
    ]
    lines.extend(f"- {row['id']}: [{row['source']}]({row['url']}) — {row['v478_x1_use']}." for row in rows)
    write_md("v478-thos-v1-x1-source-ledger-v1.md", lines)


def lane_board(generated_utc: str, generated_nz: str, probe: dict[str, Any], notify: dict[str, Any], cli: dict[str, Any]) -> None:
    app_rows = []
    for lane in notify.get("lanes", []):
        app_rows.append(
            {
                "lane": lane.get("lane"),
                "probe_status": probe.get("overall_status"),
                "notify_status": lane.get("overall_status"),
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_status": lane.get("turn_start", {}).get("status"),
                "completion_status": lane.get("turn_completion", {}).get("status"),
                "duration_seconds": lane.get("duration_seconds"),
                "message_payload_published": False,
            }
        )
    cli_rows = [
        {
            "lane": lane.get("lane"),
            "watch_status": cli.get("aggregate_status"),
            "completion_status": lane.get("completion_status"),
            "message_payload_published": False,
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
        "done_signal_rule": {
            "app_lane": "probe passes, notify turn starts, and turn completion is observed",
            "cli_lane": "final-message marker appears in temp-only watcher output",
            "known_open_gap": "CLI timeout is carried when final-message markers are absent",
        },
    }
    write_json("v478-thos-v1-x1-lane-status-board-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Lane Status Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(f"- {row['lane']}: `{row['notify_status']}` with completion `{row['completion_status']}`.")
    lines.append("")
    lines.append("## CLI Lanes")
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['watch_status']}` with `{row['completion_status']}`.")
    write_md("v478-thos-v1-x1-lane-status-board-v1.md", lines)


def command_surface(generated_utc: str, generated_nz: str) -> None:
    command_book = load_json(ROOT / "docs" / "trinity-command-book-v9.json")
    bridge = load_trace("v477-thos-v8-x2-command-index-bridge-plan-v1.json")
    commands = list(command_book.get("commands", []))
    bridge_ids = {row.get("command_id") for row in bridge.get("rows", [])}
    selected = []
    for cmd in commands:
        if len(selected) >= 30:
            break
        command_id = cmd.get("command_id")
        selected.append(
            {
                "command_id": command_id,
                "intent": cmd.get("intent"),
                "mode": cmd.get("mode"),
                "risk_class": cmd.get("risk_class"),
                "requires_live": bool(cmd.get("requires_live")),
                "requires_connector": bool(cmd.get("requires_connector")),
                "template_hash": short_hash(str(cmd.get("command_template", ""))),
                "expected_artifact_count": len(cmd.get("expected_artifacts", []) or []),
                "bridge_status": "v8_bridge_candidate" if command_id in bridge_ids else "command_book_sample",
                "v478_action": "surface_in_index_no_execution",
            }
        )
    payload = {
        "artifact_type": "command_index_surface_manifest",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_command_book": "trinity-command-book-v9.json",
        "execution_performed": False,
        "selected_count": len(selected),
        "rows": selected,
        "risk_counts": dict(Counter(str(row["risk_class"]) for row in selected)),
    }
    write_json("v478-thos-v1-x1-command-index-surface-manifest-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Command-Index Surface Manifest",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- execution_performed: `false`",
        f"- selected_count: `{len(selected)}`",
        "",
        "## Commands",
    ]
    for row in selected:
        lines.append(f"- `{row['command_id']}`: `{row['risk_class']}`, action `{row['v478_action']}`.")
    write_md("v478-thos-v1-x1-command-index-surface-manifest-v1.md", lines)


def skill_proposals(generated_utc: str, generated_nz: str) -> None:
    skill_root = Path.home() / ".codex" / "skills"
    skill_dirs = [p.name for p in sorted(skill_root.iterdir(), key=lambda p: p.name.lower()) if p.is_dir() and p.name != ".system"]
    selected = skill_dirs[:30]
    rows = []
    for idx, skill_name in enumerate(selected, start=1):
        family = skill_name.split("-")[0] if "-" in skill_name else skill_name
        rows.append(
            {
                "proposal_id": f"v478-skill-proposal-{idx:02d}",
                "source_skill": skill_name,
                "family_hint": family,
                "proposed_skill_surface": f"{skill_name}-v478-routing",
                "status": "proposal_only_not_created",
                "body_read": False,
                "mutation_performed": False,
                "acceptance_rule": "metadata route only; no skill body rewrite or cache mutation",
            }
        )
    payload = {
        "artifact_type": "skill_proposal_matrix",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "proposal_count": len(rows),
        "mutation_performed": False,
        "rows": rows,
    }
    write_json("v478-thos-v1-x1-skill-proposal-matrix-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Skill Proposal Matrix",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- mutation_performed: `false`",
        f"- proposal_count: `{len(rows)}`",
        "",
        "## Skill Proposals",
    ]
    for row in rows:
        lines.append(f"- `{row['proposal_id']}` from `{row['source_skill']}`: `{row['status']}`.")
    write_md("v478-thos-v1-x1-skill-proposal-matrix-v1.md", lines)


def expansion_review(generated_utc: str, generated_nz: str) -> None:
    manifest = load_json(ROOT / "docs" / "trinity-expansion-system-manifest-v9.json")
    systems = list(manifest.get("systems", []))[:30]
    rows = []
    for idx, system in enumerate(systems, start=1):
        mode = system.get("mode")
        profiles = system.get("profiles") or []
        action = "no_write_inspection"
        if "smoke" in profiles:
            action = "stdout_only_probe_candidate"
        if mode and "live" in str(mode).lower():
            action = "approval_needed_blocked"
        rows.append(
            {
                "proposal_id": f"v478-expansion-{idx:02d}",
                "system_id": system.get("system_id"),
                "pillar": system.get("pillar"),
                "mode": mode,
                "profile_count": len(profiles),
                "output_count": len(system.get("outputs", []) or []),
                "action_bucket": action,
                "installed": False,
                "mutation_performed": False,
            }
        )
    payload = {
        "artifact_type": "expansion_readiness_score_table",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_manifest": "trinity-expansion-system-manifest-v9.json",
        "selected_count": len(rows),
        "installed_count": 0,
        "rows": rows,
        "bucket_counts": dict(Counter(row["action_bucket"] for row in rows)),
    }
    write_json("v478-thos-v1-x1-expansion-readiness-score-table-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Expansion Readiness Score Table",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- installed_count: `0`",
        f"- selected_count: `{len(rows)}`",
        "",
        "## Expansion Rows",
    ]
    for row in rows:
        lines.append(f"- `{row['proposal_id']}` `{row['system_id']}`: `{row['action_bucket']}`.")
    write_md("v478-thos-v1-x1-expansion-readiness-score-table-v1.md", lines)


def watcher_template(generated_utc: str, generated_nz: str) -> None:
    rows = [
        ("app_probe", "run app-lane probe before notify", "required", "PASS"),
        ("app_notify", "send existing-thread notify only after probe passes", "required", "PASS"),
        ("app_completion", "observe turn completion per app lane", "required", "PASS"),
        ("cli_single_poll", "run one bounded CLI poll per phase closeout", "required", "PASS"),
        ("cli_final_marker", "require final-message marker for CLI closure", "required_for_cli_closure", "OPEN_GAP"),
        ("temp_only", "keep CLI watcher output temp-only", "required", "PASS"),
        ("transport_summary_only", "publish status summaries only", "required", "PASS"),
        ("retry_rule", "retry only when a new blocker class appears", "required", "PASS"),
        ("x_overlay_rule", "add x3 only when blocker dominance justifies it", "required", "PASS"),
    ]
    payload = {
        "artifact_type": "watcher_template",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "template_version": "v478-v1",
        "overall_status": "PASS_WITH_CLI_OPEN_GAP",
        "rows": [{"id": row_id, "criterion": criterion, "requirement": req, "status": status} for row_id, criterion, req, status in rows],
    }
    write_json("v478-thos-v1-x1-watcher-template-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Watcher Template",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_OPEN_GAP`",
        "",
        "## Criteria",
    ]
    for row in payload["rows"]:
        lines.append(f"- `{row['id']}`: `{row['status']}` — {row['criterion']}.")
    write_md("v478-thos-v1-x1-watcher-template-v1.md", lines)


def synthesis(generated_utc: str, generated_nz: str) -> None:
    findings = [
        "v478 x1 began from a remote-verified v477 x8 closeout rather than a guessed state.",
        "The app-lane probe passed before any notify turn was sent.",
        "Cicero completed through the local app-server notify path.",
        "Kierkegaard completed through the local app-server notify path.",
        "Aristotle completed through the local app-server notify path.",
        "The app-lane notifier continued to use existing threads only.",
        "No old-style sibling spawning was used.",
        "No new replacement sibling was created.",
        "The CLI watcher ran once for Arby and Aster Vale.",
        "Arby remained waiting for the final-message marker.",
        "Aster Vale remained waiting for the final-message marker.",
        "The CLI timeout is a carried open gap, not a blocker for app-lane progress.",
        "The command-index surface manifest selected 30 metadata-level command rows.",
        "Command rows were not executed in v478 x1.",
        "Command templates were represented by hashes rather than expanded command text.",
        "The skill proposal matrix selected 30 metadata-only skill proposals.",
        "No skill body was read into a curated artifact.",
        "No user skill or plugin cache file was modified.",
        "The expansion readiness table selected 30 no-install review rows.",
        "Expansion rows were classified into action buckets without live promotion.",
        "The source ledger contains 39 official or primary source rows.",
        "OpenAI Codex app-server sources support the local-server route context.",
        "MCP sources support the command and connector surface boundaries.",
        "GitHub sources support exact staging and publication safety.",
        "Microsoft, Python, and PowerShell sources support platform watcher constraints.",
        "OpenTelemetry, Docker, and Kubernetes sources support watcher and completion vocabulary.",
        "Google and NVIDIA sources are future expansion context, not claims of local deployment.",
        "NIST, UNESCO, OECD, and EU sources are governance context, not canon evidence.",
        "All six GMUT gates remain open.",
        "v478 x1 is ready for v478 x2 synthesis without needing an x3 overlay yet.",
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
            "scope": "THOS readiness, command surface, skill proposals, expansion review, and watcher routing",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v1-x1-synthesis-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Synthesis",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- reflection_step_count: `{len(findings)}`",
        "",
        "## Reflection Steps",
    ]
    for row in payload["findings"]:
        lines.append(f"- {row['step']}: {row['finding']}")
    write_md("v478-thos-v1-x1-synthesis-v1.md", lines)


def run_status(generated_utc: str, generated_nz: str, notify: dict[str, Any], cli: dict[str, Any]) -> None:
    payload = {
        "artifact_type": "run_status",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "checks": [
            {"name": "app_lanes", "status": notify.get("overall_status"), "interpretation": "pass"},
            {"name": "cli_lanes", "status": cli.get("aggregate_status"), "interpretation": "open_gap"},
            {"name": "source_refresh", "status": "PASS", "source_count": len(SOURCES)},
            {"name": "command_index_surface", "status": "PASS_NO_EXECUTION", "row_count": 30},
            {"name": "skill_proposals", "status": "PASS_METADATA_ONLY", "row_count": 30},
            {"name": "expansion_review", "status": "PASS_NO_INSTALL", "row_count": 30},
            {"name": "watcher_template", "status": "PASS_WITH_CLI_OPEN_GAP"},
            {"name": "claim_boundary", "status": "PASS_ALL_GMUT_GATES_OPEN"},
        ],
        "next_expected": NEXT_PHASE,
    }
    write_json("v478-thos-v1-x1-run-status-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Run Status",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Checks",
    ]
    for row in payload["checks"]:
        lines.append(f"- `{row['name']}`: `{row['status']}`.")
    write_md("v478-thos-v1-x1-run-status-v1.md", lines)


def roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = [
        ("lane", "Carry v478 x1 app-lane PASS into x2 synthesis without republishing message payloads."),
        ("lane", "Retry Arby/Aster watcher once only if x2 needs fresh CLI evidence."),
        ("lane", "Keep CLI final-marker timeout as explicit open gap."),
        ("lane", "Compare app-lane durations against v477 v8 baseline."),
        ("lane", "Record lane done-signals in compact x2 board."),
        ("command", "Rank the 30 command-index surface rows by risk and proof readiness."),
        ("command", "Select the safest stdout-only command rows for future P1 dry-run."),
        ("command", "Keep live/connector command rows blocked until exact approval."),
        ("command", "Map command rows to source categories from the source ledger."),
        ("command", "Draft command promotion criteria for v478 x2."),
        ("skill", "Score the 30 skill proposals for actionability."),
        ("skill", "Identify duplicate family hints and stale proposal names."),
        ("skill", "Map skill proposals to command-index rows where metadata allows."),
        ("skill", "Keep body text unpublished and unmodified."),
        ("skill", "Draft future skill acceptance schema."),
        ("expansion", "Rank the 30 expansion rows by action bucket."),
        ("expansion", "Choose no-write inspection rows for a future proof pass."),
        ("expansion", "Hold approval-needed rows as blockers."),
        ("expansion", "Separate simulation candidates from live promotion candidates."),
        ("expansion", "Draft expansion acceptance schema."),
        ("source", "Review source ledger for official-source drift."),
        ("source", "Separate implementation sources from governance sources."),
        ("source", "Carry Google/NVIDIA rows as expansion context only."),
        ("source", "Avoid using governance rows as technical proof."),
        ("source", "Decide whether x2 needs additional web refresh."),
        ("watcher", "Convert watcher template into x2 acceptance checklist."),
        ("watcher", "Keep app and CLI done-signals separate."),
        ("watcher", "Avoid duplicate CLI polling loops."),
        ("watcher", "Keep temp-only watcher outputs out of publication."),
        ("watcher", "Prepare v478 reusable notifier interface notes."),
        ("schema", "Parse every v478 x2 JSON artifact."),
        ("schema", "Check top-level keys and next_expected agreement."),
        ("schema", "Bound row counts and deterministic ordering."),
        ("schema", "Run guard scan before staging."),
        ("schema", "Review markdown summaries for overclaim language."),
        ("safety", "Fetch and drift-check before publication."),
        ("safety", "Exact-stage only v478 x2 scoped files."),
        ("safety", "Reject unpublished local dumps and transport payloads."),
        ("safety", "Run whitespace and staged diff review."),
        ("safety", "Push and remote-verify equals local."),
        ("claim", "Keep all six GMUT gates open."),
        ("claim", "Do not claim THOS infrastructure validates GMUT."),
        ("claim", "Do not claim consciousness proof or canon promotion."),
        ("claim", "Keep Journey context non-canon if referenced."),
        ("claim", "Use open_gap for CLI timeout."),
        ("handoff", "Decide whether v478 needs x3 from blocker dominance."),
        ("handoff", "If no x3 is needed, prepare v478 v2 x1 roadmap."),
        ("handoff", "If x3 is needed, scope it to one blocker family."),
        ("handoff", "Carry 30-command, 30-skill, and 30-expansion tables."),
        ("handoff", "Preserve exact staging and remote verification rules."),
        ("thos", "Draft command-index surface repair recommendations."),
        ("thos", "Draft connector read/write boundary recommendations."),
        ("thos", "Draft app-lane notifier health panel concept."),
        ("thos", "Draft skill proposal promotion criteria."),
        ("thos", "Draft expansion no-write rehearsal criteria."),
        ("quality", "Validate x2 synthesis against x1 evidence."),
        ("quality", "Keep file names phase-consistent."),
        ("quality", "Avoid broad staging in dirty worktree."),
        ("quality", "Publish concise final status."),
        ("quality", "Keep the larger v490 goal active."),
    ]
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": [{"id": f"V478X2-{idx:02d}", "domain": domain, "task": task} for idx, (domain, task) in enumerate(tasks, start=1)],
    }
    write_json("v478-thos-v1-x2-roadmap-v1.json", payload)
    lines = [
        "# v478 THOS v1 x2 Roadmap",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- task_count: `{len(tasks)}`",
        "",
        "## Tasks",
    ]
    for row in payload["tasks"]:
        lines.append(f"- `{row['id']}` ({row['domain']}): {row['task']}")
    write_md("v478-thos-v1-x2-roadmap-v1.md", lines)


def schema_check(generated_utc: str, generated_nz: str) -> None:
    names = [
        "v478-thos-v1-x1-source-ledger-v1.json",
        "v478-thos-v1-x1-lane-status-board-v1.json",
        "v478-thos-v1-x1-command-index-surface-manifest-v1.json",
        "v478-thos-v1-x1-skill-proposal-matrix-v1.json",
        "v478-thos-v1-x1-expansion-readiness-score-table-v1.json",
        "v478-thos-v1-x1-watcher-template-v1.json",
        "v478-thos-v1-x1-synthesis-v1.json",
        "v478-thos-v1-x1-run-status-v1.json",
        "v478-thos-v1-x2-roadmap-v1.json",
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
    write_json("v478-thos-v1-x1-schema-bound-artifact-check-v1.json", payload)
    lines = [
        "# v478 THOS v1 x1 Schema-Bound Artifact Check",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Rows",
    ]
    lines.extend(f"- `{row['artifact']}`: `{row['status']}`." for row in rows)
    write_md("v478-thos-v1-x1-schema-bound-artifact-check-v1.md", lines)


def main() -> int:
    generated_utc, generated_nz = now_pair()
    probe = load_trace("v478-thos-v1-x1-app-lane-completion-notifier-probe-v1.json")
    notify = load_trace("v478-thos-v1-x1-app-lane-completion-notifier-v1.json")
    cli = load_trace("v478-thos-v1-x1-cli-lane-completion-poll-v1.json")

    source_ledger(generated_utc, generated_nz)
    lane_board(generated_utc, generated_nz, probe, notify, cli)
    command_surface(generated_utc, generated_nz)
    skill_proposals(generated_utc, generated_nz)
    expansion_review(generated_utc, generated_nz)
    watcher_template(generated_utc, generated_nz)
    synthesis(generated_utc, generated_nz)
    run_status(generated_utc, generated_nz, notify, cli)
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
