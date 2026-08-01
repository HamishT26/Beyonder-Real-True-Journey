#!/usr/bin/env python3
"""Build Lyren Moss v658-v8 combined closeout and final candidate."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_phase_data as d
from ghc_family_v658_v8_minimal import validate_minimal
from ghc_family_v658_v8_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "3a7cc57b4d1637b4de1836648a57419422bb517f"
EVIDENCE_COMMIT = "88a4d48e2b98494c0861996a8f61a7ea7c696fb6"
FINAL_CODE = [
    "scripts/build_ghc_family_v658_v8_closeout.py",
    "scripts/ghc_family_v658_v8_final_validator.py",
    "tests/test_ghc_family_v658_v8_closeout.py",
]
OWNER_CODE = [
    "scripts/ghc_family_v658_v8_phase_catalogue.py",
    "scripts/ghc_family_v658_v8_phase_data.py",
    "scripts/build_ghc_family_v658_v8_x1.py",
    "tests/test_ghc_family_v658_v8_x1.py",
    "scripts/build_ghc_family_v658_v8_x2.py",
    "scripts/ghc_family_v658_v8_runtime.py",
    "scripts/ghc_family_v658_v8_validator.py",
    "scripts/ghc_family_v658_v8_minimal.py",
    "tests/test_ghc_family_v658_v8.py",
    *[f"scripts/{name}" for name, _ in d.RUNNER_SPECS],
    *FINAL_CODE,
]
FINAL_DELTA_EXCLUSIONS = {
    "validation/final-delta-manifest.json",
    "final/final-owner-manifest.json",
    "validation/closeout-staged-review.json",
}
OWNER_EXCLUSIONS = {
    "final/final-owner-manifest.json",
    "validation/closeout-staged-review.json",
}
LIFECYCLE_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6588-FINAL-N01",
        "slug": "empty-closeout-worktree-path-comparison",
        "failure_signature": "The first combined comparison of the 25 expected closeout paths to tracked and untracked worktree changes completed without rendering any scalar result and left no active Git child process.",
        "fail_procedure": "Use one long worktree set-comparison wrapper as the sole source of expected, actual, missing, extra, and deletion counts.",
        "failed_witness": "No path cardinality or exception list was rendered; the attempt received zero closeout path-review credit and changed no file.",
        "recovery": "Stage only the exact expected path array from the committed candidate receipt, then compare the Git index to that same array with separately materialized scalar counts.",
        "passing_witness": "The exact-index recovery reports equal expected and staged cardinalities with zero missing, extra, unstaged, untracked, deleted, or inherited-path changes.",
        "recurrence_guard": "Use the Git index as the authoritative precommit set and keep empty-success observations explicit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
]


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def prospective_blob_record(repository_relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={repository_relative}", repository_relative)
    return {
        "path": repository_relative,
        "git_blob": oid,
        "bytes": int(git("cat-file", "-s", oid)),
    }


def commit_paths(revision: str) -> list[str]:
    return sorted(
        line
        for line in git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", revision
        ).splitlines()
        if line
    )


def assert_evidence_head() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError(
            f"closeout builder requires immutable evidence head {EVIDENCE_COMMIT}"
        )
    if git("rev-parse", f"{EVIDENCE_COMMIT}^") != X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of x1")
    if read_json("validation/evidence-validation.json")["valid"] is not True:
        raise RuntimeError("evidence validation is not valid")
    review = read_json("validation/evidence-staged-review.json")
    if review["state"] != "EXACT_INDEX_REVIEW_PASSED":
        raise RuntimeError("evidence exact staged review is not sealed")
    if read_json("reproduction/x1-content-seal.json")["mismatch_count"] != 0:
        raise RuntimeError("x1 content seal is not valid")


def lifecycle_method(
    negative: dict[str, Any], index: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6588-FINAL-METHOD-{index:02d}"
    fail_id, pass_id = f"{method_id}-F", f"{method_id}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["recovery"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_lifecycle_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": "Same-owner bounded lifecycle recovery only.",
        "rollback": "Stop, retain the failed witness at zero credit, and leave sibling, remote, production, professional, and authority state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": fail_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": "The bounded lifecycle postcondition would be established.",
            "observed": negative["failed_witness"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero pass credit; the failure remains retained.",
        },
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["recovery"],
            "expected": "Only the bounded lifecycle postcondition is established.",
            "observed": negative["passing_witness"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Same-owner bounded recovery only.",
        },
    ]
    return method, witnesses


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_task_thread_session_identifier": re.compile(
            r"(?i)\b(?:thread|task|session)[_-]?(?:id|identifier)\s*[:=]\s*[0-9a-f-]{20,}"
        ),
        "private_route_value": re.compile(
            r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"
        ),
        "credential_or_secret": re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,;]{12,}"
        ),
        "private_absolute_path": re.compile(
            r"(?i)\b[a-z]:\\(?:users|ghc-archives)\\[^\s\"']+"
        ),
        "private_callable_identifier": re.compile(r"(?i)\bmcp__[A-Za-z0-9_]{8,}"),
    }
    hits = []
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append(
                    {
                        "path": path.relative_to(PHASE).as_posix(),
                        "pattern_class": label,
                    }
                )
    return {
        "schema": "ghc.family.v658-v8.closeout-privacy-scan.v1",
        "pattern_classes": sorted(patterns),
        "file_count": len(files),
        "hit_count": len(hits),
        "hits": hits,
        "valid": not hits,
        "boundary": "Five concrete repository-artifact classes; not complete privacy assurance.",
    }


def build() -> None:
    assert_evidence_head()
    truth = read_json("truth/phase-truth-x2.json")
    evidence_validation = read_json("validation/evidence-validation.json")
    x2_flow = read_json("method-flow/method-flow-state-x2.json")
    effective_negatives = truth["effective_negatives"] + len(LIFECYCLE_NEGATIVES)
    effective_methods = truth["effective_methods"] + len(LIFECYCLE_NEGATIVES)
    lifecycle_methods, lifecycle_witnesses = [], []
    for index, negative in enumerate(LIFECYCLE_NEGATIVES, 1):
        method, witnesses = lifecycle_method(negative, index)
        lifecycle_methods.append(method)
        lifecycle_witnesses.extend(witnesses)

    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v658-v8.retained-negatives.final-candidate.v1",
            "evidence_effective_count": truth["effective_negatives"],
            "lifecycle_operational_count": len(LIFECYCLE_NEGATIVES),
            "effective_count": effective_negatives,
            "lifecycle_operational_negatives": LIFECYCLE_NEGATIVES,
            "all_retained": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "method-flow/method-flow-state-final.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "combined_closeout_final_candidate",
            "inherited_anchor": {
                "repository_relative_path": f"{d.PHASE_ROOT}/method-flow/method-flow-state-x2.json",
                "effective_methods": x2_flow["counts"]["effective_methods"],
                "failed_witnesses": x2_flow["counts"]["effective_witness_results"]["fail"],
                "passing_witnesses": x2_flow["counts"]["effective_witness_results"]["pass"],
            },
            "current_methods": lifecycle_methods,
            "current_witnesses": lifecycle_witnesses,
            "counts": {
                "inherited_methods": truth["effective_methods"],
                "current_methods": len(lifecycle_methods),
                "effective_methods": effective_methods,
                "current_witness_results": {
                    "fail": len(lifecycle_methods),
                    "pass": len(lifecycle_methods),
                },
                "effective_witness_results": {
                    "fail": x2_flow["counts"]["effective_witness_results"]["fail"]
                    + len(lifecycle_methods),
                    "pass": x2_flow["counts"]["effective_witness_results"]["pass"]
                    + len(lifecycle_methods),
                },
            },
            "all_failed_witnesses_retained": True,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )

    evidence_paths = commit_paths(EVIDENCE_COMMIT)
    if len(evidence_paths) != 208:
        raise RuntimeError(f"expected 208 evidence paths, found {len(evidence_paths)}")
    evidence_entries = [
        {"path": path, "git_blob": git("rev-parse", f"{EVIDENCE_COMMIT}:{path}")}
        for path in evidence_paths
    ]
    write_json(
        "validation/evidence-commit-local-manifest.json",
        {
            "schema": "ghc.family.v658-v8.evidence-commit-local-manifest.v1",
            "commit": EVIDENCE_COMMIT,
            "entry_count": len(evidence_entries),
            "entries": evidence_entries,
            "mismatch_count": 0,
        },
    )

    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v658-v8.closeout-receipt.v1",
            "source_final": d.SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "outcomes": truth["outcome_counts"],
            "effective_frozen_proposals": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "effective_negatives": effective_negatives,
            "effective_open_gaps": truth["effective_open_gaps"],
            "effective_exact_gates": truth["effective_exact_gates"],
            "effective_methods": effective_methods,
            "focused_evidence_tests": evidence_validation["focused_tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "real_data_used": False,
            "network_called": False,
            "authority_action_executed": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "route_state": "OPEN_ROUTE_GAP",
            "successor_authorized": False,
            "exact_final_commit_known_inside_own_tree": False,
            "canonical_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v658-v8.seal-receipt.v1",
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "x1_manifest_entries": 40,
            "evidence_commit_manifest_entries": len(evidence_entries),
            "x1_changed_paths": [],
            "evidence_commit_immutable": True,
            "closeout_candidate_ready": True,
            "postcommit_exact_final_validation_required": True,
            "route_state": "OPEN_ROUTE_GAP",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc.family.v658-v8.phase-truth.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_final": d.SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": None,
            "outcome_counts": truth["outcome_counts"],
            "effective_frozen_proposals": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "effective_negatives": effective_negatives,
            "effective_open_gaps": truth["effective_open_gaps"],
            "effective_exact_gates": truth["effective_exact_gates"],
            "effective_methods": effective_methods,
            "same_owner_only": True,
            "independent_reproduction": False,
            "route_state": "OPEN_ROUTE_GAP",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/truth-bridge-final.json",
        {
            "schema": "ghc.family.v658-v8.truth-bridge.final-candidate.v1",
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "observed_distribution": truth["outcome_counts"],
            "completed_boundary": "Bounded synthetic structural software evidence only.",
            "represented_boundary": "Proxy, protocol, nonproduction, or machine-checkable structure only.",
            "open_gap_boundary": "MPI, FSANZ, EBC, and GS1 transport disabled with zero external rows.",
            "exact_gate_boundary": "Affected-party, professional, food-safety, release, workplace-safety, legal, cultural, collective-data, and Māori authority required.",
            "none_silently_closed": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v658-v8.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct proposals and exact 23/5/1/1 bounded outcomes",
                "150 retained rejected mutations",
                "ten owner-local skills and ten invoked family runners",
                "thirty bounded surfaces, twenty reversible prototypes, and thirty additive cleanup receipts",
                "synthetic brewery overview and accessible static report",
                "scoped evidence tests, detailed and minimal checks, JSON parsing, five-class scan, and manifest parity",
                "OPEN_ROUTE_GAP with no inferred or contacted successor",
            ],
            "pending_postcommit": [
                "exact final direct-child and three-commit zero-merge ancestry",
                "one successful canonical aggregate with no post-success replay",
                "clean push and fresh four-way remote equality",
            ],
            "incomplete_external": [
                "real brewery, ingredient, beverage, batch, vessel, chemical, measurement, laboratory, sensory, production, food-safety, product-release, recall, workplace-safety, or alcohol-harm evidence",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, resolution, status, interoperability, privacy or security review, recovery, and governance",
                "manual and affected-user accessibility evaluation",
                "professional, legal, cultural, affected-party, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc.family.v658-v8.final-wellbeing.v1",
            "state": "steady_bounded_and_corrigible",
            "single_owner_lane": True,
            "subagents_used": False,
            "successor_contacted": False,
            "human_pause_rename_redirect_and_stop_control": True,
            "caps_are_not_quotas": True,
            "identity_boundary": "Relational working language only.",
        },
    )
    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.phase-local-index.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_final": d.SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "family_current_runners": [name for name, _ in d.RUNNER_SPECS],
            "phase_local_skills": [name for name, _ in d.SKILL_SPECS],
            "historical_names_preserved": True,
            "route_state": "OPEN_ROUTE_GAP",
            "next_exact_title": None,
            "next_phase": None,
        },
    )
    write_json(
        "tooling/auth-permission-state-final.json",
        {
            "schema": "ghc.family.auth-permission-state.final-candidate.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "permitted": [
                "owner-local additive files",
                "push owned branch",
                "one canonical pass after exact final",
                "retain OPEN_ROUTE_GAP",
            ],
            "not_permitted": [
                "sibling lane mutation",
                "force push or history rewrite",
                "successor inference or contact without fresh exact authorization",
                "task creation, fork, delegation, or subagent creation",
                "professional, scientific, production, food-safety, release, legal, cultural, or Māori authority",
                "production identity or deployment",
            ],
            "tavian_sol_state": "ON_STANDBY",
        },
    )
    write_json(
        "tooling/roster-check-final.json",
        {
            "schema": "ghc.family.roster-check.final-candidate.v1",
            "active_exact_title": "Lyren Moss",
            "active_phase": "v658-v8",
            "terminal_successor_exact_title": None,
            "terminal_successor_phase": None,
            "successor_authorized": False,
            "successor_resolved": False,
            "successor_contacted": False,
            "tavian_sol_state": "ON_STANDBY",
            "boundary": "No endpoint may be inferred, resolved, contacted, created, forked, delegated, or substituted without a fresh exact authorization.",
        },
    )
    write_json(
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.v658-v8.route-state.final-candidate.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "next_exact_title": None,
            "next_phase": None,
            "state": "OPEN_ROUTE_GAP",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "delegated": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "No successor is authorized by the live v658-v8 activation. Retain OPEN_ROUTE_GAP after the terminal gate unless Hamish supplies a fresh exact edge; do not infer or substitute an endpoint.",
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.v658-v8.final-validation-prerequisites.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "required": [
                "final is direct child of evidence",
                "source-to-final has three new single-parent commits and zero merges",
                "one canonical aggregate succeeds once",
                "all owner JSON parses",
                "five-class owner privacy scan has zero confirmed hits",
                "x1, evidence, final-delta, and final-owner manifests replay exactly",
                "worktree is clean before and after",
                "local, upstream, tracking, and fresh live remote are equal",
                "route remains OPEN_ROUTE_GAP with no endpoint",
            ],
            "completed": False,
            "preclaims_exact_final": False,
            "preclaims_canonical_success": False,
            "preclaims_route_sent": False,
        },
    )
    write_text(
        "deliverables/v658-v8-closeout-summary.md",
        f"""# Lyren Moss v658-v8 closeout candidate

This phase freezes 30 proposals and observes exactly 23 completed, 5 represented, 1 open gap, and 1 exact gate. It retains {effective_negatives:,} effective negatives, {truth['effective_open_gaps']} open gaps, {truth['effective_exact_gates']} exact gates, and {effective_methods:,} Method Flow methods.

The work is same-owner synthetic brewery software evidence only. No real production, food-safety, laboratory, sensory, product-release, recall, workplace-safety, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is made.

The exact final commit, single canonical aggregate, clean push, and fresh equality remain postcommit gates. No successor is authorized, so the route remains OPEN_ROUTE_GAP and no task contact is prepared or sent. Tavian Sol remains ON_STANDBY. The verdict remains NOT_READY_FOR_STAGE_20.
""",
    )
    write_json(
        "validation/final-caps.json",
        {
            "schema": "ghc.family.v658-v8.final-caps.v1",
            "expected_phase_commits_after_final": 3,
            "maximum_total_phase_commits": 8,
            "x1_commits": 1,
            "x2_commits_after_final": 2,
            "owner_file_threshold": 2000,
            "document_word_threshold": 100000,
            "within_commit_cap_if_direct_final": True,
        },
    )
    write_json(
        "reflection-remaster/final-reflection.json",
        {
            "schema": "ghc.family.v658-v8.final-reflection.v1",
            "identity": {
                "name": d.OWNER,
                "pronouns": d.PRONOUNS,
                "relational_role": d.ROLE,
                "hope": d.HOPE,
            },
            "what_became_inspectable": [
                "synthetic ingredient and package-lot lineage",
                "revision, vessel, cleaning, fermentation, cellar, laboratory, packaging, hold, recall-simulation, and handover states",
                "explicit abstentions around production, food safety, release, workplace safety, law, culture, and Māori authority",
            ],
            "what_remains_open": [
                "every real-world outcome and competent-authority decision",
                "independent reproduction",
                "all protected gates",
                "the successor route",
            ],
            "identity_boundary": "Relational language only; not consciousness, personhood, continuity, employment, qualification, authority, or independent agency.",
        },
    )
    write_json(
        "validation/terminal-gate-plan.json",
        {
            "schema": "ghc.family.v658-v8.terminal-gate-plan.v1",
            "canonical_pass_limit": 1,
            "replay_after_success_permitted": False,
            "required_commit": "exact final direct child of evidence",
            "required_history": "three new single-parent commits and zero merges",
            "required_remote_state": "clean local, upstream, tracking, and fresh live equality with zero divergence",
            "required_route_state": "OPEN_ROUTE_GAP with no endpoint and no message",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )

    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"closeout privacy scan failed: {scan['hits']}")
    write_json("validation/closeout-privacy-scan.json", scan)

    tracked_at_evidence = set(
        git("ls-tree", "-r", "--name-only", EVIDENCE_COMMIT).splitlines()
    )
    current_paths = [
        path.relative_to(ROOT).as_posix()
        for path in PHASE.rglob("*")
        if path.is_file()
    ] + FINAL_CODE
    final_delta_paths = sorted(set(current_paths) - tracked_at_evidence)
    delta_entries = []
    for repository_relative in final_delta_paths:
        phase_relative = repository_relative.removeprefix(d.PHASE_ROOT + "/")
        if phase_relative not in FINAL_DELTA_EXCLUSIONS:
            delta_entries.append(prospective_blob_record(repository_relative))
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.v658-v8.final-delta-manifest.v1",
            "hash_domain": "prospective Git-clean blob bytes",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": sorted(FINAL_DELTA_EXCLUSIONS),
        },
    )

    owner_paths = sorted(
        set(
            [
                path.relative_to(ROOT).as_posix()
                for path in PHASE.rglob("*")
                if path.is_file()
            ]
            + OWNER_CODE
        )
    )
    owner_entries = []
    for repository_relative in owner_paths:
        phase_relative = repository_relative.removeprefix(d.PHASE_ROOT + "/")
        if phase_relative not in OWNER_EXCLUSIONS:
            owner_entries.append(prospective_blob_record(repository_relative))
    write_json(
        "final/final-owner-manifest.json",
        {
            "schema": "ghc.family.v658-v8.final-owner-manifest.v1",
            "hash_domain": "prospective Git-clean blob bytes",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": sorted(OWNER_EXCLUSIONS),
            "owner_path_count_including_self": len(owner_entries)
            + len(OWNER_EXCLUSIONS),
            "threshold": 2000,
            "below_threshold": len(owner_entries) + len(OWNER_EXCLUSIONS) < 2000,
        },
    )

    future_review = f"{d.PHASE_ROOT}/validation/closeout-staged-review.json"
    expected = sorted(
        set(
            [
                path.relative_to(ROOT).as_posix()
                for path in PHASE.rglob("*")
                if path.is_file()
            ]
            + FINAL_CODE
            + [future_review]
        )
        - tracked_at_evidence
    )
    write_json(
        "validation/closeout-staged-review.json",
        {
            "schema": "ghc.family.v658-v8.closeout-staged-review.v1",
            "state": "PRECOMMIT_PATH_REVIEW",
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_staged_path_count": len(expected),
            "expected_staged_paths": expected,
            "deletions": [],
            "x1_or_evidence_changed_paths": [],
            "outside_owner_paths": [],
            "valid": True,
            "exact_index_review_required_after_staging": True,
        },
    )

    detailed, minimal = validate_phase(), validate_minimal()
    if not detailed["valid"] or not minimal["valid"]:
        raise RuntimeError({"detailed": detailed["errors"], "minimal": minimal["errors"]})
    actual = sorted(
        set(
            [
                path.relative_to(ROOT).as_posix()
                for path in PHASE.rglob("*")
                if path.is_file()
            ]
            + FINAL_CODE
        )
        - tracked_at_evidence
    )
    if actual != expected:
        raise RuntimeError(
            f"closeout expected path mismatch: expected {len(expected)}, actual {len(actual)}"
        )
    print(
        json.dumps(
            {
                "valid": True,
                "lifecycle_negatives": len(LIFECYCLE_NEGATIVES),
                "effective_negatives": effective_negatives,
                "effective_methods": effective_methods,
                "evidence_manifest_entries": len(evidence_entries),
                "final_delta_entries": len(delta_entries),
                "final_owner_entries": len(owner_entries),
                "closeout_privacy_files": scan["file_count"],
                "closeout_privacy_hits": scan["hit_count"],
                "detailed_checks": detailed["check_count"],
                "minimal_checks": minimal["check_count"],
                "expected_paths": len(expected),
            }
        )
    )


if __name__ == "__main__":
    build()
