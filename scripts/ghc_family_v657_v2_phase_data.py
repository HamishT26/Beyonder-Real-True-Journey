#!/usr/bin/env python3
"""Phase constants for Ilyra Fen's v657-v2 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v2_phase_catalogue import (
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


PHASE = "v657-v2"
PHASE_CODE = "V6572"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward and reversible-handover cartographer"
HOPE = (
    "leave every vertical-transport maintenance claim traceable and every safety, "
    "accessibility, privacy, legal, cultural, and Māori-authority gate unmistakable"
)
BRANCH = "codex/GHC-Family/ilyra-fen-v657-v2-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v657-v2"

SOURCE_OWNER = "Lyren Moss"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v657-v1-full-tools"
SOURCE_X1 = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
SOURCE_EVIDENCE = "91c36c44b6ccecbf73892792e07525cc7577d0c8"
SOURCE_CLOSEOUT = "8ff8a0658e10e2ddec8db77bf1edb2fe9047fedb"
SOURCE_ORIGINAL_FINAL = "4d888c1387c4203bd21acd7156bed2b0a13f2bee"
SOURCE_FINAL = "4d888c1387c4203bd21acd7156bed2b0a13f2bee"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "77d3c9925b8dc993318ee575bc50294b1606005c58a73b94591c86343429e0a6"
)
SOURCE_BATON_SHA256 = (
    "1ca780ada7fc260842e6d2323a6cb32efb4fbd1aa68164cb0367c955af30438f"
)
SOURCE_BATON_CHECKOUT_SHA256 = (
    "bcebb87875ce1e66df32bbabea67188f4a307a4514bf3b615029287b8f0b424c"
)

PRIOR_FROZEN = 2440
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 15246
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15248
SOURCE_EFFECTIVE_NEGATIVES = 15248
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "no-additional-external-postfinal-negative-declared",
    "count": 0,
    "credit": 0,
    "repository_retained": False,
    "recovery": (
        "Use the committed final register's 15,248 effective total; its two final-"
        "preparation negatives are already repository-retained."
    ),
}
SOURCE_OPEN_GAPS = 105
SOURCE_EXACT_GATES = 104
SOURCE_METHODS = 1532
SOURCE_FAILED_WITNESSES = 1532
SOURCE_PASSING_WITNESSES = 1532

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic lift-maintenance work orders, isolation, "
    "inspection-state, accessibility, correction, workload, readback, and handover "
    "contracts, with GMUT Mind and Freed ID/CBR Heart explicit"
)
BOUNDED_PRACTICE = (
    "vertical-transport maintenance intake, asset and work-order provenance, hazardous-"
    "energy and out-of-service holds, component inspection-state recording, accessible "
    "notice, correction, workload, readback, and shift handover used only as a synthetic "
    "software, formal, structural, and learning lens; no employment, licensure, lift-"
    "mechanic qualification, inspection competence, maintenance authority, return-to-"
    "service decision, building-code determination, legal interpretation, cultural "
    "ratification, Māori authority, or affected-party approval"
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
