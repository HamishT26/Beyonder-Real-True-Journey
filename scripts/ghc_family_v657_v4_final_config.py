#!/usr/bin/env python3
"""Final lifecycle constants for Sable Rook v657-v4."""

from __future__ import annotations


SOURCE_COMMIT = "e282db933e535759cc1f58975126d2bb0e1cf5fd"
X1_COMMIT = "d05c484a3324bab2f893d35ff4d10d7f0269c9e9"
EVIDENCE_COMMIT = "33f7bdce2ab8684395a75e7a1ce891b284e7502a"
CLOSEOUT_COMMIT = "93347a2f081ff2d0b356bb03a9c5c690274c3624"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15787
CLOSEOUT_EFFECTIVE_METHODS = 2067
OPEN_GAPS = 108
EXACT_GATES = 107

# No additional final-preparation failure was observed before this immutable
# final candidate was built. Later read-only or routing faults must be retained
# externally rather than rewriting a sealed final commit.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = []
