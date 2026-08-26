"""Family-compatible bounded synthetic bicycle-share runner."""

from __future__ import annotations

import json

RUNNER = "ghc_family_bikeshare_accessible_notice"


def run() -> dict[str, object]:
    return {
        "schema": "ghc.family.bikeshare-runner-receipt.v1",
        "runner": RUNNER,
        "accepted": True,
        "synthetic": True,
        "real_people": 0,
        "real_assets": 0,
        "external_actions": 0,
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True))
