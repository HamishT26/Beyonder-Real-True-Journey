#!/usr/bin/env python3
"""Invoke the fifteen current v20 laboratory model families once for X2."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


MODELS = [
    "heat", "wave", "oscillator", "reaction", "entropy",
    "queue", "replication", "retry", "graph", "coding",
    "consent", "allocation", "voting", "bayes", "remedy",
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--node", required=True)
    parser.add_argument("--runner", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    results_dir = root / "x2" / "laboratory" / "results"
    requests_dir = root / "x2" / "laboratory" / "requests"
    if results_dir.exists() and any(results_dir.iterdir()):
        raise SystemExit("x2 laboratory results already exist; replay refused")
    results_dir.mkdir(parents=True, exist_ok=True)
    requests_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for index, model in enumerate(MODELS):
        request = {
            "model": model,
            "variant": (index + 1) % 2,
            "steps": 6 + ((index + 1) % 5),
            "parameter": 0.1 + 0.05 * ((index + 1) % 2),
        }
        request_path = requests_dir / f"{model}.json"
        result_path = results_dir / f"{model}.json"
        write_json(request_path, request)
        process = subprocess.run(
            [args.node, args.runner, "model", str(request_path), str(result_path)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError((model, process.stdout, process.stderr))
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if (
            result.get("schema") != "ghc.finite-model.v1"
            or result.get("request") != request
            or not result.get("rows")
            or result.get("empirical_claim") is not False
        ):
            raise RuntimeError((model, "invalid laboratory result"))
        records.append(
            {
                "model": model,
                "request_sha256": hashlib.sha256(request_path.read_bytes()).hexdigest(),
                "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
                "rows": len(result["rows"]),
                "exit_code": process.returncode,
                "empirical_claim": result["empirical_claim"],
            }
        )
    write_json(
        root / "x2" / "laboratory" / "receipt.json",
        {
            "schema": "liora.x2.laboratory-model-receipt.v1",
            "model_invocations": len(records),
            "successes": len(records),
            "replays": 0,
            "records": records,
            "credit_interpretation": "Fifteen distinct current-laboratory X2 model invocations; no rough-set projection is double-counted as a model.",
            "boundary": "Finite synthetic current-laboratory outputs only; no observation, measurement, empirical GMUT result, production THOS or Freed ID, independent reproduction, professional or authority claim. NOT_READY_FOR_STAGE_20.",
        },
    )


if __name__ == "__main__":
    main()
