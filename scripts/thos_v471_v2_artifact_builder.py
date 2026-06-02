#!/usr/bin/env python3
"""Build curated v471 THOS v2 x1/x2 skill-surface repair artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v2-x1"
PHASE_X2 = "v471-thos-v2-x2"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

APP_SIBLINGS = [
    {
        "lane": "Cicero",
        "submission_id": "019e87da-2367-7400-ad59-36230bcac8ed",
        "summary": "Requested command-surface inventory fields, frontmatter contracts, quarantine criteria, and strict non-mutating validation rows.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e87da-661f-7e33-8b0b-5645370c3ac3",
        "summary": "Separated visibility, loadability, usability, approval, and mutation authority; advised classify/isolate before editing.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e87da-b9bf-7e60-9b28-f7c75d64246e",
        "summary": "Provided validator schema, expected-negative fixtures, and x2 publication-guard reason codes.",
    },
]

SOURCE_SEEDS = [
    {
        "label": "OpenAI Codex CLI help article",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Codex CLI sandbox/autonomy context",
    },
    {
        "label": "OpenAI Academy plugins and skills",
        "url": "https://openai.com/academy/codex-plugins-and-skills",
        "use": "Codex plugin/skill concept context",
    },
    {
        "label": "OpenAI Codex skill creator sample",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md",
        "use": "Frontmatter name/description contract context",
    },
    {
        "label": "OpenAI Docs MCP",
        "url": "https://platform.openai.com/docs/docs-mcp",
        "use": "Official docs-routing context",
    },
    {
        "label": "OpenAI MCP guide",
        "url": "https://platform.openai.com/docs/mcp/",
        "use": "MCP tool/data source and prompt-injection caution context",
    },
    {
        "label": "OpenAI Computer Use guide",
        "url": "https://platform.openai.com/docs/guides/tools-computer-use",
        "use": "Computer-use tool boundary context",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {"evidence": evidence, "message": message, "row_id": row_id, "status": status}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"missing": True}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def probe_status(probe: dict[str, Any]) -> str:
    if probe.get("missing"):
        return "NOT_RUN"
    if probe.get("completed_within_wait") is True and probe.get("last_message_bytes", 0) > 0:
        return "PASS_SHAPE_ONLY"
    return "OPEN_GAP"


def build_x1(root: Path, audit: dict[str, Any], arby_probe: dict[str, Any], aster_probe: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = audit.get("skill_surface_summary", {})
    write_md(
        root / f"{PHASE_X1}-skill-surface-audit-v1.md",
        f"""
# v471 THOS v2 x1 Skill-Surface Audit

Phase: `{PHASE_X1}`

Aggregate status: `{audit.get("aggregate_status")}`

The live scan found `{summary.get("total_skill_files")}` skill files: `{summary.get("root_counts", {}).get("user_skills")}` user skills and `{summary.get("root_counts", {}).get("plugin_cache")}` plugin-cache skills.

Current affected unique skill files: `{summary.get("issue_file_count")}`. The remaining affected set is plugin-cache frontmatter/name absence, not the six user-skill files that were false positives before the BOM-aware scan.

No skill files were edited, deleted, renamed, or quarantined in this phase.
""",
    )
    written.append((root / f"{PHASE_X1}-skill-surface-audit-v1.md").as_posix())

    probe_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("arby_bounded_probe", probe_status(arby_probe), "Arby CLI probe was bounded and summarized", arby_probe),
            row("aster_bounded_probe", probe_status(aster_probe), "Aster Vale CLI probe was bounded and summarized", aster_probe),
            row("process_containment", "PASS_SHAPE_ONLY", "Probe launcher used wait and terminate-on-timeout controls"),
        ],
    }
    path = root / f"{PHASE_X1}-cli-bounded-probe-ledger-v1.json"
    write_json(path, probe_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-cli-bounded-probe-ledger-v1.md",
        """
# v471 THOS v2 x1 CLI Bounded Probe Ledger

The CLI lanes were probed through the safe launcher with read-only sandbox, non-ephemeral execution, bounded wait, and timeout termination.

Arby still surfaced skill-load errors and did not produce final advisory text inside the wait window. Aster Vale produced only startup warning/noise but also did not produce final advisory text inside the wait window.

The probe confirms process containment works; it does not prove CLI advisory reliability is restored.
""",
    )
    written.append((root / f"{PHASE_X1}-cli-bounded-probe-ledger-v1.md").as_posix())

    sibling_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_sibling_advisory", "PASS_SHAPE_ONLY", "Three existing app siblings returned v2 advisory reports", APP_SIBLINGS),
            row("old_subagent_spawn", "PASS_SHAPE_ONLY", "No new old-style subagents were spawned"),
        ],
    }
    path = root / f"{PHASE_X1}-sibling-advisory-ledger-v1.json"
    write_json(path, sibling_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-sibling-advisory-ledger-v1.md",
        """
# v471 THOS v2 x1 Sibling Advisory Ledger

Cicero, Kierkegaard, and Aristotle returned advisory-only guidance for the skill-surface repair/quarantine lane.

No new old-style subagents were spawned.
""",
    )
    written.append((root / f"{PHASE_X1}-sibling-advisory-ledger-v1.md").as_posix())

    source_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("official_source_routes", "PASS_SHAPE_ONLY", "Official/source routes were gathered for Codex CLI, plugins/skills, MCP, and computer-use context", SOURCE_SEEDS),
            row("fifty_page_request", "OPEN_GAP", "This v2 blocker repair pass did not complete a fifty-page study; source routing is scoped and explicit"),
        ],
    }
    path = root / f"{PHASE_X1}-source-routing-ledger-v1.json"
    write_json(path, source_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-source-routing-ledger-v1.md",
        """
# v471 THOS v2 x1 Source Routing Ledger

Official/source routing was refreshed for Codex CLI, plugins/skills, MCP, and computer-use context.

This artifact does not claim a full fifty-page study for v2. It records source routes relevant to the blocker being repaired.
""",
    )
    written.append((root / f"{PHASE_X1}-source-routing-ledger-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("phase_status", "OPEN_GAP", "x1 collected skill-surface and bounded-probe evidence"),
            row("publication", "NOT_RUN", "Publication deferred to paired x2 under the every-second-phase cadence"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open"),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v2 x1 Run Status

Status: local evidence phase with open gaps.

x1 produced skill-surface, bounded CLI probe, sibling advisory, source routing, and x2 handoff evidence. Publication is deferred to x2.

All six GMUT gates remain open.
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
            row("x2_task_1", "OPEN_GAP", "Publish repair/quarantine decision ledger for plugin-cache skill surfaces"),
            row("x2_task_2", "OPEN_GAP", "Publish bounded runner contract for future Arby/Aster CLI advisory attempts"),
            row("x2_task_3", "OPEN_GAP", "Carry Browser direct tool and accessibility execution as open gaps"),
        ],
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v2 x1 To x2 Handoff

x2 should publish the repair/quarantine decision ledger and bounded runner contract.

Do not edit plugin cache or skill files from this phase. Keep the action as scoped evidence and guard design.
""",
    )
    written.append((root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())
    return written


def build_x2(root: Path, audit: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = audit.get("skill_surface_summary", {})
    decision_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("user_skill_status", "PASS_SHAPE_ONLY", "User skill frontmatter false positives were cleared by the BOM-aware scan", {"user_skill_count": summary.get("root_counts", {}).get("user_skills")}),
            row("plugin_cache_quarantine_candidate", "OPEN_GAP", "Plugin-cache skills with missing frontmatter/name remain quarantine candidates, not edited files", {"affected_plugin_skill_files": summary.get("issue_file_count")}),
            row("repair_authority", "OPEN_GAP", "No plugin cache repair is performed without a separate approved write scope and rollback plan"),
        ],
    }
    path = root / f"{PHASE_X2}-repair-quarantine-decision-ledger-v1.json"
    write_json(path, decision_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-repair-quarantine-decision-ledger-v1.md",
        f"""
# v471 THOS v2 x2 Repair And Quarantine Decision Ledger

The BOM-aware scan clears the six user-skill false positives and identifies `{summary.get("issue_file_count")}` plugin-cache skill files as repair/quarantine candidates.

Decision: do not mutate plugin cache in this phase. Treat affected plugin-cache skills as `OPEN_GAP` until a separate write-approved repair or quarantine plan exists.
""",
    )
    written.append((root / f"{PHASE_X2}-repair-quarantine-decision-ledger-v1.md").as_posix())

    runner_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("read_only_non_ephemeral", "PASS_SHAPE_ONLY", "Launcher preserves read-only sandbox and no ephemeral flag"),
            row("bounded_wait", "PASS_SHAPE_ONLY", "Launcher supports wait-seconds and terminate-on-timeout"),
            row("advisory_reliability", "OPEN_GAP", "Bounded probe did not produce final advisory text in the wait window"),
        ],
    }
    path = root / f"{PHASE_X2}-bounded-runner-contract-v1.json"
    write_json(path, runner_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-bounded-runner-contract-v1.md",
        """
# v471 THOS v2 x2 Bounded Runner Contract

Future CLI advisory attempts should use read-only sandbox, non-ephemeral execution, a bounded wait, timeout termination, redacted output summaries, and no raw temp log staging.

This contract proves containment shape, not advisory reliability.
""",
    )
    written.append((root / f"{PHASE_X2}-bounded-runner-contract-v1.md").as_posix())

    guard_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("reason_codes", "PASS_SHAPE_ONLY", "Reason codes defined for next validator expansion", ["FRONTMATTER_MISSING", "FRONTMATTER_MALFORMED", "REQUIRED_KEY_MISSING", "SKILL_NAME_OVERLONG", "TOOL_SURFACE_UNAVAILABLE", "BOUNDED_PROBE_TIMEOUT"]),
            row("expected_negative_fixtures", "OPEN_GAP", "Expected-negative fixtures are specified by Aristotle but not yet executable validator fixtures"),
            row("browser_gap", "OPEN_GAP", "Direct Browser navigation/screenshot remains unavailable through callable tools"),
        ],
    }
    path = root / f"{PHASE_X2}-publication-guard-additions-v1.json"
    write_json(path, guard_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-publication-guard-additions-v1.md",
        """
# v471 THOS v2 x2 Publication Guard Additions

Next validator work should add reason codes for missing frontmatter, malformed frontmatter, missing required keys, overlong skill names, unavailable tool surfaces, and bounded probe timeouts.

The expected-negative fixture design is advisory-ready but not executable yet.
""",
    )
    written.append((root / f"{PHASE_X2}-publication-guard-additions-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v3-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("paired_publication_scope", "PASS_SHAPE_ONLY", "x1 and x2 artifacts are ready for paired validation and curated staging"),
            row("plugin_cache_gap", "OPEN_GAP", "Plugin-cache skill repair/quarantine remains unresolved"),
            row("cli_gap", "OPEN_GAP", "CLI advisory content did not complete inside bounded probes"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open"),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v2 x2 Run Status

Status: paired publication candidate with open gaps.

v2 turns the previous CLI stderr flood into a bounded runner contract and a plugin-cache repair/quarantine ledger. It does not mutate skills, repair plugin cache, claim Browser control, or prove CLI advisory reliability.

All six GMUT gates remain open.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v3-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("next_task_1", "OPEN_GAP", "Build executable expected-negative skill-surface fixtures"),
            row("next_task_2", "OPEN_GAP", "Decide whether plugin-cache repair/quarantine needs separate live-write approval"),
            row("next_task_3", "OPEN_GAP", "Keep Arby/Aster advisory retries bounded until final message output is proven"),
            row("next_task_4", "OPEN_GAP", "Keep all GMUT gates open"),
        ],
    }
    path = root / f"{PHASE_X2}-v471-thos-v3-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v471-thos-v3-handoff-v1.md",
        """
# v471 THOS v2 x2 To v3 Handoff

v3 should convert the guard additions into executable expected-negative fixtures and decide whether plugin-cache repair/quarantine needs a separate approved live-write plan.

Keep CLI advisory retries bounded and keep all GMUT gates open.
""",
    )
    written.append((root / f"{PHASE_X2}-v471-thos-v3-handoff-v1.md").as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS v2 curated artifacts.")
    parser.add_argument("--artifact-root", default="docs/trinity-live-traces")
    parser.add_argument("--audit-json", required=True)
    parser.add_argument("--arby-probe-json", required=True)
    parser.add_argument("--aster-probe-json", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    audit = read_json(Path(args.audit_json))
    arby_probe = read_json(Path(args.arby_probe_json))
    aster_probe = read_json(Path(args.aster_probe_json))
    written = build_x1(root, audit, arby_probe, aster_probe)
    written.extend(build_x2(root, audit))
    print(json.dumps({"generated_at_utc": utc_now(), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
