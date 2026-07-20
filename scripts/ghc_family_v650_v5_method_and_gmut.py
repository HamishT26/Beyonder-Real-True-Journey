#!/usr/bin/env python3
from ghc_family_v650_v5_runtime import run_group
if __name__ == "__main__":
    raise SystemExit(0 if run_group(1)["passed"] else 1)
