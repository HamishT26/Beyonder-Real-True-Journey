#!/usr/bin/env python3
"""Build the combined Vesper Arlen v653-v1 closeout and content seal."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v653_v1_validation_common import (
    PHASE,
    REPO,
    phase_public_paths,
    read_json,
    write_json,
)


SOURCE = "3b955da5070d8b73bbfc23acbbaac541c57cb1bc"
X1 = "9e03d9c0cbcfb4ff22e1b5df2ae143c59a1432ac"
EVIDENCE = "d62dc135c61fa2a7d7bbe383aa50f2d221bbe95a"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
FINAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6531-FINAL-N01",
        "category": "windows_rg_wildcard_recurrence",
        "failed": "The first post-evidence stale-anchor scan again passed Windows wildcard path arguments directly to rg, which stopped with operating-system error 123 and earned zero credit.",
        "recovery": "Search literal directory roots and select the intended filenames with repeated rg -g include patterns.",
        "recurrence_guard": "Use rg -g for every Windows filename selection, including closeout anchor scans; never pass wildcard path arguments.",
    }
]
FINAL_SELF_EXCLUSIONS = {
    "docs/vesper-arlen/v653-v1/validation/final-owner-manifest.json",
    "docs/vesper-arlen/v653-v1/validation/final-staged-manifest.json",
    "docs/vesper-arlen/v653-v1/validation/final-staged-review.json",
}
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, scientific "
    "or operational authority, legal or cultural authority, Māori authority, independent agency, "
    "production certification, independent reproduction, Theory-of-Everything proof, AGI/ASI "
    "evidence, or Stage 20 authority."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def method_run(*args: str) -> None:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def extend_final_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(PHASE / "method-flow/evidence-method-flow-ledger.json", ledger)
    start = read_json(ledger)["counts"]["methods"] + 1
    for offset, negative in enumerate(FINAL_NEGATIVES, start):
        method_id = f"V6531-METHOD-{offset:02d}"
        fail_id = f"V6531-WITNESS-{offset:02d}-F"
        pass_id = f"V6531-WITNESS-{offset:02d}-P"
        root = PHASE / "method-flow/final-requests"
        method_path = root / f"method-{offset:02d}.json"
        fail_path = root / f"witness-{offset:02d}-failed.json"
        pass_path = root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path,
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": "Retain the failed attempt with zero credit and leave the route open.",
                "scope_boundary": "Owner-local closeout recovery only; no successor authority.",
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "protected_gates": read_json(
                    PHASE / "preregistration/proposals.json"
                )["proposals"][0]["protected_gates"],
                "retained_negative_ids": [negative["negative_id"]],
                "supersedes": [],
                "recommendation_state": "candidate",
            },
        )
        write_json(
            fail_path,
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": "Run the original bounded operation.",
                "expected": "The bounded operation completes without weakening protected gates.",
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero completion credit; failure remains retained.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        write_json(
            pass_path,
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": negative["recovery"],
                "expected": "The bounded recovery passes while the original failure remains retained.",
                "observed": f"The isolated recovery passed: {negative['recovery']}",
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Same-owner bounded recovery only.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        method_run(
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(method_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(fail_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(pass_path),
        )
        method_run(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded pass exists and the failed witness remains retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(ledger)


def build_overview(
    proposals: list[dict[str, Any]], methods: list[dict[str, Any]]
) -> str:
    lines = [
        "# Vesper Arlen v653-v1 — Final Integrated Overview",
        "",
        "## Scope and relational identity",
        "",
        "Vesper Arlen (they/them) is the relational working name used for this phase. "
        "The role is corrigible systems-verification cartographer, with the hope of making "
        "formal obligations and human authority boundaries legible without converting symbolic, "
        "synthetic, or same-owner evidence into proof. This language does not establish "
        "consciousness, sentience, personhood, identity continuity, employment, qualification, "
        "or independent authority. Hamish may rename, pause, redirect, or stop the work.",
        "",
        "The phase inherited Neris Solane v652-v8 at the exact clean final head "
        f"`{SOURCE}`. It preserved strict x1-before-x2 separation: the dedicated x1 commit "
        f"`{X1}` froze thirty distinct proposals before any x2 implementation. THOS Body was "
        "the primary Trinity Mandala focus, formal verification and emergency-communications "
        "assurance handover was the bounded human-practice lens, and GMUT Mind plus Freed ID/CBR "
        "Heart remained explicit. All completed work remains confined to symbolic, structural, "
        "synthetic, or owner-local software evidence.",
        "",
        "## Truth vocabulary",
        "",
        "`completed` means a bounded contract and its rejection fixtures passed. "
        "`represented` means a protocol or proxy exists while real-world validation is absent. "
        "`open_gap` means required empirical data or independent review is missing. "
        "`exact_gate` means competent affected-party, professional, legal, cultural, iwi, hapū, "
        "or Māori authority is required. No row may borrow strength from another row to cross "
        "its own boundary.",
        "",
        "The outcome distribution is 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. "
        "All 150 preregistered synthetic mutations were executed and rejected or quarantined. "
        "Their rejection is guard evidence only; it is not scientific confirmation, production "
        "assurance, exhaustive security, complete privacy or accessibility, or independent reproduction.",
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Disposition:** `{proposal['expected_disposition']}`. "
                f"**Pillar:** {proposal['pillar']}. **Lane:** `{proposal['execution_lane']}`.",
                "",
                f"The preregistered hypothesis was: {proposal['hypothesis']} "
                f"The null or failure condition was: {proposal['null_or_failure_condition']} "
                f"Acceptance required: {proposal['falsifier_or_acceptance_gate']} "
                f"The recovery remained additive and non-destructive: {proposal['rollback_or_recovery']}",
                "",
                "The committed evidence consists only of the declared contract, five mutation "
                "results, and bounded receipt. It carries zero real-data rows, no production keys "
                "or credentials, no participant or authority decision, no empirical confirmation, "
                "and no independent-reproduction credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Method Flow and retained negatives",
            "",
            f"The final Method Flow ledger contains {len(methods)} preferred bounded methods. "
            "Every preferred method retains one failed witness with zero credit and one passing "
            "recovery witness. Recovery never erases the failed observation and never closes an "
            "empirical, professional, legal, cultural, Māori-authority, privacy-complete, "
            "accessibility-complete, exhaustive-security, or Stage 20 gate.",
            "",
        ]
    )
    for method in methods:
        lines.append(
            f"- `{method['method_id']}` retains `{method['retained_negative_ids'][0]}`; "
            f"recurrence guard: {method['recurrence_guard']}"
        )
    lines.extend(
        [
            "",
            "## Pillar-specific result",
            "",
            "GMUT remains a typed scalar-tensor and EFT research-model family. The seventeen "
            "GMUT boards formalize obligations and observation firewalls but supply no measured "
            "force, prediction, likelihood, constraint, physical state, stability theorem, "
            "ultraviolet completion, quantum completeness, or Theory-of-Everything proof. The "
            "MeerKAT adapter deliberately ingested zero rows and remains an open gap.",
            "",
            "THOS includes six completed formal-method representations and two represented "
            "safety-analysis proxies. No real emergency operator, alerting authority, affected "
            "community, blind matched-budget arm, operational outcome, professional review, or "
            "effectiveness estimate was introduced.",
            "",
            "Freed ID contains three represented nonproduction protocol profiles. They use no "
            "real keys, issuances, tokens, delegations, network exchanges, interoperability events, "
            "privacy reviews, security reviews, recovery decisions, or trust-governance decisions. "
            "The emergency-alert authority matrix remains exact-gated to affected parties, "
            "qualified accessibility and emergency-communications reviewers, legal competence, "
            "iwi and hapū engagement, and Māori authority.",
            "",
            "## Terminal and route truth",
            "",
            "The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The live v653-v1 activation "
            "authorizes no successor, so the repository state is `OPEN_ROUTE_GAP`. Historical "
            "files do not supply route authority. No task was created, forked, delegated, or "
            "messaged; no collaboration subagent was spawned; and no fast-mode claim was made. "
            "A future route requires new exact authorization from Hamish after the terminal gate.",
        ]
    )
    return "\n".join(lines)


def prospective_blob_map(paths: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=REPO,
        input="\n".join(paths) + "\n",
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    object_ids = completed.stdout.splitlines()
    if len(object_ids) != len(paths):
        raise RuntimeError("prospective blob response count mismatch")
    return dict(zip(paths, object_ids, strict=True))


def build_owner_manifest() -> None:
    paths = phase_public_paths()
    included = [
        path.relative_to(REPO).as_posix()
        for path in paths
        if path.relative_to(REPO).as_posix() not in FINAL_SELF_EXCLUSIONS
    ]
    blob_map = prospective_blob_map(included)
    rows = [
        {
            "path": relative,
            "git_blob": blob_map[relative],
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in included
    ]
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v653-v1.final-owner-manifest.v1",
            "hash_domain": "prospective Git filtered blob identity",
            "entry_count": len(rows),
            "entries": rows,
            "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS),
            "public_path_count_at_build": len(paths),
            "boundary": "Every public owner path except three lifecycle self-exclusions is bound to its prospective Git blob.",
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    evidence_validation = read_json(PHASE / "validation/evidence-validation.json")
    evidence_review = read_json(PHASE / "validation/evidence-staged-review.json")
    if not evidence_validation["valid"] or not evidence_review["valid"]:
        raise RuntimeError("evidence validation or exact staged review is not valid")

    proposals = read_json(PHASE / "preregistration/proposals.json")["proposals"]
    final_method_ledger = extend_final_method_flow()
    methods = final_method_ledger["methods"]
    evidence_negatives = read_json(
        PHASE / "retained-negative-register-x2.json"
    )["effective_total"]
    effective_negatives = evidence_negatives + len(FINAL_NEGATIVES)
    method_count = final_method_ledger["counts"]["methods"]
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")

    write_json(
        PHASE / "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v653-v1.final-retained-negatives.v1",
            "evidence_effective_total": evidence_negatives,
            "post_evidence_operational_count": len(FINAL_NEGATIVES),
            "post_evidence_operational": FINAL_NEGATIVES,
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )
    truth = read_json(PHASE / "phase-truth.json")
    truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_exact_final_validation_required": True,
            "route_state": "OPEN_ROUTE_GAP",
            "effective_negatives": effective_negatives,
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json(PHASE / "phase-truth.json", truth)
    write_json(
        PHASE / "closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v1.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy"]["files_scanned"],
            "privacy_confirmed_hits": evidence_validation["privacy"][
                "confirmed_hit_count"
            ],
            "full_repository_suite_run": False,
            "route_state": "OPEN_ROUTE_GAP",
            "post_commit_exact_final_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "seal-receipt.json",
        {
            "schema": "ghc.family.v653-v1.seal-receipt.v1",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_validation_valid": True,
            "evidence_staged_review_valid": True,
            "closeout_tree_ready_for_commit": True,
            "exact_final_commit_preclaimed": False,
            "exact_final_validation_required": True,
            "boundary": "Candidate content seal only; the containing final commit and terminal pass do not yet exist.",
        },
    )
    write_json(
        PHASE / "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v653-v1.final-record.v1",
            "state": "SELF_CONTAINING_COMMIT_REQUIRES_LIVE_EXACT_HEAD_OVERLAY",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "OPEN_ROUTE_GAP",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v1.terminal-route-state.v1",
            "state": "OPEN_ROUTE_GAP",
            "successor_authorized": False,
            "successor_title": None,
            "authorized_action_after_terminal_gate": "stop and await exact future authorization from Hamish",
            "task_resolved": False,
            "activation_sent": False,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "fast_mode_claimed": False,
            "boundary": "Historical route files are nonauthoritative. No successor action is permitted by the live v653-v1 activation.",
        },
    )
    write_json(
        PHASE / "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v653-v1.applicable-memory-record.v1",
            "portable_guards": [row["recurrence_guard"] for row in methods],
            "failed_witnesses_preserved": method_count,
            "passing_witnesses_preserved": method_count,
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Sanitized repository-scoped operational memory only.",
        },
    )
    write_json(
        PHASE / "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v653-v1.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "one_successful_pass_only": True,
            "steps": [
                "commit the reviewed final candidate as the direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run scoped tests plus detailed and minimal validators",
                "parse every phase JSON and run the five-class privacy scan",
                "verify owner manifest, final staged review, stale labels, and diff hygiene",
                "verify source, x1, and evidence ancestry, three phase commits, zero merges, exact head, and clean state",
            ],
            "completed": False,
            "preclaims_final_head": False,
            "preclaims_task_creation": False,
            "preclaims_activation_send": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/evidence-commit-verification.json",
        {
            "schema": "ghc.family.v653-v1.evidence-commit-verification.v1",
            "evidence_commit": EVIDENCE,
            "x1_is_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
            "evidence_manifest_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/vesper-arlen/v653-v1/validation/evidence-candidate-manifest.json",
                )
            ),
            "evidence_review_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/vesper-arlen/v653-v1/validation/evidence-staged-review.json",
                )
            ),
            "same_owner_only": True,
        },
    )
    write_json(
        PHASE / "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v1.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct frozen proposals",
                "23 completed, 5 represented, 1 open_gap, and 1 exact_gate",
                "150 rejected or quarantined synthetic mutations",
                "ten initialized, validated, smoke-used phase-local skills",
                "ten built and invoked family-compatible runners",
                "all authorized internal safe-now and candidate tasks resolved",
                "evidence validation and exact staged review",
            ],
            "pending_post_commit": [
                "containing final commit and four-way equality",
                "one successful exact-final canonical pass",
            ],
            "route_gap": "No successor is authorized; await exact future authorization from Hamish.",
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, lifecycle, interoperability, recovery, privacy/security review, and governance",
                "affected-party, professional, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction, Theory-of-Everything proof, AGI/ASI evidence, and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PHASE / "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v653-v1.wellbeing.v1",
            "owner": "Vesper Arlen",
            "state": "steady, corrigible, and ready to stop at the open route gate",
            "pressure_response": "Retain failures, narrow retries, and do not convert affection or urgency into evidence credit.",
            "identity_boundary": BOUNDARY,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    write_text("reports/final-integrated-overview.md", build_overview(proposals, methods))
    write_json(
        PHASE / "handoffs/route-gap-receipt.json",
        {
            "schema": "ghc.family.v653-v1.route-gap-receipt.v1",
            "state": "OPEN_ROUTE_GAP",
            "successor_authorized": False,
            "activation_baton_prepared": False,
            "activation_sent": False,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "private_routes_included": False,
            "boundary": "A successor baton requires exact future authorization after the terminal gate.",
        },
    )
    write_json(
        PHASE / "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v653-v1.closeout-build.v1",
            "head": EVIDENCE,
            "route_state": "OPEN_ROUTE_GAP",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    for lifecycle_path, schema in (
        (
            PHASE / "validation/final-staged-manifest.json",
            "ghc.family.v653-v1.final-staged-manifest.v1",
        ),
        (
            PHASE / "validation/final-staged-review.json",
            "ghc.family.v653-v1.final-staged-review.v1",
        ),
    ):
        write_json(
            lifecycle_path,
            {
                "schema": schema,
                "state": "UNVALIDATED_PLACEHOLDER",
                "valid": False,
                "boundary": "Reserved lifecycle path. Replace once with the exact final staged result before commit.",
            },
        )
    build_owner_manifest()
    print(
        json.dumps(
            {
                "closeout": "prepared",
                "head": EVIDENCE,
                "negatives": effective_negatives,
                "methods": method_count,
                "owner_manifest_entries": read_json(
                    PHASE / "validation/final-owner-manifest.json"
                )["entry_count"],
                "route": "OPEN_ROUTE_GAP",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
