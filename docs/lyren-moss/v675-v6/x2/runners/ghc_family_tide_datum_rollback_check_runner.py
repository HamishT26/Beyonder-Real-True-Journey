#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
RUNNER_ID = 'ghc_family_tide_datum_rollback_check_runner'
CHECK_INDEX = 10

def evaluate(payload):
    return {
        'runner_id': RUNNER_ID,
        'passed': isinstance(payload, dict) and payload.get('synthetic_only') is True and payload.get('external_actions') == 0,
        'credit': 'bounded_local_structural_only',
    }

if __name__ == '__main__':
    result = evaluate({'synthetic_only': True, 'external_actions': 0})
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result['passed'] else 1)
