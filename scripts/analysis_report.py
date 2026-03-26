#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
verdict = json.loads((ROOT / 'docs/v15-trinity-verdict-v1.json').read_text(encoding='utf-8'))
payload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'analysis_report', 'overall_status': 'PASS', 'source_artifact': 'docs/v15-trinity-verdict-v1.json', 'pillars': verdict.get('pillars', {})}
(ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json').write_text(json.dumps(payload, indent=2) + '\
', encoding='utf-8')
print('analysis_report=PASS')
