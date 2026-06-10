#!/usr/bin/env python3
"""Convert sibling-runner issues into bounded repair and enhancement plans."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {"available": False, "file": name}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False, "file": name}


def issue_rows(phase_slug: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    lane_board = read_json(f"{phase_slug}-lane-retry-status-board-v1.json")
    background = read_json(f"{phase_slug}-background-sibling-notifier-runner-v1.json")
    multiplex = read_json(f"{phase_slug}-local-multiplex-tui-app-server-runner-v1.json")
    if lane_board.get("cli_retry_rows"):
        open_attempts = [
            row for row in lane_board.get("cli_retry_rows", []) if str(row.get("aggregate_status", "")).startswith("OPEN_GAP")
        ]
        if open_attempts:
            rows.append(
                {
                    "id": "ISSUE-CLI-FINAL-MARKER",
                    "status": "open",
                    "evidence": f"{len(open_attempts)} CLI watch attempts did not find final markers.",
                    "safe_retry_count": len(open_attempts),
                    "repair_class": "notifier_bridge_and_completion_contract",
                    "approved_now": "repo_runner_design_only",
                }
            )
    if background.get("overall_status") == "APP_DONE_CLI_FINAL_MARKER_OPEN":
        rows.append(
            {
                "id": "ISSUE-BACKGROUND-PARTIAL",
                "status": "open",
                "evidence": "background runner can fuse app success with CLI open gap but cannot force final markers.",
                "safe_retry_count": 1,
                "repair_class": "background_completion_policy",
                "approved_now": "repo_runner_design_only",
            }
        )
    if multiplex.get("overall_status") == "APP_READY_CLI_OPEN":
        rows.append(
            {
                "id": "ISSUE-MULTIPLEX-CLI-OPEN",
                "status": "open",
                "evidence": "multiplex board can display app readiness while CLI lanes remain open.",
                "safe_retry_count": 1,
                "repair_class": "operator_visibility",
                "approved_now": "repo_runner_design_only",
            }
        )
    if not rows:
        rows.append(
            {
                "id": "ISSUE-NONE-DETECTED",
                "status": "ready",
                "evidence": "no open issue found in curated receipts for this phase.",
                "safe_retry_count": 0,
                "repair_class": "monitor_only",
                "approved_now": "no_live_repair_needed",
            }
        )
    return rows


def enhancement_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": "ENH-01",
            "name": "background_notifier_completion_contract",
            "description": "Use one runner to coordinate app completion and CLI final-marker status while keeping temp output unpublished.",
            "mutation_scope": "repo_script_only",
        },
        {
            "id": "ENH-02",
            "name": "local_multiplex_status_board",
            "description": "Show all five sibling lanes in one status surface without creating new threads.",
            "mutation_scope": "repo_script_only",
        },
        {
            "id": "ENH-03",
            "name": "fix_enhancement_plan_sandbox",
            "description": "Turn recurring open gaps into bounded repair plans and approval packets.",
            "mutation_scope": "repo_script_only",
        },
        {
            "id": "ENH-04",
            "name": "multi_agent_orchestration_skill_draft",
            "description": "Prepare a draft evolved orchestration skill before any live skill mutation.",
            "mutation_scope": "draft_artifact_only",
        },
        {
            "id": "ENH-05",
            "name": "future_background_detach_gate",
            "description": "Add a detached watcher mode only after a separate exact approval covers persistent processes.",
            "mutation_scope": "approval_required",
        },
    ]


def draft_skill(version_label: str) -> dict[str, Any]:
    body = [
        "---",
        "name: multi-agent-orchestrator-operations",
        "description: Operate the Multi Agent Orchestrator pack with proof-backed app, CLI, background notifier, and THOS phase boundaries.",
        "---",
        "",
        "# Multi Agent Orchestrator Operations",
        "",
        "Use when Codex needs to coordinate existing app and CLI sibling lanes, background notifier receipts, multiplex status boards, or THOS handoff artifacts.",
        "",
        "## Workflow",
        "1. Read the repo contract and workflow before promoting orchestration state.",
        "2. Prefer existing app lanes and existing CLI lanes; do not create replacement siblings by default.",
        "3. Run app-lane notifiers through the local app-server status path when available.",
        "4. Run CLI final-marker watchers as bounded status checks; never treat absent final markers as completion.",
        "5. Use the background sibling notifier to fuse app readiness and CLI gap evidence.",
        "6. Use the multiplex status board for operator visibility when several lanes are active.",
        "7. Use the fix-enhancement updater to convert repeated gaps into bounded repair plans.",
        "8. Publish only curated receipts, status boards, roadmaps, and approval packets.",
        "",
        "## Boundaries",
        "- No new old-style subagent spawning unless a separate exact approval says otherwise.",
        "- No live skill, plugin-cache, account, or external system mutation without separate exact approval.",
        "- No unpublished transport payloads, nonpublic dumps, auth-material, or temp output in repo artifacts.",
        "- All GMUT gates remain open unless separate closure artifacts prove otherwise.",
    ]
    return {
        "artifact_type": "multi_agent_orchestration_skill_evolution_draft",
        "version_label": version_label,
        "status": "draft_only_not_applied",
        "live_skill_mutation_performed": False,
        "line_count": len(body),
        "draft_body": body,
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    issues = issue_rows(args.phase_slug)
    enhancements = enhancement_rows()
    skill_draft = draft_skill(args.version_label)
    payload = {
        "artifact_type": "fix_enhancement_updater_runner",
        "phase_slug": args.phase_slug,
        "version_label": args.version_label,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_LIVE_SKILL_APPROVAL_REQUIRED",
        "issues": issues,
        "enhancements": enhancements,
        "skill_draft_receipt": f"{args.phase_slug}-multi-agent-orchestration-skill-evolution-draft-v1.json",
        "approval_packet_receipt": f"{args.phase_slug}-live-skill-evolution-approval-packet-v1.md",
        "policy": {
            "repo_runner_design_only": True,
            "live_skill_mutation_performed": False,
            "external_account_mutation_performed": False,
            "persistent_background_process_started": False,
        },
        "claim_boundary": {
            "scope": "fix and enhancement planning only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(TRACE_DIR / f"{args.receipt_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.receipt_prefix}-v1.md", payload)
    write_json(TRACE_DIR / f"{args.phase_slug}-multi-agent-orchestration-skill-evolution-draft-v1.json", skill_draft)
    write_skill_draft_md(TRACE_DIR / f"{args.phase_slug}-multi-agent-orchestration-skill-evolution-draft-v1.md", skill_draft)
    write_approval_md(TRACE_DIR / f"{args.phase_slug}-live-skill-evolution-approval-packet-v1.md", args, issues, enhancements)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Fix Enhancement Updater Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        "- policy: repo-runner design only; no live skill mutation; no persistent process started.",
        "- claim boundary: fix and enhancement planning only; all GMUT gates remain open.",
        "",
        "## Issues",
    ]
    for row in payload["issues"]:
        lines.append(f"- `{row['id']}` / `{row['status']}`: {row['evidence']} Repair class `{row['repair_class']}`.")
    lines.extend(["", "## Enhancements"])
    for row in payload["enhancements"]:
        lines.append(f"- `{row['id']}` {row['name']}: {row['description']} Scope `{row['mutation_scope']}`.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_skill_draft_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Multi Agent Orchestration Skill Evolution Draft",
        "",
        f"- version_label: `{payload['version_label']}`",
        "- status: `draft_only_not_applied`",
        "- live_skill_mutation_performed: `false`",
        "",
        "## Draft Body",
        "```markdown",
        *payload["draft_body"],
        "```",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_approval_md(path: Path, args: argparse.Namespace, issues: list[dict[str, Any]], enhancements: list[dict[str, Any]]) -> None:
    lines = [
        "# Live Skill Evolution Approval Packet",
        "",
        f"- phase_slug: `{args.phase_slug}`",
        f"- version_label: `{args.version_label}`",
        "- status: `approval_required_before_live_skill_mutation`",
        "- approved repo work already performed: `draft artifacts and runner scripts only`",
        "",
        "## Proposed Live Scope",
        "- Update the existing multi-agent orchestration operations skill frontmatter and body from the draft artifact.",
        "- Preserve the original skill backup locally if live mutation is later approved.",
        "- Verify YAML frontmatter after any approved live mutation.",
        "- Do not edit unrelated skills, plugin cache files, account settings, or app state.",
        "",
        "## Current Issues",
        *[f"- `{row['id']}`: {row['evidence']}" for row in issues],
        "",
        "## Enhancements",
        *[f"- `{row['id']}` {row['name']}: {row['description']}" for row in enhancements],
        "",
        "## Mandatory Pause Conditions",
        "- Any live path outside the named skill is needed.",
        "- Any body-preserving rule cannot be satisfied.",
        "- Any auth-material or nonpublic payload appears.",
        "- Any external account, plugin cache, or app state mutation is required.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--version-label", default="v12-x1")
    parser.add_argument("--receipt-prefix")
    args = parser.parse_args()
    args.receipt_prefix = args.receipt_prefix or f"{args.phase_slug}-fix-enhancement-updater-runner"
    return args


def main() -> int:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "phase_slug": payload["phase_slug"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
