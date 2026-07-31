#!/usr/bin/env python3
"""Final lifecycle constants for Lyren v657-v1."""

from __future__ import annotations


SOURCE_COMMIT = "a033d1318920de1beec288f9c5b27e7f73a8ff3b"
X1_COMMIT = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
EVIDENCE_COMMIT = "91c36c44b6ccecbf73892792e07525cc7577d0c8"
CLOSEOUT_COMMIT = "SET_AFTER_CLOSEOUT_COMMIT"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15246
CLOSEOUT_EFFECTIVE_METHODS = 1530
OPEN_GAPS = 105
EXACT_GATES = 104

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = []
