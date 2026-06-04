#!/usr/bin/env python3
"""Build a status-only stale-flow refresh receipt from curated THOS artifacts."""

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
        return {"available": False, "receipt": name}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"available": False, "receipt": name}


def status_of(payload: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = payload.get(key)
        if value is not None:
            return str(value)
    return "missing"


def classify_flows(phase_slug: str, threshold: int) -> list[dict[str, Any]]:
    background = read_json(f"{phase_slug}-background-sibling-notifier-runner-v1.json")
    multiplex = read_json(f"{phase_slug}-local-multiplex-tui-app-server-runner-v1.json")
    fix = read_json(f"{phase_slug}-fix-enhancement-updater-runner-v1.json")
    skill_receipt = read_json(f"{phase_slug}-live-skill-evolution-receipt-v1.json")
    lane_board = read_json(f"{phase_slug}-lane-retry-status-board-v1.json")
    flows: list[dict[str, Any]] = []

    cli_attempts = lane_board.get("cli_retry_rows", [])
    cli_open_attempts = [
        row for row in cli_attempts if str(row.get("aggregate_status", "")).startswith("OPEN_GAP")
    ]
    if cli_open_attempts:
        flows.append(
            {
                "id": "STALE-CLI-FINAL-MARKER",
                "surface": "cli_final_marker_contract",
                "status": "stale_open",
                "observed_count": len(cli_open_attempts),
                "threshold": threshold,
                "notify_aletheon": len(cli_open_attempts) >= threshold,
                "evidence": "curated retry board shows repeated open final-marker attempts",
                "next_action": "keep watcher status-only; improve marker contract or request exact lane mutation approval",
            }
        )

    if status_of(background, "overall_status") == "APP_DONE_CLI_FINAL_MARKER_OPEN":
        flows.append(
            {
                "id": "STALE-BACKGROUND-PARTIAL",
                "surface": "background_sibling_notifier",
                "status": "partial_open",
                "observed_count": 1,
                "threshold": threshold,
                "notify_aletheon": True,
                "evidence": "background notifier completed app lanes while CLI final markers remained open",
                "next_action": "preserve split app/CLI status and continue other approved work",
            }
        )

    if status_of(multiplex, "overall_status") == "APP_READY_CLI_OPEN":
        flows.append(
            {
                "id": "STALE-MULTIPLEX-CLI-OPEN",
                "surface": "multiplex_status_board",
                "status": "visible_open",
                "observed_count": 1,
                "threshold": threshold,
                "notify_aletheon": True,
                "evidence": "multiplex board displays app readiness with CLI lanes still open",
                "next_action": "keep board active and route repair planning through Fix-Enhancement Updater",
            }
        )

    fix_issues = fix.get("issues", [])
    open_fix_issues = [row for row in fix_issues if row.get("status") == "open"]
    if open_fix_issues:
        flows.append(
            {
                "id": "STALE-FIX-ENHANCEMENT-OPEN-ISSUES",
                "surface": "fix_enhancement_updater",
                "status": "plan_ready_open",
                "observed_count": len(open_fix_issues),
                "threshold": threshold,
                "notify_aletheon": True,
                "evidence": "fix-enhancement receipt retains open issue rows for approved repair planning",
                "next_action": "convert repeated open rows into exact packet tasks or bounded runner changes",
            }
        )

    if skill_receipt.get("verification", {}).get("matches_approved_draft") is True:
        flows.append(
            {
                "id": "READY-SKILL-EVOLUTION",
                "surface": "multi_agent_orchestrator_skill",
                "status": "ready_verified",
                "observed_count": 1,
                "threshold": threshold,
                "notify_aletheon": False,
                "evidence": "live skill evolution receipt verifies draft match and frontmatter",
                "next_action": "use evolved skill rules for future sibling-lane orchestration",
            }
        )

    if not flows:
        flows.append(
            {
                "id": "READY-NO-STALE-FLOWS",
                "surface": "phase_status",
                "status": "ready",
                "observed_count": 0,
                "threshold": threshold,
                "notify_aletheon": False,
                "evidence": "no stale-flow signals found in curated receipts",
                "next_action": "continue phase progression",
            }
        )
    return flows


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    flows = classify_flows(args.phase_slug, args.threshold)
    stale = [row for row in flows if row["status"] in {"stale_open", "partial_open", "visible_open", "plan_ready_open"}]
    payload = {
        "artifact_type": "stale_flow_refresh_runner",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "threshold": args.threshold,
        "overall_status": "STALE_FLOWS_DETECTED" if stale else "READY_NO_STALE_FLOWS",
        "notify_aletheon": any(row["notify_aletheon"] for row in flows),
        "flow_count": len(flows),
        "stale_flow_count": len(stale),
        "flows": flows,
        "policy": {
            "status_only": True,
            "live_lane_mutation_performed": False,
            "new_thread_created": False,
            "old_style_subagent_spawned": False,
            "external_account_changed": False,
        },
        "claim_boundary": {
            "scope": "stale-flow detection and next-action planning",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    write_json(TRACE_DIR / f"{args.receipt_prefix}-v1.json", payload)
    write_md(TRACE_DIR / f"{args.receipt_prefix}-v1.md", payload)
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Stale Flow Refresh Runner",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- notify_aletheon: `{str(payload['notify_aletheon']).lower()}`",
        f"- stale_flow_count: `{payload['stale_flow_count']}`",
        "- policy: status-only; no live lane mutation; no new threads; no old-style spawning.",
        "- claim boundary: stale-flow planning only; all GMUT gates remain open.",
        "",
        "## Flow Rows",
    ]
    for row in payload["flows"]:
        lines.append(
            f"- `{row['id']}` / `{row['status']}`: {row['evidence']} Next action: {row['next_action']}."
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", default="v478-thos-v12-x1")
    parser.add_argument("--threshold", type=int, default=3)
    parser.add_argument("--receipt-prefix", default="v478-thos-v12-x1-stale-flow-refresh-runner")
    return parser.parse_args()


def main() -> None:
    payload = build_payload(parse_args())
    print(json.dumps({"status": payload["overall_status"], "notify_aletheon": payload["notify_aletheon"]}, sort_keys=True))


if __name__ == "__main__":
    main()
