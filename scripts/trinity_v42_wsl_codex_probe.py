#!/usr/bin/env python3
"""Diagnose the real V42 WSL and Codex binding state without over-claiming promotion."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from trinity_v42_common import LOCAL_RUNTIME_DIR, REPO_MOUNT, ROOT, WSL_DISTRO, now_iso, safe_run, write_json, write_text

OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v42-wsl-codex-probe-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v42-wsl-codex-probe-v1.md"
CODEX_EXE = Path(r"C:\Users\hamis\.codex\.sandbox-bin\codex.exe")
CONFIG_TOML = Path(r"C:\Users\hamis\.codex\config.toml")


def run_wsl(command: str, *, timeout: int = 60) -> dict[str, Any]:
    proc = safe_run(["wsl.exe", "-d", WSL_DISTRO, "--", "bash", "-lc", command], timeout=timeout)
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "ok": proc.returncode == 0,
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# V42 WSL Codex Probe",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- WSL health state: `{payload['wsl_health_state']}`",
        f"- WSL Codex selector state: `{payload['wsl_codex_selector_state']}`",
        f"- Codex CLI WSL state: `{payload['codex_cli_wsl_state']}`",
        f"- Manual operator checkpoint required: `{payload['manual_operator_checkpoint_required']}`",
        "",
        "## Probe Results",
        "",
    ]
    for key, value in payload.get("probe_results", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {row}" for row in payload["blockers"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe the real V42 WSL and Codex selector state.")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    args = parser.parse_args()

    LOCAL_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    config_text = CONFIG_TOML.read_text(encoding="utf-8", errors="replace") if CONFIG_TOML.exists() else ""
    selector_keywords = ("wsl", "ubuntu", "bash", "environment_selector", "linux")

    inventory = safe_run(["wsl.exe", "-l", "-v"], timeout=30)
    bash_probe = run_wsl("test -x /usr/bin/bash && printf /usr/bin/bash")
    python_probe = run_wsl("command -v python3")
    git_probe = run_wsl("command -v git")
    node_probe = run_wsl("command -v node")
    npx_probe = run_wsl("command -v npx")
    repo_probe = run_wsl(f"cd {REPO_MOUNT} && git rev-parse --short HEAD", timeout=90)
    codex_version = run_wsl("'/mnt/c/Users/hamis/.codex/.sandbox-bin/codex.exe' --version", timeout=60)
    codex_exec_help = run_wsl(f"cd {REPO_MOUNT} && '/mnt/c/Users/hamis/.codex/.sandbox-bin/codex.exe' exec --help", timeout=90)

    blockers: list[str] = []
    if inventory.returncode != 0:
        blockers.append("`wsl.exe -l -v` did not complete cleanly from the Windows host.")
    if not bash_probe["ok"]:
        blockers.append("Ubuntu does not expose `/usr/bin/bash` to a bounded WSL probe.")
    if not python_probe["ok"]:
        blockers.append("`python3` is not discoverable inside Ubuntu.")
    if not git_probe["ok"]:
        blockers.append("`git` is not discoverable inside Ubuntu.")
    if not node_probe["ok"] or not npx_probe["ok"]:
        blockers.append("`node` and `npx` must both resolve inside Ubuntu for the V42 automation lane.")
    if not repo_probe["ok"]:
        blockers.append("The authoritative repo is not visible at the expected WSL mount.")

    selector_configurable = any(token in config_text.lower() for token in selector_keywords)
    if not selector_configurable:
        blockers.append("The Codex desktop WSL selector is not discoverable from repo or global config; the remaining binding proof is app-side.")

    codex_cli_ok = codex_version["ok"] and codex_exec_help["ok"]
    if not codex_cli_ok:
        blockers.append("Codex CLI did not launch cleanly from inside Ubuntu.")

    wsl_health_state = "ubuntu_repo_ready" if all([bash_probe["ok"], python_probe["ok"], git_probe["ok"], node_probe["ok"], npx_probe["ok"], repo_probe["ok"]]) else "ubuntu_health_blocked"
    if codex_cli_ok and not selector_configurable:
        selector_state = "cli_wsl_entrypoint_verified_app_selector_unresolved"
    elif codex_cli_ok:
        selector_state = "cli_wsl_entrypoint_verified"
    else:
        selector_state = "codex_cli_launch_blocked"

    overall_status = "PASS" if codex_cli_ok and selector_configurable else "WARN"
    payload = {
        "generated_utc": now_iso(),
        "phase": "v42_omega",
        "overall_status": overall_status,
        "wsl_health_state": wsl_health_state,
        "wsl_codex_selector_state": selector_state,
        "codex_cli_wsl_state": "cli_binary_launch_verified" if codex_cli_ok else "cli_binary_launch_blocked",
        "manual_operator_checkpoint_required": not selector_configurable,
        "authoritative_repo_mount": REPO_MOUNT,
        "authoritative_repo_windows_path": str(ROOT),
        "probe_results": {
            "wsl_inventory_returncode": inventory.returncode,
            "bash_path": bash_probe["stdout"],
            "python3_path": python_probe["stdout"],
            "git_path": git_probe["stdout"],
            "node_path": node_probe["stdout"],
            "npx_path": npx_probe["stdout"],
            "repo_head_from_wsl": repo_probe["stdout"],
            "codex_version": codex_version["stdout"],
            "codex_exec_help_ok": codex_exec_help["ok"],
            "config_selector_keywords_found": selector_configurable,
            "codex_exe_present": CODEX_EXE.exists(),
            "windows_python_present": bool(shutil.which("python")),
        },
        "probe_details": {
            "wsl_inventory_stdout": inventory.stdout.strip(),
            "wsl_inventory_stderr": inventory.stderr.strip(),
            "codex_exec_help_stdout_excerpt": codex_exec_help["stdout"][:1200],
            "codex_exec_help_stderr_excerpt": codex_exec_help["stderr"][:1200],
        },
        "blockers": blockers,
        "non_gating_note": "V42 treats Ubuntu itself as healthy unless the bounded host and repo probes fail; remaining selector proof is desktop-app scoped.",
    }
    write_json(Path(args.output_json), payload)
    write_text(Path(args.output_md), markdown(payload))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
