#!/usr/bin/env python3
"""Run the existing repo kairotic surface and emit a V30 proof artifact."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    sandbox_root = Path("/home/aletheon/v30-fluid-lab")
    repo_root = Path(os.environ.get("TRINITY_REPO_ROOT", "/mnt/c/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey"))
    source_script = repo_root / "scripts" / "kairotic_detector.py"
    source_artifact = repo_root / "docs" / "legacy-reconstruction" / "kairotic-detector-latest.json"

    result = subprocess.run(
        ["python3", str(source_script)],
        capture_output=True,
        text=True,
        check=False,
    )

    source_payload: dict = {}
    if source_artifact.exists():
        source_payload = json.loads(source_artifact.read_text(encoding="utf-8"))

    signals = source_payload.get("signals", []) if isinstance(source_payload, dict) else []
    payload = {
        "generated_utc": now_iso(),
        "experiment_id": "V30-E004",
        "overall_status": "PASS" if result.returncode == 0 else "WARN",
        "proof_state": "bounded_kairotic_repo_surface",
        "repo_root": str(repo_root),
        "source_script": str(source_script),
        "source_artifact": str(source_artifact),
        "source_script_returncode": result.returncode,
        "stdout_preview": result.stdout.strip().splitlines()[:10],
        "stderr_preview": result.stderr.strip().splitlines()[:10],
        "signals": signals,
        "kairotic_moment_detected": bool(signals),
    }

    artifact_path = sandbox_root / "artifacts" / "v30-e004-kairotic-integration-latest.json"
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(artifact_path)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
