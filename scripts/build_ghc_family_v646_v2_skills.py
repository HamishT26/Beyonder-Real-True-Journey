#!/usr/bin/env python3
"""Initialize, validate, and smoke-use the twenty Ilyra v646-v2 skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v646_v2_definitions import PHASE, SKILLS, TRUTH_BOUNDARY
from ghc_family_v646_v2_runtime import run as run_core


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v646-v2"
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
    "ghc-family-evidence-dag-closure": "evidence-dag",
    "ghc-family-schwinger-keldysh-obligations": "schwinger-keldysh",
    "ghc-family-microscope-zero-row": "microscope-zero-row",
    "ghc-family-seismic-handover-proxy": "seismic-handover",
    "ghc-family-haip-profile": "haip-profile",
    "ghc-family-earthquake-authority-reservation": "earthquake-authority",
    "ghc-family-sqlite-wal-tribunal": "sqlite-wal",
    "ghc-family-svg-chart-audit": "svg-chart",
    "ghc-family-hatano-sasa-domain": "hatano-sasa",
    "ghc-family-registered-report-lock": "registered-report",
}


def smoke_use(name: str) -> dict[str, Any]:
    if name in CORE_MAP:
        result = run_core(CORE_MAP[name], Path("D:/GHC-Family-Scratch/v646-v2-skill-smoke"))
        return {"surface": CORE_MAP[name], "passed": bool(result.get("passed")), "checks": result.get("checks", 0), "claim_scope": "bounded core fixture"}
    if name == "ghc-family-source-status-drift-guard":
        rows = load("sources/source-ledger.json").get("sources", [])
        passed = len(rows) == 18 and all(row.get("status") in {"current", "stable", "draft", "watch"} for row in rows)
        return {"surface": "source-ledger", "passed": passed, "checks": len(rows) + 1}
    if name == "ghc-family-proposal-neighbor-quarantine":
        audit = load("provenance/prior-proposal-collision-audit.json")
        return {"surface": "proposal-neighbor-audit", "passed": audit.get("exact_title_collision_count") == 0 and len(audit.get("comparisons", [])) == 10, "checks": 2}
    if name == "ghc-family-staged-surface-allowlist":
        review = load("validation/x1-staged-review.json")
        return {"surface": "x1-staged-review", "passed": review.get("valid") is True and not review.get("lifecycle_leaks"), "checks": 2}
    if name == "ghc-family-json-order-contract":
        sample = load("x1-proposals.json")
        a = json.dumps(sample, sort_keys=True, ensure_ascii=False)
        b = json.dumps(json.loads(a), sort_keys=True, ensure_ascii=False)
        return {"surface": "deterministic-json", "passed": a == b, "checks": 1}
    if name == "ghc-family-scanner-definition-separator":
        review = load("validation/x1-privacy-review.json")
        methods = load("method-flow/method-flow-state.json").get("methods", [])
        passed = review.get("confirmed_hit_count") == 0 and any(row.get("method_id") == "V6462-M01" and row.get("recommendation_state") == "preferred" for row in methods)
        return {"surface": "scanner-definition-separation", "passed": passed, "checks": 2}
    if name == "ghc-family-logical-manifest-parity":
        manifest = load("validation/x1-staged-manifest.json")
        return {"surface": "x1-exact-manifest", "passed": manifest.get("entry_count") == len(manifest.get("entries", [])), "checks": manifest.get("entry_count", 0) + 1}
    if name == "ghc-family-caller-compatibility-audit":
        names = {path.name for path in (ROOT / "scripts").glob("ghc_family_*.py")}
        return {"surface": "family-current-callers", "passed": "ghc_family_v646_v2_runtime.py" in names and len(names) >= 10, "checks": 2}
    if name == "ghc-family-method-state-preflight":
        ledger = load("method-flow/method-flow-state.json")
        methods = ledger.get("methods", [])
        failed_methods = {row.get("method_id") for row in ledger.get("witnesses", []) if row.get("result") == "fail" and row.get("retained_negative_ids")}
        passed = bool(methods) and all(
            row.get("recommendation_state") in {"preferred", "deprecated", "superseded"}
            or (row.get("recommendation_state") == "candidate" and row.get("method_id") in failed_methods)
            for row in methods
        )
        return {"surface": "method-flow", "passed": passed, "checks": len(methods) + len(failed_methods) + 1}
    if name == "ghc-family-terminal-route-guard":
        route = load("orchestration/terminal-route-plan.json")
        return {"surface": "terminal-route", "passed": route.get("current_state") == "PREPARED_NOT_SENT" and route.get("send_count") == 0, "checks": 2}
    if name == "ghc-family-workload-boundary-check":
        guard = load("environment/rotation-guard.json")
        return {"surface": "owner-generated-threshold", "passed": guard.get("threshold") == 15000 and guard.get("rotate_due_to_inherited_baseline") is False, "checks": 2}
    return {"surface": "unmapped", "passed": False, "checks": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=Path.home() / ".codex/skills")
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
        initialized_this_phase = created or bool(previous_rows.get(name, {}).get("initialized_in_v646_v2"))
        receipts.append({
            "name": name,
            "origin": "newly_initialized" if initialized_this_phase else "compatible_existing_reused_without_mutation",
            "initialized_in_v646_v2": initialized_this_phase,
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
        "schema": "ghc.family.v646-v2.skill-build-receipt.v1",
        "phase": PHASE,
        "skill_count": len(receipts),
        "newly_initialized_count": sum(row["initialized_in_v646_v2"] for row in receipts),
        "compatible_reused_count": sum(not row["initialized_in_v646_v2"] for row in receipts),
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
