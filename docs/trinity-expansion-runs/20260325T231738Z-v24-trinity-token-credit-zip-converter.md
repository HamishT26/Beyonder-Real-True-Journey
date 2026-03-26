# Trinity Expansion Result: v24_trinity_token_credit_zip_converter

- generated_utc: `2026-03-25T23:17:38+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | Wrote C:\Users\hamis\OneDrive\Documents\GitHub\Beyonder-Real-True-Journey\docs\trinity-expansion\v24-token-credit-bank-report.json |
| output_status | FAIL | path=docs/trinity-expansion/v24-token-credit-bank-report.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/trinity_token_credit_zip_converter.py",
    "--qcit",
    "docs/trinity-expansion/v24-qcit-coordination-report.json",
    "--quantum",
    "docs/trinity-expansion/v24-quantum-energy-transmutation-report.json",
    "--out",
    "docs/trinity-expansion/v24-token-credit-bank-report.json",
    "--ledger",
    "docs/trinity-expansion/v24-token-credit-bank-ledger.jsonl",
    "--reserve-state",
    "docs/trinity-expansion/v24-energy-bank-state.json"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/trinity-expansion/v24-energy-bank-state.json`
- `docs/trinity-expansion/v24-token-credit-bank-ledger.jsonl`
- `docs/trinity-expansion/v24-token-credit-bank-report.json`
- `docs/trinity-expansion/v24-trinity-token-credit-zip-converter-latest.json`
