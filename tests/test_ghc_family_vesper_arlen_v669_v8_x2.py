"""Evidence-stage tests for Vesper Arlen v669-v8."""

from __future__ import annotations

import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_sourdough_contracts import (
    ALLOWED_OUTCOMES,
    allowed_state_transition,
    bakers_percentage,
    canonical_bytes,
    interval_contains,
    mutate_fixture,
    positive_fixture,
    validate_fixture,
)
from ghc_family_vesper_arlen_v669_v8_sourdough import OWNER_ROOT

OWNER = ROOT / OWNER_ROOT
X1 = OWNER / "x1"
X2 = OWNER / "x2"
TOOLS = OWNER / "tools"
VALIDATION = OWNER / "validation"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def proposal_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((X1 / "proposal-freeze-shards").glob("*.json")):
        rows.extend(read_json(path)["rows"])
    return rows


def mutation_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((X2 / "mutations").glob("*.json")):
        rows.extend(read_json(path)["rows"])
    return rows


def test_core_contract_accepts_positive_and_rejects_all_mutation_classes() -> None:
    proposal = proposal_rows()[0]
    positive = positive_fixture(proposal)
    assert validate_fixture(positive).accepted is True
    for frozen in proposal["negative_fixtures"]:
        decision = validate_fixture(mutate_fixture(positive, frozen["kind"]))
        assert decision.accepted is False
        assert decision.reasons


def test_bakers_percentage_is_fixed_fixture_arithmetic_only() -> None:
    assert bakers_percentage("750", "1000") == "75.000"
    assert bakers_percentage("0", "1000") == "0.000"
    with pytest.raises(ValueError):
        bakers_percentage("1", "0")
    with pytest.raises(ValueError):
        bakers_percentage("not-a-number", "1000")


def test_state_transition_allowlist_and_refusal() -> None:
    assert allowed_state_transition("planned", "start_mix") == "mixing"
    assert allowed_state_transition("mixing", "begin_bulk") == "bulk"
    with pytest.raises(ValueError):
        allowed_state_transition("bulk", "start_mix")


def test_interval_contract_distinguishes_boundaries() -> None:
    assert interval_contains(Decimal(18), Decimal(24), Decimal(18), closed=True)
    assert not interval_contains(Decimal(18), Decimal(24), Decimal(18), closed=False)
    assert not interval_contains(Decimal(18), Decimal(24), Decimal(30), closed=True)
    with pytest.raises(ValueError):
        interval_contains(Decimal(24), Decimal(18), Decimal(20))


def test_canonical_bytes_are_deterministic_and_reject_nonfinite() -> None:
    assert canonical_bytes({"b": 2, "a": 1}) == canonical_bytes({"a": 1, "b": 2})
    with pytest.raises(ValueError):
        canonical_bytes({"value": float("nan")})


def test_exact_outcome_distribution_and_allowlist() -> None:
    ledger = read_json(X2 / "outcome-ledger.json")
    assert ledger["totals"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert len(ledger["rows"]) == 40
    assert {row["observed_disposition"] for row in ledger["rows"]} == ALLOWED_OUTCOMES
    assert all(row["expected_disposition"] == row["observed_disposition"] for row in ledger["rows"])


def test_all_160_mutations_executed_rejected_and_zero_credit() -> None:
    rows = mutation_rows()
    assert len(rows) == 160
    assert len({row["mutation_id"] for row in rows}) == 160
    assert all(row["passed"] is True for row in rows)
    assert all(row["decision"]["accepted"] is False for row in rows)
    assert all(row["completion_credit"] == 0 for row in rows)
    assert {row["kind"] for row in rows} == {"missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"}


def test_36_positive_controls_are_bounded() -> None:
    packet = read_json(X2 / "positive-controls.json")
    assert packet["total"] == len(packet["rows"]) == 36
    assert all(row["decision"]["accepted"] is True for row in packet["rows"])
    assert all(row["external_actions"] == 0 for row in packet["rows"])


def test_proposal_contract_card_parity() -> None:
    proposals = sorted((X2 / "proposals").glob("*.json"))
    contracts = sorted((X2 / "contracts").glob("*.json"))
    cards = sorted((X2 / "cards").glob("*.json"))
    assert len(proposals) == len(contracts) == len(cards) == 40
    assert [path.name for path in proposals] == [path.name for path in contracts] == [path.name for path in cards]


def test_flashcard_deck_has_four_tiers_and_ten_paragraphs() -> None:
    deck = read_json(X2 / "flashcard-deck.json")
    assert deck["card_count"] == len(deck["rows"]) == 40
    assert deck["tier_order"] == ["relational Freed ID", "Trinity pillar", "bounded practices", "task"]
    for card in deck["rows"]:
        assert card["tier_1_freed_id"]
        assert card["tier_2_pillar"]
        assert len(card["tier_3_practices"]) == 3
        assert card["tier_4_task"]
        assert len(card["paragraphs"]) == 10


@pytest.mark.parametrize(
    ("kind", "count", "state"),
    [
        ("safe_now", 60, "completed"),
        ("candidate", 30, "completed"),
        ("exact_approval", 20, "held_unexecuted"),
        ("blocked", 10, "held_unexecuted"),
        ("skill", 20, "completed"),
        ("runner", 10, "completed"),
        ("clean_fix_refine", 60, "completed"),
    ],
)
def test_portfolio_execution_counts(kind: str, count: int, state: str) -> None:
    packet = read_json(X2 / "portfolio-execution" / f"{kind}.json")
    assert len(packet["rows"]) == count
    assert all(row["execution_state"] == state for row in packet["rows"])
    assert all(row["observed_external_actions"] == 0 for row in packet["rows"])
    expected_credit = 0 if state == "held_unexecuted" else 1
    assert all(row["completion_credit"] == expected_credit for row in packet["rows"])


def test_twenty_phase_local_skills_have_required_sections() -> None:
    paths = sorted((TOOLS / "skills").glob("*/SKILL.md"))
    assert len(paths) == 20
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\nname: " + path.parent.name + "\n")
        assert "description:" in text
        assert "## Boundary" in text
        assert "## Workflow" in text
        assert "## Evidence boundary" in text
    receipt = read_json(TOOLS / "skill-smoke-receipt.json")
    assert receipt["passed"] is True
    assert len(receipt["checks"]) == 20


def test_ten_family_current_runners_pass_smoke() -> None:
    paths = sorted(ROOT.glob("scripts/ghc_family_sourdough_*_runner.py"))
    assert len(paths) == 10
    receipt = read_json(TOOLS / "runner-smoke-receipt.json")
    assert receipt["passed"] is True
    assert len(receipt["checks"]) == 10
    assert all(row["exit_code"] == 0 for row in receipt["checks"])


def test_isolated_toolchain_hash_audit_and_smokes() -> None:
    receipt = read_json(TOOLS / "isolated-toolchain-install-receipt.json")
    assert receipt["passed"] is True
    assert receipt["root_alias"] == "D_PHASE_TOOLCHAIN_ROOT"
    assert receipt["shared_prefix_mutations"] == 0
    assert receipt["wheel_count"] == 9
    assert all(row["passed"] for row in receipt["direct_hash_checks"])
    assert receipt["pip_check"]["exit_code"] == 0
    assert receipt["pip_audit"]["exit_code"] == 0
    assert receipt["pip_audit"]["vulnerability_count"] == 0
    assert len(receipt["smokes"]) == 3
    assert all(row["passed"] for row in receipt["smokes"])


def test_bounded_bandit_receipt_preserves_entrypoint_mismatch() -> None:
    receipt = read_json(TOOLS / "bandit-high-severity-receipt.json")
    assert receipt["passed"] is True
    assert receipt["command_version"] == "bandit 1.9.4"
    assert receipt["file_count"] == 13
    assert receipt["high_severity_findings"] == 0
    assert receipt["module_entrypoint_available_in_active_python"] is False
    assert "not exhaustive security" in receipt["boundary"]


def test_method_flow_retains_failed_and_passing_witnesses() -> None:
    ledger = read_json(OWNER / "method-flow/evidence-ledger.json")
    summary = read_json(OWNER / "method-flow/evidence-summary.json")
    assert len(ledger["methods"]) == summary["new_methods"] == 180
    assert summary["retained_failed_witnesses"] == summary["bounded_passing_witnesses"] == 180
    assert all(row["failed_witness"] and row["passing_bounded_witness"] and row["preferred_method"] and row["recurrence_guard"] and row["rollback"] for row in ledger["methods"])


def test_retained_negative_and_gate_arithmetic() -> None:
    negatives = read_json(X2 / "retained-negative-register.json")
    gates = read_json(X2 / "open-exact-gate-register.json")
    assert negatives["effective_negatives"] == 31850
    assert negatives["owner_additions"] == {"x1_operational": 12, "x2_operational": 5, "synthetic_mutation_rejections": 160, "isolated_tool_rejections": 3}
    assert negatives["zero_credit_erased"] == 0
    assert gates["effective_open_gaps"] == 239
    assert gates["effective_exact_gates"] == 234
    assert len(gates["new_open_gaps"]) == len(gates["new_exact_gates"]) == 2


def test_evidence_phase_truth_is_exact_and_not_terminally_promoted() -> None:
    truth = read_json(X2 / "phase-truth-evidence.json")
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["proposal_chain"] == 5230
    assert truth["effective_negatives"] == 31850
    assert truth["methods"] == 17955
    assert truth["failed_witnesses"] == 3671
    assert truth["passing_witnesses"] == 4927
    assert truth["real_people_food_samples_measurements_or_external_actions"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["validation_state"] == "EVIDENCE_BUILT_NOT_FINAL"


def test_accessible_static_report_structure_and_reservations() -> None:
    text = (X2 / "accessible-evidence-report.html").read_text(encoding="utf-8")
    assert text.lower().count("<h1") == 1
    assert 'href="#main"' in text
    assert "<main id=\"main\">" in text
    assert "<nav aria-label=" in text
    assert "<caption>" in text
    assert 'scope="col"' in text and 'scope="row"' in text
    assert "prefers-reduced-motion" in text
    assert "Manual browser" in text
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "<script" not in text.lower()
    assert "<form" not in text.lower()


def test_evidence_build_receipt_is_clean() -> None:
    receipt = read_json(VALIDATION / "evidence-build-receipt.json")
    assert receipt["passed"] is True
    assert receipt["checks"]["mutation_rejections"] == 160
    assert receipt["checks"]["positive_controls"] == 36
    assert receipt["checks"]["privacy_candidates"] == []
    assert receipt["checks"]["python_ast_findings"] == []
    assert receipt["checks"]["runner_smokes"] == 10
    assert receipt["checks"]["skill_smokes"] == 20


def test_x1_files_are_not_modified_in_evidence_delta() -> None:
    changed = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain=v1"], check=True, capture_output=True, text=True).stdout.splitlines()
    assert not [line for line in changed if "/x1/" in line.replace("\\", "/")]


def test_no_closeout_seal_final_or_handoff_exists_yet() -> None:
    assert not [path for path in (OWNER / "closeout", OWNER / "seal", OWNER / "final", OWNER / "handoffs") if path.exists()]


def test_all_owner_json_parses_and_file_ceiling_holds() -> None:
    paths = sorted(OWNER.rglob("*.json"))
    assert len(paths) >= 170
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))
    assert sum(1 for path in OWNER.rglob("*") if path.is_file()) < 2000


def test_all_owner_documents_below_word_ceiling() -> None:
    for path in OWNER.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".html", ".txt"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000
