#!/usr/bin/env python3
"""Frozen Eiren Kestrel v644-v5 x1 proposal and source definitions."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6445-P01",
        "title": "Method Flow State failure-signature, workaround-precondition, and recurrence-prevention ledger",
        "mission_surface": "THOS Body, method memory, failure signatures, triggering preconditions, bounded workaround, validation evidence, recurrence prevention, supersession, deprecation, and sibling-safe recommendations",
        "hypothesis": "A family-current method ledger can convert retained operational negatives into typed, testable recovery knowledge without erasing the original failure or treating an unvalidated workaround as a rule.",
        "null_or_failure": "A failure is recorded without its trigger, a workaround is recommended without a validation witness, a stale method stays preferred after supersession, a negative is deleted after recovery, or a private route or machine-local detail enters a public artifact.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S22", "V6445-S191", "V6445-S204"],
        "deliverables": [
            "method-flow/method-flow-state.json",
            "method-flow/workaround-validation-ledger.json",
            "method-flow/recurrence-prevention-recommendations.md",
            "tooling/ghc-family-method-flow-state-skill-receipt.json",
        ],
        "test_falsifier_or_gate": "Mutate the failure signature, trigger, approval class, workaround precondition, validation witness, recurrence guard, supersession relation, privacy class, and recommendation status; incomplete, unvalidated, stale, or privacy-unsafe methods must fail.",
        "rollback_or_recovery": "Restore the last validated method as preferred, quarantine the candidate method, retain both failure and failed-workaround evidence, and require a fresh bounded validation before reuse.",
        "protected_gates": ["credential_use", "private_routes", "destructive_action", "host_security_change", "sibling_lane", "independent_review", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 270 frozen proposals retain negatives and validate tools, but none makes failure signature, trigger precondition, workaround evidence, recurrence guard, supersession, and sibling recommendation one reusable family-current method state machine.",
    },
    {
        "proposal_id": "V6445-P02",
        "title": "GMUT disformal-map invertibility, causal-cone, and matter-metric obligation tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor and EFT research models, conformal-disformal maps, Jacobian rank, inverse map, causal cones, matter metric, frame dictionary, singular branches, observables, and formal nonpromotion",
        "hypothesis": "A typed formal tribunal can reject a proposed frame map unless its invertibility domain, singular branches, causal-cone effects, matter coupling metric, and observable dictionary are explicit.",
        "null_or_failure": "The transformation Jacobian loses rank, a singular branch is hidden, the inverse map is unspecified, matter couples to an undeclared metric, causal cones change without accounting, or formal equivalence is called empirical equivalence.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6445-S200", "V6445-S201"],
        "deliverables": [
            "physics/disformal-map-obligation-contract.json",
            "physics/causal-cone-mutation-vectors.json",
            "physics/frame-equivalence-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate conformal and disformal factors, scalar-gradient norm, Jacobian rank, inverse branch, matter metric, cone relation, observable map, and claim class; any singular, ambiguous, or promoted row must fail.",
        "rollback_or_recovery": "Return to the original typed action and unresolved observable dictionary, retain every singularity witness, and require model-specific derivation, well-posed dynamics, real data, and independent review.",
        "protected_gates": ["gmut_derivation", "invertibility", "causal_structure", "matter_coupling", "well_posedness", "real_data", "empirical_confirmation", "proof_canon", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work includes Jordan-Einstein dictionaries and generic field redefinitions; none isolates derivative-dependent disformal invertibility, singular branches, causal-cone changes, and the matter metric in one tribunal.",
    },
    {
        "proposal_id": "V6445-P03",
        "title": "GMUT strong-lensing time-delay blind real-data study",
        "mission_surface": "GMUT Mind, strong gravitational lensing, time-delay cosmography, image delays, lens mass model, line-of-sight environment, stellar kinematics, covariance, named baseline, blind analysis, identifiability, and independent review",
        "hypothesis": "A future model-specific preregistration could test a derived GMUT lensing-delay signature against frozen public observations and a named baseline using covariance-aware blinded inference.",
        "null_or_failure": "The GMUT observable is underived, catalogue metadata replace observations, lens-model or line-of-sight uncertainty is absent, covariance is missing, the holdout is unblinded, or a readiness packet is called empirical support.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6445-S198", "V6445-S199"],
        "deliverables": [
            "empirical/strong-lensing-time-delay-study-preregistration.json",
            "empirical/strong-lensing-real-row-gap.json",
            "empirical/gmut-lensing-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a derived observable, checksum-bound licensed rows, delay and imaging provenance, lens and environment models, covariance, nuisance rules, baseline, blind holdout, identifiability, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-observable gaps, run no likelihood or fit, and reopen only with a frozen analysis packet and independent review.",
        "protected_gates": ["gmut_observable_derivation", "real_data", "licensed_observations", "covariance", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior empirical proposals cover cosmology, gravitational waves, pulsars, ephemerides, and lunar ranging; none preregisters strong-lensing image delays with lens mass, line-of-sight, kinematic, covariance, and blinding obligations.",
    },
    {
        "proposal_id": "V6445-P04",
        "title": "THOS cluster-randomized site-participant estimand and informative-cluster-size protocol",
        "mission_surface": "THOS Body, cluster randomization, site and participant estimands, informative cluster size, recruitment timing, contamination, intracluster correlation, matched budgets, harms, consent, and independent review",
        "hypothesis": "A proxy protocol can distinguish site-level from participant-level estimands and reject analyses whose cluster-size mechanism or post-allocation recruitment changes the target effect.",
        "null_or_failure": "The randomization unit is confused with the analysis unit, cluster size depends on outcome risk but is ignored, recruitment follows allocation without protection, contamination is hidden, or synthetic operating characteristics are called participant evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6423-S41"],
        "deliverables": [
            "thos/cluster-estimand-contract.json",
            "thos/informative-cluster-size-mutation-vectors.json",
            "thos/real-arm-cluster-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate randomization unit, estimand population, cluster-size mechanism, recruitment timing, contamination, correlation, weighting, real-arm count, and claim class; ambiguous, biased, or promoted designs must fail.",
        "rollback_or_recovery": "Restore a prospective zero-real-arm proxy, retain every estimand conflict, and require ethics, consent, preregistration, blind matched budgets, real participants, harms monitoring, qualified statistics, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_outcomes", "harms_monitoring", "qualified_statistics", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover cluster allocation and crossover carryover; none centers the divergence between site and participant estimands under informative cluster size and post-allocation recruitment.",
    },
    {
        "proposal_id": "V6445-P05",
        "title": "Freed ID status-list cache-age, epoch-rollback, and revocation-window profile",
        "mission_surface": "Freed ID Heart, verifiable credentials, bitstring status lists, cache age, retrieval time, issuer epoch, rollback, stale-good state, suspension, revocation, privacy, interoperability, and production boundary",
        "hypothesis": "A synthetic profile can reject stale or rolled-back credential-status material and calculate a bounded unresolved exposure window without producing production identity assurance.",
        "null_or_failure": "A verifier accepts an older epoch, cache age exceeds policy, retrieval failure silently means valid, suspension and revocation are conflated, privacy leakage is ignored, or fixtures are called live status evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S12"],
        "deliverables": [
            "freed-id/status-freshness-profile.json",
            "freed-id/epoch-rollback-mutation-vectors.json",
            "freed-id/production-status-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate list purpose, status bit, issuer epoch, observed epoch, issued time, retrieval time, maximum cache age, failure policy, privacy class, and claim class; stale, rolled-back, ambiguous, or promoted rows must fail.",
        "rollback_or_recovery": "Quarantine the synthetic credential, require fresh issuer-authorized status material, retain every rollback witness, and keep real keys, proofs, issuance, resolution, interoperability, privacy and security review, and trust governance open.",
        "protected_gates": ["real_keys", "real_proofs", "live_issuance", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier status proposals address lifecycle and revocation structure; none types cache-age policy, monotonic issuer epochs, rollback detection, and the stale-good exposure window together.",
    },
    {
        "proposal_id": "V6445-P06",
        "title": "Protected-disclosure confidentiality, reprisal remedy, and independent-ombuds authority gate",
        "mission_surface": "CBR Heart, protected disclosures, serious wrongdoing, confidentiality, reprisal, remedy, independent ombuds, natural justice, affected-party participation, Māori authority, legal advice, and enacted law",
        "hypothesis": "Only authorized affected parties and competent authorities may decide disclosure eligibility, confidentiality exceptions, reprisal findings, remedies, ombuds powers, Māori wording, or legal effect.",
        "null_or_failure": "The repository identifies a whistleblower, decides serious wrongdoing, promises confidentiality, finds retaliation, orders a remedy, appoints an ombuds, interprets Māori concepts, gives legal advice, or declares enactment.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6445-S195", "V6445-S196"],
        "deliverables": [
            "cbr/protected-disclosure-authority-gate.json",
            "cbr/reprisal-remedy-question-set.json",
            "cbr/ombuds-nonappointment-boundary.json",
        ],
        "test_falsifier_or_gate": "Any real disclosure intake, identity handling, eligibility decision, confidentiality exception, reprisal finding, remedy, ombuds appointment, Māori wording, cultural conclusion, or legal conclusion requires exact authority and case-specific safeguards.",
        "rollback_or_recovery": "Keep neutral unanswered fields, accept no real case data, preserve confidentiality and cultural gates, and seek authorized professional and affected-party participation outside this technical packet.",
        "protected_gates": ["real_identity_data", "affected_party_acceptance", "maori_authority", "maori_data_governance", "confidentiality_decision", "reprisal_finding", "remedy_authority", "legal_advice", "cultural_ratification", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "The chain reserves grievance, remedy, appeal, and governance authority, but none separately gates protected-disclosure intake, confidentiality exceptions, reprisal findings, and independent-ombuds powers.",
    },
    {
        "proposal_id": "V6445-P07",
        "title": "Lineage-preserving partial-clone, sparse-cone, and dependency-closure migration tribunal",
        "mission_surface": "THOS Body, Git partial clone, sparse checkout, path dependency closure, object backfill, canonical ancestry, lean companion workspace, 15000-file threshold, reproducibility, rollback, and remote migration",
        "hypothesis": "A read-only dependency-closure tribunal plus an additive lean companion can reduce the active path surface while preserving canonical commit identity and refusing a public-repository cutover until lineage and consumer checks pass.",
        "null_or_failure": "Files are omitted without dependency analysis, partial-clone promises are mistaken for path sparsity, a lean export claims canonical history it lacks, required objects cannot backfill, or a new remote becomes authoritative before successor compatibility.",
        "approval_class": "safe_now_local_additive_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6445-S187", "V6445-S188", "V6445-S189"],
        "deliverables": [
            "repository/lean-dependency-closure.json",
            "repository/lineage-preserving-migration-tribunal.json",
            "repository/lean-companion-validation.json",
        ],
        "test_falsifier_or_gate": "Mutate included roots, importer edges, test fixtures, required Git objects, source head, ancestry claim, file count, remote state, and rollback target; missing closure, false lineage, or premature cutover must fail.",
        "rollback_or_recovery": "Keep the canonical repository authoritative, discard only the additive companion if invalid, retain its failure manifest, and retry with an expanded closure; never rewrite or force-push sibling history.",
        "protected_gates": ["canonical_history_rewrite", "remote_repository_creation", "successor_compatibility", "sibling_lane", "force_push", "dependency_completeness", "independent_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work rotates worktrees and audits Git indirection; none distinguishes partial-clone object promises from sparse path materialization while validating dependency closure and a reversible lean companion.",
    },
    {
        "proposal_id": "V6445-P08",
        "title": "Skip-link, focus-visible, and bypass-block static-report audit",
        "mission_surface": "accessible reporting, repeated blocks, skip link, main landmark, keyboard focus, focus visibility, target existence, source order, hidden content, manual testing, assistive technology, and affected-user evaluation",
        "hypothesis": "A static audit can reject reports lacking a working first-use bypass mechanism, a unique main target, or visible keyboard focus while reserving manual and affected-user conformance.",
        "null_or_failure": "The skip target is missing or duplicated, the link is not keyboard reachable, focus is visually suppressed, repeated navigation cannot be bypassed, source order breaks the target, or static checks are called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S26", "V6445-S194"],
        "deliverables": [
            "accessibility/bypass-block-contract.json",
            "accessibility/skip-link-focus-mutation-vectors.json",
            "accessibility/manual-user-evaluation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate link order, target identifier, target count, keyboard reachability, focus visibility, landmark role, hidden state, and completeness claim; broken bypass or promotion must fail.",
        "rollback_or_recovery": "Restore a visible keyboard-operable skip link and unique main landmark, retain every static failure, and reserve assistive-technology, manual, cognitive, multilingual, and affected-user evaluation.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "cognitive_accessibility_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior accessibility proposals cover reflow, contrast, focus sequence, tables, abbreviations, and glossary linkage; none makes bypass-block operation, main-target uniqueness, and visible focus one mutation-tested contract.",
    },
    {
        "proposal_id": "V6445-P09",
        "title": "Housekeeping-entropy-production and psyche-effort nonconversion classifier",
        "mission_surface": "thermo-psyche, nonequilibrium steady states, housekeeping entropy production, excess contribution, current and affinity, coarse graining, units, metaphor boundary, participant evidence, and nonconversion",
        "hypothesis": "A typed classifier can distinguish housekeeping and excess entropy-production bookkeeping in synthetic physical models while refusing to equate either with psychological effort, moral worth, or consciousness.",
        "null_or_failure": "Units are absent, currents and affinities are mismatched, steady-state assumptions are hidden, coarse-graining dependence is ignored, a negative production rate passes, or physical entropy is converted into a psyche measure.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6445-S202", "V6445-S203"],
        "deliverables": [
            "thermo-psyche/housekeeping-entropy-classifier.json",
            "thermo-psyche/current-affinity-mutation-vectors.json",
            "thermo-psyche/psyche-effort-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate units, current, affinity, sign convention, steady-state reference, coarse-graining scope, psyche label, and claim class; inconsistent, negative, or converted rows must fail.",
        "rollback_or_recovery": "Restore domain-specific quantities and units, retain every contradiction, and require independently validated participant constructs before any psychological interpretation.",
        "protected_gates": ["validated_psychometric_construct", "participant_consent", "real_participant_data", "cross_domain_conversion", "consciousness_claim", "independent_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier thermo-psyche work covers detailed balance, fluctuation relations, Onsager response, order parameters, and critical scaling; none isolates housekeeping versus excess entropy production and explicitly blocks conversion to psyche effort.",
    },
    {
        "proposal_id": "V6445-P10",
        "title": "Stage 20 validation-budget, diminishing-return, and assurance-allocation board",
        "mission_surface": "Stage 20, risk-based assurance, validation budget, marginal defect yield, evidence diversity, full repository suite, one replay, domain veto, authority evidence, diminishing returns, and nonreadiness",
        "hypothesis": "A transparent board can allocate bounded validation effort by risk and marginal information while forbidding fewer repeated checks from compensating for missing empirical, participant, legal, cultural, security, or independent evidence.",
        "null_or_failure": "Test count is reduced without a risk argument, repeated identical checks are called independent evidence, missing authority is traded for software passes, a failed check disappears, domain vetoes are averaged away, or budget savings become Stage 20 readiness.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S22", "V6445-S191", "V6445-S204"],
        "deliverables": [
            "stage20/validation-budget-board.json",
            "stage20/marginal-information-ledger.json",
            "stage20/assurance-allocation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate risk class, check diversity, marginal yield, replay owner, unresolved gate, failure retention, domain veto, and readiness claim; hidden failures, false independence, authority substitution, or promotion must fail.",
        "rollback_or_recovery": "Restore the higher-assurance plan for the affected risk, retain every omitted or failed check, and leave domain vetoes and Stage 20 readiness unchanged until exact evidence exists.",
        "protected_gates": ["independent_reproduction", "empirical_confirmation", "participant_evidence", "legal_authority", "maori_authority", "exhaustive_security", "accessibility_complete", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier work validates snapshots and preserves vetoes; none preregisters validation effort as a risk and marginal-information budget while explicitly barring software repetitions from substituting for missing domain evidence.",
    },
]


SOURCES = [
    {
        "source_id": "V6445-S187",
        "source_label": "official_git_documentation",
        "title": "git-sparse-checkout Documentation",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/sparse-checkout",
        "version_or_date": "Current official documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official sparse working-tree behavior and cone-pattern anchor; not proof of dependency closure or a migration decision",
    },
    {
        "source_id": "V6445-S188",
        "source_label": "official_git_documentation",
        "title": "Partial Clone Design Notes",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/partial-clone",
        "version_or_date": "Current official design documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official promisor remote and missing-object design anchor; not path-sparsity or repository-independence proof",
    },
    {
        "source_id": "V6445-S189",
        "source_label": "official_git_documentation",
        "title": "git-backfill Documentation",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/git-backfill",
        "version_or_date": "Current official documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official missing-object backfill anchor; not authority to change the canonical remote",
    },
    {
        "source_id": "V6445-S191",
        "source_label": "official_nist_report",
        "title": "Guidelines on Minimum Standards for Developer Verification of Software",
        "authority": "United States National Institute of Standards and Technology",
        "url": "https://csrc.nist.gov/pubs/ir/8397/final",
        "version_or_date": "NIST IR 8397, October 2021; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official developer-verification technique anchor; not exhaustive validation or independent reproduction",
    },
    {
        "source_id": "V6445-S194",
        "source_label": "official_w3c_wai",
        "title": "Understanding Success Criterion 2.4.1: Bypass Blocks",
        "authority": "World Wide Web Consortium Web Accessibility Initiative",
        "url": "https://www.w3.org/WAI/WCAG21/Understanding/bypass-blocks",
        "version_or_date": "Official understanding document; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official bypass-block interpretation; not manual keyboard or assistive-technology evaluation",
    },
    {
        "source_id": "V6445-S195",
        "source_label": "official_nz_legislation",
        "title": "Protected Disclosures (Protection of Whistleblowers) Act 2022",
        "authority": "New Zealand Parliamentary Counsel Office",
        "url": "https://www.legislation.govt.nz/act/public/2022/0020/latest/whole.html",
        "version_or_date": "Official latest in-force text; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official statutory context; not legal advice, a case decision, or authority delegated to this repository",
    },
    {
        "source_id": "V6445-S196",
        "source_label": "official_nz_ombudsman",
        "title": "Protections for whistle-blowing",
        "authority": "Office of the Ombudsman New Zealand",
        "url": "https://www.ombudsman.parliament.nz/what-we-can-help/serious-wrongdoing-work-whistle-blowing/protections-whistle-blowing",
        "version_or_date": "Official current guidance page; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official public guidance on protection and confidentiality context; not case-specific advice or appointment authority",
    },
    {
        "source_id": "V6445-S198",
        "source_label": "primary_strong_lensing_study",
        "title": "H0LiCOW I. H0 Lenses in COSMOGRAIL's Wellspring",
        "authority": "Suyu et al. / Monthly Notices of the Royal Astronomical Society",
        "url": "https://arxiv.org/abs/1607.01790",
        "version_or_date": "Primary research preprint and journal article, 2016-2017",
        "status_class": "stable",
        "evidence_role": "primary time-delay cosmography methodology and lens-data obligations; not GMUT data or confirmation",
    },
    {
        "source_id": "V6445-S199",
        "source_label": "primary_time_delay_review",
        "title": "Strong lensing time-delay cosmography in the 2020s",
        "authority": "Birrer et al.",
        "url": "https://arxiv.org/abs/2210.10833",
        "version_or_date": "Community review preprint, 2022",
        "status_class": "stable",
        "evidence_role": "review of lens modeling, line-of-sight, kinematic, blinding, and uncertainty obligations; not an inherited dataset or model test",
    },
    {
        "source_id": "V6445-S200",
        "source_label": "primary_disformal_geometry",
        "title": "Disformal transformations in a manifold",
        "authority": "Goulart and Falciano",
        "url": "https://arxiv.org/abs/2111.11634",
        "version_or_date": "Primary research preprint, 2021",
        "status_class": "stable",
        "evidence_role": "primary geometric disformal-map anchor; not a GMUT derivation, observable dictionary, or empirical result",
    },
    {
        "source_id": "V6445-S201",
        "source_label": "primary_disformal_invertibility",
        "title": "Generalized disformal invariance of cosmological perturbations with second-order field derivatives",
        "authority": "Takahashi, Motohashi, and Suyama",
        "url": "https://arxiv.org/abs/1504.00672",
        "version_or_date": "Primary research preprint and journal work, 2015",
        "status_class": "stable",
        "evidence_role": "primary invertibility and disformal-transformation scope anchor; not proof that a GMUT branch is equivalent or healthy",
    },
    {
        "source_id": "V6445-S202",
        "source_label": "primary_stochastic_thermodynamics_review",
        "title": "Stochastic thermodynamics: From principles to the cost of precision",
        "authority": "Udo Seifert",
        "url": "https://arxiv.org/abs/1810.01121",
        "version_or_date": "Primary review preprint, 2018",
        "status_class": "stable",
        "evidence_role": "stochastic-thermodynamic currents, entropy production, and precision-cost anchor; not a psyche measure",
    },
    {
        "source_id": "V6445-S203",
        "source_label": "primary_nonequilibrium_thermodynamics",
        "title": "Nonadiabatic entropy production for non-Markov dynamics",
        "authority": "Esposito and Van den Broeck / Physical Review E",
        "url": "https://doi.org/10.1103/PhysRevE.86.021127",
        "version_or_date": "Peer-reviewed article, 2012",
        "status_class": "stable",
        "evidence_role": "physical entropy-production decomposition anchor; not evidence for psychological effort or consciousness",
    },
    {
        "source_id": "V6445-S204",
        "source_label": "official_fda_guidance",
        "title": "Computer Software Assurance for Production and Quality Management System Software",
        "authority": "United States Food and Drug Administration",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software",
        "version_or_date": "Final guidance, September 2022; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official risk-based software assurance anchor; not regulatory approval, security certification, or deployment authorization",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6445-X1-N01",
        "operation": "broad prior-artifact text search",
        "failure_signature": "An unbounded recursive text scan across the large repository exceeded its sixty-second execution window.",
        "trigger_precondition": "The query combined a broad root with many historical documents instead of a Git-indexed or phase-bounded surface.",
        "recovery": "Switched to Git-indexed searches, exact filenames, and bounded phase directories.",
        "recurrence_guard": "Prefer git grep, rg --files followed by a bounded file set, or direct schema reads before any historical recursive content scan.",
        "promotion_effect": "none; the timed-out scan produced no completeness evidence",
    },
    {
        "negative_id": "V6445-X1-N02",
        "operation": "Codex CLI global package refresh",
        "failure_signature": "The package manager could not remove one locked obsolete temporary executable directory after installing the requested CLI version.",
        "trigger_precondition": "The running desktop process held the old executable while the global package update completed.",
        "recovery": "Verified the new CLI version directly and left the locked temporary directory untouched for the operating system or a later nonrunning-process cleanup.",
        "recurrence_guard": "Treat post-install cleanup warnings separately from version verification; never delete an in-use executable tree during an active desktop session.",
        "promotion_effect": "CLI version verification passed; cleanup completeness remains unclaimed",
    },
    {
        "negative_id": "V6445-X1-N03",
        "operation": "batched predecessor artifact read",
        "failure_signature": "The batch assumed a legacy proposal-ledger filename that the predecessor phase did not contain, causing the aggregate read to fail.",
        "trigger_precondition": "A filename was inferred from an older phase instead of discovered from the current predecessor tree.",
        "recovery": "Enumerated the exact predecessor phase files first and read the current x1-proposals filename.",
        "recurrence_guard": "Use file discovery or manifest lookup before batched reads across evolving artifact schemas.",
        "promotion_effect": "none; the failed batch produced no validation evidence",
    },
    {
        "negative_id": "V6445-X1-N04",
        "operation": "pointer-chain proposal summary",
        "failure_signature": "The first summary queried generic count fields and treated a missing records array as a populated base.",
        "trigger_precondition": "The query assumed a flattened index while the current artifact uses inherited_index plus new_records.",
        "recovery": "Inspected the schema property names and recursively decoded the inherited pointer chain.",
        "recurrence_guard": "Schema-introspect before field selection and validate effective_record_count against recursively collected unique IDs.",
        "promotion_effect": "none; only the corrected 270-record reconstruction is evidence",
    },
    {
        "negative_id": "V6445-X1-N05",
        "operation": "source-ledger summary",
        "failure_signature": "The first summary looked for a sources array, but the current ledger stores inherited_ledger plus added_sources.",
        "trigger_precondition": "A generic field name was assumed without reading the current ledger schema.",
        "recovery": "Read property names, then recursively combined added_sources through the inherited ledger chain.",
        "recurrence_guard": "Use the declared schema and recursive pointer fields rather than guessed collection names.",
        "promotion_effect": "none; only the corrected source reconstruction is counted",
    },
    {
        "negative_id": "V6445-X1-N06",
        "operation": "continuation output polling",
        "failure_signature": "A completed command was queried through an unavailable continuation surface and then through an already-closed completion token.",
        "trigger_precondition": "The caller did not first distinguish active asynchronous execution from a completed result.",
        "recovery": "Reverified the desired Git state directly from the repository and live remote.",
        "recurrence_guard": "Use continuation polling only for an explicitly active command; otherwise re-read the authoritative state directly.",
        "promotion_effect": "none; exact four-way Git equality came from the direct verification",
    },
    {
        "negative_id": "V6445-X1-N07",
        "operation": "preliminary source-slate deduplication gate",
        "failure_signature": "The first slate re-added four exact inherited authority URLs for secure development, credential status, accessibility, and cluster-randomized reporting.",
        "trigger_precondition": "The candidate slate was compared against remembered titles before recursively decoding all 186 inherited source rows.",
        "recovery": "Reused inherited source IDs V8-S22, V8-S12, V8-S26, and V6423-S41 and removed the duplicate additions before x1 freeze.",
        "recurrence_guard": "Run exact normalized-title and canonical-URL deduplication against the full inherited pointer chain before writing a source ledger.",
        "promotion_effect": "none; the rejected duplicate rows are not counted in the v644-v5 source addition",
    },
    {
        "negative_id": "V6445-X1-N08",
        "operation": "first complete x1 repository suite",
        "failure_signature": "The suite passed 616 of 617 tests; the inherited exact legacy constraint-hash alias returned true from CRLF worktree bytes before emitting its required retained-negative warning.",
        "trigger_precondition": "Automatic worktree line-ending conversion made the raw file hash equal the declared legacy hash, bypassing the exact alias-warning branch.",
        "recovery": "Re-materialized that unchanged inherited JSON file byte-for-byte with LF endings matching its Git blob and reran the complete suite.",
        "recurrence_guard": "Before the full suite, compare this named legacy fixture's raw hash with its immutable LF Git-blob hash and normalize only when the worktree conversion is the known cause.",
        "promotion_effect": "none; the 616/617 run is retained failed evidence and only the later 617/617 run is promoted",
    },
    {
        "negative_id": "V6445-X1-N09",
        "operation": "first legacy-fixture line-ending recovery",
        "failure_signature": "A two-step line edit and reversion produced mixed line endings, yielding a third hash that matched neither the declared nor exact legacy alias.",
        "trigger_precondition": "A small patch rewrote only the touched line while preserving converted endings on untouched lines.",
        "recovery": "Recreated the complete small JSON file through the patch tool from its exact HEAD content, producing the expected LF byte hash and passing both isolated alias tests.",
        "recurrence_guard": "For an exact byte-level fixture, rematerialize the complete file from verified repository content rather than patching one line to induce normalization.",
        "promotion_effect": "none; the mixed-ending file and failed isolated run are retained but not promoted",
    },
]


WELLBEING = """# Eiren Kestrel v644-v5 wellbeing and workload check

- Working identity: Eiren Kestrel, they/them, relational language only.
- Role: evidence cartographer and method-flow steward for this phase.
- Hope: turn failures into auditable recovery knowledge while keeping difficult claims corrigible.
- Primary pillar: THOS Body, with GMUT Mind and Freed ID/CBR Heart preserved.
- Applied occupation study: software reliability engineer and scientific-computing auditor. This is a bounded learning lens, not employment, professional registration, or authority.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Eiren lane, strict x1 before x2, no delegation, one full-suite owner validation plus one additional clean-snapshot replay at final.
- Safety: no elevation, host-security weakening, Windows-feature change, reboot, credential use, real participant action, sibling mutation, destructive migration, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Eiren Kestrel v644-v5 integrated overview

## Exact source, ownership, and continuity

This phase begins only after the Eiren-owned branch is shown to be clean, ancestral to Sylven Arc's exact v644-v4 final head, and advanced by fast-forward alone. The local branch, configured upstream, local tracking reference, and fresh live remote all resolve to the exact same source revision. Sylven's source, x1, evidence, closeout, seal, and final lifecycle remain in ancestry. No merge commit, history rewrite, force push, reset, sibling-lane mutation, or deletion is authorized or used. These facts prove repository continuity only. They do not prove scientific correctness, independent reproduction, participant outcomes, identity assurance, cultural legitimacy, legal authority, deployment safety, consciousness, AGI, ASI, or Stage 20 readiness.

Eiren Kestrel, they/them, is the relational working identity used for this packet. The role for v644-v5 is evidence cartographer and method-flow steward, with the hope of turning failures into auditable recovery knowledge while keeping difficult claims corrigible. The primary pillar is THOS Body. The applied occupational lens is software reliability engineering and scientific-computing audit. Those phrases describe the work pattern in this repository; they do not assert employment, professional registration, independent authority, personhood, or identity continuity.

## Strict x1 before x2 and the ten-proposal slate

Exactly ten proposals are frozen before any x2 outcome is produced. The novelty audit recursively reconstructs all 270 earlier frozen proposals through v644-v4 and checks exact identifiers, normalized titles, and semantic mission surfaces. Token overlap is a screening aid only; the actual novelty judgement compares mechanism, evidence object, falsifier, recovery rule, and protected gates. The expected distribution is six completed, two represented or proxy, one open gap, and one exact gate. Those are preregistered expectations, not results. The only permitted x2 classifications are completed, represented, open_gap, and exact_gate, and every failure must remain visible.

The central operational proposal is the Method Flow State ledger. A retained negative is useful only when its failure signature, triggering precondition, bounded recovery, validation witness, recurrence guard, approval class, privacy class, and supersession state remain connected. A workaround without a successful witness is a candidate, not a preferred method. A corrected run does not delete the failed run. A newer method may supersede an older method only with explicit compatibility and rollback information. Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, and private local paths.

## GMUT Mind: formal obligations and an empirical open gap

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The formal proposal focuses on conformal-disformal maps. A derivative-dependent transformation may alter the apparent form of a scalar-tensor action, but formal equivalence is conditional. The map needs a declared domain, an invertible Jacobian, explicit singular branches, a consistent inverse, a named matter-coupling metric, and an observable dictionary. Causal cones cannot be assumed unchanged when the matter metric or derivative structure changes. The synthetic tribunal can reject missing or contradictory obligations. It cannot prove that any GMUT action is ghost-free, well posed, empirically correct, canonical, or a Theory of Everything.

The empirical proposal is deliberately open. Strong-lensing time delays can support cosmographic inference only through a chain that includes measured delays and images, a lens mass model, line-of-sight environment, stellar kinematics when used, covariance and nuisance treatment, a named baseline, a blind holdout, identifiability, and independent review. This repository has official and primary methodological sources but no checksum-bound observation packet and no derived GMUT lensing-delay signature. Therefore no fit, likelihood, posterior, or empirical confirmation is run. Source metadata and a future-study preregistration never substitute for real observations.

## THOS Body: reliability, lean operation, and participant boundaries

THOS Body is represented structurally through a cluster-randomized estimand protocol. Cluster assignment, participant observation, and analysis unit are not interchangeable. If cluster size is related to prognosis or response, naive participant weighting can change the target effect. Recruitment after allocation can introduce another selection path, and contamination can blur the intervention contrast. A proxy can type these obligations and mutation-test them. With zero real arms, no ethics approval, no consent, no preregistered blind matched-budget study, no real outcome or harms data, and no independent review, it cannot support a THOS effectiveness claim.

The repository itself is also treated as a THOS reliability object. The inherited canonical repository contains more than thirty thousand tracked files, while the recent active surface is far smaller. Cutting history during an active six-seat route would create a new lineage and could strand successor checks. The x1 decision is therefore additive and reversible: preserve the canonical branch as authority for v644-v5; measure the dependency closure of the recent active scripts, tests, skills, and phase artifacts; and build a D-first lean companion or export only after its source revision and closure manifest are explicit. Git partial clone and sparse checkout solve different problems—object transfer and working-tree materialization—and neither alone proves that imports, fixtures, or historical anchors are complete. Public remote creation and canonical cutover remain unperformed until successor compatibility and exact routing requirements are known.

The validation-budget proposal does not lower truth standards. Eiren retains the full repository suite because Hamish assigned that responsibility to this seat. The phase then uses one additional clean archive-snapshot replay rather than several near-identical detached-worktree repetitions. This can reduce redundant computation while preserving a second same-owner reproducibility witness. It is not independent-team reproduction. No number of software passes can replace missing empirical data, participant evidence, legal or cultural authority, production cryptography, exhaustive security, or affected-user accessibility evaluation.

## Freed ID and CBR Heart

Freed ID receives a synthetic status-freshness profile. A verifier needs more than a status bit: list purpose, issuer identity, issued or observed epoch, retrieval time, cache-age policy, rollback handling, retrieval-failure policy, and privacy effects must be explicit. An older apparently good list must not silently override a newer revoked state. The profile can reject synthetic stale-good and rollback fixtures and calculate an unresolved exposure window. It does not create standards-conformant real keys or proofs, live issuance, live resolution, live status or revocation, cross-vendor interoperability, privacy assurance, security review, or trust governance.

CBR Heart is exact-gated for protected disclosures. New Zealand legislation and Ombudsman guidance provide public context, but they do not authorize this repository to receive a real disclosure, identify a whistleblower, decide whether serious wrongdoing occurred, promise or lift confidentiality, find retaliation, order a remedy, appoint an ombuds, interpret Māori concepts, provide legal advice, or declare enacted authority. Those decisions require authorized affected parties and competent legal, privacy, cultural, Māori, investigative, employment, and governance authorities as applicable. The x2 output may only preserve neutral questions and nonappointment boundaries.

## Accessibility and thermo-psyche boundaries

The static report will include and test a keyboard-operable skip link, a unique main landmark, and visible focus styling. Static structure can detect a missing target, duplicate target, hidden link, or suppressed focus. It cannot establish complete WCAG conformance, screen-reader behavior across products, cognitive accessibility, multilingual comprehension, or affected-user acceptance. Those evaluations remain reserved.

The thermo-psyche proposal distinguishes housekeeping and excess entropy-production bookkeeping in synthetic nonequilibrium models. Physical currents, affinities, units, sign conventions, steady-state references, and coarse-graining assumptions must remain typed. Physical entropy production is not psychological effort, moral worth, consciousness, or a universal psyche scalar. No cross-domain conversion is permitted without an independently validated construct and participant evidence.

## Terminal boundary

The terminal verdict begins and remains NOT_READY_FOR_STAGE_20. Five open-gap families and six exact-gate families remain inherited unless exact evidence closes them. Real data, independent-team scientific reproduction, blind matched-budget THOS arms, production Freed ID, affected-party legitimacy, Māori wording and authority, legal interpretation, cultural ratification, exhaustive security, complete accessibility, deployment, AGI or ASI, consciousness or personhood, proof or canon, and Theory-of-Everything claims are not established here. Only after the x1 freeze is separately committed and pushed may x2 execute. Only after the exact final head passes the full Eiren validation, one additional clean same-owner replay, privacy and lineage checks, and four-way remote equality may one sanitized baton be sent to the existing Ilyra Fen task.
"""
