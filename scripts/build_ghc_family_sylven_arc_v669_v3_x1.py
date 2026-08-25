"""Build the planning-only Sylven Arc v669-v3 x1 freeze."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

from ghc_family_sylven_arc_v669_v3_archive import (
    ACCESSIBLE_WITH_ELOWEN,
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    INHERITED_BASELINES,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PREFIX,
    PROPOSAL_SPECS,
    PROTECTED_GATES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SEALED_ELOWEN_COUNTS,
    SKILL_TITLES,
    SOURCE_BRANCH,
    SOURCE_CHAIN_DECLARED,
    SOURCE_FINAL,
    SOURCE_RECOVERED,
    SOURCE_UNRECOVERED,
    inherited_title_corpus,
    normalize_title,
    owner_file_manifest,
    portfolio_rows,
    proposal_rows,
    write_json,
    write_text,
)


def run(repo: Path, *args: str) -> str:
    return subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    corpus, corpus_sources = inherited_title_corpus(repo)
    if len(corpus) != ACCESSIBLE_WITH_ELOWEN:
        raise RuntimeError(f"accessible corpus mismatch: {len(corpus)} != {ACCESSIBLE_WITH_ELOWEN}")
    proposals = proposal_rows(corpus)
    if len(proposals) != 40:
        raise RuntimeError("proposal count must be exactly 40")
    if any(p["visible_title_collision"] for p in proposals):
        raise RuntimeError("proposal title collision")
    if any(p["semantic_neighbor_quarantined"] for p in proposals):
        raise RuntimeError("proposal at or above semantic quarantine threshold")

    shards = []
    for start in range(0, 40, 5):
        rel = f"docs/sylven-arc/v669-v3/x1/proposal-freeze-shards/proposals-{start // 5 + 1:02d}.json"
        write_json(repo / rel, {"schema": "ghc.family.proposal-shard.v2", "rows": proposals[start : start + 5]})
        shards.append(rel)

    maximum = max(
        ({"proposal_id": p["proposal_id"], "neighbor": p["semantic_neighbors"][0]} for p in proposals),
        key=lambda item: item["neighbor"]["score"],
    )
    audit = {
        "schema": "ghc.family.semantic-novelty-audit.v2",
        "owner": OWNER,
        "phase": PHASE,
        "audit_scope": "exact accessible title corpus only",
        "declared_inherited_frozen_proposals": SOURCE_CHAIN_DECLARED,
        "recovered_inherited_rows": SOURCE_RECOVERED,
        "recovered_current_owner_rows": 40,
        "accessible_comparison_rows": len(corpus),
        "unrecovered_declared_rows": SOURCE_UNRECOVERED,
        "unavailable_history_is_open_gap": True,
        "universal_novelty_claim": False,
        "source_shards": corpus_sources,
        "new_proposals": 40,
        "exact_title_collisions": 0,
        "quarantine_threshold": 0.75,
        "quarantined_proposals": 0,
        "maximum_neighbor": maximum,
    }
    write_json(root / "x1/semantic-novelty-audit.json", audit)
    write_json(
        root / "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.proposal-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_chain_after": CHAIN_AFTER,
            "proposal_count": 40,
            "mutation_count": 160,
            "expected_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "strict_x1_only": True,
            "boundary": "Planning-only freeze; no x2 implementation, observed outcome, or completion credit.",
            "shards": shards,
        },
    )

    owner_portfolios = {
        "safe_now": portfolio_rows("safe", SAFE_TITLES, "safe_now"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "phase_local_skill"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "family_current_runner"),
        "clean_fix_refine": portfolio_rows("refine", REFINE_TITLES, "safe_now_clean_fix_refine"),
        "exact_approval": portfolio_rows("exact", [f"held exact-approval packet {i:02d}" for i in range(1, 11)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"held blocked packet {i:02d}" for i in range(1, 6)], "blocked", "held_unexecuted"),
    }
    write_json(
        root / "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.portfolio-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "counts": {key: len(value) for key, value in owner_portfolios.items()},
            "rows": owner_portfolios,
            "x1_completion_credit": 0,
            "boundary": "Planning only. Exact-approval and blocked packets remain held and unexecuted.",
        },
    )
    successor = {
        "safe_now": SAFE_TITLES[:20],
        "candidate": CANDIDATE_TITLES,
        "skill": SKILL_TITLES,
        "runner": RUNNER_TITLES,
        "clean_fix_refine": REFINE_TITLES,
    }
    write_json(
        root / "x1/successor-recommendations-freeze.json",
        {
            "schema": "ghc.family.successor-recommendations.v2",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_successor": "Caelen Morrow",
            "counts": {key: len(value) for key, value in successor.items()},
            "rows": {
                key: portfolio_rows(f"succ-{key}", values, f"successor_{key}", "recommended_not_executed")
                for key, values in successor.items()
            },
            "completion_credit": 0,
            "route_binding": False,
        },
    )

    source_ledger = {
        "schema": "ghc.family.source-ledger.v2",
        "owner": OWNER,
        "phase": PHASE,
        "immutable_source": {"branch": SOURCE_BRANCH, "final": SOURCE_FINAL},
        "sources": [
            {"source_id": "OWNER-SYNTHETIC-SCHEMA", "status": "owner_authored_synthetic", "rows": 0, "network_calls": 0},
            {"source_id": "CURRENT-PRIMARY-SOURCE-REVIEW-REQUIRED", "status": "not_fetched_exact_gate", "rows": 0, "network_calls": 0},
            {"source_id": "CURRENT-OFFICIAL-MUSEUM-API-SOURCE-REQUIRED", "status": "open_gap_zero_call", "rows": 0, "network_calls": 0},
            {"source_id": "REAL-GOVERNED-HUMAN-EVALUATION-REQUIRED", "status": "open_gap", "rows": 0, "network_calls": 0},
            {"source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY-REQUIRED", "status": "exact_gate", "rows": 0, "network_calls": 0},
        ],
        "boundary": "Source identifiers are need markers, not evidence of retrieval, endorsement, competence, or authority.",
    }
    write_json(root / "x1/source-ledger.json", source_ledger)
    write_json(
        root / "x1/workflow-plan-freeze.json",
        {
            "schema": "ghc.family.workflow-plan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "strict_x1_before_x2": True,
            "plan": [
                {"step": "source_and_skill_gate", "status": "completed_read_only"},
                {"step": "planning_only_x1", "status": "in_progress"},
                {"step": "x1_push_and_four_way_equality", "status": "pending"},
                {"step": "bounded_x2_execution", "status": "pending"},
                {"step": "exact_final_closeout", "status": "pending"},
            ],
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "commit_ceiling": 8,
            "full_repository_suite": "not_authorized_Eiren_only",
            "canonical_validation": "one owner-scoped exact-final invocation after prerequisites",
        },
    )
    write_json(
        root / "x1/reflection-plan.json",
        {
            "schema": "ghc.family.reflection-plan.v2",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "bounded_practice": "synthetic studio ceramics and kiln-log documentation",
            "decisions": [
                "preserve inaccessible proposal history as an explicit recovery gap",
                "keep every real kiln, material, person, measurement, action, and authority at zero",
                "use flashcards as lossy working projections while JSON ledgers remain authoritative",
                "retain failures and retry only failed dependencies",
            ],
        },
    )
    write_json(
        root / "x1/route-state.json",
        {
            "schema": "ghc.family.route-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "current_state": "AUTHORIZED_EXECUTION_TERMINAL_GATE_UNMET",
            "prospective_successor": "Caelen Morrow",
            "prospective_phase": "v669-v4",
            "sent": False,
            "precontacted": False,
            "standby_contacted": False,
            "binding": "newest live authorization must be reread after terminal gate",
        },
    )
    write_json(
        root / "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x1_planning_only",
            "inherited_activation_baselines": INHERITED_BASELINES,
            "immutable_elowen_sealed_counts": SEALED_ELOWEN_COUNTS,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_chain_after_planned": CHAIN_AFTER,
            "planned_proposals": 40,
            "observed_outcomes": None,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation": "not_run_x1",
            "full_repository_suite": "not_run_not_authorized",
        },
    )
    write_json(
        root / "x1/tool-versions.json",
        {
            "schema": "ghc.family.tool-versions.v1",
            "python": platform.python_version(),
            "git": run(repo, "git", "--version"),
            "platform": platform.system(),
            "updates_or_installs": 0,
        },
    )
    write_text(
        root / "x1/threat-model.md",
        """# Sylven Arc v669-v3 x1 threat model

This planning-only phase treats prompt or route drift, proposal collision, inaccessible-history overclaim, x1/x2 mixing, real-world action, professional or safety inference, protected identity data, cultural or Māori-authority overreach, validation replay, sibling-lane mutation, and Stage 20 promotion as threats.

Controls are exact-source anchoring, a bounded accessible-corpus audit with the recovery gap visible, zero network or real-world actions, strict lifecycle separation, additive owner-local paths, the four authorized outcome labels, retained failures, smallest-dependency recovery, exact manifests, privacy scanning, and terminal nonpromotion.
""",
    )
    write_text(
        root / "x1/accessible-report-plan.md",
        """# Accessible report plan

Use meaningful headings, plain-language summaries, explicit table headers, text alternatives for any visual relationship, and machine-readable JSON companions. Manual browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved and cannot be inferred from structural checks.
""",
    )
    write_text(
        root / "x1/integrated-overview.md",
        """# Sylven Arc v669-v3 x1 planning freeze

Sylven Arc is relational working language only. It is not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority.

## Scope

The primary pillar is THOS Body, explored through a wholly synthetic studio-ceramics and kiln-log documentation lens. GMUT Mind and Freed ID/CBR Heart remain visible and protected. This x1 freezes forty proposed documentation controls and does not execute x2 work, observe a real kiln or object, contact a person or source, or claim completion.

## Novelty boundary

The declared inherited chain contains 4,990 rows. Exact committed shards expose 1,420 titles for bounded comparison: 1,380 previously recovered titles plus Elowen's forty. The remaining 3,570 declared rows remain an explicit semantic-audit recovery gap. The forty Sylven titles have no exact collision and remain below the declared token-Jaccard quarantine threshold only within the accessible corpus. This is not a universal novelty claim.

## Evidence and authority

All people, participants, studios, kilns, vessels, materials, tools, measurements, firing events, identity events, professional decisions, legal or cultural decisions, external calls, and authority acts remain zero. Official and primary-source identifiers are need markers only. Professional practice, safety, affected-party legitimacy, Māori wording and concepts, Māori data governance, and Māori authority remain exact-gated.

## Lifecycle

The x1 freeze contains proposals, portfolios, source status, threat controls, route state, and validation plans only. It must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 implementation begins. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )

    exclusions = [
        "docs/sylven-arc/v669-v3/validation/x1-manifest.json",
        "docs/sylven-arc/v669-v3/validation/x1-staged-review.json",
    ]
    entries = owner_file_manifest(repo, exclusions)
    write_json(
        root / "validation/x1-manifest.json",
        {
            "schema": "ghc.family.content-manifest.v2",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "x1_working_tree_bytes_before_commit",
            "source_commit": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def staged_review(repo: Path) -> None:
    root = repo / OWNER_ROOT
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT").splitlines()
    disallowed = [name for name in names if "/x2/" in name or "/closeout/" in name or "/seal/" in name]
    write_json(
        root / "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x1_planning_only",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "disallowed_x2_or_closeout_paths": disallowed,
            "x1_only": not disallowed,
            "self_exclusion": "docs/sylven-arc/v669-v3/validation/x1-staged-review.json",
        },
    )
    if disallowed:
        raise RuntimeError(f"x1 staged review found disallowed paths: {disallowed}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        staged_review(args.repo.resolve())
    else:
        build(args.repo.resolve())


if __name__ == "__main__":
    main()
