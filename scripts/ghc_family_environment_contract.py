"""Family-compatible synthetic preservation-environment runner."""
from __future__ import annotations
import json
from scripts.ghc_family_sable_v670_v4_environment_contract import positive_fixture, validate_contract
def run(): return validate_contract(positive_fixture())
if __name__ == "__main__": print(json.dumps(run(), sort_keys=True))
