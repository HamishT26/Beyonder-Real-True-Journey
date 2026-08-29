from __future__ import annotations
import json
import sys

RUNNER_ID = 'ghc_family_synthetic_patch_sequence_guard'
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}

def validate(record: dict) -> list[str]:
    errors = []
    for key in ("config_id", "schema_version", "source_pointer", "provenance"):
        if not record.get(key):
            errors.append(f"missing_{key}")
    if record.get("synthetic_only") is not True:
        errors.append("synthetic_required")
    if record.get("real_world_action") is not False:
        errors.append("real_world_action_forbidden")
    if record.get("outcome") not in ALLOWED:
        errors.append("invalid_outcome")
    return errors

def main() -> int:
    record = {"config_id":"self-test","schema_version":1,"source_pointer":"invented","provenance":"invented","synthetic_only":True,"real_world_action":False,"outcome":"completed"}
    if len(sys.argv) == 2:
        record = json.loads(open(sys.argv[1], encoding="utf-8").read())
    errors = validate(record)
    print(json.dumps({"runner": RUNNER_ID, "passed": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
