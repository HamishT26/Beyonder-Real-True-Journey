#!/usr/bin/env python3
"""Validate, smoke, and collision-free promote Elowen v688-v5 tools."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILLS = [
    "ghc-family-sgf-coordinate-profile", "ghc-family-go-neighbor-topology",
    "ghc-family-go-chain-liberties", "ghc-family-go-capture-projection",
    "ghc-family-go-ko-repetition-guard", "ghc-family-sgf-game-tree-structure",
    "ghc-family-sgf-property-escaping", "ghc-family-go-result-timing-reservation",
    "ghc-family-go-record-evidence-boundary", "ghc-family-go-accessible-board",
]
RUNNERS = [
    "ghc_family_go_board_topology.py", "ghc_family_go_capture_rules.py",
    "ghc_family_sgf_tree_records.py", "ghc_family_go_evidence_access.py",
    "ghc_family_go_contract_suite.py",
]


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def file_rows(root: Path, label_root: str, repo: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        data = path.read_bytes()
        source = path.relative_to(repo).as_posix()
        target = f"{label_root}/{path.relative_to(root).as_posix()}"
        rows.append({"source": source, "global_target": target, "bytes": len(data), "sha256_raw_bytes": hashlib.sha256(data).hexdigest(), "byte_equal": True})
    return rows


def parse_result(proc: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError({"stdout": proc.stdout[-1000:], "stderr": proc.stderr[-1000:]}) from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--global-skills", type=Path, required=True)
    parser.add_argument("--global-runners", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve(); bank = args.bank.resolve(); global_skills = args.global_skills.resolve(); global_runners = args.global_runners.resolve(); receipt = args.receipt.resolve()
    if receipt.exists():
        raise SystemExit("promotion receipt already exists; replay refused")
    local_skill_root = repo / "docs" / "elowen-cairn" / "v688-v5" / "skills"
    quick_validate = global_skills / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    proposals = load(repo / "docs" / "elowen-cairn" / "v688-v5" / "x1" / "new-proposal-freeze.json")["proposals"]
    skill_checks = []
    runner_checks = []
    files = []
    for name in SKILLS:
        if (global_skills / name).exists():
            raise SystemExit(f"global skill collision: {name}")
    for name in RUNNERS + ["ghc_family_go_sgf_core.py"]:
        if (global_runners / name).exists():
            raise SystemExit(f"global runner collision: {name}")
    for name in SKILLS:
        skill = local_skill_root / name
        validate = run([sys.executable, "-X", "utf8", str(quick_validate), str(skill)], repo)
        if validate.returncode:
            raise RuntimeError({"skill": name, "validation": validate.stdout + validate.stderr})
        skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
        local_uses = []
        for kind in ("accepting", "adverse"):
            for index in (1, 2):
                fixture = skill / "references" / f"{kind}-{index}.json"
                proc = run([sys.executable, "-B", str(skill / "scripts" / "ghc_family_go_skill.py"), "--input", str(fixture)], repo)
                result = parse_result(proc)
                expected_accept = kind == "accepting"
                if result["accepted"] is not expected_accept or (kind == "accepting" and proc.returncode != 0) or (kind == "adverse" and (proc.returncode != 2 or result["error"] != "FIELD_SET")):
                    raise RuntimeError({"skill": name, "kind": kind, "index": index, "result": result, "returncode": proc.returncode})
                local_uses.append({"kind": kind, "index": index, "accepted": result["accepted"], "error": result["error"]})
        skill_checks.append({"name": name, "quick_validate": True, "skill_read_through_eof": True, "skill_bytes": len(skill_text.encode("utf-8")), "skill_sha256": hashlib.sha256(skill_text.encode("utf-8")).hexdigest(), "local_uses": local_uses})
    fixture_root = bank / "runner-fixtures"
    fixture_root.mkdir(parents=True, exist_ok=True)
    for name in RUNNERS:
        runner = repo / "scripts" / name
        operations_line = next(line for line in runner.read_text(encoding="utf-8").splitlines() if line.startswith("ALLOWED="))
        operations = ast.literal_eval(operations_line.split("=", 1)[1])
        selected = next(row for row in proposals if row["operation"] in operations and row["expected_acceptance"])
        good = fixture_root / (name + ".accepting.json")
        bad = fixture_root / (name + ".adverse.json")
        good.write_text(json.dumps(selected["input"], sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        altered = json.loads(json.dumps(selected["input"], ensure_ascii=True)); altered["execution_request"] = True
        bad.write_text(json.dumps(altered, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        good_run = run([sys.executable, "-B", str(runner), "--input", str(good)], repo); good_result = parse_result(good_run)
        bad_run = run([sys.executable, "-B", str(runner), "--input", str(bad)], repo); bad_result = parse_result(bad_run)
        if good_run.returncode != 0 or not good_result["accepted"] or bad_run.returncode != 2 or bad_result["error"] != "FIELD_SET":
            raise RuntimeError({"runner": name, "good": good_result, "bad": bad_result})
        runner_checks.append({"name": name, "operation": selected["operation"], "local_accepting": True, "local_adverse_refused": True})
    global_runners.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        source = local_skill_root / name; target = global_skills / name
        shutil.copytree(source, target, copy_function=shutil.copy2)
        source_files = [p for p in source.rglob("*") if p.is_file()]
        for path in source_files:
            counterpart = target / path.relative_to(source)
            if path.read_bytes() != counterpart.read_bytes():
                raise RuntimeError(f"skill parity failure: {name}")
        installed_validate = run([sys.executable, "-X", "utf8", str(quick_validate), str(target)], repo)
        if installed_validate.returncode:
            raise RuntimeError({"global_skill": name, "validation": installed_validate.stdout + installed_validate.stderr})
        for kind, code in (("accepting-1.json", 0), ("adverse-1.json", 2)):
            proc = run([sys.executable, "-B", str(target / "scripts" / "ghc_family_go_skill.py"), "--input", str(target / "references" / kind)], repo)
            if proc.returncode != code:
                raise RuntimeError({"global_skill": name, "fixture": kind, "returncode": proc.returncode})
        files.extend(file_rows(source, f"skills/{name}", repo))
    support = repo / "scripts" / "ghc_family_go_sgf_core.py"
    for source in [support] + [repo / "scripts" / name for name in RUNNERS]:
        target = global_runners / source.name
        with target.open("xb") as handle:
            handle.write(source.read_bytes())
        if source.read_bytes() != target.read_bytes():
            raise RuntimeError(f"runner parity failure: {source.name}")
        files.append({"source": source.relative_to(repo).as_posix(), "global_target": f"family-current-runners/{source.name}", "bytes": len(source.read_bytes()), "sha256_raw_bytes": hashlib.sha256(source.read_bytes()).hexdigest(), "byte_equal": True})
    for row in runner_checks:
        name = row["name"]; runner = global_runners / name
        good = fixture_root / (name + ".accepting.json"); bad = fixture_root / (name + ".adverse.json")
        good_run = run([sys.executable, "-B", str(runner), "--input", str(good)], global_runners)
        bad_run = run([sys.executable, "-B", str(runner), "--input", str(bad)], global_runners)
        if good_run.returncode != 0 or bad_run.returncode != 2 or parse_result(bad_run)["error"] != "FIELD_SET":
            raise RuntimeError({"global_runner": name})
        row["installed_accepting"] = True; row["installed_adverse_refused"] = True
    result = {"schema": "ghc.family.additive-tool-promotion.v688.v5", "status": "COMPLETE", "owner": "Elowen Cairn", "phase": "v688-v5", "skills_promoted": 10, "runners_promoted": 5, "support_modules": 1, "support_module_runner_credit": 0, "skills": skill_checks, "runners": runner_checks, "files": files, "parity_files": len(files), "overwrites": 0, "deletions": 0, "local_validation_count": 10, "local_skill_use_count": 40, "installed_validation_count": 10, "installed_skill_use_count": 20, "local_runner_use_count": 10, "installed_runner_use_count": 10, "global_availability_reload_claim": False, "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    write(receipt, result)
    print(json.dumps({"status": result["status"], "skills": 10, "runners": 5, "parity_files": len(files), "overwrites": 0, "installed_checks": 30}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
