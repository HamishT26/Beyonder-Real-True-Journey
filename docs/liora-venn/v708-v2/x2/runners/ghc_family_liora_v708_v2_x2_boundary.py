#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for code_dir in (ROOT / "x1" / "code", ROOT / "x2" / "code"):
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))
import rough_set_x2 as domain

ALLOWED = ['correction_lineage', 'accessible_projection', 'authority_boundary']

parser = argparse.ArgumentParser()
parser.add_argument("--operation", required=True)
parser.add_argument("--table", required=True)
args = parser.parse_args()
if args.operation not in ALLOWED:
    raise SystemExit("outside_runner_scope")
table = json.loads(Path(args.table).read_text(encoding="utf-8"))
print(json.dumps(domain.dispatch(args.operation, table), ensure_ascii=False, sort_keys=True))
