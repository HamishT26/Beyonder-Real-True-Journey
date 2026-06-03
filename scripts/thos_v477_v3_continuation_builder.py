#!/usr/bin/env python3
"""Build sanitized v477 THOS v3 continuation receipts from notifier outputs."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v3_x1"


RECEIPTS = {
    "probe": "v477-thos-v2-x3-app-lane-notifier-probe-v1.json",
    "initial_run": "v477-thos-v2-x3-app-lane-notifier-run-v1.json",
    "retry_probe": "v477-thos-v2-x3-app-lane-notifier-retry-probe-v1.json",
    "aristotle_retry": "v477-thos-v2-x3-app-lane-notifier-aristotle-retry-v1.json",
    "kierkegaard_fresh_probe": "v477-thos-v2-x3-app-lane-notifier-kierkegaard-fresh-probe-v1.json",
    "kierkegaard_retry": "v477-thos-v2-x3-app-lane-notifier-kierkegaard-retry-v1.json",
}

V3_RECEIPTS = {
    "v3_probe": "v477-thos-v3-x1-app-lane-notifier-probe-v1.json",
    "v3_run": "v477-thos-v3-x1-app-lane-notifier-run-v1.json",
}


def run_git(args: list[str], default: str = "unknown") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return default


def read_json(name: str) -> dict:
    path = TRACES / name
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_optional_json(name: str) -> dict | None:
    path = TRACES / name
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(name: str, payload: dict) -> None:
    path = TRACES / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(name: str, body: str) -> None:
    (TRACES / name).write_text(body.strip() + "\n", encoding="utf-8")


def nz_now() -> tuple[str, str]:
    utc = dt.datetime.now(dt.timezone.utc)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12)))
    return utc.isoformat(timespec="seconds"), nz.isoformat(timespec="seconds")


def lane_status(receipt: dict, lane_name: str) -> dict:
    for lane in receipt.get("lanes", []):
        if lane.get("name") == lane_name:
            return {
                "name": lane_name,
                "receipt_status": receipt.get("overall_status"),
                "lane_status": lane.get("overall_status"),
                "read_status": lane.get("read", {}).get("status"),
                "resume_status": lane.get("resume", {}).get("status"),
                "turn_start_status": lane.get("turn_start", {}).get("status"),
                "turn_completion_status": lane.get("turn_completion", {}).get("status"),
            }
    return {"name": lane_name, "receipt_status": "missing", "lane_status": "missing"}


def build_tasks() -> list[dict]:
    domains = [
        ("app_lane_notifier", [
            "Run one probe-only pass before each new advisory turn.",
            "Use targeted retries rather than duplicate all-lane starts after a timeout.",
            "Record completion by lane, operation, attempt count, and bounded wait window.",
            "Keep unfiltered app-server events out of curated artifacts.",
            "Add stale-active-turn wording to every app-lane handoff.",
            "Prefer existing callable lanes and record blocker if only spawn tools are exposed.",
        ]),
        ("cli_lane_watchers", [
            "Refresh Arby and Aster read-only launcher health before heavy THOS delegation.",
            "Keep CLI lanes non-ephemeral and advisory-only.",
            "Record runtime duration, exit state, and sanitized blocker class.",
            "Separate CLI sandbox readiness from app-lane notifier readiness.",
            "Use watcher receipts so completed CLI reports do not require manual supervision.",
            "Avoid mutating advisory worktrees unless a separate exact approval exists.",
        ]),
        ("command_index_surface", [
            "Locate the current command book surface and its latest validation artifact.",
            "Create a compact command-index manifest for workbench discovery.",
            "Mark missing command surfaces as open gaps, not failures.",
            "Link each command to source, owner, safety level, and validation status.",
            "Keep executable examples bounded and non-destructive.",
            "Add a drift receipt when command metadata points to stale files.",
        ]),
        ("v54_v55_handoff", [
            "Locate v54 and v55 handoff packs without broad importing old archives.",
            "Create surfaced handoff receipts with title, status, and next receiver.",
            "Mark unavailable handoffs as source gaps with search paths omitted from publication.",
            "Cross-reference Orun continuity only as routing context.",
            "Do not promote handoff material into canon by assertion.",
            "Add handoff acceptance criteria for v478 continuation.",
        ]),
        ("skill_and_system_readiness", [
            "Scan skill frontmatter health only through approved non-mutating checks.",
            "Separate skill-loader repairs from THOS design artifacts.",
            "Build a skill capability index from metadata, not full skill body dumps.",
            "Flag duplicate or ambiguous skill names for later exact-path review.",
            "Add a no-plugin-cache-mutation marker to ordinary THOS phases.",
            "Create a skills-to-phase routing map for v478 and v479.",
        ]),
        ("source_refresh_and_research", [
            "Use official sources first for Codex, MCP, OpenAI Agents, NVIDIA, and cloud systems.",
            "Record source refresh as completed only after live page review.",
            "Separate journey_context_not_canon from evidence and implementation sources.",
            "Prefer source ledgers over large copied notes.",
            "Add citation-required flags to claims that depend on current product behavior.",
            "Keep search counts as process metadata rather than truth claims.",
        ]),
        ("drive_github_continuity", [
            "Use Google Drive v49 as journey context only, not physics validation.",
            "Keep GitHub remote verification authoritative for repo state.",
            "Avoid publishing restricted connector payloads into repo artifacts.",
            "Record Drive/GitHub source titles without large copied passages.",
            "Add continuity pointers for v49 to v477 without claiming full import.",
            "Keep absolute local paths out of public-facing summaries where possible.",
        ]),
        ("thos_safety_and_validation", [
            "Validate every JSON artifact before staging.",
            "Compile every new helper script before staging.",
            "Run secret, session, screen-capture, and restricted-material guards on staged files.",
            "Use exact staging only, never broad staging.",
            "Fetch and drift-check before every push.",
            "Verify remote equals local after publication.",
        ]),
        ("gmut_boundary", [
            "Keep all six GMUT gates open unless exact closure artifacts exist.",
            "Classify GMUT-adjacent THOS work as support infrastructure, not validation.",
            "Label Journey and Solas material as journey_context_not_canon.",
            "Avoid fifth-force safety, consciousness proof, or final physics claims.",
            "Preserve null, SI, conservation, baseline, equivalence, and bridge ledgers as open.",
            "Use simulation labels for any toy or fixture outputs.",
        ]),
        ("phase_management", [
            "Timestamp every x-session start and closeout in NZ time.",
            "Allow x3 or x4 overlays only for concrete blockers or hardening work.",
            "Commit every second phase where feasible and safe.",
            "Publish blocker receipts instead of forcing closure.",
            "Hand off a 60-task roadmap after each x2 or overlay closeout.",
            "Keep v477 moving toward v478 only after five-lane readiness is confirmed.",
        ]),
    ]
    tasks: list[dict] = []
    task_id = 1
    for domain, items in domains:
        for item in items:
            tasks.append({"id": f"v477-v3-task-{task_id:02d}", "domain": domain, "task": item})
            task_id += 1
    return tasks


def main() -> None:
    utc, nz = nz_now()
    receipts = {key: read_json(name) for key, name in RECEIPTS.items()}
    v3_receipts = {key: read_optional_json(name) for key, name in V3_RECEIPTS.items()}
    head = run_git(["rev-parse", "HEAD"])
    remote = run_git(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = run_git(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    lane_state = [
        {
            "name": "Cicero",
            "read_resume_probe": "PASS",
            "advisory_turn": "completed",
            "evidence_receipt": RECEIPTS["initial_run"],
            "next_use": "available_for_v477_v3_followup",
        },
        {
            "name": "Kierkegaard",
            "read_resume_probe": "PASS_AFTER_FRESH_PROBE",
            "advisory_turn": "completed_after_targeted_retry",
            "evidence_receipts": [
                RECEIPTS["kierkegaard_fresh_probe"],
                RECEIPTS["kierkegaard_retry"],
            ],
            "next_use": "available_for_v477_v3_followup_with_probe_before_duplicate_turns",
        },
        {
            "name": "Aristotle",
            "read_resume_probe": "PASS",
            "advisory_turn": "completed_after_targeted_retry",
            "evidence_receipt": RECEIPTS["aristotle_retry"],
            "next_use": "available_for_v477_v3_followup",
        },
    ]

    consolidated = {
        "generated_utc": utc,
        "generated_nz": nz,
        "phase": "v477_thos_v2_x3",
        "artifact_type": "app_lane_notifier_consolidated_handoff",
        "overall_status": "PASS_APP_LANES_RECONNECTED",
        "source_receipts": list(RECEIPTS.values()),
        "policy": {
            "existing_threads_only": True,
            "new_threads_created": False,
            "old_style_subagent_spawn_used": False,
            "unfiltered_event_stream_published": False,
            "retry_attempts_per_operation": 5,
        },
        "lane_state": lane_state,
        "notifier_runner": {
            "script": "scripts/thos_v477_app_lane_notifier_runner.py",
            "supports_probe_only": True,
            "supports_targeted_lanes": True,
            "supports_skip_start_if_active": True,
            "stream_encoding": "utf-8_replace",
            "writes_sanitized_receipts_only": True,
        },
        "claim_boundary": {
            "domain": "THOS app-lane notifier and reconnect coordination",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
        "next_expected_phase": PHASE,
    }
    write_json("v477-thos-v2-x3-app-lane-notifier-consolidated-v1.json", consolidated)
    write_md(
        "v477-thos-v2-x3-app-lane-notifier-consolidated-v1.md",
        f"""
# V477 THOS V2 X3 App-Lane Notifier Consolidated Handoff

- generated_nz: `{nz}`
- overall_status: `PASS_APP_LANES_RECONNECTED`
- policy: existing app threads only; no new threads; no old-style subagent spawning; no unfiltered app-server event stream publication.
- runner: `scripts/thos_v477_app_lane_notifier_runner.py`
- claim boundary: THOS app-lane notifier and reconnect coordination only; all GMUT gates remain open.

## Reconnection State

- Cicero: read/resume probe passed; advisory turn completed in the bounded notifier run.
- Kierkegaard: initial bounded run started a turn but did not observe completion; a fresh probe passed and the targeted retry then completed.
- Aristotle: first full-run read was blocked after the Kierkegaard timeout; targeted retry completed successfully.

## Runner Capabilities

- Supports `--probe-only` to read/resume lanes without sending a new advisory turn.
- Supports `--lanes Cicero,Kierkegaard,Aristotle` filtering for targeted retries.
- Supports `--skip-start-if-active` for safer follow-up when a lane may already have a live turn.
- Retries each app-server operation up to the configured retry count, defaulting to five attempts.
- Writes sanitized JSON/Markdown receipts only and does not persist unfiltered app-server event streams.

## Next Use

- Run a probe-only notifier check before opening duplicate app-lane turns.
- Use targeted retries when one lane times out instead of restarting all three app lanes.
- Treat all three app lanes as available for `v477_thos_v3_x1` advisory follow-up.
""",
    )

    app_lane_details = [
        lane_status(receipts["initial_run"], "Cicero"),
        lane_status(receipts["kierkegaard_fresh_probe"], "Kierkegaard"),
        lane_status(receipts["kierkegaard_retry"], "Kierkegaard"),
        lane_status(receipts["aristotle_retry"], "Aristotle"),
    ]
    fresh_v3_lane_details = []
    if v3_receipts.get("v3_run"):
        fresh_v3_lane_details = [
            lane_status(v3_receipts["v3_run"], "Cicero"),
            lane_status(v3_receipts["v3_run"], "Kierkegaard"),
            lane_status(v3_receipts["v3_run"], "Aristotle"),
        ]
    v3_run_passed = bool(v3_receipts.get("v3_run") and v3_receipts["v3_run"].get("overall_status") == "PASS")
    readiness = {
        "generated_utc": utc,
        "generated_nz": nz,
        "phase": PHASE,
        "artifact_type": "five_lane_readiness_receipt",
        "overall_status": "PASS_FIVE_LANE_READY_AFTER_V3_APP_RUN" if v3_run_passed else "PASS_WITH_CLI_LANES_READ_ONLY",
        "repo_state": {
            "local_head": head,
            "shared_remote_head": remote,
            "drift": drift,
        },
        "app_lanes": {
            "transport": "local_app_server_stdio",
            "existing_threads_only": True,
            "notifier_runner": "scripts/thos_v477_app_lane_notifier_runner.py",
            "fresh_v3_probe_receipt": V3_RECEIPTS["v3_probe"] if v3_receipts.get("v3_probe") else None,
            "fresh_v3_run_receipt": V3_RECEIPTS["v3_run"] if v3_receipts.get("v3_run") else None,
            "fresh_v3_run_status": v3_receipts["v3_run"].get("overall_status") if v3_receipts.get("v3_run") else "not_run_by_builder",
            "details": app_lane_details,
            "fresh_v3_details": fresh_v3_lane_details,
            "summary": lane_state,
        },
        "cli_lanes": [
            {
                "name": "Arby",
                "transport": "codex_cli_non_ephemeral_read_only",
                "current_phase_role": "advisory_only",
                "readiness_status": "known_lane_available_pending_next_runtime_receipt",
                "watcher_policy": "use bounded completion watcher and sanitized receipt",
            },
            {
                "name": "Aster Vale",
                "transport": "codex_cli_non_ephemeral_read_only",
                "current_phase_role": "advisory_only",
                "readiness_status": "known_lane_available_pending_next_runtime_receipt",
                "watcher_policy": "use bounded completion watcher and sanitized receipt",
            },
        ],
        "source_context": {
            "journey_context_not_canon": [
                "Beyonder-Real-True Journey v49 is useful for continuity routing and prior phase history.",
                "Journey material must not validate GMUT, close gates, or prove consciousness.",
            ],
            "official_source_refresh_queue": [
                "OpenAI Codex Windows sandbox guidance",
                "Codex app-server protocol source",
                "Model Context Protocol specification",
                "OpenAI Agents SDK documentation",
                "NVIDIA current AI infrastructure and model pages",
            ],
            "completion_claim": "queued_for_v477_v3_source_refresh_not_claimed_complete_by_this_builder",
        },
        "claim_boundary": {
            "thos_scope": "lane coordination, notifier readiness, command surface planning, and validation workflow",
            "gmut_gate_state": "all_six_gmut_gates_open",
            "canon_promotion": "not_claimed",
        },
        "next_expected_phase": "v477_thos_v3_x1",
    }
    write_json("v477-thos-v3-x1-five-lane-readiness-v1.json", readiness)
    readiness_status = "PASS_FIVE_LANE_READY_AFTER_V3_APP_RUN" if v3_run_passed else "PASS_WITH_CLI_LANES_READ_ONLY"
    write_md(
        "v477-thos-v3-x1-five-lane-readiness-v1.md",
        f"""
# V477 THOS V3 X1 Five-Lane Readiness

- generated_nz: `{nz}`
- overall_status: `{readiness_status}`
- local_head: `{head}`
- shared_remote_head: `{remote}`
- drift: `{drift}`

## App-Lane Readiness

- Cicero is reconnected through the local app-server notifier and completed the bounded advisory turn.
- Kierkegaard is reconnected through the local app-server notifier after a fresh probe and targeted retry.
- Aristotle is reconnected through the local app-server notifier after a targeted retry.
- Fresh v477 v3 probe/live notifier receipts: `{V3_RECEIPTS['v3_probe']}` and `{V3_RECEIPTS['v3_run']}`.
- Fresh v477 v3 live notifier status: `{"PASS" if v3_run_passed else "not confirmed by this builder"}`.
- The app-lane runner uses existing threads only, creates no new threads, and does not use old-style subagent spawning.

## CLI-Lane Readiness

- Arby remains an existing non-ephemeral read-only CLI advisory lane for THOS/GMUT support.
- Aster Vale remains an existing non-ephemeral read-only CLI advisory lane for THOS/GMUT support.
- The next runtime pass should use a bounded watcher receipt for each CLI lane, recording duration, completion state, and sanitized blocker class.

## Source And Claim Boundaries

- Journey material, including v49 continuity context, is `journey_context_not_canon`.
- Official source refresh is queued for v477 v3; this file does not claim that those searches are complete.
- All six GMUT gates remain open: null recovery, dimensional/SI consistency, conservation or exchange law, baseline recovery, fifth-force/equivalence constraints, and consciousness measurement bridge.
""",
    )

    roadmap = {
        "generated_utc": utc,
        "generated_nz": nz,
        "phase": PHASE,
        "artifact_type": "thos_60_task_roadmap",
        "overall_status": "READY_FOR_V477_THOS_V3_X1",
        "task_count": 60,
        "tasks": build_tasks(),
        "acceptance_criteria": [
            "Every new or updated JSON artifact parses.",
            "Every new helper script compiles.",
            "Staged files pass secret, session, screen-capture, restricted-material, and path-safety guards.",
            "No raw app-lane, CLI-lane, or connector payloads are published.",
            "No new old-style subagents are spawned.",
            "Remote verification equals local after each publication.",
        ],
        "next_expected_phase": "v477_thos_v3_x1",
    }
    write_json("v477-thos-v3-x1-thos-roadmap-v1.json", roadmap)
    write_md(
        "v477-thos-v3-x1-thos-roadmap-v1.md",
        "\n".join(
            [
                "# V477 THOS V3 X1 Roadmap",
                "",
                f"- generated_nz: `{nz}`",
                "- overall_status: `READY_FOR_V477_THOS_V3_X1`",
                "- task_count: `60`",
                "",
                "## Tasks",
                "",
                *[
                    f"- {task['id']} [{task['domain']}]: {task['task']}"
                    for task in build_tasks()
                ],
                "",
                "## Acceptance Criteria",
                "",
                "- Every new or updated JSON artifact parses.",
                "- Every new helper script compiles.",
                "- Staged files pass secret, session, screen-capture, restricted-material, and path-safety guards.",
                "- No unfiltered app-lane, CLI-lane, or connector payloads are published.",
                "- No new old-style subagents are spawned.",
                "- Remote verification equals local after each publication.",
            ]
        ),
    )


if __name__ == "__main__":
    main()
