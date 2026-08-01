#!/usr/bin/env python3
"""Phase constants for Sylven Arc's v658-v2 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v2_phase_catalogue import (
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


PHASE = "v658-v2"
PHASE_CODE = "V6582"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep each claim small enough to test, each failure visible, and every authority boundary intact"
BRANCH = "codex/GHC-Family/sylven-arc-v658-v2-full-tools"
PHASE_ROOT = "docs/sylven-arc/v658-v2"

SOURCE_OWNER = "Elowen Cairn"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v658-v1-full-tools"
SOURCE_INHERITED = "15857de0afd21f7432196bf71b2f53ab2f5504c9"
SOURCE_X1 = "6f42b9dc6fca6ffed17438030ce8c36bc2535846"
SOURCE_EVIDENCE = "dc89caf2989c9be4d62a64c59756fc167bf5c52a"
SOURCE_CLOSEOUT = "9009c83b898fe11c63a95e4e1153ad388f328d3f"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_ORIGINAL_FINAL = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = "d3aa6b08a8a6f80a9940a4ad9cc5993b61889c03d2a44eacedbc2ead0591fc8e"
SOURCE_ISOLATED_RECOVERY_SHA256 = "56ed52b7efb80ba9beea5f2d912be9714f94f68c736fd09174258123e36a91c9"
SOURCE_ROUTE_ACK_SHA256 = "5ce67e3ec50acfb098aed5aa227c7773cd28b925ad6a0af14e3f7f321f30db64"
SOURCE_ROUTE_STATE_GIT_BLOB = "bd54b702038745511d25fb6dfe4f0fefb945b2f1"
SOURCE_ROUTE_STATE_SHA256 = "7251d6303b4330be2593e0e00b64be552a3fd8629b6a4f95553991e786b65a2c"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "855248ede0afcef96737cfe4b1c66a0a092416038b7f3cbea5c402be5c54586a"

PRIOR_FROZEN = 2680
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 16657
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16657
SOURCE_EFFECTIVE_NEGATIVES = 16658
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "negative_id": "V6581-EXTERNAL-N01",
    "scope": "source_postseal_external_validation_recovery",
    "signature": "machine-enum-required-in-human-prose",
    "observed": "Elowen's sole canonical aggregate passed 152 scoped tests and 9 of 10 closeout tests but failed one prose assertion, so the aggregate retained zero credit.",
    "count": 1,
    "credit": 0,
    "retained": True,
    "repository_retained": False,
    "recovery": "Retain the failed aggregate and use one isolated dependency witness that checks the exact machine enum in JSON and equivalent meaning in prose without changing repository bytes or replaying successful checks.",
    "recurrence_guard": "Keep machine-enum assertions in machine-readable contracts and use semantic phrase checks for narrative documents.",
    "same_owner_only": True,
    "independent_reproduction": False,
}
SOURCE_OPEN_GAPS = 113
SOURCE_EXACT_GATES = 112
SOURCE_METHODS = 2931
SOURCE_FAILED_WITNESSES = 2931
SOURCE_PASSING_WITNESSES = 2931

PRIMARY_FOCUS = (
    "GMUT Mind through typed synthetic seismic-station metadata, response-stage, timing, sampling, spectral, "
    "covariance, forward-operator, inverse-identifiability, gauge, EFT, unit, provenance, and observation-firewall "
    "contracts, with THOS Body and Freed ID/CBR Heart explicit and every empirical, professional, legal, cultural, "
    "Māori-authority, affected-party, production, identity, privacy, accessibility, security, and Stage 20 gate preserved"
)
BOUNDED_PRACTICE = (
    "seismological station metadata stewardship, response documentation, correction review, alarm ownership, "
    "workload control, and shift handover used only as a synthetic software, formal, structural, and learning lens; "
    "no real person, land, station, sensor, datalogger, clock, channel, waveform, coordinate, calibration, installation, "
    "maintenance, processing, release, hazard decision, professional competence, employment, legal interpretation, "
    "cultural ratification, Māori authority, affected-party approval, or real-world outcome"
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
