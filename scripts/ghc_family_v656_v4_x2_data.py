#!/usr/bin/env python3
"""Mutable-by-addition x2 operational failure register for v656-v4."""

from __future__ import annotations


# Add only failures first observed after the immutable x1 gate. Never move an x1
# failure here and never delete an entry after a bounded recovery.
X2_OPERATIONAL_NEGATIVES: list[dict] = []
