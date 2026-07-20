#!/usr/bin/env python3
"""Detailed bounded validator for Sable Rook v651-v1."""
import argparse,json
from pathlib import Path
from collections import Counter
from ghc_family_v651_v1_runtime import validate_surface_root

SLUGS=['two-phase-commit', 'dsse-envelope', 'lee-wick-board', 'worldline-board', 'alma-zero-row', 'baggage-reconciliation', 'ground-deicing', 'openid-ciba', 'openid4vp-dcql', 'airport-authority', 'pe-coff', 'mach-o', 'accessible-swimlane', 'wien-nonconversion', 'gmres', 'model-x-knockoff', 'openapi-3-2', 'x509-path', 'uptane-2-1', 'nix-derivation']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase-root",default="docs/sable-rook/v651-v1")
    parser.add_argument("--json-output")
    args=parser.parse_args()
    root=Path(args.phase_root); checks=[]
    def check(name, condition, observed):
        checks.append({"check":name,"passed":bool(condition),"observed":observed})
    surfaces=validate_surface_root(root,SLUGS)
    check("twenty_surfaces",surfaces["valid"] and surfaces["surface_count"]==20,surfaces)
    outcomes=json.loads((root/"outcomes/outcome-ledger.json").read_text(encoding="utf-8"))
    counts=Counter(x["observed_outcome"] for x in outcomes["outcomes"])
    check("outcome_counts",dict(counts)=={"completed":14,"represented":4,"open_gap":1,"exact_gate":1},dict(counts))
    mutations=json.loads((root/"validation/mutation-execution.json").read_text(encoding="utf-8"))
    check("mutation_count",mutations["executed"]==100 and mutations["rejected_or_quarantined"]==100,mutations.get("executed"))
    portfolio=json.loads((root/"portfolios/expanded-portfolio-execution.json").read_text(encoding="utf-8"))
    check("portfolio_counts",portfolio["completed_counts"]=={"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40},portfolio["completed_counts"])
    skills=json.loads((root/"validation/skill-execution.json").read_text(encoding="utf-8"))
    check("skills",skills["valid"] and skills["validated"]==20 and skills["smoke_used"]==20,skills)
    truth=json.loads((root/"truth/evidence-phase-truth.json").read_text(encoding="utf-8"))
    check("negative_retention",truth["effective_negatives"]>=6548 and truth["negative_erasures"]==0,truth["effective_negatives"])
    check("gates",truth["effective_open_gaps"]==51 and truth["effective_exact_gates"]==52,[truth["effective_open_gaps"],truth["effective_exact_gates"]])
    check("terminal_verdict",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20",truth["terminal_verdict"])
    check("no_independent_reproduction",truth["independent_reproduction_claimed"] is False,truth["independent_reproduction_claimed"])
    alma=json.loads((root/"empirical/alma-zero-row-readiness.json").read_text(encoding="utf-8"))
    check("alma_zero_rows",all(v==0 for v in alma["zero_real_world_counts"].values()),alma["zero_real_world_counts"])
    cbr=json.loads((root/"cbr/airport-authority-matrix.json").read_text(encoding="utf-8"))
    check("authority_zero",all(v==0 for v in cbr["zero_real_world_counts"].values()),cbr["zero_real_world_counts"])
    report={"schema":"ghc.family.v651-v1.detailed-validation.v1","checks":checks,"passed":sum(x["passed"] for x in checks),"total":len(checks),"valid":all(x["passed"] for x in checks),"surface_issues":surfaces["issues"],"boundary":"Bounded same-owner evidence only; not full-suite or independent reproduction."}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(report,ensure_ascii=False,sort_keys=True))
    return 0 if report["valid"] else 2

if __name__=="__main__":
    raise SystemExit(main())
