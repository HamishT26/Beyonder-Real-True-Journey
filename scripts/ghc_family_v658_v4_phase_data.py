#!/usr/bin/env python3
"""Phase constants for Eiren Kestrel's solo v658-v4 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v4_phase_catalogue import (
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


PHASE = "v658-v4"
PHASE_CODE = "V6584"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational hydrometric evidence cartographer and correction steward"
HOPE = "make observation lineage legible while leaving water, land, safety, and authority decisions with competent and affected people"
BRANCH = "codex/GHC-Family/eiren-kestrel-v658-v4-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v658-v4"

SOURCE_OWNER = "Caelen Morrow"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v658-v3-full-tools"
SOURCE_INHERITED = "8b2ead4689da9455d8f41d8221286530278780cc"
SOURCE_X1 = "333824da3d898fc3a281669de8ca5db6d0222dcc"
SOURCE_EVIDENCE = "c8ab822b8498c525383d3f7dd66c4d55f803fe7c"
SOURCE_CLOSEOUT = "9c5f4c935d728f68b2ac612fa0affb4dfd389e05"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_CANONICAL_RECEIPT_SHA256 = "f8dea706fd199e0cc82459d0f52ced320ccb9cf56a4e602aee6b37afedf9ae48"
SOURCE_ROUTE_STATE_GIT_BLOB = "6297366abc6bd2e70a58dd06be3e8e45b0ff0b7e"
SOURCE_ROUTE_STATE_SHA256 = "efb9b0b766c63db04e8b6e73f27f1fb03e6bce4843928b4f5cc6c645a2c30061"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "0a4ca33b5904fb7b8ff95d00414f5b9813718b52eaefa7ced7fe1fbbd7ef6005"

PRIOR_FROZEN = 2740
SOURCE_EFFECTIVE_NEGATIVES = 17001
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 17001
SOURCE_OPEN_GAPS = 115
SOURCE_EXACT_GATES = 114
SOURCE_METHODS = 3275
SOURCE_FAILED_WITNESSES = 3275
SOURCE_PASSING_WITNESSES = 3275

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic hydrometric scope, station and sensor topology, observation lineage, datum, "
    "timebase, gauging computation, rating change, quality quarantine, correction, evidence relay, outage recovery, "
    "workload, readback, and handover contracts, with GMUT Mind, Freed ID, and CBR Heart explicit and every real-water, "
    "field-safety, professional, legal, cultural, Māori-authority, affected-party, production, identity, privacy, "
    "accessibility, security, and Stage 20 gate preserved"
)
BOUNDED_PRACTICE = (
    "hydrometric station documentation, water-level and streamflow observation metadata, rating and quality lineage, "
    "maintenance-event records, publication-state reservation, evidence relay, workload control, and shift handover "
    "used only as a synthetic software, formal, structural, and learning lens; no real person, river, stream, catchment, "
    "station, reach, control, benchmark, sensor, recorder, telemetry system, field note, measurement, survey, gauging, "
    "calibration, maintenance, repair, sampling, publication, forecast, site access, land or water decision, professional "
    "competence, employment, legal interpretation, cultural ratification, Māori authority, affected-party approval, "
    "or real-world outcome"
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
