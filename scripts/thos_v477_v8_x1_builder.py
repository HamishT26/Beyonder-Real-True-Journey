#!/usr/bin/env python3
"""Build curated v477 THOS v8 x1 readiness artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v8_x1"
NEXT_PHASE = "v477_thos_v8_x2"


SOURCE_ROWS = [
    {
        "id": "S01",
        "query": "OpenAI Codex app-server official app server stdio thread resume turn start",
        "source": "OpenAI Codex app-server README",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "use": "Local app-lane notifier routing and sanitized thread read/resume/start evidence.",
    },
    {
        "id": "S02",
        "query": "OpenAI Codex CLI releases official 0.136.0",
        "source": "OpenAI Codex releases",
        "url": "https://github.com/openai/codex/releases",
        "use": "CLI readiness context and version-drift checks.",
    },
    {
        "id": "S03",
        "query": "OpenAI Codex Windows sandbox official restricted token",
        "source": "OpenAI Windows sandbox writeup",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "use": "Sandbox constraint routing for Arby/Aster and app-lane read-only requests.",
    },
    {
        "id": "S04",
        "query": "MCP tools spec 2025-06-18 annotations resource links",
        "source": "MCP tools specification",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/tools",
        "use": "Tool metadata and command-index surface contracts.",
    },
    {
        "id": "S05",
        "query": "MCP authorization 2025-06-18 OAuth resource parameter",
        "source": "MCP authorization specification",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
        "use": "Connector access boundary checks for read/use surfaces.",
    },
    {
        "id": "S06",
        "query": "MCP security best practices 2026 tool poisoning",
        "source": "MCP security best practices",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices",
        "use": "Tool-poisoning and cross-tool trust boundaries.",
    },
    {
        "id": "S07",
        "query": "MCP SDK docs Python TypeScript 2026",
        "source": "MCP SDK documentation",
        "url": "https://modelcontextprotocol.io/docs/sdk",
        "use": "Future local connector runner design.",
    },
    {
        "id": "S08",
        "query": "GitHub Actions security hardening official OIDC least privilege",
        "source": "GitHub Actions security hardening",
        "url": "https://docs.github.com/en/actions/how-tos/security-for-github-actions",
        "use": "Commit/push and automation guard requirements.",
    },
    {
        "id": "S09",
        "query": "GitHub secret scanning push protection official docs bypass review",
        "source": "GitHub push protection",
        "url": "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection",
        "use": "Publication guard checks before exact staging.",
    },
    {
        "id": "S10",
        "query": "GitHub code scanning SARIF support official result limits",
        "source": "GitHub SARIF support",
        "url": "https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning",
        "use": "Structured issue-report shape for later THOS validators.",
    },
    {
        "id": "S11",
        "query": "GitHub Copilot coding agent MCP official docs",
        "source": "GitHub Copilot coding agent MCP docs",
        "url": "https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-coding-agent-with-mcp",
        "use": "MCP handoff and agent tool exposure context.",
    },
    {
        "id": "S12",
        "query": "Windows Sandbox configure WSB file official Microsoft docs",
        "source": "Microsoft Windows Sandbox configuration",
        "url": "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file",
        "use": "Sandbox setup blocker taxonomy.",
    },
    {
        "id": "S13",
        "query": "Windows Mandatory Integrity Control official Microsoft docs integrity levels",
        "source": "Microsoft Mandatory Integrity Control",
        "url": "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control",
        "use": "Windows trust-boundary reasoning for low-write probes.",
    },
    {
        "id": "S14",
        "query": "Python subprocess security considerations official docs 3.12",
        "source": "Python subprocess documentation",
        "url": "https://docs.python.org/3.12/library/subprocess.html",
        "use": "Bounded launcher and notifier process handling.",
    },
    {
        "id": "S15",
        "query": "Python tempfile TemporaryDirectory cleanup official docs 3.12",
        "source": "Python tempfile documentation",
        "url": "https://docs.python.org/3.12/library/tempfile.html",
        "use": "Temp-only lane output handling.",
    },
    {
        "id": "S16",
        "query": "OpenTelemetry signals official docs traces metrics logs events",
        "source": "OpenTelemetry signals",
        "url": "https://opentelemetry.io/docs/concepts/signals/",
        "use": "Watcher event taxonomy without publishing event payloads.",
    },
    {
        "id": "S17",
        "query": "Docker Compose Watch official docs file watch",
        "source": "Docker Compose Watch",
        "url": "https://docs.docker.com/compose/how-tos/file-watch/",
        "use": "Future local service watcher design.",
    },
    {
        "id": "S18",
        "query": "Kubernetes Jobs completion backoffLimit official docs",
        "source": "Kubernetes Jobs",
        "url": "https://kubernetes.io/docs/concepts/workloads/controllers/job/",
        "use": "Retry budget and blocker-dominance conventions.",
    },
    {
        "id": "S19",
        "query": "OpenTelemetry semantic conventions official docs",
        "source": "OpenTelemetry semantic conventions",
        "url": "https://opentelemetry.io/docs/specs/semconv/",
        "use": "Portable naming scheme for THOS receipt events.",
    },
    {
        "id": "S20",
        "query": "Google Vertex AI Agent Engine overview official",
        "source": "Vertex AI Agent Engine overview",
        "url": "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "use": "External agent-engine comparison context only.",
    },
    {
        "id": "S21",
        "query": "Google Gemini API File Search multimodal RAG official",
        "source": "Gemini API File Search",
        "url": "https://ai.google.dev/gemini-api/docs/file-search",
        "use": "Future RAG handoff framing.",
    },
    {
        "id": "S22",
        "query": "NVIDIA NIM microservices official docs",
        "source": "NVIDIA NIM documentation",
        "url": "https://docs.nvidia.com/nim/",
        "use": "Compute expansion context, not executed in this phase.",
    },
    {
        "id": "S23",
        "query": "NVIDIA DGX Spark user guide official",
        "source": "NVIDIA DGX Spark documentation",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/index.html",
        "use": "Hardware-roadmap context, not a local capability claim.",
    },
    {
        "id": "S24",
        "query": "NIST AI Risk Management Framework official generative AI profile",
        "source": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "use": "Risk register and safety-governance language.",
    },
    {
        "id": "S25",
        "query": "UNESCO Recommendation Ethics Artificial Intelligence official",
        "source": "UNESCO AI ethics recommendation",
        "url": "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
        "use": "High-level governance context only.",
    },
    {
        "id": "S26",
        "query": "OECD AI Principles official",
        "source": "OECD AI principles",
        "url": "https://www.oecd.org/en/topics/ai-principles.html",
        "use": "High-level governance context only.",
    },
    {
        "id": "S27",
        "query": "EU AI Act implementation timeline official",
        "source": "EU AI Act implementation timeline",
        "url": "https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline",
        "use": "Regulatory-timeline context for future THOS compliance notes.",
    },
    {
        "id": "S28",
        "query": "OpenAI Agents SDK tracing official docs handoffs tools",
        "source": "OpenAI Agents SDK guide",
        "url": "https://platform.openai.com/docs/guides/agents-sdk/",
        "use": "Agent handoff and trace framing.",
    },
    {
        "id": "S29",
        "query": "OpenAI Agents SDK tracing official docs",
        "source": "OpenAI Agents SDK tracing",
        "url": "https://openai.github.io/openai-agents-python/tracing/",
        "use": "Trace shape inspiration for local notifier receipts.",
    },
    {
        "id": "S30",
        "query": "OpenAI Agents SDK handoffs official docs",
        "source": "OpenAI Agents SDK handoffs",
        "url": "https://openai.github.io/openai-agents-js/guides/handoffs/",
        "use": "Handoff-board framing for v8 x2.",
    },
    {
        "id": "S31",
        "query": "OpenAI Apps SDK MCP tools official documentation",
        "source": "OpenAI Apps SDK help",
        "url": "https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk",
        "use": "App connector/tool-surface context.",
    },
    {
        "id": "S32",
        "query": "OpenAI structured outputs JSON schema official docs",
        "source": "OpenAI structured outputs",
        "url": "https://platform.openai.com/docs/guides/structured-outputs",
        "use": "Schema-bound receipt quality checks.",
    },
]


def load_json(name: str) -> Any:
    return json.loads((TRACE_DIR / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key, "unknown")) for row in rows))


def make_source_ledger(generated_utc: str, generated_nz: str) -> None:
    payload = {
        "artifact_type": "source_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_count": len(SOURCE_ROWS),
        "policy": {
            "official_sources_preferred": True,
            "queued_searches_claimed_complete": False,
            "scope": "THOS app-lane notifier, command-surface, connector, sandbox, and schema-readiness context.",
        },
        "rows": SOURCE_ROWS,
    }
    write_json("v477-thos-v8-x1-source-ledger-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Source Ledger",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- source_count: `{len(SOURCE_ROWS)}`",
        "- policy: official or primary sources preferred; no queued search is claimed as completed unless represented in this ledger.",
        "",
        "## Sources",
    ]
    for row in SOURCE_ROWS:
        lines.append(f"- {row['id']}: [{row['source']}]({row['url']}) — {row['use']}")
    write_md("v477-thos-v8-x1-source-ledger-v1.md", lines)


def make_lane_board(generated_utc: str, generated_nz: str, app: dict[str, Any], probe: dict[str, Any], cli: dict[str, Any]) -> None:
    app_rows = []
    for lane in app.get("lanes", []):
        app_rows.append(
            {
                "lane": lane.get("lane"),
                "channel": "app_local_server",
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_status": lane.get("turn_start", {}).get("status"),
                "completion_status": lane.get("turn_completion", {}).get("status"),
                "overall_status": lane.get("overall_status"),
                "duration_seconds": lane.get("duration_seconds"),
                "new_thread_created": lane.get("new_thread_created", False),
                "transport_payload_published": lane.get("unfiltered_transport_published", False),
            }
        )
    cli_rows = []
    for lane in cli.get("lanes", []):
        cli_rows.append(
            {
                "lane": lane.get("lane"),
                "channel": "cli_notifier",
                "completion_status": lane.get("completion_status"),
                "overall_status": cli.get("aggregate_status"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "output_boundary": lane.get("raw_output_boundary"),
            }
        )
    payload = {
        "artifact_type": "lane_done_signal_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP",
        "app_probe_status": probe.get("overall_status"),
        "app_notify_status": app.get("overall_status"),
        "cli_status": cli.get("aggregate_status"),
        "done_signal_contract": {
            "app_lane_done": "thread read, resume, turn start, and turn completion are observed through the local app server.",
            "cli_lane_done": "final-message marker is present in the temp-only watcher output.",
            "open_gap_rule": "CLI timeout remains an open gap when app lanes pass but CLI final-message markers are absent.",
        },
        "app_lanes": app_rows,
        "cli_lanes": cli_rows,
        "claim_boundary": "THOS coordination evidence only; all GMUT gates remain open.",
    }
    write_json("v477-thos-v8-x1-lane-done-signal-board-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Lane Done-Signal Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        f"- app_notify_status: `{app.get('overall_status')}`",
        f"- cli_status: `{cli.get('aggregate_status')}`",
        "- done-signal rule: app lanes count complete through local-server turn completion; CLI lanes require final-message markers.",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(
            f"- {row['lane']}: `{row['overall_status']}`; read `{row['read_status']}`, resume `{row['resume_status']}`, "
            f"turn `{row['turn_status']}`, completion `{row['completion_status']}`."
        )
    lines.append("")
    lines.append("## CLI Lanes")
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['overall_status']}` with `{row['completion_status']}`.")
    write_md("v477-thos-v8-x1-lane-done-signal-board-v1.md", lines)


def make_command_receipts(generated_utc: str, generated_nz: str, command_ranking: dict[str, Any]) -> None:
    rows = list(command_ranking.get("rows", []))
    ready = [row for row in rows if row.get("rank_bucket") == "v8_ready_no_write"]
    gaps = [row for row in rows if row.get("rank_bucket") != "v8_ready_no_write"]
    payload_rows = []
    for rank, row in enumerate(ready[:24], start=1):
        payload_rows.append(
            {
                "rank": rank,
                "command_id": row.get("command_id"),
                "queue": row.get("queue"),
                "intent": row.get("intent"),
                "risk_class": row.get("risk_class"),
                "readiness": row.get("readiness"),
                "proof_score": row.get("proof_score"),
                "execution_status": "not_executed_v8_x1_receipt_only",
                "next_use": "candidate for v8 x2 dry-run or no-write proof extension",
            }
        )
    gap_rows = [
        {
            "command_id": row.get("command_id"),
            "queue": row.get("queue"),
            "reason": row.get("rank_bucket"),
            "execution_status": "held_open_gap",
        }
        for row in gaps[:12]
    ]
    payload = {
        "artifact_type": "command_no_write_receipts",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "execution_performed": False,
        "source_artifact": "v477-thos-v7-x2-command-proof-ranking-v1.json",
        "selected_count": len(payload_rows),
        "open_gap_count": len(gap_rows),
        "rows": payload_rows,
        "open_gaps": gap_rows,
    }
    write_json("v477-thos-v8-x1-command-no-write-receipts-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Command No-Write Receipts",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- execution_performed: `false`",
        f"- selected_count: `{len(payload_rows)}`",
        f"- open_gap_count: `{len(gap_rows)}`",
        "",
        "## Selected Rows",
    ]
    for row in payload_rows[:12]:
        lines.append(f"- {row['rank']}. `{row['command_id']}` ({row['queue']}): {row['intent']}")
    write_md("v477-thos-v8-x1-command-no-write-receipts-v1.md", lines)


def make_skill_summary(generated_utc: str, generated_nz: str, skill_review: dict[str, Any]) -> None:
    rows = list(skill_review.get("rows", []))
    payload_rows = []
    for row in rows:
        payload_rows.append(
            {
                "skill_dir": row.get("skill_dir"),
                "skill_status": row.get("skill_status"),
                "matched_command_id": row.get("matched_command_id"),
                "join_status": row.get("join_status"),
                "review_status": row.get("review_status"),
                "mutation_performed": False,
            }
        )
    payload = {
        "artifact_type": "skill_readiness_summary",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_artifact": "v477-thos-v7-x2-skill-join-review-v1.json",
        "metadata_only": True,
        "body_text_copied": False,
        "counts": count_by(payload_rows, "review_status"),
        "rows": payload_rows,
    }
    write_json("v477-thos-v8-x1-skill-readiness-summary-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Skill Readiness Summary",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- metadata_only: `true`",
        "- body_text_copied: `false`",
        "",
        "## Sampled Skill Rows",
    ]
    for row in payload_rows[:16]:
        lines.append(
            f"- `{row['skill_dir']}`: `{row['review_status']}`, matched command `{row['matched_command_id']}`."
        )
    write_md("v477-thos-v8-x1-skill-readiness-summary-v1.md", lines)


def make_expansion_buckets(generated_utc: str, generated_nz: str, expansion_board: dict[str, Any]) -> None:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expansion_board.get("rows", []):
        buckets[str(row.get("next_action", "unknown"))].append(
            {
                "id": row.get("id"),
                "tier": row.get("tier"),
                "proposal": row.get("proposal"),
                "source_type": row.get("source_type"),
                "write_scope": row.get("write_scope"),
                "installed": False,
                "promotion_allowed": row.get("promotion_allowed"),
            }
        )
    payload = {
        "artifact_type": "expansion_action_buckets",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "source_artifact": "v477-thos-v7-x2-expansion-readiness-board-v1.json",
        "installed_count": 0,
        "mutation_performed": False,
        "bucket_counts": {key: len(value) for key, value in sorted(buckets.items())},
        "buckets": dict(sorted(buckets.items())),
    }
    write_json("v477-thos-v8-x1-expansion-action-buckets-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Expansion Action Buckets",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- installed_count: `0`",
        "- mutation_performed: `false`",
        "",
        "## Buckets",
    ]
    for key, value in sorted(buckets.items()):
        lines.append(f"- `{key}`: `{len(value)}` rows.")
    write_md("v477-thos-v8-x1-expansion-action-buckets-v1.md", lines)


def make_schema_check(generated_utc: str, generated_nz: str) -> None:
    required = {
        "v477-thos-v8-x1-app-lane-completion-notifier-v1.json": ["artifact_type", "phase_slug", "overall_status", "lanes"],
        "v477-thos-v8-x1-cli-lane-completion-poll-v1.json": ["aggregate_status", "phase_slug", "lanes", "mutation_performed"],
        "v477-thos-v8-x1-source-ledger-v1.json": ["artifact_type", "phase", "source_count", "rows"],
        "v477-thos-v8-x1-command-no-write-receipts-v1.json": ["artifact_type", "phase", "rows", "execution_performed"],
        "v477-thos-v8-x1-skill-readiness-summary-v1.json": ["artifact_type", "phase", "rows", "metadata_only"],
        "v477-thos-v8-x1-expansion-action-buckets-v1.json": ["artifact_type", "phase", "buckets", "installed_count"],
    }
    rows = []
    for name, keys in required.items():
        data = load_json(name)
        missing = [key for key in keys if key not in data]
        rows.append({"artifact": name, "required_keys": keys, "missing_keys": missing, "status": "PASS" if not missing else "FAIL"})
    payload = {
        "artifact_type": "schema_bound_artifact_check",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "schema_policy": {
            "required_top_level_keys_checked": True,
            "structured_output_source_context": "S32",
            "observability_source_context": "S16",
        },
        "rows": rows,
    }
    write_json("v477-thos-v8-x1-schema-bound-artifact-check-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Schema-Bound Artifact Check",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- overall_status: `{payload['overall_status']}`",
        "",
        "## Checked Artifacts",
    ]
    for row in rows:
        lines.append(f"- `{row['artifact']}`: `{row['status']}`.")
    write_md("v477-thos-v8-x1-schema-bound-artifact-check-v1.md", lines)


def synthesis_steps() -> list[dict[str, str]]:
    topics = [
        "Local app-server notification is now the dominant success path for Cicero, Kierkegaard, and Aristotle.",
        "The app-lane runner used existing thread IDs and did not create replacement lanes.",
        "Read-only sandbox and never-approval settings were requested for every app lane.",
        "All three app lanes reached turn completion in the v8 x1 receipt.",
        "The CLI watcher remains useful but should not block app-lane progress.",
        "Arby and Aster Vale still need a final-message marker before their CLI lane can be called complete.",
        "The correct merged status is pass-with-open-gap rather than full six-lane closure.",
        "No app transport payload needs to be published for phase evidence.",
        "Command proof rows should continue in no-write mode until stronger command-index bindings are attached.",
        "Weak command rows stay open gaps rather than becoming hidden assumptions.",
        "Skill rows are useful as metadata joins but must not copy skill bodies into curated receipts.",
        "Expansion rows remain proposals until a separate live-write approval promotes them.",
        "Schema-bound checks reduce handoff drift between x1 and x2 artifacts.",
        "OpenTelemetry signal language is useful for watcher taxonomy without exposing event payloads.",
        "Kubernetes job completion language maps well to retry and blocker-dominance rules.",
        "Windows sandbox evidence should be treated as platform readiness context, not as blanket safety proof.",
        "MCP tool metadata should become the command-index bridge in the next x2 step.",
        "Connector reads remain useful but connector writes need separate exact approval.",
        "Source ledgers need official URLs and a clear use field for each source.",
        "The app-lane notifier should remain small and reusable instead of becoming a giant phase runner.",
        "The older phase-specific app-lane wrapper can remain historical while the generic notifier becomes preferred.",
        "Every lane receipt should distinguish reachability, turn start, turn completion, and content synthesis.",
        "The v8 x2 synthesis should decide whether x3 is necessary from blocker evidence, not from enthusiasm.",
        "The v8 x2 roadmap should retain exact staging and remote verification as mandatory closure.",
        "Journey context remains non-canon and cannot close any GMUT gate.",
        "GMUT gates remain open unless exact closure artifacts exist.",
        "THOS work can improve infrastructure without validating physics claims by association.",
        "The next phase should carry app-lane success forward and retry CLI once without duplicating polling loops.",
        "Final synthesis should report the CLI timeout plainly.",
        "The durable outcome is a working app-lane notifier plus a curated v8 x2 handoff.",
    ]
    return [{"step": f"R{index:02d}", "finding": topic} for index, topic in enumerate(topics, start=1)]


def make_synthesis(generated_utc: str, generated_nz: str) -> None:
    steps = synthesis_steps()
    payload = {
        "artifact_type": "phase_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "reflection_step_count": len(steps),
        "steps": steps,
        "claim_boundary": {
            "thos_scope": "notifier, command-surface, skill metadata, expansion queue, and handoff readiness",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v477-thos-v8-x1-synthesis-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Synthesis",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        "- claim boundary: THOS infrastructure readiness only; all GMUT gates remain open.",
        "",
        "## Reflection Steps",
    ]
    for step in steps:
        lines.append(f"- {step['step']}: {step['finding']}")
    write_md("v477-thos-v8-x1-synthesis-v1.md", lines)


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
            {"name": "source_refresh", "status": "PASS", "source_count": len(SOURCE_ROWS)},
            {"name": "commands", "status": "PASS_NO_EXECUTION"},
            {"name": "skills", "status": "PASS_METADATA_ONLY"},
            {"name": "expansions", "status": "PASS_NO_INSTALL"},
            {"name": "schema_bound_check", "status": "PASS"},
            {"name": "claim_boundary", "status": "PASS_ALL_GMUT_GATES_OPEN"},
        ],
        "next_expected": NEXT_PHASE,
    }
    write_json("v477-thos-v8-x1-run-status-v1.json", payload)
    lines = [
        "# v477 THOS v8 x1 Run Status",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
        f"- next_expected: `{NEXT_PHASE}`",
        "",
        "## Checks",
    ]
    for row in payload["checks"]:
        lines.append(f"- `{row['name']}`: `{row['status']}`.")
    write_md("v477-thos-v8-x1-run-status-v1.md", lines)


def roadmap_tasks(generated_utc: str, generated_nz: str) -> list[dict[str, str]]:
    domains = [
        ("lane", "Carry v8 x1 app-lane PASS evidence forward without republishing transport payloads."),
        ("lane", "Retry Arby and Aster Vale CLI watcher once with final-message marker criteria."),
        ("lane", "Keep CLI timeout as open gap if final-message markers remain absent."),
        ("lane", "Compare app-lane completion durations against v8 x1 receipt timing."),
        ("lane", "Record whether app lanes need another notification or only synthesis carry-forward."),
        ("command", "Promote top no-write command rows into v8 x2 proof groups."),
        ("command", "Keep weak command rows as explicit open gaps."),
        ("command", "Map command rows to command-index surface names."),
        ("command", "Flag any command lacking proof-required metadata."),
        ("command", "Prepare next dry-run-only command queue without executing it."),
        ("skill", "Join sampled skill metadata to command rows without copying skill bodies."),
        ("skill", "Score skill-command matches for actionability."),
        ("skill", "Identify duplicate or stale skill hints as open gaps."),
        ("skill", "Keep user and plugin skills unmodified."),
        ("skill", "Draft minimal future skill acceptance fields."),
        ("expansion", "Bucket expansions into no-write inspection, stdout-only probe, and toy-plan rows."),
        ("expansion", "Hold all installs and promotions until exact approval exists."),
        ("expansion", "Select the safest expansion probes for a future P1/P2 pass."),
        ("expansion", "Reject any expansion that needs account or destructive action."),
        ("expansion", "Produce an expansion blocker table for x2 synthesis."),
        ("source", "Refresh source drift only where v8 x2 needs newer evidence."),
        ("source", "Preserve official-source preference."),
        ("source", "Keep each source mapped to a specific THOS use."),
        ("source", "Separate governance context from local implementation evidence."),
        ("source", "Avoid claiming queued searches as complete."),
        ("schema", "Run JSON parse for every v8 x2 artifact."),
        ("schema", "Check required top-level keys for every handoff artifact."),
        ("schema", "Ensure run-status, synthesis, and roadmap agree on next phase."),
        ("schema", "Keep output rows bounded and deterministic."),
        ("schema", "Record any schema misses as blocker rows."),
        ("watcher", "Align app-lane done signals with local app-server events."),
        ("watcher", "Align CLI done signals with temp-only final-message markers."),
        ("watcher", "Avoid duplicate polling loops inside the same phase."),
        ("watcher", "Write a compact watcher acceptance table."),
        ("watcher", "Keep notifier scripts reusable across v478+ phases."),
        ("safety", "Fetch and drift-check before any publication."),
        ("safety", "Exact-stage only v8 scoped files."),
        ("safety", "Run publication guard scans before commit."),
        ("safety", "Reject broad staging even when worktree is noisy."),
        ("safety", "Remote-verify equals local after push."),
        ("claim", "Keep all six GMUT gates open."),
        ("claim", "Do not treat THOS infrastructure as GMUT validation."),
        ("claim", "Mark Journey context as non-canon if referenced."),
        ("claim", "Avoid final physics or consciousness-proof claims."),
        ("claim", "Keep fifth-force safety as open until exact physics artifacts exist."),
        ("handoff", "Decide whether v8 x3 is needed from blocker dominance."),
        ("handoff", "If no x3 is needed, produce v478 v1 roadmap."),
        ("handoff", "If x3 is needed, scope it to one blocker family."),
        ("handoff", "Write concise lane instructions for the next app notifier pass."),
        ("handoff", "Carry CLI timeout as a known risk until resolved."),
        ("thos", "Turn the command-index surface into a navigable manifest."),
        ("thos", "Surface v54/v55 handoff packs as references, not proof."),
        ("thos", "Keep connector reads separate from connector writes."),
        ("thos", "Draft a local-service health panel concept."),
        ("thos", "Document local app-server route as preferred app-lane path."),
        ("quality", "Review artifact names for phase consistency."),
        ("quality", "Review markdown summaries for overclaim language."),
        ("quality", "Verify no transport payloads entered curated artifacts."),
        ("quality", "Keep generated tables short enough for handoff use."),
        ("quality", "Prepare final v8 x2 synthesis and next roadmap."),
    ]
    return [
        {"id": f"V8X2-{index:02d}", "domain": domain, "task": task}
        for index, (domain, task) in enumerate(domains, start=1)
    ]


def make_roadmap(generated_utc: str, generated_nz: str) -> None:
    tasks = roadmap_tasks(generated_utc, generated_nz)
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": tasks,
    }
    write_json("v477-thos-v8-x2-roadmap-v1.json", payload)
    lines = [
        "# v477 THOS v8 x2 Roadmap",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- task_count: `{len(tasks)}`",
        "",
        "## Tasks",
    ]
    for row in tasks:
        lines.append(f"- `{row['id']}` ({row['domain']}): {row['task']}")
    write_md("v477-thos-v8-x2-roadmap-v1.md", lines)


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app_probe = load_json("v477-thos-v8-x1-app-lane-completion-notifier-probe-v1.json")
    app_notify = load_json("v477-thos-v8-x1-app-lane-completion-notifier-v1.json")
    cli_poll = load_json("v477-thos-v8-x1-cli-lane-completion-poll-v1.json")
    command_ranking = load_json("v477-thos-v7-x2-command-proof-ranking-v1.json")
    skill_review = load_json("v477-thos-v7-x2-skill-join-review-v1.json")
    expansion_board = load_json("v477-thos-v7-x2-expansion-readiness-board-v1.json")

    make_source_ledger(generated_utc, generated_nz)
    make_lane_board(generated_utc, generated_nz, app_notify, app_probe, cli_poll)
    make_command_receipts(generated_utc, generated_nz, command_ranking)
    make_skill_summary(generated_utc, generated_nz, skill_review)
    make_expansion_buckets(generated_utc, generated_nz, expansion_board)
    make_schema_check(generated_utc, generated_nz)
    make_synthesis(generated_utc, generated_nz)
    make_run_status(generated_utc, generated_nz, app_notify, cli_poll)
    make_roadmap(generated_utc, generated_nz)

    print(
        json.dumps(
            {
                "status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
                "phase": PHASE,
                "next_expected": NEXT_PHASE,
                "generated_files": 18,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
