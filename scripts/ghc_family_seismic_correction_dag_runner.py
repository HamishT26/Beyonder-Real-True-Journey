from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RUNNER_ID = "AL6741-RUNNER-007"
ASPECT = "correction_dag"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def validate(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_type"]
    errors: list[str] = []
    if payload.get("owner") != "Auren Lark":
        errors.append("owner")
    if payload.get("phase") != "v674-v1":
        errors.append("phase")
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_only")
    if payload.get("external_action") is not False:
        errors.append("external_action")
    if payload.get("authority_claim") is not False:
        errors.append("authority_claim")
    if payload.get("stage20") is not False:
        errors.append("stage20")
    if payload.get("outcome") not in ALLOWED:
        errors.append("outcome")
    if not re.fullmatch(r"SYN-STN-\d{3}", str(payload.get("station_surrogate", ""))):
        errors.append("station_surrogate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    errors = validate(payload)
    print(json.dumps({"runner_id": RUNNER_ID, "aspect": ASPECT, "accepted": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
