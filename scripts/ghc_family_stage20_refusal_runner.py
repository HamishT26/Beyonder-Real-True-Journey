from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v681-v5" / "x2"


def main() -> None:
    phase = json.loads((BASE / "phase-truth.json").read_text(encoding="utf-8"))
    positives = json.loads((BASE / "positive-controls.json").read_text(encoding="utf-8"))
    mutations = json.loads((BASE / "mutation-results.json").read_text(encoding="utf-8"))
    portfolio = json.loads((BASE / "portfolio-results.json").read_text(encoding="utf-8"))
    assert phase["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert positives["accepted"] == 60
    assert mutations["rejected"] == 300
    assert len(portfolio["safe_now"]) == 120
    print(json.dumps({"runner": "ghc_family_stage20_refusal_runner", "positive_controls": 60, "rejected_mutations": 300, "safe_now": 120, "real_rows": 0, "external_actions": 0}))


if __name__ == "__main__":
    main()
