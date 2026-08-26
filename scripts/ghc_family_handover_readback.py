"""Family-compatible synthetic collection-handover readback runner."""
from __future__ import annotations
import json
from scripts.ghc_family_sable_v670_v4_collection_handover import positive_fixture, validate_record
def run():
    row = positive_fixture("archival_reading_room")
    return validate_record(row)
if __name__ == "__main__": print(json.dumps(run(), sort_keys=True))
