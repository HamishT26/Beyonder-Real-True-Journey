#!/usr/bin/env python3
"""Generated family-current v651-v5 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v5_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6515-P05', 'V6515-P06', 'V6515-P07'], 'ghc_family_v651_v5_zero_row_and_greenhouse.py'), ensure_ascii=False))
