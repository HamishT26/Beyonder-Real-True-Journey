from __future__ import annotations
import json, sys
from pathlib import Path
PHASE=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(PHASE/"x1"/"code"))
import event_workflow as ew
fixture=ew.load_fixtures()["LEW-01"]
observation=ew.OPERATIONS["duplicate_guard"](fixture)
print(json.dumps({"operation":"duplicate_guard","observation_sha256":ew.sha256_json(observation),"external_actions":0}))
