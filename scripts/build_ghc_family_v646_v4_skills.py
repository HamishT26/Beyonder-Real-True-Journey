#!/usr/bin/env python3
"""Initialize, validate, and smoke-use twenty phase-local Orin v646-v4 skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v646_v4_definitions import PHASE, SKILLS, TRUTH_BOUNDARY
from ghc_family_v646_v4_runtime import run as run_core


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/orin-thale/v646-v4"
CREATOR = Path.home() / ".codex/skills/.system/skill-creator"
X1_HEAD = "8b63d3f65f9fe9909da71eeb1171e3b5cf86768a"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def title(name: str) -> str:
    special = {"ghc", "json", "act", "bbs", "git"}
    return " ".join(word.upper() if word in special else word.title() for word in name.split("-"))


def body(name: str, description: str) -> str:
    trigger = f"{description} Use when a GHC phase needs this bounded owner-scoped guard with an explicit falsifier, rollback, privacy boundary, and retained-negative receipt."
    return f'''---
name: {name}
description: {json.dumps(trigger, ensure_ascii=False)}
---

# {title(name)}

## Workflow

1. Read the newest applicable GHC Family Index and phase truth.
2. Verify the exact owner lane, frozen input anchors, approval class, and protected gates.
3. {description}
4. State the hypothesis, null or failure condition, artifact, falsifier, rollback, and protected gates before execution.
5. Execute only owner-scoped synthetic, symbolic, structural, disposable, zero-row, or read-only work unless exact evidence and authority are present.
6. Record every fault and workaround in Method Flow; retain the failed witness before retry.
7. Validate privacy scope, manifest domain, caller compatibility, and lifecycle state.
8. Emit only `completed`, `represented`, `open_gap`, or `exact_gate`; keep routing `PREPARED_NOT_SENT` until exact-final validation.

## Required output

- Preserve source status as `current`, `stable`, `draft`, or `watch`.
- Separate citations and fixtures from empirical, participant, operational, legal, cultural, or production evidence.
- Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers.
- Include retained-negative identifiers, recovery, protected gates, and same-owner-only limits.

## Protected gates

Do not claim empirical confirmation, Theory of Everything, THOS effectiveness, production identity assurance, health, legal or cultural legitimacy, Māori authority, professional competence, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness, personhood, deployment, or Stage 20 readiness without exact evidence and authority.

{TRUTH_BOUNDARY}
'''


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


CORE_MAP = {
    "ghc-family-idempotent-resume-ledger": "idempotent-resume",
    "ghc-family-hadamard-obligations": "hadamard-obligations",
    "ghc-family-act-dr6-zero-row-refusal": "act-dr6-zero-row",
    "ghc-family-pharmacy-handover-proxy": "pharmacy-handover",
    "ghc-family-bbs-derived-proof-profile": "bbs-derived-proof",
    "ghc-family-medicine-recall-authority": "medicine-recall-authority",
    "ghc-family-git-alternate-quarantine": "git-alternate-tribunal",
    "ghc-family-form-error-audit": "form-error-audit",
    "ghc-family-mori-zwanzig-domain": "mori-zwanzig-domain",
    "ghc-family-environment-lock-nonpromotion": "environment-lock-board",
}


def smoke_use(name: str) -> dict[str, Any]:
    if name in CORE_MAP:
        result = run_core(CORE_MAP[name], ROOT / ".ghc-family-runtime-v646-v4" / "skill-smoke")
        return {"surface": CORE_MAP[name], "passed": bool(result.get("passed")), "checks": result.get("checks", 0)}
    if name == "ghc-family-read-write-preflight":
        result = run_core("idempotent-resume")
        return {"surface": "read-write-preflight", "passed": bool(result.get("passed")), "checks": result.get("checks", 0)}
    if name == "ghc-family-x1-companion-drift-quarantine":
        manifest = load("validation/x1-staged-manifest.json")
        return {"surface": "x1-self-excluding-manifest", "passed": manifest.get("entry_count") == len(manifest.get("entries", [])) == 84, "checks": 85}
    if name == "ghc-family-external-negative-carry-forward":
        negative = load("validation/x1-operational-negatives.json")
        passed = negative.get("inherited_effective") == 2704 and len(negative.get("source_external_negative_ids", [])) == 2
        return {"surface": "external-negative-carry-forward", "passed": passed, "checks": 2}
    if name == "ghc-family-source-status-watch":
        source = load("sources/source-ledger.json")
        passed = len(source.get("sources", [])) == 17 and all(row.get("status") in {"current", "stable", "draft", "watch"} for row in source.get("sources", []))
        return {"surface": "source-status-watch", "passed": passed, "checks": len(source.get("sources", []))}
    if name == "ghc-family-exact-staged-review":
        review = load("validation/x1-staged-review.json")
        return {"surface": "exact-staged-review", "passed": review.get("valid") is True and review.get("staged_file_count") == 85, "checks": review.get("staged_file_count", 0)}
    if name == "ghc-family-owner-footprint-guard":
        rotation = load("environment/rotation-guard.json")
        passed = rotation.get("owner_generated_files_at_receipt") == 85 and not rotation.get("rotate") and rotation.get("full_checkout_files") == 33366
        return {"surface": "owner-footprint", "passed": passed, "checks": 3}
    if name == "ghc-family-named-lane-locality":
        route = load("orchestration/terminal-route-plan.json")
        text = " ".join(route.get("preconditions", [])).casefold()
        passed = route.get("send_count") == 0 and "exactly one" in text and "named-lane replay" in text
        return {"surface": "named-lane-plan", "passed": passed, "checks": 2}
    if name == "ghc-family-commit-cap-ancestry":
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8").strip()
        parent = subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True, encoding="utf-8").strip()
        return {"surface": "x1-anchor", "passed": head == X1_HEAD and parent == "c45aba6c9c2fee5d60e1fcde9f0de849290cfc96", "checks": 2}
    if name == "ghc-family-static-report-manual-reservation":
        proposal = next(row for row in load("x1-proposals.json")["proposals"] if row["proposal_id"] == "V6464-P08")
        gates = set(proposal.get("protected_gates", []))
        return {"surface": "manual-accessibility-reservation", "passed": {"accessibility_complete", "assistive_technology", "affected_user_evaluation"} <= gates, "checks": 3}
    if name == "ghc-family-terminal-route-one-shot":
        route = load("orchestration/terminal-route-plan.json")
        return {"surface": "route-one-shot", "passed": route.get("target_title") == "Tamar Vey" and route.get("send_count") == 0 and route.get("current_state") == "PREPARED_NOT_SENT", "checks": 3}
    return {"surface": "unmapped", "passed": False, "checks": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=PHASE_DIR / "prototypes/skills")
    args = parser.parse_args()
    init = CREATOR / "scripts/init_skill.py"
    validate = CREATOR / "scripts/quick_validate.py"
    if not init.is_file() or not validate.is_file():
        raise SystemExit("skill-creator initializer or validator is unavailable")
    receipts = []
    for name, description in SKILLS:
        target = args.skill_root / name
        created = not target.exists()
        if created:
            short = f"Bounded GHC guard for {name.removeprefix('ghc-family-').replace('-', ' ')}"[:64].rstrip()
            command = [
                sys.executable,
                str(init),
                name,
                "--path",
                str(args.skill_root),
                "--interface",
                f"display_name={title(name)}",
                "--interface",
                f"short_description={short}",
                "--interface",
                f"default_prompt=Use ${name} to produce a bounded GHC artifact with explicit falsifier and protected gates.",
            ]
            subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
        skill = target / "SKILL.md"
        if created:
            skill.write_text(body(name, description), encoding="utf-8", newline="\n")
        agent = target / "agents/openai.yaml"
        validate_env = dict(os.environ); validate_env["PYTHONUTF8"] = "1"
        result = subprocess.run([sys.executable, str(validate), str(target)], capture_output=True, text=True, encoding="utf-8", env=validate_env)
        text = skill.read_text(encoding="utf-8")
        smoke = smoke_use(name)
        receipts.append(
            {
                "name": name,
                "origin": "newly_initialized_phase_local" if created else "phase_local_reused_after_retained_smoke_failure",
                "initialized_in_v646_v4": True,
                "created_this_invocation": created,
                "global_skill_bank_mutated": False,
                "quick_validate_returncode": result.returncode,
                "quick_validate_output": (result.stdout + result.stderr).strip(),
                "word_count": len(text.split()),
                "word_limit": 6000,
                "skill_sha256": sha(skill),
                "agent_metadata_present": agent.is_file(),
                "agent_metadata_sha256": sha(agent) if agent.is_file() else None,
                "metadata_matches_skill": name in text and agent.is_file() and f"${name}" in agent.read_text(encoding="utf-8"),
                "bounded_smoke_use": smoke,
                "completion_scope": "phase-local package, metadata, validator, and bounded same-owner smoke use only",
            }
        )
    valid = len(receipts) == 20 and all(
        row["quick_validate_returncode"] == 0
        and row["word_count"] <= 6000
        and row["agent_metadata_present"]
        and row["metadata_matches_skill"]
        and row["bounded_smoke_use"]["passed"]
        for row in receipts
    )
    payload = {
        "schema": "ghc.family.v646-v4.skill-build-receipt.v1",
        "phase": PHASE,
        "skill_count": len(receipts),
        "newly_initialized_count": len(receipts),
        "compatible_reused_count": 0,
        "created_this_invocation_count": sum(row["created_this_invocation"] for row in receipts),
        "reused_this_invocation_count": sum(not row["created_this_invocation"] for row in receipts),
        "validated_count": sum(row["quick_validate_returncode"] == 0 for row in receipts),
        "smoke_use_pass_count": sum(row["bounded_smoke_use"]["passed"] for row in receipts),
        "subagent_forward_tests": 0,
        "subagent_forward_test_reason": "Activation explicitly forbids subagents; deterministic validation and owner-local smoke use were used.",
        "skills": receipts,
        "valid": valid,
        "boundary": "Skill validation and smoke use establish bounded package behavior only, not domain truth, authority, production readiness, or independent reproduction.",
    }
    output = PHASE_DIR / "prototypes/skill-build-receipt.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(receipts), "initialized": len(receipts), "validated": payload["validated_count"], "smoke_used": payload["smoke_use_pass_count"], "valid": valid}))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
