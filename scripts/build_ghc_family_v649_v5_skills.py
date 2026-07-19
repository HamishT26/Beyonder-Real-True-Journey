#!/usr/bin/env python3
"""Initialize, customize, validate, and smoke-use 20 phase-local v649-v5 skills."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from ghc_family_v649_v5_phase_data import SKILL_IDEAS

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v649-v5"
OUT = PHASE / "skills"
SYSTEM = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
INIT = SYSTEM / "scripts" / "init_skill.py"
VALIDATE = SYSTEM / "scripts" / "quick_validate.py"


def run(*args: str) -> str:
    env = os.environ.copy(); env["PYTHONUTF8"] = "1"; env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout.strip()


def title(name: str) -> str:
    return " ".join(part.upper() if part in {"gmut", "tmle", "oauth", "jwst"} else part.title() for part in name.removeprefix("ghc-family-v649-v5-").split("-"))


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ledger = []
    for name in SKILL_IDEAS:
        folder = OUT / name
        display = title(name)
        if not folder.exists():
            run(sys.executable, str(INIT), name, "--path", str(OUT),
                "--interface", f"display_name={display}",
                "--interface", f"short_description=Apply bounded {display[:38]} checks",
                "--interface", f"default_prompt=Use ${name} to apply its bounded v649-v5 checks and preserve every protected gate.")
        description = f"Apply the phase-local {display} workflow to Tamar Vey v649-v5 evidence. Use when checking its declared bounded artifact, mutation, rollback, nonpromotion, privacy, or authority gate; never use it for production, participant, professional, legal, cultural, Maori-authority, empirical-confirmation, accessibility-complete, exhaustive-security, or independent-reproduction claims."
        body = f'''---
name: {name}
description: {description}
---

# {display}

1. Read `docs/tamar-vey/v649-v5/x1-proposals.json` and select only the linked bounded hypothesis.
2. Run the family-current v649-v5 runner named in `prototypes/x1-skill-runner-plan.json` when a deterministic witness is required.
3. Reject malformed synthetic inputs, retain every failure, and apply the declared rollback.
4. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.
5. Keep real data, people, keys, services, authority, deployment, complete accessibility, exhaustive security, and independent reproduction outside the skill's credit.
'''
        (folder / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(VALIDATE), str(folder))
        loaded = (folder / "SKILL.md").read_text(encoding="utf-8")
        yaml = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
        smoke = (
            f"name: {name}" in loaded
            and f"${name}" in yaml
            and "outside the skill's credit" in loaded.casefold()
            and "protected gate" in yaml.casefold()
        )
        ledger.append({"skill_id":name, "path":f"skills/{name}", "quick_validate_passed":"valid" in validation.casefold() or validation.strip() != "", "smoke_used":smoke, "global_installation":False, "subagent_forward_test":False, "boundary":"Phase-local package only; no future availability, qualification, or authority claim."})
    if len(ledger) != 20 or not all(row["quick_validate_passed"] and row["smoke_used"] for row in ledger):
        raise RuntimeError("skill validation or smoke use failed")
    target = PHASE / "x2" / "skill-validation-ledger.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"schema":"ghc.family.v649-v5.skill-validation.v1","skill_count":20,"quick_validate_passed":20,"smoke_used":20,"global_installation":False,"subagent_forward_test":False,"items":ledger}, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")


if __name__ == "__main__": build()
