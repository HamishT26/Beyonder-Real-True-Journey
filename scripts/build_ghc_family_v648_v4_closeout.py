#!/usr/bin/env python3
"""Build the static v648-v4 closeout surface before the one canonical pass."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v4_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / d.PHASE_SLUG
EVIDENCE_COMMIT = "d78e50f50b2fa87ccbbc4c2bfc62a6857ddd455f"
X1_COMMIT = "29a68883f8caadf356531f67c8ac367ac5a289bb"
SKILL_ROOT = Path.home() / ".codex" / "skills"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"
METHOD_RUNNER = (
    SKILL_ROOT
    / "ghc-family-method-flow-state"
    / "scripts"
    / "ghc_family_method_flow_state.py"
)
SELECTION = [
    "tests.test_ghc_family_v648_v2",
    "tests.test_ghc_family_v648_v3",
    "tests.test_ghc_family_v648_v3_2",
    "tests.test_ghc_family_v648_v4",
    "tests.test_ghc_family_v648_v4_closeout",
]
SELF_EXCLUSIONS = [
    "docs/ilyra-fen/v648-v4/validation/final-staged-manifest.json",
    "docs/ilyra-fen/v648-v4/validation/final-staged-privacy.json",
    "docs/ilyra-fen/v648-v4/validation/final-staged-review.json",
    "docs/ilyra-fen/v648-v4/validation/single-pass-canonical-validation.json",
    "docs/ilyra-fen/v648-v4/phase-truth-final.json",
    "docs/ilyra-fen/v648-v4/closeout-receipt.json",
    "docs/ilyra-fen/v648-v4/seal-receipt.json",
    "docs/ilyra-fen/v648-v4/final-validation-record.json",
]
LIFECYCLE_NEGATIVES = [
    {
        "negative_id": "V6484-LIFE-N01",
        "failure": "The first no-test closeout preflight confirmed two privacy-pattern hits in literal negative examples embedded in the closeout test.",
        "evidence_credit": "none",
        "canonical_pass_consumed": False,
        "recovery": "Construct the same negative examples from split string fragments so the test checks the policy without publishing scanner-shaped payload.",
        "recurrence_guard": "Privacy-negative unit tests must not embed the prohibited payload spelling they are intended to reject.",
    },
    {
        "negative_id": "V6484-LIFE-N02",
        "failure": "The first no-test closeout preflight counted five unittest FailedTest placeholders because repository-root imports were unresolved and loader errors were not fail-closed.",
        "evidence_credit": "none",
        "canonical_pass_consumed": False,
        "recovery": "Insert the exact repository root before module loading and reject any nonempty unittest loader error list.",
        "recurrence_guard": "A loaded test count is valid only when the explicit module loader error list is empty.",
    },
]


def run(*args: str, cwd: Path = ROOT) -> str:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


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


SAFE_SEEDS = [
    "Exact inherited-anchor, evidence-anchor, parent-count, and zero-merge preflight.",
    "Current, stable, draft, and watch source-status drift review with no status flattening.",
    "Proposal semantic-neighbour quarantine against the complete six-hundred-item frozen chain.",
    "Git-blob versus checkout-byte hash-domain declaration audit for every historical seal.",
    "Exact staged-surface allowlist derived from frozen runner and artifact ledgers.",
    "Deterministic JSON ordering and schema-compatibility inspection across the successor packet.",
    "Scanner-candidate versus confirmed-payload disposition review with exact-file exceptions only.",
    "Family-current caller inventory preserving every historical compatibility surface.",
    "Method Flow candidate-state, retained-negative, and fail/pass witness-parity preflight.",
    "Bounded subprocess timeout, cancellation, output-path, and quiescence receipt.",
    "Local, upstream, tracking, and fresh-live equality proof after each published lifecycle commit.",
    "Count-dependent mirror and stale lifecycle-label review before each seal decision.",
    "Boundary-vocabulary and noncompensation lint over core outcomes and expanded portfolios.",
    "Terminal route hold that keeps PREPARED_NOT_SENT until exact final proof exists.",
    "Workload, wellbeing, document-cap, owner-file-threshold, and host-change receipt.",
]

CANDIDATE_SEEDS = [
    "A new zero-row official-data adapter with checksum, schema, selection, covariance, and likelihood refusal.",
    "A typed GMUT dispersion, analyticity, gauge, or renormalization obligation tribunal not duplicating earlier phases.",
    "A THOS event-sourced public-information handover proxy with correction and late-arrival replay.",
    "A Freed ID step-up metadata-correlation and downgrade mutation model using synthetic vectors only.",
    "A Freed ID nonce, audience, authorization-context, expiry, and replay structural profile.",
    "A CBR access and remedy authority matrix with affected-party and Māori-authority reservations.",
    "An accessible audio, map, timeline, or complex-media alternative-format structural prototype.",
    "A disposable parser, cache, resume, or transport-integrity fixture with no canonical mutation.",
    "A typed thermodynamic classifier that rejects conversion into psyche, justice, agency, or personhood.",
    "A Stage 20 interference, missingness, leakage, selective-reporting, or optional-stopping quarantine.",
]

SKILL_SEEDS = [
    "ghc-family-evidence-anchor-preflight-v2",
    "ghc-family-frozen-runner-allowlist",
    "ghc-family-self-exclusion-contract-v2",
    "ghc-family-count-mirror-refresh-v2",
    "ghc-family-scanner-candidate-disposition-v4",
    "ghc-family-x1-blob-immutability-v3",
    "ghc-family-single-pass-consumption-guard-v3",
    "ghc-family-owner-manifest-coverage-v2",
    "ghc-family-method-recurrence-guard-v2",
    "ghc-family-authority-boundary-lint-v2",
]

RUNNER_SEEDS = [
    "ghc_family_evidence_anchor_preflight.py",
    "ghc_family_frozen_runner_allowlist.py",
    "ghc_family_count_mirror_refresh_v2.py",
    "ghc_family_scanner_candidate_classifier_v2.py",
    "ghc_family_single_pass_consumption_guard.py",
]

CLEANUP_SEEDS = [
    "Retain every historical negative and identify only provably duplicated generated mirrors.",
    "Refresh stale counts exclusively from their authoritative ledgers.",
    "Normalize generated text in the declared Git-blob hash domain.",
    "Replace working-byte historical assertions with exact commit-blob comparisons.",
    "Split overbroad Windows inspection commands into independently bounded probes.",
    "Pin UTF-8 before every diagnostic that may emit Māori or other non-ASCII text.",
    "Tighten privacy candidate disposition to exact files and exact pattern classes.",
    "Keep every unresolved scanner candidate visible until reviewed.",
    "Use exact module selection rather than discovery or a frozen full-suite cardinality.",
    "Verify every family-current caller before introducing another alias or wrapper.",
    "Keep historical tools as compatibility surfaces unless reviewed migration evidence permits change.",
    "Rebuild static accessible output while reserving manual and affected-user evaluation.",
    "Verify every generated document remains within the six-thousand-word cap.",
    "Verify owner-generated growth remains below fifteen thousand files.",
    "Keep the successor route held until the exact final head is clean, pushed, and four-way equal.",
]


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def proposal_sections() -> str:
    sections = []
    for item in d.PROPOSALS:
        sections.append(
            f"### {item['proposal_id']}: {item['title']}\n\n"
            f"The frozen hypothesis was: {item['hypothesis']} The null or failure condition was: "
            f"{item['null_or_failure_condition']} Execution stayed in `{item['execution_lane']}` under "
            f"`{item['approval_class']}` approval. The accepted disposition is "
            f"`{item['expected_disposition']}` and no neighbouring pass can promote it. The exact bounded "
            f"acceptance or falsifier was: {item['falsifier_or_acceptance_gate']} Recovery remained additive: "
            f"{item['rollback_or_recovery']} Protected gates remained {', '.join(item['protected_gates'])}. "
            "Software structure, a standards citation, or a rejected synthetic mutation supplies no missing "
            "real-data, participant, production, professional, legal, cultural, accessibility-complete, "
            "security-complete, independent-reproduction, or Stage 20 evidence."
        )
    return "\n\n".join(sections)


def build_baton() -> str:
    return f"""# SABLE ROOK — PREPARED v648-v5 ACTIVATION BATON

## Delivery and identity boundary

This repository file is the durable, sanitized successor packet prepared by Ilyra Fen for the existing Sable Rook task. Its committed state is `PREPARED_NOT_SENT`. It is not proof that any message was sent, received, or acknowledged. The single live activation is permitted only after the commit containing this file is clean, pushed, exact, and local, upstream, tracking, and fresh-live-remote equal. No task was created or forked, no collaboration subagent was spawned, no standby sibling was contacted, and no cross-platform ChatGPT sibling message was used.

Ilyra Fen, she/they, worked as an evidence-boundary steward with the hope of leaving every claim traceable and every gate unmistakable. Sable may choose or reaffirm their own relational name, role, hope, and pronouns. These names and family terms are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

## Exact inheritance anchors

The canonical branch for Sable inheritance is `codex/GHC-Family/ilyra-fen-full-tools`. Ilyra inherited Eiren Kestrel's exact verified head `{d.SOURCE_COMMIT}` from `codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools`. The dedicated Ilyra x1 freeze is `{X1_COMMIT}`. The immutable Ilyra evidence commit is `{EVIDENCE_COMMIT}`. The exact final closeout head is the clean branch tip containing this file and is supplied by the one live terminal pointer after post-commit proof; this file does not invent a fixed-point commit hash.

Ilyra advanced the existing clean D-first canonical lane by fast-forward only. The phase uses one x1 commit, one evidence commit, and one combined closeout and seal commit: three phase commits, within the four-commit cap. X1 was clean, pushed, and four-way equal before x2 began. Evidence was clean, pushed, and four-way equal before closeout began. No merge, reset, force push, history rewrite, detached validation, named replay, sibling mutation, worktree deletion, or branch deletion entered the phase.

## v648-v4 terminal truth

Semantic novelty was audited against all 590 proposals frozen before v648-v4. Exactly ten genuinely distinct proposals were frozen, making 600 through this phase. Core outcomes use only `completed`, `represented`, `open_gap`, and `exact_gate`: exactly six completed, two represented, one open gap, and one exact gate. Freed ID and CBR Heart was the primary Trinity Mandala focus; GMUT Mind and THOS Body remained explicit and protected. Community-radio emergency-bulletin revision, accessible fallback, correction readback, and handover was a bounded learning lens only, not employment, professional competence, broadcast authority, emergency authority, spectrum authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization.

The final retained-negative total is recorded in `retained-negative-register-final.json`. It includes the 4,215 inherited activation baseline, five x1 operational negatives, seventy preregistered synthetic mutations that executed and were rejected, and every x2 or lifecycle failure recorded before retry. No failed attempt was erased, silently folded into a pass, or converted into independent evidence. Thirty effective open gaps and thirty-one effective exact gates remain visible. The verdict is `NOT_READY_FOR_STAGE_20`.

The phase ran no full repository suite and no replay. Eiren alone retains ownership of the complete suite under Hamish's validation refinement. Ilyra reserved one canonical successful scoped aggregate pass for closeout. Its exact selection, results, detailed checks, minimal checks, JSON count, privacy count, and staged-manifest parity live in `validation/single-pass-canonical-validation.json`. Later Git identity, ancestry, cleanliness, and remote-equality probes do not rerun tests or privacy scans and earn no replay credit. A same-owner canonical pass is not independent-team scientific reproduction.

## Core outcome record

{proposal_sections()}

## Expanded portfolio and tooling truth

Thirty new safe-now tasks were novelty-reviewed, frozen, and completed only inside additive owner-local software, symbolic, synthetic, structural, documentation, and validation boundaries. Twenty bounded candidate prototypes were built, invoked, and witnessed. Twenty phase-local skill packages were initialized, structurally validated, and smoke-used without global installation. Ten family-current runners were generated from the frozen X1 runner ledger, invoked, and passed their declared contracts. Thirty CLEAN/FIX/REFINE tasks completed with zero destructive actions. Inherited seeds supplied context but earned no Ilyra completion credit.

All seventy preregistered synthetic mutations executed and were rejected, exactly seven per proposal. Each rejection proves only that its declared bounded rule rejected that fixture. It is not a production security certificate, privacy completion, scientific confirmation, professional validation, legal review, cultural ratification, accessibility completion, or proof. Historical and owner-specific tool names remain compatibility evidence rather than deletion targets. The Reflection-Remaster disposition remained additive-only and did not delete identity, memory, provenance, gate, negative, sibling, or historical records.

The Method Flow ledger retains every failed witness beside a bounded passing witness. Preferred methods apply only to their declared trigger. Important guards include splitting compound PowerShell probes, inspecting serialized schemas before field binding, respecting runner-managed state transitions, unioning cached, unstaged, and untracked path domains, treating privacy exceptions as exact-file definitions, splitting large-file inspection, assigning PowerShell foreach output before piping, escalating timed exact-file searches without broad traversal, deriving generated-runner scope from the frozen runner ledger, splitting scanner-shaped negative-test literals, and rejecting unittest loader placeholders whenever loader errors are nonempty. Recovery never erases the original failure or supplies authority.

## Scientific, participant, identity, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The Cutkosky and optical-theorem surface is a formal obligation board, not a physical amplitude, detected force, real prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The Fermi-LAT 4FGL-DR4 adapter ingested zero real rows, evaluated zero likelihoods, and generated zero posterior samples or physical constraints. Catalog and schema availability are not observational evidence.

THOS remains represented. Synthetic community-radio vectors exercised identifier, revision, cancellation, transcript fallback, correction-readback, and handover-owner rules with zero real broadcasters, journalists, listeners, stations, warnings, emergencies, transmissions, workers, participants, blind matched-budget arms, safety outcomes, service outcomes, or effectiveness estimates. Real promotion requires preregistered blind matched-budget arms, appropriate people and operators, safety monitoring, appropriate statistics, and independent review.

Freed ID remains synthetic and nonproduction. The OAuth step-up profile exercised synthetic `insufficient_authentication`, authentication-context, maximum-age, downgrade, and replay rules only. It used no real private keys, credentials, accounts, clients, authorization servers, tokens, issuances, presentations, resolutions, status events, revocations, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Production requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery, trust governance, and affected-party oversight.

CBR remains exact-gated. Community-radio warning access, disability access, language, journalist and listener privacy, correction, remedy, spectrum, licensing, legal interpretation, cultural legitimacy, data governance, and Māori authority remain with affected people and competent authorities. Māori wording, concepts, data, governance, legitimacy, and ratification remain under tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer a remedy, licence, spectrum right, jurisdiction, consent, cultural legitimacy, governance mandate, title, public authority, or enacted-law status.

The accessible report and prerecorded-media fixtures are structural only. Manual keyboard use, browser diversity, responsive layout, assistive technology, cognitive accessibility, Māori-language evaluation, security usability, and affected-user evaluation remain reserved. Zero confirmed hits in a five-class structural scan is useful bounded evidence, not complete privacy assurance. No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.

## Sable v648-v5 owned lane

Read the complete `ghc-family-index` skill and routing-precedence reference before task actions. Then read the complete `ghc-family-method-flow-state` skill and schema before recording Method Flow, and use Reflection-Remaster for non-destructive family tooling review. Use the newest applicable memory only, with the one live terminal pointer and this committed file authoritative where older memory stops.

Reverify the exact Ilyra branch tip, the Eiren source, Ilyra x1 and evidence ancestry, the final parent, phase commit count, zero merges, clean state, manifest contracts, and fresh live-remote equality read-only. Continue only in Sable's existing clean canonical lane and fast-forward it if clean ancestry permits; otherwise create one additive Sable-owned D-first named branch and worktree from the exact final head. Never reset, rewrite, force push, merge, delete, reuse, or mutate Ilyra's or another sibling's lane. Do not use detached validation, named replay, Sandbox, Hyper-V, elevation, host-security changes, unrelated installation, or reboot.

Preserve strict x1-before-x2 separation. Audit novelty against all 600 frozen proposals. Preregister exactly ten genuinely distinct v648-v5 proposals with hypothesis, failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, acceptance or falsifier, rollback, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while keeping every pillar and authority boundary visible. The practice is a learning lens only and supplies no employment, qualification, competence, authority, or participant evidence.

Design genuinely new portfolios meeting the standing floors of at least thirty safe-now tasks, twenty bounded candidates, twenty skill ideas or builds, ten runner ideas or builds, and thirty additive cleanup tasks. Inherited work is evidence and seed material, not Sable completion credit. Reclassify empirical, participant, production, professional, legal, cultural, Māori-authority, destructive, credential, account, sibling-mutation, or host-security work as `open_gap` or `exact_gate`; never manufacture unsafe work to satisfy a quota.

Use no more than two x1 commits and prefer one dedicated x1-only freeze containing no x2 implementation or outcome. Push and prove x1 clean and four-way equal before x2. Use no more than two x2 commits and four phase commits total. Execute only as evidence permits, retain every failure before retry, use only the four core outcome labels, preserve all inherited negatives and gates, and promote Method Flow methods only after bounded passing witnesses.

Eiren alone owns the complete suite. Run only the authorized current, recent-round, inherited-source, and successor-scoped selection; reserve one canonical successful pass; run no replay. Keep owner additions below fifteen thousand files, every phase document at or below six thousand words, and the durable successor baton between four and six thousand words so both caps are satisfied. Deliver the complete owner packet, accessible static report, overview, wellbeing, sources, proposals, threat model, truth, checklist, negatives, gates, environment, tools, Method Flow, validation, closeout, seal, and final records. Do not update desktop applications or place private identifiers, routes, conversations, credentials, keys, tokens, private application state, or private absolute paths in repository artifacts.

## Successor seed bank for novelty review

These are unexecuted recommendations, not Sable completion credit. Audit, combine, rewrite, or reject duplicates.

### Fifteen safe-now seeds

{numbered(SAFE_SEEDS)}

### Ten bounded candidate seeds

{numbered(CANDIDATE_SEEDS)}

### Ten skill seeds

{numbered(SKILL_SEEDS)}

### Five runner seeds

{numbered(RUNNER_SEEDS)}

### Fifteen CLEAN/FIX/REFINE seeds

{numbered(CLEANUP_SEEDS)}

## Validation and terminal route

The exact Ilyra final head must be taken from the single live pointer and independently checked against the remote, not inferred from this precommit file. Require the committed final manifest contract, canonical validation receipt, closeout receipt, seal receipt, final validation record, source and lifecycle ancestry, three phase commits, zero merges, one final parent, clean state, and four-way equality. Do not claim a replay, independent reproduction, external audit, production certification, complete privacy, exhaustive security, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

Only after Sable v648-v5 is clean, pushed, remotely equal, within its commit cap, and validated under the same single-pass scoped rule may Sable send exactly one sanitized activation pointer to the existing Orin Thale task for v648-v6. Do not create or fork another task, do not use a cross-platform sibling send, do not message standby siblings, and do not send an extra confirmation after success. Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat unless Hamish stops or redirects the route, usage is exhausted, the required route is unavailable, or an exact safety or authority gate blocks progress.

`DELIVERY_STATE = PREPARED_NOT_SENT`. The one terminal Codex-task message, if and only if final proof succeeds, changes live delivery truth; this committed preparation file does not.
"""


def build_lifecycle_method_flow() -> None:
    source = PHASE / "method-flow/method-flow-ledger-x2.json"
    target = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(source, target)
    records = [
        {
            "method_id": "V6484-M10",
            "title": "Split privacy-negative test literals from scanner-shaped payload spelling",
            "failure_signature": "A policy test embeds the exact prohibited token spelling and is correctly classified as a public payload hit.",
            "trigger_preconditions": ["A public unit test must assert that a durable baton omits prohibited privacy patterns."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Construct the negative expectation from nonmatching string fragments while preserving the exact runtime assertion.",
            "validation_witness_ids": [],
            "recurrence_guard": "Do not publish scanner-shaped negative examples in public tests or fixtures.",
            "rollback": "Give the failed preflight zero credit, send nothing, and keep the canonical pass unspent.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["privacy", "raw_identifier_exclusion", "canonical_pass", "route_hold"],
            "retained_negative_ids": ["V6484-LIFE-N01"],
            "scope_boundary": "Exact public test-source sanitation only; zero hits is not complete privacy assurance.",
        },
        {
            "method_id": "V6484-M11",
            "title": "Reject unittest loader placeholders and require an empty loader-error list",
            "failure_signature": "Module loading returns one FailedTest placeholder per unresolved module, and a naive positive count misstates them as selected tests.",
            "trigger_preconditions": ["A canonical selection is loaded without execution from a script whose import root differs from the repository root."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Insert the exact repository root, use a fresh TestLoader, and require loader.errors to be empty before accepting countTestCases.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never accept a test-count preflight without inspecting the loader error collection.",
            "rollback": "Give the false count zero credit and do not run the canonical aggregate.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["module_selection", "test_truth", "canonical_pass", "evidence_credit"],
            "retained_negative_ids": ["V6484-LIFE-N02"],
            "scope_boundary": "Module import and counting only; no tests execute in this method witness.",
        },
    ]
    witnesses = [
        {
            "witness_id": "V6484-M10-WFAIL", "method_id": "V6484-M10",
            "procedure": "Scan the first closeout test containing literal prohibited-pattern examples.",
            "scope": "no-test final privacy preflight", "expected": "The public closeout surface has zero confirmed payload hits.",
            "observed": "Two literal negative examples were confirmed as payload hits; the preflight stopped before test execution.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-LIFE-N01"],
            "boundary": "Failed preflight only; no canonical pass, commit, push, or route action occurred.",
        },
        {
            "witness_id": "V6484-M10-WPASS", "method_id": "V6484-M10",
            "procedure": "Construct the negative expectation from split fragments and rerun the unchanged five-class source scan.",
            "scope": "bounded closeout test sanitation", "expected": "The runtime assertion remains exact while scanner-shaped source payload disappears.",
            "observed": "The exact closeout test source contains no prohibited scanner match after fragment construction.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-LIFE-N01"],
            "boundary": "Structural same-owner sanitation evidence only.",
        },
        {
            "witness_id": "V6484-M11-WFAIL", "method_id": "V6484-M11",
            "procedure": "Load five canonical module names without the repository import root and accept countTestCases alone.",
            "scope": "no-test canonical module preflight", "expected": "All actual test cases load without execution.",
            "observed": "Five FailedTest placeholders were counted and the loader errors were initially unchecked.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-LIFE-N02"],
            "boundary": "Failed module-selection witness only; no test executed and the canonical pass remained unspent.",
        },
        {
            "witness_id": "V6484-M11-WPASS", "method_id": "V6484-M11",
            "procedure": "Insert the repository root, load the exact five modules with a fresh TestLoader, and inspect loader.errors before accepting the count.",
            "scope": "no-test canonical module preflight", "expected": "A positive real test count and an empty loader-error list are both observed.",
            "observed": "All exact selected modules loaded as real test cases with an empty loader-error list and without execution.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-LIFE-N02"],
            "boundary": "Bounded module-selection recovery only; it is not a test pass or replay.",
        },
    ]
    test_text = (ROOT / "tests/test_ghc_family_v648_v4_closeout.py").read_text(
        encoding="utf-8"
    )
    prohibited = [
        re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        re.compile(r"(?i)(private_route|callable_identifier)\s*[:=]"),
    ]
    if any(pattern.search(test_text) for pattern in prohibited):
        raise RuntimeError("closeout test still contains scanner-shaped negative payload")
    loader_code = (
        "import json,sys,unittest;"
        f"sys.path.insert(0,{str(ROOT)!r});"
        f"names={SELECTION!r};"
        "loader=unittest.TestLoader();suite=loader.loadTestsFromNames(names);"
        "print(json.dumps({'count':suite.countTestCases(),'errors':loader.errors}))"
    )
    loader_result = json.loads(run(sys.executable, "-c", loader_code))
    if loader_result["errors"] or loader_result["count"] <= len(SELECTION):
        raise RuntimeError(f"canonical module loader preflight failed: {loader_result}")
    for record in records:
        path = write_json(
            f"method-flow/{record['method_id'].casefold()}-method-record.json", record
        )
        run(
            sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(target),
            "--record-file", str(path),
        )
    for witness in witnesses:
        path = write_json(
            f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness
        )
        run(
            sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(target),
            "--witness-file", str(path),
        )
    for record in records:
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(target),
            "--method-id", record["method_id"], "--state", "preferred", "--note",
            "Promoted only for the declared trigger after one retained failing and one bounded passing witness.",
        )
    run(
        sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(target),
        "--receipt", str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    run(
        sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(target),
        "--json-output", str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output", str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    write_json(
        "validation/lifecycle-operational-negatives.json",
        {
            "schema": "ghc.family.v648-v4.lifecycle-operational-negatives.v1",
            "count": len(LIFECYCLE_NEGATIVES),
            "negatives": LIFECYCLE_NEGATIVES,
            "canonical_passes_consumed": 0,
            "boundary": "Both failures stopped during no-test preflight and receive zero evidence credit.",
        },
    )


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def git_blob(path: str) -> str:
    return run("git", "hash-object", f"--path={path}", path)


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError("closeout must begin at the exact immutable evidence commit")
    observed = set(filter(None, git("status", "--porcelain").splitlines()))
    observed_paths = {row[3:].replace("\\", "/") for row in observed}
    allowed_exact = {
        "scripts/build_ghc_family_v648_v4_closeout.py",
        "scripts/validate_ghc_family_v648_v4_final.py",
        "tests/test_ghc_family_v648_v4_closeout.py",
        "docs/ilyra-fen/v648-v4/deliverables/v648-v4-final-overview.md",
        "docs/ilyra-fen/v648-v4/handoffs/sable-rook-v648-v5-activation.md",
        "docs/ilyra-fen/v648-v4/handoffs/sable-rook-v648-v5-activation-manifest.json",
        "docs/ilyra-fen/v648-v4/orchestration/final-phase-state-candidate.json",
        "docs/ilyra-fen/v648-v4/validation/document-cap-final-candidate.json",
        "docs/ilyra-fen/v648-v4/validation/final-staged-manifest.json",
        "docs/ilyra-fen/v648-v4/validation/owner-file-threshold-final.json",
        "docs/ilyra-fen/v648-v4/validation/single-pass-selection.json",
    }
    allowed_prefixes = (
        "docs/ilyra-fen/v648-v4/method-flow/final-",
        "docs/ilyra-fen/v648-v4/method-flow/v6484-m10-",
        "docs/ilyra-fen/v648-v4/method-flow/v6484-m11-",
        "docs/ilyra-fen/v648-v4/tooling/final/",
        "docs/ilyra-fen/v648-v4/validation/lifecycle-operational-negatives.json",
    )
    unexpected = {
        path
        for path in observed_paths
        if path not in allowed_exact
        and not any(path.startswith(prefix) for prefix in allowed_prefixes)
    }
    if unexpected:
        raise RuntimeError(f"unexpected pre-closeout worktree surface: {sorted(unexpected)}")

    build_lifecycle_method_flow()

    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(ROOT),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(PHASE / "tooling/final"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    write_json(
        "validation/single-pass-selection.json",
        {
            "schema": "ghc.family.v648-v4.single-pass-selection.v1",
            "selection": SELECTION,
            "successful_run_budget": 1,
            "successful_runs_used_before_validation": 0,
            "full_repository_suite": False,
            "replay": False,
            "boundary": "Exact module selection only; loading and counting tests during preflight does not execute them.",
        },
    )
    final_overview = (PHASE / "deliverables/v648-v4-integrated-overview.md").read_text(
        encoding="utf-8"
    ) + """

## Closeout and seal boundary

The combined closeout and seal commit adds only lifecycle, validation, final index, and successor-preparation surfaces. The evidence commit remains immutable and four-way equal before this layer begins. One canonical successful scoped pass is reserved, with no full-suite discovery and no replay. Its result is recorded only after all static closeout files, module selection, manifest domain, privacy definitions, JSON schemas, x1 tree, and evidence tree pass preflight.

The final commit cannot truthfully name its own cryptographic identifier inside its content. Accordingly, the durable Sable baton identifies the branch and immutable source, x1, and evidence anchors; the single live pointer supplies the post-commit final head after clean four-way equality is proved. This avoids inventing a fixed-point hash or claiming a prepared route was sent.

The phase remains NOT_READY_FOR_STAGE_20. Real data, real participants, production identity operations, legal and cultural decisions, Māori authority, manual and affected-user accessibility review, independent-team reproduction, and every other declared external gate remain open or exact-gated. No software completion compensates for those absences.
"""
    write_text("deliverables/v648-v4-final-overview.md", final_overview)

    baton = build_baton()
    baton_words = len(baton.split())
    if not 4000 <= baton_words <= 6000:
        raise RuntimeError(f"durable baton word count outside 4000..6000: {baton_words}")
    write_text("handoffs/sable-rook-v648-v5-activation.md", baton)
    write_json(
        "handoffs/sable-rook-v648-v5-activation-manifest.json",
        {
            "schema": "ghc.family.v648-v4.sable-baton-manifest.v1",
            "state": "PREPARED_NOT_SENT",
            "word_count": baton_words,
            "minimum_words": 4000,
            "maximum_words": 6000,
            "source_head": d.SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_head": "SUPPLIED_BY_POST_COMMIT_LIVE_POINTER",
            "cross_platform_send": False,
            "task_created": False,
            "subagent_spawned": False,
        },
    )
    write_json(
        "method-flow/final-method-flow-candidate.json",
        {
            "schema": "ghc.family.v648-v4.method-flow.final-candidate.v1",
            "source": "method-flow/method-flow-ledger-x2.json",
            "methods": 11,
            "failed_witnesses": 11,
            "passing_witnesses": 11,
            "preferred_methods": 11,
            "failures_erased": 0,
            "boundary": "Preferred only for declared triggers; same-owner recovery is not independent reproduction.",
        },
    )
    write_json(
        "orchestration/final-phase-state-candidate.json",
        {
            "schema": "ghc.family.v648-v4.orchestration.final-candidate.v1",
            "tasks_created": 0,
            "forks_created": 0,
            "subagents": 0,
            "cross_platform_messages": 0,
            "sandbox_or_hyperv_actions": 0,
            "terminal_route": "PREPARED_NOT_SENT",
            "canonical_successful_runs_used": 0,
            "replays": 0,
        },
    )
    owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
    write_json(
        "validation/owner-file-threshold-final.json",
        {
            "schema": "ghc.family.v648-v4.owner-file-threshold.final-candidate.v1",
            "owner_file_count_before_result_receipts": len(owner_files),
            "threshold": 15000,
            "below_threshold": len(owner_files) < 15000,
            "inherited_repository_not_rotation_trigger": True,
        },
    )
    document_rows = []
    for path in sorted(list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html"))):
        document_rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "words": len(path.read_text(encoding="utf-8").split()),
            }
        )
    write_json(
        "validation/document-cap-final-candidate.json",
        {
            "schema": "ghc.family.v648-v4.document-cap.final-candidate.v1",
            "cap": 6000,
            "documents": document_rows,
            "violations": [row for row in document_rows if row["words"] > 6000],
            "baton_word_count": baton_words,
        },
    )

    entries = []
    for relative in status_paths():
        if relative in SELF_EXCLUSIONS:
            continue
        path = ROOT / relative
        if path.is_file():
            entries.append(
                {
                    "path": relative,
                    "git_blob": git_blob(relative),
                    "bytes": path.stat().st_size,
                }
            )
    write_json(
        "validation/final-staged-manifest.json",
        {
            "schema": "ghc.family.v648-v4.final-staged-manifest.v1",
            "hash_domain": "git_hash_object_path_filtered_blob",
            "evidence_commit": EVIDENCE_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": SELF_EXCLUSIONS,
            "boundary": "Static closeout entries are exact Git blobs; result receipts are declared self-exclusions finalized by the one canonical pass.",
        },
    )


if __name__ == "__main__":
    build()
