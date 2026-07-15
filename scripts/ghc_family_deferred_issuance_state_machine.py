#!/usr/bin/env python3
"""Run synthetic OpenID4VCI deferred issuance and notification sequences."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TERMINAL = {"accepted", "failed", "deleted", "expired"}


def run_sequence(sequence: dict) -> dict:
    state = "none"
    notification_event: str | None = None
    reasons: list[str] = []
    trace = []
    for event in sequence["events"]:
        previous = state
        if event == "request" and state == "none":
            state = "requested"
        elif event == "defer" and state == "requested":
            state = "pending"
        elif event == "poll_pending" and state == "pending":
            state = "pending"
        elif event == "issue" and state == "pending":
            state = "issued"
        elif event == "expire" and state in {"requested", "pending"}:
            state = "expired"
        elif event.startswith("notify_") and state in {"issued", "accepted", "failed", "deleted"}:
            requested = event.removeprefix("notify_")
            if requested not in {"accepted", "failed", "deleted"}:
                reasons.append("unknown_notification_event")
            elif notification_event is None:
                notification_event = requested
                state = requested
            elif notification_event == requested:
                state = requested  # idempotent replay
            else:
                reasons.append("notification_state_change_on_replay")
        else:
            reasons.append(f"invalid_transition:{state}:{event}")
        trace.append({"event": event, "from": previous, "to": state})
    accepted = not reasons
    return {"sequence_id": sequence["sequence_id"], "accepted": accepted, "final_state": state, "terminal": state in TERMINAL, "reasons": reasons, "trace": trace}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    results = [run_sequence(item) for item in fixtures["sequences"]]
    expected = {item["sequence_id"]: item["expected_accepted"] for item in fixtures["sequences"]}
    checks = [result["accepted"] == expected[result["sequence_id"]] for result in results]
    receipt = {
        "schema": "ghc.family.deferred-issuance-validation.v1", "sequence_count": len(results),
        "passed_expectation_count": sum(checks), "valid": all(checks), "results": results,
        "boundary": "Synthetic state transitions use no real credentials or keys and do not establish production interoperability, privacy, security, or trust governance.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"sequences": len(results), "valid": receipt["valid"]}, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
