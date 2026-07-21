#!/usr/bin/env python3
"""Generated family-current v651-v3 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v3_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute(['V6513-P11', 'V6513-P12', 'V6513-P13'], 'ghc_family_v651_v3_audio_formats.py'), ensure_ascii=False))
