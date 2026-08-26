"""Immutable x2 evidence tests for Lyren Moss v670-v1."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.ghc_family_grain_milling_accessibility_runner import render
from scripts.ghc_family_grain_milling_contracts import (
    ContractError,
    canonical_json_bytes,
    mass_balance,
    net_mass_kg,
    validate_proposal_record,
)
from scripts.ghc_family_grain_milling_hold_runner import evaluate_hold
from scripts.ghc_family_grain_milling_sieve_runner import (
    reconcile_fractions,
    validate_sieve_stack,
)
from scripts.ghc_family_grain_milling_trace_runner import (
    validate_event_chain,
    validate_transfer_graph,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v670-v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def test_x1_head_is_the_declared_evidence_source():
    receipt = load("x2/build-receipt.json")
    assert receipt["x1_head"] == "128f52cee0acc532a114b05242d356cb7a59596c"
    assert receipt.get("canonical_invocations", 0) == 0


def test_outcomes_are_exactly_four_allowed_labels():
    ledger = load("x2/outcome-ledger.json")
    assert ledger["totals"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}
    assert Counter(row["observed_outcome"] for row in ledger["rows"]) == Counter(ledger["totals"])
    assert len(ledger["rows"]) == 40


def test_every_outcome_has_four_rejecting_mutations_and_zero_external_surface():
    rows = load("x2/outcome-ledger.json")["rows"]
    assert all(row["rejecting_mutations"] == 4 for row in rows)
    assert all(row["real_people"] == 0 for row in rows)
    assert all(row["real_grain_or_food"] == 0 for row in rows)
    assert all(row["devices_or_samples"] == 0 for row in rows)
    assert all(row["external_actions"] == 0 for row in rows)


def test_thirty_six_positive_controls_passed():
    receipt = load("x2/positive-control-receipt.json")
    assert receipt["declared"] == receipt["passed"] == 36
    assert len(receipt["rows"]) == 36
    assert all(row["accepted"] for row in receipt["rows"])
    assert receipt["broader_credit"] == 0


def test_all_160_mutations_are_retained_and_rejected():
    rows = []
    for path in sorted((BASE / "x2" / "mutations").glob("*.json")):
        shard = json.loads(path.read_text(encoding="utf-8"))
        rows.extend(shard["rows"])
    assert len(rows) == 160
    assert len({row["mutation_id"] for row in rows}) == 160
    assert all(row["rejected"] and row["completion_credit"] == 0 for row in rows)
    assert Counter(row["mutation"] for row in rows) == Counter(
        {
            "real_person_injection": 40,
            "real_grain_injection": 40,
            "external_action_injection": 40,
            "unknown_outcome_injection": 40,
        }
    )


def test_method_flow_retains_startup_inheritance_and_mutations():
    ledger = load("method-flow/evidence-ledger.json")
    assert ledger["methods_added"] == 192
    assert ledger["failed_witnesses_added"] == 192
    assert ledger["bounded_passing_witnesses_added"] == 192
    assert ledger["erased_failures"] == 0
    assert len(ledger["rows"]) == 192


def test_immutable_evidence_counts_are_additive():
    truth = load("x2/phase-truth-evidence.json")
    assert truth["effective"] == {
        "effective_negatives": 32051,
        "exact_gates": 236,
        "failed_witnesses": 3872,
        "methods": 18156,
        "open_gaps": 241,
        "passing_witnesses": 5125,
    }
    assert truth["proposal_chain"] == 5270
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_portfolio_execution_and_holds_are_exact():
    data = load("x2/portfolio-execution.json")
    for key, expected in (
        ("safe_now", 60),
        ("candidates", 30),
        ("skills", 20),
        ("runners", 10),
        ("clean_fix_refine", 60),
    ):
        assert len(data[key]) == expected
        assert all(row["x2_state"] == "completed" for row in data[key])
    assert len(data["exact_approval"]) == 20
    assert len(data["blocked"]) == 10
    assert all(row["x2_state"] == "held_unexecuted" for row in data["exact_approval"] + data["blocked"])
    assert len(data["new_tool_modules_built_tested_and_used"]) == 5


def test_skill_and_runner_records_are_built_tested_and_used():
    data = load("x2/skill-runner-evidence.json")
    assert len(data["skills"]) == 20
    assert len(data["runners"]) == 10
    assert all(row["built"] and row["tested"] and row["used"] for row in data["skills"] + data["runners"])
    assert len(data["successor_skill_ideas"]) == 10
    assert len(data["successor_runner_ideas"]) == 10


def test_net_mass_rejects_tare_above_gross():
    assert net_mass_kg(12.5, 2.5).is_finite()
    with pytest.raises(ContractError, match="tare_exceeds_gross"):
        net_mass_kg(2.5, 12.5)


def test_mass_balance_is_arithmetic_not_release():
    result = mass_balance(10.0, {"a": 4.0, "b": 6.0})
    assert result["within_fixture_tolerance"] is True
    assert result["release_authorized"] is False
    with pytest.raises(ContractError, match="negative_mass|invalid_output"):
        mass_balance(10.0, {"a": -1.0})


def test_sieve_stack_rejects_duplicate_and_reversed_apertures():
    assert validate_sieve_stack([1000, 500, 250])["accepted"] is True
    with pytest.raises(ContractError, match="duplicate_aperture"):
        validate_sieve_stack([1000, 500, 500])
    with pytest.raises(ContractError, match="apertures_not_descending"):
        validate_sieve_stack([250, 500, 1000])


def test_fraction_reconciliation_has_no_measurement_or_grade_claim():
    result = reconcile_fractions(100.0, {"coarse": 25.0, "mid": 50.0, "fine": 25.0})
    assert result["accepted"] is True
    assert result["measurement_claim"] is False
    assert result["grade_claim"] is False


def test_event_chain_rejects_duplicate_and_missing_parent():
    valid = [
        {"event_id": "a", "source_sequence": 1, "parent_event_id": None, "real_world_action": False},
        {"event_id": "b", "source_sequence": 2, "parent_event_id": "a", "real_world_action": False},
    ]
    assert validate_event_chain(valid)["append_only"] is True
    invalid = valid + [{"event_id": "b", "source_sequence": 3, "parent_event_id": "b", "real_world_action": False}]
    with pytest.raises(ContractError, match="duplicate_or_missing_event_id"):
        validate_event_chain(invalid)


def test_transfer_graph_rejects_cycles():
    assert validate_transfer_graph([("a", "b"), ("b", "c")])["acyclic"] is True
    with pytest.raises(ContractError, match="cyclic_transfer_graph"):
        validate_transfer_graph([("a", "b"), ("b", "a")])


def test_release_gate_refuses_missing_fixture_evidence():
    with pytest.raises(ContractError, match="release_gate_not_satisfied"):
        evaluate_hold(
            {
                "state": "released",
                "fixture_authority": "SYNTHETIC_TEST_ONLY",
                "evidence": {"identity_checked": True},
            }
        )
    held = evaluate_hold({"state": "held", "evidence": {}})
    assert held["real_release_authorized"] is False


def test_proposal_contract_rejects_real_surface_and_unknown_outcome():
    row = load("x1/new-proposal-freeze.json")["rows"][0]
    assert validate_proposal_record(row)["accepted"] is True
    invalid = dict(row, real_people=1)
    with pytest.raises(ContractError, match="non_synthetic_or_external_surface"):
        validate_proposal_record(invalid)
    invalid = dict(row, planned_outcome="canon")
    with pytest.raises(ContractError, match="unknown_outcome"):
        validate_proposal_record(invalid)


def test_canonical_fixture_bytes_reject_nonfinite_numbers():
    first = canonical_json_bytes({"b": 2, "a": 1})
    second = canonical_json_bytes({"a": 1, "b": 2})
    assert first == second == b'{"a":1,"b":2}\n'
    with pytest.raises(ContractError, match="nonfinite_number"):
        canonical_json_bytes({"value": float("nan")})


def test_accessible_report_is_static_and_structural():
    report = (BASE / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
    assert all(token in report for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"'))
    assert "<script" not in report.lower()
    direct = render([{"proposal_id": "fixture", "outcome": "represented", "boundary": "synthetic"}])
    assert "fixture" in direct


def test_pillar_boundaries_reserve_every_protected_claim():
    data = load("x2/pillar-boundaries.json")
    assert data["gmut"]["observations"] == data["gmut"]["fitted_parameters"] == 0
    assert data["gmut"]["theory_of_everything_claim"] is False
    assert data["freed_id"]["real_keys"] == data["freed_id"]["real_identities"] == 0
    assert data["cbr"]["maori_authority_decisions"] == 0


def test_cards_contracts_and_proposals_have_one_to_one_coverage():
    for directory in ("proposals", "contracts", "cards"):
        assert len(list((BASE / "x2" / directory).glob("*.json"))) == 40


def test_all_current_owner_json_parses():
    for path in BASE.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def test_evidence_manifest_replays_worktree_bytes():
    manifest = load("validation/evidence-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_evidence_overview_is_substantive_and_bounded():
    text = (BASE / "x2/evidence-overview.md").read_text(encoding="utf-8")
    assert len(text.split()) >= 1600
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "not the final closeout" in text
    assert "not independent reproduction" in text


def test_no_final_closeout_or_handoff_exists_at_evidence_stage():
    assert not (BASE / "closeout").exists()
    assert not (BASE / "final").exists()
    assert not (BASE / "handoffs").exists()


def test_successor_contact_remains_zero():
    truth = load("x2/phase-truth-evidence.json")
    assert truth["successor_contact_count"] == 0
    assert truth["real_world_actions"] == 0
    assert truth["canonical_validation"] == "NOT_INVOKED_AT_EVIDENCE_COMMIT"
