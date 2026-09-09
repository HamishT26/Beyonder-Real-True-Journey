#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from ghc_family_weave_draft_core import evaluate
ALLOWED=['tieup_matrix', 'treadling_sequence']
def main():
 p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,required=True); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
 request=json.loads(a.input.read_text(encoding="utf-8"))
 result=evaluate(request) if request.get("op") in ALLOWED else {"error":"E_OPERATION_SCOPE","ok":False,"value":None}
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
 raise SystemExit(0 if result["ok"] else 2)
if __name__=="__main__": main()
