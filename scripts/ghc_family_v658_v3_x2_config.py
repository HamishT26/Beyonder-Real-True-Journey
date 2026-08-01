#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Caelen Morrow v658-v3."""

from __future__ import annotations


SOURCE_COMMIT = "8b2ead4689da9455d8f41d8221286530278780cc"
X1_COMMIT = "333824da3d898fc3a281669de8ca5db6d0222dcc"
PHASE_ROOT = "docs/caelen-morrow/v658-v3"
SOURCE_EFFECTIVE_NEGATIVES = 16831
X1_OPERATIONAL_NEGATIVES = 19
SOURCE_OPEN_GAPS = 114
SOURCE_EXACT_GATES = 113
SOURCE_METHODS = 3105
X1_METHODS = 19
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}


X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6583-X2-N01",
        "slug": "stale-scanner-self-match-validity-inconsistency",
        "failure_signature": "The first x2 build matched the stale-label scanner's own pattern definition, wrote an invalid stale-label receipt, but still marked the top-level evidence receipt valid; the whole attempt earned zero aggregate credit.",
        "candidate_workaround": "Classify the builder's scanner-definition self-match as a declared scanner false positive, require zero confirmed stale paths, and bind top-level validity to that gate.",
        "recurrence_guard": "Separate raw scanner hits from confirmed stale labels and make every component validity state a prerequisite of the aggregate receipt.",
        "fail_procedure": "Run the first evidence builder with an undifferentiated scanner over its own pattern source.",
        "fail_observed": "One scanner self-hit was written as confirmed while the aggregate remained valid; no commit, network call, authority action, or external mutation occurred.",
        "pass_procedure": "Exclude only the exact scanner-definition file from confirmed-label classification, record the false positive, and require the corrected component receipt to be valid before aggregate success.",
        "pass_observed": "The corrected stale-label gate reports zero confirmed stale paths and the aggregate validity is bound to that result.",
        "scope_boundary": "Owner-local validation-consistency recovery only; no completion, professional, legal, cultural, route, or authority credit.",
    },
]
