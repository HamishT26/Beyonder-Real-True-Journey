#!/usr/bin/env python3
"""Closeout lifecycle constants for Neris v656-v7."""

from __future__ import annotations


SOURCE_COMMIT = "7d0954ea088c9957cdcc81a07ef2c8b2d88997b3"
X1_COMMIT = "f048a624daa5d6035cb01a485d74f43151cc4cd2"
EVIDENCE_COMMIT = "c91e45d9fcc7da6bb5160767c38cdd1167b3a88a"
EVIDENCE_EFFECTIVE_NEGATIVES = 14891
EVIDENCE_EFFECTIVE_METHODS = 1176
EVIDENCE_OPEN_GAPS = 103
EVIDENCE_EXACT_GATES = 102

# Append only failures actually observed after the immutable evidence commit.
POST_EVIDENCE_NEGATIVES: list[dict[str, str]] = []
