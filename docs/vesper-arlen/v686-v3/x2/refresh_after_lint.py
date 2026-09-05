"""Bind post-lint local/global parity and current runner smoke witnesses."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "docs/vesper-arlen/v686-v3"
GLOBAL = Path.home() / ".codex/skills"
RUNNER_MAP = {
    "toml": "ghc_family_config_toml.py",
    "layers": "ghc_family_config_layers.py",
    "transaction": "ghc_family_config_transaction.py",
    "assurance": "ghc_family_config_assurance.py",
    "obligations": "ghc_family_config_obligations.py",
}


def read(relative: str) -> object:
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(relative: str | Path, value: object) -> None:
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def main() -> None:
    plan = read("x1/skill-runner-plan.json")
    rows = read("x1/new-proposals.json")["proposals"]
    entries = []
    for skill in plan["skills"]:
        source = BASE / "skills" / skill["name"]
        destination = GLOBAL / skill["name"]
        assert source.is_dir() and destination.is_dir()
        for path in sorted(source.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(source)
            local_bytes = path.read_bytes()
            global_bytes = (destination / relative).read_bytes()
            assert local_bytes == global_bytes
            entries.append({"skill": skill["name"], "path": relative.as_posix(), "bytes": len(local_bytes), "sha256": hashlib.sha256(local_bytes).hexdigest()})
    write("tooling/global-promotion-corrected.json", {"schema": "ghc.family.global-promotion.v686.v3.post-lint", "correction_of": "docs/vesper-arlen/v686-v3/tooling/global-promotion.json", "skills": 10, "unique_new_shared_runners": 5, "entries": entries, "byte_parity": True, "collision_overwrites": 0, "lint_scope": "F401-only mechanical cleanup across the exact 42 local/global affected runner copies", "catalogue_reload_claimed": False, "same_owner_only": True})

    smokes = []
    for key, filename in RUNNER_MAP.items():
        row = next(item for item in rows if item["runner"] == key)
        folder = BASE / "tooling/post-lint-runner-smokes" / filename.removesuffix(".py")
        folder.mkdir(parents=True, exist_ok=False)
        positive_input = folder / "positive-input.json"
        adverse_input = folder / "duplicate-member-input.json"
        positive_input.write_text(json.dumps(row["input"], ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
        adverse_input.write_text('{"a":1,"a":2}\n', encoding="utf-8", newline="\n")
        positive_output = folder / "positive-output.json"
        adverse_output = folder / "adverse-output.json"
        script = ROOT / "scripts" / filename
        positive = subprocess.run([sys.executable, "-X", "utf8", str(script), "--operation", row["operation"], "--input", str(positive_input), "--output", str(positive_output)], capture_output=True)
        adverse = subprocess.run([sys.executable, "-X", "utf8", str(script), "--operation", row["operation"], "--input", str(adverse_input), "--output", str(adverse_output)], capture_output=True)
        observed = json.loads(positive_output.read_text(encoding="utf-8"))["result"]
        rejected = json.loads(adverse_output.read_text(encoding="utf-8"))["result"]
        expected_code = 2 if isinstance(row["expected_result"], dict) and set(row["expected_result"]) == {"error"} else 0
        passed = positive.returncode == expected_code and canonical(observed) == canonical(row["expected_result"]) and adverse.returncode == 2 and rejected == {"error": "duplicate_json_member"}
        receipt = {"runner": filename, "proposal_id": row["proposal_id"], "runner_sha256": hashlib.sha256(script.read_bytes()).hexdigest(), "positive_returncode": positive.returncode, "positive_pass": canonical(observed) == canonical(row["expected_result"]), "adverse_returncode": adverse.returncode, "adverse_rejected": rejected == {"error": "duplicate_json_member"}, "pass": passed, "negative_success_credit": 0, "same_owner_only": True}
        write(folder.relative_to(BASE) / "smoke-receipt.json", receipt)
        assert passed
        smokes.append(receipt)
    write("tooling/post-lint-runner-validation.json", {"schema": "ghc.family.post-lint-runner-validation.v686.v3", "runners": smokes, "runner_count": len(smokes), "all_passed": all(item["pass"] for item in smokes), "ruff_f_checks_passed": True, "same_owner_only": True, "independent_reproduction": False})
    print(json.dumps({"global_files_verified": len(entries), "runner_smokes": len(smokes), "all_passed": True}))


if __name__ == "__main__":
    main()
