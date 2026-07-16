#!/usr/bin/env python3
"""Family-current entrypoint for the v646-v5 disposable reftable fixture."""

import json
from pathlib import Path

from ghc_family_v646_v5_runtime import reftable_tribunal


if __name__ == "__main__":
    scratch = Path(__file__).resolve().parents[1] / ".ghc-family-runtime-v646-v5"
    result = reftable_tribunal(scratch)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    raise SystemExit(0 if result["passed"] else 1)
