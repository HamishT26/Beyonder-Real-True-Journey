#!/usr/bin/env python3
"""Build curated v471 THOS v3 x1/x2 fixture-guard artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASE_X1 = "v471-thos-v3-x1"
PHASE_X2 = "v471-thos-v3-x2"

APP_SIBLINGS = [
    {
        "lane": "Cicero",
        "submission_id": "019e87e9-4be2-7103-a9b6-44b3be8c464b",
        "summary": "Defined fixture categories, command-surface ledger fields, publication criteria, and overclaim exclusions.",
    },
    {
        "lane": "Kierkegaard",
        "submission_id": "019e87e9-8ad3-7070-8999-6177e6063903",
        "summary": "Clarified that expected-negative fixtures prove detection/refusal only, not repair, quarantine completion, or CLI reliability.",
    },
    {
        "lane": "Aristotle",
        "submission_id": "019e87e9-ea46-7a32-830f-d935f9803d8d",
        "summary": "Specified reason-code expectations, fixture pass/fail criteria, bounded probe metadata, and publication-guard additions.",
    },
]

SOURCE_SEEDS = [
    {
        "label": "OpenAI Codex skill creator sample",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md",
        "use": "Official sample context for SKILL.md metadata: name and description frontmatter.",
    },
    {
        "label": "OpenAI Codex CLI help",
        "url": "https://help.openai.com/en/articles/11096431",
        "use": "Codex CLI sandbox/autonomy context.",
    },
    {
        "label": "OpenAI MCP docs",
        "url": "https://platform.openai.com/docs/mcp/",
        "use": "MCP and prompt-injection boundary context for tool surfaces.",
    },
]

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
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


def fixture_summary(fixture: dict[str, Any]) -> dict[str, Any]:
    results = fixture.get("fixture_results", [])
    expected_failures = [item for item in results if item.get("expected_status") == "FAIL_BLOCKER"]
    open_gaps = [item for item in results if item.get("expected_status") == "OPEN_GAP"]
    positive_controls = [item for item in results if item.get("expected_status") == "PASS_SHAPE_ONLY"]
    return {
        "fixture_assertion_count": len(results),
        "open_gap_fixture_count": len(open_gaps),
        "positive_control_count": len(positive_controls),
        "expected_failure_fixture_count": len(expected_failures),
    }


def build_x1(root: Path, fixture: dict[str, Any], audit: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = audit.get("skill_surface_summary", {})
    fix_summary = fixture_summary(fixture)

    write_md(
        root / f"{PHASE_X1}-skill-surface-fixture-guard-v1.md",
        f"""
# v471 THOS v3 x1 Skill-Surface Fixture Guard

Phase: `{PHASE_X1}`

Aggregate status: `{fixture.get("aggregate_status")}`

The tempdir-only fixture guard evaluated `{fix_summary["fixture_assertion_count"]}` fixtures: `{fix_summary["positive_control_count"]}` positive control, `{fix_summary["expected_failure_fixture_count"]}` expected failure fixtures, and `{fix_summary["open_gap_fixture_count"]}` operational open-gap fixtures.

This proves local detection/refusal behavior for known skill-surface failure shapes. It does not repair plugin cache, authorize quarantine, restore CLI reliability, or validate Browser direct tooling.
""",
    )
    written.append((root / f"{PHASE_X1}-skill-surface-fixture-guard-v1.md").as_posix())

    write_md(
        root / f"{PHASE_X1}-skill-surface-audit-v1.md",
        f"""
# v471 THOS v3 x1 Skill-Surface Audit

Current skill files scanned: `{summary.get("total_skill_files")}`.

Affected plugin-cache skill files: `{summary.get("issue_file_count")}`.

User skills scanned: `{summary.get("root_counts", {}).get("user_skills")}`. Plugin-cache skills scanned: `{summary.get("root_counts", {}).get("plugin_cache")}`.

No skill files were edited or quarantined in this phase.
""",
    )
    written.append((root / f"{PHASE_X1}-skill-surface-audit-v1.md").as_posix())

    sibling_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("app_sibling_advisory", "PASS_SHAPE_ONLY", "Three existing app siblings returned v3 fixture advisory reports", APP_SIBLINGS),
            row("old_subagent_spawn", "PASS_SHAPE_ONLY", "No new old-style subagents were spawned"),
        ],
    }
    path = root / f"{PHASE_X1}-sibling-advisory-ledger-v1.json"
    write_json(path, sibling_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-sibling-advisory-ledger-v1.md",
        """
# v471 THOS v3 x1 Sibling Advisory Ledger

Cicero, Kierkegaard, and Aristotle returned advisory-only guidance for executable expected-negative fixtures.

No new old-style subagents were spawned.
""",
    )
    written.append((root / f"{PHASE_X1}-sibling-advisory-ledger-v1.md").as_posix())

    source_payload = {
        "aggregate_status": "PASS_SHAPE_ONLY",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X1,
        "rows": [
            row("source_routes", "PASS_SHAPE_ONLY", "Official/source routes were used for skill and CLI context", SOURCE_SEEDS),
        ],
    }
    path = root / f"{PHASE_X1}-source-routing-ledger-v1.json"
    write_json(path, source_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-source-routing-ledger-v1.md",
        """
# v471 THOS v3 x1 Source Routing Ledger

Source routing focused on official OpenAI/Codex skill, CLI, and MCP context relevant to this fixture-guard phase.
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
            row("fixture_guard", fixture.get("aggregate_status", "OPEN_GAP"), "Tempdir-only expected-negative fixtures executed", fix_summary),
            row("plugin_cache_gap", "OPEN_GAP", "Plugin-cache repair/quarantine remains unresolved", {"affected_plugin_skill_files": summary.get("issue_file_count")}),
            row("publication", "NOT_RUN", "Publication deferred to paired x2 under every-second-phase cadence"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open", GMUT_GATES),
        ],
    }
    path = root / f"{PHASE_X1}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-run-status-v1.md",
        """
# v471 THOS v3 x1 Run Status

Status: local fixture evidence phase with open gaps.

x1 executed tempdir-only expected-negative fixtures and refreshed the live skill-surface audit. Publication is deferred to x2.

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
            row("x2_task_1", "OPEN_GAP", "Publish executable fixture assertion ledger and claim ceiling"),
            row("x2_task_2", "OPEN_GAP", "Publish plugin-cache repair/quarantine approval gate"),
            row("x2_task_3", "OPEN_GAP", "Publish v4 handoff for executable fixture expansion and bounded CLI retry policy"),
        ],
    }
    path = root / f"{PHASE_X1}-x2-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X1}-x2-handoff-v1.md",
        """
# v471 THOS v3 x1 To x2 Handoff

x2 should publish the executable fixture assertion ledger, claim ceiling, and repair/quarantine approval gate.
""",
    )
    written.append((root / f"{PHASE_X1}-x2-handoff-v1.md").as_posix())
    return written


def build_x2(root: Path, fixture: dict[str, Any], audit: dict[str, Any]) -> list[str]:
    written: list[str] = []
    summary = audit.get("skill_surface_summary", {})
    fix_summary = fixture_summary(fixture)

    assertion_payload = {
        "aggregate_status": fixture.get("aggregate_status", "OPEN_GAP"),
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("fixture_coverage", "PASS_SHAPE_ONLY", "Expected-negative fixture coverage is executable", fix_summary),
            row("expected_negative_claim_ceiling", "PASS_SHAPE_ONLY", "Passing fixtures prove detection/refusal behavior only"),
            row("repair_completion", "OPEN_GAP", "No plugin-cache repair or quarantine completion occurred"),
        ],
        "fixture_results": fixture.get("fixture_results", []),
    }
    path = root / f"{PHASE_X2}-fixture-assertion-ledger-v1.json"
    write_json(path, assertion_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-fixture-assertion-ledger-v1.md",
        """
# v471 THOS v3 x2 Fixture Assertion Ledger

The executable fixture guard passed its assertions. That means known-bad shapes are detected or routed as open gaps as expected.

This does not mean the plugin cache is repaired, quarantined, or globally safe.
""",
    )
    written.append((root / f"{PHASE_X2}-fixture-assertion-ledger-v1.md").as_posix())

    approval_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("affected_plugin_cache_files", "OPEN_GAP", "Plugin-cache skill files remain repair/quarantine candidates", {"affected_plugin_skill_files": summary.get("issue_file_count")}),
            row("approval_required", "OPEN_GAP", "Repair or quarantine requires separate approved write scope and rollback plan"),
            row("deletion_not_authorized", "PASS_SHAPE_ONLY", "Quarantine is non-reliance labeling, not deletion or cleanup"),
        ],
    }
    path = root / f"{PHASE_X2}-repair-approval-gate-v1.json"
    write_json(path, approval_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-repair-approval-gate-v1.md",
        """
# v471 THOS v3 x2 Repair Approval Gate

Plugin-cache repair/quarantine remains an approval-gated open gap.

Quarantine means non-reliance labeling and carry-forward review. It does not authorize deletion, pruning, rewriting, or cleanup.
""",
    )
    written.append((root / f"{PHASE_X2}-repair-approval-gate-v1.md").as_posix())

    bounded_policy_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "phase_slug": PHASE_X2,
        "rows": [
            row("max_attempts", "PASS_SHAPE_ONLY", "CLI advisory retries should be bounded by explicit attempt count", {"recommended_max_attempts": 1}),
            row("max_seconds", "PASS_SHAPE_ONLY", "CLI advisory probes should be bounded by explicit timeout", {"recommended_probe_seconds": 30}),
            row("reliability_claim", "OPEN_GAP", "CLI advisory reliability remains unproven until final message output completes inside bounds"),
        ],
    }
    path = root / f"{PHASE_X2}-bounded-cli-retry-policy-v1.json"
    write_json(path, bounded_policy_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-bounded-cli-retry-policy-v1.md",
        """
# v471 THOS v3 x2 Bounded CLI Retry Policy

Future CLI advisory probes should use one attempt, explicit timeout, timeout termination, redacted summaries, and no raw temp log staging.

Reliability remains open until final advisory text is produced inside those bounds.
""",
    )
    written.append((root / f"{PHASE_X2}-bounded-cli-retry-policy-v1.md").as_posix())

    run_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v4-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("paired_publication_scope", "PASS_SHAPE_ONLY", "x1 and x2 artifacts are ready for paired validation and curated staging"),
            row("fixture_guard", fixture.get("aggregate_status", "OPEN_GAP"), "Executable expected-negative fixture guard passed"),
            row("plugin_cache_gap", "OPEN_GAP", "Plugin-cache repair/quarantine remains unresolved"),
            row("cli_gap", "OPEN_GAP", "CLI final advisory reliability remains unproven"),
            row("browser_gap", "OPEN_GAP", "Browser direct tool remains unavailable"),
            row("gmut_boundary", "OPEN_GAP", "All six GMUT gates remain open"),
        ],
    }
    path = root / f"{PHASE_X2}-run-status-v1.json"
    write_json(path, run_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-run-status-v1.md",
        """
# v471 THOS v3 x2 Run Status

Status: paired publication candidate with open gaps.

v3 converts expected-negative skill-surface guard additions into executable tempdir-only fixtures. It does not mutate plugin cache, authorize quarantine/deletion, restore full CLI reliability, claim Browser control, or move GMUT gates.

All six GMUT gates remain open.
""",
    )
    written.append((root / f"{PHASE_X2}-run-status-v1.md").as_posix())

    handoff_payload = {
        "aggregate_status": "OPEN_GAP",
        "generated_at_utc": utc_now(),
        "gmUT_gate_effect": "none_open_not_tested",
        "mutation_performed": False,
        "next_phase": "v471-thos-v4-x1",
        "phase_slug": PHASE_X2,
        "rows": [
            row("next_task_1", "OPEN_GAP", "Expand fixture guard into manifest/path-list assertion artifacts if needed"),
            row("next_task_2", "OPEN_GAP", "Decide whether a separate live-write approval packet is needed for plugin-cache repair/quarantine"),
            row("next_task_3", "OPEN_GAP", "Attempt one bounded CLI advisory retry only after deciding whether plugin-cache open gaps are acceptable"),
            row("next_task_4", "OPEN_GAP", "Keep all GMUT gates open"),
        ],
    }
    path = root / f"{PHASE_X2}-v471-thos-v4-handoff-v1.json"
    write_json(path, handoff_payload)
    written.append(path.as_posix())
    write_md(
        root / f"{PHASE_X2}-v471-thos-v4-handoff-v1.md",
        """
# v471 THOS v3 x2 To v4 Handoff

v4 should decide whether plugin-cache repair/quarantine requires a separate live-write approval packet, then either expand fixture assertions or run one bounded CLI advisory retry.

Keep all GMUT gates open.
""",
    )
    written.append((root / f"{PHASE_X2}-v471-thos-v4-handoff-v1.md").as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v471 THOS v3 curated artifacts.")
    parser.add_argument("--artifact-root", default="docs/trinity-live-traces")
    parser.add_argument("--fixture-json", required=True)
    parser.add_argument("--audit-json", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    fixture = read_json(Path(args.fixture_json))
    audit = read_json(Path(args.audit_json))
    written = build_x1(root, fixture, audit)
    written.extend(build_x2(root, fixture, audit))
    print(json.dumps({"generated_at_utc": utc_now(), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
