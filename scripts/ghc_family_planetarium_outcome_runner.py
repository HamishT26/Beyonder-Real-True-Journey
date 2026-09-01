#!/usr/bin/env python3
"""ghc_family_planetarium_outcome_runner: four-label outcome vocabulary enforcement; synthetic owner-local evidence only."""
from __future__ import annotations
import json
import sys
from ghc_family_planetarium_contract import validate_record


def main() -> None:
    record = json.load(sys.stdin)
    result = validate_record(record)
    result["focus"] = 'four-label outcome vocabulary enforcement'
    result["runner"] = 'ghc_family_planetarium_outcome_runner'
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
