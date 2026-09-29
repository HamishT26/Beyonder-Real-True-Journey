from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location("liora_rough_set",ROOT/"x1"/"code"/"rough_set.py")
rs=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(rs)
ALLOWED=['lower_approximation', 'upper_approximation', 'regions', 'accuracy_membership', 'positive_dependency']
parser=argparse.ArgumentParser();parser.add_argument("--fixtures",required=True);parser.add_argument("--fixture-id",required=True);parser.add_argument("--operation",required=True);args=parser.parse_args()
if args.operation not in ALLOWED: raise SystemExit("unsupported_runner_operation")
envelope=json.loads(Path(args.fixtures).read_text(encoding="utf-8"));matches=[x for x in envelope["fixtures"] if x["fixture_id"]==args.fixture_id]
if len(matches)!=1: raise SystemExit("fixture_not_unique")
print(json.dumps({"fixture_id":args.fixture_id,"operation":args.operation,"result":rs.dispatch(args.operation,matches[0])},ensure_ascii=False,sort_keys=True))
