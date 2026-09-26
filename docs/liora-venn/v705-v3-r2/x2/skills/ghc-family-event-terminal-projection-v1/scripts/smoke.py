from __future__ import annotations
import json,sys
from pathlib import Path
sys.dont_write_bytecode=True;PHASE=Path(__file__).resolve().parents[4];sys.path.insert(0,str(PHASE/"x2"/"code"));import event_workflow_x2 as ew
observation=ew.OPERATIONS["terminal_projection"](ew.load_fixtures()["LEW-01"]);print(json.dumps({"operation":"terminal_projection","observation_sha256":ew.x1.sha256_json(observation),"external_actions":0}))
