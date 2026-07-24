#!/usr/bin/env python3
"""Frozen Caelen Morrow v654-v4 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v654-v4"
OWNER = "Caelen Morrow"
PRONOUNS = "they/them"
ROLE = "bounded continuity and evidence steward"
HOPE = "leave a clear, corrigible record that makes later review easier"
BRANCH = "codex/GHC-Family/caelen-morrow-v654-v4-full-tools"
PHASE_ROOT = "docs/caelen-morrow/v654-v4"

SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v654-v3-full-tools"
SOURCE_HEAD = "53354454690c40c5688aaeb86dc46a61ee079fe7"
SOURCE_ORIGIN = "74da3812daadcd6d452e899b7142dc87d684aba4"
SOURCE_X1 = "0c53bce867ec5259d9b7de8c14b92b07b678641f"
SOURCE_X1_INITIAL = "d948425f4a6d30b523849a1b5430bcc1531ce054"
SOURCE_EVIDENCE = "780acdf2225624080463c274dc88c001f5a65d54"
SOURCE_FIRST_CLOSEOUT = SOURCE_HEAD
SOURCE_EXTERNAL_RECEIPT_SHA256 = (
    "1c74c375ab48ba04cc713c3baac45aec55b93c8c8846634f68de78dd73bc9c81"
)
PRIOR_FROZEN = 1750
INHERITED_SEALED_NEGATIVES = 11155
INHERITED_EXTERNAL_NEGATIVES = 0
INHERITED_NEGATIVES = 11155
INHERITED_OPEN_GAPS = 82
INHERITED_ROUTE_OPEN_GAPS = 0
INHERITED_EXACT_GATES = 81
INHERITED_METHODS = 42
INHERITED_FAILED_WITNESSES = 42
INHERITED_PASSING_WITNESSES = 42
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "custom garment alteration and repair studio intake, fibre and component compatibility, "
    "measurement and seam documentation, machine and chemical holds, accessible status, "
    "workload control, fitting reservations, and shift handover, as a synthetic learning "
    "and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_or_operators",
    "professional_tailoring_garment_product_safety_machinery_and_hazardous_substance_authority",
    "production_identity_and_interoperability",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_and_remedy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(number, title, slug, pillar, disposition, source_ids, mission):
    if disposition == "open_gap":
        approval = "candidate_real_data_standards_access_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-query and zero-row refusal receipt with no account, key, purchase, "
            "download, ingest, measurement, fit, likelihood, posterior, constraint, prediction, "
            "or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no garment-safety, "
            "tailoring, product-recall, ownership, body-measurement privacy, warranty, remedy, "
            "legal, cultural, data-governance, affected-party, or Māori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject every preregistered mutation and retain represented status with zero real "
            "participant, operational, professional, production, interoperability, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject every preregistered mutation and emit only the declared bounded software, "
            "symbolic, formal, structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6544-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing "
            "unsupported scientific, operational, identity, accessibility, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, "
            "erases a failure, crosses an approval boundary, or promotes beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": (
            "Stop the proposal, retain every failed witness, rewrite no history, and leave external, "
            "sibling, participant, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1750_frozen_proposals": (
            "The complete 1,750-row inherited title audit found no proposal combining the "
            f"custom-garment-alteration mechanism frozen here: {title}."
        ),
    }


_P = [
    (1, "Garment alteration intake item identifier, presented-owner claim placeholder, condition, detachable pieces, custody, privacy minimization, and work-start hold", "garment-intake-custody", "Freed ID and CBR Heart", "completed", ["SRC-ISO3758", "SRC-PRIVACY-ACT"], "garment intake, custody, and privacy minimization"),
    (2, "Garment alteration work order, requested change, measurement version, fitting-consent placeholder, quote revision, scope correction, readback, and release hold", "alteration-scope-hold", "Freed ID and CBR Heart", "completed", ["SRC-ISO8559", "SRC-CGA", "SRC-PRIVACY-ACT"], "alteration scope, measurement version, and correction hold"),
    (3, "Garment fibre-content and care-label source, symbol version, missing or conflicting mark, proposed treatment, substitution, and refusal ledger", "fibre-care-refusal", "Freed ID and CBR Heart", "completed", ["SRC-ISO3758"], "fibre and care-label provenance refusal"),
    (4, "Garment seam allowance, seam type, stitch type, thread ticket, sample coupon, expected load direction, mismatch, and unpick hold", "seam-stitch-hold", "THOS Body", "completed", ["SRC-ISO4915", "SRC-ISO4916", "SRC-ISO13935"], "seam, stitch, thread, and sample-coupon hold"),
    (5, "Garment needle system, needle size and point, fabric structure, thread relation, machine state, damage signal, and substitution refusal", "needle-fabric-refusal", "THOS Body", "completed", ["SRC-ISO4915", "SRC-WORKSAFE-MACHINERY"], "needle, fabric, thread, and machine compatibility refusal"),
    (6, "Garment interlining and adhesive identifier, substrate, heat and pressure ceiling, test coupon, residue signal, delamination risk, and fusing hold", "interlining-fusing-hold", "THOS Body", "completed", ["SRC-ISO3758", "SRC-BIPM-SI"], "interlining and fusing compatibility hold"),
    (7, "Garment dye and colourfastness placeholder, hidden-area sample, cleaning-agent identity, transfer signal, treatment boundary, and alteration refusal", "dye-treatment-refusal", "Freed ID and CBR Heart", "completed", ["SRC-ISO3758", "SRC-WORKSAFE-HAZ"], "dye, cleaning-agent, and treatment refusal"),
    (8, "Garment zipper, button, snap or hook identifier, size, material, attachment geometry, load direction, replacement relation, and fitment refusal", "garment-fastener-fitment", "THOS Body", "completed", ["SRC-ISO4916", "SRC-CGA"], "garment fastener compatibility and fitment refusal"),
    (9, "Garment pattern piece, grainline, nap, stripe or plaid match, notch relation, mirrored state, cut authorization placeholder, and recut hold", "pattern-alignment-hold", "THOS Body", "completed", ["SRC-ISO4916"], "pattern grainline, nap, match, and recut hold"),
    (10, "Garment hem reference, intended length, floor or shoe context placeholder, balance point, drape proxy, correction delta, and release hold", "hem-balance-hold", "THOS Body", "completed", ["SRC-ISO8559", "SRC-BIPM-SI"], "hem reference, balance, and drape-proxy hold"),
    (11, "Garment fitting body-measurement field, anatomical definition, unit, purpose, source, correction lineage, retention limit, and privacy hold", "measurement-privacy-hold", "Freed ID and CBR Heart", "completed", ["SRC-ISO8559", "SRC-BIPM-SI", "SRC-PRIVACY-ACT"], "body-measurement definition, lineage, minimization, and privacy hold"),
    (12, "Garment pressing temperature and steam setting, material layer, press-cloth state, tool status, time ceiling, test coupon, and scorch refusal", "pressing-scorch-refusal", "THOS Body", "completed", ["SRC-ISO3758", "SRC-WORKSAFE-MACHINERY", "SRC-BIPM-SI"], "pressing, steam, tool, and scorch refusal"),
    (13, "Sewing machine guard, power state, presser foot, needle and bobbin relation, jam state, maintenance placeholder, isolation, and stop-work board", "sewing-machine-stop-work", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "sewing-machine guarding, isolation, and stop-work structure"),
    (14, "Garment studio scissors, rotary cutter, pins and needles, condition, count, container, missing-sharp signal, cleanup, and handover hold", "sharps-handover-hold", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "cutting-tool and sharps count, containment, and handover hold"),
    (15, "Garment spot-treatment substance, safety-data-sheet version, batch, decanted-container label, exposure and spill state, waste route, and service hold", "spot-treatment-boundary", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "spot-treatment identity, SDS, spill, and waste hold"),
    (16, "Garment delicate-material or prior-repair condition, unknown fibre, embellishment, weakened area, sentiment placeholder, quarantine, and specialist escalation", "delicate-garment-quarantine", "Freed ID and CBR Heart", "completed", ["SRC-ISO3758", "SRC-CGA"], "delicate material, prior repair, and unknown-condition quarantine"),
    (17, "Replacement-closure bulletin applicability matrix with edition, style-lot key, evidence gap, isolation bin, escalation state, remedy reservation, and no-release decision", "garment-notice-quarantine", "Freed ID and CBR Heart", "completed", ["SRC-CGA"], "supplier-bulletin applicability matrix and isolation decision"),
    (18, "Inclusive alteration progress card with semantic stage order, hold explanation, recovery action, text-and-shape encoding, reflow, focus order, and human accessibility review reserve", "accessible-alteration-status", "THOS Body", "completed", ["SRC-WCAG22"], "inclusive progress-card structure and reserved human review"),
    (19, "Alteration studio capacity ledger with queued job class, blocked dependency, work-in-progress ceiling, cognitive and physical load flag, rest checkpoint, responsibility transfer, and next-shift acknowledgement", "garment-workload-handover", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "capacity, load, rest, and responsibility-transfer controls"),
    (20, "Garment fitting appointment, pinning proximity, mobility and communication need placeholder, support-person option, consent reservation, pause signal, and return receipt", "fitting-reservation", "Freed ID and CBR Heart", "completed", ["SRC-PRIVACY-ACT", "SRC-WCAG22"], "fitting, accessibility, consent, and pause reservation"),
    (21, "GMUT woven-textile lattice field, warp and weft node, strain proxy, boundary displacement, anisotropy tensor, unit, and observation-firewall board", "gmut-textile-lattice", "GMUT Mind", "completed", ["SRC-ISO13934", "SRC-BIPM-SI"], "typed woven-textile lattice-field obligations"),
    (22, "GMUT garment seam graph field, stitch node, thread edge, seam-line curvature, boundary load, rupture proxy, unit, and observation-firewall board", "gmut-seam-graph", "GMUT Mind", "completed", ["SRC-ISO13935", "SRC-BIPM-SI"], "typed seam-graph field obligations"),
    (23, "GMUT garment drape shell field, panel curvature, gravity placeholder, contact boundary, bending-stiffness proxy, unit, and observation-firewall board", "gmut-drape-shell", "GMUT Mind", "completed", ["SRC-ISO13934", "SRC-BIPM-SI"], "typed garment-drape shell-field obligations"),
    (24, "THOS garment alteration intake, measurement correction, fitting hold, scope readback, workload budget, pause, and shift-handover proxy", "thos-alteration-handover", "THOS Body", "represented", ["SRC-ISO8559", "SRC-WORKSAFE-MACHINERY"], "garment alteration and handover proxy"),
    (25, "THOS garment machine, cutting, pinning and pressing hazard, unresolved fault, independent-check placeholder, harm stop, correction latency, and handover proxy", "thos-garment-hazard", "THOS Body", "represented", ["SRC-WORKSAFE-MACHINERY", "SRC-WORKSAFE-HAZ"], "garment-studio hazard and correction proxy"),
    (26, "Freed ID synthetic NDEF alteration docket with MIME-or-URI record selection, minimal payload schema, unlinkable token placeholder, lifecycle expiry, write policy, opt-in boundary, and offline-only state", "nfc-alteration-ticket", "Freed ID and CBR Heart", "represented", ["SRC-NFC-SPECS"], "synthetic NDEF docket structure and offline-only boundary"),
    (27, "Freed ID synthetic ISO IEC 20248 repair provenance envelope with signed-data schema placeholder, issuer namespace reservation, algorithm declaration, absent trust anchor, verification tri-state, revocation gap, and nonproduction firewall", "iso20248-garment-digsig", "Freed ID and CBR Heart", "represented", ["SRC-ISO20248"], "synthetic signed-data envelope with explicit trust and revocation gaps"),
    (28, "Freed ID synthetic ESPR textile passport planning board with delegated-act applicability watch, persistent item-key placeholder, material and repair-event schema, role-scoped disclosure reserve, update provenance, portability, and no-market-use firewall", "textile-dpp-profile", "Freed ID and CBR Heart", "represented", ["SRC-EU-ESPR", "SRC-PRIVACY-ACT"], "synthetic textile-passport planning board with applicability and market-use firewall"),
    (29, "GMUT real textile tensile and drape record, specimen metadata, conditioning and unit, instrument calibration, provenance, uncertainty, and zero-row likelihood-refusal adapter", "textile-data-zero-row", "GMUT Mind", "open_gap", ["SRC-ISO13934", "SRC-ISO13935", "SRC-BIPM-SI"], "real textile mechanical-data readiness"),
    (30, "CBR garment alteration safety, ownership and body-measurement privacy, supplier notice, warranty, accessible fitting, remedy, culturally significant garment, affected-party, legal, cultural, data-governance, and Māori-authority reservation", "garment-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-CGA", "SRC-PRIVACY-ACT", "SRC-WCAG22", "SRC-TE-MANA", "SRC-LOCAL-CONTEXTS"], "garment alteration, fitting, remedy, and authority reservation"),
]
PROPOSALS = [_proposal(*row) for row in _P]


def _source(source_id, status, kind, title, url, implication):
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "phase_implication": implication,
    }


SOURCES = [
    _source("SRC-WORKSAFE-MACHINERY", "current", "official_regulator_guidance", "WorkSafe New Zealand: safe use of machinery", "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "Current machinery-risk context only; no workplace assessment, competence, or compliance finding."),
    _source("SRC-WORKSAFE-HAZ", "current", "official_regulator_guidance", "WorkSafe New Zealand: safety data sheets and hazardous waste", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/safety-data-sheets/", "SDS, labelling, spill, and waste context only; no classification, disposal, workplace, or emergency decision."),
    _source("SRC-CGA", "watch", "official_legislation", "Consumer Guarantees Act 1993", "https://www.legislation.govt.nz/act/public/1993/0091/latest/DLM312829.html", "Watched legal context only; no interpretation, warranty, repair, refund, replacement, or remedy decision."),
    _source("SRC-PRIVACY-ACT", "watch", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/contents.html", "Watched legal context only; no privacy compliance, disclosure, retention, ownership, or identity decision."),
    _source("SRC-ISO3758", "current", "official_standards_catalogue", "ISO 3758:2023 textiles care labelling code using symbols", "https://www.iso.org/standard/74401.html", "Catalogue-level care-label context only; no restricted standard text, treatment approval, conformity, or professional-care claim."),
    _source("SRC-ISO4915", "stable", "official_standards_catalogue", "ISO 4915:1991 textiles stitch types classification and terminology", "https://www.iso.org/standard/10932.html", "Catalogue-level stitch terminology only; no seam design, sewing, product-safety, or conformance decision."),
    _source("SRC-ISO4916", "stable", "official_standards_catalogue", "ISO 4916:1991 textiles seam types classification and terminology", "https://www.iso.org/standard/10934.html", "Catalogue-level seam terminology only; no seam design, sewing, product-safety, or conformance decision."),
    _source("SRC-ISO8559", "current", "official_standards_catalogue", "ISO 8559-1:2017 clothing-size anthropometric definitions", "https://www.iso.org/standard/61686.html", "Catalogue-level measurement definitions only; no body measurement, sizing, fitting, population, privacy, or professional decision."),
    _source("SRC-ISO13934", "stable", "official_standards_catalogue", "ISO 13934-1:2013 textile-fabric tensile properties", "https://www.iso.org/standard/60676.html", "Catalogue-level test context and typed fields only; no specimen, instrument, measurement, result, or conformance claim."),
    _source("SRC-ISO13935", "stable", "official_standards_catalogue", "ISO 13935-1:2014 textile seam tensile properties", "https://www.iso.org/ics/59.080.30/x/", "Catalogue-level seam-test context and typed fields only; no specimen, instrument, measurement, result, or conformance claim."),
    _source("SRC-BIPM-SI", "current", "official_metrology_reference", "BIPM SI Brochure, updated 2026", "https://www.bipm.org/en/publications/si-brochure/", "Unit declarations only; no calibration, traceability, or measurement assurance."),
    _source("SRC-WCAG22", "current", "official_web_standard", "W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Structural checks only; manual, browser, assistive-technology, Māori-language, cognitive, and affected-user evaluation remain reserved."),
    _source("SRC-NFC-SPECS", "current", "official_industry_standard_catalogue", "NFC Forum NDEF technical specification", "https://nfc-forum.org/build/specifications/data-exchange-format-ndef-technical-specification/", "Synthetic NDEF fields only; no tag writing, locking, live URI, interoperability, consent, privacy, or production identity claim."),
    _source("SRC-ISO20248", "current", "official_standards_catalogue", "ISO/IEC 20248:2022 digital signature data structure schema", "https://www.iso.org/standard/81314.html", "Catalogue-level signature fields only; no real key, certificate, signature, validation, issuing authority, or conformance event."),
    _source("SRC-EU-ESPR", "watch", "primary_legislation", "Regulation (EU) 2024/1781 ecodesign and digital product passport framework", "https://eur-lex.europa.eu/eli/reg/2024/1781/eng", "Primary legal context only; no textile applicability, delegated-act status, legal interpretation, access-right, passport, product, or market decision."),
    _source("SRC-TE-MANA", "current", "maori_authority_source", "Te Mana Raraunga principles of Māori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data decisions remain under Māori authority; no authority is delegated to the repository."),
    _source("SRC-LOCAL-CONTEXTS", "current", "affected_community_governance_source", "Local Contexts Traditional Knowledge Labels", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Cultural and traditional-knowledge rights reservation only; no label is selected or applied."),
]

SAFE_TASKS = [
    f"Build and validate bounded contract and rejecting fixtures for {p['proposal_id']} {p['slug']}"
    for p in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared bounded acceptance gate for {p['proposal_id']} {p['mission_surface']}"
    for p in PROPOSALS
]
SKILL_IDEAS = [
    "ghc-family-garment-intake-lineage",
    "ghc-family-fibre-care-refusal",
    "ghc-family-seam-stitch-hold",
    "ghc-family-garment-machine-stop-work",
    "ghc-family-spot-treatment-boundary",
    "ghc-family-garment-workload-handover",
    "ghc-family-gmut-textile-field-typing",
    "ghc-family-freed-id-garment-profiles",
    "ghc-family-garment-accessibility-reservation",
    "ghc-family-garment-authority-reservation",
]
RUNNER_IDEAS = [
    "ghc_family_garment_intake_ledger.py",
    "ghc_family_garment_compatibility_refusal.py",
    "ghc_family_garment_hazard_boards.py",
    "ghc_family_garment_notice_quarantine.py",
    "ghc_family_gmut_textile_fields.py",
    "ghc_family_thos_garment_proxy.py",
    "ghc_family_freed_id_garment_profiles.py",
    "ghc_family_accessible_garment_audit.py",
    "ghc_family_v654_v4_detailed_validator.py",
    "ghc_family_v654_v4_bounded_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-scoped {surface} without deletion, history rewrite, sibling mutation, "
    "gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in (
        "schema clarity",
        "source status",
        "unit typing",
        "identifier binding",
        "privacy boundary",
        "authority reservation",
        "rollback wording",
        "accessible structure",
        "manifest coverage",
        "stale-label refusal",
    )
]


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6544-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


INHERITED_EXTERNAL_NEGATIVE_RECORDS = []


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "memory_registry_rg_timeout", "The first bounded memory-registry ripgrep search timed out before returning attributable results.", "Use a literal-path Select-String query with a longer bound and a bounded result projection.", "Prefer literal-path bounded registry reads when the memory file is cold."),
    _negative(2, "assumed_source_receipt_path", "A receipt inventory assumed a validation/evidence-build-receipt path that is not committed and produced a Git fatal for that candidate.", "Inventory exact phase filenames first, then read evidence/evidence-build-receipt.json.", "Resolve receipt paths from the committed tree before projecting their schemas."),
    _negative(3, "manifest_coverage_semantics_assumption", "The first read-only manifest audit overclaimed x1 delta and owner coverage by using guessed domains, so those two coverage assertions earned zero credit.", "Read the committed manifest builder and apply its commit-local replay and exact owner-path semantics.", "Inspect the generating validator before asserting manifest coverage beyond blob, byte, and digest replay."),
    _negative(4, "combined_environment_uniqueness_version_probe_timeout", "A combined D-drive, name, branch, and tool-version preflight timed out without complete attributable output.", "Split drive, path, branch, task-title, and version checks into scalar probes.", "Use one cold subsystem per preflight command."),
    _negative(5, "get_psdrive_free_space_timeout", "The first Get-PSDrive free-space probe timed out without a result.", "Use a bounded System.IO.DriveInfo probe and verify the exact D drive.", "Prefer DriveInfo for a single local-volume capacity check."),
    _negative(6, "full_tree_name_uniqueness_search_timeout", "A full-tree Git name search timed out before proving uniqueness.", "Use the current task-title registry plus exact branch and worktree absence checks for the full relational name.", "Do not use an unbounded repository-content search as the identity uniqueness gate."),
    _negative(7, "combined_tool_version_probe_timeout", "A combined Git, Python, and Node version command timed out after returning only Git.", "Verify each required version with its own bounded scalar command.", "Keep cold tool startup probes separate."),
    _negative(8, "unsupported_task_list_limit", "The first task-list call requested a limit above the supported maximum and was rejected.", "Use the live schema maximum and reread the bounded current registry.", "Inspect the supported task-list limit before supplying it."),
    _negative(9, "worktree_add_wrapper_timeout_after_completion", "The additive worktree wrapper timed out while Git continued the authorized checkout.", "Wait for Git to finish, then audit exact path, registration, branch, head, clean state, processes, and locks before any retry.", "Never retry a timed-out mutating Git command before a complete state audit."),
    _negative(10, "combined_worktree_audit_while_git_active_timeout", "The first combined path, branch, head, and status audit timed out while checkout processes were still active.", "Separate process completion from path, registration, head, lock, and clean-state probes.", "Do not combine worktree inspection with status while the creating Git process is active."),
    _negative(11, "powershell_get_process_timeout", "The first PowerShell Get-Process Git audit timed out without attributable output.", "Use the bounded operating-system task listing for process presence, then recheck after completion.", "Prefer the simpler process surface when PowerShell process enumeration is cold."),
    _negative(12, "worktree_status_wrapper_timeout", "The first post-checkout status wrapper timed out while its Git child continued and produced no attributable clean-state result.", "Wait for the child to finish and run one longer bounded porcelain-status probe.", "Treat timed-out status wrappers as zero credit and verify no lingering process before retry."),
    _negative(13, "semantic_novelty_threshold_failure", "The first 1,750-row semantic-novelty dry run found six proposal titles at or above the preregistered token-Jaccard threshold, so the candidate set earned zero novelty credit.", "Rewrite the colliding mechanisms and rerun the complete read-only comparison before building the frozen packet.", "Do not relax a preregistered novelty threshold to rescue templated wording."),
    _negative(14, "novelty_diagnostic_console_encoding_failure", "The first diagnostic projection of near-neighbour titles failed when the default console encoding could not emit a Māori character, so that projection earned zero diagnostic credit.", "Set the Python input and output encoding explicitly to UTF-8 and repeat only the bounded diagnostic projection.", "Force UTF-8 for bounded projections that may contain non-ASCII relational or cultural language."),
]

REJECTED_COLLISIONS = [
    {"candidate": "generic tailoring checklist", "reason": "Too broad to distinguish custody, measurements, materials, seams, machines, fitting, release, and authority mechanisms."},
    {"candidate": "generic garment provenance", "reason": "Split into custody, care-label, supplier notice, NFC, digital-signature, and digital-product-passport mechanisms."},
    {"candidate": "generic sewing safety", "reason": "Replaced by machine, sharp, pressing, chemical, workload, fitting, and exact-authority surfaces."},
    {"candidate": "generic seam model", "reason": "Split into seam-stitch refusal, a typed seam graph, and zero-row mechanical-data readiness."},
    {"candidate": "generic garment fit", "reason": "Split into measurement privacy, hem balance, fitting reservation, and THOS alteration proxy."},
    {"candidate": "generic fabric model", "reason": "Split into fibre-care refusal, a woven lattice field, and a drape shell field."},
    {"candidate": "generic component identifier", "reason": "Split into fastener fitment, supplier notice, service tag, and component-signature profiles."},
    {"candidate": "generic accessibility checklist", "reason": "Narrowed to an alteration-status timeline and fitting reservation with manual evaluation retained."},
    {"candidate": "generic remedy matrix", "reason": "Replaced by explicit affected-party, privacy, legal, cultural, data-governance, and Māori-authority reservations."},
    {"candidate": "real textile performance analysis", "reason": "Requires specimens, instruments, calibration, provenance, data, and independent review; narrowed to zero-row readiness."},
]
