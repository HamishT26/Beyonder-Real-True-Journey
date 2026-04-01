#!/usr/bin/env python3
"""Controller-aware Gmail proof artifact for V30."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller-result", default="")
    args = parser.parse_args()

    sandbox_root = Path("/home/aletheon/v30-fluid-lab")
    artifact_path = sandbox_root / "artifacts" / "v30-e001-gmail-materialization-latest.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_utc": now_iso(),
        "experiment_id": "V30-E001",
        "overall_status": "WARN",
        "proof_state": "open_with_blocker",
        "execution_mode": "controller_required",
        "steps_expected": [
            "read inbox state",
            "create draft",
            "optional send-to-self and read-back only with explicit execution-time confirmation",
        ],
        "blockers": [
            "The Gmail connector/tool surface is not available inside the bounded WSL runtime bundle.",
            "This experiment must be completed by the session controller or a future Gmail connector lane.",
        ],
        "controller_result_path": args.controller_result or "",
        "controller_result": {},
    }

    if args.controller_result:
        controller_result = read_json(Path(args.controller_result))
        if controller_result:
            payload["controller_result"] = controller_result
            payload["overall_status"] = controller_result.get("overall_status", payload["overall_status"])
            payload["proof_state"] = controller_result.get("proof_state", payload["proof_state"])
            payload["blockers"] = controller_result.get("blockers", payload["blockers"])

    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(artifact_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
