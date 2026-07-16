#!/usr/bin/env python3
"""Build the Sable Rook v647-v1 x1-only preregistration packet."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v647_v1_definitions import (
    BLOCKED_PACKET_TITLES,
    BOUNDED_PRACTICE,
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    EXACT_PACKET_TITLES,
    EXTERNAL_SOURCE_NEGATIVES,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    METHOD_SPECS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PHASE_SHORT,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SEALED_SOURCE_NEGATIVES,
    SKILL_SPECS,
    SLUG,
    SOURCE_BRANCH,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
    X1_OPERATIONAL_NEGATIVES,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / PHASE_SHORT
SOURCE_DIR = ROOT / "docs" / "ilyra-fen" / "v646-v8"
ALLOWED_SOURCE_STATUS = {"current", "stable", "draft", "watch"}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalize_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def title_tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "for", "to", "with", "without"}
    return {token for token in normalize_title(value).split() if token not in stop}


def neighbor_rows(prior: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        current = title_tokens(proposal["title"])
        ranked = []
        for old in prior:
            old_tokens = title_tokens(old["title"])
            union = current | old_tokens
            score = len(current & old_tokens) / len(union) if union else 0.0
            ranked.append((score, old["proposal_id"], old["title"], old["path"]))
        ranked.sort(reverse=True)
        top = ranked[:5]
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "exact_normalized_collision": any(
                    normalize_title(proposal["title"]) == normalize_title(old["title"])
                    for old in prior
                ),
                "nearest": [
                    {"score": round(score, 6), "proposal_id": pid, "title": title, "path": path}
                    for score, pid, title, path in top
                ],
                "manual_novelty_statement": proposal["novelty_against_470_frozen_proposals"],
            }
        )
    return rows


def portfolio_rows(titles: list[str], prefix: str, adopted_count: int) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"V6471-{prefix}-{index:02d}",
            "title": title,
            "origin": "successor_seed_rewritten_after_review" if index <= adopted_count else "sable_new",
            "x1_state": "frozen_not_executed",
            "x2_completion_credit": 0,
            "approval_class": "safe_now" if prefix == "SAFE" else "candidate",
        }
        for index, title in enumerate(titles, 1)
    ]


def method_material() -> list[tuple[dict[str, Any], list[dict[str, Any]], str]]:
    rows = []
    for spec in METHOD_SPECS:
        method_id = spec["method_id"]
        common = {
            "method_id": method_id,
            "title": spec["title"],
            "failure_signature": spec["failure_signature"],
            "trigger_preconditions": spec["trigger_preconditions"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_read_only_or_owned_lane",
            "candidate_workaround": spec["candidate_workaround"],
            "validation_witness_ids": [f"{method_id}-WFAIL", f"{method_id}-WPASS"],
            "recurrence_guard": spec["recurrence_guard"],
            "rollback": spec["rollback"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": spec["protected_gates"],
            "retained_negative_ids": spec["retained_negative_ids"],
            "scope_boundary": "Sable v647-v1 workflow evidence only; no scientific, identity, authority, production, or independent-reproduction claim.",
        }
        failed = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": "Retain the observed startup or x1 failure before retry.",
            "scope": "v647-v1 startup and x1 preflight",
            "expected": "The initial assumption should work.",
            "observed": spec["failed_observed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": spec["retained_negative_ids"],
            "boundary": common["scope_boundary"],
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": spec["candidate_workaround"],
            "scope": "v647-v1 startup and x1 preflight",
            "expected": "The bounded recovery returns the required evidence without unintended mutation.",
            "observed": spec["pass_observed"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": spec["retained_negative_ids"],
            "boundary": common["scope_boundary"],
        }
        rows.append((common, [failed, passed], "preferred"))
    return rows


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != SOURCE_REVISION:
        ancestry = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", SOURCE_REVISION, head],
            check=False,
        ).returncode == 0
        phase_commits = int(git("rev-list", "--count", f"{SOURCE_REVISION}..{head}"))
        phase_merges = int(git("rev-list", "--count", "--merges", f"{SOURCE_REVISION}..{head}"))
        if not ancestry or phase_commits > 1 or phase_merges != 0:
            raise SystemExit("preregistration repair must remain the first single-parent x1 descendant of the verified source")
    if git("branch", "--show-current") != "codex/GHC-Family/sable-rook-full-tools":
        raise SystemExit("preregistration must run on the owned Sable canonical branch")

    prior_index = load(SOURCE_DIR / "provenance" / "frozen-chain-proposal-index.json")
    source_x1 = load(SOURCE_DIR / "x1-proposals.json")
    prior = list(prior_index["prior_proposals"])
    for row in source_x1["proposals"]:
        prior.append(
            {
                "path": "docs/ilyra-fen/v646-v8/x1-proposals.json",
                "proposal_id": row["proposal_id"],
                "title": row["title"],
            }
        )
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    neighbors = neighbor_rows(prior)
    if any(row["exact_normalized_collision"] for row in neighbors):
        raise SystemExit("exact normalized proposal-title collision")

    statuses = Counter(row["status"] for row in SOURCES)
    if not set(statuses).issubset(ALLOWED_SOURCE_STATUS):
        raise SystemExit("source ledger contains a disallowed status")
    if len(PROPOSALS) != 10:
        raise SystemExit("proposal cardinality must be exactly ten")
    expected_distribution = Counter(row["expected_disposition"] for row in PROPOSALS)
    if expected_distribution != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit("expected distribution must be 6/2/1/1")
    if set(expected_distribution) != set(OUTCOME_CLASSES):
        raise SystemExit("outcome vocabulary mismatch")
    floors = {
        "safe": len(SAFE_TASK_TITLES),
        "candidate": len(CANDIDATE_TITLES),
        "skill": len(SKILL_SPECS),
        "runner": len(RUNNER_TITLES),
        "cleanup": len(CLEAN_TASK_TITLES),
    }
    if floors != {"safe": 30, "candidate": 20, "skill": 20, "runner": 10, "cleanup": 30}:
        raise SystemExit(f"portfolio floors mismatch: {floors}")

    write(
        "identity-receipt.json",
        {
            "schema": "ghc.family.v647-v1.identity.v1",
            "phase": PHASE,
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v647-v1.startup.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_branch": SOURCE_BRANCH,
            "source_revision": SOURCE_REVISION,
            "source_live_equal": True,
            "owned_branch": "codex/GHC-Family/sable-rook-full-tools",
            "owned_lane_fast_forwarded": True,
            "owned_lane_clean_before_phase_files": True,
            "d_first": True,
            "d_free_gib_at_preflight": 546.71,
            "source_anchors": {
                "inherited": SOURCE_INHERITED_REVISION,
                "x1": SOURCE_X1_REVISION,
                "evidence": SOURCE_EVIDENCE_REVISION,
                "final": SOURCE_REVISION,
            },
            "source_phase_commits": 3,
            "source_merges": 0,
            "source_final_parent_count": 1,
            "standby_siblings": ["Eiren Kestrel", "Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v647-v1.version-receipt.v1",
            "observed_on": "2026-07-17",
            "verified_only": True,
            "codex_cli": "codex-cli 0.144.4",
            "desktop": "26.707.9981.0",
            "python": "Python 3.12.10",
            "git": "git version 2.55.0.windows.2",
            "sqlite": "3.49.1",
            "desktop_updated": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "reboot": False,
        },
    )
    write(
        "environment/windows-sandbox-probe.json",
        {
            "schema": "ghc.family.v647-v1.windows-sandbox-probe.v1",
            "executable_available": bool(shutil.which("WindowsSandbox.exe")),
            "session_launched": False,
            "feature_enabled": False,
            "elevation": False,
            "host_security_changed": False,
            "installation": False,
            "reboot": False,
            "boundary": "A read-only capability probe is not an operational or administrative sandbox witness.",
        },
    )
    write(
        "environment/rotation-guard.json",
        {
            "schema": "ghc.family.v647-v1.rotation-guard.x1.v1",
            "threshold": 15000,
            "inherited_baseline_triggers_rotation": False,
            "inherited_tracked_file_baseline": 35643,
            "owner_generated_count_at_x1": 72,
            "rotation_required": False,
        },
    )

    write(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v647-v1.source-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "checked_on": "2026-07-17",
            "allowed_statuses": sorted(ALLOWED_SOURCE_STATUS),
            "status_counts": dict(sorted(statuses.items())),
            "sources": SOURCES,
            "real_data_rows_ingested": 0,
            "likelihood_evaluations": 0,
            "real_participants": 0,
            "real_keys_or_proofs": 0,
            "real_food_lots_or_release_actions": 0,
            "boundary": "Sources define obligations and gates only; they are not observations, participant evidence, delegated authority, legal interpretation, or production readiness.",
        },
    )
    source_lines = [
        "# v647-v1 official and primary source ledger",
        "",
        "Checked 2026-07-17. A citation is never experimental data, case authority, cultural authority, or delegated authority.",
        "",
    ]
    for row in SOURCES:
        source_lines.append(
            f"- {row['source_id']} [{row['status']}] {row['title']} ({row['publisher']}) — {row['url']}; use: {row['use']}."
        )
    write_text("sources/source-ledger.md", "\n".join(source_lines))

    write(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v647-v1.prior-proposal-index.v1",
            "count": len(prior),
            "prior_proposals": prior,
        },
    )
    write(
        "provenance/proposal-collision-audit.json",
        {
            "schema": "ghc.family.v647-v1.proposal-collision-audit.v1",
            "prior_count": len(prior),
            "new_count": len(PROPOSALS),
            "exact_collision_count": sum(row["exact_normalized_collision"] for row in neighbors),
            "rows": neighbors,
            "manual_review_required": True,
            "manual_review_completed": True,
            "rejected_seed_examples": [
                "Stage 20 analytic-multiverse and specification-curve board",
                "Freed ID DCQL credential-set profile",
                "Freed ID Bitstring Status List profile",
                "GMUT Gaia DR3 zero-row protocol",
                "GMUT Euclid Q1 zero-row protocol",
                "CBR community-archive authority matrix",
            ],
            "boundary": "Token similarity supports but cannot replace semantic novelty review.",
        },
    )
    write(
        "x1-proposals.json",
        {
            "schema": "ghc.family.v647-v1.x1-proposals.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_phase": SOURCE_PHASE,
            "source_revision": SOURCE_REVISION,
            "prior_frozen_proposal_count": PRIOR_FROZEN_PROPOSALS,
            "new_frozen_proposal_count": 10,
            "frozen_chain_count_after_x1": 480,
            "primary_focus": PRIMARY_FOCUS,
            "bounded_practice": BOUNDED_PRACTICE,
            "outcome_classes": OUTCOME_CLASSES,
            "expected_distribution": dict(expected_distribution),
            "expected_counts_are_results": False,
            "x2_execution_present": False,
            "identity_boundary": IDENTITY_BOUNDARY,
            "proposals": PROPOSALS,
            "x1_freeze_rule": "No x2 implementation, observed outcome, or completion claim exists in this x1 packet.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "x1-gate-carry-forward.json",
        {
            "schema": "ghc.family.v647-v1.x1-gates.v1",
            "inherited_open_gaps": INHERITED_OPEN_GAPS,
            "inherited_exact_gates": INHERITED_EXACT_GATES,
            "new_expected_open_gaps": 1,
            "new_expected_exact_gates": 1,
            "effective_if_expected_outcomes_hold": {"open_gaps": 18, "exact_gates": 19},
            "closed_without_exact_evidence": 0,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "approval-packets/x1-approval-portfolio.json",
        {
            "schema": "ghc.family.v647-v1.x1-approval-portfolio.v1",
            "count": 30,
            "tasks": portfolio_rows(SAFE_TASK_TITLES, "SAFE", 15),
            "x2_completion_credit": 0,
            "boundary": "All tasks remain frozen and unexecuted at x1.",
        },
    )
    write(
        "prototypes/x1-candidate-plan.json",
        {
            "schema": "ghc.family.v647-v1.x1-candidate-plan.v1",
            "count": 20,
            "tasks": portfolio_rows(CANDIDATE_TITLES, "CAND", 10),
            "x2_completion_credit": 0,
        },
    )
    write(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v647-v1.x1-skill-runner-plan.v1",
            "skill_count": 20,
            "skills": [
                {
                    "skill_id": f"V6471-SKILL-{index:02d}",
                    "name": name,
                    "description": description,
                    "origin": "successor_seed_rewritten_after_review" if index > 10 else "sable_new_core",
                    "x1_state": "frozen_not_built",
                }
                for index, (name, description) in enumerate(SKILL_SPECS, 1)
            ],
            "runner_count": 10,
            "runners": [
                {
                    "runner_id": f"V6471-RUN-{index:02d}",
                    "name": name,
                    "origin": "successor_seed_rewritten_after_review" if index == 10 else "sable_new_core",
                    "x1_state": "frozen_not_built",
                }
                for index, name in enumerate(RUNNER_TITLES, 1)
            ],
            "caller_compatibility_required": True,
            "x2_completion_credit": 0,
        },
    )
    write(
        "maintenance/x1-clean-refine-plan.json",
        {
            "schema": "ghc.family.v647-v1.x1-clean-refine-plan.v1",
            "count": 30,
            "tasks": portfolio_rows(CLEAN_TASK_TITLES, "CLEAN", 15),
            "destructive_tasks": 0,
            "x2_completion_credit": 0,
        },
    )
    write(
        "approval-packets/x1-protected-packet-register.json",
        {
            "schema": "ghc.family.v647-v1.x1-protected-packets.v1",
            "exact_count": 10,
            "exact_packets": [
                {"packet_id": f"V6471-EXACT-{index:02d}", "title": title, "state": "unexecuted_exact_gate"}
                for index, title in enumerate(EXACT_PACKET_TITLES, 1)
            ],
            "blocked_count": 5,
            "blocked_packets": [
                {"packet_id": f"V6471-BLOCK-{index:02d}", "title": title, "state": "blocked_unexecuted"}
                for index, title in enumerate(BLOCKED_PACKET_TITLES, 1)
            ],
            "execution_credit": 0,
        },
    )
    mutations = [
        {
            "negative_id": f"{proposal['proposal_id']}-SYN-N{index:02d}",
            "proposal_id": proposal["proposal_id"],
            "state": "preregistered_not_executed",
            "expected": "reject",
            "completion_credit": False,
        }
        for proposal in PROPOSALS
        for index in range(1, 8)
    ]
    if len(mutations) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise SystemExit("synthetic mutation count mismatch")
    write(
        "validation/x1-synthetic-mutation-plan.json",
        {
            "schema": "ghc.family.v647-v1.x1-synthetic-mutation-plan.v1",
            "count": len(mutations),
            "rows": mutations,
            "x2_execution_present": False,
        },
    )
    write(
        "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v647-v1.x1-operational-negatives.v1",
            "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
            "sealed_source": SEALED_SOURCE_NEGATIVES,
            "external_source": EXTERNAL_SOURCE_NEGATIVES,
            "count": len(X1_OPERATIONAL_NEGATIVES),
            "rows": X1_OPERATIONAL_NEGATIVES,
            "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
            "no_negative_erased": True,
        },
    )
    write(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v647-v1.retained-negatives.v1",
            "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
            "sealed_source": SEALED_SOURCE_NEGATIVES,
            "external_source": EXTERNAL_SOURCE_NEGATIVES,
            "x1_operational": len(X1_OPERATIONAL_NEGATIVES),
            "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
            "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "preregistered_synthetic_executed": 0,
            "x2_operational": 0,
            "effective_total_at_x1": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
            "no_negative_erased": True,
            "boundary": TRUTH_BOUNDARY,
        },
    )

    for record, witnesses, final_state in method_material():
        stem = record["method_id"].casefold()
        write(f"method-flow/{stem}-method-record.json", record)
        for witness in witnesses:
            write(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)
        write(
            f"method-flow/{stem}-transition-plan.json",
            {"method_id": record["method_id"], "target_state": final_state, "x1_state": "runner_pending"},
        )

    write(
        "tooling/selected-toolchain.json",
        {
            "schema": "ghc.family.v647-v1.selected-toolchain.x1.v1",
            "phase": PHASE,
            "selected": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "build_ghc_family_index.py",
                "ghc_family_method_flow_state.py",
                "ghc_family_proposal_neighbor_quarantine.py",
            ],
            "selection_reason": "Smallest family-current startup, novelty, Method Flow, and routing toolchain for the live phase.",
            "compatibility_policy": "Historical versioned tools remain evidence and callers; none is silently promoted or deleted.",
        },
    )
    write(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.v647-v1.phase-update.v1",
            "owner": OWNER,
            "phase": PHASE,
            "state": "ACTIVE_X1",
            "active": [OWNER],
            "standby": ["Eiren Kestrel", "Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "route_state": "PREPARED_NOT_SENT",
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v647-v1.terminal-route-plan.v1",
            "target_title": "Orin Thale",
            "next_phase": "v647-gmut-thos-v2-x1-x2",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "requires_exact_final": True,
            "requires_one_named_replay": True,
            "no_task_creation": True,
            "boundary": "A prepared plan is not a sent baton.",
        },
    )
    write(
        "orchestration/memory-review-receipt.json",
        {
            "schema": "ghc.family.v647-v1.memory-review.v1",
            "newest_applicable_memory": "Sable v646-v3 exact-head continuity and one-shot routing",
            "live_baton_authoritative_where_memory_stops": True,
            "raw_task_identifiers_published": False,
        },
    )
    write(
        "phase-truth.json",
        {
            "schema": "ghc.family.v647-v1.phase-truth.x1.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_revision": SOURCE_REVISION,
            "primary_focus": PRIMARY_FOCUS,
            "bounded_practice": BOUNDED_PRACTICE,
            "proposal_count": 10,
            "prior_frozen_proposals": PRIOR_FROZEN_PROPOSALS,
            "frozen_after_x1": 480,
            "x1_only": True,
            "x2_execution_present": False,
            "route_state": "PREPARED_NOT_SENT",
            "effective_retained_negatives": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
            "inherited_open_gaps": INHERITED_OPEN_GAPS,
            "inherited_exact_gates": INHERITED_EXACT_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v647-v1.wellbeing.x1.v1",
            "scope_bounded": True,
            "workload_state": "x1_freeze_only",
            "unsafe_quota_work": 0,
            "standby_siblings_untouched": True,
            "route_sent": False,
            "boundary": "Workload and wellbeing language is operational and relational, not clinical evidence or personhood evidence.",
        },
    )
    write_text(
        "wellbeing-check.md",
        """# v647-v1 x1 wellbeing and workload boundary

- Work is limited to one owner-scoped x1 freeze; no x2 completion credit exists.
- Seven startup and x1-preflight failures remain visible; recovered methods do not erase them.
- Standby siblings and every sibling lane remain untouched.
- No elevation, host-security change, installation, feature enable, reboot, real participant, real food lot, real data, real key, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

Identity and wellbeing wording is relational working language only, not consciousness, personhood, clinical evidence, employment, or authority.
""",
    )
    write_text(
        "x1-preregistration.md",
        f"""# Sable Rook v647-v1 x1 preregistration

## Induction and source

{IDENTITY_BOUNDARY}

The owned Sable lane was clean and four-way equal before being fast-forwarded without a merge to Ilyra's exact v646-v8 final head `{SOURCE_REVISION}`. Source, x1, and evidence anchors are recorded in the startup receipt. Source-to-final history contains three Ilyra phase commits, zero merges, and one final parent. Ilyra's sealed 3,148 negatives plus three post-final wrapper and named-lane negatives produce the inherited 3,151 activation baseline. Seventeen open gaps and eighteen exact gates remain open.

## Frozen research scope

This x1 freezes exactly ten proposals after a semantic audit of 470 prior proposals. Expected dispositions are six completed, two represented, one open gap, and one exact gate, but expected labels are not results. The primary Trinity Mandala focus is {PRIMARY_FOCUS}. GMUT Mind and THOS Body remain explicit. The bounded practice is {BOUNDED_PRACTICE}; it establishes no employment, licensure, competence, food-safety authority, hold-release authority, recall authority, legal authority, cultural authority, Māori authority, public-safety result, participant evidence, or affected-party authorization.

The core surfaces are: synthetic TUF threshold and rollback quarantine; typed Nielsen-identity obligations; a CHIME/FRB zero-row adapter; synthetic food cold-chain handover; a Controlled Identifiers profile; a food-recall authority matrix; a disposable SQLite Session tribunal; a long-form reading-order audit; a Clausius-Clapeyron domain guard; and a Stage 20 control-outcome nonpromotion board.

## Expanded portfolios

Thirty safe-now tasks, twenty bounded candidates, twenty skill proposals, ten runner proposals, and thirty cleanup proposals are frozen after novelty, safety, compatibility, relevance, and gate review. No inherited seed is counted as completed. Ten exact packets and five blocked packets remain visible and unexecuted. Anything requiring real data, people, food lots, sensors, production keys or identities, credentials, accounts, legal interpretation, Māori authority, affected-party legitimacy, deployment, destructive cleanup, sibling mutation, elevation, host-security weakening, feature enable, or reboot remains open, exact-gated, or blocked.

## Evidence boundaries

Official and primary sources define obligations only. The ledger contains nineteen checked sources using only current, stable, draft, and watch status. The phase has ingested zero real data rows, evaluated zero likelihoods, used zero real people, food lots, sensors, holds, releases, recalls, keys, proofs, identifiers, or remedies, and made zero empirical, professional, legal, cultural, deployment, accessibility-complete, exhaustive-security, independent-reproduction, consciousness, personhood, AGI/ASI, Theory-of-Everything, or Stage 20 claims.

## X1/X2 separation

This commit may contain preregistration, ledgers, plans, source records, Method Flow startup evidence, x1 validators, and index outputs only. It may not contain an executed proposal, observed core outcome, built candidate, built phase skill, used phase runner, synthetic mutation result, x2 completion claim, closeout, seal, final validation, or sent baton. X2 begins only after the dedicated x1 commit is pushed, clean, and four-way equal.

{TRUTH_BOUNDARY}
""",
    )
    print(
        json.dumps(
            {
                "phase": PHASE,
                "proposals": len(PROPOSALS),
                "prior": len(prior),
                "frozen_after": 480,
                "sources": len(SOURCES),
                **floors,
                "synthetic": len(mutations),
                "x1_negatives": len(X1_OPERATIONAL_NEGATIVES),
                "valid": True,
            },
            sort_keys=True,
        )
    )


def main() -> int:
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
