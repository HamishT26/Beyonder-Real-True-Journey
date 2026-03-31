#!/usr/bin/env python3
"""Bounded Hugging Face read proof with controller-result merge support."""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def public_model_probe() -> dict:
    req = urllib.request.Request(
        "https://huggingface.co/api/models?limit=3&sort=trendingScore",
        headers={"user-agent": "v30-fluid-lab/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    model_ids = [row.get("id", "") for row in payload if isinstance(row, dict)]
    return {
        "http_status": 200,
        "model_ids": [item for item in model_ids if item][:3],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller-result", default="")
    args = parser.parse_args()

    sandbox_root = Path("/home/aletheon/v30-fluid-lab")
    artifact_path = sandbox_root / "artifacts" / "v30-e002-hf-materialization-latest.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_utc": now_iso(),
        "experiment_id": "V30-E002",
        "overall_status": "WARN",
        "proof_state": "read_only_verified",
        "public_read_probe": {},
        "execution_mode": "controller_preferred",
        "blockers": [
            "A lightweight controller or session-level execution proof is still required to promote Hugging Face beyond read-only verification.",
        ],
        "controller_result_path": args.controller_result or "",
        "controller_result": {},
    }

    try:
        payload["public_read_probe"] = public_model_probe()
    except Exception as exc:  # pragma: no cover - bounded probe
        payload["public_read_probe"] = {"error": str(exc)}
        payload["overall_status"] = "WARN"
        payload["proof_state"] = "open_with_blocker"
        payload["blockers"] = [f"Public Hugging Face model-list probe failed: {exc}"]

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
