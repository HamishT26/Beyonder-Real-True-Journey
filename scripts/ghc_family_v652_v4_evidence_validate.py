#!/usr/bin/env python3
"""Detailed bounded validator for Sylven Arc v652-v4 evidence."""
import argparse
import json
from collections import Counter
from pathlib import Path
import ghc_family_v652_v4_phase_data as d


def validate(root):
    checks = []
    def check(name, condition, detail):
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
    outcomes = []
    mutations = 0
    rejected = 0
    for proposal in d.PROPOSALS:
        target = root / "surfaces" / proposal["slug"]
        contract = json.loads((target / "contract.json").read_text(encoding="utf-8"))
        mutation = json.loads((target / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((target / "bounded-receipt.json").read_text(encoding="utf-8"))
        check(proposal["proposal_id"] + ":files", target.is_dir() and len(list(target.iterdir())) == 3, proposal["slug"])
        check(proposal["proposal_id"] + ":contract", len(contract["declared_obligations"]) >= 6, len(contract["declared_obligations"]))
        check(proposal["proposal_id"] + ":mutations", mutation["valid"] and mutation["count"] == 5, mutation["rejected_or_quarantined_count"])
        check(proposal["proposal_id"] + ":receipt", receipt["valid"] and receipt["observed_outcome"] == proposal["expected_disposition"], receipt["observed_outcome"])
        check(proposal["proposal_id"] + ":zero", all(value == 0 for value in receipt["real_world_counters"].values()), receipt["real_world_counters"])
        outcomes.append(receipt["observed_outcome"])
        mutations += mutation["count"]
        rejected += mutation["rejected_or_quarantined_count"]
    check("outcome_counts", Counter(outcomes) == Counter({"completed":23,"represented":5,"open_gap":1,"exact_gate":1}), dict(Counter(outcomes)))
    check("mutation_total", mutations == 150 and rejected == 150, {"mutations": mutations, "rejected": rejected})
    return {"schema":"ghc.family.v652-v4.detailed-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(row["passed"] for row in checks),"valid":all(row["passed"] for row in checks),"boundary":"Bounded same-owner software and synthetic evidence only."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate(args.phase_root)
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
