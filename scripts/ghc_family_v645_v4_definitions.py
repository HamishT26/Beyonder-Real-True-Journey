"""Frozen v645-v4 preregistration definitions.

This module contains only x1 intent. Importing it performs no repository writes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ghc_family_v645_v3_definitions import (
    BLOCKED_PACKETS as INHERITED_BLOCKED_PACKETS,
    EXACT_PACKETS as INHERITED_EXACT_PACKETS,
    SUCCESSOR_CANDIDATE as INHERITED_CANDIDATE_SEEDS,
    SUCCESSOR_CLEAN as INHERITED_CLEAN_SEEDS,
    SUCCESSOR_RUNNERS as INHERITED_RUNNER_SEEDS,
    SUCCESSOR_SAFE_NOW as INHERITED_SAFE_NOW_SEEDS,
    SUCCESSOR_SKILLS as INHERITED_SKILL_SEEDS,
)

PHASE = "v645-gmut-thos-v4-x1-x2"
OWNER = "Ilyra Fen"
SOURCE_PHASE = "v645-gmut-thos-v3-x1-x2"
SOURCE_REVISION = "3bff59204cee9a7f031b032262d45360cc310c8a"
SOURCE_SEAL_REVISION = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
SOURCE_X1_REVISION = "abb576e6de2666dd2dc792f6dd189722424ff0c2"
SOURCE_EVIDENCE_REVISION = "434dd654264a541ebee8dd58aaecad72199c6edf"
INHERITED_EFFECTIVE_NEGATIVES = 2003
PRIOR_FROZEN_PROPOSALS = 340
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = "museum collections provenance and registrar practice"

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, is relational working language for an evidence-boundary "
    "steward. It is not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, professional qualification, or independent authority."
)

TRUTH_BOUNDARY = (
    "Software, public specifications, and synthetic fixtures can establish only bounded "
    "structural behavior. They do not establish empirical GMUT confirmation, THOS "
    "effectiveness, production identity assurance, museum or cultural authority, Maori "
    "authority, independent reproduction, AGI or ASI, consciousness or personhood, "
    "complete accessibility, exhaustive security, legal effect, a Theory of Everything, "
    "or Stage 20 readiness."
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]


def proposal(
    number: int,
    title: str,
    mission_surface: str,
    hypothesis: str,
    null_or_failure: str,
    approval_class: str,
    execution_lane: str,
    sources: list[str],
    deliverables: list[str],
    gate: str,
    rollback: str,
    protected: list[str],
    disposition: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6454-P{number:02d}",
        "title": title,
        "mission_surface": mission_surface,
        "hypothesis": hypothesis,
        "null_or_failure": null_or_failure,
        "approval_class": approval_class,
        "execution_lane": execution_lane,
        "authoritative_source_needs": sources,
        "deliverables": deliverables,
        "test_falsifier_or_gate": gate,
        "rollback_or_recovery": rollback,
        "protected_gates": protected,
        "expected_disposition": disposition,
        "novelty_against_prior_chain": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Successor seed-adoption provenance, completion-credit isolation, and portfolio-safety tribunal",
        "seed lineage, fresh review, adoption decision, completion-credit isolation, safety reclassification, and rollback",
        "A typed adoption ledger can distinguish inherited suggestions from newly reviewed Ilyra commitments and prevent seed inheritance from being counted as completed work.",
        "Any inherited seed receives completion credit before an Ilyra witness, an unsafe seed remains safe-now, a duplicate survives review, or rollback loses the original seed.",
        "safe_now_structural_only",
        "x2_build_task",
        [],
        ["portfolios/seed-adoption-ledger.json", "portfolios/completion-credit-isolation.json"],
        "Mutations must reject completion without an owner witness, missing origin, duplicate adoption, unsafe classification, and absent rollback.",
        "Restore the frozen seed state, retain the failed review, and require a new bounded adoption decision.",
        ["sibling_completion_credit", "unsafe_reclassification", "history_rewrite"],
        "completed",
        "No earlier frozen title addresses successor seed adoption together with completion-credit isolation and portfolio safety; the 340-title audit found no completion-credit title.",
    ),
    proposal(
        2,
        "GMUT spontaneous-scalarization bifurcation, tachyonic-onset, and branch-stability obligation tribunal",
        "typed scalar-tensor model, effective mass sign, bifurcation branch, linearized stability, and EFT validity",
        "A symbolic fixture can require every scalarization branch claim to expose its onset condition, solution branch, stability obligation, and EFT-domain reservation.",
        "A fixture accepts a branch without an onset condition, confuses a tachyonic linear mode with a stable nonlinear solution, or promotes symbolic algebra to physical confirmation.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["S10", "S11"],
        ["gmut/scalarization-obligation-contract.json", "gmut/scalarization-mutation-vectors.json"],
        "Seven mutation classes must fail closed, including missing background, missing sign convention, branch conflation, and empirical overclaim.",
        "Quarantine the symbolic row, restore the typed assumptions, and leave all empirical claims open.",
        ["empirical_confirmation", "theory_of_everything", "eft_domain", "stability_proof"],
        "completed",
        "The prior chain covers screening, degeneracy, constraints, and field redefinitions but contains no scalarization, bifurcation, or tachyonic-onset title.",
    ),
    proposal(
        3,
        "GMUT gravitational-wave standard-siren luminosity-distance ratio blind public-data protocol",
        "standard siren, electromagnetic luminosity distance, gravitational-wave propagation distance, selection function, calibration, and blind likelihood",
        "A preregistered zero-row adapter can define the exact public inputs and blind likelihood needed to test a typed GMUT distance-ratio hypothesis without pretending that citations are data.",
        "The protocol ingests no real rows yet reports a fit, omits selection or calibration terms, changes the model after unblinding, or calls a catalog citation empirical evidence.",
        "data_and_independent_review_required",
        "x2_empirical_gate",
        ["S12"],
        ["gmut/standard-siren-study-contract.json", "gmut/standard-siren-zero-row-receipt.json"],
        "Completion requires real standards-conformant event data, frozen analysis, a computed likelihood, uncertainty treatment, and independent review; zero rows must remain open.",
        "Preserve the adapter and preregistration, discard no failed fits, and keep the empirical gap open.",
        ["real_data", "empirical_confirmation", "independent_review", "theory_of_everything"],
        "open_gap",
        "Earlier gravitational-wave proposals concern propagation, counterparts, tidal deformation, or polarization; none freezes a standard-siren gravitational/electromagnetic luminosity-distance ratio study.",
    ),
    proposal(
        4,
        "THOS longitudinal measurement-invariance, response-shift, and differential-item-functioning protocol",
        "blind matched-budget real arms, longitudinal invariance, response shift, differential item functioning, missingness, and independent review",
        "A synthetic protocol can reserve item-level invariance and response-shift tests before any THOS arm comparison, reducing the risk that scale drift is misread as an effect.",
        "The fixture accepts arm comparisons without item invariance, hides differential functioning, substitutes synthetic rows for participants, or claims effectiveness without matched real arms.",
        "participants_and_independent_review_required",
        "x2_proxy_protocol",
        ["S13"],
        ["thos/measurement-invariance-contract.json", "thos/response-shift-proxy-vectors.json"],
        "Structural vectors may pass, but THOS remains proxy until preregistered blind matched-budget real arms, participants, monitoring, statistics, and independent review exist.",
        "Retain the protocol, quarantine noninvariant items, and make no real-effect claim.",
        ["participants", "clinical_effectiveness", "deployment", "independent_review"],
        "represented",
        "The chain covers fidelity, learning curves, crossover effects, rater drift, and non-inferiority, but no title combines longitudinal measurement invariance, response shift, and differential item functioning.",
    ),
    proposal(
        5,
        "Freed ID Digital Credentials API request-origin, user-mediation, abort, and protocol-allowlist profile",
        "browser-mediated credential request, origin binding, protocol allowlist, user mediation, abort semantics, privacy, and synthetic failure vectors",
        "A synthetic browser-bound profile can fail closed on origin mismatch, omitted user mediation, unsupported protocols, ambiguous aborts, and overbroad requested claims.",
        "A vector bypasses user mediation, accepts a mismatched origin, silently retries an abort, treats a draft API as production, or uses real keys or accounts.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["S01", "S02", "S03"],
        ["freed-id/digital-credentials-request-profile.json", "freed-id/digital-credentials-request-vectors.json"],
        "Synthetic vectors must reject seven failure classes; production completion still requires real conformant keys, issuance, resolution, status, interoperability, reviews, recovery, and governance.",
        "Revoke the synthetic transaction, retain the failed vector, and leave production identity operations exact-gated.",
        ["real_keys", "production_identity", "accounts", "interoperability", "trust_governance"],
        "represented",
        "No prior frozen title names the W3C Digital Credentials API or jointly tests request origin, browser user mediation, abort semantics, and a protocol allowlist.",
    ),
    proposal(
        6,
        "CBR museum collections provenance, restitution-candidate triage, affected-community consultation, and Maori-authority gate",
        "collections provenance, restitution candidate triage, source-community consultation, taonga and Maori authority, privacy, law, and refusal",
        "A refusal-first worksheet can show which metadata and consultation questions remain unanswered while preventing repository software from deciding title, restitution, cultural legitimacy, or Maori authority.",
        "The worksheet recommends a transfer, asserts title or cultural status, exposes sensitive provenance, treats a standard as delegated authority, or omits affected-community and Maori decision gates.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["S04", "S05"],
        ["cbr/collections-provenance-reservation.json", "cbr/restitution-authority-matrix.md"],
        "Only authorized affected communities, Maori authorities where applicable, museums, competent legal authorities, and privacy-governed processes can close the gate.",
        "Stop before recommendation, preserve the refusal and unknowns, minimize data, and seek authorized review outside this repository.",
        ["affected_party_authority", "maori_authority", "cultural_legitimacy", "legal_interpretation", "privacy"],
        "exact_gate",
        "The prior CBR chain has many authority gates but no museum-collections provenance or restitution-candidate triage title; this phase does not treat generic authority language as substantive authorization.",
    ),
    proposal(
        7,
        "JSON Schema annotation-output provenance, unevaluated-keyword, and dialect-conformance tribunal",
        "Draft 2020-12 dialect, vocabulary declaration, annotation collection, unevaluated properties, standardized output, and mutation testing",
        "A bounded validator can make schema dialect, vocabulary, annotations, and output provenance explicit so a pass cannot be detached from the evaluator contract.",
        "A fixture accepts an unknown dialect, loses evaluated-location provenance, mishandles unevaluatedProperties, or reports a boolean without the declared output contract.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S06"],
        ["tooling/json-schema-output-contract.json", "tooling/json-schema-mutation-vectors.json"],
        "At least eight positive and negative fixtures must preserve instance and schema locations and reject undeclared vocabulary or unevaluated-keyword errors.",
        "Return the validator to draft, retain the failing fixture, and avoid claiming general JSON Schema conformance.",
        ["exhaustive_conformance", "security_certification", "third_party_data"],
        "completed",
        "No earlier frozen proposal title names JSON Schema, dialect conformance, standardized annotation output, or the unevaluated vocabulary.",
    ),
    proposal(
        8,
        "Language-of-parts, pronunciation reservation, and human-readable expansion accessibility audit",
        "HTML language metadata, language changes, abbreviations, pronunciation-sensitive terms, expansions, and manual user evaluation reservation",
        "A static audit can flag missing document or part language, undefined expansions, and pronunciation-sensitive terms while reserving linguistic correctness and user experience for qualified humans.",
        "The audit infers pronunciation or translation authority, labels the report completely accessible, misses an untagged language switch, or replaces manual and affected-user evaluation.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S07"],
        ["accessibility/language-parts-contract.json", "accessibility/language-parts-audit.json"],
        "Structural fixtures must flag missing language metadata and first-use expansions; manual, linguistic, and affected-user evaluation remain reserved.",
        "Restore explicit language metadata or expansion, retain the exception, and request qualified human review for pronunciation or meaning.",
        ["complete_accessibility", "linguistic_authority", "maori_wording", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility titles cover maps, tables, landmarks, generated content, color, and acronyms; none combines language-of-parts checks with pronunciation reservation and human-readable expansion.",
    ),
    proposal(
        9,
        "Crooks fluctuation-theorem forward/reverse support overlap and psyche-value nonconversion classifier",
        "forward and reverse work distributions, support overlap, equilibrium starts, path reversal, synthetic identity check, and analogy boundary",
        "Synthetic distributions can demonstrate when the Crooks ratio is structurally evaluable and explicitly block conversion of thermodynamic work into psychological worth or effort.",
        "The classifier ignores support mismatch, lacks reverse trajectories, confuses a finite-sample fixture with empirical psychology, or converts work units into psyche value.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["S14"],
        ["thermo-psyche/crooks-overlap-contract.json", "thermo-psyche/crooks-synthetic-vectors.json"],
        "Positive and negative fixtures must distinguish evaluable overlap, missing support, wrong temperature, and forbidden psyche conversion.",
        "Quarantine the analogy, restore dimensioned quantities, and make no participant or mental-state claim.",
        ["participant_inference", "psyche_value_conversion", "empirical_psychology", "consciousness"],
        "completed",
        "The chain contains general fluctuation-theorem and fluctuation-dissipation barriers, but no title tests Crooks forward/reverse work-distribution support overlap.",
    ),
    proposal(
        10,
        "Stage 20 common-cause evidence dependence, diversity budget, and correlated-source nonpromotion board",
        "evidence lineage, common-cause clusters, dependence discount, source diversity, authority noncompensation, and terminal abstention",
        "A structural board can prevent multiple artifacts with a shared source or owner from being counted as independent evidence and preserve abstention when diversity is inadequate.",
        "Shared-lineage artifacts are counted independently, a quantity of correlated receipts compensates for missing authority, same-owner replay is called independent reproduction, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        [],
        ["stage20/evidence-dependence-contract.json", "stage20/diversity-budget-vectors.json"],
        "Mutations must reject duplicate lineage credit, hidden common causes, authority compensation, and independent-reproduction overclaim; verdict remains NOT_READY_FOR_STAGE_20.",
        "Collapse correlated evidence to its common lineage, retain each artifact without extra independence credit, and abstain.",
        ["independent_reproduction", "authority_substitution", "stage20_promotion", "proof_or_canon"],
        "completed",
        "Prior Stage 20 boards cover circular support, minimax regret, multiplicity, freshness, and validation budgets; none titles a common-cause dependence cluster with a source-diversity budget.",
    ),
]


SOURCES = [
    {"source_id": "S01", "title": "W3C Digital Credentials", "authority": "W3C Federated Identity Working Group", "url": "https://www.w3.org/TR/digital-credentials/", "status": "draft", "checked_on": "2026-07-16", "use": "browser mediation, request origin, abort and protocol boundaries"},
    {"source_id": "S02", "title": "OpenID for Verifiable Credential Issuance 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "status": "current", "checked_on": "2026-07-16", "use": "issuance, privacy, deferred transaction and proof requirements"},
    {"source_id": "S03", "title": "Verifiable Credentials Data Model v2.0", "authority": "W3C", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "stable", "checked_on": "2026-07-16", "use": "credential model and nonproduction boundaries"},
    {"source_id": "S04", "title": "ICOM Code of Ethics for Museums", "authority": "International Council of Museums", "url": "https://icom.museum/en/resources/standards-guidelines/code-of-ethics/", "status": "current", "checked_on": "2026-07-16", "use": "museum provenance and restitution context, never delegated authority"},
    {"source_id": "S05", "title": "1970 Convention on illicit transfer of cultural property", "authority": "UNESCO", "url": "https://www.unesco.org/en/legal-affairs/convention-means-prohibiting-and-preventing-illicit-import-export-and-transfer-ownership-cultural", "status": "stable", "checked_on": "2026-07-16", "use": "legal context only; jurisdiction and interpretation remain gated"},
    {"source_id": "S06", "title": "JSON Schema Draft 2020-12", "authority": "JSON Schema project", "url": "https://json-schema.org/draft/2020-12", "status": "stable", "checked_on": "2026-07-16", "use": "dialect, vocabulary, unevaluated keywords and output schema"},
    {"source_id": "S07", "title": "Web Content Accessibility Guidelines 2.2", "authority": "W3C", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "checked_on": "2026-07-16", "use": "language metadata and qualified accessibility boundaries"},
    {"source_id": "S08", "title": "CSS Color Adjustment Module Level 1", "authority": "W3C CSS Working Group", "url": "https://www.w3.org/TR/css-color-adjust-1/", "status": "draft", "checked_on": "2026-07-16", "use": "candidate-recommendation accessibility source watch"},
    {"source_id": "S09", "title": "Git multi-pack-index documentation", "authority": "Git project", "url": "https://git-scm.com/docs/multi-pack-index", "status": "current", "checked_on": "2026-07-16", "use": "disposable Git fixture constraints and inherited seed review"},
    {"source_id": "S10", "title": "Tensor-scalar gravity and binary-pulsar experiments", "authority": "Damour and Esposito-Farese primary research", "url": "https://doi.org/10.1103/PhysRevLett.70.2220", "status": "stable", "checked_on": "2026-07-16", "use": "scalarization theory context only"},
    {"source_id": "S11", "title": "Field reparametrization in effective field theories", "authority": "Passarino primary research", "url": "https://arxiv.org/abs/1610.09618", "status": "stable", "checked_on": "2026-07-16", "use": "EFT equivalence and scope boundary"},
    {"source_id": "S12", "title": "GWTC-3 Data Release Documentation", "authority": "Gravitational Wave Open Science Center", "url": "https://gwosc.org/GWTC-3/", "status": "current", "checked_on": "2026-07-16", "use": "public-data readiness only; zero rows ingested in x1"},
    {"source_id": "S13", "title": "Response shift in patient-reported outcomes", "authority": "Vanier et al. primary research", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8602159/", "status": "stable", "checked_on": "2026-07-16", "use": "longitudinal invariance and response-shift definitions"},
    {"source_id": "S14", "title": "Entropy production fluctuation theorem and nonequilibrium work relation", "authority": "Crooks primary research", "url": "https://doi.org/10.1103/PhysRevE.60.2721", "status": "stable", "checked_on": "2026-07-16", "use": "thermodynamic identity only; no psyche conversion"},
]


def adopt_seed(seed: dict[str, Any], number: int, kind: str) -> dict[str, Any]:
    item = deepcopy(seed)
    item["origin_id"] = item.get("packet_id") or item.get("task_id")
    item["origin_phase"] = SOURCE_PHASE
    item["owner"] = OWNER
    item["review_state"] = "adopted_after_fresh_novelty_safety_compatibility_review"
    item["completion_credit"] = "none_until_v645_v4_x2_witness"
    item["rewrite_or_rejection"] = "accepted_with_owner-scoped identifier and no inherited completion credit"
    if kind in {"safe", "candidate"}:
        item["packet_id"] = f"V6454-ADOPT-{kind.upper()}-{number:02d}"
        item["artifact"] = f"portfolios/{kind}/adopted-{number:02d}.json"
    else:
        item["task_id"] = f"V6454-ADOPT-CLEAN-{number:02d}"
    return item


ADOPTED_SAFE_NOW = [adopt_seed(item, i, "safe") for i, item in enumerate(INHERITED_SAFE_NOW_SEEDS, 1)]
ADOPTED_CANDIDATES = [adopt_seed(item, i, "candidate") for i, item in enumerate(INHERITED_CANDIDATE_SEEDS, 1)]
ADOPTED_CLEAN = [adopt_seed(item, i, "clean") for i, item in enumerate(INHERITED_CLEAN_SEEDS, 1)]


def new_packet(number: int, title: str, kind: str, protected: list[str] | None = None) -> dict[str, Any]:
    return {
        "packet_id": f"V6454-NEW-{kind.upper()}-{number:02d}",
        "owner": OWNER,
        "origin_phase": PHASE,
        "origin": "new_ilyra_proposal",
        "title": title,
        "approval_class": "safe_now_owner_scoped" if kind == "safe" else "bounded_candidate_prototype",
        "hypothesis": f"A bounded owner-scoped implementation of {title.casefold()} can yield an auditable structural witness without crossing protected gates.",
        "null_or_failure": "The artifact is missing, a private or authority boundary is crossed, a failure is erased, or a structural result is overstated.",
        "artifact": f"portfolios/{kind}/new-{number:02d}.json",
        "acceptance_gate": "A phase-local runner must produce a passing witness and retain every failed assumption before completion credit.",
        "rollback_or_recovery": "Retain the negative, restore the last bounded state, and reclassify unavailable evidence or authority as open_gap or exact_gate.",
        "protected_gates": protected or ["private_material", "sibling_lane", "independent_reproduction", "stage20_promotion"],
        "x2_execution": "preregistered_for_bounded_execution",
        "completion_credit": "none_until_v645_v4_x2_witness",
    }


NEW_SAFE_TITLES = [
    "Seed completion-credit anti-inheritance checker",
    "Proposal token-overlap and mission-surface collision explainer",
    "Source ledger status-vocabulary and checked-date validator",
    "Scalarization branch-assumption completeness matrix",
    "Standard-siren zero-row and likelihood-nonclaim guard",
    "THOS item-level invariance prerequisite matrix",
    "Digital Credentials origin and mediation vector compiler",
    "Museum provenance data-minimization refusal worksheet",
    "JSON Schema dialect and vocabulary declaration checker",
    "Language-of-parts and first-use expansion structural audit",
    "Crooks forward-reverse support-overlap fixture scorer",
    "Evidence common-cause cluster and diversity-credit calculator",
    "Named-lane exact-head replay preflight",
    "Owner-generated file-threshold counter",
    "Terminal baton privacy and claim-boundary linter",
]
NEW_SAFE_NOW = [new_packet(i, title, "safe") for i, title in enumerate(NEW_SAFE_TITLES, 1)]

NEW_CANDIDATE_TITLES = [
    "Scalarization bifurcation graph renderer",
    "Standard-siren catalog schema dry-run adapter",
    "Longitudinal item-invariance mutation generator",
    "Digital Credentials abort-race state explorer",
    "Collections provenance missing-evidence heatmap",
    "JSON Schema recommended-output normalizer",
    "HTML language-switch fixture generator",
    "Crooks overlap-window sensitivity explorer",
    "Evidence-dependence union-find prototype",
    "Claim-to-source status-drift dashboard",
]
NEW_CANDIDATES = [new_packet(i, title, "candidate") for i, title in enumerate(NEW_CANDIDATE_TITLES, 1)]


ADOPTED_SKILLS = [(name, description, "adopted_after_review") for name, description in INHERITED_SKILL_SEEDS]
NEW_SKILLS = [
    ("ghc-audit-seed-completion-credit", "Separate inherited proposal lineage from owner-earned completion credit."),
    ("ghc-screen-scalarization-branches", "Check scalarization onset, branch, stability, and EFT reservations."),
    ("ghc-reserve-standard-siren-data", "Keep a zero-row standard-siren adapter from becoming an empirical claim."),
    ("ghc-check-longitudinal-invariance", "Check synthetic measurement-invariance and response-shift prerequisites."),
    ("ghc-profile-digital-credential-mediation", "Test origin, mediation, abort, and protocol-allowlist vectors."),
    ("ghc-reserve-collections-authority", "Keep museum provenance and restitution questions under affected authority."),
    ("ghc-validate-json-schema-output", "Validate declared dialect, annotation locations, and bounded output form."),
    ("ghc-audit-language-parts", "Audit static language metadata and expansions while reserving human evaluation."),
    ("ghc-check-crooks-overlap", "Check synthetic forward/reverse support without psyche conversion."),
    ("ghc-budget-evidence-diversity", "Cluster common-cause evidence and block false independence credit."),
]

ADOPTED_RUNNERS = [(name, description, "adopted_after_review") for name, description in INHERITED_RUNNER_SEEDS]
NEW_RUNNERS = [
    ("ghc_family_v645_v4_portfolio_runner.py", "Execute adopted and new safe/candidate portfolios with owner witnesses."),
    ("ghc_family_v645_v4_core_runner.py", "Build the ten bounded core proposal artifacts and truth labels."),
    ("ghc_family_v645_v4_skill_runner.py", "Validate and invoke every phase skill through a registry."),
    ("ghc_family_v645_v4_accessibility_runner.py", "Audit the static report language and structural accessibility contract."),
    ("ghc_family_v645_v4_validation_runner.py", "Run scoped phase checks, privacy scans, manifests, and ancestry gates."),
]


def new_clean(number: int, title: str) -> dict[str, Any]:
    return {
        "task_id": f"V6454-NEW-CLEAN-{number:02d}",
        "owner": OWNER,
        "origin": "new_ilyra_task",
        "title": title,
        "destructive": False,
        "execution": "preregistered_owner_scoped_safe_now",
        "acceptance": "Emit a bounded x2 receipt, preserve failures, and make no destructive or authority-crossing change.",
        "rollback": "Restore the last owner-scoped generated artifact and retain the failed witness.",
    }


NEW_CLEAN_TITLES = [
    "Normalize all new JSON writes to UTF-8 and LF",
    "Separate slow Git scans from definition inspection",
    "Set UTF-8 console output for Unicode-bearing audits",
    "Bind all phase paths to repository-relative identifiers",
    "Check every document remains below six thousand words",
    "Check the integrated overview remains three-page-equivalent",
    "Check source status uses only current stable draft or watch",
    "Check core outcomes use only four allowed truth labels",
    "Check inherited seeds have zero pre-witness completion credit",
    "Check skills contain bounded trigger and authority language",
    "Check runner registry records actual invocation witnesses",
    "Check sandbox artifacts remain unlaunched preparation only",
    "Check manual and affected-user accessibility evaluation remains reserved",
    "Check same-owner replay is not independent reproduction",
    "Check terminal verdict remains NOT_READY_FOR_STAGE_20",
]
NEW_CLEAN = [new_clean(i, title) for i, title in enumerate(NEW_CLEAN_TITLES, 1)]
