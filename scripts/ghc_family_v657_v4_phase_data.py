#!/usr/bin/env python3
"""Phase constants for Sable Rook's v657-v4 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v4_phase_catalogue import (
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


PHASE = "v657-v4"
PHASE_CODE = "V6574"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational falsification-and-reproducibility steward"
HOPE = (
    "make every surviving claim easier to reproduce, challenge, or retract while "
    "safety, privacy, legal, cultural, and Māori-authority gates remain explicit"
)
BRANCH = "codex/GHC-Family/sable-rook-v657-v4-full-tools"
PHASE_ROOT = "docs/sable-rook/v657-v4"

SOURCE_OWNER = "Auren Lark"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v657-v3-full-tools"
SOURCE_X1 = "b40c2f04cd7e51ed9bc5c1174255e9e3d06af4e1"
SOURCE_EVIDENCE = "ecd67debfa384f7d4224a2600cc23a4744f8b0b5"
SOURCE_CLOSEOUT = "9953615057ffea7d9240e1deee25a959c89b600f"
SOURCE_ORIGINAL_FINAL = "e282db933e535759cc1f58975126d2bb0e1cf5fd"
SOURCE_FINAL = "e282db933e535759cc1f58975126d2bb0e1cf5fd"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "f4d50e0394f7228fda7c276673e0d5fe0494a7462ba438fbe836200dc2201417"
)
SOURCE_BATON_SHA256 = (
    "921b422de54bc1dc6802aa9621fec793fc65c1f29dda304f73e6b3bc784d2eb3"
)
SOURCE_BATON_CHECKOUT_SHA256 = (
    "eab0d6e66231f14da832e79f9e304be5e1adbd389f53a43f80998862e1ea33eb"
)

PRIOR_FROZEN = 2500
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 15605
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15608
SOURCE_EFFECTIVE_NEGATIVES = 15610
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "two-external-postfinal-readonly-operational-failures",
    "count": 2,
    "credit": 0,
    "repository_retained": False,
    "signatures": [
        "bounded-source-tail-probe-timeout-after-partial-output",
        "task-list-json-string-treated-as-object",
    ],
    "recovery": (
        "Preserve Auren's committed sealed total of 15,608, then add both external "
        "zero-credit read-only failures only to Sable's activation baseline of 15,610."
    ),
}
SOURCE_OPEN_GAPS = 107
SOURCE_EXACT_GATES = 106
SOURCE_METHODS = 1890
SOURCE_FAILED_WITNESSES = 1890
SOURCE_PASSING_WITNESSES = 1890

PRIMARY_FOCUS = (
    "GMUT Mind through bounded typed pipe-organ acoustic, wind-network, unit, continuity, "
    "covariance, conservation, stability, identifiability, and zero-row refusal contracts, "
    "with THOS Body and Freed ID/CBR Heart explicit"
)
BOUNDED_PRACTICE = (
    "heritage pipe-organ documentation, provenance review, conservation and service-state "
    "recording, correction, accessibility, readback, and handover used only as a synthetic "
    "software, formal, structural, and learning lens; no real organ, person, worship service, "
    "inspection, access at height, energization, measurement, tuning, cleaning, repair, "
    "restoration, return-to-service, heritage decision, craft competence, employment, "
    "qualification, legal interpretation, cultural ratification, Māori authority, or "
    "affected-party approval"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.727.4816.0"
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
