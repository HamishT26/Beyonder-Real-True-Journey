#!/usr/bin/env python3
"""Run only the bounded v646-v6 durable-outbox tribunal."""

from __future__ import annotations

import json

from ghc_family_v646_v6_runtime import surface_01


def main() -> int:
    result = surface_01()
    ok = len(result["mutations"]) == 7 and all(not row["accepted"] for row in result["mutations"])
    print(json.dumps({"proposal_id": result["proposal_id"], "rejected": len(result["mutations"]), "result": "pass" if ok else "fail"}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
