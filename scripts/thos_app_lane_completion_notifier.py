#!/usr/bin/env python3
"""Run a sanitized local app-server notifier for existing Codex App advisory lanes."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import queue
import subprocess
import threading
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
try:
    from thos_x1_sibling_prompt_builder import build_prompt as build_x1_sibling_prompt
except ImportError:  # pragma: no cover - fallback keeps older bundles usable.
    build_x1_sibling_prompt = None
SHARED_REMOTE = "origin/codex/GHC-Family/beyonder-shared-omega-line"
SUPPORTED_LANES = ("Cicero", "Kierkegaard", "Aristotle")


class AppServerClient:
    def __init__(self) -> None:
        self.launch_mode = "unstarted"
        self.proc = self._start_process()
        self.stdout: queue.Queue[str] = queue.Queue()
        self.stderr: queue.Queue[str] = queue.Queue()
        self.next_id = 1
        threading.Thread(target=self._reader, args=(self.proc.stdout, self.stdout), daemon=True).start()
        threading.Thread(target=self._reader, args=(self.proc.stderr, self.stderr), daemon=True).start()

    def _start_process(self) -> subprocess.Popen:
        """Start app-server directly when possible, with cmd fallback for Windows shims."""
        candidates = [
            ("direct", ["codex", "app-server", "--stdio"]),
            ("cmd_fallback", ["cmd", "/c", "codex", "app-server", "--stdio"]),
        ]
        last_error: OSError | None = None
        for launch_mode, command in candidates:
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=str(ROOT),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )
                self.launch_mode = launch_mode
                return proc
            except OSError as exc:
                last_error = exc
        raise RuntimeError("app-server launch unavailable") from last_error

    @staticmethod
    def _reader(stream: Any, target: queue.Queue[str]) -> None:
        if stream is None:
            return
        for line in stream:
            target.put(line)

    def close(self) -> None:
        if self.proc.poll() is None:
            try:
                self.proc.terminate()
            except OSError:
                return
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def request(self, method: str, params: dict[str, Any]) -> int:
        if self.proc.poll() is not None:
            raise RuntimeError("app-server transport exited")
        if self.proc.stdin is None:
            raise RuntimeError("app-server stdin unavailable")
        request_id = self.next_id
        self.next_id += 1
        try:
            self.proc.stdin.write(json.dumps({"id": request_id, "method": method, "params": params}, separators=(",", ":")) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError, ValueError) as exc:
            raise RuntimeError("app-server transport unavailable") from exc
        return request_id

    def wait_response(self, request_id: int, timeout_seconds: int) -> tuple[dict[str, Any] | None, list[str]]:
        deadline = time.time() + timeout_seconds
        observed: list[str] = []
        while time.time() < deadline:
            if self.proc.poll() is not None and self.stdout.empty():
                observed.append("app_server_exited")
                break
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
            if isinstance(method, str):
                observed.append(method)
            if message.get("id") == request_id:
                return message, sorted(set(observed))[:24]
        return None, sorted(set(observed))[:24]

    def call(self, method: str, params: dict[str, Any], *, retries: int, timeout_seconds: int) -> dict[str, Any]:
        failures: list[dict[str, Any]] = []
        for attempt in range(1, retries + 1):
            try:
                request_id = self.request(method, params)
            except RuntimeError as exc:
                failures.append(
                    {
                        "attempt": attempt,
                        "status": "transport_unavailable",
                        "message_class": classify_transport_failure(exc),
                        "observed_methods": [],
                    }
                )
                time.sleep(min(attempt, 3))
                continue
            response, observed = self.wait_response(request_id, timeout_seconds)
            if response and "result" in response:
                return {
                    "status": "ok",
                    "attempt": attempt,
                    "observed_methods": observed,
                    "result_keys": sorted(response["result"].keys()) if isinstance(response.get("result"), dict) else [],
                }
            failures.append(
                {
                    "attempt": attempt,
                    "status": "timeout" if response is None else "error",
                    "message_class": classify_error(response),
                    "observed_methods": observed,
                }
            )
            time.sleep(min(attempt, 3))
        return {"status": "failed", "failures": failures}

    def wait_turn_completion(self, *, timeout_seconds: int, retries: int) -> dict[str, Any]:
        observed: list[str] = []
        assistant_signal = False
        started_signal = False
        per_attempt = max(1, timeout_seconds // max(1, retries))
        for attempt in range(1, retries + 1):
            deadline = time.time() + per_attempt
            while time.time() < deadline:
                if self.proc.poll() is not None and self.stdout.empty():
                    observed.append("app_server_exited")
                    return {
                        "status": "transport_unavailable",
                        "attempt": attempt,
                        "observed_methods": sorted(set(observed))[:32],
                        "turn_started_observed": started_signal,
                        "assistant_signal_observed": assistant_signal,
                    }
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
                if isinstance(method, str):
                    observed.append(method)
                if method == "turn/started":
                    started_signal = True
                compact = json.dumps(message, separators=(",", ":")).lower()
                if "assistant" in compact and any(marker in compact for marker in ("guard", "task", "blocker", "watcher", "thos")):
                    assistant_signal = True
                if method == "turn/completed":
                    return {
                        "status": "completed",
                        "attempt": attempt,
                        "observed_methods": sorted(set(observed))[:32],
                        "turn_started_observed": started_signal,
                        "assistant_signal_observed": assistant_signal,
                    }
            observed.append("completion_wait_window_elapsed")
        return {
            "status": "timeout",
            "attempts": retries,
            "observed_methods": sorted(set(observed))[:32],
            "turn_started_observed": started_signal,
            "assistant_signal_observed": assistant_signal,
        }


def classify_transport_failure(exc: RuntimeError) -> str:
    message = str(exc).lower()
    if "stdin" in message:
        return "stdin_unavailable"
    if "exited" in message:
        return "process_exited"
    if "launch" in message:
        return "launch_unavailable"
    return "transport_unavailable"


def classify_error(response: dict[str, Any] | None) -> str:
    if not response or not isinstance(response.get("error"), dict):
        return "none"
    message = str(response["error"].get("message", "")).lower()
    if "not found" in message:
        return "not_found"
    if "active" in message or "busy" in message:
        return "active_turn"
    if "approval" in message or "permission" in message:
        return "approval_or_permission"
    if "timeout" in message:
        return "timeout"
    return "other"


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


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def configured_lanes() -> dict[str, str]:
    """Load private app-lane IDs from the process environment only."""
    raw = os.environ.get("THOS_APP_LANE_IDS_JSON", "")
    if not raw.strip():
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("THOS_APP_LANE_IDS_JSON must be a JSON object")
    lanes: dict[str, str] = {}
    for name in SUPPORTED_LANES:
        value = parsed.get(name)
        if isinstance(value, str) and value.strip():
            lanes[name] = value.strip()
    return lanes


def selected_lanes(lane_arg: str) -> dict[str, str]:
    lanes = configured_lanes()
    if lane_arg.lower() in {"all", "*"}:
        if not lanes:
            raise ValueError("no app lanes configured in THOS_APP_LANE_IDS_JSON")
        return dict(lanes)
    wanted = {part.strip() for part in lane_arg.split(",") if part.strip()}
    unknown = wanted - set(SUPPORTED_LANES)
    if unknown:
        raise ValueError(f"unknown lane(s): {', '.join(sorted(unknown))}")
    missing = wanted - set(lanes)
    if missing:
        raise ValueError(f"configured lane id missing for: {', '.join(sorted(missing))}")
    return {name: lanes[name] for name in SUPPORTED_LANES if name in wanted}


def prompt_for(lane: str, phase_slug: str) -> str:
    if build_x1_sibling_prompt is not None:
        return build_x1_sibling_prompt(lane, phase_slug)
    return (
        f"Existing {lane} advisory lane notifier pass for {phase_slug}. "
        "Please provide an advisory-only THOS/GMUT status report with completion criteria, "
        "watcher and app-server reliability risks, blocker classes, and 20 concrete eureka tasks "
        "spanning design, repair, cleanup, build, run, test, install, and use. If your runtime allows, "
        "take a minimum of 4 minutes of thoughtful analysis before completion. Cover the Trinity Mandala "
        "pillars: GMUT as Mind, Trinity Hybrid OS as Body, and Freed ID/CBR as Heart. "
        "Do not edit files. Do not publish transport details. Keep all GMUT gates open and make no "
        "final physics, consciousness-proof, fifth-force-safety, or canon-promotion claims."
    )


def thread_id_digest(thread_id: str) -> str:
    return hashlib.sha256(thread_id.encode("utf-8")).hexdigest()[:16]


def lane_run(client: AppServerClient, lane: str, thread_id: str, args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    row: dict[str, Any] = {
        "lane": lane,
        "thread_id_redacted": True,
        "thread_id_digest": thread_id_digest(thread_id),
        "mode": "notify" if args.notify else "probe",
        "existing_thread_only": True,
        "new_thread_created": False,
        "unfiltered_transport_published": False,
    }
    read = client.call("thread/read", {"threadId": thread_id, "includeTurns": False}, retries=args.retries, timeout_seconds=args.call_timeout_seconds)
    row["read"] = summarize_call(read)
    if read.get("status") != "ok":
        row["overall_status"] = "blocked_read"
        row["duration_seconds"] = round(time.monotonic() - started, 3)
        return row

    resume = client.call(
        "thread/resume",
        {
            "threadId": thread_id,
            "excludeTurns": True,
            "sandbox": "read-only",
            "approvalPolicy": "never",
            "cwd": str(ROOT),
        },
        retries=args.retries,
        timeout_seconds=args.call_timeout_seconds,
    )
    row["resume"] = summarize_call(resume)
    resume_ok = resume.get("status") == "ok"
    row["resume_fallback"] = {
        "allowed": bool(args.allow_turn_start_after_resume_timeout),
        "used": False,
        "reason": None,
    }
    if not resume_ok and not args.allow_turn_start_after_resume_timeout:
        row["overall_status"] = "blocked_resume"
        row["duration_seconds"] = round(time.monotonic() - started, 3)
        return row
    if not resume_ok:
        row["resume_fallback"] = {
            "allowed": True,
            "used": True,
            "reason": "read_ok_resume_timeout_turn_start_direct_probe",
        }

    if not args.notify:
        row["overall_status"] = "read_resume_ok_probe_only" if resume_ok else "read_ok_resume_fallback_probe_only"
        row["duration_seconds"] = round(time.monotonic() - started, 3)
        return row

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
    row["turn_start"] = summarize_call(turn_start)
    if turn_start.get("status") != "ok":
        row["overall_status"] = "blocked_turn_start"
        row["duration_seconds"] = round(time.monotonic() - started, 3)
        return row

    completion = client.wait_turn_completion(timeout_seconds=args.turn_timeout_seconds, retries=args.retries)
    row["turn_completion"] = completion
    row["overall_status"] = "completed" if completion["status"] == "completed" else "completion_wait_open"
    row["duration_seconds"] = round(time.monotonic() - started, 3)
    return row


def summarize_call(call: dict[str, Any]) -> dict[str, Any]:
    summary = {"status": call.get("status"), "attempt": call.get("attempt")}
    if call.get("observed_methods"):
        summary["observed_methods"] = call["observed_methods"]
    if call.get("result_keys"):
        summary["result_keys"] = call["result_keys"]
    if call.get("failures"):
        summary["failures"] = call["failures"]
    return summary


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    generated_utc, generated_nz = now_pair()
    local_head = git_text(["rev-parse", "HEAD"])
    remote_head = git_text(["rev-parse", SHARED_REMOTE])
    drift = git_text(["rev-list", "--left-right", "--count", f"HEAD...{SHARED_REMOTE}"])
    client = AppServerClient()
    try:
        init = client.call(
            "initialize",
            {
                "clientInfo": {"name": "thos-app-lane-completion-notifier", "version": "1.0"},
                "capabilities": {
                    "experimentalApi": True,
                    "optOutNotificationMethods": ["item/started", "item/completed", "thread/updated"],
                },
            },
            retries=1,
            timeout_seconds=args.call_timeout_seconds,
        )
        lanes = [lane_run(client, lane, thread_id, args) for lane, thread_id in selected_lanes(args.lanes).items()]
    finally:
        client.close()

    completed = sum(1 for lane in lanes if lane.get("overall_status") == "completed")
    probed = sum(
        1
        for lane in lanes
        if lane.get("overall_status") in {"read_resume_ok_probe_only", "read_ok_resume_fallback_probe_only"}
    )
    if args.notify:
        overall_status = "PASS" if completed == len(lanes) else "OPEN_GAP_APP_LANE_WAIT"
    else:
        overall_status = "PASS_PROBE_ONLY" if probed == len(lanes) else "OPEN_GAP_APP_LANE_PROBE"

    return {
        "artifact_type": "app_lane_completion_notifier",
        "generated_nz": generated_nz,
        "generated_utc": generated_utc,
        "phase_slug": args.phase_slug,
        "overall_status": overall_status,
        "local_head_before_run": local_head,
        "remote_head_before_run": remote_head,
        "drift_before_run": drift,
        "policy": {
            "existing_threads_only": True,
            "old_style_spawn_used": False,
            "new_threads_created": False,
            "read_only_sandbox_requested": True,
            "approval_policy_requested": "never",
            "unfiltered_transport_published": False,
            "retry_attempts_per_operation": args.retries,
            "app_server_launch_mode": client.launch_mode,
            "turn_start_after_resume_timeout_fallback_allowed": bool(args.allow_turn_start_after_resume_timeout),
        },
        "init": summarize_call(init),
        "lanes": lanes,
        "claim_boundary": {
            "scope": "THOS app-lane completion notification and coordination only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} App-Lane Completion Notifier",
        "",
        f"- generated_nz: `{payload['generated_nz']}`",
        f"- overall_status: `{payload['overall_status']}`",
        f"- local_head_before_run: `{payload['local_head_before_run']}`",
        f"- remote_head_before_run: `{payload['remote_head_before_run']}`",
        f"- drift_before_run: `{payload['drift_before_run']}`",
        "- policy: existing app threads only; no new thread creation; no old-style spawning; no unfiltered transport publication.",
        "- claim boundary: THOS coordination only; all GMUT gates remain open.",
        "",
        "## Lane Summary",
    ]
    for lane in payload["lanes"]:
        completion = lane.get("turn_completion", {})
        lines.append(
            f"- {lane['lane']}: `{lane.get('overall_status')}`, duration `{lane.get('duration_seconds')}`, "
            f"read `{lane.get('read', {}).get('status')}`, resume `{lane.get('resume', {}).get('status')}`, "
            f"turn `{lane.get('turn_start', {}).get('status', 'not_started')}`, completion `{completion.get('status', 'not_waited')}`."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", default="v477-thos-v5-x2")
    parser.add_argument("--artifact-prefix", default="v477-thos-v5-x2-app-lane-completion-notifier")
    parser.add_argument("--lanes", default="all")
    parser.add_argument("--notify", action="store_true", help="Send a phase advisory prompt and wait for completion.")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--call-timeout-seconds", type=int, default=90)
    parser.add_argument("--turn-timeout-seconds", type=int, default=900)
    parser.add_argument(
        "--allow-turn-start-after-resume-timeout",
        action="store_true",
        help="After thread/read succeeds but thread/resume times out, try turn/start directly and record the fallback in the receipt.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_result(args)
    json_path = TRACE_DIR / f"{args.artifact_prefix}-v1.json"
    md_path = TRACE_DIR / f"{args.artifact_prefix}-v1.md"
    write_json(json_path, payload)
    write_md(md_path, payload)
    print(json.dumps({"status": payload["overall_status"], "lanes": len(payload["lanes"])}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
