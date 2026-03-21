#!/usr/bin/env python3
"""Validate the v17 council mesh by delegating to the v16 validator with v17 defaults."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_ARGS = [
    "--roster",
    "docs/trinity-agent-council-roster-v8.json",
    "--command-book",
    "docs/trinity-command-book-v11.json",
    "--subagent-registry",
    "docs/trinity-subagent-registry-v5.json",
    "--runtime-session-log",
    "docs/v17-runtime-session-log-latest.json",
]


def main() -> int:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "trinity_agent_council_v16_validator.py"),
        *DEFAULT_ARGS,
        *sys.argv[1:],
    ]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
