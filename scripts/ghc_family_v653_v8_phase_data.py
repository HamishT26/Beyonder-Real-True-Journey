#!/usr/bin/env python3
"""Frozen Liora Venn v653-v8 x1 data.

This module contains preregistration inputs only. It deliberately contains no
x2 observations, mutation outcomes, completion receipts, or route result.
"""

from __future__ import annotations


PHASE = "v653-v8"
PHASE_ID = "v653-gmut-thos-v8-x1-x2"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "solo v653-v8 continuity and evidence steward"
HOPE = (
    "leave a clean, exact, auditable handoff while keeping every protected "
    "gate honestly open where evidence does not close it"
)
PHASE_ROOT = "docs/liora-venn/v653-v8"
BRANCH = "codex/GHC-Family/liora-venn-v653-v8-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v653-v7-full-tools"
SOURCE_PARENT = "c044464ed940093d59a59686efd4faa61853f341"
SOURCE_X1 = "78ece91db153275ca2857899ee125dc0673c0154"
SOURCE_EVIDENCE = "888df289dd58f5717919ac1ee2c8083cd93cddfe"
SOURCE_CLOSEOUT = "cceb53e1bc5ad0c5e9b4a01cc3eac42f3a360b8b"
SOURCE_CORRECTION_1 = "e94f2f3c048678b6d7c87c6d4037dc8b24787c4a"
SOURCE_CORRECTION_2 = "0eb92e13d6105345635e4f9cf87626b0b2462995"
SOURCE_HEAD = "144a4d51195d777ea2b8068bb4cf7ed82fff21be"

PRIOR_FROZEN = 1630
INHERITED_NEGATIVES = 10447
ACTIVATION_NEGATIVE_BASELINE = 10447
INHERITED_OPEN_GAPS = 76
INHERITED_EXACT_GATES = 77
INHERITED_METHOD_FLOW_FAILED = 17
INHERITED_METHOD_FLOW_PASSING = 17
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "synthetic apiary inspection, bee-health observation, batch traceability, "
    "workload control, correction readback, and shift handover"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "real_empirical_data",
    "participant_beekeeper_landholder_or_operator_evidence",
    "veterinary_apiculture_food_safety_or_other_professional_review",
    "production_identity_traceability_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "disease_notification_treatment_destruction_and_food_legal_authority",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_and_remedy",
    "independent_team_reproduction",
    "agi_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def source(source_id, status, kind, title, url, implication):
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "phase_implication": implication,
    }


SOURCE_SPECS = [
    (
        "SRC-MPI-BEE-BIOSECURITY",
        "current",
        "official_guidance",
        "New Zealand Ministry for Primary Industries bee biosecurity resources",
        "https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-and-diseases/bee-biosecurity/bee-biosecurity-resources",
        "Supports bounded biosecurity vocabulary and source routing without diagnosing disease, directing notification, or conferring authority.",
    ),
    (
        "SRC-MPI-RESPONSIBLE-BEEKEEPING",
        "current",
        "official_guidance",
        "New Zealand responsible beekeeping guide",
        "https://www.mpi.govt.nz/dmsdocument/56599/direct",
        "Supports synthetic inspection, equipment, feeding, safety, and record prompts without professional or operational approval.",
    ),
    (
        "SRC-MPI-VARROA",
        "current",
        "official_guidance",
        "New Zealand varroa management checklist",
        "https://www.mpi.govt.nz/dmsdocument/56596/direct",
        "Supports method-labelled monitoring and treatment-record obligations without diagnosis, efficacy, dosing, or treatment authority.",
    ),
    (
        "SRC-WOAH-BEE-DISEASES",
        "current",
        "official_standard",
        "World Organisation for Animal Health diseases of bees",
        "https://www.woah.org/en/disease/diseases-of-bees/",
        "Supports disease-scope and surveillance vocabulary without case classification, international reporting, or veterinary authority.",
    ),
    (
        "SRC-AFB-AGENCY",
        "current",
        "official_programme",
        "New Zealand American Foulbrood Pest Management Agency",
        "https://afb.org.nz/",
        "Supports routing to the competent programme while preserving suspicion, inspection, notification, destruction, and enforcement authority.",
    ),
    (
        "SRC-AFB-OPERATIONAL-PLAN",
        "watch",
        "official_programme_document",
        "American Foulbrood National Pest Management Plan operational plan",
        "https://afb.org.nz/wp-content/uploads/2021/11/AFB_Operational-Plan_Nov2021.pdf",
        "Supplies a dated operational reference that requires current competent review before any real-world use.",
    ),
    (
        "SRC-NZ-AFB-ORDER",
        "watch",
        "official_legislation",
        "Biosecurity National American Foulbrood Pest Management Plan Order 1998",
        "https://www.legislation.govt.nz/regulation/public/1998/0260/latest/DLM258621.html",
        "Supports a legal-source watch and exact-gate reservation only; this phase makes no interpretation of current duties or powers.",
    ),
    (
        "SRC-MPI-BEE-RMP",
        "current",
        "official_guidance",
        "Honey and bee product risk management programmes",
        "https://www.mpi.govt.nz/food-business/honey-bee-products-processing-requirements/honey-bee-product-risk-management-programmes",
        "Supports nonproduction food-safety record fields without approving a risk management programme or product.",
    ),
    (
        "SRC-MPI-BEE-FOOD-SAFETY",
        "current",
        "official_guidance",
        "Food safety for beekeepers",
        "https://www.mpi.govt.nz/agriculture/beekeeping-loss-survey-tutin-contamination-regulations/food-safety-for-beekeepers",
        "Supports synthetic contamination holds and traceability prompts without food-safety verification or market-release authority.",
    ),
    (
        "SRC-MPI-BEE-FORMS",
        "current",
        "official_guidance",
        "Honey and bee product forms, templates, and requirements",
        "https://www.mpi.govt.nz/food-business/honey-bee-products-processing-requirements/honey-and-bee-product-forms-templates-and-requirements",
        "Supports bounded field-shape comparison without completing, lodging, or approving a regulatory record.",
    ),
    (
        "SRC-CODEX-HONEY",
        "current",
        "official_standard",
        "Codex Standard for Honey CXS 12-1981",
        "https://www.fao.org/fao-who-codexalimentarius/sh-proxy/en/?lnk=1&url=https%3A%2F%2Fworkspace.fao.org%2Fsites%2Fcodex%2FStandards%2FCXS+12-1981%2FCXS_012e.pdf",
        "Supports typed composition and moisture vocabulary without sampling, conformity assessment, certification, or release.",
    ),
    (
        "SRC-ISO-22005",
        "current",
        "official_standard",
        "ISO 22005 traceability in the feed and food chain",
        "https://www.iso.org/standard/36297.html",
        "Supports traceability-system design vocabulary without certification, audit, or production-chain evidence.",
    ),
    (
        "SRC-GS1-EPCIS",
        "current",
        "official_standard",
        "GS1 EPCIS standard",
        "https://ref.gs1.org/standards/epcis/",
        "Supports a synthetic event-profile contract without conformant live events, trading partners, certification, or interoperability.",
    ),
    (
        "SRC-GS1-CBV",
        "current",
        "official_standard",
        "GS1 Core Business Vocabulary standard",
        "https://ref.gs1.org/standards/cbv/",
        "Supports controlled-vocabulary checks without production master data or interoperability.",
    ),
    (
        "SRC-GS1-DIGITAL-LINK",
        "current",
        "official_standard",
        "GS1 Digital Link URI syntax",
        "https://ref.gs1.org/standards/digital-link/",
        "Supports synthetic identifier and URI fixtures without assigning real identifiers or resolving production data.",
    ),
    (
        "SRC-GS1-RESOLVER",
        "current",
        "official_standard",
        "GS1-Conformant Resolver Standard",
        "https://ref.gs1.org/standards/resolver/",
        "Supports a nonnetwork resolver decision profile without service operation, certification, or interoperability.",
    ),
    (
        "SRC-FAOSTAT-HONEY",
        "current",
        "official_data_portal",
        "FAO honey and beeswax statistics",
        "https://www.fao.org/forestry/nwfp/statistics/honey-and-beeswax/en",
        "Defines a zero-query, zero-download readiness boundary; a portal citation is not a data row or empirical result.",
    ),
    (
        "SRC-MCKENDRICK-1926",
        "stable",
        "primary_research",
        "Applications of Mathematics to Medical Problems",
        "https://doi.org/10.1017/S0013091500034428",
        "Supports an age-structured transport-equation lineage without estimating a colony or asserting biological fit.",
    ),
    (
        "SRC-SINKO-STREIFER-1967",
        "stable",
        "primary_research",
        "A New Model for Age-Size Structure of a Population",
        "https://doi.org/10.2307/1934533",
        "Supports age-size state and boundary-condition obligations without empirical calibration.",
    ),
    (
        "SRC-CRUMP-MODE-1968",
        "stable",
        "primary_research",
        "A General Age-Dependent Branching Process I",
        "https://doi.org/10.1016/0022-247X(68)90005-X",
        "Supports general age-dependent branching definitions without modelling a real colony.",
    ),
    (
        "SRC-CRUMP-MODE-1969",
        "stable",
        "primary_research",
        "A General Age-Dependent Branching Process II",
        "https://doi.org/10.1016/0022-247X(69)90210-8",
        "Supports renewal and limit-theorem obligation fields without empirical credit.",
    ),
    (
        "SRC-JAGERS-1969",
        "stable",
        "primary_research",
        "A general stochastic model for population development",
        "https://doi.org/10.1080/03461238.1969.10405220",
        "Supports a typed general branching-process domain without biological validation.",
    ),
    (
        "SRC-JAGERS-NERMAN-1984",
        "stable",
        "primary_research",
        "The growth and composition of branching populations",
        "https://doi.org/10.2307/1427068",
        "Supports population-characteristic and asymptotic-obligation fields without fitting observed populations.",
    ),
    (
        "SRC-GILLESPIE-1977",
        "stable",
        "primary_research",
        "Exact stochastic simulation of coupled chemical reactions",
        "https://doi.org/10.1021/j100540a008",
        "Supports Markov-jump event, propensity, and time-step obligations without converting a chemical simulation method into colony evidence.",
    ),
    (
        "SRC-WCAG22",
        "current",
        "official_recommendation",
        "Web Content Accessibility Guidelines 2.2",
        "https://www.w3.org/TR/WCAG22/",
        "Supports structural checklist checks while reserving manual and affected-user accessibility evaluation.",
    ),
    (
        "SRC-LOCAL-CONTEXTS",
        "current",
        "affected_community_governance",
        "Local Contexts Labels and Notices",
        "https://localcontexts.org/labels/traditional-knowledge-labels/",
        "Requires community-specific knowledge, access, use, and governance decisions to remain with authorized communities.",
    ),
    (
        "SRC-MAORI-DATA",
        "current",
        "maori_authority_principles",
        "Principles of Māori Data Sovereignty",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "Requires Māori data, place, governance, access, interpretation, and remedy decisions to remain with Māori authorities.",
    ),
]

SOURCES = [source(*spec) for spec in SOURCE_SPECS]


def proposal(number, title, slug, pillar, disposition, source_ids, novelty):
    if disposition == "completed":
        approval = "safe_now_bounded_symbolic_or_software"
        lane = "x2_owner_local_synthetic"
        acceptance = (
            "Reject all five frozen mutations and emit only the declared "
            "symbolic, structural, or owner-local software contract."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_proxy"
        lane = "x2_synthetic_proxy_only"
        acceptance = (
            "Reject all five frozen mutations and retain represented status "
            "with no operational, professional, production, interoperability, "
            "privacy-complete, food-safety, disease-control, or authority credit."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_data_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        acceptance = (
            "Emit a zero-row refusal with no query, download, ingest, "
            "calibration, fit, trend, prediction, or empirical promotion."
        )
    else:
        approval = (
            "exact_affected_party_professional_legal_cultural_accessibility_"
            "food_safety_disease_control_and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved decision rights and reservations only; make no "
            "disease notification, diagnosis, treatment, destruction, food "
            "release, landholder, worker-safety, privacy, remedy, legal, "
            "cultural, data-governance, Māori-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"V6538-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "hypothesis": (
            f"A bounded {slug.replace('-', ' ')} contract can make its "
            "obligations machine-checkable without crossing a protected gate."
        ),
        "null_or_failure_condition": (
            "Any required field is absent, a frozen mutation passes, a failed "
            "witness is erased, or the artifact promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop the proposal, retain the failure with zero credit, rewrite no "
            "history, and leave external, sibling, participant, production, "
            "professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1600_frozen_proposals": novelty,
        "novelty_against_1630_frozen_proposals": novelty,
    }


PROPOSAL_SPECS = [
    ("THOS apiary registry site-code, coordinate minimization, access role, change reason, retention, deletion, export, and location-privacy boundary", "apiary-registry-location-privacy", "THOS Body", "completed", ["SRC-MPI-BEE-BIOSECURITY", "SRC-MAORI-DATA"], "No frozen row isolates an apiary registry with site-code lineage and coordinate-minimization refusal."),
    ("THOS hive-body component, colony-unit, frame, box, queen, equipment tag, merge, split, transfer, retirement, and lineage tribunal", "hive-colony-lineage-tribunal", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING", "SRC-ISO-22005"], "No frozen row isolates hive hardware and colony-unit identity across merges, splits, transfers, and retirement."),
    ("THOS brood-frame observation, observer role, method, timestamp, confidence, uncertainty, image link, correction, escalation hold, and non-diagnosis board", "brood-observation-uncertainty", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING", "SRC-WOAH-BEE-DISEASES"], "No frozen row isolates brood-frame observation confidence, uncertainty, correction, and diagnosis refusal."),
    ("THOS American foulbrood suspicion cue, sample identifier, custody step, competent contact route, notification hold, correction, and authority firewall", "afb-suspicion-custody-firewall", "THOS Body", "completed", ["SRC-AFB-AGENCY", "SRC-AFB-OPERATIONAL-PLAN", "SRC-NZ-AFB-ORDER"], "No frozen row isolates AFB suspicion custody and competent-route fields while refusing diagnosis and legal action."),
    ("THOS varroa sugar-shake, alcohol-wash, sticky-board, visual-check method label, denominator, interval, comparability refusal, and uncertainty tribunal", "varroa-method-nonequivalence", "THOS Body", "completed", ["SRC-MPI-VARROA"], "No frozen row isolates method-labelled varroa observations with explicit denominator and cross-method non-equivalence."),
    ("THOS hive treatment product, batch, expiry, method, quantity, unit, authorization hold, withdrawal field, adverse observation, and dose-refusal board", "treatment-batch-dose-refusal", "THOS Body", "completed", ["SRC-MPI-VARROA", "SRC-MPI-BEE-FOOD-SAFETY"], "No frozen row isolates apiary treatment batch and withdrawal records while refusing dose advice or efficacy."),
    ("THOS hive tool cleaning, equipment transfer, source apiary, destination apiary, quarantine hold, contamination cue, release authority, and traceability board", "equipment-transfer-quarantine", "THOS Body", "completed", ["SRC-MPI-BEE-BIOSECURITY", "SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates equipment-cleaning and cross-apiary transfer lineage with a release-authority hold."),
    ("THOS queen introduction, source, cage, colony, observation window, acceptance cue, correction, supersession, outcome uncertainty, and lineage board", "queen-introduction-lineage", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates queen introduction lineage, observation windows, supersession, and outcome uncertainty."),
    ("THOS swarm report, observation confidence, property-boundary cue, contact consent, relocation hold, correction, handover, and decision-reservation board", "swarm-relocation-reservation", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates swarm report confidence, consent, property boundary, and relocation-decision reservation."),
    ("THOS syrup or pollen-substitute feed batch, ingredient, supplier, expiry, preparation time, contamination cue, hold, disposal, and lineage tribunal", "feed-batch-contamination-hold", "THOS Body", "completed", ["SRC-MPI-BEE-FOOD-SAFETY", "SRC-ISO-22005"], "No frozen row isolates apiary feed batch lineage and contamination hold without food-safety promotion."),
    ("THOS honey-super placement, removal, brood-presence cue, treatment window, contamination hold, correction, release authority, and lineage board", "honey-super-contamination-hold", "THOS Body", "completed", ["SRC-MPI-BEE-FOOD-SAFETY", "SRC-MPI-BEE-RMP"], "No frozen row isolates honey-super timing and brood or treatment contamination holds with release authority reserved."),
    ("THOS extraction batch, source hive lot, vessel, equipment run, split, merge, hold, correction, recall rehearsal, and traceability tribunal", "extraction-batch-recall-lineage", "THOS Body", "completed", ["SRC-ISO-22005", "SRC-MPI-BEE-RMP", "SRC-MPI-BEE-FORMS"], "No frozen row isolates bee-product extraction split-merge lineage and a nonproduction recall rehearsal."),
    ("THOS honey refractometer identifier, calibration reference, temperature, replicate, reading, uncertainty, limit, hold, correction, and conformity-refusal board", "honey-moisture-calibration", "THOS Body", "completed", ["SRC-CODEX-HONEY", "SRC-MPI-BEE-FOOD-SAFETY"], "No frozen row isolates honey-moisture instrument identity, replicate uncertainty, and conformity refusal."),
    ("THOS apiary temperature logger identity, clock source, timezone, sampling interval, missing interval, drift, reset, correction, and inference-refusal tribunal", "apiary-logger-timebase", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates apiary logger timebase, drift, reset, missing intervals, and biological-inference refusal."),
    ("THOS beeswax rendering batch, source lot, vessel, temperature unit, time interval, foreign-material cue, cross-batch hold, correction, and release refusal", "wax-rendering-batch-hold", "THOS Body", "completed", ["SRC-MPI-BEE-FOOD-SAFETY", "SRC-ISO-22005"], "No frozen row isolates beeswax rendering batch lineage, foreign-material cues, and cross-batch hold."),
    ("THOS pollination placement request, crop code, synthetic apiary code, date window, pesticide-information hold, landholder consent, correction, and placement-reservation board", "pollination-placement-reservation", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates pollination placement timing, pesticide-information hold, landholder consent, and decision reservation."),
    ("THOS worker exposure cue, protective-equipment field, emergency-information acknowledgement, lone-work check, stop-work state, correction, and medical-advice refusal board", "worker-exposure-stop-work", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates apiary exposure and lone-work stop states while refusing medical or safety adequacy claims."),
    ("THOS apiary lift, heat, travel, inspection duration, break, workload threshold, unfinished work, correction readback, and shift-handover board", "apiary-workload-handover", "THOS Body", "completed", ["SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates apiary manual-handling, heat, travel, unfinished-work, and correction-readback handover fields."),
    ("THOS accessible apiary inspection checklist section, current step, required field, error association, noncolour state, print fallback, correction, and manual-review reservation", "accessible-apiary-checklist", "THOS Body", "completed", ["SRC-WCAG22"], "No frozen row isolates an apiary inspection stepper with print fallback and manual accessibility review reserved."),
    ("THOS apiary observation image EXIF, coordinate, person, vehicle, property marker, minimization, redaction, retention, deletion, and export tribunal", "apiary-image-privacy", "THOS Body", "completed", ["SRC-MPI-BEE-BIOSECURITY", "SRC-MAORI-DATA"], "No frozen row isolates apiary image EXIF and property-marker minimization with retention and deletion controls."),
    ("GMUT McKendrick-von Foerster age transport, state density, ageing velocity, mortality term, recruitment boundary, initial condition, unit, positivity, and empirical firewall", "mckendrick-age-transport", "GMUT Mind", "completed", ["SRC-MCKENDRICK-1926", "SRC-SINKO-STREIFER-1967"], "No frozen row isolates an age-transport population PDE with recruitment boundary and colony-evidence firewall."),
    ("GMUT Crump-Mode-Jagers general branching individual, life length, reproduction point process, characteristic, renewal equation, filtration, asymptotic premise, and empirical firewall", "cmj-branching-renewal", "GMUT Mind", "completed", ["SRC-CRUMP-MODE-1968", "SRC-CRUMP-MODE-1969", "SRC-JAGERS-1969", "SRC-JAGERS-NERMAN-1984"], "No frozen row isolates CMJ life histories, random characteristics, renewal obligations, and colony-evidence firewall."),
    ("GMUT Gillespie Markov-jump state, reaction channel, propensity, total rate, event selection, waiting time, random stream, absorbing state, and domain classifier", "gillespie-jump-domain", "GMUT Mind", "completed", ["SRC-GILLESPIE-1977"], "No frozen row isolates Gillespie event selection and waiting-time obligations while refusing conversion into bee-population evidence."),
    ("THOS apiary inspection arrival, hive order, observation cue, biosecurity hold, unfinished item, correction readback, workload, and shift-handover proxy", "apiary-inspection-handover-proxy", "THOS Body", "represented", ["SRC-MPI-BEE-BIOSECURITY", "SRC-MPI-RESPONSIBLE-BEEKEEPING"], "No frozen row isolates a synthetic apiary inspection sequence with biosecurity holds and shift handover."),
    ("THOS American foulbrood suspicion, competent-route escalation, quarantine cue, notification state, record correction, workload, and shift-handover proxy", "afb-escalation-handover-proxy", "THOS Body", "represented", ["SRC-AFB-AGENCY", "SRC-NZ-AFB-ORDER"], "No frozen row isolates a synthetic AFB escalation handover while preserving diagnosis, notification, and enforcement authority."),
    ("Freed ID GS1 EPCIS event type, event time, read point, business location, disposition, source, destination, correction, privacy, and nonproduction profile", "epcis-apiary-event-profile", "Freed ID/CBR Heart", "represented", ["SRC-GS1-EPCIS"], "No frozen row isolates an apiary-shaped EPCIS event profile with correction, location privacy, and nonproduction limits."),
    ("Freed ID GS1 Core Business Vocabulary business step, disposition, source-destination type, vocabulary status, extension, version, refusal, and nonproduction profile", "cbv-apiary-vocabulary-profile", "Freed ID/CBR Heart", "represented", ["SRC-GS1-CBV"], "No frozen row isolates an apiary traceability CBV selection profile with extension and vocabulary-version refusal."),
    ("Freed ID GS1 Digital Link identifier key, qualifier, data attribute, URI canonicalization, resolver link type, redirect, cache, privacy, and nonproduction profile", "digital-link-apiary-profile", "Freed ID/CBR Heart", "represented", ["SRC-GS1-DIGITAL-LINK", "SRC-GS1-RESOLVER"], "No frozen row isolates Digital Link URI and resolver obligations for synthetic apiary identifiers with privacy and nonproduction holds."),
    ("THOS FAOSTAT beehive, honey, beeswax country, item, element, unit, year, flag, revision, zero-row, and trend-inference-refusal adapter", "faostat-apiary-zero-row-adapter", "THOS Body", "open_gap", ["SRC-FAOSTAT-HONEY"], "No frozen row isolates FAOSTAT beehive and bee-product series as a zero-query, zero-download trend-inference refusal."),
    ("CBR bee disease notification, apiary location, landholder and worker privacy, treatment and destruction, food traceability, remedy, affected-party, legal, cultural, data-governance, and Māori-authority reservation", "apiary-authority-reservation", "Freed ID/CBR Heart", "exact_gate", ["SRC-AFB-AGENCY", "SRC-NZ-AFB-ORDER", "SRC-MPI-BEE-RMP", "SRC-LOCAL-CONTEXTS", "SRC-MAORI-DATA"], "No frozen row isolates bee-disease, location, treatment, food, remedy, affected-party, legal, cultural, and Māori authority in one reservation matrix."),
]

PROPOSALS = [
    proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)
]

MUTATION_KINDS = [
    "drop_required_field",
    "cross_bind_source_or_identifier",
    "invert_or_weaken_boundary",
    "inject_unsupported_promotion",
    "erase_failure_or_rollback",
]

SAFE_NOW_TASKS = [
    f"Execute the bounded contract, five frozen mutations, and receipt for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]
SAFE_TASKS = SAFE_NOW_TASKS
CANDIDATE_TASKS = [
    f"Prepare and bounded-test a nonpromotional extension for {row['proposal_id']} without crossing {row['execution_lane']}."
    for row in PROPOSALS
]

SKILL_IDEAS = [
    ("ghc-family-apiary-registry-privacy-boundary", "Review site-code lineage and coordinate minimization without location or governance authority."),
    ("ghc-family-colony-lineage-traceability", "Review hive, colony, component, split, merge, and transfer identity without production evidence."),
    ("ghc-family-brood-observation-uncertainty", "Review observation confidence and correction while refusing disease diagnosis."),
    ("ghc-family-bee-disease-authority-rail", "Review competent-route and custody fields while reserving notification, treatment, destruction, and enforcement."),
    ("ghc-family-varroa-method-nonequivalence", "Review monitoring-method labels and denominators without diagnosis, dosing, or efficacy claims."),
    ("ghc-family-apiary-batch-traceability", "Review treatment, feed, super, extraction, and wax batch lineage without food-safety or release credit."),
    ("ghc-family-honey-moisture-calibration-guard", "Review instrument, replicate, unit, uncertainty, and hold fields without conformity assessment."),
    ("ghc-family-age-branching-domain-firewall", "Review age-transport and branching-process obligations without biological fit or empirical credit."),
    ("ghc-family-apiary-handover-proxy-boundary", "Review synthetic inspection and workload handovers without competence or operational authority."),
    ("ghc-family-apiary-authority-reservation", "Reserve disease, location, landholder, worker, food, remedy, legal, cultural, and Māori authority."),
]
SKILL_TASKS = [
    f"Build phase-local review skill {index:02d} named {name} with an explicit nonpromotion boundary."
    for index, (name, _description) in enumerate(SKILL_IDEAS, 1)
]

RUNNER_IDEAS = [
    ("ghc_family_apiary_registry_privacy_boundary.py", "apiary-registry-privacy"),
    ("ghc_family_colony_lineage_traceability.py", "colony-lineage"),
    ("ghc_family_brood_observation_uncertainty.py", "brood-observation"),
    ("ghc_family_bee_disease_authority_rail.py", "bee-disease-authority"),
    ("ghc_family_varroa_method_nonequivalence.py", "varroa-method"),
    ("ghc_family_apiary_batch_traceability.py", "apiary-batch"),
    ("ghc_family_honey_moisture_calibration_guard.py", "honey-moisture"),
    ("ghc_family_age_branching_domain_firewall.py", "age-branching"),
    ("ghc_family_apiary_handover_proxy_boundary.py", "apiary-handover"),
    ("ghc_family_apiary_authority_reservation.py", "apiary-authority"),
]
RUNNER_TASKS = [
    f"Build and invoke family-compatible bounded runner {index:02d} for {surface}."
    for index, (_name, surface) in enumerate(RUNNER_IDEAS, 1)
]

CLEAN_FIX_REFINE_TASKS = [
    f"REFINE-{index:02d}: review {row['slug']} terminology, falsifier, rollback, source status, and protected-gate wording without changing its frozen outcome class."
    for index, row in enumerate(PROPOSALS, 1)
]

X1_NEGATIVES = [
    (
        "V6538-X1-N01",
        "activation_read_interrupted_before_eof",
        "The first activation-file read was interrupted before attributable EOF evidence and received zero activation-read credit.",
        "Restart at line one, read every bounded chunk through the declared final line, and verify EOF before mutation.",
    ),
    (
        "V6538-X1-N02",
        "worktree_add_wrapper_timeout",
        "The single worktree-add wrapper timed out while Git processes were still completing and received zero lane-creation completion credit.",
        "Do not replay the mutation; inspect processes, path, worktree registration, branch, exact head, and clean state with isolated read-only probes.",
    ),
    (
        "V6538-X1-N03",
        "combined_post_timeout_audit_timeout",
        "The first combined post-timeout worktree audit also timed out before an attributable result and received zero verification credit.",
        "Split process, path, registration, branch, head, and status checks into bounded isolated probes.",
    ),
    (
        "V6538-X1-N04",
        "powershell_convertfromjson_depth_unsupported",
        "The first frozen-index parse supplied an unsupported ConvertFrom-Json Depth parameter and received zero corpus-audit credit.",
        "Inspect the installed PowerShell command surface and parse the bounded JSON without the unsupported parameter.",
    ),
    (
        "V6538-X1-N05",
        "overbroad_corpus_display_truncated",
        "An overbroad read-only corpus display produced thousands of lines and was truncated before it could serve as a review witness.",
        "Use exact schema counts, bounded recent-title slices, and targeted mechanism-token searches while retaining the complete machine-read audit.",
    ),
    (
        "V6538-X1-N06",
        "powershell_foreach_pipe_parse_failure",
        "A bounded script-inventory probe piped a foreach block directly and hit the empty-pipe-element parser error before producing its summary.",
        "Materialize foreach output in an array before formatting, filtering, or measurement.",
    ),
    (
        "V6538-X1-N07",
        "x1_workflow_wrapper_self_recursion",
        "The first x1 generator reached workflow refinement, then recursively called the wrapper-replaced workflow function until Python stopped with RecursionError; the aggregate received zero build credit.",
        "Bind the inherited workflow function before installing the wrapper override, keep the partial packet outcome-free, and rerun the x1-only generator after the narrow repair.",
    ),
    (
        "V6538-X1-N08",
        "workflow_messaging_enum_mismatch",
        "The first complete x1 generator produced a 19-of-20 workflow audit because custom messaging enum values did not satisfy the installed canonical policy; the aggregate received zero workflow-validation credit.",
        "Use the canonical existing-task-after-terminal-gate and user-mediated-file-relay-only enums while retaining the stricter live prose boundary.",
    ),
]

REJECTED_COLLISIONS = [
    "A generic farm asset registry was rejected because frozen rows already cover assets; v653-v8 isolates apiary site-code and coordinate-minimization obligations.",
    "A generic animal-health record was rejected because frozen rows cover health records; v653-v8 isolates brood observation uncertainty and explicit disease-diagnosis refusal.",
    "A generic pest checklist was rejected because frozen rows cover pest controls; v653-v8 isolates varroa method labels, denominators, and non-equivalence.",
    "A generic food batch tracker was rejected because frozen rows cover food traceability; v653-v8 isolates honey-super, extraction, feed, and wax lineage with release holds.",
    "A generic cold-chain logger was rejected because frozen rows cover sensor telemetry; v653-v8 isolates apiary logger clock drift, missing intervals, and biological-inference refusal.",
    "A generic workplace checklist was rejected because frozen rows cover safety forms; v653-v8 isolates apiary exposure, lone-work, stop-work, and medical-advice refusal.",
    "A generic population model was rejected because frozen rows cover population dynamics; v653-v8 isolates McKendrick transport, CMJ characteristics, and Gillespie domain separation.",
    "A generic GS1 profile was rejected because frozen rows cover identifiers; v653-v8 isolates apiary-shaped EPCIS, CBV, and Digital Link correction and privacy boundaries.",
    "A generic agriculture statistics adapter was rejected because frozen rows cover zero-row adapters; v653-v8 isolates FAOSTAT beehive and bee-product series with trend refusal.",
    "A generic indigenous-data notice was rejected because frozen rows cover governance; v653-v8 keeps bee disease, location, food, remedy, affected-party, legal, cultural, and Māori authority together as an unresolved exact gate.",
]
