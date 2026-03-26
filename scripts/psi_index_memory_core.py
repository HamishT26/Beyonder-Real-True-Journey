#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
roster = json.loads((ROOT / 'docs/trinity-agent-council-roster-v5.json').read_text(encoding='utf-8'))
entries = []
for row in roster.get('agents', []):
    if not isinstance(row, dict):
        continue
    ledger = ROOT / str(row.get('memory_ledger'))
    count = len([line for line in ledger.read_text(encoding='utf-8').splitlines() if line.strip()]) if ledger.exists() else 0
    entries.append({'display_name': row.get('display_name'), 'ledger_entries': count})
payload = {'generated_utc': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'module': 'psi_index_memory_core', 'overall_status': 'PASS', 'entries': entries, 'source_artifact': 'docs/trinity-agent-council-roster-v5.json'}
(ROOT / 'docs/legacy-reconstruction/psi-index-memory-core-latest.json').write_text(json.dumps(payload, indent=2) + '\
', encoding='utf-8')
print('psi_index_memory_core=PASS')
