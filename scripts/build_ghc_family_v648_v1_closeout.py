#!/usr/bin/env python3
"""Build the combined Tamar Vey v648-v1 closeout and seal candidate."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v648-v1"
SOURCE = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"
X1 = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"
EVIDENCE = "b09681afe5a4cac101bab367ef761e4ac1a7b57e"
EVIDENCE_NEGATIVES = 3926
LIFECYCLE_NEGATIVES = [
    {
        "negative_id": "V6481-LC-N01",
        "failure": "A combined status-and-source scan exceeded its bounded timeout before returning output.",
        "recovery": "Retain the timeout and split the read into exact bounded probes under a non-login shell.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N02",
        "failure": "A standalone ordinary Git status probe exceeded its sixty-second bound without output.",
        "recovery": "Award no clean-state credit and use exact index, tracked-diff, and untracked-path primitives.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N03",
        "failure": "A login-shell sequence of exact Git primitives exceeded its bounded timeout.",
        "recovery": "Change only the shell invocation mode and rerun the exact split primitives.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N04",
        "failure": "A read-only process query exceeded its bounded timeout without usable output.",
        "recovery": "Discard the result and prove minimal shell responsiveness without changing process or host state.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N05",
        "failure": "The Method Flow summary wrote derived files but its final console print failed under the default Windows code page on Māori text.",
        "recovery": "Retain the failed print, rerun the same summary under explicit Python UTF-8 mode, and revalidate the ledger.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N06",
        "failure": "A general environment-directory enumeration exceeded its bounded timeout without output.",
        "recovery": "Use a path-scoped repository file-index query and retain the failed enumeration.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N07",
        "failure": "The first closeout detailed validator ran all 75 scoped tests but failed an evidence-test assumption that every method has exactly one failed witness.",
        "recovery": "Retain the failed receipt and replace only the invalid exact-cardinality assertion with balanced parity and at-least-one-per-method guards.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N08",
        "failure": "The inherited per-path staged reviewer exceeded its 180-second bound before a completed review was acknowledged.",
        "recovery": "Retain the timeout and batch exact stage-zero Git-blob reads through communicate without changing the hash or privacy domain.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N09",
        "failure": "The optimized staged reviewer rejected one private absolute traceback path in the retained failed validator receipt.",
        "recovery": "Preserve the failed test and assertion while replacing only the private location prefix, then rerun the identical five-class scan.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N10",
        "failure": "The first stale-label wrapper had a pre-execution nested-quoting syntax error and scanned no files.",
        "recovery": "Retain the parser fault and compare exact path and literal arrays with PowerShell simple-match semantics.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6481-LC-N11",
        "failure": "A closeout test found two new Method Flow witness paths absent from the prior owner-manifest path set.",
        "recovery": "Retain the failed test, stage the complete now-known surface, rebuild the exact owner manifest, and rerun the unchanged test.",
        "result": "retained_then_recovered",
    },
]
FINAL_EFFECTIVE_NEGATIVES = EVIDENCE_NEGATIVES + len(LIFECYCLE_NEGATIVES)
OPEN_GAPS = 26
EXACT_GATES = 27
METHODS = 11
FAILED_WITNESSES = 15
PASSING_WITNESSES = 15
BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, lifting safety, emergency response, worker "
    "and site privacy, remedy, legal, cultural, affected-party, and Māori concepts remain under "
    "competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. No empirical "
    "confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, "
    "professional, lifting-safety, proof or canon, or Stage 20 claim is made."
)


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, data: dict) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build() -> None:
    truth = load("phase-truth.json")
    validation = load("validation/evidence-detailed.json")
    methods = load("method-flow/method-flow-state.json")
    if not validation["valid"] or truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("validated evidence and terminal abstention are required")
    if validation["test_result"]["tests"] != 68:
        raise RuntimeError("the frozen evidence selection must retain 68 passing tests")
    if methods["counts"]["methods"] != METHODS:
        raise RuntimeError("Method Flow method count is incomplete")
    if methods["counts"]["witness_results"] != {"fail": FAILED_WITNESSES, "pass": PASSING_WITNESSES}:
        raise RuntimeError("Method Flow failed and passing witnesses are incomplete")

    evidence_receipt = load("evidence-receipt.json")
    evidence_receipt.update(
        {
            "schema": "ghc.family.v648-v1.evidence-receipt.committed.v1",
            "evidence_commit": EVIDENCE,
            "effective_negatives": EVIDENCE_NEGATIVES,
            "boundary": BOUNDARY,
        }
    )
    write_json("evidence-receipt.json", evidence_receipt)

    write_json(
        "validation/lifecycle-operational-negatives.json",
        {
            "schema": "ghc.family.v648-v1.lifecycle-operational-negatives.v1",
            "evidence_boundary_total": EVIDENCE_NEGATIVES,
            "count": len(LIFECYCLE_NEGATIVES),
            "negatives": LIFECYCLE_NEGATIVES,
            "all_retained": True,
            "erased_negative_count": 0,
        },
    )
    write_json(
        "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v648-v1.final-retained-negatives.v1",
            "inherited_and_evidence_negatives": EVIDENCE_NEGATIVES,
            "lifecycle_operational_negatives": len(LIFECYCLE_NEGATIVES),
            "effective_total": FINAL_EFFECTIVE_NEGATIVES,
            "erased_negative_count": 0,
            "boundary": "Every workflow failure remains visible; bounded recovery is not scientific, production, authority, security, or independent-reproduction evidence.",
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v648-v1.phase-anchor-contract.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "expected_phase_commit_count_at_final": 3,
            "maximum_phase_commits": 4,
            "expected_merge_count": 0,
            "expected_final_parent_count": 1,
            "history_rewrite_allowed": False,
            "force_push_allowed": False,
        },
    )
    closeout = {
        "schema": "ghc.family.v648-v1.closeout.v1",
        "owner": "Tamar Vey",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "safe_now_completed": 30,
        "candidates_completed": 20,
        "skills_validated_and_used": 20,
        "runners_invoked": 10,
        "cleanup_completed": 30,
        "synthetic_negatives_rejected": 70,
        "effective_negatives": FINAL_EFFECTIVE_NEGATIVES,
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "method_count": METHODS,
        "method_fail_witnesses": FAILED_WITNESSES,
        "method_pass_witnesses": PASSING_WITNESSES,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
    }
    write_json("closeout-receipt.json", closeout)
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v648-v1.seal.v1",
            "state": "CLOSEOUT_AND_SEAL_CANDIDATE",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "final_commit_known_at_commit_time": False,
            "postcommit_exact_head_validation_required": True,
            "named_replay_required": True,
            "remote_equality_required": True,
            "baton_send_allowed_now": False,
            "boundary": "A commit cannot contain its own not-yet-created identifier; exact-head proof is postcommit and read-only.",
        },
    )
    final_candidate = {
        "schema": "ghc.family.v648-v1.final-receipt.candidate.v1",
        "state": "POST_COMMIT_VALIDATION_REQUIRED",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_commit": None,
        "exact_final_validated": False,
        "canonical_clean": False,
        "four_way_remote_equal": False,
        "named_replay_passed": False,
        "independent_reproduction": False,
        "baton_sent": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("final-receipt.json", final_candidate)
    write_json("final-validation-record.json", final_candidate | {"schema": "ghc.family.v648-v1.final-validation-record.candidate.v1"})
    write_json("lifecycle/final-record.json", final_candidate | {"schema": "ghc.family.v648-v1.lifecycle-final-record.v1"})
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v648-v1.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "completed": False,
            "preclaims_exact_final_head": False,
            "canonical_requirements": [
                "current and authorized scoped tests",
                "detailed and minimal validators",
                "complete phase JSON parse",
                "five-class privacy scan",
                "owner-manifest parity",
                "source, x1, and evidence ancestry",
                "three phase commits and zero merges",
                "one final parent",
                "exact head and clean before and after",
                "local, upstream, tracking, and fresh live remote equality",
            ],
            "named_replay_requirements": [
                "one local-only named branch and worktree at exact final head",
                "not detached, pushed, canonical, assigned upstream, or present as a live remote ref",
                "same bounded validation exactly once",
                "clean before and after",
            ],
            "full_repository_suite": "not run; Eiren-only under the current refinement",
        },
    )
    write_json(
        "reproduction/same-owner-replay-plan.json",
        {
            "schema": "ghc.family.v648-v1.same-owner-replay-plan.v1",
            "state": "PENDING_POST_COMMIT",
            "named_lane_count": 1,
            "detached": False,
            "push_allowed": False,
            "upstream_allowed": False,
            "live_remote_ref_allowed": False,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v648-v1.successor-baton-preparation.v1",
            "target_existing_task_title": "Sylven Arc",
            "target_phase": "v648-gmut-thos-v2-x1-x2",
            "state": "PREPARED_NOT_SENT",
            "task_creation_authorized": False,
            "fork_authorized": False,
            "extra_confirmation_authorized": False,
            "send_only_after": [
                "exact final validation",
                "one named replay",
                "canonical clean state",
                "four-way remote equality",
            ],
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v648-v1.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "standby_sibling_messaged": False,
            "raw_task_identifier_present": False,
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v648-v1.final-checklist.v1",
            "complete": [
                "verified source inheritance",
                "dedicated x1 freeze and remote equality before x2",
                "ten executed proposal surfaces with 6/2/1/1 outcomes",
                "seventy executed and rejected synthetic mutations",
                "thirty safe-now tasks and twenty bounded candidates",
                "twenty phase-local skills validated and smoke-used",
                "ten family-compatible runners invoked",
                "thirty additive cleanup tasks",
                "threat model, wellbeing receipt, and structurally accessible static report",
                "evidence validation and retained Method Flow failures",
            ],
            "pending_postcommit": [
                "exact final identifier",
                "canonical exact-final validation",
                "one local-only named replay",
                "final four-way remote equality",
                "single verified Sylven Arc baton",
            ],
            "incomplete_external": [
                "real DES Y3 analysis or GMUT likelihood",
                "blind matched-budget THOS real arms and independent review",
                "production Freed ID lifecycle and interoperability",
                "affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority",
                "manual, assistive-technology, Māori-language, and affected-user accessibility review",
                "independent security review and independent-team reproduction",
                "Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
        documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
    overview = next(row for row in documents if row["path"] == "deliverables/v648-v1-final-integrated-overview.md")
    write_json(
        "validation/document-cap-receipt.json",
        {
            "schema": "ghc.family.v648-v1.document-cap.v1",
            "document_count": len(documents),
            "maximum_words": max(row["words"] for row in documents),
            "all_under_6000": all(row["words"] <= 6000 for row in documents),
            "overview_words": overview["words"],
            "documents": documents,
        },
    )
    write_json(
        "validation/final-validation-candidate.json",
        {
            "schema": "ghc.family.v648-v1.final-validation-candidate.v1",
            "evidence_validation_valid": validation["valid"],
            "evidence_tests": validation["test_result"]["tests"],
            "detailed_checks": validation["checks_total"],
            "json_parses": validation["json_files_parsed"],
            "privacy_files": validation["public_files_scanned"],
            "privacy_hits": len(validation["privacy_hits"]),
            "closeout_validation_pending": True,
            "exact_final_validation_pending": True,
            "named_replay_pending": True,
        },
    )

    truth.update(
        {
            "schema": "ghc.family.v648-v1.phase-truth.closeout-candidate.v1",
            "boundary": BOUNDARY,
            "lifecycle": "closeout_and_seal_candidate",
            "canonical_validation_state": "postcommit_required",
            "named_replay_state": "not_started",
            "route_state": "PREPARED_NOT_SENT",
            "postcommit_validation_pending": True,
            "evidence_commit": EVIDENCE,
            "effective_retained_negatives": FINAL_EFFECTIVE_NEGATIVES,
            "evidence_boundary_negatives": EVIDENCE_NEGATIVES,
            "lifecycle_operational_negatives": len(LIFECYCLE_NEGATIVES),
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
        }
    )
    write_json("phase-truth.json", truth)


if __name__ == "__main__":
    build()
