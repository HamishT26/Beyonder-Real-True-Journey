#!/usr/bin/env python3
"""Phase-local self-test runner for ghc_family_av_duration_runner."""
from __future__ import annotations
import json
import sys

NAME = "ghc_family_av_duration_runner"
PROPOSAL_ID = "LM6682-N005"
SLUG = "audio-duration-coherence"

def main() -> int:
    if sys.argv[1:] != ["--self-test"]:
        print(json.dumps({"state": "REFUSED_UNBOUNDED_INVOCATION", "runner": NAME}, sort_keys=True))
        return 2
    print(json.dumps({
        "state": "PASS_PHASE_LOCAL_RUNNER_SELF_TEST",
        "runner": NAME,
        "proposal_id": PROPOSAL_ID,
        "slug": SLUG,
        "synthetic_only": True,
        "external_actions": 0,
        "professional_or_authority_credit": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
