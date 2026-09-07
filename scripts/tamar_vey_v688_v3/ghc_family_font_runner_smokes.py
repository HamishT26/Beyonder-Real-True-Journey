"""Exercise five owner-local family-current font runners."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"


def invoke(script, payload):
    result = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(script)],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=20,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    plan = json.loads((BASE / "x1/skill-runner-plan.json").read_text(encoding="utf-8"))
    proposals = json.loads((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    by_operation = {operation: next(row for row in proposals if row["operation"] == operation) for operation in {row["operation"] for row in proposals}}
    rows = []
    for runner in plan["runners"]:
        script = ROOT / "scripts/tamar_vey_v688_v3" / runner["name"]
        operations = []
        for operation in runner["operations"]:
            proposal = by_operation[operation]
            actual = invoke(script, json.dumps(proposal["input"], separators=(",", ":"), ensure_ascii=True).encode("ascii"))
            operations.append({"operation": operation, "proposal_id": proposal["proposal_id"], "actual_output": actual, "pass": actual == proposal["expected_output"]})
        quoted = json.dumps(runner["operations"][0])
        duplicate = ("{" + '"operation":' + quoted + ',"operation":' + quoted + "}").encode("ascii")
        adverse = invoke(script, duplicate)
        rows.append(
            {
                "name": runner["name"],
                "operations": operations,
                "adverse": adverse,
                "adverse_refused": adverse == {"accepted": False, "error": "DUPLICATE_KEY", "external_credit": False, "value": None},
                "adverse_candidate_credit": 0,
                "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            }
        )
    if len(rows) != 5 or sum(len(row["operations"]) for row in rows) != 20:
        raise RuntimeError("Runner count mismatch")
    if not all(item["pass"] for row in rows for item in row["operations"]) or not all(row["adverse_refused"] for row in rows):
        raise RuntimeError("Runner smoke mismatch")
    value = {"schema": "ghc.family.font-runner-use.v1", "count": 5, "positive_operations": 20, "rows": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": 5, "positive_operations": 20, "adverse_refused": 5, "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
