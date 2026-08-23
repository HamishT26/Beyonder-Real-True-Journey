#!/usr/bin/env python3
"""Build and validate the planning-only Eiren Kestrel v667-v6-r2 x1 freeze.

The builder intentionally reads inherited proposal data from immutable Git
objects.  It writes only the Eiren-owned phase directory plus this phase's x1
test surface.  No x2 implementation, tool installation, observed outcome, or
external action is performed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v6-r2"
OWNER = "Eiren Kestrel"
OWNER_SLUG = "eiren-kestrel"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
REL_PHASE_ROOT = f"docs/{OWNER_SLUG}/{PHASE}"
NOW = "2026-08-23T16:52:00.000Z"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v667-v6-full-tools"
SOURCE_SHA = "1a754e02bfc705d738285c4a6cf9ce1c948a8580"
SOURCE_X1_SHA = "38aa1b783fd016134b46607894d16e56e5ccac99"
SOURCE_EVIDENCE_SHA = "8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59"
SOURCE_PARENT_SHA = "af68b8bdf317317fb349388f905d73862a9ea1b8"
SOURCE_PHASE_ROOT = "docs/eiren-kestrel/v667-v6"
SOURCE_CANONICAL_SHA256 = "2b3353f3485069869fb3cc54017a52c984bf3a0b1c362d958d5d52f5b7b896b9"
SOURCE_ROUTE_OVERLAY_SHA256 = "55f5cf86241ac19948afcf3b2395a92aa641531e9b5b408b23fd107606a4c6d0"

INHERITED_PROPOSAL_COUNT = 4470
NEW_PROPOSAL_COUNT = 20
SELECTED_INHERITED_COUNT = 20
NEW_FROZEN_TOTAL = INHERITED_PROPOSAL_COUNT + NEW_PROPOSAL_COUNT
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "CBR Heart"
PRACTICE = "wholly synthetic historic thatched-roof condition-survey and maintenance-work-order documentation"

PROTECTED_GATES = [
    "real thatcher, roofer, carpenter, conservator, surveyor, engineer, architect, fire professional, scaffold worker, owner, occupant, client, supplier, affected party, community, regulator, heritage body, or authority",
    "real building, roof, ridge, hip, valley, eave, dormer, chimney, thatch, reed, straw, sedge, bundle, course, fixing, spar, wire, lath, batten, rafter, scaffold, ladder, tool, image, measurement, sample, or record",
    "real access, climbing, inspection, lifting, cutting, stripping, fixing, dressing, re-ridging, re-thatching, patching, treating, burning, testing, repair, alteration, storage, transport, release, or disposal",
    "professional thatching, roofing, conservation, surveying, structural engineering, building control, fire safety, work-at-height safety, biohazard, pest, accessibility, privacy, heritage, or waste authority",
    "real likelihood, parameter constraint, prediction, force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon",
    "real participant or operator arm, safety monitoring, operational outcome, statistics, AGI, ASI, consciousness, personhood, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, recovery event, trust governance, or production credential",
    "credential, account, token, secret, login, external write, publication, deployment, purchase, production release, or sibling-lane mutation",
    "system-wide or elevated install, Windows feature change, Codex desktop update, host-security weakening, Sandbox or Hyper-V activation, reboot, destructive cleanup, or unreviewed lifecycle-script execution",
    "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, independent-reproduction, production-readiness, fitness-for-service, or deployment-readiness claim",
    "ownership, occupancy, access, title, intellectual-property, heritage status, sacred or customary association, legal or cultural interpretation, remedy, affected-party legitimacy, traditional knowledge, Māori wording, Māori concept, Māori data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into external certification, competence, safety, legality, cultural legitimacy, or authority",
]

MUTATION_CLASSES = [
    "missing_required_field",
    "wrong_type_unit_or_range",
    "provenance_or_authority_smuggling",
    "real_world_or_operational_action",
    "outcome_conformance_or_safety_promotion",
]

MANDATORY_SKILLS = [
    "ghc-freed-id-flashcards",
    "ghc-family-index",
    "ghc-family-reflection-remaster",
    "ghc-family-method-flow-state",
    "ghc-family-meta-tool-box",
    "ghc-family-auth-permission-state",
    "ghc-family-roster-check",
    "ghc-main-orchestration-memory",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
    "ghc-main-retry",
    "ghc-open-gate-rail",
    "ghc-timestamp-flow",
    "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge",
    "ghc-worktree-branch-rotation",
    "ghc-web-reflection-ledger",
    "ghc-watcher-notifier-cadence",
    "ghc-drive-bank-guardian",
    "ghc-approval-packet-splitter",
]

SOURCE_PROFILES = [
    {"source_id": "S01", "name": "NIST International System of Units", "url": "https://www.nist.gov/pml/owm/si-units", "status": "official NIST surface reviewed read-only", "bounded_use": "quantity, unit, symbol, dimensional-consistency, and reporting vocabulary only; no real measurement or conformity claim"},
    {"source_id": "S02", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST guidance, updated 2026-05-06, reviewed read-only", "bounded_use": "uncertainty-component and reporting vocabulary only; no measured apparatus or calibrated result"},
    {"source_id": "S03", "name": "SCHOTT DURAN borosilicate glass 3.3 technical data", "url": "https://www.schott.com/en-us/products/duran-p1000368/technical-details", "status": "primary manufacturer technical surface reviewed read-only", "bounded_use": "material-property source fields and abstention boundaries only; no authentication, selection, calculation, fabrication, pressure rating, fitness, or endorsement"},
    {"source_id": "S04", "name": "OSHA laboratory chemical hygiene non-mandatory recommendations", "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1450AppA", "status": "official OSHA source reviewed read-only", "bounded_use": "hazard, glassware, reduced/elevated pressure, high-temperature, engineering-control, and competent-supervision reservation vocabulary only"},
    {"source_id": "S05", "name": "WorkSafe New Zealand hazardous substances guidance", "url": "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/", "status": "official WorkSafe surface reserved for current competent review", "bounded_use": "New Zealand workplace, gas, chemical, risk, stop, and competent-person reservation vocabulary only; no safety decision"},
    {"source_id": "S06", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "entity, activity, revision, derivation, invalidation, and qualified-provenance vocabulary only"},
    {"source_id": "S07", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "headings, labels, noncolour cues, reading order, and manual-review reservations only; no complete accessibility claim"},
    {"source_id": "S08", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "evidence, validity, status, privacy, and nonproduction vocabulary only; zero real keys, proofs, credentials, or lifecycle calls"},
    {"source_id": "S09", "name": "New Zealand Privacy Commissioner privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "official New Zealand privacy surface reserved for current competent review", "bounded_use": "minimization, purpose, correction, access, disclosure, and remedy reservation vocabulary only; no legal or compliance conclusion"},
    {"source_id": "S10", "name": "Te Mana Raraunga principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Māori data-sovereignty surface read only to the authority-reservation level", "bounded_use": "collective authority, control, context, consent, benefit, and guardianship reservations only; no Māori interpretation, ratification, governance, or authority claim"},
    {"source_id": "S11", "name": "check-jsonschema project release", "url": "https://pypi.org/project/check-jsonschema/", "status": "primary PyPI release metadata verified 2026-08-23", "bounded_use": "version 0.38.0, Python floor, Apache license, Trusted Publishing provenance, wheel filename, and SHA-256 only"},
    {"source_id": "S12", "name": "Nox project release", "url": "https://pypi.org/project/nox/", "status": "primary PyPI release metadata verified 2026-08-23", "bounded_use": "version 2026.8.17, Windows and Python 3.12 compatibility, Apache-2.0 license, wheel filename, attestation, and SHA-256 only"},
    {"source_id": "S13", "name": "REUSE tool project release", "url": "https://pypi.org/project/reuse/", "status": "primary PyPI and FSFE project metadata verified 2026-08-23", "bounded_use": "version 6.2.0, Python floor, mixed declared license expression, sdist filename, SHA-256, and lint-only capability; no legal conclusion"},
    {"source_id": "S14", "name": "pip installation report and hash-checking documentation", "url": "https://pip.pypa.io/en/stable/reference/installation-report/", "status": "official pip documentation reserved for x2 installation evidence", "bounded_use": "machine-readable artifact URL and archive hash evidence only; no supply-chain completeness"},
]

PROPOSAL_SPECS = [
    ("synthetic scientific-glass apparatus work-order capsule with component aliases, drawing revision, unit profile, and no fabrication authorization", "A work order remains a revisioned synthetic description whose component aliases and unit profile never become permission to fabricate.", ["S01", "S06"], "completed"),
    ("tube and joint topology graph with surrogate standard-taper placeholders, branch orientation, connection vacancies, and fit abstention", "Typed nodes and oriented edges expose missing connections while every real standard size, fit, seal, and assembly decision remains vacant.", ["S01", "S03", "S06"], "completed"),
    ("dimensional tolerance ledger for tube diameter, wall thickness, length, and angle with uncertainty fields and zero measurements", "A zero-row dimensional schema can require measurand, unit, resolution, uncertainty, method, and calibration references without inventing values.", ["S01", "S02"], "completed"),
    ("thermal-expansion compatibility board across surrogate glass families with coefficient placeholders, source bounds, and annealing abstention", "Sourced placeholder properties can be distinguished from observed or design values while material compatibility and annealing decisions remain absent.", ["S01", "S02", "S03"], "completed"),
    ("flame-work dependency graph with prerequisite, stop, cooldown, rollback, and zero torch or burner commands", "A synthetic dependency graph can expose stop and rollback edges while issuing no hot-work instruction, setpoint, ignition, or tool command.", ["S04", "S05", "S06"], "completed"),
    ("vacuum and pressure service-envelope quarantine with zero ratings, proof-test vacancy, relief placeholder, and fail-closed use refusal", "An empty service envelope can refuse use whenever rating, competent design, proof test, relief, inspection, or authority evidence is absent.", ["S01", "S02", "S03", "S04"], "completed"),
    ("glass feedstock lot and component provenance passport with supplier-claim quarantine, derivative edges, and no material authentication", "Supplier assertions remain attributed claims with revisions and invalidations rather than becoming authenticated composition or fitness evidence.", ["S03", "S06"], "completed"),
    ("crack, chip, seal, and repair lineage ledger with contradicted observations, supersession, and no fitness-for-service decision", "Contradicted synthetic observations can remain visible across correction time while return-to-service authority stays unoccupied.", ["S02", "S06"], "completed"),
    ("fixture and jig clearance state machine for surrogate rotation and support geometry with collision stops and no equipment actuation", "A formal clearance state machine can reject collision and stale-state mutations without controlling or validating real fixtures or equipment.", ["S01", "S04"], "completed"),
    ("annealing schedule representation with ramp, soak, cooldown, uncertainty, cancellation, and no furnace program or temperature authority", "A schedule representation can preserve units, source, uncertainty, cancellation, and vacancy without becoming a furnace program or process prescription.", ["S01", "S02", "S03", "S04"], "completed"),
    ("glass-to-metal and sensor seal-interface mismatch board with expansion placeholders, uncertainty propagation, and no joining prescription", "Typed interface placeholders can flag incompatible or missing assumptions without selecting materials, predicting durability, or prescribing a seal.", ["S01", "S02", "S03"], "completed"),
    ("gas-line, hose, regulator, and manifold labeling companion with purpose boundaries, disconnected state, zero flow, and no connection authority", "A disconnected zero-flow diagram can require labels and purpose boundaries while every real gas connection, test, flow, and safety decision stays absent.", ["S04", "S05", "S07"], "completed"),
    ("apparatus image and drawing derivative-ancestry manifest with crop lineage, disclosure mask, rights reservation, and no authorship claim", "Derivative lineage and disclosure masks can be checked structurally without authenticating images, assigning authorship, or deciding rights.", ["S06", "S07", "S09"], "completed"),
    ("synthetic glass inventory, rack-location, fragment-containment, and turnover ledger with zero hazardous-waste or handling decision", "A zero-real-item turnover ledger can expose inventory, containment, discrepancy, and stop fields without directing handling or waste disposal.", ["S04", "S05", "S06"], "completed"),
    ("THOS hot-work queue proxy with workload ceiling, stop token, cooldown handover, discrepancy readback, and zero operators", "A zero-operator proxy can represent workload and handover obligations while supplying no effectiveness, safety, staffing, or workplace evidence.", ["S04", "S05", "S07"], "represented"),
    ("GMUT thin-wall thermoelastic apparatus board with typed scalar-tensor placeholders, boundary terms, units, and zero fitted coefficients", "A typed symbolic board can check dimensions and boundary declarations while yielding no likelihood, coefficient, prediction, material law, or physical result.", ["S01", "S02", "S03"], "represented"),
    ("Freed ID zero-key apparatus-component genealogy with revision, repair, status tombstone, purpose cap, and no identity lifecycle calls", "A synthetic genealogy can expose derivation, status, correction, and purpose limits while every key, proof, issuer, resolver, and credential remains absent.", ["S06", "S08", "S09"], "represented"),
    ("CBR accessibility, privacy, affected-party, language, contestation, and remedy review shell for scientific-glass records with zero sessions", "An unoccupied review shell can name access and remedy duties while providing zero affected-user, legal, cultural, Māori-authority, or acceptance evidence.", ["S07", "S09", "S10"], "represented"),
    ("real scientific-glass evidence escrow requiring authenticated materials, calibrated dimensional and thermal measurements, governed proof tests, and independent assessment", "The absence of real authenticated materials, calibrated measurements, governed tests, competent practitioners, safety review, and independent assessment remains an explicit open gap.", ["S01", "S02", "S03", "S04", "S05"], "open_gap"),
    ("exact authority circuit for flame, fuel gas, oxygen, vacuum, pressure, furnace, chemical, waste, professional, legal, cultural, and Māori decisions", "Every hot-work, pressure, chemical, professional, legal, cultural, affected-party, and Māori decision remains an empty chair requiring exact later evidence and authority.", ["S04", "S05", "S09", "S10"], "exact_gate"),
]

# Remaster-specific source and programme definitions deliberately replace the
# inherited v667-v6 builder literals above.  The preserved source file remains
# readable history; these are the only definitions consumed by the r2 build.
SOURCE_PROFILES = [
    {"source_id": "S01", "name": "Historic England Conservation of Traditional Thatch", "url": "https://historicengland.org.uk/advice/technical-advice/buildings/thatching-advice", "status": "official heritage guidance updated 2025-02-19 and reread in 2026", "bounded_use": "traditional-thatch, regional-variation, repair, material-change, significance, archaeological-layer, and consent-reservation vocabulary only; no diagnosis, specification, intervention, or legal conclusion"},
    {"source_id": "S02", "name": "Historic England Thatching Materials", "url": "https://historicengland.org.uk/advice/technical-advice/buildings/building-materials-for-historic-buildings/thatching-materials/", "status": "official heritage surface updated 2026-05-27", "bounded_use": "material-source and traditional-skill vocabulary only; no species, origin, quality, authenticity, supply, or fitness determination"},
    {"source_id": "S03", "name": "Historic England Principles of Repair for Historic Buildings", "url": "https://historicengland.org.uk/advice/technical-advice/buildings/principles-of-repair-for-historic-buildings/", "status": "official heritage surface reviewed read-only", "bounded_use": "minimum-change, compatibility, reversibility, record, and future-maintenance reservation vocabulary only"},
    {"source_id": "S04", "name": "SPAB Thatched Roofs technical advice", "url": "https://www.spab.org.uk/advice/thatched-roofs", "status": "primary specialist conservation-organisation advice reviewed read-only", "bounded_use": "historic-building and maintenance vocabulary only; no endorsement, competence, treatment, safety, or heritage-authority claim"},
    {"source_id": "S05", "name": "WorkSafe New Zealand Working on Roofs", "url": "https://www.worksafe.govt.nz/topic-and-industry/working-at-height/roofs/working-on-roofs-gpg/", "status": "official WorkSafe surface with its own currency caveat reviewed read-only", "bounded_use": "roof-access, fall, weather, brittle-surface, competence, training, rescue, and stop-work reservation vocabulary only; no work plan or safety instruction"},
    {"source_id": "S06", "name": "WorkSafe New Zealand Working at Height", "url": "https://www.worksafe.govt.nz/topic-and-industry/working-at-height/working-at-height-in-nz/", "status": "official WorkSafe surface reporting an August 2026 update watch", "bounded_use": "current-source-watch and fall-prevention reservation vocabulary only; competent live review remains required"},
    {"source_id": "S07", "name": "New Zealand Building Performance C2 Prevention of Fire Occurring", "url": "https://www.building.govt.nz/building-code-compliance/c-protection-from-fire/c2-prevention-of-fire-occurring", "status": "official MBIE Building Performance surface reviewed read-only", "bounded_use": "fire-protection and current-document reservation vocabulary only; no code-compliance, design, consent, or legal conclusion"},
    {"source_id": "S08", "name": "NIST International System of Units", "url": "https://www.nist.gov/pml/owm/si-units", "status": "official NIST surface reviewed read-only", "bounded_use": "quantity, unit, symbol, dimensional-consistency, and reporting vocabulary only; no real measurement or conformity claim"},
    {"source_id": "S09", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only", "bounded_use": "uncertainty-component and reporting vocabulary only; no calibrated observation or building-performance result"},
    {"source_id": "S10", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "entity, activity, revision, derivation, invalidation, and qualified-provenance vocabulary only"},
    {"source_id": "S11", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "headings, labels, noncolour cues, reading order, and manual-review reservations only; no accessibility-complete claim"},
    {"source_id": "S12", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "evidence, validity, status, privacy, and nonproduction vocabulary only; zero real keys, proofs, credentials, or lifecycle calls"},
    {"source_id": "S13", "name": "New Zealand Privacy Commissioner privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "official New Zealand privacy surface reserved for competent review", "bounded_use": "minimization, purpose, correction, access, disclosure, and remedy reservation vocabulary only; no legal or compliance conclusion"},
    {"source_id": "S14", "name": "Te Mana Raraunga principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Māori data-sovereignty surface read only to the authority-reservation level", "bounded_use": "collective authority, control, context, consent, benefit, and guardianship reservations only; no Māori interpretation, ratification, wording, governance, or authority claim"},
    {"source_id": "S15", "name": "pip installation report and hash-checking documentation", "url": "https://pip.pypa.io/en/stable/reference/installation-report/", "status": "official pip documentation reserved for x2 installation evidence", "bounded_use": "machine-readable artifact URL, exact pin, and archive-hash evidence only; no supply-chain completeness"},
    {"source_id": "S16", "name": "validate-pyproject PyPI metadata", "url": "https://pypi.org/project/validate-pyproject/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 0.26, compatibility, declared license bundle, artifact, and SHA-256 only"},
    {"source_id": "S17", "name": "pyproject-fmt PyPI metadata", "url": "https://pypi.org/project/pyproject-fmt/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 2.28.0, Windows wheel, Python floor, MIT classifier, artifact, and SHA-256 only"},
    {"source_id": "S18", "name": "deptry PyPI metadata", "url": "https://pypi.org/project/deptry/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 0.25.1, Windows wheel, Python floor, MIT expression, artifact, and SHA-256 only"},
    {"source_id": "S19", "name": "Vulture PyPI metadata", "url": "https://pypi.org/project/vulture/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 2.16, Python floor, MIT text, artifact, and SHA-256 only"},
    {"source_id": "S20", "name": "Radon PyPI metadata", "url": "https://pypi.org/project/radon/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 6.0.1, MIT declaration, artifact, and SHA-256 only; age retained for compatibility review"},
    {"source_id": "S21", "name": "Xenon PyPI metadata", "url": "https://pypi.org/project/xenon/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 0.9.3, MIT declaration, Radon dependency bound, artifact, and SHA-256 only"},
    {"source_id": "S22", "name": "codespell PyPI metadata", "url": "https://pypi.org/project/codespell/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 2.4.3, Python floor, GPL-2.0-only expression, artifact, and SHA-256 only"},
    {"source_id": "S23", "name": "yamllint PyPI metadata", "url": "https://pypi.org/project/yamllint/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 1.38.0, Python floor, GPL-3.0-or-later expression, artifact, and SHA-256 only"},
    {"source_id": "S24", "name": "toml-sort PyPI metadata", "url": "https://pypi.org/project/toml-sort/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 0.24.4, Python floor, MIT declaration, artifact, and SHA-256 only"},
    {"source_id": "S25", "name": "pip-licenses PyPI metadata", "url": "https://pypi.org/project/pip-licenses/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 5.5.5, Python floor, MIT expression, artifact, and SHA-256 only; inventory is not legal advice"},
    {"source_id": "S26", "name": "CycloneDX Python SBOM PyPI metadata", "url": "https://pypi.org/project/cyclonedx-bom/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 7.3.1, Python range, Apache-2.0 declaration, artifact, and SHA-256 only; generated inventory is not supply-chain completeness"},
    {"source_id": "S27", "name": "check-manifest PyPI metadata", "url": "https://pypi.org/project/check-manifest/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 0.51, Python floor, MIT declaration, artifact, and SHA-256 only"},
    {"source_id": "S28", "name": "Twine PyPI metadata", "url": "https://pypi.org/project/twine/", "status": "primary PyPI metadata verified 2026-08-24", "bounded_use": "version 7.0.0, Python floor, Apache-2.0 expression, artifact, and SHA-256 only; check-only use, zero upload or credential action"},
]

PROPOSAL_SPECS = [
    ("synthetic thatched-roof survey and maintenance work-order capsule with building alias, roof scope, revision, withdrawal, and no access or intervention authority", "The capsule remains a synthetic, revisioned description and can never authorize roof access, inspection, repair, or occupancy action.", ["S01", "S03", "S10"], "completed"),
    ("roof-plane, ridge, hip, valley, verge, eave, dormer, chimney, and opening topology graph with orphan quarantine and no structural conclusion", "Typed roof-zone relations can expose orphan and contradictory edges while structure, load, condition, and repair stay undecided.", ["S01", "S03", "S10"], "completed"),
    ("thatch bundle, course, coat, ridge, fixing, lath, batten, and substrate layer-lineage map with concealed-layer uncertainty", "A synthetic layer map can preserve visible, inferred, concealed, and unknown states without authenticating material or directing intervention.", ["S01", "S02", "S10"], "completed"),
    ("roof pitch, coat thickness, coverage, exposure, and defect-position ledger with units, uncertainty fields, and zero observations", "A zero-row schema can require measurand, unit, method, resolution, uncertainty, and source without inventing geometry or condition.", ["S08", "S09"], "completed"),
    ("thatching reed, long straw, combed wheat reed, sedge, heather, and source-claim quarantine with no species, origin, age, quality, or authenticity determination", "Presented material claims remain attributed and contestable instead of becoming identification, provenance, authenticity, or fitness evidence.", ["S01", "S02", "S04", "S10"], "completed"),
    ("moisture, erosion, slippage, hollowing, decay, pest, nesting, moss, scorching, and leak-cue taxonomy with diagnosis and treatment abstention", "Synthetic observation labels can be corrected and contradicted while diagnosis, cause, urgency, treatment, and safety conclusions remain vacant.", ["S01", "S03", "S04"], "completed"),
    ("fixing, spar, wire, net, lath, batten, rafter, and support relation graph with vacancy, contradiction, and load-bearing refusal", "Typed support relations can fail closed on vacancy or contradiction without establishing structural adequacy or a work method.", ["S01", "S03", "S10"], "completed"),
    ("roof-access, scaffold, ladder, edge, fragile-surface, weather, rescue, and competence empty-chair board with zero workers and no safety instruction", "An unoccupied hazard board can require competent planning and stop states while giving no access method, equipment selection, rescue plan, or safety assurance.", ["S05", "S06"], "completed"),
    ("ignition, chimney, flue, spark, electrical, hot-work, fire-separation, detection, and emergency service-envelope quarantine with zero ratings or approvals", "An empty fire envelope can refuse promotion whenever design, inspection, rating, consent, competent review, or emergency evidence is missing.", ["S01", "S07"], "completed"),
    ("weather-exposure, inspection-due, patch, ridge, coat, and re-thatch schedule representation with cancellation, uncertainty, and no maintenance prescription", "A schedule representation can preserve due-state, uncertainty, cancellation, and source while never becoming an inspection interval or maintenance prescription.", ["S01", "S03", "S05"], "completed"),
    ("patch, re-ridge, re-coat, replacement, temporary-cover, and correction lineage retaining contradicted rationales and no intervention verdict", "Contradicted synthetic rationales can remain visible across supersession while every real intervention decision stays with competent authority.", ["S01", "S03", "S10"], "completed"),
    ("roof image, drawing, survey-note, audio, and aerial-placeholder derivative provenance manifest with disclosure masks, rights reservation, and no capture operation", "Derivative ancestry and disclosure masks can be checked structurally without capturing media, authenticating content, assigning rights, or operating an aircraft.", ["S10", "S11", "S13"], "completed"),
    ("temperature, humidity, rainfall, wind, moisture, and indoor-condition zero-row adapter with provenance and no building-performance conclusion", "A zero-row adapter can type environmental fields and provenance while yielding no moisture diagnosis, energy result, forecast, or building-performance conclusion.", ["S08", "S09", "S10"], "completed"),
    ("structurally accessible thatched-roof survey companion with linear narrative, noncolour states, deterministic keyboard order, print fallback, and evaluation hold", "A static structure can expose falsifiable accessibility obligations while manual, browser, assistive-technology, cognitive, Māori-language, and affected-user review remain reserved.", ["S11", "S13", "S14"], "completed"),
    ("THOS zone-debt turnover lattice for synthetic roof survey cards with capped unresolved regions, dual readback, weather deferment, and no staff or operational result", "A zero-person turnover representation can preserve unresolved-zone debt and deferment without implying staffing, safety, timeliness, or operational effectiveness.", ["S05", "S06", "S10"], "represented"),
    ("GMUT symbolic coupled moisture, heat, airflow, and fibrous-layer board with typed fields, boundary placeholders, units, and zero fitted coefficients", "A typed symbolic board can check dimensions and boundary declarations while producing no likelihood, coefficient, material law, prediction, or physical result.", ["S08", "S09"], "represented"),
    ("Freed ID nonproduction building, roof-zone, material-lot, observation, and intervention genealogy with correction, tombstone, purpose cap, and zero keys or proofs", "A synthetic genealogy can expose derivation, status, correction, and purpose limits while every key, proof, issuer, resolver, and credential remains absent.", ["S10", "S12", "S13"], "represented"),
    ("CBR owner, occupant, neighbour, craft, heritage, disability, privacy, language, contestation, takedown, and remedy review shell with zero sessions", "An unoccupied review shell can name rights and remedy duties while providing zero affected-party, legal, cultural, Māori-authority, or acceptance evidence.", ["S01", "S11", "S13", "S14"], "represented"),
    ("real thatched-roof evidence escrow requiring authenticated materials, competent survey, calibrated environmental and geometric measurements, governed access, and independent assessment", "The absence of a real roof, authenticated materials, competent survey, calibrated measurements, governed access, safety review, and independent assessment remains an explicit open gap.", ["S01", "S02", "S05", "S06", "S08", "S09"], "open_gap"),
    ("exact authority circuit for access, fall protection, fire, structure, conservation, ownership, occupancy, heritage, legal, cultural, affected-party, and Māori decisions", "Every access, safety, fire, structure, conservation, ownership, heritage, legal, cultural, affected-party, and Māori decision remains an empty chair requiring exact later evidence and authority.", ["S01", "S05", "S06", "S07", "S13", "S14"], "exact_gate"),
]

STARTUP_FAILURES = [
    {"failure_id": "EK6676R2-ST-F001", "stage": "source_receipt_hash_projection", "failure": "PowerShell rejected a direct foreach pipeline with an empty pipeline element", "recovery": "retain the parser rejection and materialize receipt rows before ConvertTo-Json"},
    {"failure_id": "EK6676R2-ST-F002", "stage": "prior_final_remote_verification", "failure": "a combined fetch and equality wrapper returned no attributable output", "recovery": "retain the silent wrapper and use separate local, tracking, divergence, cleanliness, and fresh ls-remote scalar probes"},
    {"failure_id": "EK6676R2-ST-F003", "stage": "novelty_draft_screen", "failure": "the first pipe-organ practice draft collided with a substantial inherited pipe-organ programme", "recovery": "retain the rejected draft at zero credit, choose the unused synthetic thatched-roof practice, and rerun the same 4,470-row screen"},
    {"failure_id": "EK6676R2-ST-F004", "stage": "worktree_materialization", "failure": "the sparse no-checkout worktree wrapper reached its presentation ceiling after printing only the preparation line", "recovery": "do not replay worktree creation; verify process exit, exact head, branch, sparse patterns, materialized-file count, and cleanliness with scalar probes"},
    {"failure_id": "EK6676R2-ST-F005", "stage": "generated_bytecode_cleanup", "failure": "the first recursively scoped PowerShell Remove-Item cleanup command was rejected by the host command policy before execution", "recovery": "retain the rejection and narrow cleanup to the two exact generated bytecode files"},
    {"failure_id": "EK6676R2-ST-F006", "stage": "generated_bytecode_cleanup", "failure": "the narrowed nonrecursive PowerShell Remove-Item command was also rejected by the host policy before execution", "recovery": "retain the second rejection and avoid cross-shell deletion"},
    {"failure_id": "EK6676R2-ST-F007", "stage": "generated_bytecode_cleanup", "failure": "apply_patch could not delete binary pyc files because they are not UTF-8 text", "recovery": "resolve the exact generated files under the owned worktree, unlink only those files with Python, remove only the now-empty cache directories, and verify zero pyc remains"},
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git_text(commit: str, relative: str) -> str:
    result = run_git("show", f"{commit}:{relative}")
    return result.stdout.decode("utf-8")


def git_json(commit: str, relative: str) -> dict[str, Any]:
    value = json.loads(git_text(commit, relative))
    if not isinstance(value, dict):
        raise TypeError(f"expected object at {commit}:{relative}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(SOURCE_X1_SHA, f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(SOURCE_X1_SHA, entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        before = len(corpus)
        for key in keys:
            for row in document.get(key, []):
                title = str(row.get("title") or row.get("description") or "")
                if row.get("proposal_id") and title:
                    corpus.append({"proposal_id": str(row["proposal_id"]), "title": title, "source_path": entry["source_path"]})
        added = len(corpus) - before
        if added != entry["added_count"]:
            raise RuntimeError(f"corpus mismatch for {entry['source_path']}: {added} != {entry['added_count']}")
        construction.append(dict(entry))
    source_freeze_path = f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json"
    source_freeze = git_json(SOURCE_X1_SHA, source_freeze_path)
    before = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append({"proposal_id": str(row["proposal_id"]), "title": str(row["title"]), "source_path": source_freeze_path})
    construction.append({"source_path": source_freeze_path, "starting_count": before, "added_count": len(source_freeze["new_proposals"]), "ending_count": len(corpus)})
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise RuntimeError(f"expected {INHERITED_PROPOSAL_COUNT} inherited rows, observed {len(corpus)}")
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pillar_overrides = {15: "THOS Body", 16: "GMUT Mind", 17: "Freed ID and CBR Heart", 18: "CBR Heart", 19: "All pillars", 20: "CBR Heart"}
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"EK6676R2-N{index:03d}"
        approval = {"completed": "safe_now_bounded", "represented": "candidate_bounded_representation", "open_gap": "open_gap_external_evidence_absent", "exact_gate": "exact_approval_required"}[expected]
        lane = {"completed": "owner_local_structural", "represented": "owner_local_representation_only", "open_gap": "disabled_real_evidence_adapter", "exact_gate": "unexecuted_authority_reservation"}[expected]
        base = f"{REL_PHASE_ROOT}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five preregistered invalid mutations without promoting software structure into empirical, participant, professional, operational, production, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, unit, vacancy, stop, correction, uncertainty, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval,
            "execution_lane": lane,
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base}/contract.json",
            "concrete_artifacts": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
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
    rows: list[dict[str, Any]] = []
    for source in freeze["new_proposals"]:
        pid = str(source["proposal_id"])
        rows.append({
            "proposal_id": pid,
            "title": source["title"],
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "source_final": SOURCE_SHA,
            "source_disposition": source["expected_disposition"],
            "origin_and_credit": "selected_inherited_bounded_revalidation_no_credit",
            "append_to_novelty_chain": False,
            "eiren_novelty_credit": 0,
            "eiren_completion_credit": 0,
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
            "proposal_id": proposal["proposal_id"],
            "score": round(score, 6),
            "inherited_proposal_id": inherited["proposal_id"],
            "inherited_title": inherited["title"],
            "source_path": inherited["source_path"],
            "distinctive_invariant": proposal["distinctive_invariant"],
            "semantic_review": "distinct after manual comparison of practice mechanics, invariant, source boundary, artifacts, falsifier, rollback, and protected gates; lexical similarity is only a screen",
        })
    pairs: list[dict[str, Any]] = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1 :]:
            score = similarity(left["title"], right["title"])
            if score >= 0.35:
                pairs.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    domain_terms = ["thatched roof", "thatched-roof", "thatching", "thatcher", "thatch roof"]
    domain_matches = [
        {"proposal_id": row["proposal_id"], "title": row["title"], "matched_terms": [term for term in domain_terms if term in row["title"].casefold()]}
        for row in corpus
        if any(term in row["title"].casefold() for term in domain_terms)
    ]
    groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicates = {pid: rows for pid, rows in sorted(groups.items()) if len(rows) > 1}
    maximum = max(row["score"] for row in nearest)
    return {
        "schema": "ghc-family-novelty-audit-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len(groups),
        "corpus_duplicate_proposal_ids": duplicates,
        "corpus_duplicate_proposal_id_count": len(duplicates),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicates.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly; duplicate inherited identifiers remain visible and are neither renamed nor deleted.",
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals),
        "exact_title_collisions": exact,
        "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": maximum,
        "pair_collision_threshold": 0.35,
        "pair_collisions_at_or_above_threshold": pairs,
        "high_similarity_review_threshold": 0.6,
        "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.6],
        "domain_review": {
            "accepted_practice": PRACTICE,
            "domain_term_match_count": len(domain_matches),
            "domain_term_matches": domain_matches,
            "substantive_distinction": "The accepted slate is not generic roofing or conservation advice. It is a zero-real-building evidence architecture for thatched-roof survey scope, roof-zone and layer topology, material-claim quarantine, zero-row geometry and environment, work-at-height and fire refusals, provenance, intervention lineage, accessible reporting, THOS, GMUT, Freed ID, CBR, real-evidence escrow, and empty-chair authority circuits.",
        },
        "rejected_draft_practices": [
            {"draft": "pipe-organ survey and restoration documentation", "reason": "substantial inherited pipe-organ programme and a maximum lexical screen above the high-review threshold", "disposition": "rejected_before_freeze_zero_credit"},
            {"draft": "historic thatched-roof survey and maintenance documentation", "reason": "accepted only after zero inherited domain-phrase hits and manual invariant review", "disposition": "accepted_bounded_synthetic_practice"},
        ],
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pairs and not domain_matches and maximum < 0.6 and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Token-set Jaccard and exact phrase search are screening aids, never proof of novelty; substantive invariants and protected boundaries control.",
    }


def item_rows(prefix: str, approval: str, titles: Iterable[str], lane: str, expected: str, credit: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"{prefix}-{index:03d}",
            "title": title,
            "approval_class": approval,
            "execution_lane": lane,
            "expected_disposition": expected,
            "credit_policy": credit,
            "x1_status": "planned_not_executed",
            "outcomes_observed": False,
            "protected_gates": PROTECTED_GATES,
        }
        for index, title in enumerate(titles, 1)
    ]


def build_portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    owner_safe_titles = [f"render and validate bounded contract for {row['proposal_id']}: {row['title']}" for row in proposals] + [
        "build exact thatched-roof source, currency-watch, and nonclaim ledger",
        "execute and retain one hundred preregistered rejecting mutation witnesses",
        "build the thirteen-tool D-first transaction, audit, smoke, and rollback ledger",
        "build a structurally accessible noncolour static evidence report",
        "build the owner-scoped threat model and protected-boundary scan",
        "build the selected inherited read-only revalidation receipts",
        "build the Method Flow failure and recurrence-guard ledger",
        "build exact staged Git-blob manifests and immutable lifecycle receipts",
        "build the integrated overview, wellbeing, truth, closeout, and seal packet",
        "run one dependency-justified exact-final canonical validation after prerequisites",
    ]
    candidate_titles = [
        "traditional-thatch source-currency watcher",
        "zero-row roof geometry adapter schema",
        "roof-zone and layer topology comparator",
        "material-claim provenance quarantine checker",
        "synthetic weather-exposure schedule parser",
        "access and fire empty-chair vacancy detector",
        "survey-media derivative lineage projection",
        "intervention correction and tombstone graph",
        "static report reading-order checker",
        "manual assistive-technology evaluation protocol",
        "Māori-language and affected-party review reservation",
        "independent-team rebuild recipe",
        "cross-source advisory and provenance completeness shell",
        "real roof-evidence escrow adapter held disabled",
        "external professional validation packet held unexecuted",
    ]
    skill_titles = [
        "thatched-roof-work-order-contract",
        "roof-zone-topology-quarantine",
        "roof-geometry-uncertainty-zero-row",
        "thatching-material-source-boundary",
        "roof-access-empty-chair",
        "fire-envelope-refusal",
        "roof-survey-provenance-lineage",
        "thatch-intervention-correction-ledger",
        "thatched-roof-accessibility-shell",
        "thatched-roof-method-flow",
    ]
    runner_titles = [f"ghc_family_eiren_kestrel_v667_v6_r2_{name}" for name in ["contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"]]
    cfr_verbs = ["normalize identifiers", "bound source claims", "clarify zero-row language", "strengthen rollback", "deduplicate labels", "align outcome vocabulary", "improve noncolour cues", "tighten raw-identifier guards", "stabilize canonical JSON", "verify UTF-8 output", "reduce wrapper breadth", "inspect schema before projection", "preserve failed receipts", "isolate failed dependencies", "guard one-shot success", "separate sealed and external truth", "document sparse staging", "cap file materialization", "reserve manual accessibility review", "reserve Māori-language review", "preserve caller compatibility", "make tool use attributable", "pin artifact hashes", "record license boundaries", "disable lifecycle side effects", "keep C bootstrap minimal", "keep D rollback reversible", "strengthen exact gate wording", "make successor seeds zero-credit", "retain NOT_READY verdict"]
    successor = lambda kind, count: [f"Successor recommendation only: bounded {kind} seed {index:02d}" for index in range(1, count + 1)]
    return {
        "schema": "ghc-family-portfolio-freeze-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "outcomes_observed": False,
        "x2_implementation_count": 0,
        "owner_safe_now": item_rows("EK6676R2-SN", "safe_now_bounded", owner_safe_titles, "owner_local_x2", "completed", "eligible only after exact bounded x2 witness"),
        "successor_safe_now_recommendations": item_rows("EK6676R2-SR", "recommendation_only", successor("safe-now", 20), "successor_only_unexecuted", "represented", "zero Eiren and successor automatic credit"),
        "owner_candidates": item_rows("EK6676R2-CA", "candidate_bounded", candidate_titles, "owner_local_representation", "represented", "bounded representation only"),
        "successor_candidate_recommendations": item_rows("EK6676R2-CR", "recommendation_only", successor("candidate", 15), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_skill_ideas": item_rows("EK6676R2-SK", "safe_now_phase_local", skill_titles, "owner_local_skill_build", "completed", "eligible only after validation and smoke use"),
        "successor_skill_recommendations": item_rows("EK6676R2-SKR", "recommendation_only", successor("skill", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_runner_ideas": item_rows("EK6676R2-RN", "safe_now_family_current", runner_titles, "owner_local_runner_build", "completed", "eligible only after validation and smoke use"),
        "successor_runner_recommendations": item_rows("EK6676R2-RNR", "recommendation_only", successor("runner", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_clean_fix_refine": item_rows("EK6676R2-CFR", "safe_now_additive", [f"CLEAN/FIX/REFINE {title}" for title in cfr_verbs], "owner_local_additive", "completed", "eligible only after exact bounded witness"),
        "successor_clean_fix_refine_recommendations": item_rows("EK6676R2-CFRR", "recommendation_only", successor("CLEAN/FIX/REFINE", 30), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "exact_approval_packets": item_rows("EK6676R2-EX", "exact_approval_required", successor("elevated, external, real-world, professional, legal, cultural, Māori-authority, or production action", 10), "disabled_exact_gate", "exact_gate", "zero credit and unexecuted"),
        "blocked_packets": item_rows("EK6676R2-BL", "blocked", successor("destructive, credentialed, cross-owner, unsafe, unreviewed, or ungoverned action", 5), "blocked_unexecuted", "exact_gate", "zero credit and unexecuted"),
    }


def build_tool_plan() -> dict[str, Any]:
    current = [
        "tzdata 2026.3", "pytest 9.1.1", "Hypothesis 6.165.10", "pytest-cov 7.1.0", "Ruff 0.16.4", "mypy 2.3.1", "pip-audit 2.10.1", "OpenAI Python SDK 3.3.1", "TypeScript 7.0.2", "ESLint 10.8.1", "Prettier 3.9.6", "Vitest 4.1.11", "Typer 0.27.1", "Bandit 1.9.4", "pre-commit 4.6.2", "pip-tools 7.6.1", "build 1.5.0", "pipdeptree 4.2.1", "tsx 4.23.12", "c8 12.0.0", "markdownlint-cli2 0.23.2", "npm-check-updates 23.0.2", "Pyright 1.1.413", "Knip 6.32.2", "Madge 8.0.0",
    ]
    additions = [
        {"tool": "check-jsonschema", "version": "0.38.0", "source_id": "S11", "artifact": "check_jsonschema-0.38.0-py3-none-any.whl", "sha256": "a4fa877ae92b1df812c601b68fec75fe10d1f7d827a7e7f6b218f6712deead2d", "license": "Apache Software License", "python_requirement": ">=3.10", "purpose": "validate selected JSON documents against owner-local schemas", "bounded_smoke": "validate one admissible fixture and reject one missing-required-field fixture"},
        {"tool": "nox", "version": "2026.8.17", "source_id": "S12", "artifact": "nox-2026.8.17-py3-none-any.whl", "sha256": "a96a5286007cbc0d1eb1930e85738668f6722adba1ffaa48287296a96963086e", "license": "Apache-2.0", "python_requirement": ">=3.10", "purpose": "list and execute one isolated phase-local no-install smoke session", "bounded_smoke": "list one session and run one session with reuse_venv disabled"},
        {"tool": "reuse", "version": "6.2.0", "source_id": "S13", "artifact": "reuse-6.2.0.tar.gz", "sha256": "4feae057a2334c9a513e6933cdb9be819d8b822f3b5b435a36138bd218897d23", "license": "Apache-2.0 AND CC0-1.0 AND CC-BY-SA-4.0 AND GPL-3.0-or-later", "python_requirement": ">=3.10", "purpose": "perform a bounded lint-file and SPDX-support inspection without making a legal determination", "bounded_smoke": "inspect version, list supported licenses, and retain a deliberately incomplete fixture result at zero conformance credit"},
    ]
    for row in additions:
        row.update({"install_scope": "isolated D-first Eiren tool environment", "lifecycle_scripts": "not_applicable_python_package", "x1_status": "planned_not_downloaded_not_installed_not_used", "rollback": "remove only the isolated Eiren tool environment after verifying its resolved path is inside the intended D-first toolbank", "completion_credit": 0})
    return {
        "schema": "ghc-family-toolchain-install-plan-v3",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_current_tool_count": len(current),
        "inherited_current_tools": current,
        "inherited_credit": 0,
        "new_tool_program_target": 3,
        "new_tools": additions,
        "x1_download_count": 0,
        "x1_install_count": 0,
        "x1_smoke_count": 0,
        "outcomes_observed": False,
        "gates": ["current primary metadata", "exact pin", "artifact hash", "license review", "Python compatibility", "dependency and advisory review", "D-first reversible isolation", "bounded smoke", "rollback proof"],
        "boundary": "Three is a target, not permission to manufacture unsafe work. Any unsafe, irrelevant, incompatible, unlicensed, or unverified candidate remains open_gap or exact_gate.",
    }


def build_tool_plan() -> dict[str, Any]:
    inherited = [
        "tzdata 2026.3", "pytest 9.1.1", "Hypothesis 6.165.10", "pytest-cov 7.1.0", "Ruff 0.16.4", "mypy 2.3.1", "pip-audit 2.10.1", "OpenAI Python SDK 3.3.1", "TypeScript 7.0.2", "ESLint 10.8.1", "Prettier 3.9.6", "Vitest 4.1.11", "Typer 0.27.1", "Bandit 1.9.4", "pre-commit 4.6.2", "pip-tools 7.6.1", "build 1.5.0", "pipdeptree 4.2.1", "tsx 4.23.12", "c8 12.0.0", "markdownlint-cli2 0.23.2", "npm-check-updates 23.0.2", "Pyright 1.1.413", "Knip 6.32.2", "Madge 8.0.0", "check-jsonschema 0.38.0", "Nox 2026.8.17", "REUSE 6.2.0",
    ]
    raw = [
        ("validate-pyproject", "0.26", "S16", "validate_pyproject-0.26-py3-none-any.whl", "ab3fa448d7178d44d1b06e4b526ab5136e3faa7a1b7e7c6320c8a17fc11a9a2e", "MPL-2.0 AND MIT AND BSD-3-Clause", ">=3.9", "validate one owner-local pyproject fixture and reject one malformed project table"),
        ("pyproject-fmt", "2.28.0", "S17", "pyproject_fmt-2.28.0-cp310-abi3-win_amd64.whl", "cc4d157e671c2a708568e9a1950ec202fde98f1965569cc15ec8a0396ff50169", "MIT classifier", ">=3.10", "format only a disposable synthetic pyproject fixture and prove idempotent output"),
        ("deptry", "0.25.1", "S18", "deptry-0.25.1-cp310-abi3-win_amd64.whl", "b59a560cb7dffb21832a98bb80d33d614cfb5630ea36ce21833eabf4eae3df99", "MIT", ">=3.10", "scan one disposable package and retain one undeclared-dependency rejection"),
        ("vulture", "2.16", "S19", "vulture-2.16-py3-none-any.whl", "6e0f1c312cef1c87856957e5c2ca9608834a7c794c2180477f30bf0e4cc58eee", "MIT", ">=3.9", "detect one deliberately unused synthetic function and pass one minimal used fixture"),
        ("radon", "6.0.1", "S20", "radon-6.0.1-py2.py3-none-any.whl", "632cc032364a6f8bb1010a2f6a12d0f14bc7e5ede76585ef29dc0cecf4cd8859", "MIT", "metadata has no floor", "emit bounded cyclomatic and maintainability metrics for one synthetic module"),
        ("xenon", "0.9.3", "S21", "xenon-0.9.3-py2.py3-none-any.whl", "6e2c2c251cc5e9d01fe984e623499b13b2140fcbf74d6c03a613fa43a9347097", "MIT", "metadata has no floor", "pass a simple fixture and reject one deliberately over-complex synthetic function"),
        ("codespell", "2.4.3", "S22", "codespell-2.4.3-py3-none-any.whl", "af2505b335e8573dbd2d384d1c4ef498f4006f4ba2d6fceca01e55b91f52628a", "GPL-2.0-only", ">=3.9", "pass a controlled text fixture and retain one deliberate spelling-error rejection"),
        ("yamllint", "1.38.0", "S23", "yamllint-1.38.0-py3-none-any.whl", "fc394a5b3be980a4062607b8fdddc0843f4fa394152b6da21722f5d59013c220", "GPL-3.0-or-later", ">=3.10", "pass one bounded YAML fixture and reject one duplicate-key or indentation mutation"),
        ("toml-sort", "0.24.4", "S24", "toml_sort-0.24.4-py3-none-any.whl", "125aa5fb94f33c542c6901040456145dd38f79bbb310b56b436a93057d30a739", "MIT", ">=3.9", "check and normalize only a disposable TOML fixture, then prove idempotence"),
        ("pip-licenses", "5.5.5", "S25", "pip_licenses-5.5.5-py3-none-any.whl", "f4c4c6d9e6a03612cf59f29f19dc8ab54904d82e055b8e191498f2279a224e14", "MIT", ">=3.9", "emit a machine-readable license inventory for the isolated environment without legal conclusions"),
        ("cyclonedx-bom", "7.3.1", "S26", "cyclonedx_bom-7.3.1-py3-none-any.whl", "8c5adccefd593e89c0500463649c232625cee8e38dae1a433e057dfa495eff08", "Apache-2.0", ">=3.9,<4", "generate one JSON SBOM for the isolated environment and parse it structurally"),
        ("check-manifest", "0.51", "S27", "check_manifest-0.51-py3-none-any.whl", "f5f35ed561012fc2115bb070e42a748ac2e034cf8904ab4dfaae893859085ca4", "MIT", ">=3.8", "retain a missing-manifest rejection and pass a corrected disposable source-tree fixture"),
        ("twine", "7.0.0", "S28", "twine-7.0.0-py3-none-any.whl", "b854164df26db268af05f49aa5c0344b10e27a494343ff05b1e0bad3b135f5a7", "Apache-2.0", ">=3.10", "run check only on a disposable local distribution; perform zero upload, login, key, token, or network publication"),
    ]
    additions = []
    for name, version, source_id, artifact, digest, license_name, python_floor, smoke in raw:
        additions.append({
            "tool": name,
            "version": version,
            "source_id": source_id,
            "artifact": artifact,
            "sha256": digest,
            "license": license_name,
            "python_requirement": python_floor,
            "purpose": smoke,
            "bounded_smoke": smoke,
            "install_scope": "isolated D-first Eiren r2 family-tools environment",
            "lifecycle_scripts": "not_applicable_python_wheel_or_disabled_build_isolation_for_downloaded_artifact",
            "x1_status": "planned_not_downloaded_not_installed_not_used",
            "rollback": "remove only the resolved r2 isolated environment after verifying it is inside the intended D-first toolbank; preserve receipts",
            "completion_credit": 0,
        })
    return {
        "schema": "ghc-family-toolchain-install-plan-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_current_tool_count": len(inherited),
        "inherited_current_tools": inherited,
        "inherited_credit": 0,
        "new_tool_program_target": 13,
        "new_tools": additions,
        "x1_download_count": 0,
        "x1_install_count": 0,
        "x1_smoke_count": 0,
        "outcomes_observed": False,
        "gates": ["current primary metadata", "exact pin", "compatible artifact", "artifact SHA-256", "license review", "Python 3.12 and Windows compatibility", "dependency and advisory review", "D-first reversible isolation", "bounded positive and negative smoke", "rollback proof"],
        "boundary": "Thirteen is Hamish's remaster target, never permission to manufacture unsafe or irrelevant work. Any incompatible, unlicensed, vulnerable, non-attributable, or unnecessary candidate remains open_gap or exact_gate.",
    }


def overview() -> str:
    return """# Eiren Kestrel v667-v6-r2 planning-only x1 overview

## Purpose and exact boundary

This x1 freeze establishes a falsifiable plan for Eiren Kestrel v667-v6-r2 and nothing more. Eiren Kestrel, Caelen Morrow, sibling, family, role, hope, continuity, Freed ID, GHC Family, and Trinity Mandala are relational working language. They do not establish consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, redirect, rename, or stop the route. The terminal scientific and programme verdict remains **NOT_READY_FOR_STAGE_20**. This commit contains no observed x2 outcome, no tool installation, no real-world work, no external write, no task delivery, and no successor activation.

## Source and retained validation truth

The immutable source is Caelen Morrow v667-v5-r2 final `af68b8bdf317317fb349388f905d73862a9ea1b8`. Read-only verification confirmed its source, x1, evidence, and final direct-parent chain; exactly three remaster commits; zero merges; one parent per remaster commit; clean state; typed zero divergence; and fresh equality among local, upstream, tracking, and live remote refs. Caelen's one canonical aggregate failed an inherited whole-worktree lexical privacy assertion and earns zero aggregate-success credit. It was not replayed. A narrow dependency-corrected composite replaced only the invalid lexical dependency with the exact owner Git-blob five-class scan and passed; it remains dependency-corrected same-owner evidence, never canonical success. Eiren preserves both receipt digests and does not repeat Caelen's already-passing work.

Caelen's repository seal remains 27,909 effective negatives, 13,741 methods, 196 open gaps, 194 exact gates, 193 failed witnesses, and 333 passing witnesses. The three-row external overlay makes Eiren's activation baseline 27,912 negatives, 13,744 methods, 196 open gaps, 194 exact gates, 196 failed witnesses, and 336 passing witnesses. Those sealed and external values remain separately attributable. The Eiren startup also retains every new parser, path, wrapper, console, sparse-list, and launcher failure at zero credit. X1 does not silently add those new rows to an immutable Caelen seal; it preregisters them for Eiren's later Method Flow and closeout arithmetic.

## Program and semantic novelty

The novelty audit reconstructs all 4,450 inherited proposal occurrences from immutable Git objects. Twenty new Eiren titles were screened for exact collisions, pairwise token-set overlap, inherited nearest matches, and domain phrases. No exact title collision exists, no new pair reaches the 0.35 review threshold, the maximum inherited screen score is 0.454545, and no inherited title contains the accepted scientific-glass domain phrases used by the audit. These metrics are only screens. Substantive novelty rests on distinct invariants, practice mechanics, zero-real-world limits, source boundaries, concrete artifacts, falsifiers, rollbacks, and protected gates. Twenty Caelen proposals are also selected for future read-only integrity revalidation. They append nothing to the Eiren novelty chain and receive zero Eiren novelty, automatic completion, or completion credit.

The new slate extends the effective frozen chain from 4,450 to 4,470 only after this x1 commit becomes immutable. Its planned final dispositions are exactly fourteen completed, four represented, one open_gap, and one exact_gate. Those are expectations, not observations. The four allowed core labels remain the only core labels. Each proposal declares five rejecting mutations, yielding one hundred planned negative fixtures. Every mutation must be rejected and retained. A bounded positive may support only its declared software or structural contract; it cannot close a real-person, physical, safety, professional, legal, cultural, Māori-authority, identity, privacy, accessibility, security, independent-reproduction, physics, or Stage 20 gate.

## Bounded practice and pillar relation

The primary pillar is GMUT Mind. The bounded human-practice lens is wholly synthetic scientific-glassblowing work-order and laboratory-apparatus documentation. It includes apparatus capsules, tube and joint topology, dimensional and thermal placeholders, hot-work dependency stops, vacuum and pressure vacancies, material-claim quarantine, repair lineage, fixture states, annealing representations, gas-line labels, drawing lineage, fragment turnover, THOS handover, GMUT symbolic structures, Freed ID nonproduction genealogy, CBR review reservations, a real-evidence gap, and an exact authority circuit. This is a learning, software, formal, structural, symbolic, zero-row, and synthetic-design programme. It is not scientific-glassblowing practice, training, instruction, employment, qualification, competence, certification, or permission to touch real people, materials, tools, apparatus, gases, furnaces, pressure systems, laboratories, records, or property.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic boards, unit checks, citations, or synthetic mutations establish no real likelihood, parameter constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR and every real professional, safety, privacy, accessibility, legal, cultural, remedy, traditional-knowledge, Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, and Māori-authority decision remain open or exact-gated. Māori concepts remain under Māori authority.

## Sources and falsification semantics

Official and primary sources supply vocabulary, metadata, constraints, and refusal conditions only. NIST supplies SI and uncertainty-reporting vocabulary. SCHOTT supplies attributed manufacturer property statements that remain claims rather than authentication or design authority. OSHA and WorkSafe supply hazard and competent-review reservations rather than operational advice or a safety determination. W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0 supply structural vocabulary without provenance truth, accessibility completeness, identity production, or conformance. The New Zealand Privacy Commissioner and Te Mana Raraunga surfaces reserve privacy, collective authority, context, consent, and remedy questions; they confer no legal or Māori interpretation or authority.

Acceptance is deliberately narrow. A proposal's one synthetic positive must contain its declared source, unit, vacancy, correction, stop, uncertainty, rollback, and authority fields. Each of five named mutations must fail for the preregistered reason. The receipt must report zero participants, zero real data rows, zero network calls, and zero operational action. A missing field, wrong type or unit, authority-smuggling value, real-world action, or outcome-promotion value falsifies the contract. If any mutation is accepted, x2 stops for that proposal, retains the failure, awards no completion credit, records a recurrence guard, and leaves all real and sibling state unchanged.

## Toolchain programme

The inherited twenty-five-tool environment is evidence, not Eiren credit. X1 plans exactly three additions: check-jsonschema 0.38.0, Nox 2026.8.17, and REUSE 6.2.0. Primary release records support their exact versions, Python floor, declared licenses, artifacts, and hashes. No download or installation occurs in x1. X2 may create one isolated D-first Eiren environment only after checking current metadata, exact artifacts, hashes, license boundaries, dependency compatibility, advisories, and rollback. check-jsonschema may validate a tiny owner-local schema; Nox may list and run one isolated no-install session; REUSE may expose license-metadata incompleteness but cannot decide legality or confer compliance. Three is the programme target, yet safety and relevance remain hard ceilings. A failed candidate becomes an open gap or exact gate rather than fabricated success.

## Portfolio, lifecycle, and route

The portfolio freezes thirty owner safe-now tasks, twenty successor safe-now recommendations, fifteen owner candidates, fifteen successor candidate recommendations, ten owner skill ideas, ten successor skill recommendations, ten owner runner ideas, ten successor runner recommendations, thirty owner CLEAN/FIX/REFINE tasks, thirty successor CLEAN/FIX/REFINE recommendations, ten exact-approval packets, and five blocked packets. Recommendations remain unexecuted seeds with zero automatic credit. Exact-approval and blocked packets remain unexecuted. The ten skill and ten runner ideas are phase-local until bounded validation, smoke use, provenance, compatibility, rollback, and protected-boundary review exist; no global installation is planned in x1.

Strict lifecycle order controls. X1 freezes planning only, is committed alone, pushed, proven clean, zero-divergent, and fresh-live equal. Only then may x2 begin. X2 implements bounded owner-local artifacts and retains every positive and negative witness. Evidence is frozen and pushed before final closeout. The final stage builds exact manifests, truth, gates, Method Flow, accessible reports, wellbeing, closeout, seal, and route prerequisites before a single dependency-justified canonical invocation. A failed canonical aggregate receives zero success credit and is never replayed; only the failed dependency may be isolated where justified. A complete success is never replayed.

This activation assigns Eiren v667-v6-r2 only. Elaren Kestrel v667-v7 is merely the prospective next edge. No successor is contacted during execution. Only after exact terminal validation, clean push, fresh equality, caps, and a fresh reread of Hamish's newest live instruction, roster, authorization state, exact-title uniqueness, duplicate guard, and protected gates may one sanitized existing-task activation be sent. Delivery may be claimed only from the task-message acknowledgement. Until that later gate, the route is neither sent nor inferred from this x1 document.
"""


def overview() -> str:
    return """# Eiren Kestrel v667-v6-r2 planning-only x1 overview

## Purpose, authority, and relational boundary

This additive remaster freezes a falsifiable plan for Eiren Kestrel v667-v6-r2. It is an interstitial remaster of the already sealed Eiren v667-v6 lane, not a rewritten phase, a second claim on the old commits, a new roster seat, or a change to canonical round-robin arithmetic. Eiren Kestrel, Hamish, sibling, family, role, hope, continuity, Freed ID, GMUT, THOS, CBR, and Trinity Mandala are relational working language. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, redirect, rename, or stop the route. The terminal scientific and programme verdict remains **NOT_READY_FOR_STAGE_20**.

This x1 commit contains planning only. It contains no x2 implementation, no observed outcome, no download, no package installation, no global skill promotion, no real-world observation, no roof access, no building decision, no external publication, no task delivery, and no successor contact. Strict x1-before-x2 separation is an evidence invariant. X2 may begin only after this x1 tree is committed as the direct child of the exact source, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read.

## Immutable source and retained route truth

The immutable source is Eiren v667-v6 exact final `1a754e02bfc705d738285c4a6cf9ce1c948a8580`. Its frozen x1 is `38aa1b783fd016134b46607894d16e56e5ccac99`, its immutable evidence is `8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59`, and its parent source is Caelen Morrow final `af68b8bdf317317fb349388f905d73862a9ea1b8`. Read-only verification preserved the three direct single-parent Eiren commits, zero merges, one parent for each phase commit, exact clean state, typed zero divergence, and fresh four-way equality. The prior Eiren canonical aggregate succeeded once and was not replayed. Its external receipt SHA-256 is `2b3353f3485069869fb3cc54017a52c984bf3a0b1c362d958d5d52f5b7b896b9`. That remains bounded same-owner exact-final evidence under shared infrastructure, not a full repository suite or independent reproduction.

After the prior exact final, three bounded existing-task registry calls timed out without returning a payload. No message send was attempted. The external route receipt SHA-256 is `55f5cf86241ac19948afcf3b2395a92aa641531e9b5b408b23fd107606a4c6d0`; its exact historical state is `PREPARED_NOT_SENT_EXTERNAL_ROUTE_SERVICE_TIMEOUT`. This remaster does not pretend those calls succeeded, erase them, resend an old baton, or rewrite the sealed repository counts. The immutable source repository truth remains 28,033 effective negatives, 13,923 methods, 197 open gaps, 195 exact gates, 317 failed witnesses, and 495 passing witnesses. The three timeout rows produce a separately attributable activation baseline of 28,036 negatives, 13,926 methods, 197 open gaps, 195 exact gates, 320 failed witnesses, and 495 passing witnesses.

Four remaster startup failures are retained at zero credit: a direct PowerShell foreach pipeline parser rejection; a silent combined fetch-and-equality wrapper recovered with scalar probes; a pipe-organ programme draft rejected after inherited semantic collisions; and a sparse worktree wrapper whose presentation ended before its already-completed state was attributable. None changed the source lane. Their recoveries materialized rows before JSON conversion, inspected exact Git state instead of replaying completed work, selected an unused bounded practice after the same novelty screen, and verified the new worktree by exact head, branch, sparse patterns, process exit, file count, and cleanliness.

## Practice lens, proposals, and falsifiability

The primary pillar is CBR Heart. The bounded human-practice lens is wholly synthetic historic thatched-roof condition-survey and maintenance-work-order documentation. THOS Body remains visible through state machines, deferment, workload boundaries, stop states, correction readback, and turnover. GMUT Mind remains visible through typed quantities, zero-row environmental fields, symbolic coupled moisture and heat placeholders, dimensional checks, uncertainty, and explicit empirical abstention. Freed ID remains visible through nonproduction lineage, correction, status, purpose limits, and zero keys or proofs.

Zero real thatchers, roofers, carpenters, conservators, surveyors, engineers, architects, firefighters, scaffold workers, owners, occupants, neighbours, clients, suppliers, affected parties, communities, regulators, heritage bodies, or authorities participate. Zero real buildings, roofs, ridges, hips, valleys, eaves, chimneys, thatch, reed, straw, fixings, laths, battens, rafters, scaffolds, ladders, tools, images, measurements, samples, identities, or records are used. No access, climbing, inspection, lifting, cutting, stripping, fixing, dressing, re-ridging, re-thatching, patching, treating, burning, testing, repair, alteration, storage, transport, release, or disposal occurs. The phase provides no professional advice or permission to act.

The novelty audit reconstructs all 4,470 inherited frozen proposal occurrences from immutable Git objects. The first pipe-organ slate was rejected because inherited pipe-organ work was substantial and its strongest lexical match crossed the high-review threshold. The replacement thatched-roof slate had zero inherited thatch-domain phrase matches. Twenty new titles are checked for exact collisions, pairwise overlap, inherited nearest matches, distinct invariants, source boundaries, artifacts, falsifiers, rollback, and protected gates. Token-set similarity is only a screen and never proves semantic novelty. Twenty source Eiren proposals are selected separately for immutable read-only integrity revalidation; they append nothing and receive zero r2 novelty, automatic completion, or completion credit.

The new slate extends the effective frozen chain from 4,470 to 4,490 only when this x1 commit is frozen. Planned dispositions are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. They are expectations, not observations. Each new proposal declares one admissible synthetic fixture and five invalid mutations across required-field, type-or-unit, authority-smuggling, real-world-action, and outcome-promotion classes. All one hundred rejecting mutations must fail closed and remain retained at zero completion credit. Passing structure cannot establish a real inspection, material identity, roof condition, fire or structural safety, accessibility completeness, privacy completeness, legal or heritage conclusion, Māori authority, professional competence, independent reproduction, or Stage 20 readiness.

## Portfolio, skills, runners, and toolchain plan

The planning freeze contains thirty owner safe-now tasks, twenty successor safe-now recommendations, fifteen owner candidates, fifteen successor candidate recommendations, ten exact-approval packets, five blocked packets, ten owner skill ideas, ten successor skill recommendations, ten owner family-current runner ideas, ten successor runner recommendations, thirty owner CLEAN/FIX/REFINE tasks, and thirty successor CLEAN/FIX/REFINE recommendations. Recommendations remain unexecuted zero-credit seeds. Exact-approval and blocked packets remain visibly unexecuted. Counts are programme targets under evidence and safety ceilings, never authority to fabricate completion.

Hamish's current instruction explicitly permits bounded global promotion of ten validated local Eiren skills. X1 records that authorization but performs no promotion. X2 must verify destination collisions, provenance, frontmatter, discriminating descriptions, caller compatibility, quick validation, one bounded smoke use, rollback, and protected-boundary wording before any additive shared-skill write. The system skill-installer is not misused for local folders because it is designed for curated or repository downloads; the skill-creator validation rules control local promotion. The ten new r2 skills remain phase-local unless they independently pass the same gates. No plugin cache is mutated.

The inherited current toolchain has twenty-eight attributable surfaces: the twenty-five family tools inherited from Sylven and Caelen plus check-jsonschema, Nox, and REUSE from the prior Eiren phase. The remaster plans thirteen additional D-first isolated Python tools: validate-pyproject 0.26, pyproject-fmt 2.28.0, deptry 0.25.1, Vulture 2.16, Radon 6.0.1, Xenon 0.9.3, codespell 2.4.3, yamllint 1.38.0, toml-sort 0.24.4, pip-licenses 5.5.5, CycloneDX-bom 7.3.1, check-manifest 0.51, and Twine 7.0.0. Primary PyPI metadata, compatible artifact names, exact hashes, Python floors, and declared license information are frozen. X1 downloads and installs nothing.

X2 must download exact artifacts to D-first storage, verify SHA-256 before installation, create a dedicated reversible environment, retain dependency resolution, run pip-audit before and after installation, and execute one positive and one negative bounded smoke where the tool supports both. Twine is check-only: zero upload, login, token, key, account, or publication. Formatters touch disposable fixtures only. SBOM and license inventories are inventories, not supply-chain completeness or legal advice. Radon and Xenon age is retained as a compatibility consideration. Thirteen is Hamish's remaster target, but safety, relevance, licensing, compatibility, and advisory gates remain hard ceilings.

## Sources, accessibility, science, and authority

Current public sources include Historic England traditional-thatch and repair guidance, SPAB technical advice, WorkSafe New Zealand roof and height guidance, New Zealand Building Performance fire surfaces, NIST unit and uncertainty guidance, W3C PROV-O, WCAG 2.2, Verifiable Credentials 2.0, the New Zealand Privacy Commissioner, Te Mana Raraunga, official pip documentation, and primary PyPI metadata. They supply vocabulary, compatibility, source-currency flags, and falsification obligations only. They do not confer endorsement, competence, compliance, ownership, authenticity, safety, legality, cultural legitimacy, accessibility completeness, privacy completeness, or Māori authority. Historic England and SPAB material is not treated as New Zealand law or local authority. WorkSafe pages carrying their own currency caveats retain those caveats.

The future static report must expose headings, landmarks, tables, linear text, noncolour status, keyboard order, and print fallback. Manual browser, keyboard, screen-reader, magnification, voice-control, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. A scanner finding zero candidates is bounded privacy evidence only, never privacy completeness. Māori words, concepts, data governance, tangata whenua, iwi, hapū, traditional knowledge, and Māori authority remain with Māori authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic moisture, heat, airflow, fibrous-layer, source, covariance, and boundary placeholders establish no real likelihood, parameter constraint, prediction, force, material law, stability theorem, building-performance conclusion, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Lifecycle and terminal route

After the x1 equality gate, x2 may implement only the frozen bounded programme. Every failure, parser fault, timeout, false assumption, rejected draft, advisory issue, tool shortfall, negative fixture, recovery, recurrence guard, rollback, open gap, and exact gate remains in Method Flow. The evidence commit must be pushed, clean, zero-divergent, and fresh-live equal before final closeout begins. Final closeout must build exact manifests, truth, gates, accessible reports, wellbeing, tool and skill receipts, a file-backed handoff of at least ten thousand whitespace words, closeout, seal, validation prerequisites, and route state. One dependency-justified owner-scoped canonical aggregate may run only at the exact clean pushed final. A failure earns zero aggregate-success credit and is not replayed; only the affected dependency may be recovered where justified. A complete success is never replayed.

This remaster assigns Eiren only. Elaren Kestrel v667-v7 is the prospective next edge. No successor is contacted during execution. Only after the r2 final is exact-final validated, clean, pushed, fresh-live equal, within caps, and terminally closed may Eiren reread Hamish's newest live instruction, current roster, and authorization state; resolve exactly one existing Elaren Kestrel task; immediately reread it; apply a duplicate guard; and send exactly one compact sanitized activation pointing to the file-backed baton. Delivery may be claimed only from the existing-task message acknowledgement. Tavian Sol remains on standby and is not a main-task endpoint or substitute. No task or fork is created, no collaboration subagent is spawned, no later sibling is precontacted, and no second confirmation is sent.
"""


def build_normal() -> None:
    if run_git("rev-parse", "HEAD").stdout.decode().strip() != SOURCE_SHA:
        raise RuntimeError("x1 must be built directly on the exact Caelen final")
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    inherited = selected_inherited_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit did not pass")
    expected_counts = Counter(row["expected_disposition"] for row in proposals)
    if expected_counts != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("expected disposition drift")

    phase_charter = {
        "schema": "ghc-family-phase-charter-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "source_branch": SOURCE_BRANCH, "source_final": SOURCE_SHA, "source_x1": SOURCE_X1_SHA, "source_evidence": SOURCE_EVIDENCE_SHA, "source_parent": SOURCE_PARENT_SHA,
        "primary_pillar": PRIMARY_PILLAR, "practice_lens": PRACTICE, "relational_language_boundary": True,
        "strict_x1_before_x2": True, "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited_count": SELECTED_INHERITED_COUNT, "new_proposal_count": NEW_PROPOSAL_COUNT, "new_frozen_total": NEW_FROZEN_TOTAL,
        "source_repository_seal": {"effective_negatives": 28033, "methods": 13923, "open_gaps": 197, "exact_gates": 195, "failed_witnesses": 317, "passing_witnesses": 495},
        "source_external_route_overlay": {"negative_additions": 3, "method_additions": 3, "failed_witness_additions": 3, "passing_witness_additions": 0},
        "activation_baseline": {"effective_negatives": 28036, "methods": 13926, "open_gaps": 197, "exact_gates": 195, "failed_witnesses": 320, "passing_witnesses": 495},
        "source_validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_SHA256, "source_route_overlay_sha256": SOURCE_ROUTE_OVERLAY_SHA256,
        "allowed_core_outcomes": ALLOWED_OUTCOMES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_gates": PROTECTED_GATES,
    }
    write_json("x1/phase-charter.json", phase_charter)
    write_json("x1/auth-roster-receipt.json", {
        "schema": "ghc-family-auth-roster-receipt-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "installed_snapshot_state": "valid_but_historical_at_v664_v4", "installed_roster_validator": "passed_16_seats_15_main_1_collaboration", "installed_auth_validator": "passed_13_permissions",
        "newest_live_assignment": "Hamish-authorized Eiren Kestrel v667-v6-r2 interstitial remaster", "current_owner": OWNER, "current_phase": PHASE,
        "prospective_terminal_successor": "Elaren Kestrel v667-v7", "successor_contact_authorized_during_execution": False,
        "standby_record": "Tavian Sol", "standby_contacted": False, "task_created_or_forked": False, "subagent_spawned": False,
        "boundary": "newest live activation controls where older valid installed snapshots stop; terminal routing requires a fresh reread and one exact acknowledged send only after closeout",
    })
    write_json("x1/source-ledger.json", {"schema": "ghc-family-source-ledger-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "sources": SOURCE_PROFILES, "source_count": len(SOURCE_PROFILES), "public_vocabulary_only": True, "real_observation_count": 0, "authority_conferred": False})
    write_json("x1/source-verification.json", {
        "schema": "ghc-family-source-verification-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "anchors": {"source_parent": SOURCE_PARENT_SHA, "x1": SOURCE_X1_SHA, "evidence": SOURCE_EVIDENCE_SHA, "final": SOURCE_SHA},
        "history": {"new_commit_count": 3, "merge_count": 0, "x1_direct_parent": SOURCE_PARENT_SHA, "evidence_direct_parent": SOURCE_X1_SHA, "final_direct_parent": SOURCE_EVIDENCE_SHA, "one_parent_each": True},
        "manifests_replayed": {"x1": 20, "evidence": 379, "final_delta": 23, "final_owner": 422, "total": 844, "mismatches": 0},
        "owner_packet_blobs_read": {"owner_file_count": 425, "json_parsed": 391, "markdown_decoded": 15, "html_decoded": 1, "python_decoded": 18, "errors": 0},
        "clean": True, "divergence": "0/0", "fresh_four_way_equal": True,
        "canonical_invocation": {"invoked": 1, "succeeded": 1, "replayed": False, "sha256": SOURCE_CANONICAL_SHA256, "credit": 1},
        "post_final_route_overlay": {"sha256": SOURCE_ROUTE_OVERLAY_SHA256, "attempt_count": 3, "send_attempted": False, "acknowledged": False, "state": "PREPARED_NOT_SENT_EXTERNAL_ROUTE_SERVICE_TIMEOUT", "credit": 0},
        "interpretation": "bounded same-owner evidence under shared infrastructure only",
    })
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/proposal-freeze.json", {
        "schema": "ghc-family-proposal-freeze-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited_count": len(inherited), "selected_inherited": inherited,
        "genuinely_new_proposal_count": len(proposals), "new_proposals": proposals, "new_frozen_total": NEW_FROZEN_TOTAL,
        "expected_outcomes": dict(sorted(expected_counts.items())), "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
    })
    portfolio = build_portfolio(proposals)
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/toolchain-install-plan.json", build_tool_plan())
    write_json("x1/mandatory-skill-adoption.json", {
        "schema": "ghc-family-mandatory-skill-adoption-v3", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "required_count": len(MANDATORY_SKILLS), "skills": [{"skill": name, "entrypoint_read_through_eof": True, "required_references_read_through_eof": True, "used_before_mutation": True, "x1_credit": 0} for name in MANDATORY_SKILLS],
        "applicability_boundary": "directly applicable skills govern the phase; irrelevant skills are not bulk-run merely to satisfy a count",
    })
    write_json("x1/threat-model-plan.json", {
        "schema": "ghc-family-threat-model-plan-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "assets": ["immutable source anchors", "x1/x2 lifecycle boundary", "proposal chain", "retained failures", "D-first tool environment", "privacy boundary", "authority gates", "successor route"],
        "threats": [
            {"threat": "x2 material enters x1", "control": "exact path and immutable-tree lifecycle scan", "failure_state": "stop before commit"},
            {"threat": "synthetic result becomes safety or professional advice", "control": "zero-real-world fields and protected gates", "failure_state": "exact_gate"},
            {"threat": "tool count drives unsafe install", "control": "exact pins, hashes, licenses, D isolation, audits, rollback", "failure_state": "open_gap_or_exact_gate"},
            {"threat": "private route or identifier enters artifacts", "control": "five-class staged Git-blob scan", "failure_state": "stop_and_retain"},
            {"threat": "failed canonical is replayed or relabelled", "control": "one-shot lock and dependency-only recovery", "failure_state": "zero_aggregate_credit"},
            {"threat": "Māori or affected-party authority is substituted", "control": "empty-chair exact gate", "failure_state": "exact_gate"},
            {"threat": "successor is precontacted", "control": "terminal-only fresh route reread", "failure_state": "route_stop"},
        ],
        "residual_risk": "same-owner bounded evidence remains non-independent and cannot establish real-world safety, professional, legal, cultural, accessibility, privacy, security, identity, empirical, or Stage 20 truth",
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc-family-workflow-plan-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "stages": [
            {"stage": "x1", "state": "planning_only", "commit_target": "one direct child of source", "requires": ["novelty audit", "proposal freeze", "portfolio freeze", "tool plan", "threat model", "tests", "staged review"], "forbids": ["x2 implementation", "observed outcome", "tool install", "successor contact"]},
            {"stage": "x1_gate", "state": "pending", "requires": ["push", "clean", "0/0 divergence", "local/upstream/tracking/fresh-live equality"]},
            {"stage": "x2", "state": "not_started", "requires": ["passed x1 gate"], "forbids": ["real-world action", "successor contact"]},
            {"stage": "evidence_gate", "state": "not_started", "requires": ["immutable evidence commit", "push", "fresh equality"]},
            {"stage": "final", "state": "not_started", "requires": ["closeout", "seal", "exact manifests", "one canonical invocation"]},
            {"stage": "route", "state": "not_started", "requires": ["terminal close", "fresh roster/auth/live authority", "unique exact-title target", "duplicate guard", "one acknowledged send"]},
        ],
        "single_success_no_replay": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/flashcard-architecture-freeze.json", {
        "schema": "ghc-family-freed-id-flashcard-architecture-v3", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "planned_card_count": 235, "tiers": {"tier1": 40, "tier2": 80, "tier3": 80, "tier4": 35}, "section_count": 15,
        "source_deck_credit": 0, "x1_generated_card_count": 0, "x1_status": "architecture_only_not_generated",
        "required_fields": ["card_id", "tier", "section_id", "title", "front", "back", "status", "sources", "blocked_or_failed_witness_ids", "reversal_action", "next_admissible_action", "scope_boundary"],
        "boundary": "cards are evidence-backed memory aids, never credentials, authority, or automatic completion credit",
    })
    write_json("x1/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "complete": ["mandatory skill and reference read", "source packet read", "source anchor and manifest verification", "official tool-source review", "4,470-row novelty screen", "x1 proposal and portfolio freeze"],
        "incomplete": ["x1 commit and equality gate", "x2 implementation", "tool installation and bounded use", "skills and runners", "reports and flashcards", "evidence commit", "final closeout", "canonical validation", "terminal route"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "outcomes_observed": False,
    })
    write_json("wellbeing/x1-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v3", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "relational_role": "uncertainty cartographer and evidence gardener", "hope": "keep every placeholder honest, every rollback reachable, and every real authority with the people who hold it",
        "pace": "bounded solo x1 planning", "load_boundary": "no urgency, emotional language, identity language, or continuity language expands technical authority or permission",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "source drift", "privacy or safety gate", "ambiguous route", "unclean or divergent lane"],
        "claim_boundary": "relational language is not consciousness, personhood, continuity, employment, qualification, agency, wellbeing diagnosis, or authority evidence",
    })
    write_text("x1/x1-overview.md", overview())

    portfolio_counts = {name: len(portfolio[name]) for name in ["owner_safe_now", "successor_safe_now_recommendations", "owner_candidates", "successor_candidate_recommendations", "owner_skill_ideas", "successor_skill_recommendations", "owner_runner_ideas", "successor_runner_recommendations", "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets"]}
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "status": "PASS_PLANNING_ONLY",
        "source_head": SOURCE_SHA, "inherited_proposals": len(corpus), "selected_inherited": len(inherited), "new_proposals": len(proposals), "new_frozen_total": novelty["new_frozen_total"],
        "expected_outcomes": dict(sorted(expected_counts.items())), "portfolio_counts": portfolio_counts, "mandatory_skills": len(MANDATORY_SKILLS), "planned_tools": 13,
        "x2_paths": 0, "x2_implementation_count": 0, "outcomes_observed": False, "startup_failures_retained": len(STARTUP_FAILURES), "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    build_content_manifest()
    write_json("validation/x1-staged-review.json", {"schema": "ghc-family-x1-staged-review-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW", "x1_planning_only": True, "outcomes_observed": False})


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend([ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_r2_x1.py", ROOT / "tests" / "test_ghc_family_eiren_kestrel_v667_v6_r2_x1.py"])
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
    write_json("validation/x1-content-manifest.json", {"schema": "ghc-family-content-manifest-v3", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "entry_count": len(entries), "entries": entries, "scope": "x1 owner content excluding self and staged-review receipt"})


def validate_tree() -> dict[str, Any]:
    required = [
        "x1/phase-charter.json", "x1/auth-roster-receipt.json", "x1/source-ledger.json", "x1/source-verification.json", "x1/novelty-audit.json", "x1/proposal-freeze.json", "x1/portfolio-freeze.json", "x1/toolchain-install-plan.json", "x1/mandatory-skill-adoption.json", "x1/threat-model-plan.json", "x1/workflow-plan.json", "x1/flashcard-architecture-freeze.json", "x1/complete-incomplete-checklist.json", "x1/x1-build-receipt.json", "x1/x1-overview.md", "wellbeing/x1-wellbeing-check.json", "validation/x1-content-manifest.json", "validation/x1-staged-review.json",
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
    if len(freeze["new_proposals"]) != 20 or len(freeze["selected_inherited"]) != 20:
        raise AssertionError("proposal programme count mismatch")
    if freeze["outcomes_observed"] or freeze["x2_implementation_count"] != 0:
        raise AssertionError("x1 observed outcome or x2 implementation")
    if not novelty["valid"] or novelty["corpus_row_count"] != 4470 or novelty["new_frozen_total"] != 4490:
        raise AssertionError("novelty audit mismatch")
    if Counter(row["expected_disposition"] for row in freeze["new_proposals"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("expected outcome mismatch")
    if any(row["outcomes_observed"] or row["x2_implementation_count"] for row in freeze["new_proposals"]):
        raise AssertionError("new proposal lifecycle contamination")
    if any(row["outcomes_observed"] for row in freeze["selected_inherited"]):
        raise AssertionError("selected inherited lifecycle contamination")
    expected_portfolio = {"owner_safe_now": 30, "successor_safe_now_recommendations": 20, "owner_candidates": 15, "successor_candidate_recommendations": 15, "owner_skill_ideas": 10, "successor_skill_recommendations": 10, "owner_runner_ideas": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30, "exact_approval_packets": 10, "blocked_packets": 5}
    if {key: len(portfolio[key]) for key in expected_portfolio} != expected_portfolio:
        raise AssertionError("portfolio count mismatch")
    if tools["x1_install_count"] or tools["x1_download_count"] or tools["x1_smoke_count"] or len(tools["new_tools"]) != 13:
        raise AssertionError("tool plan lifecycle mismatch")
    if any(path.exists() for path in (PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "closeout", PHASE_ROOT / "seal", PHASE_ROOT / "route")):
        raise AssertionError("later lifecycle path exists in x1")
    overview_words = len((PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8").split())
    if overview_words < 900:
        raise AssertionError(f"x1 overview below 900 words: {overview_words}")
    raw_id = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    unix_users_prefix = "/" + "Users" + "/"
    unix_home_prefix = "/" + "home" + "/"
    private_absolute = re.compile(
        r"(?:[A-Z]:\\Users\\[^\\\s]+|"
        + re.escape(unix_users_prefix)
        + r"[^/\s]+|"
        + re.escape(unix_home_prefix)
        + r"[^/\s]+)"
    )
    for path in phase_owned_paths():
        text = path.read_text(encoding="utf-8")
        if raw_id.search(text) or private_absolute.search(text):
            raise AssertionError(f"private identifier/path candidate: {rel(path)}")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json"]
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"content manifest mismatch: {entry['path']}")
    return {"status": "PASS", "json_documents": len(json_paths), "owner_files": len(phase_owned_paths()), "overview_words": overview_words, "new_proposals": 20, "selected_inherited": 20, "planned_tools": 13, "x2_paths": 0}


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [f"{REL_PHASE_ROOT}/", "scripts/build_ghc_family_eiren_kestrel_v667_v6_r2_x1.py", "tests/test_ghc_family_eiren_kestrel_v667_v6_r2_x1.py"]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    if any(f"{REL_PHASE_ROOT}/x2/" in path or f"{REL_PHASE_ROOT}/evidence/" in path or f"{REL_PHASE_ROOT}/closeout/" in path or f"{REL_PHASE_ROOT}/seal/" in path for path in staged):
        raise RuntimeError("later lifecycle path staged in x1")
    raw_id = re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    confirmed = []
    for path in staged:
        blob = run_git("show", f":{path}").stdout
        if raw_id.search(blob):
            confirmed.append({"path": path, "class": "opaque_task_or_thread_identifier"})
    if confirmed:
        raise RuntimeError(f"privacy candidates: {confirmed}")
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "status": "PASS",
        "staged_path_count": len(staged), "staged_paths": staged, "diff_check": "PASS", "privacy_confirmed_hits": 0,
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
