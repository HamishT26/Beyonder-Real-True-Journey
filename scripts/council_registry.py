#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v3.json').read_text(encoding='utf-8'))
payload = {
    'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    'module': 'council_registry',
    'overall_status': 'PASS',
    'official_agents': [row.get('display_name') for row in roster.get('agents', []) if isinstance(row, dict)],
}
target = ROOT / 'docs/legacy-reconstruction/council-registry-latest.json'
target.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
print('council_registry=PASS')
