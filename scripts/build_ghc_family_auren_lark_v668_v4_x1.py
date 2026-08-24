#!/usr/bin/env python3
"""Build the dedicated planning-only Auren Lark v668-v4 x1 freeze."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ghc_family_auren_lark_v668_v4_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INITIAL_X1_HEAD,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PRONOUNS,
    PROPOSAL_BLUEPRINTS,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_ANCESTOR,
    SOURCE_BATON_SHA256,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_COMPOSITE_RECEIPT_SHA256,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SOURCE_X1,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    X1_OVERLAY,
    assert_source_and_x1_only,
    manifest_rows,
    phase_owner_files,
    portfolio_rows,
    proposal_rows,
    utc_now,
    visible_proposal_inventory,
    word_count,
    write_json,
    write_text,
)


STARTUP_FAILURES = [
    {
        "method_id": "AL6684-MF-START-001",
        "negative_id": "AL6684-NEG-START-001",
        "title": "split selected skill reads before interpretation",
        "failure_signature": "a combined fifteen-skill display exceeded the rendering bound and truncated",
        "trigger": "too many complete skill files are projected into one tool response",
        "workaround": "reread each selected skill in bounded groups through EOF before using its instructions",
        "pass_observed": "all selected family-current skills and required references were read completely",
    },
    {
        "method_id": "AL6684-MF-START-002",
        "negative_id": "AL6684-NEG-START-002",
        "title": "materialize PowerShell rows before JSON piping",
        "failure_signature": "a direct foreach-to-pipeline projection raised an empty-pipe parser fault",
        "trigger": "a compound PowerShell expression pipes directly from an unparenthesized foreach block",
        "workaround": "assign the bounded foreach result to a scalar collection before ConvertTo-Json",
        "pass_observed": "all three mandatory helper skills were located and read after the corrected projection",
    },
    {
        "method_id": "AL6684-MF-START-003",
        "negative_id": "AL6684-NEG-START-003",
        "title": "discover committed manifest paths before replay",
        "failure_signature": "the first final-manifest projection guessed a nonexistent closeout directory",
        "trigger": "a predecessor stores final manifests under validation rather than a guessed closeout path",
        "workaround": "read the exact test constants and replay only the committed validation paths",
        "pass_observed": "40 x1, 244 evidence, 26 delta, and 313 owner entries replayed with zero mismatches",
    },
    {
        "method_id": "AL6684-MF-START-004",
        "negative_id": "AL6684-NEG-START-004",
        "title": "keep omitted external receipt bytes unverified",
        "failure_signature": "the conventional predecessor validation directory was absent",
        "trigger": "the repository intentionally omits the private external receipt-bank location",
        "workaround": "retain both supplied hashes as activation assertions and do not invent or broadly search a private path",
        "pass_observed": "committed validation credit explicitly confirmed that the external D-first location was omitted",
    },
    {
        "method_id": "AL6684-MF-START-005",
        "negative_id": "AL6684-NEG-START-005",
        "title": "use scalar bounds for PowerShell line windows",
        "failure_signature": "a nested range array supplied incompatible argument types to Math.Min",
        "trigger": "PowerShell unrolls a nested numeric range before a line-window loop",
        "workaround": "assign integer start and end scalars before the bounded read",
        "pass_observed": "the canonical entrypoint and receipt behavior were read through EOF",
    },
    {
        "method_id": "AL6684-MF-X1-006",
        "negative_id": "AL6684-NEG-X1-006",
        "title": "separate Git existence checks from PowerShell expressions",
        "failure_signature": "a proposal-file existence projection had a missing closing parenthesis before execution",
        "trigger": "a native Git command and semicolon are embedded inside one PowerShell parenthesized assignment",
        "workaround": "capture each native exit code in a separate statement before constructing the result row",
        "pass_observed": "the exact proposal indexes, shards, source intake, and portfolio were read successfully",
    },
    {
        "method_id": "AL6684-MF-X1-007",
        "negative_id": "AL6684-NEG-X1-007",
        "title": "fall back from unsupported ls-tree glob magic",
        "failure_signature": "this Git build rejected glob pathspec magic for ls-tree",
        "trigger": "proposal discovery assumes ls-tree accepts the same pathspec magic as other Git commands",
        "workaround": "list exact-source docs names once and filter locally before any blob read",
        "pass_observed": "only proposal indexes and shards were passed to the exact Git-blob reader",
    },
    {
        "method_id": "AL6684-MF-X1-008",
        "negative_id": "AL6684-NEG-X1-008",
        "title": "novelty quarantine before proposal freeze",
        "failure_signature": "the first candidate set produced eight neighbors at or above the 0.75 threshold",
        "trigger": "microscope controls inherit too much wording from the immediately preceding film-calibration phase",
        "workaround": "rewrite only the eight quarantined titles around slide-specific state and refusal semantics",
        "pass_observed": "the exact-source reachable retry reported zero collisions and zero quarantined neighbors",
    },
    {
        "method_id": "AL6684-MF-X1-009",
        "negative_id": "AL6684-NEG-X1-009",
        "title": "probe Git common-dir with supported scalar syntax",
        "failure_signature": "the first target gate used an unsupported absolute-path common-dir form",
        "trigger": "a Git installation does not accept the requested path-format option combination",
        "workaround": "read the supported common-dir scalar and resolve it with the platform path library",
        "pass_observed": "the exact shared Git directory was resolved without changing state",
    },
    {
        "method_id": "AL6684-MF-X1-010",
        "negative_id": "AL6684-NEG-X1-010",
        "title": "capture native exit codes before PowerShell projection",
        "failure_signature": "a pipeline wrapper misclassified a successful common-dir probe as failed",
        "trigger": "the native exit code is inspected only after a downstream PowerShell cmdlet runs",
        "workaround": "capture output and LASTEXITCODE immediately, then perform scalar projection",
        "pass_observed": "branch, remote ref, path, source head, and clean-state gates were projected correctly",
    },
    {
        "method_id": "AL6684-MF-X1-011",
        "negative_id": "AL6684-NEG-X1-011",
        "title": "inspect completed worktree state after noisy receipt serialization",
        "failure_signature": "combined native stderr objects depth-truncated the worktree-creation JSON receipt",
        "trigger": "successful Git progress text is serialized as nested PowerShell error records",
        "workaround": "never replay creation; inspect exact branch, head, sparse file, materialized count, and junction",
        "pass_observed": "one clean Auren lane existed at the source with owner-only sparse patterns and zero files",
    },
    {
        "method_id": "AL6684-MF-X1-012",
        "negative_id": "AL6684-NEG-X1-012",
        "title": "normalize worktree path separators before registration comparison",
        "failure_signature": "a backslash target compared false against Git's forward-slash worktree record",
        "trigger": "platform-native and Git-canonical path separators are compared literally",
        "workaround": "normalize the exact target to Git separators before counting registrations",
        "pass_observed": "the Auren worktree was registered exactly once",
    },
    {
        "method_id": "AL6684-MF-X1-013",
        "negative_id": "AL6684-NEG-X1-013",
        "title": "split rejected overview patches into exact hunks",
        "failure_signature": "an oversized overview patch was rejected because one context line did not match",
        "trigger": "one multi-paragraph patch mixes unrelated hunks and contains a malformed context fragment",
        "workaround": "retain the rejected patch and apply smaller exact-context hunks without force",
        "pass_observed": "identity, source, domain, Method Flow, and lifecycle paragraphs were updated by exact hunks",
    },
    {
        "method_id": "AL6684-MF-X1-014",
        "negative_id": "AL6684-NEG-X1-014",
        "title": "verify owner branch literals after mechanical seeding",
        "failure_signature": "the first x1 builder invocation stopped on a stale Ilyra owner segment in the branch literal",
        "trigger": "a version-and-module rewrite does not replace a branch owner segment outside the phase path pattern",
        "workaround": "change only the exact branch literal and rerun the x1-only builder from the unchanged source head",
        "pass_observed": "the corrected builder accepted the exact Auren branch before generating x1",
    },
    {
        "method_id": "AL6684-MF-X1-015",
        "negative_id": "AL6684-NEG-X1-015",
        "title": "apply recovery edits as one exact hunk per file",
        "failure_signature": "a combined recovery patch was rejected on a second unmatched narrative fragment",
        "trigger": "an otherwise small dependency fix is bundled with unrelated prose and test edits",
        "workaround": "retain the rejected patch and separate archive, ledger, narrative, and test hunks",
        "pass_observed": "the exact branch dependency and additive bookkeeping were corrected without force",
    },
    {
        "method_id": "AL6684-MF-X1-016",
        "negative_id": "AL6684-NEG-X1-016",
        "title": "scope lifecycle module guards to the current owner",
        "failure_signature": "the retry preflight treated inherited Ilyra x2 and final modules as current Auren material",
        "trigger": "a mechanically seeded forbidden-module substring retains the predecessor owner and phase",
        "workaround": "change only the forbidden self-module literals to Auren v668-v4",
        "pass_observed": "the lifecycle guard accepted inherited modules while still refusing any Auren x2 or final module",
    },
    {
        "method_id": "AL6684-MF-X1-017",
        "negative_id": "AL6684-NEG-X1-017",
        "title": "disable Python bytecode in claimed no-write preflights",
        "failure_signature": "the import preflight created an ignored owner-lane scripts/__pycache__ directory",
        "trigger": "Python imports run without PYTHONDONTWRITEBYTECODE in a sparse owner lane",
        "workaround": "remove only the verified owner cache and set bytecode writes off for subsequent validation",
        "pass_observed": "the exact cache was absent and later import/test commands used bytecode suppression",
    },
    {
        "method_id": "AL6684-MF-X1-018",
        "negative_id": "AL6684-NEG-X1-018",
        "title": "honor destructive-command policy during cache cleanup",
        "failure_signature": "the recursive PowerShell cache-removal command was rejected by local policy before execution",
        "trigger": "a cleanup command uses a recursively destructive surface even for a verified cache directory",
        "workaround": "enumerate two exact cache files, delete each verified file through the platform API, then remove the empty directory",
        "pass_observed": "only the two declared bytecode files and their empty owner cache directory were removed",
    },
    {
        "method_id": "AL6684-MF-X1-019",
        "negative_id": "AL6684-NEG-X1-019",
        "title": "verify split owner paths in seeded tests",
        "failure_signature": "the first isolated x1 test invocation had twenty failures from one stale Ilyra directory segment",
        "trigger": "a mechanical full-path replacement misses a path assembled from separate string components",
        "workaround": "change only the test PHASE_ROOT owner segment, refresh changed x1 ledgers, and rerun the isolated module",
        "pass_observed": "the dependency-corrected x1 module resolved the Auren phase and all scoped tests passed",
    },
    {
        "method_id": "AL6684-MF-X1-020",
        "negative_id": "AL6684-NEG-X1-020",
        "title": "shard Method Flow when retained failures exceed the document cap",
        "failure_signature": "the refreshed x1 builder stopped on a 6119-word Method Flow ledger",
        "trigger": "additive failure retention grows one complete ledger beyond the six-thousand-word ceiling",
        "workaround": "preserve every row in deterministic five-method shards and keep a compact logical index",
        "pass_observed": "all Method Flow rows remained replayable and every phase document stayed within the cap",
    },
    {
        "method_id": "AL6684-MF-X1-021",
        "negative_id": "AL6684-NEG-X1-021",
        "title": "prefer builder word gates over brittle inline projections",
        "failure_signature": "an inline Python shard-size projection had mismatched parentheses and executed nothing",
        "trigger": "a nested comprehension, set expression, and regex are compressed into one shell argument",
        "workaround": "retain the syntax failure and rely on the builder's exact per-file word gate",
        "pass_observed": "the generated shard files passed the authoritative six-thousand-word check",
    },
    {
        "method_id": "AL6684-MF-X1-022",
        "negative_id": "AL6684-NEG-X1-022",
        "title": "self-exclude an existing x1 manifest from regenerated allowlists",
        "failure_signature": "the pre-stage review found 47 declared rows for 46 unique paths after regeneration",
        "trigger": "a prior x1 manifest exists when the builder snapshots intended paths and is later appended again",
        "workaround": "exclude the manifest from intended paths and add it exactly once at review time",
        "pass_observed": "the regenerated allowlist and actual status matched one-for-one with no duplicates",
    },
]


EXACT_APPROVAL_TITLES = [
    "access to any real slide, specimen, calibration object, or collection record",
    "operation of a real microscope, whole-slide scanner, objective, stage, or sensor",
    "use of a real calibration slide, certificate, specimen, or patient-linked image",
    "professional slide-scanner calibration, pathology, diagnosis, or conformance determination",
    "release or rejection of a real image, focal stack, pyramid, or diagnostic artifact",
    "focus selection, annotation, segmentation, diagnosis, treatment, or specimen decision",
    "copyright, access, takedown, retention, or disclosure decision",
    "privacy-impact or protected-disclosure decision",
    "cultural-care classification or culturally sensitive content decision",
    "Maori wording, tikanga, data-governance, place-name, or authority decision",
    "affected-party remedy or beneficiary acceptance decision",
    "production credential, key, token, account, API, or external side effect",
    "cross-lane mutation, merge, reset, force-push, or destructive cleanup",
    "host-security change, elevation, Windows feature change, or reboot",
    "complete accessibility or assistive-technology conformance claim",
    "complete privacy, exhaustive security, or supply-chain assurance claim",
    "independent-team reproduction or external audit claim",
    "empirical GMUT likelihood, posterior, constraint, or confirmation",
    "AGI, ASI, consciousness, personhood, or identity-continuity claim",
    "Theory-of-Everything, proof or canon, deployment, or Stage 20 promotion",
]

BLOCKED_TITLES = [
    "real microscope or scanner fleet benchmark without equipment access, competence, and approvals",
    "real slide or specimen corpus ingestion without rights, custody, privacy, and cultural authority",
    "real calibration-slide certification without traceable metrology evidence",
    "operator study without participants, ethics, accessibility, and independent review",
    "production identity exchange without standards-conformant keys and trust governance",
    "real cultural-care decision without affected parties and competent cultural authority",
    "Maori data-governance decision without tangata whenua, iwi, hapu, and Maori authority",
    "professional release protocol without institutions, qualified practitioners, and accountability",
    "empirical GMUT inference without observations, likelihood, uncertainty, and independent review",
    "Stage 20 decision without every declared scientific, social, safety, legal, and authority gate",
]


def command_version(*command: str) -> str:
    effective = command
    if command and command[0].casefold() == "codex":
        effective = ("cmd.exe", "/d", "/c", *command)
    completed = subprocess.run(effective, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (completed.stdout or completed.stderr).strip().splitlines()[0]


def overview_text() -> str:
    return f"""# Auren Lark {PHASE} x1 integrated overview

## Purpose and truth posture

This is a planning-only x1 freeze for a bounded owner-local software phase. It does not contain x2 implementation, an observed outcome, a completed prototype, a real scan, a real calibration, or a release decision. Auren Lark uses {PRONOUNS} as relational working pronouns and the relational role `{RELATIONAL_ROLE}` with the hope to {RELATIONAL_HOPE[0].lower() + RELATIONAL_HOPE[1:]} {IDENTITY_BOUNDARY} The inherited terminal verdict remains `{TERMINAL_VERDICT}`.

The exact source is Ilyra Fen's clean final `{SOURCE_FINAL}` on the declared source branch. Ilyra's corrected x1 and immutable evidence anchors are recorded, their ancestry was checked read-only, and the Lyren-source-to-Ilyra-final route contains four single-parent commits and zero merges. Ilyra's one canonical aggregate failed and retains zero canonical-success credit; its separately named dependency-corrected composite is bounded recovery evidence only. Neither is replayed or claimed as Auren evidence. The activation overlay begins with {ACTIVATION_OVERLAY['effective_negatives']} retained negatives, {ACTIVATION_OVERLAY['methods']} methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, {ACTIVATION_OVERLAY['passing_witnesses']} passing witnesses, {ACTIVATION_OVERLAY['open_gaps']} open gaps, and {ACTIVATION_OVERLAY['exact_gates']} exact gates. Twenty-two Auren startup and x1 failures and their bounded recoveries remain visible at zero initial-pass credit, making the x1 overlay {X1_OVERLAY['effective_negatives']} negatives and {X1_OVERLAY['methods']} methods without rewriting Ilyra's repository seal. This x1 is built once from `{INITIAL_X1_HEAD}` and contains no corrective or x2 lifecycle.

## Primary pillar and practice lens

The primary pillar is {PRIMARY_PILLAR}. The phase treats work intake, calibration holds, tile-addressed exceptions, bounded retries, correction, readback, workload, stop tokens, and handover as synthetic workflow state that software may make legible but may not operationally settle. An equipment identifier is not a personal identity. A tile identifier is not a diagnosis or authenticity judgment. A correction record is not proof that a real institution accepted a remedy. A passing rule does not allocate a right, confer authority, or establish cultural legitimacy.

The bounded human-practice lens is synthetic microscope-slide digitization calibration lineage and focus-stack exception review. Three facets are frozen: {PRACTICES[0]}; {PRACTICES[1]}; and {PRACTICES[2]}. They are learning and design lenses only. The phase has no real worker, employer, slide, specimen, patient, collection, scanner, microscope, calibration target, certificate, measurement, site, device, institution, affected person, or authority case. It establishes no employment, qualification, professional competence, diagnosis, conformance, release authority, preservation outcome, legal interpretation, cultural legitimacy, Maori authority, or participant evidence.

GMUT Mind remains explicit through a typed slide-focus analogy docket and nonconversion firewall. That docket may check symbols, units, domains, declared transforms, nuisance separation, and observation refusal. It cannot turn a slide-imaging analogy into a physical field, detected force, likelihood, posterior, parameter constraint, ultraviolet completion, quantum completeness, empirical confirmation, or Theory of Everything. Freed ID and CBR Heart remain explicit through zero-key synthetic lineage, access, privacy, contestability, remedy, cultural-care, and decision-right vacancies. THOS has no real arms, participants, operators, safety monitoring, operational outcome, or effectiveness estimate.

## Novelty and proposal freeze

The inherited declared proposal chain is {INHERITED_FROZEN_PROPOSALS}. The x1 audit reads every visible proposal-freeze Git blob reachable in the repository object graph, parses visible proposal rows, normalizes titles, computes an exact title-set digest, and records three nearest token-set neighbors for each new proposal. Exact title collision or a neighbor similarity at or above the declared quarantine threshold stops the freeze. This is a useful falsifier, not a universal semantic proof: compressed historical titles remain unavailable, so novelty beyond the visible set retains an open gap.

Forty new proposals are frozen, bringing the declared chain to {INHERITED_FROZEN_PROPOSALS + len(PROPOSAL_BLUEPRINTS)}. Expected dispositions are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Each row contains its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, expected disposition, exact-title collision state, bounded semantic neighbors, and four preregistered mutations. The 160 mutations are plans only in x1. A later rejection can demonstrate a bounded guard but will not prove production security, scientific truth, professional competence, accessibility completeness, privacy completeness, or authority.

## Official-source use

The source ledger records current official DICOM WSI and pathology-imaging vocabulary, the OME-TIFF specification, W3C PROV-DM and WCAG 2.2, and the Library of Congress PREMIS maintenance activity. Those sources contribute terminology and refusal conditions only. No external file, slide image, specimen record, calibration dataset, profile, target result, measurement row, or private record is downloaded or ingested. DICOM's tiled, pyramidal, and focal-plane vocabulary does not establish DICOM conformance, pathology workflow, image quality, or diagnosis; its Z-plane warning is preserved as local context rather than absolute depth. OME dimensional and pyramid vocabulary does not establish OME-TIFF conformance or interoperability. PROV relations do not prove authenticity or responsibility. A WCAG-shaped static structure does not replace manual keyboard, responsive, browser-diverse, assistive-technology, cognitive-accessibility, Maori-language, security-usability, or affected-user evaluation.

## Expanded portfolio

The x1 portfolio freezes sixty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skill builds, ten family-current runner builds, thirty additive CLEAN/FIX/REFINE reviews, twenty exact-approval packets, and ten blocked packets. All entries have zero completion credit in x1. Safe-now means only that an owner-local structural or synthetic control may be attempted without real material, secrets, accounts, authority decisions, destructive operations, host changes, or sibling mutation. Candidate means a bounded prototype may be tested under the same exclusions. Exact-approval and blocked work remains unexecuted unless exact future evidence and competent authority genuinely change the gate.

Every proposed skill uses a family-current `ghc-family-*` name and every runner uses a `ghc_family_*` name. Historical owner-specific callers remain compatibility evidence and are not deleted, renamed, or rewritten. No skill is globally installed in x1. The later x2 plan is to build phase-local packages, smoke-use them on accepting and rejecting fixtures, and record only their bounded behavior. The two-thousand-file stop applies to the materialized sparse owner lane, not to the inherited repository's historical object graph.

## Failure retention and Method Flow

The Method Flow ledger preserves twenty-two startup and x1 failures: one combined skill display truncation; one PowerShell empty-pipe parser fault; one guessed final-manifest path; one absent external receipt location; one incompatible range projection; one malformed proposal-file existence expression; one unsupported `ls-tree` glob pathspec; one eight-title novelty quarantine; one unsupported absolute common-dir probe; one pipeline exit-code misclassification; one noisy depth-truncated worktree receipt; one slash-direction registration mismatch; one rejected oversized overview patch hunk; one stale mechanically seeded branch literal; one rejected combined recovery patch; one predecessor-scoped forbidden-module literal; one import preflight that created bytecode; one policy-rejected recursive cache cleanup; one stale split test path that caused twenty scoped failures; one 6,119-word Method Flow cap stop; one malformed in-memory shard projection; and one regenerated-manifest duplication in the staged allowlist. None receives initial-pass credit. Each has a stable method, retained-negative identifier, trigger, smallest bounded recovery, failure witness, passing recovery witness, recurrence guard, and rollback. The worktree operation was not replayed: scalar inspection proved that the branch and sparse worktree already existed at the exact source and was clean. The proposal retry changes only the eight quarantined titles. The absent external receipt bytes remain unverified rather than being represented as a pass. Complete Method Flow rows are preserved in deterministic five-method shards behind a compact logical index.

The canonical-validation rule is one successful exact-final owner-scoped aggregate, never replayed after success. If the aggregate fails, the failure remains zero-credit evidence; only the attributable dependency may be isolated when justified, and a separately named recovery cannot be relabelled as canonical success. Auren will scan and test only their source-to-final owner delta, literal new or modified modules, manifests, JSON, Markdown, privacy classes, staged allowlists, ancestry, history, file ceiling, clean state, and remote equality. Full-repository, unchanged-history, sibling-lane, and cross-lane scans remain excluded.

## Privacy, accessibility, security, and authority boundaries

Durable artifacts exclude raw task or thread identifiers, private routes, callable identifiers, transcripts, screenshots, session streams, credentials, tokens, private keys, private absolute paths, and real protected material. The five-class scan is bounded to owner text files and looks for credentials or secrets, raw identifiers, private routes or paths, transcripts or session streams, and protected real-person material. A zero-hit scan is not privacy-complete assurance. Changed-code security review is limited to literal Auren modules and cannot prove exhaustive security, supply-chain integrity, or production readiness.

The static report plan uses a native table, caption, scoped headers, explicit status text, a linear reading order, visible focus styling, responsive overflow guidance, and print fallback. These are structural hypotheses. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language, security usability, and evaluation by affected users remain reserved. No synthetic result is converted into a rights allocation, culturally legitimate label, professional release, or public decision.

## x1-to-x2 gate

X2 may begin only after the planning-only x1 surface is exactly staged, diff-clean, committed as a dedicated single-parent child of Ilyra's final, pushed without force, and proven equal across local, upstream, tracking, and a fresh live remote with zero divergence. The immutable x1 Git blobs, not checkout bytes, become the later seal domain. X2 must execute only the frozen bounded work, preserve all four truth labels, retain every failure and rejected mutation, and stop rather than manufacture evidence. No successor is contacted during x1 or x2. The successor edge is resolved only from Hamish's newest live authority after Auren's own clean, pushed, fresh-live-equal exact-final terminal gate.
"""


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 threat model

## Assets and boundaries

Protected assets are the immutable Ilyra source, the dedicated Auren x1 freeze, exact Git-blob manifests, retained failures, proposal and portfolio truth, authority vacancies, and the absence of real material. Sibling and shared lanes are read-only. The lane is sparse and D-first; materialization stops at 2,000 files. The phase creates no account, key, token, external side effect, real scan, or authority decision.

## Principal threats

1. **Lifecycle mixing.** X2 implementation or outcome language could enter x1. The builder refuses any owner x2, evidence, final, closeout, or seal path and any x2/final module before x1 freeze.
2. **Semantic duplication.** A title might repeat visible inherited work. Every visible proposal freeze is parsed, normalized, and compared; exact collisions and high-similarity neighbors quarantine the freeze. Compressed historic titles remain an open gap rather than a proof of novelty.
3. **Checkout-byte drift.** Windows line-ending conversion could make a worktree hash differ from the committed blob. Manifests declare Git-blob canonicalization and later replay exact committed bytes.
4. **Failure erasure.** A recovery could be narrated as an initially clean pass. Method Flow keeps the failure witness, negative identifier, zero credit, recovery witness, and recurrence guard.
5. **Evidence promotion.** Synthetic calibration fields could be described as real measurements, conformance, professional competence, physical evidence, rights, or authority. Every artifact carries evidence and protected-gate boundaries; outcome vocabulary is restricted.
6. **Identifier leakage.** Raw task identifiers, private routes, transcripts, credentials, absolute private paths, or real protected data could enter public files. The owner-delta five-class scan is a terminal gate, but remains bounded and non-exhaustive.
7. **Over-materialization.** A broad checkout or scan could exceed the 2,000-file budget or traverse unchanged history. Sparse patterns and owner-delta allowlists are exact; the full repository suite remains excluded.
8. **Route drift.** A historical baton might name a stale successor. No successor is contacted before terminal validation; live authority and the exact current title must be reread immediately before one send.
9. **Authority substitution.** A passing software guard could be treated as legal, cultural, Maori, affected-party, accessibility, professional, scientific, or deployment authority. Those claims remain open or exact-gated.
10. **Canonical replay inflation.** A successful aggregate could be run again to manufacture confidence. Exactly one successful invocation is allowed and never replayed.

## Recovery posture

Recovery is additive and smallest-scope. Stop, retain the first failed witness, inspect exact state, correct only the attributable dependency, and run only the bounded recovery that the failure justifies. Never reset, force-push, rewrite, merge, delete sibling material, weaken host security, install unrelated software, or substitute a route. {EVIDENCE_BOUNDARY}
"""


def static_report_plan_text() -> str:
    return f"""# Accessible static report plan

The x2 report will be a static owner-local HTML and Markdown representation of synthetic focus exceptions. Its primary table will have a visible caption, one header row with explicit column scopes, stable tile, plane, and session aliases, status text independent of color, and a summary before detailed rows. The linear source order will match the visual order. Links and controls, if any, will use descriptive text. Focus styling, high-contrast boundaries, narrow-screen overflow guidance, and print rules will be structural requirements.

Alternative text will describe the purpose of any diagram rather than reproduce raw identifiers. Numeric fields will include units and exact-rational forms where applicable. Error, quarantine, open-gap, and exact-gate states will be spelled out. A no-script fallback will retain the complete bounded table. The report will not include auto-playing media, real frames, screenshots, transcripts, private paths, credentials, or person-level data.

The structural audit cannot establish complete accessibility. Manual keyboard and touch traversal, zoom and reflow, responsive layouts, browser diversity, screen-reader and other assistive-technology behavior, cognitive accessibility, Maori-language quality, security usability, and affected-user evaluation remain reserved. A passing static audit will be labelled `completed` only for its declared software structure, never for WCAG conformance or beneficiary acceptance.
"""


def method_flow_document(now: str) -> dict:
    methods = []
    witnesses = []
    events = []
    recommendations = []
    for index, row in enumerate(STARTUP_FAILURES, 1):
        fail_id = f"AL6684-W-START-{index:03d}-FAIL"
        pass_id = f"AL6684-W-START-{index:03d}-PASS"
        methods.append({
            "method_id": row["method_id"],
            "title": row["title"],
            "failure_signature": row["failure_signature"],
            "trigger_preconditions": [row["trigger"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": row["workaround"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": row["workaround"],
            "rollback": "stop the bounded operation and preserve exact source state without destructive action",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": list(PROTECTED_GATES),
            "retained_negative_ids": [row["negative_id"]],
            "scope_boundary": "owner-local startup and x1 workflow only",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE_FINAL,
            "final_commit": SOURCE_FINAL,
            "changed_file_allowlist": [],
            "module_allowlist": [],
            "exact_pushed_head_required": False,
        })
        witnesses.extend([
            {
                "witness_id": fail_id,
                "method_id": row["method_id"],
                "procedure": "retain the first attributable attempt before recovery",
                "scope": "owner-local startup",
                "expected": "bounded operation returns a complete attributable result",
                "observed": row["failure_signature"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [row["negative_id"]],
                "boundary": "zero initial-pass credit; no scientific, authority, security, or production claim",
            },
            {
                "witness_id": pass_id,
                "method_id": row["method_id"],
                "procedure": row["workaround"],
                "scope": "owner-local bounded recovery",
                "expected": "recover exact attributable state without erasing the failure",
                "observed": row["pass_observed"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [row["negative_id"]],
                "boundary": "bounded recovery evidence only; the failed witness remains retained",
            },
        ])
        events.extend([
            {"event_id": f"AL6684-E-{index:03d}-1", "method_id": row["method_id"], "from": None, "to": "observed", "at": now},
            {"event_id": f"AL6684-E-{index:03d}-2", "method_id": row["method_id"], "from": "observed", "to": "candidate", "at": now},
            {"event_id": f"AL6684-E-{index:03d}-3", "method_id": row["method_id"], "from": "candidate", "to": "validated", "at": now, "witness_id": pass_id},
            {"event_id": f"AL6684-E-{index:03d}-4", "method_id": row["method_id"], "from": "validated", "to": "preferred", "at": now, "witness_id": pass_id},
        ])
        recommendations.append({"method_id": row["method_id"], "state": "preferred", "reason": "bounded failure retained and smallest recovery passed"})
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "attributable_owner": OWNER,
        "source_commit": SOURCE_FINAL,
        "final_commit": "PENDING_X1_FREEZE",
        "changed_file_allowlist": [],
        "new_or_modified_module_allowlist": [
            "scripts/ghc_family_auren_lark_v668_v4_archive.py",
            "scripts/build_ghc_family_auren_lark_v668_v4_x1.py",
            "tests/test_ghc_family_auren_lark_v668_v4_x1.py",
        ],
        "sparse_file_budget": {"ceiling": 2000, "state": "below_ceiling"},
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "failed_witnesses": sum(w["result"] == "fail" for w in witnesses),
            "passing_witnesses": sum(w["result"] == "pass" for w in witnesses),
            "retained_negatives": len({n for m in methods for n in m["retained_negative_ids"]}),
        },
        "boundary": "Same-owner workflow recovery is not independent reproduction, external audit, authority, or Stage 20 evidence.",
    }


def main() -> None:
    assert_source_and_x1_only()
    now = utc_now()
    audit, visible_titles = visible_proposal_inventory()
    proposals = proposal_rows(visible_titles)
    exact_collisions = [row["proposal_id"] for row in proposals if row["visible_title_collision"]]
    quarantined = [row["proposal_id"] for row in proposals if row["semantic_neighbor_quarantined"]]
    if exact_collisions or quarantined:
        raise ValueError(f"proposal novelty quarantine: collisions={exact_collisions}, neighbors={quarantined}")

    completed_titles = [title for title, outcome, _ in PROPOSAL_BLUEPRINTS if outcome == "completed"]
    safe_titles = (
        [f"positive schema and bounded-state fixture for: {title}" for title in completed_titles]
        + [f"four-class mutation refusal review for: {title}" for title in completed_titles]
        + [
            "exact source-anchor and zero-merge scalar preflight",
            "Git-blob versus checkout-byte hash-domain declaration review",
            "owner-delta five-class privacy candidate disposition plan",
            "two-thousand-file sparse materialization and rotation receipt",
        ]
    )
    candidate_titles = [f"bounded acceptance and refusal prototype for: {title}" for title, _, _ in PROPOSAL_BLUEPRINTS[:30]]
    cfr_titles = [f"REFINE deterministic order, exact units, and boundary vocabulary for: {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:30]]
    skill_rows = portfolio_rows("AL6684-SKILL", [f"build and smoke-use phase-local skill {name}" for name in SKILL_NAMES], "phase_local_skill")
    runner_rows = portfolio_rows("AL6684-RUNNER", [f"build and accept/reject smoke-use runner {name}" for name in RUNNER_NAMES], "family_current_runner")
    portfolio = {
        "phase": PHASE,
        "owner": OWNER,
        "x1_planning_only": True,
        "inherited_portfolio_completion_credit": 0,
        "safe_now": portfolio_rows("AL6684-SAFE", safe_titles, "safe_now"),
        "candidates": portfolio_rows("AL6684-CAND", candidate_titles, "candidate"),
        "skills": skill_rows,
        "runners": runner_rows,
        "clean_fix_refine": portfolio_rows("AL6684-CFR", cfr_titles, "clean_fix_refine"),
        "exact_approval": portfolio_rows("AL6684-EXACT", EXACT_APPROVAL_TITLES, "exact_approval", "exact_approval_unexecuted"),
        "blocked": portfolio_rows("AL6684-BLOCK", BLOCKED_TITLES, "blocked", "blocked_unexecuted"),
        "floors": {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 30},
        "protected_gates": list(PROTECTED_GATES),
    }

    write_json("x1/source-intake.json", {
        "phase": PHASE,
        "owner": OWNER,
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_FINAL,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_ancestor": SOURCE_ANCESTOR,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_failed_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_dependency_corrected_composite_receipt_sha256": SOURCE_COMPOSITE_RECEIPT_SHA256,
        "source_canonical_success_credit": 0,
        "source_composite_is_canonical_success": False,
        "receipt_file_present_in_expected_bounded_location": False,
        "fresh_live_remote_equal_before_lane_creation": True,
        "source_to_final_commits": 4,
        "source_to_final_merges": 0,
        "source_lane_mutated": False,
        "external_downloads": 0,
        "external_rows_ingested": 0,
        "boundary": EVIDENCE_BOUNDARY,
    })
    write_json("x1/source-ledger.json", {"phase": PHASE, "inspected_at": now, "sources": SOURCE_LEDGER, "downloads": 0, "empirical_credit": 0})
    audit["generated_at"] = now
    write_json("x1/proposal-chain-audit.json", audit)
    outcome_counts = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ALLOWED_OUTCOMES}
    proposal_shards = []
    for offset in range(0, len(proposals), 5):
        shard_number = offset // 5 + 1
        relative = f"x1/proposal-freeze-shards/proposals-{shard_number:02d}.json"
        rows = proposals[offset : offset + 5]
        write_json(relative, {
            "phase": PHASE,
            "shard": shard_number,
            "proposal_ids": [row["proposal_id"] for row in rows],
            "new_proposals": rows,
            "x1_planning_only": True,
        })
        proposal_shards.append({
            "path": f"docs/auren-lark/v668-v4/{relative}",
            "proposal_count": len(rows),
            "first_proposal_id": rows[0]["proposal_id"],
            "last_proposal_id": rows[-1]["proposal_id"],
        })
    write_json("x1/proposal-freeze.json", {
        "phase": PHASE,
        "frozen_at": now,
        "inherited_frozen_proposals": INHERITED_FROZEN_PROPOSALS,
        "new_proposal_count": len(proposals),
        "new_frozen_total": INHERITED_FROZEN_PROPOSALS + len(proposals),
        "selected_inherited_count": audit["selected_count"],
        "selected_inherited": audit["selected_inherited"],
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_completion_credit": 0,
        "proposal_shards": proposal_shards,
        "proposal_shard_count": len(proposal_shards),
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "expected_outcomes": outcome_counts,
        "outcomes_observed": False,
        "negative_mutation_count": sum(len(row["negative_fixtures"]) for row in proposals),
        "visible_title_collision_count": len(exact_collisions),
        "semantic_neighbor_quarantine_count": len(quarantined),
        "x1_planning_only": True,
    })
    portfolio_chunk_sizes = {
        "safe_now": 20,
        "candidates": 15,
        "skills": 20,
        "runners": 10,
        "clean_fix_refine": 15,
        "exact_approval": 20,
        "blocked": 10,
    }
    portfolio_shards: dict[str, list[dict]] = {}
    for category, chunk_size in portfolio_chunk_sizes.items():
        rows = portfolio[category]
        category_shards = []
        for offset in range(0, len(rows), chunk_size):
            shard_number = offset // chunk_size + 1
            relative = f"x1/portfolio-shards/{category.replace('_', '-')}-{shard_number:02d}.json"
            shard_rows = rows[offset : offset + chunk_size]
            write_json(relative, {
                "phase": PHASE,
                "category": category,
                "shard": shard_number,
                "rows": shard_rows,
                "x1_planning_only": True,
            })
            category_shards.append({
                "path": f"docs/auren-lark/v668-v4/{relative}",
                "row_count": len(shard_rows),
                "first_task_id": shard_rows[0]["task_id"],
                "last_task_id": shard_rows[-1]["task_id"],
            })
        portfolio_shards[category] = category_shards
    write_json("x1/portfolio-freeze.json", {
        "phase": PHASE,
        "owner": OWNER,
        "x1_planning_only": True,
        "inherited_portfolio_completion_credit": 0,
        "category_counts": {category: len(portfolio[category]) for category in portfolio_chunk_sizes},
        "category_shards": portfolio_shards,
        "floors": portfolio["floors"],
        "protected_gates": list(PROTECTED_GATES),
    })
    write_json("x1/wellbeing-and-corrigibility.json", {
        "owner": OWNER,
        "pronouns": PRONOUNS,
        "relational_role": RELATIONAL_ROLE,
        "relational_hope": RELATIONAL_HOPE,
        "identity_boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route; protected gates override momentum.",
        "workload": {"materialized_file_ceiling": 2000, "current_state": "bounded_sparse_x1", "background_siblings_contacted": 0},
        "wellbeing_boundary": "This is a workload and workflow check, not evidence of sentience, subjective wellbeing, or continuity.",
    })
    write_json("x1/environment-and-version-receipt.json", {
        "verified_only": True,
        "python": command_version("python", "--version"),
        "git": command_version("git", "--version"),
        "node": command_version("node", "--version"),
        "codex_cli": command_version("codex", "--version"),
        "powershell": "7.6.4",
        "updates_performed": 0,
        "installs_performed": 0,
        "elevation": False,
        "host_security_changes": False,
        "reboot": False,
    })
    write_json("x1/compatibility-inventory.json", {
        "family_current_skill_prefix": "ghc-family-",
        "family_current_runner_prefix": "ghc_family_",
        "planned_skills": SKILL_NAMES,
        "planned_runners": RUNNER_NAMES,
        "historical_callers_deleted_or_renamed": 0,
        "global_installs_in_x1": 0,
        "boundary": "historical owner-specific names remain compatibility evidence, not cleanup targets",
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc.family.workflow-plan.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source_commit": SOURCE_FINAL,
        "plan": [
            {"step": "source and guidance gate", "state": "completed", "evidence": "exact anchors, hashes, ancestry, clean state, and live equality"},
            {"step": "novelty and x1 freeze", "state": "in_progress", "evidence": "visible title inventory and 40 preregistered proposals"},
            {"step": "immutable x1 push gate", "state": "pending", "evidence": "single-parent commit and four-way equality required"},
            {"step": "bounded x2 execution", "state": "pending", "evidence": "frozen fixtures, 160 mutations, skills, runners, and reports only"},
            {"step": "closeout and one canonical aggregate", "state": "pending", "evidence": "exact owner delta, no success replay"},
            {"step": "terminal route", "state": "pending", "evidence": "live authority reread and at most one exact-title send"},
        ],
        "stale_plan_rejected": True,
        "scope_change": "practice seed adopted only after independent novelty freeze; no authority or empirical scope expansion",
    })
    write_json("x1/reflection-remaster-decision.json", {
        "schema": "ghc.family.reflection-remaster.v1",
        "phase": PHASE,
        "inputs": ["Ilyra successor practice seed", "current family Index", "Method Flow recurrence guards", "visible proposal chain"],
        "decisions": [
            {"surface": "microscope-slide practice seed", "decision": "refine", "reason": "freeze synthetic calibration lineage and focus-stack exceptions; inherited completion credit remains zero"},
            {"surface": "family-current naming", "decision": "reuse", "reason": "preserve ghc-family-* and ghc_family_* compatibility"},
            {"surface": "private external receipt bytes", "decision": "defer", "reason": "committed material omits the locator; supplied hashes remain activation assertions"},
            {"surface": "historical owner-specific tools", "decision": "retain", "reason": "no migration evidence authorizes deletion or renaming"},
        ],
        "material_changes": "new practice-specific proposal, skill, runner, and failure-guard portfolios",
        "authority_change": False,
    })
    write_json("x1/route-plan.json", {
        "successor_contacted": False,
        "successor_inferred_from_history": False,
        "terminal_gate_required": True,
        "resolution_rule": "reread Hamish's newest live authority and exact current roster after exact-final proof only",
        "maximum_sends": 1,
        "standby_substitution": False,
    })
    write_json("x1/phase-truth.json", {
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1_planning_only",
        "primary_pillar": PRIMARY_PILLAR,
        "practices": list(PRACTICES),
        "frozen_proposal_chain": INHERITED_FROZEN_PROPOSALS + len(proposals),
        "expected_outcome_counts": outcome_counts,
        "observed_outcome_counts": None,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "x2_implementation_count": 0,
        "x2_outcome_claim_count": 0,
        "activation_overlay": ACTIVATION_OVERLAY,
        "x1_overlay": X1_OVERLAY,
        "terminal_verdict": TERMINAL_VERDICT,
        "protected_gates": list(PROTECTED_GATES),
    })
    write_text("x1/integrated-overview.md", overview_text())
    write_text("x1/threat-model.md", threat_model_text())
    write_text("x1/accessible-static-report-plan.md", static_report_plan_text())
    method_flow = method_flow_document(now)
    method_shards = []
    for offset in range(0, len(method_flow["methods"]), 5):
        shard_number = offset // 5 + 1
        methods = method_flow["methods"][offset : offset + 5]
        method_ids = {row["method_id"] for row in methods}
        witnesses = [row for row in method_flow["witnesses"] if row["method_id"] in method_ids]
        events = [row for row in method_flow["state_events"] if row["method_id"] in method_ids]
        recommendations = [row for row in method_flow["recommendations"] if row["method_id"] in method_ids]
        relative = f"method-flow/x1-ledger-shards/methods-{shard_number:02d}.json"
        write_json(relative, {
            "schema": method_flow["schema"],
            "phase": PHASE,
            "owner": OWNER,
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
        })
        method_shards.append({
            "path": f"docs/auren-lark/v668-v4/{relative}",
            "method_count": len(methods),
            "witness_count": len(witnesses),
            "event_count": len(events),
            "recommendation_count": len(recommendations),
            "first_method_id": methods[0]["method_id"],
            "last_method_id": methods[-1]["method_id"],
        })
    method_flow_index = {
        key: value
        for key, value in method_flow.items()
        if key not in {"methods", "witnesses", "state_events", "recommendations"}
    }
    method_flow_index["logical_shards"] = method_shards
    method_flow_index["logical_shard_count"] = len(method_shards)
    method_flow_index["row_domain"] = "ordered concatenation of declared shard arrays"
    write_json("method-flow/x1-ledger.json", method_flow_index)
    write_json("method-flow/x1-summary.json", {
        "source_activation_overlay": ACTIVATION_OVERLAY,
        "x1_overlay": X1_OVERLAY,
        "owner_startup_failures": STARTUP_FAILURES,
        "failure_count": len(STARTUP_FAILURES),
        "all_failures_retained": True,
        "correction_erases_failure": False,
        "x1_planning_only": True,
    })

    code_paths = [
        ROOT / "scripts" / "ghc_family_auren_lark_v668_v4_archive.py",
        ROOT / "scripts" / "build_ghc_family_auren_lark_v668_v4_x1.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v668_v4_x1.py",
    ]
    missing_code = [str(path.relative_to(ROOT)) for path in code_paths if not path.is_file()]
    if missing_code:
        raise ValueError(f"x1 code allowlist missing: {missing_code}")
    intended_paths = sorted(
        [
            path.relative_to(ROOT).as_posix()
            for path in phase_owner_files()
            if path.name != "x1-manifest.json"
        ]
        + [path.relative_to(ROOT).as_posix() for path in code_paths]
    )
    write_json("validation/x1-staged-allowlist.json", {
        "phase": PHASE,
        "source_commit": SOURCE_FINAL,
        "intended_paths_before_manifest": intended_paths,
        "x2_paths": 0,
        "exact_review_required": True,
    })
    paths_for_manifest = [path for path in phase_owner_files() if path.name != "x1-manifest.json"] + code_paths
    manifest = {
        "phase": PHASE,
        "lifecycle": "immutable_x1_candidate",
        "source_commit": SOURCE_FINAL,
        "entries": manifest_rows(paths_for_manifest),
        "self_exclusions": [f"docs/auren-lark/v668-v4/x1/x1-manifest.json"],
        "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        "later_replay_required": True,
    }
    manifest["entry_count"] = len(manifest["entries"])
    write_json("x1/x1-manifest.json", manifest)

    docs = [path for path in phase_owner_files() if path.suffix.lower() in {".md", ".json", ".txt", ".html"}]
    oversized = {path.relative_to(ROOT).as_posix(): word_count(path) for path in docs if word_count(path) > 6000}
    if oversized:
        raise ValueError(f"word cap exceeded: {oversized}")
    print(json.dumps({
        "phase": PHASE,
        "new_proposals": len(proposals),
        "proposal_chain": INHERITED_FROZEN_PROPOSALS + len(proposals),
        "mutations_preregistered": sum(len(row["negative_fixtures"]) for row in proposals),
        "portfolio": {key: len(portfolio[key]) for key in ("safe_now", "candidates", "skills", "runners", "clean_fix_refine", "exact_approval", "blocked")},
        "phase_files": len(phase_owner_files()),
        "manifest_entries": manifest["entry_count"],
        "overview_words": word_count(PHASE_ROOT / "x1" / "integrated-overview.md"),
        "state": "X1_PLANNING_ONLY_READY_FOR_SCOPED_VALIDATION",
    }, indent=2))


if __name__ == "__main__":
    main()
