#!/usr/bin/env python3
from ghc_family_v650_v4_runtime import run_group

if __name__ == "__main__":
    raise SystemExit(0 if run_group(7)["passed"] else 1)
