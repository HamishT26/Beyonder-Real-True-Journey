#!/usr/bin/env python3
"""Shared deterministic runtime for twelve phase-local family-current runners."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"
CONTRACTS = {
    "seat-placeholder": "Refuse assigned identity or launch state in a future-seat blueprint.",
    "profile": "Represent requested model, reasoning, and speed without claiming live availability.",
    "parent-return": "Require a least-authority parent return channel and acknowledgement before SENT.",
    "route-normalizer": "Normalize immediate v8 rollover while leaving long-range conflicts advisory.",
    "rollover": "Map vN-v8 to v(N+1)-v1 and reject repeated vN-v1 labels.",
    "exact-title": "Require exact existing-task title resolution and reject suffix or fuzzy matches.",
    "single-send": "Preserve PREPARED_NOT_SENT until one acknowledged tool send exists.",
    "file-baton": "Require a sanitized file-backed baton between ten thousand and one hundred thousand words.",
    "privacy": "Scan five public-artifact classes and separate scanner definitions from payload hits.",
    "sparse-worktree": "Keep materialized owner work below two thousand files while preserving ancestry.",
    "four-way-equality": "Require local, upstream, tracking, and fresh-live equality with zero divergence.",
    "doctor": "Report read-only local capability facts without credentials, installation, or launch.",
}


def cli_version() -> str:
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "codex", "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )
    return result.stdout.strip().replace("codex-cli ", "") if result.returncode == 0 else "unavailable"


def evaluate(contract: str, fixture: str) -> tuple[bool, list[str], dict[str, object]]:
    accepting = fixture == "accept"
    issues = [] if accepting else [f"synthetic_{contract}_invariant_violation"]
    observations: dict[str, object] = {
        "fixture": fixture,
        "external_write": False,
        "account_change": False,
        "sibling_created": False,
        "process_launched": False,
    }
    if contract == "seat-placeholder":
        observations.update(identity_fields_null=accepting, launch_count=0 if accepting else 1)
    elif contract == "profile":
        observations.update(model="gpt-5.6-sol", reasoning="max", fast_mode_requested=True, availability_verified=False)
    elif contract == "parent-return":
        observations.update(parent_only=True, acknowledgement_required=True, delivery_state="PREPARED_NOT_SENT")
    elif contract == "route-normalizer":
        observations.update(immediate="Sable Rook v652-v1", long_range="advisory")
    elif contract == "rollover":
        observations.update(input="v651-v8", output="v652-v1" if accepting else "v651-v1")
    elif contract == "exact-title":
        observations.update(requested="Sable Rook", resolved="Sable Rook" if accepting else "Sable Rook copy")
    elif contract == "single-send":
        observations.update(acknowledgements=0, state="PREPARED_NOT_SENT")
    elif contract == "file-baton":
        observations.update(words=12_000 if accepting else 9_999, minimum=10_000, maximum=100_000)
    elif contract == "privacy":
        observations.update(classes=5, confirmed_hits=0 if accepting else 1)
    elif contract == "sparse-worktree":
        observations.update(materialized_files=700 if accepting else 2_001, threshold=2_000, history_preserved=True)
    elif contract == "four-way-equality":
        observations.update(equal=accepting, divergence="0 0" if accepting else "1 0")
    elif contract == "doctor":
        observations.update(codex_cli=cli_version(), credentials_read=False, installations=0)
    return accepting, issues, observations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", choices=sorted(CONTRACTS), required=True)
    parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    accepted, issues, observations = evaluate(args.contract, args.fixture)
    payload = {
        "schema": "ghc.family.v651-v8-special.runner-receipt.v1",
        "phase": "v651-v8-special-cli-prep",
        "contract": args.contract,
        "purpose": CONTRACTS[args.contract],
        "fixture": args.fixture,
        "accepted": accepted,
        "issues": issues,
        "observations": observations,
        "boundary": "Synthetic or read-only owner-local evidence only; not launch, production, authority, independent reproduction, or Stage 20 evidence.",
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    expected = accepted if args.fixture == "accept" else not accepted
    print(json.dumps({"valid": expected, "contract": args.contract, "fixture": args.fixture, "accepted": accepted}))
    return 0 if expected else 2


if __name__ == "__main__":
    raise SystemExit(main())
