"""Select the metrology contracts from the shared laboratory."""
import argparse
import json
import sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repository",type=Path,required=True)
    ap.add_argument("--describe",action="store_true")
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    sys.path.insert(0,str(a.repository/"scripts"))
    from ghc_family_claim_evidence_lab import RULES, exercise
    families=["units","uncertainty","time","field","numeric"]
    if a.describe:
        result={"families":families,"criteria":sum(r["family"] in families for r in RULES),"mode":"description_only","execution_credit":0}
    else:
        if not a.output:
            ap.error("--output is required for execution")
        result=exercise(set(families))
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print(json.dumps({k:v for k,v in result.items() if k!="rows"}))
    return result.get("status","PASS")!="PASS"

if __name__=="__main__":
    raise SystemExit(main())
