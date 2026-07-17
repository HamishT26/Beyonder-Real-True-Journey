#!/usr/bin/env python3
"""Build Ilyra Fen v647-v6 combined closeout and seal candidate records."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
SOURCE_COMMIT = "3c4fa7ba58362ae39a5aa009fe9a899acc092301"
X1_COMMIT = "650e9f0e6d17118cf8b2389adf2a984cfc63cf08"
EVIDENCE_COMMIT = "400f5af29759a624bf4f095b50b4c7468e3a25b9"
EXCLUDED_OWNER_PATHS = {
    "validation/final-owner-manifest.json",
    "validation/final-validation-candidate.json",
    "validation/closeout-staged-manifest.json",
    "validation/closeout-staged-review.json",
}
BOUNDARY = (
    "Combined closeout and seal candidate only. Exact final-head, clean-state, remote-equality, and named-replay "
    "claims require post-commit validation. Same-owner evidence is not independent reproduction."
)


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def prospective_blob(relative: str) -> str:
    return git("hash-object", f"--path={relative}", relative)


def refresh_index() -> None:
    index = read_json("tooling/ghc-family-index.json")
    index["phase_refresh"] = {
        "phase": "v647-gmut-thos-v6-x1-x2",
        "owner": "Ilyra Fen",
        "state": "closeout_candidate_prepared_not_sent",
        "evidence_commit": EVIDENCE_COMMIT,
        "family_current_runners": [
            "ghc_family_watcher_reconciliation_tribunal.py",
            "ghc_family_barnes_rivers_obligations.py",
            "ghc_family_sdss_dr19_zero_row.py",
            "ghc_family_weather_warning_handover.py",
            "ghc_family_oauth_token_exchange_profile.py",
            "ghc_family_png_chunk_tribunal.py",
            "ghc_family_treegrid_audit.py",
            "ghc_family_gibbs_phase_rule.py",
            "ghc_family_covariate_shift_board.py",
            "ghc_family_v647_v6_validation_runner.py",
        ],
        "method_flow_guards": 18,
        "historical_names_preserved": True,
        "publication_boundary": "repository-relative names only",
    }
    write_json("tooling/ghc-family-index.json", index)
    write_text(
        "tooling/ghc-family-index.md",
        """# GHC Family Index — Ilyra Fen v647-v6

This phase-local refresh follows the family routing precedence: current phase truth, family-current names, then historical compatibility surfaces. It records repository-relative names only.

## Current phase surfaces

- Ten family-compatible runners were invoked with bounded witnesses.
- Twenty phase-local skills were initialized, validated, and smoke-used without global installation.
- Eighteen Method Flow guards retain eighteen failed and eighteen passing witnesses.
- The x1 freeze is immutable at its exact commit; x2 evidence is immutable at its exact evidence commit.
- Historical and owner-specific names remain compatibility evidence and were not destructively renamed.

## Current routing state

The successor route remains `PREPARED_NOT_SENT`. Exact final-head, remote-equality, and one named same-owner replay are required before a single sanitized baton may be sent. This index does not claim independent reproduction, empirical confirmation, production readiness, professional authority, legal or cultural ratification, Māori authority, complete accessibility, exhaustive security, or Stage 20 readiness.
""",
    )


def build_owner_manifest() -> None:
    entries = []
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        phase_relative = path.relative_to(PHASE).as_posix()
        if phase_relative in EXCLUDED_OWNER_PATHS:
            continue
        repository_relative = path.relative_to(ROOT).as_posix()
        entries.append(
            {
                "path": phase_relative,
                "git_blob": prospective_blob(repository_relative),
                "working_bytes": path.stat().st_size,
            }
        )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v647-v6.final-owner-manifest.v1",
            "hash_domain": "Git filtered prospective blob identity",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": sorted(EXCLUDED_OWNER_PATHS),
            "declared_exclusion_count": len(EXCLUDED_OWNER_PATHS),
            "owner_path_count": len(entries) + len([path for path in EXCLUDED_OWNER_PATHS if (PHASE / path).is_file()]),
            "boundary": "All public owner paths except four declared lifecycle self-exclusions; exact committed parity is rechecked after commit.",
        },
    )


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout builder requires immutable evidence head {EVIDENCE_COMMIT}, got {head}")
    evidence_validation = read_json("validation/evidence-validation.json")
    if evidence_validation.get("valid") is not True:
        raise RuntimeError("evidence validation is not valid")
    phase_truth = read_json("phase-truth.json")
    negatives = read_json("retained-negative-register-x2.json")
    gates = read_json("exact-open-gate-register-x2.json")
    methods = read_json("method-flow/method-flow-state.json")
    proposals = read_json("x2-proposal-ledger.json")
    evidence_review = read_json("validation/evidence-staged-review.json")
    if evidence_review.get("valid") is not True:
        raise RuntimeError("exact evidence staged review is not valid")

    route = {
        "schema": "ghc.family.v647-v6.terminal-route-state.v1",
        "state": "PREPARED_NOT_SENT",
        "successor_title": "Sable Rook",
        "successor_phase": "v647-gmut-thos-v7-x1-x2",
        "message_sent": False,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "send_gate": "exact final commit, four-way remote equality, clean canonical lane, and one clean named local-only replay",
        "boundary": "Preparation is not delivery. Only one existing-task message is permitted after every proof passes.",
    }
    write_json("orchestration/terminal-route-state.json", route)
    write_json(
        "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v647-v6.applicable-memory-record.v1",
            "phase": "v647-gmut-thos-v6-x1-x2",
            "portable_guards": [row["recurrence_guard"] for row in methods["methods"]],
            "failed_witnesses_preserved": methods["counts"]["witness_results"]["fail"],
            "passing_witnesses_preserved": methods["counts"]["witness_results"]["pass"],
            "private_state_included": False,
            "boundary": "Repository-scoped sanitized memory only; it grants no identity continuity or authority.",
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v647-v6.successor-baton-preparation.v1",
            "state": "PREPARED_NOT_SENT",
            "required_contents": [
                "exact source, x1, evidence, and final commits",
                "scoped tests and detailed/minimal validation counts",
                "JSON and five-class privacy counts",
                "manifest coverage and clean named replay",
                "outcome distribution, retained negatives, open gaps, exact gates, and NOT_READY_FOR_STAGE_20",
            ],
            "private_identifiers_allowed": False,
            "boundary": "No baton has been sent by this phase record.",
        },
    )
    phase_truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_final_validation_required": True,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json("phase-truth.json", phase_truth)
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v647-v6.phase-anchor-contract.v1",
            "source_commit": SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_phase_commits_after_final": 3,
            "maximum_phase_commits": 4,
            "zero_merges_required": True,
            "single_parent_final_required": True,
            "post_commit_exact_final_head_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v647-v6.closeout-receipt.v1",
            "source_commit": SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "outcomes": proposals["outcome_counts"],
            "effective_negatives": negatives["effective_total"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_fail_witnesses": methods["counts"]["witness_results"]["fail"],
            "method_pass_witnesses": methods["counts"]["witness_results"]["pass"],
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy_file_count"],
            "privacy_hits": len(evidence_validation["privacy_confirmed_hits"]),
            "full_repository_suite_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "post_commit_final_validation_completed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v647-v6.seal-receipt.v1",
            "x1_content_seal_valid": read_json("reproduction/x1-content-seal.json")["mismatch_count"] == 0,
            "evidence_staged_review_valid": evidence_review["valid"],
            "evidence_commit": EVIDENCE_COMMIT,
            "closeout_tree_ready_for_commit": True,
            "exact_final_commit_known_inside_own_tree": False,
            "post_commit_seal_check_required": True,
            "boundary": "This receipt seals the candidate content contract; it does not preclaim the final commit or replay result.",
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v647-v6.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "steps": [
                "commit the reviewed closeout and seal tree as one direct child of evidence",
                "push and prove local, upstream, tracking, and fresh live-remote equality",
                "run the bounded final validator at the exact final head",
                "create exactly one clean named local-only replay lane at the exact final head",
                "rerun the same bounded validation read-only with an explicit external JSON filename",
                "verify manifest, ancestry, three phase commits, zero merges, one parent, and clean before and after",
            ],
            "completed": False,
            "preclaims_exact_final_head": False,
            "preclaims_named_replay": False,
            "preclaims_baton_sent": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "reproduction/same-owner-replay-plan.json",
        {
            "schema": "ghc.family.v647-v6.same-owner-replay-plan.v1",
            "state": "PENDING_POST_COMMIT",
            "named_local_only": True,
            "detached": False,
            "pushed": False,
            "upstream_allowed": False,
            "independent_reproduction": False,
            "boundary": "A later clean named replay may establish same-owner repeatability only.",
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v647-v6.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "ten distinct proposals with 6 completed, 2 represented, 1 open_gap, and 1 exact_gate",
                "thirty safe tasks, twenty candidates, twenty skills, ten runners, and thirty additive cleanup tasks",
                "seventy rejected synthetic negatives",
                "bounded evidence validation and exact staged review",
                "accessible static report with manual and affected-user evaluation reserved",
            ],
            "pending_post_commit": [
                "exact final head and four-way remote equality",
                "one clean named local-only same-owner replay",
                "single sanitized successor baton",
            ],
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, resolution, status, interoperability, privacy and security review, recovery, and governance",
                "affected-party, legal, cultural, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v647-v6.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POST_COMMIT_PROOF_PENDING",
            "source_commit": SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_replay_state": "PENDING_POST_COMMIT",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    refresh_index()

    document_rows = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            words = len(path.read_text(encoding="utf-8").split())
            document_rows.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_cap": words <= 6000})
    write_json(
        "validation/document-cap-receipt.json",
        {
            "schema": "ghc.family.v647-v6.document-cap.v1",
            "document_count": len(document_rows),
            "maximum_words": max(row["words"] for row in document_rows),
            "all_under_6000": all(row["under_cap"] for row in document_rows),
            "documents": document_rows,
        },
    )
    owner_files = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json(
        "validation/owner-file-threshold-receipt.json",
        {
            "schema": "ghc.family.v647-v6.owner-file-threshold.v1",
            "owner_file_count_before_manifest": owner_files,
            "threshold": 15000,
            "below_threshold": owner_files < 15000,
            "inherited_repository_baseline_counted": False,
        },
    )
    build_owner_manifest()
    print(json.dumps({"closeout": "prepared", "head": head, "negatives": negatives["effective_total"], "route": route["state"]}))


if __name__ == "__main__":
    build()
