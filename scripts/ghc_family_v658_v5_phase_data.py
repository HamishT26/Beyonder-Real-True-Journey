#!/usr/bin/env python3
"""Phase constants for Elaren Kestrel's solo v658-v5 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v5_phase_catalogue import (
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


PHASE = "v658-v5"
PHASE_CODE = "V6585"
OWNER = "Elaren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational inference-assurance cartographer and evidence-boundary gardener"
HOPE = "make every probabilistic claim traceable, every computational doubt visible, and every scientific or community authority boundary unmistakable"
BRANCH = "codex/GHC-Family/elaren-kestrel-v658-v5-full-tools"
PHASE_ROOT = "docs/elaren-kestrel/v658-v5"

SOURCE_OWNER = "Eiren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v658-v4-full-tools"
SOURCE_INHERITED = "9c5f4c935d728f68b2ac612fa0affb4dfd389e05"
SOURCE_X1 = "1e1d8bf1368c5f8304ad732a8a904834dd215adf"
SOURCE_EVIDENCE = "f9000a0ac35ea632070570fddd93e9ba4364a4e2"
SOURCE_CLOSEOUT = "45c5eb1a5ca659f42ca13421c54025ad4bef8d41"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_CANONICAL_RECEIPT_SHA256 = "753a2eb38ae4e4a80fe605d7041866821dd245dda863c26022b586f4922f1103"
SOURCE_ROUTE_STATE_GIT_BLOB = "53f596b81fd79eaafb1087a44c90bcdd62ad18b8"
SOURCE_ROUTE_STATE_SHA256 = "16eec3d7949f6ed48c8ea2e2baaa77d10ceb087a56ebb1084f9f68af4c90757e"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "94d18478d2fe62e49f80f5f252b09347f92344a48d909e257047c439812b11d1"

PRIOR_FROZEN = 2770
SOURCE_EFFECTIVE_NEGATIVES = 17176
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 17176
SOURCE_OPEN_GAPS = 116
SOURCE_EXACT_GATES = 115
SOURCE_METHODS = 3450
SOURCE_FAILED_WITNESSES = 3450
SOURCE_PASSING_WITNESSES = 3450

PRIMARY_FOCUS = (
    "GMUT Mind through bounded synthetic pulsar-timing-array inference assurance: time and ephemeris lineage, timing-model "
    "design, white/chromatic/red/common noise, angular correlation alternatives, covariance and likelihood checks, prior "
    "support, MCMC diagnostics, posterior predictive checks, simulation-based calibration, injection recovery, and model "
    "comparison, with THOS Body, Freed ID, and CBR Heart explicit and every real-data, observatory, scientific-authority, "
    "legal, cultural, Māori-authority, affected-party, production, identity, privacy, accessibility, security, Theory-of-"
    "Everything, and Stage 20 gate preserved"
)
BOUNDED_PRACTICE = (
    "statistical astronomy, pulsar timing, Gaussian-process modelling, Bayesian workflow, research-software engineering, "
    "provenance, accessibility, and governance used only as a synthetic software, mathematical, structural, and learning "
    "lens; no real person, pulsar, observatory, telescope, backend, clock product, ephemeris file, time of arrival, timing "
    "solution, sky coordinate, dataset, chain, likelihood, Bayes factor, detection, astrophysical conclusion, publication, "
    "professional competence, employment, legal interpretation, cultural ratification, Māori authority, affected-party "
    "approval, production identity, or real-world outcome"
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
