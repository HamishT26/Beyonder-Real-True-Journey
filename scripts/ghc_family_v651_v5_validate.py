#!/usr/bin/env python3
"""Validate all twenty v651-v5 bounded surfaces."""
from __future__ import annotations
import json
from ghc_family_v651_v5_runtime import validate_all
if __name__ == "__main__":
    print(json.dumps(validate_all()))
