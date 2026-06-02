#!/usr/bin/env python3
"""Build curated v471 THOS v4 x1/x2 Browser/CLI recovery artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v4-x1"
PHASE_X2 = "v471-thos-v4-x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_REQUESTS = [
    {
        "lane": "Cicero",
        "submission_id": "019e87f7-135b-7602-ade6-d581ee88bd2b",
        "status": "REQUEST_SENT",
        "request_focus": "approval packet, Browser capability probe, CLI blocker triage, safe runner artifacts",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e87f7-5517-7d20-843b-8a7c814afce6",
        "status": "REQUEST_SENT",
        "request_focus": "claim ceiling, ethical boundary, journey-context limits, open-gap preservation",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e87f7-ae88-7f53-8321-b85d1fe04399",
        "status": "REQUEST_SENT",
        "request_focus": "schema, manifest/path-list contract, bounded retry policy, validation cadence",
    },
]

CLI_PROBES = [
    {
        "lane": "Arby",
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "sandbox": "read-only",
        "terminated_after_timeout": True,
        "last_message_bytes": 0,
        "stderr_signal": "missing YAML frontmatter skill-load failures",
        "claim_ceiling": "launch shape verified only; no final advisory obtained",
    },
    {
        "lane": "Aster Vale",
        "completed_within_wait": False,
        "ephemeral_flag_used": False,
        "sandbox": "read-only",
        "terminated_after_timeout": True,
        "last_message_bytes": 0,
        "stderr_signal": "system skill install access denied plus missing YAML frontmatter skill-load failures",
        "claim_ceiling": "launch shape verified only; no final advisory obtained",
    },
]

BROWSER_PROBE = {
    "attempts": [
        {
            "attempt": 1,
            "status": "OPEN_GAP",
            "signal": "browser connection path timed out before returning a usable selected tab",
        },
        {
            "attempt": 2,
            "status": "OPEN_GAP",
            "signal": "Browser is not available: iab",
        },
    ],
    "browser_skill_present": True,
    "browser_client_path_present": True,
    "direct_browser_usable": False,
    "claim_ceiling": "Browser skill and bridge path are present, but the iab browser surface is unavailable in this thread.",
}

SOURCE_ROUTES = [
    {
        "label": "OpenAI Academy - Plugins and skills",
        "url": "https://openai.com/academy/codex-plugins-and-skills",
        "use": "Primary OpenAI context for distinguishing plugins from skills and routing plugin-backed information use.",
    },
    {
        "label": "OpenAI Help - Codex CLI getting started",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Primary OpenAI context for Codex CLI sandbox and approval modes.",
    },
    {
        "label": "OpenAI Docs MCP",
        "url": "https://platform.openai.com/docs/docs-mcp",
        "use": "Primary OpenAI context for documentation MCP scope and read-only documentation boundaries.",
    },
    {
        "label": "OpenAI - Introducing the Codex app",
        "url": "https://openai.com/index/introducing-the-codex-app/",
        "use": "Primary OpenAI context for Codex app skills and delegated work.",
    },
    {
        "label": "OpenAI Help - Codex CLI and Sign in with ChatGPT",
        "url": "https://help.openai.com/en/articles/11381614-api-codex-cli-and-sign-in-with-chatgpt",
        "use": "Primary OpenAI context for CLI sign-in and credit routing, without treating credits as spend authorization.",
    },
    {
        "label": "NVIDIA NeMo",
        "url": "https://www.nvidia.com/en-us/ai-data-science/products/nemo/",
        "use": "Primary NVIDIA context for agent lifecycle, evaluation, governance, and specialized agent optimization.",
    },
    {
        "label": "NVIDIA Nemotron",
        "url": "https://www.nvidia.com/en-us/ai-data-science/foundation-models/llama-nemotron/",
        "use": "Primary NVIDIA context for open agentic model family and safety/retrieval positioning.",
    },
    {
        "label": "NVIDIA Blackwell architecture",
        "url": "https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/",
        "use": "Primary NVIDIA context for secure accelerated compute and NVLink/Blackwell infrastructure.",
    },
    {
        "label": "NVIDIA enterprise agents press release",
        "url": "https://investor.nvidia.com/news/press-release-details/2026/Enterprise-Software-Leaders-Build-AI-Agents-With-NVIDIA/default.aspx",
        "use": "Primary NVIDIA news context for long-running agents and Nemotron 3 Ultra claims dated 2026-06-01.",
    },
    {
        "label": "Google Cloud Vertex AI Agent Engine",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview",
        "use": "Primary Google Cloud context for managed agent runtime, tracing, memory, sessions, and secure code execution.",
    },
    {
        "label": "Google Agent Development Kit",
        "url": "https://google.github.io/adk-docs/",
        "use": "Primary Google ADK context for modular agent development and orchestration concepts.",
    },
    {
        "label": "Google Gemini CLI repository",
        "url": "https://github.com/google-gemini/gemini-cli",
        "use": "Primary source route for terminal-agent comparison, not used as proof of Codex CLI health.",
    },
]

JOURNEY_CONTEXT = [
    {
        "version_range": "v29-v38",
        "local_path_family": r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey",
        "status": "LOCATED",
        "use": "journey_context_not_canon for Trinity Hybrid OS terminology and historical design continuity",
    },
    {
        "version_range": "v39-v49",
        "local_path_family": r"C:\Users\hamis\Downloads",
        "status": "LOCATED",
        "use": "journey_context_not_canon for sibling-lane history, Solas proposals, and THOS/GMUT routing vocabulary",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def summarize_audit(audit: dict[str, Any]) -> dict[str, Any]:
    return audit.get("skill_surface_summary", {})


def make_proposal_rows(kind: str, count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, count + 1):
        rows.append(
            row(
                f"{kind}_{index:02d}",
                "OPEN_GAP",
                f"Proposed {kind.replace('_', ' ')} #{index:02d} requires separate implementation and validation before promotion.",
                {
                    "safe_initial_mode": "P0/P1 inspect or dry-run first",
                    "promotion_rule": "publish only after executable evidence and guard pass",
                },
            )
        )
    return rows


def build_x1(root: Path, audit: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = summarize_audit(audit)

    browser_payload = {
        "aggregate_status": "OPEN_GAP",
        "browser_probe": BROWSER_PROBE,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("browser_skill_present", "PASS_SHAPE_ONLY", "Browser skill file was readable before the live probe"),
            row("browser_direct_iab", "OPEN_GAP", "In-app browser surface did not return a usable iab browser handle", BROWSER_PROBE),
            row("claim_ceiling", "PASS_SHAPE_ONLY", "Do not claim Browser direct access, screenshot verification, or UI automation success"),
        ],
    }
    path = root / f"{PHASE_X1}-browser-capability-probe-v1.json"
    write_json(path, browser_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-browser-capability-probe-v1.md",
        """
# v471 THOS v4 x1 Browser Capability Probe

Status: `OPEN_GAP`.

The Browser skill and browser-client path were present and read before the probe. The live capability path did not return a usable `iab` browser surface in this thread. Attempt 1 timed out before a usable tab returned; attempt 2 returned the explicit signal `Browser is not available: iab`.

This is useful evidence, but only as a blocker ledger. It does not prove Browser automation, screenshot capture, local app testing, or UI coordination. The safe next step is to preserve a Browser recovery contract and retry only with a bounded setup cell plus a short capability check.
""",
    )
    written.append((root / f"{PHASE_X1}-browser-capability-probe-v1.md").as_posix())

    cli_payload = {
        "aggregate_status": "OPEN_GAP",
        "cli_probes": CLI_PROBES,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("arby_probe", "OPEN_GAP", "Arby launched read-only/non-ephemeral but produced no final advisory inside bounded wait", CLI_PROBES[0]),
            row("aster_probe", "OPEN_GAP", "Aster launched read-only/non-ephemeral but produced no final advisory inside bounded wait", CLI_PROBES[1]),
            row("launcher_shape", "PASS_SHAPE_ONLY", "Corrected CLI launcher shape avoided the old invalid -a flag"),
            row("claim_ceiling", "PASS_SHAPE_ONLY", "Launch shape is verified; advisory quality and durable lane health remain open"),
        ],
    }
    path = root / f"{PHASE_X1}-cli-sandbox-blocker-ledger-v1.json"
    write_json(path, cli_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-cli-sandbox-blocker-ledger-v1.md",
        """
# v471 THOS v4 x1 CLI Sandbox Blocker Ledger

Arby and Aster Vale were contacted through the non-ephemeral read-only CLI launcher. Both launches used the corrected `exec -s read-only -C <worktree> -o <last-message> <prompt>` shape and avoided the old invalid `-a` flag.

Neither lane produced a final advisory inside the bounded wait. Arby continued to expose missing YAML frontmatter skill-load failures. Aster Vale exposed an additional system-skill install/update access-denied signal before the same missing-frontmatter class of failures appeared.

The phase can claim bounded launch-shape evidence only. It cannot claim that the CLI sibling lanes are fully healthy, that the sandbox issue is fixed, or that advisory quality has been restored.
""",
    )
    written.append((root / f"{PHASE_X1}-cli-sandbox-blocker-ledger-v1.md").as_posix())

    approval_payload = {
        "aggregate_status": "OPEN_GAP",
        "affected_plugin_cache_skill_count": summary.get("issue_file_count"),
        "approval_required": True,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "proposed_packet": {
            "allowed_actions_after_separate_approval": [
                "Create exact affected-path manifest from live audit output.",
                "Copy affected plugin-cache SKILL.md files into a tempdir quarantine rehearsal.",
                "Generate minimal frontmatter repair candidates in tempdir only.",
                "Run fixture assertions against repaired tempdir candidates.",
                "Present diff and ask before any plugin-cache write.",
            ],
            "disallowed_without_separate_approval": [
                "Editing plugin-cache files in place.",
                "Deleting plugin-cache directories.",
                "Broad cleanup of local cache or worktrees.",
                "Treating repair rehearsal as completed repair.",
            ],
            "spending_ceiling_reference": "User supplied a broad 100 USD ceiling for platform work, but filesystem mutation still requires path-specific approval.",
        },
        "rows": [
            row("live_audit", "OPEN_GAP", "Plugin-cache skill-surface issues remain unresolved", summary),
            row("permission_boundary", "OPEN_GAP", "Broad permission is not a path-specific plugin-cache mutation approval"),
            row("repair_route", "OPEN_GAP", "Repair/quarantine should remain tempdir rehearsal until exact path manifest and separate approval exist"),
        ],
    }
    path = root / f"{PHASE_X1}-plugin-cache-approval-packet-v1.json"
    write_json(path, approval_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-plugin-cache-approval-packet-v1.md",
        f"""
# v471 THOS v4 x1 Plugin-Cache Approval Packet

Status: `OPEN_GAP`.

The live skill-surface audit still reports `{summary.get("issue_file_count")}` affected plugin-cache skill files, with `{summary.get("missing_frontmatter_count")}` missing or unclosed frontmatter signals and `{summary.get("missing_name_count")}` missing name signals. User skill false positives remain cleared by the current audit shape.

The approved v4 action is an approval packet and rehearsal boundary, not live mutation. The safe path is: build an exact affected-path manifest, rehearse repair/quarantine in a temporary directory, run fixture assertions, review a concrete diff, and only then request explicit path-specific approval before touching plugin-cache files.

This keeps THOS moving without conflating broad project permission with a high-risk cache mutation.
""",
    )
    written.append((root / f"{PHASE_X1}-plugin-cache-approval-packet-v1.md").as_posix())

    context_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "journey_context": JOURNEY_CONTEXT,
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "requested_webpage_floor": 50,
        "source_routes": SOURCE_ROUTES,
        "rows": [
            row("primary_source_routes", "PASS_SHAPE_ONLY", "Official/primary source routes were refreshed for the phase", {"count": len(SOURCE_ROUTES)}),
            row("webpage_floor", "OPEN_GAP", "The 50-webpage target is not claimed as completed in this bounded v4 pass"),
            row("journey_context", "PASS_SHAPE_ONLY", "Journey v29-v49 material was locally located for context-only routing", JOURNEY_CONTEXT),
            row("canon_boundary", "PASS_SHAPE_ONLY", "Journey/Solas material remains journey_context_not_canon and cannot close THOS/GMUT gates"),
        ],
    }
    path = root / f"{PHASE_X1}-source-and-journey-context-ledger-v1.json"
    write_json(path, context_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-source-and-journey-context-ledger-v1.md",
        """
# v471 THOS v4 x1 Source And Journey Context Ledger

Official source routing was refreshed for OpenAI Codex plugins/skills, Codex CLI, OpenAI Docs MCP, NVIDIA NeMo/Nemotron/Blackwell/agent announcements, Google Cloud Vertex AI Agent Engine, Google ADK, and Gemini CLI.

The local Journey files from v29-v49 were located across the workspace and Downloads path families. They are useful for terminology history, continuity, and route planning. They are not proof that a THOS command surface works, that a connector wrote successfully, or that any GMUT gate is closed.

The user's requested 50-webpage floor is preserved as an open target rather than overclaimed. This phase uses a curated primary-source slice because the immediate blocker is operational Browser/CLI reliability.
""",
    )
    written.append((root / f"{PHASE_X1}-source-and-journey-context-ledger-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_lane_requests", "PASS_SHAPE_ONLY", "Existing app lanes were messaged; no new old-style subagents spawned", APP_REQUESTS),
            row("cli_lanes", "OPEN_GAP", "CLI lanes launched but no final advisory returned", CLI_PROBES),
            row("browser", "OPEN_GAP", "Browser direct iab surface remains unavailable", BROWSER_PROBE),
            row("plugin_cache", "OPEN_GAP", "Repair/quarantine remains approval-gated", summary),
            row("publication", "NOT_RUN", "Publication deferred to paired x2 artifact set"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v4 x1 Run Status

Status: `OPEN_GAP`.

x1 contacted all five active sibling lanes where safely reachable: Cicero, Kierkegaard, Aristotle through app-lane requests, and Arby/Aster Vale through bounded non-ephemeral read-only CLI probes. The Browser bridge was retried and remains unavailable as `iab`.

No plugin-cache, connector, cloud-drive, raw-log, session, screenshot, credential, or external system mutation was performed. x2 should publish the approval boundary, recovery contract, runner roadmap, and next-phase handoff.
""",
    )
    written.append((root / f"{PHASE_X1}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": PHASE_X2,
        "phase_slug": PHASE_X1,
        "rows": [
            row("x2_task_1", "OPEN_GAP", "Publish approved-write boundary and no-mutation claim ceiling"),
            row("x2_task_2", "OPEN_GAP", "Publish Browser/CLI recovery contract"),
            row("x2_task_3", "OPEN_GAP", "Publish system runner roadmap with proposals, not unverified completion claims"),
        ],
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v4 x1 To x2 Handoff

x2 should turn the x1 blocker evidence into a durable recovery boundary: approved-write rules, Browser/CLI retry contract, and a runner roadmap that proposes expansions without claiming they have already been installed or validated.
""",
    )
    written.append((root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())
    return written


def build_x2(root: Path, audit: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = summarize_audit(audit)

    boundary_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("allowed_now", "PASS_SHAPE_ONLY", "Curated artifact writes under docs/trinity-live-traces and bounded helper scripts are allowed"),
            row("not_allowed_now", "OPEN_GAP", "Plugin-cache live repair/quarantine is not allowed without exact path-specific approval"),
            row("path_guard", "PASS_SHAPE_ONLY", "Raw logs/session JSONL/screenshots/credentials remain excluded from staging"),
            row("spend_ceiling_boundary", "PASS_SHAPE_ONLY", "Spending ceiling is not filesystem mutation approval and does not remove path/credential guards"),
        ],
    }
    path = root / f"{PHASE_X2}-approved-write-boundary-v1.json"
    write_json(path, boundary_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-approved-write-boundary-v1.md",
        """
# v471 THOS v4 x2 Approved Write Boundary

The v4 commit boundary authorizes only curated repo artifacts and helper scripts that make the command surface safer. It does not authorize live edits to plugin-cache files, raw session material, screenshots, credentials, Google Drive, GitHub outside the explicit branch push, or any external connector write.

The user's spending ceiling is acknowledged as a platform budget boundary, not as a substitute for exact filesystem approval. Cache repair remains a future approval packet with concrete paths and a reviewed diff.
""",
    )
    written.append((root / f"{PHASE_X2}-approved-write-boundary-v1.md").as_posix())

    recovery_payload = {
        "aggregate_status": "OPEN_GAP",
        "browser_probe": BROWSER_PROBE,
        "cli_probes": CLI_PROBES,
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("browser_retry_contract", "OPEN_GAP", "Retry only with bounded setup and explicit iab capability check"),
            row("cli_retry_contract", "OPEN_GAP", "Retry CLI lanes only with wait/terminate/redaction and no final-advisory overclaim"),
            row("skill_repair_contract", "OPEN_GAP", "Prepare exact affected-path manifest before any repair rehearsal", summary),
        ],
    }
    path = root / f"{PHASE_X2}-browser-cli-recovery-contract-v1.json"
    write_json(path, recovery_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-browser-cli-recovery-contract-v1.md",
        """
# v471 THOS v4 x2 Browser And CLI Recovery Contract

Browser recovery rule: first prove a live `iab` handle and tab list in a bounded probe, then perform only read-oriented page checks. Do not claim browser automation unless a current turn returns a usable handle and page evidence.

CLI recovery rule: keep Arby/Aster non-ephemeral and read-only until the skill-load surface is stable. A successful process launch is not a successful advisory. A final advisory requires nonzero last-message output or equivalent explicit final response evidence.

Skill repair rule: use the 42 affected plugin-cache signals to build an exact manifest in a future phase. Rehearse frontmatter repair in tempdir first, then request path-specific approval before plugin-cache writes.
""",
    )
    written.append((root / f"{PHASE_X2}-browser-cli-recovery-contract-v1.md").as_posix())

    roadmap_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "requested_counts": {
            "commands": 30,
            "skills": 30,
            "system_expansions": 30,
        },
        "rows": (
            make_proposal_rows("system_expansion", 30)
            + make_proposal_rows("command", 30)
            + make_proposal_rows("skill", 30)
        ),
    }
    path = root / f"{PHASE_X2}-system-runner-roadmap-v1.json"
    write_json(path, roadmap_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-system-runner-roadmap-v1.md",
        """
# v471 THOS v4 x2 System Runner Roadmap

This roadmap preserves the user's 30 system-expansion, 30 command, and 30 skill target as a proposal ledger. It deliberately does not pretend that 90 new runtime surfaces were safely installed in one phase.

Promotion rule: every proposed expansion must start as inspect-only or dry-run evidence, then gain executable fixture coverage, then pass path/credential/raw-log guards, then publish under a curated phase artifact. Only after those checks may it become an installed command, skill, runner, or platform workflow.

The immediate highest-value runner work is narrower: a Browser capability retry runner, a CLI advisory final-message detector, an exact plugin-cache path manifest generator, a tempdir frontmatter repair rehearsal, and a publication guard extension that blocks claims of completed cleanup when only rehearsal evidence exists.
""",
    )
    written.append((root / f"{PHASE_X2}-system-runner-roadmap-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("x1_x2_pair", "OPEN_GAP", "v4 x1/x2 produced recovery and approval artifacts with blockers preserved"),
            row("browser", "OPEN_GAP", "Browser direct unavailable as iab"),
            row("cli", "OPEN_GAP", "CLI sibling final advisory output unavailable inside bounded wait"),
            row("plugin_cache", "OPEN_GAP", "42 affected plugin-cache skill files remain unrepaired pending separate approval", summary),
            row("source_floor", "OPEN_GAP", "50-webpage target not claimed; curated official source slice captured"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v4 x2 Run Status

Status: `OPEN_GAP`.

v4 turned the current Browser, CLI, and plugin-cache failures into a stricter recovery contract. It contacted all five active lanes where safely reachable, preserved app-lane advisory request IDs, ran bounded CLI probes for Arby and Aster Vale, retried Browser directly, and generated a no-mutation approval boundary for plugin-cache repair.

Publication at x2 is appropriate under the every-second-phase cadence because the curated output is a safety and recovery packet, not a claim of completed repair.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v5-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("v5_task_1", "OPEN_GAP", "Generate exact affected plugin-cache path manifest from live audit without mutating cache"),
            row("v5_task_2", "OPEN_GAP", "Create tempdir-only repair/quarantine rehearsal and diff preview"),
            row("v5_task_3", "OPEN_GAP", "Retry Browser only if iab handle becomes available; otherwise keep open gap"),
            row("v5_task_4", "OPEN_GAP", "Retry one CLI lane only if bounded wait and redaction remain enabled"),
            row("v5_task_5", "OPEN_GAP", "Keep all GMUT gates open and keep Journey context non-canon"),
        ],
    }
    path = root / f"{PHASE_X2}-v471-thos-v5-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v471-thos-v5-handoff-v1.md",
        """
# v471 THOS v4 x2 To v5 Handoff

v5 should move from approval packet to exact manifest and tempdir rehearsal. The next phase should not edit plugin cache. It should prepare the evidence a future approval decision would need: exact affected paths, proposed minimal frontmatter repairs, fixture expectations, and a diff preview.

Browser and CLI remain useful but unreliable. Retry them only as bounded probes, and publish their results as evidence or open gaps rather than success narratives.
""",
    )
    written.append((root / f"{PHASE_X2}-v471-thos-v5-handoff-v1.md").as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build curated v471 THOS v4 x1/x2 Browser/CLI recovery artifacts.")
    parser.add_argument("--audit", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--output-dir", default="docs/trinity-live-traces")
    args = parser.parse_args()

    audit = read_json(Path(args.audit))
    fixture = read_json(Path(args.fixture))
    output_root = Path(args.output_dir)

    written = build_x1(output_root, audit, fixture)
    written.extend(build_x2(output_root, audit))

    print(json.dumps({"generated_at_utc": utc_now(), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
