#!/usr/bin/env python3
from __future__ import annotations

import json

from ghc_family_v653_v8_core import runner_payload


def main() -> None:
    payload = runner_payload("extraction-batch-recall-lineage")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
