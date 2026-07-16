#!/usr/bin/env python3
"""Run the bounded v646-v8 carousel structural audit."""
import json
from ghc_family_v646_v8_runtime import run

if __name__ == "__main__":
    result = run("V6468-P08")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)
