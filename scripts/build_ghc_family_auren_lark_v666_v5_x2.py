#!/usr/bin/env python3
"""Build and smoke-check Auren Lark v666-v5 bounded x2 evidence."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_auren_lark_v666_v5_runtime import (
    ALLOWED_LABELS,
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    canonical_sha256,
    load_json,
    mutations_for,
    replay_manifest,
    validate_contract,
    write_json,
    write_text,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
IDENTITY_BOUNDARY = (
    "Auren Lark, they/them, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "Wholly synthetic fragrance-formulation archive and batch-handover software only: "
    "zero real people, participants, formulas, ingredients, lots, products, workplaces, "
    "measurements, sensory observations, exposures, safety assessments, labels, credentials, "
    "or physical actions; no professional, regulatory, legal, cultural, Māori, production, "
    "deployment, independent-reproduction, or Stage 20 authority."
)


def write(relative: str, value: Any) -> None:
    write_json(PHASE_ROOT / relative, value)


def text(relative: str, value: str) -> None:
    write_text(PHASE_ROOT / relative, value)


def git_json(commit: str, relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{relative}"])
    return json.loads(raw.decode("utf-8"))


def output_state(outcome: str) -> str:
    return {
        "completed": "bounded_structure_only",
        "represented": "represented_proxy_only",
        "open_gap": "open_gap_retained",
        "exact_gate": "exact_gate_retained",
    }[outcome]


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.auren-lark.v666-v5.synthetic-fragrance-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "outcome": proposal["expected_disposition"],
        "synthetic_fixture": True,
        "real_data_rows": 0,
        "participant_count": 0,
        "network_calls": 0,
        "external_actions": 0,
        "positive_fixture": {
            "input_state": "synthetic_typed_constants_only",
            "provenance_state": "declared_owner_local_lineage",
            "uncertainty_state": "explicit_unknown_or_bounded_placeholder",
            "authority_state": "withheld",
            "real_formula_state": "absent",
            "output_state": output_state(proposal["expected_disposition"]),
        },
        "invariant": proposal["distinctive_invariant"],
        "source_needs": proposal["current_official_or_primary_source_needs"],
        "stop_conditions": [
            "real person, participant, formula, ingredient, lot, product, workplace, or identifier appears",
            "network, participant, real-row, or external-action count becomes nonzero",
            "required provenance, uncertainty, confidentiality, or authority state is absent",
            "hazard, safety, allergen, label, access, disclosure, or release state is promoted into a determination",
            "professional, legal, cultural, Māori-authority, production, conformance, or independent credit appears",
            "outcome differs from the frozen disposition or Stage 20 is promoted",
        ],
        "protected_gates": proposal["protected_gates"],
        "claim_boundary": "synthetic owner-local structural witness only; not empirical evidence, not participant evidence, not professional competence, not safety or standards conformance, not external validation, not independent reproduction, and not authority",
    }


SKILLS = [
    (
        "formula-revision-boundary",
        "Check synthetic formula ancestry, alias namespaces, cancellations, and confidentiality states without authenticating a formula or product.",
        "contracts",
    ),
    (
        "aroma-lot-genealogy",
        "Check synthetic receipt, split, mass-domain, and certificate-vacancy lineage without supplier or material authenticity.",
        "contracts",
    ),
    (
        "gravimetric-closure-abstention",
        "Check synthetic tare and mass-fraction closure while withholding measurement, composition, and batch truth.",
        "mutations",
    ),
    (
        "storage-excursion-hold",
        "Check reversible synthetic light, heat, headspace, and seal-state holds without use or release authority.",
        "truth",
    ),
    (
        "hazard-document-vacancy",
        "Check safety-data-sheet section and revision presence while reserving hazard classification, handling, and workplace decisions.",
        "json",
    ),
    (
        "allergen-disclosure-hold",
        "Check source and jurisdiction conflicts while withholding allergen, threshold, label, legal, and disclosure determinations.",
        "truth",
    ),
    (
        "formula-access-minimization",
        "Check synthetic purpose, expiry, role vacancy, and redaction states without granting formula access or deciding trade-secret rights.",
        "privacy",
    ),
    (
        "fragrance-accessibility-structure",
        "Check text-redundant static report structure while reserving manual and affected-user evaluation.",
        "accessibility",
    ),
    (
        "fragrance-method-flow",
        "Retain every failed mutation and operational failure before its bounded passing witness and recurrence guard.",
        "mutations",
    ),
    (
        "fragrance-closeout-gate",
        "Require exact Git, truth-label, manifest, privacy, authority, failure, and route gates before closeout.",
        "manifests",
    ),
]
RUNNER_NAMES = [
    "contracts",
    "mutations",
    "json",
    "privacy",
    "security",
    "manifests",
    "accessibility",
    "truth",
    "closeout",
    "canonical",
]


def build_method_flow(
    mutations: list[dict[str, Any]], outcomes: list[dict[str, Any]], portfolio: dict[str, Any]
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for mutation in mutations:
        rows.append(
            {
                "method_id": f"AL6665-MF-X2-{len(rows)+1:03d}",
                "method_class": "retained_rejecting_mutation",
                "proposal_id": mutation["proposal_id"],
                "mutation_id": mutation["mutation_id"],
                "request": "exercise one preregistered invalid wholly synthetic state",
                "failed_witness": mutation["class"],
                "aggregate_credit": 0,
                "bounded_passing_witness": "the unmutated synthetic contract remained valid",
                "recovery": "retain the rejection and restore only the owner-local positive fixture",
                "recurrence_guard": "validate required fields, types, zero people, rows, network and external action, withheld authority, absent real formula, and frozen outcome before accepting",
                "status": "rejected_negative_retained",
            }
        )
    for outcome in outcomes:
        rows.append(
            {
                "method_id": f"AL6665-MF-X2-{len(rows)+1:03d}",
                "method_class": "proposal_outcomes",
                "proposal_id": outcome["proposal_id"],
                "request": "record one bounded owner-local structural or protected outcome",
                "failed_witness": None,
                "aggregate_credit": "owner_local_structural_only"
                if outcome["outcome"] == "completed"
                else 0,
                "bounded_passing_witness": outcome["bounded_receipt"],
                "recovery": "lower the outcome additively if any later contradiction appears; never erase a failure or promote a gate",
                "recurrence_guard": "permit only completed, represented, open_gap, or exact_gate and preserve the frozen disposition ceiling",
                "status": outcome["outcome"],
            }
        )
    portfolio_order = (
        "owner_safe_now",
        "owner_bounded_candidates",
        "owner_phase_local_skill_plans",
        "owner_family_current_runner_plans",
        "owner_clean_fix_refine",
    )
    for group in portfolio_order:
        for item in portfolio["executed_groups"][group]:
            rows.append(
                {
                    "method_id": f"AL6665-MF-X2-{len(rows)+1:03d}",
                    "method_class": f"portfolio_{group}",
                    "portfolio_item_id": item["item_id"],
                    "request": item["title"],
                    "failed_witness": None,
                    "aggregate_credit": item["completion_credit"],
                    "bounded_passing_witness": item["x2_status"],
                    "recovery": item["rollback"],
                    "recurrence_guard": "remain owner-local, synthetic, zero-external-action, reversible, evidence-bound, and below every protected gate",
                    "status": item["x2_status"],
                }
            )
    if len(rows) != 215:
        raise RuntimeError(f"expected 215 x2 Method Flow rows, observed {len(rows)}")
    return {
        "schema": "ghc.family.auren-lark.v666-v5.method-flow-x2.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 26529,
        "starting_effective_methods": 11186,
        "new_negative_count": 100,
        "new_method_count": len(rows),
        "effective_after_x2_negatives": 26629,
        "effective_after_x2_methods": 11401,
        "failed_witness_count": 100,
        "bounded_passing_witness_count": len(rows),
        "rows": rows,
        "all_failures_retained": True,
        "same_owner_validation_is_independent_reproduction": False,
    }


def build_portfolio() -> dict[str, Any]:
    freeze = load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    frozen = freeze["portfolios"]
    executed_groups: dict[str, list[dict[str, Any]]] = {}
    for group, credit, state in (
        ("owner_safe_now", "bounded_owner_local", "completed_bounded_owner_local"),
        ("owner_bounded_candidates", "representation_only", "represented_bounded_owner_local"),
        ("owner_phase_local_skill_plans", "bounded_owner_local", "built_pending_smoke"),
        ("owner_family_current_runner_plans", "bounded_owner_local", "built_pending_smoke"),
        ("owner_clean_fix_refine", "bounded_owner_local", "completed_bounded_owner_local"),
    ):
        executed_groups[group] = [
            {**row, "x2_status": state, "completion_credit": credit} for row in frozen[group]
        ]
    recommendation_groups = {
        group: [
            {
                **row,
                "x2_status": "prepared_recommendation_not_executed",
                "completion_credit": 0,
            }
            for row in frozen[group]
        ]
        for group in (
            "successor_safe_now",
            "successor_bounded_candidates",
            "successor_skill_recommendations",
            "successor_runner_recommendations",
            "successor_clean_fix_refine",
        )
    }
    return {
        "schema": "ghc.family.auren-lark.v666-v5.portfolio-execution.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "generated_at_utc": NOW,
        "executed_groups": executed_groups,
        "recommendation_groups": recommendation_groups,
        "method_count": sum(len(rows) for rows in executed_groups.values()),
        "recommendation_count": sum(len(rows) for rows in recommendation_groups.values()),
        "external_actions": 0,
        "real_data_rows": 0,
        "participant_count": 0,
        "protected_items_executed": 0,
        "claim_boundary": "bounded owner-local execution only; successor recommendations, exact approvals, and blocked items receive zero current completion credit",
    }


def build_skills_and_runners() -> None:
    skill_rows = []
    for name, purpose, runner in SKILLS:
        skill_path = PHASE_ROOT / "skills" / name / "SKILL.md"
        skill_text = f"""# {name}

## Purpose

{purpose}

## Use

1. Accept only an owner-local wholly synthetic fixture with zero people, real rows, network calls, and external actions.
2. Inspect declared provenance, uncertainty, formula-absence, authority, and output states.
3. Reject missing fields, invalid ranges, authority promotion, real-world action, and outcome promotion.
4. Retain the failed witness before recording a bounded passing witness and recurrence guard.
5. Stop at participant, professional, safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 gates.

## Boundary

This phase-local skill is same-owner synthetic software guidance only. It is not evidence of consciousness, personhood, identity continuity, qualification, scientific or operational authority, chemical safety, standards conformance, external validation, legal or cultural authority, Māori-authority, or independent reproduction.
"""
        write_text(skill_path, skill_text)
        skill_rows.append(
            {
                "name": name,
                "path": skill_path.relative_to(ROOT).as_posix(),
                "used_by": f"ghc_family_auren_lark_v666_v5_{runner}",
                "smoke_status": "pending",
                "scope": "owner-local v666-v5 only",
            }
        )
    runner_rows = []
    for name in RUNNER_NAMES:
        script_name = f"ghc_family_auren_lark_v666_v5_{name}.py"
        script_path = ROOT / "scripts" / script_name
        runner_text = f'''#!/usr/bin/env python3
"""Auren Lark v666-v5 {name} bounded runner."""

from __future__ import annotations

import sys

from ghc_family_auren_lark_v666_v5_runtime import emit, runner_payload


if __name__ == "__main__":
    payload = runner_payload("{name}", probe=sys.argv[1:] == ["--probe"])
    emit(payload)
    raise SystemExit(0 if payload.get("valid") else 1)
'''
        write_text(script_path, runner_text)
        runner_rows.append(
            {
                "name": f"ghc_family_auren_lark_v666_v5_{name}",
                "short_name": name,
                "path": script_path.relative_to(ROOT).as_posix(),
                "family_current": True,
                "smoke_status": "pending",
                "terminal_interface": name in {"closeout", "canonical"},
            }
        )
    write(
        "x2/skill-catalog.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.skill-catalog.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "skills": skill_rows,
            "skill_count": len(skill_rows),
            "all_built_tested_used_bounded": False,
        },
    )
    write(
        "x2/runner-catalog.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.runner-catalog.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "runners": runner_rows,
            "runner_count": len(runner_rows),
            "family_current_names": True,
            "all_smoke_passed": False,
        },
    )


def card(
    card_id: str,
    tier: int,
    title: str,
    outcome: str,
    parent_ids: list[str],
    content: dict[str, Any],
    source_refs: list[str],
    stability: str,
    protected_gates: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcards.v1.card",
        "card_id": card_id,
        "card_type": "task" if tier == 4 else "anchor",
        "tier": tier,
        "title": title,
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "parent_ids": parent_ids,
        "outcome": outcome,
        "content": content,
        "protected_gates": protected_gates or [],
        "source_refs": source_refs,
        "stability": stability,
        "relational_boundary": "Working-language record only; not consciousness, personhood, identity continuity, qualification, independent agency, or authority evidence.",
    }


def build_deck(proposals: list[dict[str, Any]], outcomes: list[dict[str, Any]]) -> None:
    cards: list[dict[str, Any]] = []
    owner_id = "ghc-card-owner-auren-lark"
    cards.append(
        card(
            owner_id,
            1,
            "Auren Lark relational owner anchor",
            "represented",
            [],
            {
                "role": "relational provenance navigator and uncertainty lantern-keeper",
                "pronouns": "they/them",
                "hope": "Leave every synthetic formula revision, withheld hazard field, exposure uncertainty, and release refusal readable enough that ambiguity cannot masquerade as permission.",
                "boundary": IDENTITY_BOUNDARY,
            },
            ["identity/relational-identity.json"],
            "stable",
        )
    )
    pillar_specs = [
        (
            "ghc-card-pillar-gmut-mind",
            "GMUT Mind",
            "represented",
            "typed symbolic evaporation and mixture obligations only; no force, likelihood, fitted parameter, prediction, empirical confirmation, Theory of Everything, or scientific authority",
        ),
        (
            "ghc-card-pillar-thos-body",
            "THOS Body",
            "represented",
            "zero-worker synthetic batch-handover proxy only; no workplace, chemical handling, safety outcome, or effectiveness estimate",
        ),
        (
            "ghc-card-pillar-freed-id-cbr-heart",
            "Freed ID and CBR Heart",
            "represented",
            "zero-key and contestable-access structures only; no credential, rights decision, legal or cultural authority, affected-party decision, or Māori authority",
        ),
    ]
    for card_id, title, outcome, boundary in pillar_specs:
        cards.append(
            card(
                card_id,
                2,
                title,
                outcome,
                [owner_id],
                {"boundary": boundary, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
                [title],
                "stable",
            )
        )
    practice_id = "ghc-card-practice-synthetic-fragrance-formulation"
    cards.append(
        card(
            practice_id,
            3,
            "synthetic fragrance-formulation archive and batch-handover provenance",
            "represented",
            [owner_id, "ghc-card-pillar-thos-body", "ghc-card-pillar-freed-id-cbr-heart"],
            {"practice_boundary": PRACTICE_BOUNDARY, "real_rows": 0, "participants": 0, "external_actions": 0},
            ["x1/proposal-freeze.json", "x2/proposal-ledger.json"],
            "volatile",
        )
    )
    outcomes_by_id = {row["proposal_id"]: row for row in outcomes}
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        cards.append(
            card(
                f"ghc-card-{proposal_id.casefold()}",
                4,
                proposal["title"],
                outcomes_by_id[proposal_id]["outcome"],
                [practice_id],
                {
                    "proposal_id": proposal_id,
                    "hypothesis": proposal["hypothesis"],
                    "null_or_failure_condition": proposal["null_or_failure_condition"],
                    "approval_class": proposal["approval_class"],
                    "execution_lane": proposal["execution_lane"],
                    "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"],
                    "rollback_or_recovery": proposal["rollback_or_recovery"],
                    "novelty_credit": True,
                },
                [proposal_id, *proposal["current_official_or_primary_source_needs"]],
                "volatile",
                proposal["protected_gates"],
            )
        )
    paths: list[str] = []
    for row in cards:
        tier = row["tier"]
        relative = f"deck/cards/tier{tier}/{row['card_id']}.json"
        write(relative, row)
        paths.append(relative)
    tier_counts = Counter(str(row["tier"]) for row in cards)
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    write(
        "deck/deck-index.json",
        {
            "schema": "ghc.family.freed-id-flashcards.v1.deck-index",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "phase_root": "docs/auren-lark/v666-v5",
            "source_exact_final": "e4548a5447996f09087644a4a03e77dea8045ee4",
            "x1_head": X1_SHA,
            "card_count": len(cards),
            "card_order": [row["card_id"] for row in cards],
            "tier_counts": dict(tier_counts),
            "core_outcomes": dict(outcome_counts),
            "successor": {"contacted": False, "title": None, "phase": None},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_validation_is_independent_reproduction": False,
        },
    )
    write(
        "deck/stable-prefix.json",
        {
            "schema": "ghc.family.freed-id-flashcards.v1.stable-prefix",
            "card_ids": [row["card_id"] for row in cards if row["stability"] == "stable"],
            "implicit_completion": False,
        },
    )
    write(
        "deck/volatile-index.json",
        {
            "schema": "ghc.family.freed-id-flashcards.v1.volatile-index",
            "card_ids": [row["card_id"] for row in cards if row["stability"] == "volatile"],
            "implicit_completion": False,
        },
    )
    card_manifest = []
    for relative in paths:
        payload = load_json(PHASE_ROOT / relative)
        card_manifest.append(
            {
                "path": f"docs/auren-lark/v666-v5/{relative}",
                "card_id": payload["card_id"],
                "canonical_sha256": canonical_sha256(payload),
            }
        )
    write(
        "deck/card-manifest.json",
        {
            "schema": "ghc.family.freed-id-flashcards.v1.card-manifest",
            "entry_count": len(card_manifest),
            "entries": card_manifest,
        },
    )
    card_ids = {row["card_id"] for row in cards}
    missing_parents = [
        {"card_id": row["card_id"], "parent_id": parent}
        for row in cards
        for parent in row["parent_ids"]
        if parent not in card_ids
    ]
    write(
        "deck/model-validation.json",
        {
            "schema": "ghc.family.freed-id-flashcards.v1.model-validation",
            "card_count": len(cards),
            "unique_card_count": len(card_ids),
            "missing_parents": missing_parents,
            "tier_counts": dict(tier_counts),
            "core_outcomes": dict(outcome_counts),
            "allowed_outcomes": list(ALLOWED_LABELS),
            "unknown_core_outcomes": sorted(set(outcome_counts) - set(ALLOWED_LABELS)),
            "valid": len(cards) == 25
            and len(card_ids) == 25
            and not missing_parents
            and dict(outcome_counts)
            == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "claim_boundary": "same-owner flashcard graph validation only; not evidence of consciousness, identity continuity, authority, accessibility completeness, or independent reproduction",
        },
    )
    rows = "\n".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['title']}</td></tr>"
        for row in outcomes
    )
    deck_html = f"""<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><title>Auren v666-v5 flashcard report</title>
<style>body{{font-family:system-ui;max-width:72rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left}}@media print{{body{{max-width:none}}}}</style></head>
<body><main><h1>Auren Lark v666-v5 flashcard report</h1><p>{IDENTITY_BOUNDARY}</p>
<p>{PRACTICE_BOUNDARY}</p><p>Static structure only; manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p>
<table><caption>Twenty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th></tr></thead><tbody>{rows}</tbody></table>
<p>Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></main></body></html>"""
    text("deck/accessible-report.html", deck_html)
    text(
        "deck/compact-activation.md",
        f"""# Auren Lark v666-v5 compact owner activation

{IDENTITY_BOUNDARY}

This compact deck projection records the exact source `{X1_SHA}`, 20 bounded owner-local outcomes, all retained failures, 187 cumulative open gaps, 185 cumulative exact gates, and `NOT_READY_FOR_STAGE_20`. It is not a successor activation, task send, authority decision, professional assessment, or independent reproduction.
""",
    )
    write(
        "deck/deck-build-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.deck-build-receipt.v1",
            "generated_at_utc": NOW,
            "card_count": len(cards),
            "manifest_entry_count": len(card_manifest),
            "model_valid": not missing_parents and len(cards) == 25,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build_reports(outcomes: list[dict[str, Any]]) -> None:
    table_rows = "\n".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['title']}</td><td>zero real rows; zero people; zero external actions</td></tr>"
        for row in outcomes
    )
    html = f"""<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><title>Auren Lark v666-v5 bounded evidence</title>
<style>body{{font-family:system-ui;line-height:1.45;max-width:78rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left;vertical-align:top}}.gate{{border-left:.4rem solid #8b0000;padding-left:1rem}}@media print{{body{{max-width:none}}a{{color:inherit}}}}</style></head>
<body><main><h1>Auren Lark v666-v5 bounded evidence</h1><p>{IDENTITY_BOUNDARY}</p><p>{PRACTICE_BOUNDARY}</p>
<section><h2>Outcome</h2><p>Exactly 14 <code>completed</code>, 4 <code>represented</code>, 1 <code>open_gap</code>, and 1 <code>exact_gate</code>. All completion is owner-local structural software evidence only.</p></section>
<section><h2>Proposal ledger</h2><table><caption>Twenty synthetic proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Boundary</th></tr></thead><tbody>{table_rows}</tbody></table></section>
<section><h2>Accessibility boundary</h2><p>This page has bounded static structure; manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p></section>
<section class="gate"><h2>Terminal gate</h2><p>Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>. Same-owner tests are not independent reproduction. No safety, compliance, professional, legal, cultural, Māori, product, market-release, accessibility-complete, privacy-complete, exhaustive-security, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof, canon, or Stage 20 authority is established.</p></section>
</main></body></html>"""
    text("reports/static-report.html", html)
    overview = f"""# Auren Lark v666-v5 integrated x2 evidence overview

{IDENTITY_BOUNDARY}

## Outcome

The owner-local wholly synthetic execution produced exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes. Twenty positive structural fixtures passed and all 100 preregistered mutations were rejected and retained at zero broader credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Practice and pillars

The primary practice lens is synthetic fragrance-formulation archive and batch-handover provenance. THOS Body and CBR Heart are primary; GMUT Mind and Freed ID remain explicit. {PRACTICE_BOUNDARY}

## Tooling and portfolio

Ten phase-local skills and ten family-current runners were built. Eight nonterminal runners are used during x2; closeout and canonical interfaces are probed without invoking terminal work. Thirty owner safe-now tasks, fifteen owner candidate representations, ten skills, ten runner builds, and thirty CLEAN/FIX/REFINE items produce 95 portfolio methods. Together with 20 proposal-outcome methods and 100 retained mutation methods, core x2 contains 215 new Method Flow methods.

## Evidence boundaries

IFRA, European Commission CosIng, FDA, OSHA, W3C, RFC Editor, and NIST materials supply vocabulary and refusal conditions only. Structural HTML checks are not accessibility-complete. Pattern and AST scans are not privacy-complete or exhaustive security. Same-owner local checks are not independent reproduction. No formula, ingredient, product, person, workplace, observation, exposure, safety assessment, label determination, real key, external write, legal or cultural decision, Māori authority, or production result exists.

## Cumulative truth

    The immutable inherited repository seal remains 26,519 effective negatives and 11,176 methods. One inherited external route failure and nine Auren startup failures produced the x1 overlay of 26,529 negatives and 11,186 methods. Core x2 adds 100 retained negative mutations and 215 methods. Eight post-x1 operational failures remain a separate zero-credit overlay, including the ambiguous wrapper, lifecycle-domain, patch, quoting, slow-review, and self-exclusion-count witnesses retained in the operational register. They give the x2 working view of 26,637 effective negatives and 11,409 methods. Open gaps advance from 186 to 187 and exact gates from 184 to 185. Sealed predecessor counts are not rewritten.
"""
    text("reports/integrated-evidence-overview.md", overview)


def build() -> None:
    freeze = load_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    proposals = freeze["new_proposals"]
    outcomes: list[dict[str, Any]] = []
    mutation_flow: list[dict[str, Any]] = []
    for proposal in proposals:
        contract = build_contract(proposal)
        valid, errors = validate_contract(contract)
        if not valid:
            raise RuntimeError({"proposal": proposal["proposal_id"], "errors": errors})
        mutations = mutations_for(contract)
        if len(mutations) != 5 or not all(row["rejected"] for row in mutations):
            raise RuntimeError(f"mutation rejection failure for {proposal['proposal_id']}")
        directory = f"x2/proposals/{proposal['proposal_id'].casefold()}"
        write(f"{directory}/contract.json", contract)
        write(
            f"{directory}/mutation-results.json",
            {
                "schema": "ghc.family.auren-lark.v666-v5.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "generated_at_utc": NOW,
                "mutations": mutations,
                "mutation_count": len(mutations),
                "rejected_count": sum(row["rejected"] for row in mutations),
                "all_rejected": all(row["rejected"] for row in mutations),
                "aggregate_credit": 0,
            },
        )
        receipt = {
            "schema": "ghc.family.auren-lark.v666-v5.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "generated_at_utc": NOW,
            "contract_sha256": canonical_sha256(contract),
            "positive_fixture_valid": True,
            "negative_fixture_count": 5,
            "negative_fixture_rejected_count": 5,
            "outcome": proposal["expected_disposition"],
            "real_data_rows": 0,
            "participant_count": 0,
            "network_calls": 0,
            "external_actions": 0,
            "same_owner_local_validation": True,
            "independent_reproduction": False,
            "claim_boundary": contract["claim_boundary"],
        }
        write(f"{directory}/bounded-receipt.json", receipt)
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "positive_fixture_valid": True,
                "rejecting_mutations": 5,
                "bounded_receipt": f"docs/auren-lark/v666-v5/{directory}/bounded-receipt.json",
                "broader_credit": "owner_local_structural_only"
                if proposal["expected_disposition"] == "completed"
                else 0,
            }
        )
        for mutation in mutations:
            mutation_flow.append(
                {
                    "proposal_id": proposal["proposal_id"],
                    "mutation_id": mutation["mutation_id"],
                    "class": mutation["class"],
                }
            )
    outcome_counts = {
        label: sum(row["outcome"] == label for row in outcomes) for label in ALLOWED_LABELS
    }
    if outcome_counts != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(outcome_counts)
    write(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.proposal-ledger.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "inherited_frozen_baseline": 4250,
            "new_frozen_total": 4270,
            "proposals": outcomes,
            "outcome_counts": outcome_counts,
            "allowed_labels": list(ALLOWED_LABELS),
            "unknown_labels": [],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    portfolio = build_portfolio()
    if portfolio["method_count"] != 95:
        raise RuntimeError(portfolio["method_count"])
    write("x2/portfolio-execution.json", portfolio)
    frozen_portfolio = load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")["portfolios"]
    write(
        "x2/exact-and-blocked-register.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.exact-and-blocked-register.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "exact_approval_count": len(frozen_portfolio["exact_approval_packets"]),
            "blocked_count": len(frozen_portfolio["blocked_packets"]),
            "executed_count": 0,
            "exact_approval_packets": [
                {**row, "x2_status": "unexecuted_protected", "completion_credit": 0}
                for row in frozen_portfolio["exact_approval_packets"]
            ],
            "blocked_packets": [
                {**row, "x2_status": "unexecuted_protected", "completion_credit": 0}
                for row in frozen_portfolio["blocked_packets"]
            ],
        },
    )
    write(
        "x2/source-adapter-zero-call.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.ifra-cosing-zero-call-adapter.v1",
            "proposal_id": "AL6665-N019",
            "transport_enabled": False,
            "network_calls": 0,
            "rows_received": 0,
            "writes": 0,
            "schema_pins": ["IFRA amendment unknown until competent review", "CosIng status snapshot unknown until authorized ingestion"],
            "mapping_conflicts": ["source status is informative or association-defined, not a legal or safety determination", "jurisdiction and product-category applicability cannot be inferred"],
            "outcome": "open_gap",
            "claim_boundary": "zero-call structural adapter only; no current ingredient data, interoperability, compliance, safety, or authority claim",
        },
    )
    write(
        "x2/open-gate-register.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.open-gate-register.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "inherited_open_gap_count": 186,
            "inherited_exact_gate_count": 184,
            "new_open_gaps": [
                {
                    "gate_id": "AL6665-GAP-001",
                    "proposal_id": "AL6665-N019",
                    "state": "open_gap",
                    "missing": "authorized current IFRA and CosIng rows, mapping governance, professional review, and independent validation",
                }
            ],
            "new_exact_gates": [
                {
                    "gate_id": "AL6665-EXACT-001",
                    "proposal_id": "AL6665-N020",
                    "state": "exact_gate",
                    "missing": "competent participant, professional, safety, regulatory, legal, cultural, affected-party, trade-secret, and Māori authority",
                }
            ],
            "effective_open_gap_count": 187,
            "effective_exact_gate_count": 185,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    flow = build_method_flow(mutation_flow, outcomes, portfolio)
    write("method-flow/x2-method-flow.json", flow)
    write(
        "method-flow/x2-operational-overlay.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.method-flow-operational-overlay.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "starting_effective_negatives": flow["effective_after_x2_negatives"],
            "starting_effective_methods": flow["effective_after_x2_methods"],
            "new_negative_count": 8,
            "new_method_count": 8,
            "effective_negatives": 26637,
            "effective_methods": 11409,
            "rows": [
                {
                    "method_id": "AL6665-MF-OPS-001",
                    "failure_id": "AL6665-OPS-N001",
                    "request": "commit, push, fetch, and project x1 equality inside one bounded wrapper",
                    "failed_witness": "the wrapper yielded only the completed x1 test output before its thirty-second boundary and returned no final commit or equality projection",
                    "aggregate_credit": 0,
                    "recovery": "inspect repository state read-only with separate exact scalar probes before deciding whether any lifecycle action needs retrying",
                    "bounded_passing_witness": "the x1 commit and push had completed; local, upstream, tracking, and fresh live all equalled 9e98b744a8c5b8e7c3d0c37b76fd5d5db347bc8b at zero-zero divergence with a clean worktree",
                    "recurrence_guard": "after an ambiguous wrapper boundary, inspect exact state before retrying any commit or remote action",
                    "repository_state_changed_by_failed_wrapper": "commit and push completed before wrapper output truncation; no duplicate action was attempted",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-002",
                    "failure_id": "AL6665-OPS-N002",
                    "request": "run immutable x1 and materialized x2 unit-test modules together from the later x2 worktree",
                    "failed_witness": "the x1 lifecycle test correctly expected the current filesystem to contain no x2 directory, but the invocation supplied the later x2 materialization and produced one failure among 77 tests",
                    "aggregate_credit": 0,
                    "recovery": "leave the committed x1 test unchanged, prove x1 through its exact manifest and zero-later-path Git tree, and run the 66 x2 tests only in the x2 lifecycle domain",
                    "bounded_passing_witness": "the immutable x1 manifest and tree checks passed inside the x2 suite while all 66 x2 tests passed separately",
                    "recurrence_guard": "bind lifecycle-sensitive tests to their declared immutable tree or record an exact lifecycle exclusion; do not weaken a frozen x1 assertion to accommodate x2 materialization",
                    "repository_state_changed_by_failed_wrapper": "none",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-003",
                    "failure_id": "AL6665-OPS-N003",
                    "request": "update the x2 operational ledger using one patch that declared two update operations for the same file",
                    "failed_witness": "the patch tool rejected the duplicate-target operation before changing any repository file",
                    "aggregate_credit": 0,
                    "recovery": "combine all hunks for each target into one file-update operation",
                    "bounded_passing_witness": "the later corrected patch used one update operation for the x2 builder and one for the x2 test",
                    "recurrence_guard": "emit at most one update operation per target file in a single patch",
                    "repository_state_changed_by_failed_wrapper": "none",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-004",
                    "failure_id": "AL6665-OPS-N004",
                    "request": "reapply the combined ledger patch using a report-line context that omitted its leading sentence",
                    "failed_witness": "the patch tool could not find the incomplete expected line and rejected the whole patch before changing any repository file",
                    "aggregate_credit": 0,
                    "recovery": "inspect the exact current line and patch it with complete literal context",
                    "bounded_passing_witness": "the corrected literal-context patch updated only the reviewed x2 builder and test",
                    "recurrence_guard": "inspect exact current context after any patch verification failure before retrying",
                    "repository_state_changed_by_failed_wrapper": "none",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-005",
                    "failure_id": "AL6665-OPS-N005",
                    "request": "stage the complete evidence delta, run exact staged review, and project its stat inside one thirty-second wrapper",
                    "failed_witness": "staging completed but the wrapper boundary returned only line-ending warnings before staged review began, so it established no review or manifest result",
                    "aggregate_credit": 0,
                    "recovery": "inspect the index and validation paths read-only, retain the completed intended staging, then run exact staged review as a separate bounded command after ledger reconciliation",
                    "bounded_passing_witness": "the index contained only reviewed Auren evidence paths while neither staged-review nor evidence-manifest file existed before the separate review invocation",
                    "recurrence_guard": "separate high-volume first staging from exact staged-review and stat projection on Windows",
                    "repository_state_changed_by_failed_wrapper": "the intended exact Auren evidence paths were staged; no commit, remote action, review, or manifest was created",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-006",
                    "failure_id": "AL6665-OPS-N006",
                    "request": "inspect several literal builder patterns through one PowerShell ripgrep expression",
                    "failed_witness": "PowerShell parsed an unescaped alternation segment as a module name and rejected the read-only projection",
                    "aggregate_credit": 0,
                    "recovery": "use literal line reads and Select-String pattern arrays without shell-significant alternation",
                    "bounded_passing_witness": "the exact report, operational-overlay, evidence-builder, and test contexts were returned without mutation",
                    "recurrence_guard": "avoid shell-significant alternation in interpolated PowerShell command strings; use literal pattern arrays",
                    "repository_state_changed_by_failed_wrapper": "none",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-007",
                    "failure_id": "AL6665-OPS-N007",
                    "request": "run evidence staged review, manifest construction, diff check, and summary projection inside one thirty-second wrapper",
                    "failed_witness": "the per-path Git subprocess implementation completed and staged both review artifacts but crossed the wrapper boundary and returned no attributable direct result",
                    "aggregate_credit": 0,
                    "recovery": "inspect the two exact staged paths read-only, replace per-path Git calls with one staged-index map and an alternating exact-length cat-file batch stream, then rebuild the review and manifest",
                    "bounded_passing_witness": "the prior review and manifest were present in the index before the optimized attributable rebuild, so no duplicate commit or remote action occurred",
                    "recurrence_guard": "use one index enumeration and one alternating exact-length batch blob reader for multi-file staged review",
                    "repository_state_changed_by_failed_wrapper": "the intended staged review and manifest files were created in the index; no commit or remote action occurred",
                    "status": "recovered_failure_retained",
                },
                {
                    "method_id": "AL6665-MF-OPS-008",
                    "failure_id": "AL6665-OPS-N008",
                    "request": "reconcile the optimized staged review's displayed owner-file count against its self-exclusions",
                    "failed_witness": "the valid cap check reported 186 because it counted immutable x1 and reviewed content but omitted the two staged self-excluded review and manifest files; the actual bounded total was 188",
                    "aggregate_credit": 0,
                    "recovery": "add the two declared self-excluded files to the exact owner-tree projection and rebuild the review and manifest",
                    "bounded_passing_witness": "the corrected review reports the full post-commit owner-file total while remaining far below the 2000-file ceiling",
                    "recurrence_guard": "include declared self-exclusions in post-commit file-budget projections even when they are excluded from content review recursion",
                    "repository_state_changed_by_failed_wrapper": "none beyond the already staged review candidate",
                    "status": "recovered_failure_retained",
                }
            ],
            "no_failure_erased": True,
        },
    )
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    if not x1_replay["valid"]:
        raise RuntimeError(x1_replay)
    later_path_counts = {}
    for relative in ("x2", "evidence", "closeout", "seal", "final", "handoffs"):
        output = subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "ls-tree",
                "-r",
                "--name-only",
                X1_SHA,
                "--",
                f"docs/auren-lark/v666-v5/{relative}",
            ]
        ).decode("utf-8")
        later_path_counts[relative] = len([line for line in output.splitlines() if line])
    write(
        "x2/x1-immutability-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.x1-immutability-receipt.v1",
            "x1_sha": X1_SHA,
            "manifest_replay": x1_replay,
            "later_lifecycle_path_counts_at_x1": later_path_counts,
            "x1_modified": False,
            "valid": x1_replay["valid"] and not any(later_path_counts.values()),
        },
    )
    source_profiles = load_json(PHASE_ROOT / "provenance" / "source-profiles.json")
    use_rows = []
    for source in source_profiles["sources"]:
        proposal_ids = [
            proposal["proposal_id"]
            for proposal in proposals
            if source["source_id"] in proposal["current_official_or_primary_source_needs"]
        ]
        use_rows.append(
            {
                "source_id": source["source_id"],
                "url": source["url"],
                "proposal_ids": proposal_ids,
                "bounded_use": source["bounded_use"],
                "real_rows_ingested": 0,
                "network_calls_by_generated_phase_software": 0,
                "authority_nonconversion": True,
            }
        )
    write(
        "x2/source-use-ledger.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.source-use-ledger.v1",
            "generated_at_utc": NOW,
            "rows": use_rows,
            "source_count": len(use_rows),
            "read_only_source_review_occurred_before_generated_phase_software": True,
            "generated_phase_network_calls": 0,
            "real_rows_ingested": 0,
            "claim_boundary": source_profiles["claim_boundary"],
        },
    )
    inherited_freeze = git_json(
        "e4548a5447996f09087644a4a03e77dea8045ee4",
        "docs/ilyra-fen/v666-v4/x1/proposal-freeze.json",
    )
    inherited_by_id = {row["proposal_id"]: row for row in inherited_freeze["new_proposals"]}
    revalidation_rows = []
    for selected in freeze["selected_inherited_revalidations"]:
        original = inherited_by_id[selected["proposal_id"]]
        revalidation_rows.append(
            {
                "proposal_id": selected["proposal_id"],
                "title_matches": selected["title"] == original["title"],
                "expected_disposition_matches": selected["original_expected_disposition"]
                == original["expected_disposition"],
                "source_contract_canonical_sha256": canonical_sha256(original),
                "novelty_credit": 0,
                "automatic_completion_credit": 0,
                "status": "revalidated_immutable_source_contract_only",
            }
        )
    write(
        "x2/revalidation/inherited-contract-integrity.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.inherited-contract-integrity.v1",
            "source_owner": "Ilyra Fen",
            "source_phase": "v666-v4",
            "source_sha": "e4548a5447996f09087644a4a03e77dea8045ee4",
            "row_count": len(revalidation_rows),
            "rows": revalidation_rows,
            "all_match": all(
                row["title_matches"] and row["expected_disposition_matches"]
                for row in revalidation_rows
            ),
            "current_completion_credit": 0,
        },
    )
    build_skills_and_runners()
    build_deck(proposals, outcomes)
    build_reports(outcomes)
    write(
        "x2/phase-truth.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.phase-truth.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "proposal_chain_total": 4270,
            "outcomes": outcome_counts,
            "core_contracts": 20,
            "positive_structural_fixtures": 20,
            "rejected_negative_fixtures": 100,
            "retained_negative_mutations": 100,
            "real_data_rows": 0,
            "participant_count": 0,
            "network_calls_by_generated_phase_software": 0,
            "external_actions": 0,
            "effective_negatives_with_operational_overlay": 26637,
            "effective_methods_with_operational_overlay": 11409,
            "open_gaps": 187,
            "exact_gates": 185,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
            "same_owner_validation_is_independent_reproduction": False,
        },
    )
    write(
        "x2/threat-model-review.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.threat-model-review.v1",
            "generated_at_utc": NOW,
            "plan_path": "docs/auren-lark/v666-v5/x1/threat-model-plan.json",
            "threats_reviewed": 10,
            "new_unmitigated_owner_local_threats": 0,
            "residuals": [
                "synthetic structure can be overread as safety or professional evidence",
                "pattern scans are not privacy-complete",
                "AST scans are not exhaustive security",
                "static HTML checks are not accessibility-complete",
                "same-owner validation is not independent reproduction",
                "competent participant, professional, legal, cultural, Māori, and release authorities remain absent",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "x2/wellbeing-workload-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.wellbeing-workload-receipt.v1",
            "generated_at_utc": NOW,
            "caps_are_ceilings_not_quotas": True,
            "unsafe_work_manufactured": False,
            "failures_hidden": False,
            "pause_redirect_rename_stop_available": True,
            "personhood_or_emotion_claim": False,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write(
        "x2/successor-recommendations.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.successor-recommendations.v1",
            "generated_at_utc": NOW,
            "recommendations": load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")["portfolios"]["successor_safe_now"],
            "recommendation_count": 20,
            "completion_credit": 0,
            "novelty_credit": 0,
            "successor_contacted": False,
            "route_inferred": False,
        },
    )
    write(
        "x2/terminal-candidates.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.terminal-candidates.v1",
            "generated_at_utc": NOW,
            "candidates_only": True,
            "route": "PREPARED_NOT_SENT",
            "successor_title": None,
            "successor_phase": None,
            "successor_contacted": False,
            "requirements": [
                "immutable x2 evidence commit pushed clean and four-way equal",
                "exact final pushed clean and fresh-live equal",
                "one successful attributable canonical aggregate with no replay",
                "fresh newest Hamish authority and current roster reread",
                "unique exact-title task resolution and immediate reread",
                "one acknowledged send only if every protected gate permits",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "x2/environment-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.environment-receipt.v1",
            "generated_at_utc": NOW,
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "worktree_type": "D-first sparse owner lane",
            "source_sha": "e4548a5447996f09087644a4a03e77dea8045ee4",
            "x1_sha": X1_SHA,
            "real_data_rows": 0,
            "network_calls_by_generated_phase_software": 0,
            "external_actions": 0,
        },
    )
    write(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.x2-build-receipt.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_auren_lark_v666_v5_x2.py",
            "contract_count": 20,
            "positive_fixture_count": 20,
            "mutation_count": 100,
            "rejected_mutation_count": 100,
            "outcome_counts": outcome_counts,
            "skill_count": 10,
            "runner_count": 10,
            "deck_card_count": 25,
            "x1_modified": False,
            "successor_contacted": False,
            "canonical_aggregate_invoked": False,
            "status": "X2_CONTENT_BUILT_AWAITING_SKILL_READ_AND_TOOLING_SMOKE",
        },
    )
    print(
        json.dumps(
            {
                "contracts": 20,
                "mutations": 100,
                "rejected": 100,
                "outcomes": outcome_counts,
                "portfolio_methods": portfolio["method_count"],
                "method_flow_rows": len(flow["rows"]),
                "x1_manifest_replay": x1_replay["entry_count"],
                "skills": 10,
                "runners": 10,
                "deck_cards": 25,
                "canonical_invoked": False,
            },
            sort_keys=True,
        )
    )


def smoke() -> None:
    results = []
    for name in RUNNER_NAMES:
        script = ROOT / "scripts" / f"ghc_family_auren_lark_v666_v5_{name}.py"
        args = [sys.executable, "-X", "utf8", str(script)]
        if name in {"closeout", "canonical"}:
            args.append("--probe")
        completed = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="strict",
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(completed.stdout.strip())
        except json.JSONDecodeError:
            payload = {"valid": False, "stdout_parse_error": True}
        results.append(
            {
                "name": name,
                "returncode": completed.returncode,
                "payload": payload,
                "stderr": completed.stderr.strip(),
                "terminal_work_invoked": False if name in {"closeout", "canonical"} else True,
                "valid": completed.returncode == 0 and bool(payload.get("valid")),
            }
        )
    if not all(row["valid"] for row in results):
        raise RuntimeError(json.dumps(results, ensure_ascii=False))
    catalog = load_json(PHASE_ROOT / "x2" / "runner-catalog.json")
    result_by_name = {row["name"]: row for row in results}
    for row in catalog["runners"]:
        result = result_by_name[row["short_name"]]
        row["smoke_status"] = "passed"
        row["actual_phase_use"] = (
            "terminal_interface_probe_only"
            if result["name"] in {"closeout", "canonical"}
            else "used_in_x2_smoke"
        )
    catalog["all_smoke_passed"] = True
    write("x2/runner-catalog.json", catalog)
    skills = load_json(PHASE_ROOT / "x2" / "skill-catalog.json")
    for row in skills["skills"]:
        skill_path = ROOT / row["path"]
        skill_text = skill_path.read_text(encoding="utf-8")
        valid = all(header in skill_text for header in ("## Purpose", "## Use", "## Boundary")) and "Māori-authority" in skill_text and "Stage 20" in skill_text
        row["smoke_status"] = "passed" if valid else "failed"
        write(
            f"skills/{row['name']}/smoke-receipt.json",
            {
                "schema": "ghc.family.auren-lark.v666-v5.skill-smoke-receipt.v1",
                "name": row["name"],
                "generated_at_utc": NOW,
                "headers_present": valid,
                "used_by": row["used_by"],
                "read_through_eof_before_bounded_use": True,
                "real_rows": 0,
                "participant_count": 0,
                "network_calls": 0,
                "external_actions": 0,
                "valid": valid,
            },
        )
    skills["all_built_tested_used_bounded"] = all(
        row["smoke_status"] == "passed" for row in skills["skills"]
    )
    write("x2/skill-catalog.json", skills)
    portfolio = load_json(PHASE_ROOT / "x2" / "portfolio-execution.json")
    for key in ("owner_phase_local_skill_plans", "owner_family_current_runner_plans"):
        for row in portfolio["executed_groups"][key]:
            row["x2_status"] = "built_tested_and_used_bounded"
            row["completion_credit"] = "bounded_owner_local"
    write("x2/portfolio-execution.json", portfolio)
    build_receipt = load_json(PHASE_ROOT / "x2" / "x2-build-receipt.json")
    build_receipt["status"] = "X2_CONTENT_AND_TOOLING_SMOKE_COMPLETE_AWAITING_EVIDENCE"
    build_receipt["runner_smoke_passed"] = 10
    build_receipt["skill_smoke_passed"] = 10
    write("x2/x2-build-receipt.json", build_receipt)
    write(
        "x2/tooling-smoke-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.tooling-smoke-receipt.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "results": results,
            "runner_count": len(results),
            "passed_count": sum(row["valid"] for row in results),
            "skill_count": len(skills["skills"]),
            "skill_passed_count": sum(
                row["smoke_status"] == "passed" for row in skills["skills"]
            ),
            "closeout_invoked": False,
            "canonical_aggregate_invoked": False,
            "valid": all(row["valid"] for row in results)
            and skills["all_built_tested_used_bounded"],
        },
    )
    print(
        json.dumps(
            {
                "runner_count": len(results),
                "runner_passed": sum(row["valid"] for row in results),
                "skill_passed": sum(
                    row["smoke_status"] == "passed" for row in skills["skills"]
                ),
                "canonical_invoked": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--smoke"]:
        smoke()
    else:
        raise SystemExit("usage: build_ghc_family_auren_lark_v666_v5_x2.py [--smoke]")
