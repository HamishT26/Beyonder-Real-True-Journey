"""Build, validate, smoke, and optionally promote Vesper configuration skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "docs/vesper-arlen/v686-v3"
GLOBAL_SKILLS = Path.home() / ".codex/skills"
QUICK_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
RUNNER_MAP = {
    "toml": "ghc_family_config_toml.py",
    "layers": "ghc_family_config_layers.py",
    "transaction": "ghc_family_config_transaction.py",
    "assurance": "ghc_family_config_assurance.py",
    "obligations": "ghc_family_config_obligations.py",
}
RUNNERS = [ROOT / "scripts" / name for name in RUNNER_MAP.values()]


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def read(relative: str) -> object:
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def smoke(script: Path, row: dict, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    positive = output / "positive-input.json"
    adverse = output / "duplicate-member-input.json"
    write(positive, row["input"])
    adverse.write_text('{"a":1,"a":2}\n', encoding="utf-8", newline="\n")
    positive_result = output / "positive-output.json"
    adverse_result = output / "adverse-output.json"
    first = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), "--operation", row["operation"], "--input", str(positive), "--output", str(positive_result)],
        capture_output=True,
    )
    second = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), "--operation", row["operation"], "--input", str(adverse), "--output", str(adverse_result)],
        capture_output=True,
    )
    expected_code = 2 if isinstance(row["expected_result"], dict) and set(row["expected_result"]) == {"error"} else 0
    observed = json.loads(positive_result.read_text(encoding="utf-8"))["result"]
    rejected = json.loads(adverse_result.read_text(encoding="utf-8"))["result"]
    passed = first.returncode == expected_code and canonical(observed) == canonical(row["expected_result"]) and second.returncode == 2 and rejected == {"error": "duplicate_json_member"}
    receipt = {
        "proposal_id": row["proposal_id"],
        "positive_returncode": first.returncode,
        "positive_pass": canonical(observed) == canonical(row["expected_result"]),
        "adverse_returncode": second.returncode,
        "adverse_rejected": rejected == {"error": "duplicate_json_member"},
        "pass": passed,
        "negative_success_credit": 0,
        "same_owner_only": True,
        "runner_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    write(output / "smoke-receipt.json", receipt)
    if not passed:
        raise AssertionError("Skill or runner smoke failed; retained output has zero aggregate credit.")
    return receipt


def build() -> None:
    rows = read("x1/new-proposals.json")["proposals"]
    plan = read("x1/skill-runner-plan.json")
    validation_receipts = []
    for skill in plan["skills"]:
        folder = BASE / "skills" / skill["name"]
        folder.mkdir(parents=True, exist_ok=False)
        selected = [row for row in rows if row["family"] in skill["families"]]
        example = selected[0]
        trigger_text = " and ".join(trigger.replace("_", " ") for trigger in skill["families"])
        description = f"Review {trigger_text} in bounded synthetic configuration evidence."
        body = f'''---
name: {skill['name']}
description: {description}
---

# {skill['name'].removeprefix('ghc-family-').replace('-', ' ').title()}

Read [the frozen contracts](references/contracts.json) and select only the family and operation matching the current authorized configuration question. The two routed families are `{skill['families'][0]}` and `{skill['families'][1]}`. Their examples are synthetic fixtures, not facts about a person, organization, live service, credential, physical system, or authority.

Use an owner-controlled copy. Preserve exact JSON types, explicit null, false, zero, source origin, and predecessor bytes. Refuse duplicate JSON members, nonfinite values, over-budget trees, ambiguous configuration paths, missing parents, unlisted subtrees, forged receipt scope, and any empirical or authority promotion. A structured refusal may be the frozen passing result for an intentionally invalid fixture.

Run the relevant family-current runner from `scripts/` with `--operation`, `--input`, and a fresh exclusive `--output` path. Before adopting a changed caller, run one frozen accepting case and the duplicate-member adversary. A failed definition remains retained at zero success credit; a correction is separate and hash-bound. Roll back by selecting the previous validated package while preserving this package and its receipts.

TOML and INI edits are synthetic, in-memory or owner-local evidence. No configuration is deployed, no credential is loaded, no account or external system is changed, and no professional change approval is conferred. GMUT remains an unconfirmed typed scalar-tensor/EFT research-model family; THOS remains synthetic and proxy-only; Freed ID remains synthetic and nonproduction. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct and preserve `NOT_READY_FOR_STAGE_20`.
'''
        (folder / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        agents = folder / "agents"
        agents.mkdir()
        prompt = f"Use ${skill['name']} to review one bounded synthetic configuration contract."
        yaml = f'''interface:
  display_name: "{skill['name'].removeprefix('ghc-family-').replace('-', ' ').title()}"
  short_description: "Review bounded synthetic configuration changes"
  default_prompt: "{prompt}"
policy:
  allow_implicit_invocation: true
'''
        (agents / "openai.yaml").write_text(yaml, encoding="utf-8", newline="\n")
        write(folder / "references/contracts.json", {"source_x1": read("validation/x1-equality.json")["x1"], "criteria": selected, "inherited_execution_credit": 0, "same_owner_only": True})
        scripts = folder / "scripts"
        scripts.mkdir()
        for source in RUNNERS:
            shutil.copyfile(source, scripts / source.name)
        validation = subprocess.run([sys.executable, "-X", "utf8", str(QUICK_VALIDATE), str(folder)], capture_output=True, text=True)
        if validation.returncode != 0:
            raise AssertionError("Local skill metadata validation failed; diagnostic retained outside public artifacts.")
        receipt = smoke(scripts / RUNNER_MAP[example["runner"]], example, BASE / "tooling/skill-smokes" / skill["name"])
        validation_receipts.append({"name": skill["name"], "metadata_validation_pass": True, "smoke": receipt, "families": skill["families"]})

    runner_receipts = []
    for runner_key, filename in RUNNER_MAP.items():
        row = next(item for item in rows if item["runner"] == runner_key)
        runner_receipts.append({"runner": filename, "smoke": smoke(ROOT / "scripts" / filename, row, BASE / "tooling/runner-smokes" / filename.removesuffix(".py"))})
    write(BASE / "tooling/local-skill-validation.json", {"skills": validation_receipts, "runners": runner_receipts, "unique_new_shared_runners": 5, "same_owner_only": True, "independent_reproduction": False})
    print(json.dumps({"skills_validated": len(validation_receipts), "unique_shared_runners_smoked": len(runner_receipts)}))


def promote() -> None:
    validation = read("tooling/local-skill-validation.json")
    plan = read("x1/skill-runner-plan.json")
    assert len(validation["skills"]) == 10
    for skill in plan["skills"]:
        policy = read("tooling/promotion-checks/" + skill["name"] + ".json")
        assert policy["state"] == "ready" and all(policy["checks"].values())
        assert not (GLOBAL_SKILLS / skill["name"]).exists()
    entries = []
    for item in validation["skills"]:
        assert item["metadata_validation_pass"] and item["smoke"]["pass"]
        source = BASE / "skills" / item["name"]
        destination = GLOBAL_SKILLS / item["name"]
        if destination.exists():
            raise FileExistsError("Global collision; no overwrite is permitted.")
        shutil.copytree(source, destination)
        global_validation = subprocess.run([sys.executable, "-X", "utf8", str(QUICK_VALIDATE), str(destination)], capture_output=True, text=True)
        assert global_validation.returncode == 0
        for path in sorted(source.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(source)
            local_bytes = path.read_bytes()
            global_bytes = (destination / relative).read_bytes()
            assert local_bytes == global_bytes
            entries.append({"skill": item["name"], "path": relative.as_posix(), "bytes": len(local_bytes), "sha256": hashlib.sha256(local_bytes).hexdigest()})
    write(BASE / "tooling/global-promotion.json", {"skills": 10, "unique_new_shared_runners": 5, "entries": entries, "byte_parity": True, "collision_overwrites": 0, "rollback": "Select retained prior tooling and preserve these additive packages and receipts.", "same_owner_only": True, "catalogue_reload_claimed": False})
    print(json.dumps({"promoted_skills": 10, "global_files_verified": len(entries), "byte_parity": True}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--promote", action="store_true")
    args = parser.parse_args()
    promote() if args.promote else build()
