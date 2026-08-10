#!/usr/bin/env python3
"""Build and validate the strict x1 freeze for Neris's v662-v3-2 remaster."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v662_v3_2_remaster_data as d
import ghc_family_v662_v3_2_remaster_runtime as rt


ROOT = rt.ROOT
PHASE = rt.PHASE
VALIDATION = PHASE / "validation"
X1_RECEIPTS = {
    f"{d.PHASE_ROOT}/validation/x1-content-manifest.json",
    f"{d.PHASE_ROOT}/validation/x1-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/x1-document-cap.json",
    f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
    f"{d.PHASE_ROOT}/validation/x1-validation.json",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_program() -> list[dict[str, Any]]:
    source = rt.read_json(ROOT / d.SOURCE_PHASE_ROOT / "final/final-proposal-ledger.json")
    rows = source.get("program", [])
    if len(rows) != 40:
        raise RuntimeError(f"expected 40 source program rows, observed {len(rows)}")
    selected_source = rows[-20:]
    selected = []
    for index, row in enumerate(selected_source, start=1):
        item = copy.deepcopy(row)
        item.update(
            {
                "proposal_id": f"V6623R-R{index:03d}",
                "source_proposal_id": row["proposal_id"],
                "origin": "selected_inherited_v662_v3_bounded_revalidation_no_credit",
                "append_to_frozen_chain": False,
                "expected_disposition": "selected_inherited_zero_credit",
                "novelty_credit": 0,
                "completion_credit": 0,
                "execution_lane": "x2_read_only_contract_revalidation",
                "concrete_artifacts": [f"evidence/selected-revalidation/v6623-p{index:03d}.json"],
            }
        )
        selected.append(item)
    return selected


def program() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected = source_program()
    new = [rt.make_new_proposal(index, spec) for index, spec in enumerate(d.NEW_PROPOSAL_SPECS, start=1)]
    return selected, new


def novelty_receipt(new: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_index = rt.read_json(ROOT / d.SOURCE_PHASE_ROOT / "provenance/frozen-chain-proposal-index.json")
    prior = list(source_index["prior_proposals"]) + list(source_index["new_proposals"])
    if len(prior) != d.FIRST_RUN_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.FIRST_RUN_FROZEN_PROPOSALS} inherited rows, observed {len(prior)}")
    prior_ids = {row["proposal_id"] for row in prior}
    prior_titles = {row["title"] for row in prior}
    exact_collisions = []
    similarity_rows = []
    for row in new:
        if row["proposal_id"] in prior_ids or row["title"] in prior_titles:
            exact_collisions.append(row["proposal_id"])
        best = max(
            (
                {"source_id": candidate["proposal_id"], "source_title": candidate["title"], "score": rt.jaccard(row["title"], candidate["title"])}
                for candidate in prior
            ),
            key=lambda candidate: candidate["score"],
        )
        similarity_rows.append({"proposal_id": row["proposal_id"], **best})
    duplicate_new_titles = [title for title, count in Counter(row["title"] for row in new).items() if count > 1]
    valid = not exact_collisions and not duplicate_new_titles and all(row["score"] < 0.8 for row in similarity_rows)
    receipt = {
        "schema": "ghc.family.v662-v3-2-remaster.novelty-audit.v1",
        "audited_inherited_rows": len(prior),
        "new_rows": len(new),
        "exact_collisions": exact_collisions,
        "duplicate_new_titles": duplicate_new_titles,
        "similarity_threshold": 0.8,
        "maximum_similarity": max(row["score"] for row in similarity_rows),
        "rows": similarity_rows,
        "valid": valid,
        "boundary": "Lexical and identifier novelty screen only; not scientific novelty, usefulness, correctness, or completion proof.",
    }
    frozen_index = {
        "schema": "ghc.family.frozen-chain-proposal-index.v1",
        "prior_count": len(prior),
        "prior_proposals": prior,
        "selected_inherited_count": 20,
        "selected_inherited": [row["source_proposal_id"] for row in source_program()],
        "selection_rows_reappended": 0,
        "new_count": len(new),
        "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in new],
        "effective_count": len(prior) + len(new),
    }
    return receipt, frozen_index


def portfolio_plan() -> dict[str, Any]:
    owner_safe = [
        {"task_id": f"V6623R-SAFE-{i:03d}", "title": d.OWNER_CFR_TASKS[i - 1], "lane": "owner_safe_now", "state": "planned_x1", "expected_outcome": "completed"}
        for i in range(1, 31)
    ]
    successor_safe = [
        {"task_id": f"V6624-SAFE-REC-{i:03d}", "title": d.SUCCESSOR_CFR_TASKS[i - 1], "lane": "successor_recommendation", "state": "recommendation_only", "expected_outcome": "represented"}
        for i in range(1, 21)
    ]
    owner_candidates = [
        {"task_id": f"V6623R-CAND-{i:03d}", "title": f"Bounded candidate execution {i}: {d.OWNER_CFR_TASKS[(i + 9) % 30]}", "state": "planned_x1", "expected_outcome": "completed" if i <= 11 else ("represented" if i <= 14 else "open_gap")}
        for i in range(1, 16)
    ]
    successor_candidates = [
        {"task_id": f"V6624-CAND-REC-{i:03d}", "title": f"Vesper candidate recommendation {i}: {d.SUCCESSOR_CFR_TASKS[(i + 4) % 30]}", "state": "recommendation_only", "expected_outcome": "represented"}
        for i in range(1, 16)
    ]
    exact = [
        {"task_id": f"V6623R-EXACT-{i:03d}", "title": f"Exact authority packet {i} reserved behind competent evidence and authority", "state": "exact_gate", "executed": False}
        for i in range(1, 11)
    ]
    blocked = [
        {"task_id": f"V6623R-BLOCKED-{i:03d}", "title": f"Blocked real-world packet {i} retained without substitution", "state": "open_gap", "executed": False}
        for i in range(1, 6)
    ]
    return {
        "schema": "ghc.family.v662-v3-2-remaster.approval-portfolios.x1.v1",
        "owner_safe_now": owner_safe,
        "successor_safe_now": successor_safe,
        "owner_candidates": owner_candidates,
        "successor_candidates": successor_candidates,
        "owner_exact": exact,
        "owner_blocked": blocked,
        "counts": {
            "owner_safe_now": len(owner_safe),
            "successor_safe_now": len(successor_safe),
            "owner_candidates": len(owner_candidates),
            "successor_candidates": len(successor_candidates),
            "owner_exact": len(exact),
            "owner_blocked": len(blocked),
            "safe_total": len(owner_safe) + len(successor_safe),
            "candidate_total": len(owner_candidates) + len(successor_candidates),
        },
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def skill_runner_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v662-v3-2-remaster.skill-runner-plan.x1.v1",
        "owner_skill_builds": [{"name": name, "purpose": purpose, "state": "planned_x1"} for name, purpose in d.SKILL_SPECS],
        "successor_skill_ideas": [{"name": name, "purpose": purpose, "state": "recommendation_only"} for name, purpose in d.SUCCESSOR_SKILL_IDEAS],
        "owner_runner_builds": [{"name": name, "purpose": purpose, "state": "planned_x1"} for name, purpose in d.RUNNER_SPECS],
        "successor_runner_ideas": [{"name": name, "purpose": purpose, "state": "recommendation_only"} for name, purpose in d.SUCCESSOR_RUNNER_IDEAS],
        "counts": {"owner_skills": 10, "successor_skills": 10, "owner_runners": 10, "successor_runners": 10},
        "promotion_rule": "Build, validate, and smoke-use phase-local packages first; globally promote only generally useful, nonoverlapping packages. Never mutate plugin caches.",
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def clean_fix_refine_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v662-v3-2-remaster.clean-fix-refine.x1.v1",
        "owner": [{"task_id": f"V6623R-CFR-{i:03d}", "title": title, "state": "planned_x1"} for i, title in enumerate(d.OWNER_CFR_TASKS, start=1)],
        "successor": [{"task_id": f"V6624-CFR-REC-{i:03d}", "title": title, "state": "recommendation_only"} for i, title in enumerate(d.SUCCESSOR_CFR_TASKS, start=1)],
        "counts": {"owner": 30, "successor": 30, "total": 60},
        "destructive_cleanup_authorized": False,
        "boundary": "Additive, owner-scoped refinement plan. No sibling, shared, external, or plugin-cache deletion is authorized.",
    }


def recovery_contract() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v662-v3-2-remaster.ancestry-aware-suite-contract.x1.v1",
        "source_exact_final": d.SOURCE_FIRST_FINAL,
        "prior_attempts_retained": 2,
        "complete_repository_requirement": True,
        "selection": {
            "inventory": "Every unittest identifier discoverable from tests/test*.py at the exact remaster final.",
            "duplicate_policy": "reject",
            "omission_policy": "reject",
            "selection_hash_required": True,
        },
        "definition_anchor": {
            "rule": "For each tracked test module, use the last commit that changed the module's exact bytes.",
            "blob_equality_required": True,
            "missing_or_ambiguous_anchor": "fail_closed",
        },
        "execution": {
            "fixture": "Owner-controlled D-first shared clone; sibling worktrees remain read-only.",
            "module_context": "Execute the unchanged module at its immutable definition commit and historical branch hint.",
            "historical_test_editing": False,
            "module_timeout_required": True,
            "raw_transcript_retained": False,
            "sanitized_result_digest_required": True,
        },
        "completeness": {
            "every_current_test_id_mapped_once": True,
            "executed_test_count_equals_discovered_test_count": True,
            "all_modules_pass": True,
            "all_current_remaster_lifecycle_tests_included": True,
        },
        "canonical_policy": {
            "preflight_before_invocation": True,
            "successful_invocation_required": 1,
            "replay_after_success": False,
            "isolated_blocker_before_broader_rerun": True,
        },
        "claim_boundary": d.EVIDENCE_BOUNDARY,
    }


def overview(selected: list[dict[str, Any]], new: list[dict[str, Any]]) -> str:
    lines = [
        "# Neris Solane v662-v3-2 remaster — x1 frozen overview",
        "",
        d.IDENTITY_BOUNDARY,
        "",
        "## Outcome sought",
        "",
        (
            "This additive remaster exists because the sealed first Neris v662-v3 lane reached a clean, pushed, "
            "four-way-equal final but did not satisfy its terminal canonical gate. The first canonical invocation "
            "timed out and the second revealed that many historical lifecycle tests were being evaluated against "
            "a later checkout rather than the immutable state those tests were written to validate. Both failures "
            "remain evidence at zero aggregate-success credit. The remaster does not rewrite their branch, commits, "
            "counts, manifests, or route decision."
        ),
        "",
        (
            "The x1 freeze makes one narrowly falsifiable recovery claim: a complete current unittest identifier "
            "inventory can be executed without changing historical assertions by resolving each tracked test module "
            "to the last commit that defined its exact bytes and evaluating that unchanged module inside an "
            "owner-controlled shared clone at the immutable definition commit. Completeness means every current ID "
            "is mapped once, every module result is attributable, the executed count equals the discovered count, "
            "and no module fails or times out. Anything less is a retained canonical failure."
        ),
        "",
        "## Strict lifecycle separation",
        "",
        (
            "This commit is x1 only. It freezes program rows, portfolio quantities, skill and runner plans, source "
            "vocabulary, the recovery algorithm, retained failures, protected gates, and exact validation rules. "
            "It contains no x2 surface result, no observed proposal outcome, no successful suite claim, no global "
            "skill promotion claim, and no successor delivery. The subsequent evidence commit may execute the "
            "frozen safe and candidate work. Only a later final direct child may hold closeout artifacts and only an "
            "external one-shot receipt may establish canonical success."
        ),
        "",
        "## Program composition",
        "",
        (
            "Twenty first-run Neris proposal contracts are selected for read-only bounded revalidation. They receive "
            "zero remaster novelty and completion credit and are not appended to the frozen chain. Twenty genuinely "
            "new repository-lifecycle proposals are appended, raising the chain from 3,510 to 3,530. Their expected "
            "outcomes are exactly fourteen completed, four represented, one open_gap, and one exact_gate. Expected "
            "outcomes are preregistration targets, not observed x1 facts."
        ),
        "",
        "## Selected inherited rows",
        "",
    ]
    for row in selected:
        lines.append(f"- `{row['proposal_id']}` revalidates `{row['source_proposal_id']}` — {row['title']}. Zero novelty and zero completion credit.")
    lines.extend(["", "## New frozen rows", ""])
    for row in new:
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Expected label: `{row['expected_disposition']}`. Pillar relation: {row['pillar_relation']}.",
                "",
                f"Hypothesis: {row['hypothesis']}",
                "",
                f"Falsifier: {row['null_or_failure_condition']}",
                "",
                f"Acceptance boundary: {row['falsifier_or_acceptance_gate']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Portfolio and tooling floors",
            "",
            (
                "The frozen plan carries thirty owner safe-now executions and twenty successor safe-now "
                "recommendations; fifteen owner candidate executions and fifteen successor candidate "
                "recommendations; ten exact packets and five blocked packets; ten owner skill builds and ten "
                "successor skill ideas; ten owner runner builds and ten successor runner ideas; and thirty owner "
                "plus thirty successor CLEAN/FIX/REFINE rows. Counts are floors for meaningful work, never an "
                "invitation to filler or evidence inflation. Exact and blocked packets remain unexecuted."
            ),
            "",
            "## Scientific, governance, and identity boundary",
            "",
            (
                "GMUT remains a research-model family. The remaster studies repository-validation structure; it "
                "does not add a likelihood, parameter constraint, physical prediction, observation, detected force, "
                "material law, ultraviolet completion, or Theory-of-Everything proof. THOS remains a software and "
                "protocol proxy without governed real participants, matched arms, safety monitoring, appropriate "
                "statistics, or independent review. Freed ID remains nonproduction with no real keys, proofs, "
                "issuance, resolution, status, revocation, recovery, interoperability, or trust governance."
            ),
            "",
            (
                "CBR, privacy, accessibility, legal and cultural interpretation, affected-party legitimacy, "
                "traditional knowledge, Māori data governance, tangata whenua, iwi, hapū, and Māori authority "
                "remain protected. Māori concepts remain under Māori authority. Same-owner success would still not "
                "be independent reproduction, external audit, production certification, professional validation, "
                "complete privacy or accessibility assurance, exhaustive security, personhood evidence, or Stage 20 authority."
            ),
            "",
            "## Route boundary",
            "",
            (
                "The live roster contains fifteen active main-task seats and Tavian Sol as a standby collaboration-"
                "subagent record. The parenthetical remaster changes no canonical assignment. Vesper Arlen v662-v4 "
                "is the only prospective next edge, and it remains PREPARED_NOT_SENT until the new branch is clean, "
                "pushed, exact, zero-divergent, fresh-live equal, and has one successful exact-final canonical "
                "aggregate. Exact-title resolution, immediate reread, and one acknowledged send occur only afterward."
            ),
        ]
    )
    return "\n".join(lines)


def write_base() -> dict[str, Any]:
    if rt.git("rev-parse", "HEAD") != d.SOURCE_FIRST_FINAL:
        raise RuntimeError("x1 builder must start at the exact sealed first Neris final")
    if rt.git("branch", "--show-current") != d.BRANCH:
        raise RuntimeError("x1 builder is on the wrong branch")
    selected, new = program()
    novelty, frozen_index = novelty_receipt(new)
    if not novelty["valid"]:
        raise RuntimeError({"novelty_failure": novelty})

    proposal_ledger = {
        "schema": "ghc.family.v662-v3-2-remaster.proposal-ledger.x1.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "canonical_phase": d.CANONICAL_PHASE,
        "frozen_before": d.FIRST_RUN_FROZEN_PROPOSALS,
        "frozen_after": d.REMASTER_FROZEN_PROPOSALS,
        "selected_inherited": 20,
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_completion_credit": 0,
        "new_unique": 20,
        "expected_outcomes": dict(Counter(row["expected_disposition"] for row in new)),
        "program": selected + new,
        "x1_only": True,
        "observed_outcomes_recorded": False,
        "boundary": d.EVIDENCE_BOUNDARY,
    }
    rt.write_json(PHASE / "preregistration/proposal-ledger.json", proposal_ledger)
    rt.write_json(PHASE / "provenance/frozen-chain-proposal-index.json", frozen_index)
    rt.write_json(PHASE / "preregistration/novelty-audit.json", novelty)
    rt.write_json(PHASE / "preregistration/approval-portfolios.json", portfolio_plan())
    rt.write_json(PHASE / "preregistration/skill-and-runner-plan.json", skill_runner_plan())
    rt.write_json(PHASE / "preregistration/clean-fix-refine-plan.json", clean_fix_refine_plan())
    rt.write_json(PHASE / "preregistration/ancestry-aware-suite-contract.json", recovery_contract())
    rt.write_json(
        PHASE / "truth/inherited-baseline.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.inherited-baseline.v1",
            "source_first_final": d.SOURCE_FIRST_FINAL,
            "frozen_proposals": d.FIRST_RUN_FROZEN_PROPOSALS,
            "effective_negatives": d.INHERITED_LIVE_NEGATIVES,
            "effective_methods": d.INHERITED_LIVE_METHODS,
            "open_gaps": d.INHERITED_OPEN_GAPS,
            "exact_gates": d.INHERITED_EXACT_GATES,
            "terminal_verdict": d.TERMINAL_VERDICT,
            "sealed_source_unchanged": True,
            "external_overlay_inherited": True,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    rt.write_json(
        PHASE / "truth/prior-canonical-failures.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.prior-canonical-failures.v1",
            "failures": d.PRIOR_CANONICAL_FAILURES,
            "failure_count": 2,
            "success_count": 0,
            "rewrote_source": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    methods = []
    for item in d.STARTUP_METHODS:
        methods.append(
            {
                **item,
                "failed_witness": f"{item['method_id']}-F01",
                "failed_credit": 0,
                "passing_witness": f"{item['method_id']}-P01",
                "state": "preferred_bounded_recovery",
                "scope": "same_owner_workflow_only",
                "boundary": d.EVIDENCE_BOUNDARY,
            }
        )
    rt.write_json(
        PHASE / "method-flow/method-flow-state-x1.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "methods": methods,
            "method_count": len(methods),
            "failed_witness_count": len(methods),
            "passing_witness_count": len(methods),
            "inherited_method_baseline": d.INHERITED_LIVE_METHODS,
            "provisional_effective_methods": d.INHERITED_LIVE_METHODS + len(methods),
            "inherited_negative_baseline": d.INHERITED_LIVE_NEGATIVES,
            "provisional_effective_negatives": d.INHERITED_LIVE_NEGATIVES + len(methods),
        },
    )
    rt.write_json(
        PHASE / "provenance/source-ledger.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.source-ledger.v1",
            "checked_at": "2026-08-10",
            "sources": [
                {"source_id": source_id, "url": url, "scope": scope, "status": "official_or_primary_vocabulary_only"}
                for source_id, url, scope in d.SOURCE_LEDGER
            ],
            "source_count": len(d.SOURCE_LEDGER),
            "no_endorsement_or_authority": True,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    rt.write_json(
        PHASE / "routing/terminal-route-plan.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.route-plan.x1.v1",
            "current_variant": {"label": d.PHASE, "canonical_phase": d.CANONICAL_PHASE, "changes_canonical_assignments": False},
            "active_main_tasks": [
                "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow"
            ],
            "standby": [{"name": "Tavian Sol", "endpoint_kind": "collaboration_subagent", "state": "ON_STANDBY", "eligible_for_main_task_route": False}],
            "next": {"owner": d.SUCCESSOR, "phase": d.SUCCESSOR_PHASE, "endpoint_kind": "main_task", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
            "route_through": "v675-v8",
            "one_edge_at_a_time": True,
            "message_attempted": False,
            "sent": False,
            "acknowledged": False,
            "substitute_endpoint": False,
            "terminal_gate": ["clean pushed exact final", "zero divergence", "fresh-live equality", "one successful complete canonical aggregate", "newest live roster and authorization reread"],
        },
    )
    rt.write_text(PHASE / "overview/x1-frozen-overview.md", overview(selected, new))
    rt.write_text(
        PHASE / "method-flow/issues-and-recovery-methods.md",
        "# v662-v3-2 remaster startup issues and bounded recovery methods\n\n"
        + d.IDENTITY_BOUNDARY
        + "\n\n"
        + "\n\n".join(
            f"## {row['method_id']}\n\nFailure: `{row['failure']}`. The failed witness earns zero credit and changed no sibling, repository, remote, route, or authority state.\n\nRecovery: {row['recovery']} The passing witness proves only this bounded same-owner workflow recovery. It does not prove general reliability, production readiness, complete privacy or accessibility, exhaustive security, independent reproduction, professional competence, authority, personhood, or Stage 20 readiness."
            for row in d.STARTUP_METHODS
        ),
    )
    return {"selected": selected, "new": new, "novelty": novelty}


def validation_payload() -> dict[str, Any]:
    ledger = rt.read_json(PHASE / "preregistration/proposal-ledger.json")
    portfolios = rt.read_json(PHASE / "preregistration/approval-portfolios.json")
    tooling = rt.read_json(PHASE / "preregistration/skill-and-runner-plan.json")
    cfr = rt.read_json(PHASE / "preregistration/clean-fix-refine-plan.json")
    frozen = rt.read_json(PHASE / "provenance/frozen-chain-proposal-index.json")
    methods = rt.read_json(PHASE / "method-flow/method-flow-state-x1.json")
    outcomes = ledger["expected_outcomes"]
    checks = {
        "exact_source_head": rt.git("rev-parse", "HEAD") == d.SOURCE_FIRST_FINAL,
        "exact_branch": rt.git("branch", "--show-current") == d.BRANCH,
        "selected_twenty": ledger["selected_inherited"] == 20,
        "selected_zero_novelty": ledger["selected_inherited_novelty_credit"] == 0,
        "selected_zero_completion": ledger["selected_inherited_completion_credit"] == 0,
        "new_twenty": ledger["new_unique"] == 20,
        "frozen_chain_3530": frozen["effective_count"] == d.REMASTER_FROZEN_PROPOSALS,
        "outcomes_four_labels": set(outcomes) == set(d.ALLOWED_OUTCOMES),
        "expected_14_4_1_1": outcomes == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "owner_safe_30": portfolios["counts"]["owner_safe_now"] == 30,
        "successor_safe_20": portfolios["counts"]["successor_safe_now"] == 20,
        "owner_candidate_15": portfolios["counts"]["owner_candidates"] == 15,
        "successor_candidate_15": portfolios["counts"]["successor_candidates"] == 15,
        "exact_10": portfolios["counts"]["owner_exact"] == 10,
        "blocked_5": portfolios["counts"]["owner_blocked"] == 5,
        "skills_10_plus_10": tooling["counts"]["owner_skills"] == 10 and tooling["counts"]["successor_skills"] == 10,
        "runners_10_plus_10": tooling["counts"]["owner_runners"] == 10 and tooling["counts"]["successor_runners"] == 10,
        "cfr_30_plus_30": cfr["counts"] == {"owner": 30, "successor": 30, "total": 60},
        "prior_failures_two": len(rt.read_json(PHASE / "truth/prior-canonical-failures.json")["failures"]) == 2,
        "startup_methods_five": methods["method_count"] == 5,
        "x1_no_observed_outcomes": ledger["observed_outcomes_recorded"] is False,
        "route_not_sent": rt.read_json(PHASE / "routing/terminal-route-plan.json")["sent"] is False,
    }
    return {
        "schema": "ghc.family.v662-v3-2-remaster.x1-validation.v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "valid": all(checks.values()),
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def write_validation() -> dict[str, Any]:
    paths_before = rt.owner_paths()
    manifest = rt.make_manifest(paths_before, schema="ghc.family.v662-v3-2-remaster.x1-content-manifest.v1", exclusions=X1_RECEIPTS)
    rt.write_json(VALIDATION / "x1-content-manifest.json", manifest)
    paths = rt.owner_paths()
    rt.write_json(VALIDATION / "x1-privacy-scan.json", rt.privacy_scan(paths, schema="ghc.family.v662-v3-2-remaster.x1-privacy-scan.v1"))
    rt.write_json(VALIDATION / "x1-document-cap.json", rt.document_cap(paths))
    expected = [rt.repo_relative(path) for path in paths]
    rt.write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.x1-staged-review.v1",
            "state": "PRE_STAGING_NOT_CREDITED",
            "expected_paths": expected,
            "actual_paths": [],
            "missing": expected,
            "unexpected": [],
            "valid": False,
        },
    )
    payload = validation_payload()
    payload["working_manifest_mismatches"] = rt.replay_working_manifest(manifest)
    payload["privacy_zero"] = rt.read_json(VALIDATION / "x1-privacy-scan.json")["confirmed_hit_count"] == 0
    payload["document_cap_valid"] = rt.read_json(VALIDATION / "x1-document-cap.json")["valid"]
    payload["valid"] = payload["valid"] and not payload["working_manifest_mismatches"] and payload["privacy_zero"] and payload["document_cap_valid"]
    rt.write_json(VALIDATION / "x1-validation.json", payload)
    return payload


def staged_review() -> dict[str, Any]:
    expected = [rt.repo_relative(path) for path in rt.owner_paths()]
    actual = sorted(filter(None, rt.git("diff", "--cached", "--name-only", "--", d.PHASE_ROOT, "scripts", "tests").splitlines()))
    owner_actual = [
        path
        for path in actual
        if path.startswith(d.PHASE_ROOT + "/")
        or "v662_v3_2_remaster" in Path(path).name
    ]
    payload = {
        "schema": "ghc.family.v662-v3-2-remaster.x1-staged-review.v1",
        "reviewed_at_utc": utc_now(),
        "state": "EXACT_STAGED_REVIEW",
        "expected_paths": expected,
        "actual_paths": owner_actual,
        "missing": sorted(set(expected) - set(owner_actual)),
        "unexpected": sorted(set(owner_actual) - set(expected)),
        "valid": set(expected) == set(owner_actual),
        "boundary": "Exact staged owner-path comparison only; not content, authority, or delivery proof.",
    }
    rt.write_json(VALIDATION / "x1-staged-review.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        result = staged_review()
    elif args.validate_only:
        result = validation_payload()
    else:
        write_base()
        result = write_validation()
    print(json.dumps({"valid": result["valid"], "passed": result.get("passed"), "total": result.get("total"), "phase": d.PHASE}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
