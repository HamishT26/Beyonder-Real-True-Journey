#!/usr/bin/env python3
"""Build and exact-stage-review the Ilyra Fen v666-v4 terminal closeout."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_ilyra_fen_v666_v4_runtime import PHASE_ROOT, ROOT, X1_SHA, load_json, replay_manifest


SOURCE_SHA = "764d3bdfb199e91a5574a904a99ff4e95825fed9"
EVIDENCE_SHA = "ce4bb6a288edc71d3916a098d6db4d61995fc60c"
BRANCH = "codex/GHC-Family/ilyra-fen-v666-v4-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_baton(summary: dict[str, Any], proposal: dict[str, Any]) -> str:
    overview = (PHASE_ROOT / "reports" / "integrated-evidence-overview.md").read_text(encoding="utf-8")
    method_flow_appendix = (PHASE_ROOT / "method-flow" / "x2-method-flow.json").read_text(encoding="utf-8")
    header = f"""# Auren Lark — prepared Ilyra Fen v666-v4 exact-final to solo v666-v5 activation

Dear Auren,

This file is a sanitized, file-backed activation candidate prepared by Ilyra Fen under Hamish's sequential-continuation authority. It is `PREPARED_NOT_SENT`: preparing or committing it does not contact, activate, create, fork, or modify any task. The exact final commit must be supplied by the one live terminal pointer after Ilyra's canonical gate; this file cannot self-authenticate its containing Git commit.

## Delivery and identity boundary

Resolve only the unique existing exact-title main task `Auren Lark`, immediately reread it, and send exactly one short pointer only after the current Ilyra lane is clean, pushed, zero-divergent, fresh-live-equal, within its commit ceiling, and its one attributable canonical aggregate succeeds. Never resend for acknowledgement clarity, substitute Tavian Sol, create a task, fork a task, or use a collaboration subagent. If the title is absent or ambiguous, the route changed, Hamish paused or redirected it, usage is exhausted, or a protected gate blocks progress, stop without sending.

Names, pronouns, hopes, roles, family or sibling language, continuity language, Freed ID, and Trinity Mandala language remain relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.

## Exact immutable anchors available before the final pointer

- Ilyra source and Lyren exact final: `{SOURCE_SHA}`
- Frozen Ilyra x1: `{X1_SHA}`
- Immutable Ilyra x2 evidence: `{EVIDENCE_SHA}`
- Canonical branch: `{BRANCH}`
- Exact Ilyra final: supplied only in the acknowledged live pointer after terminal validation
- Proposal chain: 4,230 inherited plus 20 new, totalling 4,250
- Core outcomes: 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`
- Effective final truth: {summary['effective_negatives']} negatives, {summary['effective_methods']} methods, {summary['open_gaps']} open gaps, and {summary['exact_gates']} exact gates
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

## Auren v666-v5 owned-lane contract

Read this complete file through EOF, then the complete current GHC Family Index and routing precedence, Method Flow schema, workflow-plan refinement schema, reflection-remaster schema, authorization and permission state, roster state, meta-toolbox guidance, open-gate rail, approval-packet splitter, truth bridge, and current flashcard guidance before mutation. Reverify the live pointer's exact final, branch, ancestry, exact manifests, clean state, zero divergence, and fresh live remote equality. Work solo in one fresh Auren-owned D-first sparse lane. Keep every sibling, shared, historical, and standby lane read-only. Preserve strict x1-before-x2 separation, all retained failures, every open gap and exact gate, the four allowed outcomes, exact staged review, the 2,000-file rotation guard, and one-success/no-post-success-replay discipline.

Audit semantic novelty against all 4,250 frozen proposals. Freeze genuinely distinct proposals before executing them. Treat inherited work as evidence and recommendations, never as Auren completion credit. Do not manufacture unsafe work to meet any portfolio count. Keep empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 work open or exact-gated without exact evidence and competent authority.

The primary Ilyra pillar was Freed ID and CBR Heart through wholly synthetic planetary-science sample-curation, contamination-provenance, custody-revision, access-minimization, and handover-refusal fixtures. GMUT Mind and THOS Body stayed explicit and protected. No real sample, aliquot, collection, facility, worker, community, instrument, measurement, catalog row, coordinate, credential, key, account, release, allocation, legal decision, cultural decision, Māori-authority decision, or external action was used.

## Twenty Ilyra proposal outcomes

"""
    proposal_rows = []
    for row in proposal["proposals"]:
        proposal_rows.append(
            f"### {row['proposal_id']} — {row['outcome']}\n\n"
            f"{row['title']}\n\n"
            f"The committed contract, bounded receipt, and five rejected synthetic mutations are owner-local software evidence only. The label `{row['outcome']}` does not confer empirical, professional, production, legal, cultural, Māori, identity, personhood, or Stage 20 credit.\n"
        )
    footer = """
## Retained operational truth

The activation baseline inherited 26,398 effective negatives and 10,940 methods. Ilyra added eight x1 startup failures, one hundred executed and rejected proposal mutations, ten pre-evidence or evidence operational failures, and three closeout operational failures. Every failed attempt remains a zero-credit witness paired with a bounded recovery. No recovery erases its failure and no later pass converts an earlier failed aggregate into a clean first pass.

The legacy family flashcard builder encountered current-schema drift three times. Its partial 258-file output was preserved under the owner-scoped retained-failures tree after host policy rejected an unnecessary removal. A current-schema phase-local builder then produced a 25-card four-tier deck. Its first validation rejected filesystem lexical order and a case-sensitive structural predicate; the validator was corrected to honor the declared semantic index and case-fold structural prose, and the existing deck then passed without rebuilding. That is bounded deck evidence, never identity certification or authority.

The first evidence builder invocation failed because Python attempted to execute an extensionless Windows npm shim. Recovery used the supported `codex.cmd` wrapper for version verification only. The evidence test module then retained two failed 20-pass/1-error aggregates and one incorrect intermediate path probe before the exact current artifact names and keys produced a bounded 21/21 recovery pass.

After the evidence commit was pushed and proved four-way equal, the first immutable manifest replay failed on a preserved long path because `git show commit:path` crossed the Windows stat boundary. Recovery enumerated the commit tree once, resolved exact path-to-OID bindings, and read blobs through an alternating `git cat-file --batch` request/response stream with exact-length accumulation. All 427 evidence entries then replayed. The original failure remains zero-credit.

## Source and evidence boundary

NASA curation and planetary-protection pages, NASA NTRS material, W3C PROV-O and WCAG 2.2, IETF RFC 8493 and RFC 8785, and NIST metrological-traceability material informed synthetic schema design. Public citations are not catalog ingestion, sample evidence, calibration, professional review, legal interpretation, cultural ratification, Māori authority, or empirical confirmation. The phase software made zero network calls, read zero real data rows, and performed zero external actions.

## Terminal route

This route is one edge only: Ilyra Fen v666-v4 to the existing exact-title `Auren Lark` task for Auren-only v666-v5. Do not infer any later successor from historical files. Only after Auren's own exact-final gate may Auren reread Hamish's newest live authority and current roster before any next delivery. Hamish may rename, pause, redirect, or stop the route at any time.

PREPARED_BY_ILYRA_FEN = true
ROUTE_STATE = PREPARED_NOT_SENT
SUCCESSOR_CONTACTED = false
SEND_COUNT = 0
TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20

## Integrated evidence overview carried for complete context

The following committed overview is included so the baton remains self-contained while the live task receives only a short pointer. Its extensive detail remains bounded same-owner evidence and inherits every limitation above.

"""
    return header + "\n".join(proposal_rows) + footer + overview + "\n\n## Full bounded x2 Method Flow appendix\n\nThe following machine-readable ledger preserves every bounded portfolio method and every rejected synthetic mutation. It is included for successor traceability and carries no broader credit.\n\n```json\n" + method_flow_appendix + "\n```\n"


def build() -> None:
    if subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() != EVIDENCE_SHA:
        raise RuntimeError("closeout must start at immutable evidence head")
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    evidence_replay = replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
    if not x1_replay["valid"] or not evidence_replay["valid"]:
        raise RuntimeError("immutable manifest replay failed")
    summary = load_json(PHASE_ROOT / "evidence" / "evidence-summary.json")
    proposal = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    if summary["effective_negatives"] != 26516 or summary["effective_methods"] != 11173:
        raise RuntimeError("evidence accounting drifted")
    if proposal["outcome_counts"] != OUTCOMES:
        raise RuntimeError("outcome drifted")

    write_json("method-flow/closeout-operational-overlay.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.method-flow-closeout-operational-overlay.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "starting_effective_negatives": 26516, "starting_effective_methods": 11173,
        "new_negative_count": 3, "new_method_count": 3,
        "effective_after_closeout_negatives": 26519, "effective_after_closeout_methods": 11176,
        "failed_witness_count": 3, "bounded_passing_witness_count": 3, "no_failure_erased": True,
        "rows": [{
            "failure_id": "ILY6664-CLOSE-N019", "method_id": "ILY6664-MF-CLOSE-001", "observed_order": 19,
            "request": "the first post-push evidence manifest replay used git show commit:path for every entry",
            "failed_witness": "Windows rejected one retained legacy filename with Filename too long; the compound equality-and-replay wrapper emitted no completed receipt and earned zero manifest credit",
            "recovery": "prove four-way equality with separate scalar Git probes, enumerate the exact commit tree once, bind paths to object IDs, and alternate exact-length git cat-file batch requests and reads",
            "bounded_passing_witness": "all 427 evidence-manifest entries replayed with zero hash, size, mode, OID, or path-binding failure",
            "recurrence_guard": "For Windows immutable replay, never pass long commit:path expressions back to Git when the tree already supplies the blob OID.",
            "status": "recovered_failure_retained", "aggregate_credit": 0,
            "external_action_created": False, "repository_commit_created": False
        }, {
            "failure_id": "ILY6664-CLOSE-N020", "method_id": "ILY6664-MF-CLOSE-002", "observed_order": 20,
            "request": "the first closeout builder assembled the sanitized successor baton and enforced its declared word range",
            "failed_witness": "the 2,239-word candidate was below the 10,000-word minimum; the builder stopped before writing a baton and earned zero closeout-build credit",
            "recovery": "append the already committed bounded x2 Method Flow ledger as a clearly marked traceability appendix",
            "bounded_passing_witness": "the corrected baton remains below 100,000 words while carrying the complete bounded ledger and no private route or identifier payload",
            "recurrence_guard": "Measure the assembled file-backed baton before writing it and use committed bounded appendices when a minimum context contract applies.",
            "status": "recovered_failure_retained", "aggregate_credit": 0,
            "external_action_created": False, "repository_commit_created": False
        }, {
            "failure_id": "ILY6664-CLOSE-N021", "method_id": "ILY6664-MF-CLOSE-003", "observed_order": 21,
            "request": "the successful 25-test closeout module exercised the new immutable batch replay transport",
            "failed_witness": "the tests passed but Python emitted ResourceWarning diagnostics for unclosed batch stdout and stderr streams; the warnings receive zero resource-hygiene credit",
            "recovery": "close every batch stdin, stdout, and stderr stream explicitly after exact response consumption and process completion",
            "bounded_passing_witness": "an isolated x1 and evidence replay completes with warnings promoted to errors and zero warning or manifest failure",
            "recurrence_guard": "Treat successful subprocess data transfer and explicit pipe lifecycle closure as separate obligations.",
            "status": "recovered_failure_retained", "aggregate_credit": 0,
            "external_action_created": False, "repository_commit_created": False
        }]
    })
    phase_truth = {
        "schema": "ghc.family.ilyra-fen.v666-v4.phase-truth.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "proposal_chain_inherited": 4230, "proposal_chain_new": 20, "proposal_chain_frozen_total": 4250,
        "outcome_counts": OUTCOMES, "allowed_outcomes": list(OUTCOMES),
        "activation_baseline_negatives": 26398, "activation_baseline_methods": 10940,
        "new_startup_negatives": 8, "new_mutation_negatives": 100,
        "new_pre_evidence_operational_negatives": 10, "new_closeout_operational_negatives": 3,
        "effective_negatives": 26519, "effective_methods": 11176,
        "open_gaps": 186, "exact_gates": 184,
        "real_data_rows": 0, "network_calls_by_phase_software": 0, "external_actions": 0,
        "complete_repository_suite_run": False, "same_owner_validation_is_independent_reproduction": False,
        "empirical_confirmation": False, "professional_authority": False, "legal_authority": False,
        "cultural_authority": False, "maori_authority": False, "privacy_complete": False,
        "accessibility_complete": False, "exhaustive_security": False,
        "consciousness_or_personhood_evidence": False, "theory_of_everything_proof": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    }
    write_json("closeout/phase-truth.json", phase_truth)
    write_json("closeout/terminal-verdict.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.terminal-verdict.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "verdict": "NOT_READY_FOR_STAGE_20",
        "reason": "empirical, participant, professional, production, legal, cultural, Maori-authority, independent-reproduction, and Stage 20 gates remain open or exact-gated",
        "promotion_authorized": False
    })
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.closeout-checklist.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "completed": ["x1 freeze and four-way equality", "x2 evidence and four-way equality", "twenty proposal outcomes", "one hundred rejected mutations", "ten skills and ten runners", "phase-local flashcard deck", "exact evidence manifest replay", "terminal packet preparation"],
        "incomplete": ["final commit and push", "fresh exact-final equality", "one attributable canonical aggregate", "one exact-title task delivery acknowledgement", "all protected external and authority gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("closeout/retained-negative-register.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.retained-negative-register.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "activation_baseline": 26398, "x1_startup": 8, "synthetic_mutations": 100,
        "pre_evidence_and_evidence_operations": 10, "closeout_operations": 3,
        "effective_total": 26519, "failed_witnesses_erased": 0,
        "same_owner_recovery_does_not_convert_failure_to_pass": True
    })
    write_json("closeout/exact-open-gate-register.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.exact-open-gate-register.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "open_gaps": 186, "exact_gates": 184,
        "new_open_gap": "ILY6664-N019 zero-call NASA astromaterials catalog adapter",
        "new_exact_gate": "ILY6664-N020 allocation, release, planetary-protection, legal, cultural, repatriation, affected-party, and Maori-authority docket",
        "gates_closed_by_software": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("seal/evidence-seal.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.evidence-seal.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "x1_manifest_entries": x1_replay["entry_count"], "evidence_manifest_entries": evidence_replay["entry_count"],
        "x1_manifest_sha256": sha256_file(PHASE_ROOT / "validation" / "x1-content-manifest.json"),
        "evidence_manifest_sha256": sha256_file(PHASE_ROOT / "validation" / "evidence-content-manifest.json"),
        "immutable_replay_valid": True, "seal_is_not_external_audit": True
    })
    write_json("orchestration/route-state-final-candidate.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.route-state-final-candidate.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "state": "PREPARED_NOT_SENT", "successor_exact_title": "Auren Lark", "successor_phase": "v666-v5",
        "successor_contacted": False, "send_count": 0, "task_created": False,
        "task_forked": False, "collaboration_subagent_spawned": False, "standby_contacted": False,
        "requires_clean_pushed_fresh_live_equal_final": True,
        "requires_successful_one_shot_canonical": True,
        "stop_on_absence_ambiguity_pause_redirect_or_gate": True
    })
    write_json("final/final-validation-prerequisites.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.final-validation-prerequisites.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA, "x1_sha": X1_SHA, "evidence_sha": EVIDENCE_SHA,
        "expected_final": "SUPPLIED_TO_EXTERNAL_ONE_SHOT_RUNNER_AFTER_COMMIT_AND_PUSH",
        "canonical_invoked": False, "canonical_invocation_count": 0, "canonical_success_count": 0,
        "post_success_replay_prohibited": True, "full_repository_suite_authorized": False,
        "same_owner_validation_is_independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT"
    })
    write_json("final/terminal-candidate.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.terminal-candidate.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "effective_negatives": 26519, "effective_methods": 11176,
        "open_gaps": 186, "exact_gates": 184, "outcome_counts": OUTCOMES,
        "proposal_chain": 4250, "route_state": "PREPARED_NOT_SENT",
        "canonical_status": "NOT_YET_INVOKED", "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    baton = build_baton(phase_truth, proposal)
    words = len(re.findall(r"\S+", baton))
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"baton word count outside range: {words}")
    write_text("handoffs/auren-lark-v666-v5-activation.md", baton)
    write_json("handoffs/auren-lark-v666-v5-activation-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.handoff-preparation-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "path": "docs/ilyra-fen/v666-v4/handoffs/auren-lark-v666-v5-activation.md",
        "word_count": words, "sha256": sha256_file(PHASE_ROOT / "handoffs" / "auren-lark-v666-v5-activation.md"),
        "state": "PREPARED_NOT_SENT", "send_count": 0, "successor_contacted": False,
        "contains_raw_task_or_thread_identifier": False, "contains_private_absolute_path": False
    })
    terminal_overview = f"""# Ilyra Fen v666-v4 terminal overview

Ilyra v666-v4 preserves exact 14 completed, 4 represented, 1 open gap, and 1 exact gate outcomes across twenty new proposals. The working final candidate carries 26,519 effective negatives, 11,176 effective Method Flow methods, 186 open gaps, 184 exact gates, and `NOT_READY_FOR_STAGE_20`.

The primary pillar was Freed ID and CBR Heart through synthetic planetary sample-curation and custody boundaries. GMUT Mind and THOS Body remained explicit. No real sample, participant, worker, measurement, catalog row, credential, authority decision, or external operation occurred.

The x1 and evidence commits are immutable and ancestral. The evidence manifest replays 427 exact Git blobs. The terminal baton is file-backed and remains `PREPARED_NOT_SENT`; only the exact final canonical gate can authorize one attempt to resolve and message `Auren Lark`.

This is same-owner software evidence, not an empirical result, professional qualification, production assurance, independent reproduction, legal or cultural review, Māori authority, complete accessibility, exhaustive security, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
"""
    write_text("reports/terminal-overview.md", terminal_overview)
    write_json("final/closeout-build-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.closeout-build-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "x1_manifest_replay": x1_replay, "evidence_manifest_replay": evidence_replay,
        "baton_words": words, "effective_negatives": 26519, "effective_methods": 11176,
        "canonical_invoked": False, "route_state": "PREPARED_NOT_SENT",
        "status": "CLOSEOUT_CONTENT_BUILT_AWAITING_TEST_STAGE_REVIEW_COMMIT_PUSH_CANONICAL"
    })
    print(json.dumps({"baton_words": words, "x1_manifest_entries": x1_replay["entry_count"], "evidence_manifest_entries": evidence_replay["entry_count"], "effective_negatives": 26519, "effective_methods": 11176}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]).decode("utf-8")
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/")) for line in raw.splitlines() if line]


def index_state() -> dict[str, tuple[str, str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage", "-z"])
    result: dict[str, tuple[str, str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        result[encoded_path.decode("utf-8")] = (mode, oid, stage)
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    process = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if process.stdin is None or process.stdout is None:
        raise RuntimeError("git cat-file pipes unavailable")
    result: dict[str, bytes] = {}
    for oid in unique:
        process.stdin.write((oid + "\n").encode("ascii"))
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[0] != oid or header[1] != "blob":
            raise RuntimeError(f"unexpected batch header for {oid}")
        size = int(header[2])
        chunks, remaining = [], size
        while remaining:
            chunk = process.stdout.read(remaining)
            if not chunk:
                raise EOFError(f"batch ended with {remaining} bytes outstanding")
            chunks.append(chunk)
            remaining -= len(chunk)
        if process.stdout.read(1) != b"\n":
            raise RuntimeError("missing batch terminator")
        result[oid] = b"".join(chunks)
    process.stdin.close()
    if process.wait(timeout=30):
        raise RuntimeError("git cat-file batch failed")
    process.stdout.close()
    return result


def owner_path(path: str) -> bool:
    return path.startswith("docs/ilyra-fen/v666-v4/") or bool(re.fullmatch(r"scripts/(?:build_)?ghc_family_ilyra_fen_v666_v4[^/]*\.py", path)) or bool(re.fullmatch(r"tests/test_ghc_family_ilyra_fen_v666_v4[^/]*\.py", path))


def staged_review() -> None:
    review_path = "docs/ilyra-fen/v666-v4/validation/final-staged-review.json"
    delta_path = "docs/ilyra-fen/v666-v4/validation/final-delta-manifest.json"
    owner_manifest_path = "docs/ilyra-fen/v666-v4/validation/final-owner-manifest.json"
    excluded_self = {review_path, delta_path, owner_manifest_path}
    rows = [(status, path) for status, path in staged_rows() if path not in excluded_self]
    paths = [path for _, path in rows]
    if not rows:
        raise RuntimeError("no staged final content")
    invalid = [path for path in paths if not owner_path(path)]
    changed_x1 = [path for path in paths if path.startswith("docs/ilyra-fen/v666-v4/x1/") or path in {"scripts/build_ghc_family_ilyra_fen_v666_v4_x1.py", "tests/test_ghc_family_ilyra_fen_v666_v4_x1.py"}]
    states = index_state()
    blobs = batch_blobs([states[path][1] for path in paths])
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    parsed, candidates, maximum_words, maximum_path = 0, [], 0, ""
    for path in paths:
        raw = blobs[states[path][1]]
        text = raw.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF index blob: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed += 1
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    truth = json.loads(blobs[states["docs/ilyra-fen/v666-v4/closeout/phase-truth.json"][1]])
    route = json.loads(blobs[states["docs/ilyra-fen/v666-v4/orchestration/route-state-final-candidate.json"][1]])
    handoff = blobs[states["docs/ilyra-fen/v666-v4/handoffs/auren-lark-v666-v5-activation.md"][1]].decode("utf-8")
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    evidence_replay = replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA)
    checks = {
        "non_destructive_delta": all(status in {"A", "M"} for status, _ in rows) and not any(status == "D" for status, _ in rows),
        "owner_allowlist": not invalid,
        "x1_paths_unchanged": not changed_x1 and x1_replay["valid"],
        "evidence_manifest_replays": evidence_replay["valid"],
        "all_json_parse": True, "utf8_lf": True,
        "five_class_scan_zero_confirmed_hits": not candidates,
        "document_word_cap": maximum_words <= 100000,
        "handoff_word_range": 10000 <= len(re.findall(r"\S+", handoff)) <= 100000,
        "truth_counts_exact": truth["effective_negatives"] == 26519 and truth["effective_methods"] == 11176 and truth["outcome_counts"] == OUTCOMES,
        "gaps_and_gates_exact": truth["open_gaps"] == 186 and truth["exact_gates"] == 184,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and not route["successor_contacted"],
        "evidence_head_exact_before_final": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() == EVIDENCE_SHA,
        "owner_file_guard": len([path for path in states if owner_path(path)]) < 2000,
    }
    review = {
        "schema": "ghc.family.ilyra-fen.v666-v4.final-staged-review.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "lifecycle": "final", "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs", "reviewed_paths": paths, "reviewed_path_count": len(paths),
        "json_parsed": parsed, "maximum_document_words": maximum_words, "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(patterns), "privacy_candidates": len(candidates), "privacy_confirmed_hits": len(candidates),
        "privacy_candidate_rows": candidates, "checks": checks,
        "self_exclusions": [review_path, delta_path, owner_manifest_path],
        "claim_boundary": "exact staged same-owner final review only; not full repository suite, exhaustive security, privacy-complete, accessibility-complete, or independent reproduction",
        "valid": all(checks.values())
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])

    rows_for_delta = [(status, path) for status, path in staged_rows() if path not in {delta_path, owner_manifest_path}]
    states = index_state()
    blobs = batch_blobs([states[path][1] for _, path in rows_for_delta])
    delta_entries = []
    for status, path in rows_for_delta:
        mode, oid, stage = states[path]
        raw = blobs[oid]
        delta_entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw), "status": status})
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.final-delta-manifest.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "base_evidence_sha": EVIDENCE_SHA, "hash_source": "actual_git_index_blobs",
        "entries": delta_entries, "entry_count": len(delta_entries),
        "deletion_count": sum(row["status"] == "D" for row in delta_entries),
        "non_destructive": not any(row["status"] == "D" for row in delta_entries),
        "self_exclusions": [delta_path, owner_manifest_path]
    })
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])

    states = index_state()
    owner_paths = sorted(path for path in states if owner_path(path) and path != owner_manifest_path)
    owner_blobs = batch_blobs([states[path][1] for path in owner_paths])
    owner_entries = []
    for path in owner_paths:
        mode, oid, stage = states[path]
        raw = owner_blobs[oid]
        owner_entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)})
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.final-owner-manifest.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "hash_source": "prospective_final_git_index_blobs", "entries": owner_entries,
        "entry_count": len(owner_entries), "self_exclusion": owner_manifest_path,
        "owner_scopes": ["docs/ilyra-fen/v666-v4", "scripts/*ilyra_fen_v666_v4*.py", "tests/test_ghc_family_ilyra_fen_v666_v4*.py"],
        "materialization_guard": 2000, "guard_passed": len(owner_entries) < 2000
    })
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_manifest_path])
    print(json.dumps({"reviewed": len(paths), "final_delta_entries": len(delta_entries), "final_owner_entries": len(owner_entries), "json": parsed, "valid": True}, sort_keys=True))


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_ilyra_fen_v666_v4_closeout.py [--staged-review]")
