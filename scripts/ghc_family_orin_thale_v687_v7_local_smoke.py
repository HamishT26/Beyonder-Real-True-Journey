#!/usr/bin/env python3
"""Validate and smoke-use Orin v687-v7 local skills and runners."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
X2 = PHASE / "x2"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick-validate", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    skill_receipt = json.loads((X2 / "skill-validation.json").read_text(encoding="utf-8"))
    skill_smokes = []
    for row in skill_receipt["skills"]:
        root = PHASE / "skills" / row["skill"]
        result = run([sys.executable, "-X", "utf8", str(args.quick_validate), str(root)], ROOT)
        if result.returncode:
            raise RuntimeError(f"skill validation failed: {row['skill']}: {result.stdout} {result.stderr}")
        contracts = json.loads((root / "references" / "contracts.json").read_text(encoding="utf-8"))["contracts"]
        contract = contracts[0]
        fixture = args.scratch / f"{row['operation']}-valid.json"
        fixture.write_text(json.dumps(contract["input"], sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        script = root / "scripts" / f"ghc_family_{row['operation']}.py"
        positive = run([sys.executable, str(script), "--input", str(fixture)], script.parent)
        if positive.returncode or json.loads(positive.stdout) != contract["expected_output"]:
            raise RuntimeError(f"skill positive smoke failed: {row['skill']}")
        duplicate = args.scratch / f"{row['operation']}-duplicate.json"
        duplicate.write_text('{"operation":"x","operation":"x"}\n', encoding="utf-8", newline="\n")
        adverse = run([sys.executable, str(script), "--input", str(duplicate)], script.parent)
        if adverse.returncode == 0:
            raise RuntimeError(f"skill duplicate-key smoke escaped: {row['skill']}")
        row["quick_validation"] = "PASSED"
        row["smoke_use"] = "PASSED"
        skill_smokes.append({"skill": row["skill"], "positive": True, "duplicate_key_rejected": True})
    skill_receipt["local_validation_state"] = "PASSED"
    write(X2 / "skill-validation.json", skill_receipt)
    runner_receipt = json.loads((X2 / "runner-smokes.json").read_text(encoding="utf-8"))
    proposals = json.loads((PHASE / "x1" / "new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    runner_smokes = []
    for no, row in enumerate(runner_receipt["rows"], 1):
        contract = proposals[(no - 1) * 40]
        fixture = args.scratch / f"runner-{no:02d}-valid.json"
        fixture.write_text(json.dumps(contract["input"], sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        script = ROOT / row["runner"]
        positive = run([sys.executable, str(script), "--input", str(fixture)], ROOT / "scripts")
        if positive.returncode or json.loads(positive.stdout) != contract["expected_output"]:
            raise RuntimeError(f"runner positive smoke failed: {row['runner']}")
        duplicate = args.scratch / f"runner-{no:02d}-duplicate.json"
        duplicate.write_text('{"operation":"x","operation":"x"}\n', encoding="utf-8", newline="\n")
        adverse = run([sys.executable, str(script), "--input", str(duplicate)], ROOT / "scripts")
        if adverse.returncode == 0:
            raise RuntimeError(f"runner duplicate-key smoke escaped: {row['runner']}")
        row["positive_smoke"] = "PASSED"
        row["duplicate_key_smoke"] = "REJECTED"
        runner_smokes.append({"runner": row["runner"], "positive": True, "duplicate_key_rejected": True})
    runner_receipt["local_validation_state"] = "PASSED"
    write(X2 / "runner-smokes.json", runner_receipt)
    receipt = {"schema": "ghc.family.local-skill-runner-smoke.v1", "skills": skill_smokes, "runners": runner_smokes, "skill_count": len(skill_smokes), "runner_count": len(runner_smokes), "same_owner_only": True, "independent_reproduction": False}
    write(PHASE / "validation" / "x2-local-smoke.json", receipt)
    print(json.dumps({"status": "PASSED", "skills": len(skill_smokes), "runners": len(runner_smokes)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
