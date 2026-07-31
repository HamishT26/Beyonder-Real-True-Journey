#!/usr/bin/env python3
"""Final lifecycle constants for Vesper v656-v8."""

from __future__ import annotations


SOURCE_COMMIT = "c885a4533b2a73343990039e21d74979acb79c00"
X1_COMMIT = "25c840c4e16a2b414dc6b51f5c529379eb244d1c"
EVIDENCE_COMMIT = "a721ae1ca74f3a0d5adc9149af5bb78fe9fc57bb"
CLOSEOUT_COMMIT = "SET_AFTER_CLOSEOUT_COMMIT"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15072
CLOSEOUT_EFFECTIVE_METHODS = 1357
OPEN_GAPS = 104
EXACT_GATES = 103

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = []
