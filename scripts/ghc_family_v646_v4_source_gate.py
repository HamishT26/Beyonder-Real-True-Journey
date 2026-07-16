#!/usr/bin/env python3
"""Check v646-v4 source status, zero-row locks, and authority gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = load("sources/source-ledger.json").get("sources", [])
    act = load("gmut/act-dr6-lensing-adapter-contract.json")
    recall = load("cbr/medicine-recall-authority-matrix.json")
    gates = load("exact-open-gate-register.json")
    checks = {
        "source_count_17": len(sources) == 17,
        "source_status_vocabulary": all(row.get("status") in {"current", "stable", "draft", "watch"} for row in sources),
        "act_zero_rows": act.get("rows_ingested") == 0,
        "act_zero_likelihoods": act.get("likelihood_evaluations") == 0,
        "act_zero_constraints": act.get("constraints_emitted", 0) == 0,
        "act_open_gap": act.get("outcome") == "open_gap",
        "recall_zero_real_decisions": recall.get("real_recalls") == 0 and all(not row.get("real_decision_made") for row in recall.get("dimensions", [])),
        "recall_exact_gate": recall.get("outcome") == "exact_gate",
        "no_silent_gate_closure": gates.get("closed_without_exact_evidence") == 0,
        "effective_gates_13_14": gates.get("effective_open_gaps") == 13 and gates.get("effective_exact_gates") == 14,
    }
    valid = all(checks.values())
    result = {
        "schema": "ghc.family.v646-v4.source-gate.v1", "checks": checks,
        "official_or_primary_sources_are_context_not_observations": True,
        "same_owner_only": True, "independent_reproduction": False, "passed": valid, "valid": valid,
        "boundary": "Source status and zero-row checks do not establish empirical GMUT evidence, health authority, legal effect, cultural legitimacy, or Māori authority.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
