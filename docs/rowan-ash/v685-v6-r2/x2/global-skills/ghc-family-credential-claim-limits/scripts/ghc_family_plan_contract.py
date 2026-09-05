"""Validate an explicitly supplied owner plan without performing its tasks."""
import argparse
import json
from pathlib import Path

COUNTS = {"safe_now": 300, "candidates": 250, "clean_fix_refine": 300,
          "exact_packets": 50, "blocked_packets": 30}

def validate(plan):
    if not isinstance(plan, dict):
        return ["Expected an object"]
    errors = []
    identifiers = []
    for key, count in COUNTS.items():
        rows = plan.get(key)
        if not isinstance(rows, list) or len(rows) != count:
            errors.append(f"{key} requires {count} rows")
            continue
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("task_id", row.get("packet_id")), str):
                errors.append(f"{key} has a malformed row")
            else:
                identifiers.append(row.get("task_id", row.get("packet_id")))
    if len(identifiers) != len(set(identifiers)):
        errors.append("Task identifiers must be unique")
    if plan.get("destructive_cleanup_planned") is not False:
        errors.append("This plan authorizes additive projections only")
    return errors

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan", type=Path)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    try:
        errors = validate(json.loads(a.plan.read_text(encoding="utf-8")))
    except (ValueError, OSError) as exc:
        errors = [str(exc)]
    out = {"status": "PASS" if not errors else "FAIL", "issues": errors, "execution_credit": 0}
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print(json.dumps(out))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
