#!/usr/bin/env python3
"""Run or list the repo-native V30 fluid-lab experiments."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SANDBOX_ROOT = Path("/home/aletheon/v30-fluid-lab")
ARTIFACTS_DIR = SANDBOX_ROOT / "artifacts"
EXPERIMENTS_DIR = SANDBOX_ROOT / "experiments"

EXPERIMENTS = {
    "V30-E001": {"script": "V30-E001-gmail-materialization.py", "local": False, "description": "Controller-aware Gmail proof stub"},
    "V30-E002": {"script": "V30-E002-hf-materialization.py", "local": False, "description": "Controller-merge Hugging Face proof stub"},
    "V30-E003": {"script": "V30-E003-self-healing-bounded.py", "local": True, "description": "Bounded self-healing/support utility"},
    "V30-E004": {"script": "V30-E004-kairotic-integration.py", "local": True, "description": "Kairotic proof using the existing repo surface"},
    "V30-E005": {"script": "V30-E005-living-docs.py", "local": True, "description": "Non-authoritative living docs generation"},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_experiment(experiment_id: str) -> dict:
    meta = EXPERIMENTS[experiment_id]
    script_path = EXPERIMENTS_DIR / meta["script"]
    result = subprocess.run(["python3", str(script_path)], capture_output=True, text=True, check=False)
    artifact_hint = result.stdout.strip().splitlines()[-1].strip() if result.stdout.strip() else ""
    return {
        "experiment_id": experiment_id,
        "description": meta["description"],
        "local": meta["local"],
        "returncode": result.returncode,
        "artifact_hint": artifact_hint,
        "stdout_preview": result.stdout.strip().splitlines()[:10],
        "stderr_preview": result.stderr.strip().splitlines()[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_ids", nargs="*")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()

    if args.list:
        for experiment_id, meta in EXPERIMENTS.items():
            scope = "local" if meta["local"] else "controller"
            print(f"{experiment_id} [{scope}] - {meta['description']}")
        return 0

    selected = args.experiment_ids or list(EXPERIMENTS)
    if args.local_only:
        selected = [experiment_id for experiment_id in selected if EXPERIMENTS.get(experiment_id, {}).get("local")]

    results = [run_experiment(experiment_id) for experiment_id in selected]
    payload = {
        "generated_utc": now_iso(),
        "selected_experiments": selected,
        "results": results,
    }
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACTS_DIR / "v30-experiment-orchestrator-latest.json"
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(artifact_path)
    return 0 if all(result["returncode"] == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
