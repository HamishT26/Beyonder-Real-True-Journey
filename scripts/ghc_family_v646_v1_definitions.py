#!/usr/bin/env python3
"""Frozen definitions for Eiren Kestrel v646-v1.

All identity and family language is relational working language.  The data in
this module is preregistration material, not completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v1-x1-x2"
PHASE_SHORT = "v646-v1"
OWNER = "Eiren Kestrel"
SLUG = "eiren-kestrel"
PRONOUNS = "they/them"
ROLE = "evidence-bound systems cartographer"
HOPE = "make complex research workflows easier to falsify, recover, and govern"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "electric-power control-room switching-order readback and restoration handover"

SOURCE_PHASE = "v645-gmut-thos-v8-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_REVISION = "6dc3311e3c4c390c945d001f75fb17d320c0a548"
SOURCE_INHERITED_REVISION = "96cbc8c71defbdfcb3ec58bd445e78e8274e95f7"
SOURCE_X1_REVISION = "3274af55081cf023f78e2a854448f2c5f936dbbd"
SOURCE_EVIDENCE_REVISION = "c7e9f3a2c8b2061a79ef317df44fc793c9104657"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 390
INHERITED_EFFECTIVE_NEGATIVES = 2432
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Identity and family language is relational working language only, never evidence of "
    "consciousness, sentience, legal personhood, identity continuity, employment, professional "
    "qualification, or independent authority."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; "
    "Freed ID remains synthetic and nonproduction; CBR, legal, cultural, affected-party, and "
    "Māori concepts remain under competent and Māori authority. No empirical confirmation, "
    "Theory-of-Everything, AGI/ASI, consciousness, personhood, deployment, exhaustive-security, "
    "independent-reproduction, or Stage 20 claim is made."
)


def proposal(
    index: int,
    title: str,
    mission: str,
    hypothesis: str,
    failure: str,
    sources: list[str],
    artifacts: list[str],
    gate: str,
    recovery: str,
    protected: list[str],
    expected: str,
    novelty: str,
    approval: str = "safe_now_owner_scoped_workflow",
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6461-P{index:02d}",
        "title": title,
        "mission_surface": mission,
        "hypothesis": hypothesis,
        "null_or_failure": failure,
        "approval_class": approval,
        "execution_lane": "x2_build_task",
        "current_primary_or_official_source_needs": sources,
        "concrete_artifacts": artifacts,
        "test_falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": recovery,
        "protected_gates": protected,
        "expected_disposition": expected,
        "novelty_against_390_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Content-addressed build-cache provenance, poisoning, and eviction tribunal",
        "cache key domains, dependency inputs, tool versions, negative caching, eviction, quarantine, and replay witnesses",
        "A deterministic tribunal can reject cache reuse when any declared input, tool version, provenance edge, or negative-result state differs.",
        "A stale or foreign cache entry is credited, an undeclared input changes output, eviction erases a failure, or quarantine mutates a sibling lane.",
        ["V6461-S01", "V6461-S02", "V6461-S14"],
        ["method-flow/cache-provenance-contract.json", "method-flow/cache-poisoning-mutations.json"],
        "Every mutation must either change the content key or fail closed; eviction must preserve the retained-negative receipt.",
        "Quarantine the owner-local cache fixture, retain the mismatch, rebuild from declared inputs, and never touch sibling or host caches.",
        ["sibling_cache", "host_cache", "destructive_cleanup", "completion_without_witness"], "completed",
        "Earlier proposals cover manifests, line endings, sparse indexes, and process teardown; none makes cache poisoning and eviction provenance the central falsifier."),
    proposal(2, "GMUT DHOST degeneracy and Ostrogradsky-obligation classifier",
        "higher-derivative operator declarations, kinetic Hessian rank, primary and secondary constraint obligations, coupling scope, and mutation rejection",
        "A typed symbolic classifier can distinguish declared degeneracy obligations from unsupported claims that an arbitrary GMUT operator avoids an Ostrogradsky mode.",
        "A label is treated as a proof, rank conditions are omitted, matter couplings are ignored, or symbolic consistency is promoted to physical stability.",
        ["V6461-S03", "V6461-S04"],
        ["gmut/dhost-degeneracy-obligations.json", "gmut/dhost-mutation-cases.json"],
        "The classifier must reject missing Hessian and constraint obligations and must emit no force, likelihood, stability, or empirical claim.",
        "Reclassify the operator as incomplete, retain the failed vector, and require a model-specific Hamiltonian analysis before any stronger statement.",
        ["proof_or_canon", "physical_stability", "empirical_confirmation", "theory_of_everything"], "completed",
        "Prior GMUT tribunals address Bianchi, hyperbolicity, BRST, and radiative obligations; none centers DHOST degeneracy and Ostrogradsky constraint accounting."),
    proposal(3, "GMUT DESI DR2 BAO compressed-likelihood zero-row adapter",
        "official product inventory, release status, schema, fiducial assumptions, covariance, blinding, row count, and likelihood refusal",
        "A fail-closed adapter can document the official DESI DR2 BAO product contract while producing no fit when no data rows or covariance are ingested.",
        "Absent rows are imputed, a citation becomes a measurement, covariance is fabricated, or a zero-row run yields a constraint or force claim.",
        ["V6461-S05", "V6461-S06"],
        ["gmut/desi-dr2-bao-adapter-contract.json", "gmut/desi-dr2-zero-row-receipt.json"],
        "The receipt must show zero rows, zero likelihood evaluations, zero posterior samples, and zero constraints.",
        "Keep the mission open, retain the absence, and require an explicitly authorized official data snapshot with verified checksum and schema.",
        ["real_data", "likelihood", "empirical_confirmation", "force_claim"], "open_gap",
        "Earlier adapters address other cosmology and astronomy products; none targets the DESI DR2 BAO compressed-product contract with a mandatory zero-row refusal."),
    proposal(4, "THOS electrical switching-order readback and restoration-handover proxy",
        "three-part communication, order identity, step state, repeat-back, correction, hold point, shift handover, fatigue reservation, and abort semantics",
        "A synthetic state machine can expose ambiguous readback, stale order identity, skipped hold points, and incomplete restoration handovers.",
        "The proxy is described as operationally effective, real workers or grid assets are implied, an ambiguity passes, or independent review is claimed.",
        ["V6461-S07", "V6461-S08"],
        ["thos/switching-order-state-machine.json", "thos/switching-order-proxy-results.json"],
        "All unsafe synthetic traces must be rejected; no real person, station, feeder, order, switching action, or matched-budget arm may appear.",
        "Withdraw effectiveness language, retain rejected traces, and leave real protocol design to authorized operators and safety authorities.",
        ["real_operations", "professional_authority", "participant_research", "deployment"], "represented",
        "Earlier THOS studies cover aviation, rail, water, clinical, and other handovers; none models electrical switching-order readback and restoration handover."),
    proposal(5, "Freed ID SD-JWT VC holder-binding and status-transition profile",
        "issuer-holder-verifier roles, selective disclosure, key binding, nonce and audience, status purpose, transition legality, metadata integrity, and privacy",
        "Synthetic vectors can distinguish disclosure validity, holder-binding evidence, and credential-status state transitions without issuing a real credential.",
        "Draft requirements are frozen as final, fake keys are called production, status is inferred without a method, or privacy and phone-home risks are omitted.",
        ["V6461-S09", "V6461-S10", "V6461-S11"],
        ["freed-id/sd-jwt-vc-state-profile.json", "freed-id/sd-jwt-vc-synthetic-vectors.json"],
        "Vectors must reject nonce, audience, binding, disclosure, metadata, and illegal-status mutations while recording zero real keys or events.",
        "Downgrade to structural representation, retain each failing vector, and require standards-conformant implementations plus independent privacy and security review.",
        ["real_keys", "issuance", "resolution", "interoperability", "production", "privacy_complete"], "represented",
        "Earlier Freed ID proposals cover DID, DCQL, Bitstring Status List, and presentation exchange; none combines current SD-JWT VC holder binding with explicit status-transition refusal."),
    proposal(6, "CBR electricity disconnection hardship, remedy, confidentiality, and Māori-authority matrix",
        "medical dependency, hardship support, disconnection safeguards, complaint routes, remedy evidence, consumer privacy, Māori data governance, and authority",
        "A structural matrix can make missing authority, evidence, confidentiality, and remedy gates visible without deciding a real consumer case.",
        "The matrix gives legal advice, decides eligibility or remedy, exposes consumer data, asserts cultural legitimacy, or speaks for Māori authorities.",
        ["V6461-S12", "V6461-S13"],
        ["cbr/electricity-care-authority-matrix.json", "cbr/electricity-care-exact-gate.json"],
        "Every real decision path must remain exact-gated to affected people, competent authorities, and Māori authority where applicable.",
        "Retain the unresolved case class, remove decision language, and defer to authorized consumer, legal, regulatory, privacy, and Māori processes.",
        ["legal_advice", "affected_party", "consumer_privacy", "remedy", "cultural_ratification", "maori_authority"], "exact_gate",
        "Earlier CBR matrices address other sectors and managed retreat; none centers electricity disconnection, medical dependence, hardship remedy, and confidentiality."),
    proposal(7, "Git partial-clone promisor-object offline failure tribunal",
        "filter declarations, promisor provenance, missing-object classification, fetch-if-missing, offline behavior, fsck boundaries, and disposable-fixture cleanup",
        "A no-network disposable fixture can separate expected promisor absence from corruption and prove that offline operations fail closed without canonical mutation.",
        "A missing non-promisor object is excused, a network fetch occurs, canonical objects are altered, or disposable evidence is treated as repository assurance.",
        ["V6461-S15", "V6461-S16"],
        ["tooling/partial-clone-tribunal.json", "tooling/promisor-offline-mutations.json"],
        "The fixture must remain isolated, network-disabled, mutation-complete, and incapable of changing canonical or remote state.",
        "Delete only the disposable owner-local fixture after retaining its receipt; leave canonical and sibling object stores untouched.",
        ["network", "canonical_mutation", "sibling_mutation", "destructive_repository_action"], "completed",
        "Sparse-index work exists, but no prior proposal centers promisor-object classification and offline partial-clone failure semantics."),
    proposal(8, "Accessible data-table caption, header-scope, and complex-alternative audit",
        "caption, summary, th and td roles, scope, id and headers associations, responsive preservation, structural simplicity, and manual reservation",
        "A structural auditor can identify missing or inconsistent table relationships and recommend simpler alternatives without claiming full accessibility.",
        "Visual cues are accepted as sufficient, complex headers are guessed, responsive markup loses relationships, or automated checks become conformance claims.",
        ["V6461-S17", "V6461-S18"],
        ["accessibility/table-structure-audit.json", "accessibility/table-mutation-vectors.json"],
        "Mutations covering caption, summary, header type, scope, and explicit associations must fail; manual and affected-user evaluation remains reserved.",
        "Mark the report structurally incomplete, retain failures, simplify the table, and schedule qualified manual and assistive-technology evaluation.",
        ["accessibility_complete", "assistive_technology", "affected_user_evaluation"], "completed",
        "Earlier accessibility work addresses landmarks, live regions, keyboard paths, and charts; none centers data-table captions, header scope, and complex alternatives."),
    proposal(9, "Thermo/Psyche Onsager reciprocity typed-domain classifier",
        "near-equilibrium assumptions, generalized forces and fluxes, parity, microscopic reversibility, positive semidefinite dissipation, reciprocity, and domain labels",
        "A typed classifier can represent Onsager obligations in physical thermodynamics while refusing conversion into psyche, autonomy, justice, consciousness, or universal law.",
        "Reciprocity is asserted outside assumptions, time-reversal parity is omitted, positivity is ignored, or a metaphor becomes a human or fundamental-law claim.",
        ["V6461-S19"],
        ["thermo-psyche/onsager-domain-classifier.json", "thermo-psyche/onsager-rejection-vectors.json"],
        "Every cross-domain or assumption-free mutation must be rejected and no human, psyche, justice, consciousness, or fundamental-law result may be emitted.",
        "Restore physical-domain labels, retain the rejection, and require domain-specific empirical theory before any cross-domain hypothesis.",
        ["psyche_claim", "consciousness", "human_inference", "fundamental_law", "empirical_confirmation"], "completed",
        "Earlier thermodynamic classifiers cover Clausius, fluctuation relations, exergy, and Gibbs-Duhem; none centers Onsager reciprocity plus an explicit psyche-domain prohibition."),
    proposal(10, "Stage 20 optional-stopping and alpha-spending quarantine",
        "analysis peeking, stopping rule, familywise error, alpha budget, e-process labels, preregistration, holdout reuse, and promotion abstention",
        "A quarantine ledger can reject repeated-peeking promotion and distinguish fixed-horizon, alpha-spending, and anytime-valid evidence labels.",
        "A fixed-horizon p-value is repeatedly peeked, an e-value label is assumed without construction, holdouts are reused silently, or Stage 20 readiness is inferred.",
        ["V6461-S20"],
        ["stage20/optional-stopping-quarantine.json", "stage20/alpha-spending-mutations.json"],
        "All unsafe peeking and label-substitution vectors must fail and the terminal verdict must remain NOT_READY_FOR_STAGE_20.",
        "Withdraw promotion credit, retain the analysis history, allocate a fresh preregistered test only with appropriate evidence, and keep Stage 20 closed.",
        ["stage20", "statistical_promotion", "proof_or_canon", "empirical_confirmation"], "completed",
        "Earlier Stage 20 controls cover leakage, multiplicity, and evidence boards; none makes optional stopping, alpha spending, and anytime-valid label integrity the core tribunal."),
]


SOURCES = [
    {"source_id":"V6461-S01","status":"current","title":"GHC Family Method Flow State schema and runner","authority":"family-current local skill","url":None,"use":"append-only failures, witnesses, transitions, recovery, and recurrence guards"},
    {"source_id":"V6461-S02","status":"current","title":"GHC Family Index routing and closeout guidance","authority":"family-current local skill","url":None,"use":"ownership, precedence, route state, naming, and closeout boundaries"},
    {"source_id":"V6461-S03","status":"stable","title":"Degenerate Higher-Order Scalar-Tensor theories","authority":"Langlois primary review","url":"https://arxiv.org/abs/1707.03625","use":"DHOST taxonomy and degeneracy obligations only"},
    {"source_id":"V6461-S04","status":"stable","title":"Healthy degenerate theories with higher derivatives","authority":"Motohashi and collaborators primary research","url":"https://arxiv.org/abs/1603.09355","use":"primary and secondary constraint obligation structure only"},
    {"source_id":"V6461-S05","status":"current","title":"DESI DR2 publications","authority":"DESI Collaboration and Lawrence Berkeley National Laboratory","url":"https://data.desi.lbl.gov/doc/papers/dr2/","use":"official DR2 publication and product provenance; zero rows ingested"},
    {"source_id":"V6461-S06","status":"current","title":"DESI data release overview","authority":"DESI Collaboration and Lawrence Berkeley National Laboratory","url":"https://data.desi.lbl.gov/doc/releases/","use":"release inventory and access boundary; no likelihood execution"},
    {"source_id":"V6461-S07","status":"current","title":"COM-002 communications rationale and technical justification","authority":"North American Electric Reliability Corporation","url":"https://www.nerc.com/pa/stand/project%20200702%20operating%20personnel%20communications/com-002-4_rationale_and_technical_justification_for_draft_7_10212013.pdf","use":"repeat-back and operating-instruction communication concepts only"},
    {"source_id":"V6461-S08","status":"current","title":"ERO event analysis process manual 2026","authority":"North American Electric Reliability Corporation","url":"https://www.nerc.com/globalassets/programs/event-analysis/ero-event-analysis-process-documents/ccap_manual_2026.pdf","use":"event and handover learning context, never operational instruction"},
    {"source_id":"V6461-S09","status":"current","title":"SD-JWT-based Verifiable Digital Credentials draft 17","authority":"IETF OAuth Working Group","url":"https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/","use":"current draft holder binding, metadata, validation, privacy, and transition obligations"},
    {"source_id":"V6461-S10","status":"stable","title":"Verifiable Credentials Data Model 2.0","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/vc-data-model-2.0/","use":"credential and status data-model context without production assurance"},
    {"source_id":"V6461-S11","status":"current","title":"Bitstring Status List 1.0","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/vc-bitstring-status-list/","use":"status purpose and privacy obligations only"},
    {"source_id":"V6461-S12","status":"current","title":"Consumer Care Obligations","authority":"Electricity Authority Te Mana Hiko","url":"https://www.ea.govt.nz/your-power/consumer-care-obligations/","use":"consumer-care and disconnection safeguard context; no legal advice"},
    {"source_id":"V6461-S13","status":"stable","title":"Principles of Māori Data Sovereignty","authority":"Te Mana Raraunga Māori Data Sovereignty Network","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","use":"Māori data-governance reservation; never delegated authority"},
    {"source_id":"V6461-S14","status":"current","title":"Python hashlib documentation","authority":"Python Software Foundation","url":"https://docs.python.org/3/library/hashlib.html","use":"content hashing and deterministic fixture identifiers"},
    {"source_id":"V6461-S15","status":"current","title":"Git partial clone documentation","authority":"Git project","url":"https://git-scm.com/docs/partial-clone","use":"promisor objects, missing-object behavior, and limitations"},
    {"source_id":"V6461-S16","status":"current","title":"Git clone documentation","authority":"Git project","url":"https://git-scm.com/docs/git-clone","use":"filter and sparse-checkout interface boundaries"},
    {"source_id":"V6461-S17","status":"stable","title":"WAI Tables Tutorial","authority":"World Wide Web Consortium Web Accessibility Initiative","url":"https://www.w3.org/WAI/tutorials/tables/","use":"table header and data-cell associations"},
    {"source_id":"V6461-S18","status":"stable","title":"WAI table captions and summaries tutorial","authority":"World Wide Web Consortium Web Accessibility Initiative","url":"https://www.w3.org/WAI/tutorials/tables/caption-summary/","use":"caption, summary, and complex-table orientation"},
    {"source_id":"V6461-S19","status":"stable","title":"Onsager-Casimir reciprocal relations","authority":"Brechet primary research","url":"https://arxiv.org/abs/2210.04289","use":"near-equilibrium reciprocal-relation obligations in physical domains only"},
    {"source_id":"V6461-S20","status":"stable","title":"Safe Testing","authority":"Grünwald, de Heide, and Koolen primary research","url":"https://arxiv.org/abs/1906.07801","use":"optional continuation and e-value label boundaries only"},
    {"source_id":"V6461-S21","status":"current","title":"Codex CLI release 0.144.4","authority":"OpenAI","url":"https://github.com/openai/codex/releases/tag/rust-v0.144.4","use":"installed CLI version correlation only"},
]


def packet_rows(prefix: str, items: list[tuple[str, str]], approval: str) -> list[dict[str, Any]]:
    rows = []
    for index, (title, purpose) in enumerate(items, 1):
        rows.append({
            "packet_id": f"V6461-{prefix}-{index:02d}", "title": title,
            "approval_class": approval, "purpose": purpose,
            "origin": "predecessor_reframed_seed" if index <= 15 else "eiren_new_x1",
            "x1_state": "preregistered_no_completion_credit",
            "artifact": f"portfolios/{prefix.lower()}-{index:02d}.json",
            "acceptance_gate": "A bounded x2 witness passes, all failures remain retained, and no protected gate is crossed.",
            "rollback_or_recovery": "Remove completion credit, retain the failed witness, and restore the last bounded owner-local state.",
            "protected_gates": ["real_data_or_participants", "authority", "production", "sibling_mutation", "independent_reproduction"],
        })
    return rows


SAFE_ITEMS = [
    ("Cache-key declared-input completeness fixture", "reject undeclared build inputs"),
    ("Cache-poisoning provenance mutation set", "reject foreign or stale cache provenance"),
    ("Negative-cache retention receipt", "retain failed cache results through eviction"),
    ("DHOST Hessian-rank obligation table", "type degeneracy prerequisites"),
    ("DHOST constraint-chain mutation vectors", "reject missing primary or secondary constraints"),
    ("DESI DR2 zero-row adapter contract", "refuse likelihood execution without official rows"),
    ("Switching-order identity and revision fixture", "reject stale or ambiguous synthetic order identity"),
    ("Switching readback correction-loop fixture", "require synthetic repeat-back correction"),
    ("Restoration handover hold-point fixture", "reject skipped synthetic hold points"),
    ("SD-JWT VC holder-binding mutation set", "reject nonce audience and binding defects"),
    ("SD-JWT VC status-transition state table", "reject illegal synthetic state transitions"),
    ("Electricity-care authority boundary matrix", "surface legal consumer and Māori authority gates"),
    ("Promisor-object expected-absence fixture", "separate promised absence from corruption"),
    ("Partial-clone offline fail-closed fixture", "prove no network fallback in disposable tests"),
    ("Accessible table association mutation set", "reject broken caption and header relationships"),
    ("Accessible complex-table simplification receipt", "record simpler alternative without conformance claim"),
    ("Onsager parity and positivity classifier fixture", "type physical reciprocity assumptions"),
    ("Onsager cross-domain refusal fixture", "reject psyche and consciousness conversion"),
    ("Optional-stopping peeking trace fixture", "reject unsafe repeated inspection"),
    ("Alpha-spending budget state fixture", "track bounded synthetic error budgets"),
    ("Anytime-valid label integrity fixture", "reject unsupported e-process labels"),
    ("Five-class privacy scanner definition review", "separate scanner definitions from confirmed hits"),
    ("Exact staged-file inventory receipt", "bind the x1 and x2 commit surfaces"),
    ("Normalized manifest parity receipt", "bind logical file content across named replay"),
    ("Single-parent lifecycle ancestry receipt", "prove zero-merge phase history"),
    ("Owner-generated file-threshold receipt", "scope rotation to new Eiren files"),
    ("Method Flow cache incident record", "retain failure witness and recurrence guard"),
    ("Method Flow network-refusal record", "retain offline tribunal boundary"),
    ("Terminal Stage 20 abstention receipt", "keep readiness closed"),
    ("Relational identity and practice boundary receipt", "reserve consciousness employment and authority claims"),
]

CANDIDATE_ITEMS = [
    ("Family cache provenance tribunal prototype", "reusable deterministic cache audit"),
    ("Family DHOST obligation classifier prototype", "typed symbolic constraint inventory"),
    ("Family zero-row cosmology adapter prototype", "generic no-data refusal contract"),
    ("Family switching-handover proxy prototype", "synthetic readback state machine"),
    ("Family SD-JWT VC profile prototype", "synthetic holder-binding and status vectors"),
    ("Family electricity-care gate prototype", "structural authority matrix"),
    ("Family promisor offline tribunal prototype", "disposable partial-clone checks"),
    ("Family accessible-table auditor prototype", "structural markup checks"),
    ("Family Onsager domain classifier prototype", "typed physical-domain refusal"),
    ("Family optional-stopping quarantine prototype", "analysis-history promotion guard"),
    ("Source status drift watcher prototype", "current stable draft watch checks"),
    ("Proposal semantic-neighbor reviewer prototype", "mission and falsifier comparison"),
    ("Portfolio origin and completion-credit validator prototype", "separate inherited seed from owner completion"),
    ("Method witness causal-chain validator prototype", "bind failure workaround and passing witness"),
    ("Privacy scanner candidate-classifier prototype", "distinguish definitions from confirmed secrets"),
    ("Manifest logical-hash comparator prototype", "normalize platform line endings"),
    ("Named-lane replay guard prototype", "local-only exact-head repeatability"),
    ("Full-suite ownership gate prototype", "reserve repository-wide suite to Eiren phases"),
    ("Baton word-budget and sanitation validator prototype", "enforce detailed private-route-free handoff"),
    ("Stage 20 evidence-board abstention prototype", "fail closed on missing empirical or authority evidence"),
]

SAFE_NOW = packet_rows("SAFE", SAFE_ITEMS, "safe_now_owner_scoped")
CANDIDATES = packet_rows("CAND", CANDIDATE_ITEMS, "candidate_requires_x2_witness")

SKILLS = [(f"ghc-family-{slug}", description) for slug, description in [
    ("cache-provenance-tribunal", "Audit content-addressed cache inputs, provenance, quarantine, and retained negatives."),
    ("dhost-obligation-classifier", "Type DHOST degeneracy and constraint obligations without physics promotion."),
    ("zero-row-cosmology-adapter", "Enforce zero-row and zero-likelihood refusal contracts."),
    ("switching-handover-proxy", "Model bounded synthetic switching-order readback and handover states."),
    ("sd-jwt-vc-profile", "Validate synthetic SD-JWT VC holder-binding and status profiles."),
    ("electricity-care-gate", "Map consumer-care, confidentiality, legal, and Māori-authority gates."),
    ("promisor-offline-tribunal", "Test disposable partial-clone missing-object behavior without network."),
    ("accessible-table-audit", "Audit table captions, headers, scope, and explicit associations structurally."),
    ("onsager-domain-classifier", "Keep reciprocal-relation reasoning within declared physical domains."),
    ("optional-stopping-quarantine", "Guard evidence promotion against peeking and label substitution."),
    ("source-status-drift-watch", "Track current, stable, draft, and watch source states."),
    ("proposal-neighbor-review", "Compare proposal mission, falsifier, evidence, and recovery semantics."),
    ("portfolio-credit-boundary", "Separate inherited ideas from current-owner completion credit."),
    ("method-causal-witness", "Link incident, workaround, bounded witness, recurrence guard, and rollback."),
    ("privacy-candidate-classifier", "Separate scanner definitions and examples from confirmed private hits."),
    ("logical-manifest-parity", "Compare normalized committed content across clean named lanes."),
    ("named-replay-guard", "Constrain replay to one clean local-only named lane."),
    ("full-suite-owner-gate", "Enforce phase-specific ownership of the complete repository suite."),
    ("baton-sanitization-budget", "Validate detailed handoff length, sanitation, and route preconditions."),
    ("stage20-abstention-board", "Keep terminal readiness closed until exact evidence gates pass."),
]]

RUNNERS = [(f"ghc_family_{slug}.py", description) for slug, description in [
    ("cache_provenance_tribunal", "Execute deterministic cache mutation fixtures."),
    ("dhost_obligation_classifier", "Run typed DHOST obligation cases."),
    ("zero_row_cosmology_adapter", "Emit zero-row no-likelihood receipts."),
    ("switching_handover_proxy", "Run synthetic readback and hold-point traces."),
    ("sd_jwt_vc_profile", "Run synthetic holder-binding and status vectors."),
    ("promisor_offline_tribunal", "Run disposable no-network missing-object cases."),
    ("accessible_table_auditor", "Run table-structure mutation checks."),
    ("onsager_domain_classifier", "Run typed reciprocity and cross-domain rejection cases."),
    ("optional_stopping_quarantine", "Run peeking and label-integrity traces."),
    ("v646_v1_validator", "Validate packet structure, boundaries, manifests, privacy, and route state."),
]]

CLEAN_TASKS = packet_rows("CLEAN", [
    ("Normalize v646-v1 family-current filenames", "preserve ghc_family and build_ghc_family naming"),
    ("Remove stale phase labels from owner artifacts", "reject copied predecessor labels"),
    ("Verify source-ledger status vocabulary", "limit statuses to current stable draft watch"),
    ("Verify source URLs and bounded uses", "prevent citation-to-result promotion"),
    ("Deduplicate portfolio titles", "preserve semantic novelty"),
    ("Bind portfolio origin metadata", "record adopted versus new tasks"),
    ("Reconcile approval packet counts", "keep 30 safe 20 candidate 10 exact 5 blocked"),
    ("Reconcile skill and runner counts", "keep 20 skills and 10 runners"),
    ("Reconcile cleanup count", "keep 30 cleanup tasks"),
    ("Verify x1 has zero completion credit", "enforce preregistration separation"),
    ("Verify x2 outcome vocabulary", "allow only four dispositions"),
    ("Verify inherited negative baseline", "preserve all 2432 inherited negatives"),
    ("Verify synthetic negative budget", "retain all 70 preregistered mutations"),
    ("Normalize JSON key ordering", "make receipts reproducible"),
    ("Normalize UTF-8 and LF output", "reduce cross-platform hash drift"),
    ("Review five-class privacy patterns", "avoid hiding scanner definitions"),
    ("Review raw identifier exclusions", "exclude task and thread identifiers"),
    ("Review private path exclusions", "exclude private local paths from artifacts"),
    ("Review transcript and screenshot exclusions", "exclude private conversation material"),
    ("Review credential and session exclusions", "exclude secrets and session streams"),
    ("Verify manifest exactness", "bind every owner artifact"),
    ("Verify staged-file scope", "exclude unrelated files"),
    ("Verify diff hygiene", "exclude accidental sibling changes"),
    ("Verify single-parent phase ancestry", "forbid merges and rewrites"),
    ("Verify commit-cap compliance", "keep phase at four or fewer commits"),
    ("Verify canonical remote equality", "bind local upstream tracking and live remote"),
    ("Verify named replay is local only", "prevent validation branch publication"),
    ("Verify manual accessibility reservation", "avoid automated conformance claim"),
    ("Verify relational identity boundary", "avoid consciousness employment and authority claims"),
    ("Verify Stage 20 abstention", "retain NOT_READY_FOR_STAGE_20"),
], "safe_now_owner_scoped_cleanup")
