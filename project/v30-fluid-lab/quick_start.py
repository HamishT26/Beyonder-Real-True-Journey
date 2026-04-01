#!/usr/bin/env python3
"""Quick-start runner for the repo-native V30 fluid lab."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SANDBOX_ROOT = "/home/aletheon/v30-fluid-lab"


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_command(cmd: list[str], description: str, timeout: int = 120) -> bool:
    print(f"- {description}")
    print(f"  command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"  result: TIMEOUT after {timeout}s")
        return False

    if result.returncode == 0:
        print("  result: PASS")
        if result.stdout.strip():
            preview = result.stdout.strip().splitlines()[-1]
            print(f"  output: {preview[:180]}")
        return True

    print(f"  result: FAIL ({result.returncode})")
    if result.stderr.strip():
        print(f"  error: {result.stderr.strip()[:200]}")
    return False


def main() -> int:
    print_header("V30 FLUID LAB QUICK START")
    print("This runner only executes the bounded local V30 lane.")
    print("Controller-run proofs such as Gmail and Hugging Face stay outside this script.")

    is_wsl = os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")
    print(f"\n- wsl_detected: {is_wsl}")
    print(f"- python: {sys.version.split()[0]}")
    print(f"- sandbox_root: {SANDBOX_ROOT}")

    for name in ("experiments", "artifacts", "logs", "snapshots", "temp"):
        Path(SANDBOX_ROOT, name).mkdir(parents=True, exist_ok=True)

    results = [
        run_command(["python3", f"{SANDBOX_ROOT}/capability_discovery_probe.py"], "Capability discovery", timeout=180),
        run_command(["python3", f"{SANDBOX_ROOT}/fluid_capability_test_suite.py"], "Capability test suite", timeout=360),
        run_command(["python3", f"{SANDBOX_ROOT}/v30_experiment_orchestrator.py", "--list"], "List V30 experiments", timeout=60),
        run_command(["python3", f"{SANDBOX_ROOT}/v30_experiment_orchestrator.py", "--local-only"], "Run bounded local V30 experiments", timeout=360),
    ]

    print_header("V30 QUICK START COMPLETE")
    print(f"- success_count: {sum(1 for item in results if item)} / {len(results)}")
    print("- next_step: review artifacts in /home/aletheon/v30-fluid-lab/artifacts")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
