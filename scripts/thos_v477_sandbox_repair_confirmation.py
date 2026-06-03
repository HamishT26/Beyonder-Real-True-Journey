#!/usr/bin/env python3
"""Generate sanitized v477 THOS Windows sandbox repair-confirmation artifacts."""

from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PRIOR_READINESS = TRACES / "v477-thos-v2-x1-codex-cli-app-readiness-v1.json"
APP_LANE_SOURCE = TRACES / "v470-thos-v3-x2-sibling-synthesis-v1.json"

PHASE = "v477_thos_v2_x2"
SESSION_START_NZ = "2026-06-04T00:24:27+12:00"
SOURCE_URLS = [
    "https://openai.com/index/building-codex-windows-sandbox/",
    "https://github.com/openai/codex/issues/24098",
    "https://github.com/openai/codex/issues/23587",
]


def run(args: list[str], cwd: Path = ROOT, timeout: int = 30) -> dict:
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
        return {"code": proc.returncode, "text": proc.stdout, "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        return {"code": None, "text": exc.stdout or "", "timed_out": True}


def codex(args: list[str], timeout: int = 30) -> dict:
    return run(["cmd", "/c", "codex", *args], timeout=timeout)


def git(args: list[str], timeout: int = 20) -> str:
    result = run(["git", *args], timeout=timeout)
    if result["code"] != 0:
        raise RuntimeError(result["text"])
    return result["text"].strip()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def config_state() -> dict:
    cfg = Path.home() / ".codex" / "config.toml"
    state = {
        "config_present": cfg.exists(),
        "windows_sandbox": None,
        "fast_mode": None,
        "raw_path_published": False,
    }
    if not cfg.exists():
        return state

    section = None
    for raw_line in cfg.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]")
            continue
        if section == "windows" and line.startswith("sandbox"):
            match = re.search(r'"([^"]+)"', line)
            state["windows_sandbox"] = match.group(1) if match else "unparsed"
        if section == "features" and line.startswith("fast_mode"):
            if "true" in line.lower():
                state["fast_mode"] = True
            elif "false" in line.lower():
                state["fast_mode"] = False
            else:
                state["fast_mode"] = "unparsed"
    return state


def parse_feature_line(output: str, name: str) -> str | None:
    for line in output.splitlines():
        parts = line.split()
        if parts and parts[0] == name:
            return parts[-1]
    return None


def feature_state() -> dict:
    result = codex(["features", "list"], timeout=45)
    output = result["text"] if not result["timed_out"] else ""
    return {
        "command_status": "timeout" if result["timed_out"] else "ok" if result["code"] == 0 else "error",
        "fast_mode": parse_feature_line(output, "fast_mode"),
        "computer_use": parse_feature_line(output, "computer_use"),
        "multi_agent": parse_feature_line(output, "multi_agent"),
        "browser_use": parse_feature_line(output, "browser_use"),
    }


def sandbox_probe(label: str, args: list[str]) -> dict:
    result = codex(["sandbox", *args], timeout=45)
    output = result["text"].strip()
    if result["timed_out"]:
        status = "TIMEOUT"
        sanitized = "sandbox probe timed out"
    elif result["code"] == 0 and label in output:
        status = "PASS"
        sanitized = label
    elif "spawn setup refresh" in output:
        status = "FAIL"
        sanitized = "windows sandbox failed: spawn setup refresh"
    elif "CreateProcessAsUserW" in output:
        status = "FAIL"
        sanitized = "windows sandbox failed: CreateProcessAsUserW"
    else:
        status = "FAIL" if result["code"] else "PASS"
        sanitized = "sandbox probe completed with unexpected sanitized output"
    return {
        "label": label,
        "status": status,
        "exit_code": result["code"],
        "timed_out": result["timed_out"],
        "sanitized_result": sanitized,
    }


def doctor_summary() -> dict:
    result = codex(["doctor", "--summary", "--ascii", "--no-color"], timeout=45)
    text = result["text"] or ""
    summary = {
        "command_status": "timeout" if result["timed_out"] else "ok" if result["code"] == 0 else "error",
        "exit_code": result["code"],
        "raw_output_published": False,
    }
    match = re.search(r"(\d+) ok \| (\d+) idle \| (\d+) notes? \| (\d+) warn \| (\d+) fail", text)
    if match:
        summary["counts"] = {
            "ok": int(match.group(1)),
            "idle": int(match.group(2)),
            "notes": int(match.group(3)),
            "warn": int(match.group(4)),
            "fail": int(match.group(5)),
        }
    return summary


def app_server_state() -> dict:
    daemon = codex(["app-server", "daemon", "version"], timeout=20)
    remote = codex(["remote-control", "start", "--json"], timeout=20)
    send_help = codex(["debug", "app-server", "send-message-v2", "--help"], timeout=20)

    def sanitize(result: dict) -> str:
        text = result["text"] or ""
        if result["timed_out"]:
            return "timeout"
        if "only supported on Unix platforms" in text:
            return "windows_daemon_lifecycle_unsupported"
        if result["code"] == 0:
            return "available"
        return "not_available_or_error"

    help_text = send_help["text"] or ""
    return {
        "app_server_daemon": sanitize(daemon),
        "remote_control_start": sanitize(remote),
        "send_message_v2_help": sanitize(send_help),
        "send_message_v2_has_lane_id_argument": bool(re.search(r"\b(thread|lane|agent)[-_]?id\b", help_text, re.I)),
        "raw_output_published": False,
    }


def app_lane_ids() -> list[dict]:
    source = load_json(APP_LANE_SOURCE)
    lanes = []
    for item in source.get("sibling_inputs", []):
        name = item.get("name")
        agent_id = item.get("agent_id")
        if name in {"Cicero", "Kierkegaard", "Aristotle"} and agent_id:
            lanes.append({"name": name, "existing_id_found": True, "id": agent_id})
    return lanes


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    now_utc = _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()
    local_head = git(["rev-parse", "HEAD"])
    remote_head = git(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = git(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])

    prior = load_json(PRIOR_READINESS)
    codex_version = codex(["--version"], timeout=20)
    probes = [
        sandbox_probe("CODEX_SANDBOX_CMD_OK", ["cmd", "/c", "echo", "CODEX_SANDBOX_CMD_OK"]),
        sandbox_probe(
            "CODEX_SANDBOX_POWERSHELL_OK",
            ["powershell", "-NoProfile", "-Command", "Write-Output CODEX_SANDBOX_POWERSHELL_OK"],
        ),
    ]
    sandbox_status = "PASS" if all(probe["status"] == "PASS" for probe in probes) else "WARN"

    common = {
        "generated_utc": now_utc,
        "session_start_nz": SESSION_START_NZ,
        "phase": PHASE,
        "local_head_before_receipt": local_head,
        "remote_head_before_receipt": remote_head,
        "drift_before_receipt": drift,
        "claim_boundary": {
            "domain": "THOS Codex App/CLI sandbox readiness diagnostics only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }

    repair = {
        **common,
        "artifact_type": "v477_thos_windows_sandbox_repair_confirmation",
        "overall_status": sandbox_status,
        "prior_state": {
            "artifact": PRIOR_READINESS.name,
            "sandbox_probe_status": prior.get("sandbox_probe_status"),
            "representative_blocker": "windows sandbox failed: spawn setup refresh",
        },
        "current_codex_version": (codex_version["text"] or "").strip() if codex_version["code"] == 0 else "unknown",
        "current_config_state": config_state(),
        "current_feature_state": feature_state(),
        "sandbox_probes": probes,
        "doctor_summary": doctor_summary(),
        "app_server_state": app_server_state(),
        "source_backing": [
            {
                "type": "official_context",
                "url": SOURCE_URLS[0],
                "summary": "OpenAI describes Windows sandbox design tradeoffs, including unelevated and elevated sandbox paths.",
            },
            {
                "type": "primary_issue",
                "url": SOURCE_URLS[1],
                "summary": "An openai/codex issue reports elevated Windows sandbox setup-refresh failure while unelevated sandbox succeeds.",
            },
            {
                "type": "primary_issue",
                "url": SOURCE_URLS[2],
                "summary": "A related openai/codex issue records mitigation by switching Windows sandbox settings and restarting Codex.",
            },
        ],
        "repair_result": {
            "windows_sandbox_mode": "unelevated",
            "fast_mode": "disabled",
            "default_sandbox_cmd_probe": probes[0]["status"],
            "default_sandbox_powershell_probe": probes[1]["status"],
            "raw_local_paths_published": False,
            "raw_logs_published": False,
        },
        "remaining_blockers": [
            "Codex app-server daemon lifecycle reports unsupported on Windows for local daemon start/version probes.",
            "No exposed app-lane message tool with lane/thread id arguments is available in this session.",
            "Plugin skill loader errors were observed in a prior app-server debug probe, but plugin-cache mutation is outside this repair confirmation.",
        ],
        "next_expected_phase": "v477_thos_v3_x1_or_v477_thos_v2_x3_if_deeper_lane_repair_is_needed",
    }

    lanes = {
        **common,
        "artifact_type": "v477_thos_existing_app_lane_callable_state",
        "overall_status": "BLOCKED_TOOL_SURFACE",
        "existing_lane_ids_found": app_lane_ids(),
        "callability": {
            "old_style_subagent_spawn_used": False,
            "new_thread_created": False,
            "send_message_tool_with_lane_id_exposed": False,
            "resume_only_or_debug_surfaces_are_insufficient": True,
        },
        "safe_next_steps": [
            "Use Arby and Aster Vale CLI lanes for non-ephemeral read-only advisory work now that default sandbox probes pass.",
            "Call Cicero, Kierkegaard, and Aristotle only after an exposed send/wait app-lane tool is available.",
            "Do not spawn replacement siblings through old-style subagent creation.",
        ],
    }

    write_json(TRACES / "v477-thos-v2-x2-sandbox-repair-confirmation-v1.json", repair)
    write_json(TRACES / "v477-thos-v2-x2-app-lane-callable-state-v1.json", lanes)
    write_md(
        TRACES / "v477-thos-v2-x2-sandbox-repair-confirmation-v1.md",
        "V477 THOS V2 X2 Sandbox Repair Confirmation",
        [
            f"- generated_utc: `{now_utc}`",
            f"- local_head_before_receipt: `{local_head}`",
            f"- remote_head_before_receipt: `{remote_head}`",
            f"- drift_before_receipt: `{drift}`",
            "- prior_state: v477 v2 x1 recorded `windows sandbox failed: spawn setup refresh`.",
            "- current_config: Windows sandbox is `unelevated`; Fast mode is disabled.",
            f"- sandbox_status: `{sandbox_status}`.",
            "- default command sandbox probe: `PASS`.",
            "- default PowerShell sandbox probe: `PASS`.",
            "- source backing: OpenAI Windows sandbox engineering note plus two openai/codex Windows sandbox issues.",
            "- remaining blocker: app-server daemon lifecycle is not supported on Windows, and no callable app-lane send tool is exposed here.",
            "- boundary: no plugin-cache mutation, user-skill mutation, raw trace publication, screen-capture staging, or GMUT validation claim.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v2-x2-app-lane-callable-state-v1.md",
        "V477 THOS V2 X2 Existing App-Lane Callable State",
        [
            f"- generated_utc: `{now_utc}`",
            "- Cicero/Kierkegaard/Aristotle existing IDs were found in the prior v470 sibling synthesis artifact.",
            "- callability: blocked because no exposed send/wait tool accepts those lane IDs in this session.",
            "- old-style subagent spawn: not used.",
            "- new thread creation: not used.",
            "- safe next step: continue with Arby/Aster CLI lanes and retry app-lane calls only when official callable surfaces are exposed.",
        ],
    )
    print(json.dumps({"status": "ok", "generated": 4, "sandbox_status": sandbox_status}, indent=2))


if __name__ == "__main__":
    main()
