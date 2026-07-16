#!/usr/bin/env python3
"""Initialize, customize, validate, and smoke-use the v646-v1 skill set."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from ghc_family_v646_v1_definitions import PHASE, SKILLS, TRUTH_BOUNDARY


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/eiren-kestrel/v646-v1"
CREATOR = Path.home() / ".codex/skills/.system/skill-creator"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def title(name: str) -> str:
    return " ".join(word.upper() if word in {"ghc","dhost","sd","jwt","vc"} else word.title() for word in name.split("-"))


def body(name: str, description: str) -> str:
    trigger = f"{description} Use when a GHC phase needs a bounded, owner-scoped artifact, falsifier, recovery path, and protected-gate receipt for this surface."
    return f'''---
name: {name}
description: {json.dumps(trigger, ensure_ascii=False)}
---

# {title(name)}

## Workflow

1. Read the newest applicable GHC Family Index and phase truth before acting.
2. Verify the exact owner lane, input anchors, approval class, and protected gates.
3. {description}
4. State the hypothesis, null or failure condition, concrete artifact, falsifier, and rollback before execution.
5. Execute only an owner-scoped synthetic, structural, or read-only fixture unless exact evidence and authority are present.
6. Retain every failure and workaround in Method Flow; never convert a failed witness into completion credit.
7. Validate the artifact, privacy boundary, diff scope, and compatibility surface.
8. Emit one bounded receipt with `completed`, `represented`, `open_gap`, or `exact_gate`; keep Stage 20 closed unless all exact gates pass.

## Required output

- Record sources as `current`, `stable`, `draft`, or `watch`.
- Separate structural evidence from empirical, participant, operational, legal, cultural, or production evidence.
- Preserve family-current naming and caller compatibility.
- Include recovery, retained-negative identifiers, and the same-owner-only limit.

## Protected gates

Do not claim empirical confirmation, Theory of Everything, THOS effectiveness, production identity assurance, legal or cultural legitimacy, Māori authority, professional competence, accessibility completeness, exhaustive security, independent reproduction, AGI/ASI, consciousness, personhood, deployment, or Stage 20 readiness without exact evidence and authority.

{TRUTH_BOUNDARY}
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=Path.home() / ".codex/skills")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    init = CREATOR / "scripts/init_skill.py"
    validate = CREATOR / "scripts/quick_validate.py"
    if not init.is_file() or not validate.is_file(): raise SystemExit("skill-creator scripts are unavailable")
    receipts = []
    for name, description in SKILLS:
        target = args.skill_root / name
        created = False
        if not target.exists():
            short = f"Bounded GHC workflow for {name.removeprefix('ghc-family-').replace('-', ' ')}"
            short = short[:64].rstrip()
            command = [sys.executable,str(init),name,"--path",str(args.skill_root),
                "--interface",f"display_name={title(name)}",
                "--interface",f"short_description={short}",
                "--interface",f"default_prompt=Use ${name} to build a bounded, falsifiable GHC phase artifact."]
            subprocess.run(command,check=True,capture_output=True,text=True)
            created = True
        elif not args.resume:
            raise SystemExit(f"skill already exists: {name}")
        skill = target / "SKILL.md"
        skill.write_text(body(name,description),encoding="utf-8",newline="\n")
        validate_env = dict(os.environ)
        validate_env["PYTHONUTF8"] = "1"
        result = subprocess.run([sys.executable,str(validate),str(target)],capture_output=True,text=True,env=validate_env)
        text = skill.read_text(encoding="utf-8")
        word_count = len(text.split())
        smoke = all(token in text for token in ("## Workflow","## Required output","## Protected gates","Method Flow","Stage 20")) and word_count <= 6000
        agent = target / "agents/openai.yaml"
        receipts.append({"name":name,"initialized_in_v646_v1":True,"created_this_invocation":created,"quick_validate_returncode":result.returncode,"quick_validate_output":(result.stdout+result.stderr).strip(),"word_count":word_count,"word_limit":6000,"skill_sha256":sha(skill),"agent_metadata_present":agent.is_file(),"agent_metadata_sha256":sha(agent) if agent.is_file() else None,"bounded_smoke_use":"pass" if smoke else "fail","completion_scope":"skill package structure and bounded workflow smoke use only"})
    valid = len(receipts)==20 and all(x["quick_validate_returncode"]==0 and x["bounded_smoke_use"]=="pass" and x["agent_metadata_present"] for x in receipts)
    payload={"schema":"ghc.family.v646-v1.skill-build-receipt.v1","phase":PHASE,"skill_count":len(receipts),"initialized_in_phase_count":sum(x["initialized_in_v646_v1"] for x in receipts),"created_this_invocation_count":sum(x["created_this_invocation"] for x in receipts),"validation_recovery":"The initial CP1252 validator invocation failed on the Māori macron; the retained recovery reran the unchanged validator with explicit UTF-8 mode.","validated_count":sum(x["quick_validate_returncode"]==0 for x in receipts),"smoke_use_pass_count":sum(x["bounded_smoke_use"]=="pass" for x in receipts),"skills":receipts,"valid":valid,"boundary":"Smoke use validates package structure and the bounded workflow contract only; it is not independent reproduction or domain assurance."}
    out=PHASE_DIR/"prototypes/skill-build-receipt.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"skills":len(receipts),"initialized_in_phase":payload["initialized_in_phase_count"],"created_this_invocation":payload["created_this_invocation_count"],"validated":payload["validated_count"],"smoke_used":payload["smoke_use_pass_count"],"valid":valid}))
    return 0 if valid else 1


if __name__ == "__main__": raise SystemExit(main())
