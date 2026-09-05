"""Recover only the three failed adverse package-smoke dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


def rejects(call: Callable[[], Any]) -> bool:
    try:
        call()
    except Exception:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--composite", type=Path, required=True)
    args = parser.parse_args()
    initial = json.loads(args.initial.read_text(encoding="utf-8"))
    if (
        initial["status"] != "FAIL"
        or initial["direct_package_count"] != 13
        or initial["positive_pass_count"] != 13
        or initial["adverse_rejection_count"] != 10
    ):
        raise SystemExit("initial package-smoke boundary changed")

    import cbor2
    from intervaltree import Interval, IntervalTree
    from more_itertools import one

    rows = [
        {
            "package": "intervaltree",
            "adverse": "reject a zero-length interval when inserted into a tree",
            "rejected": rejects(lambda: IntervalTree([Interval(1, 1, "invalid")])),
        },
        {
            "package": "more-itertools",
            "adverse": "reject an empty iterable where exactly one item is required",
            "rejected": rejects(lambda: one([])),
        },
        {
            "package": "cbor2",
            "adverse": "reject a truncated 32-bit integer payload",
            "rejected": rejects(lambda: cbor2.loads(bytes([0x1A]))),
        },
    ]
    passed = all(row["rejected"] for row in rows)
    recovery = {
        "schema": "ghc.family.elaren-v685-v7.package-smoke-recovery.v1",
        "status": "PASS" if passed else "FAIL",
        "isolated_dependency_count": 3,
        "rows": rows,
        "initial_aggregate_success_credit": 0,
        "initial_failure_retained": True,
        "unchanged_successes_replayed": False,
    }
    composite = {
        "schema": "ghc.family.elaren-v685-v7.package-smoke-composite.v1",
        "status": "PASS_DEPENDENCY_CORRECTED_COMPOSITE" if passed else "FAIL",
        "direct_package_count": 13,
        "positive_pass_count": initial["positive_pass_count"],
        "initial_adverse_rejection_count": initial["adverse_rejection_count"],
        "recovered_adverse_rejection_count": sum(row["rejected"] for row in rows),
        "effective_adverse_rejection_count": initial["adverse_rejection_count"] + sum(row["rejected"] for row in rows),
        "aggregate_success_credit": 0,
        "component_completion": passed,
        "same_owner_only": True,
        "production_or_exhaustive_security_claimed": False,
    }
    for path, payload in ((args.output, recovery), (args.composite, composite)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps({"status": composite["status"], "effective_adverse_rejections": composite["effective_adverse_rejection_count"], "unchanged_successes_replayed": False}, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
