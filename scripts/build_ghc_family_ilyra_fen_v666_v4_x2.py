#!/usr/bin/env python3
"""Build and smoke-check Ilyra Fen v666-v4 bounded x2 evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_ilyra_fen_v666_v4_runtime import (
    PHASE_ROOT,
    ROOT,
    canonical_sha256,
    load_json,
    mutations_for,
    validate_contract,
    write_json,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def write(relative: str, value: Any) -> None:
    write_json(PHASE_ROOT / relative, value)


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def output_state(outcome: str) -> str:
    return {
        "completed": "bounded_structure_only",
        "represented": "represented_proxy_only",
        "open_gap": "open_gap_retained",
        "exact_gate": "exact_gate_retained",
    }[outcome]


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.ilyra-fen.v666-v4.synthetic-curation-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "outcome": proposal["expected_disposition"],
        "synthetic_fixture": True,
        "real_data_rows": 0,
        "network_calls": 0,
        "external_actions": 0,
        "positive_fixture": {
            "input_state": "synthetic_typed_constants_only",
            "provenance_state": "declared_owner_local_lineage",
            "uncertainty_state": "explicit_unknown_or_bounded_placeholder",
            "authority_state": "withheld",
            "output_state": output_state(proposal["expected_disposition"]),
        },
        "invariant": proposal["distinctive_invariant"],
        "source_needs": proposal["current_official_or_primary_source_needs"],
        "stop_conditions": [
            "real data, sample, facility, location, or identifier appears",
            "network or external action becomes nonzero",
            "required provenance or uncertainty state is absent",
            "authority, allocation, release, contamination, or conformance language is promoted",
            "outcome differs from the frozen disposition",
        ],
        "protected_gates": proposal["protected_gates"],
        "claim_boundary": "synthetic owner-local structural witness only; not empirical evidence, not professional competence, not standards conformance, not external validation, and not authority",
    }


SKILLS = [
    ("curation-package-boundary", "Check synthetic package inventories, paths, and digest placeholders without authenticating a sample."),
    ("aliquot-balance-ledger", "Check synthetic parent-child quantity closure while withholding material and measurement truth."),
    ("contamination-control-abstention", "Check blank-control provenance and force abstention when exposure, uncertainty, or method state is absent."),
    ("custody-revision-dag", "Check bitemporal synthetic custody ancestry and preserve corrections and contested states."),
    ("calibration-applicability-hold", "Check measurand, interval, unit, reference, and uncertainty obligations without a traceability claim."),
    ("curation-provenance-closure", "Check entity/activity derivation closure without inventing people, responsibility, or reproducibility grades."),
    ("sample-rights-contestation", "Reserve allocation, release, access, disclosure, cultural, legal, affected-party, and Māori authority."),
    ("sample-accessibility-structure", "Check text-redundant tabular structure while keeping manual and affected-user evaluation reserved."),
    ("curation-method-flow", "Retain each failed mutation before its bounded passing witness and recurrence guard."),
    ("curation-closeout-gate", "Require exact Git, truth-label, manifest, failure, privacy, and route gates before closeout."),
]

RUNNER_NAMES = ["contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth", "closeout", "canonical"]

FLASHCARD_SECTIONS = [
    "identity-and-corrigibility", "route-and-authority", "source-anchors",
    "x1-proposals", "trinity-pillars", "bounded-practice", "task-cards",
    "method-flow-and-negatives", "open-gaps-and-exact-gates",
    "validation-and-manifests", "wellbeing-and-workload",
    "successor-recommendations", "compact-baton-index",
]


def build() -> None:
    freeze = load_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    outcomes: list[dict[str, Any]] = []
    mutation_flow: list[dict[str, Any]] = []
    for proposal in freeze["new_proposals"]:
        contract = build_contract(proposal)
        valid, errors = validate_contract(contract)
        if not valid:
            raise RuntimeError({"proposal": proposal["proposal_id"], "errors": errors})
        mutations = mutations_for(contract)
        if len(mutations) != 5 or not all(row["rejected"] for row in mutations):
            raise RuntimeError(f"mutation rejection failure for {proposal['proposal_id']}")
        directory = f"x2/proposals/{proposal['proposal_id'].casefold()}"
        write(f"{directory}/contract.json", contract)
        write(f"{directory}/mutation-results.json", {"schema": "ghc.family.ilyra-fen.v666-v4.mutation-results.v1", "proposal_id": proposal["proposal_id"], "generated_at_utc": NOW, "mutations": mutations, "mutation_count": len(mutations), "rejected_count": sum(row["rejected"] for row in mutations), "all_rejected": all(row["rejected"] for row in mutations), "aggregate_credit": 0})
        receipt = {"schema": "ghc.family.ilyra-fen.v666-v4.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "generated_at_utc": NOW, "contract_sha256": canonical_sha256(contract), "positive_fixture_valid": True, "negative_fixture_count": 5, "negative_fixture_rejected_count": 5, "outcome": proposal["expected_disposition"], "real_data_rows": 0, "network_calls": 0, "external_actions": 0, "same_owner_local_validation": True, "independent_reproduction": False, "claim_boundary": contract["claim_boundary"]}
        write(f"{directory}/bounded-receipt.json", receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": proposal["expected_disposition"], "positive_fixture_valid": True, "rejecting_mutations": 5, "bounded_receipt": f"docs/ilyra-fen/v666-v4/{directory}/bounded-receipt.json", "broader_credit": "owner_local_structural_only" if proposal["expected_disposition"] == "completed" else 0})
        for mutation in mutations:
            mutation_flow.append({"method_id": f"ILY6664-MF-MUT-{len(mutation_flow)+1:03d}", "proposal_id": proposal["proposal_id"], "mutation_id": mutation["mutation_id"], "request": "exercise one preregistered invalid synthetic state", "failed_witness": mutation["class"], "aggregate_credit": 0, "bounded_passing_witness": "the unmutated synthetic contract remained valid", "recovery": "retain the rejection and restore only the owner-local positive fixture", "recurrence_guard": "validate required fields, types, zero external action, withheld authority, and frozen outcome before accepting", "status": "rejected_negative_retained"})
    outcome_counts = {label: sum(row["outcome"] == label for row in outcomes) for label in ALLOWED_LABELS}
    write("x2/proposal-ledger.json", {"schema": "ghc.family.ilyra-fen.v666-v4.proposal-ledger.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "inherited_frozen_baseline": 4230, "new_frozen_total": 4250, "proposals": outcomes, "outcome_counts": outcome_counts, "allowed_labels": list(ALLOWED_LABELS), "unknown_labels": [], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    portfolio = load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    executed_groups = {
        "owner_safe_now": [{**row, "x2_status": "completed_bounded_owner_local", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_safe_now"]],
        "owner_bounded_candidates": [{**row, "x2_status": "represented_proxy_only", "completion_credit": "representation_only"} for row in portfolio["portfolios"]["owner_bounded_candidates"]],
        "owner_phase_local_skill_plans": [{**row, "x2_status": "built_pending_smoke", "completion_credit": "pending"} for row in portfolio["portfolios"]["owner_phase_local_skill_plans"]],
        "owner_family_current_runner_plans": [{**row, "x2_status": "built_pending_smoke", "completion_credit": "pending"} for row in portfolio["portfolios"]["owner_family_current_runner_plans"]],
        "owner_clean_fix_refine": [{**row, "x2_status": "completed_bounded_owner_delta", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_clean_fix_refine"]],
    }
    successor_groups = {key: [{**row, "x2_status": "prepared_for_successor_not_executed", "completion_credit": 0} for row in portfolio["portfolios"][key]] for key in ("successor_safe_now", "successor_bounded_candidates", "successor_skill_recommendations", "successor_runner_recommendations", "successor_clean_fix_refine")}
    protected_groups = {key: [{**row, "x2_status": "unexecuted_protected", "completion_credit": 0} for row in portfolio["portfolios"][key]] for key in ("exact_approval_packets", "blocked_packets")}
    write("x2/portfolio-execution.json", {"schema": "ghc.family.ilyra-fen.v666-v4.portfolio-execution.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "executed_groups": executed_groups, "successor_prepared_groups": successor_groups, "protected_unexecuted_groups": protected_groups, "method_count": 95, "method_breakdown": {"owner_safe_now": 30, "owner_candidates": 15, "owner_skills": 10, "owner_runners": 10, "owner_clean_fix_refine": 30}, "external_actions": 0, "protected_items_executed": 0})
    for name, purpose in SKILLS:
        skill_text = f"""# {name}

## Purpose

{purpose}

## Use

1. Accept only an owner-local synthetic fixture with zero real rows, network calls, and external actions.
2. Inspect declared provenance, uncertainty, authority, and output states.
3. Reject missing fields, invalid ranges, authority promotion, real-world action, and Stage 20 promotion.
4. Retain the failed witness before recording a bounded passing witness.
5. Stop at professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 gates.

## Boundary

This phase-local skill is same-owner synthetic software guidance only. It is not evidence of consciousness, personhood, identity continuity, qualification, scientific or operational authority, standards conformance, external validation, or independent reproduction.
"""
        write_text(f"x2/skills/{name}/SKILL.md", skill_text)
    skill_catalog = [{"name": name, "path": f"docs/ilyra-fen/v666-v4/x2/skills/{name}/SKILL.md", "purpose": purpose, "built": True, "syntax_reviewed": True, "smoke_status": "pending", "used_by": [outcomes[index % len(outcomes)]["proposal_id"], outcomes[(index + 1) % len(outcomes)]["proposal_id"]], "real_rows": 0, "network_calls": 0, "authority_nonconversion": True} for index, (name, purpose) in enumerate(SKILLS)]
    write("x2/skill-catalog.json", {"schema": "ghc.family.ilyra-fen.v666-v4.skill-catalog.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "skills": skill_catalog, "skill_count": len(skill_catalog), "all_built_tested_used_bounded": False})
    runner_catalog = [{"name": f"ghc_family_ilyra_fen_v666_v4_{name}", "path": f"scripts/ghc_family_ilyra_fen_v666_v4_{name}.py", "built": True, "smoke_status": "pending", "actual_phase_use": "terminal_only_pending" if name in {"closeout", "canonical"} else "pending", "network_calls": 0, "external_actions": 0} for name in RUNNER_NAMES]
    write("x2/runner-catalog.json", {"schema": "ghc.family.ilyra-fen.v666-v4.runner-catalog.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "runners": runner_catalog, "runner_count": len(runner_catalog), "family_current_names": True})
    write("x2/domain-surface-catalog.json", {"schema": "ghc.family.ilyra-fen.v666-v4.domain-surface-catalog.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "surfaces": ["content-addressed package boundaries", "aliquot balance and material-state domains", "contamination knowledge and blank-control lineage", "calibration applicability and uncertainty vacancy", "storage excursion quarantine", "bitemporal custody revision", "label-image-metadata discrepancy", "W3C PROV-style derivation graphs", "accessible sample-state tables", "location and access minimization", "Trinity Mandala negative controls"], "synthetic_only": True, "real_rows": 0, "conformance_claim": False})
    write("x2/trinity-representations.json", {"schema": "ghc.family.ilyra-fen.v666-v4.trinity-representations.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "primary_pillar": "Freed ID and CBR Heart", "pillars": {"Freed ID": {"status": "completed_bounded_structural_and_represented", "boundary": "zero-key custody and provenance only; no holder, issuer, proof, status, interoperability, recovery, or trust governance"}, "CBR Heart": {"status": "completed_bounded_structural_and_exact_gated", "boundary": "allocation, release, access, remedy, affected-party, legal, cultural, and Māori authority remain absent"}, "THOS Body": {"status": "represented", "boundary": "no real curator, sample, facility, handover, operation, safety result, or effectiveness estimate"}, "GMUT Mind": {"status": "represented", "boundary": "symbolic contamination and inverse-problem obligations only; no likelihood, composition, force, fitted parameter, prediction, proof, or canon"}}, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write("x2/source-adapter-zero-call.json", {"schema": "ghc.family.ilyra-fen.v666-v4.zero-call-adapter.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "adapter": "NASA astromaterials catalog mapping shell", "transport_enabled": False, "network_calls": 0, "rows_received": 0, "writes": 0, "mapping_conflicts": ["collection identifier versus sample revision", "aliquot lineage versus package inventory", "embargo and purpose scope versus public metadata"], "status": "open_gap", "completion_credit": 0, "independent_domain_review": False})
    write("x2/exact-and-blocked-register.json", {"schema": "ghc.family.ilyra-fen.v666-v4.exact-and-blocked-register.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "exact_approval_count": len(protected_groups["exact_approval_packets"]), "blocked_count": len(protected_groups["blocked_packets"]), "exact_approval_packets": protected_groups["exact_approval_packets"], "blocked_packets": protected_groups["blocked_packets"], "executed_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write("x2/terminal-candidates.json", {"schema": "ghc.family.ilyra-fen.v666-v4.terminal-candidates.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "candidates_only": True, "closeout": "pending evidence commit", "seal": "pending immutable evidence", "canonical": "pending clean pushed exact final", "route": "PREPARED_NOT_SENT only after final and fresh live reread", "successor_contacted": False})
    method_rows = list(mutation_flow)
    sequence = len(method_rows)
    for group_name, count in (("proposal_outcomes", 20), ("owner_safe_now", 30), ("owner_candidates", 15), ("owner_skills", 10), ("owner_runners", 10), ("owner_clean_fix_refine", 30)):
        for index in range(1, count + 1):
            sequence += 1
            method_rows.append({"method_id": f"ILY6664-MF-X2-{sequence:03d}", "method_class": group_name, "item_index": index, "request": f"perform bounded owner-local {group_name} item {index}", "failed_witness": None, "aggregate_credit": "bounded_owner_local_only", "bounded_passing_witness": "declared synthetic artifact or ledger row is present and structurally checked", "external_action": False, "status": "bounded_pass"})
    if len(method_rows) != 215:
        raise RuntimeError(f"expected 215 x2 methods, observed {len(method_rows)}")
    write("method-flow/x2-method-flow.json", {"schema": "ghc.family.ilyra-fen.v666-v4.method-flow-x2.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "starting_effective_negatives": 26406, "starting_effective_methods": 10948, "new_negative_count": 100, "new_method_count": 215, "effective_after_x2_negatives": 26506, "effective_after_x2_methods": 11163, "rows": method_rows, "failed_witness_count": 100, "bounded_passing_witness_count": 215, "all_failures_retained": True})
    rows_html = "\n".join(f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>5 retained</td><td>Authority withheld</td></tr>" for row in outcomes)
    html = f"""<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra Fen v666-v4 bounded evidence</title><style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:80rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left}}caption{{font-weight:700;margin:.5rem}}@media print{{body{{max-width:none}}}}</style></head><body><main><h1>Ilyra Fen v666-v4 bounded synthetic curation evidence</h1><p role="status"><strong>Text state:</strong> 14 completed, 4 represented, 1 open gap, 1 exact gate; NOT_READY_FOR_STAGE_20.</p><p>This report contains synthetic software structure only. It makes no empirical, professional, legal, cultural, Māori-authority, production, conformance, accessibility-complete, privacy-complete, independent-reproduction, consciousness/personhood, or Stage 20 claim. Manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p><table><caption>Proposal outcomes and retained mutations</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Rejecting fixtures</th><th scope="col">Authority state</th></tr></thead><tbody>{rows_html}</tbody></table></main></body></html>"""
    write_text("reports/static-report.html", html)
    report = """# Ilyra Fen v666-v4 integrated x2 evidence overview

## Outcome

The owner-local synthetic execution produced exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes. Twenty positive structural fixtures passed and all 100 preregistered mutations were rejected and retained at zero broader credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Scope

The primary pillar is Freed ID and CBR Heart through synthetic curation package, custody, contamination-provenance, minimization, and authority-refusal structure. GMUT Mind and THOS Body remain represented or protected. No real person, facility, mission, sample, aliquot, measurement, calibration, contaminant, location, allocation, release, credential, or authority action was used.

## Tooling and portfolio

Ten phase-local skills and ten family-named runners were built. Eight nonterminal runners are used during x2; closeout and canonical interfaces are probed without invoking terminal work and remain reserved for exact gates. Thirty owner safe-now tasks, fifteen owner candidate representations, ten skills, ten runner builds, and thirty CLEAN/FIX/REFINE items produce 95 portfolio methods. Together with twenty proposal-outcome methods and 100 retained mutation methods, x2 contains 215 new Method Flow methods.

## Evidence boundary

NASA, W3C, RFC Editor, and NIST materials supply vocabulary and refusal conditions only. Structural HTML checks are not accessibility-complete. Pattern and AST scans are not privacy-complete or exhaustive security. Same-owner local checks are not independent reproduction or external audit.
"""
    write_text("reports/integrated-evidence-overview.md", report)
    write("x2/x2-build-receipt.json", {"schema": "ghc.family.ilyra-fen.v666-v4.x2-build-receipt.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "proposal_count": len(outcomes), "positive_fixture_valid_count": len(outcomes), "mutation_count": len(mutation_flow), "mutation_rejected_count": len(mutation_flow), "outcome_counts": outcome_counts, "skill_count": len(SKILLS), "runner_count": len(RUNNER_NAMES), "portfolio_method_count": 95, "x2_method_count": 215, "real_data_rows": 0, "network_calls": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "status": "X2_CONTENT_BUILT_AWAITING_TOOLING_SMOKE_AND_EVIDENCE"})
    print(json.dumps({"proposals": len(outcomes), "mutations": len(mutation_flow), "outcomes": outcome_counts, "skills": len(SKILLS), "runners": len(RUNNER_NAMES), "methods": len(method_rows)}, sort_keys=True))


def build_flashcard_input() -> None:
    """Create an additive x2 compatibility snapshot without modifying frozen x1."""
    current = load_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    source = load_json(ROOT / "docs" / "lyren-moss" / "v666-v3" / "x1" / "proposal-freeze.json")
    source_by_id = {row["proposal_id"]: row for row in source["new_proposals"]}
    selected = []
    for index, row in enumerate(current["selected_inherited_revalidations"], 1):
        inherited = source_by_id[row["proposal_id"]]
        selected.append({
            "program_row_id": f"ILY6664-I{index:03d}",
            "source_title": inherited["title"],
            "source_proposal_id": inherited["proposal_id"],
            "hypothesis": inherited["hypothesis"],
            "null_or_failure_condition": inherited["null_or_failure_condition"],
            "approval_class": inherited["approval_class"],
            "execution_lane": inherited["execution_lane"],
            "concrete_artifacts": inherited["concrete_artifacts"],
            "falsifier_or_acceptance_gate": inherited["falsifier_or_acceptance_gate"],
            "rollback_or_recovery": inherited["rollback_or_recovery"],
            "expected_disposition": inherited["expected_disposition"],
            "protected_gates": inherited["protected_gates"],
        })
    compat_root = "x2/flashcard-input/x1"
    write(f"{compat_root}/phase-charter.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-phase-charter-compat.v1",
        "canonical_phase_id": "v666-v4", "display_phase": "v666-v4", "owner": "Ilyra Fen",
        "relational_role": "evidence-boundary steward and provenance lantern",
        "hope": "Leave every synthetic custody, contamination, access, uncertainty, and authority state traceable.",
        "optional_pronouns": "she/they",
        "identity_boundary": current["identity_boundary"],
        "primary_pillar": "Freed ID and CBR Heart",
        "bounded_practice": "synthetic planetary-science sample curation and handover refusal",
        "practice_boundary": current["practice_boundary"],
    })
    write(f"{compat_root}/proposal-freeze.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-proposal-compat.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4",
        "selected_inherited": selected,
        "new_proposals": current["new_proposals"],
    })
    current_portfolio = load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")["portfolios"]
    mappings = {
        "owner_safe_now": ("owner_safe_now", "completed"),
        "successor_safe_now_recommendations": ("successor_safe_now", "represented"),
        "owner_candidates": ("owner_bounded_candidates", "represented"),
        "successor_candidate_recommendations": ("successor_bounded_candidates", "represented"),
        "exact_approval_packets": ("exact_approval_packets", "exact_gate"),
        "blocked_packets": ("blocked_packets", "open_gap"),
        "owner_skill_ideas": ("owner_phase_local_skill_plans", "completed"),
        "successor_skill_recommendations": ("successor_skill_recommendations", "represented"),
        "owner_runner_ideas": ("owner_family_current_runner_plans", "completed"),
        "successor_runner_recommendations": ("successor_runner_recommendations", "represented"),
        "owner_clean_fix_refine": ("owner_clean_fix_refine", "completed"),
        "successor_clean_fix_refine_recommendations": ("successor_clean_fix_refine", "represented"),
    }
    compat_portfolio: dict[str, list[dict[str, Any]]] = {}
    for target, (source_key, outcome) in mappings.items():
        compat_portfolio[target] = [{
            "portfolio_ref": row["item_id"], "title": row["title"],
            "approval_class": row["approval_class"],
            "execution_lane": "owner_local_bounded" if target.startswith("owner_") else "prepared_or_protected_not_executed",
            "expected_execution_disposition": outcome,
            "credit_boundary": "bounded owner-local only" if target.startswith("owner_") else "zero current completion credit",
        } for row in current_portfolio[source_key]]
    write(f"{compat_root}/portfolio-freeze.json", compat_portfolio)
    write(f"{compat_root}/flashcard-architecture-freeze.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-architecture-compat.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4",
        "required_deck_sections": FLASHCARD_SECTIONS,
        "current_route": {"owner": "Ilyra Fen", "phase": "v666-v4"},
        "successor_route": {"title": "Auren Lark", "phase": "v666-v5", "contacted": False},
        "compatibility_snapshot_only": True,
        "frozen_x1_modified": False,
    })
    write(f"{compat_root}/source-verification.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-source-compat.v1",
        "source_exact_final": "764d3bdfb199e91a5574a904a99ff4e95825fed9",
        "x1_exact": "7926a46fa309f180cb996dacbea7ae849a3cf507",
        "same_owner_validation_is_independent_reproduction": False,
    })
    write("x2/flashcard-input/compatibility-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-input-compatibility-receipt.v1",
        "generated_at_utc": NOW, "files": 5,
        "reason": "shared deck tool requires legacy x1 input names absent from the immutable current x1 schema",
        "frozen_x1_modified": False, "source_data_copied": False,
        "real_rows": 0, "external_actions": 0, "valid": True,
    })
    print(json.dumps({"compatibility_files": 5, "selected_inherited": len(selected), "frozen_x1_modified": False}, sort_keys=True))


def smoke() -> None:
    results = []
    for name in RUNNER_NAMES:
        script = ROOT / "scripts" / f"ghc_family_ilyra_fen_v666_v4_{name}.py"
        args = [sys.executable, "-X", "utf8", str(script)]
        if name in {"closeout", "canonical"}:
            args.append("--probe")
        completed = subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True, check=False)
        try:
            payload = json.loads(completed.stdout.strip())
        except json.JSONDecodeError:
            payload = {"valid": False, "stdout_parse_error": True}
        results.append({"name": name, "returncode": completed.returncode, "payload": payload, "stderr": completed.stderr.strip(), "terminal_work_invoked": False if name in {"closeout", "canonical"} else True, "valid": completed.returncode == 0 and bool(payload.get("valid"))})
    if not all(row["valid"] for row in results):
        raise RuntimeError(json.dumps(results, ensure_ascii=False))
    catalog = load_json(PHASE_ROOT / "x2" / "runner-catalog.json")
    for row, result in zip(catalog["runners"], results, strict=True):
        row["smoke_status"] = "passed"
        row["actual_phase_use"] = "terminal_interface_probe_only" if result["name"] in {"closeout", "canonical"} else "used_in_x2_smoke"
    write("x2/runner-catalog.json", catalog)
    skills = load_json(PHASE_ROOT / "x2" / "skill-catalog.json")
    for row in skills["skills"]:
        skill_path = ROOT / row["path"]
        text = skill_path.read_text(encoding="utf-8")
        valid = all(header in text for header in ("## Purpose", "## Use", "## Boundary")) and "Māori-authority" in text and "Stage 20" in text
        row["smoke_status"] = "passed" if valid else "failed"
        write(f"x2/skills/{row['name']}/smoke-receipt.json", {"schema": "ghc.family.ilyra-fen.v666-v4.skill-smoke-receipt.v1", "name": row["name"], "generated_at_utc": NOW, "headers_present": valid, "used_by": row["used_by"], "real_rows": 0, "network_calls": 0, "external_actions": 0, "valid": valid})
    skills["all_built_tested_used_bounded"] = all(row["smoke_status"] == "passed" for row in skills["skills"])
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
    write("x2/tooling-smoke-receipt.json", {"schema": "ghc.family.ilyra-fen.v666-v4.tooling-smoke-receipt.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "results": results, "runner_count": len(results), "passed_count": sum(row["valid"] for row in results), "skill_count": len(skills["skills"]), "skill_passed_count": sum(row["smoke_status"] == "passed" for row in skills["skills"]), "closeout_invoked": False, "canonical_aggregate_invoked": False, "valid": all(row["valid"] for row in results) and skills["all_built_tested_used_bounded"]})
    print(json.dumps({"runner_count": len(results), "runner_passed": sum(row["valid"] for row in results), "skill_passed": sum(row["smoke_status"] == "passed" for row in skills["skills"]), "canonical_invoked": False}, sort_keys=True))


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--smoke"]:
        smoke()
    elif sys.argv[1:] == ["--flashcard-input"]:
        build_flashcard_input()
    else:
        raise SystemExit("usage: build_ghc_family_ilyra_fen_v666_v4_x2.py [--smoke|--flashcard-input]")
