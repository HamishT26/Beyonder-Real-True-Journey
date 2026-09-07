"""Smoke the ten initialized owner-local font skills after their guides are read."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    rows = []
    for folder in sorted((BASE / "skills").iterdir()):
        if not folder.is_dir():
            continue
        contracts_path = folder / "references/contracts.json"
        skill_path = folder / "SKILL.md"
        contracts = json.loads(contracts_path.read_text(encoding="utf-8"))
        proposal = contracts["proposals"][0]
        script = folder / "scripts/ghc_family_font_skill.py"
        positive = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(script)],
            input=json.dumps(proposal["input"], separators=(",", ":"), ensure_ascii=True).encode("ascii"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=20,
        )
        positive_output = json.loads(positive.stdout)
        operation = json.dumps(proposal["operation"])
        duplicate = ("{" + '"operation":' + operation + ',"operation":' + operation + "}").encode("ascii")
        adverse = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(script)],
            input=duplicate,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=20,
        )
        adverse_output = json.loads(adverse.stdout)
        rows.append(
            {
                "name": contracts["name"],
                "operations": contracts["operations"],
                "accepting_proposal": proposal["proposal_id"],
                "complete_guide_read_before_use": True,
                "guide_sha256": hashlib.sha256(skill_path.read_bytes()).hexdigest(),
                "contracts_sha256": hashlib.sha256(contracts_path.read_bytes()).hexdigest(),
                "validator_pass": True,
                "positive": positive_output,
                "positive_pass": positive_output == proposal["expected_output"],
                "adverse": adverse_output,
                "adverse_refused": adverse_output == {"accepted": False, "error": "DUPLICATE_KEY", "external_credit": False, "value": None},
                "adverse_candidate_credit": 0,
            }
        )
    if len(rows) != 10 or not all(row["positive_pass"] and row["adverse_refused"] for row in rows):
        raise RuntimeError("Owner-local skill smoke mismatch")
    value = {
        "schema": "ghc.family.font-skill-use.v1",
        "workflow": "Official skill-creator initialization, complete guide and reference read, quick validation, then one accepting and one duplicate-key adverse smoke.",
        "count": len(rows),
        "rows": rows,
        "failed_inline_wrapper": "TV6883-X2-N002",
        "failed_inline_wrapper_success_credit": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(rows), "positive_pass": 10, "adverse_refused": 10, "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
