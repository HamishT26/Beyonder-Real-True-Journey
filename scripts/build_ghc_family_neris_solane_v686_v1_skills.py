"""Build, validate, smoke, and collision-safely promote ten Neris report skills."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
X1 = "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323"
RUNNERS = ["trace", "budget", "analysis", "provenance", "export"]


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def write_json(path: Path, value) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True, encoding="utf-8")


def validate(validator: Path, folder: Path) -> dict:
    process = run([sys.executable, "-B", "-X", "utf8", str(validator), str(folder)])
    return {"exit_code": process.returncode, "output": (process.stdout + process.stderr).strip(), "valid": process.returncode == 0}


def smoke(folder: Path, proposal: dict) -> dict:
    runner = folder / "scripts" / ("ghc_family_report_" + proposal["runner"] + ".py")
    positive = run([sys.executable, "-B", "-X", "utf8", str(runner), "--fixture", str(folder / "references/positive.json")], cwd=folder)
    adverse = run([sys.executable, "-B", "-X", "utf8", str(runner), "--fixture", str(folder / "references/adverse.json")], cwd=folder)
    positive_value = json.loads(positive.stdout) if positive.returncode == 0 and positive.stdout.strip() else {}
    adverse_value = json.loads(adverse.stdout) if adverse.returncode == 0 and adverse.stdout.strip() else {}
    return {
        "positive": positive.returncode == 0 and positive_value.get("accepted") is True,
        "adverse": adverse.returncode == 0 and adverse_value.get("accepted") is False and "malformed_fixture" in adverse_value.get("errors", []),
        "positive_observed": positive_value,
        "adverse_observed": adverse_value,
    }


def files_manifest(folder: Path) -> list[dict]:
    return [
        {"path": path.relative_to(folder).as_posix(), "bytes": path.stat().st_size, "sha256": hash_file(path)}
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    ]


def prepare(validator: Path) -> list[dict]:
    plan = read("x1/skill-runner-plan.json")
    proposals = read("x1/new-proposals.json")["proposals"]
    identity = read("x1/identity-and-practice.json")
    results = []
    for skill in plan["skills"]:
        folder = BASE / "skills" / skill["name"]
        selected = [proposal for proposal in proposals if proposal["family"] in skill["families"]]
        first = selected[0]
        runner_names = sorted({proposal["runner"] for proposal in selected})
        description = "Audit synthetic " + " and ".join(name.replace("_", " ") for name in skill["families"]) + " reports with frozen typed oracles and retained failures."
        source_lines = "\n".join(f"- [{url}]({url})" for url in skill["source_refs"])
        guide = f'''---
name: {skill["name"]}
description: {json.dumps(description)}
---

# {skill["name"].removeprefix("ghc-family-").replace("-", " ").title()}

Use this skill when one of the two retained families in [the frozen contracts](references/contracts.json) exactly matches a synthetic report review. Select by family and operation, not lexical resemblance. The package validates a reported JSON value against a frozen input, preserves strict JSON types, records the computed result, and verifies that the input did not mutate.

Run the matching `scripts/ghc_family_report_*.py` with `--fixture references/positive.json`. A fixture must contain `operation`, `input`, and `reported`. The adverse fixture intentionally omits a required field and must return `malformed_fixture`. Preserve that rejection rather than broadening the input silently.

The package includes five shared report tribunals and their five inherited protocol dependencies so it remains portable. Ten package copies still represent five unique new report runners. Read the exact source contract before adapting a fixture; never replace a preregistered oracle with observed output.

Primary vocabulary sources:

{source_lines}

A local pass is same-owner software evidence only. It does not establish a real participant, operational system, empirical GMUT result, professional qualification, production identity lifecycle, complete privacy or accessibility, exhaustive security, independent reproduction, legal or cultural authority, Māori authority, consciousness, personhood, a Theory of Everything, canon, or Stage 20 readiness.

Rollback selects a retained prior skill or holds the affected family. It does not delete this package, a failed witness, history, or another owner's work. {identity["identity_boundary"]}
'''
        write_text(folder / "SKILL.md", guide)
        write_text(
            folder / "agents/openai.yaml",
            "interface:\n"
            + "  display_name: " + json.dumps(skill["name"].removeprefix("ghc-family-").replace("-", " ").title()) + "\n"
            + "  short_description: \"Audit typed synthetic reports and refusals\"\n"
            + "  default_prompt: " + json.dumps("Use $" + skill["name"] + " to audit this bounded synthetic report.") + "\n",
        )
        write_json(folder / "references/contracts.json", {"families": skill["families"], "contracts": selected, "protected_gates": identity["protected_gates"]})
        write_json(folder / "references/positive.json", {"operation": first["operation"], "input": first["input"], "reported": first["expected_result"]})
        write_json(folder / "references/adverse.json", {"operation": first["operation"], "input": first["input"]})
        for runner in RUNNERS:
            for prefix in ["report", "protocol"]:
                source = ROOT / "scripts" / f"ghc_family_{prefix}_{runner}.py"
                destination = folder / "scripts" / source.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("xb") as stream:
                    stream.write(source.read_bytes())
        first_validation = validate(validator, folder)
        first_smoke = smoke(folder, first)
        if not first_validation["valid"] or not first_smoke["positive"] or not first_smoke["adverse"]:
            raise RuntimeError("Local skill candidate failed: " + skill["name"])
        promotion = {
            "schema": "ghc.family.neris.skill-promotion.v1",
            "source_x1": X1,
            "owner": "Neris Solane",
            "phase": "v686-v1",
            "families": skill["families"],
            "unique_new_runners_used": runner_names,
            "all_shared_report_runners": [f"ghc_family_report_{name}.py" for name in RUNNERS],
            "inherited_protocol_dependencies": [f"ghc_family_protocol_{name}.py" for name in RUNNERS],
            "candidate_validation": first_validation,
            "candidate_smoke": first_smoke,
            "global_destination_preflight": "collision_free_in_x1_and_rechecked_at_install",
            "rollback": "Select a retained prior skill; preserve this package and all failures.",
            "same_owner_only": True,
        }
        write_json(folder / "references/promotion.json", promotion)
        second_validation = validate(validator, folder)
        if not second_validation["valid"]:
            raise RuntimeError("Skill became invalid after promotion record: " + skill["name"])
        results.append(
            {
                "name": skill["name"],
                "source": folder.relative_to(ROOT).as_posix(),
                "families": skill["families"],
                "contract_count": len(selected),
                "validation": second_validation,
                "smoke": first_smoke,
                "files": files_manifest(folder),
            }
        )
    write_json(BASE / "x2/local-skills-validation.json", {"schema": "ghc.family.neris.local-skills.v1", "skills": results, "count": len(results), "unique_shared_report_runners": 5, "same_owner_only": True})
    return results


def install(validator: Path, global_root: Path, prepared: list[dict]) -> list[dict]:
    installed = []
    proposals = read("x1/new-proposals.json")["proposals"]
    for row in prepared:
        source = ROOT / row["source"]
        destination = global_root / row["name"]
        if destination.exists():
            raise FileExistsError("Global skill destination collision: " + row["name"])
        shutil.copytree(source, destination)
        source_files = row["files"]
        destination_files = files_manifest(destination)
        parity = source_files == destination_files
        validation = validate(validator, destination)
        first = next(proposal for proposal in proposals if proposal["family"] in row["families"])
        observed_smoke = smoke(destination, first)
        result = {
            "name": row["name"],
            "source": row["source"],
            "file_count": len(source_files),
            "byte_parity": parity,
            "post_copy_validation": validation,
            "post_copy_smoke": observed_smoke,
            "files": source_files,
        }
        installed.append(result)
        if not parity or not validation["valid"] or not observed_smoke["positive"] or not observed_smoke["adverse"]:
            write_json(BASE / "x2/global-promotion-partial.json", {"installations": installed, "success_credit": 0})
            raise RuntimeError("Installed skill failed validation: " + row["name"])
    write_json(
        BASE / "x2/global-promotion-installation.json",
        {
            "schema": "ghc.family.neris.global-promotion.v1",
            "skills": installed,
            "installed_count": len(installed),
            "unique_shared_report_runners": 5,
            "inherited_protocol_dependencies": 5,
            "status": "PASS",
            "deletions": 0,
            "overwrites": 0,
            "plugin_cache_mutation": False,
            "same_owner_only": True,
            "catalogue_reload_claimed": False,
        },
    )
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validator", required=True, type=Path)
    parser.add_argument("--global-root", required=True, type=Path)
    args = parser.parse_args()
    prepared = prepare(args.validator)
    installed = install(args.validator, args.global_root, prepared)
    print(json.dumps({"local_skills": len(prepared), "global_skills": len(installed), "unique_shared_runners": 5, "byte_parity": all(row["byte_parity"] for row in installed)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
