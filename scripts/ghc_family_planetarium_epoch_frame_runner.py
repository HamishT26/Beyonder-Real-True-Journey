#!/usr/bin/env python3
"""ghc_family_planetarium_epoch_frame_runner: epoch and reference-frame nonconversion firewall; synthetic owner-local evidence only."""
from __future__ import annotations
import json
import sys
from ghc_family_planetarium_contract import validate_record


def main() -> None:
    record = json.load(sys.stdin)
    result = validate_record(record)
    result["focus"] = 'epoch and reference-frame nonconversion firewall'
    result["runner"] = 'ghc_family_planetarium_epoch_frame_runner'
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
