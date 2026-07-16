#!/usr/bin/env python3
"""Run only the disposable v646-v6 JSON text-sequence tribunal."""

from __future__ import annotations

import json

from ghc_family_v646_v6_runtime import surface_07


def main() -> int:
    result = surface_07()
    contract = result["contract"]
    ok = len(contract["positive_records"]) == 2 and not contract["positive_failures"] and contract["disposable_fixture_removed"] and all(not row["accepted"] for row in result["mutations"])
    print(json.dumps({"proposal_id": result["proposal_id"], "records": len(contract["positive_records"]), "rejected": len(result["mutations"]), "result": "pass" if ok else "fail"}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
