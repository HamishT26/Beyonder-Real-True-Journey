from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_sylven_arc_v680_v5_contracts import mutate, positive_fixture, validate

freeze = json.loads((ROOT / "docs" / "sylven-arc" / "v680-v5" / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
proposal = freeze["proposals"][4]
positive = validate(proposal, positive_fixture(proposal))
invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
print(json.dumps({
    "authority_conferred": False,
    "invalid_reasons": invalid["reasons"],
    "invalid_rejected": not invalid["accepted"],
    "positive_accepted": positive["accepted"],
    "proposal_id": proposal["proposal_id"],
    "real_world_rows": 0,
}))
