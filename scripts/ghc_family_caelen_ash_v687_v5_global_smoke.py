#!/usr/bin/env python3
"""Smoke the five copied global Caelen v687-v5 runner interfaces after byte-parity promotion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, OPS
from ghc_family_caelen_ash_v687_v5_core import strict_equal, strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-evidence", type=Path, required=True)
    parser.add_argument("--global-scripts", type=Path, required=True)
    args = parser.parse_args()
    proposals = strict_load(PHASE / "x1" / "new-proposals.json")["proposals"]
    by_operation = {operation: next(row for row in proposals if row["operation"] == operation) for operation, *_ in OPS[:5]}
    rows = []
    for operation, *_ in OPS[:5]:
        target = args.global_scripts / f"ghc_family_caelen_ash_v687_v5_{operation}.py"
        input_path = args.runtime_evidence / f"{operation}-input.json"
        output_path = args.runtime_evidence / f"{operation}-global-output.json"
        run = subprocess.run(
            [sys.executable, str(target), "--input", str(input_path), "--output", str(output_path)],
            cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
        )
        expected = by_operation[operation]["expected_output"]
        observed = strict_load(output_path) if output_path.exists() else None
        rows.append(
            {
                "operation": operation,
                "exit_code": run.returncode,
                "complete_result_matched": run.returncode == 0 and strict_equal(observed, expected),
                "global_copy": True,
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    if not all(row["complete_result_matched"] for row in rows):
        raise SystemExit("global shared-interface smoke failed")
    destination = PHASE / "x2" / "global-install-smoke.json"
    with destination.open("xb") as stream:
        stream.write((json.dumps(rows, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8"))
    print(json.dumps({"global_shared_interfaces_smoked": len(rows), "passed": len(rows)}))


if __name__ == "__main__":
    main()
