#!/usr/bin/env python3
"""Resume Auren v677-v7 only after the retained npm-list timeout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import build_ghc_family_auren_lark_v677_v7_x2 as phase


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_persisted_successes(x2: Path) -> dict[str, Any]:
    contracts = sorted((x2 / "contracts").glob("AUR6777-N*.json"))
    evidence = sorted((x2 / "evidence").glob("AUR6777-N*-receipt.json"))
    skills = sorted(path for path in (x2 / "skills").iterdir() if path.is_dir())
    mutations = load(x2 / "mutation-ledger.json")
    skill_receipt = load(x2 / "skill-validation-receipt.json")
    runner_receipt = load(x2 / "runner-smoke-receipt.json")
    deck = load(x2 / "flashcards" / "deck.json")
    portfolio = load(x2 / "portfolio-execution.json")
    checks = {
        "contracts": len(contracts) == 60,
        "evidence": len(evidence) == 60,
        "mutations": mutations.get("rejected") == 240 and mutations.get("accepted") == 0,
        "skills": len(skills) == 20 and len(skill_receipt.get("positive", [])) == 20,
        "runners": runner_receipt.get("runner_count") == 10,
        "flashcards": deck.get("card_count") == 135,
        "safe_now": len(portfolio.get("owner_safe_now", [])) == 120,
        "candidates": len(portfolio.get("owner_candidate", [])) == 80,
        "clean_fix_refine": len(portfolio.get("owner_clean_fix_refine", [])) == 100,
    }
    if not all(checks.values()):
        raise RuntimeError("persisted pre-toolchain success set is incomplete: " + json.dumps(checks, sort_keys=True))
    return deck


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if phase.run(repo, "rev-parse", "HEAD") != phase.X1:
        raise SystemExit("toolchain recovery requires the immutable Auren x1 head")
    root = repo / "docs" / phase.OWNER_SLUG / phase.PHASE
    x1 = root / "x1"
    x2 = root / "x2"
    deck = require_persisted_successes(x2)
    proposals = load(x1 / "new-proposal-freeze.json")["proposals"]
    inherited = load(x1 / "inherited-proposal-selection.json")["rows"]
    plan = load(x1 / "skill-runner-plan.json")
    startup = load(x1 / "method-flow-startup.json")
    operational_failures = [
        (row["failure_id"], row["failure"], row["recovery_id"], row["recovery"])
        for row in startup["startup_failure_recovery_pairs"]
    ] + phase.X2_OPERATIONAL_FAILURES

    tools = phase.tool_receipt(repo)
    if not tools["all_versions_present"] or not tools["tzdata_functional_smoke"]["passed"]:
        raise RuntimeError("dependency-corrected direct tool probes did not all succeed")
    phase.dump(x2 / "toolchain" / "verification-receipt.json", tools)
    phase.dump(
        x2 / "toolchain" / "operational-failures.json",
        {
            "pairs": [
                {"failure_id": f, "failure": ft, "recovery_id": p, "recovery": pt}
                for f, ft, p, pt in operational_failures
            ]
        },
    )
    ledger = phase.method_flow(
        proposals,
        inherited,
        plan["owner_skill_ideas"],
        list(phase.RUNNER_MAP),
        list(phase.TOOL_VERSIONS),
        deck["cards"],
        operational_failures,
    )
    phase.dump(x2 / "method-flow" / "ledger.json", ledger)
    phase.dump(
        x2 / "phase-truth.json",
        {
            "owner": phase.OWNER,
            "phase": phase.PHASE,
            "source": phase.SOURCE,
            "x1": phase.X1,
            "lifecycle_state": "X2_EVIDENCE_PRECOMMIT",
            "declared_proposal_chain": 8210,
            "outcomes": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "inherited_revalidated_at_zero_credit": 60,
            "preregistered_mutations_executed": 240,
            "preregistered_mutations_rejected": 240,
            "owner_safe_now_completed": 120,
            "owner_candidate_completed": 80,
            "owner_clean_fix_refine_completed": 100,
            "phase_local_skills_built_validated_and_used": 20,
            "family_current_runners_built_validated_and_used": 10,
            "new_direct_tools_installed_and_used": 0,
            "existing_tool_surfaces_verified": 25,
            "global_skill_promotions": 0,
            "flashcards": len(deck["cards"]),
            "real_world_rows": 0,
            "external_real_world_actions": 0,
            **ledger["effective"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    phase.dump(
        x2 / "owner-local-skill-state.json",
        {
            "validated_owner_local_candidates": phase.LOCAL_VALIDATION_CANDIDATES,
            "global_promotion_target": 0,
            "global_promotion_completed": 0,
            "state": "OWNER_LOCAL_ONLY_NO_GLOBAL_INSTALLATION",
            "overwrite_allowed": False,
        },
    )
    phase.write_text(
        x2 / "accessible-report-draft.html",
        """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Auren Lark v677-v7 evidence</title></head>
<body><header><h1>Auren Lark v677-v7 evidence</h1><p>Same-owner synthetic software and documentation evidence only.</p></header>
<nav aria-label="Sections"><ol><li><a href="#program">Program</a></li><li><a href="#tools">Tools</a></li><li><a href="#boundaries">Boundaries</a></li></ol></nav>
<main><section id="program"><h2>Program</h2><p>Sixty inherited rows retain zero novelty and automatic completion credit. Sixty new source-bounded contracts produced 42 completed, 12 represented, 3 open-gap, and 3 exact-gate structural outcomes.</p></section>
<section id="tools"><h2>Tools and cards</h2><p>Twenty-five existing tool surfaces received read-only version verification; twenty owner-local skills, ten family runners, and 135 four-tier cards received bounded accepting and rejecting checks.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>No real requester, representative, agency, record, access request, correction, counterstatement, disclosure, refusal, complaint, appeal, remedy, disposal, person, participant, measurement, identity event, rights decision, professional decision, legal or cultural decision, Māori-authority act, empirical GMUT confirmation, THOS effectiveness, production Freed ID, complete accessibility or privacy assurance, exhaustive security, independent reproduction, proof, canon, or Stage 20 authority is established.</p></section></main>
<footer><p>Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p></footer></body></html>""",
    )
    print(
        json.dumps(
            {
                "status": "RECOVERED_X2_FROM_TOOLCHAIN_BOUNDARY",
                "operational_failures": len(operational_failures),
                "tools_verified": tools["observed_package_count"],
                "method_flow": {
                    "failed": ledger["phase_failed_witnesses"],
                    "passed": ledger["phase_passing_witnesses"],
                },
                "successful_components_replayed": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
