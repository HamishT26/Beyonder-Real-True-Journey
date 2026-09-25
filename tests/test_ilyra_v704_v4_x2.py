from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_coupled_uncertainty import ContractError, evaluate  # noqa: E402


PLAN = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "planning" / "proposals"


def contracts_for(profile_index: int) -> list[dict]:
    rows = []
    for file in sorted(PLAN.glob("*.json"))[10:]:
        rows.append(json.loads(file.read_text(encoding="utf-8"))["contracts"][profile_index])
    assert len(rows) == 10
    return rows


@pytest.mark.parametrize("profile_index", range(15))
def test_frozen_x2_contracts_match_independent_engine(profile_index: int) -> None:
    for contract in contracts_for(profile_index):
        assert evaluate(contract["request"]) == contract["expected"]


@pytest.mark.parametrize("profile_index", range(15))
def test_x2_boundaries_and_one_malformed_subject(profile_index: int) -> None:
    rows = {row["operation"]: row for row in contracts_for(profile_index)}
    gap = evaluate(rows["rectangularity_gap"]["request"])
    covariance = evaluate(rows["relabel_covariance"]["request"])
    zero = evaluate(rows["discount_zero_certificate"]["request"])
    mixture = evaluate(rows["mixture_representation"]["request"])
    calibration = evaluate(rows["calibration_evidence_gap"]["request"])
    authority = evaluate(rows["authority_gate"]["request"])
    assert gap["nonnegative"] is True
    assert covariance["equal"] is True
    assert zero["transition_independent_after_first_reward"] is True
    assert mixture["outcome"] == "represented"
    assert calibration["outcome"] == "open_gap"
    assert authority["outcome"] == "exact_gate"
    malformed = copy.deepcopy(rows["rectangularity_gap"]["request"])
    malformed["input"]["global_models"][0][0][0][0] = "2"
    with pytest.raises(ContractError):
        evaluate(malformed)
