#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Eiren Kestrel v662-v1."""

from __future__ import annotations

from ghc_family_v662_v1_data import *  # noqa: F401,F403
import ghc_family_v662_v1_data as x1


X1_FREEZE = "b0e059893c1fa594a8382d10cad6ac6c6a21d164"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Eiren x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6621-X2-N001",
        "signature": "first_combined_x2_build_received_a_nonzero_skill_validator_result_for_the_first_phase_local_skill",
        "recovery": "Retain the stopped aggregate at zero credit, rerun the exact quick validator only for ghc-family-footwear-pair-identity, require its attributable pass, and let the builder reuse the initialized phase-local skill without global installation.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6621-X2-N002",
        "signature": "second_combined_x2_build_reused_the_default_cp1252_child_validator_and_repeated_the_first_skill_failure",
        "recovery": "Retain the repeated stop, reproduce the exact no-UTF-8 child command to expose its UnicodeDecodeError, and launch both skill-creator child scripts with explicit Python UTF-8 mode before continuing.",
        "completion_credit": 0,
    },
]
