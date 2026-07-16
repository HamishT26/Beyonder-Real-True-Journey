#!/usr/bin/env python3
"""Validate v646-v6 source-to-evidence nonconversion and authority boundaries."""

from __future__ import annotations

import json
from pathlib import Path

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    source = load("sources/source-ledger.json")
    empirical = load("empirical/erosita-erass1-zero-row-receipt.json")["surface_summary"]
    thos = load("thos/hydrographic-handover-contract.json")
    freed = load("freed-id/dpop-binding-profile.json")
    cbr = load("cbr/navigation-chart-authority-reservation.json")
    checks = {
        "source_no_authority": source["authority_delegated"] is False,
        "erosita_zero_rows": empirical["real_rows"] == empirical["downloads"] == empirical["likelihood_calls"] == 0,
        "thos_zero_operations": thos["real_people"] == thos["real_vessels"] == thos["real_hazards"] == thos["real_notices"] == 0,
        "freed_zero_real_material": freed["private_keys"] == freed["real_tokens"] == freed["network_exchanges"] == 0,
        "cbr_no_decision": cbr["real_cases"] == cbr["decisions_made"] == 0 and cbr["authority_delegated"] is False,
    }
    receipt = {
        "schema": "ghc.family.v646-v6.source-gate.v1",
        "checks": checks,
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "result": "pass" if all(checks.values()) else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    path = PHASE / "sources/source-use-receipt.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=True))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
