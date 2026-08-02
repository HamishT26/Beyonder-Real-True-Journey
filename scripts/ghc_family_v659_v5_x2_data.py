#!/usr/bin/env python3
"""Additive x2-only truth overlay for Orin Thale v659-v5.

The frozen x1 data module remains immutable. Its unused, template-prefilled
``X2_FAILURES`` constant was never consumed by an x1 builder, test, receipt,
or truth artifact and is not evidence. X2 consumers import this overlay so
only failures actually observed after the pushed x1 boundary receive credit.
"""

from __future__ import annotations

from ghc_family_v659_v5_data import *  # noqa: F401,F403
import ghc_family_v659_v5_data as x1


X1_FREEZE = "17058d117f4f57c0b5a8e13e9046264499fbce62"
PREFILLED_X1_X2_FAILURES_IGNORED = tuple(x1.PREFILLED_X1_X2_FAILURES_IGNORED)

# Only post-freeze failures actually observed in Orin's owned lane receive x2
# Method Flow credit.  The inherited template rows remain visible through the
# explicit ignored-template collection above and are never reclassified.
X2_FAILURES: list[dict[str, object]] = [dict(row) for row in x1.X2_FAILURES]
