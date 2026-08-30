from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.ghc_family_sylven_arc_v676_v7_r2_core import (
    LABELS,
    privacy_candidates,
    validate_contract,
    validate_flashcard,
)


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v676-v7-r2"
X1 = ROOT / "x1"
X2 = ROOT / "x2"
SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
X1_HEAD = "82c5a8a45af8abcb17df5c793853be6fdc97c8ee"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase_truth_is_owner_scoped_and_not_stage20() -> None:
    truth = load(X2 / "phase-truth.json")
    assert truth["owner"] == "Sylven Arc"
    assert truth["phase"] == "v676-v7-r2"
    assert truth["source"] == SOURCE
    assert truth["x1"] == X1_HEAD
    assert truth["lifecycle_state"] == "X2_EVIDENCE_PRECOMMIT"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_world_rows"] == 0
    assert truth["external_real_world_actions"] == 0


def test_sixty_new_outcomes_use_only_four_labels() -> None:
    values = load(X2 / "proposal-outcomes.json")
    assert len(values["outcomes"]) == 60
    assert values["counts"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert {row["outcome"] for row in values["outcomes"]} <= LABELS
    assert all(row["real_world_rows"] == 0 and row["external_actions"] == 0 for row in values["outcomes"])


def test_sixty_contracts_are_structurally_valid_zero_row_fixtures() -> None:
    paths = sorted((X2 / "contracts").glob("SA6767R2-N*.json"))
    assert len(paths) == 60
    for path in paths:
        value = load(path)
        assert validate_contract(value) == []
        assert value["real_world_rows"] == 0
        assert value["external_actions"] == 0


def test_each_contract_has_one_bounded_receipt() -> None:
    contracts = {path.stem for path in (X2 / "contracts").glob("*.json")}
    receipts = sorted((X2 / "evidence").glob("*-receipt.json"))
    assert len(receipts) == 60
    assert {path.name.removesuffix("-receipt.json") for path in receipts} == contracts
    assert all(load(path)["structural_contract_passed"] is True for path in receipts)
    assert all(load(path)["real_world_execution_credit"] == 0 for path in receipts)
    assert all(load(path)["independent_reproduction"] is False for path in receipts)


def test_four_mutations_per_new_proposal_are_rejected_and_retained() -> None:
    ledger = load(X2 / "mutation-ledger.json")
    assert ledger["mutation_count"] == 240
    assert ledger["accepted"] == 0
    assert ledger["rejected"] == 240
    assert len(ledger["rows"]) == 240
    assert all(row["accepted"] is False and row["errors"] for row in ledger["rows"])


def test_sixty_inherited_rows_remain_zero_credit_revalidations() -> None:
    inherited = load(X2 / "inherited-revalidation.json")
    assert inherited["row_count"] == 60
    assert len(inherited["rows"]) == 60
    assert all(row["sylven_r2_novelty_credit"] == 0 for row in inherited["rows"])
    assert all(row["new_novelty_credit"] == 0 for row in inherited["rows"])
    assert all(row["automatic_completion_credit"] == 0 for row in inherited["rows"])


def test_portfolio_counts_and_protected_holds() -> None:
    portfolio = load(X2 / "portfolio-execution.json")
    assert len(portfolio["owner_safe_now"]) == 120
    assert len(portfolio["owner_candidate"]) == 80
    assert len(portfolio["successor_candidate_recommendations"]) == 20
    assert len(portfolio["owner_clean_fix_refine"]) == 100
    assert len(portfolio["exact_approval"]) == 20
    assert len(portfolio["blocked"]) == 10
    held = portfolio["exact_approval"] + portfolio["blocked"]
    assert all(row["execution_authorized"] is False and row["state"] == "UNEXECUTED" for row in held)


def test_twenty_phase_local_skills_passed_both_smoke_polarities() -> None:
    receipt = load(X2 / "skill-validation-receipt.json")
    assert len(receipt["positive"]) == 20
    assert len(receipt["rejecting"]) == 20
    assert all(row["quick_validate_passed"] and row["smoke"]["accepted"] for row in receipt["positive"])
    assert all(row["accepted"] is False for row in receipt["rejecting"])
    dirs = sorted(path for path in (X2 / "skills").iterdir() if path.is_dir())
    assert len(dirs) == 20
    assert all("TODO" not in (path / "SKILL.md").read_text(encoding="utf-8") for path in dirs)


def test_five_skills_were_globally_promoted_with_byte_parity() -> None:
    receipt = load(X2 / "global-promotion-receipt.json")
    assert receipt["promoted_count"] == 5
    assert len(receipt["rows"]) == 5
    assert all(row["byte_parity"] for row in receipt["rows"])
    assert all(row["source_tree_digest"] == row["destination_tree_digest"] for row in receipt["rows"])


def test_ten_family_current_runners_passed_accepting_and_rejecting_smokes() -> None:
    receipt = load(X2 / "runner-smoke-receipt.json")
    assert receipt["runner_count"] == 10
    assert len(receipt["receipts"]) == 10
    assert all(row["positive"]["expectation_met"] for row in receipt["receipts"])
    assert all(row["rejecting"]["expectation_met"] for row in receipt["receipts"])
    assert all(row["positive"]["accepted"] is True for row in receipt["receipts"])
    assert all(row["rejecting"]["accepted"] is False for row in receipt["receipts"])


def test_thirteen_tool_receipt_is_d_first_bounded_and_non_elevated() -> None:
    receipt = load(X2 / "toolchain/transaction-receipt.json")
    assert receipt["direct_tool_count"] == 13
    assert len(receipt["direct_versions"]) == 13
    assert len(receipt["smokes"]) == 13
    assert all(row["positive"] == "passed_once" and row["rejecting"] == "rejected_once" for row in receipt["smokes"])
    assert receipt["python_pip_check"] == "pass"
    assert receipt["python_advisory_snapshot"]["status"] == "zero_known_findings"
    assert receipt["python_advisory_snapshot"]["exhaustive_security"] is False
    assert receipt["node_local_audit"]["known_findings"] == 0
    assert receipt["node_local_audit"]["exhaustive_security"] is False
    assert receipt["system_python_mutated"] is False
    assert receipt["path_or_profile_mutated"] is False
    assert receipt["codex_desktop_updated"] is False
    assert receipt["elevation_or_reboot"] is False
    assert receipt["codex_cli"] == {
        "observed": "codex-cli 0.151.0",
        "requested": "codex-cli 0.151.0",
        "reinstalled": False,
    }


def test_all_six_toolchain_operational_failures_remain_paired() -> None:
    values = load(X2 / "toolchain/operational-failures.json")
    assert len(values["pairs"]) == 6
    assert len({row["failure_id"] for row in values["pairs"]}) == 6
    assert len({row["recovery_id"] for row in values["pairs"]}) == 6
    assert all(row["failure"] and row["recovery"] for row in values["pairs"])


def test_flashcard_deck_has_four_tiers_and_content_addressing() -> None:
    deck = load(X2 / "flashcards/deck.json")
    index = load(X2 / "flashcards/index.json")
    assert deck["card_count"] == 135
    assert deck["family_anchor_count"] == 15
    assert deck["program_card_count"] == 120
    assert len(deck["sections"]) == 14
    assert deck["content_addressed"] is True
    assert deck["supersession_non_erasing"] is True
    assert index["card_count"] == 135
    assert len(index["cards"]) == 135
    for card in deck["cards"]:
        assert validate_flashcard(card) == []


def test_flashcard_index_replays_canonical_card_digests() -> None:
    deck = load(X2 / "flashcards/deck.json")
    index = load(X2 / "flashcards/index.json")
    expected = {
        card["card_id"]: hashlib.sha256(
            json.dumps(card, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        for card in deck["cards"]
    }
    expected = {
        card["card_id"]: hashlib.sha256(
            json.dumps(
                {key: value for key, value in card.items() if key != "content_digest"},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        for card in deck["cards"]
    }
    observed = {row["card_id"]: row["content_digest"] for row in index["cards"]}
    assert observed == expected


def test_method_flow_preserves_exact_failure_and_pass_accounting() -> None:
    ledger = load(X2 / "method-flow/ledger.json")
    assert ledger["phase_failed_witnesses"] == 289
    assert ledger["phase_passing_witnesses"] == 604
    assert len(ledger["events"]) == 893
    assert ledger["failure_nonerasure"] is True
    assert ledger["effective"] == {
        "bounded_passing_witnesses": 21243,
        "effective_methods": 35399,
        "effective_negatives": 43184,
        "exact_gates": 356,
        "open_gaps": 365,
        "retained_failed_witnesses": 14845,
    }


def test_generated_json_is_strictly_parseable() -> None:
    paths = sorted(ROOT.rglob("*.json"))
    assert len(paths) >= 170
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_generated_phase_artifacts_have_no_confirmed_private_payload() -> None:
    candidates: list[tuple[str, list[str]]] = []
    for path in sorted(X2.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".yaml"}:
            found = privacy_candidates(path.read_text(encoding="utf-8"))
            if found:
                candidates.append((path.relative_to(REPO).as_posix(), found))
    assert candidates == []


def test_accessible_report_has_structural_landmarks_and_reserved_reviews() -> None:
    report = (X2 / "accessible-report-draft.html").read_text(encoding="utf-8")
    for token in ("<html", "lang=\"en\"", "<title>", "<nav", "<ol", "<main", "<h1", "<h2", "<section"):
        assert token in report
    for reserved in ("manual", "browser", "assistive-technology", "Māori-language", "affected-user"):
        assert reserved.lower() in report.lower()


@pytest.mark.parametrize("field", ["production_ready", "empirical_confirmation", "stage20_ready"])
def test_no_contract_promotes_protected_claims(field: str) -> None:
    assert all(load(path)[field] is False for path in (X2 / "contracts").glob("*.json"))
