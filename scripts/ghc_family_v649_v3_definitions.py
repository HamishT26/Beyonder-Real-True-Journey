#!/usr/bin/env python3
"""Frozen x1 definitions for Sable Rook v649-v3.

This module contains preregistration data only. It contains no x2 execution
result, empirical observation, participant result, or authority decision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ghc_family_v649_v3_phase_data import (
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    PROPOSALS,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    SOURCES,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v649-gmut-thos-v3-x1-x2"
PHASE_SHORT = "v649-v3"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-reproducibility steward"
HOPE = "keep every surviving claim easy to challenge or retract"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = (
    "community food-bank lot intake, allergen and recall hold, accessible distribution "
    "notice, correction readback, workload control, and shift handover"
)

SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_REVISION = "a801ebd12f89f0afdc224a65ea311239ad5a94ca"
SOURCE_INHERITED_REVISION = "26e61bc8161d29a229c362c9a6aefedbbd8b49f5"
SOURCE_X1_REVISION = "d20d13d2e17adbf35d0088fb38c66fab470a460f"
SOURCE_EVIDENCE_REVISION = "81059ca0db3c778d8f8bf1a7b12579b75ca24b98"
OWNED_BRANCH = "codex/GHC-Family/sable-rook-full-tools"

INHERITED_FROZEN_PROPOSALS = 660
INHERITED_SEALED_NEGATIVES = 4836
INHERITED_EXTERNAL_NEGATIVES = 4
INHERITED_EFFECTIVE_NEGATIVES = 4840
INHERITED_OPEN_GAPS = 36
INHERITED_EXACT_GATES = 37
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, scientific authority, "
    "operational authority, legal authority, cultural authority, Māori authority, or "
    "independent agency. Hamish may rename, pause, redirect, or stop the route."
)

GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, food-safety, legal, cultural, Māori-authority, "
    "identity, production, deployment, privacy-complete, proof or canon, destructive, "
    "account-secret, sibling-merge, accessibility-complete, exhaustive-security, "
    "independent-reproduction, AGI or ASI, consciousness or personhood, "
    "Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without "
    "exact evidence and authority. Māori concepts remain under Māori authority."
)

MUTATION_KINDS = [
    "missing_required_obligation",
    "invalid_domain_or_type",
    "silent_state_or_authority_promotion",
    "boundary_or_unit_erasure",
    "replay_lineage_or_generation_break",
    "resource_or_budget_violation",
    "forbidden_claim_promotion",
]


def synthetic_mutation_plan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal_row in PROPOSALS:
        proposal_number = int(proposal_row["proposal_id"].split("P")[-1])
        for index, kind in enumerate(MUTATION_KINDS, 1):
            rows.append(
                {
                    "mutation_id": f"V6493-MUT-P{proposal_number:02d}-{index:02d}",
                    "proposal_id": proposal_row["proposal_id"],
                    "kind": kind,
                    "status": "preregistered_not_executed",
                    "expected": "reject_or_quarantine",
                    "retained_negative_id": f"V6493-SYN-N-P{proposal_number:02d}-{index:02d}",
                }
            )
    return rows
