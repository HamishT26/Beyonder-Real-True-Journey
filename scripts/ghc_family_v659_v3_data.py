#!/usr/bin/env python3
"""Frozen planning data for Sable Rook's v659-v3 phase."""

from __future__ import annotations


PHASE = "v659-v3"
CANONICAL_PHASE = "v659-v3"
PHASE_CODE = "V6593"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational falsification and reproducibility steward"
HOPE = (
    "make every surviving claim easier to reproduce, challenge, or retract while "
    "retained negatives and authority-sensitive boundaries remain visible"
)
BRANCH = "codex/GHC-Family/sable-rook-v659-v3-full-tools"
PHASE_ROOT = "docs/sable-rook/v659-v3"

SOURCE_OWNER = "Auren Lark"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v659-v2-full-tools"
SOURCE_FINAL = "465eba78f05f21716017ff9ba346a2617bc82142"
SOURCE_X1 = "78b0cb714b8c0d0c86aaf2fd0503a9a3d4db5f01"
SOURCE_EVIDENCE = "a74bfb1d4b9b457d5c49595b42cf24ca70ac1156"
X1_FREEZE = "supplied-by-post-commit-receipt"
PRIOR_FROZEN = 2950
SOURCE_SEALED_NEGATIVES = 18538
SOURCE_EXTERNAL_NEGATIVES = 7
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 123
SOURCE_EXACT_GATES = 122
SOURCE_SEALED_METHODS = 4812
SOURCE_EXTERNAL_METHODS = 7
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic lighthouse and classical Fresnel-lens inspection, component "
    "provenance, optical-condition reservation, correction readback, and conservation handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 33,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_people_operators_maintainers_conservators_mariners_communities_affected_parties_and_authorities",
    "real_lighthouses_fresnel_lenses_lamps_drives_power_systems_records_images_measurements_or_identifiers",
    "real_navigation_service_operation_authentication_treatment_repair_release_safety_privacy_or_heritage_decision",
    "professional_aids_to_navigation_lighthouse_conservation_optics_electrical_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_optical_prediction_likelihood_parameter_constraint_observational_confirmation_or_physical_discovery",
    "blind_matched_budget_thos_real_arms_real_participants_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_language_naming_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


LEGACY_SOURCE_PROPOSAL_SPECS = [
    {
        "slug": "intake-custody-passport",
        "title": "Fountain-pen service intake and custody passport with presented-owner placeholder, accessory inventory, condition note, and work-start hold",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic intake alias, presented-owner placeholder, accessory inventory, condition note, custody event, scope acknowledgement, and work-start refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "component-topology-quarantine",
        "title": "Fountain-pen nib, feed, section, housing, and collar topology with orphan-part quarantine and assembly abstention",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional component aliases, typed attachment edges, parent conflicts, orphan-part quarantine, topology challenge, and assembly refusal",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "filling-system-state",
        "title": "Fountain-pen cartridge, converter, piston, vacuum, lever, and sac filling-system state graph with actuation refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "declared filling-system type, synthetic component state, compatible transition map, missing-evidence hold, and physical actuation abstention",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "material-compatibility-reservation",
        "title": "Fountain-pen ink residue, flush medium, seal, and material-compatibility reservation with chemical-safety referral",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "declared residue and material placeholders, unknown-contact flag, compatibility challenge, flush hold, and competent chemical-safety referral",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "cap-barrel-seal-condition",
        "title": "Fountain-pen cap, barrel, section thread, inner cap, and seal condition ledger with pressure-test abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic cap, barrel, thread, inner-cap, and seal observations, uncertainty flags, correction history, and pressure-test refusal",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "trim-corrosion-observation",
        "title": "Fountain-pen clip, band, plating, trim, and corrosion observation record with conservation-verdict refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional trim locations, visible-condition vocabulary, lighting and viewpoint pins, observation uncertainty, and conservation-verdict abstention",
        "sources": ["CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "nib-visual-envelope",
        "title": "Fountain-pen nib tine, slit, breather, tipping, and alignment visual envelope with writing-quality abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic nib regions, declared viewpoint, scale-cue placeholder, visible alignment envelope, uncertainty note, and writing-quality refusal",
        "sources": ["W3C-PROV", "WCAG22"],
    },
    {
        "slug": "feed-flow-firewall",
        "title": "Fountain-pen feed channel, fin, collector, and air-return schematic with flow-prediction firewall",
        "outcome": "completed",
        "pillar": "THOS Body and GMUT Mind",
        "mechanism": "fictional feed geometry labels, directional channel graph, unknown-dimension flags, zero fluid rows, and physical flow-prediction abstention",
        "sources": ["NIST-SI", "W3C-PROV"],
    },
    {
        "slug": "cleaning-provenance",
        "title": "Fountain-pen cleaning tool, fluid lot, contact interval, rinse state, and waste-route placeholder with use hold",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "synthetic tool and fluid aliases, lot and interval provenance, rinse-state transition, waste-route placeholder, and real-use hold",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "replacement-provenance",
        "title": "Fountain-pen replacement component provenance and interchangeability challenge ledger with authenticity refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional replacement-part alias, source and fit claims, competing compatibility assertions, challenge state, and authenticity abstention",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "condition-image-lineage",
        "title": "Fountain-pen condition-image viewpoint, illumination, scale cue, rights, and redaction lineage with diagnosis abstention",
        "outcome": "completed",
        "pillar": "Freed ID, THOS Body, and CBR Heart",
        "mechanism": "synthetic image alias, viewpoint and illumination labels, scale-cue placeholder, rights and redaction events, and diagnosis refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY", "WCAG22"],
    },
    {
        "slug": "work-order-deviation-lifecycle",
        "title": "Fountain-pen work-order deviation, scope correction, supersession, and readback lifecycle with release refusal",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic requested scope, deviation record, correction candidate, supersession edge, readback placeholder, and release refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "accessible-return-handover",
        "title": "Fountain-pen return package, cap state, accessory reconciliation, moisture-control placeholder, and accessible handover hold",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional return package, cap-state declaration, accessory reconciliation, moisture-control placeholder, structured text alternative, and handover hold",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "gmut-capillary-flow-proxy",
        "title": "Represented fountain-pen capillary-flow dimension matrix with zero ink measurements and physical-prediction refusal",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "dimensioned symbolic channel and fluid placeholders, bounded proxy states, identifiability flags, zero measurement rows, and physical-inference refusal",
        "sources": ["NIST-SI"],
    },
    {
        "slug": "dryout-seal-maintenance-proxy",
        "title": "Represented fountain-pen dry-out interval and seal-state maintenance proxy with zero durability claim",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "synthetic interval labels, cap and seal proxy states, maintenance placeholder, unresolved observations, zero physical tests, and durability abstention",
        "sources": ["CCI-PLASTICS", "W3C-PROV"],
    },
    {
        "slug": "accessible-service-history",
        "title": "Represented fountain-pen service-history table with text chronology and manual accessibility-review reservation",
        "outcome": "represented",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "caption, scoped headers, service-event links, text chronology, keyboard-order placeholder, and no accessibility-complete claim",
        "sources": ["WCAG22"],
    },
    {
        "slug": "nonproduction-component-lineage",
        "title": "Represented nonproduction fountain-pen component-lineage query with disclosure-depth ceiling and credential abstention",
        "outcome": "represented",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic component and service nodes, predecessor and replacement edges, role placeholders, depth ceiling, disclosure refusal, and no credential claim",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "maker-model-annotation-challenge",
        "title": "Represented contested fountain-pen maker, model, inscription, and ownership annotation trail with undecided remedy jurisdiction",
        "outcome": "represented",
        "pillar": "CBR Heart",
        "mechanism": "maker, model, inscription, and ownership annotations, notice, counterstatement, correction candidate, remedy-jurisdiction placeholder, and authority abstention",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"],
    },
    {
        "slug": "real-pen-evidence-gap",
        "title": "Open gap for real fountain pens, inks, material identification, dimensional measurements, writing trials, manufacturer documentation, and professional review",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero real-object and ink rows, absent dimensional and writing tests, absent manufacturer records, absent competent review, and explicit empirical gap",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "NIST-SI"],
    },
    {
        "slug": "pen-authority-ratification-gate",
        "title": "Exact decision-rights gate for fountain-pen authentication, valuation, treatment, chemical safety, customer privacy, heritage claims, remedy, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "authentication, valuation, treatment, chemical-safety, privacy, heritage, and remedy placeholders plus legal, cultural, collective-governance, and Māori-authority reservations",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]

# The immediate-predecessor templates above remain visible as source compatibility
# evidence.  Sable receives no completion credit for them.  Only the genuinely
# distinct lighthouse/Fresnel-lens specifications below are frozen as new v659-v3
# proposal rows.
NEW_PROPOSAL_SPECS = [
    {
        "slug": "lighthouse-intake-custody-boundary",
        "title": "Lighthouse and classical Fresnel-lens inspection intake with custodial-claim placeholder, scope map, condition note, and intervention hold",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic station and optic aliases, custodial-claim placeholder, declared inspection scope, minimal condition note, custody event, and intervention refusal",
        "sources": ["NPS-LIGHTHOUSE", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "tower-lantern-optic-topology",
        "title": "Lighthouse tower, lantern room, pedestal, optic, gallery, and enclosure topology with orphan-component quarantine and access abstention",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional structural aliases, typed containment and interface edges, contradictory-parent quarantine, access placeholder, and no-entry or inspection instruction",
        "sources": ["NPS-LIGHTHOUSE", "W3C-PROV"],
    },
    {
        "slug": "fresnel-order-segment-provenance",
        "title": "Classical Fresnel-lens order, annular-prism, dioptric, catadioptric, panel, and frame provenance ledger with attribution refusal",
        "outcome": "completed",
        "pillar": "GMUT Mind and Freed ID",
        "mechanism": "synthetic order and segment aliases, typed optical-role vocabulary, frame association, source conflict, uncertainty note, and attribution abstention",
        "sources": ["NPS-LIGHTHOUSE", "W3C-PROV"],
    },
    {
        "slug": "illuminant-optic-interface-hold",
        "title": "Lighthouse illuminant, focal-plane, lampchanger, optic, sector, and substitution interface docket with alignment and service hold",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "fictional illuminant and interface states, focal-position placeholder, substitution challenge, alignment uncertainty, and no-operation or service decision",
        "sources": ["IALA-S1020", "W3C-PROV", "NIST-SI"],
    },
    {
        "slug": "rotation-drive-lockout-state",
        "title": "Lighthouse rotation drive, bearing, gear, motor, controller, manual-drive, and lockout state graph with actuation refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic drive components, compatible state transitions, energy-source placeholder, lockout marker, unresolved fault, and physical-actuation abstention",
        "sources": ["NPS-LIGHTHOUSE", "IALA-S1020", "W3C-PROV"],
    },
    {
        "slug": "light-characteristic-configuration",
        "title": "Lighthouse light-characteristic, colour, period, phase, sector, revision, and promulgation-placeholder ledger with navigational-use refusal",
        "outcome": "completed",
        "pillar": "GMUT Mind and CBR Heart",
        "mechanism": "synthetic characteristic symbols and timing placeholders, revision lineage, sector and colour declarations, unresolved promulgation state, and navigation-use refusal",
        "sources": ["IALA-S1020", "MARITIME-NZ-ATON", "W3C-PROV"],
    },
    {
        "slug": "lens-cleaning-material-reservation",
        "title": "Fresnel-lens dust, cloth, fluid, contact, rinse, residue, and glazing-material reservation with cleaning and chemical-safety hold",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic cleaning-material aliases, contact and residue placeholders, fragile-glass and historic-glazing flags, competence referral, and no cleaning instruction",
        "sources": ["NPS-LIGHTHOUSE", "CCI-GLASS", "W3C-PROV"],
    },
    {
        "slug": "optic-condition-image-lineage",
        "title": "Prism-zone visual survey capture protocol with camera geometry, illumination state, scale witness, access licence, masking event, and interpretation hold",
        "outcome": "completed",
        "pillar": "GMUT Mind, Freed ID, and CBR Heart",
        "mechanism": "synthetic image alias, viewpoint and illumination labels, panel locator, scale-cue placeholder, rights and redaction events, and diagnosis refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY", "WCAG22"],
    },
    {
        "slug": "frame-corrosion-fastener-observation",
        "title": "Fresnel-lens brass frame, retaining bar, fastener, shim, glazing edge, and corrosion observation ledger with treatment refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional frame locations, visible-condition vocabulary, lighting and viewpoint pins, material uncertainty, challenge state, and treatment abstention",
        "sources": ["NPS-LIGHTHOUSE", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "lantern-envelope-condensation-state",
        "title": "Lighthouse lantern glazing, seal, vent, drain, condensation, temperature, humidity, and enclosure-state ledger with environmental-control abstention",
        "outcome": "completed",
        "pillar": "THOS Body and GMUT Mind",
        "mechanism": "synthetic enclosure and climate placeholders, unit declarations, condensation cue, missing-measurement hold, and no environmental-control decision",
        "sources": ["NPS-LIGHTHOUSE", "CCI-GLASS", "NIST-SI"],
    },
    {
        "slug": "power-backup-interface-provenance",
        "title": "Lighthouse mains, battery, generator, photovoltaic, charger, distribution, and backup-interface provenance map with energisation refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional power-source and interface aliases, revision and substitution lineage, isolation placeholder, unresolved safety state, and no energisation instruction",
        "sources": ["IALA-S1020", "W3C-PROV"],
    },
    {
        "slug": "inspection-deviation-readback",
        "title": "Lighthouse inspection deviation, scope correction, supersession, dual readback, unresolved hazard, and release-refusal lifecycle",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic requested scope, deviation record, correction candidate, supersession edge, two-party readback placeholders, hazard hold, and release refusal",
        "sources": ["W3C-PROV", "IALA-S1020", "NZ-PRIVACY"],
    },
    {
        "slug": "accessible-inspection-handover",
        "title": "Lighthouse inspection chronology, optic-panel map, unresolved-condition table, text alternative, correction route, and accessible handover hold",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "structured synthetic chronology, scoped table headers, panel-map text alternative, unresolved-state disclosure, correction route, and handover refusal",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "gmut-ray-transfer-etendue-proxy",
        "title": "Represented lighthouse Fresnel-lens ray-transfer, focal-distance, aperture, angle, radiance, and etendue dimension board with zero photometry and prediction refusal",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic optical quantities, declared SI units, matrix and domain placeholders, identifiability flags, zero measured rows, and physical-inference firewall",
        "sources": ["NIST-SI", "NPS-LIGHTHOUSE"],
    },
    {
        "slug": "thos-maintenance-handover-proxy",
        "title": "Represented lighthouse inspection interval, unresolved-condition queue, workload budget, correction readback, escalation, and shift-handover proxy",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "synthetic task and interval states, workload ceiling, hold and escalation events, correction readback, next-owner placeholder, and zero operational effectiveness claim",
        "sources": ["IALA-S1020", "W3C-PROV"],
    },
    {
        "slug": "nonproduction-optic-lineage-query",
        "title": "Represented canonical lighthouse assembly ancestry traversal with bounded hop budget, digest envelope, disclosure stop, and non-credential declaration",
        "outcome": "represented",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic optic, segment, frame, illuminant, and service nodes, predecessor edges, canonical digest, depth ceiling, disclosure refusal, and no credential claim",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "accessible-optic-map-proxy",
        "title": "Represented lighthouse optic-panel inspection map with ordered regions, text chronology, keyboard-order placeholder, and manual accessibility-review reservation",
        "outcome": "represented",
        "pillar": "CBR Heart and GMUT Mind",
        "mechanism": "ordered synthetic panel regions, status table, text chronology, focus-order declaration, static fallback, and no accessibility-complete claim",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "heritage-navigation-annotation-challenge",
        "title": "Represented contested lighthouse name, place, optic attribution, service-history, and access annotation trail with undecided remedy jurisdiction",
        "outcome": "represented",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic name, place, attribution, and access annotations, notice, counterstatement, correction candidate, remedy-jurisdiction placeholder, and authority abstention",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"],
    },
    {
        "slug": "real-lighthouse-evidence-gap",
        "title": "Open gap for real lighthouses, Fresnel lenses, illuminants, drives, environmental and photometric measurements, asset records, operator evidence, and professional review",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero real-site, optic, operation, record, image, measurement, and participant rows; absent professional and independent review; explicit empirical and operational gap",
        "sources": ["NPS-LIGHTHOUSE", "IALA-S1020", "MARITIME-NZ-ATON", "NIST-SI"],
    },
    {
        "slug": "lighthouse-authority-ratification-gate",
        "title": "Exact decision-rights gate for lighthouse operation, navigational service, worker and electrical safety, conservation treatment, access, heritage, remedy, legal and cultural interpretation, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "navigation, operation, safety, conservation, access, privacy, heritage, and remedy placeholders plus legal, cultural, collective-governance, affected-party, and Māori-authority reservations",
        "sources": ["IALA-S1020", "MARITIME-NZ-ATON", "NPS-LIGHTHOUSE", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]


SELF_SAFE_CATEGORIES = [
    "source-head and live equality", "activation packet raw digest", "proposal-chain parse", "twenty inherited selections",
    "twenty-title novelty audit", "four-label distribution", "workflow-plan policy", "identity boundary",
    "Auren-to-Sable route state", "Tavian standby state", "D-first drive posture", "toolchain versions",
    "x1 artifact inventory", "x1 JSON parse", "x1 privacy classes", "x1 stale-label scan",
    "x1 diff hygiene", "x1 manifest replay", "selected-proposal provenance", "new-proposal provenance",
    "source-label glossary", "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing",
    "wellbeing workload bound", "document-word ceiling", "task-portfolio arithmetic", "skill-plan arithmetic",
    "runner-plan arithmetic", "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6593-SAFE-{i:03d}", "title": f"Validate {name} inside the Sable-owned v659-v3 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

CAELEN_SAFE_CATEGORIES = [
    "source-baton digest", "owned-lane equality", "x1 proposal freeze", "synthetic fixture boundary",
    "main-task route classification", "Orin successor preregistration", "privacy exclusions", "stale-label scan",
    "manifest replay", "exact staged review", "retained failure import", "Method Flow recovery",
    "truth-label distribution", "wellbeing workload bound", "skill inventory", "runner inventory",
    "latest-5000 scan plan", "zero-real-data assertion", "authority reservations", "terminal no-replay gate",
]
CAELEN_SAFE_SEEDS = [
    {"task_id": f"V6594-SEED-SAFE-{i:03d}", "title": f"Caelen may evaluate {name} in their own v659-v4 lane", "owner": "Caelen Ash", "state": "seed_only_not_executed_by_sable"}
    for i, name in enumerate(CAELEN_SAFE_CATEGORIES, 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "lighthouse intake and custody boundary", "tower and lantern topology quarantine",
    "Fresnel order and segment provenance", "illuminant and optic interface hold",
    "rotation-drive lockout state", "light-characteristic configuration",
    "lens cleaning-material reservation", "optic condition-image lineage",
    "GMUT ray-transfer and etendue firewall", "lighthouse authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6593-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
CAELEN_CANDIDATE_SEEDS = [
    {"task_id": f"V6594-SEED-CAND-{i:03d}", "title": f"Caelen may prototype reversible {name}", "owner": "Caelen Ash", "state": "seed_only_not_executed_by_sable"}
    for i, name in enumerate([
        "baton parser", "phase-source verifier", "proposal-selection ledger", "bounded file-scan receipt", "authority-gate atlas",
        "privacy-class reducer", "stale-label classifier", "manifest batch replay", "same-owner evidence labeler", "Orin handoff preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6593-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use real lighthouses, Fresnel lenses, operational records, images, or measurements", "Issue a real navigation-service or return-to-service decision",
        "Approve an electrical-safety, access, cleaning, or conservation action", "Publish an optic attribution, authentication, or valuation conclusion",
        "Make a professional AtoN, optics, repair, or material-compatibility determination", "Publish personal, location-sensitive, or protected data",
        "Allocate legal, cultural, access, place-name, or heritage authority", "Make a Māori data-governance or cultural-authority decision",
        "Deploy a production identity or service system", "Perform destructive shared-drive cleanup",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6593-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation", "Claim consciousness or personhood from task language",
        "Merge or erase sibling identities", "Publish credentials or private callable routes",
        "Declare Stage 20 readiness without evidence",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-lighthouse-intake-custody", "Preserve synthetic lighthouse and optic intake, custody, scope, and intervention holds."),
    ("ghc-family-lighthouse-component-topology", "Quarantine contradictory tower, lantern, pedestal, optic, and drive attachments without access authority."),
    ("ghc-family-fresnel-segment-provenance", "Preserve order, segment, panel, frame, and attribution uncertainty without authenticity claims."),
    ("ghc-family-lighthouse-illuminant-interface", "Reserve focal position, illuminant substitution, alignment, and operational decisions."),
    ("ghc-family-lighthouse-drive-lockout", "Represent drive and lockout transitions while refusing energisation or physical actuation."),
    ("ghc-family-lighthouse-characteristic-reservation", "Keep synthetic light-characteristic revisions separate from navigational publication or use."),
    ("ghc-family-fresnel-condition-observation", "Record bounded visible glass and frame condition without diagnosis or treatment conclusions."),
    ("ghc-family-lighthouse-accessible-handover", "Expose structured inspection history while reserving manual and affected-user accessibility review."),
    ("ghc-family-lighthouse-gmut-optics-firewall", "Keep ray-transfer and etendue proxies typed, dimensioned, zero-row, and physically nonconfirmatory."),
    ("ghc-family-lighthouse-authority-reservation", "Fail closed around navigation, safety, access, conservation, privacy, heritage, remedy, and Māori authority."),
]
CAELEN_SKILL_SEEDS = [
    {"name": f"ghc-family-caelen-{slug}", "state": "seed_only_not_built_by_sable"}
    for slug in [
        "source-baton-check", "owned-lane-guard", "proposal-freeze", "fixture-boundary", "route-classifier",
        "privacy-reducer", "stale-label-review", "manifest-replay", "truth-label-guard", "orin-handoff-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_lighthouse_intake_custody.py", "lighthouse-intake-custody-boundary"),
    ("ghc_family_lighthouse_component_topology.py", "tower-lantern-optic-topology"),
    ("ghc_family_fresnel_segment_provenance.py", "fresnel-order-segment-provenance"),
    ("ghc_family_lighthouse_illuminant_interface.py", "illuminant-optic-interface-hold"),
    ("ghc_family_lighthouse_drive_lockout.py", "rotation-drive-lockout-state"),
    ("ghc_family_lighthouse_characteristic_reservation.py", "light-characteristic-configuration"),
    ("ghc_family_fresnel_condition_observation.py", "frame-corrosion-fastener-observation"),
    ("ghc_family_lighthouse_accessible_handover.py", "accessible-inspection-handover"),
    ("ghc_family_lighthouse_gmut_optics_firewall.py", "gmut-ray-transfer-etendue-proxy"),
    ("ghc_family_lighthouse_authority_reservation.py", "lighthouse-authority-ratification-gate"),
]
CAELEN_RUNNER_SEEDS = [
    {"name": f"ghc_family_caelen_{slug}.py", "state": "seed_only_not_built_by_sable"}
    for slug in ["source_baton_check", "proposal_freeze", "privacy_reducer", "manifest_replay", "orin_handoff_preflight"]
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory", "family-name preference", "compatibility wrapper retention", "caller evidence",
    "trigger collision review", "stale owner label review", "stale phase label review", "stale route title review",
    "absolute-path privacy review", "raw identifier privacy review", "credential-pattern review", "transcript-pattern review",
    "duplicate proposal review", "duplicate task review", "duplicate skill review", "duplicate runner review",
    "JSON formatting", "Markdown heading order", "source-label consistency", "truth-label consistency",
    "rollback coverage", "protected-gate coverage", "failure-credit consistency", "same-owner labelling",
    "manifest exclusions", "file-cap posture", "document-cap posture", "commit-cap posture",
    "D-first storage posture", "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6593-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
CAELEN_CLEAN_SEEDS = [
    {"task_id": f"V6594-SEED-CLEAN-{i:03d}", "title": f"Caelen may review and refine {name}", "state": "seed_only_not_executed_by_sable"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("NPS-LIGHTHOUSE", "official_us_national_park_service", "https://www.nps.gov/maritime/nhlpa/handbook/HistoricLighthousePreservationHandbook.pdf", "Historic lighthouse and classical Fresnel-lens component, condition, and preventive-care vocabulary only; no inspection, treatment, access, or conservation conformance claim."),
    ("IALA-S1020", "official_international_organization_for_marine_aids_to_navigation", "https://www.iala.int/product/s1020/", "Marine aids-to-navigation design, signalling, maintenance, power, heritage, and culture requirement vocabulary only; no conformance or service-authority claim."),
    ("MARITIME-NZ-ATON", "official_maritime_new_zealand", "https://www.maritimenz.govt.nz/readiness-and-response/navigational-safety-and-communications/aids-to-navigation/", "New Zealand aids-to-navigation system and application vocabulary only; no installation, alteration, removal, or navigational-authority decision."),
    ("CCI-GLASS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/ceramics-glass-preventive-conservation.html", "Glass fragility, handling, storage, and environmental-risk vocabulary only; no diagnosis, treatment, or conservation conformance claim."),
    ("CCI-METALS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html", "Metal condition and corrosion-care vocabulary only; no diagnosis, treatment, safety, or conservation conformance claim."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/pml/special-publication-811", "SI quantity, unit, symbol, and measurement-uncertainty vocabulary."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "General provenance entity, activity, agent, and lineage vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/WAI/standards-guidelines/wcag/", "Accessible structure vocabulary with manual and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty reservation; no Māori authority claim."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without signature or credential claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic reverse-chronological tracked-path selection method."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "UTF-8 deterministic JSON parse and serialization implications."),
]

LEGACY_TEMPLATE_STARTUP_FAILURES = [
    {
        "negative_id": "V6593-X1-N001",
        "signature": "first-tool-call-assumed-unavailable-shell-command-surface",
        "recovery": "Use the installed exec-command surface and keep subsequent repository probes bounded and literal.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N002",
        "signature": "first-activation-baton-read-truncated-after-line-180",
        "recovery": "Read the exact Git object contiguously in bounded forty-line windows through EOF and verify total line and word counts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N003",
        "signature": "parallel-three-window-baton-render-exceeded-model-context",
        "recovery": "Stop parallel rendering and complete the same immutable baton sequentially with nonoverlapping bounded windows.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N004",
        "signature": "broad-repository-path-discovery-returned-truncated-historical-listing",
        "recovery": "Restrict path discovery to the current v659 source owner, exact phase, and named activation artifacts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N005",
        "signature": "backend-rejected-write-stdin-control-c-on-noninteractive-session",
        "recovery": "Do not inject control bytes; poll the yielded command with the supported wait surface and inspect its terminal result.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N006",
        "signature": "powershell-materialized-statistics-probe-used-an-empty-pipe-element",
        "recovery": "Materialize the foreach results into a task-specific variable before sorting and projecting bounded scalar output.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N007",
        "signature": "broad-receipt-filename-search-exceeded-useful-owner-local-bound",
        "recovery": "Stop the broad search, inspect the exact owner and phase receipt directory, and verify the successful receipt by supplied SHA-256.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N008",
        "signature": "first-owned-lane-absence-preflight-had-powershell-cast-and-semicolon-parse-error",
        "recovery": "Capture each Git exit code separately, resolve literal branch and path targets, then create one additive Auren-owned worktree from the verified immutable source.",
        "recovery_passed": True,
    },
]

STARTUP_FAILURES = [
    {
        "negative_id": "V6593-X1-N001",
        "signature": "combined-source-equality-wrapper-completed-without-a-usable-receipt",
        "recovery": "Split branch, local, upstream, tracking, live-remote, divergence, and cleanliness into bounded scalar probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N002",
        "signature": "unquoted-divergence-revision-expression-returned-no-usable-scalar",
        "recovery": "Quote the exact triple-dot revision expression and emit exit code plus a labelled divergence scalar.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N003",
        "signature": "combined-commit-surface-counter-returned-no-usable-receipt",
        "recovery": "Count x1, evidence, final, and source-to-final surfaces with separate exact revision probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N004",
        "signature": "write-all-before-read-git-cat-file-batch-probe-deadlocked-and-left-a-helper",
        "recovery": "Stream one object query at a time through one cat-file process, drain each response immediately, and stop only the verified orphan helper.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N005",
        "signature": "auth-validation-summary-selected-issues-while-the-schema-emits-errors",
        "recovery": "Inspect exact top-level keys and read the errors array without rerunning the already successful validator.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N006",
        "signature": "worktree-add-wrapper-yielded-before-the-original-checkout-reached-terminal-state",
        "recovery": "Do not duplicate checkout; monitor the exact original Git process and verify branch and head after it exits.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N007",
        "signature": "powershell-foreach-output-was-piped-directly-and-triggered-an-empty-pipe-element",
        "recovery": "Materialize foreach output into an array before sorting, projecting, or serializing it.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N008",
        "signature": "bounded-checkout-wait-wrapper-returned-no-scalar-while-the-original-process-remained-active",
        "recovery": "Use direct short PID probes, retain the wait-wrapper failure, and avoid a second checkout invocation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N009",
        "signature": "official-source-search-wrapper-assumed-an-mcp-content-array-and-rendered-no-evidence",
        "recovery": "Serialize the installed web result object directly and keep the first wrapper failure at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N010",
        "signature": "combined-post-check-mixed-full-untracked-status-file-count-and-worktree-registration-without-a-receipt",
        "recovery": "Split revision, tracked status, tracked-file count, untracked status, and worktree registration into bounded probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N011",
        "signature": "first-full-untracked-scan-wrapper-returned-before-its-read-only-git-process-reached-terminal-state",
        "recovery": "Retain the wrapper failure and inspect the exact Git process before any further untracked scan.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N012",
        "signature": "second-untracked-scan-was-launched-before-the-first-read-only-scan-was-confirmed-terminal",
        "recovery": "Do not launch a third scan; verify both exact processes terminate and use exact staged manifests for the x1 boundary.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N013",
        "signature": "first-x1-materialization-failed-closed-on-two-title-neighbour-collisions",
        "recovery": "Retain the failed build, inspect exact nearest inherited titles, and revise only the two colliding titles before rerunning the same bounded novelty gate.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N014",
        "signature": "combined-process-and-staged-status-probe-completed-without-a-usable-receipt",
        "recovery": "Retain the missing receipt at zero credit and split the exact staged-name query from any process inspection before continuing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N015",
        "signature": "first-exact-index-reviewer-lost-embedded-python-quotes-through-windows-native-argument-handling",
        "recovery": "Retain the syntax failure at zero credit and pass the unchanged reviewer through standard input instead of a quote-bearing native argument.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N016",
        "signature": "first-running-index-review-overclassified-public-drive-root-capacity-probes-as-private-local-paths",
        "recovery": "Inspect only the exact candidate line numbers, disclose no matched value, and distinguish root-only storage probes from paths carrying private suffixes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N017",
        "signature": "first-root-only-adjudicator-assumed-one-source-slash-and-missed-escaped-root-literals",
        "recovery": "Accept one-or-more source escape slashes only when the complete quoted literal ends at the drive root, then rerun the unchanged five-class review.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X1-N018",
        "signature": "final-restage-wrapper-promoted-benign-git-line-ending-warnings-to-a-terminating-powershell-error",
        "recovery": "Inspect the existing index first, retain the wrapper failure, and use the native exit code rather than PowerShell stderr classification for any required idempotent restage.",
        "recovery_passed": True,
    },
]

LEGACY_TEMPLATE_X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6593-X2-N001",
        "signature": "combined-post-x1-equality-wrapper-returned-no-usable-receipt",
        "recovery": "Retain the wrapper failure at zero credit, then split local, upstream, tracking, fresh-live, divergence, ancestry, commit-delta, and cleanliness checks into bounded literal probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X2-N002",
        "signature": "initial-x2-build-wrapper-returned-before-original-child-reached-terminal-state",
        "recovery": "Do not launch a duplicate build or scan; retain the wrapper failure and monitor the exact original Python PID plus declared scan and truth paths until the original process exits.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X2-N003",
        "signature": "bounded-wait-process-wrapper-returned-no-usable-probe-output",
        "recovery": "Retain the wait-wrapper failure, avoid replay, and use direct short PID and exact-artifact probes until the original process exits with one complete scan and truth packet.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X2-N004",
        "signature": "combined-governance-probe-assumed-nonexistent-skill-state-subdirectories",
        "recovery": "Use the exact references/current-roster.json and references/current-state.json locations declared by the fully read roster and authorization skills, then validate them read-only.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X2-N005",
        "signature": "windows-rg-rejected-literal-wildcard-reference-paths",
        "recovery": "Search each exact skill root with a -g '*.md' filter or read the declared reference paths literally; do not pass wildcard text as a Windows path.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6593-X2-N006",
        "signature": "method-flow-validator-and-summary-stdout-exceeded-wrapper-output-budget",
        "recovery": "Keep the complete on-disk receipts, update the changed-input ledger for this retained failure, suppress bulk stdout on the isolated validation and summary commands, and read only exact scalar counts.",
        "recovery_passed": True,
    },
]

X2_FAILURES: list[dict[str, object]] = []
