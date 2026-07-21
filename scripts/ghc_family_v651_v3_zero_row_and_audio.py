#!/usr/bin/env python3
"""Generated family-current v651-v3 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v3_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6513-P05', 'V6513-P06', 'V6513-P07'], 'ghc_family_v651_v3_zero_row_and_audio.py'), ensure_ascii=False))
