#!/usr/bin/env python3
"""Frozen x1 catalogue for Lyren Moss's solo v658-v8 phase."""

from __future__ import annotations


def source(source_id: str, title: str, publisher: str, url: str, status: str, use: str) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "publisher": publisher,
        "url": url,
        "status": status,
        "observed_on": "2026-08-02",
        "use": use,
    }


OFFICIAL_SOURCES = [
    source("MPI-FCP", "Food control plans", "New Zealand Food Safety, Ministry for Primary Industries", "https://www.mpi.govt.nz/food-business/running-a-food-business/food-control-plans", "current", "risk-control and documented-plan vocabulary only; no registration, verification, food-safety, or compliance claim"),
    source("MPI-GOP", "Applying Good Operating Practice to your business", "New Zealand Food Safety, Ministry for Primary Industries", "https://www.mpi.govt.nz/food-business/food-safety-codes-standards/good-operating-practice/applying-good-operating-practice-to-your-business", "current", "documented operating-practice vocabulary only; no tailored procedure, professional advice, or compliance claim"),
    source("MPI-RECALL", "Food recall guidance for businesses", "New Zealand Food Safety, Ministry for Primary Industries", "https://www.mpi.govt.nz/food-business/food-recalls/food-recall-guidance-for-businesses", "current", "batch identification, hold, trace, notification, reconciliation, and mock-recall vocabulary only; no real risk assessment, recall, or regulator contact"),
    source("FSANZ-ALCOHOL-LABELLING", "Labelling of alcoholic beverages", "Food Standards Australia New Zealand", "https://www.foodstandards.gov.au/consumer/labelling/Labelling-of-alcoholic-beverages", "current_watch", "alcohol-content, standard-drink, pregnancy-warning, energy-labelling, and legibility vocabulary only; no label approval or compliance claim"),
    source("FSANZ-CODE", "Food Standards Code legislation", "Food Standards Australia New Zealand", "https://www.foodstandards.gov.au/food-standards-code/legislation", "current_watch", "Code structure and beer or alcoholic-beverage standard references only; no legal interpretation or conformance claim"),
    source("NZ-ALCOHOL-ACT", "Sale and Supply of Alcohol Act 2012", "New Zealand Legislation", "https://www.legislation.govt.nz/act/public/2012/0120/latest/DLM4925300.html", "current_watch", "alcohol-sale and supply authority-reservation context only; no licensing, sale, supply, or legal advice"),
    source("WORKSAFE-WES", "Workplace exposure standards and biological exposure indices", "WorkSafe New Zealand", "https://www.worksafe.govt.nz/topic-and-industry/monitoring/workplace-exposure-standards-and-biological-exposure-indices/", "current_watch", "airborne-contaminant and exposure-boundary vocabulary only; no hazard assessment, workplace instruction, or safety determination"),
    source("GS1-TRACEABILITY", "GS1 Global Traceability Standard", "GS1", "https://www.gs1.org/standards/gs1-global-traceability-standard/current-standard", "current", "traceable-object, batch or lot, transformation-event, disposition, and data-sensitivity vocabulary only; no identifier allocation or interoperability claim"),
    source("EBC-ANALYTICA", "Analytica-EBC and European Brewery Convention analysis work", "European Brewery Convention", "https://europeanbreweryconvention.eu/", "current_watch", "brewing, malting, sampling, laboratory-method, and revision vocabulary only; no method access, laboratory competence, result, or professional claim"),
    source("BA-DRAUGHT-MANUAL", "Draught Beer Quality Manual", "Brewers Association", "https://www.brewersassociation.org/educational-publications/draught-beer-quality-manual/", "current_watch", "draught component, gas, sanitation, and line-state vocabulary only; no equipment operation, service, or beverage-quality claim"),
    source("W3C-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "entity, activity, derivation, revision, invalidation, and attribution lineage"),
    source("W3C-WCAG-22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "machine-checkable document structure and notice vocabulary; manual and affected-user evaluation remain reserved"),
    source("W3C-VC-DM-20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model-2.0/", "current", "synthetic nonproduction artifact-envelope vocabulary only; no live identity, proof, or trust"),
    source("W3C-DATA-INTEGRITY", "Verifiable Credential Data Integrity 1.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-integrity/", "current", "proof-configuration vocabulary only; no key, signature, verification, security, or interoperability claim"),
    source("RFC-8785", "JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "deterministic JSON representation vocabulary only; no cryptographic assurance"),
    source("NZ-PRIVACY-PRINCIPLES", "Privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "purpose, minimisation, correction, retention, use, and disclosure reservations only; no legal advice"),
    source("TE-MANA-RARAUNGA", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "Māori data rights, interests, governance, collective benefit, and authority reservation only"),
    source("LOCAL-CONTEXTS-TK", "Traditional Knowledge Labels", "Local Contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "current_watch", "community-defined notice and authority-reservation context only; no label selection or application"),
]


PROTECTED_GATES = [
    "real_people_workers_consumers_businesses_breweries_suppliers_distributors_communities_and_affected_parties",
    "real_ingredients_beverages_batches_vessels_packages_chemicals_measurements_samples_results_and_records",
    "real_brewing_cleaning_sanitation_processing_packaging_labelling_storage_distribution_sale_supply_recall_or_release_decision",
    "professional_brewing_food_safety_laboratory_metrology_workplace_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_fermentation_kinetics_mass_balance_process_control_or_confirmation",
    "blind_matched_budget_thos_real_arms_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_language_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def proposal(number: int, title: str, slug: str, pillar: str, mechanism: str, sources: list[str]) -> dict:
    if number <= 23:
        expected, approval, lane = "completed", "safe_now_bounded_structural_formal_or_synthetic_software", "x2_owner_local_bounded_synthetic"
    elif number <= 28:
        expected, approval, lane = "represented", "candidate_proxy_protocol_or_nonproduction_schema", "x2_owner_local_representation_only"
    elif number == 29:
        expected, approval, lane = "open_gap", "candidate_external_data_readiness_without_transport_or_real_rows", "x2_owner_local_zero_row_readiness"
    else:
        expected, approval, lane = "exact_gate", "outside_hamish_authority_affected_party_legal_cultural_and_maori_authority_required", "not_executed_authority_reservation"
    return {
        "proposal_id": f"V6588-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported empirical, professional, production, food-safety, release, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, Theory-of-Everything, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or crosses a protected person, beverage, production, professional, safety, rights, legal, cultural, Māori-authority, identity, or Stage 20 gate.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"surfaces/{slug}/contract.json", f"surfaces/{slug}/mutation-results.json", f"surfaces/{slug}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no real-person, real-beverage, empirical, production, food-safety, release, participant, professional, workplace-safety, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        "rollback_or_recovery": "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, businesses, beverages, production state, sibling lanes, external systems, rights, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected,
    }


PROPOSAL_SPECS = [
    ("Fictional brewery scope card with zero real batches, no production use, and release refusal", "brewery-scope-card", "All pillars", "fictional brewery alias, zero-batch declaration, bounded purpose, production-use refusal, and release abstention", ["MPI-FCP", "MPI-GOP", "W3C-PROV"]),
    ("Synthetic malt, hop, yeast, water, adjunct, and package-lot intake passport with acceptance hold", "brewery-ingredient-intake", "THOS Body and Freed ID", "ingredient and package-lot aliases, supplier placeholder, receipt state, specification placeholder, quarantine, and acceptance refusal", ["GS1-TRACEABILITY", "MPI-GOP", "W3C-PROV"]),
    ("Brewing-water source and treatment profile with sampling placeholders and no potability claim", "brewery-water-profile", "THOS Body and CBR Heart", "water-source alias, treatment step, sampling placeholder, unit, uncertainty, hold, and potability refusal", ["MPI-FCP", "MPI-GOP", "W3C-PROV"]),
    ("Malt and hop storage-condition ledger with age, lot, pest, moisture, and suitability holds", "brewery-material-storage", "THOS Body", "material lot, storage zone, age, moisture placeholder, pest cue, excursion, quarantine, and suitability refusal", ["MPI-GOP", "EBC-ANALYTICA", "W3C-PROV"]),
    ("Recipe and process-specification revision pin with supersession, dependency, and production-instruction refusal", "brewery-recipe-revision", "THOS Body and CBR Heart", "recipe alias, process revision, supersession, dependency, change reason, approval placeholder, and production-instruction refusal", ["W3C-PROV", "RFC-8785", "MPI-GOP"]),
    ("Brewhouse vessel, valve, hose, and transfer-topology graph with isolation and operation abstention", "brewery-transfer-topology", "THOS Body", "vessel and line aliases, connection graph, valve state, transfer boundary, isolation hold, and equipment-operation refusal", ["BA-DRAUGHT-MANUAL", "MPI-GOP", "W3C-PROV"]),
    ("Mash-rest and conversion-state schedule with unit checks, sample placeholders, and setpoint refusal", "brewery-mash-schedule", "THOS Body and GMUT Mind", "mash stage, time and temperature units, conversion sample placeholder, deviation, hold, and process-setpoint refusal", ["EBC-ANALYTICA", "MPI-GOP", "W3C-PROV"]),
    ("Boil and hop-addition event docket with lot lineage, clock uncertainty, and bitterness-prediction abstention", "brewery-boil-hop-docket", "THOS Body and GMUT Mind", "boil stage, hop lot, event clock, quantity unit, uncertainty, correction, and bitterness-prediction refusal", ["EBC-ANALYTICA", "GS1-TRACEABILITY", "W3C-PROV"]),
    ("Cleaning and sanitation state register with chemical-lot, concentration placeholder, rinse, and verification holds", "brewery-cleaning-state", "THOS Body and CBR Heart", "cleaning cycle, chemical lot, concentration placeholder, contact window, rinse state, verification placeholder, and use refusal", ["MPI-GOP", "WORKSAFE-WES", "W3C-PROV"]),
    ("Yeast culture, propagation, pitch, harvest, and generation lineage with viability and biosecurity abstention", "brewery-yeast-lineage", "THOS Body and Freed ID", "yeast alias, culture and propagation lineage, generation, viability placeholder, quarantine, and pitch refusal", ["EBC-ANALYTICA", "GS1-TRACEABILITY", "W3C-PROV"]),
    ("Fermentation-batch state machine with gravity and temperature placeholders, deviation hold, and verdict refusal", "brewery-fermentation-state", "THOS Body and GMUT Mind", "fermentation batch, stage transition, gravity and temperature placeholders, deviation, correction, hold, and fermentation-verdict refusal", ["EBC-ANALYTICA", "MPI-GOP", "W3C-PROV"]),
    ("Cellar temperature, pressure, and vessel-state record with calibration placeholders and safety abstention", "brewery-cellar-state", "THOS Body", "cellar vessel, temperature and pressure placeholders, calibration state, excursion, isolation, and safety-determination refusal", ["WORKSAFE-WES", "EBC-ANALYTICA", "W3C-PROV"]),
    ("Carbonation and dissolved-gas measurement envelope with unit, method, uncertainty, and package-release refusal", "brewery-carbonation-envelope", "THOS Body and GMUT Mind", "gas identity, measurement method, unit, uncertainty, vessel dependency, conflict hold, and release refusal", ["BA-DRAUGHT-MANUAL", "EBC-ANALYTICA", "W3C-PROV"]),
    ("Maturation, conditioning, and transfer chain with custody, loss placeholder, contamination hold, and completion refusal", "brewery-conditioning-chain", "THOS Body", "conditioning batch, vessel custody, transfer event, loss placeholder, contamination cue, quarantine, and completion refusal", ["GS1-TRACEABILITY", "MPI-GOP", "W3C-PROV"]),
    ("Filtration, centrifugation, and stabilisation batch record with media lineage and suitability abstention", "brewery-filtration-record", "THOS Body", "separation process, media lot, equipment alias, differential placeholder, integrity hold, and suitability refusal", ["EBC-ANALYTICA", "MPI-GOP", "W3C-PROV"]),
    ("Container, closure, can-end, crown, keg, and package-lot integrity docket with release hold", "brewery-package-integrity", "THOS Body and Freed ID", "container and closure lot, packaging event, seam or closure placeholder, damage cue, quarantine, and release refusal", ["GS1-TRACEABILITY", "MPI-RECALL", "W3C-PROV"]),
    ("Alcohol-content, standard-drink, pregnancy-warning, energy, and legibility label reservation board", "brewery-label-reservation", "CBR Heart and THOS Body", "label revision, analytical-result placeholder, alcohol-content and warning fields, legibility state, legal-review hold, and label-approval refusal", ["FSANZ-ALCOHOL-LABELLING", "FSANZ-CODE", "NZ-ALCOHOL-ACT"]),
    ("Blinded sensory-sample and panel docket with randomisation, assessor placeholders, and quality-verdict refusal", "brewery-sensory-reservation", "THOS Body and CBR Heart", "sensory sample alias, randomisation, blinding, assessor-role placeholder, response absence, privacy hold, and quality-verdict refusal", ["EBC-ANALYTICA", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("Laboratory method, standard, instrument, calibration, blank, and result-placeholder provenance record", "brewery-lab-metrology", "THOS Body and GMUT Mind", "method revision, standard lot, instrument alias, calibration state, blank, result placeholder, uncertainty, and competence refusal", ["EBC-ANALYTICA", "RFC-8785", "W3C-PROV"]),
    ("Deviation, nonconformance, correction, and preventive-action lifecycle with disposition-authority refusal", "brewery-nonconformance-lifecycle", "THOS Body and CBR Heart", "deviation, evidence placeholder, containment, correction, preventive action, review placeholder, and disposition refusal", ["MPI-GOP", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("Batch inventory, hold, trace, reconciliation, and mock-recall state machine with zero external action", "brewery-recall-simulation", "THOS Body and CBR Heart", "batch and lot inventory, hold, upstream and downstream trace, reconciliation, mock notification, zero transport, and real-recall refusal", ["MPI-RECALL", "GS1-TRACEABILITY", "W3C-PROV"]),
    ("Carbon-dioxide, cleaning-chemical, pressure, and confined-space hazard reservation with no safety instruction", "brewery-hazard-reservation", "CBR Heart and THOS Body", "hazard class, gas and chemical placeholder, pressure state, access hold, escalation placeholder, and workplace-safety instruction refusal", ["WORKSAFE-WES", "BA-DRAUGHT-MANUAL", "W3C-PROV"]),
    ("GMUT typed fermentation mass-balance and kinetic operator with unit, domain, identifiability, and production firewalls", "gmut-fermentation-operator", "GMUT Mind", "typed substrate and product states, mass-balance placeholder, kinetic operator, unit and domain check, identifiability, falsifier, and production refusal", ["EBC-ANALYTICA", "W3C-PROV", "RFC-8785"]),
    ("THOS deterministic brewery-batch checkpoint receipt with partition digest and orphan isolation", "thos-brewery-checkpoint", "THOS Body", "deterministic synthetic batch partition, dependency digest, checkpoint, bounded retry, orphan quarantine, and throughput-claim refusal", ["W3C-PROV", "RFC-8785", "GS1-TRACEABILITY"]),
    ("THOS synthetic cellar-shift handover proxy with unresolved-batch digest and acknowledgement placeholder", "thos-cellar-handover", "THOS Body and CBR Heart", "synthetic cellar handover, unresolved batch digest, hold conflict, acknowledgement placeholder, escalation, and operational-handover refusal", ["MPI-GOP", "WORKSAFE-WES", "W3C-PROV"]),
    ("Nonproduction Freed ID brewery-batch lineage capsule with amendment, expiry, and live-proof refusal", "freed-id-brewery-batch", "Freed ID", "synthetic batch envelope, digest, transformation lineage, amendment, expiry, revocation hold, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "W3C-PROV"]),
    ("Purpose-bound Freed ID disclosure card for synthetic brewing inputs and packaging with contest route", "freed-id-brewery-provenance", "Freed ID and CBR Heart", "purpose-bound input and packaging disclosure card, field-level withholding reason, correction and contest route, sunset state, and trust-decision refusal", ["W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "GS1-TRACEABILITY"]),
    ("Keyboard-readable brewery batch, hold, laboratory, label, and handover evidence atlas with human-evaluation reservation", "brewery-accessible-evidence-atlas", "CBR Heart and THOS Body", "accessible brewery evidence atlas, scoped tables, noncolour states, source links, reflow, print fallback, and manual-evaluation reservation", ["W3C-WCAG-22", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("MPI, FSANZ, EBC, and GS1 zero-row brewery capability gateway with disabled transport", "brewery-zero-row-gateway", "All pillars", "external food, alcohol-labelling, brewing-method, and traceability capability watch, disabled transport, schema placeholders, zero rows, and external-validation refusal", ["MPI-RECALL", "FSANZ-CODE", "EBC-ANALYTICA", "GS1-TRACEABILITY"]),
    ("CBR brewery worker, consumer, alcohol-harm, water, environment, privacy, recall, remedy, and Māori-authority covenant", "cbr-brewery-authority-covenant", "CBR Heart across all pillars", "worker and consumer safety, alcohol harm, water and environmental interest, business and personal privacy, recall and label notice, remedy, affected-party governance, law, culture, and Māori-authority reservation", ["NZ-PRIVACY-PRINCIPLES", "NZ-ALCOHOL-ACT", "TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-brewery-scope-firewall", "Constrain fictional brewery aliases, zero real batches, bounded purpose, and no production, food-safety, or release use."),
    ("ghc-family-brewery-ingredient-provenance", "Constrain ingredient, package, supplier, lot, receipt, storage, quarantine, and acceptance abstention."),
    ("ghc-family-brewery-process-revision", "Constrain recipe, process, vessel, transfer, mash, boil, cleaning, and revision records without operating instructions."),
    ("ghc-family-brewery-cellar-state", "Constrain yeast, fermentation, cellar, gas, conditioning, filtration, and package states without production conclusions."),
    ("ghc-family-brewery-lab-metrology-boundary", "Constrain methods, instruments, standards, calibration, sensory placeholders, uncertainty, and competence refusal."),
    ("ghc-family-brewery-packaging-labelling-reservation", "Constrain package lineage, label revisions, warning placeholders, trace holds, and legal or release abstention."),
    ("ghc-family-gmut-fermentation-firewall", "Constrain typed fermentation operators, units, domains, identifiability, falsifiers, and process-prediction refusal."),
    ("ghc-family-thos-brewery-checkpoint", "Constrain deterministic batches, checkpoints, bounded retries, orphan isolation, and synthetic handover proxies."),
    ("ghc-family-brewery-freed-id", "Constrain nonproduction batch and ingredient lineage, digests, amendments, expiry, and trust abstention."),
    ("ghc-family-brewery-authority-reservation", "Fail closed around people, beverages, food and workplace safety, alcohol harm, privacy, law, culture, affected parties, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_brewery_scope_firewall.py", "brewery-scope-card"),
    ("ghc_family_brewery_ingredient_provenance.py", "brewery-ingredient-intake"),
    ("ghc_family_brewery_process_revision.py", "brewery-recipe-revision"),
    ("ghc_family_brewery_cellar_state.py", "brewery-fermentation-state"),
    ("ghc_family_brewery_lab_metrology_boundary.py", "brewery-lab-metrology"),
    ("ghc_family_brewery_packaging_labelling_reservation.py", "brewery-label-reservation"),
    ("ghc_family_gmut_fermentation_firewall.py", "gmut-fermentation-operator"),
    ("ghc_family_thos_brewery_checkpoint.py", "thos-brewery-checkpoint"),
    ("ghc_family_brewery_freed_id.py", "freed-id-brewery-batch"),
    ("ghc_family_brewery_authority_reservation.py", "cbr-brewery-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6588-X1-N{number:02d}",
        "scope": "startup_and_x1",
        "signature": slug,
        "observed": failure,
        "credit": 0,
        "retained": True,
        "recovery": recovery,
        "recurrence_guard": guard,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


X1_OPERATIONAL_NEGATIVES = [
    negative(1, "combined-guidance-display-truncated", "The combined lifecycle-guidance display exceeded its bounded output surface, so the affected files did not earn complete-read credit.", "Reread every affected guidance file individually through exact EOF before mutation.", "Keep required instruction-file reads individually attributable when combined output can truncate."),
    negative(2, "bundled-source-git-verifier-no-payload", "The first bundled source Git verifier completed without returning usable scalar verification evidence.", "Rerun branch, head, ancestry, clean-state, divergence, and fresh-remote checks as bounded scalar probes.", "No serialized verifier payload earns credit; split source checks before relying on them."),
    negative(3, "manifest-replay-javascript-backslash-escape", "The first manifest replay wrapper used a non-raw JavaScript template, corrupting Windows backslashes before PowerShell received the repository path.", "Use a raw wrapper string and rerun the read-only manifest replay against exact immutable commits.", "Treat Windows paths as literal data across JavaScript and PowerShell boundaries."),
    negative(4, "final-owner-manifest-scope-filter-mismatch", "The first owner-manifest set audit counted only the documentation prefix and therefore omitted owner-local scripts and tests, reporting a false 22-path mismatch.", "Validate the declared 273 entry blobs plus two explicit self-exclusions across the full final tree and retain the narrower diagnostic at zero credit.", "Derive owner-manifest scope from its declared path set rather than a documentation-only prefix."),
    negative(5, "proposal-audit-wrapper-backtick-syntax", "The first bounded proposal-audit wrapper embedded a PowerShell backtick inside a JavaScript template and failed before execution.", "Use a character-code separator with no cross-language quoting ambiguity and rerun the audit.", "Avoid nested template delimiters in multi-language wrappers."),
    negative(6, "proposal-index-schema-fallback-truncated", "The first proposal-index reader guessed entries or proposals keys, fell through to a full JSON rendering, and exceeded the output budget.", "Inspect the actual top-level keys, then project only prior_proposals and new_proposals in bounded title windows.", "Inspect JSON keys before selectors and never dump a large frozen chain as fallback evidence."),
    negative(7, "branch-absence-show-ref-native-stop", "The first collision probe used a failing show-ref command under stop-on-error semantics, so the expected absent branch aborted the wrapper.", "Use for-each-ref, which returns a bounded empty result for an absent exact ref, then separately verify path and worktree registration absence.", "Probe expected Git-ref absence with a nonexceptional exact selector."),
    negative(8, "route-hash-wrapper-backtick-syntax", "The first route and baton hash wrapper embedded PowerShell escape syntax in a JavaScript template and failed before execution.", "Build revision-path specifications by string concatenation and rerun the exact blob and checkout hash probes.", "Do not nest PowerShell escape characters inside JavaScript template delimiters."),
    negative(9, "git-blob-sha-wrapper-backtick-syntax", "The first byte-stream SHA-256 wrapper again embedded a PowerShell backtick in the JavaScript source and failed before execution.", "Invoke Git with an unquoted no-space repository path through a redirected byte stream and hash those exact blob bytes.", "Prefer delimiter-free argument construction for byte-exact cross-shell hashing."),
    negative(10, "integrated-overview-patch-context-mismatch", "The first semantic integrated-overview patch did not match the exact generated scaffold context and changed no file.", "Insert the new overview as an explicit constant through a small attributable patch, redirect the function, and remove the stale scaffold separately.", "Use small structural patches around generated long-form blocks instead of one large context-sensitive replacement."),
    negative(11, "legacy-overview-regex-overconstrained", "The first bounded legacy-overview removal regex was overconstrained and matched no text, so it changed no file.", "Use exact start and end function markers, verify one match and its byte length, then remove only that bounded scaffold.", "Prefer verified structural markers over long literal-body regexes for generated text cleanup."),
    negative(12, "workflow-multihunk-patch-context-mismatch", "A combined workflow, reflection, index, and threat-model patch failed because one mojibake-rendered context line did not match; the patch changed no file.", "Apply small ASCII-stable structural patches, then use bounded line-identity rewrites for the encoding-sensitive generated lines.", "Keep generated Unicode-sensitive edits in isolated hunks with independently verifiable context."),
    negative(13, "singleline-regex-greedy-crossline", "The first bulk line-rewrite regex enabled single-line dot matching, so an in-memory decision-line match consumed later lines and the wrapper stopped before writing.", "Discard the in-memory result and use newline-excluding or literal line-array selectors.", "Never combine greedy dot matching with line anchors for multi-line source rewrites."),
    negative(14, "multiline-regex-line-selector-no-match", "The revised .NET line regex still returned zero matches for a visibly present decision line and stopped before writing.", "Read exact lines into an array, require one contains match per stable identifier, replace that index, and write once.", "Prefer exact identifier-indexed line rewrites when cross-runtime regex semantics are uncertain."),
    negative(15, "build-range-select-invalid-regex", "A diagnostic Select-String pattern left an opening parenthesis unescaped, raised an invalid-regex error, and caused an oversized fallback display.", "Use SimpleMatch or an escaped function signature and project only the requested line window.", "Treat source-range selectors as bounded evidence tools and validate regex syntax before use."),
    negative(16, "unicode-stale-scan-powershell-quote-termination", "The first Unicode stale-label scan used a double-quoted PowerShell pattern that failed parsing before ripgrep ran.", "Use one literal single-quoted pattern and rerun the exact four-file scan.", "Prefer literal quoting for non-ASCII ripgrep alternations in PowerShell."),
    negative(17, "proposal-27-novelty-threshold-failure", "The first x1 builder stopped before artifact generation because proposal V6588-P27 had 0.6667 token-set Jaccard similarity to V6587-P27, above the strict 0.60 rail.", "Rewrite only proposal 27 as a purpose-bound field-level disclosure card with withholding reasons, correction, contest, and sunset semantics, then rerun the preregistered audit.", "Treat every proposal as mechanism-level distinct, including recurring Freed ID representation surfaces."),
    negative(18, "stale-scan-pattern-split-as-paths", "The first active-path stale-label ripgrep invocation serialized a spaced alternation incorrectly, so terminal and successor fragments were treated as file paths.", "Pass patterns and paths through an explicit native-argument array and separate inherited provenance from active authored files.", "Never rely on implicit Windows native serialization for a spaced compound regex."),
    negative(19, "stale-scan-regex-native-serialization-loss", "The next stale-label attempt lost embedded quote and bracket characters while serializing one compound regex, producing an unclosed-character-class error.", "Use separate simple -e patterns and an exact file list instead of one complex Windows-native regex argument.", "Prefer several literal patterns to a quoting-sensitive compound regex on Windows."),
    negative(20, "stale-scan-glob-path-domain-mismatch", "The first separate-pattern scan used provenance exclusions that did not match phase-prefixed Windows paths, so immutable inherited proposal metadata produced a context-truncated stream.", "Construct the exact active file list first, exclude the two inherited provenance files by normalized path, then run the simple-pattern scan over that list.", "Bind stale-label exclusions to the actual rendered path domain before scanning large inherited metadata."),
    negative(21, "combined-staged-untracked-probe-yielded", "The combined staged-set wrapper returned its expected, actual, deletion, and unstaged scalars but yielded before serializing the final untracked scalar, so it earned no complete clean-state credit.", "Confirm the wrapper child has exited, then query untracked state only within the exact owner paths and retain a later full postcommit clean proof.", "Keep long repository-wide untracked traversal separate from fast staged-set verification."),
    negative(22, "git-add-stderr-redirection-exit-one", "A warning-suppression git-add wrapper returned exit one with no output, so it earned no staging credit even though some index updates may have occurred.", "Inspect the index, then rerun the same exact owner-path git add without stderr suppression and review the staged set.", "Do not suppress native Git diagnostics during exact staging."),
]


SAFE_TASKS = [
    {
        "task_id": f"V6588-SAFE-{index:03d}",
        "proposal_id": item["proposal_id"],
        "task": f"Materialize the bounded synthetic contract or explicit reservation for {item['slug']}.",
        "approval_class": item["approval_class"],
        "x1_execution": False,
        "planned_lane": "x2" if item["expected_disposition"] in {"completed", "represented"} else item["execution_lane"],
    }
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {
        "task_id": f"V6588-CAND-{index:03d}",
        "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.",
        "approval_class": "candidate_owner_local_review_required",
        "x1_execution": False,
        "planned_lane": "x2_if_bounded_evidence_permits",
    }
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {
        "task_id": f"V6588-CLEAN-{index:03d}",
        "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.",
        "approval_class": "safe_now_additive_cleanup",
        "x1_execution": False,
        "planned_lane": "x2",
    }
    for index, item in enumerate(PROPOSALS, 1)
]
