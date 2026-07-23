#!/usr/bin/env python3
"""Minimal bounded validator for Sylven Arc v652-v4 evidence."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    outcomes = json.loads((args.phase_root / "evidence" / "proposal-outcomes.json").read_text(encoding="utf-8"))
    negatives = json.loads((args.phase_root / "truth" / "evidence-retained-negative-register.json").read_text(encoding="utf-8"))
    gaps = json.loads((args.phase_root / "truth" / "evidence-open-gap-register.json").read_text(encoding="utf-8"))
    gates = json.loads((args.phase_root / "truth" / "evidence-exact-gate-register.json").read_text(encoding="utf-8"))
    flow = json.loads((args.phase_root / "method-flow" / "evidence-method-flow-ledger.json").read_text(encoding="utf-8"))
    checks = {
        "proposal_count": outcomes["proposal_count"] == 30,
        "outcomes": outcomes["counts"] == {"completed":23,"represented":5,"open_gap":1,"exact_gate":1},
        "mutations": outcomes["mutation_count"] == 150 and outcomes["mutation_rejected_or_quarantined_count"] == 150,
        "negatives": negatives["effective_after_evidence"] == 8548,
        "gaps": gaps["effective_count"] == 65,
        "gates": gates["effective_count"] == 66,
        "methods": flow["counts"]["methods"] == 15,
        "witnesses": flow["counts"]["witness_results"] == {"fail":15,"pass":15},
        "terminal": outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": outcomes["terminal_route"] == "PREPARED_NOT_SENT",
    }
    result = {"schema":"ghc.family.v652-v4.minimal-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(checks.values()),"valid":all(checks.values())}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
