#!/usr/bin/env python3
"""Retry an existing Codex app lane by reading the thread then starting a turn directly.

This repair runner exists for the specific case where thread/read succeeds but
thread/resume repeatedly times out. It publishes status-only receipts and never
stores raw thread IDs, prompts, route payloads, or advisory text.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from thos_app_lane_completion_notifier import (
    AppServerClient,
    ROOT,
    TRACE_DIR,
    now_pair,
    prompt_for,
    selected_lanes,
    summarize_call,
    thread_id_digest,
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Direct App-Lane Turn-Start Retry",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- lane: `{payload['lane']}`",
        f"- read_status: `{payload['read'].get('status')}`",
        f"- turn_start_status: `{payload.get('turn_start', {}).get('status', 'not_started')}`",
        f"- completion_status: `{payload.get('turn_completion', {}).get('status', 'not_waited')}`",
        "- policy: existing thread only; direct turn-start retry after resume timeout; read-only sandbox; no raw transport publication.",
        "- boundary: no raw thread ID, route handle, prompt body, advisory text, app-server payload, credentials, screenshots, or local paths are published.",
        "- claim boundary: THOS app-lane retry only; GMUT, physics, consciousness, legal, and canon gates remain open.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run_lane(args: argparse.Namespace, lane: str, thread_id: str) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    client = AppServerClient()
    try:
        init = client.call(
            "initialize",
            {
                "clientInfo": {"name": "ghc-app-lane-direct-turn-start-retry", "version": "1.0"},
                "capabilities": {
                    "experimentalApi": True,
                    "optOutNotificationMethods": ["item/started", "item/completed", "thread/updated"],
                },
            },
            retries=1,
            timeout_seconds=args.call_timeout_seconds,
        )
        read = client.call(
            "thread/read",
            {"threadId": thread_id, "includeTurns": False},
            retries=args.retries,
            timeout_seconds=args.call_timeout_seconds,
        )
        payload: dict[str, Any] = {
            "artifact_type": "ghc_app_lane_direct_turn_start_retry",
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "phase_slug": args.phase_slug,
            "lane": lane,
            "thread_id_redacted": True,
            "thread_id_digest": thread_id_digest(thread_id),
            "existing_thread_only": True,
            "new_thread_created": False,
            "resume_attempted": False,
            "resume_skip_reason": "prior_read_ok_resume_timeout_open_gap",
            "read_only_sandbox_requested": True,
            "approval_policy_requested": "never",
            "init": summarize_call(init),
            "read": summarize_call(read),
            "publication_boundary": {
                "raw_thread_id_published": False,
                "raw_route_handle_published": False,
                "raw_prompt_body_published": False,
                "raw_advisory_text_published": False,
                "raw_app_server_payload_published": False,
                "credentials_published": False,
                "screen_capture_files_published": False,
                "local_absolute_paths_published": False,
            },
            "claim_boundary": {
                "scope": "THOS app-lane direct retry only",
                "gmut_empirical_closure": "not_claimed",
                "final_physics": "not_claimed",
                "consciousness_proof": "not_claimed",
                "legal_closure": "not_claimed",
                "canon_promotion": "not_claimed",
            },
        }
        if read.get("status") != "ok":
            payload["overall_status"] = "OPEN_GAP_DIRECT_TURN_READ_BLOCKED"
            return payload
        turn_start = client.call(
            "turn/start",
            {
                "threadId": thread_id,
                "input": [{"type": "text", "text": prompt_for(lane, args.phase_slug)}],
                "cwd": str(ROOT),
                "approvalPolicy": "never",
                "sandboxPolicy": {"type": "readOnly"},
            },
            retries=args.retries,
            timeout_seconds=args.call_timeout_seconds,
        )
        payload["turn_start"] = summarize_call(turn_start)
        if turn_start.get("status") != "ok":
            payload["overall_status"] = "OPEN_GAP_DIRECT_TURN_START_BLOCKED"
            return payload
        completion = client.wait_turn_completion(timeout_seconds=args.turn_timeout_seconds, retries=args.retries)
        payload["turn_completion"] = completion
        payload["overall_status"] = (
            "PASS_DIRECT_TURN_START_COMPLETED"
            if completion.get("status") == "completed"
            else "OPEN_GAP_DIRECT_TURN_COMPLETION_WAIT"
        )
        return payload
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--lane", required=True)
    parser.add_argument("--artifact-prefix", required=True)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--call-timeout-seconds", type=int, default=45)
    parser.add_argument("--turn-timeout-seconds", type=int, default=420)
    args = parser.parse_args()

    lanes = selected_lanes(args.lane)
    if args.lane not in lanes:
        raise SystemExit(f"lane not configured: {args.lane}")
    payload = run_lane(args, args.lane, lanes[args.lane])
    json_path = TRACE_DIR / f"{args.artifact_prefix}-v1.json"
    md_path = TRACE_DIR / f"{args.artifact_prefix}-v1.md"
    write_json(json_path, payload)
    write_md(md_path, payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": payload["phase_slug"], "lane": payload["lane"]}, indent=2))
    return 0 if str(payload["overall_status"]).startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
