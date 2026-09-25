from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from scripts.ghc_family_coupled_uncertainty import ContractError, evaluate


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v704-v4" / "planning"
PROFILES = json.loads((PLAN / "profiles.json").read_text(encoding="utf-8"))["profiles"]


def req(op: str, index: int = 0):
    return {"op": op, "input": copy.deepcopy(PROFILES[index])}


def test_validate_record():
    assert evaluate(req("validate_record"))["model_fixed_across_trajectory"] is True


def test_policy_enumeration_count():
    result = evaluate(req("policy_enumeration", 1))
    assert result["count"] == 2 ** len(PROFILES[1]["states"])


def test_fixed_model_value_count():
    assert len(evaluate(req("fixed_model_value"))["per_model"]) == 2


def test_lower_not_above_upper():
    lower = Fraction(evaluate(req("lower_envelope", 2))["value"])
    upper = Fraction(evaluate(req("upper_envelope", 2))["value"])
    assert lower <= upper


def test_robust_policy_retains_ties():
    result = evaluate(req("robust_global_policy", 3))
    assert result["policies"]


def test_optimistic_policy_retains_ties():
    result = evaluate(req("optimistic_global_policy", 3))
    assert result["policies"]


def test_regret_nonnegative():
    result = evaluate(req("global_policy_regret", 4))
    assert Fraction(result["maximum"]) >= 0


def test_horizon_trace_has_base_layer():
    result = evaluate(req("horizon_layer_trace", 5))
    assert all(len(row["layers"]) == PROFILES[5]["horizon"] + 1 for row in result["traces"])


def test_coupling_signature_is_bounded():
    result = evaluate(req("coupling_signature", 6))
    assert len(result["differing_rows"]) <= 2 * len(PROFILES[6]["states"])


def test_missing_models_rejected():
    request = req("validate_record")
    del request["input"]["global_models"]
    with pytest.raises(ContractError):
        evaluate(request)


def test_mass_mismatch_rejected():
    request = req("validate_record")
    request["input"]["global_models"][0][0][0][0] = "2"
    with pytest.raises(ContractError):
        evaluate(request)


def test_bad_policy_rejected():
    request = req("validate_record")
    request["input"]["fixed_policy"][0] = 2
    with pytest.raises(ContractError):
        evaluate(request)


def test_invalid_discount_rejected():
    request = req("validate_record")
    request["input"]["discount"] = "3/2"
    with pytest.raises(ContractError):
        evaluate(request)


def test_deterministic_repeat():
    request = req("robust_global_policy", 7)
    assert evaluate(request) == evaluate(copy.deepcopy(request))


def test_all_frozen_x1_contracts_match():
    for proposal_file in sorted((PLAN / "proposals").glob("*.json"))[:10]:
        payload = json.loads(proposal_file.read_text(encoding="utf-8"))
        for contract in payload["contracts"]:
            assert evaluate(contract["request"]) == contract["expected"]
