from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipts = []
    for index in range(1, 11):
        runner = ROOT / "scripts" / f"ghc_family_lens_runner_{index:02d}.py"
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(runner)], capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        receipts.append({"runner": runner.stem, "returncode": result.returncode, **payload})
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "owner": "Tamar Vey",
        "passed_count": sum(row.get("positive_accepted") and row.get("invalid_rejected") for row in receipts),
        "phase": "v680-v3",
        "receipts": receipts,
        "runner_count": len(receipts),
        "schema": "ghc.family.runner-smoke.v680.v3.x2",
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(receipts), "passed": payload["passed_count"]}))
    return 0 if payload["passed_count"] == 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
