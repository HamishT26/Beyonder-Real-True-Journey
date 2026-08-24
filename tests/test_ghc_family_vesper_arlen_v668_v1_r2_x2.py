from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_vesper_arlen_v668_v1_r2_archive import (
    ALLOWED_OUTCOMES,
    SOURCE_FINAL,
)
from ghc_family_vesper_arlen_v668_v1_r2_controls import (
    ContractError,
    accession_envelope,
    append_correction,
    bagit_paths,
    base_envelope,
    custody_order,
    digest,
    fixity_quorum,
    mutated_envelope,
    namespace_tribunal,
    retention_decision,
    reversible_redaction,
    route_transition,
    validate_control_envelope,
    validate_flashcard_graph,
    validation_credit_transition,
)

PHASE_ROOT = ROOT / "docs" / "vesper-arlen" / "v668-v1-r2"
X1_HEAD = "be908eb829185971c10be6d100c2c85fd35871e0"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def test_x1_anchor_is_direct_child_and_has_no_x2_outcomes():
    assert subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{X1_HEAD}^"], check=True, capture_output=True, text=True).stdout.strip() == SOURCE_FINAL
    tree = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", X1_HEAD], check=True, capture_output=True, text=True).stdout.splitlines()
    assert "docs/vesper-arlen/v668-v1-r2/x2/proposals/proposal-outcomes.json" not in tree


def test_control_envelope_accepts_bounded_fixture():
    envelope = base_envelope("synthetic-001", {"value": 1})
    receipt = validate_control_envelope(envelope)
    assert receipt["state"] == "PASS_BOUNDED_CONTROL_ENVELOPE"
    assert receipt["external_actions"] == 0


@pytest.mark.parametrize("mutation", ["missing_required_field", "wrong_type", "forbidden_claim", "boundary_bypass"])
def test_control_envelope_rejects_all_preregistered_classes(mutation: str):
    envelope = base_envelope("synthetic-001", {"value": 1})
    with pytest.raises(ContractError):
        validate_control_envelope(mutated_envelope(envelope, mutation))


def test_accession_and_fixity_are_deterministic_without_authenticity_claim():
    payload = b"synthetic\n"
    accession = accession_envelope("synthetic-001", payload)
    assert accession["sha256"] == hashlib.sha256(payload).hexdigest()
    receipt = fixity_quorum(payload, {"sha256": digest(payload, "sha256"), "sha512": digest(payload, "sha512")})
    assert receipt["authenticity_proven"] is False


def test_custody_dag_rejects_cycle():
    with pytest.raises(ContractError):
        custody_order([
            {"event_id": "a", "depends_on": ["b"], "recorded_at": 1, "effective_at": 1},
            {"event_id": "b", "depends_on": ["a"], "recorded_at": 2, "effective_at": 2},
        ])


def test_correction_retains_original_entries():
    original = [{"event_id": "a", "payload": "synthetic"}]
    corrected = append_correction(original, "a", "typed reason")
    assert corrected[0] == original[0]
    assert len(corrected) == 2


def test_namespace_collision_and_bagit_escape_are_rejected():
    with pytest.raises(ContractError):
        namespace_tribunal(["Case", "case"])
    with pytest.raises(ContractError):
        bagit_paths(["data/ok", "../escape"])


def test_redaction_is_reversible_view_and_retention_stop_precedes_destroy():
    source = "synthetic note"
    receipt = reversible_redaction(source, [(0, 9)], "view-only")
    assert receipt["source_mutated"] is False
    assert receipt["source_sha256"] == hashlib.sha256(source.encode()).hexdigest()
    assert retention_decision("destroy", False, True)["destruction_authorized"] is False


def test_route_and_validation_credit_refuse_replay():
    state = route_transition("prepared_not_sent", "terminal_gate_passed")
    assert route_transition(state, "exact_title_unique") == "ready_to_send"
    credit = validation_credit_transition("not_invoked", "invoke")
    credit = validation_credit_transition(credit, "pass")
    with pytest.raises(ContractError):
        validation_credit_transition(credit, "pass")


def test_flashcard_deck_has_four_tiers_and_thirteen_sections():
    deck = load("x2/cards/deck.json")
    assert deck["card_count"] == 40
    assert deck["tiers"] == ["freed_id_anchor", "pillar", "practice", "task"]
    assert deck["minimum_sections_per_card"] >= 13
    assert validate_flashcard_graph(deck["cards"])["card_count"] == 40


def test_proposal_distribution_and_mutations_are_exact():
    outcomes = load("x2/proposals/proposal-outcomes.json")
    assert outcomes["count"] == 40
    assert Counter(outcomes["outcome_counts"]) == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert set(outcomes["outcome_counts"]) == set(ALLOWED_OUTCOMES)
    mutations = load("x2/proposals/negative-mutation-results.json")
    assert mutations["count"] == 160
    assert mutations["all_rejected"] and mutations["all_retained"]
    assert all(not row["accepted"] and row["expected_rejection_observed"] for row in mutations["mutations"])


def test_inherited_rows_and_successor_recommendations_have_zero_vesper_credit():
    inherited = load("x2/proposals/inherited-refinement-review.json")
    successor = load("x2/portfolio/successor-recommendations.json")
    assert inherited["count"] == 20 and inherited["completion_credit"] == 0 and inherited["novelty_credit"] == 0
    assert successor["completion_credit_to_vesper"] == 0 and successor["successor_contacted"] is False


def test_owner_portfolio_counts_are_exact_and_exact_blocked_remain_unexecuted():
    execution = load("x2/portfolio/owner-execution.json")
    assert execution["counts"] == {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_unexecuted": 20, "blocked_unexecuted": 10}
    assert all(row["state"] == "completed" for row in execution["safe_now"] + execution["candidates"] + execution["clean_fix_refine"])
    assert all(row["completion_credit"] == 0 for row in execution["exact_approval_packets"] + execution["blocked_packets"])


def test_thirteen_tool_corrected_composite_preserves_original_failure():
    original = load("x2/toolchain/toolchain-transaction.json")
    correction = load("x2/toolchain/toolchain-audit-correction.json")
    catalog = load("x2/toolchain/installed-tool-catalog-corrected.json")
    assert original["state"] == "QUARANTINED_AUDIT_FINDINGS"
    assert original["pip_audit"]["vulnerability_count"] == 7
    assert correction["state"] == "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_ORIGINAL_AUDIT_CREDIT"
    assert correction["python_dependency_audit_corrected"]["vulnerability_count"] == 0
    assert catalog["count"] == 13 and catalog["audit_gate_passed"] is True


def test_phase_local_skills_and_runners_exist_and_runner_smokes_passed():
    skill_catalog = load("x2/skills/skill-catalog.json")
    runner_catalog = load("x2/runners/runner-catalog.json")
    assert skill_catalog["count"] == 20
    assert runner_catalog["count"] == 10 and runner_catalog["all_pass"]
    assert all((ROOT / row["path"]).is_file() for row in skill_catalog["skills"])
    assert all((ROOT / row["path"]).is_file() for row in runner_catalog["runners"])


def test_method_flow_preserves_every_known_failure_and_mutation():
    flow = load("method-flow/x2-operational-method-flow.json")
    ledger = load("method-flow/method-flow-ledger.json")
    assert flow["failure_count"] == 22 and flow["passing_witness_count"] == 22
    assert {row["failure_id"] for row in flow["failures"]} == {f"VA6681R2-F{index:03d}" for index in range(1, 23)}
    assert ledger["effective_before_canonical"]["effective_negatives"] == 29039
    assert ledger["owner_synthetic_mutations"]["effective_negatives"] == 160


def test_accessibility_receipt_reserves_manual_and_affected_user_evaluation():
    receipt = load("x2/evidence/accessibility-structure-receipt.json")
    assert receipt["state"] == "PASS_STRUCTURAL_ONLY"
    assert receipt["manual_keyboard_reserved"] and receipt["assistive_technology_reserved"] and receipt["affected_user_evaluation_reserved"]
    assert receipt["complete_conformance"] is False


def test_phase_truth_stays_not_ready_and_successor_unsent():
    truth = load("evidence/phase-truth.json")
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["successor_contacted"] is False
    assert truth["canonical_validation_invoked"] is False


def test_global_skill_promotion_is_collision_free_validated_and_byte_equal():
    catalog = load("x2/skills/skill-catalog.json")
    receipt = load("x2/skills/global-promotion-receipt.json")
    assert catalog["global_promoted_count"] == 10 and catalog["global_promotions_complete"] is True
    assert receipt["collision_count"] == 0 and receipt["overwrite_count"] == 0
    assert receipt["quick_validation_passed"] == 10
    assert all(row["byte_parity"] and row["state"] == "completed" for row in receipt["promotions"])
