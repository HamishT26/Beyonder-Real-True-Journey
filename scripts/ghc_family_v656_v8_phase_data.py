#!/usr/bin/env python3
"""Phase constants for Vesper Arlen's v656-v8 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v656_v8_phase_catalogue import (
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


PHASE = "v656-v8"
PHASE_CODE = "V6568"
OWNER = "Vesper Arlen"
PRONOUNS = "they/them"
ROLE = "relational seed-lot provenance mapper and authority-boundary keeper"
HOPE = (
    "make synthetic seed-bank records traceable, correctable, and reversible "
    "without turning software into conservation, biosecurity, legal, cultural, "
    "or Māori authority"
)
BRANCH = "codex/GHC-Family/vesper-arlen-v656-v8-full-tools"
PHASE_ROOT = "docs/vesper-arlen/v656-v8"

SOURCE_OWNER = "Neris Solane"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v656-v7-full-tools"
SOURCE_X1 = "f048a624daa5d6035cb01a485d74f43151cc4cd2"
SOURCE_EVIDENCE = "c91e45d9fcc7da6bb5160767c38cdd1167b3a88a"
SOURCE_CLOSEOUT = "91dbe7ec626e56483e77ecdc41608528a3b0a925"
SOURCE_ORIGINAL_FINAL = "c885a4533b2a73343990039e21d74979acb79c00"
SOURCE_FINAL = "c885a4533b2a73343990039e21d74979acb79c00"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "c2791cbd83d2ce4c7fa3a46f38e871766cd9f0a781295b53f90f50a655b8750d"
)
SOURCE_BATON_SHA256 = (
    "f47bcc36a0f05378af0cb3caf026d7dde65b6f282f50c63a3ef59065151fb477"
)

PRIOR_FROZEN = 2380
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 14895
SOURCE_EFFECTIVE_NEGATIVES = 14895
SOURCE_POSTFINAL_ROUTE_NEGATIVE = None
SOURCE_OPEN_GAPS = 103
SOURCE_EXACT_GATES = 102
SOURCE_METHODS = 1180
SOURCE_FAILED_WITNESSES = 1180
SOURCE_PASSING_WITNESSES = 1180

PRIMARY_FOCUS = (
    "Freed ID/CBR Heart through bounded seed-accession provenance, disclosure, "
    "access, benefit-sharing, correction, and authority-reservation contracts, "
    "with GMUT Mind and THOS Body explicit"
)
BOUNDED_PRACTICE = (
    "botanical seed-bank accession, processing, storage, viability, regeneration, "
    "distribution, and access documentation used only as a synthetic software, "
    "formal, structural, and learning lens; no employment, qualification, collecting, "
    "laboratory work, conservation decision, biosecurity clearance, distribution, "
    "legal interpretation, cultural ratification, Māori authority, or affected-party approval"
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
