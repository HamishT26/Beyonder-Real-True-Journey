#!/usr/bin/env python3
"""Build the dedicated planning-only Ilyra Fen v668-v3 x1 freeze."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ghc_family_ilyra_fen_v668_v3_archive import (
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
        "method_id": "IF6683-MF-START-001",
        "negative_id": "IF6683-NEG-START-001",
        "title": "bounded numbered guidance-window recovery",
        "failure_signature": "complete auth-state display truncated before EOF",
        "trigger": "a current guidance file exceeds one attributable display window",
        "workaround": "read bounded numbered windows through the exact final line and preserve the first truncation",
        "pass_observed": "all guidance and schema files named by the activation were read through EOF",
    },
    {
        "method_id": "IF6683-MF-START-002",
        "negative_id": "IF6683-NEG-START-002",
        "title": "missing external receipt remains explicit",
        "failure_signature": "expected owner receipt directory was absent",
        "trigger": "activation names an external receipt hash but the expected bounded directory is absent",
        "workaround": "retain the missing local receipt as an open evidence condition and use the live sanitized activation hash without inventing a file",
        "pass_observed": "source anchors and activation packet hash were independently verified without claiming a local receipt file",
    },
    {
        "method_id": "IF6683-MF-START-003",
        "negative_id": "IF6683-NEG-START-003",
        "title": "avoid broad receipt-hash wrapper replay",
        "failure_signature": "broad exact-hash search wrapper returned no attributable result or session handle",
        "trigger": "a recursive receipt search crosses an unnecessarily broad archive surface",
        "workaround": "do not replay the broad search; use bounded owner receipt locations and exact source evidence",
        "pass_observed": "no repeated broad search ran and no absent receipt was promoted into a passing witness",
    },
    {
        "method_id": "IF6683-MF-START-004",
        "negative_id": "IF6683-NEG-START-004",
        "title": "discover exact phase paths before projection",
        "failure_signature": "assumed proposal-chain audit subdirectory did not exist",
        "trigger": "an inherited phase may place an artifact directly under x1 instead of a guessed child folder",
        "workaround": "use rg --files on the exact owner phase and then read the discovered literal path",
        "pass_observed": "the exact proposal-chain audit and phase truth were read from discovered paths",
    },
    {
        "method_id": "IF6683-MF-START-005",
        "negative_id": "IF6683-NEG-START-005",
        "title": "inspect worktree state after wrapper receipt loss",
        "failure_signature": "worktree creation wrapper returned no projected receipt after its bounded wait",
        "trigger": "a Git worktree operation may complete even when its orchestration wrapper loses output",
        "workaround": "do not replay creation; inspect exact path, branch ref, worktree record, HEAD, sparse config, and clean status",
        "pass_observed": "one fresh sparse Ilyra lane existed at the exact source with zero materialized owner files and a clean state",
    },
    {
        "method_id": "IF6683-MF-X1-006",
        "negative_id": "IF6683-NEG-X1-006",
        "title": "novelty quarantine before proposal freeze",
        "failure_signature": "first x1 novelty gate found one exact inherited title collision and two high-similarity neighbors",
        "trigger": "a proposed exact-gate title reuses inherited terminal vocabulary too closely",
        "workaround": "inspect only the quarantined neighbor records and rewrite the two titles around film-specific decision vacancies and noncompensating receipt classes",
        "pass_observed": "the bounded retry reported zero exact collisions and zero neighbors at or above the declared threshold",
    },
    {
        "method_id": "IF6683-MF-X1-007",
        "negative_id": "IF6683-NEG-X1-007",
        "title": "invoke Windows command shims through cmd",
        "failure_signature": "direct Python CreateProcess of the Codex PowerShell shim returned access denied",
        "trigger": "a version probe targets a PowerShell command shim rather than a native executable",
        "workaround": "invoke the exact read-only version probe through cmd.exe and retain the failed direct attempt",
        "pass_observed": "the bounded cmd invocation returned the attributable Codex CLI version without update or installation",
    },
    {
        "method_id": "IF6683-MF-X1-008",
        "negative_id": "IF6683-NEG-X1-008",
        "title": "expand untracked status for exact allowlists",
        "failure_signature": "default Git status collapsed the partially generated owner directory to a parent path",
        "trigger": "an untracked directory contains exact builder-owned recovery artifacts",
        "workaround": "request --untracked-files=all and classify each literal repository-relative path",
        "pass_observed": "the pre-freeze gate accepted only exact x1, Method Flow, validation, script, and test paths",
    },
    {
        "method_id": "IF6683-MF-X1-009",
        "negative_id": "IF6683-NEG-X1-009",
        "title": "format colon-adjacent PowerShell values explicitly",
        "failure_signature": "PowerShell rejected a double-quoted line receipt because a variable was immediately followed by a colon",
        "trigger": "a diagnostic formats path, line number, and content inside one interpolated string",
        "workaround": "use the PowerShell format operator with separately supplied scalar values",
        "pass_observed": "the corrected bounded probe displayed only the exact candidate lines for disposition",
    },
    {
        "method_id": "IF6683-MF-X1-010",
        "negative_id": "IF6683-NEG-X1-010",
        "title": "shard oversized phase ledgers before x2",
        "failure_signature": "pre-x2 word audit found proposal-freeze and portfolio-freeze above the six-thousand-word ceiling",
        "trigger": "a complete structured x1 ledger exceeds the per-document word budget",
        "workaround": "retain compact deterministic indexes and split complete rows into bounded category shards in a second x1-only commit",
        "pass_observed": "every owner phase document measured at or below six thousand words before x2 began",
    },
    {
        "method_id": "IF6683-MF-X1-011",
        "negative_id": "IF6683-NEG-X1-011",
        "title": "preserve both Git porcelain status columns",
        "failure_signature": "a global string strip removed the first status column from the first modified path",
        "trigger": "porcelain status output begins with a significant leading space for an unstaged worktree modification",
        "workaround": "consume raw subprocess stdout with splitlines and parse each two-column status record without global trimming",
        "pass_observed": "the correction preflight classified every exact modified and untracked x1 path without column loss",
    },
    {
        "method_id": "IF6683-MF-X1-012",
        "negative_id": "IF6683-NEG-X1-012",
        "title": "exclude only current-phase self rows from inherited novelty audit",
        "failure_signature": "the second x1 build compared the pushed initial x1 against itself and quarantined all forty proposals",
        "trigger": "an additive x1 correction runs after the phase's initial proposal freeze is already reachable",
        "workaround": "exclude only proposal rows whose source path is inside the current owner phase while preserving every inherited sibling and earlier-phase row",
        "pass_observed": "the correction re-audit preserved the inherited visible-title digest domain and reported zero non-self collisions",
    },
]


EXACT_APPROVAL_TITLES = [
    "access to any real film or collection object",
    "operation of a real film scanner or transport",
    "use of a real calibration target or certificate",
    "professional scanner calibration or conformance determination",
    "release or rejection of a real preservation master",
    "restoration, grading, crop, or defect-removal decision",
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
    "real scanner fleet benchmark without equipment access, competence, and approvals",
    "real film corpus ingestion without rights, custody, privacy, and cultural authority",
    "real calibration target certification without traceable metrology evidence",
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
    return f"""# Ilyra Fen {PHASE} x1 integrated overview

## Purpose and truth posture

This is a planning-only x1 freeze for a bounded owner-local software phase. It does not contain x2 implementation, an observed outcome, a completed prototype, a real scan, a real calibration, or a release decision. Ilyra Fen uses she/they pronouns and the relational role `{RELATIONAL_ROLE}` with the hope to {RELATIONAL_HOPE[0].lower() + RELATIONAL_HOPE[1:]} {IDENTITY_BOUNDARY} The inherited terminal verdict remains `{TERMINAL_VERDICT}`.

The exact source is Lyren Moss's clean final `{SOURCE_FINAL}` on the declared source branch. The inherited x1 and evidence anchors are recorded, their ancestry was checked read-only, and source-to-final contains three single-parent commits and zero merges. Lyren's successful canonical aggregate is inherited evidence only and will not be replayed or claimed as Ilyra evidence. The activation overlay begins with {ACTIVATION_OVERLAY['effective_negatives']} retained negatives, {ACTIVATION_OVERLAY['methods']} methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, {ACTIVATION_OVERLAY['passing_witnesses']} passing witnesses, {ACTIVATION_OVERLAY['open_gaps']} open gaps, and {ACTIVATION_OVERLAY['exact_gates']} exact gates. Twelve Ilyra startup and x1 failures and their bounded recoveries remain visible at zero initial-pass credit, making the x1 overlay {X1_OVERLAY['effective_negatives']} negatives and {X1_OVERLAY['methods']} methods without rewriting Lyren's seal. The retained initial x1 freeze is `{INITIAL_X1_HEAD}`; this correction remains x1-only and changes no source or x2 truth.

## Primary pillar and practice lens

The primary pillar is {PRIMARY_PILLAR}. The phase treats record identity, custody, correction, challenge, contestability, access questions, remedy vacancies, and decision rights as data that software may make legible but may not settle. An equipment identifier is not a personal identity. A frame identifier is not an authenticity judgment. A correction record is not proof that a real collection accepted a remedy. A passing rule does not allocate a right, confer authority, or establish cultural legitimacy.

The bounded human-practice lens is synthetic film-scanner calibration custody and frame-registration exception review. Three facets are frozen: {PRACTICES[0]}; {PRACTICES[1]}; and {PRACTICES[2]}. They are learning and design lenses only. The phase has no real worker, employer, film, collection, scanner, calibration target, certificate, measurement, site, device, institution, affected person, or authority case. It establishes no employment, qualification, professional competence, conformance, release authority, preservation outcome, legal interpretation, cultural legitimacy, Maori authority, or participant evidence.

GMUT Mind remains explicit through a typed optical-transfer and nuisance-parameter obligation board plus a nonconversion firewall. That board may check symbols, units, domains, declared transforms, nuisance separation, and observation refusal. It cannot turn an optical-scanning analogy into a physical field, detected force, likelihood, posterior, parameter constraint, ultraviolet completion, quantum completeness, empirical confirmation, or Theory of Everything. THOS Body remains explicit as a synthetic exception queue, workload ceiling, pause, correction replay, readback, and shift-handover proxy. It has no blind matched-budget real arms, participants, operators, safety monitoring, operational outcome, or effectiveness estimate.

## Novelty and proposal freeze

The inherited declared proposal chain is {INHERITED_FROZEN_PROPOSALS}. The x1 audit reads every visible proposal-freeze Git blob reachable in the repository object graph, parses visible proposal rows, normalizes titles, computes an exact title-set digest, and records three nearest token-set neighbors for each new proposal. Exact title collision or a neighbor similarity at or above the declared quarantine threshold stops the freeze. This is a useful falsifier, not a universal semantic proof: compressed historical titles remain unavailable, so novelty beyond the visible set retains an open gap.

Forty new proposals are frozen, bringing the declared chain to {INHERITED_FROZEN_PROPOSALS + len(PROPOSAL_BLUEPRINTS)}. Expected dispositions are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Each row contains its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, expected disposition, exact-title collision state, bounded semantic neighbors, and four preregistered mutations. The 160 mutations are plans only in x1. A later rejection can demonstrate a bounded guard but will not prove production security, scientific truth, professional competence, accessibility completeness, privacy completeness, or authority.

## Official-source use

The source ledger records current official pages from FADGI, the International Color Consortium, W3C PROV-DM and WCAG 2.2, and the Library of Congress PREMIS maintenance activity. Those sources contribute terminology and status only. No external file, calibration dataset, film image, profile, target result, measurement row, or private record is downloaded or ingested. FADGI itself distinguishes technical foundations and evaluation programs from a casual metric-only claim; this phase therefore refuses any FADGI-conformance label. ICC vocabulary does not establish that a synthetic profile is correct. PROV relations do not prove authenticity or responsibility. A WCAG-shaped static structure does not replace manual keyboard, responsive, browser-diverse, assistive-technology, cognitive-accessibility, Maori-language, security-usability, or affected-user evaluation.

## Expanded portfolio

The x1 portfolio freezes sixty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skill builds, ten family-current runner builds, thirty additive CLEAN/FIX/REFINE reviews, twenty exact-approval packets, and ten blocked packets. All entries have zero completion credit in x1. Safe-now means only that an owner-local structural or synthetic control may be attempted without real material, secrets, accounts, authority decisions, destructive operations, host changes, or sibling mutation. Candidate means a bounded prototype may be tested under the same exclusions. Exact-approval and blocked work remains unexecuted unless exact future evidence and competent authority genuinely change the gate.

Every proposed skill uses a family-current `ghc-family-*` name and every runner uses a `ghc_family_*` name. Historical owner-specific callers remain compatibility evidence and are not deleted, renamed, or rewritten. No skill is globally installed in x1. The later x2 plan is to build phase-local packages, smoke-use them on accepting and rejecting fixtures, and record only their bounded behavior. The two-thousand-file stop applies to the materialized sparse owner lane, not to the inherited repository's historical object graph.

## Failure retention and Method Flow

The Method Flow ledger preserves twelve startup and x1 failures: a truncated long guidance display; an absent expected external receipt directory; a broad receipt-hash wrapper that returned no attributable result; an incorrect assumed proposal-audit path; a worktree-creation wrapper that lost its projected receipt; the first proposal freeze stopped on an inherited exact-title collision plus two high-similarity neighbors; the first Codex version probe attempted to execute a PowerShell shim directly from Python and received access denied; default Git status collapsed the partially generated owner directory instead of exposing exact allowlist paths; a colon-adjacent PowerShell variable caused a diagnostic parser error; the pre-x2 word audit found two oversized JSON ledgers; a globally trimmed porcelain-status string lost the significant first column of its first record; and the correction novelty audit initially compared the pushed x1 against itself. None receives initial-pass credit. Each has a stable method, retained-negative identifier, trigger, smallest bounded recovery, failure witness, passing recovery witness, recurrence guard, and rollback. The worktree operation was not replayed: scalar inspection proved that the branch and sparse worktree already existed at the exact source and was clean. The proposal retry changes only the two quarantined titles. The version recovery invokes the same read-only probe through the Windows command shim. Status recovery uses literal untracked paths and raw two-column porcelain records, line receipts use the format operator, current-phase self rows alone are excluded from inherited novelty comparison, and complete proposal and portfolio rows move into deterministic bounded shards while their original paths become indexes. The absent receipt remains absent rather than being represented as a pass.

The canonical-validation rule is one successful exact-final owner-scoped aggregate, never replayed after success. If the aggregate fails, the failure remains zero-credit evidence; only the attributable dependency may be isolated when justified, and a separately named recovery cannot be relabelled as canonical success. Ilyra will scan and test only her source-to-final owner delta, literal new or modified modules, manifests, JSON, Markdown, privacy classes, staged allowlists, ancestry, history, file ceiling, clean state, and remote equality. Full-repository, unchanged-history, sibling-lane, and cross-lane scans remain excluded.

## Privacy, accessibility, security, and authority boundaries

Durable artifacts exclude raw task or thread identifiers, private routes, callable identifiers, transcripts, screenshots, session streams, credentials, tokens, private keys, private absolute paths, and real protected material. The five-class scan is bounded to owner text files and looks for credentials or secrets, raw identifiers, private routes or paths, transcripts or session streams, and protected real-person material. A zero-hit scan is not privacy-complete assurance. Changed-code security review is limited to literal Ilyra modules and cannot prove exhaustive security, supply-chain integrity, or production readiness.

The static report plan uses a native table, caption, scoped headers, explicit status text, a linear reading order, visible focus styling, responsive overflow guidance, and print fallback. These are structural hypotheses. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language, security usability, and evaluation by affected users remain reserved. No synthetic result is converted into a rights allocation, culturally legitimate label, professional release, or public decision.

## x1-to-x2 gate

X2 may begin only after the planning-only x1 surface is exactly staged, diff-clean, committed as a dedicated single-parent child of Lyren's final, pushed without force, and proven equal across local, upstream, tracking, and a fresh live remote with zero divergence. The immutable x1 Git blobs, not checkout bytes, become the later seal domain. X2 must execute only the frozen bounded work, preserve all four truth labels, retain every failure and rejected mutation, and stop rather than manufacture evidence. No successor is contacted during x1 or x2. The successor edge is resolved only from Hamish's newest live authority after Ilyra's own clean, pushed, fresh-live-equal exact-final terminal gate.
"""


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 threat model

## Assets and boundaries

Protected assets are the immutable Lyren source, the dedicated Ilyra x1 freeze, exact Git-blob manifests, retained failures, proposal and portfolio truth, authority vacancies, and the absence of real material. Sibling and shared lanes are read-only. The lane is sparse and D-first; materialization stops at 2,000 files. The phase creates no account, key, token, external side effect, real scan, or authority decision.

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

The x2 report will be a static owner-local HTML and Markdown representation of synthetic calibration exceptions. Its primary table will have a visible caption, one header row with explicit column scopes, stable frame and session aliases, status text independent of color, and a summary before detailed rows. The linear source order will match the visual order. Links and controls, if any, will use descriptive text. Focus styling, high-contrast boundaries, narrow-screen overflow guidance, and print rules will be structural requirements.

Alternative text will describe the purpose of any diagram rather than reproduce raw identifiers. Numeric fields will include units and exact-rational forms where applicable. Error, quarantine, open-gap, and exact-gate states will be spelled out. A no-script fallback will retain the complete bounded table. The report will not include auto-playing media, real frames, screenshots, transcripts, private paths, credentials, or person-level data.

The structural audit cannot establish complete accessibility. Manual keyboard and touch traversal, zoom and reflow, responsive layouts, browser diversity, screen-reader and other assistive-technology behavior, cognitive accessibility, Maori-language quality, security usability, and affected-user evaluation remain reserved. A passing static audit will be labelled `completed` only for its declared software structure, never for WCAG conformance or beneficiary acceptance.
"""


def method_flow_document(now: str) -> dict:
    methods = []
    witnesses = []
    events = []
    recommendations = []
    for index, row in enumerate(STARTUP_FAILURES, 1):
        fail_id = f"IF6683-W-START-{index:03d}-FAIL"
        pass_id = f"IF6683-W-START-{index:03d}-PASS"
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
            {"event_id": f"IF6683-E-{index:03d}-1", "method_id": row["method_id"], "from": None, "to": "observed", "at": now},
            {"event_id": f"IF6683-E-{index:03d}-2", "method_id": row["method_id"], "from": "observed", "to": "candidate", "at": now},
            {"event_id": f"IF6683-E-{index:03d}-3", "method_id": row["method_id"], "from": "candidate", "to": "validated", "at": now, "witness_id": pass_id},
            {"event_id": f"IF6683-E-{index:03d}-4", "method_id": row["method_id"], "from": "validated", "to": "preferred", "at": now, "witness_id": pass_id},
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
            "scripts/ghc_family_ilyra_fen_v668_v3_archive.py",
            "scripts/build_ghc_family_ilyra_fen_v668_v3_x1.py",
            "tests/test_ghc_family_ilyra_fen_v668_v3_x1.py",
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
    skill_rows = portfolio_rows("IF6683-SKILL", [f"build and smoke-use phase-local skill {name}" for name in SKILL_NAMES], "phase_local_skill")
    runner_rows = portfolio_rows("IF6683-RUNNER", [f"build and accept/reject smoke-use runner {name}" for name in RUNNER_NAMES], "family_current_runner")
    portfolio = {
        "phase": PHASE,
        "owner": OWNER,
        "x1_planning_only": True,
        "inherited_portfolio_completion_credit": 0,
        "safe_now": portfolio_rows("IF6683-SAFE", safe_titles, "safe_now"),
        "candidates": portfolio_rows("IF6683-CAND", candidate_titles, "candidate"),
        "skills": skill_rows,
        "runners": runner_rows,
        "clean_fix_refine": portfolio_rows("IF6683-CFR", cfr_titles, "clean_fix_refine"),
        "exact_approval": portfolio_rows("IF6683-EXACT", EXACT_APPROVAL_TITLES, "exact_approval", "exact_approval_unexecuted"),
        "blocked": portfolio_rows("IF6683-BLOCK", BLOCKED_TITLES, "blocked", "blocked_unexecuted"),
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
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "receipt_file_present_in_expected_bounded_location": False,
        "fresh_live_remote_equal_before_lane_creation": True,
        "source_to_final_commits": 3,
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
            "path": f"docs/ilyra-fen/v668-v3/{relative}",
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
                "path": f"docs/ilyra-fen/v668-v3/{relative}",
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
        "inputs": ["Lyren successor practice seed", "current family Index", "Method Flow recurrence guards", "visible proposal chain"],
        "decisions": [
            {"surface": "audiovisual transfer portfolio", "decision": "refine", "reason": "narrow to calibration custody and frame registration; inherited completion credit remains zero"},
            {"surface": "family-current naming", "decision": "reuse", "reason": "preserve ghc-family-* and ghc_family_* compatibility"},
            {"surface": "broad receipt search", "decision": "defer", "reason": "prior wrapper lost attributable output and the exact source gate already passed"},
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
    write_json("method-flow/x1-ledger.json", method_flow_document(now))
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
        ROOT / "scripts" / "ghc_family_ilyra_fen_v668_v3_archive.py",
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v668_v3_x1.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v668_v3_x1.py",
    ]
    missing_code = [str(path.relative_to(ROOT)) for path in code_paths if not path.is_file()]
    if missing_code:
        raise ValueError(f"x1 code allowlist missing: {missing_code}")
    intended_paths = sorted(
        [path.relative_to(ROOT).as_posix() for path in phase_owner_files()]
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
        "self_exclusions": [f"docs/ilyra-fen/v668-v3/x1/x1-manifest.json"],
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
