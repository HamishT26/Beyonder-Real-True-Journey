#!/usr/bin/env python3
"""Final lifecycle constants for Elaren v656-v6."""

from __future__ import annotations


SOURCE_COMMIT = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
X1_COMMIT = "9c0227286b93672a4d98dba305e1c627a2300279"
EVIDENCE_COMMIT = "0744740cc17dfa57b0d151957d1edc7a2bb2c282"
CLOSEOUT_COMMIT = "7fd248f8322e5d8a6c8d8b02bdaa8eab3d5139b1"
CLOSEOUT_EFFECTIVE_NEGATIVES = 14725
CLOSEOUT_EFFECTIVE_METHODS = 1011
OPEN_GAPS = 102
EXACT_GATES = 101
FINAL_PREPARATION_NEGATIVES = [
    {
        "negative_id": "V6566-X2-N27",
        "slug": "absent-successor-named-test-module",
        "failure_signature": "The bounded search found no existing Neris- or v656-v7-named test module and returned no matches.",
        "candidate_workaround": "Add one Elaren-owned successor-scope module that validates only the committed Neris baton, unsent route, and authority reservations.",
        "recurrence_guard": "Treat successor-scoped coverage as an explicit bounded route contract; never infer it from a nonexistent named module.",
        "fail_procedure": "Search existing test filenames for Neris or v656-v7 coverage.",
        "fail_observed": "No matching module existed, so the search returned nonzero and earned zero coverage credit.",
        "pass_procedure": "Run the additive Elaren successor-scope tests without contacting or acting for Neris.",
        "pass_observed": "The successor-scope module validated the prepared baton, unsent route, next edge, word cap, and protected authority boundaries.",
        "scope_boundary": "Elaren-owned route-contract coverage only; no Neris completion or authority credit.",
    }
]
