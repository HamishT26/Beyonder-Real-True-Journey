#!/usr/bin/env python3
"""Frozen x1 catalogue for Vesper Arlen's v656-v8 phase."""

from __future__ import annotations


def source(
    source_id: str,
    title: str,
    publisher: str,
    url: str,
    status: str,
    use: str,
) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-07-31",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source(
        "FAO-GENEBANK-STANDARDS",
        "Genebank Standards for Plant Genetic Resources for Food and Agriculture",
        "Food and Agriculture Organization of the United Nations",
        "https://www.fao.org/plant-treaty/areas-of-work/the-multilateral-system/genebank-standards/en/",
        "current",
        "seed accession, storage, viability, regeneration, documentation, and distribution vocabulary only",
    ),
    source(
        "FAO-PLANT-TREATY",
        "International Treaty on Plant Genetic Resources for Food and Agriculture",
        "Food and Agriculture Organization of the United Nations",
        "https://www.fao.org/plant-treaty/overview/text-treaty/en/",
        "current",
        "treaty and Farmers' Rights context only; no legal interpretation, access decision, or benefit-sharing authority",
    ),
    source(
        "KEW-MSB",
        "Millennium Seed Bank",
        "Royal Botanic Gardens, Kew",
        "https://www.kew.org/science/collections-and-resources/research-facilities/millennium-seed-bank",
        "current",
        "seed conservation, research, processing, banking, and partnership vocabulary only",
    ),
    source(
        "KEW-SEED-ACCESS",
        "Access our seed collections",
        "Royal Botanic Gardens, Kew",
        "https://www.kew.org/science/engage/accessing-our-science/access-our-collections/seed-collections",
        "current",
        "request, availability, terms, material, and distribution vocabulary with every real release decision reserved",
    ),
    source(
        "KEW-SEED-CONSERVATION-STANDARDS",
        "Seed Conservation Standards for MSB Partnership Collections",
        "Royal Botanic Gardens, Kew",
        "https://brahmsonline.kew.org/Content/Projects/msbp/resources/Training/MSBP-Seed-Conservation-Standards.pdf",
        "stable",
        "collection, drying, cleaning, storage, germination testing, and documentation vocabulary only",
    ),
    source(
        "TDWG-DARWIN-CORE",
        "Darwin Core",
        "Biodiversity Information Standards (TDWG)",
        "https://www.tdwg.org/standards/dwc/",
        "current",
        "occurrence, event, taxon, identification, location, material entity, and record-level vocabulary only",
    ),
    source(
        "CBD-NAGOYA",
        "Nagoya Protocol on Access and Benefit-sharing",
        "Convention on Biological Diversity",
        "https://www.cbd.int/abs/text",
        "current",
        "access, prior informed consent, mutually agreed terms, compliance, and benefit-sharing context with all authority reserved",
    ),
    source(
        "MPI-SEEDS-SOWING",
        "Seeds for Sowing Import Health Standard",
        "New Zealand Ministry for Primary Industries",
        "https://www.mpi.govt.nz/dmsdocument/1151/direct",
        "current",
        "import-health, treatment, testing, certification, quarantine, and clearance vocabulary with every real decision reserved",
    ),
    source(
        "MPI-SEED-IMPORT-STEPS",
        "Steps to importing seeds for sowing",
        "New Zealand Ministry for Primary Industries",
        "https://www.mpi.govt.nz/import/plants-flowers-seeds-plant-growing-products/seeds-for-sowing/steps-to-importing-seeds-for-sowing",
        "current",
        "official import process vocabulary only; no permit, biosecurity, quarantine, or clearance claim",
    ),
    source(
        "W3C-PROV-O",
        "PROV-O: The PROV Ontology",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/prov-o/",
        "stable",
        "entity, activity, agent, derivation, generation, invalidation, revision, and attribution lineage",
    ),
    source(
        "RFC-3339",
        "RFC 3339: Date and Time on the Internet",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc3339.html",
        "stable",
        "synthetic UTC timestamps, intervals, observations, corrections, tests, and handovers",
    ),
    source(
        "RFC-8785",
        "RFC 8785: JSON Canonicalization Scheme",
        "RFC Editor",
        "https://www.rfc-editor.org/rfc/rfc8785.html",
        "stable",
        "deterministic synthetic contract, receipt, and manifest serialization",
    ),
    source(
        "NIST-SP811",
        "NIST SP 811: Guide for the Use of the International System of Units",
        "National Institute of Standards and Technology",
        "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "stable",
        "quantity, unit, symbol, conversion, and uncertainty discipline without real metrology",
    ),
    source(
        "W3C-WCAG-22",
        "Web Content Accessibility Guidelines 2.2",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/WCAG22/",
        "current",
        "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    ),
    source(
        "NZ-PRIVACY-PRINCIPLES",
        "Privacy Act 2020 information privacy principles",
        "Office of the Privacy Commissioner New Zealand",
        "https://www.privacy.org.nz/privacy-principles/",
        "current",
        "purpose, collection, fairness, security, access, correction, retention, use, disclosure, and identifier reservations",
    ),
    source(
        "TMR-PRINCIPLES",
        "Principles of Māori Data Sovereignty",
        "Te Mana Raraunga",
        "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "current",
        "authority-reservation context only; Māori data governance remains with Māori authorities",
    ),
    source(
        "LOCAL-CONTEXTS-LABELS",
        "Traditional Knowledge and Biocultural Labels",
        "Local Contexts",
        "https://localcontexts.org/labels/about-the-labels/",
        "current",
        "community-defined provenance, protocol, and permission vocabulary with community authority reserved",
    ),
    source(
        "W3C-VC-DM-20",
        "Verifiable Credentials Data Model v2.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/vc-data-model/",
        "current",
        "synthetic credential vocabulary only; no real issuer, holder, verifier, proof, status, or trust decision",
    ),
    source(
        "W3C-DID-10",
        "Decentralized Identifiers v1.0",
        "World Wide Web Consortium",
        "https://www.w3.org/TR/did-1.0/",
        "stable",
        "synthetic identifier-document vocabulary only; no live method, resolution, key, controller, or trust claim",
    ),
    source(
        "C2PA-24",
        "C2PA Content Credentials Technical Specification 2.4",
        "Coalition for Content Provenance and Authenticity",
        "https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html",
        "current",
        "manifest, assertion, ingredient, action, binding, validation, and trust-model vocabulary without signing",
    ),
]


PROTECTED_GATES = [
    "real_people_collectors_curators_researchers_growers_communities_and_affected_parties",
    "real_seeds_plants_taxa_populations_accessions_specimens_locations_images_and_genetic_resources",
    "real_collection_processing_storage_viability_regeneration_distribution_import_quarantine_and_destruction_decisions",
    "real_measurements_calibration_statistics_genetics_likelihoods_predictions_and_empirical_confirmation",
    "professional_botany_taxonomy_seed_science_conservation_genetics_biosecurity_laboratory_and_health_and_safety_authority",
    "sensitive_locality_traditional_knowledge_genetic_resource_and_culturally_restricted_information",
    "production_identity_live_keys_proofs_resolution_status_revocation_interoperability_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority",
    "affected_party_prior_informed_consent_access_benefit_sharing_remedy_and_collective_governance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
    expected_disposition: str,
) -> dict:
    approval = "safe_now_bounded_structural_formal_or_synthetic_software"
    execution_lane = "x2_owner_local_bounded_synthetic"
    if expected_disposition == "open_gap":
        approval = "candidate_external_readiness_without_network_call"
        execution_lane = "x2_owner_local_zero_row_readiness"
    elif expected_disposition == "exact_gate":
        approval = "exact_approval_authorized_affected_party_required"
        execution_lane = "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6568-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable software obligations while "
            "refusing unsupported conservation, biosecurity, empirical, professional, identity, "
            "legal, cultural, Māori-authority, production, deployment, or Stage 20 promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or crosses a protected empirical, participant, professional, "
            "production, legal, cultural, Māori-authority, identity, or Stage 20 gate."
        ),
        "approval_class": approval,
        "execution_lane": execution_lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": (
            "The valid synthetic fixture passes, five preregistered mutations are rejected, "
            "and the receipt grants no real-material, participant, conservation, biosecurity, "
            "professional, production, legal, cultural, Māori-authority, identity, "
            "accessibility-complete, security-complete, independent-reproduction, "
            "Theory-of-Everything, or Stage 20 credit."
        ),
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave real "
            "people, plants, seeds, accessions, locations, permits, accounts, external services, "
            "sibling lanes, conservation decisions, biosecurity decisions, release decisions, "
            "professional decisions, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected_disposition,
    }


PROPOSAL_SPECS = [
    ("Seed-bank accession identity ledger with synthetic lot token, material-entity class, institution hold, acquisition event, correction lineage, and no-ownership claim", "seed-accession-ledger", "Freed ID and CBR Heart", "seed-bank accession identity, synthetic lot token, material-entity class, institution hold, acquisition event, correction lineage, and ownership-claim refusal", ["TDWG-DARWIN-CORE", "W3C-PROV-O", "KEW-MSB"]),
    ("Seed collection-event docket with source-population token, sampling-plan placeholder, collection interval, collector-role hold, permit reservation, and no-representativeness claim", "seed-collection-event-docket", "THOS Body and CBR Heart", "seed collection-event docket, source-population token, sampling-plan placeholder, collection interval, collector-role hold, permit reservation, and representativeness-claim refusal", ["TDWG-DARWIN-CORE", "KEW-SEED-CONSERVATION-STANDARDS", "CBD-NAGOYA"]),
    ("Seed-lot quantity and mass envelope with count method, subsample lineage, SI unit, uncertainty placeholder, destructive-test hold, and no-inventory-fitness claim", "seed-lot-quantity-envelope", "GMUT Mind and THOS Body", "seed-lot quantity and mass envelope, count method, subsample lineage, SI unit, uncertainty placeholder, destructive-test hold, and inventory-fitness refusal", ["NIST-SP811", "FAO-GENEBANK-STANDARDS", "W3C-PROV-O"]),
    ("Taxonomic determination revision register with name usage, determiner-role hold, confidence class, synonym cue, supersession, and no-taxon-authority claim", "seed-taxonomy-revision", "Freed ID and CBR Heart", "taxonomic determination revision, name usage, determiner-role hold, confidence class, synonym cue, supersession, and taxon-authority refusal", ["TDWG-DARWIN-CORE", "W3C-PROV-O"]),
    ("Seed cleaning and processing lineage with batch token, operation order, separation method placeholder, contamination cue, operator hold, and no-purity claim", "seed-processing-lineage", "THOS Body and Freed ID", "seed cleaning and processing lineage, batch token, operation order, separation method placeholder, contamination cue, operator hold, and purity-claim refusal", ["KEW-SEED-CONSERVATION-STANDARDS", "FAO-GENEBANK-STANDARDS", "W3C-PROV-O"]),
    ("Seed moisture-measurement docket with method placeholder, sample fraction, wet and dry mass units, uncertainty, calibration hold, and no-storage-readiness claim", "seed-moisture-docket", "GMUT Mind and THOS Body", "seed moisture-measurement docket, method placeholder, sample fraction, wet and dry mass units, uncertainty, calibration hold, and storage-readiness refusal", ["KEW-SEED-CONSERVATION-STANDARDS", "NIST-SP811", "RFC-3339"]),
    ("Drying-room batch map with tray token, loading interval, temperature and humidity placeholders, gap state, exception hold, and no-process-validation claim", "seed-drying-batch-map", "THOS Body", "seed drying-room batch map, tray token, loading interval, temperature and humidity placeholders, gap state, exception hold, and process-validation refusal", ["KEW-SEED-CONSERVATION-STANDARDS", "RFC-3339", "NIST-SP811"]),
    ("Equilibrium-relative-humidity observation series with logger token, interval, missingness, calibration hold, correction path, and no-equilibrium conclusion", "seed-erh-series", "GMUT Mind and THOS Body", "equilibrium-relative-humidity observation series, logger token, interval, missingness, calibration hold, correction path, and equilibrium-conclusion refusal", ["KEW-SEED-CONSERVATION-STANDARDS", "RFC-3339", "NIST-SP811"]),
    ("Seed packaging and seal docket with container class, barrier-property placeholder, label digest, seal state, replacement lineage, and no-longevity claim", "seed-packaging-seal-docket", "THOS Body and Freed ID", "seed packaging and seal docket, container class, barrier-property placeholder, label digest, seal state, replacement lineage, and longevity-claim refusal", ["FAO-GENEBANK-STANDARDS", "KEW-SEED-CONSERVATION-STANDARDS", "RFC-8785"]),
    ("Cold-store location and excursion ledger with vault-zone token, setpoint placeholder, observation window, excursion state, access hold, and no-storage-safety claim", "seed-cold-store-ledger", "THOS Body and Freed ID", "cold-store location and excursion ledger, vault-zone token, setpoint placeholder, observation window, excursion state, access hold, and storage-safety refusal", ["FAO-GENEBANK-STANDARDS", "KEW-SEED-CONSERVATION-STANDARDS", "RFC-3339"]),
    ("Cryopreservation reservation card with material token, protocol placeholder, rate and temperature units, operator hold, recovery-test reservation, and no-survival claim", "seed-cryopreservation-reserve", "THOS Body and CBR Heart", "cryopreservation reservation card, material token, protocol placeholder, rate and temperature units, operator hold, recovery-test reservation, and survival-claim refusal", ["FAO-GENEBANK-STANDARDS", "NIST-SP811", "W3C-PROV-O"]),
    ("Seed viability-test design envelope with method class, sample-size placeholder, replicate tokens, controls, scoring authority hold, and no-result claim", "seed-viability-design", "GMUT Mind and THOS Body", "seed viability-test design envelope, method class, sample-size placeholder, replicate tokens, controls, scoring authority hold, and result-claim refusal", ["FAO-GENEBANK-STANDARDS", "KEW-SEED-CONSERVATION-STANDARDS", "NIST-SP811"]),
    ("Germination observation series with replicate token, elapsed day, seedling-state vocabulary, censoring, correction, and no-viability estimate", "seed-germination-series", "GMUT Mind and THOS Body", "germination observation series, replicate token, elapsed day, seedling-state vocabulary, censoring, correction, and viability-estimate refusal", ["FAO-GENEBANK-STANDARDS", "RFC-3339", "W3C-PROV-O"]),
    ("Seed diagnostic-image custody board with synthetic asset token, capture method hold, transformation chain, scorer reservation, redaction, and no-diagnosis claim", "seed-diagnostic-image-custody", "Freed ID and THOS Body", "seed diagnostic-image custody, synthetic asset token, capture method hold, transformation chain, scorer reservation, redaction, and diagnosis-claim refusal", ["C2PA-24", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Dormancy and pretreatment plan with treatment class, duration and temperature placeholders, rationale hold, competing-plan cue, and no-germination recommendation", "seed-dormancy-plan", "GMUT Mind and CBR Heart", "seed dormancy and pretreatment plan, treatment class, duration and temperature placeholders, rationale hold, competing-plan cue, and germination-recommendation refusal", ["FAO-GENEBANK-STANDARDS", "KEW-SEED-CONSERVATION-STANDARDS", "NIST-SP811"]),
    ("Regeneration-decision reservation board with threshold placeholder, generation history, genetic-drift cue, isolation hold, competent review, and no-regeneration order", "seed-regeneration-reserve", "CBR Heart and THOS Body", "seed regeneration-decision reservation, threshold placeholder, generation history, genetic-drift cue, isolation hold, competent review, and regeneration-order refusal", ["FAO-GENEBANK-STANDARDS", "FAO-PLANT-TREATY", "W3C-PROV-O"]),
    ("Safety-duplicate lineage with source and duplicate tokens, shipment hold, quantity parity, receipt digest, discrepancy state, and no-resilience claim", "seed-safety-duplicate-lineage", "Freed ID and THOS Body", "seed safety-duplicate lineage, source and duplicate tokens, shipment hold, quantity parity, receipt digest, discrepancy state, and resilience-claim refusal", ["FAO-GENEBANK-STANDARDS", "W3C-PROV-O", "RFC-8785"]),
    ("Seed distribution-request docket with requester class, purpose placeholder, quantity, terms hold, availability state, and no-release authorization", "seed-distribution-request", "CBR Heart and THOS Body", "seed distribution-request docket, requester class, purpose placeholder, quantity, terms hold, availability state, and release-authorization refusal", ["KEW-SEED-ACCESS", "FAO-PLANT-TREATY", "NZ-PRIVACY-PRINCIPLES"]),
    ("Material-transfer and benefit-sharing lineage with agreement-reference placeholder, provider and recipient roles, benefit hold, expiry, and no-legal-status claim", "seed-transfer-benefit-lineage", "CBR Heart and Freed ID", "material-transfer and benefit-sharing lineage, agreement-reference placeholder, provider and recipient roles, benefit hold, expiry, and legal-status refusal", ["CBD-NAGOYA", "FAO-PLANT-TREATY", "W3C-PROV-O"]),
    ("Seed import and quarantine reservation docket with commodity token, certificate and permit placeholders, treatment hold, isolation state, and no-clearance claim", "seed-import-quarantine-reserve", "CBR Heart and THOS Body", "seed import and quarantine reservation, commodity token, certificate and permit placeholders, treatment hold, isolation state, and clearance-claim refusal", ["MPI-SEEDS-SOWING", "MPI-SEED-IMPORT-STEPS", "W3C-PROV-O"]),
    ("Accessible public accession summary with heading structure, field definitions, provenance link, status text, table associations, correction path, and manual review reserved", "seed-accessible-summary", "THOS Body and CBR Heart", "accessible public accession summary, heading structure, field definitions, provenance link, status text, table associations, correction path, and manual-review reservation", ["W3C-WCAG-22", "TDWG-DARWIN-CORE", "W3C-PROV-O"]),
    ("Seed-record contestation and correction docket with pseudonymous token, minimised context, conflicting account, uncertainty, response hold, and consensus refusal", "seed-record-contestation", "CBR Heart and Freed ID", "seed-record contestation and correction docket, pseudonymous token, minimised context, conflicting account, uncertainty, response hold, and consensus-promotion refusal", ["W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES", "TDWG-DARWIN-CORE"]),
    ("Sensitive locality and traditional-knowledge publication firewall with spatial coarsening, audience grant, authority checkpoint, expiry, audit, and fail-closed disclosure", "seed-sensitive-publication", "CBR Heart and Freed ID", "sensitive locality and traditional-knowledge publication firewall, spatial coarsening, audience grant, authority checkpoint, expiry, audit, and fail-closed disclosure", ["TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS", "NZ-PRIVACY-PRINCIPLES"]),
    ("GMUT seed-longevity Arrhenius-type dimensional proxy with temperature and moisture domains, coefficient units, sign conventions, calibration quarantine, and prediction refusal", "gmut-seed-longevity-proxy", "GMUT Mind", "GMUT seed-longevity Arrhenius-type dimensional proxy, temperature and moisture domains, coefficient units, sign conventions, calibration quarantine, and prediction refusal", ["NIST-SP811", "FAO-GENEBANK-STANDARDS", "RFC-8785"]),
    ("GMUT population-sampling covariance proxy with finite-lot domain, allele-count placeholders, covariance units, drift quarantine, and no-genetic inference", "gmut-seed-sampling-proxy", "GMUT Mind", "GMUT population-sampling covariance proxy, finite-lot domain, allele-count placeholders, covariance units, drift quarantine, and genetic-inference refusal", ["FAO-GENEBANK-STANDARDS", "NIST-SP811", "RFC-8785"]),
    ("THOS seed-bank incident and handover choreography with stale logger input, seal discrepancy, quarantine, workload cue, escalation, rollback, and no-operational decision", "thos-seed-bank-handover", "THOS Body", "THOS seed-bank incident and handover choreography, stale logger input, seal discrepancy, quarantine, workload cue, escalation, rollback, and operational-decision refusal", ["FAO-GENEBANK-STANDARDS", "KEW-MSB", "W3C-PROV-O"]),
    ("Freed ID synthetic accession disclosure-and-status capsule with purpose, audience, minimised fields, retention clock, correction, and live proof disabled", "freed-id-seed-accession-capsule", "Freed ID and CBR Heart", "Freed ID seed accession disclosure-and-status capsule, purpose, audience, minimised fields, retention clock, correction, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DID-10", "NZ-PRIVACY-PRINCIPLES"]),
    ("Freed ID orthographic seed-image custody card with ingredient digest, crop and annotation lineage, disclosure shield, unsigned state, and origin nonclaim", "freed-id-seed-image-plan", "Freed ID", "Freed ID orthographic seed-image custody, ingredient digest, crop and annotation lineage, disclosure shield, unsigned state, and origin-claim refusal", ["C2PA-24", "W3C-PROV-O", "NZ-PRIVACY-PRINCIPLES"]),
    ("Kew seed-collection no-network query tribunal with accession and taxon placeholders, page-stop invariant, no-data response, citation capture, and zero-row witness", "seed-zero-row-adapter", "Freed ID and GMUT Mind", "Kew seed-collection no-network query tribunal, accession and taxon placeholders, page-stop invariant, no-data response, citation capture, and zero-row witness", ["KEW-SEED-ACCESS", "TDWG-DARWIN-CORE", "NZ-PRIVACY-PRINCIPLES"]),
    ("CBR genetic-resource non-automation covenant for access, prior informed consent, benefit sharing, Farmers' Rights, restricted knowledge, remedy, law, culture, and Māori decision authority", "cbr-seed-authority-matrix", "CBR Heart", "genetic-resource access, prior informed consent, benefit sharing, Farmers' Rights, traditional knowledge, privacy, remedy, legal, cultural, data-governance, and Māori-authority reservation", ["CBD-NAGOYA", "FAO-PLANT-TREATY", "TMR-PRINCIPLES", "LOCAL-CONTEXTS-LABELS"]),
]


PROPOSALS = [
    proposal(
        number,
        title,
        slug,
        pillar,
        mechanism,
        sources,
        "completed" if number <= 23 else "represented" if number <= 28 else "open_gap" if number == 29 else "exact_gate",
    )
    for number, (title, slug, pillar, mechanism, sources) in enumerate(PROPOSAL_SPECS, 1)
]


SKILL_SPECS = [
    ("ghc-family-seed-accession-provenance", "Freeze synthetic accession identity, acquisition, institution, correction, and ownership boundaries."),
    ("ghc-family-seed-collection-event-boundary", "Separate collection-event structure, source-population claims, permits, and representativeness."),
    ("ghc-family-seed-processing-custody", "Preserve drying, cleaning, packaging, seal, sample, and transformation lineage."),
    ("ghc-family-seed-moisture-storage-boundary", "Track units, calibration holds, drying, humidity, cold-store location, and excursion state."),
    ("ghc-family-seed-viability-test-reserve", "Structure test design and observations while reserving scoring, inference, and laboratory authority."),
    ("ghc-family-seed-regeneration-nonpromotion", "Expose regeneration cues without issuing conservation, genetic, or operational decisions."),
    ("ghc-family-seed-distribution-benefit-reserve", "Constrain requests, transfers, access, benefit sharing, import, quarantine, and release."),
    ("ghc-family-seed-accessibility-report", "Generate accessible structural summaries while reserving manual and affected-user evaluation."),
    ("ghc-family-seed-freed-id-disclosure", "Constrain synthetic accession identity, disclosure, status, proof, and image-lineage claims."),
    ("ghc-family-seed-cultural-authority-reserve", "Fail closed around genetic resources, traditional knowledge, benefit, remedy, governance, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_seed_accession_provenance.py", "seed-accession-ledger"),
    ("ghc_family_seed_collection_event.py", "seed-collection-event-docket"),
    ("ghc_family_seed_processing_custody.py", "seed-processing-lineage"),
    ("ghc_family_seed_storage_boundary.py", "seed-cold-store-ledger"),
    ("ghc_family_seed_viability_reserve.py", "seed-viability-design"),
    ("ghc_family_seed_regeneration_nonpromotion.py", "seed-regeneration-reserve"),
    ("ghc_family_seed_distribution_benefit.py", "seed-distribution-request"),
    ("ghc_family_seed_accessibility_report.py", "seed-accessible-summary"),
    ("ghc_family_seed_freed_id_disclosure.py", "freed-id-seed-accession-capsule"),
    ("ghc_family_seed_cultural_authority_reserve.py", "cbr-seed-authority-matrix"),
]


def negative(number: int, signature: str, observed: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6568-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": signature,
        "observed": observed,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "memory-registry-broad-search-timeout", "The first broad registry search exceeded its ten-second bound and returned no usable result.", "Use exact GHC, Vesper, Neris, closeout, and routing terms against the memory registry, then open only the one directly referenced rollout.", "Begin memory retrieval with bounded exact terms and never scan all rollout content before the registry identifies a target."),
    negative(2, "powershell-skill-inventory-empty-pipe-element", "The first skill inventory pipeline contained an empty pipeline element and failed before reading a skill.", "Use a materialized file array and one scalar literal-path read per required skill and reference.", "Materialize foreach output before piping and validate the PowerShell expression before combining reads."),
    negative(3, "powershell-manifest-summary-empty-pipe-element", "The first manifest-summary pipeline contained an empty pipeline element and produced no manifest evidence.", "Read the exact manifest path, parse one JSON object, and emit scalar counts separately.", "Keep manifest parsing and display as separate bounded operations."),
    negative(4, "git-probe-from-nonrepository-cwd", "An initial Git revision probe ran from the Codex configuration directory and failed because it was not a repository.", "Anchor every Git probe with git -C or an explicit repository workdir.", "Resolve and display the intended repository root before the first Git command."),
    negative(5, "worktree-add-outer-timeout-after-registration", "The additive D-first worktree command exceeded its outer bound after Git had already registered and populated the lane.", "Audit the exact path, .git indirection, registered branch, HEAD, process state, and cleanliness; continue in place only after all pass.", "After a mutating command timeout, inspect durable state before any retry and never create a duplicate worktree blindly."),
    negative(6, "post-worktree-compound-audit-timeout", "A broad post-timeout audit combined Git state with recursive lock discovery and exceeded its bound.", "Split path, .git, HEAD, branch, process, lock, and status checks into bounded scalar probes.", "Never combine recursive filesystem inspection with Git worktree recovery under one timeout."),
    negative(7, "gitfile-read-short-timeout", "The first very short bounded read of the worktree .git indirection timed out without evidence.", "Repeat only the exact literal-path read with a longer bounded timeout and no unrelated operations.", "Treat startup latency separately from command failure and keep recovery probes scalar."),
    negative(8, "phase-root-only-manifest-map-false-mismatch", "The first manifest comparison mapped only phase documents and falsely reported thirty-two missing script and test blobs.", "Build the Git tree map from the complete commit and compare only the paths declared by the manifest.", "Scope manifest comparison by declared entries, not by an assumed phase-directory prefix."),
    negative(9, "compound-source-truth-inspection-timeout", "A combined status, head, directory listing, and multi-JSON parse exceeded its bound without useful output.", "Run clean-state, revision, listing, and JSON reads as separate scalar probes.", "Keep large-worktree Git traversal independent from JSON parsing and filesystem enumeration."),
    negative(10, "windows-rg-wildcard-path-rejection", "A recursive-grep command passed Windows wildcard paths directly and failed with an invalid filename error.", "Pass directories as roots and use rg -g include patterns for filenames.", "Use ripgrep glob filters rather than shell-style wildcard path operands on Windows."),
    negative(11, "candidate-domain-semantic-novelty-collision", "The first radio-observatory concept overlapped inherited astronomy, LOFAR, HERA, EHT, MeerKAT, and planetarium proposal families and was abandoned before freeze.", "Select the seed-bank accession, storage, viability, distribution, and authority-boundary lens after whole-chain title screening showed no seed-bank or herbarium title collision.", "Screen candidate domains against the complete frozen title chain before drafting the phase catalogue."),
    negative(12, "activation-baton-working-tree-vs-git-blob-hash-domain", "The first x1 build compared the committed activation baton against a working-tree byte digest and stopped because Windows checkout line endings differed from the exact Git blob.", "Retain the failed build, compute the SHA-256 over git show binary output at the exact source commit, and use that immutable Git-blob digest.", "Declare the hash domain explicitly and use Git object bytes for committed-baton verification across Windows worktrees."),
    negative(13, "seed-image-title-inherited-transformation-collision", "The first seed-image proposal title reached 0.6818 Jaccard similarity with the inherited remote-sensing transformation docket and the x1 build stopped before writing the packet.", "Retain the failed build and reframe the title around orthographic custody, ingredient digest, crop and annotation lineage, disclosure shielding, unsigned state, and origin nonclaim.", "Run the exact whole-chain novelty audit before any x1 artifact write and revise only colliding titles without weakening their falsifier or authority boundaries."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6568-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Build and validate the bounded synthetic contract for {item['slug']}.",
        "approval_class": "safe_now_owner_local_additive",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6568-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6568-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, and stale-label cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
