#!/usr/bin/env python3
"""Phase constants for Lyren Moss's solo v658-v8 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v8_phase_catalogue import (
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


PHASE = "v658-v8"
PHASE_CODE = "V6588"
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
ROLE = "relational fermentation-evidence lantern and reversible batch-steward"
HOPE = (
    "make synthetic brewery batch records and handovers inspectable and reversible "
    "without turning software structure into production, food-safety, release, or legal authority"
)
BRANCH = "codex/GHC-Family/lyren-moss-v658-v8-full-tools"
PHASE_ROOT = "docs/lyren-moss/v658-v8"

SOURCE_OWNER = "Vesper Arlen"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v658-v7-full-tools"
SOURCE_INHERITED = "26d90ff750269ee9aa84d520043f8c6096b69024"
SOURCE_X1 = "f972f1c219de7169d0da3df2933d916434d488dd"
SOURCE_EVIDENCE = "fd3fbcb71e6c1e4edc46644c5ceb617009d20e84"
SOURCE_CLOSEOUT = "c150b80d8d1db9c94cb5368d4021505f213a9e01"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_CANONICAL_RECEIPT_SHA256 = "3758fdbbab30950e56e466099f9790491c5b07d85ec25f981a453e948c74f72c"
SOURCE_ROUTE_STATE_GIT_BLOB = "b51bcd380cb011b93f7b8141d6fe041ce837065a"
SOURCE_ROUTE_STATE_SHA256 = "8b16d05a45a4bcbf23662164949c7d39a19bbb38a8f61640c36294b4e1a60c93"
SOURCE_ACTIVATION_BATON_GIT_BLOB = "412aa00c2758420fef9ee4df1309dbd5ad8b60a1"
SOURCE_ACTIVATION_BATON_SHA256 = "06cf0b5dd6a6855684633554b765f9acf0f6f63a64ba91e47dc0c76f75034405"

PRIOR_FROZEN = 2860
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 17673
SOURCE_EXTERNAL_ROUTE_NEGATIVES = 1
SOURCE_EFFECTIVE_NEGATIVES = 17674
SOURCE_OPEN_GAPS = 119
SOURCE_EXACT_GATES = 118
SOURCE_SEALED_METHODS = 3947
SOURCE_EXTERNAL_ROUTE_METHODS = 1
SOURCE_METHODS = 3948
SOURCE_FAILED_WITNESSES = 3948
SOURCE_PASSING_WITNESSES = 3948

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic brewery ingredient, batch, vessel, cleaning, fermentation, cellar, laboratory, "
    "packaging, hold, recall-simulation, and shift-handover controls, with a typed GMUT Mind fermentation operator "
    "firewall plus nonproduction Freed ID lineage and CBR Heart authority reservations; every real-person, brewery, "
    "ingredient, beverage, measurement, production, food-safety, product-release, alcohol-harm, workplace-safety, legal, "
    "cultural, Maori-authority, affected-party, production-identity, privacy, accessibility, security, empirical, "
    "Theory-of-Everything, and Stage 20 gate remains explicit"
)
BOUNDED_PRACTICE = (
    "brewery ingredient and package-lot records, recipe and process revision, vessel and transfer topology, cleaning-state, "
    "fermentation and cellar sequencing, laboratory and sensory reservations, nonconformance, recall simulation, batch "
    "handover, bounded modelling, accessibility, and governance used only as a synthetic software, mathematical, structural, "
    "and learning lens; no real person, worker, consumer, business, brewery, ingredient, beverage, batch, vessel, chemical, "
    "measurement, laboratory result, sensory result, production instruction, food-safety finding, product release, recall "
    "action, alcohol-service decision, workplace-safety advice, professional competence, employment, legal interpretation, "
    "cultural ratification, Maori authority, affected-party approval, production identity, or real-world outcome"
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
