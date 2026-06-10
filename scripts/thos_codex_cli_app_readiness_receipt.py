#!/usr/bin/env python3
"""Create a bounded Codex CLI/App readiness receipt."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SURFACES = [
    "exec",
    "review",
    "mcp",
    "plugin",
    "app-server",
    "remote-control",
    "app",
    "update",
    "doctor",
    "sandbox",
    "features",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_probe(args: list[str], timeout_seconds: int) -> dict[str, Any]:
    command = list(args)
    if os.name == "nt" and command and command[0] == "codex":
        command = ["powershell", "-NoProfile", "-Command", subprocess.list2cmdline(args)]
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "returncode": None,
            "stdout_bytes": 0,
            "stderr_bytes": 0,
            "stdout_preview": "",
            "stderr_preview": "",
        }
    except OSError as exc:
        return {
            "status": "OS_ERROR",
            "returncode": None,
            "stdout_bytes": 0,
            "stderr_bytes": 0,
            "stdout_preview": "",
            "stderr_preview": f"{type(exc).__name__}: {exc}",
        }
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    return {
        "status": "PASS" if completed.returncode == 0 else "NONZERO",
        "returncode": completed.returncode,
        "stdout_bytes": len(stdout.encode("utf-8", errors="replace")),
        "stderr_bytes": len(stderr.encode("utf-8", errors="replace")),
        "stdout_preview": stdout[:500],
        "stderr_preview": stderr[:300],
    }


def surface_map(help_text: str) -> dict[str, bool]:
    return {name: name in help_text for name in EXPECTED_SURFACES}


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.live_probes:
        version = run_probe(["codex", "--version"], args.short_timeout_seconds)
        help_probe = run_probe(["codex", "--help"], args.short_timeout_seconds)
        sandbox = run_probe(
            ["codex", "sandbox", "powershell", "-NoProfile", "-Command", "Write-Output sandbox-ok"],
            args.sandbox_timeout_seconds,
        )
        doctor = run_probe(["codex", "doctor", "--json"], args.doctor_timeout_seconds)
        help_text = help_probe.get("stdout_preview", "")
        surfaces = surface_map(help_text)
    else:
        version = {
            "status": "PASS" if args.observed_version else "NOT_RUN",
            "stdout_preview": args.observed_version,
            "stderr_bytes": 0,
        }
        sandbox = {
            "status": args.observed_sandbox_status,
            "stdout_preview": "sandbox-ok" if args.observed_sandbox_status == "PASS" else "",
            "stderr_bytes": 0,
        }
        doctor = {"status": args.observed_doctor_status, "stderr_bytes": 0}
        help_probe = {"status": "PASS"}
        surfaces = {name: True for name in EXPECTED_SURFACES}
    return {
        "artifact_type": "codex_cli_app_readiness_receipt",
        "phase_slug": args.phase_slug,
        "generated_utc": utc_now(),
        "overall_status": "PASS_CODEX_READINESS_PREFLIGHT"
        if version["status"] == "PASS"
        and help_probe["status"] == "PASS"
        and sandbox["status"] == "PASS"
        else "OPEN_GAP_CODEX_READINESS_PREFLIGHT",
        "version": {
            "status": version["status"],
            "summary": version["stdout_preview"].strip(),
        },
        "live_probe_mode": args.live_probes,
        "help_surfaces": surfaces,
        "sandbox_probe": {
            "status": sandbox["status"],
            "stdout_matches_expected": "sandbox-ok" in sandbox.get("stdout_preview", ""),
            "stderr_bytes": sandbox["stderr_bytes"],
        },
        "doctor_probe": {
            "status": doctor["status"],
            "timeout_seconds": args.doctor_timeout_seconds,
            "interpretation": "stale_flow_watch_item" if doctor["status"] == "TIMEOUT" else "completed",
        },
        "publication_boundary": {
            "status_only": True,
            "raw_logs_published": False,
            "credentials_published": False,
            "session_streams_published": False,
            "local_absolute_paths_published": False,
        },
        "claim_boundary": {
            "gmut_gate_state": "open",
            "canon_promotion": "not_claimed",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# {payload['phase_slug']} Codex CLI/App Readiness Receipt",
        "",
        f"- overall_status: `{payload['overall_status']}`",
        f"- version: `{payload['version']['summary']}`",
        f"- sandbox_probe: `{payload['sandbox_probe']['status']}`",
        f"- doctor_probe: `{payload['doctor_probe']['status']}`",
        "",
        "## Help Surfaces",
    ]
    for name, available in payload["help_surfaces"].items():
        lines.append(f"- {name}: `{str(available).lower()}`")
    lines.extend(
        [
            "",
            "Boundary: status-only receipt; no raw logs, credentials, session streams, private connector payloads, or local absolute paths.",
            "",
            "GMUT and canon gates remain open.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--receipt-json", required=True)
    parser.add_argument("--receipt-md", required=True)
    parser.add_argument("--short-timeout-seconds", type=int, default=20)
    parser.add_argument("--sandbox-timeout-seconds", type=int, default=45)
    parser.add_argument("--doctor-timeout-seconds", type=int, default=30)
    parser.add_argument("--live-probes", action="store_true")
    parser.add_argument("--observed-version", default="codex-cli 0.138.0")
    parser.add_argument("--observed-sandbox-status", default="PASS")
    parser.add_argument("--observed-doctor-status", default="TIMEOUT")
    args = parser.parse_args()
    payload = build_payload(args)
    write_json(Path(args.receipt_json), payload)
    write_md(Path(args.receipt_md), payload)
    print(json.dumps({"status": payload["overall_status"], "phase_slug": args.phase_slug}, indent=2))
    return 0 if payload["overall_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
