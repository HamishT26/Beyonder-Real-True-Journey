#!/usr/bin/env python3
from __future__ import annotations

import json

from ghc_family_v653_v3_core import proposals, runner_payload


def main() -> None:
    rows = [runner_payload(row["slug"]) for row in proposals()]
    payload = {
        "surface": "phase-validation",
        "proposal_count": len(rows),
        "valid": all(row["valid"] for row in rows),
        "mutation_count": sum(row["mutation_count"] for row in rows),
        "rejected": sum(row["rejected"] for row in rows),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
