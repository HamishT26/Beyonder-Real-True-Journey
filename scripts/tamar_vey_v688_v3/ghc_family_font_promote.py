"""Collision-free byte-preserving promotion of validated font skills and runners."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
SKILL_ROOT = pathlib.Path.home() / ".codex" / "skills"
RUNNER_ROOT = pathlib.Path.home() / ".codex" / "scripts"
VALIDATOR = SKILL_ROOT / ".system/skill-creator/scripts/quick_validate.py"


def invoke(script, payload):
    process = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(script)],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=25,
    )
    return json.loads(process.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    plan = json.loads((BASE / "x1/skill-runner-plan.json").read_text(encoding="utf-8"))
    proposals = json.loads((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    by_operation = {operation: next(row for row in proposals if row["operation"] == operation) for operation in {row["operation"] for row in proposals}}
    skill_use = json.loads((BASE / "x2/skill-use.json").read_text(encoding="utf-8"))
    runner_use = json.loads((BASE / "x2/runner-use.json").read_text(encoding="utf-8"))
    if skill_use["count"] != 10 or runner_use["count"] != 5:
        raise RuntimeError("Local use receipts are incomplete")

    local_skills = [(BASE / "skills" / row["name"], SKILL_ROOT / row["name"], row) for row in plan["skills"]]
    local_runners = [(ROOT / "scripts/tamar_vey_v688_v3" / row["name"], RUNNER_ROOT / row["name"], row) for row in plan["runners"]]
    local_core = ROOT / "scripts/tamar_vey_v688_v3/ghc_family_font_evidence_core.py"
    global_core = RUNNER_ROOT / "ghc_family_font_evidence_core.py"
    collisions = [str(destination.name) for _, destination, _ in local_skills + local_runners if destination.exists()]
    if global_core.exists():
        collisions.append(global_core.name)
    if collisions:
        raise RuntimeError("Global destination collision: " + ", ".join(collisions))

    RUNNER_ROOT.mkdir(parents=True, exist_ok=True)
    for source, destination, _ in local_skills:
        shutil.copytree(source, destination, copy_function=shutil.copy2)
    for source, destination, _ in local_runners:
        shutil.copy2(source, destination)
    shutil.copy2(local_core, global_core)

    skill_validations = 0
    skill_positive = 0
    skill_adverse = 0
    for source, destination, row in local_skills:
        subprocess.run([sys.executable, "-B", "-X", "utf8", str(VALIDATOR), str(destination)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25)
        skill_validations += 1
        proposal = by_operation[row["operations"][0]]
        script = destination / "scripts/ghc_family_font_skill.py"
        positive = invoke(script, json.dumps(proposal["input"], separators=(",", ":"), ensure_ascii=True).encode("ascii"))
        skill_positive += positive == proposal["expected_output"]
        quoted = json.dumps(proposal["operation"])
        duplicate = ("{" + '"operation":' + quoted + ',"operation":' + quoted + "}").encode("ascii")
        adverse = invoke(script, duplicate)
        skill_adverse += adverse == {"accepted": False, "error": "DUPLICATE_KEY", "external_credit": False, "value": None}

    runner_positive = 0
    runner_adverse = 0
    for source, destination, row in local_runners:
        for operation in row["operations"]:
            proposal = by_operation[operation]
            actual = invoke(destination, json.dumps(proposal["input"], separators=(",", ":"), ensure_ascii=True).encode("ascii"))
            runner_positive += actual == proposal["expected_output"]
        quoted = json.dumps(row["operations"][0])
        duplicate = ("{" + '"operation":' + quoted + ',"operation":' + quoted + "}").encode("ascii")
        adverse = invoke(destination, duplicate)
        runner_adverse += adverse == {"accepted": False, "error": "DUPLICATE_KEY", "external_credit": False, "value": None}

    if (skill_validations, skill_positive, skill_adverse, runner_positive, runner_adverse) != (10, 10, 10, 20, 5):
        raise RuntimeError("Global validation or smoke mismatch")

    members = []
    for source, destination, row in local_skills:
        for path in sorted(item for item in source.rglob("*") if item.is_file() and "__pycache__" not in item.parts):
            relative = path.relative_to(source)
            target = destination / relative
            source_bytes = path.read_bytes()
            target_bytes = target.read_bytes()
            if source_bytes != target_bytes:
                raise RuntimeError("Global skill byte mismatch: " + row["name"] + "/" + relative.as_posix())
            members.append(
                {
                    "kind": "skill",
                    "name": row["name"],
                    "relative": relative.as_posix(),
                    "source": path.relative_to(ROOT).as_posix(),
                    "bytes": len(source_bytes),
                    "sha256": hashlib.sha256(source_bytes).hexdigest(),
                }
            )
    for source, destination, row in local_runners:
        source_bytes = source.read_bytes()
        if source_bytes != destination.read_bytes():
            raise RuntimeError("Global runner byte mismatch: " + row["name"])
        members.append({"kind": "runner", "name": row["name"], "relative": row["name"], "source": source.relative_to(ROOT).as_posix(), "bytes": len(source_bytes), "sha256": hashlib.sha256(source_bytes).hexdigest()})
    core_bytes = local_core.read_bytes()
    if core_bytes != global_core.read_bytes():
        raise RuntimeError("Global shared core byte mismatch")
    members.append({"kind": "runner_core", "name": global_core.name, "relative": global_core.name, "source": local_core.relative_to(ROOT).as_posix(), "bytes": len(core_bytes), "sha256": hashlib.sha256(core_bytes).hexdigest()})

    value = {
        "schema": "ghc.family.font-promotion-receipt.v1",
        "skills": 10,
        "runners": 5,
        "shared_core": 1,
        "file_count": len(members),
        "members": members,
        "overwrites": 0,
        "caches_copied": 0,
        "all_source_global_bytes_equal": True,
        "global_skill_validations": skill_validations,
        "global_skill_positive": skill_positive,
        "global_skill_adverse_refused": skill_adverse,
        "global_runner_operations": runner_positive,
        "global_runner_adverse_refused": runner_adverse,
        "independent_reproduction": False,
        "rollback": "Stop selecting the collision-free promoted paths; preserve source, global bytes, and receipt. No existing destination was overwritten.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": 10, "runners": 5, "files": len(members), "byte_equal": True, "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
