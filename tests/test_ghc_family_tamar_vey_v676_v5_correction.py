from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v676-v5"


def load(path: str) -> dict:
    return json.loads((BASE / path).read_text(encoding="utf-8"))


def test_correction_retains_failed_canonical_at_zero_credit() -> None:
    receipt = load("correction/correction-receipt.json")
    assert receipt["failed_canonical_status"] == "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"
    assert receipt["failed_canonical_success_count"] == 0
    assert receipt["failed_canonical_receipt_sha256"] == "e9fc4dce5135b235d111e47945c99b06d6fe10b35f27159a879dd0040d407f20"


def test_corrected_truth_uses_exact_chain_and_bounded_labels() -> None:
    truth = load("correction/phase-truth.json")
    assert truth["declared_proposal_chain"] == 7590
    assert truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_validator_contract_contains_corrected_chain_only() -> None:
    source = (ROOT / "scripts" / "ghc_family_tamar_vey_v676_v5_final_validator.py").read_text(encoding="utf-8")
    assert '"proposal_chain_7590"' in source
    assert '"proposal_chain_7550"' not in source


def test_corrected_route_remains_prepared_and_unsent() -> None:
    route = load("orchestration/terminal-route-hold-corrected.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["send_count"] == 0
    assert route["provisional_exact_title"] == "Elowen Cairn"
    assert route["provisional_phase"] == "v676-v6"
