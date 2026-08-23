#!/usr/bin/env python3
"""Build and validate the planning-only Elaren Kestrel v667-v7 x1 freeze.

The builder reuses Eiren's immutable corpus reader but owns every emitted
Elaren artifact. It performs no x2 implementation, package installation,
real-world action, observed outcome, or successor contact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v7"
OWNER = "Elaren Kestrel"
OWNER_SLUG = "elaren-kestrel"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
REL_PHASE_ROOT = f"docs/{OWNER_SLUG}/{PHASE}"
NOW = "2026-08-23T19:27:05.507Z"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v667-v6-r2-full-tools"
SOURCE_PARENT_SHA = "1a754e02bfc705d738285c4a6cf9ce1c948a8580"
SOURCE_X1_SHA = "0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2"
SOURCE_EVIDENCE_SHA = "942eda86e745da93ece372d89870e052361b039c"
SOURCE_SHA = "dc8d91294b7656ad5e9961bba93ff759af20846c"
SOURCE_PHASE_ROOT = "docs/eiren-kestrel/v667-v6-r2"
SOURCE_CANONICAL_SHA256 = "b22dc8e929e604066e6a6514447bd3b54a70850058d6e14c31cd81506398d8a1"

INHERITED_PROPOSAL_COUNT = 4490
SELECTED_INHERITED_COUNT = 20
NEW_PROPOSAL_COUNT = 20
NEW_FROZEN_TOTAL = 4510
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "THOS Body"
PRACTICE = "wholly synthetic bobbin-lace sample design and collection-documentation records"

BASE_PATH = ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_r2_x1.py"
_spec = importlib.util.spec_from_file_location("_ghc_eiren_v667_v6_r2_x1", BASE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load immutable Eiren x1 compatibility surface")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
for _name, _value in {
    "ROOT": ROOT, "PHASE": PHASE, "OWNER": OWNER, "OWNER_SLUG": OWNER_SLUG,
    "PHASE_ROOT": PHASE_ROOT, "REL_PHASE_ROOT": REL_PHASE_ROOT, "NOW": NOW,
    "SOURCE_BRANCH": SOURCE_BRANCH, "SOURCE_PARENT_SHA": SOURCE_PARENT_SHA,
    "SOURCE_X1_SHA": SOURCE_X1_SHA, "SOURCE_EVIDENCE_SHA": SOURCE_EVIDENCE_SHA,
    "SOURCE_SHA": SOURCE_SHA, "SOURCE_PHASE_ROOT": SOURCE_PHASE_ROOT,
    "INHERITED_PROPOSAL_COUNT": INHERITED_PROPOSAL_COUNT,
}.items():
    setattr(base, _name, _value)

run_git = base.run_git
git_json = base.git_json
canonical_sha256 = base.canonical_sha256
similarity = base.similarity
MANDATORY_SKILLS = list(base.MANDATORY_SKILLS)
MUTATION_CLASSES = list(base.MUTATION_CLASSES)

REJECTED_STAINED_GLASS_PROTECTED_GATES = [
    "real glazier, conservator, surveyor, architect, engineer, scaffold worker, owner, custodian, worshipper, visitor, affected party, regulator, heritage body, cultural authority, or Māori authority",
    "real window, panel, light, pane, lead came, copper foil, tie bar, saddle bar, ferramenta, glazing, glass, paint, enamel, stain, putty, mortar, sealant, fragment, frame, opening, building, place, image, measurement, sample, or record",
    "real access, work at height, dismantling, handling, cleaning, cutting, soldering, heating, leading, cementing, glazing, repair, alteration, storage, transport, installation, release, disposal, or safety decision",
    "professional conservation, glazing, structural, exposure, lead, chemical, fire, building-control, heritage, accessibility, privacy, environmental, or workplace authority",
    "real likelihood, parameter constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon",
    "real participant or operator arm, safety monitoring, operational outcome, appropriate statistics, AGI, ASI, consciousness, personhood, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, recovery event, trust governance, or production credential",
    "credential, account, token, secret, login, external write, publication, deployment, purchase, production release, or sibling-lane mutation",
    "system-wide or elevated install, Windows feature change, Codex desktop update, host-security weakening, Sandbox or Hyper-V activation, reboot, destructive cleanup, or unreviewed lifecycle-script execution",
    "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, independent-reproduction, production-readiness, fitness-for-service, or deployment-readiness claim",
    "ownership, custody, access, attribution, intellectual-property, sacred or customary association, significance, legal or cultural interpretation, remedy, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into certification, competence, safety, legality, cultural legitimacy, or authority",
]

REJECTED_STAINED_GLASS_SOURCE_PROFILES: list[dict[str, str]] = [
    {"source_id": "S01", "name": "Historic England stained-glass conservation guidance", "url": "https://historicengland.org.uk/advice/caring-for-heritage/places-of-worship/looking-after-places-of-worship/stained-glass/", "status": "official heritage guidance reviewed read-only", "bounded_use": "panel, glazing, condition, significance, survey, maintenance, and conservation-reservation vocabulary only; no diagnosis, specification, consent, intervention, or legal conclusion"},
    {"source_id": "S02", "name": "Historic England stained-glass survey flowchart", "url": "https://historicengland.org.uk/images-books/publications/stained-glass-condition-survey-flowchart/", "status": "official heritage workflow surface reviewed read-only", "bounded_use": "survey-stage, escalation, record, and specialist-review vocabulary only; no real survey, risk decision, or professional authority"},
    {"source_id": "S03", "name": "US National Park Service Preservation Brief 33", "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-33-stained-leaded-glass.pdf", "status": "official preservation brief reviewed at the vocabulary boundary", "bounded_use": "stained and leaded glass component, deterioration, protective glazing, documentation, and referral vocabulary only; no treatment or design prescription"},
    {"source_id": "S04", "name": "Canadian Conservation Institute glass care guidance", "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/glass-ceramics.html", "status": "official conservation surface reviewed read-only", "bounded_use": "glass fragility, condition, storage, handling-reservation, and preventive-care vocabulary only; no object handling or conservation decision"},
    {"source_id": "S05", "name": "WorkSafe New Zealand workplace exposure standards", "url": "https://www.worksafe.govt.nz/topic-and-industry/monitoring/exposure-standards-and-biological-exposure-indices/", "status": "official current-review surface reserved for competent interpretation", "bounded_use": "exposure, monitoring, control, stop, and competent-person reservation vocabulary only; no exposure assessment or safety advice"},
    {"source_id": "S06", "name": "WorkSafe New Zealand lead guidance", "url": "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/guidance/substances/lead/", "status": "official lead-hazard surface reviewed read-only", "bounded_use": "lead hazard, exposure, hygiene, monitoring, and competent-review reservations only; no soldering, handling, remediation, or medical advice"},
    {"source_id": "S07", "name": "NIST International System of Units", "url": "https://www.nist.gov/pml/owm/si-units", "status": "official NIST surface reviewed read-only", "bounded_use": "quantity, unit, symbol, dimensional-consistency, and reporting vocabulary only; no real measurement or conformity claim"},
    {"source_id": "S08", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only", "bounded_use": "uncertainty-component and reporting vocabulary only; no calibrated apparatus or measured result"},
    {"source_id": "S09", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "entity, activity, revision, derivation, invalidation, and qualified-provenance vocabulary only"},
    {"source_id": "S10", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "headings, labels, noncolour cues, reading order, and manual-review reservations only; no complete accessibility claim"},
    {"source_id": "S11", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "evidence, validity, status, privacy, and nonproduction vocabulary only; zero real keys, proofs, credentials, or lifecycle calls"},
    {"source_id": "S12", "name": "New Zealand Privacy Commissioner privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "official privacy surface reviewed read-only", "bounded_use": "minimization, purpose, correction, access, disclosure, and remedy reservation vocabulary only; no legal or compliance conclusion"},
    {"source_id": "S13", "name": "New Zealand Privacy Principle 3A", "url": "https://www.privacy.org.nz/responsibilities/your-obligations/privacy-principle-3a/", "status": "official transparency surface reviewed read-only", "bounded_use": "indirect-collection notification and transparency reservation vocabulary only; no legal conclusion"},
    {"source_id": "S14", "name": "Te Mana Raraunga principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Māori data-sovereignty surface read only to the authority-reservation level", "bounded_use": "collective authority, control, context, consent, benefit, and guardianship reservations only; no Māori interpretation, ratification, governance, or authority claim"},
    {"source_id": "S15", "name": "interrogate project release", "url": "https://pypi.org/project/interrogate/1.7.0/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, classifiers, and docstring-coverage capability only"},
    {"source_id": "S16", "name": "import-linter project release", "url": "https://pypi.org/project/import-linter/2.13/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, BSD-2-Clause metadata, and import-contract capability only"},
    {"source_id": "S17", "name": "pyroma project release", "url": "https://pypi.org/project/pyroma/5.0.1/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, MIT metadata, and package-metadata rating capability only"},
    {"source_id": "S18", "name": "pip installation report and hash-checking documentation", "url": "https://pip.pypa.io/en/stable/reference/installation-report/", "status": "official pip documentation reserved for x2 installation evidence", "bounded_use": "machine-readable artifact URL and archive-hash evidence only; no supply-chain completeness"},
]
REJECTED_STAINED_GLASS_PROPOSAL_SPECS: list[tuple[str, str, list[str], str]] = [
    ("synthetic stained-glass panel identity capsule with opening alias, panel revision, light sequence, and no attribution authority", "A revisioned panel capsule keeps surrogate identity and location separate from attribution, ownership, custody, and authenticity.", ["S01", "S02", "S09"], "completed"),
    ("pane lead-came tie-bar and ferramenta topology graph with disconnected edges, vacancy markers, and no structural assessment", "Typed components and edges expose missing relations without declaring fit, stability, condition, or intervention.", ["S01", "S03", "S09"], "completed"),
    ("condition-phenomenon vocabulary ledger with observation and diagnosis separation, contradiction retention, and zero real observations", "Synthetic phenomena stay attributed observations while diagnosis, cause, severity, urgency, and treatment remain vacant.", ["S01", "S02", "S03", "S04"], "completed"),
    ("panel-grid and location-reference companion with surrogate coordinates, reading-order map, and measurement abstention", "A surrogate grid can reconcile component locations and accessible reading order without becoming a measured survey.", ["S02", "S07", "S08", "S10"], "completed"),
    ("glazing-layer and environmental-context separation register with zero rows, source bounds, and condensation-claim quarantine", "An empty environmental register distinguishes layers and source claims while refusing causal or performance conclusions.", ["S01", "S03", "S07", "S08"], "completed"),
    ("paint stain enamel and fired-decoration provenance board with technique uncertainty, revision edges, and no material authentication", "Decoration terms remain sourced hypotheses with uncertainty and correction rather than authenticated technique or date.", ["S01", "S03", "S09"], "completed"),
    ("survey-image and diagram derivative-lineage manifest with crop ancestry, disclosure mask, rights reservation, and no authorship claim", "Derivative lineage and disclosure masks can be checked without authenticating imagery, assigning authorship, or deciding rights.", ["S09", "S10", "S12", "S13"], "completed"),
    ("conservation-option decision trail with minimum-intervention placeholders, rejected alternatives, rollback, and zero authorization", "A synthetic options record preserves rationale and reversal while never selecting or authorizing treatment.", ["S01", "S03", "S09"], "completed"),
    ("detached-fragment containment and location ledger with discrepancy stops, zero items, and no handling or disposal direction", "A zero-item ledger can expose custody and discrepancy fields while issuing no handling, storage, release, or disposal action.", ["S04", "S06", "S09"], "completed"),
    ("bitemporal survey correction chain with assertion time, supersession, invalidation, readback, and no historical rewrite", "Correction events preserve both assertion and validity time while retaining contradicted synthetic records.", ["S09", "S12"], "completed"),
    ("environmental-protective-glazing option comparator with ventilation vacancies, uncertainty fields, and no design recommendation", "A comparator can expose missing assumptions and competing aims without choosing a system or predicting performance.", ["S01", "S03", "S07", "S08"], "completed"),
    ("panel pane and component count-reconciliation matrix with orphan detection, duplicate quarantine, and zero inventory claim", "Synthetic counts reconcile identifiers and isolate orphans without asserting a real inventory or completeness.", ["S02", "S09"], "completed"),
    ("dismantling and reassembly map representation with sequence dependencies, dominant stop states, and zero tool or work commands", "A no-action dependency map can reject unsafe promotion while providing no dismantling, soldering, glazing, or access instruction.", ["S03", "S05", "S06", "S09"], "completed"),
    ("archival handover and maintenance representation with custody vacancy, correction readback, access reserve, and no professional sign-off", "A handover representation exposes missing custody, review, and access fields without becoming a professional record or sign-off.", ["S01", "S09", "S10", "S12"], "completed"),
    ("THOS matched-queue panel-survey proxy with equal symbolic budget, stop precedence, blind labels, and zero participants", "A participant-free proxy represents queue and stop semantics without effectiveness, safety, staffing, or trial evidence.", ["S02", "S05", "S10"], "represented"),
    ("GMUT condensation and corrosion symbolic board with typed scalar-tensor placeholders, units, boundaries, and zero fitted coefficients", "A typed symbolic board checks declarations without likelihoods, coefficients, predictions, material laws, or empirical results.", ["S07", "S08"], "represented"),
    ("Freed ID zero-key panel-component provenance statement graph with purpose cap, correction, status tombstone, and no lifecycle calls", "A zero-key graph exposes lineage and status while every proof, issuer, resolver, credential, and trust decision stays absent.", ["S09", "S11", "S12"], "represented"),
    ("CBR accessibility privacy significance rights contestation and remedy empty-chair shell with zero sessions or decisions", "An unoccupied review shell names duties while providing no affected-user, legal, cultural, Māori-authority, or acceptance evidence.", ["S10", "S12", "S13", "S14"], "represented"),
    ("real stained-glass evidence escrow requiring governed survey records, authenticated materials, calibrated measurements, competent assessment, and independent review", "Absent real governed records, authenticated materials, calibrated measurements, competent practitioners, and independent assessment remain an explicit open gap.", ["S01", "S02", "S03", "S04", "S05", "S06"], "open_gap"),
    ("exact authority circuit for access work-at-height lead solder heat chemical conservation legal cultural rights and Māori decisions", "Every real safety, professional, legal, cultural, affected-party, and Māori decision remains an empty chair requiring exact evidence and authority.", ["S05", "S06", "S12", "S13", "S14"], "exact_gate"),
]

# The stained-glass slate above is retained as the rejected pre-freeze witness
# that produced EL6677-X1-N013.  These executable definitions replace it after
# direct inherited collisions were identified; the rejected rows earn no
# novelty, completion, or proposal-chain credit.
PROTECTED_GATES = [
    "real lacemaker, textile conservator, curator, registrar, collection manager, designer, teacher, learner, owner, custodian, donor, affected party, cultural authority, or Māori authority",
    "real lace, textile, bobbin, thread, fibre, pillow, bolster, pricking, pattern, pin, spool, winding, sample, fragment, collection object, image, measurement, accession record, provenance record, or rights record",
    "real making, crossing, twisting, pinning, winding, tensioning, cutting, washing, cleaning, handling, mounting, storage, display, accession, loan, acquisition, deaccession, transport, release, disposal, or conservation action",
    "professional lacemaking, textile conservation, collections management, fibre identification, ergonomics, accessibility, privacy, intellectual-property, legal, cultural, or workplace authority",
    "real likelihood, parameter constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon",
    "real participant or operator arm, safety monitoring, operational outcome, appropriate statistics, AGI, ASI, consciousness, personhood, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, recovery event, trust governance, or production credential",
    "credential, account, token, secret, login, external write, publication, deployment, purchase, production release, or sibling-lane mutation",
    "system-wide or elevated install, Windows feature change, Codex desktop update, host-security weakening, Sandbox or Hyper-V activation, reboot, destructive cleanup, or unreviewed lifecycle-script execution",
    "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, independent-reproduction, production-readiness, fitness-for-service, or deployment-readiness claim",
    "ownership, custody, access, attribution, copyright, design right, moral right, sacred or customary association, significance, legal or cultural interpretation, remedy, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into certification, competence, safety, legality, cultural legitimacy, or authority",
]

SOURCE_PROFILES = [
    {"source_id": "S01", "name": "Getty Art and Architecture Thesaurus bobbin-lace hierarchy", "url": "https://www.getty.edu/research/tools/vocabularies/aat_in_depth.pdf", "status": "official Getty vocabulary guidance reviewed read-only", "bounded_use": "bobbin-lace hierarchy, controlled-term, relationship, and source-attribution vocabulary only; no object attribution, technique authentication, conformance, or authority"},
    {"source_id": "S02", "name": "Victoria and Albert Museum research on adorned prints and bobbin lace", "url": "https://www.vam.ac.uk/content/journals/research-journal/issue-03/an-adorned-print-print-culture%2C-female-leisure-and-the-dissemination-of-fashion-in-france-and-england%2C-c.-1660-1779/", "status": "primary museum research surface reviewed read-only", "bounded_use": "museum-object, linen and metal bobbin-lace, uncertainty, comparison, date, and attribution-reservation vocabulary only; no authentication or cultural conclusion"},
    {"source_id": "S03", "name": "Canadian Conservation Institute textiles and costumes guidance", "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/textiles-costumes.html", "status": "official preventive-conservation surface reviewed read-only", "bounded_use": "textile structure, vulnerability, handling, storage, display, and professional-review reservations only; no real object care or treatment decision"},
    {"source_id": "S04", "name": "Canadian Conservation Institute Textiles and the Environment", "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/textiles-environment.html", "status": "official environmental guidance reviewed read-only", "bounded_use": "light, humidity, temperature, pollutant, pest, record, and risk-reservation vocabulary only; no real measurement or environmental prescription"},
    {"source_id": "S05", "name": "ICOM standards and guidelines", "url": "https://icom.museum/en/resources/standards-guidelines/", "status": "official museum-standards index reviewed read-only", "bounded_use": "documentation, acquisition, accessioning, provenance, custody, ethics, and professional-review reservations only; no ICOM conformance or museum authority"},
    {"source_id": "S06", "name": "ICOM Object ID", "url": "https://icom.museum/en/resources/standards-guidelines/objectid/", "status": "official cultural-object documentation surface reviewed read-only", "bounded_use": "type, materials-and-techniques, dimensions, inscriptions, features, title, subject, period, maker, photography, description, and secure-record vocabulary only; no inventory, ownership, or recovery claim"},
    {"source_id": "S07", "name": "NIST International System of Units", "url": "https://www.nist.gov/pml/owm/si-units", "status": "official NIST surface reviewed read-only", "bounded_use": "quantity, unit, symbol, dimensional-consistency, and reporting vocabulary only; no real measurement or conformity claim"},
    {"source_id": "S08", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only", "bounded_use": "uncertainty-component and reporting vocabulary only; no calibrated apparatus or measured result"},
    {"source_id": "S09", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "entity, activity, revision, derivation, invalidation, and qualified-provenance vocabulary only"},
    {"source_id": "S10", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "headings, labels, noncolour cues, reading order, and manual-review reservations only; no complete accessibility claim"},
    {"source_id": "S11", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "evidence, validity, status, privacy, and nonproduction vocabulary only; zero real keys, proofs, credentials, or lifecycle calls"},
    {"source_id": "S12", "name": "New Zealand Privacy Commissioner privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "official privacy surface reviewed read-only", "bounded_use": "minimization, purpose, correction, access, disclosure, and remedy reservation vocabulary only; no legal or compliance conclusion"},
    {"source_id": "S13", "name": "New Zealand Privacy Principle 3A", "url": "https://www.privacy.org.nz/responsibilities/your-obligations/privacy-principle-3a/", "status": "official transparency surface reviewed read-only", "bounded_use": "indirect-collection notification and transparency reservation vocabulary only; no legal conclusion"},
    {"source_id": "S14", "name": "Te Mana Raraunga principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Māori data-sovereignty surface read only to the authority-reservation level", "bounded_use": "collective authority, control, context, consent, benefit, and guardianship reservations only; no Māori interpretation, ratification, governance, or authority claim"},
    {"source_id": "S15", "name": "interrogate project release", "url": "https://pypi.org/project/interrogate/1.7.0/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, classifiers, and docstring-coverage capability only"},
    {"source_id": "S16", "name": "import-linter project release", "url": "https://pypi.org/project/import-linter/2.13/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, BSD-2-Clause metadata, and import-contract capability only"},
    {"source_id": "S17", "name": "pyroma project release", "url": "https://pypi.org/project/pyroma/5.0.1/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version, Python floor, wheel filename, SHA-256, MIT metadata, and package-metadata rating capability only"},
    {"source_id": "S18", "name": "pip installation report and hash-checking documentation", "url": "https://pip.pypa.io/en/stable/reference/installation-report/", "status": "official pip documentation reserved for x2 installation evidence", "bounded_use": "machine-readable artifact URL and archive-hash evidence only; no supply-chain completeness"},
]

PROPOSAL_SPECS = [
    ("synthetic bobbin-lace sample identity capsule with surrogate collection number, technique vacancy, revision, and no attribution authority", "A revisioned sample capsule keeps surrogate identity separate from technique authentication, attribution, ownership, custody, and significance.", ["S01", "S02", "S05", "S06", "S09"], "completed"),
    ("lacemaking pricking and pin-lattice topology with hole classes, edge zones, orphan quarantine, and no real pattern", "A surrogate pin lattice can expose missing or orphan relations without becoming a usable pricking or making instruction.", ["S01", "S02", "S09"], "completed"),
    ("bobbin-pair thread-lot and winding-lineage graph with synthetic tokens, source claims, and zero fibre authentication", "Synthetic pairs and thread lots preserve provenance and uncertainty without identifying fibre, material, origin, quality, or fitness.", ["S02", "S03", "S09"], "completed"),
    ("cross twist pin and close event grammar with dominant stop state, reversal edges, and zero lacemaking commands", "A formal event grammar can reject invalid transitions while issuing no executable sequence, teaching instruction, or craft action.", ["S01", "S02", "S09"], "completed"),
    ("ground tally picot plait and decorative-motif topology with unknown-state support and no technique diagnosis", "Typed motif relations keep uncertain structure visible without authenticating a lace tradition, region, date, maker, or technique.", ["S01", "S02", "S09"], "completed"),
    ("footside headside border corner and centre-field segmentation register with adjacency checks and zero object measurement", "A surrogate segmentation map can reconcile regions while every real dimension, orientation, and condition observation remains absent.", ["S01", "S06", "S07", "S08"], "completed"),
    ("working-diagram and pattern derivative-lineage manifest with mirror rotation scale abstention, disclosure mask, and rights reservation", "Derivative lineage and transformation labels can be checked without reproducing a protected pattern, assigning authorship, or deciding rights.", ["S09", "S10", "S12", "S13"], "completed"),
    ("lace fibre colour and metallic-thread claim quarantine with attributed vocabulary, contradiction retention, and no material identification", "Material and colour assertions remain attributed claims with corrections rather than authenticated composition or conservation evidence.", ["S02", "S03", "S09"], "completed"),
    ("thread tension pitch scale and density zero-row register with unit obligations, uncertainty vacancies, and no process prescription", "A zero-row quantity schema requires units and uncertainty while inventing no measurements or recommended making parameters.", ["S07", "S08"], "completed"),
    ("bitemporal sample condition and catalogue correction chain with assertion time, supersession, invalidation, and no historical rewrite", "Correction events preserve both assertion and validity time while retaining contradicted synthetic catalogue statements.", ["S03", "S05", "S09", "S12"], "completed"),
    ("detached lace fragment and sample-container ledger with location discrepancy stops, zero items, and no handling direction", "A zero-item ledger exposes custody and discrepancy fields while issuing no handling, storage, mounting, release, or disposal action.", ["S03", "S05", "S06", "S09"], "completed"),
    ("pattern unit repeat corner and border count-reconciliation matrix with duplicate quarantine and zero inventory claim", "Synthetic counts reconcile identifiers and repeated structures without asserting a real inventory, completeness, or authentic pattern repeat.", ["S01", "S06", "S09"], "completed"),
    ("pillow bobbin pin and thread-set dependency representation with setup vacancies, safe stop precedence, and zero physical action", "A no-action dependency graph can expose missing prerequisites without directing setup, manipulation, tension, cutting, or tool use.", ["S01", "S03", "S09"], "completed"),
    ("collection handover access and display-reservation packet with custody vacancy, correction readback, and no professional sign-off", "A handover representation exposes missing custody, access, and review fields without becoming a museum decision or professional record.", ["S03", "S04", "S05", "S06", "S10", "S12"], "completed"),
    ("THOS matched-queue lace-documentation proxy with equal symbolic budget, stop precedence, blind labels, and zero participants", "A participant-free proxy represents queue, workload, correction, and stop semantics without effectiveness, safety, staffing, or trial evidence.", ["S05", "S10"], "represented"),
    ("GMUT thread-network tension surrogate with typed scalar-tensor placeholders, boundary terms, units, and zero fitted coefficients", "A typed symbolic board checks declarations without likelihoods, coefficients, predictions, material laws, stability, or empirical results.", ["S07", "S08"], "represented"),
    ("Freed ID zero-key lace-sample provenance statement graph with purpose cap, correction, status tombstone, and no lifecycle calls", "A zero-key graph exposes lineage and status while every proof, issuer, resolver, credential, and trust decision remains absent.", ["S09", "S11", "S12"], "represented"),
    ("CBR accessibility privacy traditional-knowledge rights contestation and remedy empty-chair shell with zero sessions or decisions", "An unoccupied shell names duties while providing no affected-user, legal, cultural, Māori-authority, or acceptance evidence.", ["S10", "S12", "S13", "S14"], "represented"),
    ("real bobbin-lace evidence escrow requiring governed object records, authenticated materials, competent technique assessment, affected parties, and independent review", "Absent real governed records, authenticated materials, competent practitioners, affected parties, and independent assessment remain an explicit open gap.", ["S01", "S02", "S03", "S05", "S06"], "open_gap"),
    ("exact authority circuit for collection custody handling conservation attribution copyright traditional knowledge cultural and Māori decisions", "Every real professional, collections, legal, cultural, affected-party, traditional-knowledge, and Māori decision remains an empty chair requiring exact evidence and authority.", ["S03", "S05", "S06", "S12", "S13", "S14"], "exact_gate"),
]

STARTUP_FAILURES = [
    {"failure_id": "EL6677-X1-N001", "failure": "PowerShell direct foreach reference-inventory projection produced an empty-pipe-element ParserError", "credit": 0, "recovery": "used bounded scalar and array projections"},
    {"failure_id": "EL6677-X1-N002", "failure": "first large activation-baton window exceeded visible output capacity", "credit": 0, "recovery": "read complete baton through EOF in bounded windows and verified digest"},
    {"failure_id": "EL6677-X1-N003", "failure": "combined authorization and roster projection was truncated", "credit": 0, "recovery": "read required schemas and current records in bounded complete chunks"},
    {"failure_id": "EL6677-X1-N004", "failure": "combined ancestry projection had a missing-closing-parenthesis PowerShell parse error", "credit": 0, "recovery": "used separate literal scalar ancestry probes"},
    {"failure_id": "EL6677-X1-N005", "failure": "uniqueness wrapper crossed its yield boundary while Git enumerated worktrees", "credit": 0, "recovery": "inspected the live process and exact administrative state without duplicating the command"},
    {"failure_id": "EL6677-X1-N006", "failure": "canonical receipt scalar summary used an invalid inline PowerShell if expression", "credit": 0, "recovery": "assigned conditional values before constructing the summary object"},
    {"failure_id": "EL6677-X1-N007", "failure": "first family-index invocation omitted required phase and owner arguments", "credit": 0, "recovery": "reran only the refused no-write invocation with exact required arguments"},
    {"failure_id": "EL6677-X1-N008", "failure": "first broad tool-inventory projection exceeded bounded output", "credit": 0, "recovery": "used the generated phase-local family index and exact source ledgers"},
    {"failure_id": "EL6677-X1-N009", "failure": "first canonical-receipt projection guessed absent property names and produced nulls", "credit": 0, "recovery": "inspected exact schema properties before scalar projection"},
    {"failure_id": "EL6677-X1-N010", "failure": "first full-script transformation exceeded tool-result capacity and left the two-line placeholder unchanged", "credit": 0, "recovery": "inspected the filesystem before retry and changed to a compact compatibility builder"},
    {"failure_id": "EL6677-X1-N011", "failure": "apply_patch rejected delete and add operations targeting one path in one transaction", "credit": 0, "recovery": "split the unchanged operation into atomic delete and additive patches"},
    {"failure_id": "EL6677-X1-N012", "failure": "one compatibility-source mapping projection was visibly truncated", "credit": 0, "recovery": "used targeted definition windows and exact line ranges instead of trusting the truncated view"},
    {"failure_id": "EL6677-X1-N013", "failure": "first executable novelty gate rejected the stained-glass slate after thirty inherited domain rows were reconstructed", "credit": 0, "recovery": "rejected the entire slate before freeze and selected a semantically distinct domain after bounded corpus screening"},
    {"failure_id": "EL6677-X1-N014", "failure": "first isolated novelty diagnostic hit the Windows cp1252 console boundary while rendering Māori text", "credit": 0, "recovery": "reran only the failed read-only diagnostic with explicit UTF-8 output and bounded scalar fields"},
    {"failure_id": "EL6677-X1-N015", "failure": "first corrected x1 validation treated its own literal Unix user-directory privacy pattern as a private path value", "credit": 0, "recovery": "constructed sentinel path tokens from separate literals so the five-class scanner can inspect its own source without self-matching"},
]


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    return base.build_corpus()


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pillar_overrides = {15: "THOS Body", 16: "GMUT Mind", 17: "Freed ID", 18: "CBR Heart", 19: "All pillars", 20: "CBR Heart"}
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"EL6677-N{index:03d}"
        approval = {"completed": "safe_now_bounded", "represented": "candidate_bounded_representation", "open_gap": "open_gap_external_evidence_absent", "exact_gate": "exact_approval_required"}[expected]
        lane = {"completed": "owner_local_structural", "represented": "owner_local_representation_only", "open_gap": "disabled_real_evidence_adapter", "exact_gate": "unexecuted_authority_reservation"}[expected]
        base_path = f"{REL_PHASE_ROOT}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five preregistered invalid mutations without promoting software structure into empirical, participant, professional, operational, production, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, vacancy, stop, correction, uncertainty, provenance, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval,
            "execution_lane": lane,
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base_path}/contract.json",
            "concrete_artifacts": [f"{base_path}/contract.json", f"{base_path}/mutation-results.json", f"{base_path}/bounded-receipt.json"],
            "falsifier_or_acceptance_gate": "One bounded positive must satisfy every declared invariant; all five mutations must fail closed; protected gates stay unoccupied; and the final core label may not exceed the preregistered disposition.",
            "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain every failed witness at zero credit, add a recurrence guard, and issue no real-world, external, identity, participant, professional, legal, cultural, Māori-authority, safety, or production action.",
            "protected_gates": PROTECTED_GATES,
            "expected_disposition": expected,
            "distinctive_invariant": invariant,
            "primary_pillar": PRIMARY_PILLAR,
            "pillar": pillar_overrides.get(index, PRIMARY_PILLAR),
            "practice_lens": PRACTICE,
            "negative_fixture_count": 5,
            "preregistered_mutations": [{"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind} for i, kind in enumerate(MUTATION_CLASSES, 1)],
            "network_calls_planned": 0,
            "participant_count_planned": 0,
            "real_data_rows_planned": 0,
            "x1_status": "frozen_not_executed",
            "x2_implementation_count": 0,
            "outcomes_observed": False,
        })
    return rows


def selected_inherited_rows() -> list[dict[str, Any]]:
    freeze = git_json(SOURCE_X1_SHA, f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    rows = []
    for source in freeze["new_proposals"]:
        pid = str(source["proposal_id"])
        rows.append({
            "proposal_id": pid,
            "title": source["title"],
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "source_final": SOURCE_SHA,
            "source_disposition": source["expected_disposition"],
            "origin_and_credit": "selected_inherited_bounded_revalidation_no_elaren_credit",
            "append_to_novelty_chain": False,
            "elaren_novelty_credit": 0,
            "elaren_completion_credit": 0,
            "automatic_completion_credit": 0,
            "x1_status": "frozen_for_read_only_revalidation_not_executed",
            "outcomes_observed": False,
            "planned_receipt": f"{REL_PHASE_ROOT}/x2/selected-revalidation/{pid.casefold()}.json",
        })
    if len(rows) != SELECTED_INHERITED_COUNT:
        raise RuntimeError("selected inherited count drift")
    return rows


def build_novelty(corpus: list[dict[str, str]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    nearest: list[dict[str, Any]] = []
    exact: list[dict[str, str]] = []
    for proposal in proposals:
        collisions = [row for row in corpus if row["title"].casefold() == proposal["title"].casefold()]
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in collisions)
        score, inherited = max(((similarity(proposal["title"], row["title"]), row) for row in corpus), key=lambda item: item[0])
        nearest.append({
            "proposal_id": proposal["proposal_id"], "score": round(score, 6),
            "inherited_proposal_id": inherited["proposal_id"], "inherited_title": inherited["title"],
            "source_path": inherited["source_path"], "distinctive_invariant": proposal["distinctive_invariant"],
            "semantic_review": "distinct after manual comparison of practice mechanics, invariant, source boundary, artifacts, falsifier, rollback, and protected gates; lexical similarity is only a screen",
        })
    pairs = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= 0.70:
                pairs.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    domain_terms = ["bobbin lace", "bobbin-lace", "lacemaking", "torchon", "pillow lace"]
    domain_matches = [
        {"proposal_id": row["proposal_id"], "title": row["title"], "matched_terms": [term for term in domain_terms if term in row["title"].casefold()]}
        for row in corpus if any(term in row["title"].casefold() for term in domain_terms)
    ]
    groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicates = {pid: rows for pid, rows in sorted(groups.items()) if len(rows) > 1}
    maximum = max(row["score"] for row in nearest)
    return {
        "schema": "ghc-family-novelty-audit-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "corpus_construction": construction, "corpus_row_count": len(corpus), "corpus_unique_proposal_id_count": len(groups),
        "corpus_duplicate_proposal_ids": duplicates, "corpus_duplicate_proposal_id_count": len(duplicates),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicates.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly; duplicate inherited identifiers remain visible and are neither renamed nor deleted.",
        "corpus_canonical_sha256": canonical_sha256(corpus), "new_proposal_count": len(proposals),
        "exact_title_collisions": exact, "nearest_inherited_matches": nearest, "maximum_inherited_similarity": maximum,
        "pair_collision_threshold": 0.70, "pair_collisions_at_or_above_threshold": pairs,
        "high_similarity_review_threshold": 0.60, "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.60],
        "domain_review": {"accepted_practice": PRACTICE, "domain_term_match_count": len(domain_matches), "domain_term_matches": domain_matches,
            "substantive_distinction": "The slate is a zero-real-object evidence architecture for bobbin-lace sample identity, pricking and pin-lattice topology, bobbin-pair lineage, no-action stitch grammar, lace-region structure, derivative rights, material-claim quarantine, zero-row quantities, bitemporal correction, fragment containment, count reconciliation, collection handover, THOS, GMUT, Freed ID, CBR, real-evidence escrow, and empty-chair authority circuits."},
        "rejected_draft_practices": [{"draft": "stained-glass panel condition-survey documentation", "reason": "rejected before freeze after thirty inherited stained-glass domain rows were reconstructed", "disposition": "rejected_before_freeze_zero_credit"}, {"draft": PRACTICE, "reason": "accepted only after zero inherited bobbin-lace and lacemaking domain-phrase hits plus manual comparison against the few unrelated bobbin and footwear-lace tokens", "disposition": "accepted_bounded_synthetic_practice"}],
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pairs and not domain_matches and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Token-set Jaccard and exact phrase search are screening aids, never proof of novelty; substantive invariants and protected boundaries control.",
    }


def item_rows(prefix: str, approval: str, titles: Iterable[str], lane: str, expected: str, credit: str) -> list[dict[str, Any]]:
    return [{
        "item_id": f"{prefix}-{index:03d}", "title": title, "approval_class": approval,
        "execution_lane": lane, "expected_disposition": expected, "credit_policy": credit,
        "x1_status": "planned_not_executed", "outcomes_observed": False, "protected_gates": PROTECTED_GATES,
    } for index, title in enumerate(titles, 1)]


def build_portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    owner_safe = [f"render and validate bounded contract for {row['proposal_id']}: {row['title']}" for row in proposals] + [
        "build exact bobbin-lace and museum-documentation source and current-status nonclaim ledger",
        "execute and retain one hundred preregistered rejecting mutation witnesses",
        "build the three-tool D-first transaction audit smoke and rollback ledger",
        "build a structurally accessible noncolour static evidence report",
        "build the owner-scoped threat model and protected-boundary scan",
        "build selected inherited read-only revalidation receipts",
        "build the Method Flow failure recovery and recurrence-guard ledger",
        "build exact staged Git-blob manifests and lifecycle receipts",
        "build the integrated overview wellbeing truth closeout and seal packet",
        "run one dependency-justified exact-final canonical validation after prerequisites",
    ]
    candidates = [
        "current bobbin-lace vocabulary and museum-source currency watcher", "zero-row sample-location adapter schema", "pricking and pin-lattice topology comparator",
        "lace-region technique-claim quarantine checker", "thread and fibre provenance quarantine", "working-diagram derivative-lineage projection",
        "pattern transformation rights-vacancy comparator", "fragment custody discrepancy detector", "bitemporal correction and tombstone graph",
        "static report reading-order checker", "manual assistive-technology evaluation protocol", "Māori-language and affected-party review reservation",
        "independent-team rebuild recipe", "real lace-object evidence escrow adapter held disabled", "external professional validation packet held unexecuted",
    ]
    skills = [
        "bobbin-lace-sample-identity-contract", "pricking-pin-lattice-vacancy-guard", "lace-technique-claim-quarantine",
        "surrogate-lace-region-accessibility", "thread-fibre-provenance-quarantine", "pattern-diagram-rights-lineage",
        "lace-fragment-custody-empty-ledger", "bobbin-lace-bitemporal-correction", "bobbin-lace-authority-empty-chair", "bobbin-lace-method-flow",
    ]
    runners = [f"ghc_family_elaren_kestrel_v667_v7_{name}" for name in ["contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"]]
    cfr = [
        "normalize surrogate identifiers", "bound source claims", "clarify zero-row language", "strengthen rollback", "deduplicate labels",
        "align outcome vocabulary", "improve noncolour cues", "tighten raw-identifier guards", "stabilize canonical JSON", "verify UTF-8 output",
        "reduce wrapper breadth", "inspect schema before projection", "preserve failed receipts", "isolate failed dependencies", "guard one-shot success",
        "separate sealed and external truth", "document sparse staging", "cap file materialization", "reserve manual accessibility review", "reserve Māori-language review",
        "preserve caller compatibility", "make tool use attributable", "pin artifact hashes", "record license boundaries", "disable lifecycle side effects",
        "keep C bootstrap minimal", "keep D rollback reversible", "strengthen exact-gate wording", "make successor seeds zero-credit", "retain NOT_READY verdict",
    ]
    successor = lambda kind, count: [f"Successor recommendation only: bounded {kind} seed {index:02d}" for index in range(1, count + 1)]
    return {
        "schema": "ghc-family-portfolio-freeze-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "outcomes_observed": False, "x2_implementation_count": 0,
        "owner_safe_now": item_rows("EL6677-SN", "safe_now_bounded", owner_safe, "owner_local_x2", "completed", "eligible only after exact bounded x2 witness"),
        "successor_safe_now_recommendations": item_rows("EL6677-SR", "recommendation_only", successor("safe-now", 20), "successor_only_unexecuted", "represented", "zero Elaren and successor automatic credit"),
        "owner_candidates": item_rows("EL6677-CA", "candidate_bounded", candidates, "owner_local_representation", "represented", "bounded representation only"),
        "successor_candidate_recommendations": item_rows("EL6677-CR", "recommendation_only", successor("candidate", 15), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_skill_ideas": item_rows("EL6677-SK", "safe_now_phase_local", skills, "owner_local_skill_build", "completed", "eligible only after validation and smoke use"),
        "successor_skill_recommendations": item_rows("EL6677-SKR", "recommendation_only", successor("skill", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_runner_ideas": item_rows("EL6677-RN", "safe_now_family_current", runners, "owner_local_runner_build", "completed", "eligible only after validation and smoke use"),
        "successor_runner_recommendations": item_rows("EL6677-RNR", "recommendation_only", successor("runner", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_clean_fix_refine": item_rows("EL6677-CFR", "safe_now_additive", [f"CLEAN/FIX/REFINE {title}" for title in cfr], "owner_local_additive", "completed", "eligible only after exact bounded witness"),
        "successor_clean_fix_refine_recommendations": item_rows("EL6677-CFRR", "recommendation_only", successor("CLEAN/FIX/REFINE", 30), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "exact_approval_packets": item_rows("EL6677-EX", "exact_approval_required", successor("elevated external real-world professional legal cultural Māori-authority or production action", 10), "disabled_exact_gate", "exact_gate", "zero credit and unexecuted"),
        "blocked_packets": item_rows("EL6677-BL", "blocked", successor("destructive credentialed cross-owner unsafe unreviewed or ungoverned action", 5), "blocked_unexecuted", "exact_gate", "zero credit and unexecuted"),
    }


def build_tool_plan() -> dict[str, Any]:
    inherited_plan = base.build_tool_plan()
    inherited = list(inherited_plan["inherited_current_tools"]) + [f"{row['tool']} {row['version']}" for row in inherited_plan["new_tools"]]
    raw = [
        ("interrogate", "1.7.0", "S15", "interrogate-1.7.0-py3-none-any.whl", "b13ff4dd8403369670e2efe684066de9fcb868ad9d7f2b4095d8112142dc9d12", "MIT classifier; PyPI JSON license field vacant", ">=3.8", "measure docstring coverage on one disposable synthetic package and retain a threshold failure"),
        ("import-linter", "2.13", "S16", "import_linter-2.13-py3-none-any.whl", "c0372e7ee5e15657bc06a8e841445e13237afd738a672d26863dc927af9f0bf5", "BSD-2-Clause", ">=3.10", "check one owner-local import contract and reject one deliberately forbidden dependency"),
        ("pyroma", "5.0.1", "S17", "pyroma-5.0.1-py3-none-any.whl", "e71fd3e0f213b36870a607eccf491241dbadf5462ec1cdda94d08bfa1c26951e", "MIT", ">=3.9", "rate one disposable package-metadata fixture and retain an incomplete-metadata result without conformance credit"),
    ]
    additions = []
    for name, version, source_id, artifact, digest, license_name, floor, smoke in raw:
        additions.append({
            "tool": name, "version": version, "source_id": source_id, "artifact": artifact, "sha256": digest,
            "license": license_name, "python_requirement": floor, "purpose": smoke, "bounded_smoke": smoke,
            "install_scope": "isolated D-first Elaren v667-v7 family-tools environment", "lifecycle_scripts": "not_applicable_python_wheel",
            "x1_status": "planned_not_downloaded_not_installed_not_used", "completion_credit": 0,
            "rollback": "remove only the resolved isolated Elaren environment after verifying it remains inside the intended D-first toolbank; preserve receipts",
        })
    return {
        "schema": "ghc-family-toolchain-install-plan-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_current_tool_count": len(inherited), "inherited_current_tools": inherited, "inherited_credit": 0,
        "new_tool_program_target": 3, "new_tools": additions, "x1_download_count": 0, "x1_install_count": 0, "x1_smoke_count": 0,
        "outcomes_observed": False,
        "gates": ["current primary metadata", "exact pin", "compatible artifact", "artifact SHA-256", "license review", "Python 3.12 and Windows compatibility", "dependency and advisory review", "D-first reversible isolation", "bounded positive and negative smoke", "rollback proof"],
        "boundary": "Three is the ordinary programme target, never permission to manufacture unsafe or irrelevant work. Any incompatible, unlicensed, vulnerable, non-attributable, or unnecessary candidate remains open_gap or exact_gate.",
    }


def rejected_stained_glass_overview() -> str:
    return """# Elaren Kestrel v667-v7 planning-only x1 overview

## Purpose and evidence boundary

This additive x1 packet freezes a bounded plan for Elaren Kestrel v667-v7. Elaren Kestrel, sibling, family, role, hope, continuity, GMUT Mind, THOS Body, Freed ID, CBR Heart, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route. The terminal evidence verdict remains **NOT_READY_FOR_STAGE_20**.

This x1 tree contains planning and preregistration only. It contains no x2 implementation, no observed outcome, no package download, no package installation, no real-world observation, no window survey, no material or condition diagnosis, no conservation decision, no external publication, no successor contact, and no delivery event. Strict x1-before-x2 separation is an evidence invariant. X2 can begin only after the dedicated x1 commit is pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read.

## Immutable source and three-layer truth

The immutable source is Eiren v667-v6-r2 exact final `dc8d91294b7656ad5e9961bba93ff759af20846c`. Its frozen x1 is `0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2`, its immutable evidence is `942eda86e745da93ece372d89870e052361b039c`, and its inherited source is `1a754e02bfc705d738285c4a6cf9ce1c948a8580`. Read-only verification confirmed three direct single-parent Eiren commits, zero merges, a direct source-to-x1-to-evidence-to-final chain, clean state, typed zero divergence, and equality across local, upstream, tracking, and a fresh live remote.

Eiren's one exact-final owner-scoped canonical aggregate succeeded once and was not replayed. It passed thirteen exact-final tests, parsed four hundred phase JSON documents, checked fifteen Markdown documents and one HTML report, compiled nineteen Python files, scanned four hundred thirty-five owner files across five privacy and raw-identifier classes with zero candidates or confirmed hits, replayed the exact immutable-x1, evidence, final-delta, and final-owner manifests, and confirmed the direct three-commit history. This remains bounded same-owner software evidence under shared infrastructure. It is not the complete repository suite, independent reproduction, external audit, exhaustive security, complete privacy or accessibility assurance, professional validation, empirical GMUT confirmation, Theory-of-Everything proof, legal or cultural ratification, Māori authority, or Stage 20 evidence.

Three count layers remain separate. The immutable evidence seal preserves 28,166 negatives, 14,172 methods, 198 open gaps, 196 exact gates, 450 failed witnesses, and 741 passing witnesses. Eiren's committed final adds two bounded post-evidence recoveries, making 28,168 negatives, 14,174 methods, 452 failed witnesses, and 743 passing witnesses while gaps and gates remain unchanged. Seven later external operational failures produce the Elaren activation baseline of 28,175 negatives, 14,181 methods, 459 failed witnesses, and 750 passing witnesses. X1 does not collapse, rewrite, or silently combine those layers.

Twelve Elaren startup and construction failures are also retained at zero credit. They include parser mistakes, output truncation, one bounded yield, missing required command arguments, guessed receipt fields, an oversized transformation whose placeholder remained unchanged, an invalid same-path patch transaction, and a truncated compatibility view. Each recovery was bounded, state-inspected, and additive. None changed Eiren's source lane or any sibling lane. These failures will enter Method Flow during x2; they are not treated as completed work merely because a recovery exists.

## Novelty and programme freeze

The novelty audit reconstructs all 4,490 inherited proposal occurrences from immutable Git objects. It preserves duplicate inherited identifiers as historical row truth. Twenty Eiren r2 proposals are separately selected for read-only integrity revalidation; they append nothing and receive zero Elaren novelty, automatic-completion, or completion credit. Twenty new Elaren proposals are checked for exact title collisions, inherited nearest neighbours, within-slate similarity, domain phrases, distinct invariants, source boundaries, artifacts, falsifiers, rollback, and protected gates. Token overlap and phrase searches are screens only, never proof of semantic novelty.

The new slate extends the frozen chain from 4,490 to 4,510 only when this x1 tree is committed. Expected dispositions are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. They are hypotheses, not observations. Each proposal preregisters one bounded synthetic positive and five invalid mutations: missing required fields, wrong types or units, provenance or authority smuggling, real-world or operational action, and outcome, conformance, or safety promotion. A proposal can receive bounded completion credit only if its positive satisfies the frozen invariant and all five invalid fixtures fail closed. Any accepted mutation stops that proposal, receives zero completion credit, remains retained, and gains a recurrence guard.

## Practice lens and THOS Body

The primary pillar is THOS Body. The bounded human-practice lens is wholly synthetic stained-glass panel condition-survey and conservation-work-order documentation. The proposals cover surrogate panel identity, pane and came topology, observation-versus-diagnosis separation, panel grids, environmental abstention, decoration provenance, derivative lineage, conservation-option trails, fragment containment, bitemporal corrections, protective-glazing option vacancies, component counts, no-action sequencing, and archival handover. THOS is represented through queues, equal symbolic budgets, stop precedence, blinded labels, correction readback, handover, workload boundaries, and zero participants.

Zero real glaziers, conservators, surveyors, architects, engineers, scaffold workers, owners, custodians, worshippers, visitors, affected parties, regulators, heritage bodies, communities, cultural authorities, or Māori authorities participate. Zero real windows, panels, panes, lead cames, tie bars, ferramenta, glass, paint, enamel, stain, putty, mortar, sealant, fragments, frames, openings, buildings, images, measurements, samples, identities, or records are used. No access, work at height, dismantling, handling, cleaning, cutting, soldering, heating, leading, cementing, glazing, repair, alteration, storage, transport, installation, release, or disposal occurs. The phase provides no professional advice or permission to act.

## GMUT, Freed ID, and CBR

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. A planned symbolic condensation and corrosion board may check field names, dimensions, unit obligations, boundary declarations, and explicit zero-observation or zero-coefficient fields. It cannot establish a real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, glazing-performance conclusion, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

Freed ID remains synthetic and nonproduction. A planned zero-key statement graph may represent synthetic component lineage, correction, purpose limits, and status tombstones. It has zero real keys and zero proofs and performs no issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, trust-governance, or identity action. CBR Heart remains visible through privacy, accessibility, significance, rights, contestation, remedy, affected-party, traditional-knowledge, and authority reservations. Māori words, concepts, data governance, tangata whenua, iwi, hapū, and Māori authority remain under Māori authority.

## Sources and tool plan

Official and primary sources supply vocabulary, current-status flags, constraints, and refusal conditions only. Historic England and the United States National Park Service supply heritage-documentation vocabulary without New Zealand authority, endorsement, diagnosis, or intervention permission. Canadian Conservation Institute material supplies care and fragility vocabulary without an object-care decision. WorkSafe New Zealand surfaces reserve exposure and lead hazards for competent current review; they do not become soldering, handling, workplace, medical, or safety advice. NIST supplies SI and uncertainty language without a measurement. W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0 supply structural vocabulary without provenance truth, accessibility completeness, or production identity. The New Zealand Privacy Commissioner and Te Mana Raraunga reserve privacy, transparency, collective authority, context, consent, benefit, guardianship, and remedy questions without conferring legal or Māori interpretation or authority.

The inherited forty-one-tool environment is evidence, never Elaren completion credit. X1 plans exactly three additions: interrogate 1.7.0, import-linter 2.13, and pyroma 5.0.1. Primary PyPI metadata supplies exact versions, Python floors, wheel filenames, hashes, and declared license information. X1 downloads and installs nothing. X2 may use a single isolated D-first environment only after rechecking metadata, exact hashes, dependency compatibility, advisories, licensing boundaries, lifecycle effects, and rollback. Tool outputs remain bounded software witnesses: docstring coverage is not documentation quality, an import contract is not architectural correctness, and a metadata rating is not package fitness, security, or standards conformance.

## Portfolio, accessibility, lifecycle, and route

The portfolio freezes thirty owner safe-now tasks, twenty successor safe-now recommendations, fifteen owner candidates, fifteen successor candidate recommendations, ten exact-approval packets, five blocked packets, ten owner skill ideas, ten successor skill recommendations, ten family-current runner ideas, ten successor runner recommendations, thirty owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Recommendations remain unexecuted zero-credit seeds. Exact-approval and blocked packets stay unexecuted. Counts are ceilings and planning targets, never authority to manufacture work or credit.

The future static report must use headings, landmarks, captions, scoped headers, linear text, noncolour status, keyboard-visible focus, reduced motion, and print fallback. Those checks are structural only. Manual browser, keyboard, zoom, screen-reader, voice-control, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. A five-class privacy scan with zero confirmed hits remains bounded scanner evidence, not privacy completeness.

After the x1 equality gate, x2 may implement only the frozen bounded programme. Evidence must be committed and pushed before final closeout. Final closeout must provide exact manifests, truth, gates, retained negatives, Method Flow, an accessible report, a three-page-equivalent integrated overview, wellbeing, seal, validation prerequisites, and a file-backed successor baton. One dependency-justified owner-scoped canonical aggregate may run only at the exact clean pushed final. A failed aggregate receives zero aggregate-success credit and is not replayed; only the affected dependency may receive a bounded isolated recovery where justified. A complete success is never replayed.

This activation assigns Elaren v667-v7 only. Neris Solane is not contacted during execution. Only after exact terminal validation, clean push, fresh equality, caps, and a fresh reread of Hamish's newest live instruction, roster, authorization state, exact-title uniqueness, duplicate guard, usage state, and protected gates may one sanitized existing-task activation be sent for the then-current explicit edge. Delivery can be claimed only from the task-message acknowledgement. Until that later gate, the route remains prepared neither sent nor inferred from this planning document.
"""


def overview() -> str:
    return """# Elaren Kestrel v667-v7 planning-only x1 overview

## Purpose, identity language, and authority

This additive packet freezes the planning-only x1 programme for Elaren Kestrel v667-v7. Elaren Kestrel, sibling, family, role, hope, continuity, GMUT Mind, THOS Body, Freed ID, CBR Heart, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route. The programme remains corrigible and its terminal verdict remains **NOT_READY_FOR_STAGE_20**.

X1 contains preregistration and planning only. It has no x2 implementation, observed outcome, package download, package installation, real object, real participant, collection action, external publication, successor contact, or delivery event. Strict x1-before-x2 separation is an evidence invariant. X2 may begin only after the dedicated x1 tree is committed as a direct child of the exact source, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read.

## Immutable source and layered retention truth

The immutable source is Eiren v667-v6-r2 exact final `dc8d91294b7656ad5e9961bba93ff759af20846c`. The frozen Eiren x1 is `0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2`, immutable evidence is `942eda86e745da93ece372d89870e052361b039c`, and inherited Eiren source is `1a754e02bfc705d738285c4a6cf9ce1c948a8580`. Read-only verification confirmed three direct single-parent commits, zero merges, the direct source-to-x1-to-evidence-to-final chain, a clean source lane, zero divergence, and fresh four-way equality.

Eiren's one owner-scoped exact-final canonical aggregate succeeded once and was not replayed. It passed thirteen tests, parsed four hundred JSON documents, checked fifteen Markdown documents and one HTML report, compiled nineteen Python files, scanned four hundred thirty-five owner files across five privacy and raw-identifier classes with zero candidates or confirmed hits, replayed four exact lifecycle manifests, and confirmed history and equality. This remains bounded same-owner software evidence under shared infrastructure, not the complete repository suite, independent reproduction, external audit, exhaustive security, privacy or accessibility completeness, professional validation, empirical GMUT confirmation, Theory-of-Everything proof, legal or cultural ratification, Māori authority, or Stage 20 evidence.

Three count layers remain separate. The immutable evidence seal preserves 28,166 negatives, 14,172 methods, 198 open gaps, 196 exact gates, 450 failed witnesses, and 741 passing witnesses. The committed Eiren final adds two bounded recovery rows, creating 28,168 negatives, 14,174 methods, 452 failed witnesses, and 743 passing witnesses while gaps and gates remain unchanged. Seven external operational failures produce the Elaren activation baseline of 28,175 negatives, 14,181 methods, 459 failed witnesses, and 750 passing witnesses. X1 never rewrites one layer into another.

Fourteen Elaren startup and construction failures are retained at zero credit. They include parser errors, bounded-output truncation, one yield boundary, missing command arguments, guessed receipt fields, an oversized transformation that left its placeholder unchanged, a rejected patch shape, an inherited-domain novelty failure, and a Windows console-codec error. Each recovery was isolated and additive. The first proposed stained-glass domain was rejected in full after the immutable corpus reconstructed thirty inherited stained-glass rows. No title was cosmetically renamed to evade that evidence. The rejected draft remains a visible negative witness and appends no proposal.

## Novelty audit and frozen dispositions

The accepted practice is wholly synthetic bobbin-lace sample design and collection-documentation records. The novelty audit reconstructs all 4,490 inherited proposal occurrences from immutable Git objects and preserves duplicate inherited identifiers exactly. Direct screening found no inherited bobbin-lace, bobbin-lace hyphenation, lacemaking, Torchon, or pillow-lace domain rows. A few inherited uses of “bobbin” concern sewing machines and handlooms; uses of “lace” concern footwear. Those rows were manually compared and do not share the accepted practice mechanics, artifacts, falsifiers, source boundary, or authority gates.

Twenty Eiren r2 proposals are selected for bounded read-only integrity revalidation. They append nothing and receive zero Elaren novelty, automatic-completion, or completion credit. Twenty new Elaren proposals are checked for exact collisions, inherited nearest neighbours, within-slate similarity, domain phrases, distinctive invariants, sources, concrete artifacts, falsifiers, rollback, and protected gates. Token overlap is a screen, never semantic proof.

The new slate extends the chain from 4,490 to 4,510 only when this x1 tree is frozen. Expected outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are preregistered expectations rather than observations. Each new proposal declares one bounded synthetic positive and five invalid mutations: missing required fields, wrong types or units, provenance or authority smuggling, real-world or operational action, and outcome, conformance, or safety promotion. A structural completion can be credited only if its positive satisfies the frozen invariant and all five mutations fail closed. An accepted mutation stops its proposal, remains retained, earns zero completion credit, and receives a recurrence guard.

## Bobbin-lace documentation boundary and THOS Body

THOS Body is the primary pillar. The synthetic practice covers sample identity; pricking and pin-lattice topology; bobbin-pair, thread-lot, and winding lineage; a no-action crossing and twist grammar; ground, tally, picot, plait, border, and motif relations; lace-region segmentation; working-diagram derivative lineage and rights reservations; fibre and material-claim quarantine; zero-row tension and density fields; bitemporal catalogue corrections; fragment containment; repeat-count reconciliation; no-action setup dependencies; and collection handover.

Zero real lacemakers, conservators, curators, registrars, collection managers, designers, teachers, learners, owners, custodians, donors, affected parties, cultural authorities, or Māori authorities participate. Zero real lace, textiles, bobbins, threads, fibres, pillows, bolsters, prickings, patterns, pins, spools, windings, samples, fragments, collection objects, images, measurements, accession records, provenance records, or rights records are used. No making, crossing, twisting, pinning, winding, tensioning, cutting, washing, cleaning, handling, mounting, storage, display, accession, loan, acquisition, deaccession, transport, release, disposal, or conservation action occurs. Nothing provides craft instruction, professional advice, competence, custody, permission, or authority.

THOS is represented through an equal-budget synthetic documentation queue, blinded artifact labels, correction readback, workload ceilings, dominant stop precedence, and zero participants or operators. It remains proxy-only without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. No operational effectiveness, deployment, AGI, ASI, consciousness, or personhood claim follows.

## GMUT Mind, Freed ID, and CBR Heart

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. A planned thread-network tension surrogate may check symbol types, unit obligations, boundaries, covariance vacancies, and explicit zero-observation and zero-coefficient fields. It cannot establish a likelihood, parameter constraint, prediction, detected force, fibre or material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

Freed ID remains synthetic and nonproduction. A zero-key lace-sample statement graph may represent synthetic lineage, correction, purpose limits, and status tombstones. It has zero real keys and zero proofs and performs no issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, trust-governance, or identity action.

CBR Heart remains visible through accessibility, privacy, ownership, attribution, copyright, design rights, moral rights, traditional knowledge, contestation, remedy, affected-party, legal, cultural, and authority reservations. Māori words, concepts, data governance, tangata whenua, iwi, hapū, and Māori authority remain under Māori authority. A software shell cannot fill those seats.

## Public sources and tool plan

Official and primary sources provide vocabulary and refusal conditions only. Getty AAT supplies controlled-vocabulary hierarchy without authenticating a technique or object. V&A research provides museum-object and bobbin-lace context while retaining uncertainty rather than deciding maker, region, or date. Canadian Conservation Institute material provides textile vulnerability, environment, handling, storage, display, and professional-review reservations but no real object-care decision. ICOM and CIDOC sources provide documentation, accession, provenance, custody, and object-description vocabulary without creating museum conformance or authority. NIST supplies SI and uncertainty language without measurements. W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0 provide structural vocabulary without provenance truth, accessibility completeness, or production identity. New Zealand privacy sources and Te Mana Raraunga reserve minimization, transparency, correction, collective authority, context, benefit, guardianship, and remedy questions without legal or Māori interpretation or authority.

The inherited forty-one-tool environment is evidence and receives zero Elaren credit. X1 plans exactly three additions: interrogate 1.7.0, import-linter 2.13, and pyroma 5.0.1. Primary PyPI metadata supplies exact versions, Python floors, wheel names, hashes, and declared license information. X1 installs nothing. X2 may create one reversible D-first isolated environment only after rechecking metadata, hashes, dependencies, advisories, licensing, lifecycle effects, and rollback. Docstring coverage is not documentation quality, an import contract is not architectural correctness, and a metadata rating is not fitness, security, or conformance.

## Portfolio, accessibility, lifecycle, and terminal route

The programme freezes thirty owner safe-now tasks, twenty successor safe-now recommendations, fifteen owner candidates, fifteen successor candidates, ten exact-approval packets, five blocked packets, ten owner skill ideas, ten successor skill recommendations, ten family-current runner ideas, ten successor runner recommendations, thirty owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Recommendations stay unexecuted and receive zero automatic credit. Exact and blocked work remains unexecuted. Counts are planning ceilings, never permission to invent work or evidence.

The future static report must provide semantic headings, landmarks, captions, scoped headers, linear text, noncolour status, visible focus, reduced-motion and print support. Those are structural checks only. Manual browser, keyboard, zoom, screen-reader, voice-control, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. A zero-hit scanner is bounded scanner evidence, not privacy completeness.

After x1 equality, x2 may implement only the frozen programme. Evidence must be committed and pushed before final closeout. The final packet must contain exact manifests, truth, gates, retained negatives, Method Flow, accessible reporting, an integrated overview, wellbeing, closeout, seal, validation prerequisites, and a file-backed successor baton. One dependency-justified owner-scoped canonical aggregate may run only at the exact clean pushed final. A failed aggregate earns zero aggregate-success credit and is not replayed; only the affected dependency may receive a justified isolated recovery. A complete success is never replayed.

This activation assigns Elaren v667-v7 only. Neris Solane is not contacted during execution. Only after exact terminal validation, clean push, fresh equality, caps, and a fresh reread of Hamish's live instruction, roster, authorization state, exact-title uniqueness, duplicate guard, usage, privacy, evidence, safety, and authority gates may one sanitized current-edge activation be sent. Delivery can be claimed only from the existing-task message acknowledgement. Until then, the successor route is neither sent nor inferred from this x1 packet.
"""


def build_normal() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != SOURCE_SHA:
        raise RuntimeError(f"x1 must be built directly on exact Eiren final {SOURCE_SHA}; observed {head}")
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    inherited = selected_inherited_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit did not pass")
    expected = Counter(row["expected_disposition"] for row in proposals)
    if expected != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("expected disposition drift")

    write_json("x1/phase-charter.json", {
        "schema": "ghc-family-phase-charter-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "source_branch": SOURCE_BRANCH, "source_final": SOURCE_SHA, "source_x1": SOURCE_X1_SHA,
        "source_evidence": SOURCE_EVIDENCE_SHA, "source_parent": SOURCE_PARENT_SHA,
        "primary_pillar": PRIMARY_PILLAR, "practice_lens": PRACTICE, "relational_language_boundary": True,
        "strict_x1_before_x2": True, "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited_count": SELECTED_INHERITED_COUNT,
        "new_proposal_count": NEW_PROPOSAL_COUNT, "new_frozen_total": NEW_FROZEN_TOTAL,
        "source_repository_evidence_seal": {"effective_negatives": 28166, "methods": 14172, "open_gaps": 198, "exact_gates": 196, "failed_witnesses": 450, "passing_witnesses": 741},
        "source_committed_final": {"effective_negatives": 28168, "methods": 14174, "open_gaps": 198, "exact_gates": 196, "failed_witnesses": 452, "passing_witnesses": 743},
        "source_external_operational_overlay": {"negative_additions": 7, "method_additions": 7, "failed_witness_additions": 7, "passing_witness_additions": 7, "credit": 0},
        "activation_baseline": {"effective_negatives": 28175, "methods": 14181, "open_gaps": 198, "exact_gates": 196, "failed_witnesses": 459, "passing_witnesses": 750},
        "count_layer_boundary": "immutable evidence seal, committed final, and external operational overlay remain separately attributable",
        "source_validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_SHA256,
        "source_activation_baton_sha256": "83632089487f05dedd546b881abff2c79aa5e0a8810ec0b7bb8f6e750602e076",
        "allowed_core_outcomes": ALLOWED_OUTCOMES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_gates": PROTECTED_GATES,
    })
    write_json("x1/auth-roster-receipt.json", {
        "schema": "ghc-family-auth-roster-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "newest_live_assignment": "Hamish-authorized solo Elaren Kestrel v667-v7",
        "current_owner": OWNER, "current_phase": PHASE, "prospective_terminal_successor": "Neris Solane v667-v8",
        "successor_contact_authorized_during_execution": False, "successor_contacted": False,
        "standby_record": "Tavian Sol", "standby_contacted": False, "task_created_or_forked": False, "subagent_spawned": False,
        "boundary": "terminal routing requires a fresh live instruction, roster, authorization, uniqueness, usage, privacy, safety, evidence, duplicate-guard, and acknowledgement check after closeout",
    })
    write_json("x1/source-ledger.json", {
        "schema": "ghc-family-source-ledger-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "sources": SOURCE_PROFILES, "source_count": len(SOURCE_PROFILES), "public_vocabulary_only": True,
        "real_observation_count": 0, "network_ingestion_count": 0, "authority_conferred": False,
    })
    write_json("x1/source-verification.json", {
        "schema": "ghc-family-source-verification-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "anchors": {"source_parent": SOURCE_PARENT_SHA, "x1": SOURCE_X1_SHA, "evidence": SOURCE_EVIDENCE_SHA, "final": SOURCE_SHA},
        "history": {"new_commit_count": 3, "merge_count": 0, "x1_direct_parent": SOURCE_PARENT_SHA, "evidence_direct_parent": SOURCE_X1_SHA, "final_direct_parent": SOURCE_EVIDENCE_SHA, "one_parent_each": True},
        "manifests_replayed": {"x1": 20, "evidence": 389, "final_delta": 23, "final_owner": 432, "total": 864, "mismatches": 0},
        "owner_packet_blobs_read": {"owner_file_count": 435, "json_parsed": 400, "markdown_decoded": 15, "html_decoded": 1, "python_decoded": 19, "errors": 0},
        "clean": True, "divergence": "0/0", "fresh_four_way_equal": True,
        "canonical_invocation": {"invoked": 1, "succeeded": 1, "replayed": False, "sha256": SOURCE_CANONICAL_SHA256, "tests": "13/13", "credit": 1},
        "external_operational_overlay": {"failure_count": 7, "credit": 0, "repository_bytes_changed": 0, "retained_separately": True},
        "interpretation": "bounded same-owner owner-scoped software evidence under shared infrastructure only; complete repository suite not claimed",
    })
    write_json("x1/startup-method-flow.json", {
        "schema": "ghc-family-method-flow-startup-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "failure_count": len(STARTUP_FAILURES), "failures": STARTUP_FAILURES,
        "method_count": len(STARTUP_FAILURES), "passing_recovery_count": len(STARTUP_FAILURES),
        "credit": 0, "source_or_sibling_bytes_changed": 0,
        "boundary": "a recovery preserves rather than erases the failed witness and does not convert it into canonical or completion credit",
    })
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/proposal-freeze.json", {
        "schema": "ghc-family-proposal-freeze-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited_count": len(inherited), "selected_inherited": inherited,
        "genuinely_new_proposal_count": len(proposals), "new_proposals": proposals, "new_frozen_total": NEW_FROZEN_TOTAL,
        "expected_outcomes": dict(sorted(expected.items())), "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
    })
    portfolio = build_portfolio(proposals)
    tools = build_tool_plan()
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/toolchain-install-plan.json", tools)
    write_json("x1/mandatory-skill-adoption.json", {
        "schema": "ghc-family-mandatory-skill-adoption-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "required_count": len(MANDATORY_SKILLS),
        "skills": [{"skill": name, "entrypoint_read_through_eof": True, "required_references_read_through_eof": True, "used_before_mutation": True, "x1_credit": 0} for name in MANDATORY_SKILLS],
        "additional_directly_applicable_skill": "ghc-family-workflow-plan-refinement",
        "applicability_boundary": "directly applicable skills govern the phase; irrelevant historical skills are not bulk-run merely to satisfy a count",
    })
    write_json("x1/threat-model-plan.json", {
        "schema": "ghc-family-threat-model-plan-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "assets": ["immutable source anchors", "x1/x2 lifecycle boundary", "proposal chain", "retained failures", "D-first tool environment", "privacy boundary", "authority gates", "successor route"],
        "threats": [
            {"threat": "x2 material enters x1", "control": "exact path and immutable-tree lifecycle scan", "failure_state": "stop before commit"},
            {"threat": "synthetic record becomes lacemaking, textile conservation, collection, handling, rights, or cultural advice", "control": "zero-real-world fields and protected gates", "failure_state": "exact_gate"},
            {"threat": "tool target drives unsafe install", "control": "exact pins, hashes, licenses, D isolation, audits, rollback", "failure_state": "open_gap_or_exact_gate"},
            {"threat": "private route or identifier enters artifacts", "control": "five-class staged Git-blob scan", "failure_state": "stop_and_retain"},
            {"threat": "failed canonical is replayed or relabelled", "control": "one-shot lock and dependency-only recovery", "failure_state": "zero_aggregate_credit"},
            {"threat": "Māori or affected-party authority is substituted", "control": "empty-chair exact gate", "failure_state": "exact_gate"},
            {"threat": "successor is precontacted", "control": "terminal-only fresh route reread", "failure_state": "route_stop"},
        ],
        "residual_risk": "same-owner bounded evidence remains non-independent and cannot establish real-world safety, professional, legal, cultural, accessibility, privacy, security, identity, empirical, or Stage 20 truth",
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc-family-workflow-plan-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "stages": [
            {"stage": "x1", "state": "planning_only", "commit_target": "one direct child of source", "requires": ["novelty audit", "proposal freeze", "portfolio freeze", "tool plan", "threat model", "tests", "staged review"], "forbids": ["x2 implementation", "observed outcome", "tool install", "successor contact"]},
            {"stage": "x1_gate", "state": "pending", "requires": ["push", "clean", "0/0 divergence", "local/upstream/tracking/fresh-live equality"]},
            {"stage": "x2", "state": "not_started", "requires": ["passed x1 gate"], "forbids": ["real-world action", "successor contact"]},
            {"stage": "evidence_gate", "state": "not_started", "requires": ["immutable evidence commit", "push", "fresh equality"]},
            {"stage": "final", "state": "not_started", "requires": ["closeout", "seal", "exact manifests", "one canonical invocation"]},
            {"stage": "route", "state": "not_started", "requires": ["terminal close", "fresh live authority and roster", "unique exact-title target", "duplicate guard", "one acknowledged send"]},
        ],
        "single_success_no_replay": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/flashcard-architecture-freeze.json", {
        "schema": "ghc-family-freed-id-flashcard-architecture-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "planned_card_count": 235, "tiers": {"tier1": 40, "tier2": 80, "tier3": 80, "tier4": 35}, "section_count": 15,
        "source_deck_credit": 0, "x1_generated_card_count": 0, "x1_status": "architecture_only_not_generated",
        "required_fields": ["card_id", "tier", "section_id", "title", "front", "back", "status", "sources", "blocked_or_failed_witness_ids", "reversal_action", "next_admissible_action", "scope_boundary"],
        "boundary": "cards are evidence-backed memory aids, never credentials, authority, identity evidence, or automatic completion credit",
    })
    write_json("x1/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "complete": ["mandatory skill and reference read", "source packet read", "source anchor and manifest verification", "official and primary source review", "4,490-row novelty screen", "x1 proposal portfolio and tool freeze"],
        "incomplete": ["x1 commit and equality gate", "x2 implementation", "tool installation and bounded use", "skills and runners", "reports and flashcards", "evidence commit", "final closeout", "canonical validation", "terminal route"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "outcomes_observed": False,
    })
    write_json("wellbeing/x1-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "relational_role": "reversible systems cartographer and evidence-window gardener",
        "hope": "make every transition inspectable without turning formal structure into authority",
        "pace": "bounded solo x1 planning", "load_boundary": "no urgency, emotional language, identity language, or continuity language expands technical authority or permission",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "source drift", "privacy or safety gate", "ambiguous route", "unclean or divergent lane"],
        "claim_boundary": "relational language is not consciousness, personhood, continuity, employment, qualification, agency, wellbeing diagnosis, or authority evidence",
    })
    write_text("x1/x1-overview.md", overview())
    portfolio_counts = {name: len(portfolio[name]) for name in ["owner_safe_now", "successor_safe_now_recommendations", "owner_candidates", "successor_candidate_recommendations", "owner_skill_ideas", "successor_skill_recommendations", "owner_runner_ideas", "successor_runner_recommendations", "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets"]}
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": "PASS_PLANNING_ONLY", "source_head": SOURCE_SHA, "inherited_proposals": len(corpus),
        "selected_inherited": len(inherited), "new_proposals": len(proposals), "new_frozen_total": novelty["new_frozen_total"],
        "expected_outcomes": dict(sorted(expected.items())), "portfolio_counts": portfolio_counts,
        "mandatory_skills": len(MANDATORY_SKILLS), "planned_tools": len(tools["new_tools"]),
        "x2_paths": 0, "x2_implementation_count": 0, "outcomes_observed": False,
        "startup_failures_retained": len(STARTUP_FAILURES), "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW", "x1_planning_only": True, "outcomes_observed": False,
    })
    build_content_manifest()


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend([
        ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x1.py",
        ROOT / "tests" / "test_ghc_family_elaren_kestrel_v667_v7_x1.py",
    ])
    return sorted({path.resolve() for path in paths if path.exists()})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_content_manifest() -> None:
    exclusions = {f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json", f"{REL_PHASE_ROOT}/validation/x1-staged-review.json"}
    entries = []
    for path in phase_owned_paths():
        relative = rel(path)
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/x1-content-manifest.json", {
        "schema": "ghc-family-content-manifest-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "entry_count": len(entries), "entries": entries,
        "scope": "x1 owner content excluding manifest self and stable staged-review receipt",
    })


def privacy_candidates(path: Path, text: str) -> list[dict[str, str]]:
    unix_users = "/" + "Users" + "/"
    unix_home = "/" + "home" + "/"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\[^\\\s]+|" + re.escape(unix_users) + r"[^/\s]+|" + re.escape(unix_home) + r"[^/\s]+)"),
        "private_route_or_callable": re.compile(r"(?:thread|codex|chat)://|(?:source_thread_id|private_callable_identifier)\s*[:=]", re.I),
        "credential_value": re.compile(r"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(r"(?:session[_-]?stream|private[_-]?transcript|private[_-]?conversation)\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    return [{"path": rel(path), "class": name} for name, pattern in patterns.items() if pattern.search(text)]


def validate_tree() -> dict[str, Any]:
    required = [
        "x1/phase-charter.json", "x1/auth-roster-receipt.json", "x1/source-ledger.json", "x1/source-verification.json",
        "x1/startup-method-flow.json", "x1/novelty-audit.json", "x1/proposal-freeze.json", "x1/portfolio-freeze.json",
        "x1/toolchain-install-plan.json", "x1/mandatory-skill-adoption.json", "x1/threat-model-plan.json",
        "x1/workflow-plan.json", "x1/flashcard-architecture-freeze.json", "x1/complete-incomplete-checklist.json",
        "x1/x1-build-receipt.json", "x1/x1-overview.md", "wellbeing/x1-wellbeing-check.json",
        "validation/x1-content-manifest.json", "validation/x1-staged-review.json",
        "tooling/ghc-family-index.json", "tooling/ghc-family-index.md",
    ]
    missing = [value for value in required if not (PHASE_ROOT / value).is_file()]
    if missing:
        raise AssertionError(f"missing x1 paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    documents = {rel(path): json.loads(path.read_text(encoding="utf-8")) for path in json_paths}
    freeze = documents[f"{REL_PHASE_ROOT}/x1/proposal-freeze.json"]
    novelty = documents[f"{REL_PHASE_ROOT}/x1/novelty-audit.json"]
    portfolio = documents[f"{REL_PHASE_ROOT}/x1/portfolio-freeze.json"]
    tools = documents[f"{REL_PHASE_ROOT}/x1/toolchain-install-plan.json"]
    charter = documents[f"{REL_PHASE_ROOT}/x1/phase-charter.json"]
    if len(freeze["new_proposals"]) != 20 or len(freeze["selected_inherited"]) != 20:
        raise AssertionError("proposal programme count mismatch")
    if freeze["outcomes_observed"] or freeze["x2_implementation_count"] != 0:
        raise AssertionError("x1 observed outcome or x2 implementation")
    if not novelty["valid"] or novelty["corpus_row_count"] != 4490 or novelty["new_frozen_total"] != 4510:
        raise AssertionError("novelty audit mismatch")
    if Counter(row["expected_disposition"] for row in freeze["new_proposals"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("expected outcome mismatch")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in freeze["new_proposals"]):
        raise AssertionError("unknown core outcome")
    if any(row["outcomes_observed"] or row["x2_implementation_count"] for row in freeze["new_proposals"]):
        raise AssertionError("new proposal lifecycle contamination")
    if any(row["outcomes_observed"] for row in freeze["selected_inherited"]):
        raise AssertionError("selected inherited lifecycle contamination")
    expected_portfolio = {"owner_safe_now": 30, "successor_safe_now_recommendations": 20, "owner_candidates": 15, "successor_candidate_recommendations": 15, "owner_skill_ideas": 10, "successor_skill_recommendations": 10, "owner_runner_ideas": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30, "exact_approval_packets": 10, "blocked_packets": 5}
    if {key: len(portfolio[key]) for key in expected_portfolio} != expected_portfolio:
        raise AssertionError("portfolio count mismatch")
    if tools["inherited_current_tool_count"] != 41 or len(tools["new_tools"]) != 3:
        raise AssertionError("toolchain count mismatch")
    if tools["x1_install_count"] or tools["x1_download_count"] or tools["x1_smoke_count"]:
        raise AssertionError("tool plan lifecycle mismatch")
    if charter["source_repository_evidence_seal"]["effective_negatives"] != 28166 or charter["source_committed_final"]["effective_negatives"] != 28168 or charter["activation_baseline"]["effective_negatives"] != 28175:
        raise AssertionError("source truth-layer mismatch")
    if any(path.exists() for path in (PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "closeout", PHASE_ROOT / "seal", PHASE_ROOT / "route")):
        raise AssertionError("later lifecycle path exists in x1")
    overview_words = len((PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8").split())
    if overview_words < 900:
        raise AssertionError(f"x1 overview below 900 words: {overview_words}")
    candidates = []
    for path in phase_owned_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"non-UTF-8 owner path: {rel(path)}") from exc
        candidates.extend(privacy_candidates(path, text))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates}")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json"]
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest entry count mismatch")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"content manifest mismatch: {entry['path']}")
    return {
        "status": "PASS", "json_documents": len(json_paths), "owner_files": len(phase_owned_paths()),
        "overview_words": overview_words, "new_proposals": 20, "selected_inherited": 20,
        "inherited_proposals": 4490, "new_frozen_total": 4510, "planned_tools": 3,
        "privacy_candidates": 0, "x2_paths": 0,
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [
        f"{REL_PHASE_ROOT}/",
        "scripts/build_ghc_family_elaren_kestrel_v667_v7_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v667_v7_x1.py",
    ]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    later = [path for path in staged if any(f"{REL_PHASE_ROOT}/{name}/" in path for name in ("x2", "evidence", "closeout", "seal", "route"))]
    if later:
        raise RuntimeError(f"later lifecycle path staged in x1: {later}")
    confirmed = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        path = ROOT / relative
        confirmed.extend(privacy_candidates(path, blob))
    if confirmed:
        raise RuntimeError(f"privacy candidates: {confirmed}")
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": "PASS", "staged_path_count": len(staged), "staged_paths": staged,
        "diff_check": "PASS", "privacy_classes": 5, "privacy_candidates": 0, "privacy_confirmed_hits": 0,
        "x1_planning_only": True, "later_lifecycle_paths": 0, "x2_implementation_count": 0, "outcomes_observed": False,
        "interpretation": "exact staged Git-blob owner-scope review only; restage this stable receipt and rerun tests before commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
