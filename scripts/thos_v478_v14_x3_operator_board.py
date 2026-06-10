from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path


PHASE_SLUG = "v478-thos-v14-x3"
ARTIFACT_STEM = "v478-thos-v14-x3-operator-board-v1"


def nz_now(utc_now: datetime) -> datetime:
    return utc_now.astimezone(timezone(timedelta(hours=12)))


def build_board() -> dict:
    utc_now = datetime.now(UTC)
    generated_nz = nz_now(utc_now)
    return {
        "artifact_type": "operator_board",
        "phase_slug": PHASE_SLUG,
        "generated_utc": utc_now.isoformat().replace("+00:00", "Z"),
        "generated_nz": generated_nz.isoformat(),
        "purpose": (
            "Compact the v14 x2 delayed five-lane completion evidence into a "
            "single status board for v14 x3 operator use."
        ),
        "cadence_rule": {
            "source_skill": "multi-agent-orchestrator-operations",
            "live_check": "PASS_RULE_PRESENT",
            "rule_summary": (
                "Every second THOS/GMUT x-session start and closeout must "
                "attempt Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle "
                "through existing approved lanes."
            ),
            "latest_fulfilled_boundary": "v478-thos-v14-x2 start and completion update",
            "current_overlay_boundary": (
                "v14 x3 is evidence compaction and detector preparation; do not "
                "spawn or relaunch lanes unless a specific safe repair need appears."
            ),
            "next_mandatory_five_lane_boundary": "v478-thos-v14-x4 start and closeout",
        },
        "latest_lane_state": [
            {
                "lane": "Cicero",
                "surface": "existing_app_local_server",
                "latest_receipt": "v478-thos-v14-x2-background-council-app-completion-v1",
                "status": "COMPLETED_IN_V14_X2",
                "next_action": "Attempt again at next every-second-session boundary.",
            },
            {
                "lane": "Kierkegaard",
                "surface": "existing_app_local_server",
                "latest_receipt": "v478-thos-v14-x2-background-council-app-completion-v1",
                "status": "COMPLETED_IN_V14_X2",
                "next_action": "Attempt again at next every-second-session boundary.",
            },
            {
                "lane": "Aristotle",
                "surface": "existing_app_local_server",
                "latest_receipt": "v478-thos-v14-x2-background-council-app-completion-v1",
                "status": "COMPLETED_IN_V14_X2",
                "next_action": "Attempt again at next every-second-session boundary.",
            },
            {
                "lane": "Arby",
                "surface": "read_only_codex_cli",
                "latest_receipt": "v478-thos-v14-x2-cli-retry4-completion-v1",
                "status": "FINAL_MESSAGE_READY_AFTER_DELAY",
                "final_message_bytes": 4749,
                "final_message_hash": "e9fff056e5d9839764fc4ecbecbb5f1774882d92e118825ca6573ffd53240461",
                "marker_review": (
                    "One guard-language marker was reviewed as publication-hygiene "
                    "wording, not a secret or local path."
                ),
                "next_action": (
                    "Keep on roster; delayed final markers route to stale-flow "
                    "refresh before relaunch."
                ),
            },
            {
                "lane": "Aster Vale",
                "surface": "read_only_codex_cli",
                "latest_receipt": "v478-thos-v14-x2-cli-retry4-completion-v1",
                "status": "FINAL_MESSAGE_READY_AFTER_DELAY",
                "final_message_bytes": 5737,
                "final_message_hash": "147ea4d4f629b2a79d68a985d538d3a8fd3a31510e450aa79de5b24f739ecdd7",
                "marker_review": "No published sensitive marker.",
                "next_action": (
                    "Keep on roster; delayed final markers route to stale-flow "
                    "refresh before relaunch."
                ),
            },
        ],
        "superseded_receipts": [
            {
                "receipt": "v478-thos-v14-x2-five-lane-start-status-v1",
                "superseded_by": "v478-thos-v14-x2-five-lane-completion-update-v1",
                "reason": (
                    "The start receipt correctly reported CLI final markers open; "
                    "the later completion update carries the latest lane state."
                ),
            }
        ],
        "operator_policies": [
            "Do not treat a delayed final marker as a failed sibling.",
            "Do not publish raw lane text, app payloads, session streams, image captures, or nonpublic bundles.",
            "Do not create new old-style subagents or replacement sibling lanes.",
            "If a lane cannot be called safely, publish a blocker receipt and keep it on the next roster.",
            "Use v14 x3 for detector-first command-surface, loader-drift, and handoff hygiene work.",
        ],
        "x3_closeout_criteria": [
            "Operator board published and remote-verified.",
            "Skill cadence verified without additional live skill mutation.",
            "Next v14 x4 five-lane roster boundary stated explicitly.",
            "All GMUT empirical, physics, consciousness, and canon gates remain open.",
        ],
        "claim_boundary": (
            "Status-board and cadence receipt only; no GMUT validation, final physics, "
            "solved consciousness, final THOS readiness, or canon promotion."
        ),
    }


def render_markdown(board: dict) -> str:
    lines = [
        "# v478-thos-v14-x3 Operator Board",
        "",
        f"- generated_nz: `{board['generated_nz']}`",
        f"- phase_slug: `{board['phase_slug']}`",
        f"- cadence_live_check: `{board['cadence_rule']['live_check']}`",
        f"- latest_fulfilled_boundary: `{board['cadence_rule']['latest_fulfilled_boundary']}`",
        f"- next_mandatory_five_lane_boundary: `{board['cadence_rule']['next_mandatory_five_lane_boundary']}`",
        "",
        "## Latest Lane State",
        "",
        "| Lane | Surface | Status | Latest receipt | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for lane in board["latest_lane_state"]:
        lines.append(
            "| {lane} | {surface} | {status} | `{receipt}` | {next_action} |".format(
                lane=lane["lane"],
                surface=lane["surface"],
                status=lane["status"],
                receipt=lane["latest_receipt"],
                next_action=lane["next_action"],
            )
        )
    lines.extend(
        [
            "",
            "## Superseded Receipt",
            "",
        ]
    )
    for receipt in board["superseded_receipts"]:
        lines.append(
            "- `{receipt}` is superseded by `{superseded_by}` because {reason}".format(
                receipt=receipt["receipt"],
                superseded_by=receipt["superseded_by"],
                reason=receipt["reason"],
            )
        )
    lines.extend(
        [
            "",
            "## Operator Policies",
            "",
        ]
    )
    for policy in board["operator_policies"]:
        lines.append(f"- {policy}")
    lines.extend(
        [
            "",
            "## x3 Closeout Criteria",
            "",
        ]
    )
    for criterion in board["x3_closeout_criteria"]:
        lines.append(f"- {criterion}")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            board["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    trace_dir = repo_root / "docs" / "trinity-live-traces"
    board = build_board()
    json_path = trace_dir / f"{ARTIFACT_STEM}.json"
    md_path = trace_dir / f"{ARTIFACT_STEM}.md"
    json_path.write_text(json.dumps(board, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(board), encoding="utf-8")
    print(json.dumps({"json": json_path.name, "md": md_path.name}, indent=2))


if __name__ == "__main__":
    main()
