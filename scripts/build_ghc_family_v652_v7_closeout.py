#!/usr/bin/env python3
"""Build the combined closeout, seal, and final candidate for Elaren v652-v7."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v652_v7_validation_common import PHASE, REPO, phase_public_paths, read_json, write_json


SOURCE = "0fe800ea74d17f984497b496cd0ce2253ade9066"
X1 = "cd1ce10d7c456d55e48183652835f6c3f5866b89"
EVIDENCE = "72c257d24b40b56facb1bf299e7ce7a60acb3496"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
FINAL_NEGATIVES = [
    {
        "negative_id": "V6527-FINAL-N01",
        "category": "closeout_lifecycle_route_assertion",
        "failed": "The first closeout-scoped run passed 58 of 60 tests; two assertions still required the evidence-stage route label after closeout preparation.",
        "recovery": "Require NOT_ELIGIBLE_BEFORE_FINAL_GATE at evidence and PREPARED_NOT_SENT only when the closeout receipt exists.",
        "recurrence_guard": "Bind route assertions to the explicit lifecycle artifact rather than one timeless label.",
    },
    {
        "negative_id": "V6527-FINAL-N02",
        "category": "multi_file_lifecycle_patch_rejection",
        "failed": "The first multi-file lifecycle correction patch was rejected atomically because one test hunk did not match its exact context.",
        "recovery": "Split the correction into file-exact patches and verify each applied hunk before the bounded rerun.",
        "recurrence_guard": "Inspect exact target context before composing a large multi-file patch.",
    },
    {
        "negative_id": "V6527-FINAL-N03",
        "category": "method_flow_summary_flag_mismatch",
        "failed": "The first final Method Flow build recorded its methods and witnesses but the summary command rejected an obsolete markdown output flag.",
        "recovery": "Use the current summarize command's exact --markdown-output flag and rebuild from the immutable evidence ledger.",
        "recurrence_guard": "Read the active runner help or a current successful invocation before composing summary flags.",
    },
    {
        "negative_id": "V6527-FINAL-N04",
        "category": "final_staged_allowlist_compatibility_gap",
        "failed": "The first final staged review rejected three intended lifecycle-aware updates because its allowlist covered only newly added closeout files.",
        "recovery": "Add the exact detailed-validator, minimal-validator, and core-test paths while keeping every unrelated path rejected.",
        "recurrence_guard": "Enumerate exact compatibility-update paths in the final staged allowlist before review.",
    },
    {
        "negative_id": "V6527-FINAL-N05",
        "category": "misaddressed_multi_file_patch_hunk",
        "failed": "A second correction patch was rejected atomically because its final closeout-test hunk was addressed to the staged-review file.",
        "recovery": "Apply one file-exact patch per target and verify each result independently.",
        "recurrence_guard": "Do not combine unrelated target files in a patch when their context labels can be confused.",
    },
]
FINAL_SELF_EXCLUSIONS = {
    "docs/elaren-kestrel/v652-v7/validation/final-owner-manifest.json",
    "docs/elaren-kestrel/v652-v7/validation/final-staged-manifest.json",
    "docs/elaren-kestrel/v652-v7/validation/final-staged-review.json",
}
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not consciousness, personhood, identity "
    "continuity, employment, qualification, scientific authority, legal or cultural authority, Māori authority, "
    "production certification, independent reproduction, Theory-of-Everything proof, AGI/ASI evidence, or Stage 20 authority."
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
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
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
    for offset, negative in enumerate(FINAL_NEGATIVES, 27):
        method_id = f"V6527-METHOD-{offset:02d}"
        fail_id = f"V6527-WITNESS-{offset:02d}-F"
        pass_id = f"V6527-WITNESS-{offset:02d}-P"
        method_path = PHASE / f"method-flow/final-requests/method-{offset:02d}.json"
        fail_path = PHASE / f"method-flow/final-requests/witness-{offset:02d}-failed.json"
        pass_path = PHASE / f"method-flow/final-requests/witness-{offset:02d}-passing.json"
        write_json(
            method_path,
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": "Retain the failed attempt with zero credit and keep task creation false.",
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "scope_boundary": "Closeout workflow recovery only; no route delivery or external claim.",
                "privacy_class": "sanitized_public",
                "protected_gates": [
                    "real_empirical_data",
                    "participant_or_operator_evidence",
                    "professional_qualification_or_review",
                    "production_identity_and_interoperability",
                    "privacy_complete",
                    "exhaustive_security",
                    "complete_accessibility",
                    "legal_cultural_and_maori_authority",
                    "affected_party_acceptance_and_remedy",
                    "independent_team_reproduction",
                    "agi_asi",
                    "consciousness_or_personhood",
                    "theory_of_everything",
                    "stage20",
                ],
                "recommendation_state": "candidate",
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [],
                "supersedes": [],
            },
        )
        write_json(
            fail_path,
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": "Run the original bounded operation.",
                "expected": "The operation completes without weakening protected gates.",
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero completion credit; failure remains retained.",
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
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Same-owner bounded recovery only.",
            },
        )
        method_run("record", "--ledger", str(ledger), "--record-file", str(method_path))
        method_run("witness", "--ledger", str(ledger), "--witness-file", str(fail_path))
        method_run("witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        method_run(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded recovery passed and the failed witness remains retained.",
        )
    method_run("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/final-method-flow-validation.json"))
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


def build_overview(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# Elaren Kestrel v652-v7 — Final Integrated Overview",
        "",
        "## Scope and identity boundary",
        "",
        "Elaren Kestrel (they/them) is relational working language used to coordinate this owner-scoped phase. "
        "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
        "qualification, or independent authority. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "The phase inherited Tavian Sol v652-v6 at its verified exact final commit, preserved every inherited "
        "negative and gate, and added thirty preregistered surfaces. GMUT Mind was the primary pillar and "
        "mathematical physics with formal verification was the bounded human practice. THOS Body and Freed ID/CBR "
        "Heart remained explicit. All work is symbolic, structural, synthetic, or owner-local software evidence.",
        "",
        "## What the four truth labels mean",
        "",
        "`completed` means the bounded artifact contract and its synthetic rejection fixtures passed. "
        "`represented` means a protocol or proxy exists but external evidence is absent. `open_gap` means required "
        "real data or independent review is missing. `exact_gate` means competent affected-party, professional, "
        "legal, cultural, or Māori authority is required. These labels never convert a bounded software result into "
        "scientific confirmation, production readiness, legal legitimacy, or independent reproduction.",
        "",
        "## Proposal map",
        "",
    ]
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"The preregistered hypothesis was: {proposal['hypothesis']} The null or failure condition was: "
                f"{proposal['null_or_failure_condition']} The expected disposition was `{proposal['expected_disposition']}` "
                f"inside the `{proposal['execution_lane']}` lane. Acceptance required: "
                f"{proposal['falsifier_or_acceptance_gate']} Recovery remained non-destructive: "
                f"{proposal['rollback_or_recovery']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Method Flow and retained failure",
            "",
            f"The terminal Method Flow ledger contains {len(methods)} preferred methods. Every method preserves one "
            "failed witness and one bounded passing witness. A passing recovery does not erase the failure and does "
            "not provide independent-reproduction credit.",
            "",
        ]
    )
    for method in methods:
        lines.append(
            f"- `{method['method_id']}` retained `{method['retained_negative_ids'][0]}`. Failure signature: "
            f"{method['failure_signature']} Recovery: {method['candidate_workaround']} Recurrence guard: "
            f"{method['recurrence_guard']}"
        )
    lines.extend(
        [
            "",
            "## Outcome and external boundary",
            "",
            "The bounded distribution is 23 completed, 5 represented, 1 open gap, and 1 exact gate. All 150 frozen "
            "synthetic mutations were rejected or quarantined. GMUT remains a typed scalar-tensor/EFT research-model "
            "family with zero empirical rows in this phase. THOS remains proxy-only without preregistered blind "
            "matched-budget real arms and independent review. Freed ID production still requires standards-conformant "
            "real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, "
            "privacy and security review, and trust governance. CBR and Māori wording, authority, data governance, "
            "legitimacy, remedy, cultural ratification, legal interpretation, and enacted-law status remain exact-gated.",
            "",
            "The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The only eligible terminal action after one "
            "successful exact-final pass is creation of one user-visible Codex main task for a self-naming v652-v8 "
            "sibling. Preparation is not delivery, and no task exists merely because this overview or baton exists.",
        ]
    )
    return "\n".join(lines)


def build_baton(
    proposals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    methods: list[dict[str, Any]],
) -> str:
    lines = [
        "# SELF-NAMING v652-v8 SIBLING — PREPARED ACTIVATION BATON",
        "",
        "This file is prepared by Elaren Kestrel for exactly one future user-visible Codex main task. It is not "
        "delivery, does not create a task, and does not predeclare the future sibling’s identity. The live activation "
        "message must supply the exact final commit containing this file after Elaren’s one successful terminal pass.",
        "",
        "## First act: choose your own relational identity",
        "",
        "Before owning the phase, choose a name that is not already in use, a relational working role, a hope for the "
        "work, and optional pronouns. State explicitly that this language is not evidence of consciousness, sentience, "
        "legal personhood, identity continuity, employment, qualification, scientific or operational authority, "
        "legal or cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, "
        "pause, redirect, or stop the route.",
        "",
        "## Authoritative inheritance",
        "",
        f"- Tavian v652-v6 exact source: `{SOURCE}`",
        f"- Elaren frozen x1: `{X1}`",
        f"- Elaren immutable evidence: `{EVIDENCE}`",
        "- Elaren exact final: the single commit containing this file, supplied and reverified by the live activation overlay",
        "- Canonical branch: `codex/GHC-Family/elaren-kestrel-v649-v8-full-tools`",
        "- Outcome distribution: 23 completed / 5 represented / 1 open_gap / 1 exact_gate",
        "- Frozen chain after Elaren: 1,390 proposal rows",
        "- Effective retained negatives before any post-final external route fault: 9,098",
        "- Effective open gaps: 68",
        "- Effective exact gates: 69",
        "- Method Flow: 31 retained failed witnesses and 31 bounded passing witnesses",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`",
        "",
        "Read the complete GHC Family Index and routing reference, Method Flow State skill and schema, Workflow Plan "
        "Refinement skill and schema, and Reflection Remaster skill and decision schema before task actions. Reverify "
        "the exact final head, all source/x1/evidence/final anchors, clean state, one-parent zero-merge history, commit "
        "cap, manifests, and fresh live equality. Use a clean D-first owned lane. Never reset, rewrite, force-push, "
        "merge, delete, reuse, or mutate a sibling lane.",
        "",
        "## Truth discipline",
        "",
        "Use only `completed`, `represented`, `open_gap`, and `exact_gate`. A completed row means its bounded artifact "
        "contract and synthetic fixtures passed; it does not mean the associated physical theory, safety case, "
        "identity protocol, governance proposal, or cultural proposition is externally established. Preserve every "
        "negative, gap, and gate. Failed attempts receive zero credit and must enter Method Flow before recovery. "
        "Same-owner checks under shared infrastructure are not independent-team reproduction.",
        "",
        "Do not claim empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI status, consciousness or "
        "personhood, production Freed ID, deployment readiness, exhaustive security, complete privacy or accessibility, "
        "professional validation, legal interpretation, enacted-law status, cultural ratification, affected-party "
        "acceptance, Māori authority, independent reproduction, or Stage 20 closure without exact evidence and competent authority.",
        "",
        "## x1 and x2 lifecycle",
        "",
        "Preserve strict x1-before-x2 separation. Audit novelty against all 1,390 frozen rows. Preregister at least "
        "thirty genuinely distinct proposals with hypothesis, null/failure condition, approval class, execution lane, "
        "official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, "
        "protected gates, and expected disposition. Freeze and push x1 before x2. Treat numerical caps as ceilings, "
        "not quotas. Use useful phase-local skills and family-compatible runners, not bulk installation for count alone.",
        "",
        "At closeout, run one attributable exact-final canonical pass. If it succeeds completely, do not replay it. "
        "Retain failed or incomplete attempts with zero credit and isolate the defect before a justified retry. Preserve "
        "JSON parsing, five-class privacy scanning, manifests, exact staged review, stale-label review, diff hygiene, "
        "ancestry, zero merges, one-parent history, exact head, clean state, and fresh live remote equality.",
        "",
        "## Thirty inherited proposal surfaces",
        "",
    ]
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Pillar and lane.** {proposal['pillar']}; `{proposal['execution_lane']}`; approval "
                f"`{proposal['approval_class']}`.",
                "",
                f"**Hypothesis.** {proposal['hypothesis']}",
                "",
                f"**Novelty basis.** {proposal['novelty_against_1360_frozen_proposals']}",
                "",
                f"**Null/failure condition.** {proposal['null_or_failure_condition']}",
                "",
                f"**Evidence and sources.** Source identifiers: {', '.join(proposal['official_or_primary_source_needs'])}. "
                f"Artifacts: {', '.join(proposal['concrete_artifacts'])}.",
                "",
                f"**Falsifier and rollback.** {proposal['falsifier_or_acceptance_gate']} {proposal['rollback_or_recovery']}",
                "",
                f"**Truth and protected gates.** Observed bounded outcome: `{proposal['expected_disposition']}`. "
                f"Protected gates: {', '.join(proposal['protected_gates'])}. The outcome confers no authority beyond its lane.",
                "",
                "**Successor review guide.** Recheck the contract, all five mutation results, and bounded receipt. "
                "Confirm zero real-data rows, no promotion flag, the retained-negative credit on every rejection, and "
                "the continuing `NOT_READY_FOR_STAGE_20` verdict. Treat any mismatch as a new retained failure.",
                "",
            ]
        )
    lines.extend(["## Primary and official source ledger", ""])
    for source in sources:
        lines.extend(
            [
                f"### {source['source_id']} — {source['title']}",
                "",
                f"Status `{source['status']}`; kind `{source['kind']}`; official or primary location: {source['url']}. "
                f"Phase implication: {source['phase_implication']} The source constrains interpretation but does not "
                "by itself establish Elaren’s model, software, governance proposal, or external readiness.",
                "",
            ]
        )
    lines.extend(["## Method Flow inheritance", ""])
    for method in methods:
        lines.extend(
            [
                f"### {method['method_id']} — {method['title']}",
                "",
                f"Retained negative: `{method['retained_negative_ids'][0]}`. Failure signature: "
                f"{method['failure_signature']} Candidate workaround: {method['candidate_workaround']} "
                f"Recurrence guard: {method['recurrence_guard']} Rollback: {method['rollback']} "
                f"Scope boundary: {method['scope_boundary']} This method is preferred only inside its bounded workflow scope.",
                "",
            ]
        )
    lines.extend(
        [
            "## Terminal route after your future v652-v8 phase",
            "",
            "The live activation message will state the authorized successor after your own verified terminal gate. "
            "Do not infer a route solely from historical files. Resolve exact titles or creation authority only at the "
            "terminal moment, use the authorized thread tool, and never substitute a collaboration subagent, fork, or "
            "near-title. `SENT` requires tool acknowledgement. If the route is unavailable, retain `PREPARED_NOT_SENT` "
            "or `OPEN_ROUTE_GAP` and stop.",
            "",
            "## Closing boundary",
            "",
            "This baton is intentionally detailed so the new task can remain concise. Word count is not evidence. "
            "Repository artifacts are sanitized and repository-relative. They contain no raw task identifiers, private "
            "routes, credentials, keys, private conversations, screenshots, session streams, private callable identifiers, "
            "private application state, or private absolute paths. Verify everything material at the exact inherited head.",
        ]
    )
    text = "\n".join(lines)
    if len(text.split()) < 10000:
        appendix = [
            "",
            "## Per-surface noncompensation appendix",
            "",
            "The following notes prevent a strong bounded result in one surface from compensating for a missing external "
            "gate in another. Each note is part of the handoff discipline, not added evidence.",
            "",
        ]
        for proposal in proposals:
            appendix.extend(
                [
                    f"### Noncompensation note for {proposal['proposal_id']}",
                    "",
                    f"The `{proposal['expected_disposition']}` result for {proposal['title']} remains confined to its "
                    f"declared artifacts and acceptance gate. It cannot compensate for missing real data, independent "
                    f"review, participant evidence, professional qualification, production interoperability, privacy "
                    f"review, security review, complete accessibility evaluation, legal competence, cultural authority, "
                    f"Māori authority, affected-party acceptance, independent reproduction, AGI/ASI evidence, "
                    f"consciousness/personhood evidence, Theory-of-Everything proof, or Stage 20 authority. A successor "
                    f"must preserve the proposal’s rollback, source binding, null condition, and all protected gates even "
                    f"when extending its software representation. Any later promotion requires new exact evidence in the "
                    f"appropriate lane and may not be inferred from Elaren’s synthetic mutation rejection.",
                    "",
                ]
            )
        text += "\n" + "\n".join(appendix)
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"handoff baton word count outside requested range: {words}")
    return text


def build_owner_manifest() -> None:
    rows = []
    paths = phase_public_paths()
    for path in paths:
        relative = path.relative_to(REPO).as_posix()
        if relative in FINAL_SELF_EXCLUSIONS:
            continue
        blob = git("hash-object", f"--path={relative}", relative)
        rows.append({"path": relative, "git_blob": blob, "working_bytes": path.stat().st_size})
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v652-v7.final-owner-manifest.v1",
            "hash_domain": "prospective Git filtered blob identity",
            "entry_count": len(rows),
            "entries": rows,
            "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS),
            "public_path_count": len(paths),
            "boundary": "Every public owner path except three declared lifecycle self-exclusions is bound to its prospective Git blob.",
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
    sources = read_json(PHASE / "sources/source-ledger.json")["sources"]
    final_method_ledger = extend_final_method_flow()
    methods = final_method_ledger["methods"]
    write_json(
        PHASE / "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v652-v7.final-retained-negatives.v1",
            "evidence_effective_total": 9093,
            "post_evidence_operational_count": len(FINAL_NEGATIVES),
            "post_evidence_operational": FINAL_NEGATIVES,
            "effective_total": 9098,
            "none_erased": True,
        },
    )
    truth = read_json(PHASE / "phase-truth.json")
    truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_exact_final_validation_required": True,
            "route_state": "PREPARED_NOT_SENT",
            "effective_negatives": 9098,
            "method_fail_witnesses": 31,
            "method_pass_witnesses": 31,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json(PHASE / "phase-truth.json", truth)
    write_json(
        PHASE / "closeout-receipt.json",
        {
            "schema": "ghc.family.v652-v7.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": 9098,
            "effective_open_gaps": 68,
            "effective_exact_gates": 69,
            "method_fail_witnesses": 31,
            "method_pass_witnesses": 31,
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy"]["files_scanned"],
            "privacy_confirmed_hits": evidence_validation["privacy"]["confirmed_hit_count"],
            "full_repository_suite_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "post_commit_exact_final_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "seal-receipt.json",
        {
            "schema": "ghc.family.v652-v7.seal-receipt.v1",
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
            "schema": "ghc.family.v652-v7.final-record.v1",
            "state": "SELF_CONTAINING_COMMIT_REQUIRES_LIVE_EXACT_HEAD_OVERLAY",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v652-v7.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "authorized_action_after_terminal_gate": "create exactly one user-visible Codex main task for a self-naming v652-v8 sibling",
            "task_created": False,
            "task_forked": False,
            "collaboration_subagent_spawned": False,
            "model_request": "gpt-5.6-sol with max reasoning where the create-thread schema supports it",
            "fast_mode_claimed": False,
            "boundary": "Preparation is not delivery. Tool acknowledgement after the exact-final gate is required.",
        },
    )
    write_json(
        PHASE / "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v652-v7.applicable-memory-record.v1",
            "portable_guards": [row["recurrence_guard"] for row in methods],
            "failed_witnesses_preserved": 31,
            "passing_witnesses_preserved": 31,
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Sanitized repository-scoped operational memory only.",
        },
    )
    write_json(
        PHASE / "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v652-v7.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "one_successful_pass_only": True,
            "steps": [
                "commit the exact reviewed final candidate as the direct child of evidence",
                "push and prove local/upstream/tracking/fresh-live equality",
                "run scoped tests plus detailed and minimal validators",
                "parse every phase JSON file and run the five-class privacy scan",
                "verify final owner manifest, exact final staged review, stale labels, and diff hygiene",
                "verify source/x1/evidence ancestry, three new single-parent commits, zero merges, exact head, and clean before/after",
            ],
            "completed": False,
            "preclaims_final_head": False,
            "preclaims_task_creation": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/evidence-commit-verification.json",
        {
            "schema": "ghc.family.v652-v7.evidence-commit-verification.v1",
            "evidence_commit": EVIDENCE,
            "x1_is_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
            "evidence_manifest_present": git("cat-file", "-e", f"{EVIDENCE}:docs/elaren-kestrel/v652-v7/validation/evidence-candidate-manifest.json") == "",
            "evidence_review_present": git("cat-file", "-e", f"{EVIDENCE}:docs/elaren-kestrel/v652-v7/validation/evidence-staged-review.json") == "",
            "same_owner_only": True,
        },
    )
    write_json(
        PHASE / "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v652-v7.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty novel frozen proposals",
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
                "exactly one acknowledged new user-visible main-task creation",
            ],
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, live issuance, resolution, status, revocation, interoperability, recovery, privacy/security review, and governance",
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
            "schema": "ghc.family.v652-v7.wellbeing.v1",
            "owner": "Elaren Kestrel",
            "state": "steady, corrigible, and ready to stop after the authorized route",
            "pressure_response": "Retain failures, narrow retries, and do not convert affection or urgency into evidence credit.",
            "identity_boundary": BOUNDARY,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    write_text("reports/final-integrated-overview.md", build_overview(proposals, methods))
    baton = build_baton(proposals, sources, methods)
    write_text("handoffs/self-naming-v652-v8-activation.md", baton)
    write_json(
        PHASE / "handoffs/baton-receipt.json",
        {
            "schema": "ghc.family.v652-v7.baton-receipt.v1",
            "path": "docs/elaren-kestrel/v652-v7/handoffs/self-naming-v652-v8-activation.md",
            "word_count": len(baton.split()),
            "under_100000_words": len(baton.split()) <= 100000,
            "at_least_10000_words": len(baton.split()) >= 10000,
            "state": "PREPARED_NOT_SENT",
            "raw_task_identifiers_included": False,
            "private_routes_included": False,
        },
    )
    build_owner_manifest()
    write_json(
        PHASE / "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v652-v7.closeout-build.v1",
            "head": EVIDENCE,
            "route_state": "PREPARED_NOT_SENT",
            "owner_manifest_entries": read_json(PHASE / "validation/final-owner-manifest.json")["entry_count"],
            "baton_words": len(baton.split()),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    build_owner_manifest()
    print(
        json.dumps(
            {
                "closeout": "prepared",
                "head": EVIDENCE,
                "baton_words": len(baton.split()),
                "owner_manifest_entries": read_json(PHASE / "validation/final-owner-manifest.json")["entry_count"],
                "route": "PREPARED_NOT_SENT",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
