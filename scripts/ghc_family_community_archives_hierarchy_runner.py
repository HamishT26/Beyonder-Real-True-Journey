#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_community_archives_contract import runner_smoke

if __name__ == "__main__":
    result = runner_smoke(2)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["positive_accepted"] and result["invalid_rejected"] else 1)
