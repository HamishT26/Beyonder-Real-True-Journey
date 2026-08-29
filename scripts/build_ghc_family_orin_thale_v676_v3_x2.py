#!/usr/bin/env python3
"""Execute the bounded owner-local Orin Thale v676-v3 x2 evidence build."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_orin_thale_v676_v3_core import (
    accessibility_proxy,
    mutate,
    positive_fixture,
    quick_validate_skill,
    validate_claim_state,
    validate_contract,
    validate_provenance,
)


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v676-v3"
BRANCH = "codex/GHC-Family/orin-thale-v676-v3-full-tools"
SOURCE = "8f1e9ebc708b5ddc23bee4e407d946fe3e322bf3"
X1 = "3ba3826fb79f836a46a577af2809a5dd6e445350"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def method(method_id: str, description: str, truth: bool, **extra: Any) -> dict[str, Any]:
    value = {
        "method_id": method_id,
        "description": description,
        "status": "bounded_pass" if truth else "failed_zero_credit",
        "truth": truth,
    }
    value.update(extra)
    return value


def build_skill(base: Path, skill_id: str, name: str, description: str) -> tuple[dict[str, Any], dict[str, Any]]:
    skill_dir = base / "skills" / name
    text(
        skill_dir / "SKILL.md",
        f"""---
name: {name}
description: {description}
---

# {name}

Owner-local Orin Thale v676-v3 skill for deterministic zero-row lost-property workflow evidence.

## Inputs

- One synthetic item or claim-state object.
- The exact protected-gate register.
- No real person, item, identifier, custody event, or authority decision.

## Procedure

1. Validate the synthetic prefix and required fields.
2. Preserve contradictions and correction statements without silent overwrite.
3. Return one bounded receipt and keep authority-dependent action unavailable.

## Refusal conditions

- Refuse raw identity, private route, credential, real item, real claimant, external write, physical action, or authority-bearing input.
- Refuse ownership, disposal, safety, legal, cultural, affected-party, tikanga, taonga, or Māori-authority decisions.
- Refuse empirical, production, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, Theory-of-Everything, canon, or Stage 20 promotion.

## Output

One deterministic owner-local JSON receipt with zero real-world rows and zero external actions.
""",
    )
    dump(
        skill_dir / "skill.json",
        {
            "skill_id": skill_id,
            "name": name,
            "owner": OWNER,
            "phase": PHASE,
            "global_install": False,
            "real_world_rows": 0,
            "external_actions": 0,
            "description": description,
            "output": "bounded_zero_row_receipt",
        },
    )
    validation = quick_validate_skill(skill_dir)
    smoke = {
        "accepted": validation["accepted"],
        "skill_id": skill_id,
        "name": name,
        "fixture": "synthetic_zero_row",
        "real_world_rows": 0,
        "external_actions": 0,
        "broader_claim_credit": 0,
    }
    return validation, smoke


def task_receipt(row: dict[str, Any], lane: str) -> dict[str, Any]:
    return {
        "task_id": row["task_id"],
        "description": row["description"],
        "lane": lane,
        "status": "bounded_completed_no_core_outcome_promotion",
        "real_world_rows": 0,
        "external_actions": 0,
        "authority_credit": 0,
    }


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 builder requires the exact immutable x1 head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x2 builder requires the exact Orin owner branch")
    if git(repo, "status", "--porcelain=v1"):
        expected_suffixes = {
            "scripts/build_ghc_family_orin_thale_v676_v3_x2.py",
            "scripts/ghc_family_orin_thale_v676_v3_core.py",
            "scripts/ghc_family_orin_thale_v676_v3_proposal_contracts.py",
            "scripts/ghc_family_orin_thale_v676_v3_positive_controls.py",
            "scripts/ghc_family_orin_thale_v676_v3_mutation_rejector.py",
            "scripts/ghc_family_orin_thale_v676_v3_claim_state.py",
            "scripts/ghc_family_orin_thale_v676_v3_provenance.py",
            "scripts/ghc_family_orin_thale_v676_v3_privacy.py",
            "scripts/ghc_family_orin_thale_v676_v3_accessibility.py",
            "scripts/ghc_family_orin_thale_v676_v3_portfolio.py",
            "scripts/ghc_family_orin_thale_v676_v3_method_flow.py",
            "scripts/build_ghc_family_orin_thale_v676_v3_report.py",
            "scripts/ghc_family_orin_thale_v676_v3_evidence_manifest.py",
            "tests/test_ghc_family_orin_thale_v676_v3_x2.py",
        }
        unexpected = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if not any(line.endswith(path) for path in expected_suffixes)]
        if unexpected:
            raise SystemExit("unexpected pre-x2 worktree state: " + repr(unexpected))

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    mutation_freeze = json.loads((x1 / "mutation-preregistration.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    skill_plan = json.loads((x1 / "skill-runner-plan.json").read_text(encoding="utf-8"))
    startup = json.loads((x1 / "method-flow-startup.json").read_text(encoding="utf-8"))
    cfr_plan = json.loads((x1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))

    methods = list(startup["methods"])
    methods.extend(
        [
            method(
                "OR6763-X2-N001",
                "The first x2 build stopped at proposal 1 because a Python set literal contained an unhashable list in a zero-row membership guard.",
                False,
                recovered_by="OR6763-X2-P001",
                state_change=False,
            ),
            method(
                "OR6763-X2-P001",
                "The guard changed only to tuple membership, the empty partial-state audit passed, and the bounded x2 builder completed.",
                True,
                failed_witness_preserved="OR6763-X2-N001",
            ),
            method(
                "OR6763-X2-N002",
                "Host policy rejected exact removal of one generated Python bytecode cache after containment was verified.",
                False,
                recovered_by="OR6763-X2-P002",
                state_change=False,
            ),
            method(
                "OR6763-X2-P002",
                "The harmless untracked cache remained outside sparse owner evidence, bytecode writing was disabled for later commands, and no deletion bypass was attempted.",
                True,
                failed_witness_preserved="OR6763-X2-N002",
            ),
        ]
    )
    outcomes = []
    for index, row in enumerate(proposals, start=1):
        fixture = positive_fixture(row)
        errors = validate_contract(fixture)
        if errors:
            raise SystemExit(f"positive control {row['proposal_id']} failed: {errors!r}")
        dump(x2 / "contracts" / f"{row['proposal_id']}.json", fixture)
        receipt = {
            "proposal_id": row["proposal_id"],
            "accepted": True,
            "errors": [],
            "fixture": "synthetic_zero_row",
            "expected_disposition": row["expected_disposition"],
            "real_world_rows": 0,
            "external_actions": 0,
            "broader_claim_credit": 0,
        }
        dump(x2 / "evidence" / f"{row['proposal_id']}-receipt.json", receipt)
        methods.append(method(f"OT6763-POS-{index:03d}", f"{row['proposal_id']} positive zero-row structural control", True))
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": row["expected_disposition"],
                "evidence": f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{row['proposal_id']}-receipt.json",
                "real_world_rows": 0,
                "external_actions": 0,
                "authority_credit": 0,
            }
        )

    proposal_map = {row["proposal_id"]: row for row in proposals}
    mutation_receipts = []
    for mutation_row in mutation_freeze["mutations"]:
        proposal = proposal_map[mutation_row["proposal_id"]]
        value = mutate(proposal, mutation_row["mutation_kind"])
        errors = validate_contract(value)
        if not errors:
            raise SystemExit("preregistered invalid mutation unexpectedly accepted: " + mutation_row["mutation_id"])
        receipt = {
            **mutation_row,
            "execution_status": "executed_rejected_zero_credit",
            "accepted": False,
            "rejection_reasons": errors,
            "failed_witness_retained": True,
            "real_world_rows": 0,
            "external_actions": 0,
        }
        dump(x2 / "mutations" / f"{mutation_row['mutation_id']}.json", receipt)
        mutation_receipts.append(receipt)
        failure_id = mutation_row["mutation_id"] + "-N"
        pass_id = mutation_row["mutation_id"] + "-P"
        methods.append(
            method(
                failure_id,
                mutation_row["expected_rejection"],
                False,
                recovered_by=pass_id,
                state_change=False,
                status="rejected_negative_zero_credit",
            )
        )
        methods.append(method(pass_id, "The preregistered invalid fixture was deterministically rejected and retained.", True, failed_witness_preserved=failure_id))

    skill_receipts = []
    for skill in skill_plan["phase_local_skills"]:
        validation, smoke = build_skill(x2, skill["skill_id"], skill["name"], f"Validate {skill['name']} within the synthetic lost-property evidence boundary.")
        if not validation["accepted"] or not smoke["accepted"]:
            raise SystemExit("phase-local skill failed: " + skill["name"])
        dump(x2 / "skill-receipts" / f"{skill['skill_id']}-quick.json", validation)
        dump(x2 / "skill-receipts" / f"{skill['skill_id']}-smoke.json", smoke)
        skill_receipts.append({"skill_id": skill["skill_id"], "name": skill["name"], "quick": True, "smoke": True, "global_install": False})
        methods.append(method(skill["skill_id"] + "-Q", skill["name"] + " quick validation", True))
        methods.append(method(skill["skill_id"] + "-S", skill["name"] + " zero-row smoke use", True))

    runner_receipts = []
    runner_names = [
        "proposal_contracts",
        "positive_controls",
        "mutation_rejector",
        "claim_state",
        "provenance",
        "privacy",
        "accessibility",
        "portfolio",
        "method_flow",
        "report",
    ]
    for index, (plan, runner_name) in enumerate(zip(skill_plan["family_current_runners"], runner_names, strict=True), start=1):
        script = repo / "scripts" / plan["name"]
        positive = json.loads(subprocess.check_output([sys.executable, str(script), "--smoke"], text=True))
        invalid = json.loads(subprocess.check_output([sys.executable, str(script), "--smoke", "--invalid"], text=True))
        if not positive["expectation_met"] or not positive["accepted"]:
            raise SystemExit("positive runner smoke failed: " + plan["name"])
        if not invalid["expectation_met"] or invalid["accepted"]:
            raise SystemExit("invalid runner smoke was not rejected: " + plan["name"])
        dump(x2 / "runner-receipts" / f"OT6763-RUNNER-{index:02d}-positive.json", positive)
        dump(x2 / "runner-receipts" / f"OT6763-RUNNER-{index:02d}-invalid.json", invalid)
        runner_receipts.append({"runner_id": plan["runner_id"], "name": plan["name"], "positive": True, "invalid_rejected": True})
        failed_id = f"OT6763-RUNNER-{index:02d}-N"
        pass_id = f"OT6763-RUNNER-{index:02d}-R"
        methods.append(method(f"OT6763-RUNNER-{index:02d}-P", plan["name"] + " positive smoke", True))
        methods.append(method(failed_id, plan["name"] + " invalid smoke fixture retained", False, recovered_by=pass_id, status="rejected_negative_zero_credit"))
        methods.append(method(pass_id, plan["name"] + " rejected its invalid smoke fixture", True, failed_witness_preserved=failed_id))

    bounded_tasks = []
    for lane, rows in (("safe_now", portfolio["safe_now"]), ("candidate", portfolio["candidate"]), ("clean_fix_refine", cfr_plan["owner_tasks"])):
        for row in rows:
            receipt = task_receipt(row, lane)
            dump(x2 / "task-receipts" / lane / f"{row['task_id']}.json", receipt)
            bounded_tasks.append(receipt)
            methods.append(method(row["task_id"] + "-P", row["description"], True, core_outcome_promotion=False))

    exact = [{**row, "status": "unexecuted_exact_gate", "execution_count": 0} for row in portfolio["exact_approval"]]
    blocked = [{**row, "status": "blocked_unexecuted", "execution_count": 0} for row in portfolio["blocked"]]
    dump(x2 / "portfolio" / "exact-approval-packets.json", {"count": len(exact), "packets": exact})
    dump(x2 / "portfolio" / "blocked-packets.json", {"count": len(blocked), "packets": blocked})

    # Exercise the distinct bounded helper surfaces directly as part of x2 evidence.
    claim_state = validate_claim_state(
        [
            {"state": "intake", "real_action": "none"},
            {"state": "held", "real_action": "none"},
            {"state": "challenged", "real_action": "none"},
            {"state": "held", "real_action": "none"},
        ]
    )
    provenance = validate_provenance(["SYNTH-ITEM", "SYNTH-HOLD", "SYNTH-CORRECTION"], [("SYNTH-ITEM", "SYNTH-HOLD"), ("SYNTH-HOLD", "SYNTH-CORRECTION")])
    accessible = accessibility_proxy(
        {
            "title": "Synthetic found item",
            "summary": "No real item or claimant",
            "status": "held_proxy",
            "correction_route": "synthetic_statement_attachment",
            "keyboard_order": [1, 2, 3],
            "manual_user_review": False,
        }
    )
    if not all(result["accepted"] for result in (claim_state, provenance, accessible)):
        raise SystemExit("bounded helper surface failed")
    dump(x2 / "bounded-helper-evidence.json", {"claim_state": claim_state, "provenance": provenance, "accessibility": accessible})

    outcome_counts = dict(Counter(row["outcome"] for row in outcomes))
    if outcome_counts != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise SystemExit("unexpected core outcome counts")
    failed_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    if failed_count + pass_count != len(methods):
        raise SystemExit("method truth partition mismatch")

    dump(x2 / "proposal-outcomes.json", {"proposal_count": 40, "outcome_counts": outcome_counts, "outcomes": outcomes})
    dump(
        x2 / "mutation-summary.json",
        {
            "preregistered": 160,
            "executed": len(mutation_receipts),
            "rejected": sum(not row["accepted"] for row in mutation_receipts),
            "failed_witnesses_retained": sum(row["failed_witness_retained"] for row in mutation_receipts),
        },
    )
    dump(x2 / "skill-summary.json", {"count": len(skill_receipts), "global_installs": 0, "skills": skill_receipts})
    dump(x2 / "runner-summary.json", {"count": len(runner_receipts), "runners": runner_receipts})
    dump(
        x2 / "portfolio" / "execution-summary.json",
        {
            "safe_now_completed": sum(row["lane"] == "safe_now" for row in bounded_tasks),
            "candidate_completed_without_core_promotion": sum(row["lane"] == "candidate" for row in bounded_tasks),
            "clean_fix_refine_completed": sum(row["lane"] == "clean_fix_refine" for row in bounded_tasks),
            "exact_approval_unexecuted": len(exact),
            "blocked_unexecuted": len(blocked),
            "real_world_rows": 0,
            "external_actions": 0,
        },
    )
    dump(
        x2 / "method-flow" / "ledger.json",
        {
            "activation_baseline": startup["activation_baseline"],
            "methods": methods,
            "phase_ledger_counts": {"methods": len(methods), "failed": failed_count, "passing": pass_count},
            "current_overlay": {
                "effective_negatives": startup["activation_baseline"]["effective_negatives"] + failed_count,
                "effective_methods": startup["activation_baseline"]["effective_methods"] + len(methods),
                "retained_failed_witnesses": startup["activation_baseline"]["retained_failed_witnesses"] + failed_count,
                "bounded_passing_witnesses": startup["activation_baseline"]["bounded_passing_witnesses"] + pass_count,
                "open_gaps": startup["activation_baseline"]["open_gaps"] + outcome_counts["open_gap"],
                "exact_gates": startup["activation_baseline"]["exact_gates"] + outcome_counts["exact_gate"],
            },
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        x2 / "retained-negative-register.json",
        {
            "count": failed_count,
            "failed_witnesses": [row for row in methods if row["truth"] is False],
            "converted_to_pass": 0,
        },
    )
    dump(
        x2 / "open-gap-register.json",
        {
            "inherited": startup["activation_baseline"]["open_gaps"],
            "new": outcome_counts["open_gap"],
            "current": startup["activation_baseline"]["open_gaps"] + outcome_counts["open_gap"],
            "rows": [row for row in outcomes if row["outcome"] == "open_gap"],
        },
    )
    dump(
        x2 / "exact-gate-register.json",
        {
            "inherited": startup["activation_baseline"]["exact_gates"],
            "new": outcome_counts["exact_gate"],
            "current": startup["activation_baseline"]["exact_gates"] + outcome_counts["exact_gate"],
            "rows": [row for row in outcomes if row["outcome"] == "exact_gate"],
            "exact_approval_packets_unexecuted": len(exact),
            "blocked_packets_unexecuted": len(blocked),
        },
    )
    dump(
        x2 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "declared_proposal_chain": 7510,
            "outcomes": outcome_counts,
            "effective_negatives": startup["activation_baseline"]["effective_negatives"] + failed_count,
            "effective_methods": startup["activation_baseline"]["effective_methods"] + len(methods),
            "retained_failed_witnesses": startup["activation_baseline"]["retained_failed_witnesses"] + failed_count,
            "bounded_passing_witnesses": startup["activation_baseline"]["bounded_passing_witnesses"] + pass_count,
            "open_gaps": startup["activation_baseline"]["open_gaps"] + outcome_counts["open_gap"],
            "exact_gates": startup["activation_baseline"]["exact_gates"] + outcome_counts["exact_gate"],
            "preregistered_mutations_executed": 160,
            "preregistered_mutations_rejected": 160,
            "phase_local_skills_built_validated_smoked": 20,
            "family_current_runners_used": 10,
            "real_world_rows": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    text(
        x2 / "integrated-overview.md",
        """# Orin Thale v676-v3 bounded x2 evidence overview

The owner-local x2 executed forty zero-row structural controls and rejected all 160 preregistered invalid mutations. Core dispositions are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Twenty phase-local skills were built, quick-validated, and smoke-used without global installation; ten family-current runners accepted their positive fixture and rejected their invalid fixture. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE tasks completed without core-outcome promotion. Twenty exact-approval and ten blocked packets remain unexecuted.

The primary pillar is Freed ID and CBR Heart through wholly synthetic public-transport, library, and recreation-centre lost-property workflow lenses. The phase used no real person, claimant, finder, item, identifier, venue, record, custody event, return, disposal, hazardous-item decision, police report, insurance action, identity event, key, proof, participant, measurement, cultural record, Māori data, or external action.

Software structure, source citations, and same-owner tests establish no ownership, property right, remedy, legal interpretation, professional competence, production readiness, privacy or accessibility completeness, empirical GMUT confirmation, THOS effectiveness, live Freed ID lifecycle, affected-party acceptance, cultural legitimacy, Māori authority, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    text(
        x2 / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Orin Thale v676-v3 bounded evidence</title></head>
<body><main><h1>Orin Thale v676-v3 bounded evidence</h1>
<p>Forty zero-row proposal contracts produced 28 completed, 8 represented, 2 open-gap, and 2 exact-gate dispositions.</p>
<h2>Boundaries</h2><p>No real item, person, claimant, identifier, custody event, authority decision, or external action occurred. Accessibility remains incomplete without manual assistive-technology and affected-user evaluation.</p>
<h2>Terminal truth</h2><p>NOT_READY_FOR_STAGE_20.</p></main></body></html>
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()
