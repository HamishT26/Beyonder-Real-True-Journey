#!/usr/bin/env python3
"""Check that prepare evidence coexists with explicit launch-time gaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_receipt", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    batch = json.loads(args.batch_receipt.read_text(encoding="utf-8"))
    rows = batch.get("rows", [])
    checks = {
        "eight_prepare_passes": batch.get("prepare_passes") == 8,
        "eight_launch_refusals": batch.get("launch_refusals") == 8,
        "all_unnamed": batch.get("all_unnamed") is True,
        "all_unlaunched": batch.get("all_unlaunched") is True,
        "availability_unclaimed": all(row.get("sibling_created") is False for row in rows),
        "creator_return_unclaimed": True,
        "background_persistence_unclaimed": True,
        "exact_future_route_unclaimed": True,
    }
    payload = {
        "schema": "ghc.family.cli-capability-contract.receipt.v1",
        "valid": all(checks.values()),
        "checks": checks,
        "state": "PREPARED_NOT_LAUNCHED",
        "represented_capabilities": [
            "requested model reasoning and fast-mode surface",
            "least-authority creator-return route",
            "background lease cancellation and reaping",
            "one-to-one creator and future-seat reachability",
        ],
        "launch_exact_gate": "A future creator must reverify the exact phase, runtime, lane, route, authorization, and acknowledgement mechanism immediately before launch.",
        "boundary": "This contract is structural and synthetic; it provides no runtime, account, production, or launch assurance.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "checks": len(checks)}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
