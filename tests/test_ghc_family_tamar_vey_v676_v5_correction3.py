from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v676-v5"


def load(path: str) -> dict:
    return json.loads((BASE / path).read_text(encoding="utf-8"))


def test_third_correction_truth_is_exact() -> None:
    truth = load("correction3/phase-truth.json")
    assert truth["declared_proposal_chain"] == 7590
    assert truth["current_overlay"]["effective_negatives"] == 42439
    assert truth["current_overlay"]["effective_methods"] == 33114
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_named_fixture_recovery_is_retained() -> None:
    receipt = load("correction3/correction-receipt.json")
    assert receipt["new_failure_id"] == "TV6765-POST-N010"
    assert receipt["external_preflight_materialized_owner_files"] == 589
    assert receipt["external_preflight_first_final_tests"] == 11
    assert receipt["failed_canonical_success_count"] == 0


def test_validator_prepares_named_git_fixture_before_final_tests() -> None:
    source = (ROOT / "scripts" / "ghc_family_tamar_vey_v676_v5_final_validator.py").read_text(encoding="utf-8")
    assert "prepare_named_git_fixture(repo, first_final_dir, FIRST_FINAL)" in source
    assert 'run_pytest(first_final_dir, "tests/test_ghc_family_tamar_vey_v676_v5_final.py")' in source
    assert 'run_pytest(repo, "tests/test_ghc_family_tamar_vey_v676_v5_correction3.py")' in source


def test_third_route_remains_prepared_not_sent() -> None:
    route = load("orchestration/terminal-route-hold-corrected3.json")
    assert route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0
    assert route["provisional_exact_title"] == "Elowen Cairn"
    assert route["provisional_phase"] == "v676-v6"
