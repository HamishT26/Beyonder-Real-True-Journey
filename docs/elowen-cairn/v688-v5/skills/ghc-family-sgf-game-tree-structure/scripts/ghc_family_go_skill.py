#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ghc_family_go_sgf_core as core
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args()
try: result=core.evaluate(core.strict_loads(a.input.read_text(encoding='utf-8')))
except ValueError as exc: result=core.err(str(exc))
print(json.dumps(result,sort_keys=True,ensure_ascii=False))
raise SystemExit(0 if result['accepted'] else 2)
