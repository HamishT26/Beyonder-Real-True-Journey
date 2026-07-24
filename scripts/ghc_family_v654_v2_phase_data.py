#!/usr/bin/env python3
"""Frozen Elowen Cairn v654-v2 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v654-v2"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "solo evidence-and-continuity steward"
HOPE = (
    "leave a precise, recoverable record that preserves failures and protected gates "
    "while adding genuinely useful work"
)
BRANCH = "codex/GHC-Family/elowen-cairn-v654-v2-full-tools"
PHASE_ROOT = "docs/elowen-cairn/v654-v2"

SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_HEAD = "105d7fb75e9948ced0362f2c22066d4f15b4e330"
SOURCE_ORIGIN = "180a9b42330be6494e6a1ea3700e001860cffb3d"
SOURCE_X1 = "e5d685fb3a4a84af32fe5914eb0f8d069c854e97"
SOURCE_EVIDENCE = "136d55ba5af1f4f596da0c47d9be931a785cdb18"
SOURCE_FIRST_CLOSEOUT = "10058ab90152d6a1483cddb5654925b07f878fd0"
PRIOR_FROZEN = 1690
INHERITED_SEALED_NEGATIVES = 10791
INHERITED_EXTERNAL_NEGATIVES = 6
INHERITED_NEGATIVES = 10797
INHERITED_OPEN_GAPS = 78
INHERITED_EXACT_GATES = 79
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "letterpress printing and hand bookbinding, including type, paper, ink, imposition, "
    "press setup, proof correction, collation, accessible notice, workload control, and "
    "shift handover, as a synthetic learning lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED_GATES = [
    "empirical_data_and_real_likelihood",
    "real_participants_workers_or_operators",
    "professional_machinery_chemical_environmental_and_conservation_authority",
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
            "Emit unresolved decision rights and reservations only; make no machinery-safety, "
            "chemical, environmental, conservation, publishing, rights, remedy, legal, cultural, "
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
        "proposal_id": f"V6542-P{number:02d}",
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
        "novelty_against_1690_frozen_proposals": (
            "The complete 1,690-row inherited title audit found no proposal combining the "
            f"letterpress/bookbinding mechanism frozen here: {title}."
        ),
    }


_P = [
    (1, "Letterpress typecase glyph, foundry source, face, style, point size, sorts count, damage quarantine, and provenance ledger", "typecase-glyph-lineage", "Freed ID and CBR Heart", "completed", ["SRC-LOC-PAPER"], "typecase glyph and sorts lineage"),
    (2, "Letterpress composition job, manuscript revision, line measure, leading, hyphenation, justification, correction, and proof-hold board", "composition-proof-hold", "THOS Body", "completed", ["SRC-LOC-BOOKS"], "composition revision and proof hold"),
    (3, "Letterpress imposition sheet, page order, signature, work-and-turn state, gripper, trim, blank-page, and refusal map", "imposition-signature-map", "Freed ID and CBR Heart", "completed", ["SRC-LOC-BOOKS"], "imposition and signature mapping"),
    (4, "Letterpress paper stock mill, lot, grain direction, basis weight, caliper, moisture acclimation, substitution, and hold ledger", "paper-stock-lineage", "Freed ID and CBR Heart", "completed", ["SRC-LOC-PAPER", "SRC-BIPM-SI"], "paper stock lineage and substitution hold"),
    (5, "Letterpress ink batch, pigment and vehicle label, colour name, viscosity and tack proxy, contamination, substitution, and quarantine board", "ink-batch-quarantine", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ", "SRC-ISO12647"], "ink batch and contamination quarantine"),
    (6, "Letterpress roller diameter, durometer record, stripe setting, glazing status, wash state, adjustment revision, and setup refusal", "roller-setup-refusal", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY", "SRC-BIPM-SI"], "roller setup and adjustment refusal"),
    (7, "Letterpress chase, quoin, furniture, lockup map, type-high gauge, loose-form signal, correction, and print-run hold", "chase-lockup-map", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY", "SRC-BIPM-SI"], "chase lockup and loose-form hold"),
    (8, "Letterpress platen or cylinder packing layer, thickness, compressibility class, crush limit, revision, pressure change, and rollback board", "packing-pressure-revision", "GMUT Mind", "completed", ["SRC-BIPM-SI"], "packing thickness and pressure revision"),
    (9, "Letterpress makeready overlay, pressure hotspot, impression-depth proxy, delta, correction readback, rollback, and release refusal", "makeready-pressure-map", "GMUT Mind", "completed", ["SRC-ISO12647", "SRC-BIPM-SI"], "makeready pressure hotspot map"),
    (10, "Letterpress feed board sheet count, double-feed signal, gripper edge, registration mark, jam state, restart refusal, and receipt", "feed-registration-jam", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "feed registration and jam refusal"),
    (11, "Letterpress guard, interlock, power and isolation state, unexpected transition, alarm acknowledgement, competent reset, and release refusal", "press-interlock-state", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "press guarding and isolation refusal"),
    (12, "Print-shop ink, solvent and cleaning-agent label, safety-data link, ventilation state, ignition-source hold, spill state, and refusal board", "print-chemical-boundary", "Freed ID and CBR Heart", "completed", ["SRC-WORKSAFE-HAZ"], "print chemical label and ventilation boundary"),
    (13, "Print-shop noise, manual handling, repetitive task, workload budget, fatigue flag, rotation, stop-work, and handover board", "print-workload-boundary", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "printing workload and harm-stop structure"),
    (14, "Print-shop wash-up rag, waste ink, solvent container, contamination class, segregation, discharge hold, disposal route, and receipt", "print-waste-hold", "Freed ID and CBR Heart", "completed", ["SRC-EPA-DISPOSAL", "SRC-RMA-DISCHARGE"], "printing waste segregation and discharge hold"),
    (15, "Letterpress drying interval, set-off observation, rub-resistance proxy, stack height, interleaf state, uncertainty, and release refusal", "ink-drying-release", "GMUT Mind", "completed", ["SRC-ISO12647", "SRC-BIPM-SI"], "ink drying and set-off refusal"),
    (16, "Letterpress proof approval version, correction mark, readback, unresolved error, author-state placeholder, print-run hold, and audit trail", "proof-correction-readback", "THOS Body", "completed", ["SRC-LOC-BOOKS"], "proof correction and run hold"),
    (17, "Letterpress edition, impression, print-run sequence, spoilage, overrun, cancellation, copy identifier, and lineage ledger", "edition-impression-lineage", "Freed ID and CBR Heart", "completed", ["SRC-ISBN", "SRC-RFC9562"], "edition and impression lineage"),
    (18, "Hand-binding signature collation, gathering order, duplicate or missing section, sewing station, correction, quarantine, and receipt", "binding-collation-hold", "Freed ID and CBR Heart", "completed", ["SRC-LOC-BOOKS"], "binding signature collation and hold"),
    (19, "Accessible print-production ticket heading, table header, error summary, noncolour hold, focus order, reflow, print order, and structural audit", "accessible-print-ticket", "THOS Body", "completed", ["SRC-WCAG22"], "accessible print-production ticket structure"),
    (20, "Letterpress edition-change queue, proof-signoff latency, unresolved lockup defect, dual readback, work-in-progress limit, break trigger, and owner-transfer board", "letterpress-owner-transfer", "THOS Body", "completed", ["SRC-WORKSAFE-MACHINERY"], "letterpress edition-change workload and owner transfer"),
    (21, "GMUT Reynolds thin-film ink field, viscosity, film gap, pressure gradient, boundary flux, conservation, unit, and observation-firewall board", "reynolds-ink-film", "GMUT Mind", "completed", ["SRC-REYNOLDS", "SRC-BIPM-SI"], "typed Reynolds thin-film ink obligations"),
    (22, "GMUT Lucas-Washburn paper-capillary field, surface tension, viscosity, pore radius, contact angle, penetration, unit, and observation-firewall board", "lucas-washburn-paper", "GMUT Mind", "completed", ["SRC-LUCAS-WASHBURN", "SRC-BIPM-SI"], "typed Lucas-Washburn paper-capillary obligations"),
    (23, "GMUT Kelvin-Voigt packing field, elastic modulus, viscosity, strain, strain rate, dissipation, unit, and observation-firewall board", "kelvin-voigt-packing", "GMUT Mind", "completed", ["SRC-KELVIN-VOIGT", "SRC-BIPM-SI"], "typed Kelvin-Voigt packing obligations"),
    (24, "THOS letterpress setup, loose form, feed jam, stop-work, workload budget, correction readback, and shift-handover proxy", "thos-letterpress-handover", "THOS Body", "represented", ["SRC-WORKSAFE-MACHINERY"], "letterpress setup and handover proxy"),
    (25, "THOS proof correction, binding collation, missing signature, correction latency, fatigue flag, harm stop, and handover proxy", "thos-binding-correction", "THOS Body", "represented", ["SRC-LOC-BOOKS"], "proof and binding correction proxy"),
    (26, "Freed ID UUIDv7 print job, sheet, signature and copy binding, clock rollback, duplicate identifier, privacy, and nonproduction profile", "uuidv7-print-assets", "Freed ID and CBR Heart", "represented", ["SRC-RFC9562"], "UUIDv7 print-asset profile"),
    (27, "Freed ID ISBN registrant element, publication element, check digit, edition and impression relation, agency reservation, privacy, and nonproduction profile", "isbn-edition-profile", "Freed ID and CBR Heart", "represented", ["SRC-ISBN"], "ISBN edition and impression profile"),
    (28, "Freed ID DOI prefix, suffix, referent metadata, work-edition-manifestation relation, resolution refusal, privacy, and nonproduction profile", "doi-print-referent", "Freed ID and CBR Heart", "represented", ["SRC-DOI"], "DOI print referent profile"),
    (29, "GMUT real letterpress spectral reflectance, solid-ink density, paper field, provenance, uncertainty, standards access, and zero-row measurement adapter", "print-measurement-zero-row", "GMUT Mind", "open_gap", ["SRC-ISO12647"], "letterpress measurement readiness"),
    (30, "CBR printing machinery and chemical safety, environmental discharge, conservation, publishing and design rights, accessibility, remedy, affected-party, legal, cultural, data-governance, and Maori-authority reservation", "printing-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-WORKSAFE-MACHINERY", "SRC-WORKSAFE-HAZ", "SRC-EPA-DISPOSAL", "SRC-NZ-COPYRIGHT", "SRC-TE-MANA", "SRC-LOCAL-CONTEXTS"], "printing and binding authority reservation"),
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
    _source("SRC-WORKSAFE-MACHINERY", "current", "official_regulator_guidance", "WorkSafe New Zealand: safe use of machinery", "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "Current guarding and machinery-risk context only; no workplace assessment, competence, or compliance finding."),
    _source("SRC-WORKSAFE-HAZ", "current", "official_regulator_guidance", "WorkSafe New Zealand: hazardous-substance information, instruction, supervision, and training", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/information-instruction-supervision-training/", "Refusal and handover context only; no workplace approval."),
    _source("SRC-EPA-DISPOSAL", "current", "official_regulator_notice", "New Zealand EPA disposal notice", "https://www.epa.govt.nz/hazardous-substances/rules-notices-and-how-to-comply/epa-notices-rules-you-must-follow/disposal-notice/", "Disposal context only; no classification or disposal decision."),
    _source("SRC-RMA-DISCHARGE", "watch", "official_legislation", "Resource Management Act 1991 section 15", "https://www.legislation.govt.nz/act/public/1991/0069/latest/DLM231977.html", "Watched legal context only; no legal interpretation or discharge authorization."),
    _source("SRC-LOC-PAPER", "current", "official_preservation_guidance", "Library of Congress: care, handling, and storage of works on paper", "https://www.loc.gov/preservation/care/paper.html", "Synthetic paper handling fields only; no conservation treatment decision."),
    _source("SRC-LOC-BOOKS", "current", "official_preservation_guidance", "Library of Congress: preserving your books", "https://guides.loc.gov/preserving-your-books", "Synthetic book and binding care fields only; no professional conservation decision."),
    _source("SRC-ISO12647", "stable", "official_standards_catalogue", "ISO 12647-1 graphic technology process-control parameters and measurement methods", "https://www.iso.org/standard/57816.html", "Typed parameters and zero-row readiness only; no conformance, measurement, or production claim."),
    _source("SRC-REYNOLDS", "stable", "primary_historical_source", "Reynolds, On the theory of lubrication", "https://ndlsearch.ndl.go.jp/books/R100000136-I1572543024476456448", "Typed thin-film obligations only; no empirical ink-transfer model."),
    _source("SRC-LUCAS-WASHBURN", "stable", "primary_research", "Washburn, The dynamics of capillary flow", "https://doi.org/10.1103/PhysRev.17.273", "Typed capillary-flow obligations only; no paper measurement or fitted parameter."),
    _source("SRC-KELVIN-VOIGT", "stable", "primary_research", "A reappraisal and generalization of the Kelvin-Voigt model", "https://doi.org/10.1016/j.mechrescom.2008.09.005", "Typed viscoelastic obligations only; no press-packing characterization."),
    _source("SRC-BIPM-SI", "current", "official_metrology_reference", "BIPM SI Brochure", "https://www.bipm.org/en/publications/si-brochure", "Unit declarations only; no calibration or measurement assurance."),
    _source("SRC-RFC9562", "stable", "official_internet_standard", "RFC 9562 Universally Unique IDentifiers", "https://www.rfc-editor.org/rfc/rfc9562.html", "Synthetic UUID vectors only; no production identity, uniqueness guarantee, or lifecycle governance."),
    _source("SRC-ISBN", "current", "official_identifier_guidance", "International ISBN Agency Users' Manual", "https://www.isbn-international.org/index.php/content/isbn-users-manual/29", "Synthetic ISBN fields only; no allocation, registrant, publication, or agency decision."),
    _source("SRC-DOI", "current", "official_identifier_guidance", "DOI Foundation DOI Handbook", "https://www.doi.org/doi-handbook/html/", "Synthetic DOI metadata only; no registration, resolution, rights, or persistence claim."),
    _source("SRC-WCAG22", "current", "official_web_standard", "W3C Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Structural accessibility checks only; manual and affected-user evaluation remain reserved."),
    _source("SRC-NZ-COPYRIGHT", "watch", "official_legislation", "Copyright Act 1994", "https://www.legislation.govt.nz/act/public/1994/0143/latest/DLM345634.html", "Watched legal context only; no interpretation, ownership, licence, remedy, or publishing decision."),
    _source("SRC-TE-MANA", "current", "maori_authority_source", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Maori data decisions remain under Maori authority; no authority is delegated to the repository."),
    _source("SRC-LOCAL-CONTEXTS", "current", "affected_community_governance_source", "Local Contexts Traditional Knowledge Labels", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Cultural and traditional-knowledge rights reservation only; no label is applied."),
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
    "ghc-family-letterpress-type-paper-lineage",
    "ghc-family-imposition-signature-map",
    "ghc-family-press-lockup-refusal",
    "ghc-family-print-chemical-boundary",
    "ghc-family-print-waste-hold",
    "ghc-family-proof-binding-readback",
    "ghc-family-gmut-print-field-typing",
    "ghc-family-thos-letterpress-handover",
    "ghc-family-freed-id-print-assets",
    "ghc-family-printing-authority-reservation",
]
RUNNER_IDEAS = [
    "ghc_family_letterpress_material_ledger.py",
    "ghc_family_press_state_boards.py",
    "ghc_family_print_worker_boundary_boards.py",
    "ghc_family_print_waste_release_refusal.py",
    "ghc_family_gmut_print_fields.py",
    "ghc_family_thos_letterpress_proxy.py",
    "ghc_family_freed_id_print_profiles.py",
    "ghc_family_accessible_print_audit.py",
    "ghc_family_v654_v2_detailed_validator.py",
    "ghc_family_v654_v2_bounded_suite.py",
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
        "negative_id": f"V6542-X1-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


INHERITED_EXTERNAL_NEGATIVE_RECORDS = [
    {
        "negative_ids": ["V6541-EXT-N01"],
        "signature": "committed_validator_proposal_ledger_filename_assumption",
        "failed": "A post-seal validator assumed the wrong committed proposal-ledger filename and received zero validation credit.",
        "recovery": "Discover and bind the committed filename before the bounded validator retry.",
        "recurrence_guard": "Resolve exact committed receipt and ledger names from the tree before validation.",
    },
    {
        "negative_ids": ["V6541-EXT-N02"],
        "signature": "windows_wildcard_path_assumption",
        "failed": "A Windows wildcard path assumption failed before producing attributable evidence.",
        "recovery": "Use literal paths and an explicitly materialized bounded file inventory.",
        "recurrence_guard": "Never depend on wildcard expansion for exact Windows validation paths.",
    },
    {
        "negative_ids": ["V6541-EXT-N03", "V6541-EXT-N04", "V6541-EXT-N05"],
        "signature": "workflow_commit_cap_property_projection_assumptions",
        "failed": "Three incorrect workflow commit-cap property projections failed closed and received zero credit.",
        "recovery": "Inspect the exact workflow receipt schema and bind only its committed property names.",
        "recurrence_guard": "Discover receipt keys before projecting workflow commit-cap fields.",
    },
    {
        "negative_ids": ["V6541-EXT-N06"],
        "signature": "external_bridge_repo_import_path_omission",
        "failed": "The first canonical attempt ran zero tests because the external bridge omitted the repository from its import path.",
        "recovery": "Apply the narrow external in-memory import-path correction without changing a repository byte.",
        "recurrence_guard": "Preflight the repository import root in external test bridges before invoking the canonical selector.",
    },
]


X1_OPERATIONAL_NEGATIVES = [
    _negative(1, "startup_skill_memory_discovery_timeout", "The first combined skill-file and memory-registry discovery exceeded its time bound with no attributable result.", "Split skill discovery from memory lookup and use exact names or bounded filters.", "Use one cold filesystem or memory scan per bounded probe."),
    _negative(2, "filtered_skill_memory_discovery_timeout", "The second filtered directory and memory lookup also exceeded its bound before output.", "Probe exact expected skill names first, then use filesystem filters independently.", "Do not combine directory enumeration with a large registry search."),
    _negative(3, "foreach_pipeline_parser_fault", "A PowerShell foreach statement was piped directly and failed before execution.", "Materialize foreach output in an array before piping.", "Never pipe directly from a PowerShell foreach statement."),
    _negative(4, "combined_source_probe_timeout", "A combined D-drive, Git root, branch, head, and status probe timed out without attributable output.", "Split storage, exact head, and cleanliness into isolated bounded probes.", "One cold Git or filesystem subsystem per probe."),
    _negative(5, "validation_record_path_assumption", "A blob-size inventory assumed final-validation-record.json was under validation instead of final.", "Discover exact committed filenames before binding blob paths.", "Use the exact tree inventory rather than lifecycle filename guesses."),
    _negative(6, "frozen_proposal_id_field_assumption", "The first frozen-corpus projection used id rather than proposal_id and reported false missing fields.", "Inspect top-level and entry keys before binding the query.", "Bind proposal_id and title only after schema discovery."),
    _negative(7, "unavailable_dotnet_hash_helper_assumption", "The first frozen-corpus hash projection assumed unavailable HashData and ToHexString helpers.", "Use the installed SHA256 provider and explicit hexadecimal formatting.", "Probe runtime APIs or use the compatible streaming provider."),
    _negative(8, "proposal_schema_field_name_assumption", "The first Tamar proposal completeness query used shortened field names and produced a false failure count.", "Bind the committed null_or_failure_condition, official_or_primary_source_needs, falsifier_or_acceptance_gate, and rollback_or_recovery names.", "Inspect exact proposal keys before validating."),
    _negative(9, "worktree_add_wrapper_timeout_after_completion", "The owned worktree-add wrapper timed out although the operation completed successfully.", "Audit exact path, registration, branch, head, clean state, and running Git processes before any retry.", "Never retry a timed-out worktree mutation before a complete state audit."),
    _negative(10, "large_phase_data_patch_context_mismatch", "The first large phase-data patch matched no bytes at a source-list context.", "Replace the new owner-local module as one exact file and retain the failed patch.", "Prefer whole-file replacement for a new generated data module when inherited Unicode context is unstable."),
    _negative(11, "overview_patch_unicode_context_mismatch", "The first overview-function patch matched no bytes at an inherited Unicode heading context.", "Replace only the owner-local function between stable ASCII definition markers.", "Use stable ASCII function boundaries instead of inherited mojibake in large generated-text patches."),
    _negative(12, "windows_rg_wildcard_path_assumption", "A Windows ripgrep inventory passed a wildcard as a literal path and failed before a complete stale-string scan.", "Enumerate explicit files or search a literal directory with a filename filter.", "Do not pass unresolved Windows wildcard paths to ripgrep."),
    _negative(13, "workflow_single_seat_cycle_rejected", "The first workflow-plan audit rejected a one-label no-successor cycle and wrote two open-gap issues with zero workflow-pass credit.", "Retain the failed packet and represent the no-successor boundary as a second nonowner route label while normalizing only the one authorized Elowen assignment.", "Preflight the current runner's minimum two-label cycle rule without inventing a successor owner or phase."),
]

REJECTED_COLLISIONS = [
    {"candidate": "generic printing checklist", "reason": "Too broad to distinguish press, proof, binding, and authority mechanisms."},
    {"candidate": "generic print provenance", "reason": "Split into type, paper, ink, edition, signature, and copy lineage."},
    {"candidate": "generic press safety", "reason": "Replaced by guard, interlock, feed, chemical, waste, workload, and exact-authority surfaces."},
    {"candidate": "generic ink model", "reason": "Split into Reynolds thin-film, drying refusal, and zero-row measurement mechanisms."},
    {"candidate": "generic paper absorption", "reason": "Narrowed to typed Lucas-Washburn obligations with no empirical claim."},
    {"candidate": "generic viscoelastic packing", "reason": "Narrowed to Kelvin-Voigt strain, rate, dissipation, unit, and observation-firewall fields."},
    {"candidate": "generic publishing identifier", "reason": "Split into UUIDv7, ISBN, and DOI nonproduction profiles."},
    {"candidate": "generic accessibility checklist", "reason": "Narrowed to a print-production ticket with specific structural checks."},
    {"candidate": "generic cultural rights matrix", "reason": "Replaced by explicit affected-party, data-governance, and Maori-authority reservations."},
    {"candidate": "real print quality analysis", "reason": "Requires measurements, standards access, and independent review; narrowed to zero-row readiness."},
]
