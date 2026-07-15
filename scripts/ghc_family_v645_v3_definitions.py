#!/usr/bin/env python3
"""Frozen Eiren Kestrel v645-v3 x1 definitions.

The ten research proposals are the scientific spine.  The larger approval,
skill, runner, and maintenance portfolios are parallel preregistration ledgers;
they do not silently change a research proposal's disposition.
"""

from __future__ import annotations


IDENTITY_BOUNDARY = (
    "Relational working language only; not evidence of consciousness, sentience, "
    "legal personhood, identity continuity, employment, or independent authority."
)

TRUTH_BOUNDARY = (
    "Software and synthetic fixtures can establish only bounded structural behavior. "
    "They do not establish empirical GMUT confirmation, THOS effectiveness, production "
    "identity assurance, legal or cultural authority, independent reproduction, AGI/ASI, "
    "complete accessibility, exhaustive security, or Stage 20 readiness."
)


def proposal(pid: str, title: str, surface: str, hypothesis: str, failure: str,
             approval: str, lane: str, sources: list[str], deliverables: list[str],
             gate: str, recovery: str, protected: list[str], disposition: str,
             novelty: str) -> dict:
    return {
        "proposal_id": pid,
        "title": title,
        "mission_surface": surface,
        "hypothesis": hypothesis,
        "null_or_failure": failure,
        "approval_class": approval,
        "execution_lane": lane,
        "authoritative_source_needs": sources,
        "deliverables": deliverables,
        "test_falsifier_or_gate": gate,
        "rollback_or_recovery": recovery,
        "protected_gates": protected,
        "expected_disposition": disposition,
        "novelty_against_prior_chain": novelty,
    }


PROPOSALS = [
    proposal(
        "V6453-P01",
        "Method Flow causal-incident graph, counterfactual workaround, and retry-quarantine ledger",
        "Method Flow State, causal edge, sanitized failure signature, counterfactual workaround, witness, retry quarantine, recurrence guard, rollback, and sibling recommendation",
        "An append-only incident graph can preserve each operational negative, distinguish observed causes from hypotheses, test a bounded counterfactual workaround, and quarantine repeated retries without treating recovery as independent evidence.",
        "A causal edge is asserted without a witness, a failed attempt is erased, a workaround is promoted without a passing bounded test, retry quarantine is bypassed, or same-owner recovery is called independent reproduction.",
        "safe_now_structural_only", "x2_build_task", [],
        ["method-flow/causal-incident-contract.json", "method-flow/retry-quarantine-vectors.json", "method-flow/method-flow-state.json"],
        "Mutation cases must reject missing negative links, circular unsupported causes, state promotion without a pass, retry after quarantine, absent rollback, and unbounded recommendations.",
        "Return the method to observed or candidate, retain every event and failed witness, quarantine the signature, and require a new precondition before retry.",
        ["history_rewrite", "private_material", "sibling_authority", "independent_team_reproduction"],
        "completed",
        "No prior frozen title combines a causal incident graph, a counterfactual workaround witness, and retry quarantine; the 330-title audit found no causal-incident or retry-quarantine match.",
    ),
    proposal(
        "V6453-P02",
        "GMUT redundant EFT operator, integration-by-parts, and field-redefinition quotient tribunal",
        "GMUT Mind, typed scalar-tensor EFT, operator basis, integration by parts, equations of motion, field redefinition, perturbative order, S-matrix boundary, units, and nonpromotion",
        "A symbolic structural tribunal can reject a claimed independent GMUT operator basis when redundant operators are not quotiented consistently by integration by parts, equations of motion, and perturbative field redefinitions.",
        "Equivalent representatives are double counted, a field redefinition is used beyond its perturbative order, boundary terms are omitted, dimensions mismatch, or Lagrangian-form equivalence is misreported as an empirical or S-matrix result.",
        "safe_now_research_scaffold", "x2_build_task", ["V6453-S01", "V6453-S02"],
        ["physics/eft-quotient-contract.json", "physics/eft-redundancy-vectors.json", "physics/eft-nonpromotion-boundary.json"],
        "Mutate dimensions, total derivatives, equation-of-motion use, invertibility, perturbative order, and observable language; invalid quotient steps must fail closed.",
        "Restore the last typed representative set, retain rejected reductions, and require a model-specific calculation and observation before stronger claims.",
        ["empirical_gmut_claim", "unique_prediction", "theory_of_everything", "proof_canon"],
        "completed",
        "Earlier phases tested Noether identities, hyperbolicity, characteristics, Ostrogradsky stability, and positivity. None centered an explicit operator quotient under integration by parts, equations of motion, and field redefinitions.",
    ),
    proposal(
        "V6453-P03",
        "GMUT satellite-laser-ranging frame-dragging nodal-residual blind public-data protocol",
        "GMUT Mind, ILRS normal points, CRD lineage, satellite orbit model, nodal residual, frame dragging, covariance, gravity model, withheld labels, baseline, real rows, and independent review",
        "A preregistered adapter could test a frozen frame-dragging residual only after official SLR observations, station and CRD provenance, orbit and gravity models, covariance, exclusions, a baseline, blind holdout, and independent review are present.",
        "Zero real rows are ingested, station or format lineage is absent, model choices are tuned after inspection, covariance is missing, non-gravitomagnetic effects are ignored, or synthetic data are reported as a measurement.",
        "safe_now_protocol_only_real_data_required", "x2_open_gap", ["V6453-S03", "V6453-S04", "V6453-S05"],
        ["empirical/slr-frame-dragging-study-contract.json", "empirical/slr-adapter-readiness.json", "empirical/slr-open-gap.json"],
        "Require nonzero official observations and complete provenance, frozen force and gravity models, covariance, exclusions, baseline, blind holdout, and independent review; absence keeps the study open.",
        "Retain zero-row receipts, run no fit, report no frame-dragging constraint, and reopen only under a separately reviewed real-data protocol.",
        ["real_data_download", "empirical_gmut_claim", "likelihood_result", "independent_review", "account_or_api_key"],
        "open_gap",
        "The prior chain covers many cosmology and gravitational-wave adapters but no ILRS satellite-laser-ranging nodal-residual protocol for frame dragging.",
    ),
    proposal(
        "V6453-P04",
        "THOS geodetic station-log discontinuity, reference-frame change-control, and shift-handover proxy",
        "THOS Body, geodetic observatory operations, station log, equipment or monument discontinuity, reference frame, change control, unresolved state, matched information budget, synthetic handover, and independent review",
        "A synthetic THOS handover can preserve station discontinuities, equipment changes, effective epochs, reference-frame consequences, unresolved anomalies, ownership, and acceptance under matched information budgets.",
        "A discontinuity disappears, an epoch is changed silently, equipment lineage is lost, unresolved state is marked closed, shifts receive unequal evidence, or proxy scores are called real observatory effectiveness.",
        "safe_now_proxy_only", "x2_proxy_task", ["V6453-S05", "V6453-S06"],
        ["thos/station-handover-contract.json", "thos/station-discontinuity-vectors.json", "thos/real-observatory-reservation.json"],
        "Mutate station, equipment, monument, epoch, frame, anomaly, owner, acceptance, matched budget, and claim language; lost or unauthorized state must reject.",
        "Restore the frozen synthetic log, retain failed vectors, and require competent observatory authority, real arms, worker safeguards, and independent review for effectiveness claims.",
        ["real_workers", "operational_authority", "effectiveness_claim", "independent_review", "deployment"],
        "represented",
        "Earlier THOS work covers alarm handover but not geodetic station-log discontinuities, effective epochs, and reference-frame change control.",
    ),
    proposal(
        "V6453-P05",
        "Freed ID deferred credential transaction, notification, replay, and expiry state-machine profile",
        "Freed ID Heart, OpenID4VCI 1.0, deferred issuance, transaction identifier, access token boundary, notification identifier, idempotency, replay, expiry, synthetic wallet, and production reservation",
        "A synthetic state machine can reject malformed or replayed deferred-issuance and notification transitions while preserving the final OpenID4VCI protocol boundaries and reserving real cryptography and interoperability.",
        "An unknown or consumed transaction succeeds, polling ignores interval or expiry, notification replay changes state non-idempotently, tokens cross scope, or synthetic fixtures are called production identity assurance.",
        "safe_now_synthetic_identity_profile", "x2_proxy_task", ["V6453-S07"],
        ["freed-id/deferred-issuance-profile.json", "freed-id/deferred-notification-vectors.json", "freed-id/production-issuance-reservation.json"],
        "Mutate transaction state, token scope, polling interval, expiry, notification ID, event, replay count, and result language; invalid transitions must reject deterministically.",
        "Return to the last valid synthetic state, retain rejected transitions, expose no real credentials, and require standards-conformant keys, live interoperability, privacy and security review, and trust governance for production.",
        ["real_keys", "production_identity", "interoperability", "privacy_assurance", "independent_security_review", "trust_governance"],
        "represented",
        "Prior phases cover OpenID4VCI nonce and proof-of-possession plus DCQL. None joins deferred transaction lifecycle, notification idempotency, replay, and expiry under the final 1.0 specification.",
    ),
    proposal(
        "V6453-P06",
        "CBR geodetic-datum migration, cadastral nonconversion, affected-holder remedy, and Maori-authority gate",
        "CBR Heart, NZGD2000, coordinate transformation, cadastral boundary, reference epoch, affected landholder, survey authority, remedy, privacy, legal interpretation, Maori authority, data governance, and cultural legitimacy",
        "A refusal-first authority matrix can prevent software from converting geodetic-coordinate guidance into a cadastral-boundary or rights decision without competent survey and legal authority, affected-holder participation, privacy governance, and Maori authority where relevant.",
        "A coordinate transform is treated as title evidence, boundary rights are inferred, an affected holder is omitted, private location data are exposed, consultation substitutes for authority, or Maori concepts are treated as software-owned.",
        "exact_authority_gate", "x2_exact_gate", ["V6453-S08", "V6453-S09", "V6453-S10"],
        ["cbr/datum-migration-authority-matrix.json", "cbr/cadastral-refusal-cases.json", "cbr/geodetic-authority-reservation.md"],
        "Every boundary, title, remedy, private-location, Maori wording, data-governance, legitimacy, or legal conclusion must remain refused without exact competent and affected-party authority.",
        "Return the matter to unknown and exact-gated, retain the refusal, expose no real location data, and route it to competent survey, legal, privacy, affected-holder, and Maori authorities.",
        ["property_rights", "legal_interpretation", "affected_party_acceptance", "maori_authority", "maori_data_governance", "location_privacy", "cultural_ratification"],
        "exact_gate",
        "The prior chain has Maori data-sovereignty gates but no joined datum-migration, cadastral nonconversion, affected-landholder, privacy, remedy, and Maori-authority boundary.",
    ),
    proposal(
        "V6453-P07",
        "Git multi-pack-index, commit-graph, and reachability-bitmap integrity tribunal",
        "repository integrity, Git multi-pack index, incremental chain, commit graph, reachability bitmap, verify command, object lookup, read-only fixture, rollback, and noncanonical test repository",
        "A family-compatible temporary-repository tribunal can detect malformed acceleration structures and prove that verification failures do not change canonical Git history or owner worktrees.",
        "A corrupt structure receives credit, a destructive repack touches the canonical repository, verification output is ignored, object reachability changes, or a temporary fixture is called production proof.",
        "safe_now_local_fixture_tooling", "x2_build_task", ["V6453-S11", "V6453-S12", "V6453-S13"],
        ["security/git-acceleration-contract.json", "security/git-acceleration-vectors.json", "tooling/git-acceleration-runner-receipt.json"],
        "Exercise valid, missing, malformed, stale, and mismatched acceleration fixtures in a temporary repository; canonical refs and objects must remain unchanged.",
        "Discard only the additive temporary fixture, retain failure receipts, and leave canonical object storage untouched.",
        ["canonical_object_mutation", "destructive_action", "sibling_lane", "history_rewrite", "private_material"],
        "completed",
        "Earlier repository proposals cover index stages and many Git surfaces but not the joint integrity of MIDX, commit-graph, and reachability bitmap acceleration structures.",
    ),
    proposal(
        "V6453-P08",
        "Complex geospatial map, coordinate-table, and text-alternative accessibility audit",
        "accessible static report, complex image, geospatial map, short alternative, long description, data table, coordinate reference, reading order, keyboard reachability, structural audit, and manual reservation",
        "A bounded structural audit can reject a generated geospatial report lacking equivalent map purpose, salient relationships, accessible coordinate data, headings, labels, and explicit manual and affected-user reservations.",
        "A map has only a filename alt, a long description omits relationships, a coordinate table lacks headers or reference context, visual order replaces reading order, or automation is called complete accessibility.",
        "safe_now_structural_accessibility", "x2_build_task", ["V6453-S14"],
        ["accessibility/geospatial-report-contract.json", "accessibility/complex-map-vectors.json", "validation/manual-accessibility-reservation.json"],
        "Mutate alternative text, long-description linkage, coordinate table headers, reference-system context, reading order, labels, and claim language; missing equivalence must fail.",
        "Restore the last structurally valid report, retain failures, and reserve manual and affected-user evaluation.",
        ["complete_accessibility", "affected_user_evaluation", "production_deployment"],
        "completed",
        "Prior accessibility proposals address titles, refresh, headings, landmarks, tables, and charts; none centers a complex geospatial map with coordinate-reference and equivalent data-table obligations.",
    ),
    proposal(
        "V6453-P09",
        "Jarzynski nonequilibrium-work equality and psyche-effort nonconversion classifier",
        "thermodynamics, Jarzynski equality, nonequilibrium work, free-energy difference, exponential average, sampling bias, synthetic trajectories, psyche analogy, dimensional typing, and nonconversion",
        "A typed synthetic calculator can verify the algebraic Jarzynski relation on declared fixtures while rejecting any conversion of thermodynamic work or free energy into psychological effort or spiritual truth.",
        "Units or sign conventions drift, exponential averaging is replaced by an ordinary mean, poor sampling is hidden, synthetic agreement is called an experiment, or psyche labels are treated as physical quantities.",
        "safe_now_synthetic_physics", "x2_build_task", ["V6453-S15"],
        ["thermo-psyche/jarzynski-contract.json", "thermo-psyche/jarzynski-fixtures.json", "thermo-psyche/psyche-nonconversion-boundary.json"],
        "Mutate beta, work values, free-energy sign, averaging rule, sample count, units, and psyche labels; algebraic or category errors must reject.",
        "Restore the typed synthetic fixture, retain failures, and require real physical observations for empirical thermodynamics and separate validated measures for psychology.",
        ["human_subjects", "clinical_claim", "metaphysical_proof", "empirical_thermodynamics"],
        "completed",
        "Prior thermo-psyche work covers Landauer, Onsager, fluctuation-dissipation, and exergy, but not Jarzynski nonequilibrium work with an explicit psyche-effort nonconversion boundary.",
    ),
    proposal(
        "V6453-P10",
        "Stage 20 e-value, optional-stopping, and anytime-valid promotion rejection board",
        "Stage 20 evidence governance, e-value, e-process, optional stopping, optional continuation, filtration, threshold, preregistration, sequential decision, synthetic evidence stream, and nonpromotion",
        "A synthetic evidence board can distinguish a valid nonnegative e-process rule from naive repeated testing and refuse Stage 20 promotion when the declared process, null, filtration, threshold, or external evidence is absent.",
        "A fixed-horizon score is repeatedly peeked at, the e-process condition is not checked, thresholds are selected post hoc, optional continuation is misused, or synthetic evidence is called scientific confirmation.",
        "safe_now_structural_decision_board", "x2_build_task", ["V6453-S16", "V6453-S17"],
        ["stage20/anytime-valid-contract.json", "stage20/sequential-evidence-vectors.json", "stage20/terminal-evidence-board.json"],
        "Mutate null, filtration, nonnegativity, expectation bound, stopping rule, threshold, continuation, and external-evidence status; invalid sequential promotion must reject.",
        "Return the board to NOT_READY_FOR_STAGE_20, retain failed streams, and require independently reviewed real evidence before any promotion.",
        ["empirical_confirmation", "independent_reproduction", "stage20_promotion", "proof_canon"],
        "completed",
        "Earlier boards cover evidence ladders and Goodhart divergence; none uses e-values and optional-stopping validity as the explicit sequential promotion boundary.",
    ),
]


SOURCES = [
    {"source_id": "V6453-S01", "title": "Field reparametrization in effective field theories", "url": "https://arxiv.org/abs/1610.09618", "authority": "primary research paper", "status": "stable"},
    {"source_id": "V6453-S02", "title": "Low Energy Effective Field Theory Operator Basis at d <= 9", "url": "https://arxiv.org/abs/2012.09188", "authority": "primary research paper", "status": "stable"},
    {"source_id": "V6453-S03", "title": "ILRS Data", "url": "https://ilrs.gsfc.nasa.gov/data_and_products/data/index.html", "authority": "official ILRS service", "status": "current"},
    {"source_id": "V6453-S04", "title": "ILRS Consolidated Laser Ranging Data Format", "url": "https://ilrs.gsfc.nasa.gov/data_and_products/formats/crd.html", "authority": "official ILRS service", "status": "current"},
    {"source_id": "V6453-S05", "title": "IERS Conventions Chapter 4 - Terrestrial reference systems and frames", "url": "https://iers-conventions.obspm.fr/content/chapter4/icc4.pdf", "authority": "official IERS conventions", "status": "current"},
    {"source_id": "V6453-S06", "title": "ILRS Data Centers", "url": "https://ilrs.gsfc.nasa.gov/data_and_products/data_centers/index.html", "authority": "official ILRS service", "status": "current"},
    {"source_id": "V6453-S07", "title": "OpenID for Verifiable Credential Issuance 1.0", "url": "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "authority": "OpenID Final Specification", "status": "current"},
    {"source_id": "V6453-S08", "title": "New Zealand Geodetic Datum 2000", "url": "https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/geodetic-datums/new-zealand-geodetic-datum-2000-nzgd2000", "authority": "official LINZ guidance", "status": "current"},
    {"source_id": "V6453-S09", "title": "Transformations between WGS84 and NZGD2000", "url": "https://www.linz.govt.nz/guidance/geodetic-system/understanding-coordinate-conversions/geodetic-datum-conversions/transformations-between-wgs84-and-nzgd2000", "authority": "official LINZ guidance", "status": "current"},
    {"source_id": "V6453-S10", "title": "Meridional circuits", "url": "https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/projections/meridional-circuits", "authority": "official LINZ guidance", "status": "current"},
    {"source_id": "V6453-S11", "title": "Git multi-pack-index", "url": "https://git-scm.com/docs/git-multi-pack-index", "authority": "official Git documentation", "status": "current"},
    {"source_id": "V6453-S12", "title": "Git commit-graph", "url": "https://git-scm.com/docs/git-commit-graph", "authority": "official Git documentation", "status": "current"},
    {"source_id": "V6453-S13", "title": "Git bitmap format", "url": "https://git-scm.com/docs/bitmap-format", "authority": "official Git documentation", "status": "current"},
    {"source_id": "V6453-S14", "title": "W3C WAI Complex Images Tutorial", "url": "https://www.w3.org/WAI/tutorials/images/complex/", "authority": "official W3C guidance", "status": "current"},
    {"source_id": "V6453-S15", "title": "Nonequilibrium Equality for Free Energy Differences", "url": "https://doi.org/10.1103/PhysRevLett.78.2690", "authority": "primary peer-reviewed paper", "status": "stable"},
    {"source_id": "V6453-S16", "title": "Universal inference", "url": "https://doi.org/10.1073/pnas.1922664117", "authority": "primary peer-reviewed paper", "status": "stable"},
    {"source_id": "V6453-S17", "title": "Anytime validity is free: inducing sequential tests", "url": "https://doi.org/10.1093/jrsssb/qkag050", "authority": "primary peer-reviewed paper", "status": "current"},
    {"source_id": "V6453-S18", "title": "Windows Sandbox sample configuration files", "url": "https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-sample-configuration", "authority": "official Microsoft documentation", "status": "current"},
    {"source_id": "V6453-S19", "title": "Windows Sandbox command line", "url": "https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli", "authority": "official Microsoft documentation", "status": "current"},
]


def packet(packet_id: str, title: str, owner: str, approval_class: str,
           execution: str, artifact: str, acceptance: str,
           protected: list[str] | None = None) -> dict:
    return {
        "packet_id": packet_id,
        "title": title,
        "owner": owner,
        "approval_class": approval_class,
        "x2_execution": execution,
        "hypothesis": f"A bounded, sanitized implementation of {title.lower()} can produce auditable structural evidence without crossing protected authority or empirical gates.",
        "null_or_failure": "The artifact is missing, privacy boundaries are crossed, a synthetic or structural result is overstated, a failure is erased, or a protected gate is silently closed.",
        "artifact": artifact,
        "acceptance_gate": acceptance,
        "rollback_or_recovery": "Retain the negative, restore the last validated bounded state, and leave any unavailable authority or evidence explicitly open.",
        "protected_gates": protected or ["private_material", "sibling_lane", "independent_reproduction", "stage20_promotion"],
    }


EIREN_SAFE_NOW = [
    packet("V6453-SAFE-01", "Causal Method Flow incident graph", "Eiren Kestrel", "safe_now", "execute", "method-flow/causal-incident-contract.json", "All incident nodes retain negative links, witnesses, rollback, and recommendation state."),
    packet("V6453-SAFE-02", "EFT operator-quotient structural tribunal", "Eiren Kestrel", "safe_now", "execute", "physics/eft-quotient-contract.json", "Redundant and independent representatives separate deterministically."),
    packet("V6453-SAFE-03", "Zero-row ILRS adapter readiness screen", "Eiren Kestrel", "safe_now", "execute_protocol_only", "empirical/slr-adapter-readiness.json", "No fit or measurement is emitted when real rows equal zero."),
    packet("V6453-SAFE-04", "Synthetic geodetic station handover proxy", "Eiren Kestrel", "safe_now", "execute_proxy", "thos/station-handover-contract.json", "Discontinuities, epochs, owners, and unresolved state survive all mutations."),
    packet("V6453-SAFE-05", "Deferred credential issuance state machine", "Eiren Kestrel", "safe_now", "execute_proxy", "freed-id/deferred-issuance-profile.json", "Invalid, replayed, expired, or mis-scoped transitions reject."),
    packet("V6453-SAFE-06", "Datum-migration authority refusal matrix", "Eiren Kestrel", "safe_now", "execute_refusal_only", "cbr/datum-migration-authority-matrix.json", "Cadastral, legal, privacy, affected-party, and Maori-authority conclusions remain exact-gated."),
    packet("V6453-SAFE-07", "Git acceleration read-only integrity lab", "Eiren Kestrel", "safe_now", "execute_local_fixture", "security/git-acceleration-contract.json", "Temporary fixtures verify while canonical refs and objects remain unchanged."),
    packet("V6453-SAFE-08", "Complex geospatial accessibility structure audit", "Eiren Kestrel", "safe_now", "execute", "accessibility/geospatial-report-contract.json", "Equivalent short text, long description, coordinate table, labels, and reservations are present."),
    packet("V6453-SAFE-09", "Jarzynski synthetic equality calculator", "Eiren Kestrel", "safe_now", "execute_synthetic", "thermo-psyche/jarzynski-contract.json", "Typed fixtures satisfy the declared algebra and reject psyche-quantity conversion."),
    packet("V6453-SAFE-10", "Anytime-valid sequential evidence board", "Eiren Kestrel", "safe_now", "execute_synthetic", "stage20/anytime-valid-contract.json", "Invalid optional-stopping rules reject and Stage 20 remains not ready."),
    packet("V6453-SAFE-11", "Bounded long-read timeout recurrence guard", "Eiren Kestrel", "safe_now", "execute", "method-flow/read-timeout-method.json", "Initial timeout and successful bounded retry both remain visible."),
    packet("V6453-SAFE-12", "Primary-source freshness and status ledger", "Eiren Kestrel", "safe_now", "execute", "sources/source-ledger.json", "Every material source has authority, status, URL, and nonpromotion boundary."),
    packet("V6453-SAFE-13", "Five-class public-artifact privacy scanner", "Eiren Kestrel", "safe_now", "execute", "validation/privacy-scan.json", "Raw route, ID, credential, private-path, and private-state classes return zero hits."),
    packet("V6453-SAFE-14", "Owner-scoped Windows Sandbox blueprint and linter", "Eiren Kestrel", "safe_now", "execute_blueprint_only", "sandbox/sandbox-blueprint-validation.json", "Six isolated profiles lint; host feature enablement, elevation, and reboot remain separately gated."),
    packet("V6453-SAFE-15", "Owner-generated file-count and rotation guard", "Eiren Kestrel", "safe_now", "execute", "maintenance/owner-file-threshold.json", "Only source-to-final owner files count and remain below 15000."),
]


SUCCESSOR_SAFE_NOW_TITLES = [
    "Cross-phase approval-packet inheritance validator",
    "Source-status drift and supersession screen",
    "GMUT operator-basis dimensional-analysis cross-check",
    "SLR station-metadata completeness matrix",
    "THOS matched-information-budget handover comparator",
    "Deferred-issuance polling backoff mutation corpus",
    "Freed ID notification idempotency replay table",
    "CBR affected-holder notice and remedy reservation",
    "Git object-acceleration nonmutation preflight",
    "Complex-map coordinate-table caption audit",
    "Jarzynski finite-sample bias caution board",
    "Sequential evidence threshold provenance ledger",
    "Windows Sandbox mapped-folder least-write profile",
    "Method Flow recurrence-cluster sibling recommendation",
    "Phase-scoped index and orchestration refresh",
]
SUCCESSOR_SAFE_NOW = [
    packet(f"V6453-NEXT-SAFE-{i:02d}", title, "Ilyra Fen", "safe_now_seed", "successor_preregister_and_execute_if_adopted", f"successor-seeds/safe-{i:02d}.json", "Successor must re-preregister, preserve gates, and supply its own witness before completion credit.")
    for i, title in enumerate(SUCCESSOR_SAFE_NOW_TITLES, 1)
]


EIREN_CANDIDATE_TITLES = [
    "ILRS CRD parser interface with zero-row default",
    "Symbolic EFT representative reducer",
    "Geodetic discontinuity mutation-corpus generator",
    "Deferred-notification idempotency automaton",
    "Windows Sandbox CLI availability probe",
    "Temporary Git MIDX and commit-graph laboratory",
    "Synthetic e-process simulation harness",
    "Complex-map alternative renderer",
    "LF-normalized exact-manifest portability layer",
    "Accessible static evidence-report composer",
]
EIREN_CANDIDATE = [
    packet(f"V6453-CAND-{i:02d}", title, "Eiren Kestrel", "candidate_prototype", "build_test_and_retain_candidate", f"prototypes/candidate-{i:02d}.json", "Prototype must pass its bounded fixture; candidate status does not imply production readiness.")
    for i, title in enumerate(EIREN_CANDIDATE_TITLES, 1)
]


SUCCESSOR_CANDIDATE_TITLES = [
    "Cross-owner proposal semantic-embedding collision screen",
    "IERS station discontinuity schema adapter",
    "SLR force-model assumption diff tool",
    "OpenID4VCI transaction expiry clock abstraction",
    "Privacy-preserving cadastral scenario fixture",
    "Git bitmap reachability fixture generator",
    "Screen-reader map-description rubric",
    "Jarzynski rare-event sampling diagnostic",
    "E-value product-process invariant checker",
    "Sandbox session artifact egress sanitizer",
]
SUCCESSOR_CANDIDATE = [
    packet(f"V6453-NEXT-CAND-{i:02d}", title, "Ilyra Fen", "candidate_seed", "successor_evaluate_before_build", f"successor-seeds/candidate-{i:02d}.json", "Successor must make a fresh safety decision and retain any failed prototype witness.")
    for i, title in enumerate(SUCCESSOR_CANDIDATE_TITLES, 1)
]


EXACT_TITLES = [
    "Ingest and fit official ILRS observations",
    "Recruit geodetic observatory workers for THOS arms",
    "Issue real standards-conformant credentials and keys",
    "Operate live credential resolution, status, and revocation",
    "Interpret cadastral title or property rights",
    "Approve Maori wording, authority, and data governance",
    "Enable or alter host Windows virtualization features with reboot",
    "Deploy a production sandbox or identity service",
    "Commission an independent-team scientific reproduction",
    "Promote the Trinity Mandala to Stage 20 or proof/canon status",
]
EXACT_PACKETS = [
    packet(f"V6453-EXACT-{i:02d}", title, "Eiren Kestrel", "exact_approval", "do_not_execute", f"approval-packets/exact-{i:02d}.json", "Requires exact external evidence and competent authority; remains open in this phase.", ["exact_authority", "external_evidence", "privacy", "non_destructive_host"])
    for i, title in enumerate(EXACT_TITLES, 1)
]


BLOCKED_TITLES = [
    "Claim empirical GMUT confirmation without real data",
    "Claim THOS effectiveness without blind matched-budget real arms",
    "Claim production Freed ID assurance without live interoperability and review",
    "Claim enacted CBR or cultural legitimacy without affected authorities",
    "Claim independent reproduction, consciousness, personhood, AGI/ASI, or exhaustive security without evidence",
]
BLOCKED_PACKETS = [
    packet(f"V6453-BLOCKED-{i:02d}", title, "Eiren Kestrel", "blocked", "prohibited_without_new_evidence", f"approval-packets/blocked-{i:02d}.json", "No execution or promotion is permitted; the negative boundary remains explicit.", ["truth_boundary", "authority_boundary", "nonpromotion"])
    for i, title in enumerate(BLOCKED_TITLES, 1)
]


EIREN_SKILLS = [
    ("ghc-audit-proposal-novelty", "Audit a proposed phase title and mission surface against frozen prior proposals before x1 freeze."),
    ("ghc-record-method-incidents", "Record sanitized workflow negatives, witnesses, recurrence guards, and retry quarantine in Method Flow State."),
    ("ghc-verify-source-lineage", "Verify source head, seal ancestry, single-parent history, clean state, and remote equality read-only."),
    ("ghc-test-sandbox-blueprints", "Lint owner-scoped Windows Sandbox configurations and preserve host-change gates."),
    ("ghc-screen-empirical-adapters", "Fail closed when real rows, provenance, baselines, blinding, or independent review are missing."),
    ("ghc-review-freed-id-state-machines", "Review synthetic credential protocol transitions while reserving real cryptographic assurance."),
    ("ghc-reserve-authority-gates", "Keep legal, cultural, Maori-authority, affected-party, and enacted-law decisions exact-gated."),
    ("ghc-audit-static-accessibility", "Audit bounded static-report structure and reserve manual and affected-user evaluation."),
    ("ghc-verify-git-acceleration", "Test MIDX, commit-graph, and bitmap integrity only in additive temporary repositories."),
    ("ghc-build-sequential-evidence-board", "Build a synthetic anytime-valid evidence board that refuses unsupported Stage 20 promotion."),
]

SUCCESSOR_SKILLS = [
    ("ghc-audit-packet-inheritance", "Audit inherited approval packets before successor adoption."),
    ("ghc-compare-reference-frame-epochs", "Compare typed geodetic epochs without inferring property rights."),
    ("ghc-validate-crd-lineage", "Validate ILRS CRD metadata and zero-row boundaries."),
    ("ghc-test-notification-idempotency", "Test deferred credential notification replay behavior on synthetic fixtures."),
    ("ghc-review-map-alternatives", "Review complex-map alternatives and coordinate-table equivalence."),
    ("ghc-measure-rare-event-sampling", "Measure synthetic Jarzynski rare-event sensitivity without empirical promotion."),
    ("ghc-check-eprocess-invariants", "Check nonnegative e-process fixtures and optional-stopping boundaries."),
    ("ghc-sanitize-sandbox-egress", "Screen sandbox outputs before any host or repository ingress."),
    ("ghc-triage-git-object-graphs", "Triage acceleration-structure failures in disposable Git fixtures."),
    ("ghc-refresh-phase-index", "Refresh phase-scoped family index, Method Flow, and orchestration receipts."),
]

EIREN_RUNNERS = [
    ("ghc_family_v645_v3_portfolio_validator.py", "Validate research and approval-packet counts and cross-links."),
    ("ghc_family_sandbox_blueprint_linter.py", "Lint .wsb profiles without launching or altering host features."),
    ("ghc_family_eft_quotient_validator.py", "Evaluate typed synthetic EFT redundancy fixtures."),
    ("ghc_family_deferred_issuance_state_machine.py", "Evaluate synthetic deferred issuance and notification transitions."),
    ("ghc_family_anytime_evidence_board.py", "Evaluate synthetic e-value streams and reject unsupported promotion."),
]

SUCCESSOR_RUNNERS = [
    ("ghc_family_slr_crd_lineage_validator.py", "Validate official-format metadata and zero-row readiness."),
    ("ghc_family_geodetic_handover_mutator.py", "Generate station-discontinuity handover fixtures."),
    ("ghc_family_complex_map_accessibility_auditor.py", "Audit map alternatives and coordinate tables."),
    ("ghc_family_git_acceleration_fixture.py", "Create and verify disposable MIDX and commit-graph fixtures."),
    ("ghc_family_sandbox_egress_guard.py", "Scan sandbox outputs before approved ingress."),
]


EIREN_CLEAN_TITLES = [
    "Audit owner-generated file count against the 15000 threshold",
    "Review stale owner and phase labels in v645-v3 artifacts",
    "Normalize new text artifacts to LF and UTF-8",
    "Verify no duplicate v645-v3 proposal identifiers or titles",
    "Verify approval-class counts and execution boundaries",
    "Check family-current ghc_family and build_ghc_family naming",
    "Retain legacy versioned tools as compatibility surfaces",
    "Scan public artifacts for five private-material classes",
    "Audit source statuses and superseded drafts",
    "Check Method Flow preferred states have passing witnesses",
    "Check sandbox mapped folders are least-write and owner-scoped",
    "Check static report title, headings, landmarks, and no auto-refresh",
    "Check exact staged-file set before each commit",
    "Check ancestry, zero merges, and source seal reachability",
    "Check final local, upstream, tracking, and live-remote equality",
]
EIREN_CLEAN = [
    {"task_id": f"V6453-CLEAN-{i:02d}", "title": title, "owner": "Eiren Kestrel", "execution": "execute_in_x2", "destructive": False, "acceptance": "Emit a bounded receipt; retain every negative and make no sibling-lane mutation."}
    for i, title in enumerate(EIREN_CLEAN_TITLES, 1)
]

SUCCESSOR_CLEAN_TITLES = [
    "Reaudit inherited packet identifiers before adding successor IDs",
    "Recheck primary-source freshness at successor start",
    "Recheck owner-generated file threshold from source head",
    "Recheck Method Flow schema and structural counts",
    "Recheck private-material exclusions in proposed artifacts",
    "Recheck line-ending portability before manifest creation",
    "Recheck all candidate prototypes remain bounded",
    "Recheck exact and blocked packets remain unexecuted",
    "Recheck sandbox blueprint paths are placeholders or owner scoped",
    "Recheck Git temporary fixtures cannot address canonical object storage",
    "Recheck static-report alternatives after successor content changes",
    "Recheck proposal semantic novelty against the expanded frozen chain",
    "Recheck x1-only staging before successor freeze",
    "Recheck source-to-final single-parent history",
    "Recheck one-baton terminal delivery gate",
]
SUCCESSOR_CLEAN = [
    {"task_id": f"V6453-NEXT-CLEAN-{i:02d}", "title": title, "owner": "Ilyra Fen", "execution": "successor_reassess_before_execution", "destructive": False, "acceptance": "Successor emits its own bounded receipt and preserves every inherited negative."}
    for i, title in enumerate(SUCCESSOR_CLEAN_TITLES, 1)
]
