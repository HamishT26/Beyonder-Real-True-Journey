#!/usr/bin/env python3
"""Narrow adapter for the GHC Family position and move-graph skill."""
from pathlib import Path
import importlib.util,json,os,sys
ALLOWED={"position_graph","move_tree"}
def core_path():
    for parent in Path(__file__).resolve().parents:
        candidate=parent/"scripts"/"ghc_family_chess_records_core.py"
        if candidate.is_file():return candidate
    root=os.environ.get("GHC_CHESS_RUNNER_ROOT")
    if root and (Path(root)/"ghc_family_chess_records_core.py").is_file():return Path(root)/"ghc_family_chess_records_core.py"
    raise SystemExit("CORE_NOT_FOUND")
def main():
    if len(sys.argv)!=2:raise SystemExit("usage: ghc_family_chess_record_skill.py FIXTURE.json")
    data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if data.get("operation") not in ALLOWED:print(json.dumps({"accepted":False,"error":"operation_not_allowed","allowed":sorted(ALLOWED)}));return 2
    path=core_path();spec=importlib.util.spec_from_file_location("ghc_chess_core",path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.evaluate(data);print(json.dumps(result,sort_keys=True));return 0 if result["accepted"] else 2
if __name__=="__main__":raise SystemExit(main())
