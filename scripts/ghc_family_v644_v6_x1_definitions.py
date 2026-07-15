#!/usr/bin/env python3
"""Frozen Ilyra Fen v644-v6 x1 proposal and source definitions."""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6446-P01",
        "title": "Metrological traceability, decision-rule, and guard-band obligation tribunal",
        "mission_surface": "GMUT Mind, measurement science, measurand definition, calibration hierarchy, metrological traceability, uncertainty budget, decision rule, guard band, false-acceptance risk, and claim nonpromotion",
        "hypothesis": "A typed tribunal can reject a synthetic GMUT measurement claim unless the measurand, calibration chain, uncertainty components, decision rule, guard band, and risk allocation are explicit and mutually consistent.",
        "null_or_failure": "The measurand is ambiguous, traceability is asserted without an unbroken documented chain, uncertainty is omitted or double counted, the acceptance rule is reconstructed after seeing the result, or a synthetic conformity row is called empirical confirmation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S205"],
        "deliverables": [
            "physics/metrological-traceability-contract.json",
            "physics/guard-band-decision-mutations.json",
            "physics/measurement-claim-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate measurand, unit, calibration parent, uncertainty component, coverage statement, guard-band direction, decision threshold, risk owner, and claim class; ambiguous, broken, under-budgeted, retrospective, or promoted rows must fail.",
        "rollback_or_recovery": "Restore the last explicit measurement model, retain the failed decision witness, and require qualified metrology review plus real calibrated observations before any empirical claim.",
        "protected_gates": ["real_data", "calibration_evidence", "qualified_metrology_review", "independent_review", "empirical_confirmation", "proof_canon", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 280 frozen proposals include uncertainty budgets and empirical protocols, but none binds traceability hierarchy, conformity decision rules, guard bands, and false-acceptance risk in one mutation-tested GMUT tribunal.",
    },
    {
        "proposal_id": "V6446-P02",
        "title": "GMUT positive self-adjoint extension, boundary-domain, and spectral-stability tribunal",
        "mission_surface": "GMUT Mind, scalar-tensor and EFT research models, spatial operator, Hilbert-space domain, positive self-adjoint extension, boundary form, deficiency freedom, conserved energy, spectral lower bound, and formal nonpromotion",
        "hypothesis": "A formal tribunal can reject a proposed linearized GMUT boundary prescription unless the operator domain, boundary form, positive self-adjoint extension, conserved-energy condition, and spectral lower-bound obligation are stated.",
        "null_or_failure": "A differential expression is mistaken for a complete operator, its domain is absent, inequivalent extensions are hidden, the boundary form does not vanish, positivity or a lower bound is missing, or formal stability is called empirical truth.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S206"],
        "deliverables": [
            "physics/self-adjoint-extension-contract.json",
            "physics/boundary-domain-spectral-mutations.json",
            "physics/formal-stability-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate operator domain, boundary pairing, extension identifier, positivity witness, energy form, spectral lower bound, local-dynamics condition, and claim class; incomplete, inequivalent, unstable, or promoted rows must fail.",
        "rollback_or_recovery": "Return to the unresolved boundary-domain register, retain every failed extension witness, and require model-specific derivation, well-posed dynamics, independent mathematical review, and real observations.",
        "protected_gates": ["gmut_derivation", "well_posedness", "spectral_stability", "independent_mathematical_review", "real_data", "empirical_confirmation", "proof_canon"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals test principal symbols, boundary well-posedness, and covariant phase space; none treats the operator domain and choice among positive self-adjoint extensions as a separate spectral-stability obligation.",
    },
    {
        "proposal_id": "V6446-P03",
        "title": "GMUT galaxy-cluster weak-lensing and hydrostatic-mass blind real-data study",
        "mission_surface": "GMUT Mind, galaxy clusters, weak-lensing mass, hydrostatic mass proxy, selection function, shear calibration, photometric redshift, covariance, blinded mass ratio, derived observable, and independent review",
        "hypothesis": "A future model-specific preregistration could test a derived GMUT cluster-mass observable against checksum-bound weak-lensing and hydrostatic measurements using a frozen blind analysis and named baseline.",
        "null_or_failure": "The GMUT observable is underived, source metadata replace licensed observation rows, shear or redshift systematics are absent, selection and covariance are missing, the mass-ratio holdout is unblinded, or a readiness packet is called empirical support.",
        "approval_class": "candidate_real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V6446-S207"],
        "deliverables": [
            "empirical/cluster-mass-study-preregistration.json",
            "empirical/cluster-real-row-gap.json",
            "empirical/gmut-cluster-confirmation-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Require a derived observable, checksum-bound licensed rows, selection function, shear and redshift calibration, hydrostatic assumptions, covariance, nuisance rules, baseline, blind holdout, identifiability, and independent review; any absence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row and underived-observable gaps, run no likelihood or fit, and reopen only with a frozen analysis packet, authorized data handling, and independent review.",
        "protected_gates": ["gmut_observable_derivation", "real_data", "licensed_observations", "covariance", "blind_holdout", "parameter_identifiability", "independent_review", "empirical_confirmation"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Prior empirical proposals cover cosmology, waves, pulsars, ephemerides, lunar ranging, and strong-lensing time delays; none preregisters a blind weak-lensing versus hydrostatic cluster-mass comparison with selection and calibration obligations.",
    },
    {
        "proposal_id": "V6446-P04",
        "title": "THOS stepped-wedge secular-trend, rollout-sequence, and treatment-switch estimand protocol",
        "mission_surface": "THOS Body, stepped-wedge cluster trial, rollout sequence, calendar time, secular trend, treatment switch, period effect, estimand, matched budget, harms, consent, and independent review",
        "hypothesis": "A proxy protocol can reject stepped-wedge analyses that confound treatment with time, obscure the rollout sequence, or change the estimand after treatment switching.",
        "null_or_failure": "Calendar time is omitted, rollout allocation is not frozen, treatment and period effects are inseparable, switch adherence is hidden, carryover is ignored, or synthetic operating characteristics are called participant evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S208"],
        "deliverables": [
            "thos/stepped-wedge-estimand-contract.json",
            "thos/secular-trend-rollout-mutations.json",
            "thos/real-arm-stepped-wedge-proxy-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate cluster sequence, period index, secular-trend model, switch time, adherence, carryover, estimand, real-arm count, and claim class; confounded, ambiguous, or promoted designs must fail.",
        "rollback_or_recovery": "Restore a prospective zero-real-arm proxy, retain every time-treatment conflict, and require ethics, consent, preregistration, blind matched budgets, real participants, harms monitoring, qualified statistics, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "blind_matched_budget_arms", "real_participants", "real_outcomes", "harms_monitoring", "qualified_statistics", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover cluster estimands, crossover carryover, and allocation; none centers secular time, staggered rollout sequence, and treatment-switch estimands in a stepped-wedge design.",
    },
    {
        "proposal_id": "V6446-P05",
        "title": "Freed ID holder-consent, disclosure-purpose, and verifier-policy hash-binding profile",
        "mission_surface": "Freed ID Heart, verifiable presentation, holder consent, requested attributes, disclosed attributes, purpose string, verifier policy hash, audience, nonce, transaction binding, minimization, interoperability, and production boundary",
        "hypothesis": "A synthetic profile can reject a presentation when holder consent does not bind the requested disclosure set, declared purpose, verifier policy hash, audience, nonce, and transaction context.",
        "null_or_failure": "Consent is generic, disclosed attributes exceed the request, purpose changes after approval, verifier policy is unversioned, audience or nonce is absent, or fixture verification is called production identity assurance.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S09", "V6437-S147"],
        "deliverables": [
            "freed-id/consent-policy-binding-profile.json",
            "freed-id/disclosure-diff-mutation-vectors.json",
            "freed-id/production-consent-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate request set, disclosure set, purpose, policy digest, audience, nonce, holder decision, transaction identifier, and claim class; excessive, stale, unbound, replayable, or promoted rows must fail.",
        "rollback_or_recovery": "Reject the synthetic transaction, retain the failed disclosure witness, require fresh holder action for changed policy, and keep real keys, proofs, issuance, resolution, status, interoperability, privacy and security review, and trust governance open.",
        "protected_gates": ["real_keys", "real_proofs", "live_issuance", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance", "production"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier Freed ID work binds proof purpose, audience, status, and policy concepts separately; none freezes the exact disclosure diff and holder decision against a digest of the verifier policy and declared purpose.",
    },
    {
        "proposal_id": "V6446-P06",
        "title": "CBR beneficiary-data retention, deletion, secondary-use, and Māori access authority gate",
        "mission_surface": "CBR Heart, remedy fund, beneficiary data, retention schedule, deletion, secondary use, collective access, Māori data governance, privacy, audit, affected-party participation, legal authority, and cultural authority",
        "hypothesis": "Only authorized affected parties, Māori data-governance authorities, privacy professionals, fund governors, and competent legal authorities may decide real beneficiary retention, deletion, secondary use, access, or disclosure.",
        "null_or_failure": "The repository accepts beneficiary records, chooses a retention period, promises deletion, authorizes secondary use, defines Māori collective access, identifies recipients, interprets law, or declares legitimacy without exact authority.",
        "approval_class": "exact_approval_needed",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6431-S83", "V6432-S96"],
        "deliverables": [
            "cbr/beneficiary-data-lifecycle-authority-gate.json",
            "cbr/retention-secondary-use-question-set.json",
            "cbr/maori-data-access-nondecision-boundary.json",
        ],
        "test_falsifier_or_gate": "Any real beneficiary intake, retention choice, deletion promise, secondary-use approval, access grant, disclosure, Māori wording, cultural conclusion, privacy conclusion, or legal conclusion requires exact role-specific authority and affected-party safeguards.",
        "rollback_or_recovery": "Keep neutral unanswered fields, accept no real beneficiary data, preserve privacy and Māori authority gates, and seek authorized affected-party, cultural, privacy, governance, and legal participation outside this technical packet.",
        "protected_gates": ["real_identity_data", "beneficiary_privacy", "affected_party_acceptance", "maori_authority", "maori_data_governance", "retention_authority", "secondary_use_authority", "legal_advice", "cultural_ratification", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "The chain reserves remedy-fund governance and Māori authority, but none separately gates the complete beneficiary-data lifecycle across retention, deletion, secondary use, and collective access.",
    },
    {
        "proposal_id": "V6446-P07",
        "title": "Git conditional-include, environment-override, and safe-directory scope tribunal",
        "mission_surface": "THOS Body, repository reliability, Git configuration scope, includeIf, environment override, safe.directory, worktree config, origin visibility, canonical branch, validation lane, and rollback",
        "hypothesis": "A read-only configuration tribunal can explain effective Git settings by origin and reject a named validation lane whose conditional includes, environment overrides, or safe-directory scope could change lineage or trust assumptions.",
        "null_or_failure": "A config value is read without its origin or scope, includeIf matching is assumed, an environment override is hidden, safe.directory is broadened, worktree config diverges silently, or a diagnostic becomes authority to mutate host configuration.",
        "approval_class": "safe_now_read_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S211"],
        "deliverables": [
            "repository/git-config-scope-contract.json",
            "repository/conditional-include-mutation-vectors.json",
            "repository/named-validation-lane-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate config origin, scope, include condition, environment tuple, safe-directory entry, worktree setting, branch, and action class; hidden, overbroad, divergent, or mutating rows must fail.",
        "rollback_or_recovery": "Make no configuration change, retain the diagnostic witness, stop the candidate validation lane if scope is ambiguous, and return to the clean canonical owner lane.",
        "protected_gates": ["host_configuration_change", "host_security_change", "credential_use", "sibling_lane", "history_rewrite", "force_push", "independent_reproduction"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier repository work audits worktree indirection, sparse checkout, and lineage; none types conditional includes, environment overrides, configuration origin, and safe-directory scope as one read-only validation-lane tribunal.",
    },
    {
        "proposal_id": "V6446-P08",
        "title": "Figure-caption, short-and-long text alternative, and underlying-data structural audit",
        "mission_surface": "accessible reporting, figure purpose, concise alternative text, long description, caption, data table, decorative image, programmatic association, static audit, manual testing, and affected-user evaluation",
        "hypothesis": "A static audit can reject a report figure when its purpose, concise alternative, long description or equivalent data, caption association, and decorative status are missing or contradictory.",
        "null_or_failure": "An informative figure has empty alternative text, a complex chart lacks an equivalent description or data table, the caption is unassociated, decorative content is announced, or static structure is called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S212"],
        "deliverables": [
            "accessibility/figure-alternative-contract.json",
            "accessibility/nontext-structure-mutation-vectors.json",
            "accessibility/manual-user-evaluation-reservation.json",
        ],
        "test_falsifier_or_gate": "Mutate figure role, alt text, caption link, long-description target, data-table association, decorative flag, hidden state, and completeness claim; missing, contradictory, inaccessible, or promoted rows must fail.",
        "rollback_or_recovery": "Restore a meaningful text equivalent and structural association, retain every static failure, and reserve assistive-technology, manual, cognitive, multilingual, and affected-user evaluation.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "cognitive_accessibility_review", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior accessibility proposals cover reflow, contrast, focus, tables, abbreviations, bypass blocks, and glossary linkage; none binds figure purpose, short alternative, long equivalent, caption, and underlying data in one contract.",
    },
    {
        "proposal_id": "V6446-P09",
        "title": "Thermodynamic-length, Fisher-metric, and psyche-distance nonconversion classifier",
        "mission_surface": "thermo-psyche, thermodynamic length, Fisher-information metric, control parameter, covariance, protocol speed, dissipative bound, units, coordinate invariance, metaphor boundary, and psyche nonconversion",
        "hypothesis": "A typed classifier can calculate synthetic thermodynamic length only from a declared control manifold and metric while refusing to convert that physical geometry into psychological distance, effort, moral worth, or consciousness.",
        "null_or_failure": "The metric is nonpositive, coordinates and units are unspecified, the path parameterization changes the claimed invariant, covariance is absent, a dissipation bound is treated as equality, or physical length is renamed psyche distance.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6446-S213"],
        "deliverables": [
            "thermo-psyche/thermodynamic-length-classifier.json",
            "thermo-psyche/fisher-metric-mutation-vectors.json",
            "thermo-psyche/psyche-distance-nonconversion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate metric symmetry, eigenvalue sign, coordinate unit, path endpoints, discretization, covariance source, psyche label, and claim class; inconsistent, nonpositive, coordinate-dependent, or converted rows must fail.",
        "rollback_or_recovery": "Restore domain-specific physical quantities, retain every failed metric witness, and require independently validated participant constructs before any psychological interpretation.",
        "protected_gates": ["validated_psychometric_construct", "participant_consent", "real_participant_data", "cross_domain_conversion", "consciousness_claim", "independent_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier thermo-psyche work covers entropy production, response, fluctuation, order parameters, and critical scaling; none treats thermodynamic length and its Fisher metric while explicitly blocking a psyche-distance conversion.",
    },
    {
        "proposal_id": "V6446-P10",
        "title": "Assurance-case defeater, rebuttal, and residual-uncertainty argument graph",
        "mission_surface": "Stage 20, structured assurance, claim, argument, evidence, defeater, rebuttal, residual uncertainty, domain veto, evidence freshness, review owner, and nonreadiness",
        "hypothesis": "A typed assurance graph can reject a readiness argument when a live defeater lacks an evidence-backed rebuttal, residual uncertainty is hidden, evidence is stale, or a domain veto is averaged away.",
        "null_or_failure": "A claim has no supporting evidence, evidence does not entail the claim, a counterexample disappears after a passing test, rebuttal is circular, uncertainty has no owner, or software evidence substitutes for empirical, participant, legal, cultural, privacy, or security authority.",
        "approval_class": "safe_now_structural_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6445-S191", "V6446-S214"],
        "deliverables": [
            "stage20/assurance-defeater-graph.json",
            "stage20/rebuttal-residual-uncertainty-mutations.json",
            "stage20/domain-veto-nonpromotion-boundary.json",
        ],
        "test_falsifier_or_gate": "Mutate claim, evidence link, freshness, defeater state, rebuttal independence, uncertainty owner, domain veto, and readiness class; unsupported, circular, stale, hidden, or promoted arguments must fail.",
        "rollback_or_recovery": "Reopen the affected claim, retain every defeater and failed rebuttal, restore the domain veto, and require exact evidence and authorized review before any readiness decision.",
        "protected_gates": ["independent_reproduction", "empirical_confirmation", "participant_evidence", "legal_authority", "maori_authority", "privacy_review", "exhaustive_security", "accessibility_complete", "stage20_external_decision"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals preserve vetoes and allocate validation effort; none models a readiness argument as claim-evidence edges with explicit defeaters, noncircular rebuttals, residual uncertainty, freshness, and domain-specific vetoes.",
    },
]


SOURCES = [
    {
        "source_id": "V6446-S205",
        "source_label": "official_bipm_metrology_guidance",
        "title": "JCGM 106:2012 Evaluation of measurement data - The role of measurement uncertainty in conformity assessment",
        "authority": "Joint Committee for Guides in Metrology / BIPM",
        "url": "https://www.bipm.org/en/doi/10.59161/jcgm106-2012",
        "version_or_date": "JCGM 106:2012; official BIPM record checked 15 July 2026",
        "status_class": "stable",
        "evidence_role": "primary international metrology guidance for decision rules, guard bands, and conformity risk; not GMUT calibration or empirical confirmation",
    },
    {
        "source_id": "V6446-S206",
        "source_label": "primary_mathematical_physics",
        "title": "Dynamics in Non-Globally-Hyperbolic Static Spacetimes II: General Analysis of Prescriptions for Dynamics",
        "authority": "Ishibashi and Wald / Classical and Quantum Gravity",
        "url": "https://arxiv.org/abs/gr-qc/0305012",
        "version_or_date": "Primary research article, 2003",
        "status_class": "stable",
        "evidence_role": "primary positive self-adjoint-extension and conserved-dynamics anchor; not a GMUT derivation or stability proof",
    },
    {
        "source_id": "V6446-S207",
        "source_label": "primary_cluster_weak_lensing_study",
        "title": "Weighing the Giants - I. Weak-lensing masses for 51 massive galaxy clusters: project overview, data analysis methods and cluster images",
        "authority": "von der Linden et al. / Monthly Notices of the Royal Astronomical Society",
        "url": "https://academic.oup.com/mnras/article/439/1/2/962441",
        "version_or_date": "Primary peer-reviewed article, 2014",
        "status_class": "stable",
        "evidence_role": "primary blind weak-lensing calibration and systematic-uncertainty methodology; not inherited observation rows or a GMUT test",
    },
    {
        "source_id": "V6446-S208",
        "source_label": "primary_reporting_guideline",
        "title": "Reporting of stepped wedge cluster randomised trials: extension of the CONSORT 2010 statement with explanation and elaboration",
        "authority": "Hemming et al. / BMJ",
        "url": "https://www.bmj.com/content/363/bmj.k1614",
        "version_or_date": "Peer-reviewed reporting guideline, 2018",
        "status_class": "stable",
        "evidence_role": "primary stepped-wedge design and reporting obligation anchor; not ethics approval or THOS participant evidence",
    },
    {
        "source_id": "V6446-S211",
        "source_label": "official_git_documentation",
        "title": "git-config Documentation",
        "authority": "Git project",
        "url": "https://git-scm.com/docs/git-config",
        "version_or_date": "Current official documentation; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official configuration scope, includeIf, environment override, and safe.directory anchor; not authority to change host or sibling configuration",
    },
    {
        "source_id": "V6446-S212",
        "source_label": "official_w3c_wai",
        "title": "Understanding Success Criterion 1.1.1: Non-text Content",
        "authority": "World Wide Web Consortium Web Accessibility Initiative",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/non-text-content",
        "version_or_date": "Official WCAG 2.2 understanding document; checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official text-alternative interpretation; not complete conformance, assistive-technology testing, or affected-user evaluation",
    },
    {
        "source_id": "V6446-S213",
        "source_label": "primary_thermodynamic_geometry",
        "title": "Measuring thermodynamic length",
        "authority": "Gavin E. Crooks / Physical Review Letters",
        "url": "https://doi.org/10.1103/PhysRevLett.99.100602",
        "version_or_date": "Primary peer-reviewed article, 2007",
        "status_class": "stable",
        "evidence_role": "primary thermodynamic-length and Fisher-metric anchor; not a psyche metric or participant evidence",
    },
    {
        "source_id": "V6446-S214",
        "source_label": "official_nist_systems_security_engineering",
        "title": "Engineering Trustworthy Secure Systems",
        "authority": "United States National Institute of Standards and Technology",
        "url": "https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final",
        "version_or_date": "NIST SP 800-160 Volume 1 Revision 1, November 2022; current page checked 15 July 2026",
        "status_class": "current",
        "evidence_role": "official systems-security engineering and assurance reasoning anchor; not exhaustive security, certification, deployment, or Stage 20 approval",
    },
]


X1_NEGATIVES = [
    {
        "negative_id": "V6446-X1-N01",
        "operation": "combined source-and-template inspection",
        "failure_signature": "A four-command combined inspection exceeded its ten-second execution envelope before returning output.",
        "trigger_precondition": "Several Git, Python, and large-file reads shared one short orchestration envelope.",
        "recovery": "Recorded the timeout and split inspection into bounded single-purpose commands.",
        "recurrence_guard": "Use separate commands and a measured envelope for large repository state or template reads; never infer success from a timed-out batch.",
        "promotion_effect": "none; the timed-out batch produced no validation evidence",
    },
    {
        "negative_id": "V6446-X1-N02",
        "operation": "short-envelope Git and runner retry",
        "failure_signature": "The first separated retry still exceeded the same ten-second envelope while the large worktree status scan was active.",
        "trigger_precondition": "The retry separated logical checks but retained an envelope below the observed repository scan duration.",
        "recovery": "Raised only the command timeout, kept the check unchanged, and obtained exact clean branch and upstream evidence.",
        "recurrence_guard": "Use a sixty-second ceiling for large D-drive Git state checks while keeping output and query scope bounded.",
        "promotion_effect": "none; only the later completed direct checks are evidence",
    },
    {
        "negative_id": "V6446-X1-N03",
        "operation": "PowerShell ripgrep structure query",
        "failure_signature": "A double-quoted regular expression containing JSON quote syntax caused a PowerShell parse error before ripgrep ran.",
        "trigger_precondition": "Nested shell and regular-expression quotation was composed in one command without a literal single-quoted pattern.",
        "recovery": "Retried with a single-quoted ripgrep expression and a single target file.",
        "recurrence_guard": "Use literal single-quoted ripgrep patterns in PowerShell and avoid nested JSON quoting in composite inspection commands.",
        "promotion_effect": "none; the parse failure changed no file and supplied no evidence",
    },
    {
        "negative_id": "V6446-X1-N04",
        "operation": "Method Flow explicit validation transition for V6446-M02",
        "failure_signature": "The runner rejected an explicit validated-to-validated transition because the passing witness had already advanced the method automatically.",
        "trigger_precondition": "The caller treated witness recording and validated-state promotion as separate operations without first reading the returned method state.",
        "recovery": "Retained the rejected transition and applied only the allowed validated-to-preferred transition.",
        "recurrence_guard": "After recording a witness, inspect the returned method_state; do not request validated when a passing witness has already supplied it.",
        "promotion_effect": "none for the rejected command; the separate preferred transition succeeded only after the witness had validated the method",
    },
    {
        "negative_id": "V6446-X1-N05",
        "operation": "Method Flow explicit validation transition for V6446-M03",
        "failure_signature": "The runner rejected a second explicit validated-to-validated transition after the passing witness had already advanced the method.",
        "trigger_precondition": "The same batched transition assumption was repeated for the second method before the first runner error was observed.",
        "recovery": "Retained the second rejection, confirmed both methods were preferred only after successful witnesses, and preregistered a state-aware runner guard.",
        "recurrence_guard": "Run and inspect one witness result before the next state operation; use set-state preferred only from the returned validated state.",
        "promotion_effect": "none for the rejected command; no witness or negative was erased",
    },
    {
        "negative_id": "V6446-X1-N06",
        "operation": "first complete x1 source-collision gate",
        "failure_signature": "The builder rejected two source additions whose URLs differed from inherited rows but whose normalized titles duplicated inherited W3C and OpenID specifications.",
        "trigger_precondition": "The preliminary slate checked canonical URLs but did not also compare normalized titles across all 200 inherited source rows.",
        "recovery": "Resolved and reused inherited source IDs V8-S09 and V6437-S147, removed both duplicate additions, and reran normalized-title and canonical-URL deduplication before the builder retry.",
        "recurrence_guard": "Compare both normalized title and canonical URL against the recursively decoded inherited ledger before assigning any new source ID.",
        "promotion_effect": "none; the rejected builder run produced no valid x1 freeze and the duplicate rows are not counted",
    },
    {
        "negative_id": "V6446-X1-N07",
        "operation": "second complete x1 expected-file gate",
        "failure_signature": "The builder generated the packet but reported four expected files absent: two phase index receipts had no writer and the two validation outputs were checked before their own creation.",
        "trigger_precondition": "The inherited expected-file list outpaced its direct writer map and treated terminal self-outputs as ordinary pre-existing inputs.",
        "recovery": "Added explicit phase index writers and classified only the two terminal validation outputs as deferred self-outputs created after the presence check.",
        "recurrence_guard": "Map every expected non-self file to a writer or immutable input and keep a named minimal set of terminal self-outputs outside prewrite presence checks.",
        "promotion_effect": "none; the incomplete expected-file run is retained and only a later zero-missing build may be frozen",
    },
    {
        "negative_id": "V6446-X1-N08",
        "operation": "first combined scoped x1 test run",
        "failure_signature": "The scoped run passed 55 of 56 tests; the named-validation receipt called the sequential branch authoritative but omitted the explicit canonical label required by the test and phase rule.",
        "trigger_precondition": "The receipt used a near-synonym where the frozen user boundary and validator require an exact canonical-role statement.",
        "recovery": "Changed the generated canonical_rule to name the canonical sequential branch explicitly and retained the failed 55/56 run.",
        "recurrence_guard": "Use exact frozen boundary vocabulary for canonical role, same-owner replay, and independent-reproduction limits; test the generated receipt rather than implied synonyms.",
        "promotion_effect": "none; only a later 56/56 scoped run may be promoted",
    },
    {
        "negative_id": "V6446-X1-N09",
        "operation": "first exact staged-blob x1 seal review",
        "failure_signature": "All 44 staged files and 35 JSON blobs passed file-set, parse, and privacy checks, but 21 of 36 content-seal hashes differed because the seal used working-tree bytes while Git staged normalized blob bytes.",
        "trigger_precondition": "Python-generated text used Windows working-tree newlines while Git attributes and clean filters normalized the staged representation.",
        "recovery": "Changed the x1 content seal to declare and hash exact Git blob bytes produced through repository attributes and clean filters, then required staged-blob parity.",
        "recurrence_guard": "Use Git-blob SHA-256 for committed-byte manifests and keep normalized logical-text hashes as a separately named domain; never compare an undeclared working-tree domain to staged blobs.",
        "promotion_effect": "none; the 21-mismatch review is retained and only a later zero-mismatch staged review may be promoted",
    },
]


WELLBEING = """# Ilyra Fen v644-v6 wellbeing and workload check

- Working identity: Ilyra Fen, she/they, relational language only.
- Role: evidence-boundary steward for this phase.
- Hope: leave every claim traceable and every gate unmistakable.
- Primary pillar: GMUT Mind, with THOS Body and Freed ID/CBR Heart kept visible.
- Applied practice study: measurement science and metrology. This is a bounded learning lens, not employment, certification, professional registration, or authority.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Ilyra lane, strict x1 before x2, no delegation, scoped round-robin validation plus exactly one additional named-lane replay.
- Safety: no elevation, host-security weakening, Windows-feature change, reboot, credential use, real participant action, sibling mutation, detached validation, destructive migration, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, or independent authority.
"""


OVERVIEW = """# Ilyra Fen v644-v6 integrated overview

## Exact source, ownership, and continuity

This phase begins only after the existing Ilyra-owned canonical branch is shown clean, ancestral to Eiren Kestrel's corrected exact v644-v5 final head, and advanced by fast-forward alone. The local branch, configured upstream, local tracking reference, and a fresh live remote all resolve to the same source revision. The verified Sylven source and seal and Eiren's x1, evidence, closeout, seal, original final record, and corrected final record remain in ancestry. The source-to-final history contains no merge commit and the corrected final commit is single-parent. No reset, history rewrite, force push, sibling-lane mutation, branch reuse, deletion, or merge is authorized. These facts establish repository continuity only; they do not establish scientific correctness, independent reproduction, participant outcomes, identity assurance, cultural legitimacy, legal authority, deployment safety, consciousness, AGI, ASI, or Stage 20 readiness.

Ilyra Fen, she/they, is the relational working identity used for this packet. The role is evidence-boundary steward, with the hope of leaving every claim traceable and every gate unmistakable. The primary Trinity Mandala pillar is GMUT Mind. The bounded human practice lens is measurement science and metrology. This describes a way of organizing uncertainty, traceability, and decisions in the repository. It does not assert employment, certification, professional registration, authority, personhood, sentience, or continuity of identity. Hamish may pause, rename, redirect, or stop the lane.

## Strict x1 before x2 and semantic novelty

Exactly ten proposals are frozen before any x2 implementation or outcome is produced. The novelty audit recursively reconstructs all 280 frozen proposals through v644-v5 and checks unique identifiers, normalized titles, mission surfaces, mechanisms, evidence objects, falsifiers, recovery rules, and protected gates. Token overlap is only a screening aid and cannot substitute for semantic review. The expected distribution is six completed, two represented or proxy, one open gap, and one exact gate. These values are preregistered expectations rather than observed outcomes. X2 may use only completed, represented, open_gap, and exact_gate. Every timeout, tooling fault, negative witness, blocker, workaround, rollback, recurrence guard, and recommendation remains visible through the Method Flow State record.

The ten surfaces are distinct from the inherited chain. Metrological traceability and guard-band decision rules differ from a generic uncertainty budget. Positive self-adjoint extensions differ from principal-symbol or boundary-well-posedness checks because the operator domain and extension choice are themselves evidence obligations. Galaxy-cluster weak-lensing calibration differs from strong-lensing time-delay, lunar-ranging, pulsar, waveform, and background-cosmology studies. A stepped-wedge trial has a time-treatment confounding structure not captured by ordinary cluster or crossover designs. Holder consent bound to a verifier-policy digest differs from status freshness and generic proof-purpose checks. Beneficiary-data retention and secondary use form a lifecycle authority decision distinct from fund arithmetic. Git conditional configuration differs from worktree indirection and sparse checkout. Figure alternatives differ from tables, contrast, reflow, focus, and bypass blocks. Thermodynamic length differs from entropy production and response coefficients. An assurance-case defeater graph differs from counting checks or budgeting validation effort.

## GMUT Mind and measurement-science obligations

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The metrology proposal creates a synthetic obligation tribunal, not a laboratory claim. A measurand must be defined before a value can be compared. Its unit, calibration hierarchy, uncertainty components, correlations, coverage statement, decision threshold, guard band, and risk owner need explicit representation. A traceability assertion must name an unbroken documented chain rather than merely mention a standard. A decision rule fixed after a result is observed cannot be presented as preregistered. Passing a synthetic conformity row does not make a model empirically confirmed. Real calibrated observations, qualified metrology review, model-specific derivation, and independent review remain outside the safe-now lane.

The formal GMUT proposal addresses positive self-adjoint extensions. A differential expression alone is not a fully specified operator: the Hilbert space and operator domain matter. In a setting with boundary freedom, inequivalent positive self-adjoint extensions may encode different admissible dynamics. A formal contract therefore asks for a boundary form, domain, extension identifier, positivity or lower-bound witness, conserved-energy condition, and a statement of how local dynamics is preserved. The tribunal can find missing or contradictory fields in synthetic records. It cannot prove that a particular GMUT action admits the assumed reduction, that nonlinear evolution is well posed, that a spectrum is physically complete, or that the theory is canonical, empirically correct, or a Theory of Everything.

The empirical cluster proposal is deliberately open. A scientifically meaningful weak-lensing and hydrostatic-mass comparison needs a derived model-specific observable, licensed and checksum-bound observations, selection function, shear and photometric-redshift calibration, mass-profile and hydrostatic assumptions, covariance, nuisance rules, a named baseline, frozen blinding rules, identifiability, and independent review. The source ledger supplies primary methodology but no observation packet owned by this phase. No likelihood, fit, posterior, force, prediction, or confirmation can be produced from metadata. The correct x2 result is a structured preregistration and zero-row gap receipt.

## THOS Body and repository reliability

THOS Body remains represented or proxy-only. The stepped-wedge proposal makes calendar time explicit because treatment exposure increases by rollout period. A secular trend can therefore imitate or conceal an intervention effect. Cluster sequence, switch time, adherence, carryover, period effect, estimand, missingness, harms, and analysis plan must be frozen prospectively. A synthetic mutation harness can reject a design in which treatment and time are inseparable or a post-switch estimand is silently changed. With zero real arms, no ethics approval, no consent, no blind matched-budget study, no participant outcomes, no harms monitoring, and no independent review, it cannot support a THOS effectiveness claim.

Repository reliability is bounded by Hamish's current validation refinement. Eiren alone owns the full repository suite. This non-Eiren phase runs checks scoped to the most recent v641-v660 round-robin evidence and the new v644-v6 packet, followed by exactly one additional bounded replay. The replay uses a clean named validation branch and D-drive worktree, not a detached worktree. The Ilyra canonical sequential branch remains authoritative. The validation lane cannot rewrite history, become a second canonical source, change host trust settings, or claim independent-team reproduction. Git configuration is inspected read-only with origin and scope so conditional includes, environment overrides, worktree settings, and safe-directory assumptions cannot silently change the evidence context.

The Method Flow State begins before execution. Each failed command is recorded before a retry. A workaround is a candidate until a bounded witness passes; only then may it become validated or preferred. A successful retry does not delete the timeout, parse error, stale artifact, failed mutation, or portability witness that preceded it. Recurrence guards name the trigger they prevent, rollbacks preserve the canonical branch, and recommendations state sibling-safe boundaries. This is same-owner workflow evidence within shared infrastructure, never independent reproduction.

## Freed ID and CBR Heart

Freed ID receives a consent and verifier-policy binding profile. A presentation request names an audience, nonce, transaction context, purpose, requested attributes, and a digest of the verifier policy. The holder decision must bind that exact context, and the disclosed set must not exceed what was approved. A changed purpose or policy digest requires a new decision. Synthetic fixtures can expose excess disclosure, stale consent, or replayable context. They do not create standards-conformant real keys or proofs, live issuance, resolution, status or revocation, cross-vendor interoperability, privacy assurance, security review, trust governance, or production identity assurance.

CBR Heart is exact-gated for the lifecycle of real beneficiary information. Public privacy principles and Māori data-sovereignty principles provide context, not delegated authority. This repository cannot accept real beneficiary records, select a retention period, promise deletion, approve secondary use, assign collective access, identify recipients, decide Māori wording, interpret law, or declare cultural legitimacy. Those choices require authorized affected parties, Māori authorities, privacy professionals, fund governors, legal authorities, and other competent roles as applicable. X2 may preserve neutral unanswered questions, prohibited-action boundaries, and a role matrix. It may not make the decisions.

## Accessibility, thermo-psyche, and assurance

The static report will treat every informative figure as an evidence object with a purpose, concise text alternative, programmatically associated caption, and a long description or equivalent data table when complexity requires it. Decorative images must be marked so they do not add noise. Static checks can detect missing links and contradictions, but they cannot establish screen-reader behavior, keyboard experience across products, cognitive accessibility, multilingual comprehension, manual conformance, or affected-user acceptance. Complete accessibility remains unclaimed.

The thermo-psyche proposal confines thermodynamic length to a declared physical control manifold and metric. Metric symmetry, positivity, coordinates, units, covariance source, path endpoints, discretization, and parameterization must be explicit. A dissipative bound is not automatically an equality. A coordinate-invariant physical length is not psychological distance, effort, moral worth, identity, or consciousness. Any participant interpretation would need a separately validated construct, consent, real participant evidence, and independent review.

The assurance-case proposal links claims, arguments, evidence, defeaters, rebuttals, evidence freshness, residual uncertainty, review owners, and domain vetoes. A passing software check may rebut a narrow software defeater; it cannot rebut missing real data, ethics, production cryptography, Māori authority, legal authority, privacy review, independent reproduction, exhaustive security, or affected-user evaluation. Circular rebuttals and stale evidence fail. An unresolved defeater remains visible and keeps the corresponding readiness claim open.

## Source, privacy, and terminal boundaries

The phase source ledger combines inherited primary and official references with current v644-v6 additions. Each addition is labelled current or stable and states what it can and cannot support. No source is treated as endorsement, proof, delegated authority, or an observation dataset. Repository artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, and private local paths. Privacy scans cover the exact generated file set and named forbidden pattern classes. Git-index blob manifests remain distinct from normalized logical-text hashes.

The terminal verdict begins and remains NOT_READY_FOR_STAGE_20. Five inherited open-gap families and six inherited exact-gate families remain open unless exact evidence and authority close them. Real data, blind matched-budget THOS arms, production Freed ID, affected-party legitimacy, Māori wording and authority, remedy-fund beneficiary decisions, legal interpretation, cultural ratification, exhaustive security, complete accessibility, deployment, independent-team reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Theory-of-Everything claims are not established. Only after the x1 freeze is committed, pushed, clean, and four-way remote-equal may x2 begin. Only after evidence, closeout, seal, and the exact final head pass scoped canonical validation plus exactly one clean named-lane replay may one sanitized activation baton be sent to the existing Sable Rook task.
"""
