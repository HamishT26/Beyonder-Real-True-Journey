#!/usr/bin/env python3
"""Minimal bounded validator for Eiren Kestrel v652-v5 evidence."""
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
    method_count = negatives["x1_operational"] + negatives["x2_operational"]
    checks = {
        "proposal_count": outcomes["proposal_count"] == 30,
        "outcomes": outcomes["counts"] == {"completed":23,"represented":5,"open_gap":1,"exact_gate":1},
        "mutations": outcomes["mutation_count"] == 150 and outcomes["mutation_rejected_or_quarantined_count"] == 150,
        "negatives": negatives["effective_after_evidence"] == (
            negatives["inherited_effective"]
            + negatives["x1_operational"]
            + negatives["x2_operational"]
            + negatives["synthetic_mutations_executed_and_rejected_or_quarantined"]
        ),
        "gaps": gaps["effective_count"] == gaps["inherited_count"] + len(gaps["new"]),
        "gates": gates["effective_count"] == gates["inherited_count"] + len(gates["new"]),
        "methods": flow["counts"]["methods"] == method_count,
        "witnesses": flow["counts"]["witness_results"] == {"fail":method_count,"pass":method_count},
        "terminal": outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": outcomes["terminal_route"] == "PREPARED_NOT_SENT",
    }
    result = {"schema":"ghc.family.v652-v5.minimal-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(checks.values()),"valid":all(checks.values())}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
