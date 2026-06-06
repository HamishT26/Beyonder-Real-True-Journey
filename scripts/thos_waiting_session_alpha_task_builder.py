#!/usr/bin/env python3
"""Build status-safe Alpha task ledgers for x1/x2 waiting windows."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


X1_ALPHA_TASKS = [
    "Inventory the current command-surface receipts and identify stale, missing, or weakly evidenced command-book entries.",
    "Sample local skill manifests for missing frontmatter, weak descriptions, duplicate themes, or overlong names without editing user skills.",
    "Map candidate skill improvements into exact future approval packets instead of mutating broad skill folders.",
    "Review system-expansion cache boards for stale generated-latest artifacts and mark which need refresh receipts.",
    "Crosswalk watcher/notifier scripts against the current no-babysitting cadence policy.",
    "Draft next x2 build candidates that improve final-marker clarity without publishing raw lane text.",
    "Identify command runner rollback gaps and propose dry-run-first repair tasks.",
    "Refresh source-ledger priorities for OpenAI/Codex, MCP, OWASP, Google Cloud, NVIDIA, GitHub/npm, and local docs.",
    "Create a small risk board for any helper that could mutate files, launch processes, or touch external accounts.",
    "Trace Trinity Mandala coverage across GMUT Mind, THOS Body, and Freed ID/CBR Heart for the next phase.",
    "Convert repeated blockers into stale-flow entries with next safe retry conditions.",
    "Prepare exact staging inventories before any commit so broad worktree churn is ignored.",
    "Check whether the previous x2 build queue produced reusable scripts or only documentation receipts.",
    "Draft approval-packet candidates for any skill, plugin-cache, user-skill, or account-surface changes before touching them.",
    "Maintain a concise next-boundary handoff so phase progression stays sequential and auditable.",
]

X2_PREP_TASKS = [
    "Reconcile x1 lane metadata with open gaps before build work begins.",
    "Pick the highest-leverage build item that can be completed inside the approved repo scope.",
    "Create or update validators before adding new artifacts whenever practical.",
    "Record which x1 eureka tasks are deferred because they need exact approval.",
    "Run local JSON/script/guard checks before staging any x2 artifact.",
    "Keep GMUT, physics, consciousness, and canon gates open unless exact evidence changes that state.",
    "Use watcher/notifier receipts as supervision evidence instead of repeated manual polling.",
    "Prepare next x1 prompt policy while current x2 work validates.",
    "Review source-ledger claims for primary-source support and remove weak overclaims.",
    "End with a publication-ready build validation receipt or an honest blocker receipt.",
]

X2_BUILD_SESSION_TASKS = [
    "Spend the first 5 minutes selecting one build target and one validation target from the x1 eureka queue.",
    "Spend the next 10 minutes implementing or refining the selected repo-scoped helper, receipt, validator, or roadmap.",
    "Spend the next 5 minutes running JSON parse, script compile, guard, whitespace, and staged-diff checks where applicable.",
    "Spend the next 5 minutes integrating source-ledger and Trinity Mandala implications into the build receipt.",
    "Spend the final 5 minutes preparing exact staging, remote drift checks, and next-boundary handoff.",
    "If no safe build target exists, use the 30-minute window to produce an approval-packet candidate and blocker receipt instead of forcing mutation.",
]


def build_receipt(phase_slug: str, next_phase_slug: str | None, boundary: str) -> dict[str, object]:
    threshold = 15 if boundary == "x1" else 10
    return {
        "artifact_type": "waiting_session_alpha_task_framework",
        "phase_slug": phase_slug,
        "next_phase_slug": next_phase_slug,
        "boundary": boundary,
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_status": "PASS_WAITING_SESSION_ALPHA_TASK_FRAMEWORK_READY",
        "cadence_policy": {
            "x1_wait_mark_minutes": 15,
            "x2_prep_mark_minutes": 10,
            "x2_build_run_test_use_minimum_minutes": 30,
            "watchers_and_notifiers_supervise_lanes": True,
            "aletheon_must_work_productively_between_marks": True,
            "no_pre_mark_sibling_status_or_artifact_upload_checks": True,
            "current_boundary_wait_mark_minutes": threshold,
        },
        "alpha_task_banks": {
            "x1_15_minute_alpha_tasks": X1_ALPHA_TASKS,
            "x2_10_minute_prep_tasks": X2_PREP_TASKS,
            "x2_30_minute_build_run_test_use_tasks": X2_BUILD_SESSION_TASKS,
        },
        "system_surface_reflection_targets": [
            "local skill manifests and SKILL.md frontmatter",
            "command-surface core and autonomy contracts",
            "system-expansion cache boards and latest receipts",
            "watcher, notifier, supervisor, launcher, and TUI helper scripts",
            "source ledgers and public research receipts",
            "phase closeout, handoff, and stale-flow receipts",
        ],
        "mutation_boundary": {
            "repo_scoped_receipts_allowed": True,
            "repo_scoped_helper_scripts_allowed_when_validated": True,
            "broad_skill_mutation_allowed": False,
            "plugin_cache_mutation_allowed": False,
            "user_skill_mutation_allowed_without_exact_packet": False,
            "external_account_mutation_allowed": False,
        },
        "claim_boundary": {
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "credentials_published": False,
            "local_absolute_paths_published": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def write_md(receipt: dict[str, object], path: str) -> None:
    lines = [
        f"# {receipt['phase_slug']} Waiting Session Alpha Task Framework",
        "",
        f"- Status: `{receipt['overall_status']}`",
        f"- Boundary: `{receipt['boundary']}`",
        "- x1 wait mark: `15` minutes",
        "- x2 prep mark: `10` minutes",
        "- x2 build/run/test/use minimum: `30` minutes",
        "- Watchers and notifiers supervise lanes: true",
        "- Aletheon works productively between marks: true",
        "",
        "## x1 15-Minute Alpha Tasks",
        "",
    ]
    banks = receipt["alpha_task_banks"]  # type: ignore[index]
    for index, task in enumerate(banks["x1_15_minute_alpha_tasks"], start=1):  # type: ignore[index]
        lines.append(f"{index}. {task}")
    lines.extend(["", "## x2 10-Minute Prep Tasks", ""])
    for index, task in enumerate(banks["x2_10_minute_prep_tasks"], start=1):  # type: ignore[index]
        lines.append(f"{index}. {task}")
    lines.extend(["", "## x2 30-Minute Build/Run/Test/Use Tasks", ""])
    for index, task in enumerate(banks["x2_30_minute_build_run_test_use_tasks"], start=1):  # type: ignore[index]
        lines.append(f"{index}. {task}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This framework is for repo-scoped receipts, helper scripts, validators, and exact approval packets. It does not approve broad skill mutation, plugin-cache edits, user-skill edits, external account mutation, raw lane text publication, or GMUT/canon closure claims.",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Alpha task ledgers for scheduled waiting windows.")
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--next-phase-slug")
    parser.add_argument("--boundary", choices=["x1", "x2"], required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    args = parser.parse_args()

    receipt = build_receipt(args.phase_slug, args.next_phase_slug, args.boundary)
    Path(args.receipt_json).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    write_md(receipt, args.receipt_md)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
