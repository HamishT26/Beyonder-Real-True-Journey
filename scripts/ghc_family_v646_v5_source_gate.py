#!/usr/bin/env python3
"""Check source status, zero-row, proxy, and authority boundaries for v646-v5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def evaluate() -> dict:
    sources = load("sources/source-ledger.json")
    ledger = load("x2-proposal-ledger.json")
    by_id = {row["proposal_id"]: row for row in ledger["proposals"]}
    checks = {
        "source_status_vocabulary": all(row["status"] in {"current", "stable", "draft", "watch"} for row in sources["sources"]),
        "source_count_23": len(sources["sources"]) == 23,
        "rubin_open_gap": by_id["V6465-P03"]["outcome"] == "open_gap" and by_id["V6465-P03"]["real_rows"] == 0,
        "thos_represented": by_id["V6465-P04"]["outcome"] == "represented" and by_id["V6465-P04"]["real_participants_or_animals"] == 0,
        "freed_id_represented": by_id["V6465-P05"]["outcome"] == "represented" and by_id["V6465-P05"]["real_keys_or_transactions"] == 0,
        "cbr_exact_gate": by_id["V6465-P06"]["outcome"] == "exact_gate" and not by_id["V6465-P06"]["authority_delegated"],
        "citation_observation_nonconversion": sources["real_rows"] == sources["real_participants_or_animals"] == sources["real_keys_or_transactions"] == 0,
        "authority_not_delegated": sources["authority_delegated"] is False,
    }
    return {"schema": "ghc.family.v646-v5.source-gate.v1", "checks": checks, "passed": sum(checks.values()), "check_count": len(checks), "valid": all(checks.values()), "boundary": "Current official and primary sources constrain requirements and provenance only; citations are not observations, participants, transactions, or authority."}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"checks": result["check_count"], "passed": result["passed"], "valid": result["valid"]}))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
