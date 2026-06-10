#!/usr/bin/env python3
"""Run sanitized v477 THOS app-lane notifier checks through local app-server."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import queue
import subprocess
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE_DEFAULT = "v477_thos_v2_x3"
LANES = {
    "Cicero": "019e485f-172b-72c0-adf7-27daea722143",
    "Kierkegaard": "019e485f-1aa5-7c31-b578-748091f7e319",
    "Aristotle": "019e5158-28ef-75b1-a3f5-563bb358e44e",
}
PROMPTS = {
    "Cicero": (
        "Existing Cicero advisory lane reconnect for v477 THOS. Provide an advisory-only report: "
        "publication guardrails, command/watch surface risks, app-lane reconnect risks, and 10 concrete "
        "Eureka tasks. Do not edit files. Keep all GMUT gates open and make no final physics or canon claims."
    ),
    "Kierkegaard": (
        "Existing Kierkegaard advisory lane reconnect for v477 THOS. Provide an advisory-only report: "
        "humility and overclaim boundaries, local-data handling boundaries, Journey context as non-canon, and 10 "
        "concrete Eureka tasks. Do not edit files. Keep all GMUT gates open and make no final physics or canon claims."
    ),
    "Aristotle": (
        "Existing Aristotle advisory lane reconnect for v477 THOS. Provide an advisory-only report: validator "
        "status taxonomy, blocker dominance rules, watcher/notifier acceptance criteria, and 10 concrete Eureka "
        "tasks. Do not edit files. Keep all GMUT gates open and make no final physics or canon claims."
    ),
}


class AppServerClient:
    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            ["cmd", "/c", "codex", "app-server", "--stdio"],
            cwd=str(ROOT),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        self.stdout: queue.Queue[str] = queue.Queue()
        self.stderr: queue.Queue[str] = queue.Queue()
        self.next_id = 1
        threading.Thread(target=self._reader, args=(self.proc.stdout, self.stdout), daemon=True).start()
        threading.Thread(target=self._reader, args=(self.proc.stderr, self.stderr), daemon=True).start()

    @staticmethod
    def _reader(stream, target: queue.Queue[str]) -> None:
        for line in stream:
            target.put(line)

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def request(self, method: str, params: dict) -> int:
        if self.proc.stdin is None:
            raise RuntimeError("app server stdin unavailable")
        request_id = self.next_id
        self.next_id += 1
        payload = {"id": request_id, "method": method, "params": params}
        self.proc.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        return request_id

    def wait_response(self, request_id: int, timeout_seconds: int) -> tuple[dict | None, list[str]]:
        deadline = time.time() + timeout_seconds
        observed: list[str] = []
        while time.time() < deadline:
            try:
                line = self.stdout.get(timeout=0.5).strip()
            except queue.Empty:
                continue
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                observed.append("non_json_line")
                continue
            method = message.get("method")
            if method:
                observed.append(method)
            if message.get("id") == request_id:
                return message, observed
        return None, observed

    def call(self, method: str, params: dict, *, attempts: int, timeout_seconds: int) -> dict:
        failures = []
        for attempt in range(1, attempts + 1):
            request_id = self.request(method, params)
            response, observed = self.wait_response(request_id, timeout_seconds)
            if response and "result" in response:
                return {
                    "status": "ok",
                    "attempt": attempt,
                    "observed_methods": sorted(set(observed))[:16],
                    "result_keys": sorted(response.get("result", {}).keys())
                    if isinstance(response.get("result"), dict)
                    else [],
                }
            message = None
            if response and isinstance(response.get("error"), dict):
                message = response["error"].get("message")
            failures.append(
                {
                    "attempt": attempt,
                    "status": "timeout" if response is None else "error",
                    "message_class": classify_message(message),
                    "observed_methods": sorted(set(observed))[:16],
                }
            )
            time.sleep(min(attempt, 3))
        return {"status": "failed", "failures": failures}

    def wait_turn_completion(self, *, timeout_seconds: int, attempts: int) -> dict:
        all_methods: list[str] = []
        assistant_signal = False
        per_attempt = max(1, timeout_seconds // max(1, attempts))
        for attempt in range(1, attempts + 1):
            deadline = time.time() + per_attempt
            while time.time() < deadline:
                try:
                    line = self.stdout.get(timeout=0.5).strip()
                except queue.Empty:
                    continue
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    all_methods.append("non_json_line")
                    continue
                method = message.get("method")
                if method:
                    all_methods.append(method)
                compact = json.dumps(message, separators=(",", ":"))[:1200].lower()
                if "assistant" in compact and any(
                    marker in compact for marker in ("guard", "boundary", "validator", "eureka", "blocker")
                ):
                    assistant_signal = True
                if method == "turn/completed":
                    return {
                        "status": "completed",
                        "attempt": attempt,
                        "observed_methods": sorted(set(all_methods))[:24],
                        "assistant_signal_observed": assistant_signal,
                    }
            all_methods.append("completion_wait_window_elapsed")
        return {
            "status": "timeout",
            "attempts": attempts,
            "observed_methods": sorted(set(all_methods))[:24],
            "assistant_signal_observed": assistant_signal,
        }


def classify_message(message: str | None) -> str:
    if not message:
        return "none"
    lowered = message.lower()
    if "not found" in lowered:
        return "not_found"
    if "active turn" in lowered or "cannot accept" in lowered:
        return "active_turn"
    if "permission" in lowered or "approval" in lowered:
        return "approval_or_permission"
    if "timeout" in lowered:
        return "timeout"
    return "other"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def git_text(args: list[str], timeout_seconds: int = 20) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_seconds,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout)
    return proc.stdout.strip()


def selected_lanes(lane_arg: str) -> dict[str, str]:
    if lane_arg.strip().lower() in {"all", "*"}:
        return dict(LANES)
    wanted = {part.strip() for part in lane_arg.split(",") if part.strip()}
    unknown = sorted(wanted - set(LANES))
    if unknown:
        raise ValueError(f"unknown lane name(s): {', '.join(unknown)}")
    return {name: LANES[name] for name in LANES if name in wanted}


def safe_thread_status(call: dict) -> str | None:
    if call.get("status") != "ok":
        return None
    response = call.get("response") or {}
    thread = response.get("result", {}).get("thread", {})
    status = thread.get("status")
    if isinstance(status, str):
        return status
    if isinstance(status, dict):
        return status.get("type") or status.get("status") or "structured"
    return None


def run_notifier(args: argparse.Namespace) -> dict:
    now_utc = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    # NZST is UTC+12 for this June 2026 run; avoid requiring the optional Windows tzdata package.
    nz_tz = dt.timezone(dt.timedelta(hours=12), name="NZST")
    now_nz = dt.datetime.now(nz_tz).replace(microsecond=0).isoformat()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = git_text(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    client = AppServerClient()
    lanes = []
    try:
        init = client.call(
            "initialize",
            {
                "clientInfo": {"name": "ghc-v477-app-lane-notifier", "version": "1.0"},
                "capabilities": {
                    "experimentalApi": True,
                    "optOutNotificationMethods": [
                        "item/started",
                        "item/completed",
                        "thread/updated",
                    ],
                },
            },
            attempts=1,
            timeout_seconds=args.call_timeout_seconds,
        )
        for lane_name, thread_id in selected_lanes(args.lanes).items():
            lane = {
                "name": lane_name,
                "thread_id": thread_id,
                "prompt_kind": "v477_thos_advisory_only",
                "raw_stream_published": False,
            }
            read = client.call(
                "thread/read",
                {"threadId": thread_id, "includeTurns": False},
                attempts=args.retries,
                timeout_seconds=args.call_timeout_seconds,
            )
            lane["read"] = summarize_call(read)
            lane["thread_status_at_read"] = safe_thread_status(read)
            if read["status"] != "ok":
                lane["overall_status"] = "blocked_read"
                lanes.append(lane)
                continue
            resume = client.call(
                "thread/resume",
                {
                    "threadId": thread_id,
                    "excludeTurns": True,
                    "sandbox": "read-only",
                    "approvalPolicy": "never",
                    "cwd": str(ROOT),
                },
                attempts=args.retries,
                timeout_seconds=args.call_timeout_seconds,
            )
            lane["resume"] = summarize_call(resume)
            lane["thread_status_after_resume"] = safe_thread_status(resume)
            if resume["status"] != "ok":
                lane["overall_status"] = "blocked_resume"
                lanes.append(lane)
                continue
            if args.skip_start_if_active and lane.get("thread_status_after_resume") not in {None, "idle"}:
                lane["overall_status"] = "resume_ok_start_skipped_non_idle"
                lanes.append(lane)
                continue
            if args.probe_only:
                lane["overall_status"] = "read_resume_ok_probe_only"
                lanes.append(lane)
                continue
            turn = client.call(
                "turn/start",
                {
                    "threadId": thread_id,
                    "input": [{"type": "text", "text": PROMPTS[lane_name]}],
                    "cwd": str(ROOT),
                    "approvalPolicy": "never",
                    "sandboxPolicy": {"type": "readOnly"},
                },
                attempts=args.retries,
                timeout_seconds=args.call_timeout_seconds,
            )
            lane["turn_start"] = summarize_call(turn)
            if turn["status"] != "ok":
                lane["overall_status"] = "blocked_turn_start"
                lanes.append(lane)
                continue
            completion = client.wait_turn_completion(
                timeout_seconds=args.turn_timeout_seconds,
                attempts=args.retries,
            )
            lane["turn_completion"] = completion
            lane["overall_status"] = "completed" if completion["status"] == "completed" else "turn_completion_wait_open"
            lanes.append(lane)
    finally:
        client.close()

    completed = sum(1 for lane in lanes if lane.get("overall_status") == "completed")
    reachable = sum(1 for lane in lanes if lane.get("read", {}).get("status") == "ok" and lane.get("resume", {}).get("status") == "ok")
    lane_count = len(selected_lanes(args.lanes))
    overall = "PASS" if completed == lane_count and not args.probe_only else "WARN"
    if args.probe_only and reachable == lane_count:
        overall = "PASS_PROBE_ONLY"

    return {
        "generated_utc": now_utc,
        "generated_nz": now_nz,
        "phase": args.phase,
        "artifact_type": "app_lane_notifier_runner",
        "overall_status": overall,
        "local_head_before_run": local_head,
        "remote_head_before_run": remote_head,
        "drift_before_run": drift,
        "runner_policy": {
            "existing_threads_only": True,
            "new_threads_created": False,
            "old_style_subagent_spawn_used": False,
            "raw_stream_published": False,
            "probe_only": args.probe_only,
            "retry_attempts_per_operation": args.retries,
        },
        "init": summarize_call(init),
        "lanes": lanes,
        "claim_boundary": {
            "domain": "THOS app-lane notifier and reconnect coordination",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
        "next_expected_phase": "v477_thos_v3_x1_or_continue_v477_overlay_if_lane_turns_remain_open",
    }


def summarize_call(call: dict) -> dict:
    result = {
        "status": call.get("status"),
        "attempt": call.get("attempt"),
    }
    if call.get("observed_methods"):
        result["observed_methods"] = call["observed_methods"]
    if call.get("result_keys"):
        result["result_keys"] = call["result_keys"]
    if call.get("failures"):
        result["failures"] = call["failures"]
    return result


def write_outputs(result: dict, suffix: str, artifact_prefix: str) -> None:
    json_path = TRACES / f"{artifact_prefix}-{suffix}-v1.json"
    md_path = TRACES / f"{artifact_prefix}-{suffix}-v1.md"
    write_json(json_path, result)
    lane_lines = []
    for lane in result["lanes"]:
        lane_lines.append(
            f"- {lane['name']}: `{lane.get('overall_status')}` "
            f"(read `{lane.get('read', {}).get('status')}`, resume `{lane.get('resume', {}).get('status')}`, "
            f"turn `{lane.get('turn_start', {}).get('status', 'not_started')}`)."
        )
    write_md(
        md_path,
        f"{result['phase']} App-Lane Notifier",
        [
            f"- generated_nz: `{result['generated_nz']}`",
            f"- local_head_before_run: `{result['local_head_before_run']}`",
            f"- remote_head_before_run: `{result['remote_head_before_run']}`",
            f"- drift_before_run: `{result['drift_before_run']}`",
            f"- overall_status: `{result['overall_status']}`",
            "- policy: existing app threads only; no new threads; no old-style subagent spawning; no unfiltered event stream publication.",
            "- claim boundary: THOS reconnect/notifier coordination only; all GMUT gates remain open.",
            "",
            "## Lane Status",
            *lane_lines,
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", default=PHASE_DEFAULT)
    parser.add_argument("--suffix", default="run")
    parser.add_argument("--artifact-prefix", default="v477-thos-v2-x3-app-lane-notifier")
    parser.add_argument("--lanes", default="all", help="Comma-separated lane names or all.")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--skip-start-if-active", action="store_true")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--call-timeout-seconds", type=int, default=90)
    parser.add_argument("--turn-timeout-seconds", type=int, default=900)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_notifier(args)
    write_outputs(result, args.suffix, args.artifact_prefix)
    print(json.dumps({"status": result["overall_status"], "lanes": len(result["lanes"])}, indent=2))


if __name__ == "__main__":
    main()
