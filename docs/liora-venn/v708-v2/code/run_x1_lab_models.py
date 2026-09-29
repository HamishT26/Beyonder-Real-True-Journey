#!/usr/bin/env python3
"""Invoke the fifteen current v20 laboratory model families once for X1."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


MODELS = ["heat", "wave", "oscillator", "reaction", "entropy", "queue", "replication", "retry", "graph", "coding", "consent", "allocation", "voting", "bayes", "remedy"]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--node", required=True)
    parser.add_argument("--runner", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    records = []
    for index, model in enumerate(MODELS):
        request = {"model": model, "variant": index % 2, "steps": 6 + index % 5, "parameter": 0.1 + 0.05 * (index % 2)}
        request_path = root / "x1" / "laboratory" / "requests" / f"{model}.json"
        result_path = root / "x1" / "laboratory" / "results" / f"{model}.json"
        write_json(request_path, request)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        process = subprocess.run([args.node, args.runner, "model", str(request_path), str(result_path)], text=True, capture_output=True)
        if process.returncode != 0:
            raise RuntimeError((model, process.stdout, process.stderr))
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if result.get("schema") != "ghc.finite-model.v1" or result.get("request") != request or not result.get("rows"):
            raise RuntimeError((model, "invalid laboratory result"))
        records.append({"model": model, "request_sha256": hashlib.sha256(request_path.read_bytes()).hexdigest(), "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(), "rows": len(result["rows"]), "exit_code": process.returncode, "empirical_claim": result.get("empirical_claim")})
    write_json(root / "x1" / "laboratory" / "receipt.json", {"schema": "liora.x1.laboratory-model-receipt.v1", "model_invocations": len(records), "successes": len(records), "replays": 0, "records": records, "credit_interpretation": "Fifteen current-laboratory model invocations. The fifteen rough-set coordinate files are bounded projections of owner results and receive no additional model-count credit.", "boundary": "Finite synthetic current-laboratory outputs only; no observation, measurement, empirical GMUT result, production THOS or Freed ID, independent reproduction, professional or authority claim. NOT_READY_FOR_STAGE_20."})


if __name__ == "__main__":
    main()
