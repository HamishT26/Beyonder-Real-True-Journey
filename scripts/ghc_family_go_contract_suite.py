#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ghc_family_go_sgf_core as core
ALLOWED={'position_digest', 'accessible_board', 'property_identifier', 'suicide_projection', 'simple_ko', 'text_escape', 'chain_component', 'time_record', 'variation_path', 'setup_partition', 'komi_rational', 'sgf_coordinate', 'authority_boundary', 'orthogonal_neighbors', 'move_sequence', 'liberty_frontier', 'game_tree_dag', 'record_evidence', 'capture_projection', 'result_token'}
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args()
try:
 payload=core.strict_loads(a.input.read_text(encoding='utf-8'))
 result=core.err('OPERATION_SCOPE') if not isinstance(payload,dict) or payload.get('operation') not in ALLOWED else core.evaluate(payload)
except ValueError as exc: result=core.err(str(exc))
print(json.dumps(result,sort_keys=True,ensure_ascii=False))
raise SystemExit(0 if result['accepted'] else 2)
