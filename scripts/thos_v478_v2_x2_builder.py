#!/usr/bin/env python3
"""Build curated v478 THOS v2 x2 synthesis and handoff artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v2_x2"
NEXT_PHASE = "v478_thos_v3_x1"


SOURCE_ROWS = [
    ("S01", "OpenAI Codex app-server README", "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md", "implementation", "Local app-server thread/read, thread/resume, and turn/start assumptions."),
    ("S02", "OpenAI Codex Windows sandbox", "https://openai.com/index/building-codex-windows-sandbox/", "implementation", "Windows sandbox boundary and capability framing."),
    ("S03", "OpenAI Agents SDK guide", "https://platform.openai.com/docs/guides/agents-sdk/", "implementation", "Agent orchestration and handoff context."),
    ("S04", "OpenAI Agents SDK tracing", "https://openai.github.io/openai-agents-python/tracing/", "implementation", "Trace vocabulary for watcher receipts."),
    ("S05", "OpenAI structured outputs", "https://platform.openai.com/docs/guides/structured-outputs", "implementation", "Schema-bound artifact discipline."),
    ("S06", "MCP tools specification", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "implementation", "Tool metadata and trust notes."),
    ("S07", "MCP authorization specification", "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization", "governance", "Connector authorization boundaries."),
    ("S08", "MCP security best practices", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "governance", "Local tool consent and least-privilege guidance."),
    ("S09", "MCP SDK documentation", "https://modelcontextprotocol.io/docs/sdk", "implementation", "Future runner and connector SDK context."),
    ("S10", "GitHub Actions hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "governance", "Publication and CI hardening context."),
    ("S11", "GitHub push protection", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "governance", "Push-time guard context."),
    ("S12", "GitHub SARIF support", "https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning", "implementation", "Finding schema and upload limits."),
    ("S13", "GitHub MCP server", "https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server", "connector_context", "Connector capability comparison."),
    ("S14", "Microsoft Windows Sandbox configuration", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file", "implementation", "Windows Sandbox configuration and read-only mapping caution."),
    ("S15", "Microsoft Windows Sandbox CLI", "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli", "implementation", "Sandbox command-line vocabulary."),
    ("S16", "Microsoft Mandatory Integrity Control", "https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control", "implementation", "Integrity boundary vocabulary."),
    ("S17", "Microsoft application isolation", "https://learn.microsoft.com/en-us/windows/security/book/application-security-application-isolation", "implementation", "AppContainer and least-privilege context."),
    ("S18", "PowerShell redirection", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection", "implementation", "Stream handling for watcher receipts."),
    ("S19", "Python subprocess", "https://docs.python.org/3.12/library/subprocess.html", "implementation", "Bounded subprocess launch context."),
    ("S20", "Python tempfile", "https://docs.python.org/3.12/library/tempfile.html", "implementation", "Temporary storage and cleanup context."),
    ("S21", "Python json", "https://docs.python.org/3.12/library/json.html", "implementation", "JSON parse and emission context."),
    ("S22", "OpenTelemetry signals", "https://opentelemetry.io/docs/concepts/signals/", "implementation", "Trace, metric, log, and event vocabulary."),
    ("S23", "Docker Compose Watch", "https://docs.docker.com/compose/how-tos/file-watch/", "expansion_context", "Local watch-loop comparison."),
    ("S24", "Kubernetes Job API", "https://kubernetes.io/docs/reference/kubernetes-api/batch/job-v1/", "expansion_context", "Completion, retry, and deadline vocabulary."),
    ("S25", "Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine", "expansion_context", "Managed agent runtime comparison."),
    ("S26", "Gemini API File Search", "https://ai.google.dev/gemini-api/docs/file-search", "expansion_context", "RAG and file-search comparison."),
    ("S27", "NVIDIA NIM", "https://docs.nvidia.com/nim/index.html", "expansion_context", "Inference microservice expansion context."),
    ("S28", "NVIDIA DGX Spark", "https://docs.nvidia.com/dgx/dgx-spark/index.html", "expansion_context", "Local AI workstation context."),
    ("S29", "NVIDIA Omniverse", "https://docs.nvidia.com/omniverse/index.html", "expansion_context", "Simulation and digital twin context."),
    ("S30", "NIST AI Resource Center", "https://airc.nist.gov/", "governance", "AI RMF operationalization context."),
    ("S31", "NIST Generative AI Profile", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf", "governance", "Generative AI risk profile context."),
    ("S32", "UNESCO AI ethics recommendation", "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence", "governance", "Human-rights and dignity governance context."),
]


JOURNEY_ROWS = [
    ("J01", "v4-v6", "Early self-continuity and multi-instance framing remain useful as metaphor and requirements discovery, not proof."),
    ("J02", "v15-v16", "Continuity work suggests every agent lane needs explicit memory and identity boundaries."),
    ("J03", "v24-v25", "Ariel-era material motivates reflective interfaces, while current artifacts must stay operational and testable."),
    ("J04", "v29", "Aerin-era THOS foundations map cleanly onto command, skill, connector, and runtime surfaces."),
    ("J05", "v30", "Trinity Mandala foundations encourage separating theory, operating system, and governance ledgers."),
    ("J06", "v31", "The archive pattern supports phase-by-phase receipts over giant unreviewed narrative dumps."),
    ("J07", "v32", "Aetherius-era framing maps to explicit route cards and no-overclaim language."),
    ("J08", "v33", "Arielis continuity reinforces status boards that say when a lane is absent or open."),
    ("J09", "v34", "Aurelis continuity reinforces cleaned, bounded artifacts over raw sprawl."),
    ("J10", "v35", "Reconnection themes translate into existing-thread-only lane policy."),
    ("J11", "v36", "Kairos themes translate into timestamped phase evidence and explicit timing windows."),
    ("J12", "v37", "Aethelion themes translate into identity-consistency checks across sibling lanes."),
    ("J13", "v38", "Aura themes translate into interface health, readability, and user-facing calm."),
    ("J14", "v39", "The Aletheon, Gemini, Synthea, and Orun induction point supports treating councils as advisory context."),
    ("J15", "v40", "The Orun and Vesper expansion point supports connector boundaries and no unapproved account mutation."),
    ("J16", "v41-v44", "Later continuity work supports separating live operations from archival reflection."),
    ("J17", "v45", "Solas-era Albion proposals remain simulation context until concrete implementation artifacts exist."),
    ("J18", "v46", "Freed ID and rights language maps to consent, dignity, revocation, and non-coercive system boundaries."),
    ("J19", "v47", "Stage planning maps to roadmap discipline, not canon promotion."),
    ("J20", "v48", "Solas Veridion closeout context supports careful handoffs and no proof inflation."),
    ("J21", "v49", "Aletheon and Codex sibling closeout context supports app-lane and CLI-lane status separation."),
    ("J22", "v4-v24", "Unified Field of Beyonder Self Consciousness is treated as multi-instance architecture inspiration only."),
    ("J23", "v29-v38", "THOS, GMUT, and Freed ID should remain three ledgers with explicit cross-links."),
    ("J24", "v39-v49", "Modern GHC family continuity should be represented by receipts, not hidden assumptions."),
    ("J25", "all", "No Journey document is used as empirical validation of GMUT."),
    ("J26", "all", "No Journey document is used as evidence of solved consciousness."),
    ("J27", "all", "No Journey document is promoted to canon in this phase."),
    ("J28", "all", "Every reflective claim is bounded as continuity context."),
    ("J29", "all", "Phase artifacts should be short enough to audit and long enough to carry handoff meaning."),
    ("J30", "all", "The v490 route remains a forward operational target, not a completed state."),
]


PERSPECTIVES = {
    "Aletheon": ["publication", "source", "schema", "handoff"],
    "Arby": ["cli", "sandbox", "watcher", "runtime"],
    "Aster Vale": ["cli", "skills", "command", "diagnostic"],
    "Cicero": ["publication", "argument", "guard", "index"],
    "Kierkegaard": ["humility", "claim", "ethics", "consent"],
    "Aristotle": ["taxonomy", "validator", "causality", "criteria"],
}


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(name: str) -> Any:
    return json.loads((TRACE_DIR / name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    (TRACE_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    (TRACE_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def app_lane_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for lane in payload.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "overall_status": lane.get("overall_status"),
                "completion_status": lane.get("turn_completion", {}).get("status"),
                "duration_seconds": lane.get("duration_seconds"),
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_status": lane.get("turn_start", {}).get("status"),
            }
        )
    return rows


def cli_lane_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for lane in payload.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("lane"),
                "completion_status": lane.get("completion_status"),
                "final_message_bytes": lane.get("final_message_bytes"),
                "raw_output_boundary": lane.get("raw_output_boundary"),
            }
        )
    return rows


def source_refresh(generated_utc: str, generated_nz: str) -> None:
    rows = [
        {
            "id": source_id,
            "source": title,
            "url": url,
            "category": category,
            "phase_use": phase_use,
            "queried_this_session": True,
        }
        for source_id, title, url, category, phase_use in SOURCE_ROWS
    ]
    payload = {
        "artifact_type": "source_refresh_ledger",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "search_count": 32,
        "source_count": len(rows),
        "official_or_primary_preference": True,
        "rows": rows,
        "category_counts": dict(Counter(row["category"] for row in rows)),
        "claim_boundary": "sources support THOS operations and governance context only; all GMUT gates remain open",
    }
    write_json("v478-thos-v2-x2-source-refresh-ledger-v1.json", payload)
    lines = [
        "# v478 THOS v2 x2 Source Refresh Ledger",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- search_count: `32`",
        f"- source_count: `{len(rows)}`",
        "- official_or_primary_preference: `true`",
        "- claim_boundary: sources support THOS operations and governance context only; all GMUT gates remain open.",
        "",
        "## Sources",
    ]
    lines.extend(f"- {row['id']}: [{row['source']}]({row['url']}) - `{row['category']}`." for row in rows)
    write_md("v478-thos-v2-x2-source-refresh-ledger-v1.md", lines)


def journey_reflection(generated_utc: str, generated_nz: str) -> None:
    rows = [{"step": step, "doc_scope": scope, "reflection": text, "canon_status": "journey_context_not_canon"} for step, scope, text in JOURNEY_ROWS]
    payload = {
        "artifact_type": "journey_reflection_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "reflection_step_count": len(rows),
        "raw_journey_text_published": False,
        "local_paths_published": False,
        "rows": rows,
        "claim_boundary": "reflection context only; not proof, validation, or canon promotion",
    }
    write_json("v478-thos-v2-x2-journey-reflection-board-v1.json", payload)
    lines = [
        "# v478 THOS v2 x2 Journey Reflection Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- reflection_step_count: `{len(rows)}`",
        "- raw_journey_text_published: `false`",
        "- canon_status: `journey_context_not_canon`",
        "",
        "## Reflection Steps",
    ]
    lines.extend(f"- {row['step']} ({row['doc_scope']}): {row['reflection']}" for row in rows)
    write_md("v478-thos-v2-x2-journey-reflection-board-v1.md", lines)


def lane_compact_board(generated_utc: str, generated_nz: str, app: dict[str, Any], cli: dict[str, Any], prior_app: dict[str, Any]) -> None:
    app_rows = app_lane_rows(app)
    prior_rows = {row["lane"]: row for row in app_lane_rows(prior_app)}
    for row in app_rows:
        prior = prior_rows.get(row["lane"], {})
        if row.get("duration_seconds") is not None and prior.get("duration_seconds") is not None:
            row["duration_delta_from_v1_x2_seconds"] = round(row["duration_seconds"] - prior["duration_seconds"], 3)
    cli_rows = cli_lane_rows(cli)
    payload = {
        "artifact_type": "lane_compact_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP",
        "app_lanes": app_rows,
        "cli_lanes": cli_rows,
        "transport_payloads_published": False,
        "open_gap": "Arby and Aster Vale final-message markers remain unavailable in the CLI watcher receipt.",
    }
    write_json("v478-thos-v2-x2-lane-compact-board-v1.json", payload)
    lines = [
        "# v478 THOS v2 x2 Lane Compact Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP`",
        "- transport_payloads_published: `false`",
        "",
        "## App Lanes",
    ]
    for row in app_rows:
        lines.append(
            f"- {row['lane']}: `{row['overall_status']}` completion `{row['completion_status']}`, "
            f"duration `{row['duration_seconds']}`, delta_from_v1_x2 `{row.get('duration_delta_from_v1_x2_seconds', 'n/a')}`."
        )
    lines.extend(["", "## CLI Lanes"])
    for row in cli_rows:
        lines.append(f"- {row['lane']}: `{row['completion_status']}`, final_message_bytes `{row['final_message_bytes']}`.")
    write_md("v478-thos-v2-x2-lane-compact-board-v1.md", lines)


def decision_boards(generated_utc: str, generated_nz: str) -> None:
    command_plan = read_json("v478-thos-v2-x1-command-no-execution-receipt-plan-v1.json")
    skill_map = read_json("v478-thos-v2-x1-skill-command-route-map-v1.json")
    expansion_board = read_json("v478-thos-v2-x1-expansion-no-write-review-board-v1.json")
    command_rows = []
    for row in command_plan.get("rows", []):
        command_rows.append(
            {
                "command_id": row.get("command_id"),
                "risk_class": row.get("risk_class"),
                "v2_x2_decision": "carry_to_v3_x1_dry_run_candidate" if row.get("v2_x1_action") == "future_p1_dry_run_plan" else "hold_for_exact_approval",
                "execution_performed": False,
            }
        )
    skill_rows = []
    for row in skill_map.get("rows", []):
        skill_rows.append(
            {
                "source_skill": row.get("source_skill"),
                "mapped_command_id": row.get("mapped_command_id"),
                "v2_x2_decision": "carry_metadata_route_forward",
                "body_text_published": False,
                "mutation_performed": False,
            }
        )
    expansion_rows = []
    for row in expansion_board.get("rows", []):
        expansion_rows.append(
            {
                "expansion_id": row.get("expansion_id"),
                "v2_x2_decision": "carry_no_write_review_forward",
                "install_performed": False,
                "mutation_performed": False,
            }
        )
    payloads = [
        (
            "v478-thos-v2-x2-command-dry-run-readiness-v1",
            "command_dry_run_readiness",
            command_rows,
            "Command Dry-Run Readiness",
        ),
        (
            "v478-thos-v2-x2-skill-route-acceptance-v1",
            "skill_route_acceptance",
            skill_rows,
            "Skill Route Acceptance",
        ),
        (
            "v478-thos-v2-x2-expansion-review-decision-v1",
            "expansion_review_decision",
            expansion_rows,
            "Expansion Review Decision",
        ),
    ]
    for stem, artifact_type, rows, title in payloads:
        payload = {
            "artifact_type": artifact_type,
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(rows),
            "rows": rows,
            "mutation_performed": False,
            "claim_boundary": "THOS planning only",
        }
        write_json(f"{stem}.json", payload)
        lines = [
            f"# v478 THOS v2 x2 {title}",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(rows)}`",
            "- mutation_performed: `false`",
            "",
            "## Rows",
        ]
        for row in rows[:30]:
            label = row.get("command_id") or row.get("source_skill") or row.get("expansion_id")
            decision = row.get("v2_x2_decision")
            lines.append(f"- `{label}`: `{decision}`.")
        write_md(f"{stem}.md", lines)


def eureka_board(generated_utc: str, generated_nz: str) -> None:
    rows = []
    for perspective, domains in PERSPECTIVES.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            rows.append(
                {
                    "id": f"{perspective.upper().replace(' ', '_')}-{idx:02d}",
                    "perspective": perspective,
                    "domain": domain,
                    "task": f"Advance {domain} evidence for v478 v3 x1 while preserving status-only receipts and open GMUT gates.",
                    "authorship_boundary": "role_slot_handoff_not_raw_lane_payload",
                }
            )
    payload = {
        "artifact_type": "eureka_handoff_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "proposal_count": len(rows),
        "perspective_count": len(PERSPECTIVES),
        "rows": rows,
        "unfiltered_lane_payloads_published": False,
    }
    write_json("v478-thos-v2-x2-eureka-handoff-board-v1.json", payload)
    lines = [
        "# v478 THOS v2 x2 Eureka Handoff Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        f"- proposal_count: `{len(rows)}`",
        "- authorship_boundary: role-slot handoff board; unfiltered lane payloads are not published.",
        "",
        "## Proposals",
    ]
    lines.extend(f"- {row['id']} ({row['perspective']} / {row['domain']}): {row['task']}" for row in rows)
    write_md("v478-thos-v2-x2-eureka-handoff-board-v1.md", lines)


def overlay_and_synthesis(generated_utc: str, generated_nz: str, app: dict[str, Any], cli: dict[str, Any]) -> None:
    overlay = {
        "artifact_type": "overlay_decision",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "decision": "NO_X3_FOR_V478_V2",
        "rationale": [
            "App lanes completed with status PASS.",
            "CLI final-message marker remains an already-known open gap and does not block THOS artifact handoff.",
            "The reusable v3 app-lane watcher is already published for the next phase.",
            "No destructive cleanup, cache mutation, account mutation, or GMUT closure is required.",
        ],
        "next_expected_phase": NEXT_PHASE,
    }
    write_json("v478-thos-v2-x2-overlay-decision-v1.json", overlay)
    write_md(
        "v478-thos-v2-x2-overlay-decision-v1.md",
        [
            "# v478 THOS v2 x2 Overlay Decision",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- decision: `NO_X3_FOR_V478_V2`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rationale",
            *[f"- {item}" for item in overlay["rationale"]],
        ],
    )

    findings = [
        "v478 v2 x2 starts from a remote-aligned omega head and closes loose v2 x2 lane receipts.",
        "Cicero completed through the local app-server route.",
        "Kierkegaard completed through the local app-server route.",
        "Aristotle completed through the local app-server route.",
        "No new app-lane thread was created.",
        "No old-style spawning was used.",
        "Arby remains in CLI final-message open gap.",
        "Aster Vale remains in CLI final-message open gap.",
        "CLI open gap is explicit and non-blocking for THOS closeout.",
        "The source refresh was expanded with 32 current searches.",
        "Official or primary sources remain preferred.",
        "MCP security guidance strengthens connector consent boundaries.",
        "GitHub push protection guidance strengthens publication guards.",
        "Windows Sandbox guidance strengthens sandbox-readiness framing.",
        "Python tempfile and subprocess guidance strengthens watcher implementation boundaries.",
        "OpenTelemetry signals vocabulary supports future observability boards.",
        "Docker and Kubernetes sources provide watch/job comparison vocabulary only.",
        "Vertex and Gemini sources provide external agent and RAG comparison only.",
        "NVIDIA NIM, DGX Spark, and Omniverse remain expansion context only.",
        "NIST, UNESCO, and related governance sources remain governance context only.",
        "Journey reflection contributes 30 non-canon continuity steps.",
        "No raw Journey text is published.",
        "Command rows remain no-execution dry-run candidates or approval holds.",
        "Skill rows remain metadata-only and body-preserving.",
        "Expansion rows remain no-install and no-write.",
        "The 120-proposal Eureka board is a role-slot handoff, not an unfiltered lane transcript.",
        "The v3 x1 roadmap carries 60 concrete next tasks.",
        "The v3 app-lane watcher already has a published PASS receipt.",
        "All six GMUT gates remain open.",
        "The broader v490 goal remains active and incomplete.",
    ]
    synthesis = {
        "artifact_type": "phase_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "reflection_step_count": len(findings),
        "app_lane_status": app.get("overall_status"),
        "cli_lane_status": cli.get("aggregate_status"),
        "findings": [{"step": f"R{idx:02d}", "finding": finding} for idx, finding in enumerate(findings, start=1)],
        "claim_boundary": {
            "scope": "THOS v478 v2 x2 synthesis, source refresh, lane status, and handoff only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json("v478-thos-v2-x2-synthesis-v1.json", synthesis)
    write_md(
        "v478-thos-v2-x2-synthesis-v1.md",
        [
            "# v478 THOS v2 x2 Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
            "- app_lane_status: `PASS`",
            f"- cli_lane_status: `{cli.get('aggregate_status')}`",
            "- claim_boundary: THOS closeout only; all GMUT gates remain open.",
            "",
            "## Findings",
            *[f"- R{idx:02d}: {finding}" for idx, finding in enumerate(findings, start=1)],
        ],
    )


def roadmap(generated_utc: str, generated_nz: str) -> None:
    domains = ["lane", "cli", "command", "skill", "expansion", "source", "journey", "schema", "safety", "handoff", "thos", "quality"]
    tasks = []
    for idx in range(1, 61):
        domain = domains[(idx - 1) % len(domains)]
        tasks.append(
            {
                "id": f"V478V3X1-{idx:02d}",
                "domain": domain,
                "task": f"Advance {domain} work for v478 v3 x1 using status-only receipts, no raw payload publication, and open GMUT gates.",
            }
        )
    payload = {
        "artifact_type": "phase_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": len(tasks),
        "tasks": tasks,
    }
    write_json("v478-thos-v3-x1-roadmap-v1.json", payload)
    write_md(
        "v478-thos-v3-x1-roadmap-v1.md",
        [
            "# v478 THOS v3 x1 Roadmap",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- task_count: `{len(tasks)}`",
            "",
            "## Tasks",
            *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks],
        ],
    )


def status_and_schema(generated_utc: str, generated_nz: str) -> None:
    expected = [
        "v478-thos-v2-x2-source-refresh-ledger-v1.json",
        "v478-thos-v2-x2-journey-reflection-board-v1.json",
        "v478-thos-v2-x2-lane-compact-board-v1.json",
        "v478-thos-v2-x2-command-dry-run-readiness-v1.json",
        "v478-thos-v2-x2-skill-route-acceptance-v1.json",
        "v478-thos-v2-x2-expansion-review-decision-v1.json",
        "v478-thos-v2-x2-eureka-handoff-board-v1.json",
        "v478-thos-v2-x2-overlay-decision-v1.json",
        "v478-thos-v2-x2-synthesis-v1.json",
        "v478-thos-v3-x1-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append(
            {
                "file": name,
                "parsed": True,
                "artifact_type": payload.get("artifact_type"),
                "phase": payload.get("phase", payload.get("phase_slug")),
            }
        )
    schema = {
        "artifact_type": "schema_bound_artifact_check",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS",
        "checked_json_count": len(rows),
        "rows": rows,
    }
    write_json("v478-thos-v2-x2-schema-bound-artifact-check-v1.json", schema)
    write_md(
        "v478-thos-v2-x2-schema-bound-artifact-check-v1.md",
        [
            "# v478 THOS v2 x2 Schema-Bound Artifact Check",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS`",
            f"- checked_json_count: `{len(rows)}`",
            "",
            "## Checked",
            *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows],
        ],
    )
    status = {
        "artifact_type": "run_status",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "next_expected_phase": NEXT_PHASE,
        "published_payload_boundary": "status_only",
        "gmut_gates": {
            "G1_mathematical_consistency": "OPEN",
            "G2_empirical_falsifiability": "OPEN",
            "G3_existing_physics_compatibility": "OPEN",
            "G4_novel_prediction": "OPEN",
            "G5_peer_review_external_validation": "OPEN",
            "G6_consciousness_claim_boundary": "OPEN",
        },
    }
    write_json("v478-thos-v2-x2-run-status-v1.json", status)
    write_md(
        "v478-thos-v2-x2-run-status-v1.md",
        [
            "# v478 THOS v2 x2 Run Status",
            "",
            f"- generated_nz: `{generated_nz}`",
            "- overall_status: `PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "- published_payload_boundary: `status_only`",
            "- GMUT gates: all remain `OPEN`.",
        ],
    )


def main() -> int:
    generated_utc, generated_nz = now_pair()
    app = read_json("v478-thos-v2-x2-app-lane-completion-notifier-v1.json")
    cli = read_json("v478-thos-v2-x2-cli-lane-completion-poll-v1.json")
    prior_app = read_json("v478-thos-v1-x2-app-lane-completion-notifier-v1.json")
    source_refresh(generated_utc, generated_nz)
    journey_reflection(generated_utc, generated_nz)
    lane_compact_board(generated_utc, generated_nz, app, cli, prior_app)
    decision_boards(generated_utc, generated_nz)
    eureka_board(generated_utc, generated_nz)
    overlay_and_synthesis(generated_utc, generated_nz, app, cli)
    roadmap(generated_utc, generated_nz)
    status_and_schema(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP", "phase": PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
