#!/usr/bin/env python3
"""Trinity energy bank system.

Aggregates regenerated energy/token-credit outputs into a persistent reserve and
projects available run budgets for upcoming message exchanges.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "docs" / "energy-bank-state.json"
REPORT_PATH = ROOT / "docs" / "energy-bank-report.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _project_sessions(reserve_tokens: float, reserve_credits: float, sessions: int) -> list[dict[str, float]]:
    projections: list[dict[str, float]] = []
    remaining_tokens = reserve_tokens
    remaining_credits = reserve_credits
    for session in range(1, sessions + 1):
        planned_tokens = 9000 + session * 1200
        planned_credits = round(planned_tokens / 1000, 6)

        coverage = 0.0
        if planned_tokens > 0:
            coverage = min(1.0, remaining_tokens / planned_tokens)

        covered_tokens = min(remaining_tokens, planned_tokens)
        covered_credits = min(remaining_credits, planned_credits)
        uncovered_tokens = max(0.0, planned_tokens - covered_tokens)
        uncovered_credits = max(0.0, planned_credits - covered_credits)

        remaining_tokens = max(0.0, remaining_tokens - planned_tokens)
        remaining_credits = max(0.0, remaining_credits - planned_credits)

        projections.append(
            {
                "session": session,
                "planned_tokens": planned_tokens,
                "planned_credits": planned_credits,
                "token_coverage_ratio": round(coverage, 6),
                "covered_tokens": round(covered_tokens, 6),
                "covered_credits": round(covered_credits, 6),
                "uncovered_tokens": round(uncovered_tokens, 6),
                "uncovered_credits": round(uncovered_credits, 6),
                "token_surplus_after_session": round(remaining_tokens, 6),
                "credit_surplus_after_session": round(remaining_credits, 6),
            }
        )
    return projections


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Trinity energy bank system")
    parser.add_argument("--token-report", default="docs/token-credit-bank-report.json")
    parser.add_argument("--quantum", default="docs/quantum-energy-transmutation-report.json")
    parser.add_argument("--cache-report", default="docs/cache-waste-regenerator-report.json")
    parser.add_argument("--state", default=str(STATE_PATH.relative_to(ROOT)))
    parser.add_argument("--out", default=str(REPORT_PATH.relative_to(ROOT)))
    parser.add_argument(
        "--reserve-growth",
        type=float,
        default=1.0,
        help="Fraction of regenerated assets routed into long-term reserve",
    )
    parser.add_argument(
        "--reserve-cap-multiplier",
        type=float,
        default=10.0,
        help="Multiplier for dynamic reserve-cap growth target (10x default)",
    )
    parser.add_argument(
        "--auto-max-cap",
        action="store_true",
        help="Automatically elevate reserve cap multiplier up to --cap-ceiling based on reimbursement pressure",
    )
    parser.add_argument(
        "--cap-ceiling",
        type=float,
        default=100.0,
        help="Upper bound for auto-max reserve cap multiplier",
    )
    parser.add_argument(
        "--projection-sessions",
        type=int,
        default=10,
        help="Number of upcoming sessions to project (minimum 1)",
    )
    args = parser.parse_args()

    token_report = _load_json(ROOT / args.token_report)
    quantum = _load_json(ROOT / args.quantum)
    cache_report = _load_json(ROOT / args.cache_report)
    state_path = ROOT / args.state
    out_path = ROOT / args.out

    prior_state = _load_json(state_path)
    prior_tokens = float(prior_state.get("reserve_tokens", 0.0))
    prior_credits = float(prior_state.get("reserve_credits", 0.0))
    prior_energy = float(prior_state.get("reserve_energy_units", 0.0))

    token_outputs = token_report.get("outputs", {})
    reserve_tokens_consumed = float(token_outputs.get("reserve_tokens_consumed", 0.0))
    reserve_credits_consumed = float(token_outputs.get("reserve_credits_consumed", 0.0))
    reserve_energy_consumed = float(token_outputs.get("reserve_energy_consumed", 0.0))

    post_spend_tokens = max(0.0, prior_tokens - reserve_tokens_consumed)
    post_spend_credits = max(0.0, prior_credits - reserve_credits_consumed)
    post_spend_energy = max(0.0, prior_energy - reserve_energy_consumed)

    regenerated_tokens = float(token_outputs.get("tokens_regenerated", 0.0))
    regenerated_credits = float(token_outputs.get("credits_regenerated", 0.0))
    usable_energy = float(quantum.get("outputs", {}).get("net_usable_energy", 0.0))
    cache_tokens = float(cache_report.get("outputs", {}).get("reclaimed_tokens", 0.0))
    cache_credits = float(cache_report.get("outputs", {}).get("reclaimed_credits", 0.0))
    cache_energy = float(cache_report.get("outputs", {}).get("reclaimed_energy_units", 0.0))

    growth = max(0.0, min(1.5, args.reserve_growth))
    cap_multiplier = max(1.0, args.reserve_cap_multiplier)
    cap_ceiling = max(cap_multiplier, args.cap_ceiling)
    if args.auto_max_cap:
        reimbursement_ratio = float(token_outputs.get("reimbursement_ratio", 1.0))
        remaining_tokens = float(token_outputs.get("remaining_tokens_demand", 0.0))
        used_tokens = float(token_report.get("inputs", {}).get("tokens_used", 0.0))
        pressure = 1.0
        if used_tokens > 0:
            pressure += min(1.0, remaining_tokens / used_tokens)
        pressure *= max(1.0, reimbursement_ratio)
        cap_multiplier = min(cap_ceiling, max(cap_multiplier, round(cap_multiplier * pressure, 6)))

    prev_cap_tokens = float(prior_state.get("reserve_cap_tokens", 0.0))
    prev_cap_credits = float(prior_state.get("reserve_cap_credits", 0.0))
    prev_cap_energy = float(prior_state.get("reserve_cap_energy_units", 0.0))

    dynamic_cap_tokens = max(prev_cap_tokens, max(prior_tokens, 1.0) * cap_multiplier)
    dynamic_cap_credits = max(prev_cap_credits, max(prior_credits, 1.0) * cap_multiplier)
    dynamic_cap_energy = max(prev_cap_energy, max(prior_energy, 1.0) * cap_multiplier)

    reserve_tokens = round(min(dynamic_cap_tokens, post_spend_tokens + (regenerated_tokens + cache_tokens) * growth), 6)
    reserve_credits = round(min(dynamic_cap_credits, post_spend_credits + (regenerated_credits + cache_credits) * growth), 6)
    reserve_energy = round(min(dynamic_cap_energy, post_spend_energy + (usable_energy + cache_energy) * growth), 6)

    projection_sessions = max(1, args.projection_sessions)
    projections = _project_sessions(reserve_tokens, reserve_credits, projection_sessions)
    total_planned_tokens = round(sum(float(item["planned_tokens"]) for item in projections), 6)
    total_covered_tokens = round(sum(float(item["covered_tokens"]) for item in projections), 6)
    total_uncovered_tokens = round(sum(float(item["uncovered_tokens"]) for item in projections), 6)
    total_planned_credits = round(sum(float(item["planned_credits"]) for item in projections), 6)
    total_covered_credits = round(sum(float(item["covered_credits"]) for item in projections), 6)
    total_uncovered_credits = round(sum(float(item["uncovered_credits"]) for item in projections), 6)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "trinity-energy-bank-system",
        "inputs": {
            "reserve_growth": growth,
            "reserve_cap_multiplier": cap_multiplier,
            "auto_max_cap": bool(args.auto_max_cap),
            "cap_ceiling": cap_ceiling,
            "projection_sessions": projection_sessions,
            "regenerated_tokens": regenerated_tokens,
            "regenerated_credits": regenerated_credits,
            "net_usable_energy": usable_energy,
            "cache_reclaimed_tokens": cache_tokens,
            "cache_reclaimed_credits": cache_credits,
            "cache_reclaimed_energy_units": cache_energy,
            "reserve_tokens_consumed": reserve_tokens_consumed,
            "reserve_credits_consumed": reserve_credits_consumed,
            "reserve_energy_consumed": reserve_energy_consumed,
        },
        "outputs": {
            "post_spend_tokens": round(post_spend_tokens, 6),
            "post_spend_credits": round(post_spend_credits, 6),
            "post_spend_energy_units": round(post_spend_energy, 6),
            "reserve_cap_tokens": round(dynamic_cap_tokens, 6),
            "reserve_cap_credits": round(dynamic_cap_credits, 6),
            "reserve_cap_energy_units": round(dynamic_cap_energy, 6),
            "reserve_tokens": reserve_tokens,
            "reserve_credits": reserve_credits,
            "reserve_energy_units": reserve_energy,
            "projected_sessions": projections,
            "projection_summary": {
                "sessions": projection_sessions,
                "planned_tokens": total_planned_tokens,
                "covered_tokens": total_covered_tokens,
                "uncovered_tokens": total_uncovered_tokens,
                "planned_credits": total_planned_credits,
                "covered_credits": total_covered_credits,
                "uncovered_credits": total_uncovered_credits,
            },
        },
    }

    state_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "updated_utc": report["generated_utc"],
                "reserve_tokens": reserve_tokens,
                "reserve_credits": reserve_credits,
                "reserve_energy_units": reserve_energy,
                "reserve_cap_tokens": round(dynamic_cap_tokens, 6),
                "reserve_cap_credits": round(dynamic_cap_credits, 6),
                "reserve_cap_energy_units": round(dynamic_cap_energy, 6),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Updated {state_path}")


if __name__ == "__main__":
    main()
