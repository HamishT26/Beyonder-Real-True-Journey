from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v676-v5"


def load(path: str) -> dict:
    return json.loads((BASE / path).read_text(encoding="utf-8"))


def test_second_correction_truth_is_exact_and_bounded() -> None:
    truth = load("correction2/phase-truth.json")
    assert truth["declared_proposal_chain"] == 7590
    assert truth["current_overlay"] == {
        "effective_negatives": 42438,
        "effective_methods": 33112,
        "retained_failed_witnesses": 14099,
        "bounded_passing_witnesses": 19702,
        "open_gaps": 357,
        "exact_gates": 349,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_second_correction_retains_both_new_failures() -> None:
    flow = load("correction2/method-flow-overlay.json")
    assert [row["id"] for row in flow["methods"]] == ["TV6765-POST-N008", "TV6765-POST-N009"]
    assert flow["corrected_phase_ledger_counts"] == {"methods": 660, "failed": 210, "passing": 450}
    assert flow["recovery_erases_failure"] is False


def test_validator_uses_lifecycle_specific_materialization() -> None:
    source = (ROOT / "scripts" / "ghc_family_tamar_vey_v676_v5_final_validator.py").read_text(encoding="utf-8")
    assert 'run_pytest(first_final_dir, "tests/test_ghc_family_tamar_vey_v676_v5_final.py")' in source
    assert 'run_pytest(correction1_dir, "tests/test_ghc_family_tamar_vey_v676_v5_correction.py")' in source
    assert 'run_pytest(repo, "tests/test_ghc_family_tamar_vey_v676_v5_correction2.py")' in source


def test_second_corrected_route_is_prepared_not_sent() -> None:
    route = load("orchestration/terminal-route-hold-corrected2.json")
    assert route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0
    assert route["provisional_exact_title"] == "Elowen Cairn"
    assert route["provisional_phase"] == "v676-v6"
