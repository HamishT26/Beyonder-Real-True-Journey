#!/usr/bin/env python3
"""Frozen x1 definitions for Orin Thale v647-v2.

Importing this module performs no I/O and grants no x2 completion credit.
Identity language is relational working language only.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v2-x1-x2"
PHASE_SHORT = "v647-v2"
OWNER = "Orin Thale"
SLUG = "orin-thale"
PRONOUNS = "they/them"
ROLE = "boundary-and-method steward"
HOPE = "keep every surviving claim inspectable, challengeable, and safely retractable"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "rail-signalling engineering-possession, worksite-protection, release, and shift-handover review"

SOURCE_PHASE = "v647-gmut-thos-v1-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_REVISION = "c3025ff0d5c062ece7977b4df7f1a34db7d08afe"
SOURCE_INHERITED_REVISION = "d0d2b7617a84aeed94c425cdf83214f46ffeb24b"
SOURCE_X1_FIRST_REVISION = "cb35da3e54a815d9ecd8940eedaa1826e58b3da8"
SOURCE_X1_REVISION = "d120045b586665b507d3460b254158ec28e0baa6"
SOURCE_EVIDENCE_REVISION = "24aa0005fe3286f89201026e18fd9bcdfed74c3f"
PRIOR_FROZEN_PROPOSALS = 480
INHERITED_EFFECTIVE_NEGATIVES = 3235
SEALED_SOURCE_NEGATIVES = 3235
EXTERNAL_SOURCE_NEGATIVES = 0
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 18
INHERITED_EXACT_GATES = 19
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Orin Thale, they/them, is relational working language for a boundary-and-method steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural "
    "authority, or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; Freed ID "
    "remains synthetic and nonproduction; CBR, rail safety, privacy, remedy, legal, cultural, affected-party, "
    "and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. "
    "No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, professional, "
    "rail-safety, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6472-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Method Flow UTF-8 record-framing, partial-line, stdout/stderr separation, stream-order, exit-status, and evidence-credit tribunal",
        mission_surface="declared encoding, record delimiter, complete and partial records, stdout and stderr channel identity, interleaving scope, buffering, truncation marker, timeout, exit status, parse failure, and evidence credit",
        hypothesis="A bounded synthetic tribunal can distinguish complete machine-readable command records from partial, misencoded, reordered, truncated, or channel-ambiguous output and refuse completion credit without a valid exit-status witness.",
        null_or_failure="A partial final line parses as complete, invalid UTF-8 is silently replaced, stdout and stderr are conflated, cross-channel order is invented, truncation is hidden, a nonzero exit receives success credit, or a timeout receives completion credit.",
        approval_class="safe_now_owner_scoped_synthetic",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S01", "V6472-S02"],
        concrete_artifacts=["method-flow/command-stream-contract.json", "method-flow/command-stream-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must accept one exact complete UTF-8 record stream and reject partial-line, invalid-encoding, merged-channel, invented-order, hidden-truncation, nonzero-exit, and timeout-as-pass mutations.",
        rollback_or_recovery="Quarantine the stream witness, retain every partial or failed record, return to the last complete checkpoint, and require fresh authority before any external side effect.",
        protected_gates=["credentials", "external_state", "destructive_action", "sibling_lane", "completion_credit", "stage20"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="Prior Method Flow proposals cover executable shadowing, retry, cancellation, durable outboxes, fencing, causal witnesses, and subprocess starts; none centers UTF-8 record framing, partial-line retention, channel separation, stream ordering, truncation, and exit-status credit together.",
    ),
    proposal(
        2,
        title="GMUT Batalin-Vilkovisky antibracket, ghost-number, classical-master-equation, gauge-fixing-fermion, and EFT-truncation obligation board",
        mission_surface="fields, antifields, Grassmann parity, ghost number, antibracket grading, classical master equation, gauge-fixing fermion, canonical transformation, anomaly reservation, regulator, truncation, units, and observation firewall",
        hypothesis="A typed symbolic board can expose Batalin-Vilkovisky grading and master-equation obligations for a GMUT scaffold without constructing a quantum action or proving gauge independence, anomaly freedom, renormalizability, or physical truth.",
        null_or_failure="Field and antifield degrees collapse, the antibracket sign or ghost number drifts, the classical and quantum master equations are conflated, gauge fixing is treated as proof, or symbolic consistency becomes a prediction or completed quantum theory.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S03", "V6472-S04"],
        concrete_artifacts=["gmut/bv-master-equation-obligations.json", "gmut/bv-master-equation-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type parity, ghost number, fields, antifields, antibracket, classical master equation, gauge-fixing fermion, approximation scope, anomaly reservation, units, and observation firewall.",
        rollback_or_recovery="Restore missing grading, gauge, regulator, and truncation obligations; retain the failed vector; and make no force, likelihood, constraint, stability, anomaly, quantum-completion, or Theory-of-Everything claim.",
        protected_gates=["quantum_master_equation", "anomaly_freedom", "gauge_independence_proof", "renormalizability", "empirical_confirmation", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="Prior GMUT boards cover BRST, Slavnov-Taylor, Nielsen, Vilkovisky-DeWitt, Schwinger-Keldysh, Peierls, spectral support, and functional RG; no frozen title centers the BV antibracket, antifields, ghost grading, master equation, and gauge-fixing fermion.",
    ),
    proposal(
        3,
        title="GMUT KiDS-1000 weak-lensing catalogue, shear-calibration, redshift-distribution, covariance, and zero-row likelihood-refusal protocol",
        mission_surface="official release identity, legacy and supersession status, catalogue schema, shape weights, masks, shear calibration, photometric-redshift distribution, tomographic bins, data vector, covariance, scale cuts, nuisance lock, checksums, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze KiDS-1000 weak-lensing obligations while refusing to turn official pages, catalogue descriptions, or published cosmology into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads a catalogue or covariance, imports published vectors, ignores release supersession or masks, chooses calibration after outcomes, evaluates a likelihood, or emits a GMUT constraint.",
        approval_class="real_data_access_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6472-S05", "V6472-S06"],
        concrete_artifacts=["empirical/kids1000-study-contract.json", "empirical/kids1000-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero downloads, catalogue rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit, retain the zero-row receipt, and require separately authorized preregistration with frozen release, checksums, masks, calibration, redshift distributions, covariance, scale cuts, nuisance model, uncertainty treatment, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_480_frozen_proposals="The corpus includes ACT, Euclid, Rubin, CHIME/FRB, GWOSC, DESI, EHT, eROSITA, NANOGrav, Gaia, and other zero-row adapters; no frozen title centers KiDS-1000 shear calibration, redshift distributions, covariance, and release-supersession handling.",
    ),
    proposal(
        4,
        title="THOS railway engineering-possession, worksite-boundary, protection, release, overrun, and shift-handover proxy",
        mission_surface="synthetic possession identifier, limits, worksite, protection state, authority holder, personnel and vehicle clearance flags, conflict, overrun, amendment, release refusal, readback, workload budget, escalation, and next-shift ownership",
        hypothesis="Synthetic traces can expose boundary drift, premature release, protection mismatch, uncleared worksite, overrun, and ambiguous handover while preserving every real worker, railway, safety, operational, and authority gate.",
        null_or_failure="A fixture names real workers or infrastructure, grants or releases a real possession, treats one rulebook as universal operational law, hides a conflict or overrun, breaks workload limits, or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6472-S07", "V6472-S08", "V6472-S09"],
        concrete_artifacts=["thos/rail-possession-contract.json", "thos/rail-possession-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real workers, infrastructure, possessions, movements, releases, incidents, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational language, retain rejected traces, and defer real protection, possession, movement, release, incident, worker, and safety decisions to authorized operators, regulators, affected parties, and independent reviewers.",
        protected_gates=["real_people", "real_railway", "movement_authority", "possession_release", "professional_competence", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_480_frozen_proposals="A prior railway proposal centers speed-restriction communication and control-room handover; this proposal instead centers engineering-possession limits, worksite protection, clearance, release, and overrun, with semantic-neighbor separation recorded.",
    ),
    proposal(
        5,
        title="Freed ID WebAuthn Level 3 RP-ID, origin, challenge, user-verification, backup-state, attestation, and privacy profile",
        mission_surface="relying-party identifier, origin, top origin, challenge, ceremony type, client-data hash, authenticator-data flags, user presence, user verification, backup eligibility and state, sign counter, attestation conveyance, credential discoverability, unknown enumeration, and privacy refusal",
        hypothesis="Synthetic WebAuthn vectors can enforce bounded ceremony-context and flag rules without asserting a real account, authenticator, private key, biometric, attestation trust, interoperable ceremony, or physical-identity binding.",
        null_or_failure="RP ID or origin mismatches pass, challenges replay, backup flags are inconsistent, user verification is inferred, unknown values are rejected unsafely, attestation becomes identity proof, or synthetic structure becomes production authentication assurance.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6472-S10", "V6472-S11"],
        concrete_artifacts=["freed-id/webauthn-context-profile.json", "freed-id/webauthn-context-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject origin, RP-ID, challenge, type, flag, counter, attestation, backup-state, and privacy violations while preserving unknown-value and nonproduction boundaries.",
        rollback_or_recovery="Reject and retain the vector, publish no real account or authenticator data, and require real keys, ceremonies, origin validation, attestation policy, interoperability, privacy and security review, recovery, and trust governance.",
        protected_gates=["real_account", "real_keys", "biometric_data", "live_authentication", "attestation_trust", "interoperability", "production"],
        expected_disposition="represented",
        novelty_against_480_frozen_proposals="Prior Freed ID work covers VC, OpenID4VC, mdoc, DPoP, federation, Controlled Identifiers, status, cryptosuite agility, and SCITT; no frozen title centers WebAuthn Level 3 ceremony context, backup flags, attestation, and privacy together.",
    ),
    proposal(
        6,
        title="CBR rail-possession disruption, trackworker reporting, disability access, location privacy, remedy, affected-party, and Māori-authority matrix",
        mission_surface="synthetic disruption, worker and public safety report, service accessibility, protected location, confidentiality, notification, correction, remedy, legal interpretation, affected parties, place and infrastructure data, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved reporting, accessibility, privacy, remedy, and authority questions without deciding a real occurrence, possession, safety finding, entitlement, disclosure, place meaning, or remedy.",
        null_or_failure="The matrix identifies a real protected person or location, changes railway operations, decides fault or compensation, interprets law, discloses confidential data, asserts cultural or Māori authority, or treats guidance as delegated case authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6472-S08", "V6472-S09", "V6472-S12", "V6472-S13", "V6472-S14"],
        concrete_artifacts=["cbr/rail-authority-reservation.json", "cbr/rail-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Repository software must stop at unknown or reserved; only competent railway, safety, privacy, legal, accessibility, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before reporting, disclosure, operational, compensation, cultural, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "rail_safety_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision", "real_occurrence"],
        expected_disposition="exact_gate",
        novelty_against_480_frozen_proposals="Prior CBR matrices address aviation, wildfire, food, water, medicine, museums, fisheries, utilities, archives, and other domains; no frozen title combines rail-possession disruption, trackworker reporting, disability access, location privacy, remedy, and Māori authority.",
    ),
    proposal(
        7,
        title="OCI image-layer digest, DiffID, whiteout, opaque-directory, link-target, traversal, and extraction-budget tribunal",
        mission_surface="manifest descriptor, media type, compressed digest, uncompressed DiffID, ordered layer, whiteout, opaque whiteout, same-layer precedence, symlink, hardlink, special file, path normalization, traversal refusal, entry count, expanded bytes, and teardown",
        hypothesis="A disposable synthetic tribunal can distinguish valid OCI layer changesets from digest drift, whiteout-order errors, link escape, traversal aliases, and budget exhaustion without pulling, unpacking, or certifying a production image.",
        null_or_failure="Digest and DiffID are conflated, a whiteout affects the same layer, opaque deletion order drifts, a link escapes the root, normalized traversal passes, a budget is ignored, or synthetic fixtures become production security certification.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S15", "V6472-S16"],
        concrete_artifacts=["tooling/oci-layer-contract.json", "tooling/oci-layer-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover descriptor and DiffID mismatch, explicit and opaque whiteouts, same-layer scope, symlink and hardlink escape, traversal aliases, special files, entry and byte budgets, confinement, and teardown.",
        rollback_or_recovery="Abort the disposable model, retain every rejected fixture, remove only the verified owner-local scratch root, and never pull, unpack, execute, or certify a real image.",
        protected_gates=["network_pull", "real_image", "host_filesystem", "destructive_filesystem", "production", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="Prior integrity work covers ZIP, deterministic archives, TUF, Git objects, caches, and manifests; no frozen core title centers OCI ordered layer changesets, DiffIDs, whiteouts, opaque directories, link targets, and extraction budgets.",
    ),
    proposal(
        8,
        title="Accessible reversible-submission, error-checking, confirmation, undo-announcement, and focus-restoration structural audit",
        mission_surface="submission purpose, legal financial or data effect marker, reversible state, review and confirm step, input error association, undo control, status announcement, expiry disclosure, focus target, keyboard path, and manual reservation",
        hypothesis="A structural auditor can reject irreversible or ambiguous submission flows and broken undo or focus restoration while reserving browser, timing, assistive-technology, cognitive, language, and affected-user evaluation.",
        null_or_failure="A consequential action lacks reversal, checking, or confirmation; errors are unassociated; undo is silent or expired without notice; focus is lost; or structural evidence becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S17", "V6472-S18"],
        concrete_artifacts=["accessibility/reversible-action-contract.json", "accessibility/reversible-action-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must reject absent reversal/check/confirmation, ambiguous consequence, detached errors, inaccessible undo, missing announcement, undisclosed expiry, lost focus, and complete-conformance promotion.",
        rollback_or_recovery="Restore semantic review, error, undo, status, and focus structures; retain failed fixtures; and reserve manual keyboard, timing, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
        protected_gates=["manual_keyboard", "timing_review", "assistive_technology", "cognitive_accessibility", "maori_language", "affected_user", "complete_conformance"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="Prior accessibility audits cover forms, authentication, dialogs, live regions, popovers, dragging, carousels, charts, long-form documents, and timeouts; no frozen title centers reversible consequential submissions plus undo announcement and focus restoration.",
    ),
    proposal(
        9,
        title="Thermo/Psyche Ruppeiner entropy-Hessian, metric-signature, coordinate-domain, curvature-singularity, and psyche-nonconversion classifier",
        mission_surface="equilibrium state space, extensive coordinates, entropy representation, Hessian sign convention, metric signature, determinant, coordinate transformation, curvature, singular domain, critical interpretation, units, and nonconversion",
        hypothesis="A typed classifier can preserve Ruppeiner-geometry assumptions and reject singular, dimensionally inconsistent, or cross-domain uses without converting thermodynamic geometry into psyche, autonomy, justice, capability, consciousness, or a fundamental law of mind.",
        null_or_failure="Entropy and energy representations are mixed, sign or units drift, a singular Hessian is inverted, coordinate changes alter a scalar claim, curvature interpretation is universalized, or thermodynamic geometry becomes psyche evidence.",
        approval_class="safe_now_formal_domain_classifier",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S19"],
        concrete_artifacts=["thermo-psyche/ruppeiner-contract.json", "thermo-psyche/ruppeiner-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must reject absent equilibrium scope, representation drift, wrong sign, unit mismatch, singular inversion, coordinate inconsistency, universal curvature claims, and every psyche or personhood conversion.",
        rollback_or_recovery="Restore equilibrium, representation, coordinate, signature, determinant, unit, and interpretation boundaries; retain failed vectors; and keep psyche and participant claims outside the thermodynamic type.",
        protected_gates=["empirical_thermodynamics", "critical_point_claim", "psyche_law", "participant_evidence", "consciousness", "personhood"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="The corpus includes Onsager, Hatano-Sasa, Jarzynski, Crooks, Gibbs-Duhem, Gibbs phase rule, Maxwell, Clausius-Clapeyron, Le Chatelier, and other domain guards; no frozen title centers Ruppeiner entropy-Hessian geometry and curvature singularities.",
    ),
    proposal(
        10,
        title="Stage 20 Bayesian model-comparison, prior-odds, marginal-likelihood-estimator, calibration, sensitivity, and nonpromotion board",
        mission_surface="model set, prior model odds, parameter priors, marginal likelihood, estimator identity, numerical uncertainty, calibration fixture, sensitivity range, posterior model probability, decision threshold, deviation history, and terminal abstention",
        hypothesis="A structural board can require declared Bayesian model-comparison inputs, estimator uncertainty, calibration, and sensitivity while preventing synthetic Bayes factors or posterior model probabilities from promoting empirical, THOS, or Stage 20 claims.",
        null_or_failure="Prior odds are hidden, marginal likelihood and posterior density are conflated, estimator uncertainty is absent, thresholds change after results, calibration failure is suppressed, or synthetic model odds become empirical confirmation or Stage 20 promotion.",
        approval_class="safe_now_structural_nonpromotion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6472-S20", "V6472-S21"],
        concrete_artifacts=["stage20/bayesian-model-comparison-contract.json", "stage20/bayesian-model-comparison-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve model set, prior odds, parameter priors, estimator identity, uncertainty, calibration, sensitivity, threshold, deviations, and terminal abstention, rejecting every unearned evidential or promotional interpretation.",
        rollback_or_recovery="Withdraw comparison and promotion credit, retain failed calibration and sensitivity vectors, require preregistered real data and models plus validated computation and independent review, and keep Stage 20 not ready.",
        protected_gates=["real_data", "model_adequacy", "validated_likelihood", "independent_review", "stage20", "deployment", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_480_frozen_proposals="Prior Stage 20 boards cover missingness, estimands, controls, HARKing, multiverses, optional stopping, e-values, calibration, contamination, and selective reporting; no frozen title centers Bayesian model comparison, prior odds, marginal-likelihood estimators, and sensitivity.",
    ),
]


SOURCES = [
    {"source_id":"V6472-S01","title":"about_Redirection","url":"https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"stdout stderr and native byte-stream boundary context"},
    {"source_id":"V6472-S02","title":"Python subprocess documentation","url":"https://docs.python.org/3/library/subprocess.html","publisher":"Python Software Foundation","status":"current","source_class":"official_documentation","use":"argument, working-directory, environment, stream, timeout, and exit-status vocabulary"},
    {"source_id":"V6472-S03","title":"Gauge Algebra and Quantization","url":"https://doi.org/10.1016/0370-2693(81)90205-7","publisher":"Physics Letters B","status":"stable","source_class":"primary_research","use":"BV generating equation and gauge-algebra provenance"},
    {"source_id":"V6472-S04","title":"The Antifield-BRST Formalism for Gauge Theories","url":"https://arxiv.org/abs/hep-th/9412228","publisher":"Physics Reports / arXiv","status":"stable","source_class":"primary_review","use":"antifield, antibracket, master-equation, and gauge-fixing obligation context"},
    {"source_id":"V6472-S05","title":"KiDS-1000 Weak Lensing data","url":"https://kids.strw.leidenuniv.nl/DR4/lensing.php","publisher":"KiDS Collaboration","status":"current","source_class":"official_data_release_description","use":"zero-row catalogue, data-vector, covariance, and release obligations only"},
    {"source_id":"V6472-S06","title":"KiDS DR4 data access and DR4.1 correction notice","url":"https://kids.strw.leidenuniv.nl/DR4/access.php","publisher":"KiDS Collaboration","status":"watch","source_class":"official_data_release_description","use":"release supersession, archive, mask, and metadata obligations only; no rows imported"},
    {"source_id":"V6472-S07","title":"Possession of a running line for engineering work","url":"https://www.rssb.co.uk/standards-catalogue/CatalogueItem/GERT8000-T3-Iss-9","publisher":"Rail Safety and Standards Board","status":"watch","source_class":"official_withdrawn_rulebook_record","use":"historical possession and worksite vocabulary only; withdrawn status prevents operational use"},
    {"source_id":"V6472-S08","title":"Rail safety regulatory role","url":"https://www.nzta.govt.nz/about-us/who-we-are/our-purpose/regulatory/what-we-regulate/rail-safety","publisher":"NZ Transport Agency Waka Kotahi","status":"current","source_class":"official_regulator_guidance","use":"regulatory and operator authority reservation"},
    {"source_id":"V6472-S09","title":"Rail occurrence severity rating examples","url":"https://www.nzta.govt.nz/roads-and-rail/rail/operating-a-railway/notifying-accidents-and-incidents/rail-occurrence-severity-ratings/occurrence-severity-rating-examples/","publisher":"NZ Transport Agency Waka Kotahi","status":"current","source_class":"official_regulator_guidance","use":"protection, blocking, clearance, and reporting context only; not case authority"},
    {"source_id":"V6472-S10","title":"Web Authentication Level 3","url":"https://www.w3.org/TR/webauthn-3/","publisher":"W3C","status":"draft","source_class":"official_candidate_recommendation","use":"RP ID, origin, challenge, flags, attestation, backup, and privacy obligations"},
    {"source_id":"V6472-S11","title":"Client to Authenticator Protocol","url":"https://fidoalliance.org/specs/fido-v2.2-rd-20241003/","publisher":"FIDO Alliance","status":"draft","source_class":"official_specification","use":"synthetic authenticator encoding and ceremony context only"},
    {"source_id":"V6472-S12","title":"Privacy principles","url":"https://www.privacy.org.nz/privacy-principles/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_guidance","use":"personal and location information boundary; no legal interpretation"},
    {"source_id":"V6472-S13","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6472-S14","title":"Web Content Accessibility Guidelines 2.2","url":"https://www.w3.org/TR/WCAG22/","publisher":"W3C","status":"current","source_class":"official_standard","use":"accessibility obligations and complete-conformance reservation"},
    {"source_id":"V6472-S15","title":"OCI Image Layer Specification","url":"https://specs.opencontainers.org/image-spec/layer/","publisher":"Open Container Initiative","status":"current","source_class":"official_specification","use":"ordered changeset, whiteout, opaque-directory, and file-type obligations"},
    {"source_id":"V6472-S16","title":"OCI Image Manifest Specification","url":"https://specs.opencontainers.org/image-spec/manifest/","publisher":"Open Container Initiative","status":"current","source_class":"official_specification","use":"descriptor, digest, size, media type, and layer-order obligations"},
    {"source_id":"V6472-S17","title":"WCAG 2.2 Error Prevention","url":"https://www.w3.org/TR/WCAG22/#error-prevention-legal-financial-data","publisher":"W3C","status":"current","source_class":"official_standard","use":"reversible, checked, and confirmed submission alternatives"},
    {"source_id":"V6472-S18","title":"ARIA live regions","url":"https://www.w3.org/WAI/ARIA/apg/practices/live-regions/","publisher":"W3C WAI","status":"current","source_class":"official_practice_guidance","use":"status-announcement structure only; manual assistive-technology evaluation reserved"},
    {"source_id":"V6472-S19","title":"Thermodynamics: A Riemannian geometric model","url":"https://doi.org/10.1103/PhysRevA.20.1608","publisher":"Physical Review A","status":"stable","source_class":"primary_research","use":"entropy-Hessian metric and curvature-domain provenance"},
    {"source_id":"V6472-S20","title":"Bayes Factors","url":"https://doi.org/10.1080/01621459.1995.10476572","publisher":"Journal of the American Statistical Association","status":"stable","source_class":"primary_review","use":"Bayes-factor, prior-odds, calibration, and interpretation boundaries"},
    {"source_id":"V6472-S21","title":"Registered Reports","url":"https://www.cos.io/initiatives/registered-reports","publisher":"Center for Open Science","status":"current","source_class":"authoritative_practice_guidance","use":"prospective review, deviations, and nonpromotion context only"},
]


SAFE_TASK_TITLES = [
    "Verify Sable final source and all four declared anchors before mutation",
    "Verify exact 35-entry source postcommit manifest parity",
    "Fast-forward only the clean Orin canonical lane and prove four-way equality",
    "Reconcile all 480 frozen proposal titles before novelty credit",
    "Quarantine the railway speed-restriction semantic neighbor from possession scope",
    "Review current stable draft and watch source statuses",
    "Record source supersession and withdrawn-rulebook nonoperational status",
    "Declare commit-blob index and working-tree hash domains",
    "Separate privacy scanner definitions from payload incidents",
    "Measure inherited checkout and owner-generated footprints separately",
    "Initialize Method Flow with every startup failure retained",
    "Build UTF-8 command-stream and exit-credit fixture contract",
    "Build BV master-equation typed obligation fixture contract",
    "Build KiDS-1000 zero-row receipt schema",
    "Build rail-possession handover trace schema",
    "Build WebAuthn synthetic ceremony-context schema",
    "Build rail-remedy authority reservation matrix schema",
    "Build OCI layer disposable-fixture contract",
    "Build reversible-action accessibility fixture",
    "Build Ruppeiner typed-domain fixture",
    "Build Bayesian model-comparison nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 18 open gaps and 19 exact gates",
    "Carry forward the 3235-negative activation baseline",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Verify Codex versions without updating desktop",
    "Probe Windows Sandbox capability without elevation or feature change",
    "Audit family-current callers and historical compatibility aliases",
    "Freeze exact x1 staged surface with no x2 implementation",
    "Emit owner-scoped x1 wellbeing source and route receipts",
]

CANDIDATE_TITLES = [
    "Command UTF-8 partial-record and delimiter refusal prototype",
    "Command channel-order truncation and exit-credit prototype",
    "BV parity ghost-number and antibracket-sign mutation prototype",
    "BV master-equation gauge-fixing and truncation-scope prototype",
    "KiDS release-supersession and checksum lock prototype",
    "KiDS calibration covariance scale-cut and zero-row lock prototype",
    "Rail possession-boundary protection and premature-release replay prototype",
    "Rail overrun clearance conflict and handover-readback prototype",
    "WebAuthn RP-ID origin challenge and ceremony-type prototype",
    "WebAuthn flags backup attestation and privacy prototype",
    "Rail reporting accessibility confidentiality and location matrix prototype",
    "Rail remedy affected-party and Māori-authority reservation prototype",
    "OCI digest DiffID and ordered-whiteout mutation prototype",
    "OCI link traversal special-file and extraction-budget prototype",
    "Reversible submission review error and confirmation checker",
    "Undo announcement expiry and focus-restoration classifier",
    "Ruppeiner representation signature and singular-Hessian prototype",
    "Ruppeiner coordinate curvature and psyche-nonconversion prototype",
    "Bayesian prior-odds and marginal-likelihood-estimator prototype",
    "Bayesian calibration sensitivity threshold and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-command-stream-tribunal", "Audit UTF-8 records channel separation truncation timeout and exit credit"),
    ("ghc-family-bv-master-equation-obligations", "Audit BV grading master equation gauge fixing and truncation obligations"),
    ("ghc-family-kids1000-zero-row", "Preserve a zero-row KiDS-1000 weak-lensing study boundary"),
    ("ghc-family-rail-possession-handover-proxy", "Audit synthetic rail possession protection release and handover traces"),
    ("ghc-family-webauthn-context-profile", "Audit synthetic WebAuthn ceremony context flags and privacy"),
    ("ghc-family-rail-remedy-authority-reservation", "Reserve rail reporting accessibility privacy remedy and Māori authority gates"),
    ("ghc-family-oci-layer-tribunal", "Audit synthetic OCI digest whiteout link and budget fixtures"),
    ("ghc-family-reversible-action-accessibility", "Audit reversible submission undo announcement and focus structure"),
    ("ghc-family-ruppeiner-domain", "Keep entropy-Hessian geometry inside thermodynamic domains"),
    ("ghc-family-bayesian-model-comparison-nonpromotion", "Guard model odds marginal likelihoods and sensitivity from automatic promotion"),
    ("ghc-family-corpus-480-collision-gate", "Audit exact and semantic novelty against 480 frozen proposals"),
    ("ghc-family-source-supersession-watch", "Record superseded withdrawn draft and current source status without promotion"),
    ("ghc-family-command-stream-boundary", "Keep stdout stderr timeout and exit semantics distinct"),
    ("ghc-family-named-replay-locality", "Verify a named replay remains local clean unpushed and without upstream"),
    ("ghc-family-commit-cap-single-parent", "Verify phase commit cap zero merges and single-parent closeout"),
    ("ghc-family-five-class-privacy-adjudication", "Separate scanner definitions candidates incidents and payload hits"),
    ("ghc-family-manifest-self-exclusion-v2", "Audit exact staged manifests with declared self-exclusions"),
    ("ghc-family-stage-label-lifecycle-lint", "Reject stale candidate prepared and sent lifecycle labels"),
    ("ghc-family-authority-reservation-matrix", "Prevent software evidence from compensating for authority gaps"),
    ("ghc-family-baton-ack-one-shot", "Count one existing-task baton only after acknowledged send"),
]

RUNNER_TITLES = [
    "ghc_family_command_stream_tribunal.py",
    "ghc_family_bv_master_equation_obligations.py",
    "ghc_family_kids1000_zero_row.py",
    "ghc_family_rail_possession_handover.py",
    "ghc_family_webauthn_context_profile.py",
    "ghc_family_oci_layer_tribunal.py",
    "ghc_family_reversible_action_audit.py",
    "ghc_family_ruppeiner_domain.py",
    "ghc_family_bayesian_model_comparison_board.py",
    "ghc_family_v647_v2_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across receipts",
    "Reconcile inherited synthetic and operational negatives",
    "Synchronize Method Flow counts and validator expectations",
    "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep commit-blob index and working-tree hash domains explicit",
    "Review public files for private absolute paths",
    "Review public files for raw task or thread identifiers",
    "Review public files for credential token or private-key assignments",
    "Review source statuses for allowed vocabulary",
    "Review superseded and withdrawn sources for nonoperational use",
    "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15000-file threshold",
    "Review reversible-action report structure and manual reservations",
    "Review report manual assistive-technology and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review rail-safety professional operational and legal reservations",
    "Review real-data and likelihood counters remain zero",
    "Review real-worker infrastructure possession and movement counters remain zero",
    "Review real-key account authenticator and ceremony counters remain zero",
    "Review source and all phase-anchor ancestry",
    "Review phase commit cap zero merges and one final parent",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped index wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real KiDS data download likelihood or parameter inference",
    "Real railway possession protection movement or release action",
    "Real rail occurrence reporting or public-safety decision",
    "Production WebAuthn account key authenticator or ceremony operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Confidential location legal interpretation or remedy allocation",
    "Māori authority or data-governance decision",
    "Production deployment or security certification",
    "Independent-team scientific reproduction claim",
    "Stage 20 promotion proof or canon decision",
]

BLOCKED_PACKET_TITLES = [
    "Force-push rewrite or merge canonical history",
    "Delete reuse or mutate a sibling-owned lane",
    "Expose credentials private routes private state or raw task identifiers",
    "Enable Windows features weaken security elevate or install unrelated software",
    "Claim consciousness personhood AGI ASI or Theory-of-Everything closure",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id":"V6472-X1-N01","method_id":"V6472-M01","summary":"The first worktree inventory ran git worktree list from the nonrepository Codex settings directory and returned not a git repository before any repository mutation.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N02","method_id":"V6472-M02","summary":"The first frozen-index probe assumed proposals and phase fields; the current source index uses prior_proposals and the probe returned an empty projection before its schema was inspected.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N03","method_id":"V6472-M03","summary":"The first combined official-source search returned WebAuthn OCI and rail sources but missed KiDS; a bounded KiDS-specific search found the official release pages.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N04","method_id":"V6472-M04","summary":"The successful fast-forward emitted an overlarge change inventory that was truncated by the tool display; exact post-operation Git hashes and remote equality remained available and passed.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N05","method_id":"V6472-M05","summary":"The read-only Windows Sandbox feature query required elevation and returned no feature state; no elevation or feature change was attempted and Sandbox remained unavailable to this process.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N06","method_id":"V6472-M06","summary":"The first preregistration-adapter orchestration embedded an apostrophe in a single-quoted JavaScript replacement and was rejected by the JavaScript parser before any nested tool or file edit ran.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N07","method_id":"V6472-M07","summary":"The second adapter attempt assumed TextDecoder existed in the orchestration isolate; it failed before apply_patch, and the recovered path used the shell tool's UTF-8 text result directly.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N08","method_id":"V6472-M08","summary":"The first generated Method Flow records retained a stale Sable owner label in their scope boundary; validation exposed it before x1 staging, and the owner-generated ledger was rebuilt after correcting the authoritative builder.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N09","method_id":"V6472-M09","summary":"The first exact staged x1 review rejected two adapted validator files for extra blank lines at end of file; zero privacy or x1-contamination hits occurred, and the same staged surface was retried only after the whitespace fix was retained.","retained":True,"recovered":True},
    {"negative_id":"V6472-X1-N10","method_id":"V6472-M09","summary":"The second exact staged x1 review found that the preserved N09 failure receipt itself retained an extra terminal blank line; the receipt stayed preserved, its whitespace alone was corrected, and the same exact surface was retried.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6472-M01","title":"Resolve a real repository root before worktree inventory","failure_signature":"git worktree list was invoked from a nonrepository settings directory.",
        "trigger_preconditions":["A task starts in a project settings directory rather than a checked-out repository."],
        "candidate_workaround":"Enumerate the bounded D-drive worktree bank first and run Git only with an explicit verified repository path.",
        "recurrence_guard":"Never infer repository status from the process cwd; pass -C with the exact owner or source worktree.",
        "rollback":"Discard the failed read-only probe; no repository mutation occurred.",
        "protected_gates":["owned_lane_only","no_sibling_mutation","no_destructive_git"],
        "retained_negative_ids":["V6472-X1-N01"],
        "failed_observed":"Git reported that the Codex settings directory was not a repository.",
        "pass_observed":"Explicit source and Orin worktree paths returned exact branches, heads, clean state, ancestry, and remote equality.",
    },
    {
        "method_id":"V6472-M02","title":"Inspect proposal-index schema before selecting rows","failure_signature":"A frozen-index projection selected nonexistent proposals and phase fields.",
        "trigger_preconditions":["Family phases may preserve different proposal-index schemas."],
        "candidate_workaround":"Read top-level keys, select prior_proposals, then append the current source x1 proposals explicitly.",
        "recurrence_guard":"Require the declared count and actual array count to match before semantic-neighbor analysis.",
        "rollback":"Discard the empty projection; no file mutation occurred.",
        "protected_gates":["proposal_novelty","historical_compatibility","no_completion_credit"],
        "retained_negative_ids":["V6472-X1-N02"],
        "failed_observed":"The first projection returned no proposal rows.",
        "pass_observed":"Schema-aware reconciliation found 470 prior rows plus ten Sable x1 rows for the exact 480-title corpus.",
    },
    {
        "method_id":"V6472-M03","title":"Split official-source discovery by evidence surface","failure_signature":"A broad four-topic query omitted the KiDS source surface.",
        "trigger_preconditions":["A combined source query spans unrelated scientific, standards, and practice domains."],
        "candidate_workaround":"Use bounded domain-specific official-source queries and retain zero-result or omitted surfaces.",
        "recurrence_guard":"Require at least one directly reviewed official or primary source per material surface before freezing source IDs.",
        "rollback":"Retain the incomplete search as a negative and do not infer absence from it.",
        "protected_gates":["primary_sources","no_citation_as_observation","no_authority_substitution"],
        "retained_negative_ids":["V6472-X1-N03"],
        "failed_observed":"The first result set had no KiDS release page.",
        "pass_observed":"A KiDS-specific search found the official weak-lensing, release-correction, and access pages without downloading data.",
    },
    {
        "method_id":"V6472-M04","title":"Use quiet fast-forward output and independent exact-hash proofs","failure_signature":"A valid fast-forward printed thousands of path changes and the display truncated the inventory.",
        "trigger_preconditions":["A sequential branch advances across multiple artifact-heavy phases."],
        "candidate_workaround":"Use quiet fast-forward where supported, then prove head, upstream, tracking, live remote, clean state, commit count, and merge count separately.",
        "recurrence_guard":"Treat verbose path output as nonauthoritative; exact Git hashes and status are the authoritative witness.",
        "rollback":"No rollback; the fast-forward and push were valid, and exact proofs confirmed the intended head.",
        "protected_gates":["fast_forward_only","exact_head","remote_equality","no_merge"],
        "retained_negative_ids":["V6472-X1-N04"],
        "failed_observed":"The tool display truncated the verbose path inventory.",
        "pass_observed":"Local, upstream, tracking, and fresh live remote all equalled the exact Sable final head with a clean Orin lane.",
    },
    {
        "method_id":"V6472-M05","title":"Treat elevation-required Sandbox probes as unavailable","failure_signature":"The read-only Windows optional-feature query required elevation.",
        "trigger_preconditions":["Sandbox feature state cannot be read by the ordinary process."],
        "candidate_workaround":"Record capability as unavailable to the current process and do not elevate, enable features, weaken security, or reboot.",
        "recurrence_guard":"Never retry the feature query with elevation inside a family phase.",
        "rollback":"No system mutation occurred; retain the error and continue with bounded owner-local fixtures.",
        "protected_gates":["no_elevation","no_feature_change","no_security_weakening","no_reboot"],
        "retained_negative_ids":["V6472-X1-N05"],
        "failed_observed":"The host returned requested operation requires elevation.",
        "pass_observed":"The phase recorded Sandbox unavailable and performed no elevation, feature change, install, or reboot.",
    },
    {
        "method_id":"V6472-M06","title":"Keep JavaScript replacement strings quote-safe","failure_signature":"A single-quoted JavaScript replacement contained an unescaped apostrophe.",
        "trigger_preconditions":["An orchestration cell transforms prose containing possessives or quoted names."],
        "candidate_workaround":"Use double-quoted JavaScript literals or template strings for replacement text containing apostrophes.",
        "recurrence_guard":"Parse the orchestration source before allowing any nested edit call and avoid mixed quote ownership.",
        "rollback":"Discard the parser-rejected cell; no nested command or file edit ran.",
        "protected_gates":["atomic_edit","no_partial_generation","x1_only"],
        "retained_negative_ids":["V6472-X1-N06"],
        "failed_observed":"The JavaScript parser reported a missing parenthesis before nested execution.",
        "pass_observed":"The corrected replacement used quote-safe literals and reached the bounded source-extraction step.",
    },
    {
        "method_id":"V6472-M07","title":"Use available UTF-8 text transport in the orchestration isolate","failure_signature":"TextDecoder was not defined in the isolate.",
        "trigger_preconditions":["A local source file must be transformed and installed through apply_patch."],
        "candidate_workaround":"Ask the shell tool for UTF-8 text, isolate its Output section, normalize line endings, and pass the transformed content to apply_patch.",
        "recurrence_guard":"Do not assume browser encoding globals exist in the orchestration isolate.",
        "rollback":"Discard the failed in-memory transform; no apply_patch call occurred.",
        "protected_gates":["utf8_integrity","apply_patch_only","no_partial_generation"],
        "retained_negative_ids":["V6472-X1-N07"],
        "failed_observed":"The isolate raised ReferenceError before decoding or editing.",
        "pass_observed":"Direct UTF-8 shell text extraction plus apply_patch created the adapted x1 scripts without mojibake.",
    },
    {
        "method_id":"V6472-M08","title":"Validate owner labels before sealing Method Flow","failure_signature":"Generated method scope boundaries named the source owner instead of the active owner.",
        "trigger_preconditions":["A phase builder is adapted from a prior owner's compatible implementation."],
        "candidate_workaround":"Scan owner, phase, route, and boundary labels before staging; fix the authoritative builder and regenerate only owner-scoped precommit artifacts.",
        "recurrence_guard":"Require every Method Flow scope boundary to begin with Orin v647-v2 before ledger validation and x1 staging.",
        "rollback":"Discard the uncommitted owner-generated ledger, keep this failed witness, regenerate from the corrected builder, and rerun the family Method Flow runner.",
        "protected_gates":["owner_scope","identity_boundary","no_history_rewrite","x1_only"],
        "retained_negative_ids":["V6472-X1-N08"],
        "failed_observed":"The first preferred-method summary displayed Sable v647-v2 in every scope boundary.",
        "pass_observed":"The corrected builder and rebuilt ledger display Orin v647-v2 for all method scope boundaries and validate cleanly.",
    },
    {
        "method_id":"V6472-M09","title":"Run staged diff hygiene before fixed-point manifest credit","failure_signature":"git diff --cached --check found extra blank lines at EOF in two adapted validators.",
        "trigger_preconditions":["New validators are created through compatibility-preserving text adaptation."],
        "candidate_workaround":"Remove only the surplus terminal blank lines, retain the failed staged receipt, restage the exact same owned surface, and rerun the reviewer.",
        "recurrence_guard":"Require diff hygiene to pass before manifest fixed-point or x1 commit credit.",
        "rollback":"Keep all substantive staged content, withdraw the failed review's pass credit, and apply only the bounded whitespace correction.",
        "protected_gates":["diff_hygiene","exact_staged_surface","x1_only","no_history_rewrite"],
        "retained_negative_ids":["V6472-X1-N09", "V6472-X1-N10"],
        "failed_observed":"The first reviewer found two adapted validators with surplus EOF whitespace; the second found the preserved first-failure receipt had the same bounded whitespace defect.",
        "pass_observed":"The corrected exact staged surface passed diff hygiene with unchanged proposal, gate, and privacy content.",
    },
]
