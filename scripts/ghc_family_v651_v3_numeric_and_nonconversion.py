#!/usr/bin/env python3
"""Generated family-current v651-v3 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v3_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6513-P15', 'V6513-P16', 'V6513-P18', 'V6513-P19', 'V6513-P20'], 'ghc_family_v651_v3_numeric_and_nonconversion.py'), ensure_ascii=False))
