#!/usr/bin/env python3
"""Evaluate synthetic anytime-valid evidence streams and promotion boundaries."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def evaluate(stream: dict) -> dict:
    reasons: list[str] = []
    factors = stream.get("e_factors", [])
    if stream.get("mode") != "declared_eprocess":
        reasons.append("not_a_declared_eprocess")
    if not factors or any(not isinstance(value, (int, float)) or value < 0 or not math.isfinite(value) for value in factors):
        reasons.append("invalid_nonnegative_factors")
    if stream.get("threshold", 0) <= 1:
        reasons.append("invalid_threshold")
    products = []
    value = 1.0
    for factor in factors if not reasons or reasons == ["not_a_declared_eprocess"] else []:
        value *= factor
        products.append(round(value, 8))
    crossing = next((index + 1 for index, product in enumerate(products) if product >= stream.get("threshold", float("inf"))), None)
    external = stream.get("external_empirical_evidence", False) and stream.get("independent_review", False)
    stage20_ready = not reasons and crossing is not None and external
    return {"stream_id": stream["stream_id"], "structurally_accepted": not reasons, "products": products, "first_crossing": crossing, "external_gates_satisfied": external, "stage20_ready": stage20_ready, "reasons": reasons}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    results = [evaluate(item) for item in fixtures["streams"]]
    expected = {item["stream_id"]: item["expected_structurally_accepted"] for item in fixtures["streams"]}
    checks = [result["structurally_accepted"] == expected[result["stream_id"]] for result in results]
    receipt = {
        "schema": "ghc.family.anytime-evidence-board.v1", "stream_count": len(results),
        "passed_expectation_count": sum(checks), "valid": all(checks) and not any(item["stage20_ready"] for item in results),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "results": results,
        "boundary": "Synthetic e-process arithmetic cannot supply external empirical evidence, independent review, proof, canon, or Stage 20 authority.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"streams": len(results), "valid": receipt["valid"], "verdict": receipt["terminal_verdict"]}, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
