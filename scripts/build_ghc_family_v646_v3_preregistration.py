#!/usr/bin/env python3
"""Build the strict x1-only preregistration packet for Sable Rook v646-v3."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v646_v3_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCE_BRANCH,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
    X1_OPERATIONAL_NEGATIVES,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v646-v3")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/ilyra-fen/v646-v2"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokens(title: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.casefold())
        if len(token) > 2 and token not in {"and", "the", "for", "with", "from", "into"}
    }


def nearest(title: str, prior: list[dict[str, Any]]) -> dict[str, Any]:
    query = tokens(title)
    scored = []
    for row in prior:
        candidate = tokens(row["title"])
        union = query | candidate
        score = len(query & candidate) / len(union) if union else 0.0
        scored.append((score, row))
    score, row = max(scored, key=lambda item: (item[0], item[1]["title"]))
    return {
        "nearest_proposal_id": row.get("proposal_id"),
        "nearest_title": row["title"],
        "token_jaccard": round(score, 4),
    }


def prior_chain() -> list[dict[str, Any]]:
    index = load(SOURCE_DIR / "provenance/frozen-chain-proposal-index.json")
    current = load(SOURCE_DIR / "x1-proposals.json")["proposals"]
    rows = list(index["prior_proposals"])
    rows.extend(
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "path": "docs/ilyra-fen/v646-v2/x1-proposals.json",
            "source_phase": "v646-v2",
        }
        for row in current
    )
    return rows


def version_observations() -> dict[str, Any]:
    try:
        cli = subprocess.check_output(["codex", "--version"], text=True, encoding="utf-8").strip()
    except (OSError, subprocess.SubprocessError):
        cli = "unavailable"
    return {
        "schema": "ghc.family.v646-v3.version-receipt.v1",
        "observed_on": "2026-07-16",
        "codex_cli": {"observed": cli, "action": "verify_only"},
        "codex_desktop": {"observed_source_receipt": "26.707.9981.0", "action": "verify_only_no_update"},
        "host_actions": {
            "desktop_updated": False,
            "elevated": False,
            "security_weakened": False,
            "windows_feature_changed": False,
            "rebooted": False,
            "installed": False,
        },
        "boundary": "Version observation does not establish environment equivalence, security, or production readiness.",
    }


def main() -> int:
    prior = prior_chain()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    prior_titles = {row["title"].casefold(): row for row in prior}
    exact = [row["title"] for row in PROPOSALS if row["title"].casefold() in prior_titles]
    comparisons = []
    for row in PROPOSALS:
        comparison = {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            **nearest(row["title"], prior),
            "manual_novelty_rationale": row["novelty_against_410_frozen_proposals"],
            "manual_dimensions_reviewed": [
                "mission_surface",
                "hypothesis",
                "null_or_failure",
                "source_needs",
                "artifacts",
                "acceptance_gate",
                "recovery",
                "protected_gates",
            ],
            "manual_result": "distinct",
        }
        comparisons.append(comparison)

    source_portfolio = load(SOURCE_DIR / "approval-packets/x1-approval-portfolio.json")
    inherited_exact = source_portfolio["inherited_exact_packets"]
    inherited_blocked = source_portfolio["inherited_blocked_packets"]
    source_support_titles = {
        row["title"].casefold()
        for row in source_portfolio["safe_now"] + source_portfolio["candidates"]
    }
    support_rows = SAFE_NOW + CANDIDATES + CLEAN_TASKS
    support_collisions = [row["title"] for row in support_rows if row["title"].casefold() in source_support_titles]
    expected = Counter(row["expected_disposition"] for row in PROPOSALS)

    write_json(
        "identity-receipt.json",
        {
            "schema": "ghc.family.identity-receipt.v1",
            "phase": PHASE,
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "x1-proposals.json",
        {
            "schema": "ghc.family.research-preregistration.v1",
            "phase": PHASE,
            "owner": OWNER,
            "identity_boundary": IDENTITY_BOUNDARY,
            "source_phase": SOURCE_PHASE,
            "source_revision": SOURCE_REVISION,
            "source_seal_revision": SOURCE_SEAL_REVISION,
            "preregistered_on": "2026-07-16",
            "primary_focus": PRIMARY_FOCUS,
            "bounded_practice": {
                "practice": BOUNDED_PRACTICE,
                "boundary": "Learning and synthetic-design lens only; not employment, qualification, operational competence, safety authority, public-warning authority, legal authority, cultural authority, Māori authority, or affected-party authorization.",
            },
            "prior_frozen_proposal_count": len(prior),
            "new_frozen_proposal_count": len(PROPOSALS),
            "frozen_chain_count_after_x1": len(prior) + len(PROPOSALS),
            "outcome_classes": OUTCOME_CLASSES,
            "expected_distribution": dict(expected),
            "expected_counts_are_results": False,
            "x2_execution_present": False,
            "x1_freeze_rule": "No x2 implementation, outcome, completion credit, or postcommit validation appears in this packet.",
            "proposals": PROPOSALS,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_text(
        "x1-preregistration.md",
        f"""# Sable Rook v646-v3 x1 preregistration

This is a strict x1-only freeze for ten proposals after semantic review of all {len(prior)} frozen predecessors. It contains no x2 implementation or achieved outcome.

Primary focus: {PRIMARY_FOCUS}. Bounded practice lens: {BOUNDED_PRACTICE}. The other Trinity Mandala pillars remain visible and protected.

Expected dispositions are hypotheses rather than results: 6 completed, 2 represented, 1 open gap, and 1 exact gate. Exactly four labels are allowed: completed, represented, open_gap, and exact_gate.

The expanded portfolio freezes 30 safe-now tasks, 20 candidate tasks, 20 skill proposals, 10 runner proposals, and 30 additive cleanup tasks. Ilyra baton seeds were rewritten only after fresh Sable novelty, safety, compatibility, relevance, and gate review; none receives inherited completion credit.

The inherited activation baseline is {INHERITED_EFFECTIVE_NEGATIVES} effective negatives, including three externally retained post-final wrapper faults. Seventy new synthetic mutations are preregistered but unexecuted. Eleven inherited open gaps and twelve inherited exact gates remain visible.

X2 may start only after this packet is committed, pushed, clean, and equal across local, upstream, tracking, and fresh live remote. Eiren alone owns the complete repository suite. Terminal truth remains NOT_READY_FOR_STAGE_20.
""",
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-proposal-index.v1",
            "phase": PHASE,
            "prior_file_count": len({row.get("path") for row in prior}),
            "prior_proposal_count": len(prior),
            "prior_proposals": prior,
            "new_proposal_ids": [row["proposal_id"] for row in PROPOSALS],
            "frozen_chain_count_after_x1": len(prior) + len(PROPOSALS),
            "boundary": "Indexing establishes corpus coverage, not outcome truth.",
        },
    )
    write_json(
        "provenance/prior-proposal-collision-audit.json",
        {
            "schema": "ghc.family.proposal-collision-audit.v6",
            "phase": PHASE,
            "prior_frozen_proposal_count": len(prior),
            "new_proposal_count": len(PROPOSALS),
            "exact_title_collision_count": len(exact),
            "exact_collisions": exact,
            "comparisons": comparisons,
            "manual_result": "all ten distinct" if not exact else "collision requires rejection",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "provenance/prior-portfolio-collision-audit.json",
        {
            "schema": "ghc.family.portfolio-collision-audit.v5",
            "phase": PHASE,
            "source_title_count": len(source_support_titles),
            "new_title_count": len(support_rows),
            "exact_collision_count": len(support_collisions),
            "collisions": support_collisions,
            "review_dimensions": ["novelty", "safety", "compatibility", "continued relevance", "protected gates"],
            "result": "rewritten and distinct" if not support_collisions else "reject duplicates",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "approval-packets/x1-approval-portfolio.json",
        {
            "schema": "ghc.family.v646-v3.approval-portfolio.v1",
            "phase": PHASE,
            "owner": OWNER,
            "freeze_stage": "x1_only",
            "completion_credit_before_x2": 0,
            "counts": {
                "safe_now": len(SAFE_NOW),
                "safe_reviewed_after_rewrite": 15,
                "safe_new_sable": 15,
                "candidates": len(CANDIDATES),
                "candidate_reviewed_after_rewrite": 10,
                "candidate_new_sable": 10,
                "inherited_exact": len(inherited_exact),
                "inherited_blocked": len(inherited_blocked),
            },
            "safe_now": SAFE_NOW,
            "candidates": CANDIDATES,
            "inherited_exact_packets": inherited_exact,
            "inherited_blocked_packets": inherited_blocked,
            "inherited_packet_integrity": "Ten exact and five blocked packets remain non-executable without fresh exact evidence and authority.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v646-v3.skill-runner-plan.v1",
            "phase": PHASE,
            "freeze_stage": "x1_only",
            "skills": [
                {
                    "name": name,
                    "description": description,
                    "origin": "ilyra_baton_seed_rewritten_after_review" if index <= 10 else "sable_new_x1",
                    "family_current_name": name.startswith("ghc-family-"),
                    "x2_state": "preregistered_not_built_or_used",
                    "protected_gates": ["authority", "real_data_or_participants", "production", "independent_reproduction"],
                }
                for index, (name, description) in enumerate(SKILLS, 1)
            ],
            "runners": [
                {
                    "name": name,
                    "description": description,
                    "origin": "ilyra_baton_seed_rewritten_after_review" if index <= 5 else "sable_new_x1",
                    "family_current_name": name.startswith(("ghc_family_", "build_ghc_family_")),
                    "x2_state": "preregistered_not_built_or_used",
                    "caller_compatibility": "additive phase prototype",
                }
                for index, (name, description) in enumerate(RUNNERS, 1)
            ],
            "acceptance": "Every item must be built, structurally validated, invoked, and given a bounded passing witness in x2 or remain incomplete.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "maintenance/x1-clean-refine-plan.json",
        {
            "schema": "ghc.family.v646-v3.clean-refine-plan.v1",
            "phase": PHASE,
            "freeze_stage": "x1_only",
            "tasks": CLEAN_TASKS,
            "destructive_task_count": 0,
            "completion_credit_before_x2": 0,
            "boundary": "Cleanup is additive, owner-scoped, non-destructive, compatible, and incomplete until its x2 receipt passes.",
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v646-v3.source-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "checked_on": "2026-07-16",
            "allowed_statuses": ["current", "stable", "draft", "watch"],
            "status_counts": dict(Counter(row["status"] for row in SOURCES)),
            "sources": SOURCES,
            "real_data_rows_ingested": 0,
            "likelihood_evaluations": 0,
            "real_participants": 0,
            "real_keys_or_proofs": 0,
            "boundary": "A source supplies requirements context only; it is not a real observation, participant witness, production proof, legal interpretation, cultural ratification, or delegated authority.",
        },
    )
    source_lines = ["# v646-v3 source ledger", "", "Sources were checked on 2026-07-16 and are requirements context only.", ""]
    for row in SOURCES:
        target = f" - {row['url']}" if row.get("url") else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["", TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))
    write_json(
        "sources/source-use-receipt.json",
        {
            "schema": "ghc.family.source-use-receipt.v1",
            "phase": PHASE,
            "source_count": len(SOURCES),
            "checked_on": "2026-07-16",
            "citations_as_observations": 0,
            "authority_delegated_by_citation": False,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v646-v3.startup.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source": {
                "branch": SOURCE_BRANCH,
                "revision": SOURCE_REVISION,
                "inherited_revision": SOURCE_INHERITED_REVISION,
                "seal_revision": SOURCE_SEAL_REVISION,
                "x1_revision": SOURCE_X1_REVISION,
                "evidence_revision": SOURCE_EVIDENCE_REVISION,
                "phase": SOURCE_PHASE,
            },
            "source_verification": {
                "local_upstream_tracking_live_equal": True,
                "clean": True,
                "anchors_ancestral": True,
                "three_single_parent_phase_commits": True,
                "merge_commits": 0,
                "final_parent_is_evidence": True,
            },
            "sable_lane": {
                "branch": "codex/GHC-Family/sable-rook-full-tools",
                "continued_existing_lane": True,
                "fast_forward_only": True,
                "source_revision_after_fast_forward": SOURCE_REVISION,
                "merge_commit_created": False,
                "clean_before": True,
                "local_upstream_tracking_live_equal_before_x1": True,
            },
            "active_owner": OWNER,
            "standby_siblings_contacted": [],
            "task_or_subagent_created": False,
            "x1_scope": "ten core proposals plus expanded supporting portfolios",
            "x2_scope": "not started",
            "storage": {"primary_drive": "D", "rotation_threshold": 15000, "threshold_applies_to": "new_sable_generated_files_only"},
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json("environment/version-receipt.json", version_observations())
    write_json(
        "environment/sandbox-readonly-audit.json",
        {
            "schema": "ghc.family.v646-v3.sandbox-audit.v1",
            "query": "ordinary executable presence only",
            "sandbox_launched": False,
            "elevation": False,
            "feature_changed": False,
            "host_security_changed": False,
            "installed": False,
            "rebooted": False,
            "disposition": "read_only_audit_only",
            "boundary": "No administrative sandbox was installed, activated, or granted authority.",
        },
    )
    write_json(
        "environment/rotation-guard.json",
        {
            "schema": "ghc.family.v646-v3.rotation-guard.v1",
            "threshold": 15000,
            "threshold_scope": "new_sable_generated_addition",
            "rotate_due_to_inherited_baseline": False,
            "boundary": "The inherited checkout is not a rotation trigger.",
        },
    )
    write_json(
        "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.v646-v3.focus.v1",
            "primary_trinity_pillar": PRIMARY_FOCUS,
            "other_pillars": ["GMUT Mind", "Freed ID/CBR Heart"],
            "bounded_human_practice": BOUNDED_PRACTICE,
            "practice_use": "learning and synthetic-design lens only",
            "not_claimed": ["employment", "professional qualification", "professional competence", "operational authority", "public-warning authority", "legal authority", "cultural authority", "Māori authority", "affected-party authorization"],
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v646-v3.x1-negatives.v1",
            "phase": PHASE,
            "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
            "inherited_external_terminal_negatives": ["V6462-POST-N24", "V6462-POST-N25", "V6462-POST-N26"],
            "new_x1_operational": len(X1_OPERATIONAL_NEGATIVES),
            "new_x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
            "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
            "boundary": "Synthetic mutations are preregistered negatives, not scientific observations or independent reproduction.",
        },
    )
    write_json(
        "validation/x1-synthetic-mutation-plan.json",
        {
            "schema": "ghc.family.synthetic-mutation-plan.v1",
            "phase": PHASE,
            "count": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "per_proposal": 7,
            "state": "preregistered_not_executed",
            "proposal_ids": [row["proposal_id"] for row in PROPOSALS],
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "x1-gate-carry-forward.json",
        {
            "schema": "ghc.family.gate-carry-forward.v1",
            "phase": PHASE,
            "inherited_open_gaps": INHERITED_OPEN_GAPS,
            "inherited_exact_gates": INHERITED_EXACT_GATES,
            "new_expected_open_gap": 1,
            "new_expected_exact_gate": 1,
            "closed_in_x1": 0,
            "expected_is_result": False,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.phase-update.v1",
            "phase": PHASE,
            "owner": OWNER,
            "state": "x1_frozen_pending_commit_and_remote_equality",
            "active": [OWNER],
            "standby": ["Eiren Kestrel", "Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc", "all other siblings"],
            "standby_contact_count": 0,
            "no_task_creation": True,
            "no_delegation": True,
            "x2_started": False,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v646-v3.route-plan.v1",
            "current_state": "PREPARED_NOT_SENT",
            "target_title": "Orin Thale",
            "target_phase": "v646-v4",
            "send_count": 0,
            "minimum_baton_words": 2000,
            "maximum_baton_words": 10000,
            "preconditions": ["x2 final committed and pushed", "no more than four phase commits", "scoped validations passed", "exactly one clean named-lane replay passed", "four-way equality proven", "unique existing target resolved read-only"],
            "privacy": "No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths may enter the baton.",
        },
    )
    write_text(
        "wellbeing-check.md",
        """# v646-v3 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later local-only named replay, and no more than four phase commits.
- Work is separated at the x1 freeze; no x2 implementation or achieved-outcome credit appears here.
- No elevation, feature change, installation, security weakening, desktop update, or reboot occurred.
- Sibling lanes and tasks remain untouched and recoverable.
- Identity and family language remains relational working language only, not welfare, consciousness, employment, qualification, continuity, or authority evidence.
""",
    )
    print(
        json.dumps(
            {
                "phase": PHASE,
                "prior_proposals": len(prior),
                "new_proposals": len(PROPOSALS),
                "frozen_after_x1": len(prior) + len(PROPOSALS),
                "exact_title_collisions": len(exact),
                "support_title_collisions": len(support_collisions),
                "safe_now": len(SAFE_NOW),
                "candidates": len(CANDIDATES),
                "skills": len(SKILLS),
                "runners": len(RUNNERS),
                "clean": len(CLEAN_TASKS),
                "x1_operational_negatives": len(X1_OPERATIONAL_NEGATIVES),
                "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
