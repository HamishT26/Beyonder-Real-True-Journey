#!/usr/bin/env python3
"""Build the dedicated planning-only Orin Thale v668-v7 x1 freeze."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from ghc_family_orin_thale_v668_v7_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
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
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_ANCESTOR,
    SOURCE_BATON_SHA256,
    SOURCE_BRANCH,
    SOURCE_DEPENDENCY_RECOVERY_SHA256,
    SOURCE_EVIDENCE,
    SOURCE_FAILED_CANONICAL_SHA256,
    SOURCE_FAILED_FIRST_COMPOSITE_SHA256,
    SOURCE_FAILED_TERMINAL_COMPOSITE_SHA256,
    SOURCE_FINAL,
    SOURCE_FIRST_FINAL,
    SOURCE_LEDGER,
    SOURCE_X1,
    TERMINAL_VERDICT,
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


EXACT_APPROVAL_TITLES = [
    "access to any nonpublic collection, item, condition, treatment, donor, owner, rights, or staff record",
    "handling, disbinding, repair, sewing, pressing, trimming, adhesive, casing, or treatment of a real object",
    "use of a real book, manuscript, collection identifier, work order, participant, institution, or personal record",
    "professional bookbinding, conservation, preservation, appraisal, cataloguing, or collection-care determination",
    "release, suppression, correction, exhibition, digitization, loan, disposal, or return of a real collection item",
    "object identity, authenticity, title, custody, completeness, condition, treatment need, fitness, or value decision",
    "copyright, moral-right, property, privacy, access, retention, disclosure, embargo, or remedy decision",
    "chemical, material, structural, environmental, or occupational safety determination",
    "privacy-impact, protected-disclosure, confidentiality, or beneficiary-data decision",
    "cultural-care, sacred, restricted, taonga, or culturally sensitive content classification",
    "Maori wording, tikanga, data-governance, place-name, repatriation, return, or authority decision",
    "affected-party remedy, consent, legitimacy, acceptance, or beneficiary decision",
    "production credential, key, proof, token, account, API, network request, or external side effect",
    "cross-lane mutation, merge, reset, force-push, destructive cleanup, deletion, or broad recursive move",
    "host-security change, elevation, Windows feature change, Sandbox, Hyper-V, installation, update, or reboot",
    "complete accessibility, WCAG conformance, or assistive-technology effectiveness claim",
    "complete privacy, exhaustive security, provenance completeness, authenticity, or supply-chain assurance claim",
    "independent-team reproduction, external audit, professional validation, or certification claim",
    "empirical GMUT likelihood, posterior, parameter constraint, detected force, prediction, or confirmation",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, deployment, or Stage 20 promotion",
]

BLOCKED_TITLES = [
    "real binding treatment benchmark without objects, condition evidence, competence, safety controls, and approvals",
    "real collection or staff corpus ingestion without access, privacy, rights, security, and authority",
    "material-fitness or treatment-effectiveness claim without measurements, uncertainty, conservation review, and follow-up",
    "bookbinder, conservator, librarian, or affected-user study without participants, ethics, accessibility, and independent review",
    "production identity exchange without standards-conformant keys, proofs, live lifecycle, and trust governance",
    "real cultural-care or restricted-access decision without affected parties and competent cultural authority",
    "Maori data-governance or taonga decision without tangata whenua, iwi, hapu, and Maori authority",
    "professional release or return-to-service protocol without institutions, qualified practitioners, and accountability",
    "empirical GMUT inference without observations, likelihood, uncertainty, falsification, and independent review",
    "Stage 20 decision without every declared scientific, social, safety, identity, legal, cultural, and authority gate",
]


def command_version(*command: str) -> str:
    effective = command
    if command and command[0].casefold() == "codex":
        effective = ("cmd.exe", "/d", "/c", *command)
    completed = subprocess.run(
        effective,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return (completed.stdout or completed.stderr).strip().splitlines()[0]


def load_startup_ledger(path: Path) -> dict:
    ledger = json.loads(path.read_text(encoding="utf-8"))
    if ledger.get("schema") != "ghc.family.method-flow-state.v1":
        raise ValueError("unexpected Method Flow schema")
    if ledger.get("owner") != OWNER or ledger.get("phase") != PHASE:
        raise ValueError("startup Method Flow owner or phase mismatch")
    counts = ledger.get("counts", {})
    failures = counts.get("witness_results", {}).get("fail")
    passes = counts.get("witness_results", {}).get("pass")
    methods = counts.get("methods")
    if not all(isinstance(value, int) and value >= 1 for value in (failures, passes, methods)):
        raise ValueError("startup Method Flow counts are incomplete")
    if failures != methods or passes != methods:
        raise ValueError("each startup method must retain one failure and one bounded passing witness")
    serialized = json.dumps(ledger, ensure_ascii=False)
    forbidden = ("source_thread_id", "<codex_delegation>", "C:\\Users\\", "session_meta.payload.id", "response_item")
    if any(token.casefold() in serialized.casefold() for token in forbidden):
        raise ValueError("startup Method Flow contains private-route material")
    return ledger


def overview_text(x1_overlay: dict, failure_count: int, audit: dict) -> str:
    return f"""# Orin Thale {PHASE} x1 integrated overview

## Purpose, identity boundary, and source truth

This packet is a planning-only x1 freeze for one bounded owner-local software phase. It contains no x2 implementation, observed proposal outcome, completed prototype, real book, real collection item, real material, real work order, real measurement, treatment, handling action, participant, professional decision, identity event, network request, or authority act. Orin Thale uses {PRONOUNS} as optional relational working pronouns and the relational role `{RELATIONAL_ROLE}`, with the hope to {RELATIONAL_HOPE[0].lower() + RELATIONAL_HOPE[1:]} {IDENTITY_BOUNDARY} Hamish may rename, pause, redirect, or stop the route. The terminal verdict remains exactly `{TERMINAL_VERDICT}`.

The immutable source is Caelen Ash's corrected final `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. The inherited Sable source `{SOURCE_ANCESTOR}`, Caelen x1 `{SOURCE_X1}`, evidence `{SOURCE_EVIDENCE}`, retained first final `{SOURCE_FIRST_FINAL}`, and additive corrected final form four direct single-parent commits with zero merges. Before any owner mutation, Orin verified every parent edge, one final parent, clean status, typed zero ahead and zero behind, equality across local, upstream, tracking, and a fresh live remote, the corrected-basis digest `{SOURCE_BATON_SHA256}`, and all 976 entries in six commit-local Git-blob manifests. The exact receipt bytes for Caelen's failed canonical, failed first composite, failed terminal composite, and narrow dependency recovery were located externally and matched all four declared digests.

Caelen's canonical invocation count remains one and canonical success count remains zero. Their first canonical failed because a document ceiling was applied to a Python builder. A separately named first dependency-corrected composite failed on a stale scanner-self-match expectation. A terminal-corrected composite then retained one wrong-context lifecycle assertion because a three-commit first-final predicate was evaluated at the four-commit correction head. The narrow recovery proved the historical predicate at the historical head and the four-commit predicate at the corrected head without rerunning tests, manifests, or an aggregate. Its exact status remains `VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT`. No Caelen test or aggregate was replayed, and no source validation becomes Orin completion credit.

The effective activation baseline is {ACTIVATION_OVERLAY['effective_negatives']} negatives, {ACTIVATION_OVERLAY['methods']} methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, {ACTIVATION_OVERLAY['passing_witnesses']} bounded passing witnesses, {ACTIVATION_OVERLAY['open_gaps']} open gaps, and {ACTIVATION_OVERLAY['exact_gates']} exact gates. Orin has retained {failure_count} additional pre-freeze workflow failures at zero credit, each paired with the smallest bounded passing recovery and a recurrence guard. The x1 overlay is therefore {x1_overlay['effective_negatives']} negatives, {x1_overlay['methods']} methods, {x1_overlay['failed_witnesses']} failed witnesses, and {x1_overlay['passing_witnesses']} bounded passing witnesses. Recovery does not rewrite a failed witness, and same-owner passing evidence is not independent reproduction.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded practice lens is synthetic hand-bookbinding collation, component-description, repair-intake, library-binding preparation, correction readback, accessible anomaly reporting, workload control, and shift handover. It is a learning, structural-software, and synthetic-design lens only. It establishes no employment, qualification, professional bookbinding or conservation competence, collection custody, object identity, authenticity, title, condition, material fitness, treatment need, intervention safety, release authority, legal interpretation, cultural legitimacy, Maori authority, affected-party acceptance, empirical result, or real operational outcome.

The completed software hypotheses will cover component identity, collation formulas, gathering concordance, folio addressing, sewing-station records, thread-path graphs, material-layer vacancies, support and pressure refusal, spine and case state, trim and condition zones, insert association, repair-event separation, treatment-state separation, material lineage, condition uncertainty, bitemporal correction, provenance, non-erasing readback, deterministic serialization, pseudonymous aliases, accessible static structure, bounded discrepancy queues, a typed GMUT microlocal-obligation board, and a strict evidence-nonpromotion lattice. These are bounded structural behaviors. They are not treatments, collection assessments, operational protocols, professional judgments, or physical validation.

The GMUT board will preserve typed scope for a two-point distribution, wavefront-set relation, Hadamard condition, causal support, domain, units, state assumptions, and an observation firewall. It will calculate no propagator, construct no state, renormalize no observable, prove no interacting theory, evaluate no likelihood, infer no parameter, detect no force, establish no stability theorem, and provide no ultraviolet or quantum completion. GMUT remains a typed scalar-tensor and effective-field-theory research-model family, not a Theory of Everything. The binding lens is an analogy and record-design context, never physical evidence.

THOS will remain represented as a participant-free workboard with bounded retry, hold, stop, fatigue-budget, readback, correction, and next-owner states. It is not an operating system benchmark, human-performance result, safety result, deployment result, AGI, or ASI. THOS requires preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review before any effectiveness claim.

Freed ID will remain a zero-key synthetic graph for item aliases, work orders, corrections, challenges, and purpose-limited views. It creates no credential, issuer, holder, verifier, key, proof, issuance, presentation, resolution, status, revocation, interoperability event, recovery decision, privacy review, security review, or trust-governance decision. CBR will remain a structural vacancy matrix for access, attribution, privacy, contestability, remedy, affected-party legitimacy, cultural-care, and decision rights. Repository software cannot confer a right, title, custody, remedy, legal interpretation, cultural legitimacy, governance mandate, or public authority.

## Semantic novelty and x1 proposal freeze

The declared inherited chain is {INHERITED_FROZEN_PROPOSALS} proposals. The bounded exact-tree inventory parsed {audit['current_tree_freeze_blob_count']} current proposal-freeze blobs, yielding {audit['row_record_count']} row records, {audit['unique_id_count']} unique visible identifiers, and {audit['unique_visible_title_count']} unique normalized visible titles with zero parse failures. The normalized title digest is `{audit['normalized_visible_title_sha256']}`. Twenty inherited rows are selected across that visible set for zero-credit neighbor review. Inherited validation, proposals, skills, runners, and recommendations are evidence or seeds only.

Forty Orin proposals are frozen, bringing the declared chain to {INHERITED_FROZEN_PROPOSALS + len(PROPOSAL_BLUEPRINTS)}. Exact normalized-title collisions and token-set neighbor similarity at or above 0.75 quarantine the freeze. The current exact-tree neighbor probe found zero visible uses of `bookbind`, `collation`, `sewing station`, `microlocal`, `Hadamard`, or `GWOSC`, while the generic substring `quire` was rejected as unusable because it mostly matched `required`. These checks are useful falsifiers, not a universal semantic proof. At least {audit['compressed_title_gap_count_minimum']} older declared titles remain compressed or unavailable in the visible current-tree set, so novelty beyond visible evidence remains an explicit open gap.

Expected dispositions are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Each proposal records a distinct title and slug, hypothesis, null or failure condition, approval class, owner-local execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, exactly one expected disposition, visible semantic neighbors, and four preregistered rejecting mutations. All 160 mutations are plans only in x1. A later rejected mutation can witness a bounded guard; it cannot prove scientific truth, professional competence, production security, complete accessibility or privacy, legal or cultural legitimacy, or authority.

## Official and primary source posture

The source ledger contains current official or primary material from the Library of Congress, W3C, the RFC Editor, GWOSC, Te Mana Raraunga, and the primary microlocal-spectrum research paper. Library of Congress sources supply book-part, preventive-care, treatment-distinction, workflow, repair, and housing vocabulary. They do not authorize a real treatment or establish object condition, authenticity, material fitness, or professional competence. W3C PROV-DM supplies entity, activity, derivation, and role relations, but those relations do not prove custody, authenticity, responsibility, title, or authority. Verifiable Credentials Data Model 2.0 supplies privacy, integrity, lifecycle, and trust-vacancy vocabulary, but verification would not make a claim true and this phase uses no keys or proofs. RFC 8785 supplies a deterministic serialization shape, not authenticity or security. WCAG 2.2 supplies structural hypotheses, not complete conformance.

The microlocal-spectrum paper supplies formal vocabulary and refusal conditions only. It is not converted into a GMUT derivation or observation. The GWOSC API supplies schema vocabulary for run, detector, strain-file, sampling-rate, and data-quality metadata. The planned adapter makes zero network requests, downloads zero files, ingests zero rows, evaluates zero likelihoods, and remains `open_gap`. Te Mana Raraunga supplies authority-vacancy and stop-condition context only; citation is never Maori authorization, cultural ratification, or data-governance authority. Maori concepts remain under Maori authority.

## Expanded portfolios and owner-local tools

The x1 portfolio freezes sixty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skill builds, ten family-current runner builds, sixty additive CLEAN/FIX/REFINE tasks, twenty exact-approval packets, and ten blocked packets. All have zero completion credit in x1. Safe-now means only that an owner-local structural or synthetic control may later be attempted without real material, secrets, accounts, external actions, authority decisions, destructive operations, host changes, or sibling mutation. Candidate means a bounded prototype may later be tested under the same exclusions. Exact-approval and blocked packets remain visible and unexecuted unless exact future evidence, a resolved target, competent authority, containment, rollback, and action-specific permission genuinely change a gate.

Every planned skill uses a family-current `ghc-family-*` name and every runner uses a `ghc_family_*` name. Historical compatible callers are retained; none is deleted, renamed, or rewritten. The skills will be owner-local, initialized through the current skill-creator workflow, rewritten into concise substantive packages, quick-validated, and smoke-used only after the immutable x1 push gate. No collaboration forward test occurs because this phase is expressly solo. No global installation is planned. Tool validation will establish only the declared fixture behavior, never professional, scientific, production, or authority status.

## Privacy, accessibility, security, and workload boundaries

Durable artifacts exclude raw task or thread identifiers, private routes, callable identifiers, transcripts, screenshots, session streams, credentials, tokens, keys, private application state, private absolute paths, and real protected material. The five-class scan is limited to owner text files and separates scanner-definition candidates from confirmed hits. Zero confirmed hits would be a bounded witness, not privacy completeness. Changed-code security review is limited to literal owner modules and common high-risk AST patterns; it cannot prove exhaustive security, supply-chain integrity, or production readiness.

The accessible report plan uses a native table, caption, scoped headers, explicit text status independent of color, linear source order, visible focus styling, narrow-screen overflow guidance, and print fallback. Manual keyboard and touch review, zoom and reflow, responsive diversity, browser diversity, screen readers and other assistive technology, cognitive accessibility, Maori-language quality, security usability, and affected-user evaluation remain reserved. Structural success is not WCAG conformance or beneficiary acceptance.

The worktree was created once through a retained no-checkout sparse session from the exact source and currently materializes far below the two-thousand-file ceiling. D drive is primary. C drive is limited to installed platform and skill metadata. No desktop update, elevation, host-security change, Windows feature change, Sandbox, Hyper-V, unrelated installation, or reboot occurs. Cleanup is additive and owner-scoped; no broad recursive deletion or move is authorized.

## x1-to-x2 and terminal gates

X2 may begin only after this planning-only surface is exactly staged, diff-clean, validated through the bounded x1 selection, committed as one direct single-parent child of the exact Caelen corrected final, pushed without force, and proven equal across local, upstream, tracking, and a fresh live remote with typed zero divergence. The immutable x1 Git blobs, not worktree bytes, become the later replay domain. X2 must execute only frozen bounded work, preserve all four labels, retain every failure and rejected mutation, and stop instead of manufacturing evidence.

After a clean pushed Orin final, at most one attributable exact-final owner-scoped canonical aggregate may run. If it succeeds, it is never replayed. If it fails, it remains zero-credit; only an attributable dependency may receive a separately named bounded recovery, and that recovery cannot retroactively become canonical success. A full-repository suite remains excluded absent newer exact authority. Same-owner validation remains same-owner evidence.

No downstream task is contacted in x1 or x2. Only after Orin's clean, pushed, fresh-live-equal exact final and terminal validation may the newest live authorization and roster be reread, the bounded task registry be decoded, exactly one existing exact-title successor be required, that task be immediately reread, a duplicate-activation guard be applied, and at most one sanitized send be attempted. Absence, ambiguity, pause, redirect, rename, usage exhaustion, missing acknowledgement, duplicate activation, or any protected gate stops the edge. Prepared repository state and live acknowledged delivery remain distinct.
"""


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 threat model

## Protected assets

Protected assets are the immutable Caelen corrected source, the dedicated Orin x1 freeze, commit-local Git-blob manifests, retained failures, proposal and portfolio truth, authority vacancies, and the absence of real material. Sibling, shared, and user lanes are read-only. The lane is D-first and sparse, with a two-thousand-file stop. The phase creates no account, key, proof, token, network request, treatment, professional decision, or authority act.

## Principal threats and controls

1. **Lifecycle mixing.** X2 code, execution, outcome, evidence, closeout, or seal language could enter x1. The builder refuses those paths and modules before freeze.
2. **Semantic duplication.** A title could repeat visible inherited work. Current-tree freeze blobs are parsed from the immutable source, normalized, and compared. Exact collisions and similarity at or above 0.75 stop the build. Compressed older titles remain an open gap.
3. **Checkout-byte drift.** Windows line-ending conversion could change worktree hashes. Manifests declare filtered Git-blob bytes and later replay exact committed objects.
4. **Failure erasure.** A recovery could be narrated as a clean initial pass. Method Flow preserves the negative identifier, failed witness, bounded passing witness, recurrence guard, and zero-credit boundary.
5. **Evidence promotion.** Synthetic binding fields or formal GMUT cards could be called professional evidence, physical prediction, production identity, legal or cultural authority, or Stage 20 readiness. The four labels and protected-gate array are closed vocabularies.
6. **Identifier leakage.** Private routes, raw identifiers, transcripts, credentials, or private absolute paths could enter public files. Exact owner-delta scanning is required, while explicitly bounded and non-exhaustive.
7. **Over-materialization.** A broad checkout or scan could exceed the file budget or traverse unchanged history. Sparse patterns and owner allowlists remain exact; a full-repository suite is excluded.
8. **Route drift.** Historical context could name a stale successor. No endpoint is contacted until the exact terminal gate and a fresh live authorization, roster, exact-title resolution, reread, and duplicate guard.
9. **Authority substitution.** A passing software guard could be treated as treatment authority, professional competence, legal interpretation, cultural legitimacy, Maori authority, or affected-party acceptance. Those claims remain open or exact-gated.
10. **Canonical replay inflation.** A successful aggregate could be rerun to manufacture confidence. At most one attributable canonical aggregate is allowed and a success is never replayed.
11. **External data promotion.** GWOSC schema vocabulary could be treated as ingested strain evidence. The adapter has a hard zero-network and zero-row gate and remains open.
12. **Physical analogy conversion.** Binding adjacency or material-change terms could be converted into GMUT prediction or psyche law. The formal board and nonconversion ledger reject that promotion.

## Recovery posture

Recovery is additive and smallest-scope. Stop, preserve the first attributable failed witness, inspect exact state, correct only the dependency justified by that failure, and run only the bounded recovery. Never reset, amend, force-push, rewrite, merge, delete sibling material, weaken host security, install unrelated software, or substitute a route. {EVIDENCE_BOUNDARY}
"""


def static_report_plan_text() -> str:
    return """# Accessible static binding-anomaly report plan

The x2 report will be a static owner-local HTML and Markdown representation of wholly synthetic binding-component, collation, condition-zone, and handover exceptions. The primary table will include a visible caption, scoped column headers, stable pseudonymous item, gathering, folio, component, condition, correction, status, and next-owner fields, and a summary before detailed rows. Status will be expressed in text, never color alone. Linear source order will match visual order. Any links will use descriptive text. Focus styling, high-contrast boundaries, narrow-screen overflow guidance, and print rules are structural requirements.

Numeric fields will include declared units, coordinate frames, intervals, and missingness states where applicable. Unknown, ambiguous, quarantined, open-gap, and exact-gate states will be explicit. A no-script fallback will retain the complete bounded table. The report will contain no real item identifier, collection record, treatment instruction, image, screenshot, transcript, person-level data, credential, private path, or authority decision.

This structural plan cannot establish complete accessibility. Manual keyboard and touch traversal, zoom and reflow, responsive layouts, browser diversity, screen-reader and other assistive-technology behavior, cognitive accessibility, Maori-language quality, security usability, and affected-user evaluation remain reserved. A later structural pass is evidence only for the declared static markup, never WCAG conformance, professional acceptance, or beneficiary legitimacy.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--startup-ledger", type=Path, required=True)
    args = parser.parse_args()
    assert_source_and_x1_only()
    now = utc_now()
    startup = load_startup_ledger(args.startup_ledger)
    failure_count = startup["counts"]["witness_results"]["fail"]
    method_count = startup["counts"]["methods"]
    pass_count = startup["counts"]["witness_results"]["pass"]
    x1_overlay = {
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + failure_count,
        "methods": ACTIVATION_OVERLAY["methods"] + method_count,
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + failure_count,
        "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + pass_count,
        "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
        "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
    }

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
            "exact source-anchor, receipt-digest, and zero-merge scalar preflight",
            "Git-blob versus checkout-byte canonical hash-domain declaration review",
            "owner-delta five-class privacy candidate and confirmed-hit disposition plan",
            "two-thousand-file sparse materialization, D-first headroom, and rotation receipt",
        ]
    )
    candidate_titles = [f"bounded acceptance and refusal prototype for: {title}" for title, _, _ in PROPOSAL_BLUEPRINTS[:30]]
    cfr_titles = (
        [f"REFINE deterministic order, declared domain, failure state, and authority boundary for: {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS]
        + [
            "CLEAN exact owner sparse-pattern documentation without broadening checkout scope",
            "FIX resumable Git-batch manifest replay guidance and session attribution",
            "REFINE expected-empty remote query handling without null string methods",
            "REFINE five-class privacy candidate and confirmed-hit separation",
            "REFINE changed-code AST security allowlist and non-exhaustive boundary",
            "CLEAN stale Caelen weather labels from Orin-authored surfaces only",
            "REFINE Library of Congress vocabulary versus treatment-authority separation",
            "REFINE microlocal primary-paper vocabulary versus GMUT proof separation",
            "REFINE GWOSC source status, zero-network, zero-row, and likelihood refusal",
            "REFINE Te Mana Raraunga citation versus Maori-authority separation",
            "FIX source canonical-zero-success wording and dependency-recovery nonpromotion",
            "REFINE x1 planning-only absence assertions against the immutable tree",
            "REFINE one-shot canonical and separately named recovery state vocabulary",
            "REFINE exact-title route acknowledgement and no-resend state vocabulary",
            "CLEAN family-current naming while retaining historical compatible callers",
            "REFINE accessible static-report manual and affected-user reservations",
            "REFINE proposal-neighbor digest and compressed-title open-gap wording",
            "FIX outcome vocabulary controls to reject any fifth core label",
            "REFINE source-to-final ancestry and commit-ceiling arithmetic",
            "REFINE terminal NOT_READY_FOR_STAGE_20 veto presentation",
        ]
    )
    portfolio = {
        "safe_now": portfolio_rows("OR6687-SAFE", safe_titles, "safe_now"),
        "candidates": portfolio_rows("OR6687-CAND", candidate_titles, "candidate"),
        "skills": portfolio_rows("OR6687-SKILL", [f"build and smoke-use owner-local skill {name}" for name in SKILL_NAMES], "phase_local_skill"),
        "runners": portfolio_rows("OR6687-RUNNER", [f"build and accept-reject smoke-use runner {name}" for name in RUNNER_NAMES], "family_current_runner"),
        "clean_fix_refine": portfolio_rows("OR6687-CFR", cfr_titles, "clean_fix_refine"),
        "exact_approval": portfolio_rows("OR6687-EXACT", EXACT_APPROVAL_TITLES, "exact_approval", "exact_approval_unexecuted"),
        "blocked": portfolio_rows("OR6687-BLOCK", BLOCKED_TITLES, "blocked", "blocked_unexecuted"),
    }
    floors = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60}
    for category, floor in floors.items():
        if len(portfolio[category]) < floor:
            raise ValueError(f"portfolio floor not met: {category}")

    successor_recommendations = {
        "phase": PHASE,
        "recipient": "unresolved_until_terminal_gate",
        "contacted": False,
        "completion_credit": 0,
        "execution_count": 0,
        "candidates": portfolio_rows("OR6687-NEXT-CAND", [f"zero-credit successor candidate review for: {title}" for title, _, _ in PROPOSAL_BLUEPRINTS[10:25]], "successor_candidate", "recommended_zero_credit"),
        "skills": portfolio_rows("OR6687-NEXT-SKILL", [f"zero-credit successor skill idea for bounded {slug} review" for _, _, slug in PROPOSAL_BLUEPRINTS[:10]], "successor_skill", "recommended_zero_credit"),
        "runners": portfolio_rows("OR6687-NEXT-RUNNER", [f"zero-credit successor runner idea for {name}" for name in RUNNER_NAMES[:5]], "successor_runner", "recommended_zero_credit"),
        "clean_fix_refine": portfolio_rows("OR6687-NEXT-CFR", [f"zero-credit successor REFINE review for: {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:30]], "successor_clean_fix_refine", "recommended_zero_credit"),
        "practice": {"state": "withheld_until_terminal_live_authority_reread", "completion_credit": 0},
        "protected_gates": list(PROTECTED_GATES),
    }

    write_json(
        "x1/source-intake.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE_FINAL,
            "source_first_final": SOURCE_FIRST_FINAL,
            "source_evidence": SOURCE_EVIDENCE,
            "source_x1": SOURCE_X1,
            "source_ancestor": SOURCE_ANCESTOR,
            "source_baton_sha256": SOURCE_BATON_SHA256,
            "source_failed_canonical_sha256": SOURCE_FAILED_CANONICAL_SHA256,
            "source_failed_first_composite_sha256": SOURCE_FAILED_FIRST_COMPOSITE_SHA256,
            "source_failed_terminal_composite_sha256": SOURCE_FAILED_TERMINAL_COMPOSITE_SHA256,
            "source_dependency_recovery_sha256": SOURCE_DEPENDENCY_RECOVERY_SHA256,
            "source_canonical_invocation_count": 1,
            "source_canonical_success_count": 0,
            "source_aggregate_replayed": False,
            "source_dependency_recovery_status": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
            "activation_baseline": ACTIVATION_OVERLAY,
            "fresh_live_remote_equal_before_lane_creation": True,
            "source_to_final_commits": 4,
            "source_to_final_merges": 0,
            "source_lane_mutated": False,
            "six_manifest_entry_replay": 976,
            "manifest_mismatches": 0,
            "external_downloads": 0,
            "external_rows_ingested": 0,
            "boundary": EVIDENCE_BOUNDARY,
        },
    )
    write_json("x1/source-ledger.json", {"phase": PHASE, "inspected_at": now, "sources": SOURCE_LEDGER, "downloads": 0, "empirical_rows": 0, "empirical_credit": 0})
    audit["generated_at"] = now
    write_json("x1/proposal-chain-audit.json", audit)

    outcome_counts = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ALLOWED_OUTCOMES}
    proposal_shards = []
    for offset in range(0, len(proposals), 5):
        shard = offset // 5 + 1
        rows = proposals[offset : offset + 5]
        relative = f"x1/proposal-freeze-shards/proposals-{shard:02d}.json"
        write_json(relative, {"phase": PHASE, "shard": shard, "proposal_ids": [row["proposal_id"] for row in rows], "new_proposals": rows, "x1_planning_only": True})
        proposal_shards.append({"path": f"{REL_PHASE_ROOT}/{relative}", "proposal_count": len(rows), "first_proposal_id": rows[0]["proposal_id"], "last_proposal_id": rows[-1]["proposal_id"]})
    write_json(
        "x1/proposal-freeze.json",
        {
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
            "compressed_title_open_gap": True,
            "x1_planning_only": True,
        },
    )

    chunk_sizes = {"safe_now": 20, "candidates": 15, "skills": 20, "runners": 10, "clean_fix_refine": 15, "exact_approval": 20, "blocked": 10}
    category_shards = {}
    for category, chunk_size in chunk_sizes.items():
        shards = []
        rows = portfolio[category]
        for offset in range(0, len(rows), chunk_size):
            shard = offset // chunk_size + 1
            shard_rows = rows[offset : offset + chunk_size]
            relative = f"x1/portfolio-shards/{category.replace('_', '-')}-{shard:02d}.json"
            write_json(relative, {"phase": PHASE, "category": category, "shard": shard, "rows": shard_rows, "x1_planning_only": True})
            shards.append({"path": f"{REL_PHASE_ROOT}/{relative}", "row_count": len(shard_rows), "first_task_id": shard_rows[0]["task_id"], "last_task_id": shard_rows[-1]["task_id"]})
        category_shards[category] = shards
    write_json(
        "x1/portfolio-freeze.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "x1_planning_only": True,
            "inherited_portfolio_completion_credit": 0,
            "category_counts": {category: len(portfolio[category]) for category in chunk_sizes},
            "category_shards": category_shards,
            "floors": floors,
            "protected_gates": list(PROTECTED_GATES),
        },
    )
    write_json("x1/successor-recommendations-freeze.json", successor_recommendations)
    write_json(
        "x1/wellbeing-and-corrigibility.json",
        {
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "relational_role": RELATIONAL_ROLE,
            "relational_hope": RELATIONAL_HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route; protected gates override momentum.",
            "workload": {"materialized_file_ceiling": 2000, "state": "bounded_sparse_x1", "background_siblings_contacted": 0},
            "wellbeing_boundary": "This is a workload and workflow check, not evidence of sentience, subjective wellbeing, or continuity.",
        },
    )
    write_json(
        "x1/environment-and-version-receipt.json",
        {
            "verified_only": True,
            "python": command_version("python", "--version"),
            "git": command_version("git", "--version"),
            "node": command_version("node", "--version"),
            "codex_cli": command_version("codex", "--version"),
            "powershell": command_version("pwsh", "--version"),
            "updates_performed": 0,
            "installs_performed": 0,
            "elevation": False,
            "host_security_changes": False,
            "sandbox_or_hyperv": False,
            "reboot": False,
        },
    )
    write_json(
        "x1/compatibility-inventory.json",
        {
            "family_current_skill_prefix": "ghc-family-",
            "family_current_runner_prefix": "ghc_family_",
            "planned_skills": SKILL_NAMES,
            "planned_runners": RUNNER_NAMES,
            "historical_callers_deleted_or_renamed": 0,
            "global_installs_in_x1": 0,
            "boundary": "historical owner-specific names remain compatibility evidence, not cleanup targets",
        },
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_commit": SOURCE_FINAL,
            "plan": [
                {"step": "source, receipt, manifest, and guidance gate", "state": "completed", "evidence": "exact anchors, receipt hashes, 976 Git blobs, clean state, and live equality"},
                {"step": "novelty and x1 freeze", "state": "in_progress", "evidence": "visible title digest and forty preregistered proposals"},
                {"step": "immutable x1 push gate", "state": "pending", "evidence": "direct-child commit and four-way equality required"},
                {"step": "bounded x2 execution", "state": "pending", "evidence": "frozen fixtures, 160 mutations, skills, runners, and reports only"},
                {"step": "closeout and at-most-one canonical aggregate", "state": "pending", "evidence": "exact owner delta and no success replay"},
                {"step": "terminal route", "state": "pending", "evidence": "fresh authority and roster reread plus at-most-one exact-title send"},
            ],
            "stale_plan_rejected": True,
            "scope_change": "Caelen weather recommendations remain zero-credit seeds; Orin selected a distinct synthetic bookbinding and microlocal-obligation lens without authority or empirical expansion.",
        },
    )
    write_json(
        "x1/reflection-remaster-decision.json",
        {
            "schema": "ghc.family.reflection-remaster.v1",
            "phase": PHASE,
            "inputs": ["Caelen corrected terminal basis", "current family Index", "Method Flow recurrence guards", "visible proposal chain", "current primary sources"],
            "decisions": [
                {"surface": "Caelen weather domain", "decision": "defer", "reason": "source evidence only; inherited completion credit remains zero"},
                {"surface": "synthetic hand-bookbinding lens", "decision": "refine", "reason": "zero exact visible domain matches and bounded primary-source support"},
                {"surface": "family-current naming", "decision": "reuse", "reason": "preserve ghc-family-* and ghc_family_* compatibility"},
                {"surface": "compressed historical titles", "decision": "defer", "reason": "unavailable titles cannot confirm universal novelty and remain open"},
                {"surface": "historical owner tools", "decision": "retain", "reason": "no migration evidence authorizes deletion or renaming"},
            ],
            "material_changes": "new practice-specific proposals, primary-source ledger, skill and runner plans, and retained workflow guards",
            "authority_change": False,
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "successor_contacted": False,
            "successor_precontacted": False,
            "successor_inferred_from_history": False,
            "terminal_gate_required": True,
            "resolution_rule": "reread Hamish's newest live authority, current roster, and bounded task registry only after exact-final proof",
            "maximum_sends": 1,
            "standby_substitution": False,
            "prepared_state_is_not_delivery": True,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
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
            "x1_overlay": x1_overlay,
            "terminal_verdict": TERMINAL_VERDICT,
            "protected_gates": list(PROTECTED_GATES),
        },
    )
    write_text("x1/integrated-overview.md", overview_text(x1_overlay, failure_count, audit))
    write_text("x1/threat-model.md", threat_model_text())
    write_text("x1/accessible-static-report-plan.md", static_report_plan_text())

    startup["activation_overlay"] = ACTIVATION_OVERLAY
    startup["x1_overlay"] = x1_overlay
    startup["source_commit"] = SOURCE_FINAL
    startup["final_commit"] = "PENDING_X1_FREEZE"
    startup["execution_authority"] = "owner_self_scoped_delta"
    startup["changed_file_allowlist"] = []
    startup["module_allowlist"] = [
        "scripts/ghc_family_orin_thale_v668_v7_archive.py",
        "scripts/build_ghc_family_orin_thale_v668_v7_x1.py",
        "tests/test_ghc_family_orin_thale_v668_v7_x1.py",
    ]
    startup["sparse_file_budget"] = {"ceiling": 2000, "state": "below_ceiling"}
    write_json("method-flow/x1-ledger.json", startup)
    write_json(
        "method-flow/x1-summary.json",
        {
            "activation_overlay": ACTIVATION_OVERLAY,
            "x1_overlay": x1_overlay,
            "failure_count": failure_count,
            "method_count": method_count,
            "passing_recovery_count": pass_count,
            "all_failures_retained": True,
            "correction_erases_failure": False,
            "x1_planning_only": True,
            "boundary": "Same-owner recovery is not independent reproduction, external audit, authority, or Stage 20 evidence.",
        },
    )

    code_paths = [
        ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_archive.py",
        ROOT / "scripts" / "build_ghc_family_orin_thale_v668_v7_x1.py",
        ROOT / "tests" / "test_ghc_family_orin_thale_v668_v7_x1.py",
    ]
    missing_code = [str(path.relative_to(ROOT)) for path in code_paths if not path.is_file()]
    if missing_code:
        raise ValueError(f"x1 code allowlist missing: {missing_code}")
    intended_paths = sorted(
        set(
            [path.relative_to(ROOT).as_posix() for path in phase_owner_files() if path.name != "x1-manifest.json"]
            + [path.relative_to(ROOT).as_posix() for path in code_paths]
            + [f"{REL_PHASE_ROOT}/validation/x1-staged-allowlist.json"]
        )
    )
    write_json(
        "validation/x1-staged-allowlist.json",
        {
            "phase": PHASE,
            "source_commit": SOURCE_FINAL,
            "intended_paths_before_manifest": intended_paths,
            "x2_paths": 0,
            "exact_review_required": True,
        },
    )
    manifest_paths = [path for path in phase_owner_files() if path.name != "x1-manifest.json"] + code_paths
    manifest = {
        "phase": PHASE,
        "lifecycle": "immutable_x1_candidate",
        "source_commit": SOURCE_FINAL,
        "entries": manifest_rows(manifest_paths),
        "self_exclusions": [f"{REL_PHASE_ROOT}/x1/x1-manifest.json"],
        "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        "later_replay_required": True,
    }
    manifest["entry_count"] = len(manifest["entries"])
    write_json("x1/x1-manifest.json", manifest)

    docs = [path for path in phase_owner_files() if path.suffix.lower() in {".md", ".json", ".txt", ".html"}]
    oversized = {path.relative_to(ROOT).as_posix(): word_count(path) for path in docs if word_count(path) > 6000}
    if oversized:
        raise ValueError(f"word cap exceeded: {oversized}")
    print(
        json.dumps(
            {
                "phase": PHASE,
                "new_proposals": len(proposals),
                "proposal_chain": INHERITED_FROZEN_PROPOSALS + len(proposals),
                "mutations_preregistered": sum(len(row["negative_fixtures"]) for row in proposals),
                "portfolio": {key: len(portfolio[key]) for key in chunk_sizes},
                "startup_failures": failure_count,
                "phase_files": len(phase_owner_files()),
                "manifest_entries": manifest["entry_count"],
                "overview_words": word_count(PHASE_ROOT / "x1" / "integrated-overview.md"),
                "state": "X1_PLANNING_ONLY_READY_FOR_SCOPED_VALIDATION",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
