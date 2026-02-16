#!/usr/bin/env python3
"""Validate Trinity token/credit and energy-bank reports.

Enforces required keys and basic guardrails so suite runs fail loudly on
malformed reimbursement/reserve artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_TOKEN_OUTPUTS = {
    "reserve_tokens_available": (0.0, None),
    "reserve_credits_available": (0.0, None),
    "reserve_tokens_consumed": (0.0, None),
    "reserve_credits_consumed": (0.0, None),
    "remaining_tokens_demand": (0.0, None),
    "remaining_credits_demand": (0.0, None),
    "tokens_regenerated": (0.0, None),
    "topup_tokens_for_target_ratio": (0.0, None),
    "credits_regenerated": (0.0, None),
    "total_tokens_covered": (0.0, None),
    "total_credits_covered": (0.0, None),
    "token_delta": (None, None),
    "credit_delta": (None, None),
    "reimbursement_ratio": (0.0, None),
}

REQUIRED_ENERGY_OUTPUTS = {
    "post_spend_tokens": (0.0, None),
    "post_spend_credits": (0.0, None),
    "post_spend_energy_units": (0.0, None),
    "reserve_cap_tokens": (0.0, None),
    "reserve_cap_credits": (0.0, None),
    "reserve_cap_energy_units": (0.0, None),
    "reserve_tokens": (0.0, None),
    "reserve_credits": (0.0, None),
    "reserve_energy_units": (0.0, None),
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing report: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}") from exc


def check_outputs(name: str, outputs: dict, required: dict[str, tuple[float | None, float | None]]) -> None:
    if not isinstance(outputs, dict):
        raise SystemExit(f"{name}: outputs must be an object")

    for key, (min_v, max_v) in required.items():
        if key not in outputs:
            raise SystemExit(f"{name}: missing outputs.{key}")
        value = outputs[key]
        if not isinstance(value, (int, float)):
            raise SystemExit(f"{name}: outputs.{key} must be numeric")
        fval = float(value)
        if min_v is not None and fval < min_v:
            raise SystemExit(f"{name}: outputs.{key} must be >= {min_v}")
        if max_v is not None and fval > max_v:
            raise SystemExit(f"{name}: outputs.{key} must be <= {max_v}")


def check_token_consistency(report: dict) -> None:
    outputs = report.get("outputs", {})
    consumed = float(outputs.get("reserve_tokens_consumed", 0.0))
    available = float(outputs.get("reserve_tokens_available", 0.0))
    if consumed > available:
        raise SystemExit("token-credit: reserve_tokens_consumed cannot exceed reserve_tokens_available")

    used = float(report.get("inputs", {}).get("tokens_used", 0.0))
    total_covered = float(outputs.get("total_tokens_covered", 0.0))
    ratio = float(outputs.get("reimbursement_ratio", 0.0))
    if used > 0 and abs(ratio - (total_covered / used)) > 1e-5:
        raise SystemExit("token-credit: reimbursement_ratio inconsistent with total_tokens_covered / tokens_used")

    target_ratio = float(report.get("inputs", {}).get("target_reimbursement_ratio", 1.0))
    if ratio + 1e-6 < target_ratio:
        raise SystemExit("token-credit: reimbursement_ratio is below target_reimbursement_ratio")




def check_energy_consistency(report: dict) -> None:
    outputs = report.get("outputs", {})
    if float(outputs.get("reserve_tokens", 0.0)) > float(outputs.get("reserve_cap_tokens", 0.0)):
        raise SystemExit("energy-bank: reserve_tokens cannot exceed reserve_cap_tokens")
    if float(outputs.get("reserve_credits", 0.0)) > float(outputs.get("reserve_cap_credits", 0.0)):
        raise SystemExit("energy-bank: reserve_credits cannot exceed reserve_cap_credits")
    if float(outputs.get("reserve_energy_units", 0.0)) > float(outputs.get("reserve_cap_energy_units", 0.0)):
        raise SystemExit("energy-bank: reserve_energy_units cannot exceed reserve_cap_energy_units")

def check_energy_projection(report: dict) -> None:
    projections = report.get("outputs", {}).get("projected_sessions")
    if not isinstance(projections, list) or not projections:
        raise SystemExit("energy-bank: outputs.projected_sessions must be a non-empty list")
    expected_sessions = int(report.get("inputs", {}).get("projection_sessions", 10))
    if expected_sessions < 1:
        raise SystemExit("energy-bank: inputs.projection_sessions must be >= 1")
    if len(projections) != expected_sessions:
        raise SystemExit("energy-bank: projected_sessions length must match inputs.projection_sessions")

    prev_token_surplus = None
    prev_credit_surplus = None
    for item in projections:
        if not isinstance(item, dict):
            raise SystemExit("energy-bank: projected_sessions entries must be objects")
        if "token_coverage_ratio" not in item:
            raise SystemExit("energy-bank: projected session missing token_coverage_ratio")
        ratio = item["token_coverage_ratio"]
        if not isinstance(ratio, (int, float)):
            raise SystemExit("energy-bank: token_coverage_ratio must be numeric")
        if float(ratio) < 0.0 or float(ratio) > 1.0:
            raise SystemExit("energy-bank: token_coverage_ratio must be in [0,1]")

        required_keys = (
            "planned_tokens",
            "covered_tokens",
            "uncovered_tokens",
            "planned_credits",
            "covered_credits",
            "uncovered_credits",
            "token_surplus_after_session",
            "credit_surplus_after_session",
        )
        for key in required_keys:
            if key not in item:
                raise SystemExit(f"energy-bank: projected session missing {key}")
            if not isinstance(item[key], (int, float)):
                raise SystemExit(f"energy-bank: projected session {key} must be numeric")

        planned_tokens = float(item["planned_tokens"])
        covered_tokens = float(item["covered_tokens"])
        uncovered_tokens = float(item["uncovered_tokens"])
        planned_credits = float(item["planned_credits"])
        covered_credits = float(item["covered_credits"])
        uncovered_credits = float(item["uncovered_credits"])

        if abs((covered_tokens + uncovered_tokens) - planned_tokens) > 1e-4:
            raise SystemExit("energy-bank: covered_tokens + uncovered_tokens must equal planned_tokens")
        if abs((covered_credits + uncovered_credits) - planned_credits) > 1e-4:
            raise SystemExit("energy-bank: covered_credits + uncovered_credits must equal planned_credits")

        if planned_tokens > 0 and abs((covered_tokens / planned_tokens) - float(ratio)) > 1e-4:
            raise SystemExit("energy-bank: token_coverage_ratio inconsistent with covered_tokens / planned_tokens")

        token_surplus = float(item["token_surplus_after_session"])
        credit_surplus = float(item["credit_surplus_after_session"])
        if token_surplus < 0.0 or credit_surplus < 0.0:
            raise SystemExit("energy-bank: projected surplus values must be non-negative")
        if prev_token_surplus is not None and token_surplus > prev_token_surplus + 1e-6:
            raise SystemExit("energy-bank: token_surplus_after_session must be non-increasing")
        if prev_credit_surplus is not None and credit_surplus > prev_credit_surplus + 1e-6:
            raise SystemExit("energy-bank: credit_surplus_after_session must be non-increasing")
        prev_token_surplus = token_surplus
        prev_credit_surplus = credit_surplus

    summary = report.get("outputs", {}).get("projection_summary")
    if not isinstance(summary, dict):
        raise SystemExit("energy-bank: outputs.projection_summary must be an object")
    required_summary_keys = (
        "sessions",
        "planned_tokens",
        "covered_tokens",
        "uncovered_tokens",
        "planned_credits",
        "covered_credits",
        "uncovered_credits",
    )
    for key in required_summary_keys:
        if key not in summary:
            raise SystemExit(f"energy-bank: projection_summary missing {key}")
        if not isinstance(summary[key], (int, float)):
            raise SystemExit(f"energy-bank: projection_summary.{key} must be numeric")

    if int(summary["sessions"]) != expected_sessions:
        raise SystemExit("energy-bank: projection_summary.sessions must match inputs.projection_sessions")

    sum_planned_tokens = sum(float(i["planned_tokens"]) for i in projections)
    sum_covered_tokens = sum(float(i["covered_tokens"]) for i in projections)
    sum_uncovered_tokens = sum(float(i["uncovered_tokens"]) for i in projections)
    sum_planned_credits = sum(float(i["planned_credits"]) for i in projections)
    sum_covered_credits = sum(float(i["covered_credits"]) for i in projections)
    sum_uncovered_credits = sum(float(i["uncovered_credits"]) for i in projections)

    if abs(float(summary["planned_tokens"]) - sum_planned_tokens) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.planned_tokens mismatch")
    if abs(float(summary["covered_tokens"]) - sum_covered_tokens) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.covered_tokens mismatch")
    if abs(float(summary["uncovered_tokens"]) - sum_uncovered_tokens) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.uncovered_tokens mismatch")
    if abs(float(summary["planned_credits"]) - sum_planned_credits) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.planned_credits mismatch")
    if abs(float(summary["covered_credits"]) - sum_covered_credits) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.covered_credits mismatch")
    if abs(float(summary["uncovered_credits"]) - sum_uncovered_credits) > 1e-4:
        raise SystemExit("energy-bank: projection_summary.uncovered_credits mismatch")

    if float(summary["planned_tokens"]) < 0.0 or float(summary["planned_credits"]) < 0.0:
        raise SystemExit("energy-bank: projection_summary planned values must be non-negative")
    if float(summary["covered_tokens"]) < 0.0 or float(summary["covered_credits"]) < 0.0:
        raise SystemExit("energy-bank: projection_summary covered values must be non-negative")
    if float(summary["uncovered_tokens"]) < 0.0 or float(summary["uncovered_credits"]) < 0.0:
        raise SystemExit("energy-bank: projection_summary uncovered values must be non-negative")
    if float(summary["covered_tokens"]) - float(summary["planned_tokens"]) > 1e-6:
        raise SystemExit("energy-bank: projection_summary covered_tokens cannot exceed planned_tokens")
    if float(summary["covered_credits"]) - float(summary["planned_credits"]) > 1e-6:
        raise SystemExit("energy-bank: projection_summary covered_credits cannot exceed planned_credits")
    if abs((float(summary["covered_tokens"]) + float(summary["uncovered_tokens"])) - float(summary["planned_tokens"])) > 1e-4:
        raise SystemExit("energy-bank: projection_summary covered_tokens + uncovered_tokens must equal planned_tokens")
    if abs((float(summary["covered_credits"]) + float(summary["uncovered_credits"])) - float(summary["planned_credits"])) > 1e-4:
        raise SystemExit("energy-bank: projection_summary covered_credits + uncovered_credits must equal planned_credits")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate token-credit and energy-bank reports")
    parser.add_argument("--token", default="docs/token-credit-bank-report.json")
    parser.add_argument("--energy", default="docs/energy-bank-report.json")
    args = parser.parse_args()

    token = load_json(Path(args.token))
    energy = load_json(Path(args.energy))

    check_outputs("token-credit", token.get("outputs"), REQUIRED_TOKEN_OUTPUTS)
    status = token.get("outputs", {}).get("status")
    if status not in {"surplus", "deficit"}:
        raise SystemExit("token-credit: outputs.status must be 'surplus' or 'deficit'")
    check_token_consistency(token)

    check_outputs("energy-bank", energy.get("outputs"), REQUIRED_ENERGY_OUTPUTS)
    check_energy_consistency(energy)
    check_energy_projection(energy)

    print("validated token-credit and energy-bank reports")


if __name__ == "__main__":
    main()
