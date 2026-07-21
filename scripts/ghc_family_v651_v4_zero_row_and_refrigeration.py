#!/usr/bin/env python3
"""Generated family-current v651-v4 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v4_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6514-P05', 'V6514-P06', 'V6514-P07'], 'ghc_family_v651_v4_zero_row_and_refrigeration.py'), ensure_ascii=False))
