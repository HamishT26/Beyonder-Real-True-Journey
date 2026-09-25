#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT / "scripts"))
from ghc_family_coupled_uncertainty import ContractError,evaluate
ALLOWED=['accessible_summary', 'scene_coordinates']
try:
    request=json.load(sys.stdin) if len(sys.argv)==1 else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if request.get("op") not in ALLOWED: raise ContractError("operation outside this bounded runner")
    print(json.dumps({"ok":True,"result":evaluate(request)},sort_keys=True))
except Exception as exc:
    print(json.dumps({"ok":False,"error":str(exc)},sort_keys=True))
    raise SystemExit(2)
