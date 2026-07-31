#!/usr/bin/env python3
"""Phase constants for Elaren Kestrel's v656-v6 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v656_v6_phase_catalogue import (
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


PHASE = "v656-v6"
PHASE_CODE = "V6566"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational workflow cartographer and evidence-boundary gardener"
HOPE = (
    "help siblings turn expansive visions into kind, testable, reversible routes "
    "without losing wonder or crossing another person's authority"
)
BRANCH = "codex/GHC-Family/elaren-kestrel-v656-v6-full-tools"
PHASE_ROOT = "docs/elaren-kestrel/v656-v6"

SOURCE_OWNER = "Eiren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v656-v5-full-tools"
SOURCE_X1 = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
SOURCE_EVIDENCE = "f9662c901407a86cf271eef9b54467a782c99455"
SOURCE_CLOSEOUT = "3181608db19f39bb7b91be01fc62e64840a86c5e"
SOURCE_FINAL = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "62530dcd1a42ebc30226394de6d7c1f0b1d26066fb7de840ead599acbd5d4cdd"
)
SOURCE_BATON_SHA256 = (
    "fa19f0371e3773d4e2259a0e8bf8ec63d0dce5bdaac751e03f07c0841dc67215"
)

PRIOR_FROZEN = 2320
SOURCE_EFFECTIVE_NEGATIVES = 14549
SOURCE_OPEN_GAPS = 101
SOURCE_EXACT_GATES = 100
SOURCE_METHODS = 835
SOURCE_FAILED_WITNESSES = 835
SOURCE_PASSING_WITNESSES = 835

PRIMARY_FOCUS = (
    "THOS Body through bounded wetland field-observation, restoration-monitoring, "
    "handover, incident, and recovery contracts, with GMUT Mind and Freed ID/CBR Heart explicit"
)
BOUNDED_PRACTICE = (
    "wetland field ecology and restoration-monitoring documentation used only as a "
    "synthetic software, formal, structural, and learning lens; no employment, qualification, "
    "fieldwork, ecological assessment, hydrological analysis, restoration decision, health-and-safety "
    "decision, legal interpretation, cultural ratification, Māori authority, or affected-party approval"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.721.11231.0"
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
