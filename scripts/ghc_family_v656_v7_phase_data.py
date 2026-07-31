#!/usr/bin/env python3
"""Phase constants for Neris Solane's v656-v7 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v656_v7_phase_catalogue import (
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


PHASE = "v656-v7"
PHASE_CODE = "V6567"
OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "relational volcanic-observatory provenance steward"
HOPE = (
    "make synthetic monitoring records auditable and reversible while refusing "
    "to turn software structure into hazard advice or professional authority"
)
BRANCH = "codex/GHC-Family/neris-solane-v656-v7-full-tools"
PHASE_ROOT = "docs/neris-solane/v656-v7"

SOURCE_OWNER = "Elaren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v656-v6-full-tools"
SOURCE_X1 = "9c0227286b93672a4d98dba305e1c627a2300279"
SOURCE_EVIDENCE = "0744740cc17dfa57b0d151957d1edc7a2bb2c282"
SOURCE_CLOSEOUT = "7fd248f8322e5d8a6c8d8b02bdaa8eab3d5139b1"
SOURCE_ORIGINAL_FINAL = "778e3ca49c25a8aced6701258733f5e11c1b3a82"
SOURCE_FINAL = "7d0954ea088c9957cdcc81a07ef2c8b2d88997b3"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "3bed84c5d0faa3d9b33e5f4909939a33ee270443353a529009ab7d70a3551689"
)
SOURCE_BATON_SHA256 = (
    "427a8064a4ed8b9ef44617d27464a97a0f375b59a9dfb61b49336c7201d45bb9"
)

PRIOR_FROZEN = 2350
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 14729
SOURCE_EFFECTIVE_NEGATIVES = 14730
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "negative_id": "ELAREN-V656-V6-POSTFINAL-ROUTE-N01",
    "signature": "task-list-query-argument-rejection",
    "observed": (
        "A post-final task-list call rejected the unsupported query argument. "
        "The validated repository and its sealed register were not changed."
    ),
    "credit": 0,
    "retained": True,
    "overlay_only": True,
    "repository_rewritten": False,
}
SOURCE_OPEN_GAPS = 102
SOURCE_EXACT_GATES = 101
SOURCE_METHODS = 1015
SOURCE_FAILED_WITNESSES = 1015
SOURCE_PASSING_WITNESSES = 1015

PRIMARY_FOCUS = (
    "THOS Body through bounded volcanic-observatory monitoring, provenance, "
    "handover, incident, and recovery contracts, with GMUT Mind and Freed ID/CBR Heart explicit"
)
BOUNDED_PRACTICE = (
    "volcano-monitoring and observatory documentation used only as a synthetic "
    "software, formal, structural, and learning lens; no employment, qualification, "
    "fieldwork, hazard assessment, alert setting, eruption forecasting, aviation advice, "
    "emergency decision, legal interpretation, cultural ratification, Māori authority, "
    "or affected-party approval"
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
