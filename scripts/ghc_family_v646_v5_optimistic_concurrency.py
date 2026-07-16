#!/usr/bin/env python3
"""Family-current entrypoint for the v646-v5 optimistic-concurrency fixture."""

import json

from ghc_family_v646_v5_runtime import optimistic_concurrency


if __name__ == "__main__":
    result = optimistic_concurrency()
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    raise SystemExit(0 if result["passed"] else 1)
