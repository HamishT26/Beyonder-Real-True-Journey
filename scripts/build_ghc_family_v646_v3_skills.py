#!/usr/bin/env python3
"""Initialize, validate, and smoke-use the twenty Sable v646-v3 skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v646_v3_definitions import PHASE, SKILLS, TRUTH_BOUNDARY
from ghc_family_v646_v3_runtime import run as run_core


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v646-v3"
CREATOR = Path.home() / ".codex/skills/.system/skill-creator"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def title(name: str) -> str:
    special = {"ghc", "json", "haip", "svg", "wal"}
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
4. State the hypothesis, null or failure condition, concrete artifact, falsifier, and rollback before execution.
5. Execute only owner-scoped synthetic, symbolic, structural, or read-only work unless exact evidence and authority are present.
6. Record every fault and workaround in Method Flow; retain the failed witness before any retry.
7. Validate JSON order, privacy scope, manifest domain, caller compatibility, and lifecycle state.
8. Emit only `completed`, `represented`, `open_gap`, or `exact_gate`; leave the route `PREPARED_NOT_SENT` until final validation.

## Required output

- Keep source status within `current`, `stable`, `draft`, or `watch`.
- Separate citations and fixtures from empirical, participant, operational, legal, cultural, or production evidence.
- Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers.
- Include retained-negative identifiers, recovery, protected gates, and same-owner-only limits.

## Protected gates

Do not claim empirical confirmation, Theory of Everything, THOS effectiveness, production identity assurance, legal or cultural legitimacy, Māori authority, professional competence, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness, personhood, deployment, or Stage 20 readiness without exact evidence and authority.

{TRUTH_BOUNDARY}
'''


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


CORE_MAP = {
    "ghc-family-cross-manifest-edge-quarantine": "cross-manifest",
    "ghc-family-kallen-lehmann-obligations": "kallen-lehmann",
    "ghc-family-pta-zero-row-adapter": "nanograv-zero-row",
    "ghc-family-water-lab-handover-proxy": "water-lab-handover",
    "ghc-family-vc-related-resource-integrity": "related-resource",
    "ghc-family-boil-water-authority-reservation": "boil-water-authority",
    "ghc-family-sqlite-migration-lock": "sqlite-migration",
    "ghc-family-chart-modality-parity": "chart-modality",
    "ghc-family-harada-sasa-domain": "harada-sasa",
    "ghc-family-registered-report-checksum": "registered-report",
}


def smoke_use(name: str) -> dict[str, Any]:
    if name in CORE_MAP:
        result = run_core(CORE_MAP[name], ROOT / ".ghc-family-runtime-v646-v3" / "skill-smoke")
        return {"surface": CORE_MAP[name], "passed": bool(result.get("passed")), "checks": result.get("checks", 0), "claim_scope": "bounded core fixture"}
    if name == "ghc-family-external-negative-reconciler":
        negatives = load("validation/x1-operational-negatives.json")
        passed = negatives.get("inherited_effective") == 2619 and len(negatives.get("inherited_external_terminal_negatives", [])) == 3
        return {"surface": "external-negative-baseline", "passed": passed, "checks": 2}
    if name == "ghc-family-phase-local-test-quarantine":
        proposals = load("x1-proposals.json")
        return {"surface": "phase-local-selection", "passed": proposals.get("frozen_chain_count_after_x1") == 420, "checks": 1}
    if name == "ghc-family-exact-revision-credit":
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8").strip()
        return {"surface": "exact-revision", "passed": head == "5894a1e1fcb923b37d5ce109824b61ad24739fb5", "checks": 1}
    if name == "ghc-family-windows-refspec-guard":
        route = load("environment/startup-receipt.json")["source"]
        return {"surface": "refspec-components", "passed": route.get("branch", "").count("/") >= 2 and len(route.get("revision", "")) == 40, "checks": 2}
    if name == "ghc-family-shell-summary-sequencer":
        methods = load("method-flow/method-flow-state.json").get("methods", [])
        return {"surface": "shell-sequencing", "passed": any(row.get("method_id") == "V6463-M02" and row.get("recommendation_state") == "preferred" for row in methods), "checks": 1}
    if name == "ghc-family-manifest-fixed-point":
        manifest = load("validation/x1-staged-manifest.json")
        return {"surface": "x1-exact-manifest", "passed": manifest.get("entry_count") == len(manifest.get("entries", [])), "checks": manifest.get("entry_count", 0) + 1}
    if name == "ghc-family-svg-alternative-audit":
        result = run_core("chart-modality", ROOT / ".ghc-family-runtime-v646-v3" / "skill-smoke")
        return {"surface": "chart-modality", "passed": bool(result.get("passed")), "checks": result.get("checks", 0)}
    if name == "ghc-family-authority-matrix-lint":
        result = run_core("boil-water-authority")
        return {"surface": "authority-matrix", "passed": bool(result.get("passed")), "checks": result.get("checks", 0)}
    if name == "ghc-family-zero-row-likelihood-refusal":
        result = run_core("nanograv-zero-row")
        passed = result.get("passed") and result.get("rows_ingested") == 0 and result.get("likelihood_evaluations") == 0
        return {"surface": "zero-row-refusal", "passed": bool(passed), "checks": result.get("checks", 0)}
    if name == "ghc-family-named-lane-locality-proof":
        route = load("orchestration/terminal-route-plan.json")
        passed = "exactly one" in " ".join(route.get("preconditions", [])).casefold() and route.get("send_count") == 0
        return {"surface": "named-lane-plan", "passed": passed, "checks": 2}
    return {"surface": "unmapped", "passed": False, "checks": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=PHASE_DIR / "prototypes/skills")
    args = parser.parse_args()
    init = CREATOR / "scripts/init_skill.py"
    validate = CREATOR / "scripts/quick_validate.py"
    if not init.is_file() or not validate.is_file():
        raise SystemExit("skill-creator initializer or validator is unavailable")
    receipt_path = PHASE_DIR / "prototypes/skill-build-receipt.json"
    previous_rows: dict[str, Any] = {}
    if receipt_path.is_file():
        previous_rows = {row["name"]: row for row in json.loads(receipt_path.read_text(encoding="utf-8")).get("skills", [])}
    receipts = []
    for name, description in SKILLS:
        target = args.skill_root / name
        created = False
        reused = target.exists()
        if not reused:
            short = f"Bounded GHC guard for {name.removeprefix('ghc-family-').replace('-', ' ')}"[:64].rstrip()
            command = [
                sys.executable, str(init), name, "--path", str(args.skill_root),
                "--interface", f"display_name={title(name)}",
                "--interface", f"short_description={short}",
                "--interface", f"default_prompt=Use ${name} to produce a bounded GHC artifact with explicit falsifier and protected gates.",
            ]
            subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
            target.joinpath("SKILL.md").write_text(body(name, description), encoding="utf-8", newline="\n")
            created = True
        skill = target / "SKILL.md"
        agent = target / "agents/openai.yaml"
        validate_env = dict(os.environ); validate_env["PYTHONUTF8"] = "1"
        result = subprocess.run([sys.executable, str(validate), str(target)], capture_output=True, text=True, encoding="utf-8", env=validate_env)
        text = skill.read_text(encoding="utf-8")
        smoke = smoke_use(name)
        metadata_matches = name in text and agent.is_file()
        initialized_this_phase = created or bool(previous_rows.get(name, {}).get("initialized_in_v646_v3"))
        receipts.append({
            "name": name,
            "origin": "newly_initialized" if initialized_this_phase else "compatible_existing_reused_without_mutation",
            "initialized_in_v646_v3": initialized_this_phase,
            "created_this_invocation": created,
            "existing_package_mutated": False if not initialized_this_phase else None,
            "quick_validate_returncode": result.returncode,
            "quick_validate_output": (result.stdout + result.stderr).strip(),
            "word_count": len(text.split()),
            "word_limit": 6000,
            "skill_sha256": sha(skill),
            "agent_metadata_present": agent.is_file(),
            "agent_metadata_sha256": sha(agent) if agent.is_file() else None,
            "metadata_matches_skill": metadata_matches,
            "bounded_smoke_use": smoke,
            "completion_scope": "skill package, metadata, validator, and bounded owner-local smoke use only",
        })
    valid = len(receipts) == 20 and all(
        row["quick_validate_returncode"] == 0
        and row["word_count"] <= 6000
        and row["agent_metadata_present"]
        and row["metadata_matches_skill"]
        and row["bounded_smoke_use"]["passed"]
        for row in receipts
    )
    payload = {
        "schema": "ghc.family.v646-v3.skill-build-receipt.v1",
        "phase": PHASE,
        "skill_count": len(receipts),
        "newly_initialized_count": sum(row["initialized_in_v646_v3"] for row in receipts),
        "compatible_reused_count": sum(not row["initialized_in_v646_v3"] for row in receipts),
        "validated_count": sum(row["quick_validate_returncode"] == 0 for row in receipts),
        "smoke_use_pass_count": sum(row["bounded_smoke_use"]["passed"] for row in receipts),
        "subagent_forward_tests": 0,
        "subagent_forward_test_reason": "Activation explicitly forbids subagents; deterministic validation and owner-local smoke use were used.",
        "skills": receipts,
        "valid": valid,
        "boundary": "Skill validation and smoke use establish bounded package behavior only, not domain truth, authority, production readiness, or independent reproduction.",
    }
    output = receipt_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(receipts), "initialized": payload["newly_initialized_count"], "reused": payload["compatible_reused_count"], "validated": payload["validated_count"], "smoke_used": payload["smoke_use_pass_count"], "valid": valid}))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
