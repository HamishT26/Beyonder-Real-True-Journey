"""Family-current synthetic flag provenance_correction runner."""
from __future__ import annotations
import argparse
import json
from ghc_family_flag_contract import evaluate_contract

PROFILE = "provenance_correction"

def run(payload):
    return evaluate_contract(payload, PROFILE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=["valid", "invalid"], default="valid")
    args = parser.parse_args()
    payload = {"synthetic": args.fixture == "valid", "real_object": False, "external_actions": 0, "record_id": "SA6731-SMOKE", "vacancies": ["real_observation"], "authority_holds": ["professional", "legal", "cultural", "maori_authority"]}
    result = run(payload)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 2)

if __name__ == "__main__":
    main()
