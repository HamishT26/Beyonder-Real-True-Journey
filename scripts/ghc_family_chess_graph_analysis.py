#!/usr/bin/env python3
"""Family-current bounded chess-record runner."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ghc_family_chess_records_core as core
ALLOWED=["position_graph","move_tree","board_material","halfmove_timeline"]
def main():
    if len(sys.argv)!=2:raise SystemExit("usage: runner INPUT.json")
    payload=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if payload.get("operation") not in ALLOWED:
        result={"accepted":False,"error":"operation_group","value":None,"disposition":"completed","boundary":core.BOUNDARY}
    else:result=core.evaluate(payload)
    print(json.dumps(result,sort_keys=True))
    return 0 if result["accepted"] else 2
if __name__=="__main__":raise SystemExit(main())

