#!/usr/bin/env python3
"""Generated family-current v651-v5 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v5_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6515-P11', 'V6515-P12', 'V6515-P13', 'V6515-P18', 'V6515-P19', 'V6515-P20'], 'ghc_family_v651_v5_formats.py'), ensure_ascii=False))
