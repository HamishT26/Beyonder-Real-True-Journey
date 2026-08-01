#!/usr/bin/env python3
"""Frozen x1 catalogue for Elaren Kestrel's solo v658-v5 phase."""

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
    source("NANOGRAV-15YR-BACKGROUND", "15-year gravitational-wave background summary", "NANOGrav", "https://nanograv.org/15yr/Summary/Background", "current", "public description of pulsar-timing-array correlation and evidence vocabulary only; no detection credit"),
    source("NANOGRAV-DATA", "NANOGrav public data releases", "NANOGrav", "https://nanograv.org/science/data", "current", "dataset and release-lineage vocabulary only; no download, row, timing solution, or empirical analysis"),
    source("EPTA-DR2", "European Pulsar Timing Array Data Release 2", "European Pulsar Timing Array", "https://www.epta.eu.org/epta-dr2.html", "current", "release, timing-model, noise-model, and posterior-product vocabulary only; no row or inference"),
    source("IPTA-DR2", "International Pulsar Timing Array Data Release 2", "International Pulsar Timing Array", "https://www.ipta4gw.org/data-release-2/", "current_watch", "international release and timing-product context only; no ingestion or interoperability claim"),
    source("PINT-DOCS", "PINT pulsar timing documentation", "NANOGrav PINT", "https://nanograv-pint.readthedocs.io/en/latest/", "current", "timing-model, time-scale, ephemeris, design-matrix, and residual vocabulary only; no software conformance"),
    source("IAU-SOFA", "Standards of Fundamental Astronomy", "International Astronomical Union SOFA Board", "https://www.iausofa.org/", "current", "astronomical time and reference-system vocabulary only; no precision or implementation claim"),
    source("IERS-CONVENTIONS", "IERS Conventions", "International Earth Rotation and Reference Systems Service", "https://www.iers.org/iers/en/dataproducts/conventions/conventions", "current_watch", "reference-system and Earth-orientation lineage vocabulary only; no operational transformation"),
    source("JPL-DE440", "The JPL Planetary and Lunar Ephemerides DE440 and DE441", "NASA Jet Propulsion Laboratory", "https://ssd.jpl.nasa.gov/doc/de440_de441.html", "published", "solar-system ephemeris identity, version, and uncertainty context only; no file or barycentric result"),
    source("TEMPO2", "TEMPO2, a new pulsar-timing package", "Monthly Notices of the Royal Astronomical Society", "https://doi.org/10.1111/j.1365-2966.2006.11030.x", "published", "timing residual, clock, ephemeris, design, and fit vocabulary only; no package-validation claim"),
    source("BAYESIAN-WORKFLOW", "Bayesian workflow", "arXiv primary manuscript", "https://arxiv.org/abs/2011.01808", "published", "iterative prior, computation, predictive, and model-checking vocabulary only"),
    source("SBC", "Simulation-based calibration", "Bayesian Analysis primary manuscript", "https://arxiv.org/abs/1804.06788", "published", "rank-statistic calibration and failure-diagnostic vocabulary only; no real calibration result"),
    source("RHAT-ESS", "Rank-normalization, folding, and localization: an improved R-hat", "Bayesian Analysis primary manuscript", "https://arxiv.org/abs/1903.08008", "published", "R-hat and effective-sample-size diagnostic vocabulary only"),
    source("ARVIZ-DIAGNOSE", "ArviZ diagnostics API", "ArviZ project", "https://python.arviz.org/projects/stats/en/latest/api/generated/arviz_stats.diagnose.html", "current", "diagnostic-interface vocabulary only; no package execution or conformance claim"),
    source("NANOGRAV-PPC", "Posterior predictive checks for pulsar timing array analyses", "NANOGrav primary manuscript", "https://arxiv.org/abs/2407.20510", "preprint_watch", "posterior-predictive discrepancy and checking vocabulary only; no astrophysical inference"),
    source("NANOGRAV-CORRELATION-PITFALL", "On the spurious detection of spatial correlations in pulsar timing arrays", "Primary manuscript", "https://arxiv.org/abs/2306.05558", "preprint_watch", "correlation-comparator and misspecification-risk vocabulary only"),
    source("W3C-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "entity, activity, derivation, revision, invalidation, and attribution lineage"),
    source("W3C-WCAG-22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "machine-checkable structure and notice vocabulary; manual and affected-user evaluation remain reserved"),
    source("W3C-VC-DM-20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model-2.0/", "current", "synthetic nonproduction artifact-envelope vocabulary only; no live identity, proof, or trust"),
    source("W3C-DATA-INTEGRITY", "Verifiable Credential Data Integrity 1.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-integrity/", "current", "proof-configuration vocabulary only; no key, signature, verification, security, or interoperability claim"),
    source("RFC-8785", "JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "deterministic JSON representation vocabulary only; no cryptographic assurance"),
    source("NZ-PRIVACY-PRINCIPLES", "Privacy principles", "Office of the Privacy Commissioner New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "purpose, minimization, correction, retention, use, and disclosure reservations only; no legal advice"),
    source("TE-MANA-RARAUNGA", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "Māori data rights, interests, governance, collective benefit, and authority reservation only"),
    source("LOCAL-CONTEXTS-TK", "Traditional Knowledge Labels", "Local Contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "current_watch", "community-defined notice and authority-reservation context only; no label selection or application"),
]


PROTECTED_GATES = [
    "real_people_participants_astronomers_engineers_observatories_collaborations_and_affected_parties",
    "real_pulsars_telescopes_backends_clocks_ephemerides_toas_timing_solutions_chains_and_datasets",
    "real_observation_download_ingestion_processing_inference_detection_publication_or_operational_decision",
    "professional_astronomy_statistics_metrology_engineering_science_privacy_security_or_accessibility_authority",
    "empirical_gmut_likelihood_prediction_constraint_force_flow_or_confirmation",
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
        "proposal_id": f"V6585-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar_relation": pillar,
        "mechanism": mechanism,
        "hypothesis": f"A bounded {mechanism} contract can expose falsifiable synthetic obligations while refusing unsupported empirical, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, Theory-of-Everything, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, erases a failure, or crosses a protected data, person, scientific, professional, production, rights, legal, cultural, Māori-authority, identity, or Stage 20 gate.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"surfaces/{slug}/contract.json", f"surfaces/{slug}/mutation-results.json", f"surfaces/{slug}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "The valid synthetic fixture passes, five preregistered mutations are rejected, and the receipt grants no real-data, empirical, detection, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        "rollback_or_recovery": "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, observatories, data, instruments, sibling lanes, external systems, rights, and authority state unchanged.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": expected,
    }


PROPOSAL_SPECS = [
    ("Synthetic PTA ensemble declaration with pulsar aliases, sky placeholders, spans, backend classes, observation absence, and no-inference lock", "pta-ensemble-declaration", "GMUT Mind and CBR Heart", "synthetic PTA ensemble, alias, sky placeholder, span, backend class, observation absence, and inference refusal", ["NANOGRAV-DATA", "EPTA-DR2", "IPTA-DR2"]),
    ("Time-of-arrival batch manifest with frequency, uncertainty, flag schema, clock lineage, duplicate quarantine, and zero observed rows", "pta-toa-batch-manifest", "GMUT Mind and Freed ID", "TOA batch metadata, frequency, uncertainty, flags, clock lineage, duplicate quarantine, and zero-row boundary", ["PINT-DOCS", "TEMPO2", "W3C-PROV"]),
    ("Clock-correction lineage across UTC, TAI, TT and BIPM placeholders with leap-event watch and no absolute-time verdict", "pta-clock-correction-lineage", "GMUT Mind and Freed ID", "clock scale, correction version, leap-event watch, derivation, ambiguity, and absolute-time refusal", ["PINT-DOCS", "IAU-SOFA", "IERS-CONVENTIONS"]),
    ("Solar-system ephemeris nuisance ledger with DE identity, digest, barycentric-transform placeholder, uncertainty class, and no-position claim", "pta-ephemeris-nuisance-ledger", "GMUT Mind and Freed ID", "ephemeris identity, digest, barycentric-transform placeholder, nuisance state, uncertainty, and position-claim refusal", ["JPL-DE440", "PINT-DOCS", "W3C-PROV"]),
    ("Timing-model design matrix with parameter units, free-frozen states, rank audit, projection lineage, and no fitted solution", "pta-timing-design-matrix", "GMUT Mind", "timing-model parameters, units, free-frozen states, matrix rank, projection lineage, and fitted-solution refusal", ["PINT-DOCS", "TEMPO2", "BAYESIAN-WORKFLOW"]),
    ("Backend-specific EFAC, EQUAD and ECORR white-noise hyperparameter contract with support bounds and no precision claim", "pta-white-noise-hyperparameters", "GMUT Mind", "backend white-noise hyperparameters, units, support, block structure, uncertainty, and precision refusal", ["NANOGRAV-DATA", "EPTA-DR2", "BAYESIAN-WORKFLOW"]),
    ("Chromatic dispersion-noise basis with frequency scaling, epoch grouping, Fourier modes, support, and propagation-effect abstention", "pta-chromatic-dispersion-basis", "GMUT Mind", "chromatic dispersion basis, frequency scaling, epochs, modes, support, and propagation-effect refusal", ["EPTA-DR2", "PINT-DOCS", "BAYESIAN-WORKFLOW"]),
    ("Achromatic red-noise Fourier basis with frequency grid, amplitude and spectral-index support, truncation, and source abstention", "pta-red-noise-fourier-basis", "GMUT Mind", "achromatic Fourier basis, frequency grid, spectral support, truncation, residual channel, and source refusal", ["NANOGRAV-15YR-BACKGROUND", "EPTA-DR2", "BAYESIAN-WORKFLOW"]),
    ("Common-spectrum process registry with shared spectral law, pulsar coupling, alternative labels, identifiability hold, and no-background claim", "pta-common-spectrum-registry", "GMUT Mind", "common-spectrum process, shared law, pulsar coupling, alternatives, identifiability, and background-claim refusal", ["NANOGRAV-15YR-BACKGROUND", "NANOGRAV-CORRELATION-PITFALL", "BAYESIAN-WORKFLOW"]),
    ("Pairwise angular-separation matrix with synthetic sky vectors, symmetry, diagonal handling, tolerance, and zero celestial-position claim", "pta-angular-separation-matrix", "GMUT Mind", "synthetic sky vector, pair separation, symmetry, diagonal policy, tolerance, and celestial-position refusal", ["NANOGRAV-15YR-BACKGROUND", "IAU-SOFA", "RFC-8785"]),
    ("Hellings-Downs overlap-reduction kernel with normalization convention, limiting cases, symmetry, and no detection promotion", "pta-hellings-downs-kernel", "GMUT Mind", "Hellings-Downs kernel, normalization, limiting cases, symmetry, tolerance, and detection refusal", ["NANOGRAV-15YR-BACKGROUND", "NANOGRAV-CORRELATION-PITFALL", "BAYESIAN-WORKFLOW"]),
    ("Monopole clock-error correlation comparator with kernel identity, nuisance interpretation, mismatch hold, and no clock diagnosis", "pta-monopole-comparator", "GMUT Mind", "monopole comparator, clock-error hypothesis, kernel identity, mismatch hold, and diagnosis refusal", ["NANOGRAV-CORRELATION-PITFALL", "IERS-CONVENTIONS", "BAYESIAN-WORKFLOW"]),
    ("Dipole ephemeris-error correlation comparator with projection convention, axis placeholders, mismatch hold, and no ephemeris diagnosis", "pta-dipole-comparator", "GMUT Mind", "dipole comparator, ephemeris-error hypothesis, projection convention, axis placeholders, and diagnosis refusal", ["NANOGRAV-CORRELATION-PITFALL", "JPL-DE440", "BAYESIAN-WORKFLOW"]),
    ("Uncorrelated common-red comparator with shared spectrum, independent pulsar draws, exchangeability note, and no spatial-correlation claim", "pta-uncorrelated-common-red", "GMUT Mind", "uncorrelated common-red comparator, shared spectrum, independent draws, exchangeability, and spatial-claim refusal", ["NANOGRAV-15YR-BACKGROUND", "NANOGRAV-CORRELATION-PITFALL", "BAYESIAN-WORKFLOW"]),
    ("Composite PTA covariance assembly with component provenance, symmetry, positive-semidefinite audit, conditioning, jitter, and no data fit", "pta-covariance-assembly", "GMUT Mind and THOS Body", "covariance components, provenance, symmetry, PSD audit, conditioning, jitter, and fit refusal", ["BAYESIAN-WORKFLOW", "PINT-DOCS", "W3C-PROV"]),
    ("Gaussian-process likelihood factorization with quadratic form, log determinant, normalization, failure states, and zero empirical likelihood", "pta-gp-likelihood-factorization", "GMUT Mind", "Gaussian-process likelihood factorization, quadratic form, log determinant, normalization, failures, and empirical-likelihood refusal", ["BAYESIAN-WORKFLOW", "RHAT-ESS", "PINT-DOCS"]),
    ("Prior support and transform ledger with units, Jacobian, boundary mass, sensitivity plan, provenance, and no posterior conclusion", "pta-prior-support-ledger", "GMUT Mind and Freed ID", "prior support, transform, units, Jacobian, boundary mass, sensitivity, and posterior-conclusion refusal", ["BAYESIAN-WORKFLOW", "SBC", "W3C-PROV"]),
    ("Sampler-run diagnostic docket with seeds, warmup, divergences, rank R-hat, bulk-tail ESS, chain status, and no convergence guarantee", "pta-sampler-diagnostics", "GMUT Mind and THOS Body", "sampler seeds, warmup, divergences, rank R-hat, ESS, chains, and convergence-guarantee refusal", ["RHAT-ESS", "ARVIZ-DIAGNOSE", "BAYESIAN-WORKFLOW"]),
    ("Posterior-predictive residual check board with discrepancy registry, replicated placeholders, tail alerts, multiplicity note, and no adequacy verdict", "pta-posterior-predictive-board", "GMUT Mind", "posterior-predictive discrepancies, replicated placeholders, tails, multiplicity, and adequacy-verdict refusal", ["NANOGRAV-PPC", "BAYESIAN-WORKFLOW", "ARVIZ-DIAGNOSE"]),
    ("Simulation-based calibration rank ledger with generative provenance, rank bins, uniformity diagnostics, failure quarantine, and no calibrated-instrument claim", "pta-simulation-calibration", "GMUT Mind", "simulation-based calibration, generative provenance, ranks, uniformity diagnostics, quarantine, and calibration-claim refusal", ["SBC", "BAYESIAN-WORKFLOW", "ARVIZ-DIAGNOSE"]),
    ("Blinded synthetic injection-recovery protocol with commitment digest, reveal gate, interval coverage, bias placeholders, and no sensitivity claim", "pta-injection-recovery", "GMUT Mind and Freed ID", "synthetic injection, blind commitment, reveal gate, coverage, bias placeholders, and sensitivity-claim refusal", ["SBC", "RFC-8785", "W3C-PROV"]),
    ("Evidence-estimator triangulation register with method assumptions, uncertainty, disagreement quarantine, stopping rule, and no Bayes-factor result", "pta-evidence-triangulation", "GMUT Mind and THOS Body", "evidence-estimator methods, assumptions, uncertainty, disagreement, stopping rule, and Bayes-factor refusal", ["BAYESIAN-WORKFLOW", "NANOGRAV-15YR-BACKGROUND", "W3C-PROV"]),
    ("Model-comparison decision sheet with prior odds, comparator coverage, sensitivity, null outcome, wording firewall, and no discovery claim", "pta-model-comparison-sheet", "GMUT Mind and CBR Heart", "prior odds, comparator coverage, sensitivity, null outcome, wording firewall, and discovery refusal", ["NANOGRAV-15YR-BACKGROUND", "NANOGRAV-CORRELATION-PITFALL", "BAYESIAN-WORKFLOW"]),
    ("THOS deterministic PTA shard and checkpoint protocol with partition digest, retry budget, orphan quarantine, and no throughput claim", "thos-pta-shard-checkpoint", "THOS Body", "deterministic shard, checkpoint, partition digest, retry budget, orphan quarantine, and throughput-claim refusal", ["W3C-PROV", "RFC-8785", "BAYESIAN-WORKFLOW"]),
    ("THOS covariance-cache provenance and invalidation protocol with dependency digest, scope lease, stale-entry quarantine, and no performance claim", "thos-pta-covariance-cache", "THOS Body and Freed ID", "covariance cache, dependency digest, scope lease, invalidation, stale quarantine, and performance-claim refusal", ["W3C-PROV", "RFC-8785", "PINT-DOCS"]),
    ("Freed ID synthetic PTA analysis-artifact envelope with digest, derivation, amendment, expiry, revocation hold, and no live proof", "freed-id-pta-artifact-envelope", "Freed ID", "synthetic analysis-artifact envelope, digest, derivation, amendment, expiry, revocation hold, and live-proof refusal", ["W3C-VC-DM-20", "W3C-DATA-INTEGRITY", "W3C-PROV"]),
    ("Freed ID PTA model-card disclosure with purpose, assumptions, exclusions, limitation lineage, contest route, and no trust decision", "freed-id-pta-model-card", "Freed ID and CBR Heart", "model-card purpose, assumptions, exclusions, limitations, contest route, provenance, and trust-decision refusal", ["W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "W3C-PROV"]),
    ("Structurally accessible PTA inference atlas with scoped tables, noncolour comparator states, provenance links, reflow and manual-evaluation reservation", "pta-accessible-inference-atlas", "CBR Heart and THOS Body", "accessible inference atlas, scoped tables, noncolour states, provenance, reflow, and manual-evaluation reservation", ["W3C-WCAG-22", "W3C-PROV", "NZ-PRIVACY-PRINCIPLES"]),
    ("NANOGrav, IPTA and EPTA zero-row capability gateway with release watch, disabled transport, schema placeholders, and no external validation", "pta-release-capability-gateway", "All pillars", "external PTA release capability, release watch, disabled transport, schema placeholders, zero rows, and external-validation refusal", ["NANOGRAV-DATA", "IPTA-DR2", "EPTA-DR2"]),
    ("CBR observatory, Indigenous sky-knowledge, sensitive-location, collective-data, publication, remedy and Māori-authority covenant", "cbr-pta-authority-covenant", "CBR Heart across all pillars", "observatory and Indigenous sky-knowledge relationships, sensitive locations, collective data, publication, remedy, community protocol, and Māori-authority reservation", ["TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "NZ-PRIVACY-PRINCIPLES"]),
]


PROPOSALS = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]


SKILL_SPECS = [
    ("ghc-family-pta-scope-firewall", "Constrain synthetic PTA scope, zero rows, aliases, spans, backend classes, and no-inference states."),
    ("ghc-family-pta-time-ephemeris-lineage", "Constrain clock scales, corrections, ephemeris identity, digests, transforms, uncertainty, and abstention."),
    ("ghc-family-pta-noise-basis", "Constrain white, chromatic, red, and common-process bases, supports, units, provenance, and source refusal."),
    ("ghc-family-pta-correlation-kernels", "Constrain angular separation, Hellings-Downs, monopole, dipole, and uncorrelated comparators."),
    ("ghc-family-pta-covariance-likelihood", "Constrain covariance assembly, PSD checks, conditioning, factorization, normalization, and likelihood abstention."),
    ("ghc-family-pta-bayesian-diagnostics", "Constrain priors, transforms, MCMC diagnostics, posterior predictive checks, and nonpromotion."),
    ("ghc-family-pta-injection-calibration", "Constrain SBC, blinded synthetic injection recovery, estimator triangulation, and model comparison."),
    ("ghc-family-pta-thos-orchestration", "Constrain deterministic shards, checkpoints, cache provenance, invalidation, retry, and recovery."),
    ("ghc-family-pta-freed-id-provenance", "Constrain synthetic artifact envelopes, model cards, digests, amendments, expiry, and revocation holds."),
    ("ghc-family-pta-authority-reservation", "Fail closed around people, observatories, Indigenous sky knowledge, sensitive locations, publication, law, culture, and Māori authority."),
]


RUNNER_SPECS = [
    ("ghc_family_pta_scope_firewall.py", "pta-ensemble-declaration"),
    ("ghc_family_pta_time_ephemeris_lineage.py", "pta-clock-correction-lineage"),
    ("ghc_family_pta_noise_basis.py", "pta-white-noise-hyperparameters"),
    ("ghc_family_pta_correlation_kernels.py", "pta-hellings-downs-kernel"),
    ("ghc_family_pta_covariance_likelihood.py", "pta-covariance-assembly"),
    ("ghc_family_pta_bayesian_diagnostics.py", "pta-sampler-diagnostics"),
    ("ghc_family_pta_injection_calibration.py", "pta-simulation-calibration"),
    ("ghc_family_pta_thos_orchestration.py", "thos-pta-shard-checkpoint"),
    ("ghc_family_pta_freed_id_provenance.py", "freed-id-pta-artifact-envelope"),
    ("ghc_family_pta_authority_reservation.py", "cbr-pta-authority-covenant"),
]


def negative(number: int, slug: str, failure: str, recovery: str, guard: str) -> dict:
    return {
        "negative_id": f"V6585-X1-N{number:02d}",
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
    negative(1, "powershell-empty-pipeline-parser-failure", "The first inventory wrapper placed a foreach expression directly inside a pipeline and failed before any repository probe completed.", "Materialize the foreach results into a scalar collection before piping or serializing them.", "Never place an empty or syntactically ambiguous foreach expression at a PowerShell pipeline boundary."),
    negative(2, "schema-batch-positional-argument-omission", "A schema-reading batch assumed positional PowerShell arguments that were not supplied, so four requested reads failed before opening.", "Use explicit literal paths in a bounded loop and verify every selected file reaches EOF.", "Bind every batched schema path explicitly rather than relying on transport-specific positional arguments."),
    negative(3, "python-c-windows-quote-stripping", "The first manifest verifier used python -c and Windows native argument processing stripped inner quotes, producing a syntax error.", "Pass multiline verifier source over standard input to python -.", "Use stdin for quote-rich multiline Python diagnostics on Windows."),
    negative(4, "powershell-parenthesized-command-form", "A clean-state wrapper used an invalid parenthesized PowerShell command form and failed before Git status completed.", "Capture each Git command result and exit code in scalar variables before object projection.", "Separate native command execution from PowerShell expression grouping."),
    negative(5, "cp1252-maori-keyword-scan-output", "The first keyword audit completed its file search but failed while printing a Māori title through the CP1252 console.", "Set UTF-8 output explicitly and rerun only the read-only display layer.", "Use UTF-8 console output before rendering Unicode repository text."),
    negative(6, "rg-unix-wildcard-on-windows", "A generic-builder search passed Unix-style path wildcards directly to rg on Windows and matched no intended files.", "Use rg -g glob filters rooted at the exact repository path.", "Use ripgrep glob arguments rather than shell-expanded Unix wildcards on Windows."),
    negative(7, "powershell-backtick-javascript-template-collision", "A route-hash probe embedded a PowerShell backtick inside a JavaScript template literal and failed before hashing.", "Use literal command strings without JavaScript template interpolation and hash the exact Git blob separately.", "Keep PowerShell escape syntax out of JavaScript template delimiters."),
    negative(8, "powershell-revision-variable-javascript-interpolation", "A second route probe used a PowerShell revision variable form that JavaScript attempted to interpolate before execution.", "Pass the exact revision and repository-relative path as literal command arguments.", "Avoid cross-language variable sigils in nested command transport."),
    negative(9, "powershell-rg-pattern-quote-terminator", "The first supplemental stale-label wrapper lost a nested PowerShell quote terminator before ripgrep executed and earned zero scan credit.", "Pass each stale-label token as a separate literal ripgrep -e pattern.", "Avoid one composite quoted regex when command transport spans JavaScript, PowerShell, and ripgrep."),
]


SAFE_TASKS = [
    {"task_id": f"V6585-SAFE-{index:03d}", "proposal_id": item["proposal_id"], "task": f"Build and validate the bounded synthetic contract for {item['slug']}.", "approval_class": "safe_now_owner_local_additive", "x1_execution": False, "planned_lane": "x2"}
    for index, item in enumerate(PROPOSALS, 1)
]


CANDIDATE_TASKS = [
    {"task_id": f"V6585-CAND-{index:03d}", "task": f"Prototype a reversible cross-surface refinement for {PROPOSALS[(index - 1) % len(PROPOSALS)]['slug']}.", "approval_class": "candidate_owner_local_review_required", "x1_execution": False, "planned_lane": "x2_if_bounded_evidence_permits"}
    for index in range(1, 21)
]


CLEAN_TASKS = [
    {"task_id": f"V6585-CLEAN-{index:03d}", "task": f"Run additive compatibility, privacy, provenance, stale-label, and nonpromotion cleanup for {item['slug']}.", "approval_class": "safe_now_additive_cleanup", "x1_execution": False, "planned_lane": "x2"}
    for index, item in enumerate(PROPOSALS, 1)
]
