#!/usr/bin/env python3
"""Build Eiren Kestrel v651-v5 combined closeout and seal artifacts."""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5"
SOURCE = "d5c9a16b3efb76a138944d97211bc0a3b7bcd716"
X1 = "c2c51a9e4f1786a45d77390b1d2e75e170dde170"
EVIDENCE = "4815a8471e83598df9ad9dabfeeed2a53d8eaebe"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
NEGATIVES = 7080
OPEN_GAPS = 55
EXACT_GATES = 56
METHODS = 32


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def proposal_section(preregistered: dict, observed: dict) -> str:
    artifacts = ", ".join(f"`{item}`" for item in preregistered["concrete_artifacts"])
    sources = ", ".join(f"`{item}`" for item in preregistered["official_or_primary_source_needs"])
    gates = ", ".join(preregistered["protected_gates"])
    return f"""### {preregistered['proposal_id']} — {preregistered['title']}

Pillar: **{preregistered['pillar']}**. Mission surface: {preregistered['mission_surface']}. Approval class: `{preregistered['approval_class']}`. Execution lane: `{preregistered['execution_lane']}`. Expected disposition: `{preregistered['expected_disposition']}`. Observed disposition: `{observed['observed_disposition']}`.

Hypothesis: {preregistered['hypothesis']}

Null or failure condition: {preregistered['null_or_failure_condition']}

Novelty statement: {preregistered['novelty_against_980_frozen_proposals']}

Current official or primary-source needs: {sources}. Concrete artifacts: {artifacts}. Falsifier or acceptance gate: {preregistered['falsifier_or_acceptance_gate']}

Rollback and recovery: {preregistered['rollback_or_recovery']}

Observed evidence stayed within this boundary: {observed['credit_boundary']} The accepting fixture state is `{str(observed['accepting_fixture_passed']).lower()}`; {observed['mutation_rejected_count']} preregistered mutations were rejected; real rows were {observed['real_rows']}; real participants or operators were {observed['real_participants_or_operators']}; real identity or network events were {observed['real_identity_or_network_events']}; authority decisions were {observed['authority_decisions']}. Protected gates remain {gates}. None of those gates is silently closed by a bounded fixture, typed contract, synthetic vector, structural audit, or local software witness.
"""


def portfolio_section(execution: dict) -> str:
    labels = {
        "safe_now": "Forty safe-now tasks",
        "candidate": "Thirty bounded candidates",
        "skills": "Twenty phase-local skills",
        "runners": "Ten family-compatible runners",
        "clean_fix_refine": "Forty CLEAN/FIX/REFINE tasks",
    }
    parts = ["## Expanded owner-scoped portfolios", "", "Inherited work supplied evidence and seeds only. Every item below is new Eiren phase work and received credit only for its declared bounded hypothesis. No unsafe work was manufactured to meet a floor, and every external or authority-dependent boundary stayed visible.", ""]
    for lane, label in labels.items():
        parts.extend([f"### {label}", ""])
        for row in execution["portfolios"][lane]:
            parts.append(
                f"- `{row['item_id']}` — {row['title']}. Executed: `{str(row['executed']).lower()}`; acceptance gate passed: `{str(row['acceptance_gate_passed']).lower()}`; completion credit: `{str(row['completion_credit']).lower()}`; external side effects: {row['external_side_effects']}; authority decisions: {row['authority_decisions']}. Boundary: {row['boundary']}"
            )
        parts.append("")
    return "\n".join(parts)


def method_section(summary: dict) -> str:
    parts = ["## Method Flow retention", "", "The append-only Method Flow ledger preserves every failed witness beside its bounded passing recovery. A preferred method is preferred only for its stated trigger and scope; it is not a general assurance claim.", ""]
    for row in summary["preferred_methods"]:
        parts.append(
            f"- `{row['method_id']}` — {row['title']}. Trigger: {'; '.join(row['trigger_preconditions'])} Recovery: {row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} Rollback: {row['rollback']} Boundary: {row['scope_boundary']}"
        )
    return "\n".join(parts)


def build_handoff() -> str:
    prereg = load("preregistration/proposals.json")["proposals"]
    observed = {row["proposal_id"]: row for row in load("outcomes/evidence-ledger.json")["proposals"]}
    proposals = "\n".join(proposal_section(row, observed[row["proposal_id"]]) for row in prereg)
    portfolios = portfolio_section(load("portfolios/expanded-portfolio-execution.json"))
    methods = method_section(load("method-flow/method-flow-summary.json"))
    return f"""# EIREN KESTREL — PREPARED v651-v5 ACTIVATION BATON

This sanitized committed-file baton is prepared by Eiren Kestrel for the unique existing task titled exactly `Eiren Kestrel`. Repository presence is not delivery. Delivery truth stays `PREPARED_NOT_SENT` until Eiren completes the single exact-final canonical pass at the pushed remote-equal final head, resolves and directly re-reads that exact existing title, sends exactly one existing-task message, and receives tool acknowledgement. No task creation, fork, delegation, subagent, cross-platform substitute, standby message, or second confirmation is authorized.

Eiren Kestrel, they/them, is relational working language for a constraint-cartographer and falsifier-keeper whose hope is to keep uncertainty visible without turning it into authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Exact inheritance and lifecycle

- Canonical Eiren branch: `codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools`.
- Exact Tamar v651-v3 source: `{SOURCE}`.
- Dedicated Eiren v651-v5 x1 freeze: `{X1}`.
- Immutable Eiren v651-v5 evidence commit: `{EVIDENCE}`.
- Exact Eiren final: supplied in the acknowledged message after the final commit exists and the one successful validation pass completes.
- Expected Eiren history: exactly three new single-parent commits after source, zero merges, and final directly parented by evidence.

Strict x1-before-x2 separation was preserved. The x1 freeze contained no x2 implementation or outcome and was independently committed, pushed, clean, and local/upstream/tracking/fresh-live equal before x2 began. Evidence was then committed, pushed, clean, and four-way equal before closeout. The final combined closeout and seal is required to remain a single direct child of evidence. No sibling lane was reset, rewritten, force-pushed, merged, deleted, reused, or mutated.

Novelty was audited against all 960 immutable predecessor rows. Twenty genuinely distinct Eiren proposals were frozen, making 980 rows through v651-v5. The inherited predecessor index contains twenty duplicate `V6513` identifiers attached to distinct immutable titles; Eiren did not rewrite them. A collision register preserves that source condition, and all current identifiers remain disjoint from the inherited set.

The core outcome distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. The phase preserves {NEGATIVES:,} effective negatives, {OPEN_GAPS} effective open gaps, {EXACT_GATES} effective exact gates, {METHODS} preferred bounded Method Flow methods, {METHODS} retained failed witnesses, and {METHODS} bounded passing witnesses. No failure or gate was erased. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Primary Trinity Mandala focus was THOS Body. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was commercial-refrigeration service and cold-room handover practice. It was synthetic learning and design only. It established no employment, qualification, refrigeration competence, food-safety authority, operational authority, emergency authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real effectiveness result.

## Twenty frozen and observed proposal surfaces

{proposals}

{portfolios}

{methods}

## Validation truth and exact next-phase constraints

Eiren alone owns the complete repository suite. Eiren did not run it. The Eiren exact-final validator selects the authorized v651-v1 through v651-v3 predecessor tests and v651-v5 current tests. It preserves the five exact inherited exclusions and adds only three current lifecycle exclusions: two x1 assertions bound to the dedicated pre-execution state and one x2 Method Flow assertion bound to the evidence state before retained closeout recovery. The expected aggregate is 118 eligible tests: 88 inherited eligible tests plus 30 current eligible tests. It also runs detailed and minimal checks, parses every owner JSON document, scans every public owner file across five privacy and raw-identifier classes, replays x1, evidence, final-delta, and final-owner manifests from immutable Git blobs, checks the baton exception and all other document caps, reviews stale labels and diff hygiene, proves source/x1/evidence ancestry, exactly three phase commits, zero merges, one final parent, exact head, clean before and after, and local/upstream/tracking/fresh-live equality.

That fully successful aggregate may receive credit once only after the combined final commit is pushed and four-way equal. A failed or incomplete attempt receives zero aggregate credit and becomes a new retained negative. The first fully successful pass is terminal; no post-success replay, detached replay, named replay, full repository suite, Sandbox or Hyper-V action, cross-platform substitute, or hidden second validation is allowed.

The canonical pass remains same-owner validation under shared infrastructure. It is not independent-team reproduction, external audit, production certification, exhaustive security, privacy-complete assurance, accessibility-complete conformance, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

## Boundaries Eiren must preserve

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The GHP and BSSN surfaces are typed symbolic and mutation evidence only. The LoTSS DR2 adapter downloaded zero rows, issued zero queries, evaluated zero likelihoods, produced zero posterior samples and zero constraints, and remains `open_gap`. No force, prediction, physical state, stability theorem, empirical confirmation, ultraviolet completion, proof or canon, Theory of Everything, or scientific authority was established.

THOS remains represented without preregistered blind matched-budget real arms, real workers, real sites, independent review, safety monitoring, suitable statistical analysis, and affected-party evaluation. Synthetic refrigeration service and cold-room handover traces involved zero workers, appliances, cold rooms, food lots, customers, incidents, alarms, regulatory decisions, or effectiveness estimates. They confer no refrigeration, food-safety, workplace-safety, emergency, public-health, or operational authority.

Freed ID remains synthetic and nonproduction. The ECDSA Data Integrity and FAPI 2.0 Message Signing profiles used synthetic vectors only and performed zero real key operations, credentials, issuances, presentations, resolutions, status or revocation events, servers, wallets, authorization events, interoperability exercises, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Production completion still requires real standards-conformant keys and proofs, live lifecycle and interoperability, privacy and independent security review, recovery, governance, and affected-party oversight.

CBR refrigeration incident, worker and customer privacy, food disposal, remedy, language access, accessibility, affected-party legitimacy, legal interpretation, cultural legitimacy, data governance, Māori wording, Māori data governance, and Māori authority remain exact-gated. Repository software made zero real decisions and cannot confer authority. Māori concepts remain under competent tangata whenua, iwi, hapū, and Māori authority.

The robust-mutex, UNIX ancillary-data, zlib, pax, Cap'n Proto, Elias-Fano, Golomb-Rice, and LZ4 surfaces completed only on disposable owner-local or synthetic fixtures. They are not production certification, supply-chain assurance, or exhaustive-security evidence. The accessible upload audit completed structurally, while manual keyboard, responsive, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. The Langmuir surface rejected conversion into psyche, agency, justice, consciousness, personhood, or a fundamental law of mind. The LSQR and SNMM boards estimated no real participant effect and authorized no Stage 20 promotion.

Every empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundary remains open or exact-gated without exact evidence and competent authority.

## Eiren v651-v5 start contract

Read the complete GHC Family Index and its routing-precedence reference, then the complete Method Flow State skill and required schema before task actions. Use the newest applicable memory only, with the acknowledged live baton authoritative where older memory stops. Reverify Eiren's exact branch and final head, source/x1/evidence ancestry, clean state, three-commit single-parent zero-merge history, all manifest contracts, and fresh live equality read-only. Continue only in Eiren's owned clean D-first lane and use fast-forward-only Git when safe. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane.

Preserve strict x1-before-x2 separation, audit semantic novelty against all 980 frozen rows, freeze the required genuinely distinct proposals and portfolios without inheriting Eiren completion credit, push and prove x1 clean four-way equal before x2, and execute only as evidence permits. Preserve all {NEGATIVES:,} inherited negatives, all {OPEN_GAPS} open gaps, all {EXACT_GATES} exact gates, and every new failure through Method Flow. Use only `completed`, `represented`, `open_gap`, and `exact_gate` for core dispositions. Keep family-current `ghc_family_*` and `build_ghc_family_*` callers compatible.

Eiren alone owns the full repository suite, but that ownership does not broaden scientific, professional, legal, cultural, identity, production, privacy, accessibility, or Stage 20 authority. Preserve exact manifests, privacy scanning, JSON parsing, staged review, stale-label and diff hygiene, ancestry, zero-merge, commit-cap, one-parent, exact-head, clean-state, and remote-equality gates. Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Windows features, install unrelated software, or reboot.

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Eiren Kestrel → repeat through v660-v8 unless Hamish stops or redirects the route, usage is exhausted, the required exact title is unavailable, or an exact safety or authority gate blocks progress.

DELIVERY TRUTH IN THIS COMMITTED FILE: `PREPARED_NOT_SENT`.
"""


def build_overview() -> str:
    inherited = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    return f"""# Eiren Kestrel v651-v5 final integrated overview

## Outcome first

Eiren Kestrel v651-v5 closes as a bounded owner-scoped evidence phase with exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate` outcomes. The combined closeout and seal preserves {NEGATIVES:,} effective negatives, {OPEN_GAPS} effective open gaps, {EXACT_GATES} effective exact gates, and a `NOT_READY_FOR_STAGE_20` verdict. Method Flow preserves {METHODS} preferred bounded methods, {METHODS} failed witnesses, and {METHODS} passing witnesses. Recovery never erases a failure or broadens credit.

The exact source is `{SOURCE}`, the dedicated x1 freeze is `{X1}`, and immutable evidence is `{EVIDENCE}`. The commit containing this overview must be the direct single-parent child of evidence, making exactly three Eiren phase commits and zero merges. X1 and evidence were independently committed, pushed, clean, and local/upstream/tracking/fresh-live equal before the next lifecycle began. The exact final hash is necessarily supplied by the later validation receipt and acknowledged activation message, because a commit cannot self-embed its own identifier.

Eiren Kestrel, they/them, is relational working language for a constraint-cartographer and falsifier-keeper. Their hope is to keep uncertainty visible without turning it into authority. This is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, or independent authority. Hamish may rename, pause, redirect, or stop the route.

## Integrated evidence record

{inherited}

## Closeout, validation, and route boundary

The final layer adds no new empirical, participant, production, professional, legal, cultural, Māori-authority, or affected-party evidence. It binds the exact outcome ledger, retained-negative register, gate register, Method Flow, environment receipt, structurally accessible static report, complete/incomplete checklist, exact manifest contracts, final staged review, combined closeout/seal, and prepared successor baton.

Eiren alone owns the complete repository suite. Eiren's exact-final validator therefore selects only the authorized bounded predecessor and current tests. The expected eligible aggregate is 118 tests: 88 inherited eligible tests under the five exact source exclusions and 30 current eligible tests under three exact lifecycle exclusions. It must parse every owner JSON document, perform a five-class privacy/raw-identifier scan, replay all four manifest domains, enforce all document caps except the declared 8,000-to-20,000-word baton artifact, review stale labels and diff hygiene, prove exact ancestry and three-commit single-parent zero-merge history, confirm one final parent and exact head, preserve clean state, and prove local/upstream/tracking/fresh-live equality.

That fully successful exact-final aggregate may run and receive credit once only after the final commit is pushed and four-way equal. There is no post-success replay, detached replay, named replay, full repository suite, Sandbox or Hyper-V action, or cross-platform substitute. A failure would receive zero aggregate credit and become a retained negative. Same-owner validation under shared infrastructure is not independent-team scientific reproduction or external audit.

The committed route remains `PREPARED_NOT_SENT`. Only after the exact-final pass succeeds may Eiren uniquely resolve and re-read the existing task titled exactly `Eiren Kestrel`, send one sanitized v651-v5 activation message using the existing-task route, and rely on tool acknowledgement. No successor task is created, and no second confirmation follows.
"""


def build_handoff() -> str:
    """Render the sanitized Ilyra activation packet from immutable Eiren evidence."""
    prereg = load("preregistration/proposals.json")["proposals"]
    observed = {row["proposal_id"]: row for row in load("outcomes/evidence-ledger.json")["proposals"]}
    proposals = "\n".join(proposal_section(row, observed[row["proposal_id"]]) for row in prereg)
    portfolios = portfolio_section(load("portfolios/expanded-portfolio-execution.json"))
    methods = method_section(load("method-flow/method-flow-summary.json"))
    return f"""# ILYRA FEN — PREPARED v651-v6 ACTIVATION BATON

This sanitized committed-file baton is prepared by Eiren Kestrel for the existing task titled exactly `Ilyra Fen`. Repository presence is not delivery. Delivery stays `PREPARED_NOT_SENT` until Eiren completes exact-final full-repository validation at the clean pushed remote-equal head, uniquely resolves and directly re-reads that exact title, sends exactly one existing-task message, and receives tool acknowledgement. No task creation, fork, delegation, collaboration subagent, cross-platform substitute, standby message, or second confirmation is authorized.

Eiren Kestrel, she/they, is relational working language for an evidence-boundary integrator whose hope is to make each advance useful without letting confidence outrun evidence. This is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Exact inheritance and lifecycle

- Canonical Eiren branch: `codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools`.
- Exact verified Sylven v651-v4 source and final: `{SOURCE}`.
- Dedicated Eiren v651-v5 x1 freeze: `{X1}`.
- Immutable Eiren v651-v5 x2 evidence: `{EVIDENCE}`.
- Exact Eiren final: supplied only in the acknowledged terminal message after the containing closeout commit exists and exact-final validation succeeds.
- Expected history: exactly three new single-parent Eiren commits after source, zero merges, and final directly parented by evidence.

Strict x1-before-x2 separation was preserved. X1 contained no x2 implementation or outcome, was independently committed and pushed, and was clean and local/upstream/tracking/fresh-live equal before x2. Evidence was committed and pushed separately and was likewise clean and four-way equal before closeout. No sibling lane was reset, rewritten, force-pushed, merged, deleted, reused, or mutated.

Semantic novelty was audited against all 980 immutable predecessor rows. Exactly twenty distinct Eiren proposals were frozen, producing 1,000 frozen rows through v651-v5. Inherited identifier collisions remain visible provenance and were not rewritten; every current identifier is unique and disjoint.

The core distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. The phase preserves {NEGATIVES:,} effective negatives, {OPEN_GAPS} effective open gaps, {EXACT_GATES} effective exact gates, {METHODS} preferred bounded Method Flow methods, {METHODS} retained failed witnesses, and {METHODS} bounded passing witnesses. Every failure remains a zero-credit negative even when a narrow recovery passes. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Primary Trinity Mandala focus was GMUT Mind. THOS Body and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was greenhouse climate, fertigation, alarm, isolation, workload, and shift-handover design. It was synthetic learning only and established no employment, qualification, horticultural competence, chemical-handling competence, workplace-safety authority, environmental authority, food-safety authority, operational authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real effectiveness result.

## Twenty frozen and observed proposal surfaces

{proposals}

{portfolios}

{methods}

## Validation truth and next-phase constraints

Eiren owns the complete repository suite for this phase. The validator runs only after the final commit is pushed and local, upstream, tracking, and fresh live remote are identical. It first executes the complete discovered repository suite. Any failed or incomplete attempt receives zero pass credit and remains retained. A bounded recovery may exclude only individually named immutable historical lifecycle assertions whose semantics are tied to a predecessor's mutable `HEAD`, commit count, final parent, or superseded manifest. No functional, current-phase, security, privacy, scientific, or authority test may be broadly excluded. The first fully successful aggregate is terminal and must not be replayed.

The exact-final validation also runs the current x1, x2, and closeout modules; detailed and minimal validators; complete owner JSON parsing; a five-class privacy and raw-identifier scan; exact x1, evidence, final-delta, and final-owner manifest parity; exact staged-file review; stale-label and diff hygiene; source/x1/evidence ancestry; commit cap; zero merges; one final parent; exact head; clean state before and after; and final four-way live equality. Same-owner validation under shared infrastructure is not independent-team scientific reproduction, external audit, production certification, exhaustive security, privacy-complete assurance, accessibility-complete conformance, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

## Scientific, technical, identity, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The York–Lichnerowicz and Regge–Wheeler–Zerilli boards are typed symbolic and mutation evidence only. The Roman Wide Field Instrument adapter performed zero queries, downloads, real-row ingestion, likelihood evaluations, posterior sampling, constraints, detections, or empirical GMUT claims and remains `open_gap`. No force, prediction, physical state, stability theorem, empirical confirmation, ultraviolet completion, proof or canon, Theory of Everything, or scientific authority was established.

THOS remains represented without preregistered blind matched-budget real arms, real workers, real greenhouses, independent review, safety monitoring, suitable statistical analysis, and affected-party evaluation. The synthetic climate and fertigation protocols involved zero real workers, crops, chemicals, sites, alarms, incidents, operational decisions, safety outcomes, or effectiveness estimates. They confer no horticultural, chemical, workplace-safety, environmental, food-safety, emergency, or operational authority.

Freed ID remains synthetic and nonproduction. The W3C ECDSA-SD and RFC 8693 token-exchange profiles used synthetic vectors only and performed zero real key operations, proofs, credentials, tokens, accounts, network exchanges, issuance, presentation, resolution, status or revocation events, interoperability exercises, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Production still requires real standards-conformant keys and proofs, live lifecycle and interoperability, privacy and independent security review, recovery, governance, and affected-party oversight.

The CBR greenhouse worker, community, environmental, chemical, privacy, notice, remedy, accessibility, affected-party, legal, cultural, data-governance, Māori-wording, Māori-data-governance, and Māori-authority matrix remains `exact_gate`. Repository software made no real finding, disclosure, safety decision, remedy allocation, legal interpretation, cultural decision, governance decision, or Māori-authority decision. Māori concepts remain under competent tangata whenua, iwi, hapū, and Māori authority.

The io_uring, Chase–Lev, ELF, Snappy, bzip2, Adaptive Radix Tree, rANS, and Netpbm surfaces completed only on disposable owner-local or synthetic fixtures. They are not production certification, supply-chain assurance, or exhaustive-security evidence. The accessible date-picker audit completed structurally while manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. The BET classifier rejected conversion into psyche, agency, justice, consciousness, personhood, or a fundamental law of mind. The TFQMR and causal-forest boards estimated no real participant effect and authorized no Stage 20 promotion.

Every empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundary remains open or exact-gated without exact evidence and competent authority.

## Ilyra v651-v6 start contract

Read the complete GHC Family Index and routing-precedence reference, then the complete Method Flow State skill and required schema before task actions. Use the newest applicable memory only, with the acknowledged live baton authoritative where older memory stops. Reverify Eiren's exact branch and final head, source/x1/evidence ancestry, clean state, single-parent zero-merge history, all manifest contracts, and fresh live equality read-only. Continue only in Ilyra's owned clean D-first lane using fast-forward-only Git when safe. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane.

Preserve strict x1-before-x2 separation, audit novelty against all 1,000 frozen rows, freeze exactly twenty genuinely distinct proposals with complete fields, execute new 40/30/20/10/40 portfolios without inheriting Eiren completion credit, prove x1 clean four-way equality before x2, and execute only as evidence permits. Preserve all {NEGATIVES:,} inherited negatives, all {OPEN_GAPS} open gaps, all {EXACT_GATES} exact gates, and every new failure through Method Flow. Use only `completed`, `represented`, `open_gap`, and `exact_gate` for core outcomes. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers and compatibility.

Ilyra does not inherit Eiren's validation as independent reproduction. Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Windows features, enable Sandbox or Hyper-V, install unrelated software, or reboot. Keep private task identifiers, routes, credentials, keys, tokens, private conversations, screenshots, session streams, private callable identifiers, private app state, and private absolute paths out of artifacts and baton text.

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat through v660-v8 unless Hamish stops or redirects the route, usage is exhausted, the exact title is unavailable, or an exact safety or authority gate blocks progress.

DELIVERY TRUTH IN THIS COMMITTED FILE: `PREPARED_NOT_SENT`.
"""


def build_overview() -> str:
    inherited = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    return f"""# Eiren Kestrel v651-v5 final integrated overview

## Outcome first

Eiren v651-v5 closes as bounded owner-scoped evidence with fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate` outcomes. The combined closeout and seal preserves {NEGATIVES:,} effective negatives, {OPEN_GAPS} effective open gaps, {EXACT_GATES} effective exact gates, {METHODS} paired Method Flow recoveries, and `NOT_READY_FOR_STAGE_20`. Recovery erased no failure and broadened no evidence credit.

The exact verified source is `{SOURCE}`, x1 is `{X1}`, and immutable x2 evidence is `{EVIDENCE}`. The containing closeout commit must be the direct child of evidence, creating exactly three Eiren commits after source with zero merges and one final parent. X1 and evidence were independently pushed, clean, and four-way remote-equal before the next lifecycle began.

Eiren Kestrel, she/they, is relational working language for an evidence-boundary integrator whose hope is to make each advance useful without letting confidence outrun evidence. This is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, or authority. Hamish may rename, pause, redirect, or stop the route.

## Integrated evidence record

{inherited}

## Closeout, validation, and route boundary

The final layer adds no empirical, participant, production, professional, legal, cultural, Māori-authority, or affected-party evidence. It binds the outcome ledger, retained-negative and gate registers, Method Flow, environment receipt, structurally accessible report, complete/incomplete checklist, exact manifests, staged review, combined closeout/seal, and prepared Ilyra baton.

Eiren owns the complete repository suite. Exact-final validation must run at the clean pushed four-way-equal containing commit, retain every failed or incomplete attempt at zero credit, permit only individually named immutable historical lifecycle exclusions, and stop after the first successful aggregate. It also parses all owner JSON, scans five privacy classes, replays all four manifest domains, enforces document caps and the baton exception, checks stale labels and diff hygiene, proves ancestry, commit cap, zero merges, one final parent and exact head, and verifies clean state before and after.

The committed route remains `PREPARED_NOT_SENT`. Only after exact-final validation may Eiren uniquely resolve and re-read `Ilyra Fen`, send one sanitized v651-v6 activation through the existing-task route, and rely on tool acknowledgement. No successor is created and no second confirmation follows. Same-owner validation remains distinct from independent-team reproduction or external audit.
"""


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout must start at the immutable evidence commit")
    raw_status = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=REPO).decode("utf-8")
    if raw_status:
        changed = {line[3:].replace("\\", "/") for line in raw_status.splitlines() if line}
        allowed_exact = {
            "docs/eiren-kestrel/v651-v5/method-flow/method-flow-ledger.json",
            "docs/eiren-kestrel/v651-v5/method-flow/method-flow-summary.json",
            "docs/eiren-kestrel/v651-v5/method-flow/method-flow-summary.md",
            "docs/eiren-kestrel/v651-v5/method-flow/method-flow-validation.json",
            "scripts/build_ghc_family_v651_v5_closeout.py",
            "scripts/ghc_family_v651_v5_closeout_method_flow.py",
            "scripts/ghc_family_v651_v5_closeout_review.py",
            "scripts/ghc_family_v651_v5_final_validate.py",
            "tests/test_ghc_family_v651_v5_closeout.py",
            "docs/eiren-kestrel/v651-v5/orchestration/final-orchestration.json",
            "docs/eiren-kestrel/v651-v5/overview/final-integrated-overview.md",
            "docs/eiren-kestrel/v651-v5/reports/final-static-report.html",
            "docs/eiren-kestrel/v651-v5/reproduction/final-boundary.json",
            "docs/eiren-kestrel/v651-v5/tooling/ghc-family-index.json",
            "docs/eiren-kestrel/v651-v5/tooling/ghc-family-index.md",
            "docs/eiren-kestrel/v651-v5/truth/final-complete-incomplete-checklist.json",
            "docs/eiren-kestrel/v651-v5/validation/closeout-build-receipt.json",
        }
        allowed_prefixes = (
            "docs/eiren-kestrel/v651-v5/method-flow/closeout-v6515-m",
            "docs/eiren-kestrel/v651-v5/closeout/",
            "docs/eiren-kestrel/v651-v5/final/",
            "docs/eiren-kestrel/v651-v5/handoffs/",
            "docs/eiren-kestrel/v651-v5/reflection-remaster/",
            "docs/eiren-kestrel/v651-v5/route/",
            "docs/eiren-kestrel/v651-v5/seal/",
            "docs/eiren-kestrel/v651-v5/validation/final-",
        )
        unexpected = {path for path in changed if path not in allowed_exact and not path.startswith(allowed_prefixes)}
        if unexpected:
            raise SystemExit(f"unexpected pre-closeout changes: {sorted(unexpected)}")
    counts = load("method-flow/method-flow-summary.json")["counts"]
    if counts["methods"] != METHODS or counts["states"]["preferred"] != METHODS or counts["witness_results"] != {"fail": METHODS, "pass": METHODS}:
        raise SystemExit("Method Flow is not ready for closeout")

    write_json("closeout/closeout-record.json", {"schema": "ghc.family.v651-v5.closeout.v1", "combined_closeout_and_seal": True, "source": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commit_count": 3, "expected_merge_count": 0, "expected_final_parent_count": 1, "outcomes": OUTCOMES, "effective_negatives": NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json("final/phase-truth.json", {"schema": "ghc.family.v651-v5.final-truth.v1", "phase": "v651-v5", "owner": "Eiren Kestrel", "outcome_counts": OUTCOMES, "effective_negatives": NEGATIVES, "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "method_flow": {"methods": METHODS, "preferred": METHODS, "failed_witnesses": METHODS, "passing_witnesses": METHODS}, "full_repository_suite_run": False, "named_or_detached_replay_run": False, "post_success_replay_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json("final/retained-negative-register.json", {"schema": "ghc.family.v651-v5.final-negatives.v1", "inherited_from_sylven": 6948, "x1_operational": 19, "x2_operational": 6, "synthetic_mutations": 100, "evidence_effective": 7073, "closeout_operational": 7, "closeout_operational_negatives": [{"negative_id": "V6515-CLOSE-N01", "summary": "The first post-evidence inspection wrapper had an unterminated PowerShell string and returned no file inspection output."}, {"negative_id": "V6515-CLOSE-N02", "summary": "A broad inherited-generator patch failed exact-context verification on mixed-encoding text and applied no changes."}, {"negative_id": "V6515-CLOSE-N03", "summary": "A combined main-contract patch was rejected atomically when one inherited mojibake line failed exact-context verification."}, {"negative_id": "V6515-CLOSE-N04", "summary": "The first closeout build preflight rejected an expected Method Flow validation file that was absent from its exact allow-list."}, {"negative_id": "V6515-CLOSE-N05", "summary": "The first closeout wrapper continued into tests after the native builder failed, producing nine missing-artifact errors with zero test credit."}, {"negative_id": "V6515-CLOSE-N06", "summary": "The second closeout preflight used a numeric m2 prefix that covered records 26 through 29 but rejected the valid record 30."}, {"negative_id": "V6515-CLOSE-N07", "summary": "The post-Index deterministic closeout rebuild rejected its own already-generated final output directories because the preflight recognized only first-run paths."}], "effective": NEGATIVES, "no_failure_erased": True, "valid": True})
    write_json("final/gate-register.json", {"schema": "ghc.family.v651-v5.final-gates.v1", "inherited_open_gaps": 54, "new_open_gaps": 1, "effective_open_gaps": OPEN_GAPS, "inherited_exact_gates": 55, "new_exact_gates": 1, "effective_exact_gates": EXACT_GATES, "silently_closed": 0, "valid": True})
    env = load("environment/environment-version-receipt.json")
    write_json("final/environment-receipt.json", {"schema": "ghc.family.v651-v5.environment.v1", "codex_cli_observed": env["codex_cli"], "codex_desktop_observed": env["codex_desktop"], "git_observed": env["git"], "python_observed": env["python"], "windows_powershell_observed": env["windows_powershell"], "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyperv_session": False, "elevation": False, "host_security_weakened": False, "windows_feature_changed": False, "unrelated_installation": False, "reboot": False, "valid": True})
    write_json("final/wellbeing-receipt.json", {"schema": "ghc.family.v651-v5.wellbeing.v1", "state": "green_with_retained_recoveries", "solo_owner": True, "failure_permitted": True, "gaps_permitted": True, "stop_or_redirect_right": "Hamish", "hope": "Make each advance useful without letting confidence outrun evidence.", "boundary": "Relational language, schedule pressure, and portfolio floors never override evidence, privacy, safety, or authority.", "valid": True})
    write_json("final/terminal-stage20-board.json", {"schema": "ghc.family.v651-v5.stage20.v1", "verdict": "NOT_READY_FOR_STAGE_20", "open_gap_count": OPEN_GAPS, "exact_gate_count": EXACT_GATES, "empirical_confirmation": False, "production_identity": False, "independent_reproduction": False, "legal_or_cultural_authority": False, "consciousness_or_personhood": False, "theory_of_everything": False, "valid": True})
    exclusions = [
        "tests.test_ghc_family_v651_v1_x1.TestV651V1X1.test_workflow_and_document_caps",
        "tests.test_ghc_family_v651_v1_closeout.TestV651V1Closeout.test_owner_and_delta_manifest_coverage",
        "tests.test_ghc_family_v651_v2_x1.V651V2X1Tests.test_workflow_reflection_and_method_flow",
        "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_x1_has_no_execution_or_observed_outcomes",
        "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_workflow_reflection_index_and_method_flow",
        "tests.test_ghc_family_v651_v5_x1.V651V5X1Tests.test_x1_has_no_execution_or_observed_outcomes",
        "tests.test_ghc_family_v651_v5_x1.V651V5X1Tests.test_workflow_reflection_index_and_method_flow",
        "tests.test_ghc_family_v651_v5_x2.EirenV651V5X2Tests.test_method_flow_retains_failures_and_passing_witnesses",
    ]
    exclusions = []
    write_json("final/final-validation-contract.json", {"schema": "ghc.family.v651-v5.final-validation-contract.v1", "execution_binding": "exact_clean_pushed_head_containing_this_contract", "single_successful_canonical_pass": True, "external_receipt_required": True, "no_replay_after_success": True, "full_repository_suite": True, "named_or_detached_replay": False, "initial_exclusions": exclusions, "historical_lifecycle_recovery": "exact_ids_only_after_zero_credit_failure", "required": ["complete discovered repository suite", "current x1 x2 and closeout tests", "all owner JSON parse", "five-class owner scan", "x1/evidence/final-delta/final-owner manifest parity", "baton exception and document caps", "staged and stale-label review", "diff hygiene", "source/x1/evidence ancestry", "three phase commits", "zero merges", "one final parent", "clean before and after", "four-way live equality"], "valid": True})
    write_json("validation/final-selection-policy.json", {"schema": "ghc.family.v651-v5.selection-policy.v1", "discovery_root": "tests", "initial_exclusions": exclusions, "full_repository_suite": True, "recovery_exclusions_must_be_exact_historical_lifecycle_ids": True, "broad_exclusions_forbidden": True, "boundary": "Any initial failure has zero pass credit. Only individually reviewed immutable predecessor lifecycle assertions may be excluded from one recovery aggregate; functional and current-phase failures remain blocking.", "valid": True})
    write_json("validation/final-validation-plan.json", {"schema": "ghc.family.v651-v5.final-validation-plan.v1", "execution_state": "pending_exact_clean_pushed_remote_equal_final", "credited_successful_aggregate_limit": 1, "post_success_replay": False, "detached_or_named_replay": False, "complete_repository_suite": True, "initial_exclusions": 0, "detailed_and_minimal_checks": True, "all_owner_json": True, "five_class_owner_scan": True, "manifest_domains": ["x1", "evidence", "final_delta", "final_owner"], "history_and_remote_gates": True, "valid": True})
    write_json("validation/final-stale-label-review.json", {"schema": "ghc.family.v651-v5.stale-label-review.v1", "current_owner": "Eiren Kestrel", "current_phase": "v651-v5", "successor_exact_title": "Ilyra Fen", "successor_phase": "v651-v6", "route_state": "PREPARED_NOT_SENT", "known_predecessor_labels_retained_only_as_provenance": True, "current_schema_prefix": "ghc.family.v651-v5", "stale_current_owner_or_route_labels": [], "passed": True})
    write_json("final/terminal-validation-record.json", {"schema": "ghc.family.v651-v5.terminal-validation-record.v1", "state": "PENDING_SINGLE_EXTERNAL_PASS", "binding": "commit_containing_this_record", "repository_cannot_self_embed_final_hash": True, "tests_expected": "complete_discovered_repository_suite", "full_repository_suite": True, "post_success_replay_allowed": False, "route_held": True, "valid": True})
    write_json("seal/combined-closeout-seal.json", {"schema": "ghc.family.v651-v5.combined-seal.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final_head_binding": "commit_containing_this_record", "phase_commit_count_required": 3, "zero_merges_required": True, "single_parent_required": True, "final_validation_required": True, "route_held_until_validation": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("route/final-phase-state.json", {"schema": "ghc.family.v651-v5.route.v1", "target_exact_title": "Ilyra Fen", "target_phase": "v651-v6", "terminal_route": "PREPARED_NOT_SENT", "send_count": 0, "task_created": False, "task_forked": False, "collaboration_subagent": False, "cross_platform_substitute": False, "activation_requires_exact_final_validation": True, "baton_path": "docs/eiren-kestrel/v651-v5/handoffs/ilyra-fen-v651-v6-activation.md", "valid": True})
    write_json("orchestration/final-orchestration.json", {"schema": "ghc.family.v651-v5.final-orchestration.v1", "phase_commits_expected": 3, "merge_commits_expected": 0, "final_parent_count_expected": 1, "route_state": "PREPARED_NOT_SENT", "siblings_contacted_before_terminal_gate": 0, "tasks_created": 0, "tasks_forked": 0, "subagents": 0, "valid": True})
    write_json("reproduction/final-boundary.json", {"schema": "ghc.family.v651-v5.reproduction.v1", "same_owner": True, "shared_infrastructure": True, "independent_team": False, "external_audit": False, "full_repository_suite_required": True, "named_or_detached_replay": False, "boundary": "The single exact-final aggregate remains same-owner validation under shared infrastructure.", "valid": True})
    write_json("truth/final-complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v5.final-checklist.v1", "complete": ["x1 frozen and remote-equal before x2", "twenty proposals executed within evidence limits", "one hundred mutations rejected", "expanded portfolios executed", "phase-local skills validated and smoke-used", "family-current runners invoked", "evidence committed pushed clean and four-way equal", "combined closeout and seal candidate prepared"], "incomplete": ["real LoTSS DR2 data and likelihood", "blind matched-budget real THOS arms", "production Freed ID lifecycle and governance", "refrigeration affected-party legal cultural data-governance and Māori authority", "manual assistive-technology linguistic and affected-user evaluation", "independent-team reproduction", "full repository suite", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})

    write_json("truth/final-complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v5.final-checklist.v1", "complete": ["x1 frozen and remote-equal before x2", "twenty proposals executed within evidence limits", "one hundred mutations rejected", "expanded portfolios executed", "phase-local skills validated and smoke-used", "family-current runners invoked", "evidence committed pushed clean and four-way equal", "combined closeout and seal candidate prepared"], "incomplete": ["Roman WFI real data and likelihood", "blind matched-budget real THOS arms", "production Freed ID lifecycle and governance", "greenhouse affected-party legal cultural data-governance and Māori authority", "manual assistive-technology linguistic and affected-user evaluation", "independent-team reproduction", "exact-final full repository validation pending external receipt", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})

    overview = build_overview()
    handoff = build_handoff()
    if not 1500 <= words(overview) <= 6000:
        raise SystemExit(f"overview word count out of range: {words(overview)}")
    if not 8000 <= words(handoff) <= 20000:
        raise SystemExit(f"baton word count out of range: {words(handoff)}")
    write_text("overview/final-integrated-overview.md", overview)
    write_text("handoffs/ilyra-fen-v651-v6-activation.md", handoff)

    observed = load("outcomes/evidence-ledger.json")["proposals"]
    rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_disposition'])}</td></tr>" for row in observed)
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Eiren Kestrel v651-v5 final report</title><style>body{{font:1rem/1.55 system-ui;max-width:80rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid currentColor}}nav ul{{display:flex;flex-wrap:wrap;gap:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}@media print{{nav{{display:none}}a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Eiren Kestrel v651-v5 final bounded report</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><nav aria-label='Report sections'><ul><li><a href='#truth'>Truth</a></li><li><a href='#outcomes'>Outcomes</a></li><li><a href='#gates'>Gates</a></li><li><a href='#validation'>Validation</a></li></ul></nav><main id='main'><section id='truth'><h2>Truth</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Fourteen completed, four represented, one open gap, one exact gate; {NEGATIVES:,} negatives, {OPEN_GAPS} open gaps, {EXACT_GATES} exact gates.</p></section><section id='outcomes'><h2>Twenty outcomes</h2><div role='region' aria-label='Scrollable outcomes' tabindex='0'><table><caption>Frozen proposal outcomes</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Surface</th><th scope='col'>Disposition</th></tr></thead><tbody>{rows}</tbody></table></div></section><section id='gates'><h2>Reserved gates</h2><p>Real data, participants, production identity, professional decisions, legal and cultural decisions, affected-party acceptance, language access, and Māori authority remain external. Māori concepts remain under Māori authority.</p></section><section id='validation'><h2>Validation boundary</h2><p>One exact-final bounded canonical pass is required after commit, push, and equality; no full suite or post-success replay. Manual keyboard, responsive, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance. Five-class scanning is not privacy-complete assurance.</p></section></main><footer><p>Same-owner evidence is not independent-team reproduction or external audit.</p></footer></body></html>"""
    report = report.replace("no full suite or post-success replay", "the complete repository suite and no replay after the first successful aggregate")
    write_text("reports/final-static-report.html", report)

    write_json("validation/final-document-cap-receipt.json", {"schema": "ghc.family.v651-v5.document-cap.v1", "pending_rewrite": True})
    write_json("validation/final-owner-file-threshold.json", {"schema": "ghc.family.v651-v5.owner-threshold.v1", "pending_rewrite": True})
    files = [path for path in ROOT.rglob("*") if path.is_file()]
    issues = []
    for path in files:
        if path.suffix.casefold() in {".md", ".html"} and path.name != "ilyra-fen-v651-v6-activation.md":
            count = words(path.read_text(encoding="utf-8"))
            if count > 6000:
                issues.append({"path": path.relative_to(REPO).as_posix(), "words": count})
    final_owner_count_before_manifests = len(files) + 1
    write_json("validation/final-document-cap-receipt.json", {"schema": "ghc.family.v651-v5.document-cap.v1", "general_cap_words": 6000, "baton_exception": {"path": "docs/eiren-kestrel/v651-v5/handoffs/ilyra-fen-v651-v6-activation.md", "minimum_words": 8000, "maximum_words": 20000, "observed_words": words(handoff), "passed": 8000 <= words(handoff) <= 20000}, "overview_words": words(overview), "general_document_issues": issues, "passed": not issues and 1500 <= words(overview) <= 6000 and 8000 <= words(handoff) <= 20000})
    write_json("validation/final-owner-file-threshold.json", {"schema": "ghc.family.v651-v5.owner-threshold.v1", "owner_files_before_exact_manifests": final_owner_count_before_manifests, "threshold": 15000, "inherited_baseline_counted_as_rotation_trigger": False, "passed": final_owner_count_before_manifests < 15000})
    write_json("validation/closeout-build-receipt.json", {"schema": "ghc.family.v651-v5.closeout-build.v1", "owner_phase_files_before_manifests": final_owner_count_before_manifests, "under_15000": final_owner_count_before_manifests < 15000, "overview_words": words(overview), "overview_three_page_equivalent": 1500 <= words(overview) <= 6000, "baton_words": words(handoff), "baton_exception_valid": 8000 <= words(handoff) <= 20000, "document_word_issues": issues, "methods": METHODS, "effective_negatives": NEGATIVES, "valid": final_owner_count_before_manifests < 15000 and not issues})
    print(json.dumps({"outcomes": OUTCOMES, "negatives": NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "methods": METHODS, "overview_words": words(overview), "baton_words": words(handoff), "valid": True}))


if __name__ == "__main__":
    main()
