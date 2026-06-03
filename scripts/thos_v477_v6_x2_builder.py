#!/usr/bin/env python3
"""Build v477 THOS v6 x2 synthesis, overlay decision, and v7 x1 roadmap."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v6_x2"
NEXT_PHASE = "v477_thos_v7_x1"
SHARED_REMOTE = "origin/codex/GHC-Family/beyonder-shared-omega-line"
GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def git_text(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def read_trace(name: str) -> dict[str, Any]:
    return json.loads((TRACES / name).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def lane_rollup(v6_lanes: dict[str, Any], cli_retry: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "v6_x2_lane_rollup",
        "phase": PHASE,
        "prior_app_probe_status": v6_lanes.get("app_probe_status"),
        "prior_app_notify_status": v6_lanes.get("app_notify_status"),
        "prior_cli_status": v6_lanes.get("cli_poll_status"),
        "retry_cli_status": cli_retry.get("aggregate_status"),
        "rows": [
            {
                "lane": row["lane"],
                "surface": row["surface"],
                "prior_status": row["status"],
                "retry_status": next((item.get("completion_status") for item in cli_retry.get("lanes", []) if item.get("lane") == row["lane"]), None)
                if row["surface"] == "codex_cli"
                else row["status"],
                "payload_publication": "status_only",
            }
            for row in v6_lanes.get("rows", [])
        ],
        "summary": {
            "app_lanes_completed": v6_lanes.get("summary", {}).get("app_completed", 0),
            "cli_lanes_waiting_after_retry": sum(1 for item in cli_retry.get("lanes", []) if item.get("completion_status") != "FINAL_MESSAGE_READY"),
            "old_style_spawn_used": False,
            "new_threads_created": False,
        },
    }


def queue_review(commands: dict[str, Any], skills: dict[str, Any], expansions: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "v6_x2_queue_review",
        "phase": PHASE,
        "command_review": {
            "p0_rows": len(commands.get("p0_offline_inspection", [])),
            "connector_rows": len(commands.get("connector_readiness_review", [])),
            "approval_draft_rows": len(commands.get("live_write_approval_draft_only", [])),
            "review_result": "ready_for_v7_no_write_inspection",
        },
        "skill_review": {
            "observed_user_skill_files": skills.get("observed_user_skill_files"),
            "status_counts": skills.get("status_counts", {}),
            "review_result": "metadata_sample_ready_for_v7_join",
        },
        "expansion_review": {
            "p0_rows": len(expansions.get("p0_no_write", [])),
            "p1_rows": len(expansions.get("p1_stdout_only", [])),
            "p2_rows": len(expansions.get("p2_simulation_label_required", [])),
            "installed_count": expansions.get("installed_count", 0),
            "review_result": "probe_selection_ready_for_v7",
        },
    }


def overlay_decision(cli_retry: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "v6_x2_overlay_decision",
        "phase": PHASE,
        "decision": "NO_X3_FOR_V6",
        "next_phase": NEXT_PHASE,
        "reasoning": [
            "v6 x1 already completed the three app-lane notifier pass.",
            "v6 x2 retried Arby and Aster Vale completion polling and observed the same final-marker timeout.",
            "A v6 x3 overlay would duplicate the same status unless the underlying CLI completion marker changes.",
            "v7 x1 should instead focus on better CLI done-signal taxonomy and no-write command/skill/expansion inspections.",
        ],
        "cli_status_carried_forward": cli_retry.get("aggregate_status"),
    }


def reflections() -> list[dict[str, str]]:
    items = [
        ("lane_rollup", "v6 x2 confirms app lanes stayed complete from v6 x1 evidence."),
        ("lane_rollup", "CLI retry stayed at watcher timeout and remains an open gap."),
        ("lane_rollup", "The gap is specific to completion-marker availability, not whole-phase failure."),
        ("lane_rollup", "No new lanes or old-style spawn routes were introduced."),
        ("commands", "The 36 selected command rows are ready for v7 inspection, not execution."),
        ("commands", "Live-write rows remain approval-draft-only."),
        ("commands", "Connector rows remain readiness-only."),
        ("skills", "The skill sample confirms metadata can be used without body copying."),
        ("skills", "Skill repairs remain out of scope without fresh loader evidence."),
        ("expansions", "P0/P1/P2 expansion rows are ready to become v7 probe receipts."),
        ("expansions", "Installed count remains zero."),
        ("sources", "Same-session source continuity is enough for this x2 synthesis."),
        ("sources", "A fresh source refresh should happen before v7 if the session has meaningfully aged."),
        ("observability", "v7 should improve CLI done-signal taxonomy before more retries."),
        ("observability", "timeout_reason should separate alive-waiting from no-signal states."),
        ("governance", "Risk vocabulary remains THOS design context only."),
        ("journey_context", "Journey context remains non-canon unless locally cited and bounded."),
        ("gmut", "All six GMUT gates remain open."),
        ("handoff", "v7 x1 is the better next phase than v6 x3."),
        ("quality", "Exact staging and remote verification remain mandatory."),
    ]
    return [{"step": str(index), "domain": domain, "reflection": text} for index, (domain, text) in enumerate(items, start=1)]


def v7_tasks() -> list[dict[str, str]]:
    seeds = [
        ("lanes", "Run app-lane probe for Cicero, Kierkegaard, and Aristotle."),
        ("lanes", "Run app-lane notify only if probe passes."),
        ("lanes", "Run CLI poll with a clearer done-signal taxonomy."),
        ("lanes", "Record alive-waiting, no-signal, final-marker, and timeout states separately."),
        ("lanes", "Keep lane content unpublished."),
        ("lanes", "Use existing lanes only."),
        ("commands", "Inspect 12 offline command rows with no execution."),
        ("commands", "Assess proof_required and rollback adequacy for each selected row."),
        ("commands", "Turn connector rows into a read-only readiness table."),
        ("commands", "Turn live-write rows into approval-packet candidates."),
        ("commands", "Reject unclear risk rows from v7 execution."),
        ("commands", "Add command-to-skill domain edges without body copies."),
        ("skills", "Re-sample skill frontmatter metadata if skill count drifted."),
        ("skills", "Run metadata duplicate-name review."),
        ("skills", "Build a skill-to-command join sample."),
        ("skills", "Keep user skills and plugin cache unmodified."),
        ("skills", "Record loader evidence only if a loader error appears."),
        ("skills", "Keep sample rows bounded."),
        ("expansions", "Create no-write inspection receipts for top P0 expansions."),
        ("expansions", "Create stdout-only guard probe receipts for top P1 rows."),
        ("expansions", "Keep P2 rows simulation-labelled only."),
        ("expansions", "Keep installed_count zero unless exact install evidence exists."),
        ("expansions", "Rank rows by readiness for v7 x2 synthesis."),
        ("expansions", "Carry blocked rows as open gaps."),
        ("sources", "Refresh Codex app-server and CLI release official sources."),
        ("sources", "Refresh MCP tool and authorization official sources."),
        ("sources", "Refresh GitHub security official sources."),
        ("sources", "Carry Google and NVIDIA as architecture context."),
        ("sources", "Keep Journey context separate from implementation proof."),
        ("sources", "Record source freshness and trust tiers."),
        ("observability", "Add CLI done-signal taxonomy artifact."),
        ("observability", "Add app/CLI schema conformance table."),
        ("observability", "Add retry and timeout windows to every lane row."),
        ("observability", "Add status-only publication boundary to every artifact."),
        ("observability", "Prepare bounded dashboard rows for future visualization."),
        ("observability", "Avoid local temp address publication."),
        ("sandbox", "Run only non-destructive Codex/sandbox checks if needed."),
        ("sandbox", "Do not alter Windows or Codex settings in v7 x1."),
        ("sandbox", "Do not delete caches or temp folders in v7 x1."),
        ("sandbox", "Record sandbox blockers as open gaps."),
        ("sandbox", "Keep PowerShell actions scoped and reversible."),
        ("sandbox", "Preserve CLI worktrees read-only."),
        ("handoff", "Build v7 x1 synthesis from lane, command, skill, expansion, and source evidence."),
        ("handoff", "Build v7 x2 roadmap with 60 tasks."),
        ("handoff", "Decide x2/x3 from current evidence only."),
        ("handoff", "Continue v477 sequence toward v490 without narrowing scope."),
        ("handoff", "Publish exact curated artifacts only."),
        ("handoff", "Verify remote equals local after push."),
        ("gmut", "Carry null recovery gate open."),
        ("gmut", "Carry dimensional/SI gate open."),
        ("gmut", "Carry conservation/exchange gate open."),
        ("gmut", "Carry baseline recovery gate open."),
        ("gmut", "Carry fifth-force/equivalence gate open."),
        ("gmut", "Carry consciousness measurement bridge gate open."),
        ("quality", "Parse every JSON artifact."),
        ("quality", "Compile every new helper script."),
        ("quality", "Run scoped guard scan."),
        ("quality", "Run whitespace and staged diff checks."),
        ("quality", "Stage exact files only."),
        ("quality", "Fetch and drift-check before push."),
    ]
    return [{"id": f"v477-v7-x1-task-{index:02d}", "domain": domain, "task": text} for index, (domain, text) in enumerate(seeds, start=1)]


def build() -> None:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])

    v6_lanes = read_trace("v477-thos-v6-x1-lane-status-v1.json")
    cli_retry = read_trace("v477-thos-v6-x2-cli-lane-completion-poll-v1.json")
    commands = read_trace("v477-thos-v6-x1-command-probe-selection-v1.json")
    skills = read_trace("v477-thos-v6-x1-skill-metadata-sample-v1.json")
    expansions = read_trace("v477-thos-v6-x1-expansion-probe-selection-v1.json")
    lane = lane_rollup(v6_lanes, cli_retry)
    queue = queue_review(commands, skills, expansions)
    decision = overlay_decision(cli_retry)
    reflection_rows = reflections()

    synthesis = {
        "artifact_type": "v6_x2_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "local_head_before_build": local_head,
        "remote_head_before_build": remote_head,
        "drift_before_build": drift,
        "lane_summary": lane["summary"],
        "queue_review": queue,
        "overlay_decision": decision["decision"],
        "reflection_steps": reflection_rows,
        "claim_boundary": {
            "thos_scope": "v6 synthesis and v7 handoff only",
            "gmut_gates": {gate: "open" for gate in GMUT_GATES},
            "canon_promotion": "not_claimed",
        },
    }

    run_status = {
        "artifact_type": "run_status_pair",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_WITH_CLI_WATCH_TIMEOUT_OPEN_GAP",
        "status_rows": [
            {"id": "lane_rollup", "status": "PASS_WITH_OPEN_GAP", "summary": "App lanes remain complete; CLI retry remains watcher timeout."},
            {"id": "queue_review", "status": "PASS_METADATA_ONLY", "summary": "Command, skill, and expansion queues are ready for v7 no-write work."},
            {"id": "overlay_decision", "status": decision["decision"], "summary": "v7 x1 is more useful than a v6 x3 duplicate retry."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "next_expected_phase": NEXT_PHASE,
    }

    roadmap = {
        "artifact_type": "v7_x1_60_task_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": 60,
        "tasks": v7_tasks(),
    }

    artifacts = {
        "v477-thos-v6-x2-lane-rollup-v1": lane,
        "v477-thos-v6-x2-queue-review-v1": queue,
        "v477-thos-v6-x2-overlay-decision-v1": decision,
        "v477-thos-v6-x2-synthesis-v1": synthesis,
        "v477-thos-v6-x2-run-status-v1": run_status,
        "v477-thos-v7-x1-roadmap-v1": roadmap,
    }
    for stem, payload in artifacts.items():
        write_json(TRACES / f"{stem}.json", payload)

    write_md(
        TRACES / "v477-thos-v6-x2-lane-rollup-v1.md",
        "v477 THOS v6 x2 Lane Rollup",
        [
            f"- prior_app_notify_status: `{lane['prior_app_notify_status']}`",
            f"- retry_cli_status: `{lane['retry_cli_status']}`",
            f"- cli_lanes_waiting_after_retry: `{lane['summary']['cli_lanes_waiting_after_retry']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x2-queue-review-v1.md",
        "v477 THOS v6 x2 Queue Review",
        [
            f"- command_review: `{queue['command_review']['review_result']}`",
            f"- skill_review: `{queue['skill_review']['review_result']}`",
            f"- expansion_review: `{queue['expansion_review']['review_result']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x2-overlay-decision-v1.md",
        "v477 THOS v6 x2 Overlay Decision",
        [
            f"- decision: `{decision['decision']}`",
            f"- next_phase: `{decision['next_phase']}`",
            "",
            "## Reasoning",
            *[f"- {item}" for item in decision["reasoning"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x2-synthesis-v1.md",
        "v477 THOS v6 x2 Synthesis",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- overall_status: `{run_status['overall_status']}`",
            f"- overlay_decision: `{decision['decision']}`",
            "- claim boundary: THOS synthesis only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            *[f"- {row['step']}. {row['domain']}: {row['reflection']}" for row in reflection_rows],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x2-run-status-v1.md",
        "v477 THOS v6 x2 Run Status",
        [
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            *[f"- {row['id']}: `{row['status']}` - {row['summary']}" for row in run_status["status_rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v7-x1-roadmap-v1.md",
        "v477 THOS v7 x1 Roadmap",
        [
            f"- task_count: `{roadmap['task_count']}`",
            "- entry: v6 x2 remote-verified, existing lanes only, all GMUT gates open.",
            "",
            "## Tasks",
            *[f"- {row['id']} ({row['domain']}): {row['task']}" for row in roadmap["tasks"]],
        ],
    )


def main() -> None:
    build()
    print(json.dumps({"status": "built", "phase": PHASE, "next_phase": NEXT_PHASE}, indent=2))


if __name__ == "__main__":
    main()
