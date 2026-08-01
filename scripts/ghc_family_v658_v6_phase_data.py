#!/usr/bin/env python3
"""Phase constants for Neris Solane's solo v658-v6 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v6_phase_catalogue import (
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


PHASE = "v658-v6"
PHASE_CODE = "V6586"
OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "relational volcanic-observatory provenance steward"
HOPE = "make synthetic monitoring and inference records auditable without turning software structure into scientific or operational authority"
BRANCH = "codex/GHC-Family/neris-solane-v658-v6-full-tools"
PHASE_ROOT = "docs/neris-solane/v658-v6"

SOURCE_OWNER = "Elaren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v658-v5-full-tools"
SOURCE_INHERITED = "45c5eb1a5ca659f42ca13421c54025ad4bef8d41"
SOURCE_X1 = "4de28e3fd9c9ed6b7205b3be62fcdb7938a2784b"
SOURCE_EVIDENCE = "aab5bc11331282186d1087283d0a3f96d9a1f270"
SOURCE_CLOSEOUT = "1005e3b8d6a743ba8cb5a7000aa945a8be262c49"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_CANONICAL_RECEIPT_SHA256 = "6b872e9a68016ead79ccdc7e52e5d29360fdef6ab37480f6a89b47140e1221db"
SOURCE_ROUTE_STATE_GIT_BLOB = "f6725991b9a16629cf1ef079fdc9b0ee44af22b4"
SOURCE_ROUTE_STATE_SHA256 = "1551a35af3814ff76e63ebef53c29e5dcc9bbe3761cdc87755e5a4f476a8e9a8"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "0dd45c9038fab707f59d4aad3f25da4dd057d39385c5f7eba5d1bd36a0d7811e"

PRIOR_FROZEN = 2800
SOURCE_EFFECTIVE_NEGATIVES = 17336
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 17336
SOURCE_OPEN_GAPS = 117
SOURCE_EXACT_GATES = 116
SOURCE_METHODS = 3610
SOURCE_FAILED_WITNESSES = 3610
SOURCE_PASSING_WITNESSES = 3610

PRIMARY_FOCUS = (
    "GMUT Mind through bounded synthetic volcanic-observatory monitoring provenance and model assurance: seismic and "
    "acoustic channels, GNSS and tilt, InSAR placeholders, volcanic-gas and geochemistry custody, thermal and visual "
    "observations, hydrothermal and meteorological covariates, multistream alignment, anomaly candidates, uncertainty, "
    "blinded synthetic unrest scenarios, and a typed forward-operator firewall, with THOS Body, Freed ID, and CBR Heart "
    "explicit and every real-data, hazard-message, scientific-authority, legal, cultural, Māori-authority, affected-party, "
    "production, identity, privacy, accessibility, security, Theory-of-Everything, and Stage 20 gate preserved"
)
BOUNDED_PRACTICE = (
    "volcano-monitoring vocabulary, sensor and sample provenance, bounded modelling, research-software engineering, "
    "accessibility, and governance used only as a synthetic software, mathematical, structural, and learning lens; no real "
    "person, maunga, volcano, observatory, station, instrument, image, sample, waveform, coordinate, location, observation, "
    "dataset, alert, forecast, diagnosis, eruption probability, hazard conclusion, public communication, publication, "
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
