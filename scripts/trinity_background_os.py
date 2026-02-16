#!/usr/bin/env python3
"""Trinity Background OS runner.

Runs coordinated maintenance cycles (suite + cache regenerator + bank updates)
for AFK/autonomous continuity with bounded loop controls.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATUS = ROOT / "docs" / "trinity-background-os-status.json"
DEFAULT_LOCKFILE = ROOT / "docs" / ".trinity-background-os.lock"


def _repo_path(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _run(cmd: list[str]) -> dict[str, object]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": (proc.stdout or "")[-4000:],
        "stderr": (proc.stderr or "")[-4000:],
    }


def _acquire_lock(path: Path, force: bool) -> None:
    payload = {
        "pid": os.getpid(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "trinity-background-os",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    if force and path.exists():
        path.unlink(missing_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise SystemExit(f"lock exists: {path} (use --force-lock to override)") from exc
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2) + "\n")


def _release_lock(path: Path) -> None:
    path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Trinity background OS cycle loop")
    parser.add_argument("--profile", default="quick", choices=("quick", "standard", "deep"))
    parser.add_argument("--cycles", type=int, default=1, help="Number of background cycles to run")
    parser.add_argument("--interval-sec", type=int, default=0, help="Sleep between cycles")
    parser.add_argument("--max-runtime-sec", type=int, default=0, help="Stop early when runtime budget is reached (0 = unlimited)")
    parser.add_argument("--status", default=str(DEFAULT_STATUS.relative_to(ROOT)))
    parser.add_argument("--lockfile", default=str(DEFAULT_LOCKFILE.relative_to(ROOT)), help="Repo-relative lock file path")
    parser.add_argument("--force-lock", action="store_true", help="Replace an existing lock file before starting")
    parser.add_argument("--cache-purge", action="store_true", help="Purge reclaimed cache/tmp artifacts each cycle")
    parser.add_argument("--fail-fast", action="store_true", help="Stop further cycles after the first failed cycle")
    args = parser.parse_args()

    cycles = max(1, args.cycles)
    runtime_budget = max(0, args.max_runtime_sec)
    suite_started = time.monotonic()
    lockfile = _repo_path(args.lockfile)
    _acquire_lock(lockfile, force=args.force_lock)

    status_rows: list[dict[str, object]] = []
    stopped_reason = "completed"

    try:
        for i in range(1, cycles + 1):
            elapsed = time.monotonic() - suite_started
            if runtime_budget and elapsed >= runtime_budget:
                stopped_reason = "max_runtime_reached"
                break

            started = datetime.now(timezone.utc).isoformat()
            steps = []
            steps.append(_run(["python3", "scripts/run_all_trinity_systems.py", "--profile", args.profile, "--step-timeout-sec", "0"]))
            cache_cmd = ["python3", "scripts/cache_waste_regenerator.py", "--out", "docs/cache-waste-regenerator-report.json"]
            if args.cache_purge:
                cache_cmd.extend(["--purge", "--prune-empty-dirs"])
            steps.append(_run(cache_cmd))
            steps.append(
                _run(
                    [
                        "python3",
                        "scripts/validate_cache_waste_report.py",
                        "--cache",
                        "docs/cache-waste-regenerator-report.json",
                    ]
                )
            )
            steps.append(
                _run(
                    [
                        "python3",
                        "scripts/trinity_energy_bank_system.py",
                        "--token-report",
                        "docs/token-credit-bank-report.json",
                        "--cache-report",
                        "docs/cache-waste-regenerator-report.json",
                        "--reserve-growth",
                        "1.0",
                        "--reserve-cap-multiplier",
                        "10.0",
                        "--auto-max-cap",
                        "--cap-ceiling",
                        "100.0",
                    ]
                )
            )

            ok = all(int(s["returncode"]) == 0 for s in steps)
            status_rows.append(
                {
                    "cycle": i,
                    "started_utc": started,
                    "finished_utc": datetime.now(timezone.utc).isoformat(),
                    "ok": ok,
                    "steps": steps,
                }
            )

            if args.fail_fast and not ok:
                stopped_reason = "fail_fast"
                break

            if i < cycles and args.interval_sec > 0:
                time.sleep(args.interval_sec)
    finally:
        _release_lock(lockfile)

    out = _repo_path(args.status)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "generated_utc": datetime.now(timezone.utc).isoformat(),
                "engine": "trinity-background-os",
                "profile": args.profile,
                "cycles_requested": cycles,
                "cycles_completed": len(status_rows),
                "runtime_budget_sec": runtime_budget,
                "stopped_reason": stopped_reason,
                "runs": status_rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
