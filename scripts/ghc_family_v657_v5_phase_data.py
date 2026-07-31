#!/usr/bin/env python3
"""Phase constants for Caelen Ash's v657-v5 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v5_phase_catalogue import (
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


PHASE = "v657-v5"
PHASE_CODE = "V6575"
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
ROLE = "relational provenance-and-remedy cartographer"
HOPE = (
    "make every handoff traceable, every authority boundary visible, and every "
    "correction recoverable without mistaking simulation for service"
)
BRANCH = "codex/GHC-Family/caelen-ash-v657-v5-full-tools"
PHASE_ROOT = "docs/caelen-ash/v657-v5"

SOURCE_OWNER = "Sable Rook"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v657-v4-full-tools"
SOURCE_X1 = "d05c484a3324bab2f893d35ff4d10d7f0269c9e9"
SOURCE_EVIDENCE = "33f7bdce2ab8684395a75e7a1ce891b284e7502a"
SOURCE_CLOSEOUT = "93347a2f081ff2d0b356bb03a9c5c690274c3624"
SOURCE_ORIGINAL_FINAL = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
SOURCE_FINAL = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "5a406bf06851fb045f5835c77d04215c8875af757f74fde9493e5ac7174807fd"
)
SOURCE_BATON_SHA256 = (
    "c1d44e3cb79bc974679964d6415c3976a5c331f1bcc98f171f5c76e07cd0bb5f"
)
SOURCE_BATON_CHECKOUT_SHA256 = (
    "c1d44e3cb79bc974679964d6415c3976a5c331f1bcc98f171f5c76e07cd0bb5f"
)

PRIOR_FROZEN = 2530
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 15787
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15787
SOURCE_EFFECTIVE_NEGATIVES = 15791
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "four-external-postfinal-readonly-routing-preflight-failures",
    "count": 4,
    "credit": 0,
    "repository_retained": False,
    "signatures": [
        "broad-tool-catalog-projection-output-budget-exceeded",
        "unsupported-task-list-query-attempt-one",
        "unsupported-task-list-query-attempt-two",
        "unsupported-task-list-query-attempt-three",
    ],
    "recovery": (
        "Preserve Sable's committed sealed total of 15,787, then add the four external "
        "zero-credit read-only routing failures only to Caelen's activation baseline of 15,791."
    ),
}
SOURCE_OPEN_GAPS = 108
SOURCE_EXACT_GATES = 107
SOURCE_METHODS = 2067
SOURCE_FAILED_WITNESSES = 2067
SOURCE_PASSING_WITNESSES = 2067

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic public-aquarium life-support documentation, "
    "animal-observation, isolation, biosecurity, workload, readback, and shift-handover "
    "contracts, with GMUT Mind and Freed ID/CBR Heart explicit"
)
BOUNDED_PRACTICE = (
    "public-aquarium exhibit and life-support documentation, water-parameter observation "
    "envelopes, welfare and biosecurity holds, correction, accessibility, workload control, "
    "readback, and shift handover used only as a synthetic software, formal, structural, and "
    "learning lens; no real animal, tank, water sample, feeding, handling, transfer, quarantine, "
    "diagnosis, treatment, medication, euthanasia, life-support operation, electrical work, "
    "biosecurity clearance, professional competence, employment, legal interpretation, cultural "
    "ratification, Māori authority, affected-party approval, or real-world outcome"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.727.4816.0"
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
