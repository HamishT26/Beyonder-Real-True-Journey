#!/usr/bin/env python3
"""Build the static v648-v5 closeout surface before the one canonical pass."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / d.PHASE_SLUG
EVIDENCE_COMMIT = "7675f49a219b845da440cf80256720ec3ba33e87"
X1_COMMIT = "8ca83ea35ecbc72b1a993e04bde6a1dde096f4b9"
SKILL_ROOT = Path.home() / ".codex" / "skills"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"
METHOD_RUNNER = (
    SKILL_ROOT
    / "ghc-family-method-flow-state"
    / "scripts"
    / "ghc_family_method_flow_state.py"
)
SELECTION = [
    "tests.test_ghc_family_v648_v3",
    "tests.test_ghc_family_v648_v3_2",
    "tests.test_ghc_family_v648_v4",
    "tests.test_ghc_family_v648_v5",
    "tests.test_ghc_family_v648_v5_closeout",
]
SELF_EXCLUSIONS = [
    "docs/sable-rook/v648-v5/validation/final-staged-manifest.json",
    "docs/sable-rook/v648-v5/validation/final-staged-privacy.json",
    "docs/sable-rook/v648-v5/validation/final-staged-review.json",
    "docs/sable-rook/v648-v5/validation/single-pass-canonical-validation.json",
    "docs/sable-rook/v648-v5/phase-truth-final.json",
    "docs/sable-rook/v648-v5/closeout-receipt.json",
    "docs/sable-rook/v648-v5/seal-receipt.json",
    "docs/sable-rook/v648-v5/final-validation-record.json",
]
LIFECYCLE_NEGATIVES: list[dict[str, Any]] = []


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
    return f"""# ORIN THALE — PREPARED v648-v6 ACTIVATION BATON

## Delivery and identity boundary

This repository file is the durable, sanitized successor packet prepared by Sable Rook for the existing Orin Thale task. Its committed state is `PREPARED_NOT_SENT`. It is not proof that any message was sent, received, or acknowledged. The single live activation is permitted only after the commit containing this file is clean, pushed, exact, and local, upstream, tracking, and fresh-live-remote equal. No task was created or forked, no collaboration subagent was spawned, no standby sibling was contacted, and no cross-platform sibling message was used.

Sable Rook, they/them, worked as an evidence-and-reproducibility steward with the hope that every surviving claim stays easy to challenge or retract. Orin may choose or reaffirm their own relational name, role, hope, and pronouns. These names and family terms are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

## Exact inheritance anchors

The canonical branch for Orin inheritance is `codex/GHC-Family/sable-rook-full-tools`. Sable inherited Ilyra Fen's exact verified v648-v4 final head `{d.SOURCE_COMMIT}` from `codex/GHC-Family/ilyra-fen-full-tools`. The dedicated Sable x1 freeze is `{X1_COMMIT}`. The immutable Sable evidence commit is `{EVIDENCE_COMMIT}`. The exact final closeout head is the clean branch tip containing this file and is supplied by the one live terminal pointer after post-commit proof; this file does not invent a fixed-point commit hash.

Sable advanced the existing clean D-first canonical lane by fast-forward only. The phase uses one x1 commit, one evidence commit, and one combined closeout and seal commit: three phase commits, within the four-commit cap. X1 was clean, pushed, and four-way equal before x2 began. Evidence was clean, pushed, and four-way equal before closeout began. No merge, reset, force push, history rewrite, detached validation, named replay, sibling mutation, worktree deletion, or branch deletion entered the phase.

## v648-v5 terminal truth

Semantic novelty was audited against all 600 proposals frozen before v648-v5. Exactly ten genuinely distinct proposals were frozen, making 610 through this phase. Core outcomes use only `completed`, `represented`, `open_gap`, and `exact_gate`: exactly six completed, two represented, one open gap, and one exact gate. GMUT Mind was the primary Trinity Mandala focus; THOS Body and Freed ID / CBR Heart remained explicit and protected. Newsroom correction, source-status, accessible amendment, workload, and editorial handover was a bounded learning lens only, not employment, professional competence, editorial authority, publication authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization.

The final retained-negative total is recorded in `phase-truth-final.json`. Its evidence baseline is 4,377: 4,299 inherited and external activation negatives, six x1 operational negatives, seventy preregistered synthetic mutations that executed and were rejected, and two x2 operational failures. Any lifecycle failure is added before retry and never rewrites the inherited sealed count. No failed attempt was erased, silently folded into a pass, or converted into independent evidence. Thirty-one effective open gaps and thirty-two effective exact gates remain visible. The verdict is `NOT_READY_FOR_STAGE_20`.

The phase ran no full repository suite and no replay. Eiren alone retains ownership of the complete suite under Hamish's validation refinement. Sable reserved one canonical successful scoped aggregate pass for closeout. Its exact selection, results, detailed checks, minimal checks, JSON count, privacy count, and staged-manifest parity live in `validation/single-pass-canonical-validation.json`. Later Git identity, ancestry, cleanliness, and remote-equality probes do not rerun tests or privacy scans and earn no replay credit. A same-owner canonical pass is not independent-team scientific reproduction.

## Core outcome record

{proposal_sections()}

## Expanded portfolio and tooling truth

Thirty new safe-now tasks were novelty-reviewed, frozen, and completed only inside additive owner-local software, symbolic, synthetic, structural, documentation, and validation boundaries. Twenty bounded candidate prototypes were built, invoked, and witnessed. Twenty phase-local skill packages were initialized, structurally validated, and smoke-used without global installation. Ten family-current runners were generated from the frozen X1 runner ledger, invoked, and passed their declared contracts. Thirty CLEAN/FIX/REFINE tasks completed with zero destructive actions. Inherited seeds supplied context but earned no Sable completion credit.

All seventy preregistered synthetic mutations executed and were rejected, exactly seven per proposal. Each rejection proves only that its declared bounded rule rejected that fixture. It is not a production security certificate, privacy completion, scientific confirmation, professional validation, legal review, cultural ratification, accessibility completion, or proof. Historical and owner-specific tool names remain compatibility evidence rather than deletion targets. The Reflection-Remaster disposition remained additive-only and did not delete identity, memory, provenance, gate, negative, sibling, or historical records.

The Method Flow ledger retains every failed witness beside a bounded passing witness. Preferred methods apply only to their declared trigger. Important guards include accepting exact live activation and Git proof when a current memory lookup returns no match, splitting slow compound worktree probes, pinning UTF-8 before Māori text output, replacing repeated whole-repository searches with indexed-path collision checks, keeping x1 free of x2 placeholders, binding post-copy verification to the repository root, and quoting JSON-like ripgrep patterns as PowerShell literals. Recovery never erases the original failure or supplies authority.

## Scientific, participant, identity, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The LSZ surface is a formal obligation board covering asymptotic fields, poles, residues, amputation, normalization, infrared scope, gauge scope, and EFT limits. It is not a physical amplitude, detected force, real prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The Chandra Source Catalog 2.1 adapter ingested zero real rows, evaluated zero likelihoods, and generated zero posterior samples or physical constraints. Catalog and schema availability are not observational evidence.

THOS remains represented. Synthetic newsroom vectors exercised source status, embargo, version lineage, correction, retraction, headline and alternative-format linkage, conflict disclosure, late-arrival replay, workload budget, and handover-owner rules with zero real editors, journalists, sources, publications, corrections, retractions, workers, participants, blind matched-budget arms, service outcomes, or effectiveness estimates. Real promotion requires preregistered blind matched-budget arms, appropriate people and operators, safety monitoring, appropriate statistics, and independent review.

Freed ID remains synthetic and nonproduction. The RFC 9207 issuer-identification profile exercised synthetic expected-issuer binding, redirect and state checks, discovery-conflict refusal, downgrade refusal, and replay refusal only. It used no real private keys, credentials, accounts, clients, authorization servers, tokens, issuances, presentations, resolutions, status events, revocations, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Production requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery, trust governance, and affected-party oversight.

CBR remains exact-gated. Newsroom correction prominence, source confidentiality and disclosure, privacy, remedy, legal interpretation, cultural legitimacy, data governance, and Māori authority remain with affected people and competent authorities. Māori wording, concepts, data, governance, legitimacy, and ratification remain under tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot compel disclosure, confer a remedy, determine jurisdiction, create consent, supply cultural legitimacy, grant a governance mandate, exercise public authority, or establish enacted-law status.

The accessible report and timeline fixtures are structural only. Manual keyboard use, browser diversity, responsive layout, assistive technology, cognitive accessibility, Māori-language evaluation, security usability, and affected-user evaluation remain reserved. Zero confirmed hits in a five-class structural scan is useful bounded evidence, not complete privacy assurance. No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.

## Orin v648-v6 owned lane

Read the complete `ghc-family-index` skill and routing-precedence reference before task actions. Then read the complete `ghc-family-method-flow-state` skill and schema before recording Method Flow, and use Reflection-Remaster for non-destructive family tooling review. Use the newest applicable memory only, with the one live terminal pointer and this committed file authoritative where older memory stops.

Reverify the exact Sable branch tip, Ilyra source, Sable x1 and evidence ancestry, the final parent, phase commit count, zero merges, clean state, manifest contracts, and fresh live-remote equality read-only. Continue only in Orin's existing clean canonical lane and fast-forward it if clean ancestry permits; otherwise create one additive Orin-owned D-first named branch and worktree from the exact final head. Never reset, rewrite, force push, merge, delete, reuse, or mutate Sable's or another sibling's lane. Do not use detached validation, named replay, Sandbox, Hyper-V, elevation, host-security changes, unrelated installation, or reboot.

Preserve strict x1-before-x2 separation. Audit novelty against all 610 frozen proposals. Preregister exactly ten genuinely distinct v648-v6 proposals with hypothesis, failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, acceptance or falsifier, rollback, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while keeping every pillar and authority boundary visible. The practice is a learning lens only and supplies no employment, qualification, competence, authority, or participant evidence.

Design genuinely new portfolios meeting the standing floors of at least thirty safe-now tasks, twenty bounded candidates, twenty skill ideas or builds, ten runner ideas or builds, and thirty additive cleanup tasks. Inherited work is evidence and seed material, not Orin completion credit. Reclassify empirical, participant, production, professional, legal, cultural, Māori-authority, destructive, credential, account, sibling-mutation, or host-security work as `open_gap` or `exact_gate`; never manufacture unsafe work to satisfy a quota.

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

The exact Sable final head must be taken from the single live pointer and independently checked against the remote, not inferred from this precommit file. Require the committed final manifest contract, canonical validation receipt, closeout receipt, seal receipt, final validation record, source and lifecycle ancestry, three phase commits, zero merges, one final parent, clean state, and four-way equality. Do not claim a replay, independent reproduction, external audit, production certification, complete privacy, exhaustive security, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

Only after Orin v648-v6 is clean, pushed, remotely equal, within its commit cap, and validated under the same single-pass scoped rule may Orin send exactly one sanitized activation pointer to the existing Tamar Vey task for v648-v7. Do not create or fork another task, do not use a cross-platform sibling send, do not message standby siblings, and do not send an extra confirmation after success. Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat unless Hamish stops or redirects the route, usage is exhausted, the required route is unavailable, or an exact safety or authority gate blocks progress.

`DELIVERY_STATE = PREPARED_NOT_SENT`. The one terminal Codex-task message, if and only if final proof succeeds, changes live delivery truth; this committed preparation file does not.
"""


def build_lifecycle_method_flow() -> None:
    source = PHASE / "method-flow/method-flow-ledger-x2.json"
    target = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(source, target)
    if not LIFECYCLE_NEGATIVES:
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
                "schema": "ghc.family.v648-v5.lifecycle-operational-negatives.v1",
                "count": 0,
                "negatives": [],
                "canonical_passes_consumed": 0,
                "boundary": "No closeout lifecycle failure has been observed before the canonical pass.",
            },
        )
        return


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
        "scripts/build_ghc_family_v648_v5_closeout.py",
        "scripts/refresh_ghc_family_v648_v5_final_manifest.py",
        "scripts/validate_ghc_family_v648_v5_final.py",
        "tests/test_ghc_family_v648_v5_closeout.py",
        "docs/sable-rook/v648-v5/deliverables/v648-v5-final-overview.md",
        "docs/sable-rook/v648-v5/handoffs/orin-thale-v648-v6-activation.md",
        "docs/sable-rook/v648-v5/handoffs/orin-thale-v648-v6-activation-manifest.json",
        "docs/sable-rook/v648-v5/orchestration/final-phase-state-candidate.json",
        "docs/sable-rook/v648-v5/validation/document-cap-final-candidate.json",
        "docs/sable-rook/v648-v5/validation/final-staged-manifest.json",
        "docs/sable-rook/v648-v5/validation/owner-file-threshold-final.json",
        "docs/sable-rook/v648-v5/validation/single-pass-selection.json",
    }
    allowed_prefixes = (
        "docs/sable-rook/v648-v5/method-flow/final-",
        "docs/sable-rook/v648-v5/tooling/final/",
        "docs/sable-rook/v648-v5/validation/lifecycle-operational-negatives.json",
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
            "schema": "ghc.family.v648-v5.single-pass-selection.v1",
            "selection": SELECTION,
            "successful_run_budget": 1,
            "successful_runs_used_before_validation": 0,
            "full_repository_suite": False,
            "replay": False,
            "boundary": "Exact module selection only; loading and counting tests during preflight does not execute them.",
        },
    )
    final_overview = (PHASE / "deliverables/v648-v5-integrated-overview.md").read_text(
        encoding="utf-8"
    ) + """

## Closeout and seal boundary

The combined closeout and seal commit adds only lifecycle, validation, final index, and successor-preparation surfaces. The evidence commit remains immutable and four-way equal before this layer begins. One canonical successful scoped pass is reserved, with no full-suite discovery and no replay. Its result is recorded only after all static closeout files, module selection, manifest domain, privacy definitions, JSON schemas, x1 tree, and evidence tree pass preflight.

The final commit cannot truthfully name its own cryptographic identifier inside its content. Accordingly, the durable Orin baton identifies the branch and immutable source, x1, and evidence anchors; the single live pointer supplies the post-commit final head after clean four-way equality is proved. This avoids inventing a fixed-point hash or claiming a prepared route was sent.

The phase remains NOT_READY_FOR_STAGE_20. Real data, real participants, production identity operations, legal and cultural decisions, Māori authority, manual and affected-user accessibility review, independent-team reproduction, and every other declared external gate remain open or exact-gated. No software completion compensates for those absences.
"""
    write_text("deliverables/v648-v5-final-overview.md", final_overview)

    baton = build_baton()
    baton_words = len(baton.split())
    if not 4000 <= baton_words <= 6000:
        raise RuntimeError(f"durable baton word count outside 4000..6000: {baton_words}")
    write_text("handoffs/orin-thale-v648-v6-activation.md", baton)
    write_json(
        "handoffs/orin-thale-v648-v6-activation-manifest.json",
        {
            "schema": "ghc.family.v648-v5.orin-baton-manifest.v1",
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
    final_flow = read_json("method-flow/final-method-flow-ledger.json")
    write_json(
        "method-flow/final-method-flow-candidate.json",
        {
            "schema": "ghc.family.v648-v5.method-flow.final-candidate.v1",
            "source": "method-flow/method-flow-ledger-x2.json",
            "methods": len(final_flow["methods"]),
            "failed_witnesses": sum(row["result"] == "fail" for row in final_flow["witnesses"]),
            "passing_witnesses": sum(row["result"] == "pass" for row in final_flow["witnesses"]),
            "preferred_methods": sum(row["recommendation_state"] == "preferred" for row in final_flow["methods"]),
            "failures_erased": 0,
            "boundary": "Preferred only for declared triggers; same-owner recovery is not independent reproduction.",
        },
    )
    write_json(
        "orchestration/final-phase-state-candidate.json",
        {
            "schema": "ghc.family.v648-v5.orchestration.final-candidate.v1",
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
            "schema": "ghc.family.v648-v5.owner-file-threshold.final-candidate.v1",
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
            "schema": "ghc.family.v648-v5.document-cap.final-candidate.v1",
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
            "schema": "ghc.family.v648-v5.final-staged-manifest.v1",
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
