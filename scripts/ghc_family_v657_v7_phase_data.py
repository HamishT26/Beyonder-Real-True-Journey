#!/usr/bin/env python3
"""Phase constants for Liora Venn's v657-v7 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v7_phase_catalogue import (
    CANDIDATE_TASKS,
    CLEAN_TASKS,
    OFFICIAL_SOURCES,
    PROPOSALS,
    PROTECTED_GATES,
    RUNNER_SPECS,
    SAFE_TASKS,
    SKILL_SPECS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v657-v7"
PHASE_CODE = "V6577"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "relational continuity-and-evidence steward"
HOPE = (
    "make hidden control, accessibility, and handover failures easier to see "
    "without promoting synthetic structure into authority"
)
BRANCH = "codex/GHC-Family/liora-venn-v657-v7-full-tools"
PHASE_ROOT = "docs/liora-venn/v657-v7"

SOURCE_OWNER = "Orin Thale"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v657-v6-full-tools"
SOURCE_X1 = "f7161b026d270a131cc8449e75a7562fe04f0f66"
SOURCE_EVIDENCE = "a8b76a81a588e0cb7b64c3ec17f508151e349b7e"
SOURCE_CLOSEOUT = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
SOURCE_ORIGINAL_FINAL = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
SOURCE_FINAL = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "92a685c604f6dae0536ead0a8868722e7d3af2cb1f550c7f100806a35bfb0d23"
)
SOURCE_BATON_SHA256 = (
    "9456813e82a311c0afa73df22cb08c17f0ade1c04a180526d66a15c167e11160"
)
SOURCE_BATON_CHECKOUT_SHA256 = SOURCE_BATON_SHA256

PRIOR_FROZEN = 2590
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 16144
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16144
SOURCE_EFFECTIVE_NEGATIVES = 16145
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "V6576-POST-N01",
    "count": 1,
    "credit": 0,
    "repository_retained": False,
    "signatures": ["invalid-powershell-boolean-formatter-after-clean-equality-output"],
    "recovery": (
        "A scalar read-only recovery established FOUR_WAY_EQUAL=True, DIVERGENCE=0 0, "
        "and STATUS_ROWS=0. The fault remains external to Orin's sealed 16,144 count."
    ),
}
SOURCE_OPEN_GAPS = 110
SOURCE_EXACT_GATES = 109
SOURCE_METHODS = 2420
SOURCE_FAILED_WITNESSES = 2420
SOURCE_PASSING_WITNESSES = 2420

PRIMARY_FOCUS = (
    "GMUT Mind through typed geometric and wave-optics domains, diffraction, reflection, "
    "curvature, spectral response, uncertainty, covariance, identifiability, and observation-"
    "firewall obligations, with THOS Body and Freed ID/CBR Heart explicit and protected"
)
BOUNDED_PRACTICE = (
    "telescope-optics and observatory-instrument preparation, optic and instrument custody, "
    "alignment, coating, vacuum and energy holds, synthetic observation envelopes, correction, "
    "accessibility, workload, readback, and shift handover used only as a synthetic software, "
    "formal, structural, and learning lens; no real person, telescope, observatory, mirror, "
    "lens, filter, coating, laser, vacuum system, instrument, measurement, celestial observation, "
    "professional competence, safety release, employment, legal interpretation, cultural "
    "ratification, Māori authority, affected-party approval, or real-world outcome"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.727.6591.0"
CHATGPT_DESKTOP_VERSION = "1.2026.190.0"
GIT_VERSION = "git version 2.55.0.windows.2"
PYTHON_VERSION = "Python 3.12.10"
NODE_VERSION = "v24.18.0"

EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)
