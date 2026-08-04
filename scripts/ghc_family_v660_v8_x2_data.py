#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Auren Lark v660-v8."""

from __future__ import annotations

from ghc_family_v660_v8_data import *  # noqa: F401,F403
import ghc_family_v660_v8_data as x1


X1_FREEZE = "a456cadc82887ada7a963d08c04944e33d641522"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Auren x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = []
