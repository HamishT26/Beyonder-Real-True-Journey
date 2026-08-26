"""Family-compatible sparse-index materialization receipt runner."""
from __future__ import annotations
import json
from scripts.ghc_family_sable_v670_v4_evidence_guard import run_named_guard
def run(): return run_named_guard("sparse_index_receipt")
if __name__ == "__main__": print(json.dumps(run(), sort_keys=True))
