"""Family-compatible synthetic collection-custody runner."""
from __future__ import annotations
import json
from scripts.ghc_family_sable_v670_v4_collection_handover import positive_fixture, validate_record
def run(): return validate_record(positive_fixture())
if __name__ == "__main__": print(json.dumps(run(), sort_keys=True))
