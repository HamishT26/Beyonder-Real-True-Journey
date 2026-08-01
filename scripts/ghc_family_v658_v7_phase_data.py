#!/usr/bin/env python3
"""Phase constants for Vesper Arlen's solo v658-v7 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v7_phase_catalogue import (
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


PHASE = "v658-v7"
PHASE_CODE = "V6587"
OWNER = "Vesper Arlen"
PRONOUNS = "they/them"
ROLE = "relational aircraft-maintenance evidence custodian"
HOPE = "make synthetic maintenance records and handovers auditable without turning software structure into airworthiness or operational authority"
BRANCH = "codex/GHC-Family/vesper-arlen-v658-v7-full-tools"
PHASE_ROOT = "docs/vesper-arlen/v658-v7"

SOURCE_OWNER = "Neris Solane"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v658-v6-full-tools"
SOURCE_INHERITED = "1005e3b8d6a743ba8cb5a7000aa945a8be262c49"
SOURCE_X1 = "1591612c83feb7f47fb0b044525bf4b37f71bfb7"
SOURCE_EVIDENCE = "35ee24d2e708451e3862cbb81bc9103a691bd497"
SOURCE_CLOSEOUT = "26d90ff750269ee9aa84d520043f8c6096b69024"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_CANONICAL_RECEIPT_SHA256 = "8f3f749b37bc9e454d97363dd302bd2c7bc88a2f1c5047c7b51075e5d78b8f25"
SOURCE_ROUTE_STATE_GIT_BLOB = "353f50a03cfd2dab6768bb68bd01f6a4a6034abf"
SOURCE_ROUTE_STATE_SHA256 = "26e7d5b7ff727156f6c3bd8c9223295bb6ef7b0f7d7a56ea745d7cc3867bfa33"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "d881f16456919631a0adbde990d8a1ebff5e21b64b0b017e3b91926325f25213"

PRIOR_FROZEN = 2830
SOURCE_EFFECTIVE_NEGATIVES = 17496
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 17496
SOURCE_OPEN_GAPS = 118
SOURCE_EXACT_GATES = 117
SOURCE_METHODS = 3770
SOURCE_FAILED_WITNESSES = 3770
SOURCE_PASSING_WITNESSES = 3770

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic aircraft-maintenance record, configuration, tooling, part-provenance, inspection, "
    "functional-check, discrepancy, deferred-item, workload, and shift-handover controls, with a typed GMUT Mind fatigue and "
    "damage-operator firewall plus nonproduction Freed ID lineage and CBR Heart authority reservations; every real-aircraft, "
    "person, organisation, part, defect, measurement, maintenance, release-to-service, airworthiness, flight-safety, legal, "
    "cultural, Māori-authority, affected-party, production, identity, privacy, accessibility, security, Theory-of-Everything, "
    "and Stage 20 gate remains explicit"
)
BOUNDED_PRACTICE = (
    "aircraft-maintenance records, configuration control, task-card sequencing, tooling and part traceability, inspection and "
    "functional-check boundaries, deferred-item status, shift handover, bounded modelling, accessibility, and governance used "
    "only as a synthetic software, mathematical, structural, and learning lens; no real person, operator, organisation, "
    "aircraft, registration, flight, component, part, defect, measurement, tool, task, inspection, certification, release, "
    "airworthiness finding, safety advice, professional competence, employment, legal interpretation, cultural ratification, "
    "Māori authority, affected-party approval, production identity, or real-world outcome"
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
