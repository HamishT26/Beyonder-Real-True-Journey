"""Family-compatible external-receipt state runner for Sable v670-v4."""
from __future__ import annotations
import json
from scripts.ghc_family_sable_v670_v4_evidence_guard import run_named_guard
def run(): return run_named_guard("external_receipt_state")
if __name__ == "__main__": print(json.dumps(run(), sort_keys=True))
