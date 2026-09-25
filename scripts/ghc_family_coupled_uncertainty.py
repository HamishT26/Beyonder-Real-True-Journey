#!/usr/bin/env python3
"""Exact finite globally coupled transition-model operations for Ilyra v704-v4."""

from __future__ import annotations

import itertools
import json
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


SCOPE = "finite_synthetic_globally_coupled_uncertainty"
X1_OPERATIONS = {
    "validate_record",
    "policy_enumeration",
    "fixed_model_value",
    "lower_envelope",
    "upper_envelope",
    "robust_global_policy",
    "optimistic_global_policy",
    "global_policy_regret",
    "horizon_layer_trace",
    "coupling_signature",
}


class ContractError(ValueError):
    """A bounded public input violates the declared finite contract."""


def frac(value: Any) -> Fraction:
    if isinstance(value, bool):
        raise ContractError("boolean is not a rational scalar")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ContractError(f"invalid rational scalar: {value!r}") from exc


def q(value: Fraction | int) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _vector(values: list[Any], length: int, label: str) -> list[Fraction]:
    if not isinstance(values, list) or len(values) != length:
        raise ContractError(f"{label} must have length {length}")
    return [frac(x) for x in values]


def validate_profile(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ContractError("input must be an object")
    states = raw.get("states")
    actions = raw.get("actions")
    if not isinstance(states, list) or not 1 <= len(states) <= 4 or len(set(states)) != len(states):
        raise ContractError("states must contain one to four unique labels")
    if actions != ["a0", "a1"]:
        raise ContractError("actions must be exactly a0 and a1")
    n = len(states)
    rewards_raw = raw.get("rewards")
    if not isinstance(rewards_raw, list) or len(rewards_raw) != n:
        raise ContractError("reward row count mismatch")
    rewards = [_vector(row, 2, "reward row") for row in rewards_raw]
    terminal = _vector(raw.get("terminal"), n, "terminal")
    initial = _vector(raw.get("initial"), n, "initial")
    if any(x < 0 for x in initial) or sum(initial) != 1:
        raise ContractError("initial distribution must be nonnegative and sum to one")
    discount = frac(raw.get("discount"))
    if not 0 <= discount <= 1:
        raise ContractError("discount must be between zero and one")
    horizon = raw.get("horizon")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or not 0 <= horizon <= 4:
        raise ContractError("horizon must be an integer from zero to four")
    policy = raw.get("fixed_policy")
    if not isinstance(policy, list) or len(policy) != n or any(a not in (0, 1) for a in policy):
        raise ContractError("fixed policy must choose action zero or one per state")
    models_raw = raw.get("global_models")
    if not isinstance(models_raw, list) or not 1 <= len(models_raw) <= 4:
        raise ContractError("one to four global models are required")
    models: list[list[list[list[Fraction]]]] = []
    for model in models_raw:
        if not isinstance(model, list) or len(model) != n:
            raise ContractError("global model state count mismatch")
        parsed_model = []
        for state_rows in model:
            if not isinstance(state_rows, list) or len(state_rows) != 2:
                raise ContractError("global model action count mismatch")
            parsed_actions = []
            for row in state_rows:
                parsed = _vector(row, n, "transition row")
                if any(x < 0 for x in parsed) or sum(parsed) != 1:
                    raise ContractError("transition rows must be nonnegative and sum to one")
                parsed_actions.append(parsed)
            parsed_model.append(parsed_actions)
        models.append(parsed_model)
    return {
        "profile_id": raw.get("profile_id"),
        "label": raw.get("label"),
        "states": list(states),
        "actions": list(actions),
        "rewards": rewards,
        "terminal": terminal,
        "discount": discount,
        "horizon": horizon,
        "initial": initial,
        "fixed_policy": list(policy),
        "global_models": models,
        "uncertainty_contract": raw.get("uncertainty_contract"),
    }


def enumerate_policies(state_count: int) -> list[list[int]]:
    return [[(mask >> state) & 1 for state in range(state_count)] for mask in range(2**state_count)]


def evaluate_policy(profile: dict[str, Any], policy: list[int], model_index: int) -> dict[str, Any]:
    values = list(profile["terminal"])
    layers = [[q(x) for x in values]]
    model = profile["global_models"][model_index]
    for _ in range(profile["horizon"]):
        next_values = []
        for state, action in enumerate(policy):
            future = sum((prob * values[target] for target, prob in enumerate(model[state][action])), Fraction(0))
            next_values.append(profile["rewards"][state][action] + profile["discount"] * future)
        values = next_values
        layers.append([q(x) for x in values])
    scalar = sum((profile["initial"][i] * values[i] for i in range(len(values))), Fraction(0))
    return {"vector": [q(x) for x in values], "scalar": q(scalar), "layers": layers}


def policy_table(profile: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for policy in enumerate_policies(len(profile["states"])):
        values = [Fraction(evaluate_policy(profile, policy, m)["scalar"]) for m in range(len(profile["global_models"]))]
        rows.append({"policy": policy, "model_values": [q(x) for x in values], "lower": q(min(values)), "upper": q(max(values))})
    return rows


def best_rows(table: list[dict[str, Any]], field: str) -> dict[str, Any]:
    best = max(Fraction(row[field]) for row in table)
    return {"value": q(best), "policies": [row["policy"] for row in table if Fraction(row[field]) == best]}


def evaluate(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ContractError("request must be an object")
    operation = request.get("op")
    if operation not in X1_OPERATIONS:
        raise ContractError(f"unsupported x1 operation: {operation!r}")
    profile = validate_profile(request.get("input"))
    base: dict[str, Any] = {"scope": SCOPE, "external_credit": False}
    table = policy_table(profile)
    fixed = [evaluate_policy(profile, profile["fixed_policy"], m) for m in range(len(profile["global_models"]))]
    robust = best_rows(table, "lower")
    optimistic = best_rows(table, "upper")
    if operation == "validate_record":
        return {**base, "states": len(profile["states"]), "actions": 2, "global_models": len(profile["global_models"]), "horizon": profile["horizon"], "model_fixed_across_trajectory": True}
    if operation == "policy_enumeration":
        return {**base, "count": len(table), "policies": [row["policy"] for row in table]}
    if operation == "fixed_model_value":
        return {**base, "policy": profile["fixed_policy"], "per_model": [{"model": m, "vector": row["vector"], "scalar": row["scalar"]} for m, row in enumerate(fixed)]}
    if operation == "lower_envelope":
        return {**base, "value": q(min(Fraction(row["scalar"]) for row in fixed))}
    if operation == "upper_envelope":
        return {**base, "value": q(max(Fraction(row["scalar"]) for row in fixed))}
    if operation == "robust_global_policy":
        return {**base, **robust, "all_policy_bounds": [{"policy": row["policy"], "lower": row["lower"]} for row in table]}
    if operation == "optimistic_global_policy":
        return {**base, **optimistic, "all_policy_bounds": [{"policy": row["policy"], "upper": row["upper"]} for row in table]}
    if operation == "global_policy_regret":
        chosen = next(row for row in table if row["policy"] == robust["policies"][0])
        model_best = [max(Fraction(row["model_values"][m]) for row in table) for m in range(len(profile["global_models"]))]
        regrets = [model_best[m] - Fraction(chosen["model_values"][m]) for m in range(len(model_best))]
        return {**base, "policy": robust["policies"][0], "per_model": [q(x) for x in regrets], "maximum": q(max(regrets))}
    if operation == "horizon_layer_trace":
        return {**base, "policy": profile["fixed_policy"], "traces": [{"model": m, "layers": row["layers"]} for m, row in enumerate(fixed)]}
    if operation == "coupling_signature":
        differing = []
        for state in range(len(profile["states"])):
            for action in (0, 1):
                if profile["global_models"][0][state][action] != profile["global_models"][1][state][action]:
                    differing.append([state, action])
        return {**base, "differing_rows": differing}
    raise AssertionError("unreachable")


def main() -> int:
    if len(sys.argv) == 2:
        request = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        request = json.load(sys.stdin)
    try:
        result = evaluate(request)
    except (ContractError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({"ok": False, "error": str(exc), "scope": SCOPE}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, "result": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
