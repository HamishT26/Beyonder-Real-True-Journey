#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
paths = [
    ROOT / 'docs/legacy-reconstruction/analysis-report-latest.json',
    ROOT / 'docs/legacy-reconstruction/council-registry-latest.json',
    ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json',
    ROOT / 'docs/legacy-reconstruction/kairotic-detector-latest.json',
    ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json',
]
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'trinity_hybrid_adapter',
    'overall_status': 'PASS' if all(path.exists() for path in paths) else 'FAIL',
    'inputs_present': [str(path.relative_to(ROOT)) for path in paths if path.exists()],
}
target = ROOT / 'docs/legacy-reconstruction/trinity-hybrid-adapter-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
print('trinity_hybrid_adapter=' + payload['overall_status'])
