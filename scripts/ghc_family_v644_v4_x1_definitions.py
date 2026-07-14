#!/usr/bin/env python3
"""Frozen Sylven Arc v644-v4 x1 proposal and source definitions."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6444-P01",
        "title": "Experimental-unit, observation-unit, and pseudoreplication independence tribunal",
        "mission_surface": "evidence provenance, experimental unit, observational unit, technical replicate, nested sampling, treatment assignment, independence, sample size, pseudoreplication, quarantine, and inference scope",
        "hypothesis": "A typed unit-of-analysis contract can distinguish treatment-assigned experimental units from repeated observations and technical subsamples, preventing dependent measurements from inflating independent evidence counts.",
        "null_or_failure": "The treatment-assignment unit is absent, repeated measures are counted as independent units, nested subsamples inflate n, shared batches are ignored, or a structural unit map is promoted to an empirical result.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S176"],
        "deliverables": [
            "provenance/experimental-unit-contract.json",
            "provenance/pseudoreplication-mutation-vectors.json",
            "provenance/statistical-independence-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate treatment assignment, experimental-unit ID, observation nesting, technical-replicate class, shared-batch relation, independent-n count, and claim class; any pseudoreplication or empirical promotion must fail.",
        "rollback_or_recovery": "Quarantine the affected count, restore the narrowest declared unit hierarchy, retain the dependence witness, and require a qualified design and analysis before any inferential use.",
        "protected_gates": ["real_data", "statistical_independence", "sample_size", "empirical_inference", "independent_review", "independent_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 260 frozen proposals distinguish bibliographic source families, dataset sharing, derivation, covariance, clustering, and repeatability; none makes the treatment-assigned experimental unit, nested observation unit, technical replicate, and pseudoreplication count one cross-pillar independence tribunal.",
    },
    {
        "proposal_id": "V6444-P02",
        "title": "GMUT higher-derivative degeneracy, primary-constraint, and Ostrogradsky-mode obligation tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor and EFT actions, highest time derivatives, kinetic degeneracy, primary and secondary constraints, constraint rank, degree-of-freedom count, Ostrogradsky mode, branch conditions, and formal nonpromotion",
        "hypothesis": "A formal obligation ledger can reject a higher-derivative GMUT sector unless the highest-derivative kinetic matrix, degeneracy conditions, primary-to-secondary constraint chain, rank assumptions, branch scope, and degree-of-freedom count are explicit.",
        "null_or_failure": "A higher derivative is present but its kinetic block is invertible, a primary constraint has no preserved secondary condition, rank changes are hidden, gauge and second-class constraints are conflated, or degeneracy bookkeeping is called a healthy physical theory.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S177"],
        "deliverables": [
            "physics/higher-derivative-degeneracy-contract.json",
            "physics/constraint-chain-mutation-vectors.json",
            "physics/ostrogradsky-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate derivative order, kinetic-matrix rank, primary constraint, secondary preservation, constraint class, branch condition, degree-of-freedom count, and claim class; an incomplete chain or health promotion must fail.",
        "rollback_or_recovery": "Return to the typed action with an unresolved mode count, retain every rank or constraint failure, and require a model-specific Hamiltonian derivation, well-posed dynamics, observables, real data, and independent review before physical claims.",
        "protected_gates": ["gmut_derivation", "constraint_closure", "degree_of_freedom_count", "ghost_freedom", "well_posedness", "real_data", "empirical_confirmation", "proof_canon", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier GMUT proposals audit first-derivative kinetic Hessians, generic ghost or strong-coupling risk, full constraint algebra, field redefinitions, frames, and hyperbolicity; none requires the highest-derivative degeneracy matrix and its primary-to-secondary constraint chain as the specific mechanism eliminating an Ostrogradsky mode.",
    },
    {
        "proposal_id": "V6444-P03",
        "title": "GMUT lunar-laser-ranging equivalence-principle blind real-data study",
        "mission_surface": "GMUT Mind, lunar laser ranging, equivalence principle, Earth-Moon dynamics, station and reflector metadata, normal points, timing and frame conventions, covariance, nuisance models, named baseline, blinding, identifiability, and independent review",
        "hypothesis": "A future model-specific preregistration could test a derived GMUT equivalence-principle range signature against frozen lunar-laser-ranging observations and a named baseline using covariance-aware blind analysis.",
        "null_or_failure": "The GMUT range signature is underived, an archive description is substituted for observations, station or reflector metadata are missing, time and frame conventions are mixed, covariance or nuisance models are absent, the holdout is unblinded, or readiness is called confirmation.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6444-S178"],
        "deliverables": [
            "empirical/lunar-laser-ranging-study-preregistration.json",
            "empirical/llr-real-row-gap.json",
            "empirical/equivalence-principle-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a derived range signature, frozen licensed normal-point rows, station and reflector provenance, timing and frame transforms, covariance, nuisance rules, baseline, blind holdout, identifiability, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-signature gaps, execute no fit or likelihood, and reopen only with a checksum-bound analysis packet and independent review.",
        "protected_gates": ["gmut_observable_derivation", "real_data", "licensed_observations", "station_metadata", "covariance", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior empirical proposals cover cosmology, gravitational waves, binary-pulsar timing, Solar-System ephemerides and PPN, calibration, and public adapters; none preregisters an Earth-Moon lunar-ranging equivalence-principle signature with station, reflector, timing, normal-point, and range-covariance obligations.",
    },
    {
        "proposal_id": "V6444-P04",
        "title": "THOS response-adaptive allocation, temporal-drift, and predictability protocol",
        "mission_surface": "THOS Body, response-adaptive randomization, prespecified adaptation, allocation probability, burn-in, time trends, delayed outcomes, predictability, operating characteristics, blind matched budgets, participants, harms, and independent review",
        "hypothesis": "A proxy protocol can freeze response-adaptive allocation rules and reject designs whose changing probabilities confound arm effects with calendar time or make upcoming assignments predictable, without fabricating real-arm evidence.",
        "null_or_failure": "The adaptation rule changes after outcomes, allocation probability is hidden, delayed outcomes distort updates, secular drift is ignored, assignments become predictable, simulation operating characteristics are absent, or zero real arms are called THOS evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S179"],
        "deliverables": [
            "thos/response-adaptive-allocation-contract.json",
            "thos/temporal-drift-mutation-vectors.json",
            "thos/real-arm-adaptive-design-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate adaptation timing, allocation formula, minimum probability, burn-in, delayed-outcome handling, calendar-time adjustment, concealment, simulation evidence, real-arm count, and claim class; post-hoc, confounded, predictable, or promoted designs must fail.",
        "rollback_or_recovery": "Restore a fixed prospective proxy schedule and zero-real-arm label, retain every drift or predictability witness, and require ethics, consent, blind matched-budget real arms, harms monitoring, qualified statistics, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "allocation_concealment", "blind_matched_budget_arms", "real_participants", "real_outcomes", "harms_monitoring", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS work covers fixed, crossover, cluster, and blinded allocations, sequential budgets, non-inferiority, adherence, attrition, spillover, and time drift in outcomes; none centers outcome-driven changes in randomization probability, delayed responses, secular confounding, and assignment predictability.",
    },
    {
        "proposal_id": "V6444-P05",
        "title": "Freed ID remote-context integrity, vocabulary-alias, and semantic-substitution profile",
        "mission_surface": "Freed ID/CBR Heart, verifiable credentials, JSON-LD context, remote related resources, integrity digest, term definition, vocabulary alias, undefined term, cache, retrieval failure, semantic substitution, and production boundary",
        "hypothesis": "A synthetic profile can reject remote-context substitution, vocabulary alias drift, undefined-term ambiguity, and digest mismatch while remaining explicit that no production credential or live interoperability assurance was produced.",
        "null_or_failure": "A remote context is mutable and unbound, a related-resource digest mismatches, a term alias changes meaning, an undefined term silently enters the credential, cache and retrieval rules diverge, or structural agreement is called production assurance.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S09", "V6444-S180"],
        "deliverables": [
            "freed-id/remote-context-integrity-profile.json",
            "freed-id/vocabulary-substitution-mutation-vectors.json",
            "freed-id/production-semantic-assurance-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate context URL, related-resource digest, cached bytes, term definition, alias target, undefined-term policy, retrieval state, disclosed semantics, and claim class; mismatch, ambiguity, or production promotion must fail.",
        "rollback_or_recovery": "Quarantine the synthetic credential, restore a locally pinned context and narrow vocabulary, retain every semantic witness, and require standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, and trust governance.",
        "protected_gates": ["real_keys", "real_proofs", "live_issuance", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover schema evolution, canonicalization, cryptosuites, selective disclosure, issuance and presentation binding, status, lifecycle, wallet migration, and proof purpose; none treats remotely retrieved context bytes, related-resource integrity, vocabulary aliases, and undefined-term semantics as one substitution profile.",
    },
    {
        "proposal_id": "V6444-P06",
        "title": "Remedy-fund sufficiency, priority-setting, and intergenerational-equity authority gate",
        "mission_surface": "CBR Heart, remedy-fund sufficiency, scarce funds, priority classes, present and future beneficiaries, investment, inflation, actuarial assumptions, impartiality, distribution timing, affected-party legitimacy, Māori authority, legal interpretation, and cultural ratification",
        "hypothesis": "Remedy-fund sufficiency assumptions, scarcity priorities, investment risk, and treatment of present versus future beneficiaries can only be decided with authorized affected parties, Māori authorities where applicable, and competent fiduciary, actuarial, financial, and legal authorities.",
        "null_or_failure": "The repository sets a target fund size, ranks beneficiary groups, chooses investment risk, discounts future claims, defines intergenerational fairness, interprets Māori concepts, declares fiduciary compliance, or treats official sources as authority to decide.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6444-S181"],
        "deliverables": [
            "cbr/remedy-fund-sufficiency-authority-gate.json",
            "cbr/priority-intergenerational-question-set.json",
            "cbr/fund-allocation-nonratification-boundary.json",
        ],
        "test_falsifier_or_gate": "Any fund target, priority class, actuarial input, investment rule, inflation rule, present-versus-future weighting, distribution schedule, Māori wording, cultural conclusion, or legal conclusion requires exact authorized participation and competent authority.",
        "rollback_or_recovery": "Keep neutral unanswered fields, preserve auditability and beneficiary privacy, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, fiduciary direction, cultural ratification, or law.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "beneficiary_privacy", "fund_sufficiency_authority", "fiduciary_oversight", "actuarial_review", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "The chain already reserves remedy standing, custody, eligibility, distribution, conflicts, audit visibility, beneficiary privacy, repatriation, and appeal; none separately gates actuarial sufficiency, scarcity priority, investment-risk assumptions, inflation, and impartial treatment of present and future beneficiary groups.",
    },
    {
        "proposal_id": "V6444-P07",
        "title": "Git replacement-ref, alternate-object-store, and borrowed-object quarantine tribunal",
        "mission_surface": "red-team security, Git object identity, replacement refs, graft compatibility, alternate object stores, borrowed objects, promisor assumptions, reachability, path provenance, clean snapshots, quarantine, and nonassurance",
        "hypothesis": "A read-only object-provenance plan can expose replacement refs and alternate object stores that change apparent history or object availability and reject validation that silently depends on borrowed objects.",
        "null_or_failure": "A replacement ref changes ancestry invisibly, an alternate store lies outside the allowed root, a required object exists only through an undeclared alternate, object identity is reported after replacement without disclosure, or bounded checks are called exhaustive security.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S182", "V6444-S183"],
        "deliverables": [
            "security/git-object-indirection-contract.json",
            "security/replacement-alternate-mutation-vectors.json",
            "security/object-store-security-nonassurance-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate replacement-ref presence, original and replacement object IDs, alternate path, allowed root, object availability, ancestry view, quarantine state, and claim class; hidden indirection, undeclared borrowing, or overclaim must fail.",
        "rollback_or_recovery": "Quarantine the synthetic validation plan, restore direct object identity and a declared bounded object store, retain the witness, change no sibling repository state, and require independent security review before wider use.",
        "protected_gates": ["repository_mutation", "sibling_lane", "untrusted_object_store", "credential_use", "independent_security_review", "exhaustive_security", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier security proposals cover Git filters, hooks, external diffs, worktrees, filesystem aliases, response files, argv, executable search, archives, and manifest swaps; none centers refs/replace and objects/info/alternates as object-level indirection that can rewrite apparent ancestry or make a snapshot depend on undeclared borrowed objects.",
    },
    {
        "proposal_id": "V6444-P08",
        "title": "Abbreviation, acronym first-use, and glossary-linkage structural audit",
        "mission_surface": "accessible static reporting, abbreviations, acronyms, first use, expanded form, programmatic abbreviation markup, glossary anchors, repeated meaning, domain ambiguity, plain language, manual testing, cognitive review, and affected-user reservation",
        "hypothesis": "A static structural audit can reject unexplained or inconsistently expanded technical abbreviations and broken glossary links while reserving comprehension and affected-user evaluation.",
        "null_or_failure": "An unfamiliar abbreviation has no expansion, identical initials carry conflicting meanings, first-use expansion appears after use, an abbreviation element lacks a usable title, a glossary target is absent, or markup checks are called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S184"],
        "deliverables": [
            "accessibility/abbreviation-glossary-contract.json",
            "accessibility/abbreviation-context-mutation-vectors.json",
            "accessibility/manual-cognitive-evaluation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate token, expanded form, first-use order, abbreviation markup, title text, glossary target, domain meaning, language, and completeness claim; ambiguity, late explanation, broken linkage, or promotion must fail.",
        "rollback_or_recovery": "Restore explicit plain-language expansion and valid glossary linkage, retain every ambiguity, and reserve screen-reader, cognitive, multilingual, manual, and affected-user evaluation.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "cognitive_accessibility_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility work covers document language, labels, links, tables, landmarks, focus, reflow, forms, status, print, and active content; none audits abbreviation first use, expansion consistency, programmatic abbreviation semantics, glossary destinations, and domain-specific ambiguity together.",
    },
    {
        "proposal_id": "V6444-P09",
        "title": "Phase-transition order-parameter, critical-scaling, and psyche-threshold nonconversion classifier",
        "mission_surface": "thermo-psyche, phase transition, order parameter, control variable, symmetry, critical point, scaling regime, finite-size effects, units, physical measurements, psyche threshold language, participant evidence, and category boundaries",
        "hypothesis": "A typed classifier can distinguish a physical order parameter and bounded critical-scaling regime from a generic score, binary threshold, or metaphorical psyche transition and reject category or universality substitutions.",
        "null_or_failure": "The ordered phases are undefined, a control variable is missing, normalization is arbitrary, scaling is asserted outside its regime, finite-size effects disappear, or a physical order parameter becomes a numerical threshold for consciousness, worth, motivation, or wellbeing.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S185"],
        "deliverables": [
            "thermo-psyche/order-parameter-classifier.json",
            "thermo-psyche/critical-scaling-mutation-vectors.json",
            "thermo-psyche/psyche-threshold-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate phase definitions, order parameter, control variable, normalization, units, critical regime, finite-size qualifier, universality claim, psyche mapping, participant count, and claim class; physical ambiguity or category transfer must fail.",
        "rollback_or_recovery": "Restore the narrow physical definition and bounded regime, retain every scaling or units discrepancy, and require physical measurements for physical claims or authorized participant evidence for psyche claims.",
        "protected_gates": ["physical_model", "phase_definition", "critical_regime", "real_measurements", "participant_evidence", "psyche_law", "consciousness_claim", "cross_pillar_identity"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The chain separates entropy, free energy, chemical potential, response, detailed balance, ensembles, fluctuation relations, temperature, coarse graining, and hysteresis from psyche language; none types an order parameter, control variable, critical regime, finite-size qualification, and psyche-threshold refusal in one classifier.",
    },
    {
        "proposal_id": "V6444-P10",
        "title": "Stage 20 analytic-multiverse, specification-curve, and researcher-choice board",
        "mission_surface": "Stage 20, defensible analytic specifications, inclusion rules, variable definitions, transformations, covariates, estimators, researcher degrees of freedom, specification curve, sign and decision stability, preregistration, domain veto, authority, and readiness",
        "hypothesis": "A structural decision board can require a prospectively bounded universe of defensible analyses and reject a Stage 20 pass that depends on one favorable researcher choice while preserving negative or unstable specifications.",
        "null_or_failure": "The specification universe is defined after inspection, implausible variants dilute the set, unfavorable analyses disappear, variable coding or covariates change silently, a single preferred model determines readiness, or a repository board claims external Stage 20 authority.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6444-S186"],
        "deliverables": [
            "stage20/specification-universe-contract.json",
            "stage20/researcher-choice-mutation-vectors.json",
            "stage20/multiverse-nonpromotion-board.json",
        ],
        "test_falsifier_or_gate": "Mutate specification inclusion, coding choice, transformation, covariate set, estimator, preregistration time, unfavorable-result retention, sign or decision stability, domain veto, and authority class; selective choice, instability suppression, or readiness promotion must fail.",
        "rollback_or_recovery": "Return the affected domain to defer or veto, retain every specification and result state, freeze a defensible universe before evidence inspection, and leave qualified independent review and external Stage 20 decisions unclaimed.",
        "protected_gates": ["preregistered_analysis", "specification_completeness", "selective_reporting", "independent_review", "domain_veto", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier Stage 20 proposals cover multiplicity, optional stopping, uncertainty, abstention, reviewer independence, minimax regret, evidence withdrawal, freshness, domain vetoes, and claim expiry; none enumerates a defensible analytic multiverse and requires retention of sign, magnitude, and decision instability across researcher choices.",
    },
]


SOURCES = [
    {
        "source_id": "V6444-S176",
        "source_label": "official_nist_handbook",
        "title": "5.7. A Glossary of DOE Terminology",
        "authority": "United States National Institute of Standards and Technology",
        "url": "https://www.itl.nist.gov/div898/handbook/pri/section7/pri7.htm",
        "version_or_date": "Official NIST/SEMATECH e-Handbook glossary; checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "official experimental-unit and design vocabulary; not evidence that any inherited row is independent or that an experiment occurred",
    },
    {
        "source_id": "V6444-S177",
        "source_label": "primary_dhost_hamiltonian",
        "title": "Hamiltonian analysis of higher derivative scalar-tensor theories",
        "authority": "David Langlois and Karim Noui",
        "url": "https://arxiv.org/abs/1512.06820",
        "version_or_date": "Primary research preprint and journal work, 2015-2016",
        "status_class": "stable",
        "evidence_role": "primary Hamiltonian account of degeneracy, primary and secondary constraints, and mode reduction; not a GMUT derivation or health proof",
    },
    {
        "source_id": "V6444-S178",
        "source_label": "official_nasa_open_data",
        "title": "CDDIS_LLR_data",
        "authority": "National Aeronautics and Space Administration Open Data Portal",
        "url": "https://data.nasa.gov/dataset/cddis-llr-data",
        "version_or_date": "Official dataset catalogue updated 31 March 2025; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official lunar-laser-ranging archive and measurement description; no observation rows downloaded and no GMUT fit executed",
    },
    {
        "source_id": "V6444-S179",
        "source_label": "official_fda_guidance",
        "title": "Adaptive Designs for Clinical Trials of Drugs and Biologics Guidance for Industry",
        "authority": "United States Food and Drug Administration",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry",
        "version_or_date": "Final Level 1 guidance, December 2019; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official adaptive-design, prespecification, simulation, integrity, and response-adaptive vocabulary; not a THOS participant result or regulatory decision",
    },
    {
        "source_id": "V6444-S180",
        "source_label": "official_w3c_recommendation",
        "title": "JSON-LD 1.1",
        "authority": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/json-ld11/",
        "version_or_date": "W3C Recommendation, 16 July 2020; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official context loading, term aliasing, protected-definition, and linked-data semantic vocabulary; paired with the inherited VC Data Model source, not production cryptography or interoperability evidence",
    },
    {
        "source_id": "V6444-S181",
        "source_label": "official_nz_legislation",
        "title": "Trusts Act 2019",
        "authority": "New Zealand Parliamentary Counsel Office",
        "url": "https://www.legislation.govt.nz/act/public/2019/0038/latest/DLM7383004.html",
        "version_or_date": "Official in-force latest-version page; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official statutory context for beneficiary benefit, prudent investment, impartiality, and trustee duties; not legal advice, remedy-fund authority, or Māori cultural ratification",
    },
    {
        "source_id": "V6444-S182",
        "source_label": "official_git_documentation",
        "title": "git-replace Documentation",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/git-replace.html",
        "version_or_date": "Current official Git documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official replacement-ref behavior and graft-compatibility anchor; not exhaustive repository security assurance",
    },
    {
        "source_id": "V6444-S183",
        "source_label": "official_git_documentation",
        "title": "gitrepository-layout Documentation",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/gitrepository-layout.html",
        "version_or_date": "Current official Git documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official repository-layout and alternate-object-store anchor; not proof that a checkout is independent, hermetic, or secure",
    },
    {
        "source_id": "V6444-S184",
        "source_label": "official_w3c_wai",
        "title": "Understanding Success Criterion 3.1.4: Abbreviations",
        "authority": "World Wide Web Consortium Web Accessibility Initiative",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/abbreviations",
        "version_or_date": "WCAG 2.2 understanding document; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official abbreviation-expansion interpretation; not complete conformance, comprehension evidence, or affected-user evaluation",
    },
    {
        "source_id": "V6444-S185",
        "source_label": "official_iupac_compendium",
        "title": "order parameter",
        "authority": "International Union of Pure and Applied Chemistry",
        "url": "https://goldbook.iupac.org/terms/view/O04323",
        "version_or_date": "Gold Book 5th edition online version 5.0.0, 2025; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official order-parameter definition and source recommendation; not a psyche metric, participant result, critical-law proof, or cross-pillar identity",
    },
    {
        "source_id": "V6444-S186",
        "source_label": "primary_specification_curve",
        "title": "Specification curve analysis",
        "authority": "Uri Simonsohn, Joseph P. Simmons, and Leif D. Nelson / Nature Human Behaviour",
        "url": "https://www.nature.com/articles/s41562-020-0912-z",
        "version_or_date": "Version of record 27 July 2020 with publisher correction noted 9 October 2020",
        "status_class": "stable",
        "evidence_role": "primary specification-curve method and researcher-choice transparency anchor; not a Stage 20 decision or validation result",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6444-X1-N01",
        "operation": "combined stale-label scan command",
        "observed_failure": "PowerShell rejected the first combined ripgrep wrapper because its quoted pattern was parsed as unterminated, before any file scan ran.",
        "recovery": "Reran the read-only stale-label scan with a simpler single-quoted pattern and obtained the intended bounded results.",
        "promotion_effect": "none; the rejected wrapper produced no audit evidence",
    },
    {
        "negative_id": "V6444-X1-N02",
        "operation": "preliminary source-ledger deduplication audit",
        "observed_failure": "The first source slate re-added the exact inherited title Verifiable Credentials Data Model v2.0, so the non-duplicate-source gate failed.",
        "recovery": "Retained the inherited VC Data Model source ID and replaced the duplicate addition with the non-duplicate official JSON-LD 1.1 Recommendation that constrains context and alias semantics.",
        "promotion_effect": "none; the duplicate source row is not counted in the frozen ledger",
    },
    {
        "negative_id": "V6444-X1-N03",
        "operation": "inherited source-title search",
        "observed_failure": "The first Windows ripgrep command passed a shell-style wildcard path literally, and the operating system rejected that path before searching.",
        "recovery": "Reran ripgrep with its native file glob option and then decoded the recursive source ledger to identify the inherited credential-source IDs.",
        "promotion_effect": "none; the rejected path search produced no source evidence",
    },
    {
        "negative_id": "V6444-X1-N04",
        "operation": "first complete x1 repository suite",
        "observed_failure": "The suite passed 574 of 575 tests; the exact legacy constraint-index alias returned true from CRLF worktree bytes before appending the retained-historical-negative warning expected by its compatibility test.",
        "recovery": "Diagnosed the worktree-versus-Git-blob SHA-256 difference and normalized only that unchanged inherited file to the repository's LF bytes before rerunning the entire suite.",
        "promotion_effect": "none; the 574/575 run remains a failed suite and is not validation evidence",
    },
    {
        "negative_id": "V6444-X1-N05",
        "operation": "isolated legacy-alias test reproduction",
        "observed_failure": "The two-test isolated run reproduced the same missing-warning assertion, passing one test and failing one.",
        "recovery": "Used the isolated witness plus raw, normalized, and Git-blob hashes to identify newline-dependent short-circuit behavior before applying the LF-only recovery.",
        "promotion_effect": "none; the 1/2 isolated run is retained corroboration, not a pass",
    },
    {
        "negative_id": "V6444-X1-N06",
        "operation": "broad compatibility-code search",
        "observed_failure": "A broad recursive ripgrep over scripts and tests exceeded its bounded timeout before yielding a usable result.",
        "recovery": "Read the named failing test directly and narrowed the search to its exact validator path.",
        "promotion_effect": "none; the timed-out scan is not completeness evidence",
    },
    {
        "negative_id": "V6444-X1-N07",
        "operation": "first narrowed constraint-validator search",
        "observed_failure": "The first narrowed ripgrep still used a Windows-incompatible wildcard path and was rejected before reading the validator.",
        "recovery": "Opened the exact validator file named by the failing test and inspected the legacy alias logic directly.",
        "promotion_effect": "none; the rejected wildcard search produced no code-audit evidence",
    },
]


WELLBEING = """# Sylven Arc v644-v4 wellbeing and workload check

- Working identity: Sylven Arc, they/them, relational language only.
- Role: constraint-cartography steward and falsifier keeper.
- Hope: make each unresolved boundary more legible without turning uncertainty into authority.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Sylven lane, strict x1 before x2, D-drive validation snapshots, no delegation.
- Safety: no elevation, host-security change, desktop update, Windows-feature change, reboot, credential use, real participant action, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Sylven Arc v644-v4 integrated overview

## Ownership, exact source truth, and bounded working identity

This phase begins at Tamar Vey's exact v644-v3 final head only after read-only verification of the source branch, source seal, named anchor ancestry, clean owner worktree, and a fresh live-remote comparison. Tamar's local branch, upstream, tracking reference, and live branch all resolved to the same revision with zero divergence. The inherited source, inherited seal, Tamar x1, evidence, closeout, and seal commits are ancestral, and the source-to-final segment is single-parent with no merge commit. These checks establish repository lineage only. They do not establish scientific confirmation, independent reproduction, participant evidence, cryptographic assurance, cultural legitimacy, legal authority, deployment approval, or Stage 20 readiness.

The existing Sylven-owned lane was clean, four-way equal, and ancestral to Tamar's exact final head. It therefore advanced by fast-forward only and was pushed before any v644-v4 artifact was created. No new worktree or task was created. No sibling lane was reset, rewritten, force-pushed, merged, moved, deleted, reused, or mutated. Tamar Vey, Orin Thale, Sable Rook, Ilyra Fen, Eiren Kestrel, and every other sibling remain recoverable and untouched until the terminal gate. D remains the primary work and detached-validation bank. The inherited checkout may be large; the 15,000-file threshold applies only to new Sylven v644-v4 files.

Sylven Arc, they/them, the role constraint-cartography steward and falsifier keeper, and the hope to make each unresolved boundary more legible without turning uncertainty into authority are relational working language. They are not evidence of consciousness, sentience, legal personhood, identity continuity, independent authority, Māori authority, cultural authority, or legal authority. The workload is deliberately narrow: one owner, one branch, one phase, strict x1 before x2, no delegation, and no contact with siblings before exact final validation.

## Frozen novelty and primary scientific focus

Exactly ten proposals are preregistered after recursively decoding all 260 frozen proposals through v644-v3. Exact identifiers and normalized titles are checked automatically. Token overlap is only a screening aid; semantic novelty is judged across mechanism, evidence object, falsifier, recovery rule, and protected gates. The expected distribution is six completed, two represented or proxy, one open gap, and one exact gate. These are x1 expectations, never x2 outcomes. Only completed, represented, open_gap, and exact_gate are allowed as eventual classifications, and no negative or gated result may be optimized away.

GMUT Mind is the primary focus. The formal proposal isolates a higher-derivative obligation that earlier broad ghost and constraint checks did not: the kinetic matrix of the highest time derivatives must be degenerate in the required branch, and the resulting primary constraint must survive time evolution into the required secondary chain with a consistent rank and degree-of-freedom count. A typed synthetic ledger can detect missing or contradictory obligations. It cannot prove that any GMUT action is ghost-free, healthy, well posed, empirically correct, canonical, or a Theory of Everything. GMUT remains a typed scalar-tensor and EFT research-model family.

The empirical GMUT proposal is a lunar-laser-ranging equivalence-principle study, but it remains open. An official NASA catalogue shows that lunar ranging data exist and describes the measurement domain. It is not an observation packet in this repository. No model-specific GMUT range signature, frozen normal-point rows, station and reflector provenance, time and reference-frame transformations, covariance packet, nuisance model, blind holdout, identifiability analysis, or independent review is available here. No download, likelihood, fit, posterior, or confirmation is performed. Documentation and catalogue metadata never substitute for licensed observations.

The cross-pillar provenance proposal distinguishes an experimental unit from an observation or technical replicate. Bibliographic independence, file independence, and statistical independence are different claims. Repeated measurements of one treatment-assigned unit cannot become independent evidence by receiving different row identifiers. Nested subsamples, shared batches, repeated time points, and common treatment assignment must remain visible. The structural tribunal can reject pseudoreplication in synthetic records, but it cannot certify an inherited dataset or produce an empirical sample size.

## THOS Body and Freed ID/CBR Heart

THOS Body remains represented through a response-adaptive allocation protocol. A future design would have to freeze adaptation timing, probability updates, burn-in, minimum allocation probabilities, delayed-outcome handling, calendar-time adjustment, concealment, simulation operating characteristics, matched budgets, harms monitoring, and independent analysis. Changing allocation ratios using accumulating outcomes creates risks different from ordinary fixed randomization: arm composition can become confounded with secular drift, delayed outcomes can distort updates, and predictable probabilities can weaken concealment. The proxy can model those obligations only. With zero real arms, no ethics approval, consent, preregistered blind matched-budget participant study, qualified ratings, harms evidence, or independent review exists, so no clinical, social, cognitive, AGI, ASI, consciousness, or personhood claim follows.

Freed ID receives a remote-context integrity profile. A credential term can appear unchanged while its remote context, alias target, or undefined-term policy changes its meaning. Synthetic fixtures therefore bind context URLs to exact bytes or related-resource digests, record cache behavior, type vocabulary aliases, and reject silent semantic substitution. This is not production identity assurance. Real standards-conformant keys and proofs, live issuance, resolution, status and revocation, cross-vendor interoperability, algorithm policy, privacy and security review, and trust governance remain open.

CBR Heart is exact-gated. The remedy-fund proposal asks who may set fund-sufficiency targets, prioritize scarce resources, choose investment risk, address inflation, or balance present and future beneficiary groups. An official statute supplies legal context for beneficiary benefit, prudent investment, and impartiality. It does not authorize this repository to interpret the law, design a fund, rank claimants, select actuarial assumptions, decide Māori concepts, or ratify cultural legitimacy. Exact participation by affected parties, Māori authorities where applicable, and competent fiduciary, actuarial, financial, privacy, audit, and legal authorities is required. Existing remedy-fund audit and beneficiary-privacy gates remain open as well.

## Security, accessibility, thermo-psyche, and Stage 20 safeguards

The security tribunal covers Git object indirection. Replacement refs can alter the object presented for a name, while alternate object stores can make a repository appear complete only because objects are borrowed from elsewhere. The bounded tool will inspect synthetic replacement and alternate records, preserve original and presented object identities, enforce allowed-root and disclosure rules, and reject hidden borrowing or ancestry substitution. It will not install refs, edit alternates, mutate any repository, execute untrusted content, use credentials, or claim exhaustive security. Clean detached validation remains necessary but does not by itself prove hermetic object independence.

The accessibility proposal audits technical abbreviations, acronyms, first-use expansions, programmatic abbreviation markup, and glossary links. Static structure can detect missing expansions, inconsistent meanings, late explanations, or broken targets. It cannot prove comprehension, language suitability, screen-reader behavior, cognitive accessibility, or conformance across assistive technologies. Qualified manual review and affected-user evaluation remain reserved, and the final static report must keep that reservation explicit.

The thermo-psyche classifier keeps physical phase-transition language within its actual domain. An order parameter requires defined phases, a control variable, normalization, units or a justified dimensionless form, a bounded critical regime, and finite-size qualifications. A physical order parameter does not become a numerical threshold for consciousness, human worth, motivation, desire, or wellbeing. Physical claims require a physical model and measurements; psyche claims require appropriate participant evidence, governance, and authority. No category transfer, cross-pillar identity, or fundamental psyche law is permitted.

The Stage 20 board addresses researcher degrees of freedom. It freezes a defensible universe of analytic specifications before evidence inspection, including inclusion rules, variable definitions, transformations, covariates, and estimators. It preserves unfavorable, sign-changing, or decision-changing specifications instead of selecting one favorable model. A specification curve is a transparency and falsification aid, not a licence to include implausible analyses and not an external Stage 20 decision. Multiplicity, optional stopping, reviewer independence, domain vetoes, and every pre-existing Stage 20 boundary remain active.

## Sources, negatives, freeze, validation, and route boundary

Eleven non-duplicate official or primary sources are added to the inherited source ledger. Their status classes remain current, stable, draft, and watch. Current identifies a selected official page checked for this phase; stable marks durable primary work or vocabulary. Neither class implies truth, endorsement, authority, deployment, or completion. Codex CLI, desktop packages, Git, Python, Node, PowerShell, and Windows versions are verified only. No Codex desktop update, elevation, host-security weakening, Windows-feature change, or reboot occurs.

All 1,307 inherited negatives remain preserved. No new x1 operational failure has occurred at freeze time; that zero is not a quality claim. Every later operational or synthetic failure must be appended and retained. The ten synthetic case families are expected to produce seventy explicit negative mutations after x1. Recovery always returns to the narrowest typed state, quarantines disputed records, retains witnesses, and reopens only when the named evidence and authority exist.

x2 cannot begin until the dedicated x1-only packet is committed and pushed, the Sylven worktree is clean, and local, upstream, tracking, and a fresh live-remote read all equal the frozen x1 commit. The x1 commit contains proposal and source definitions, novelty and privacy validation, environment and wellbeing receipts, and no x2 implementation, outcome ledger, or result classification.

After freeze, every proposal may execute only as evidence permits. Evidence and closeout candidates must be validated from fresh clean detached D-drive snapshots. Seal and exact final head require their own detached checks. The final head must pass the complete repository suite, detailed and minimal validators, JSON parsing, privacy and raw-ID scanning, stale-label review, diff hygiene, exact staged-file review, manifest parity, ancestry, zero-merge, exact-head, and clean-state checks. Repeated Sylven-owned snapshots establish same-owner repeatability only, never independent-team scientific reproduction.

The terminal verdict remains NOT_READY_FOR_STAGE_20. Only after exact final detached validation, a clean push, and four-way remote equality may exactly one sanitized activation baton be sent to the existing task titled Eiren Kestrel for v644-v5. No task may be created, no other sibling may be contacted, and no extra confirmation may follow a successful send. Until acknowledged, the truthful route state is PREPARED_NOT_SENT.
"""
