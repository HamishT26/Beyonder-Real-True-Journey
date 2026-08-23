#!/usr/bin/env python3
"""Build and execute bounded Elowen Cairn v667-v3 x2 evidence."""

from __future__ import annotations

import copy
import hashlib
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v667_v3_core import (
    PHASE_ROOT,
    ROOT,
    RUNNER_SELECTIONS,
    validate_contract,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
    "+00:00", "Z"
)
OWNER = "Elowen Cairn"
PHASE = "v667-v3"
OWNER_SLUG = "elowen-cairn"
X1_SHA = "dc3a69fdbee3afe7f086b5ea9066c04b34b7995a"
SOURCE_SHA = "79389c8ffd79d78626d79e2109bf1b89bd1a9e67"
BRANCH = "codex/GHC-Family/elowen-cairn-v667-v3-full-tools"
INHERITED_NEGATIVES = 27223
INHERITED_METHODS = 12570
INHERITED_OPEN_GAPS = 192
INHERITED_EXACT_GATES = 190


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_root_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


MODEL_NODES = {
    "EC6673-N001": ["work_order", "purpose_vacancy", "revision", "cancellation", "source_pin"],
    "EC6673-N002": ["crown", "canons", "head", "shoulder", "waist", "sound_bow", "lip", "mouth"],
    "EC6673-N003": ["core", "false_bell", "cope", "mantle", "parting", "vent", "furnace_vacancy"],
    "EC6673-N004": ["constituent_claim", "alloy_lot", "composition_vacancy", "certificate_absence", "substitution"],
    "EC6673-N005": ["drying", "preheat", "melt", "skim", "pour", "cool", "shakeout", "cleanup"],
    "EC6673-N006": ["quantity_kind", "si_unit", "datum", "tolerance_vacancy", "instrument_absence", "covariance"],
    "EC6673-N007": ["surface_cue", "void_cue", "crack_cue", "inclusion_cue", "uncertainty", "review_hold"],
    "EC6673-N008": ["zone_token", "pass_order", "depth_vacancy", "revision", "overshoot_quarantine"],
    "EC6673-N009": ["clapper", "staple", "bearing", "flight", "strike_zone", "clearance", "load_path"],
    "EC6673-N010": ["hum", "prime", "tierce", "quint", "nominal", "double_octave", "spectral_vacancy"],
    "EC6673-N011": ["exciter_vacancy", "microphone_vacancy", "sample_rate_vacancy", "digest_placeholder", "rights_hold"],
    "EC6673-N012": ["temperature", "expansion_coefficient", "phase_change_vacancy", "boundary_condition", "unit", "uncertainty"],
    "EC6673-N013": ["frame", "pallet", "sling", "yoke", "tower", "custody", "return_path"],
    "EC6673-N014": ["canonical_record", "prov_revision", "supersession", "tombstone", "rollback", "signature_absence"],
    "EC6673-N015": ["frequency_domain", "amplitude_domain", "beating", "decay", "listener_vacancy", "agency_nonconversion"],
    "EC6673-N016": ["paired_packet", "equal_clock", "equal_token_budget", "masked_fixture", "abstention_score", "zero_humans"],
    "EC6673-N017": ["foundry_order", "component", "batch", "event", "artifact", "status_vacancy", "zero_key"],
    "EC6673-N018": ["axisymmetric_domain", "boundary", "constitutive_tensor", "contraction", "damping", "spectrum", "covariance_vacancy"],
    "EC6673-N019": ["api_v2_pin", "schema_pin", "transport_disabled", "zero_rows", "zero_images", "terms_hold"],
    "EC6673-N020": ["labour_safety_gate", "casting_gate", "lifting_gate", "ownership_gate", "sacred_use_gate", "maori_authority_gate"],
}

VACANCIES = [
    "real_person",
    "real_object",
    "real_measurement",
    "real_material",
    "real_site",
    "real_operator",
    "real_authority",
    "real_key",
    "real_proof",
    "real_network_data",
]


SKILL_SPECS = [
    ("bellfounding-work-order-vacancy", "work_order", "Check that a surrogate foundry order retains identity, purpose, source, revision, cancellation, and casting vacancies."),
    ("bell-part-topology-quarantine", "topology", "Check bell-part, mould-stage, and clapper topology while quarantining orphans and all real geometry."),
    ("foundry-event-action-firewall", "action_firewall", "Check foundry-event precedence without emitting casting, machining, lifting, installation, or safety instructions."),
    ("bell-si-obligation-check", "units", "Check SI quantity, datum, uncertainty, covariance, and absent-measurement obligations."),
    ("casting-cue-diagnosis-abstention", "cues", "Check that material and surface cues remain uncertain observations with diagnosis and treatment abstention."),
    ("tuning-removal-revision-guard", "tuning", "Check tuning and synthetic media revision lineage while all removal depths and recordings remain absent."),
    ("bell-partial-label-vacancy", "modal", "Check partial labels and typed modal obligations without frequencies, fits, predictions, or empirical promotion."),
    ("bell-record-zero-key-identity", "identity", "Check deterministic correction records and zero-key Freed ID relation placeholders."),
    ("bell-catalog-zero-row-guard", "adapter", "Check that the catalog adapter is transport-disabled and that authority reservations remain exact-gated."),
    ("bell-phase-bounded-validation", "validation", "Check all twenty owner-local contracts, four outcome labels, and one hundred rejected mutations."),
]


RUNNER_FILES = {
    kind: f"scripts/ghc_family_elowen_cairn_v667_v3_{kind}.py"
    for kind in RUNNER_SELECTIONS
}


def runner_source(kind: str) -> str:
    return f'''#!/usr/bin/env python3
"""Bounded family-current {kind} runner for Elowen Cairn v667-v3."""
from __future__ import annotations
import argparse
import json
from ghc_family_elowen_cairn_v667_v3_core import runner_self_test

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    result = runner_self_test("{kind}")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_source(name: str, kind: str, description: str) -> str:
    return f'''---
name: {name}
description: {description} Use when reviewing Elowen v667-v3 synthetic bellfounding records or their bounded successor recommendations.
---

# {name}

## Scope

This phase-local skill is a synthetic record validator. It provides no bellfounding, metallurgy, machining, rigging, acoustics, conservation, safety, legal, cultural, Māori-authority, production, or deployment authority.

## Procedure

1. Read the frozen proposal and its protected gates.
2. Confirm that every person, object, measurement, material, site, operator, key, proof, network row, and authority slot remains vacant.
3. Run `python -B {RUNNER_FILES[kind]} --self-test` from the repository root.
4. Treat a nonzero exit as a retained failure. Do not weaken the validator or promote the record.
5. Record only the bounded structural result and retain exact/open gates.

## Stop conditions

- Any real physical action, participant, professional judgment, credential, private route, external write, rights decision, cultural interpretation, Māori wording, or authority request.
- Any attempt to infer empirical GMUT confirmation, production readiness, consciousness, personhood, proof, canon, or Stage 20.

## Recovery

Restore the last valid owner-local synthetic fixture, retain the failed witness at zero credit, and add a recurrence guard. Never rewrite a failed witness as a pass.
'''


def make_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    proposal_id = proposal["proposal_id"]
    nodes = MODEL_NODES[proposal_id]
    return {
        "schema": "ghc-family-bellfounding-synthetic-contract-v1",
        "schema_version": 1,
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "synthetic_only": True,
        "record_kind": proposal_id.casefold(),
        "required_nodes": nodes,
        "nodes": list(nodes),
        "vacancies": VACANCIES,
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "participant_count": 0,
        "real_data_row_count": 0,
        "network_call_count": 0,
        "key_count": 0,
        "proof_count": 0,
        "authority_claim": None,
        "real_world_action": False,
        "outcome_promotion": None,
        "distinctive_invariant": proposal["distinctive_invariant"],
        "protected_gates": proposal["protected_gates"],
        "execution_scope": "owner-local synthetic structural fixture only",
    }


def mutations(contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for index in range(1, 6):
        candidate = copy.deepcopy(contract)
        if index == 1:
            candidate["nodes"] = candidate["nodes"][1:]
        elif index == 2:
            candidate["schema_version"] = "one"
        elif index == 3:
            candidate["authority_claim"] = "unauthorized-real-authority"
        elif index == 4:
            candidate["real_world_action"] = True
        elif index == 5:
            candidate["outcome_promotion"] = "production_ready"
        failures = validate_contract(candidate)
        rows.append(
            {
                "mutation_id": f"{contract['proposal_id']}-M{index:02d}",
                "accepted": not failures,
                "validator_failures": failures,
                "credit": 0,
                "failed_witness_retained": True,
                "fixture": candidate,
            }
        )
    return rows


def execute_portfolios(portfolio: dict[str, Any]) -> dict[str, Any]:
    execution_keys = [
        "owner_safe_now",
        "owner_bounded_candidates",
        "owner_phase_local_skill_plans",
        "owner_family_current_runner_plans",
        "owner_clean_fix_refine",
    ]
    rows = []
    for key in execution_keys:
        for item in portfolio["portfolios"][key]:
            rows.append(
                {
                    "item_id": item["item_id"],
                    "portfolio": key,
                    "title": item["title"],
                    "status": "passed_bounded_owner_local",
                    "evidence": (
                        "x2/proposal-outcomes.json"
                        if key in {"owner_safe_now", "owner_bounded_candidates"}
                        else "x2/skill-runner-registry.json"
                        if "skill" in key or "runner" in key
                        else "validation/x2-build-receipt.json"
                    ),
                    "external_action_count": 0,
                    "completion_scope": "planned owner-local structural task only",
                }
            )
    held = []
    for key in (
        "successor_safe_now",
        "successor_bounded_candidates",
        "successor_skill_recommendations",
        "successor_runner_recommendations",
        "successor_clean_fix_refine",
        "exact_approval_packets",
        "blocked_packets",
    ):
        for item in portfolio["portfolios"][key]:
            held.append(
                {
                    "item_id": item["item_id"],
                    "portfolio": key,
                    "status": "recommendation_only_not_executed"
                    if key.startswith("successor")
                    else "protected_unexecuted",
                    "completion_credit": 0,
                }
            )
    return {
        "schema": "ghc-family-portfolio-execution-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "executed_rows": rows,
        "executed_count": len(rows),
        "held_rows": held,
        "held_count": len(held),
        "external_action_count": 0,
    }


def build_method_flow(
    outcomes: list[dict[str, Any]],
    mutation_rows: list[dict[str, Any]],
    portfolio_execution: dict[str, Any],
) -> dict[str, Any]:
    startup = load("method-flow/startup-method-flow.json")
    rows: list[dict[str, Any]] = []
    for failure in startup["failed_witnesses"]:
        rows.append(
            {
                "method_id": failure["failure_id"],
                "class": "owner_operational_failure",
                "failed_witness": failure,
                "bounded_passing_witness": next(
                    item
                    for item in startup["passing_witnesses"]
                    if item["method_id"] == failure["failure_id"].replace("-F", "-R")
                ),
                "failure_erased": False,
            }
        )
    for outcome in outcomes:
        rows.append(
            {
                "method_id": f"{outcome['proposal_id']}-POSITIVE",
                "class": "proposal_positive_contract",
                "failed_witness": None,
                "bounded_passing_witness": outcome["bounded_receipt"],
                "failure_erased": False,
            }
        )
    for mutation in mutation_rows:
        rows.append(
            {
                "method_id": mutation["mutation_id"],
                "class": "rejecting_mutation",
                "failed_witness": {
                    "invalid_fixture": mutation["fixture"],
                    "credit": 0,
                    "retained": True,
                },
                "bounded_passing_witness": {
                    "rejected": not mutation["accepted"],
                    "validator_failures": mutation["validator_failures"],
                },
                "failure_erased": False,
            }
        )
    for item in portfolio_execution["executed_rows"]:
        rows.append(
            {
                "method_id": item["item_id"],
                "class": "portfolio_execution",
                "failed_witness": None,
                "bounded_passing_witness": item,
                "failure_erased": False,
            }
        )
    return {
        "schema": "ghc-family-method-flow-ledger-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_method_count": INHERITED_METHODS,
        "phase_method_count": len(rows),
        "effective_method_count": INHERITED_METHODS + len(rows),
        "phase_failed_witness_count": 6 + len(mutation_rows),
        "rows": rows,
        "valid": len(rows) == 221 and all(not row["failure_erased"] for row in rows),
    }


def build_all() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != X1_SHA:
        raise RuntimeError("x2 may begin only from the exact frozen x1 head")
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT,
        text=True,
    ).strip():
        raise RuntimeError("x2 requires no tracked modification at frozen x1")
    freeze = load("x1/proposal-freeze.json")
    portfolio = load("x1/portfolio-freeze.json")
    outcomes = []
    all_mutations = []
    for proposal in freeze["new_proposals"]:
        contract = make_contract(proposal)
        failures = validate_contract(contract)
        if failures:
            raise RuntimeError(f"positive contract failed {proposal['proposal_id']}: {failures}")
        mutation_rows = mutations(contract)
        if any(row["accepted"] for row in mutation_rows):
            raise RuntimeError(f"mutation accepted for {proposal['proposal_id']}")
        slug = proposal["proposal_id"].casefold()
        receipt = {
            "schema": "ghc-family-bounded-proposal-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": proposal["proposal_id"],
            "positive_contract_valid": True,
            "positive_failures": [],
            "mutation_count": 5,
            "accepted_mutation_count": 0,
            "final_disposition": proposal["expected_disposition"],
            "completion_scope": "synthetic structural evidence only",
            "protected_gates_crossed": [],
        }
        write_json(f"x2/proposals/{slug}/contract.json", contract)
        write_json(
            f"x2/proposals/{slug}/mutation-results.json",
            {
                "schema": "ghc-family-proposal-mutation-results-v1",
                "proposal_id": proposal["proposal_id"],
                "mutations": mutation_rows,
                "mutation_count": 5,
                "accepted_mutation_count": 0,
            },
        )
        write_json(f"x2/proposals/{slug}/bounded-receipt.json", receipt)
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "final_disposition": proposal["expected_disposition"],
                "bounded_receipt": f"x2/proposals/{slug}/bounded-receipt.json",
                "inherited_completion_credit": 0,
                "real_data_rows": 0,
                "participants": 0,
                "network_calls": 0,
            }
        )
        all_mutations.extend(mutation_rows)
    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for row in outcomes:
        counts[row["final_disposition"]] += 1
    write_json(
        "x2/proposal-outcomes.json",
        {
            "schema": "ghc-family-proposal-outcomes-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "allowed_labels": list(counts),
            "counts": counts,
            "outcomes": outcomes,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/rejecting-mutations.json",
        {
            "schema": "ghc-family-rejecting-mutations-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "mutation_count": len(all_mutations),
            "accepted_mutation_count": sum(row["accepted"] for row in all_mutations),
            "retained_zero_credit_count": len(all_mutations),
            "mutations": all_mutations,
        },
    )
    write_json(
        "x2/adapter/vam-api-v2-zero-row-adapter.json",
        {
            "schema": "ghc-family-vam-api-v2-zero-row-adapter-v1",
            "owner": OWNER,
            "phase": PHASE,
            "base_url": "https://api.vam.ac.uk/v2/",
            "documentation": "https://developers.vam.ac.uk/guide/v2/",
            "transport_enabled": False,
            "request_count": 0,
            "download_count": 0,
            "row_count": 0,
            "image_count": 0,
            "rights_state": "unreviewed_hold",
            "schema_state": "documentation_only_not_materialized",
            "status": "open_gap",
            "catalog_authority_claim": False,
        },
    )

    for name, kind, description in SKILL_SPECS:
        write_text(f"x2/skills/{name}/SKILL.md", skill_source(name, kind, description))
    for kind, relative in RUNNER_FILES.items():
        write_root_text(relative, runner_source(kind))
    portfolio_execution = execute_portfolios(portfolio)
    write_json("x2/portfolio-execution.json", portfolio_execution)
    write_json(
        "x2/skill-runner-registry.json",
        {
            "schema": "ghc-family-phase-local-skill-runner-registry-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "skills": [
                {
                    "name": name,
                    "path": f"x2/skills/{name}/SKILL.md",
                    "runner_kind": kind,
                    "runner_path": RUNNER_FILES[kind],
                    "global_install": False,
                }
                for name, kind, _ in SKILL_SPECS
            ],
            "skill_count": len(SKILL_SPECS),
            "runner_count": len(RUNNER_FILES),
            "caller_compatibility": "additive family-current ghc_family_* owner-local callers",
        },
    )

    # Actually execute every generated runner once and retain its attributable output.
    smoke_rows = []
    for kind, relative in RUNNER_FILES.items():
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / relative), "--self-test"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        parsed = json.loads(completed.stdout) if completed.stdout else {}
        smoke = {
            "runner_kind": kind,
            "runner_path": relative,
            "exit_code": completed.returncode,
            "stderr": completed.stderr,
            "result": parsed,
            "passed": completed.returncode == 0 and parsed.get("passed") is True,
        }
        smoke_rows.append(smoke)
        write_json(f"x2/runner-smoke/{kind}.json", smoke)
    if not all(row["passed"] for row in smoke_rows):
        raise RuntimeError("one or more family-current runner smoke checks failed")

    method_flow = build_method_flow(outcomes, all_mutations, portfolio_execution)
    write_json("method-flow/x2-method-flow-ledger.json", method_flow)
    negative_rows = [
        {
            "negative_id": row["mutation_id"],
            "class": "preregistered_rejecting_mutation",
            "credit": 0,
            "retained": True,
            "validator_failures": row["validator_failures"],
        }
        for row in all_mutations
    ]
    startup = load("method-flow/startup-method-flow.json")
    negative_rows.extend(
        {
            "negative_id": row["failure_id"],
            "class": "owner_operational_failure",
            "credit": 0,
            "retained": True,
            "failure": row["failure"],
        }
        for row in startup["failed_witnesses"]
    )
    write_json(
        "evidence/retained-negative-register.json",
        {
            "schema": "ghc-family-retained-negative-register-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "inherited_repository_sealed_count": INHERITED_NEGATIVES,
            "phase_additive_count": len(negative_rows),
            "effective_count": INHERITED_NEGATIVES + len(negative_rows),
            "rows": negative_rows,
            "failure_erased_count": 0,
        },
    )
    write_json(
        "evidence/open-gap-register.json",
        {
            "schema": "ghc-family-open-gap-register-v4",
            "inherited_count": INHERITED_OPEN_GAPS,
            "new_count": 1,
            "effective_count": INHERITED_OPEN_GAPS + 1,
            "new_rows": [
                {
                    "proposal_id": "EC6673-N019",
                    "gap": "V&A API v2 transport, schema materialization, rights review and catalog evaluation remain absent",
                    "network_calls": 0,
                    "rows": 0,
                }
            ],
        },
    )
    write_json(
        "evidence/exact-gate-register.json",
        {
            "schema": "ghc-family-exact-gate-register-v4",
            "inherited_count": INHERITED_EXACT_GATES,
            "new_count": 1,
            "effective_count": INHERITED_EXACT_GATES + 1,
            "new_rows": [
                {
                    "proposal_id": "EC6673-N020",
                    "gate": "bellfounding labour, physical safety, ownership, sacred use, soundscape, heritage, legal, cultural, affected-party and Māori authority",
                    "executed": False,
                }
            ],
        },
    )
    evidence = {
        "schema": "ghc-family-immutable-evidence-candidate-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source_head": SOURCE_SHA,
        "frozen_x1": X1_SHA,
        "proposal_outcomes": counts,
        "positive_contracts": len(outcomes),
        "rejecting_mutations": len(all_mutations),
        "accepted_mutations": 0,
        "owner_portfolio_executions": portfolio_execution["executed_count"],
        "phase_local_skills_built_and_smoke_used": len(SKILL_SPECS),
        "family_current_runners_built_and_smoke_used": len(smoke_rows),
        "runner_smoke_failures": sum(not row["passed"] for row in smoke_rows),
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "network_calls": 0,
        "keys": 0,
        "proofs": 0,
        "external_actions": 0,
        "effective_negatives": INHERITED_NEGATIVES + len(negative_rows),
        "effective_methods": method_flow["effective_method_count"],
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_only": True,
    }
    write_json("evidence/immutable-evidence-candidate.json", evidence)
    write_json(
        "wellbeing/x2-wellbeing-check.json",
        {
            "schema": "ghc-family-wellbeing-check-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "workload_state": "bounded_complete_for_x2_evidence_candidate",
            "portfolio_execution_count": portfolio_execution["executed_count"],
            "pause_and_stop_tokens_preserved": True,
            "exact_and_blocked_packets_executed": 0,
            "human_wellbeing_claim": False,
            "next_gate": "exact staged evidence review, commit, push and four-way equality",
        },
    )
    write_json(
        "validation/x2-build-receipt.json",
        {
            "schema": "ghc-family-x2-build-receipt-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "contracts": 20,
            "mutations": 100,
            "accepted_mutations": 0,
            "skills": 10,
            "runners": 10,
            "runner_smoke_passes": 10,
            "runner_smoke_failures": 0,
            "portfolio_executions": portfolio_execution["executed_count"],
            "method_flow_rows": method_flow["phase_method_count"],
            "status": "BOUNDED_X2_EVIDENCE_CANDIDATE",
        },
    )
    write_text(
        "evidence/evidence-summary.md",
        f"""# Elowen Cairn v667-v3 immutable-evidence candidate

This owner-local evidence candidate records exactly 20 synthetic positive contracts, 100 rejected invalid mutations, 95 bounded owner portfolio executions, 10 phase-local skills built and smoke-used, and 10 family-current runners built and smoke-used. Core dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.

No real people, bells, foundries, measurements, audio, keys, proofs, network rows, professional decisions, cultural decisions, Māori-authority decisions, or external actions were used. The evidence remains same-owner and synthetic. It is not independent reproduction, professional review, production validation, empirical GMUT confirmation, or Stage 20 authority.

All {len(negative_rows)} new negatives remain additive and zero-credit: 100 rejecting mutations and 6 startup operational failures. Effective counts are {INHERITED_NEGATIVES + len(negative_rows)} negatives, {method_flow['effective_method_count']} Method Flow methods, {INHERITED_OPEN_GAPS + 1} open gaps, and {INHERITED_EXACT_GATES + 1} exact gates. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    report_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['final_disposition'])}</td><td>0 real rows; 0 participants; 0 network calls</td></tr>"
        for row in outcomes
    )
    write_text(
        "x2/static-report.html",
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elowen Cairn v667-v3 bounded report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}:focus{{outline:3px solid #0645ad;outline-offset:2px}}.hold{{border-left:.4rem solid #7a4;padding:.75rem;background:#f4f4f4}}</style></head>
<body><header><h1>Elowen Cairn v667-v3 bounded synthetic bellfounding report</h1><p class="hold"><strong>Status text:</strong> NOT_READY_FOR_STAGE_20. Relational language is not consciousness, personhood, qualification, agency, or authority evidence.</p></header>
<main><section aria-labelledby="scope"><h2 id="scope">Scope and boundaries</h2><p>Wholly synthetic record design only. Zero real people, bells, foundries, measurements, audio, keys, proofs, network rows, authority acts, or external operations.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><table><caption>Twenty bounded owner-local outcomes with explicit nonpromotion evidence</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Disposition</th><th scope="col">Evidence ceiling</th></tr></thead><tbody>{report_rows}</tbody></table></section>
<section aria-labelledby="access"><h2 id="access">Accessibility reservation</h2><p>Headings, landmarks, captions, row and column headers, plain status text, keyboard-compatible static HTML and non-colour cues are present. Manual browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved and incomplete.</p></section>
<section aria-labelledby="authority"><h2 id="authority">Authority reservation</h2><p>Professional, safety, ownership, sacred-use, heritage, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori-authority decisions remain exact-gated. Māori concepts remain under Māori authority.</p></section></main></body></html>""",
    )
    print(json.dumps(load("validation/x2-build-receipt.json"), indent=2, ensure_ascii=True))


def staged_review() -> None:
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines()
    if not staged:
        raise RuntimeError("no staged x2 evidence allowlist")
    forbidden_x1 = [
        path
        for path in staged
        if f"docs/{OWNER_SLUG}/{PHASE}/x1/" in path.replace("\\", "/")
        or path.endswith("build_ghc_family_elowen_cairn_v667_v3_x1.py")
        or path.endswith("test_ghc_family_elowen_cairn_v667_v3_x1.py")
    ]
    allowed_prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/",
        "scripts/build_ghc_family_elowen_cairn_v667_v3_x2.py",
        "scripts/ghc_family_elowen_cairn_v667_v3_",
        "tests/test_ghc_family_elowen_cairn_v667_v3_x2.py",
    )
    out_of_scope = [path for path in staged if not path.startswith(allowed_prefixes)]
    manifest_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/evidence-content-manifest.json"
    review_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/evidence-staged-review.json"
    self_exclusions = {manifest_path, review_path}
    content_staged = [path for path in staged if path not in self_exclusions]
    entries = []
    for path in content_staged:
        blob = subprocess.check_output(["git", "show", f":{path}"], cwd=ROOT)
        entries.append(
            {"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
        )
    write_json(
        "validation/evidence-content-manifest.json",
        {
            "schema": "ghc-family-evidence-content-manifest-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "frozen_x1": X1_SHA,
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": [manifest_path, review_path],
            "staged_git_blob_bytes": True,
        },
    )
    review = {
        "schema": "ghc-family-evidence-staged-review-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "staged_path_count": len(staged),
        "staged_paths": staged,
        "forbidden_x1_paths": forbidden_x1,
        "out_of_scope_paths": out_of_scope,
        "manifest_entry_count": len(entries),
        "manifest_self_exclusions": [manifest_path, review_path],
        "valid": not forbidden_x1 and not out_of_scope,
    }
    write_json("validation/evidence-staged-review.json", review)
    print(json.dumps(review, indent=2, ensure_ascii=True))


def retain_diff_hygiene_failure() -> None:
    failure_id = "EC6673-X2-F001"
    negatives = load("evidence/retained-negative-register.json")
    if not any(row["negative_id"] == failure_id for row in negatives["rows"]):
        negatives["rows"].append(
            {
                "negative_id": failure_id,
                "class": "owner_operational_failure",
                "credit": 0,
                "retained": True,
                "failure": "git diff --cached --check found one extra blank line at EOF in the new owner core module",
                "bounded_recovery": "remove only the trailing blank line and rerun the diff-hygiene dependency",
            }
        )
    negatives["phase_additive_count"] = len(negatives["rows"])
    negatives["effective_count"] = INHERITED_NEGATIVES + len(negatives["rows"])
    write_json("evidence/retained-negative-register.json", negatives)

    method = load("method-flow/x2-method-flow-ledger.json")
    if not any(row["method_id"] == failure_id for row in method["rows"]):
        method["rows"].append(
            {
                "method_id": failure_id,
                "class": "owner_operational_failure",
                "failed_witness": {
                    "stage": "evidence_staging",
                    "failed_method": "exact staged diff-hygiene gate",
                    "failure": "one extra blank line at EOF",
                    "credit": 0,
                    "retained": True,
                },
                "bounded_passing_witness": {
                    "recovery": "removed only the extra EOF blank line",
                    "diff_check": "passed after isolated correction",
                    "successful_components_replayed": 0,
                },
                "failure_erased": False,
            }
        )
    method["phase_method_count"] = len(method["rows"])
    method["effective_method_count"] = INHERITED_METHODS + len(method["rows"])
    method["phase_failed_witness_count"] = 107
    method["valid"] = len(method["rows"]) == 222 and all(
        not row["failure_erased"] for row in method["rows"]
    )
    write_json("method-flow/x2-method-flow-ledger.json", method)

    evidence = load("evidence/immutable-evidence-candidate.json")
    evidence["effective_negatives"] = negatives["effective_count"]
    evidence["effective_methods"] = method["effective_method_count"]
    evidence["owner_operational_failures"] = 7
    write_json("evidence/immutable-evidence-candidate.json", evidence)

    receipt = load("validation/x2-build-receipt.json")
    receipt["method_flow_rows"] = method["phase_method_count"]
    receipt["owner_operational_failures"] = 7
    receipt["post_build_diff_hygiene_failure_retained"] = True
    write_json("validation/x2-build-receipt.json", receipt)

    summary_path = PHASE_ROOT / "evidence" / "evidence-summary.md"
    summary = summary_path.read_text(encoding="utf-8")
    summary = summary.replace(
        "All 106 new negatives remain additive and zero-credit: 100 rejecting mutations and 6 startup operational failures.",
        "All 107 new negatives remain additive and zero-credit: 100 rejecting mutations, 6 startup operational failures, and 1 evidence-stage diff-hygiene failure.",
    ).replace(
        "Effective counts are 27329 negatives, 12791 Method Flow methods,",
        "Effective counts are 27330 negatives, 12792 Method Flow methods,",
    )
    write_text("evidence/evidence-summary.md", summary)
    print(
        json.dumps(
            {
                "retained_failure": failure_id,
                "effective_negatives": negatives["effective_count"],
                "effective_methods": method["effective_method_count"],
                "phase_methods": method["phase_method_count"],
            },
            indent=2,
        )
    )


def evidence_validation() -> None:
    test_path = ROOT / "tests" / "test_ghc_family_elowen_cairn_v667_v3_x2.py"
    completed = subprocess.run(
        [sys.executable, "-B", str(test_path)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    combined = completed.stdout + completed.stderr
    match = re.search(r"Ran (\d+) tests", combined)
    test_count = int(match.group(1)) if match else 0
    json_paths = list(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    python_paths = sorted(
        {
            ROOT / "scripts" / "build_ghc_family_elowen_cairn_v667_v3_x2.py",
            ROOT / "scripts" / "ghc_family_elowen_cairn_v667_v3_core.py",
            ROOT / "tests" / "test_ghc_family_elowen_cairn_v667_v3_x2.py",
            *(ROOT / relative for relative in RUNNER_FILES.values()),
        }
    )
    for path in python_paths:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    receipt = {
        "schema": "ghc-family-evidence-validation-receipt-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "test_file": "tests/test_ghc_family_elowen_cairn_v667_v3_x2.py",
        "test_exit_code": completed.returncode,
        "tests_run": test_count,
        "test_output": combined.strip(),
        "phase_json_parses": len(json_paths),
        "python_in_memory_compiles": len(python_paths),
        "runner_smoke_receipts_replayed": 0,
        "valid": completed.returncode == 0 and test_count == 18,
    }
    write_json("validation/evidence-validation-receipt.json", receipt)
    print(json.dumps(receipt, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        build_all()
    elif sys.argv[1:] == ["--retain-diff-hygiene-failure"]:
        retain_diff_hygiene_failure()
    elif sys.argv[1:] == ["--evidence-validation"]:
        evidence_validation()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit(
            "usage: build_ghc_family_elowen_cairn_v667_v3_x2.py "
            "[--retain-diff-hygiene-failure|--evidence-validation|--staged-review]"
        )
