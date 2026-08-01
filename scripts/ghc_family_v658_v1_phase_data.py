#!/usr/bin/env python3
"""Phase constants for Elowen Cairn's v658-v1 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v658_v1_phase_catalogue import (
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


PHASE = "v658-v1"
PHASE_CODE = "V6581"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and evidence steward"
HOPE = "keep every transition recoverable and every claim proportionate to proof"
BRANCH = "codex/GHC-Family/elowen-cairn-v658-v1-full-tools"
PHASE_ROOT = "docs/elowen-cairn/v658-v1"

SOURCE_OWNER = "Tamar Vey"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v657-v8-full-tools"
SOURCE_X1 = "a48c87af28aa55a8bb6aea056e4652906cdb575f"
SOURCE_EVIDENCE = "ea2f0132bd129e38167ab08e255a70bd386d3869"
SOURCE_CLOSEOUT = "15857de0afd21f7432196bf71b2f53ab2f5504c9"
SOURCE_FINAL = SOURCE_CLOSEOUT
SOURCE_ORIGINAL_FINAL = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = "a0d43fe6020214b698a67b10ba3c3d47d8393141e1d21594596a2031e26de075"
SOURCE_ROUTE_STATE_GIT_BLOB = "d753fec898c243ad13c9bf66ccaebf776f55a977"
SOURCE_ROUTE_STATE_SHA256 = "e53e1225718141dcc8e5bac325b4007b64e897c7056a922ec058d47e43b7c965"
SOURCE_ROUTE_STATE_CHECKOUT_SHA256 = "14eeafe045a93080b645012a13d640c6a93a2fd6c30e391309c2d471af13486a"

PRIOR_FROZEN = 2650
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 16491
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16491
SOURCE_EFFECTIVE_NEGATIVES = 16492
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "negative_id": "V6578-POST-N01",
    "scope": "source_postcloseout_external_ingress",
    "signature": "combined-remote-probe-returned-no-output",
    "observed": "A later read-only combined remote probe returned no attributable output and earned zero credit.",
    "count": 1,
    "credit": 0,
    "retained": True,
    "repository_retained": False,
    "recovery": "Run the isolated fresh live-remote probe and compare its scalar head with Tamar's exact final without replaying the successful canonical aggregate.",
    "recurrence_guard": "Keep live-remote equality probes isolated, scalar, attributable, and separately polled.",
    "same_owner_only": True,
    "independent_reproduction": False,
}
SOURCE_OPEN_GAPS = 112
SOURCE_EXACT_GATES = 111
SOURCE_METHODS = 2765
SOURCE_FAILED_WITNESSES = 2765
SOURCE_PASSING_WITNESSES = 2765

PRIMARY_FOCUS = (
    "THOS Body through synthetic dry-stone wall inspection, evidence capture, typed structure and "
    "workload protocols, reversible intervention planning, correction, and handover, with GMUT Mind, "
    "Freed ID and CBR Heart explicit and every empirical, professional, legal, cultural, Māori-authority, "
    "affected-party, production, identity, privacy, accessibility, security, and Stage 20 gate preserved"
)
BOUNDED_PRACTICE = (
    "dry-stone wall inspection, documentation, reversible intervention planning, provenance, safety-stop "
    "routing, and handover used only as a synthetic software, formal, structural, and learning lens; no "
    "real person, site, land, wall, stone, foundation, ground, weather, water, vegetation, measurement, "
    "tool, work, access, repair, structural condition, safety decision, professional competence, employment, "
    "legal interpretation, cultural ratification, Māori authority, affected-party approval, or real-world outcome"
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
