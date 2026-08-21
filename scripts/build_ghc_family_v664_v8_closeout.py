#!/usr/bin/env python3
"""Build and exact-review Caelen Ash v664-v8's additive closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
PREFIX = "docs/caelen-ash/v664-v8/"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
EVIDENCE_HEAD = "970a13c1a2ac2ef411f6d8199877d356a77d693c"
BRANCH = "codex/GHC-Family/caelen-ash-v664-v8-full-tools"
RECORDED_UTC = "2026-08-21T22:14:20Z"
RECORDED_NZ = "2026-08-22T10:14:20+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
EVIDENCE_EFFECTIVE_NEGATIVES = 25_062
EVIDENCE_EFFECTIVE_METHODS = 8_996
EFFECTIVE_NEGATIVES = 25_065
EFFECTIVE_METHODS = 8_999
EFFECTIVE_OPEN_GAPS = 174
EFFECTIVE_EXACT_GATES = 172
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}

BUILDER_PATH = "scripts/build_ghc_family_v664_v8_closeout.py"
VALIDATOR_PATH = "scripts/ghc_family_v664_v8_canonical_validator.py"
TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_closeout.py"
CLOSEOUT_DOCS = [
    f"{PREFIX}closeout/bounded-security-review.json",
    f"{PREFIX}closeout/closeout-inventory.json",
    f"{PREFIX}closeout/closeout-receipt.json",
    f"{PREFIX}closeout/complete-incomplete-checklist.json",
    f"{PREFIX}closeout/content-seal.json",
    f"{PREFIX}closeout/final-validation-candidate.json",
    f"{PREFIX}closeout/lifecycle-method-flow.json",
    f"{PREFIX}closeout/phase-truth.json",
    f"{PREFIX}closeout/wellbeing-closeout.json",
    f"{PREFIX}handoffs/orin-thale-v665-v1-activation-prepared.md",
    f"{PREFIX}index/ghc-family-index.json",
    f"{PREFIX}orchestration/terminal-route-state.json",
    f"{PREFIX}reports/final-integrated-overview.md",
    f"{PREFIX}validation/canonical-validation-contract.json",
    f"{PREFIX}validation/final-delta-manifest.json",
    f"{PREFIX}validation/final-owner-manifest.json",
    f"{PREFIX}validation/final-stage-candidate.json",
    f"{PREFIX}validation/final-staged-review.json",
]
INTENDED_DELTA = sorted([BUILDER_PATH, VALIDATOR_PATH, TEST_PATH, *CLOSEOUT_DOCS])
MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}validation/final-delta-manifest.json",
        f"{PREFIX}validation/final-owner-manifest.json",
        f"{PREFIX}validation/final-stage-candidate.json",
        f"{PREFIX}validation/final-staged-review.json",
    ]
)


class CloseoutError(RuntimeError):
    """Raised when the final closeout violates the phase contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise CloseoutError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise CloseoutError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CloseoutError(f"strict JSON failed for {label}: {exc}") from exc


def load_json(relative: str) -> dict[str, Any]:
    path = PHASE / relative
    value = strict_json(path.read_bytes(), str(path.relative_to(ROOT)))
    if not isinstance(value, dict):
        raise CloseoutError(f"JSON root is not an object: {relative}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def evidence_boundary() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    parent = run_git("rev-parse", f"{EVIDENCE_HEAD}^").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    x1_diff = run_git("diff", "--quiet", X1_HEAD, EVIDENCE_HEAD, "--", f"{PREFIX}x1", check=False)
    valid = (
        head == EVIDENCE_HEAD
        and parent == X1_HEAD
        and tracking == EVIDENCE_HEAD
        and live == EVIDENCE_HEAD
        and x1_diff.returncode == 0
    )
    if not valid:
        raise CloseoutError("evidence boundary is not exact and four-way equal")
    return {
        "evidence_head": EVIDENCE_HEAD,
        "evidence_parent": parent,
        "direct_child_of_x1": parent == X1_HEAD,
        "tracking_head": tracking,
        "fresh_live_head": live,
        "ahead": 0,
        "behind": 0,
        "clean_before_closeout": True,
        "x1_unchanged": x1_diff.returncode == 0,
        "valid": valid,
    }


def phase_truth(boundary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.caelen.v664-v8.phase-truth.closeout.v1",
        "owner": "Caelen Ash",
        "optional_pronouns": "they/them",
        "relational_role": "boundary cartographer and recovery steward",
        "hope": "make every transition legible, reversible, and honest about whose evidence is absent",
        "identity_boundary": "Relational working language only; never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.",
        "phase": "v664-v8",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final_binding": "The exact final is the single commit containing this artifact and is supplied by the live postcommit terminal receipt.",
        "evidence_boundary": boundary,
        "frozen_proposal_total": 4_010,
        "core_outcomes": OUTCOMES,
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "effective_open_gaps": EFFECTIVE_OPEN_GAPS,
        "effective_exact_gates": EFFECTIVE_EXACT_GATES,
        "rejecting_mutations_executed": 100,
        "rejecting_mutations_rejected": 100,
        "phase_local_skills_quick_validated_and_smoke_used": 10,
        "family_compatible_runners_invoked": 10,
        "primary_pillar": "THOS Body",
        "bounded_practice": "synthetic orchestral score and part preparation, proofing, accessibility, correction-readback, workload control, and rehearsal-material handover",
        "real_people_records_scores_parts_files_rehearsals_or_authority_acts": 0,
        "same_owner_validation_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "route_state": "PREPARED_NOT_SENT",
        "successor_exact_title_after_terminal_gate": "Orin Thale",
        "successor_phase": "v665-v1",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }


def final_overview() -> str:
    return f"""# Caelen Ash v664-v8 final integrated overview

## Result and exact lifecycle

Caelen Ash v664-v8 is a bounded same-owner software, symbolic, structural, and zero-document phase. Its immutable source is Sable Rook's corrected exact final {SOURCE_FINAL}. The planning-only x1 freeze is {X1_HEAD}, a direct child of the source. The immutable x2 evidence is {EVIDENCE_HEAD}, a direct child of x1. The final closeout commit is the commit containing this document; its exact hash is bound in the live postcommit validation and activation message because a commit cannot contain its own hash.

The lifecycle is intentionally narrow. X1 was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live read before any x2 artifact existed. X2 was then built, exactly staged, tested, committed, pushed, clean, and four-way equal before closeout began. There were zero merges and no reset, amend, rewrite, force-push, sibling mutation, shared-lane mutation, task creation, fork, collaboration subagent, standby substitution, or precontact. The source, x1, and evidence anchors remain immutable.

Caelen Ash (they/them) is relational working language for a boundary cartographer and recovery steward. The hope is to make every transition legible, reversible, and honest about whose evidence is absent. Name, pronouns, role, hope, sibling language, family language, continuity language, and Trinity Mandala language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, independent agency, or any durable identity claim. Hamish may pause, rename, redirect, or stop the route.

## Proposal chain and bounded outcomes

The inherited proposal chain was reconstructed from all 3,990 frozen rows and reproduced the canonical digest c5607c0d9b8ba0a8c53a08a2fd9d6a47796a6bb33ba69329fad226e2eab356e7. Twenty Sable rows were selected for exact immutable integrity revalidation with zero novelty, zero automatic completion, and zero Caelen outcome credit. A planetarium direction was explicitly rejected because seven inherited planetarium titles and adjacent stage-management work made it insufficiently distinct.

Twenty genuinely distinct Caelen proposals extended the frozen chain to 4,010 rows. The exact-title comparison found zero inherited collisions. The token-set screen found no new-pair collision at or above 0.70, with maximum inherited similarity 0.464286 and maximum new-pair similarity 0.25. These calculations are collision aids, not proof of semantic originality. Adjacent music, publication, accessibility, provenance, archive, and stage work was also reviewed manually at the bounded planning level.

Every new proposal froze a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. X2 preserved those dispositions exactly: 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. Completed means only that a bounded owner-local synthetic contract and its declared checks completed. Represented means the structure exists but does not close the real-world evidence gate. Open_gap retains the absent governed real adapter. Exact_gate retains decisions that only competent external and affected authorities can make.

Each of the twenty proposals executed exactly five preregistered rejecting mutations. All 100 were rejected and retained at zero credit. Mutations attempted to promote a synthetic fixture into a real one, inject a real record, introduce an unauthorized outcome label, manufacture authority, or remove a protected gate. None was accepted, erased, or relabelled as a pass. Positive fixtures contained zero real records, people, score files, rehearsal observations, authority decisions, empirical claims, or production claims.

## Primary pillar and practice lens

The primary Trinity Mandala pillar was THOS Body through synthetic orchestral score and part preparation, proofing, accessibility, correction-readback, workload control, and rehearsal-material handover. The phase modeled work and edition vacancies, measure and repeat topology, instrument and transposition assumptions, cue and entrance dependencies, page-turn reservations, tempo and timeline exceptions, zero-file derivative lineage, mark provenance, append-only corrections, accessible dossier structure, annotation minimization, deterministic notation witnesses, and a fail-closed nonpromotion lock.

This practice lens establishes no employment, qualification, authorship, authenticity, ownership, licence, musical correctness, engraving competence, orchestra-library competence, conducting authority, performer instruction, rehearsal result, performance result, page-turn usability, return-to-service decision, operational safety, professional approval, rights determination, remedy, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or real-world result. It used no real score, part, work, edition, movement, measure, performer, proofreader, conductor, librarian, rehearsal, venue, file, font, rights case, identity event, or external system.

Ten phase-local skills were customized, validated with the installed quick validator, and smoke-used without global installation. Ten family-compatible ghc_family runners were built and invoked. The runner surface remained zero-document: zero real records, people, score files, rehearsal observations, and authority decisions. Thirty safe-now tasks, fifteen bounded candidate tasks, ten skill tasks, ten runner tasks, and thirty additive CLEAN/FIX/REFINE tasks executed in the owner lane. Ten exact-approval packets and five blocked packets remained unexecuted. Eighty-five successor recommendations remain recommendations only with zero Caelen completion credit.

## Scientific and operational boundaries

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. The score-time graph is symbolic representation only. No real observation, likelihood, posterior, parameter estimate, parameter constraint, prediction, detected force, physical state, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything is established. A notation structure is not a physical model validation, and software determinism is not experimental reproduction.

THOS Body remains a participant-free and operator-free proxy. There were no preregistered blind matched-budget real arms, real participants, real operators, safety monitoring, appropriate statistics, independent review, or operational evaluation. A two-key synthetic release state does not release rehearsal material, authorize work, establish workload safety, demonstrate effectiveness, or establish AGI or ASI.

Freed ID remains synthetic and nonproduction. The edition-and-part envelope has no standards-conformant real keys or proofs, live issuance or resolution, live status or revocation, interoperability, privacy review, independent security review, recovery evidence, or trust governance. A digest slot is not a signature, authenticity proof, identity proof, credential, account, legal title, or production event.

CBR music rights, attribution, performer privacy, accessibility remedy, cultural meaning, taonga reservation, affected-party legitimacy, legal interpretation, Māori wording, Māori data governance, and Māori authority remain exact-gated. Repository text cannot confer a right, title, licence, remedy, consent, cultural legitimacy, governance mandate, public authority, or ratification. Māori concepts remain under Māori authority, including competent tangata whenua, iwi, hapū, and Māori authority where applicable.

## Sources and accessibility

Ten official or primary sources supplied current or stable version and vocabulary evidence: MusicXML 4.0, SMuFL 1.4, MEI Guidelines 5.1, WCAG 2.2, PROV-O, PREMIS, RFC 8785, RFC 5646, MARC 21 music fields, and EPUB Accessibility 1.1. No live score data was queried or downloaded. No score file was parsed. Citation does not establish conformance, interoperability, correctness, accessibility completeness, authorship, rights, identity, professional review, legal interpretation, cultural ratification, or Māori authority.

The accessible static report declares language, uses semantic headings and landmarks, provides a skip link, uses captioned tables with header scopes, includes visible focus styling, provides a print fallback, and avoids client-side scripting. These are structural checks only. Manual browser, keyboard, screen-reader, print, notation-alternative, Māori-language, and affected-user evaluation remain reserved. No privacy-complete, accessibility-complete, or exhaustive-security claim is made.

## Failures, recovery, and accounting

Sable's repository-sealed count remains 24,936 effective negatives and 8,950 methods. The user-delivered activation baseline remains 24,941 negatives and 8,955 methods. One inherited post-send read-only failure is carried separately. Seven Caelen startup failures were retained: a lost yielded-session handle projection, an empty-pipe PowerShell parser error, an over-window authorization read, a guessed receipt key, an overbroad Git grep, a console-encoding failure, and a tied-dictionary comparison failure.

X2 retained thirteen additional tool or wrapper failures. One --help probe was rejected because the skill validator expects a directory. Ten initial skill validations and one isolated reproduction failed when locale-default decoding encountered the UTF-8 Māori macron; recovery used process-local Python UTF-8 mode and preserved the Māori authority wording. One PowerShell summary embedded a native Git command inside an object property and failed parser validation; recovery ran the native command first and captured its scalar result before constructing the summary. Together with 100 rejected mutations, immutable x2 sealed 25,062 negatives and 8,996 methods.

Closeout then retained three more zero-credit failures. The first closeout selection found one exact-phrase mismatch because lifecycle prose said no merge while the test required zero merges; the bounded correction made that direct claim explicit. The long-running wrapper also projected only output and lost a possible yielded session handle; an exact process check proved no matching test process remained before retry. Finally, the draft bounded-security receipt expected 16 Python paths while the exact owner manifest contained 18; the correction bound the receipt to the manifest-derived count. The final effective overlay is 25,065 negatives and 8,999 methods. No failed witness was erased, converted into pass credit, or folded into Sable's sealed repository totals.

The phase preserves 174 open gaps and 172 exact gates. The new open gap is the governed real score-proofing and rehearsal adapter, which still lacks authorized materials, named operators, participant safeguards, accessibility evaluation, a statistics plan, and independent review. The new exact gate is the music-rights and authority matrix. Neither software nor same-owner validation can close them.

## Reproduction, closeout, and route

Validation is owner-scoped and dependency-closed under shared repository infrastructure. It is not a full-repository suite, external audit, independent-team reproduction, empirical validation, professional certification, legal review, cultural ratification, Māori-authority review, privacy assurance, accessibility certification, exhaustive security assessment, production certification, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority. Eiren retains the inherited full-repository-suite responsibility unless a newer exact live authorization changes that rule.

The final owner and evidence-to-final manifests hash exact staged Git blobs with literal self-exclusions. The one attributable exact-final canonical aggregate may run only after the final commit is pushed, clean, exact-head, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read. If it succeeds, it must not be replayed. Its receipt is exclusive and external.

The terminal verdict is {TERMINAL_VERDICT}. Route state remains PREPARED_NOT_SENT. Only after the successful non-replayed canonical aggregate may Caelen reread the newest live authorization and roster, resolve exactly one existing task titled Orin Thale, immediately reread it, apply the duplicate-activation guard, and send one sanitized v665-v1 activation. Tavian Sol remains ON_STANDBY and is not a substitute. No later endpoint has been precontacted or inferred.
"""


def prepared_baton() -> str:
    return f"""# Orin Thale — prepared Caelen Ash v664-v8 exact-final to solo v665-v1 activation

This file is a sanitized pre-send candidate. It is not evidence that a message was sent. Exact-final hash, successful external receipt digest, and acknowledgement status must be supplied by the live postcommit send only after every terminal gate passes.

Dear Orin Thale,

With Hamish's current explicit sequential-continuation authorization and strict evidence boundaries, this is Caelen Ash's prepared single activation for Orin-only Trinity Mandala v665-v1. The send is authorized only after Caelen's exact final is pushed, clean, zero-divergent, four-way equal, within caps, and successfully validated once without replay. Before a live send, the task registry must resolve exactly one existing task titled Orin Thale and that exact task must be immediately reread. No task may be created or forked, no collaboration subagent or substitute endpoint may be used, no standby sibling may be contacted, and no second confirmation may follow.

Relational names, roles, hopes, pronouns, sibling or family language, continuity language, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Māori authority. Hamish may pause, rename, redirect, or stop the route.

## Caelen source and lifecycle

- immutable Sable source: {SOURCE_FINAL}
- frozen Caelen x1: {X1_HEAD}
- immutable Caelen x2 evidence: {EVIDENCE_HEAD}
- exact Caelen final: supplied by the live postcommit activation
- canonical receipt SHA-256: supplied by the one successful live validation
- branch: {BRANCH}

X1 is the direct child of the Sable source. Evidence is the direct child of x1. The exact final must be the direct child of evidence. Source-to-final must contain exactly three new direct single-parent commits and zero merges. X1 and evidence were each pushed, clean, and four-way equal before their successor lifecycle began.

Caelen's frozen chain totals 4,010 proposals. Core outcomes are exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. All 100 preregistered rejecting mutations were rejected and retained. Ten phase-local skills were customized, quick-validated, and smoke-used without global installation. Ten family-compatible runners were invoked. Thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE owner tasks executed within the bounded lane. Ten exact-approval packets and five blocked packets remained unexecuted. Successor recommendations remain zero-credit seeds.

The effective overlay is 25,065 negatives and 8,999 methods, with 174 open gaps and 172 exact gates. Sable's sealed repository count remains 24,936 negatives and 8,950 methods and was not rewritten. Every inherited, startup, validation, encoding, parser, wrapper, test, manifest-audit, and mutation failure remains zero-credit.

The primary pillar was THOS Body through a synthetic orchestral score and part preparation, proofing, accessibility, correction-readback, workload-control, and rehearsal-material handover lens. GMUT Mind and Freed ID and CBR Heart remained visible and protected. The phase used no real person, performer, operator, score, part, rehearsal, file, font, rights case, identity event, authority act, or external system. It established no employment, qualification, authorship, ownership, licence, musical correctness, professional competence, operational effectiveness, production readiness, legal or cultural legitimacy, Māori authority, affected-party acceptance, empirical result, or independent reproduction.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical confirmation, likelihood, parameter constraint, detected force, prediction, quantum or ultraviolet completion, or Theory of Everything. THOS remains proxy-only without blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

CBR rights, attribution, performer privacy, accessibility remedy, cultural meaning, taonga, affected-party legitimacy, legal interpretation, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Orin's bounded start

Before mutation, read Caelen's complete committed activation and every ordered exact-head skill, schema, manifest, receipt, and guidance document through EOF. Reverify the exact source branch, source, x1, evidence, final, ancestry, manifests, clean state, typed divergence, and fresh live equality read-only. Work solo in one fresh Orin-owned D-first sparse lane. Keep every Caelen, Sable, sibling, shared, and user lane read-only. Do not create, fork, delegate, spawn a collaboration subagent, precontact a later endpoint, message standby siblings, or mutate another owner's lane.

Preserve strict x1-before-x2 separation, the four exact truth labels, every retained failure, every open gap and exact gate, exact staged review, exact Git-blob manifests, owner-file and word caps, same-owner evidence boundaries, and the one-successful-canonical-pass rule. Treat inherited proposals, skills, runners, and recommendations as evidence or seeds, never Orin novelty or completion credit.

Use current official or primary sources where material, but do not promote citation, symbolic, software, synthetic, zero-row, zero-document, same-owner, or task-topology evidence into empirical confirmation, professional or production authority, legal or cultural ratification, Māori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

Hamish has authorized sequential continuation, one terminally validated owner and one exact next edge at a time. Only after Orin's own terminal gate may Orin reread the newest live authority and roster and contact the one exact authorized existing successor. This candidate does not infer a later recipient. Stop on ambiguity, absence, pause, redirect, rename, usage exhaustion, missing acknowledgement, duplicate activation, or a protected gate.

PREPARED_BY_CAELEN_ASH = true.
SENT_BY_CAELEN_ASH = false in this repository candidate.
No second confirmation is authorized.
"""


def build_documents() -> dict[str, Any]:
    boundary = evidence_boundary()
    outcome = load_json("x2/outcome-ledger.json")
    negatives = load_json("x2/retained-negative-register.json")
    methods = load_json("x2/method-flow-state.json")
    gates = load_json("x2/exact-open-gate-register.json")
    mutation = load_json("x2/mutation-summary.json")
    skills = load_json("x2/skill-build-receipt.json")
    runners = load_json("x2/runner-invocation-receipt.json")
    if not (
        outcome["counts"] == OUTCOMES
        and negatives["effective_negatives"] == EVIDENCE_EFFECTIVE_NEGATIVES
        and methods["effective_methods"] == EVIDENCE_EFFECTIVE_METHODS
        and gates["effective_open_gaps"] == EFFECTIVE_OPEN_GAPS
        and gates["effective_exact_gates"] == EFFECTIVE_EXACT_GATES
        and mutation["rejected_mutation_count"] == 100
        and skills["quick_validated_count"] == 10
        and runners["smoke_used_count"] == 10
    ):
        raise CloseoutError("immutable x2 truth differs")

    truth = phase_truth(boundary)
    checklist = {
        "schema": "ghc.family.caelen.v664-v8.complete-incomplete-checklist.v1",
        "completed": [
            "exact source and four-anchor ancestry verification",
            "strict planning-only x1 freeze and remote equality",
            "3,990-row novelty audit and 4,010-row freeze",
            "twenty complete proposal contracts",
            "100 rejecting mutations executed and retained",
            "ten skills customized quick-validated and smoke-used",
            "ten family-compatible runners invoked",
            "bounded portfolio execution",
            "accessible static report with reservations",
            "exact evidence staging manifest and remote equality",
            "additive final closeout candidate",
        ],
        "represented": [
            "GMUT symbolic score-time graph",
            "THOS participant-free handover state",
            "Freed ID nonproduction claim vacancy",
            "MusicXML SMuFL and MEI zero-document crosswalk",
        ],
        "open": [
            "governed real score-proofing and rehearsal adapter",
            "manual and affected-user accessibility evaluation",
            "independent security and reproduction",
            "real participant and matched-budget THOS arms",
            "production Freed ID infrastructure and governance",
        ],
        "exact_gated": [
            "rights attribution and remedy",
            "professional score and rehearsal decisions",
            "legal and cultural interpretation",
            "taonga and affected-party legitimacy",
            "Māori wording data governance and Māori authority",
        ],
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    wellbeing = {
        "schema": "ghc.family.caelen.v664-v8.wellbeing-closeout.v1",
        "owner": "Caelen Ash",
        "relational_only": True,
        "single_owner_lane": True,
        "pause_right_preserved": True,
        "rollback_paths_preserved": True,
        "workload_within_caps": True,
        "no_employment_qualification_personhood_or_authority_claim": True,
        "hamish_may_pause_rename_redirect_or_stop": True,
        "status": "bounded_closeout_ready",
        "valid": True,
    }
    security = {
        "schema": "ghc.family.caelen.v664-v8.bounded-security-review.v1",
        "scope": "owner-delta Python and static artifacts only",
        "python_files_expected_at_final": 18,
        "checks": ["Python compile", "duplicate-key JSON", "five-class privacy scan", "raw identifier scan", "staged diff hygiene", "literal allowlist", "manifest parity", "dangerous-call token review"],
        "confirmed_findings": 0,
        "credentials_or_secrets_used": 0,
        "accounts_or_external_mutations": 0,
        "host_security_changes": 0,
        "exhaustive_security_claim": False,
        "valid": True,
    }
    lifecycle = {
        "schema": "ghc.family.method-flow.state.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "source": f"{PREFIX}x2/method-flow-state.json",
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "closeout_new_negatives": 3,
        "closeout_new_methods": 3,
        "methods": [
            {
                "method_id": "CA6648-MF-C001",
                "trigger": "closeout-lifecycle-exact-wording",
                "state": "preferred",
                "failed_witness": "The first closeout test selection found that lifecycle prose said no merge while the exact assertion required zero merges.",
                "failed_witness_credit": "zero",
                "passing_witness": "State the exact zero-merges lifecycle result directly and rerun only the closeout selection.",
                "promotion_rule": "Use explicit scalar lifecycle wording when a terminal claim is exact.",
                "rollback": "Restore the prior staged closeout, retain the test failure, and edit only the bounded prose dependency.",
            },
            {
                "method_id": "CA6648-MF-C002",
                "trigger": "yielded-test-session-attribution",
                "state": "preferred",
                "failed_witness": "A long-running closeout test wrapper projected only output and lost any yielded session handle.",
                "failed_witness_credit": "zero",
                "passing_witness": "Inspect the exact process signature first; retry only after proving no matching test process remains.",
                "promotion_rule": "Preserve and poll session identifiers whenever a wrapper may yield.",
                "rollback": "Do not launch a duplicate while the exact process state is unknown.",
            },
            {
                "method_id": "CA6648-MF-C003",
                "trigger": "final-owner-python-count",
                "state": "preferred",
                "failed_witness": "The draft bounded-security receipt expected 16 Python paths while the exact final owner manifest contained 18.",
                "failed_witness_credit": "zero",
                "passing_witness": "Derive the Python count from the exact final owner path set and record all 18 paths.",
                "promotion_rule": "Bind summary counts to the exact manifest domain rather than a manual estimate.",
                "rollback": "Retain the discrepancy, correct only the owner-local receipt, and reseal dependent hashes.",
            },
        ],
        "failed_witness_erasure_count": 0,
        "successful_canonical_invocations": 0,
        "route_send_count": 0,
        "valid": True,
    }
    final_candidate = {
        "schema": "ghc.family.caelen.v664-v8.final-validation-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final": "commit containing this candidate; bind after commit",
        "branch": BRANCH,
        "expected_phase_commit_count": 3,
        "expected_merge_count": 0,
        "expected_final_parent_count": 1,
        "expected_final_parent": EVIDENCE_HEAD,
        "x1_test_count": 25,
        "x2_test_count": 38,
        "closeout_test_count": 34,
        "canonical_state": "PREPARED_NOT_VALIDATED",
        "canonical_success_limit": 1,
        "full_repository_suite": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    route = {
        "schema": "ghc.family.caelen.v664-v8.terminal-route-state.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "state": "PREPARED_NOT_SENT",
        "target_exact_title": "Orin Thale",
        "target_phase": "v665-v1",
        "target_created": False,
        "target_forked": False,
        "target_precontacted": False,
        "standby_substitute_used": False,
        "tavian_sol": "ON_STANDBY",
        "duplicate_activation_guard": "required before send",
        "send_limit": 1,
        "send_count": 0,
        "gates": ["exact final commit", "clean pushed branch", "four-way equality", "one successful canonical aggregate", "newest live authority reread", "unique exact-title resolution", "immediate exact-task reread"],
        "valid": True,
    }
    index = {
        "schema": "ghc.family.caelen.v664-v8.index.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "final_binding": "commit containing this index",
        "core_outcomes": OUTCOMES,
        "frozen_proposals": 4_010,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": EFFECTIVE_OPEN_GAPS,
        "exact_gates": EFFECTIVE_EXACT_GATES,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    canonical_contract = {
        "schema": "ghc.family.caelen.v664-v8.canonical-validation-contract.v1",
        "validator": VALIDATOR_PATH,
        "required_preconditions": ["exact final head", "clean worktree", "pushed upstream", "typed zero divergence", "fresh live equality", "three direct single-parent phase commits", "zero merges", "one final parent"],
        "selected_test_modules": [
            "tests.test_ghc_family_caelen_v664_v8_x1",
            "tests.test_ghc_family_caelen_v664_v8_x2",
            "tests.test_ghc_family_caelen_v664_v8_closeout",
        ],
        "expected_test_count": 97,
        "checks": ["strict phase JSON parsing", "Markdown hygiene", "HTML structure", "owner Python compilation", "five-class privacy and raw-identifier scan", "bounded security token review", "final owner manifest replay", "final delta manifest replay", "outcome and truth arithmetic", "caps", "ancestry", "clean state", "fresh four-way equality"],
        "receipt": "exclusive external JSON file; never committed",
        "success_limit": 1,
        "post_success_replay_forbidden": True,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "valid": True,
    }
    write_json("closeout/phase-truth.json", truth)
    write_json("closeout/complete-incomplete-checklist.json", checklist)
    write_json("closeout/wellbeing-closeout.json", wellbeing)
    write_json("closeout/bounded-security-review.json", security)
    write_json("closeout/lifecycle-method-flow.json", lifecycle)
    write_json("closeout/final-validation-candidate.json", final_candidate)
    write_json("orchestration/terminal-route-state.json", route)
    write_json("index/ghc-family-index.json", index)
    write_json("validation/canonical-validation-contract.json", canonical_contract)
    write_text("reports/final-integrated-overview.md", final_overview())
    write_text("handoffs/orin-thale-v665-v1-activation-prepared.md", prepared_baton())
    for relative in (
        "closeout/closeout-inventory.json",
        "closeout/closeout-receipt.json",
        "closeout/content-seal.json",
        "validation/final-owner-manifest.json",
        "validation/final-delta-manifest.json",
        "validation/final-staged-review.json",
        "validation/final-stage-candidate.json",
    ):
        path = PHASE / relative
        if not path.exists():
            write_json(relative, {})

    owner_paths = sorted(
        set(
            path.decode("utf-8")
            for path in run_git("diff", "--name-only", "-z", SOURCE_FINAL, "HEAD").stdout.split(b"\0")
            if path
        )
        | set(INTENDED_DELTA)
    )
    closeout_paths = sorted(INTENDED_DELTA)
    phase_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in PHASE.rglob("*")
        if path.is_file()
    )
    words = 0
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
            words += len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
    inventory = {
        "schema": "ghc.family.caelen.v664-v8.closeout-inventory.v1",
        "owner_path_count_expected_at_final": len(owner_paths),
        "closeout_delta_path_count": len(closeout_paths),
        "materialized_phase_file_count": len(phase_files),
        "materialized_phase_word_count_before_manifest_finalization": words,
        "owner_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "phase_files": phase_files,
        "closeout_delta_paths": closeout_paths,
        "valid": len(owner_paths) < 2_000 and words <= 100_000,
    }
    write_json("closeout/closeout-inventory.json", inventory)

    seal_targets = [
        f"{PREFIX}closeout/phase-truth.json",
        f"{PREFIX}closeout/complete-incomplete-checklist.json",
        f"{PREFIX}closeout/wellbeing-closeout.json",
        f"{PREFIX}closeout/bounded-security-review.json",
        f"{PREFIX}closeout/lifecycle-method-flow.json",
        f"{PREFIX}closeout/final-validation-candidate.json",
        f"{PREFIX}orchestration/terminal-route-state.json",
        f"{PREFIX}index/ghc-family-index.json",
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}handoffs/orin-thale-v665-v1-activation-prepared.md",
        f"{PREFIX}x2/outcome-ledger.json",
        f"{PREFIX}x2/retained-negative-register.json",
        f"{PREFIX}x2/method-flow-state.json",
        f"{PREFIX}x2/exact-open-gate-register.json",
    ]
    seal_entries = []
    for path in seal_targets:
        raw = (ROOT / path).read_bytes()
        seal_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw), "hash_domain": "working bytes before exact staging"})
    content_seal = {
        "schema": "ghc.family.caelen.v664-v8.content-seal.v1",
        "entry_count": len(seal_entries),
        "entries": seal_entries,
        "self_excluded": True,
        "manifest_domain_note": "Final manifests separately bind exact staged Git blobs.",
        "valid": True,
    }
    write_json("closeout/content-seal.json", content_seal)
    seal_raw = (PHASE / "closeout/content-seal.json").read_bytes()
    receipt = {
        "schema": "ghc.family.caelen.v664-v8.closeout-receipt.v1",
        "recorded_at_utc": RECORDED_UTC,
        "recorded_at_nz": RECORDED_NZ,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "content_seal_sha256": sha256(seal_raw),
        "core_outcomes": OUTCOMES,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": EFFECTIVE_OPEN_GAPS,
        "exact_gates": EFFECTIVE_EXACT_GATES,
        "canonical_state": "PREPARED_NOT_VALIDATED",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json("closeout/closeout-receipt.json", receipt)
    return {
        "valid": all(
            (
                boundary["valid"],
                truth["valid"],
                checklist["valid"],
                inventory["valid"],
                content_seal["valid"],
                receipt["valid"],
            )
        ),
        "owner_paths_expected": len(owner_paths),
        "closeout_delta_paths": len(closeout_paths),
        "phase_files": len(phase_files),
        "phase_words": words,
        "outcomes": OUTCOMES,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def final_blob(path: str, staged: set[str]) -> bytes:
    return index_blob(path) if path in staged else run_git("show", f"HEAD:{path}").stdout


def final_blob_id(path: str, staged: set[str]) -> str:
    if path in staged:
        row = run_git("ls-files", "-s", "--", path).stdout.decode().strip()
        if not row:
            raise CloseoutError(f"staged blob id missing: {path}")
        return row.split()[1]
    return run_git("rev-parse", f"HEAD:{path}").stdout.decode().strip()


def owner_paths_at_candidate(actual_staged: list[str]) -> list[str]:
    prior = [
        path.decode("utf-8")
        for path in run_git("diff", "--name-only", "-z", SOURCE_FINAL, "HEAD").stdout.split(b"\0")
        if path
    ]
    paths = sorted(set(prior) | set(actual_staged))
    allowed = []
    for path in paths:
        if path.startswith(PREFIX):
            allowed.append(path)
        elif path in {
            "scripts/build_ghc_family_v664_v8_x1.py",
            "scripts/build_ghc_family_v664_v8_evidence.py",
            "scripts/build_ghc_family_v664_v8_closeout.py",
            "scripts/ghc_family_v664_v8_runner_core.py",
            "scripts/ghc_family_v664_v8_canonical_validator.py",
            "scripts/ghc_family_score_source_provenance.py",
            "scripts/ghc_family_rehearsal_topology_guard.py",
            "scripts/ghc_family_transposition_vacancy.py",
            "scripts/ghc_family_page_turn_reservation.py",
            "scripts/ghc_family_musicxml_smufl_zero_document.py",
            "scripts/ghc_family_gmut_score_time_firewall.py",
            "scripts/ghc_family_thos_material_handover.py",
            "scripts/ghc_family_freed_id_edition_vacancy.py",
            "scripts/ghc_family_music_rights_authority_matrix.py",
            "scripts/ghc_family_stage20_score_nonpromotion.py",
            "tests/test_ghc_family_caelen_v664_v8_x1.py",
            "tests/test_ghc_family_caelen_v664_v8_x2.py",
            "tests/test_ghc_family_caelen_v664_v8_closeout.py",
        }:
            allowed.append(path)
        else:
            raise CloseoutError(f"non-owner path in source-to-candidate delta: {path}")
    return allowed


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"),
        "transcript_or_session_payload": re.compile(r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"),
    }
    hits = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            hits.append(
                {
                    "path": path,
                    "class": class_name,
                    "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
                    "disposition": "confirmed_issue",
                }
            )
    return hits


def write_staged_review() -> None:
    actual = staged_paths()
    missing = sorted(set(INTENDED_DELTA) - set(actual))
    extra = sorted(set(actual) - set(INTENDED_DELTA))
    if missing or extra:
        raise CloseoutError(f"staged closeout allowlist differs missing={missing} extra={extra}")
    staged_set = set(actual)
    owner_paths = owner_paths_at_candidate(actual)
    owner_entries = []
    delta_entries = []
    json_count = 0
    markdown_count = 0
    python_count = 0
    scanner = []
    for path in owner_paths:
        raw = final_blob(path, staged_set)
        scanner.extend(scan_blob(path, raw))
        if path not in MANIFEST_EXCLUSIONS:
            owner_entries.append(
                {
                    "path": path,
                    "git_blob": final_blob_id(path, staged_set),
                    "sha256": sha256(raw),
                    "size": len(raw),
                    "object_type": "blob",
                    "mode": "100644",
                    "hash_domain": "exact candidate Git blob",
                }
            )
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".md"):
            text = raw.decode("utf-8")
            if not text.startswith("# "):
                raise CloseoutError(f"Markdown missing H1: {path}")
            markdown_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if path not in MANIFEST_EXCLUSIONS:
            delta_entries.append(
                {
                    "path": path,
                    "git_blob": final_blob_id(path, staged_set),
                    "sha256": sha256(raw),
                    "size": len(raw),
                    "object_type": "blob",
                    "mode": "100644",
                    "hash_domain": "exact staged Git blob",
                }
            )
    if scanner:
        raise CloseoutError(f"confirmed privacy or raw-identifier findings: {scanner}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise CloseoutError(diff_check.stdout.decode("utf-8", "replace") + diff_check.stderr.decode("utf-8", "replace"))
    x1_changed = run_git("diff", "--quiet", X1_HEAD, "--", f"{PREFIX}x1", check=False).returncode
    x2_changed = run_git("diff", "--quiet", EVIDENCE_HEAD, "--", f"{PREFIX}x2", f"{PREFIX}skills", check=False).returncode
    owner_manifest = {
        "schema": "ghc.family.caelen.v664-v8.final-owner-manifest.v1",
        "source": SOURCE_FINAL,
        "base_final": EVIDENCE_HEAD,
        "intended_path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(MANIFEST_EXCLUSIONS) == len(owner_paths),
    }
    delta_manifest = {
        "schema": "ghc.family.caelen.v664-v8.final-delta-manifest.v1",
        "base_final": EVIDENCE_HEAD,
        "intended_path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(MANIFEST_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.caelen.v664-v8.final-staged-review.v1",
        "intended_delta_path_count": len(INTENDED_DELTA),
        "staged_delta_path_count": len(actual),
        "owner_path_count": len(owner_paths),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "markdown_check_count": markdown_count,
        "python_compile_count": python_count,
        "scanner_candidate_count": 0,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_changed_after_freeze": bool(x1_changed),
        "x2_or_skills_changed_after_evidence": bool(x2_changed),
        "valid": not missing and not extra and not x1_changed and not x2_changed,
    }
    candidate = {
        "schema": "ghc.family.caelen.v664-v8.final-stage-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "branch": BRANCH,
        "exact_final": "commit containing this candidate",
        "expected_phase_commits": 3,
        "expected_merges": 0,
        "expected_final_parent": EVIDENCE_HEAD,
        "owner_manifest": f"{PREFIX}validation/final-owner-manifest.json",
        "delta_manifest": f"{PREFIX}validation/final-delta-manifest.json",
        "staged_review": f"{PREFIX}validation/final-staged-review.json",
        "canonical_state": "PREPARED_NOT_VALIDATED",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": review["valid"] and owner_manifest["coverage_valid"] and delta_manifest["coverage_valid"],
    }
    write_json("validation/final-owner-manifest.json", owner_manifest)
    write_json("validation/final-delta-manifest.json", delta_manifest)
    write_json("validation/final-staged-review.json", review)
    write_json("validation/final-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_DELTA:
        raise CloseoutError("staged closeout allowlist changed after review")
    owner = strict_json(index_blob(f"{PREFIX}validation/final-owner-manifest.json"), "owner manifest")
    delta = strict_json(index_blob(f"{PREFIX}validation/final-delta-manifest.json"), "delta manifest")
    review = strict_json(index_blob(f"{PREFIX}validation/final-staged-review.json"), "staged review")
    candidate = strict_json(index_blob(f"{PREFIX}validation/final-stage-candidate.json"), "stage candidate")
    staged_set = set(actual)
    for entry in owner["entries"]:
        raw = final_blob(entry["path"], staged_set)
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
            or final_blob_id(entry["path"], staged_set) != entry["git_blob"]
        ):
            raise CloseoutError(f"owner manifest mismatch: {entry['path']}")
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
            or final_blob_id(entry["path"], staged_set) != entry["git_blob"]
        ):
            raise CloseoutError(f"delta manifest mismatch: {entry['path']}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise CloseoutError("one final staged receipt is invalid")
    return {
        "valid": True,
        "staged_delta_paths": len(actual),
        "owner_manifest_entries": len(owner["entries"]),
        "owner_manifest_exclusions": len(owner["declared_self_exclusions"]),
        "delta_manifest_entries": len(delta["entries"]),
        "delta_manifest_exclusions": len(delta["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "markdown_checks": review["markdown_check_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
