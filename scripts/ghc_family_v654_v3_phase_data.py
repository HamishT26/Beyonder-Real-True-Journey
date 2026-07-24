#!/usr/bin/env python3
"""Frozen Sylven Arc v654-v3 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v654-v3"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = (
    "keep uncertainty visible without turning it into authority, while leaving every "
    "failure and recovery legible"
)
BRANCH = "codex/GHC-Family/sylven-arc-v654-v3-full-tools"
PHASE_ROOT = "docs/sylven-arc/v654-v3"

SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v654-v2-full-tools"
SOURCE_HEAD = "74da3812daadcd6d452e899b7142dc87d684aba4"
SOURCE_ORIGIN = "105d7fb75e9948ced0362f2c22066d4f15b4e330"
SOURCE_X1 = "8a8062a360dd6510d999cabe22cd38417f59def6"
SOURCE_EVIDENCE = "eeb1988daa9ca454568c294edf1c0c6d225a9844"
SOURCE_FIRST_CLOSEOUT = "74da3812daadcd6d452e899b7142dc87d684aba4"
PRIOR_FROZEN = 1720
INHERITED_SEALED_NEGATIVES = 10963
INHERITED_EXTERNAL_NEGATIVES = 5
INHERITED_NEGATIVES = 10968
INHERITED_OPEN_GAPS = 79
INHERITED_ROUTE_OPEN_GAPS = 2
INHERITED_EXACT_GATES = 80
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "community bicycle workshop service intake, component compatibility, torque and wear "
    "documentation, safety holds, accessible notice, workload control, and shift handover, "
    "as a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_or_operators",
    "professional_bicycle_repair_product_safety_machinery_and_hazardous_substance_authority",
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
            "Emit unresolved decision rights and reservations only; make no bicycle-safety, "
            "repair, product-recall, ownership, theft-reporting, warranty, remedy, legal, cultural, "
            "data-governance, affected-party, or Maori-authority decision."
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
        "proposal_id": f"V6543-P{number:02d}",
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
        "novelty_against_1720_frozen_proposals": (
            "The complete 1,720-row inherited title audit found no proposal combining the "
            f"community-bicycle-workshop mechanism frozen here: {title}."
        ),
    }


_P = [
    (1, "Bicycle service intake frame identifier, presented-owner claim placeholder, condition, accessory, custody, privacy minimization, and work-start hold", "service-intake-custody", "Freed ID and CBR Heart", "completed", ["SRC-ISO4210", "SRC-PRIVACY-ACT"], "service intake, custody, and privacy minimization"),
    (2, "Bicycle work-order symptom, inspection finding, estimate revision, consent placeholder, scope change, correction readback, and release hold", "work-order-scope-hold", "THOS Body", "completed", ["SRC-CGA", "SRC-PRIVACY-ACT"], "work-order scope and correction hold"),
    (3, "Bicycle component fastener, manufacturer-document version, torque unit, allowable range, tool status, substitution, and refusal ledger", "torque-spec-refusal", "THOS Body", "completed", ["SRC-ISO4210", "SRC-BIPM-SI"], "fastener torque provenance and substitution refusal"),
    (4, "Bicycle wheel side, spoke position, tension target, tolerance, gauge provenance, outlier, adjustment sequence, and release hold", "wheel-tension-hold", "THOS Body", "completed", ["SRC-PARK-WHEEL", "SRC-BIPM-SI"], "wheel tension mapping and release hold"),
    (5, "Bicycle rim and tyre bead-seat diameter, width, hook state, pressure ceiling, tube or tubeless state, mismatch, and fitment refusal", "rim-tyre-fitment", "THOS Body", "completed", ["SRC-ISO5775"], "rim and tyre compatibility refusal"),
    (6, "Bicycle brake pad and rotor material, wear, thickness, contamination, bedding placeholder, replacement state, and release refusal", "brake-friction-hold", "THOS Body", "completed", ["SRC-ISO4210-BRAKES"], "brake friction-component release hold"),
    (7, "Bicycle hydraulic brake fluid type, component compatibility, batch, contamination, bleed state, spill state, waste route, and service hold", "brake-fluid-boundary", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ", "SRC-ISO4210-BRAKES"], "hydraulic brake-fluid compatibility and waste hold"),
    (8, "Bicycle cable and hose route, bend, abrasion, steering sweep, retention, interference, correction, and movement refusal", "cable-hose-routing", "THOS Body", "completed", ["SRC-ISO4210"], "cable and hose routing movement refusal"),
    (9, "Bicycle chain pitch and wear proxy, direction, chainring and cassette relation, replacement scope, lubrication state, and run hold", "chain-wear-hold", "THOS Body", "completed", ["SRC-ISO9633", "SRC-BIPM-SI"], "chain wear and drivetrain scope hold"),
    (10, "Bicycle derailleur hanger alignment proxy, limit state, cable tension, gear path, overshift signal, correction, and release refusal", "derailleur-release-refusal", "THOS Body", "completed", ["SRC-ISO4210"], "derailleur alignment and overshift refusal"),
    (11, "Bicycle crank, spindle, bottom-bracket interface, thread or press-fit state, preload, fixing torque, play, and mismatch hold", "crank-interface-hold", "THOS Body", "completed", ["SRC-ISO4210", "SRC-BIPM-SI"], "crank and bottom-bracket interface hold"),
    (12, "Bicycle headset and bearing stack, orientation, preload, binding, play, steering sweep, correction, and release hold", "headset-steering-hold", "THOS Body", "completed", ["SRC-ISO4210"], "headset and steering release hold"),
    (13, "Bicycle suspension component identifier, service interval, fluid specification, pressure placeholder, travel, seal state, and competence hold", "suspension-competence-hold", "THOS Body", "completed", ["SRC-ISO4210", "SRC-BIPM-SI"], "suspension service competence hold"),
    (14, "Bicycle carbon-composite fork, handlebar or seatpost surface, impact-history placeholder, clamp zone, torque history, anomaly, quarantine, and manufacturer escalation", "carbon-component-quarantine", "Freed ID and CBR Heart", "completed", ["SRC-ISO4210", "SRC-CGA"], "carbon-component anomaly quarantine"),
    (15, "Bicycle lamp and reflector function, mount, aim placeholder, power state, visibility note, legal-context watch, and release record", "lighting-reflector-record", "THOS Body", "completed", ["SRC-NZTA-CYCLING"], "lighting and reflector structural record"),
    (16, "Bicycle repair-stand clamp, support point, centre-of-mass proxy, stability, torque reaction, fall zone, and stop-work board", "repair-stand-stop-work", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "repair-stand stability and stop-work structure"),
    (17, "Bicycle component part number, batch, recall-notice version, applicability, affected work order, quarantine, and release refusal", "recall-quarantine", "Freed ID and CBR Heart", "completed", ["SRC-CONSUMER-RECALL", "SRC-CGA"], "component recall applicability and quarantine"),
    (18, "Accessible bicycle service-status timeline, work-order state, safety hold, current step, error relation, noncolour cue, zoom, and manual-evaluation reservation", "accessible-service-status", "THOS Body", "completed", ["SRC-WCAG22"], "accessible service-status structure"),
    (19, "Bicycle workshop queue, unresolved safety defect, dual readback, work-in-progress limit, fatigue flag, break trigger, and shift-handover board", "workload-handover", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "workload control and shift handover"),
    (20, "Bicycle test-ride request, route placeholder, weather and traffic hold, equipment state, unresolved defect, authorization reservation, and return receipt", "test-ride-reservation", "THOS Body", "completed", ["SRC-NZTA-CYCLING", "SRC-PRIVACY-ACT"], "test-ride authorization reservation"),
    (21, "GMUT bicycle wheel spoke-network field, rim-node displacement, pretension, graph Laplacian, boundary load, unit, and observation-firewall board", "gmut-spoke-network", "GMUT Mind", "completed", ["SRC-PARK-WHEEL", "SRC-BIPM-SI"], "typed spoke-network field obligations"),
    (22, "GMUT bicycle chain discrete-link field, pitch, articulation angle, sprocket boundary, tension flux, conservation, unit, and observation-firewall board", "gmut-chain-field", "GMUT Mind", "completed", ["SRC-ISO9633", "SRC-BIPM-SI"], "typed discrete-chain field obligations"),
    (23, "GMUT bicycle tyre contact-patch field, pressure, carcass stiffness, rolling-loss proxy, boundary work, unit, and observation-firewall board", "gmut-tyre-contact", "GMUT Mind", "completed", ["SRC-ISO5775", "SRC-BIPM-SI"], "typed tyre-contact field obligations"),
    (24, "THOS bicycle service intake, safety-critical defect, scope correction, stop-work, workload budget, readback, and shift-handover proxy", "thos-service-handover", "THOS Body", "represented", ["SRC-ISO4210", "SRC-WORKSAFE-MACHINERY"], "bicycle service and handover proxy"),
    (25, "THOS bicycle brake and steering release, unresolved fault, independent-check placeholder, harm stop, correction latency, and handover proxy", "thos-brake-steering", "THOS Body", "represented", ["SRC-ISO4210-BRAKES", "SRC-WORKSAFE-MACHINERY"], "brake and steering release proxy"),
    (26, "Freed ID NFC Forum NDEF bicycle service tag, record type, payload, URI binding, write-lock state, consent, privacy, and nonproduction profile", "nfc-service-tag", "Freed ID and CBR Heart", "represented", ["SRC-NFC-SPECS"], "NFC service-tag identity profile"),
    (27, "Freed ID ISO IEC 20248 bicycle component DigSig, data element, domain-authority placeholder, signature suite, verification-state placeholder, privacy, and nonproduction profile", "iso20248-component-digsig", "Freed ID and CBR Heart", "represented", ["SRC-ISO20248"], "ISO 20248 component signature profile"),
    (28, "Freed ID EU battery-passport data carrier, product identifier, model, lifecycle field, access-right placeholder, update lineage, privacy, legal-status watch, and nonproduction profile", "battery-passport-profile", "Freed ID and CBR Heart", "represented", ["SRC-EU-BATTERY", "SRC-PRIVACY-ACT"], "battery-passport identity and access profile"),
    (29, "GMUT real bicycle power-meter FIT record, device metadata, unit, calibration status, provenance, uncertainty, and zero-row likelihood-refusal adapter", "fit-power-zero-row", "GMUT Mind", "open_gap", ["SRC-GARMIN-FIT", "SRC-BIPM-SI"], "real bicycle power-data readiness"),
    (30, "CBR bicycle repair safety, ownership and theft-reporting privacy, recall, warranty, accessible notice, remedy, affected-party, legal, cultural, data-governance, and Maori-authority reservation", "bicycle-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-NZTA-CYCLING", "SRC-CONSUMER-RECALL", "SRC-CGA", "SRC-PRIVACY-ACT", "SRC-TE-MANA", "SRC-LOCAL-CONTEXTS"], "bicycle repair and remedy authority reservation"),
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
    _source("SRC-NZTA-CYCLING", "current", "official_transport_guidance", "Waka Kotahi NZ Transport Agency: cycle equipment", "https://www.nzta.govt.nz/driving-skills/learn-to-drive/roadcode/new-zealand-cycling-code/equipment", "Current public cycling-equipment context only; no repair, inspection, roadworthiness, or legal finding."),
    _source("SRC-ISO4210", "current", "official_standards_catalogue", "ISO 4210-1:2023 cycles safety requirements and vocabulary", "https://www.iso.org/standard/78075.html", "Vocabulary and bounded field obligations only; no access to restricted text, conformity, test, or product-safety claim."),
    _source("SRC-ISO4210-BRAKES", "current", "official_standards_catalogue", "ISO 4210-4:2023 bicycle braking test methods", "https://www.iso.org/standard/78079.html", "Catalogue-level braking context only; no brake test, measurement, inspection, or conformance claim."),
    _source("SRC-ISO5775", "current", "official_standards_catalogue", "ISO 5775-1:2023 bicycle tyre designations and dimensions", "https://www.iso.org/standard/80740.html", "Catalogue-level tyre/rim designations only; no fitment approval or measurement assurance."),
    _source("SRC-ISO9633", "stable", "official_standards_catalogue", "ISO 9633:2001 cycle chains characteristics and test methods", "https://www.iso.org/standard/23532.html", "Confirmed standard context and typed fields only; no chain test, service decision, or conformance claim."),
    _source("SRC-PARK-WHEEL", "current", "manufacturer_technical_guidance", "Park Tool spoke tension measurement and adjustment", "https://www.parktool.com/en-us/blog/repair-help/wheel-tension-measurement", "Technical context only; no endorsement, professional competence, tool calibration, or wheel release decision."),
    _source("SRC-WORKSAFE-MACHINERY", "current", "official_regulator_guidance", "WorkSafe New Zealand: safe use of machinery", "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "Current machinery-risk context only; no workplace assessment, competence, or compliance finding."),
    _source("SRC-WORKSAFE-HAZ", "current", "official_regulator_guidance", "WorkSafe New Zealand: hazardous-substance information and supervision", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/information-instruction-supervision-training/", "Chemical label and refusal context only; no classification, disposal, workplace, or emergency decision."),
    _source("SRC-CONSUMER-RECALL", "current", "official_consumer_guidance", "New Zealand Consumer Protection: product recalls", "https://www.consumerprotection.govt.nz/general-help/common-consumer-issues/product-recalls", "Recall-notice structure and remedy context only; no applicability, remedy, supplier, or legal decision."),
    _source("SRC-CGA", "watch", "official_legislation", "Consumer Guarantees Act 1993", "https://www.legislation.govt.nz/act/public/1993/0091/latest/DLM312829.html", "Watched legal context only; no interpretation, warranty, repair, refund, replacement, or remedy decision."),
    _source("SRC-PRIVACY-ACT", "watch", "official_legislation", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/0031/latest/contents.html", "Watched legal context only; no privacy compliance, disclosure, retention, ownership, or identity decision."),
    _source("SRC-BIPM-SI", "current", "official_metrology_reference", "BIPM SI Brochure, updated 2026", "https://www.bipm.org/en/publications/si-brochure", "Unit declarations only; no calibration, traceability, or measurement assurance."),
    _source("SRC-WCAG22", "current", "official_web_standard", "W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Structural checks only; manual, browser, assistive-technology, Maori-language, cognitive, and affected-user evaluation remain reserved."),
    _source("SRC-NFC-SPECS", "current", "official_industry_standard_catalogue", "NFC Forum specifications including NDEF and URI record types", "https://nfc-forum.org/build/specifications", "Synthetic NDEF fields only; no tag writing, locking, live URI, interoperability, consent, privacy, or production identity claim."),
    _source("SRC-ISO20248", "stable", "official_standards_catalogue", "ISO/IEC 20248 digital signature data structure schema", "https://www.iso.org/standard/67412.html", "Catalogue-level signature fields only; no real key, certificate, signature, validation, issuing authority, or conformance event."),
    _source("SRC-EU-BATTERY", "watch", "primary_legislation", "Regulation (EU) 2023/1542 batteries and battery passport", "https://eur-lex.europa.eu/eli/reg/2023/1542/oj", "Primary legal context only; no applicability, legal interpretation, access-right, passport, product, or market decision."),
    _source("SRC-GARMIN-FIT", "current", "primary_vendor_protocol", "Garmin Flexible and Interoperable Data Transfer protocol", "https://developer.garmin.com/fit/protocol/", "Zero-row schema readiness only; no SDK download, device access, account, personal activity, calibration, fit, likelihood, or empirical claim."),
    _source("SRC-TE-MANA", "current", "maori_authority_source", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Maori data decisions remain under Maori authority; no authority is delegated to the repository."),
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
    "ghc-family-bicycle-intake-lineage",
    "ghc-family-bicycle-torque-spec-refusal",
    "ghc-family-wheel-tension-hold",
    "ghc-family-brake-fluid-boundary",
    "ghc-family-carbon-component-quarantine",
    "ghc-family-bicycle-workload-handover",
    "ghc-family-gmut-bicycle-field-typing",
    "ghc-family-freed-id-service-tags",
    "ghc-family-bicycle-accessibility-reservation",
    "ghc-family-bicycle-authority-reservation",
]
RUNNER_IDEAS = [
    "ghc_family_bicycle_intake_ledger.py",
    "ghc_family_bicycle_fitment_refusal.py",
    "ghc_family_bicycle_brake_steering_boards.py",
    "ghc_family_bicycle_recall_quarantine.py",
    "ghc_family_gmut_bicycle_fields.py",
    "ghc_family_thos_bicycle_proxy.py",
    "ghc_family_freed_id_bicycle_profiles.py",
    "ghc_family_accessible_bicycle_audit.py",
    "ghc_family_v654_v3_detailed_validator.py",
    "ghc_family_v654_v3_bounded_suite.py",
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
        "negative_id": f"V6543-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


INHERITED_EXTERNAL_NEGATIVE_RECORDS = [
    {
        "negative_ids": ["V6542-HANDOFF-N01"],
        "signature": "unsupported_task_list_page_size",
        "failed": "The source-owner routing preflight requested an unsupported task-list page size and received zero route credit.",
        "recovery": "Use the supported bounded task-list schema and uniquely resolve the exact existing title.",
        "recurrence_guard": "Inspect the live task-tool schema before supplying optional pagination fields.",
    },
    {
        "negative_ids": ["V6542-HANDOFF-N02"],
        "signature": "long_range_route_nonsequential_phase_order",
        "failed": "The long-range route audit found a nonsequential phase order and granted zero activation credit.",
        "recovery": "Retain the issue as an open gap while using only the separately valid immediate route.",
        "recurrence_guard": "Never infer phase ownership from a long-range route whose sequence audit fails.",
    },
    {
        "negative_ids": ["V6542-HANDOFF-N03"],
        "signature": "long_range_route_normalization_requires_confirmation",
        "failed": "The long-range route audit found spelling or label normalization requiring confirmation and granted zero activation credit.",
        "recovery": "Keep the unresolved seat and spelling drift explicit; do not invent or normalize identity.",
        "recurrence_guard": "Require exact live authority before normalizing any relational label or seat.",
    },
    {
        "negative_ids": ["V6542-HANDOFF-N04"],
        "signature": "combined_predelivery_source_probe_timeout",
        "failed": "A combined pre-delivery source probe timed out before producing a complete attributable result.",
        "recovery": "Split clean-state, ancestry, manifest, and remote-equality checks into bounded scalar probes.",
        "recurrence_guard": "Use one cold Git or filesystem subsystem per pre-delivery probe.",
    },
    {
        "negative_ids": ["V6542-HANDOFF-N05"],
        "signature": "postdelivery_timestamp_wrapper_timeout",
        "failed": "A post-delivery timestamp wrapper timed out and earned no additional delivery credit.",
        "recovery": "Retain the acknowledged delivery state and audit immutable evidence without resending.",
        "recurrence_guard": "Never repeat an acknowledged one-shot delivery because a later wrapper times out.",
    },
]


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "skill_discovery_foreach_pipeline_parser_fault", "A PowerShell foreach statement was piped directly during skill discovery and failed before execution.", "Materialize foreach output before piping.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(2, "method_flow_schema_filename_assumption", "The first Method Flow schema read assumed a nonexistent method-flow-state-schema filename.", "Read the exact references/schema.md path named by the skill.", "Resolve every skill-relative reference from the complete SKILL.md before use."),
    _negative(3, "combined_worktree_and_receipt_search_timeout", "A combined worktree inventory and receipt search exceeded its bound without complete attributable output.", "Split worktree discovery from exact receipt probes.", "Use one cold filesystem subsystem per bounded discovery command."),
    _negative(4, "multi_root_receipt_search_timeout", "A narrowed multi-root receipt search still timed out before a complete result.", "Probe the exact expected receipt path and digest directly.", "Prefer exact candidate paths over recursive multi-root scans."),
    _negative(5, "combined_source_verification_timeout", "A combined source branch, history, clean-state, remote, and digest verification timed out before a complete result.", "Split immutable refs, ancestry, live remote, clean state, and digest into scalar probes.", "Keep local Git checks separate from fresh-live and filesystem hashing."),
    _negative(6, "external_receipt_property_projection_assumption", "The first external receipt projection used property names not present in the committed schema.", "Inspect receipt keys before binding exact fields.", "Discover JSON schema keys before projecting evidence."),
    _negative(7, "unsupported_convertfromjson_depth_parameter", "Windows PowerShell 5.1 rejected the unsupported ConvertFrom-Json Depth parameter.", "Omit the unsupported parameter and parse the bounded document with the installed command surface.", "Preflight shell-version-specific parameters."),
    _negative(8, "artifact_group_foreach_pipeline_parser_fault", "A small artifact-group read piped directly from foreach and failed before execution.", "Materialize the artifact group before piping.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(9, "method_flow_property_projection_assumption", "The first compact Method Flow projection used property names not present in the committed schema.", "Inspect a real method and witness before binding names.", "Bind Method Flow keys only after schema and instance discovery."),
    _negative(10, "method_flow_foreach_pipeline_parser_fault", "A compact Method Flow foreach projection was piped directly and failed before execution.", "Materialize projection output before formatting.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(11, "frozen_chain_top_level_array_assumption", "The first frozen-chain parser assumed a proposals array instead of prior_proposals plus new_proposals.", "Inspect top-level keys and concatenate the two committed arrays.", "Discover proposal-chain schema before counting or hashing."),
    _negative(12, "git_ls_tree_default_buffer_exhaustion", "Node execFileSync exhausted its default buffer while reading the source tree and produced no manifest credit.", "Retry the unchanged read-only command with an explicit bounded 128 MB buffer.", "Set a justified output buffer before large Git tree reads."),
    _negative(13, "combined_route_audit_read_timeout", "A combined immediate and long-range route-audit read timed out before complete output.", "Read each route artifact in its own bounded scalar probe.", "Do not aggregate independent route artifacts in one cold read."),
    _negative(14, "full_route_json_wrapper_timeout", "A formatted full-route JSON wrapper timed out and earned no audit credit.", "Read the raw scalar audit fields separately.", "Prefer bounded scalar extraction over whole-object formatting for large route records."),
    _negative(15, "branch_preflight_exit_code_expression_parser_fault", "A branch and path preflight embedded child exit-code expressions inside a PowerShell hash literal and failed before execution.", "Compute scalar exit codes before constructing the record.", "Never embed child-process statements inside PowerShell literal expressions."),
    _negative(16, "worktree_add_wrapper_timeout_after_completion", "The owned worktree-add wrapper timed out after Git had completed the additive checkout.", "Audit exact path, registration, branch, head, clean state, processes, and locks before deciding whether to retry.", "Never retry a timed-out mutating Git command before a complete state audit."),
    _negative(17, "worktree_registration_separator_assumption", "The first registration counter compared a backslash path with Git's forward-slash worktree output and falsely reported zero.", "Normalize separators and inspect the exact registration record.", "Normalize path separators before comparing Git administrative output."),
    _negative(18, "novelty_search_foreach_pipeline_parser_fault", "The first novelty search piped directly from foreach and failed before execution.", "Materialize the search output before sorting or formatting.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(19, "candidate_novelty_foreach_whitespace_parser_fault", "A candidate novelty query omitted required whitespace in a foreach statement and failed before execution.", "Correct the syntax and rerun the unchanged read-only calculation.", "Use formatted multi-line PowerShell for nontrivial loops."),
    _negative(20, "keyword_search_foreach_whitespace_parser_fault", "A keyword search omitted required whitespace in a foreach statement and failed before execution.", "Correct the syntax and rerun the unchanged read-only search.", "Use formatted multi-line PowerShell for nontrivial loops."),
    _negative(21, "combined_status_diff_and_selectstring_timeout", "A combined status, full untracked-file diff, and Select-String inspection timed out before attributable output.", "Split clean-state and bounded source-range inspections into separate probes.", "Never combine potentially large untracked-file inspection with Git status."),
    _negative(22, "large_mixed_context_patch_mismatch", "A combined accessible-report and x1-test patch failed because one Unicode context line did not match exactly.", "Split the change into smaller exact-context patches and retain the failed attempt.", "Do not combine Unicode-sensitive and independent source edits in one patch."),
    _negative(23, "inherited_proposal_index_phase_pointer_assumption", "The first x1 build pointed to Tamar v654-v1's 1,690-row index and stopped before generating the packet because the activation baseline requires 1,720.", "Bind the exact committed Elowen v654-v2 frozen-chain index and rerun from the unchanged x1 data.", "Resolve the immediate source-owner proposal index before building a successor freeze."),
    _negative(24, "broad_frozen_index_inventory_timeout", "A recursive frozen-index inventory over the inherited docs tree timed out without a complete result.", "Probe the exact expected Elowen phase path and verify its 1,690 plus 30 equals 1,720 counts.", "Prefer exact phase-local artifact paths over recursive repository inventories."),
    _negative(25, "workflow_runner_existing_task_policy_mismatch", "The first workflow-plan request was rejected because the current runner hard-codes an existing-task route while Hamish's live terminal authority requires one new user-visible main task.", "Retain the failed audit, supply the validator's compatibility literal only for its structural check, and record the exact live new-task authority in separate controlling fields.", "Never let a compatibility literal override newer exact live route authority or trigger a premature task action."),
    _negative(26, "powershell_upstream_shorthand_interpolation", "The first post-push divergence wrapper let PowerShell reinterpret the unquoted upstream shorthand, so Git received an invalid revision and the comparison earned zero credit.", "Quote HEAD...@{u} as a literal Git argument; the recovery proved zero ahead and zero behind.", "Quote every Git upstream shorthand passed through PowerShell."),
]

REJECTED_COLLISIONS = [
    {"candidate": "generic bicycle service checklist", "reason": "Too broad to distinguish intake, fitment, torque, braking, steering, release, and authority mechanisms."},
    {"candidate": "generic bicycle provenance", "reason": "Split into custody, recall, NFC, component-signature, and battery-passport mechanisms."},
    {"candidate": "generic workshop safety", "reason": "Replaced by repair-stand, chemical, workload, test-ride, and exact-authority surfaces."},
    {"candidate": "generic wheel model", "reason": "Split into spoke-tension workflow and a typed spoke-network field board."},
    {"candidate": "generic tyre model", "reason": "Split into rim-fitment refusal and a typed contact-patch field board."},
    {"candidate": "generic drivetrain model", "reason": "Split into chain wear, derailleur release, crank interface, and a discrete-link field board."},
    {"candidate": "generic component identifier", "reason": "Split into service-tag, digital-signature, recall, and battery-passport profiles."},
    {"candidate": "generic accessibility checklist", "reason": "Narrowed to a service-status timeline with explicit structural and manual reservations."},
    {"candidate": "generic remedy matrix", "reason": "Replaced by explicit affected-party, privacy, legal, cultural, data-governance, and Maori-authority reservations."},
    {"candidate": "real bicycle telemetry analysis", "reason": "Requires data access, device provenance, calibration evidence, and independent review; narrowed to zero-row readiness."},
]
