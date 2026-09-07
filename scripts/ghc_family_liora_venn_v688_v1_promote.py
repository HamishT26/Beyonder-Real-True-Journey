"""Exclusively promote ten validated Liora skills and five compatible runners."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/liora-venn/v688-v1")
X1 = "421abce86426674b67e0cbd5ce63ad463421fc9f"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_liora_venn_v688_v1_x1_audit import privacy


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--runner-root", type=Path, required=True)
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads((ROOT / BASE / "x1/skill-runner-plan.json").read_text(encoding="utf-8"))
    assert not args.runner_root.exists(), "RUNNER_BANK_COLLISION"
    members = []
    for item in plan["skills"]:
        source = ROOT / BASE / "skills" / item["name"]
        destination = args.skill_root / item["name"]
        assert not destination.exists(), "SKILL_COLLISION:" + item["name"]
        manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
        expected = {row["relative"] for row in manifest["members"]} | {"manifest.json"}
        actual = {path.relative_to(source).as_posix() for path in source.rglob("*") if path.is_file()}
        assert expected == actual, item["name"]
        for row in manifest["members"]:
            assert hashlib.sha256((source / row["relative"]).read_bytes()).hexdigest() == row["sha256"]
        for relative in sorted(actual):
            members.append({"kind": "skill", "name": item["name"], "relative": relative, "source": (BASE / "skills" / item["name"] / relative).as_posix()})
    for name in [row["name"] for row in plan["runners"]] + [plan["core"]]:
        members.append({"kind": "runner", "name": name, "relative": name, "source": "scripts/" + name})
    assert len(members) == 56, len(members)
    data = {row["source"]: (ROOT / row["source"]).read_bytes() for row in members}
    scan = privacy(data)
    assert scan["confirmed_hits"] == 0, scan
    target = ROOT / BASE / "x2/promotion-receipt.json"
    assert not target.exists(), "PROMOTION_RECEIPT_ALREADY_EXISTS"
    for item in plan["skills"]:
        (args.skill_root / item["name"]).mkdir()
    args.runner_root.mkdir(parents=True)
    for row in members:
        destination = args.skill_root / row["name"] / row["relative"] if row["kind"] == "skill" else args.runner_root / row["relative"]
        allowed_root = (args.skill_root / row["name"]).resolve() if row["kind"] == "skill" else args.runner_root.resolve()
        assert destination.resolve().is_relative_to(allowed_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = data[row["source"]]
        with destination.open("xb") as handle:
            handle.write(raw)
        assert destination.read_bytes() == raw
        row.update({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})

    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    validations = []
    for item in plan["skills"]:
        result = subprocess.run([sys.executable, "-X", "utf8", str(args.skill_root / ".system/skill-creator/scripts/quick_validate.py"), str(args.skill_root / item["name"])], capture_output=True, text=True, encoding="utf-8", env=env)
        assert result.returncode == 0, (item["name"], result.stdout, result.stderr)
        validations.append({"name": item["name"], "global_quick_validate_pass": True})

    cases = json.loads((ROOT / BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    global_smokes = []
    for item in plan["runners"]:
        for operation in item["operations"]:
            fixture = args.bank / "smoke-inputs" / (operation + ".json")
            case = next(row for row in cases if row["operation"] == operation and row["expected_output"]["accepted"])
            result = subprocess.run([sys.executable, "-X", "utf8", str(args.runner_root / item["name"]), str(fixture)], capture_output=True, text=True, encoding="utf-8", env=env)
            assert result.returncode == 0 and canonical(json.loads(result.stdout)) == canonical(case["expected_output"]), (item["name"], operation)
            global_smokes.append({"runner": item["name"], "operation": operation, "fixture": case["proposal_id"], "pass": True, "duplicate_witness_credit": 0})
    for row in members:
        destination = args.skill_root / row["name"] / row["relative"] if row["kind"] == "skill" else args.runner_root / row["relative"]
        assert hashlib.sha256(destination.read_bytes()).hexdigest() == row["sha256"]
    receipt = {
        "schema": "ghc.family.exclusive-promotion.v1",
        "owner": "Liora Venn",
        "phase": "v688-v1",
        "x1": X1,
        "skill_count": 10,
        "runner_count": 5,
        "shared_dependencies": 1,
        "file_count": 56,
        "members": members,
        "prepromotion_privacy": scan,
        "global_skill_validation": validations,
        "global_runner_operation_smokes": global_smokes,
        "overwrites": 0,
        "source_global_byte_equal": True,
        "caches_copied": 0,
        "source_compatibility_preserved": True,
        "runner_bank_label": "Liora Venn v688-v1 additive global tools",
        "rollback": "Stop selecting these additive packages; retain source, receipt, and older callers. No deletion is performed.",
        "boundary": "Promotion proves byte parity and bounded callable behavior only; no empirical, professional, production, legal, cultural, Māori-authority, independent-reproduction, or Stage 20 claim.",
    }
    target.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"state": "GLOBAL_PROMOTION_PASS", "promoted_skills": 10, "promoted_runners": 5, "parity_files": 56, "operation_smokes": 10, "overwrites": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
