#!/usr/bin/env python3
"""Frozen planning data for Orin Thale's v659-v5 phase."""

from __future__ import annotations


PHASE = "v659-v5"
CANONICAL_PHASE = "v659-v5"
PHASE_CODE = "V6595"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational provenance-and-remedy cartographer"
HOPE = (
    "make every handoff traceable, every authority boundary visible, and every "
    "correction recoverable without mistaking simulation for service"
)
BRANCH = "codex/GHC-Family/orin-thale-v659-v5-full-tools"
PHASE_ROOT = "docs/orin-thale/v659-v5"

SOURCE_OWNER = "Sable Rook"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v659-v3-full-tools"
SOURCE_FINAL = "fceb00d31c77f63ba1e0c4342c9a721304bcf5da"
SOURCE_X1 = "3cb76380d33dd177154e6308f13c04cf5b5e900a"
SOURCE_EVIDENCE = "04d167b799ba8b9de885e66ff8ee480bf5b219b2"
SOURCE_CLOSEOUT_BASE = "91d0ee0d7c4f37dbaa13f07d191f8af4b2464f73"
X1_FREEZE = "pending_until_x2"
PRIOR_FROZEN = 2970
SOURCE_SEALED_NEGATIVES = 18779
SOURCE_EXTERNAL_NEGATIVES = 1
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 124
SOURCE_EXACT_GATES = 123
SOURCE_SEALED_METHODS = 5053
SOURCE_EXTERNAL_METHODS = 1
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 0
NEW_UNIQUE_COUNT = 40
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "Freed ID/CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic oral-history magnetic-tape accession, carrier observation, "
    "consent and access reservation, digitization lineage, correction, accessible "
    "finding-aid, workload control, readback, and handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 33,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_narrators_interviewers_archivists_technicians_communities_affected_parties_and_authorities",
    "real_interviews_recordings_tapes_playback_equipment_transcripts_consent_records_rights_records_measurements_or_identifiers",
    "real_accession_playback_transfer_redaction_release_takedown_remedy_privacy_or_cultural_decision",
    "professional_oral_history_archival_preservation_audio_engineering_privacy_security_or_accessibility_authority",
    "empirical_gmut_audio_prediction_likelihood_parameter_constraint_observational_confirmation_or_physical_discovery",
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
# distinct lighthouse/Fresnel-lens specifications below are frozen as new v659-v5
# proposal rows.
LEGACY_PHASE_NEW_PROPOSAL_SPECS = [
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


# Orin receives the entire 2,970-row chain as immutable comparison evidence.
# None of the rows below is inherited completion credit; all forty are new,
# preregistered v659-v5 contracts in a previously unused oral-history and
# magnetic-tape lens.
TEMPLATE_NEW_PROPOSAL_SPECS = [
    {
        "slug": "oral-history-accession-custody-boundary",
        "title": "Synthetic oral-history magnetic-tape accession intake with depositor placeholder, carrier inventory, consent-status hold, and custody event",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic accession and carrier aliases, depositor placeholder, minimal inventory, consent-status reservation, custody event, and processing refusal",
        "sources": ["OHA-ARCHIVING", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "magnetic-tape-carrier-topology",
        "title": "Open-reel and cassette carrier, reel, hub, pack, leader, shell, and container topology with orphan-part quarantine",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional carrier components, typed containment edges, contradictory-parent quarantine, uncertainty flags, and no handling instruction",
        "sources": ["IASA-TC04", "ARCHIVES-NZ-AV", "W3C-PROV"],
    },
    {
        "slug": "carrier-condition-observation",
        "title": "Magnetic-tape pack, edge, splice, leader, shell, label, and visible-residue observation ledger with diagnosis abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic carrier regions, bounded visible-condition vocabulary, viewpoint and lighting pins, uncertainty note, and diagnosis or treatment refusal",
        "sources": ["ARCHIVES-NZ-AV", "IASA-TC04", "W3C-PROV"],
    },
    {
        "slug": "av-storage-environment-reservation",
        "title": "Audiovisual storage temperature, humidity, fluctuation, enclosure, support, and inspection-due placeholders with control-action hold",
        "outcome": "completed",
        "pillar": "THOS Body and GMUT Mind",
        "mechanism": "synthetic environment and enclosure states, declared units, missing-measurement marker, review-due placeholder, and environmental-control abstention",
        "sources": ["ARCHIVES-NZ-AV", "NIST-SI", "W3C-PROV"],
    },
    {
        "slug": "playback-compatibility-hold",
        "title": "Magnetic-tape format, width, speed, track pattern, reel interface, machine profile, and playback-compatibility docket with operation refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional carrier and machine profiles, compatibility assertions, conflict challenge, competence referral, and no loading or playback instruction",
        "sources": ["IASA-TC04", "ARCHIVES-NZ-AV", "W3C-PROV"],
    },
    {
        "slug": "tape-transport-state-boundary",
        "title": "Tape-path, guide, head, capstan, pinch-roller, tension, and transport-state graph with threading and actuation refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic transport components, compatible state transitions, unresolved fault and tension placeholders, isolation marker, and physical-actuation abstention",
        "sources": ["IASA-TC04", "W3C-PROV"],
    },
    {
        "slug": "speed-equalization-reservation",
        "title": "Playback speed, equalization family, reference level, azimuth, channel gain, and calibration-age reservation with setting-change hold",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "declared symbolic settings and units, provenance source, unresolved compatibility flag, calibration-age placeholder, and no equipment-setting recommendation",
        "sources": ["IASA-TC04", "NIST-SI", "W3C-PROV"],
    },
    {
        "slug": "track-channel-layout-provenance",
        "title": "Magnetic-tape track, channel, side, direction, programme segment, silence marker, and layout revision provenance map",
        "outcome": "completed",
        "pillar": "Freed ID and GMUT Mind",
        "mechanism": "synthetic track and channel aliases, directional layout edges, revision lineage, ambiguity quarantine, and content-interpretation refusal",
        "sources": ["IASA-TC04", "W3C-PROV"],
    },
    {
        "slug": "audio-transfer-event-chain",
        "title": "Synthetic audio-transfer event with source carrier, machine profile, signal path, operator placeholder, timestamp, hold, and handoff lineage",
        "outcome": "completed",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "fictional transfer activity, source and destination aliases, machine-profile digest, operator placeholder, timestamp basis, hold state, and no real transfer claim",
        "sources": ["IASA-TC04", "W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "source-capture-fixity-envelope",
        "title": "Source-capture byte count, digest, segment boundary, retry event, mismatch quarantine, and no-authenticity fixity envelope",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "synthetic byte count and digest, ordered segment aliases, retry lineage, mismatch quarantine, challenge state, and authenticity or signature abstention",
        "sources": ["IETF-JCS", "W3C-PROV", "IASA-TC04"],
    },
    {
        "slug": "preservation-master-format-reservation",
        "title": "Preservation-master audio container, encoding, sample structure, metadata profile, format-version, and migration-hold declaration",
        "outcome": "completed",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic format and profile declarations, version pins, embedded-metadata placeholder, migration hold, and no repository conformance claim",
        "sources": ["LOC-RFS", "IASA-TC04", "W3C-PROV"],
    },
    {
        "slug": "access-derivative-lineage",
        "title": "Preservation master, access derivative, transcript, excerpt, waveform image, and checksum ancestry with disclosure stop",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic master and derivative nodes, transformation edges, purpose labels, checksum envelope, disclosure ceiling, and release refusal",
        "sources": ["W3C-PROV", "IETF-JCS", "OHA-ARCHIVING"],
    },
    {
        "slug": "audio-qc-cue-ledger",
        "title": "Audio quality-control cue ledger with segment clock, channel, cue class, reviewer placeholder, uncertainty, and repair abstention",
        "outcome": "completed",
        "pillar": "THOS Body and GMUT Mind",
        "mechanism": "synthetic time-bounded cue rows, channel labels, declared cue classes, reviewer placeholder, uncertainty note, and signal-repair refusal",
        "sources": ["IASA-TC04", "NIST-SI", "W3C-PROV"],
    },
    {
        "slug": "timebase-wow-flutter-annotation",
        "title": "Timebase, wow, flutter, drift, dropout, noise, and interruption annotation board with zero measurements and causal abstention",
        "outcome": "completed",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic audio-condition quantities, SI unit placeholders, interval annotations, zero measured rows, uncertainty flags, and causal or restoration refusal",
        "sources": ["NIST-SI", "IASA-TC04", "W3C-PROV"],
    },
    {
        "slug": "narrator-consent-scope-state",
        "title": "Oral-history narrator consent-scope, intended use, repository, access tier, revision, review, and release-hold state machine",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic consent-state placeholders, purpose and access declarations, revision and review events, unresolved scope conflict, and no consent inference",
        "sources": ["OHA-PRINCIPLES", "OHA-ARCHIVING", "NZ-PRIVACY"],
    },
    {
        "slug": "embargo-access-clock-reservation",
        "title": "Oral-history embargo, review date, access tier, expiry candidate, extension request, notification, and release-authority reservation",
        "outcome": "completed",
        "pillar": "CBR Heart",
        "mechanism": "synthetic embargo and access states, clock basis, review candidate, notification placeholder, conflicting instruction hold, and no automatic release",
        "sources": ["OHA-ARCHIVING", "NZ-PRIVACY", "W3C-PROV"],
    },
    {
        "slug": "withdrawal-takedown-remedy-lifecycle",
        "title": "Oral-history withdrawal, correction, access restriction, takedown request, counterstatement, remedy route, and unresolved-jurisdiction lifecycle",
        "outcome": "completed",
        "pillar": "CBR Heart",
        "mechanism": "synthetic request and notice events, correction and restriction candidates, counterstatement, unresolved remedy jurisdiction, and decision-rights abstention",
        "sources": ["OHA-PRINCIPLES", "OHA-ARCHIVING", "NZ-PRIVACY"],
    },
    {
        "slug": "narrator-name-display-separation",
        "title": "Source narrator identifier, preferred display name, pseudonym placeholder, pronunciation note, revision, and public-label separation ledger",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic source and display fields, pseudonym placeholder, pronunciation and revision provenance, disclosure hold, and naming-authority refusal",
        "sources": ["OHA-PRINCIPLES", "NZ-PRIVACY", "W3C-PROV"],
    },
    {
        "slug": "cultural-sensitivity-segment-hold",
        "title": "Oral-history culturally sensitive segment flag with source cue, community-review placeholder, access hold, counterstatement, and no-content judgment",
        "outcome": "completed",
        "pillar": "CBR Heart",
        "mechanism": "synthetic segment and sensitivity placeholders, provenance cue, community-review reservation, access hold, contestation path, and cultural-judgment refusal",
        "sources": ["OHA-PRINCIPLES", "TE-MANA-RARAUNGA", "W3C-PROV"],
    },
    {
        "slug": "maori-data-governance-reservation",
        "title": "Māori oral-history data-governance reservation with whakapapa and collective-interest placeholders, authority hold, and no-ratification claim",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic collective-interest and governance placeholders, access and purpose reservations, authority hold, challenge route, and explicit Māori-authority abstention",
        "sources": ["TE-MANA-RARAUNGA", "NZ-PRIVACY", "OHA-PRINCIPLES"],
    },
    {
        "slug": "third-party-mention-disclosure-hold",
        "title": "Third-party mention, identifiability cue, sensitivity class, notice placeholder, redaction candidate, and disclosure hold",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic mention and identity cues, sensitivity placeholder, indirect-collection notice state, redaction candidate, and disclosure refusal",
        "sources": ["NZ-PRIVACY", "OHA-PRINCIPLES", "W3C-PROV"],
    },
    {
        "slug": "audio-redaction-mask-lineage",
        "title": "Audio redaction mask, reason code, segment boundary, reversible edit event, derivative digest, reviewer placeholder, and source-preservation hold",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic time masks and reason codes, edit-event provenance, derivative digest, reviewer placeholder, source retention reservation, and no release authority",
        "sources": ["W3C-PROV", "NZ-PRIVACY", "IETF-JCS"],
    },
    {
        "slug": "transcript-correction-provenance",
        "title": "Oral-history transcript token, time anchor, uncertainty, correction proposal, narrator-review placeholder, supersession, and readback provenance",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic transcript tokens and time anchors, uncertainty tags, correction candidates, review placeholder, supersession edges, and no accuracy-complete claim",
        "sources": ["OHA-PRINCIPLES", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "translation-interpretation-attribution",
        "title": "Oral-history translation, interpretation note, source-language placeholder, translator role, version, contestation, and meaning-authority refusal",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic source and target text aliases, translator-role placeholder, version lineage, contestation state, uncertainty note, and interpretive-authority abstention",
        "sources": ["OHA-PRINCIPLES", "W3C-PROV", "WCAG22"],
    },
    {
        "slug": "rights-permission-use-matrix",
        "title": "Oral-history ownership-claim, licence placeholder, permission scope, territory, medium, excerpt, expiry, and rights-clearance hold matrix",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic claim and permission assertions, scope and expiry placeholders, conflict flag, evidence-link requirement, and legal-rights conclusion refusal",
        "sources": ["OHA-ARCHIVING", "NZ-PRIVACY", "W3C-PROV"],
    },
    {
        "slug": "accessible-oral-history-finding-aid",
        "title": "Accessible oral-history finding-aid table with structured headings, segment chronology, text alternatives, restriction status, and manual-review reservation",
        "outcome": "completed",
        "pillar": "CBR Heart",
        "mechanism": "structured synthetic headings and table relationships, ordered chronology, text alternatives, restriction disclosure, keyboard-order placeholder, and no accessibility-complete claim",
        "sources": ["WCAG22", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "audio-alternative-navigation-map",
        "title": "Oral-history audio, transcript, summary, topic cue, speaker-label placeholder, chapter navigation, and alternative-format availability map",
        "outcome": "completed",
        "pillar": "CBR Heart and THOS Body",
        "mechanism": "synthetic media and alternative nodes, ordered chapter cues, speaker-label placeholders, availability state, navigation fallback, and no accessibility conformance claim",
        "sources": ["WCAG22", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "oral-history-privacy-minimization",
        "title": "Oral-history metadata purpose, necessity, indirect-source notice, sensitive-field minimization, access, correction, and disclosure reservation",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "synthetic metadata fields, purpose and necessity declarations, IPP 3A notice placeholder, minimization flags, correction path, and no legal-compliance conclusion",
        "sources": ["NZ-PRIVACY", "OHA-PRINCIPLES", "W3C-PROV"],
    },
    {
        "slug": "retention-deletion-export-boundary",
        "title": "Oral-history retention rule, preservation exception placeholder, deletion request, export package, audit event, and destructive-action hold",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic retention and deletion assertions, exception placeholder, export manifest, audit lineage, conflict quarantine, and no destructive execution",
        "sources": ["NZ-PRIVACY", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "av-incident-quarantine-lifecycle",
        "title": "Audiovisual carrier or file incident, affected-scope placeholder, quarantine, preservation copy, notification, recovery point, and release refusal",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic incident and scope aliases, quarantine transition, preservation-copy placeholder, notification state, recovery point, and no operational release",
        "sources": ["IASA-TC04", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "digitization-workload-queue",
        "title": "Oral-history digitization queue with task class, carrier-risk placeholder, consent hold, effort budget, dependency, pause, escalation, and no-throughput claim",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic queue rows, workload ceiling, risk and consent placeholders, dependencies, pause and escalation events, and zero operational-effectiveness claim",
        "sources": ["IASA-TC04", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "oral-history-shift-handover",
        "title": "Oral-history preservation shift handover with unresolved carrier, consent and rights holds, correction queue, dual readback, workload ceiling, and release refusal",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic unresolved-work ledger, consent and rights holds, correction queue, two-party readback placeholders, workload bound, escalation, and release refusal",
        "sources": ["IASA-TC04", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "canonical-oral-history-package",
        "title": "Canonical oral-history package index with ordered asset digests, profile version, transition map, collision refusal, and non-credential declaration",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "synthetic asset index, canonical JSON profile, ordered digests, profile-version lineage, collision challenge, and no signature, key, credential, or production claim",
        "sources": ["IETF-JCS", "W3C-PROV", "OHA-ARCHIVING"],
    },
    {
        "slug": "gmut-audio-signal-proxy",
        "title": "Represented GMUT analog-audio source, transfer function, channel tensor, frequency, phase, amplitude, and noise dimension board with zero signals",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic scalar and tensor audio quantities, declared dimensions and units, transfer placeholders, identifiability flags, zero signal rows, and physical-inference firewall",
        "sources": ["NIST-SI", "IASA-TC04"],
    },
    {
        "slug": "gmut-tape-transport-proxy",
        "title": "Represented GMUT tape-transport speed, tension, head-gap, flux, timebase, coupling, and uncertainty proxy with zero carrier measurements",
        "outcome": "represented",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "typed symbolic transport and magnetic placeholders, unit declarations, bounded parameter domains, zero measurements, uncertainty flags, and no prediction or material claim",
        "sources": ["NIST-SI", "IASA-TC04"],
    },
    {
        "slug": "thos-oral-history-study-protocol",
        "title": "Represented THOS oral-history preservation workflow comparison protocol with blind matched-budget arms, participant and operator gates, safety monitoring, and zero enrolment",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "future-study protocol placeholders, blind matched-budget arm requirements, participant and operator governance, safety and statistics gates, zero enrolment, and no effectiveness claim",
        "sources": ["OHA-PRINCIPLES", "IASA-TC04"],
    },
    {
        "slug": "nonproduction-oral-history-lineage-query",
        "title": "Represented nonproduction oral-history asset-lineage traversal with bounded hop budget, disclosure stop, canonical digest, and no identity credential",
        "outcome": "represented",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic carrier, capture, master, derivative, transcript, and redaction nodes, predecessor edges, hop ceiling, disclosure refusal, and no live identifier or credential",
        "sources": ["W3C-PROV", "IETF-JCS", "OHA-ARCHIVING"],
    },
    {
        "slug": "accessible-transcript-map-proxy",
        "title": "Represented oral-history transcript and restriction map with ordered segments, speaker placeholders, text chronology, keyboard order, and affected-user review hold",
        "outcome": "represented",
        "pillar": "CBR Heart",
        "mechanism": "ordered synthetic transcript regions, restriction table, speaker placeholders, text chronology, focus-order declaration, static fallback, and no accessibility-complete claim",
        "sources": ["WCAG22", "OHA-ARCHIVING", "W3C-PROV"],
    },
    {
        "slug": "real-oral-history-evidence-gap",
        "title": "Open gap for real narrators, interviews, magnetic tapes, playback equipment, transfers, measurements, consent and rights records, repositories, practitioners, and independent review",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero real-person, interview, carrier, machine, audio, transcript, consent, rights, measurement, repository, and participant rows; absent professional and independent review",
        "sources": ["OHA-PRINCIPLES", "OHA-ARCHIVING", "IASA-TC04", "ARCHIVES-NZ-AV", "NIST-SI"],
    },
    {
        "slug": "oral-history-authority-ratification-gate",
        "title": "Exact decision-rights gate for oral-history consent, access, restriction, withdrawal, redaction, rights, preservation treatment, privacy, remedy, legal and cultural interpretation, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "consent, access, restriction, withdrawal, redaction, rights, preservation, privacy, remedy, legal, cultural, collective-governance, affected-party, and Māori-authority reservations",
        "sources": ["OHA-PRINCIPLES", "OHA-ARCHIVING", "IASA-TC04", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]


SELF_SAFE_CATEGORIES = [
    "source-head and live equality", "activation packet raw digest", "proposal-chain parse", "zero inherited completion selections",
    "forty-title novelty audit", "four-label distribution", "workflow-plan policy", "identity boundary",
    "Sable-to-Orin route state", "Tavian standby state", "D-first drive posture", "toolchain versions",
    "x1 artifact inventory", "x1 JSON parse", "x1 privacy classes", "x1 stale-label scan",
    "x1 diff hygiene", "x1 manifest replay", "source-proposal non-credit", "new-proposal provenance",
    "source-label glossary", "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing",
    "wellbeing workload bound", "document-word ceiling", "task-portfolio arithmetic", "skill-plan arithmetic",
    "runner-plan arithmetic", "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6595-SAFE-{i:03d}", "title": f"Validate {name} inside the Orin-owned v659-v5 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6595-SEED-SAFE-{i:03d}",
        "title": f"A later live-reverified successor may evaluate {name} in its own lane",
        "owner": "live_reverification_required",
        "state": "seed_only_not_executed_or_routed_by_orin",
    }
    for i, name in enumerate([
        "source baton digest", "owned-lane equality", "proposal freeze", "synthetic fixture boundary",
        "privacy exclusions", "manifest replay", "Method Flow recovery", "truth-label distribution",
        "authority reservations", "terminal no-replay gate",
    ], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "oral-history accession and consent boundary", "magnetic-tape carrier topology quarantine",
    "audio transfer and derivative lineage", "consent, embargo, and access reservation",
    "narrator correction and supersession provenance", "audio redaction mask lineage",
    "accessible oral-history finding aid", "digitization workload and handover",
    "GMUT audio signal firewall", "oral-history authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6595-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6595-SEED-CAND-{i:03d}", "title": f"A later live-reverified successor may prototype reversible {name}", "owner": "live_reverification_required", "state": "seed_only_not_executed_or_routed_by_orin"}
    for i, name in enumerate([
        "baton parser", "phase-source verifier", "proposal-freeze ledger", "bounded file-scan receipt", "authority-gate atlas",
        "privacy-class reducer", "stale-label classifier", "manifest batch replay", "same-owner evidence labeler", "live-route preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6595-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use real narrators, interviews, magnetic tapes, recordings, consent records, rights records, transcripts, or measurements", "Issue a real accession, playback, transfer, release, or takedown decision",
        "Approve a cleaning, repair, signal-processing, redaction, preservation, or access action", "Publish an authenticity, ownership, rights, or consent conclusion",
        "Make a professional oral-history, archival, audio-engineering, preservation, privacy, or accessibility determination", "Publish personal, sensitive, culturally protected, or collective data",
        "Allocate legal, cultural, access, naming, ownership, remedy, or heritage authority", "Make a Māori data-governance or cultural-authority decision",
        "Deploy a production identity or service system", "Perform destructive shared-drive cleanup",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6595-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation", "Claim consciousness or personhood from task language",
        "Merge or erase sibling identities", "Publish credentials or private callable routes",
        "Declare Stage 20 readiness without evidence",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-oral-history-accession-boundary", "Preserve synthetic oral-history accession, custody, consent-status, and processing holds."),
    ("ghc-family-magnetic-tape-carrier-map", "Quarantine contradictory carrier, reel, hub, pack, leader, shell, and container relations."),
    ("ghc-family-audio-transfer-lineage", "Preserve source, machine-profile, transfer, master, derivative, and fixity lineage without authenticity claims."),
    ("ghc-family-consent-access-reservation", "Reserve consent, embargo, restriction, release, withdrawal, and access decisions to competent affected parties."),
    ("ghc-family-narrator-correction-provenance", "Track transcript and display-label correction, review, supersession, and readback without accuracy authority."),
    ("ghc-family-audio-redaction-lineage", "Track synthetic time masks, reasons, derivatives, review placeholders, and source-preservation holds."),
    ("ghc-family-oral-history-finding-aid", "Expose structured chronology and alternatives while reserving manual and affected-user accessibility review."),
    ("ghc-family-av-workload-handover", "Bound digitization workload, unresolved holds, escalation, dual readback, and release refusal."),
    ("ghc-family-gmut-audio-firewall", "Keep audio and tape-transport proxies typed, dimensioned, zero-row, and physically nonconfirmatory."),
    ("ghc-family-cultural-authority-reservation", "Fail closed around consent, access, rights, privacy, remedy, legal, cultural, collective, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-future-successor-{slug}", "state": "seed_only_not_built_or_routed_by_orin"}
    for slug in [
        "source-baton-check", "owned-lane-guard", "proposal-freeze", "fixture-boundary", "route-classifier",
        "privacy-reducer", "stale-label-review", "manifest-replay", "truth-label-guard", "live-route-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_oral_history_accession_boundary.py", "oral-history-accession-custody-boundary"),
    ("ghc_family_magnetic_tape_carrier_map.py", "magnetic-tape-carrier-topology"),
    ("ghc_family_audio_transfer_lineage.py", "audio-transfer-event-chain"),
    ("ghc_family_consent_access_reservation.py", "narrator-consent-scope-state"),
    ("ghc_family_narrator_correction_provenance.py", "transcript-correction-provenance"),
    ("ghc_family_audio_redaction_lineage.py", "audio-redaction-mask-lineage"),
    ("ghc_family_oral_history_finding_aid.py", "accessible-oral-history-finding-aid"),
    ("ghc_family_av_workload_handover.py", "oral-history-shift-handover"),
    ("ghc_family_gmut_audio_firewall.py", "gmut-audio-signal-proxy"),
    ("ghc_family_cultural_authority_reservation.py", "oral-history-authority-ratification-gate"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_future_successor_{slug}.py", "state": "seed_only_not_built_or_routed_by_orin"}
    for slug in ["source_baton_check", "proposal_freeze", "privacy_reducer", "manifest_replay", "live_route_preflight"]
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
    {"task_id": f"V6595-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6595-SEED-CLEAN-{i:03d}", "title": f"A later live-reverified successor may review and refine {name}", "state": "seed_only_not_executed_or_routed_by_orin"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

LEGACY_OFFICIAL_SOURCES = [
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

OFFICIAL_SOURCES = [
    ("OHA-PRINCIPLES", "primary_oral_history_association", "https://oralhistory.org/principles-and-best-practices-revised-2018/", "Narrator respect, ongoing participation, consent, preparation, preservation, and access vocabulary only; no participant acceptance, ethical ratification, or professional-practice claim."),
    ("OHA-ARCHIVING", "primary_oral_history_association", "https://oralhistory.org/archives-principles-and-best-practices-complete-manual/", "Appraisal, accession, metadata, preservation, access, collaboration, ownership, and rights-management vocabulary only; no repository, rights, consent, or professional conformance claim."),
    ("IASA-TC04", "primary_international_association_of_sound_and_audiovisual_archives", "https://www.iasa-web.org/tc04/audio-preservation", "Digital-audio object, metadata, identifier, signal-extraction, ingest, storage, planning, and access vocabulary only; no playback, transfer, engineering, or preservation conformance claim."),
    ("ARCHIVES-NZ-AV", "official_archives_new_zealand", "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/implementation/care-and-storage-of-physical-records/audiovisual-storage", "Audiovisual carrier identification, handling, storage, and playback-referral vocabulary only; no real handling, diagnosis, playback, deposit, or preservation result."),
    ("LOC-RFS", "official_library_of_congress", "https://www.loc.gov/preservation/resources/rfs/", "The current published Recommended Formats Statement's audio-format and accessibility-support vocabulary only; no acquisition, repository, migration, or format-conformance claim."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/pml/special-publication-811", "SI quantity, unit, symbol, and measurement-uncertainty vocabulary only; no measured audio or carrier result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "General provenance entity, activity, agent, and lineage vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current WCAG 2.2 structure, time-based-media, navigation, and status vocabulary with manual and affected-user review reserved; no accessibility-complete claim."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority or ratification claim."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without signature, key, proof, credential, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic reverse-chronological tracked-path selection method."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "UTF-8 deterministic JSON parse and serialization implications."),
]

LEGACY_TEMPLATE_STARTUP_FAILURES = [
    {
        "negative_id": "V6595-X1-N001",
        "signature": "first-tool-call-assumed-unavailable-shell-command-surface",
        "recovery": "Use the installed exec-command surface and keep subsequent repository probes bounded and literal.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N002",
        "signature": "first-activation-baton-read-truncated-after-line-180",
        "recovery": "Read the exact Git object contiguously in bounded forty-line windows through EOF and verify total line and word counts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N003",
        "signature": "parallel-three-window-baton-render-exceeded-model-context",
        "recovery": "Stop parallel rendering and complete the same immutable baton sequentially with nonoverlapping bounded windows.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N004",
        "signature": "broad-repository-path-discovery-returned-truncated-historical-listing",
        "recovery": "Restrict path discovery to the current v659 source owner, exact phase, and named activation artifacts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N005",
        "signature": "backend-rejected-write-stdin-control-c-on-noninteractive-session",
        "recovery": "Do not inject control bytes; poll the yielded command with the supported wait surface and inspect its terminal result.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N006",
        "signature": "powershell-materialized-statistics-probe-used-an-empty-pipe-element",
        "recovery": "Materialize the foreach results into a task-specific variable before sorting and projecting bounded scalar output.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N007",
        "signature": "broad-receipt-filename-search-exceeded-useful-owner-local-bound",
        "recovery": "Stop the broad search, inspect the exact owner and phase receipt directory, and verify the successful receipt by supplied SHA-256.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N008",
        "signature": "first-owned-lane-absence-preflight-had-powershell-cast-and-semicolon-parse-error",
        "recovery": "Capture each Git exit code separately, resolve literal branch and path targets, then create one additive Auren-owned worktree from the verified immutable source.",
        "recovery_passed": True,
    },
]

LEGACY_PHASE_STARTUP_FAILURES = [
    {
        "negative_id": "V6595-X1-N001",
        "signature": "combined-source-equality-wrapper-completed-without-a-usable-receipt",
        "recovery": "Split branch, local, upstream, tracking, live-remote, divergence, and cleanliness into bounded scalar probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N002",
        "signature": "unquoted-divergence-revision-expression-returned-no-usable-scalar",
        "recovery": "Quote the exact triple-dot revision expression and emit exit code plus a labelled divergence scalar.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N003",
        "signature": "combined-commit-surface-counter-returned-no-usable-receipt",
        "recovery": "Count x1, evidence, final, and source-to-final surfaces with separate exact revision probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N004",
        "signature": "write-all-before-read-git-cat-file-batch-probe-deadlocked-and-left-a-helper",
        "recovery": "Stream one object query at a time through one cat-file process, drain each response immediately, and stop only the verified orphan helper.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N005",
        "signature": "auth-validation-summary-selected-issues-while-the-schema-emits-errors",
        "recovery": "Inspect exact top-level keys and read the errors array without rerunning the already successful validator.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N006",
        "signature": "worktree-add-wrapper-yielded-before-the-original-checkout-reached-terminal-state",
        "recovery": "Do not duplicate checkout; monitor the exact original Git process and verify branch and head after it exits.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N007",
        "signature": "powershell-foreach-output-was-piped-directly-and-triggered-an-empty-pipe-element",
        "recovery": "Materialize foreach output into an array before sorting, projecting, or serializing it.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N008",
        "signature": "bounded-checkout-wait-wrapper-returned-no-scalar-while-the-original-process-remained-active",
        "recovery": "Use direct short PID probes, retain the wait-wrapper failure, and avoid a second checkout invocation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N009",
        "signature": "official-source-search-wrapper-assumed-an-mcp-content-array-and-rendered-no-evidence",
        "recovery": "Serialize the installed web result object directly and keep the first wrapper failure at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N010",
        "signature": "combined-post-check-mixed-full-untracked-status-file-count-and-worktree-registration-without-a-receipt",
        "recovery": "Split revision, tracked status, tracked-file count, untracked status, and worktree registration into bounded probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N011",
        "signature": "first-full-untracked-scan-wrapper-returned-before-its-read-only-git-process-reached-terminal-state",
        "recovery": "Retain the wrapper failure and inspect the exact Git process before any further untracked scan.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N012",
        "signature": "second-untracked-scan-was-launched-before-the-first-read-only-scan-was-confirmed-terminal",
        "recovery": "Do not launch a third scan; verify both exact processes terminate and use exact staged manifests for the x1 boundary.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N013",
        "signature": "first-x1-materialization-failed-closed-on-two-title-neighbour-collisions",
        "recovery": "Retain the failed build, inspect exact nearest inherited titles, and revise only the two colliding titles before rerunning the same bounded novelty gate.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N014",
        "signature": "combined-process-and-staged-status-probe-completed-without-a-usable-receipt",
        "recovery": "Retain the missing receipt at zero credit and split the exact staged-name query from any process inspection before continuing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N015",
        "signature": "first-exact-index-reviewer-lost-embedded-python-quotes-through-windows-native-argument-handling",
        "recovery": "Retain the syntax failure at zero credit and pass the unchanged reviewer through standard input instead of a quote-bearing native argument.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N016",
        "signature": "first-running-index-review-overclassified-public-drive-root-capacity-probes-as-private-local-paths",
        "recovery": "Inspect only the exact candidate line numbers, disclose no matched value, and distinguish root-only storage probes from paths carrying private suffixes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N017",
        "signature": "first-root-only-adjudicator-assumed-one-source-slash-and-missed-escaped-root-literals",
        "recovery": "Accept one-or-more source escape slashes only when the complete quoted literal ends at the drive root, then rerun the unchanged five-class review.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N018",
        "signature": "final-restage-wrapper-promoted-benign-git-line-ending-warnings-to-a-terminating-powershell-error",
        "recovery": "Inspect the existing index first, retain the wrapper failure, and use the native exit code rather than PowerShell stderr classification for any required idempotent restage.",
        "recovery_passed": True,
    },
]

TEMPLATE_STARTUP_FAILURES = [
    {
        "negative_id": "V6595-X1-N001",
        "signature": "initial-memory-registry-probe-used-a-nonexistent-relative-memory-path",
        "recovery": "Use the documented literal memories/MEMORY.md path, retain the failed path assumption, and treat live v659 activation as authoritative over historical memory.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N002",
        "signature": "first-skill-inventory-piped-foreach-output-directly-and-triggered-an-empty-pipe-element",
        "recovery": "Materialize foreach output into a task-specific array before sorting, projecting, or JSON serialization.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N003",
        "signature": "skill-inventory-repeated-the-known-direct-foreach-pipeline-parser-failure",
        "recovery": "Retain the recurrence separately and apply the materialized-array guard before every later multi-row PowerShell projection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N004",
        "signature": "artifact-reference-search-used-an-invalid-optional-token-regex",
        "recovery": "Use an ASCII-safe literal alternation without a bare repetition operator and preserve the failed search at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N005",
        "signature": "parallel-source-status-probe-outlived-its-wrapper-and-lost-the-original-session-handle",
        "recovery": "Confirm the original Git process terminated, then split tracked cleanliness and untracked-path checks into separate bounded scalar probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N006",
        "signature": "proposal-index-probe-assumed-a-nonexistent-rows-array",
        "recovery": "Inspect exact top-level JSON keys first, then combine prior_proposals and new_proposals according to the committed schema.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N007",
        "signature": "first-official-source-search-wrapper-assumed-a-content-array-and-rendered-no-usable-result",
        "recovery": "Serialize the installed web result directly, narrow to official domains, and retain the first empty rendering at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N008",
        "signature": "first-semantic-data-patch-failed-closed-on-an-inherited-unicode-byte-mismatch",
        "recovery": "Split the change into smaller ASCII-anchored hunks and replace Unicode authority wording only against exact UTF-8 text.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N009",
        "signature": "official-source-list-replacement-failed-closed-on-a-second-inherited-unicode-byte-mismatch",
        "recovery": "Preserve the inherited list under an explicit legacy name and add the verified Orin source list separately without byte-sensitive replacement.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N010",
        "signature": "first-x1-test-update-failed-closed-on-the-same-inherited-unicode-byte-mismatch",
        "recovery": "Separate ASCII-only assertions from the exact UTF-8 authority assertion and keep all three failed patches independently visible.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N011",
        "signature": "first-precommit-summary-typed-a-property-name-as-a-powershell-command-and-yielded-before-terminal-output",
        "recovery": "Follow the original process to completion, retain the typo at zero credit, and use direct property projection in later scalar summaries.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N012",
        "signature": "workflow-skill-fixture-validator-was-pointed-at-the-flat-phase-refinement-output",
        "recovery": "Retain the missing-fixture-path failure at zero credit, distinguish the skill-package fixture validator from the phase-plan runner, and run the bounded refinement only against the regenerated request that includes this failure.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N013",
        "signature": "combined-prestage-status-wrapper-completed-without-a-scalar-receipt",
        "recovery": "Retain the missing summary at zero credit and split the empty-index proof from later bounded status and allowlist checks.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N014",
        "signature": "first-index-review-summary-projected-guessed-null-field-names-from-four-valid-receipts",
        "recovery": "Retain the incomplete scalar projection at zero credit, inspect each exact top-level key set, and use only the committed schema fields in the corrected staged review.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N015",
        "signature": "second-index-review-assumed-a-lowercase-route-state-value-in-two-valid-receipts",
        "recovery": "Retain the failed two-check review at zero credit, inspect the exact staged values, and compare the declared uppercase held-state literal without changing route state.",
        "recovery_passed": True,
    },
]

LEGACY_TEMPLATE_X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6595-X2-N001",
        "signature": "combined-post-x1-equality-wrapper-returned-no-usable-receipt",
        "recovery": "Retain the wrapper failure at zero credit, then split local, upstream, tracking, fresh-live, divergence, ancestry, commit-delta, and cleanliness checks into bounded literal probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N002",
        "signature": "initial-x2-build-wrapper-returned-before-original-child-reached-terminal-state",
        "recovery": "Do not launch a duplicate build or scan; retain the wrapper failure and monitor the exact original Python PID plus declared scan and truth paths until the original process exits.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N003",
        "signature": "bounded-wait-process-wrapper-returned-no-usable-probe-output",
        "recovery": "Retain the wait-wrapper failure, avoid replay, and use direct short PID and exact-artifact probes until the original process exits with one complete scan and truth packet.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N004",
        "signature": "combined-governance-probe-assumed-nonexistent-skill-state-subdirectories",
        "recovery": "Use the exact references/current-roster.json and references/current-state.json locations declared by the fully read roster and authorization skills, then validate them read-only.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N005",
        "signature": "windows-rg-rejected-literal-wildcard-reference-paths",
        "recovery": "Search each exact skill root with a -g '*.md' filter or read the declared reference paths literally; do not pass wildcard text as a Windows path.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N006",
        "signature": "method-flow-validator-and-summary-stdout-exceeded-wrapper-output-budget",
        "recovery": "Keep the complete on-disk receipts, update the changed-input ledger for this retained failure, suppress bulk stdout on the isolated validation and summary commands, and read only exact scalar counts.",
        "recovery_passed": True,
    },
]

TEMPLATE_X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6595-X2-N001",
        "signature": "parallel-post-push-equality-wrapper-returned-no-full-cleanliness-receipt-within-its-bounded-window",
        "recovery": "Retain the missing row at zero credit, verify no Git process remains, and run one separate exact full-status probe before declaring x1 clean.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N002",
        "signature": "first-bulk-terminology-rewrite-used-case-insensitive-powershell-hash-keys-and-failed-before-file-mutation",
        "recovery": "Retain the parser failure at zero credit and use an ordered pair list so upper- and lower-case replacements remain distinct.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N003",
        "signature": "broad-current-tree-run-evaluated-the-immutable-x1-manifest-against-the-advanced-x2-data-file",
        "recovery": "Retain the named x1 failure, exclude no eligible x2 test, and materialize the exact x1 Git archive for the later immutable-x1 selection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N004",
        "signature": "broad-current-tree-run-evaluated-the-x1-no-x2-surface-assertion-after-authorized-x2-materialization",
        "recovery": "Retain the named x1 failure and bind x1 phase-separation credit only to the exact x1 commit tree in the later canonical selection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N005",
        "signature": "x2-manifest-hash-was-stale-after-the-current-x2-test-expectations-were-corrected",
        "recovery": "Retain the named manifest failure, regenerate the self-excluding x2 manifest after all current code edits, and rerun only the eligible x2 selection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N006",
        "signature": "first-evidence-surface-inventory-summary-was-drowned-by-inherited-line-ending-diagnostics",
        "recovery": "Retain the missing scalar at zero credit and rerun the read-only path inventory with command-local normalization disabled and stderr suppressed.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N007",
        "signature": "first-full-evidence-index-reviewer-outlived-its-wrapper-and-returned-no-attributable-receipt",
        "recovery": "Retain the missing receipt, wait for the exact read-only process to exit, and replace per-path Git process startup with one indexed-object map plus one drained batch reader.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N008",
        "signature": "bounded-wait-wrapper-for-the-original-reviewer-yielded-without-a-usable-process-state-receipt",
        "recovery": "Retain the wait failure and use short direct PID, CPU, and child-process probes until the original reviewer exits; do not launch a duplicate while it remains alive.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N009",
        "signature": "valid-second-staged-review-pass-lost-its-combined-postflight-summary-to-line-ending-warning-noise",
        "recovery": "Keep the valid staged-review receipt, retain the wrapper loss separately, and run receipt cleanliness and diff hygiene as warning-free scalar probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N010",
        "signature": "first-diff-hygiene-probe-found-crlf-carriage-returns-throughout-mechanically-copied-x2-templates",
        "recovery": "Retain the hygiene failure and normalize only the Sable-owned x2 code and test text to LF before regenerating manifests and restaging.",
        "recovery_passed": True,
    },
]


# ---------------------------------------------------------------------------
# Orin Thale v659-v5 live-authorized phase data.
#
# The large structures above are retained template evidence from the immutable
# Caelen v659-v4 builder.  The assignments below are the only active v659-v5
# planning surface.  Selected inherited rows are revalidation references only:
# they are not reappended, novel, executed, or credited as Orin outcomes.
# ---------------------------------------------------------------------------

PHASE = "v659-v5"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6595"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-boundary steward"
HOPE = "keep every surviving claim traceable, falsifiable, and easy to retract"
BRANCH = "codex/GHC-Family/orin-thale-v659-v5-full-tools"
PHASE_ROOT = "docs/orin-thale/v659-v5"

SOURCE_OWNER = "Caelen Ash"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v659-v4-full-tools"
SOURCE_FINAL = "3ce23aede614994bdec1e700a98388166bcb0334"
SOURCE_X1 = "8f1d7f05d3e79ede4b6579a68f1e0d901eba8669"
SOURCE_EVIDENCE = "f8b5273a21820aab0de5a462dbe99b804088efa9"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
X1_FREEZE = "17058d117f4f57c0b5a8e13e9046264499fbce62"

PRIOR_FROZEN = 3010
SOURCE_SEALED_NEGATIVES = 19006
SOURCE_EXTERNAL_NEGATIVES = 5
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 125
SOURCE_EXACT_GATES = 124
SOURCE_SEALED_METHODS = 5280
SOURCE_EXTERNAL_METHODS = 5
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic upholstered-furniture conservation intake, frame and layer "
    "topology, condition and intervention lineage, accessibility, workload control, "
    "correction readback, and shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_owners_custodians_conservators_upholsterers_workers_participants_communities_affected_parties_and_authorities",
    "real_furniture_textiles_fillings_fasteners_springs_webbing_finishes_tools_chemicals_measurements_images_records_or_identifiers",
    "real_handling_sampling_disassembly_cleaning_treatment_repair_reupholstery_testing_release_or_disposal",
    "professional_conservation_upholstery_fire_safety_chemical_safety_heritage_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_heritage_ownership_remedy_language_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [
    "V6594-P004", "V6594-P010", "V6594-P012", "V6594-P013", "V6594-P014",
    "V6594-P018", "V6594-P021", "V6594-P022", "V6594-P026", "V6594-P028",
    "V6594-P029", "V6594-P030", "V6594-P031", "V6594-P032", "V6594-P033",
    "V6594-P034", "V6594-P036", "V6594-P037", "V6594-P039", "V6594-P040",
]

NEW_PROPOSAL_SPECS = [
    {
        "slug": "upholstery-intake-custody-passport",
        "title": "Synthetic upholstered-furniture conservation intake with object alias, component inventory, condition-note provenance, custody event, and work-start hold",
        "outcome": "completed",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic object and package aliases, minimal component inventory, condition-note source, custody transition, scope acknowledgement, and work-start refusal",
        "sources": ["CCI-FURNITURE", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "frame-joint-topology-quarantine",
        "title": "Upholstered-furniture frame, rail, stile, leg, brace, block, and joint topology with contradictory-parent quarantine and repair abstention",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional frame nodes, typed attachment edges, contradictory parents, orphan quarantine, uncertainty flags, and physical-repair refusal",
        "sources": ["CCI-FURNITURE", "W3C-PROV"],
    },
    {
        "slug": "upholstery-layer-stack-map",
        "title": "Upholstery cover, interliner, batting, filling, decking, webbing, spring, and frame layer-stack map with concealed-layer uncertainty",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic ordered layer nodes, adjacency and containment relations, visibility states, concealed-layer uncertainty, conflict quarantine, and no opening instruction",
        "sources": ["CCI-FURNITURE", "CPSC-1640", "W3C-PROV"],
    },
    {
        "slug": "visible-condition-observation-ledger",
        "title": "Upholstery tear, abrasion, distortion, staining, fading, loss, corrosion, and residue observation ledger with diagnosis and treatment abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "bounded fictional observation vocabulary, declared region and viewpoint, lighting pin, uncertainty note, correction lineage, and diagnosis or treatment refusal",
        "sources": ["CCI-FURNITURE", "W3C-PROV"],
    },
    {
        "slug": "textile-weave-pattern-provenance",
        "title": "Upholstery textile warp, weft, pile, repeat, seam, trim, orientation, and replacement-claim provenance with fibre-identification refusal",
        "outcome": "completed",
        "pillar": "GMUT Mind and Freed ID",
        "mechanism": "synthetic textile-region labels, directional weave and pattern assertions, source and revision lineage, conflict state, and material-identification abstention",
        "sources": ["CCI-TEXTILES", "W3C-PROV"],
    },
    {
        "slug": "fastener-evidence-graph",
        "title": "Upholstery tack, nail, staple, screw, clip, dowel, adhesive, and stitch evidence graph with removal-sequence and authenticity refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional fastener aliases, attachment locations, visible-state assertions, sequence unknowns, competing provenance claims, and no removal or authenticity conclusion",
        "sources": ["CCI-FURNITURE", "W3C-PROV"],
    },
    {
        "slug": "webbing-spring-lashing-state",
        "title": "Upholstery webbing, spring, lashing, edge-roll, tension, attachment, and support-state graph with load-test abstention",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic support components, typed connections, qualitative state labels, uncertainty and conflict flags, zero measured loads, and no actuation or load test",
        "sources": ["CCI-FURNITURE", "NIST-UNCERTAINTY", "W3C-PROV"],
    },
    {
        "slug": "fill-material-compatibility-hold",
        "title": "Upholstery hair, fibre, feather, foam, batting, barrier, and unknown-fill declaration with sampling, chemical, and fire-safety holds",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional material declarations, unknown and contested state, source and age placeholders, compatibility challenge, sampling refusal, and competent safety referral",
        "sources": ["CCI-FURNITURE", "CPSC-1640", "W3C-PROV"],
    },
    {
        "slug": "dimension-uncertainty-envelope",
        "title": "Upholstered-furniture dimension, coordinate frame, measurand, unit, resolution, uncertainty, and zero-real-measurement envelope",
        "outcome": "completed",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic dimensions, declared SI units, reference-frame and measurand placeholders, uncertainty fields, zero measured rows, and geometric-conformance abstention",
        "sources": ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"],
    },
    {
        "slug": "condition-image-viewpoint-lineage",
        "title": "Upholstery condition-image viewpoint, illumination, scale-cue, crop, derivative, rights, redaction, and diagnosis-refusal lineage",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic image aliases, viewpoint and lighting labels, scale-cue placeholder, derivative and redaction events, rights reservation, and diagnosis refusal",
        "sources": ["W3C-PROV", "WCAG22", "NZ-PRIVACY"],
    },
    {
        "slug": "intervention-correction-lineage",
        "title": "Upholstery intervention proposal, approval placeholder, deviation, correction, supersession, readback, and release-hold lineage",
        "outcome": "completed",
        "pillar": "Freed ID, THOS Body, and CBR Heart",
        "mechanism": "synthetic intervention and approval placeholders, deviation events, correction candidate, supersession edge, dual readback, and no physical execution or release",
        "sources": ["CCI-FURNITURE", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "component-removal-reassembly-hold",
        "title": "Upholstery component-removal position, orientation, container, sequence, dependency, reassembly, and loss-prevention docket with destructive-action refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional component and container aliases, position and orientation declarations, dependency graph, sequence conflicts, reconciliation hold, and no removal or reassembly action",
        "sources": ["CCI-FURNITURE", "W3C-PROV"],
    },
    {
        "slug": "cleaning-contact-medium-reservation",
        "title": "Upholstery vacuum, screen, brush, solvent, aqueous medium, dwell, contact, extraction, waste, and hazard reservation with use refusal",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic tool and medium declarations, contact and dwell placeholders, unknown-material conflict, hazard and waste route reservation, and no cleaning instruction",
        "sources": ["CCI-FURNITURE", "CCI-TEXTILES", "W3C-PROV"],
    },
    {
        "slug": "canonical-upholstery-package",
        "title": "Canonical upholstery condition-and-intervention package with ordered asset digests, profile version, collision refusal, and noncredential declaration",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "synthetic asset index, deterministic JSON profile, ordered digests, profile-version lineage, collision challenge, and no key, proof, credential, signature, or production claim",
        "sources": ["IETF-JCS", "W3C-PROV"],
    },
    {
        "slug": "gmut-upholstery-contact-network-proxy",
        "title": "Represented GMUT upholstery contact-network, layer tensor, spring graph, stiffness, dissipation, boundary, and uncertainty board with zero measurements",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic scalar, tensor, network, constitutive, unit, domain, and uncertainty obligations, zero measurement rows, and physical-inference firewall",
        "sources": ["NIST-SI", "NIST-UNCERTAINTY"],
    },
    {
        "slug": "thos-upholstery-study-protocol",
        "title": "Represented THOS upholstery-record workflow comparison with blind matched-budget arms, governed participants and operators, safety monitoring, statistics, and zero enrolment",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "future-study protocol placeholders, blind matched-budget requirements, governance, safety monitoring, analysis plan, zero participants or operators, and no effectiveness claim",
        "sources": ["CCI-FURNITURE", "W3C-PROV"],
    },
    {
        "slug": "nonproduction-upholstery-lineage-query",
        "title": "Represented Freed ID upholstery custody, component, condition, image, proposal, intervention, correction, and package lineage query with disclosure ceiling",
        "outcome": "represented",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic provenance nodes and predecessor edges, hop budget, purpose and disclosure stops, deterministic digest, and no live identifier, key, proof, or credential",
        "sources": ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"],
    },
    {
        "slug": "accessible-upholstery-report-proxy",
        "title": "Represented accessible upholstery condition report with headings, table associations, noncolour status, text alternatives, focus order, and manual-review reservation",
        "outcome": "represented",
        "pillar": "CBR Heart and THOS Body",
        "mechanism": "structured synthetic report, headings and table relationships, noncolour state, alternative text, focus-order declaration, static fallback, and no accessibility-complete claim",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "real-upholstery-evidence-gap",
        "title": "Open gap for real upholstered objects, owners, custodians, conservators, upholsterers, materials, measurements, interventions, participants, outcomes, and independent review",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero real-object, person, material, measurement, treatment, safety-test, participant, operator, service, or outcome rows and absent professional and independent review",
        "sources": ["CCI-FURNITURE", "CPSC-1640", "NIST-UNCERTAINTY"],
    },
    {
        "slug": "upholstery-authority-ratification-gate",
        "title": "Exact decision-rights gate for upholstery ownership, custody, treatment, fire and chemical safety, privacy, accessibility, heritage, remedy, legal and cultural interpretation, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "ownership, custody, treatment, fire and chemical safety, privacy, accessibility, heritage, remedy, legal, cultural, collective-governance, affected-party, and Māori-authority reservations",
        "sources": ["CCI-FURNITURE", "CPSC-1640", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]

SELF_SAFE_CATEGORIES = [
    "Caelen source-head and live equality", "activation packet and overlay digests", "proposal-chain exact parse",
    "twenty inherited revalidation selections", "twenty-title novelty screen", "new-outcome distribution",
    "workflow-plan policy", "identity and authority boundary", "fifteen-main-task roster arithmetic",
    "Tavian standby state", "D-first drive posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene",
    "x1 manifest replay", "selected-row no-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound",
    "document-word ceiling", "portfolio arithmetic", "skill-plan arithmetic", "runner-plan arithmetic",
    "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6595-SAFE-{i:03d}", "title": f"Validate {name} inside the Orin-owned v659-v5 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6595-LIORA-SAFE-{i:03d}", "title": f"Liora may independently evaluate {name} in the Liora-owned v659-v6 lane", "owner": "Liora Venn", "state": "recommendation_only_not_executed_or_credited_by_orin"}
    for i, name in enumerate([
        "exact source baton digest", "owned-lane four-way equality", "inherited-selection no-credit",
        "new-proposal append-only chain", "synthetic fixture boundary", "five-class privacy exclusions",
        "commit-local manifest replay", "Method Flow failed-witness retention", "truth-label distribution",
        "authority-reservation completeness", "canonical-pass replay guard", "route-number arithmetic",
        "exact-title route uniqueness", "immediate bounded reread", "D-first storage posture",
        "document and file ceilings", "family-current caller compatibility", "manual accessibility reservation",
        "same-owner evidence labelling", "terminal NOT_READY preservation",
    ], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "upholstery intake and custody boundary", "frame and layer topology quarantine",
    "condition observation and image lineage", "fastener and removal-sequence hold",
    "webbing, spring, and support-state graph", "material compatibility and safety reservation",
    "dimension and uncertainty envelope", "intervention correction and supersession lineage",
    "GMUT contact-network firewall", "upholstery authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6595-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6595-LIORA-CAND-{i:03d}", "title": f"Liora may prototype reversible {name}", "owner": "Liora Venn", "state": "recommendation_only_not_executed_or_credited_by_orin"}
    for i, name in enumerate([
        "baton and overlay verifier", "source ancestry tribunal", "selected-row no-credit classifier",
        "new-row semantic-neighbour screen", "bounded privacy adjudicator", "manifest object batch reader",
        "stale-route-number classifier", "same-owner evidence labeler", "canonical-pass replay guard",
        "exact-title delivery preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6595-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use or treat real upholstered furniture, components, textiles, fillings, finishes, or records",
        "Make a real custody, handling, disassembly, cleaning, treatment, repair, reupholstery, release, or disposal decision",
        "Perform a fire, chemical, load, structural, environmental, or occupational-safety test or determination",
        "Publish an authenticity, provenance, ownership, value, heritage, or conservation conclusion",
        "Make a professional conservation, upholstery, engineering, fire-safety, privacy, or accessibility determination",
        "Publish personal, sensitive, culturally protected, or collective information",
        "Allocate legal, cultural, property, access, naming, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, or Māori-authority decision",
        "Deploy a production identity, credential, repository, or service system",
        "Perform destructive cleanup or mutation outside the exact Orin-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6595-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, or authority from task language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, or gates",
        "Publish credentials, private routes, raw task identifiers, private paths, transcripts, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-upholstery-intake-boundary", "Preserve synthetic object intake, custody, scope, component inventory, and work-start holds."),
    ("ghc-family-upholstery-layer-map", "Map synthetic cover, interliner, filling, support, and frame layers while quarantining contradictory relations."),
    ("ghc-family-upholstery-fastener-hold", "Track fastener evidence and sequence uncertainty without removal, authenticity, or treatment authority."),
    ("ghc-family-upholstery-support-state", "Represent webbing, springs, lashing, and support states with zero-load and actuation firewalls."),
    ("ghc-family-upholstery-material-reservation", "Fail closed around unknown fill, compatibility, sampling, chemical, and fire-safety decisions."),
    ("ghc-family-upholstery-intervention-lineage", "Track proposal, approval placeholder, deviation, correction, supersession, readback, and release holds."),
    ("ghc-family-upholstery-accessibility-report", "Expose structured condition reports while reserving manual, assistive-technology, and affected-user review."),
    ("ghc-family-upholstery-workload-handover", "Bound unresolved work, workload, correction readback, escalation, and shift handover."),
    ("ghc-family-gmut-upholstery-firewall", "Keep contact-network and constitutive proxies typed, dimensioned, zero-row, and physically nonconfirmatory."),
    ("ghc-family-upholstery-authority-gate", "Reserve ownership, treatment, safety, heritage, remedy, legal, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-liora-{slug}", "owner": "Liora Venn", "state": "recommendation_only_not_built_or_installed_by_orin"}
    for slug in [
        "baton-overlay-verifier", "source-ancestry-guard", "inherited-selection-no-credit",
        "proposal-novelty-screen", "privacy-adjudicator", "manifest-batch-replay",
        "route-number-normalizer", "canonical-pass-replay-guard", "same-owner-truth-labeler",
        "exact-title-delivery-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_upholstery_intake_boundary.py", "upholstery-intake-custody-passport"),
    ("ghc_family_upholstery_layer_map.py", "upholstery-layer-stack-map"),
    ("ghc_family_upholstery_fastener_hold.py", "fastener-evidence-graph"),
    ("ghc_family_upholstery_support_state.py", "webbing-spring-lashing-state"),
    ("ghc_family_upholstery_material_reservation.py", "fill-material-compatibility-hold"),
    ("ghc_family_upholstery_intervention_lineage.py", "intervention-correction-lineage"),
    ("ghc_family_upholstery_accessibility_report.py", "accessible-upholstery-report-proxy"),
    ("ghc_family_upholstery_workload_handover.py", "component-removal-reassembly-hold"),
    ("ghc_family_gmut_upholstery_firewall.py", "gmut-upholstery-contact-network-proxy"),
    ("ghc_family_upholstery_authority_gate.py", "upholstery-authority-ratification-gate"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_liora_{slug}.py", "owner": "Liora Venn", "state": "recommendation_only_not_built_or_run_by_orin"}
    for slug in ["baton_overlay_verifier", "proposal_novelty_screen", "privacy_adjudicator", "manifest_batch_replay", "exact_title_delivery_preflight"]
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory", "family-current name preference", "compatibility wrapper retention", "caller evidence",
    "trigger collision review", "stale owner label review", "stale phase label review", "stale route number review",
    "absolute-path privacy review", "raw identifier privacy review", "credential-pattern review", "transcript-pattern review",
    "duplicate proposal review", "duplicate task review", "duplicate skill review", "duplicate runner review",
    "JSON canonical formatting", "Markdown heading order", "source-label consistency", "truth-label consistency",
    "rollback coverage", "protected-gate coverage", "failure-credit consistency", "same-owner labelling",
    "manifest exclusions", "file-cap posture", "document-cap posture", "commit-cap posture",
    "D-first storage posture", "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6595-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6595-LIORA-CLEAN-{i:03d}", "title": f"Liora may independently review and refine {name}", "owner": "Liora Venn", "state": "recommendation_only_not_executed_or_credited_by_orin"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-FURNITURE", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/furniture-wooden-objects-basketry.html", "Furniture, upholstery, handling, storage, deterioration, and preventive-care vocabulary only; no diagnosis, treatment, professional competence, or conservation-conformance claim."),
    ("CCI-TEXTILES", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/textiles-costumes.html", "Textile structure and care vocabulary only; no fibre identification, sampling, cleaning, treatment, or professional claim."),
    ("CPSC-1640", "official_us_consumer_product_safety_commission", "https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/Flammable-Fabrics-Act", "Current upholstered-furniture flammability and component vocabulary only; no test, certification, compliance, legal, or safety determination."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si-2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real measurement result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured furniture or material result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, and qualified provenance vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current WCAG 2.2 structure and interaction vocabulary with manual, assistive-technology, and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal or compliance conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, or cultural interpretation claim."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]

STARTUP_FAILURES = [
    {
        "negative_id": "V6595-X1-N001",
        "signature": "powershell-five-one-lacked-sha256-hashdata-and-convert-tohexstring",
        "recovery": "Retain the unavailable API assumption, use Get-FileHash or SHA256.Create with explicit lowercase formatting, and verify the overlay digest without mutating it.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N002",
        "signature": "broad-drive-wide-overlay-search-exceeded-its-bounded-window-without-output",
        "recovery": "Stop only the exact attributable search process, retain the timeout, and use the literal sanitized handoff-bank segment named by the live baton.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N003",
        "signature": "unified-exec-process-interrupt-was-unsupported-for-the-running-search",
        "recovery": "Retain the unsupported interrupt, resolve the exact rg command line and PID read-only, then stop only that attributable search process.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N004",
        "signature": "powershell-word-count-domain-reported-21552-words-versus-the-baton-pointer-21412",
        "recovery": "Preserve both counts with their measurement domains, rely on exact file identity and SHA-256 rather than an unstated tokenizer, and make no content-integrity claim from word count alone.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N005",
        "signature": "direct-foreach-output-pipeline-triggered-powershell-empty-pipe-element-parser-failure",
        "recovery": "Retain the parser fault and materialize foreach rows into a scalar array before projection or JSON serialization.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N006",
        "signature": "source-evidence-manifest-was-incorrectly-assumed-to-cover-the-complete-x1-to-evidence-diff",
        "recovery": "Credit exact parity only for the 288 declared entries, retain the coverage failure, and use the exact owner and final-delta contracts for their separately declared coverage domains.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N007",
        "signature": "git-worktree-wrapper-returned-before-the-original-checkout-process-tree-reached-terminal-state",
        "recovery": "Do not rerun, reset, or interrupt checkout; follow the exact original Git process tree to terminal state, then prove exact head, branch, tracked cleanliness, and zero untracked paths.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N008",
        "signature": "four-query-official-source-search-exceeded-the-model-output-context-and-was-truncated",
        "recovery": "Retain the truncated result at zero credit and use narrow one-domain primary or official searches with short responses and exact source URLs.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N009",
        "signature": "direct-follow-up-open-of-the-cpsc-upholstered-furniture-page-returned-an-internal-403-fetch-failure",
        "recovery": "Retain the fetch failure and use the official CPSC Flammable Fabrics Act and business-guidance search result without treating a citation as a compliance determination.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N010",
        "signature": "windows-ripgrep-rejected-literal-wildcard-paths-during-template-reference-review",
        "recovery": "Retain the Windows path failure and search literal roots with explicit -g filename filters rather than wildcard path arguments.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N011",
        "signature": "first-process-tree-status-projection-returned-no-attributable-scalar-output",
        "recovery": "Retain the blank projection and use a no-profile exact-PID probe with an explicit terminal-state string.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N012",
        "signature": "first-tracked-cleanliness-wrapper-yielded-a-session-before-git-status-completed",
        "recovery": "Follow the one original unified session without launching a duplicate; accept cleanliness only after that exact process exits zero with no porcelain rows.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N013",
        "signature": "first-untracked-cleanliness-wrapper-yielded-a-session-before-ls-files-completed",
        "recovery": "Follow the exact original session to terminal state and require an explicit zero untracked count before mutation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X1-N014",
        "signature": "inherited-v659-v4-template-referenced-an-undefined-prefilled-failure-variable",
        "recovery": "Retain the latent template assumption and define an explicit ignored-template-failure list that receives no Orin failure, method, or completion credit.",
        "recovery_passed": True,
    },
]

PREFILLED_X1_X2_FAILURES_IGNORED = [*TEMPLATE_X2_FAILURES]
X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6595-X2-N001",
        "signature": "post-x1-full-status-reported-a-stat-only-inherited-receipt-modification-after-byte-exact-restoration",
        "recovery": "Retain the stat-cache fault, compare the working clean-filter blob with the exact HEAD blob, require equality and an empty diff, then refresh only that exact path before any x2 mutation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N002",
        "signature": "exact-path-update-index-really-refresh-returned-needs-update-despite-proven-clean-filter-blob-equality",
        "recovery": "Retain the refresh warning at zero credit, make no content change, and require both exact-path and complete-worktree porcelain to return empty before x2 starts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N003",
        "signature": "combined-x2-builder-content-and-hardcoded-term-inspection-exceeded-the-model-context-and-was-truncated",
        "recovery": "Retain the oversized inspection at zero credit, split inspection into bounded line windows and targeted literal searches, and patch only after each inherited assumption is attributable.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N004",
        "signature": "first-skill-validation-pass-rejected-all-ten-initialized-packages-because-skill-creator-metadata-omitted-the-default-prompt",
        "recovery": "Retain the 0-of-10 validation at zero credit, add an explicit default_prompt that names each exact skill while preserving the generated display metadata, then rerun the validator only against the changed packages.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N005",
        "signature": "parallel-reflection-remaster-invocation-produced-no-output-directory-or-attributable-receipt",
        "recovery": "Retain the missing reflection surface at zero credit, isolate the exact current runner with one bounded focus value, require an explicit zero exit and the complete four-file receipt set before continuing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N006",
        "signature": "method-flow-summarizer-emitted-the-complete-preferred-method-list-and-truncated-the-tool-output-after-writing-valid-artifacts",
        "recovery": "Retain the oversized stdout at zero credit, use the written UTF-8 summary artifacts as the evidence surface, suppress repetitive stdout on the changed-ledger rerun, and project only bounded count and validity fields.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N007",
        "signature": "first-scoped-x2-suite-passed-twenty-checks-but-failed-the-three-page-overview-floor-at-899-words",
        "recovery": "Retain the 20-of-21 scoped run at zero credit, add substantive source-use, workload, selected-revalidation, and falsification sections to the overview, regenerate dependent receipts, and rerun only the changed scoped x2 suite.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N008",
        "signature": "first-219-path-evidence-staging-emitted-one-line-ending-warning-per-path-and-truncated-the-wrapper-output-after-staging-succeeded",
        "recovery": "Retain the warning flood at zero credit, preserve the same Git clean conversion, suppress only safe-CRLF advisory output with core.safecrlf=false for the changed staging pass, and require exact staged Git-blob manifest parity before credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N009",
        "signature": "post-warning-ledger-regeneration-wrapper-output-was-lost-when-the-tool-result-exceeded-the-active-context-budget",
        "recovery": "Retain the lost wrapper output at zero credit, do not rerun credited work, and inspect the completed child exit plus exact bounded on-disk receipts before continuing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N010",
        "signature": "combined-status-and-method-flow-projection-repeated-line-ending-warning-noise-and-expanded-the-entire-preferred-method-ledger-until-output-truncated",
        "recovery": "Retain the recurrence at zero credit, set command-local core.safecrlf=false for read-only diff probes, select only scalar Method Flow counts, and keep every later diagnostic below its explicit output budget.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N011",
        "signature": "broad-repository-method-flow-command-search-returned-an-oversized-truncated-result-before-the-current-phase-command-was-isolated",
        "recovery": "Retain the broad-search fault at zero credit, limit searches to the exact v659-v5 scripts or declared runner filenames, and inspect only bounded matching lines.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N012",
        "signature": "first-exact-x2-staged-review-stopped-on-two-unadjudicated-transcript-or-session-privacy-candidates",
        "recovery": "Retain the failed tribunal at zero credit, rewrite boundary prose without prohibited literal terms, classify only the exact reviewed scanner function and literal pattern as a scanner definition, then regenerate and rerun the unchanged-scope staged tribunal.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6595-X2-N013",
        "signature": "first-privacy-recovery-would-have-modified-the-frozen-x1-generic-staged-reviewer-and-was-stopped-by-the-unstaged-surface-check",
        "recovery": "Retain the stopped lifecycle violation at zero credit, restore the reviewer exactly to the x1 Git blob, and remove the self-trigger from the new x2 runtime's equivalent split-literal regex construction instead.",
        "recovery_passed": True,
    },
]

STARTUP_FAILURES.append(
    {
        "negative_id": "V6595-X1-N015",
        "signature": "first-workflow-plan-refinement-audit-rejected-all-fifteen-endpoint-rows-without-route-controllers",
        "recovery": "Retain the 15-issue zero-credit audit, add each public relational predecessor as route_controller without changing seat order or phase arithmetic, regenerate the request, and require a 20-of-20 zero-issue pass.",
        "recovery_passed": True,
    }
)

STARTUP_FAILURES.extend(
    [
        {
            "negative_id": "V6595-X1-N018",
            "signature": "first-generic-exact-staged-review-classified-root-only-capacity-probes-as-private-path-candidates",
            "recovery": "Retain the failed staged review, classify only complete shutil.disk_usage drive-root literals as visible root-capacity probe candidates, keep all other absolute-path matches fail-closed, and rerun the exact unchanged staged surface.",
            "recovery_passed": True,
        },
        {
            "negative_id": "V6595-X1-N019",
            "signature": "quote-heavy-inline-python-root-literal-test-failed-in-the-powershell-parser-before-python-ran",
            "recovery": "Retain the parser fault and encode the bounded root-literal adjudication directly in the reviewed runner through apply_patch instead of a nested quote-bearing command.",
            "recovery_passed": True,
        },
    ]
)

STARTUP_FAILURES.append(
    {
        "negative_id": "V6595-X1-N017",
        "signature": "hardcoded-caelen-evidence-reviewer-ignored-help-and-rewrote-an-inherited-receipt-in-the-orin-worktree",
        "recovery": "Retain the command-assumption and inherited-path mutation at zero credit, inspect the exact diff, restore only that receipt byte-for-byte through an explicit patch, prove zero remaining inherited-path diff, and do not reuse hardcoded phase reviewers for Orin.",
        "recovery_passed": True,
    }
)

STARTUP_FAILURES.append(
    {
        "negative_id": "V6595-X1-N016",
        "signature": "mechanical-template-preparation-created-five-untracked-x2-and-closeout-files-before-the-x1-freeze",
        "recovery": "Retain the separation fault, remove only the five exact newly created Orin-owned untracked copies while preserving their immutable Caelen templates, and materialize them again only after x1 is committed, pushed, clean, and four-way equal.",
        "recovery_passed": True,
    }
)
