#!/usr/bin/env python3
"""Generated family-current v651-v5 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v5_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6515-P08', 'V6515-P09', 'V6515-P10'], 'ghc_family_v651_v5_identity_and_authority.py'), ensure_ascii=False))
