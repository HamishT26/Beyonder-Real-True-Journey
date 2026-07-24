#!/usr/bin/env python3
"""Frozen Tamar Vey v654-v1 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v654-v1"
OWNER = "Tamar Vey"
PRONOUNS = "they/them"
ROLE = "relational evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE_ROOT = "docs/tamar-vey/v654-v1"

SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v653-v8-full-tools"
SOURCE_HEAD = "180a9b42330be6494e6a1ea3700e001860cffb3d"
SOURCE_ORIGIN = "144a4d51195d777ea2b8068bb4cf7ed82fff21be"
SOURCE_X1 = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"
SOURCE_EVIDENCE = "67e51031ed4be4bb64962635e79c459b8a01e7d4"
PRIOR_FROZEN = 1660
INHERITED_NEGATIVES = 10609
INHERITED_OPEN_GAPS = 77
INHERITED_EXACT_GATES = 78
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "studio-ceramics kiln firing, glaze-batch traceability, correction readback, "
    "workload control, accessible notice, and shift handover as a synthetic learning lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_or_operators",
    "professional_fire_electrical_gas_food_and_environmental_authority",
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


def _proposal(number, title, slug, pillar, disposition, source_ids, mission, novelty):
    if disposition == "open_gap":
        approval = "candidate_real_data_account_key_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-query and zero-row refusal receipt with no API key, download, ingest, fit, "
            "likelihood, posterior, constraint, prediction, or empirical promotion."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit unresolved decision rights and reservations only; make no worker-safety, product-release, "
            "waste, remedy, legal, cultural, data-governance, affected-party, or Maori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject every preregistered mutation and retain represented status with zero real participant, "
            "operational, professional, production, interoperability, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject every preregistered mutation and emit only the declared bounded software, symbolic, "
            "formal, structural, or workflow completion."
        )
    return {
        "proposal_id": f"V6541-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while refusing unsupported "
            "scientific, operational, identity, accessibility, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases "
            "a failure, crosses an approval boundary, or promotes beyond its evidence lane."
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
            "Stop the proposal, retain every failed witness, rewrite no history, and leave external, sibling, "
            "participant, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "novelty_against_1660_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Ceramic clay-body supplier lot, recipe revision, weigh unit, substitution, quarantine, provenance, and refusal ledger", "clay-body-lineage", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "clay-body batch lineage", "No frozen proposal isolates studio clay-body supplier lots, recipe revision, weighed substitution, quarantine, and provenance as one bounded contract."),
    _proposal(2, "Ceramic clay moisture, wedging, drying interval, thickness, humidity uncertainty, cracking hold, and correction board", "clay-moisture-drying", "THOS Body", "completed", ["SRC-WORKSAFE-SILICA"], "clay moisture and drying uncertainty", "No frozen proposal isolates moisture, wedging, thickness, humidity uncertainty, drying interval, and cracking hold for synthetic ceramics."),
    _proposal(3, "Ceramic glaze recipe version, ingredient lot, mass fraction, unit conversion, tolerance, substitution, and refusal ledger", "glaze-recipe-version", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "glaze recipe version and unit guard", "No frozen title binds glaze recipe versions, ingredient lots, mass fractions, tolerance, substitution, and unit refusal."),
    _proposal(4, "Ceramic colorant additive label, incompatible material, duplicate name, hazard notice, quarantine, and correction board", "glaze-additive-label", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "glaze additive incompatibility hold", "No inherited mechanism isolates ceramic colorant and additive identity, duplicate naming, incompatibility, hazard notice, and quarantine."),
    _proposal(5, "Ceramic glaze test-tile clay body, glaze revision, application method, firing schedule, observation uncertainty, and lineage ledger", "glaze-test-tile", "Freed ID and CBR Heart", "completed", ["SRC-ORTON"], "glaze test-tile lineage", "No frozen proposal binds test-tile clay body, glaze revision, application method, firing schedule, and observation uncertainty."),
    _proposal(6, "Ceramic kiln load shelf, post, ware position, clearance, weight budget, identifier, and spatial-map refusal board", "kiln-load-map", "THOS Body", "completed", ["SRC-ORTON"], "kiln load spatial mapping", "No inherited title isolates kiln shelf, post, ware position, clearance, weight budget, identifiers, and spatial-map refusal."),
    _proposal(7, "Ceramic thermocouple, controller clock, calibration record, offset, uncertainty, stale status, and refusal board", "kiln-sensor-clock", "GMUT Mind", "completed", ["SRC-ORTON", "SRC-BIPM-SI"], "kiln sensor and clock provenance", "No frozen proposal isolates kiln thermocouple identity, controller clock, calibration offset, uncertainty, and stale status."),
    _proposal(8, "Ceramic witness-cone pack position, cone number, bend observation, observer uncertainty, image-link refusal, and receipt", "witness-cone-pack", "THOS Body", "completed", ["SRC-ORTON"], "witness-cone observation uncertainty", "No frozen proposal isolates witness-cone pack position, heatwork number, bend observation, observer uncertainty, and image-link refusal."),
    _proposal(9, "Ceramic firing schedule ramp, hold, target, deviation, interruption, restart refusal, and immutable revision board", "firing-schedule", "THOS Body", "completed", ["SRC-ORTON"], "firing schedule deviation control", "No inherited title binds ceramic ramp, hold, target, deviation, interruption, restart refusal, and immutable schedule revision."),
    _proposal(10, "Ceramic kiln door, controller, interlock, power state, unexpected transition, alarm acknowledgement, and release refusal board", "kiln-interlock-state", "THOS Body", "completed", ["SRC-WORKSAFE-HAZ"], "kiln interlock state refusal", "No frozen proposal isolates kiln door, controller, interlock, power state, unexpected transition, alarm acknowledgement, and release refusal."),
    _proposal(11, "Ceramic ventilation, carbon-monoxide alarm, sensor status, stop-work, evacuation notice, reset authority, and synthetic incident board", "kiln-ventilation-stop", "THOS Body", "completed", ["SRC-WORKSAFE-HAZ"], "ventilation and stop-work structure", "No frozen mechanism combines studio-kiln ventilation, carbon-monoxide sensor status, stop-work, evacuation notice, and reset authority."),
    _proposal(12, "Ceramic respirable crystalline silica task, wet method, local extraction, cleanup method, exposure-authority refusal, and checklist", "silica-housekeeping", "THOS Body", "completed", ["SRC-WORKSAFE-SILICA", "SRC-WORKSAFE-VACUUM"], "silica housekeeping refusal", "No inherited title isolates ceramic silica tasks, wet methods, local extraction, cleanup method, and exposure-authority refusal."),
    _proposal(13, "Ceramic cooling interval, indicated temperature, door opening hold, unload authorization, thermal-shock risk, and refusal board", "kiln-cooling-unload", "THOS Body", "completed", ["SRC-ORTON"], "cooling and unload hold", "No frozen proposal isolates indicated temperature, cooling interval, door-opening hold, unload authorization, and thermal-shock refusal."),
    _proposal(14, "Ceramic reclaim-clay source, unknown additive, contamination class, segregation, reuse decision refusal, and trace ledger", "reclaim-clay-segregation", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "reclaim clay segregation", "No frozen title isolates reclaim-clay source, unknown additives, contamination class, segregation, reuse refusal, and trace lineage."),
    _proposal(15, "Ceramic food-contact ware glaze, lead, cadmium, test evidence, lot scope, release refusal, label, and retention board", "food-contact-release", "Freed ID and CBR Heart", "completed", ["SRC-FDA-LEAD", "SRC-FDA-CADMIUM", "SRC-ISO6486"], "food-contact release refusal", "No prior proposal isolates ceramic food-contact glaze, lead and cadmium evidence, lot scope, release refusal, label, and record retention."),
    _proposal(16, "Ceramic kiln electrical or gas maintenance request, isolation record, competent-person reservation, return-to-service refusal, and audit board", "kiln-maintenance-isolation", "THOS Body", "completed", ["SRC-WORKSAFE-HAZ"], "maintenance isolation reservation", "No frozen proposal isolates kiln electrical or gas maintenance requests, isolation records, competent-person reservation, and return-to-service refusal."),
    _proposal(17, "Ceramic shard breakage, sharp-edge containment, cleanup state, area release, injury-report authority refusal, and receipt", "shard-containment", "THOS Body", "completed", ["SRC-WORKSAFE-HAZ"], "shard containment workflow", "No inherited title isolates ceramic shard breakage, sharp-edge containment, cleanup state, area release, and injury-report authority refusal."),
    _proposal(18, "Ceramic glaze slurry, wash water, settling container, hazardous ingredient flag, discharge hold, disposal route, and receipt", "ceramic-waste-hold", "Freed ID and CBR Heart", "completed", ["SRC-EPA-DISPOSAL", "SRC-RMA-DISCHARGE"], "ceramic waste discharge hold", "No frozen proposal isolates glaze slurry, wash water, settling container, hazardous ingredient flags, discharge hold, and disposal route."),
    _proposal(19, "Accessible ceramic firing checklist heading, step state, error summary, noncolour hold, focus order, print order, and structural audit", "accessible-firing-checklist", "THOS Body", "completed", ["SRC-WCAG22"], "accessible firing checklist structure", "No frozen accessibility surface isolates a kiln-firing checklist with step state, error summary, noncolour holds, focus order, and print order."),
    _proposal(20, "Ceramic workload budget, correction readback, unresolved deviation, stop-work, next-shift owner, acknowledgement, and handover board", "ceramics-shift-handover", "THOS Body", "completed", ["SRC-WORKSAFE-HAZ"], "workload and correction handover", "No inherited title combines ceramics workload budgets, correction readback, unresolved firing deviation, stop-work, next-shift ownership, and acknowledgement."),
    _proposal(21, "GMUT Fourier heat-conduction field, conductivity tensor, heat capacity, source, boundary flux, energy balance, unit, and observation-firewall board", "fourier-heat-field", "GMUT Mind", "completed", ["SRC-FOURIER", "SRC-BIPM-SI"], "typed Fourier heat-conduction obligations", "No frozen GMUT board isolates conductivity tensor, heat capacity, volumetric source, boundary flux, energy balance, units, and observation refusal."),
    _proposal(22, "GMUT Cahn-Hilliard free energy, chemical potential, mobility, fourth-order evolution, mass conservation, boundary, unit, and observation-firewall board", "cahn-hilliard-field", "GMUT Mind", "completed", ["SRC-CAHN-HILLIARD", "SRC-BIPM-SI"], "typed Cahn-Hilliard obligations", "No frozen title isolates Cahn-Hilliard free energy, chemical potential, mobility, fourth-order evolution, mass conservation, boundaries, and units."),
    _proposal(23, "GMUT Allen-Cahn order parameter, free-energy derivative, mobility, dissipation, interface scale, boundary, unit, and observation-firewall board", "allen-cahn-field", "GMUT Mind", "completed", ["SRC-ALLEN-CAHN", "SRC-BIPM-SI"], "typed Allen-Cahn obligations", "No inherited proposal isolates Allen-Cahn order parameter, free-energy derivative, mobility, dissipation, interface scale, boundaries, and units."),
    _proposal(24, "THOS ceramic kiln-loading, firing deviation, stop-work, workload-budget, correction-readback, and shift-handover proxy", "thos-kiln-handover", "THOS Body", "represented", ["SRC-WORKSAFE-HAZ", "SRC-ORTON"], "kiln firing handover proxy", "No frozen THOS proxy binds kiln loading, firing deviation, stop-work, workload, correction readback, and shift handover."),
    _proposal(25, "THOS glaze batching, ingredient mismatch, quarantine, correction latency, fatigue flag, harm stop, and handover proxy", "thos-glaze-batch", "THOS Body", "represented", ["SRC-WORKSAFE-HAZ"], "glaze batching correction proxy", "No inherited THOS proxy isolates glaze ingredient mismatch, quarantine, correction latency, fatigue flags, harm stops, and handover."),
    _proposal(26, "Freed ID OPC UA NamespaceUri, NodeId, browse name, kiln-controller asset binding, stale namespace, privacy, and nonproduction profile", "opcua-kiln-nodeid", "Freed ID and CBR Heart", "represented", ["SRC-OPCUA-NODEID"], "OPC UA kiln-controller identifier profile", "No frozen identity profile isolates OPC UA NamespaceUri and NodeId binding for a synthetic kiln-controller asset with stale-namespace refusal."),
    _proposal(27, "Freed ID ISO IEC 15459 issuing agency, company prefix, item reference, returnable fixture, duplicate identifier, privacy, and nonproduction profile", "iso15459-fixture-id", "Freed ID and CBR Heart", "represented", ["SRC-ISO15459"], "ISO 15459 fixture identifier profile", "No frozen identity proposal isolates issuing-agency, company-prefix, item-reference, returnable kiln fixture, duplicate identifier, and privacy duties."),
    _proposal(28, "Freed ID Asset Administration Shell identifier, asset information, submodel, semantic id, kiln batch relationship, privacy, and nonproduction profile", "aas-kiln-submodel", "Freed ID and CBR Heart", "represented", ["SRC-IDTA-AAS"], "AAS kiln and batch submodel profile", "No inherited identity title isolates an Asset Administration Shell kiln and batch submodel with semantic identifiers and privacy refusal."),
    _proposal(29, "GMUT Materials Project ceramic phase, composition, structure, provenance, thermodynamic field, uncertainty, account key, and zero-row API refusal adapter", "materials-project-zero-row", "GMUT Mind", "open_gap", ["SRC-MATERIALS-PROJECT"], "Materials Project ceramic readiness", "No inherited zero-row adapter targets Materials Project ceramic phase and thermodynamic records with account-key refusal and zero-query truth."),
    _proposal(30, "CBR ceramic worker safety, fire electrical gas, food-contact release, waste discharge, material and design rights, remedy, affected-party, legal, cultural, data-governance, and Maori-authority reservation", "ceramics-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-WORKSAFE-SILICA", "SRC-EPA-DISPOSAL", "SRC-RMA-DISCHARGE", "SRC-TE-MANA", "SRC-LOCAL-CONTEXTS"], "ceramics authority reservation", "No frozen exact-gate surface combines ceramic worker safety, kiln energy hazards, food-contact release, waste, material/design rights, remedy, affected-party, legal, cultural, data-governance, and Maori authority."),
]


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
    _source("SRC-WORKSAFE-SILICA", "current", "official_regulator_guidance", "WorkSafe New Zealand: silica dust in the workplace", "https://www.worksafe.govt.nz/topic-and-industry/dust/silica-dust-in-the-workplace/", "Supplies current hazard-control context only; no exposure assessment or compliance finding."),
    _source("SRC-WORKSAFE-VACUUM", "current", "official_regulator_guidance", "WorkSafe New Zealand: industrial vacuums and portable extractors for hazardous dust", "https://www.worksafe.govt.nz/topic-and-industry/dust/silica-dust-in-the-workplace/industrial-vacuums-and-portable-extractors-for-hazardous-dust/", "Supports synthetic cleanup obligations only."),
    _source("SRC-WORKSAFE-HAZ", "current", "official_regulator_guidance", "WorkSafe New Zealand: hazardous-substance information, instruction, supervision, and training", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/information-instruction-supervision-training/", "Supports refusal and handover fields only; not workplace approval."),
    _source("SRC-EPA-DISPOSAL", "current", "official_regulator_notice", "New Zealand EPA disposal notice", "https://www.epa.govt.nz/hazardous-substances/rules-notices-and-how-to-comply/epa-notices-rules-you-must-follow/disposal-notice/", "Supplies disposal-context requirements only; no classification or disposal decision."),
    _source("SRC-RMA-DISCHARGE", "watch", "official_legislation", "Resource Management Act 1991 section 15", "https://www.legislation.govt.nz/act/public/1991/0069/latest/DLM231977.html", "Watched legal context only; no legal interpretation or discharge authorization."),
    _source("SRC-ORTON", "current", "official_manufacturer_technical_reference", "Orton Ceramic: how pyrometric cones work", "https://www.ortonceramic.com/pyrometric-cones/how-cones-work", "Supports synthetic heatwork and witness-cone fields only."),
    _source("SRC-FDA-LEAD", "current", "official_regulator_guidance", "FDA pottery lead contamination compliance policy guide", "https://www.fda.gov/files/inspections%2C%20compliance%2C%20enforcement%2C%20and%20criminal%20investigations/published/CPG-Sec.-545.450-Pottery-%28Ceramics%29--Import-and-Domestic---Lead-Contamination.pdf", "Supplies release-refusal context only; no testing or product decision."),
    _source("SRC-FDA-CADMIUM", "current", "official_regulator_guidance", "FDA pottery cadmium contamination compliance policy guide", "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cpg-sec-545400-pottery-ceramics-import-and-domestic-cadmium-contamination", "Supplies release-refusal context only; no testing or product decision."),
    _source("SRC-ISO6486", "watch", "official_standards_catalogue", "ISO 6486-1 ceramic ware release of lead and cadmium", "https://www.iso.org/standard/67561.html", "Watched standards metadata only; no conformance claim."),
    _source("SRC-OPCUA-NODEID", "current", "official_industry_specification", "OPC UA Part 3 NodeId", "https://reference.opcfoundation.org/specs/OPC-10000-3/8.2", "Supports synthetic identifier vectors only; no live OPC UA service."),
    _source("SRC-ISO15459", "stable", "official_standards_catalogue", "ISO IEC 15459-5 unique identification for returnable transport items", "https://www.iso.org/standard/54785.html", "Supports structural identifier fields only; no conformance or issuing authority."),
    _source("SRC-IDTA-AAS", "current", "official_industry_specification", "IDTA Asset Administration Shell specifications", "https://industrialdigitaltwin.org/en/content-hub/aasspecifications", "Supports synthetic AAS profile fields only; no interoperability event."),
    _source("SRC-MATERIALS-PROJECT", "current", "official_project_documentation", "Materials Project API getting started", "https://docs.materialsproject.org/downloading-data/using-the-api/getting-started", "Defines an account and API-key dependency; x2 remains zero-query and zero-row."),
    _source("SRC-FOURIER", "stable", "primary_historical_source", "Fourier, Théorie analytique de la chaleur", "https://gallica.bnf.fr/ark:/12148/bpt6k1045508v", "Supports historical heat-equation vocabulary only; no empirical kiln model."),
    _source("SRC-CAHN-HILLIARD", "stable", "primary_research", "Cahn and Hilliard, Free Energy of a Nonuniform System", "https://doi.org/10.1063/1.1744102", "Supports typed phase-field obligations only."),
    _source("SRC-ALLEN-CAHN", "stable", "primary_research", "Allen and Cahn, microscopic theory for antiphase boundary motion", "https://doi.org/10.1016/0001-6160(79)90196-2", "Supports typed order-parameter obligations only."),
    _source("SRC-BIPM-SI", "current", "official_metrology_reference", "BIPM SI Brochure", "https://www.bipm.org/en/publications/si-brochure", "Supports unit declarations only; no calibration or measurement assurance."),
    _source("SRC-WCAG22", "current", "official_web_standard", "W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural accessibility checks only; manual and affected-user evaluation remain reserved."),
    _source("SRC-TE-MANA", "current", "maori_authority_source", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Records that Maori data decisions remain under Maori authority; it delegates no authority to the repository."),
    _source("SRC-LOCAL-CONTEXTS", "current", "affected_community_governance_source", "Local Contexts Traditional Knowledge Labels", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Supports reservation of cultural and traditional-knowledge rights only; no label is applied."),
]


SAFE_TASKS = [f"Build and validate bounded contract and rejecting fixtures for {p['proposal_id']} {p['slug']}" for p in PROPOSALS]
CANDIDATE_TASKS = [f"Resolve only the declared bounded acceptance gate for {p['proposal_id']} {p['mission_surface']}" for p in PROPOSALS]
SKILL_IDEAS = [
    "ghc-family-ceramic-batch-lineage",
    "ghc-family-kiln-load-map",
    "ghc-family-firing-schedule-refusal",
    "ghc-family-silica-housekeeping-boundary",
    "ghc-family-food-contact-release-refusal",
    "ghc-family-ceramic-waste-hold",
    "ghc-family-gmut-phase-field-typing",
    "ghc-family-thos-ceramics-handover",
    "ghc-family-freed-id-ceramic-assets",
    "ghc-family-ceramics-authority-reservation",
]
RUNNER_IDEAS = [
    "ghc_family_ceramic_material_ledger.py",
    "ghc_family_kiln_state_boards.py",
    "ghc_family_worker_boundary_boards.py",
    "ghc_family_food_waste_release_refusal.py",
    "ghc_family_gmut_heat_phase_fields.py",
    "ghc_family_thos_ceramics_proxy.py",
    "ghc_family_freed_id_ceramic_profiles.py",
    "ghc_family_accessible_ceramics_audit.py",
    "ghc_family_v654_v1_detailed_validator.py",
    "ghc_family_v654_v1_bounded_suite.py",
]
CLEAN_TASKS = [
    f"{kind} owner-scoped {surface} without deletion, history rewrite, sibling mutation, gate weakening, or unsupported promotion"
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
        "negative_id": f"V6541-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "plan_output_truncated_at_tool_boundary", "The first plan update returned an oversized app-layer payload and received zero planning-output credit.", "Reissue only the compact current plan state and verify the single in-progress step.", "Keep plan updates concise and omit inherited narrative."),
    _negative(2, "skill_read_timed_out", "The first unbounded skill read timed out before attributable EOF evidence.", "Read explicit bounded line windows through the declared final line and verify EOF.", "Use bounded line windows for long skill files."),
    _negative(3, "foreach_pipeline_parser_fault", "A PowerShell foreach block was piped directly and failed before execution.", "Materialize foreach output into an array before piping to JSON serialization.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(4, "manifest_summary_emitted_entries", "A manifest summary accidentally emitted its entire entries array and the display truncated.", "Project only scalar counts, exclusions, and mismatch totals; verify blobs separately in batch.", "Never serialize entry-bearing manifests without an explicit scalar projection."),
    _negative(5, "combined_ancestry_wrapper_timeout", "A combined ancestry and remote wrapper timed out without an attributable aggregate result.", "Split head, parent, ancestry, status, and live-remote checks into bounded isolated probes.", "Do not combine cold Git and network checks."),
    _negative(6, "isolated_parent_probe_timeout", "The first isolated parent probe also timed out before producing a result.", "Use git cat-file with a larger bound and parse the direct parent line.", "Prefer direct object reads for exact parent checks."),
    _negative(7, "negative_register_summary_overbroad", "A negative-register summary included all 150 mutation rows and truncated.", "Read only named scalar properties and mutation counts.", "Select scalar properties before serialization."),
    _negative(8, "fast_forward_output_overlarge", "The safe fast-forward succeeded but emitted a large inherited path summary that truncated.", "Audit exact head, branch, clean state, divergence, and fresh remote separately.", "Suppress or bound diffstat-like output for large inherited fast-forwards."),
    _negative(9, "frozen_corpus_rows_field_assumption", "The first novelty query assumed a nonexistent rows field after correctly observing the total count.", "Use the actual prior_proposals and new_proposals arrays and verify their counts.", "Inspect exact JSON schema keys before binding a query."),
    _negative(10, "standards_query_foreach_parser_fault", "A standards-source inventory repeated the empty-pipe PowerShell parser fault.", "Materialize the result array before serialization.", "Apply the foreach materialization guard to all inventories."),
    _negative(11, "source_search_output_exceeded_context", "A combined standards and research-source web query returned an oversized result and received zero bounded-source-review credit.", "Use direct official URLs and one bounded targeted query at a time.", "Never combine broad source searches when direct primary URLs are available."),
    _negative(12, "combined_status_negative_probe_timeout", "A combined status and negative-register probe timed out without attributable output.", "Run status/head and register projection as separate bounded probes.", "One cold subsystem per bounded probe."),
    _negative(13, "negative_register_path_assumption", "A scalar probe used a nonexistent root-level negative-register path and returned nulls plus an error.", "Discover the exact final/retained-negative-register.json path before reading.", "Use rg --files before assuming lifecycle receipt locations."),
    _negative(14, "negative_register_depth_projection_overbroad", "A depth-limited serialization still emitted the full synthetic-mutation array.", "Project the eight named scalar fields directly and never serialize the source object.", "Treat depth as insufficient; construct a new scalar object."),
    _negative(15, "script_inventory_foreach_parser_fault", "A script-size inventory piped directly from foreach and failed before execution.", "Materialize the rows, then serialize the array.", "Reuse the tested foreach materialization pattern."),
    _negative(16, "broad_route_search_timeout", "A repository-wide route-text search timed out before attributable results.", "Restrict the search to the exact Liora packet and closeout builder.", "Scope text searches to the smallest authoritative directory."),
    _negative(17, "overview_patch_context_mismatch", "The first large overview patch did not apply because inherited mojibake prevented exact context matching.", "Keep the failed patch as zero credit, add the new function with ASCII context, then remove the legacy block by one bounded mechanical replacement.", "Use small ASCII anchors around inherited non-ASCII content."),
    _negative(18, "method_flow_redundant_validated_transition", "The first Method Flow build attempted an explicit validated transition after the passing witness had already promoted the method and failed closed.", "Remove the redundant transition, rebuild the temporary ledger, retain the failed invocation, and promote only validated to preferred.", "Inspect runner state effects: a passing witness performs candidate-to-validated promotion automatically."),
    _negative(19, "workflow_runner_one_off_route_enum_mismatch", "The first workflow audit rejected a one-off future-task route because the runner accepts only its existing-task messaging enum; it also warned that object-shaped placeholders are not recognized.", "Represent the runner's live-phase no-contact policy with its supported enum, retain the one-off post-closeout creation authority in explicit extension fields, and use a string placeholder in the cycle.", "Model special post-closeout task creation as an explicit extension without weakening the runner's live-phase messaging guard."),
    _negative(20, "privacy_scanner_credential_label_false_positive", "The first x1 scan treated six contextual API-key labels with no secret values as confirmed credentials and failed closed.", "Retain the failed scan, require credential assignments or bearer-shaped values rather than labels alone, and rerun every public x1 path.", "Credential scanning must distinguish a protected dependency label from an actual assigned secret while preserving bearer and assignment detection."),
]

REJECTED_COLLISIONS = [
    {"candidate": "generic kiln safety checklist", "reason": "Too broad to distinguish bounded fields or protected authority gates."},
    {"candidate": "generic ceramics provenance", "reason": "Mechanism underspecified; replaced by separate clay, glaze, test-tile, and asset bindings."},
    {"candidate": "W3C PROV ceramic batch profile", "reason": "W3C PROV already appears in the frozen chain; replaced by mechanism-specific ledgers."},
    {"candidate": "generic heat equation board", "reason": "Replaced by typed Fourier energy, boundary, tensor, and unit obligations."},
    {"candidate": "generic phase-field board", "reason": "Split into distinct Cahn-Hilliard and Allen-Cahn conservation/dissipation mechanisms."},
    {"candidate": "digital product passport for pottery", "reason": "Broad product-passport mechanisms already overlap frozen identity work."},
    {"candidate": "generic occupational safety proxy", "reason": "Replaced by silica, ventilation, interlock, maintenance, workload, and authority-specific surfaces."},
    {"candidate": "generic accessibility checklist", "reason": "Replaced by a firing-step, error-summary, noncolour, focus, and print contract."},
    {"candidate": "generic cultural rights matrix", "reason": "Replaced by explicit material/design rights and Maori-authority reservations."},
    {"candidate": "Materials Project analysis", "reason": "Would require an account key and real data; narrowed to zero-query readiness."},
]
