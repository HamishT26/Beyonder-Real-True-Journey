#!/usr/bin/env python3
"""Phase constants for Orin Thale's v657-v6 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v6_phase_catalogue import (
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


PHASE = "v657-v6"
PHASE_CODE = "V6576"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-boundary steward"
HOPE = "keep every claim traceable, falsifiable, and retractable"
BRANCH = "codex/GHC-Family/orin-thale-v657-v6-full-tools"
PHASE_ROOT = "docs/orin-thale/v657-v6"

SOURCE_OWNER = "Caelen Ash"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v657-v5-full-tools"
SOURCE_X1 = "7fdae81a188decacbee20c2f2c283b7104c0e91a"
SOURCE_EVIDENCE = "e2f0f3535f968e26fab748385c950cf4b7de085a"
SOURCE_CLOSEOUT = "7f68e945166e6bfb0680a1be83e935513b9768f4"
SOURCE_ORIGINAL_FINAL = "87815f96a372849dfb42a09d785515e858ea7925"
SOURCE_FINAL = "87815f96a372849dfb42a09d785515e858ea7925"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "c3cf95cb502c55213ecff19e3d8d1403888af15742f0c37d4b82d7bcdc157340"
)
SOURCE_BATON_SHA256 = (
    "754c5e24a14df7bbad2999f26245456867a8ab65edee495d93a525d9bf0b7149"
)
SOURCE_BATON_CHECKOUT_SHA256 = SOURCE_BATON_SHA256

PRIOR_FROZEN = 2560
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 15966
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15966
SOURCE_EFFECTIVE_NEGATIVES = 15966
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "no-external-postfinal-routing-failure",
    "count": 0,
    "credit": 0,
    "repository_retained": False,
    "signatures": [],
    "recovery": "No additional post-final route-preflight failure occurred before acknowledged activation.",
}
SOURCE_OPEN_GAPS = 109
SOURCE_EXACT_GATES = 108
SOURCE_METHODS = 2242
SOURCE_FAILED_WITNESSES = 2242
SOURCE_PASSING_WITNESSES = 2242

PRIMARY_FOCUS = (
    "GMUT Mind through typed forge thermal, heat-transfer, constitutive, dimensional, "
    "uncertainty, and observation-firewall obligations, with THOS Body and Freed ID/CBR "
    "Heart explicit and protected"
)
BOUNDED_PRACTICE = (
    "blacksmithing and forge job planning, workpiece and tooling provenance, thermal "
    "observation, hot-work holds, correction, accessibility, workload, readback, and shift "
    "handover used only as a synthetic software, formal, structural, and learning lens; no "
    "real person, forge, workpiece, alloy authentication, heat, flame, fuel, oxygen, tool, "
    "machine, electrical or gas system, measurement, treatment, inspection, safety release, "
    "professional competence, employment, legal interpretation, cultural ratification, "
    "Māori authority, affected-party approval, or real-world outcome"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.727.4816.0"
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
