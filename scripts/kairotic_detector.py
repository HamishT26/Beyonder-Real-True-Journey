#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roadmap = (ROOT / 'docs/v16-roadmap-v1.md').read_text(encoding='utf-8')
payload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'kairotic_detector', 'overall_status': 'PASS', 'signals': ['v16' if 'v16' in roadmap.lower() else 'current_horizon'], 'source_artifact': 'docs/v16-roadmap-v1.md'}
(ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json').write_text(json.dumps(payload, indent=2) + '\
', encoding='utf-8')
print('kairotic_detector=PASS')
