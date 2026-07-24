#!/usr/bin/env python3
"""Bounded deterministic runtime for Liora Venn v653-v8."""

from __future__ import annotations

from pathlib import Path

try:
    import ghc_family_v653_v2_core as base
except ModuleNotFoundError:  # package-style import from repository-root tests
    from scripts import ghc_family_v653_v2_core as base


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/liora-venn/v653-v8"
PROPOSALS_PATH = PHASE / "preregistration/proposals.json"
MUTATION_PLAN_PATH = PHASE / "validation/preregistered-mutation-plan.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

base.REPO = REPO
base.PHASE = PHASE
base.PROPOSALS_PATH = PROPOSALS_PATH
base.MUTATION_PLAN_PATH = MUTATION_PLAN_PATH
base.ALLOWED_OUTCOMES = ALLOWED_OUTCOMES

_contract_for = base.contract_for
_bounded_receipt = base.bounded_receipt


def contract_for(proposal):
    contract = _contract_for(proposal)
    contract["schema"] = "ghc.family.v653-v8.surface-contract.v1"
    return contract


def bounded_receipt(contract, results):
    receipt = _bounded_receipt(contract, results)
    receipt["schema"] = "ghc.family.v653-v8.bounded-receipt.v1"
    return receipt


base.contract_for = contract_for
base.bounded_receipt = bounded_receipt

read_json = base.read_json
proposals = base.proposals
proposal_by_slug = base.proposal_by_slug
obligations_from_title = base.obligations_from_title
mutations_for = base.mutations_for
apply_mutation = base.apply_mutation
execute_mutations = base.execute_mutations
validate_contract = base.validate_contract
evaluate_surface = base.evaluate_surface
runner_payload = base.runner_payload


if __name__ == "__main__":
    base.main()
