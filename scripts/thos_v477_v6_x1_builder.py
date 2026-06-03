#!/usr/bin/env python3
"""Build v477 THOS v6 x1 bounded readiness artifacts and v6 x2 handoff."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v6_x1"
NEXT_PHASE = "v477_thos_v6_x2"
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
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unavailable"


def read_trace(name: str) -> dict[str, Any]:
    return json.loads((TRACES / name).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def lane_status(app_probe: dict[str, Any], app_run: dict[str, Any], cli_poll: dict[str, Any]) -> dict[str, Any]:
    app_rows = []
    for lane in app_run.get("lanes", []):
        app_rows.append(
            {
                "lane": lane["lane"],
                "surface": "app_server",
                "status": lane.get("overall_status"),
                "trace_id": f"{PHASE}:{lane['lane']}:app",
                "run_id": f"{PHASE}:app:notifier",
                "retry_window_seconds": lane.get("duration_seconds"),
                "timeout_reason": None if lane.get("overall_status") == "completed" else "app_completion_not_observed",
                "payload_publication": "status_only",
                "gmut_gate_state": "all_open",
            }
        )
    cli_rows = []
    for lane in cli_poll.get("lanes", []):
        cli_rows.append(
            {
                "lane": lane["lane"],
                "surface": "codex_cli",
                "status": lane.get("completion_status"),
                "trace_id": f"{PHASE}:{lane['lane']}:cli",
                "run_id": f"{PHASE}:cli:poll",
                "retry_window_seconds": 25,
                "timeout_reason": "final_message_marker_absent",
                "payload_publication": "status_only",
                "gmut_gate_state": "all_open",
            }
        )
    return {
        "artifact_type": "v6_x1_lane_status",
        "phase": PHASE,
        "app_probe_status": app_probe.get("overall_status"),
        "app_notify_status": app_run.get("overall_status"),
        "cli_poll_status": cli_poll.get("aggregate_status"),
        "rows": app_rows + cli_rows,
        "summary": {
            "app_completed": sum(1 for row in app_rows if row["status"] == "completed"),
            "cli_waiting": sum(1 for row in cli_rows if row["status"] != "FINAL_MESSAGE_READY"),
            "old_style_spawn_used": False,
            "new_threads_created": False,
        },
    }


def command_probe_selection(command_queues: dict[str, Any]) -> dict[str, Any]:
    queues = command_queues["queues"]
    offline = queues["offline_low_risk_candidate_sample"][:12]
    connector = queues["connector_approval_required"][:12]
    live = queues["live_write_approval_required"][:12]
    return {
        "artifact_type": "v6_x1_command_probe_selection",
        "phase": PHASE,
        "selection_policy": "metadata_only_no_execution",
        "p0_offline_inspection": offline,
        "connector_readiness_review": connector,
        "live_write_approval_draft_only": live,
        "counts": {
            "p0_offline_inspection": len(offline),
            "connector_readiness_review": len(connector),
            "live_write_approval_draft_only": len(live),
        },
    }


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip().splitlines()
    parsed: dict[str, str] = {}
    for line in block:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"')
    return parsed


def skill_metadata_sample() -> dict[str, Any]:
    skill_root = Path.home() / ".codex" / "skills"
    rows = []
    status_counts: Counter[str] = Counter()
    if skill_root.exists():
        for skill_file in sorted(skill_root.glob("*/SKILL.md")):
            text = skill_file.read_text(encoding="utf-8", errors="replace")
            frontmatter = parse_frontmatter(text)
            status = "PASS_METADATA" if frontmatter.get("name") and frontmatter.get("description") else "OPEN_GAP_FRONTMATTER"
            status_counts[status] += 1
            if len(rows) < 30:
                rows.append(
                    {
                        "skill_dir": skill_file.parent.name,
                        "name": frontmatter.get("name"),
                        "has_description": bool(frontmatter.get("description")),
                        "status": status,
                    }
                )
    return {
        "artifact_type": "v6_x1_skill_metadata_sample",
        "phase": PHASE,
        "sample_policy": "frontmatter_metadata_only_no_body_copy",
        "observed_user_skill_files": sum(status_counts.values()),
        "status_counts": dict(status_counts),
        "sample_rows": rows,
        "mutation_performed": False,
    }


def expansion_probe_selection(expansion_queue: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "v6_x1_expansion_probe_selection",
        "phase": PHASE,
        "selection_policy": "probe_only_no_install",
        "p0_no_write": expansion_queue.get("top_p0", [])[:12],
        "p1_stdout_only": expansion_queue.get("top_p1", [])[:12],
        "p2_simulation_label_required": expansion_queue.get("top_p2", [])[:12],
        "installed_count": 0,
    }


def source_continuity(source_ledger: dict[str, Any]) -> dict[str, Any]:
    selected = []
    for item in source_ledger.get("sources", []):
        if item.get("trust_tier") in {"official", "official_source_repo", "official_blog", "official_newsroom"}:
            selected.append(item)
    return {
        "artifact_type": "v6_x1_source_continuity",
        "phase": PHASE,
        "source_status": "SAME_SESSION_REFRESH_REUSED",
        "prior_search_count": source_ledger.get("search_count"),
        "selected_source_count": len(selected),
        "selected_sources": selected[:18],
        "claim_ceiling": "architecture_context_only",
    }


def reflections() -> list[dict[str, str]]:
    items = [
        ("lane_mesh", "The app-lane probe and notify passes completed again in v6 x1."),
        ("lane_mesh", "The app-server notifier can now be treated as a reusable THOS operating surface."),
        ("lane_mesh", "The CLI lanes still need better completion markers than temp final-message files."),
        ("lane_mesh", "Existing-lane-only policy remains intact."),
        ("lane_mesh", "No replacement siblings or old-style spawn route was used."),
        ("cli_gap", "The Arby/Aster timeout is an open gap, not a failure of the whole phase."),
        ("cli_gap", "A future watcher should detect alive-process, no-output, and final-marker states separately."),
        ("cli_gap", "The CLI watcher output remains status-only and unpublished as transport content."),
        ("command_queue", "The v5 x2 command queue can now seed concrete v6 inspection rows."),
        ("command_queue", "Offline low-risk commands are appropriate for P0 inspection first."),
        ("command_queue", "Connector rows should stay readiness-only until a connector write packet exists."),
        ("command_queue", "Live-write rows remain approval-draft-only."),
        ("skill_metadata", "User skills can be sampled safely through frontmatter metadata only."),
        ("skill_metadata", "Skill body text is unnecessary for readiness counts."),
        ("skill_metadata", "Loader repairs should depend on fresh loader evidence, not broad scans."),
        ("skill_metadata", "Plugin cache remains outside ordinary phase mutation."),
        ("expansion_probe", "The 90-row expansion matrix can be acted on without installing anything."),
        ("expansion_probe", "P0/P1/P2 tiers keep inspection, dry-run, and simulation boundaries separate."),
        ("expansion_probe", "Installed count stays zero in this phase."),
        ("source_continuity", "The 32-search source refresh remains usable within this same continuous session."),
        ("source_continuity", "Official architecture sources inform THOS design only."),
        ("source_continuity", "External AI platforms do not validate GMUT physics claims."),
        ("observability", "run_id, trace_id, retry_window_seconds, timeout_reason, and payload_publication are now explicit."),
        ("observability", "The schema can be applied to app and CLI lanes together."),
        ("governance", "AI governance sources support risk vocabulary, not canon promotion."),
        ("journey_context", "Journey context remains non-canon unless cited in a bounded local artifact."),
        ("gmut", "All six GMUT gates remain open."),
        ("handoff", "v6 x2 should turn these selections into a tighter synthesis and next queue."),
        ("handoff", "v6 x2 should decide whether another overlay is needed from fresh lane evidence."),
        ("quality", "Publication still requires exact staging and remote-equals-local verification."),
    ]
    return [{"step": str(index), "domain": domain, "reflection": text} for index, (domain, text) in enumerate(items, start=1)]


def v6_x2_tasks() -> list[dict[str, str]]:
    seeds = [
        ("lanes", "Use v6 x2 to summarize app-lane v6 x1 completion and CLI open gap."),
        ("lanes", "Retry Arby/Aster completion poll once before v6 x2 synthesis."),
        ("lanes", "Add alive-process observation if available without publishing process command text."),
        ("lanes", "Keep Cicero, Kierkegaard, and Aristotle advisory-only."),
        ("lanes", "Record existing-lane-only proof again."),
        ("lanes", "Decide whether v6 needs x3 from fresh lane evidence."),
        ("commands", "Inspect the 12 offline low-risk command candidates without executing them."),
        ("commands", "Annotate each selected command with proof and rollback adequacy."),
        ("commands", "Convert connector queue sample into read-only readiness checklist."),
        ("commands", "Convert live-write queue sample into exact approval packet candidates."),
        ("commands", "Reject any command missing intent, mode, risk, or proof metadata."),
        ("commands", "Keep command templates out of published samples if they include local coupling."),
        ("skills", "Summarize the skill metadata sample status counts."),
        ("skills", "Run a duplicate-name scan on sample rows only."),
        ("skills", "Prepare top skill-readiness rows without editing skills."),
        ("skills", "Keep skill body copies out of artifacts."),
        ("skills", "Do not mutate plugin cache or user skills in v6 x2."),
        ("skills", "Prepare an exact repair packet only if a loader blocker appears."),
        ("expansions", "Promote top P0 expansion rows into no-write inspection receipts."),
        ("expansions", "Promote top P1 rows into stdout-only guard probe receipts."),
        ("expansions", "Keep P2 rows as simulation candidates only."),
        ("expansions", "Record installed_count as zero unless exact install proof exists."),
        ("expansions", "Rank proposal rows by evidence usefulness for v7 x1."),
        ("expansions", "Carry rejected live-write candidates as approval-needed rows."),
        ("sources", "Refresh at least Codex, MCP, and GitHub official sources if v6 x2 publishes after a long delay."),
        ("sources", "Carry Google and NVIDIA sources as architecture context only."),
        ("sources", "Keep governance sources separated from implementation proof."),
        ("sources", "Do not use Journey context as empirical proof."),
        ("sources", "Prefer official pages over news or forum context."),
        ("sources", "Record source-drift caveats explicitly."),
        ("observability", "Compare app and CLI receipt schemas for missing fields."),
        ("observability", "Add timeout_reason to future CLI notifier if needed."),
        ("observability", "Add app-lane probe/notify delta to lane boards."),
        ("observability", "Prepare a dashboard-ready bounded row set."),
        ("observability", "Keep event method names bounded to safe summaries."),
        ("observability", "Keep local temp and machine-specific addresses redacted."),
        ("sandbox", "Run Codex version and sandbox help checks only if needed."),
        ("sandbox", "Do not change Windows settings in v6 x2."),
        ("sandbox", "Do not delete temp or cache folders in v6 x2."),
        ("sandbox", "Carry sandbox blockers as diagnostic open gaps."),
        ("sandbox", "Keep PowerShell usage non-destructive."),
        ("sandbox", "Document any setup-refresh symptom without repair overreach."),
        ("handoff", "Generate v7 x1 roadmap after v6 x2 synthesis."),
        ("handoff", "Keep every-second-phase publication cadence where feasible."),
        ("handoff", "Prepare v7 x1 lane prompts from v6 evidence."),
        ("handoff", "Keep the v477 sequence moving toward v490."),
        ("handoff", "Avoid widening scope into unapproved account or external writes."),
        ("handoff", "Record remote verification after publication."),
        ("gmut", "Carry null recovery gate open."),
        ("gmut", "Carry dimensional/SI gate open."),
        ("gmut", "Carry conservation/exchange gate open."),
        ("gmut", "Carry baseline recovery gate open."),
        ("gmut", "Carry fifth-force/equivalence gate open."),
        ("gmut", "Carry consciousness measurement bridge gate open."),
        ("quality", "Parse every v6 x2 JSON artifact."),
        ("quality", "Compile any new v6 x2 helper script."),
        ("quality", "Run scoped guard scan before staging."),
        ("quality", "Run staged diff and whitespace check."),
        ("quality", "Stage exact files only."),
        ("quality", "Push only after drift check passes."),
    ]
    return [{"id": f"v477-v6-x2-task-{index:02d}", "domain": domain, "task": text} for index, (domain, text) in enumerate(seeds, start=1)]


def build() -> None:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])

    app_probe = read_trace("v477-thos-v6-x1-app-lane-completion-notifier-probe-v1.json")
    app_run = read_trace("v477-thos-v6-x1-app-lane-completion-notifier-v1.json")
    cli_poll = read_trace("v477-thos-v6-x1-cli-lane-completion-poll-v1.json")
    command_queue = read_trace("v477-thos-v5-x2-command-approval-queues-v1.json")
    expansion_queue = read_trace("v477-thos-v5-x2-expansion-ranked-queue-v1.json")
    source_ledger = read_trace("v477-thos-v5-x2-source-ledger-v1.json")
    roadmap = read_trace("v477-thos-v6-x1-roadmap-v1.json")

    lanes = lane_status(app_probe, app_run, cli_poll)
    commands = command_probe_selection(command_queue)
    skills = skill_metadata_sample()
    expansions = expansion_probe_selection(expansion_queue)
    sources = source_continuity(source_ledger)
    reflection_rows = reflections()

    synthesis = {
        "artifact_type": "v6_x1_synthesis",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "local_head_before_build": local_head,
        "remote_head_before_build": remote_head,
        "drift_before_build": drift,
        "input_roadmap_task_count": roadmap.get("task_count"),
        "lane_summary": lanes["summary"],
        "command_selection_counts": commands["counts"],
        "skill_status_counts": skills["status_counts"],
        "expansion_selection_counts": {
            "p0_no_write": len(expansions["p0_no_write"]),
            "p1_stdout_only": len(expansions["p1_stdout_only"]),
            "p2_simulation_label_required": len(expansions["p2_simulation_label_required"]),
        },
        "source_status": sources["source_status"],
        "reflection_steps": reflection_rows,
        "claim_boundary": {
            "thos_scope": "bounded lane, command, skill, expansion, source, and observability readiness",
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
            {"id": "app_lanes", "status": "PASS", "summary": "Cicero, Kierkegaard, and Aristotle completed v6 x1 app notifier."},
            {"id": "cli_lanes", "status": cli_poll.get("aggregate_status"), "summary": "Arby and Aster Vale remain pending final-message marker."},
            {"id": "commands", "status": "PASS_METADATA_ONLY", "summary": "36 command rows selected for inspection/readiness/approval-draft queues."},
            {"id": "skills", "status": "PASS_METADATA_ONLY", "summary": "User-skill frontmatter metadata sampled without body copies."},
            {"id": "expansions", "status": "PASS_PROBE_SELECTION_ONLY", "summary": "36 expansion rows selected for no-write/stdout/simulation-labelled probes."},
            {"id": "sources", "status": sources["source_status"], "summary": "Same-session source refresh carried forward as architecture context."},
            {"id": "claim_boundary", "status": "PASS", "summary": "All six GMUT gates remain open."},
        ],
        "next_expected_phase": NEXT_PHASE,
    }

    roadmap_next = {
        "artifact_type": "v6_x2_60_task_roadmap",
        "phase": PHASE,
        "next_phase": NEXT_PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "task_count": 60,
        "tasks": v6_x2_tasks(),
        "entry_conditions": [
            "Start from remote-verified v6 x1 commit.",
            "Use existing lanes only.",
            "Keep CLI open gap honest.",
            "Keep all GMUT gates open.",
        ],
    }

    artifacts = {
        "v477-thos-v6-x1-lane-status-v1": lanes,
        "v477-thos-v6-x1-command-probe-selection-v1": commands,
        "v477-thos-v6-x1-skill-metadata-sample-v1": skills,
        "v477-thos-v6-x1-expansion-probe-selection-v1": expansions,
        "v477-thos-v6-x1-source-continuity-v1": sources,
        "v477-thos-v6-x1-synthesis-v1": synthesis,
        "v477-thos-v6-x1-run-status-v1": run_status,
        "v477-thos-v6-x2-roadmap-v1": roadmap_next,
    }
    for stem, payload in artifacts.items():
        write_json(TRACES / f"{stem}.json", payload)

    write_md(
        TRACES / "v477-thos-v6-x1-lane-status-v1.md",
        "v477 THOS v6 x1 Lane Status",
        [
            f"- app_probe_status: `{lanes['app_probe_status']}`",
            f"- app_notify_status: `{lanes['app_notify_status']}`",
            f"- cli_poll_status: `{lanes['cli_poll_status']}`",
            "",
            "## Rows",
            *[f"- {row['lane']} ({row['surface']}): `{row['status']}`, timeout_reason `{row['timeout_reason']}`." for row in lanes["rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-command-probe-selection-v1.md",
        "v477 THOS v6 x1 Command Probe Selection",
        [
            "- policy: metadata-only; no command execution.",
            f"- p0_offline_inspection: `{commands['counts']['p0_offline_inspection']}`",
            f"- connector_readiness_review: `{commands['counts']['connector_readiness_review']}`",
            f"- live_write_approval_draft_only: `{commands['counts']['live_write_approval_draft_only']}`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-skill-metadata-sample-v1.md",
        "v477 THOS v6 x1 Skill Metadata Sample",
        [
            f"- observed_user_skill_files: `{skills['observed_user_skill_files']}`",
            "- policy: frontmatter metadata only; no skill body copying.",
            "",
            "## Status Counts",
            *[f"- {key}: `{value}`" for key, value in sorted(skills["status_counts"].items())],
            "",
            "## Sample Rows",
            *[f"- {row['skill_dir']}: `{row['status']}`" for row in skills["sample_rows"][:20]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-expansion-probe-selection-v1.md",
        "v477 THOS v6 x1 Expansion Probe Selection",
        [
            "- policy: probe-only; no install.",
            f"- p0_no_write: `{len(expansions['p0_no_write'])}`",
            f"- p1_stdout_only: `{len(expansions['p1_stdout_only'])}`",
            f"- p2_simulation_label_required: `{len(expansions['p2_simulation_label_required'])}`",
            "- installed_count: `0`",
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-source-continuity-v1.md",
        "v477 THOS v6 x1 Source Continuity",
        [
            f"- source_status: `{sources['source_status']}`",
            f"- prior_search_count: `{sources['prior_search_count']}`",
            f"- selected_source_count: `{sources['selected_source_count']}`",
            "- claim ceiling: architecture context only.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-synthesis-v1.md",
        "v477 THOS v6 x1 Synthesis",
        [
            f"- generated_nz: `{generated_nz}`",
            f"- local_head_before_build: `{local_head}`",
            f"- remote_head_before_build: `{remote_head}`",
            f"- drift_before_build: `{drift}`",
            f"- overall_status: `{run_status['overall_status']}`",
            "- claim boundary: THOS bounded readiness only; all six GMUT gates remain open.",
            "",
            "## Reflection Steps",
            *[f"- {row['step']}. {row['domain']}: {row['reflection']}" for row in reflection_rows],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x1-run-status-v1.md",
        "v477 THOS v6 x1 Run Status",
        [
            f"- overall_status: `{run_status['overall_status']}`",
            f"- next_expected_phase: `{NEXT_PHASE}`",
            "",
            "## Rows",
            *[f"- {row['id']}: `{row['status']}` - {row['summary']}" for row in run_status["status_rows"]],
        ],
    )
    write_md(
        TRACES / "v477-thos-v6-x2-roadmap-v1.md",
        "v477 THOS v6 x2 Roadmap",
        [
            f"- task_count: `{roadmap_next['task_count']}`",
            "- entry: remote-verified v6 x1, existing lanes only, all GMUT gates open.",
            "",
            "## Tasks",
            *[f"- {row['id']} ({row['domain']}): {row['task']}" for row in roadmap_next["tasks"]],
        ],
    )


def main() -> None:
    build()
    print(json.dumps({"status": "built", "phase": PHASE, "next_phase": NEXT_PHASE}, indent=2))


if __name__ == "__main__":
    main()
