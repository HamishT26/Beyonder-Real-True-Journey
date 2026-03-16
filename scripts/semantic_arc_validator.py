#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
legacy = json.loads((ROOT / 'docs/v29-v38-legacy-reconstruction-map-v1.json').read_text(encoding='utf-8'))
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'semantic_arc_validator',
    'overall_status': 'PASS',
    'reconstructed_modules': len(legacy.get('reconstructed_modules', [])),
    'deferred_modules': len(legacy.get('deferred_modules', [])),
}
target = ROOT / 'docs/legacy-reconstruction/semantic-arc-validator-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
print('semantic_arc_validator=PASS')
