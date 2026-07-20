"""Frozen definitions for Orin Thale's v650-v4 x1 preregistration.

Importing this module performs no I/O.  Observed outcomes are intentionally
absent until x2.
"""

from __future__ import annotations

PHASE = "v650-v4"
OWNER = "Orin Thale"
PHASE_ROOT = "docs/orin-thale/v650-v4"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-full-tools"
SOURCE_HEAD = "b3c9e5ea94f28432911810fa9374eff15fecabad"
SOURCE_CLOSEOUT = "15347fc1d8434533a2516c4d5b60d5b605eee122"
SOURCE_EVIDENCE = "f449d71c8452ea0538ed71eb6d032acb86cb8968"
SOURCE_X1 = "9cf6c85372f64d9c71d3dd207e8018b3af0931e8"
SOURCE_ORIGIN = "b8ece75b5be908a514bc0ea99398f92decd6de8e"
PRIOR_FROZEN = 800
ACTIVATION_NEGATIVES = 5811
INHERITED_OPEN_GAPS = 45
INHERITED_EXACT_GATES = 46

BOUNDARY = (
    "Relational identity and family language are working language only. "
    "Software, citations, symbolic checks, synthetic fixtures, and same-owner "
    "validation confer no consciousness, personhood, empirical confirmation, "
    "professional competence, production readiness, legal or cultural authority, "
    "Maori authority, independent reproduction, or Stage 20 authorization."
)

PROTECTED = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_authority",
    "production_identity",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance",
    "independent_reproduction",
    "stage20",
]


def _proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    disposition: str,
    sources: list[str],
    mission: str,
    novelty: str,
) -> dict:
    if disposition == "open_gap":
        approval = "candidate_empirical_evidence_dependency"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-row receipt, perform no download or likelihood, and retain "
            "the empirical and independent-review gates."
        )
    elif disposition == "exact_gate":
        approval = "exact_approval_needed"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit reservations only; make no safety, remedy, affected-party, legal, "
            "cultural, data-governance, or Maori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject all five preregistered mutations and retain represented status "
            "with zero production, participant, operational, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject all five preregistered mutations and emit only the declared "
            "bounded software, symbolic, formal, or structural completion."
        )
    return {
        "proposal_id": f"V6504-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose declared obligations while "
            "refusing unsupported promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a "
            "preregistered mutation, erases a negative, or promotes a result beyond "
            "its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": (
            "Stop the proposal, retain every failed witness, remove no history, and "
            "leave external, sibling, participant, production, and authority state unchanged."
        ),
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_800_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(
        1,
        "Method Flow hazard-pointer protection-slot, retired-list, scan, ABA, stalled-thread, teardown, and evidence-credit tribunal",
        "hazard-pointer",
        "GMUT Mind",
        "completed",
        ["SRC-HAZARD-POINTER"],
        "hazard-pointer publication, protection slots, retired lists, scanning, ABA handling, stalled threads, teardown, and evidence credit",
        "The frozen epoch-reclamation and copy-on-write proposals do not model per-thread hazard slots and retired-node scans.",
    ),
    _proposal(
        2,
        "GMUT Wigner Poincare-representation mass, spin, little-group, positive-energy, polarization, gauge, EFT, unit, and observation-firewall board",
        "wigner-representation",
        "GMUT Mind",
        "completed",
        ["SRC-WIGNER"],
        "Wigner Poincare representations, mass, spin, little groups, positive energy, polarization, gauge reservation, EFT scope, units, and observation firewalls",
        "No frozen proposal isolates Wigner little-group representation obligations.",
    ),
    _proposal(
        3,
        "GMUT Coleman-Mandula S-matrix symmetry, mass-spectrum, analyticity, nontrivial-scattering, generator-kernel, direct-product, supersymmetry-reservation, EFT, and observation-firewall board",
        "coleman-mandula",
        "GMUT Mind",
        "completed",
        ["SRC-COLEMAN-MANDULA"],
        "Coleman-Mandula S-matrix assumptions, spectrum finiteness, analyticity, scattering nontriviality, generator kernels, direct products, supersymmetry reservation, EFT scope, and observation firewalls",
        "No frozen proposal isolates the Coleman-Mandula assumption set and nonpromotion boundary.",
    ),
    _proposal(
        4,
        "GMUT Stueckelberg gauge-restoration, compensator, mass-term, gauge-fixing, decoupling-limit, strong-coupling, EFT, unit, and observation-firewall board",
        "stueckelberg",
        "GMUT Mind",
        "completed",
        ["SRC-STUECKELBERG"],
        "Stueckelberg compensators, gauge restoration, mass terms, gauge fixing, decoupling limits, strong-coupling reservations, EFT scope, units, and observation firewalls",
        "No frozen proposal isolates Stueckelberg compensator and decoupling-limit obligations.",
    ),
    _proposal(
        5,
        "GMUT 2MASS All-Sky Point Source Catalog photometry, flag, uncertainty, selection, checksum, covariance, and zero-row likelihood-refusal adapter",
        "twomass-zero-row",
        "GMUT Mind",
        "open_gap",
        ["SRC-2MASS-RELEASE", "SRC-2MASS-PSC"],
        "2MASS catalogue provenance, photometry, flags, uncertainty, selection, checksum, covariance, and zero-row likelihood refusal",
        "No frozen empirical adapter targets the 2MASS All-Sky Point Source Catalog.",
    ),
    _proposal(
        6,
        "Freed ID RFC 7523 JWT assertion issuer, subject, audience, expiry, identifier, replay, client-authentication, authorization-grant, and nonproduction profile",
        "jwt-assertion",
        "Freed ID and CBR Heart",
        "represented",
        ["SRC-RFC7523"],
        "RFC 7523 JWT bearer assertions, claim binding, replay refusal, client authentication, authorization grants, and nonproduction reservation",
        "Frozen JWT token profiles do not isolate RFC 7523 assertion processing in both grant and client-authentication roles.",
    ),
    _proposal(
        7,
        "Freed ID RFC 7009 token-revocation endpoint, authentication, token-type hint, unsupported token, cascade, privacy, replay, and nonproduction profile",
        "token-revocation",
        "Freed ID and CBR Heart",
        "represented",
        ["SRC-RFC7009"],
        "RFC 7009 token-revocation endpoints, authentication, token hints, unsupported-token handling, cascade scope, privacy, replay, and nonproduction reservation",
        "No frozen profile isolates RFC 7009 revocation-endpoint request and response behavior.",
    ),
    _proposal(
        8,
        "Freed ID RFC 7591 dynamic-client-registration metadata, software-statement, redirect-URI, initial-access-token, credential, response, minimization, and nonproduction profile",
        "dynamic-client-registration",
        "Freed ID and CBR Heart",
        "represented",
        ["SRC-RFC7591"],
        "RFC 7591 dynamic client registration, metadata, software statements, redirect URIs, initial access, credentials, response binding, minimization, and nonproduction reservation",
        "The frozen RFC 7592 management profile begins after registration; no proposal isolates RFC 7591 creation semantics.",
    ),
    _proposal(
        9,
        "THOS e-bike battery-repair intake, serial-minimization, state-of-charge, isolation, thermal-flag, charger-compatibility, release-refusal, workload, and shift-handover proxy",
        "ebike-repair-proxy",
        "THOS Body",
        "represented",
        ["SRC-CPSC-MICROMOBILITY", "SRC-WORKSAFE-LITHIUM"],
        "e-bike battery-repair intake, identifier minimization, state of charge, isolation, thermal flags, charger compatibility, release refusal, workload control, and handover",
        "No frozen THOS proxy uses an e-bike battery-repair workshop and its repair-specific hold and handover states.",
    ),
    _proposal(
        10,
        "CBR e-bike battery worker, customer, disability, fire-risk, location, disposal, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix",
        "ebike-authority-matrix",
        "Freed ID and CBR Heart",
        "exact_gate",
        ["SRC-CRPD", "SRC-TE-MANA-RARAUNGA", "SRC-NZ-BATTERY-DISPOSAL", "SRC-CPSC-MICROMOBILITY"],
        "e-bike battery worker and customer rights, disability access, fire-risk information, location privacy, disposal, remedy, affected-party acceptance, legal and cultural authority, data governance, and Maori authority",
        "No frozen authority matrix reserves this e-bike repair, disposal, worker-customer, and location combination.",
    ),
    _proposal(
        11,
        "BSON length-prefix, element-type, cstring, UTF-8, duplicate-key, nesting, truncation, resource-budget, and refusal tribunal",
        "bson",
        "THOS Body",
        "completed",
        ["SRC-BSON"],
        "BSON length prefixes, element types, cstrings, UTF-8, duplicate keys, nesting, truncation, resource budgets, and refusal",
        "BSON and its length-prefixed typed element grammar are absent from the frozen ledger.",
    ),
    _proposal(
        12,
        "XZ stream-header, block, filter-chain, index, checksum, concatenation, padding, resource-budget, and refusal tribunal",
        "xz-stream",
        "THOS Body",
        "completed",
        ["SRC-XZ"],
        "XZ stream headers, blocks, filter chains, indexes, checksums, concatenation, padding, resource budgets, and refusal",
        "XZ stream and filter-chain semantics are absent from the frozen format tribunals.",
    ),
    _proposal(
        13,
        "Count-Min Sketch width, depth, hash-family, conservative-update, overflow, merge, error-bound, heavy-hitter, and refusal tribunal",
        "count-min-sketch",
        "GMUT Mind",
        "completed",
        ["SRC-COUNT-MIN"],
        "Count-Min Sketch widths, depths, hash families, conservative updates, overflow, merges, error bounds, heavy hitters, and refusal",
        "No frozen probabilistic data-structure proposal models Count-Min overestimation and merge bounds.",
    ),
    _proposal(
        14,
        "WebVTT header, cue-timing, settings, region, voice, class, malformed-markup, overlap, resource-budget, and refusal tribunal",
        "webvtt",
        "THOS Body",
        "completed",
        ["SRC-WEBVTT"],
        "WebVTT headers, cue timing, settings, regions, voice and class spans, malformed markup, overlap, resource budgets, and refusal",
        "The frozen media-accessibility audit reserves human evaluation but does not exercise WebVTT grammar and cue-state refusal.",
    ),
    _proposal(
        15,
        "Clenshaw recurrence coefficient-order, interval-map, terminal-step, scaling, overflow, cancellation, reference-oracle, and convergence tribunal",
        "clenshaw",
        "GMUT Mind",
        "completed",
        ["SRC-CLENSHAW"],
        "Clenshaw recurrence coefficient order, interval mapping, terminal steps, scaling, overflow, cancellation, reference oracles, and convergence",
        "No frozen numerical-method proposal isolates backward Clenshaw recurrence and its terminal step.",
    ),
    _proposal(
        16,
        "Apache ORC postscript, footer, stripe, stream, compression, row-index, statistics, schema-evolution, resource-budget, and refusal tribunal",
        "apache-orc",
        "THOS Body",
        "completed",
        ["SRC-APACHE-ORC"],
        "Apache ORC postscripts, footers, stripes, streams, compression, row indexes, statistics, schema evolution, resource budgets, and refusal",
        "The frozen Parquet tribunal does not model ORC tail-first metadata, stripe streams, or row indexes.",
    ),
    _proposal(
        17,
        "Accessible Kanban lane, card-order, move-control, drag-alternative, keyboard, focus, status-announcement, filtered-count, fallback, and manual-reservation audit",
        "accessible-kanban",
        "THOS Body",
        "completed",
        ["SRC-WCAG22", "SRC-WAI-ARIA", "SRC-WAI-STATUS"],
        "Kanban lanes, card order, explicit move controls, dragging alternatives, keyboard and focus behavior, status announcements, filtered counts, fallbacks, and manual reservation",
        "The frozen generic dragging-alternative audit does not model lane ownership, card order, filtering, and move-state announcements as one board.",
    ),
    _proposal(
        18,
        "Thermo-Psyche virial equation, compressibility-factor, density-expansion, coefficient, temperature-domain, phase-limit, unit, and agency-nonconversion classifier",
        "virial-nonconversion",
        "GMUT Mind",
        "completed",
        ["SRC-NIST-VIRIAL"],
        "virial equations, compressibility factors, density expansions, coefficients, temperature domains, phase limits, units, and agency nonconversion",
        "No frozen Thermo-Psyche classifier isolates virial-density expansions and compressibility-factor domains.",
    ),
    _proposal(
        19,
        "Stage 20 parametric g-formula time-varying-treatment, confounder-history, consistency, sequential-exchangeability, positivity, model-specification, Monte-Carlo, sensitivity, and nonpromotion board",
        "g-formula-nonpromotion",
        "THOS Body",
        "completed",
        ["SRC-GFORMULA"],
        "parametric g-formula time-varying treatments, confounder histories, consistency, sequential exchangeability, positivity, model specification, Monte Carlo, sensitivity, and nonpromotion",
        "The frozen marginal-structural-model board uses weighting; no proposal isolates generative parametric g-formula simulation.",
    ),
    _proposal(
        20,
        "QPACK field-section, static-table, dynamic-table, insert-count, blocked-stream, acknowledgment, cancellation, capacity, and refusal tribunal",
        "qpack",
        "THOS Body",
        "completed",
        ["SRC-RFC9204"],
        "QPACK field sections, static and dynamic tables, insert counts, blocked streams, acknowledgments, cancellation, capacity, and refusal",
        "QPACK's out-of-order dynamic-table and blocked-stream state machine is absent from the frozen HTTP tribunals.",
    ),
]


SOURCES = [
    ("SRC-HAZARD-POINTER", "stable", "primary_research", "Hazard pointers: safe memory reclamation for lock-free objects", "https://research.ibm.com/publications/hazard-pointers-safe-memory-reclamation-for-lock-free-objects"),
    ("SRC-WIGNER", "stable", "primary_research", "On unitary representations of the inhomogeneous Lorentz group", "https://cds.cern.ch/record/405887/"),
    ("SRC-COLEMAN-MANDULA", "stable", "primary_research", "All Possible Symmetries of the S Matrix", "https://doi.org/10.1103/PhysRev.159.1251"),
    ("SRC-STUECKELBERG", "stable", "primary_research_review", "The Stueckelberg Field", "https://arxiv.org/abs/hep-th/0304245"),
    ("SRC-2MASS-RELEASE", "stable", "official_data_archive", "2MASS All-Sky Data Release", "https://irsa.ipac.caltech.edu/data/2MASS/docs/releases/allsky/index.html"),
    ("SRC-2MASS-PSC", "stable", "official_data_dictionary", "2MASS All-Sky Point Source Catalog format", "https://irsa.ipac.caltech.edu/2MASS/download/allsky/format_psc.html"),
    ("SRC-RFC7523", "stable", "official_standard", "RFC 7523 OAuth JWT Assertion Profiles", "https://www.rfc-editor.org/info/rfc7523"),
    ("SRC-RFC7009", "stable", "official_standard", "RFC 7009 OAuth Token Revocation", "https://www.rfc-editor.org/info/rfc7009"),
    ("SRC-RFC7591", "stable", "official_standard", "RFC 7591 OAuth Dynamic Client Registration", "https://www.rfc-editor.org/info/rfc7591"),
    ("SRC-CPSC-MICROMOBILITY", "current", "official_safety_guidance", "CPSC Micromobility Information Center", "https://www.cpsc.gov/Safety-Education/Safety-Education-Centers/Micromobility-Information-Center"),
    ("SRC-WORKSAFE-LITHIUM", "current", "official_safety_guidance", "WorkSafe safe use of lithium-ion batteries", "https://www.worksafe.govt.nz/topic-and-industry/energy-safety/safe-use-of-lithium-ion-batteries-and-battery-products/"),
    ("SRC-CRPD", "stable", "official_treaty", "Convention on the Rights of Persons with Disabilities", "https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-rights-persons-disabilities"),
    ("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty"),
    ("SRC-NZ-BATTERY-DISPOSAL", "current", "official_environment_guidance", "New Zealand battery drop-off guidance", "https://environment.govt.nz/what-you-can-do/campaigns/recycle/recycle-item/"),
    ("SRC-BSON", "current", "official_format_specification", "BSON specification version 1.1", "https://bsonspec.org/spec.html"),
    ("SRC-XZ", "current", "official_format_specification", "XZ file format specification", "https://tukaani.org/xz/xz-file-format.txt"),
    ("SRC-COUNT-MIN", "stable", "primary_research", "An improved data stream summary: the Count-Min sketch", "https://doi.org/10.1016/j.jalgor.2003.12.001"),
    ("SRC-WEBVTT", "current", "official_format_specification", "WebVTT specification", "https://w3c.github.io/webvtt/"),
    ("SRC-CLENSHAW", "stable", "primary_research", "A note on the summation of Chebyshev series", "https://doi.org/10.1090/S0025-5718-1955-0071856-0"),
    ("SRC-APACHE-ORC", "current", "official_format_specification", "Apache ORC specification", "https://orc.apache.org/specification/"),
    ("SRC-WCAG22", "current", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/"),
    ("SRC-WAI-ARIA", "current", "official_accessibility_standard", "WAI-ARIA 1.2", "https://www.w3.org/TR/wai-aria/"),
    ("SRC-WAI-STATUS", "current", "official_accessibility_technique", "ARIA22 status messages", "https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA22"),
    ("SRC-NIST-VIRIAL", "stable", "official_technical_reference", "NIST vapor-phase fugacity model from virial coefficients", "https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6654.pdf"),
    ("SRC-GFORMULA", "stable", "primary_method_source", "Parametric g-formula for sustained treatment strategies", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7351102/"),
    ("SRC-RFC9204", "current", "official_standard", "RFC 9204 QPACK", "https://www.rfc-editor.org/info/rfc9204"),
]


SKILLS = [
    "ghc-family-hazard-pointer-credit-audit",
    "ghc-family-wigner-representation-firewall",
    "ghc-family-coleman-mandula-assumption-board",
    "ghc-family-stueckelberg-scope-guard",
    "ghc-family-twomass-zero-row-refusal",
    "ghc-family-jwt-assertion-profile",
    "ghc-family-token-revocation-profile",
    "ghc-family-dynamic-client-registration-profile",
    "ghc-family-ebike-repair-proxy",
    "ghc-family-ebike-authority-reservation",
    "ghc-family-bson-refusal-audit",
    "ghc-family-xz-stream-refusal-audit",
    "ghc-family-count-min-bound-audit",
    "ghc-family-webvtt-cue-audit",
    "ghc-family-clenshaw-recurrence-audit",
    "ghc-family-orc-stripe-audit",
    "ghc-family-kanban-accessibility-audit",
    "ghc-family-virial-domain-classifier",
    "ghc-family-g-formula-nonpromotion",
    "ghc-family-qpack-state-audit",
]

RUNNERS = [
    "ghc_family_v650_v4_method_and_gmut.py",
    "ghc_family_v650_v4_twomass_refusal.py",
    "ghc_family_v650_v4_identity_profiles.py",
    "ghc_family_v650_v4_ebike_proxy.py",
    "ghc_family_v650_v4_authority_matrix.py",
    "ghc_family_v650_v4_format_tribunals.py",
    "ghc_family_v650_v4_numeric_tribunals.py",
    "ghc_family_v650_v4_accessibility.py",
    "ghc_family_v650_v4_nonconversion.py",
    "ghc_family_v650_v4_stage20.py",
]

REJECTED_COLLISIONS = [
    {
        "candidate": "Freed ID OAuth resource-indicator profile",
        "nearest_prior_id": "V6488-P05",
        "reason": "The mechanism and RFC surface were already frozen; different wording would be cosmetic.",
    },
    {
        "candidate": "Stage 20 synthetic-control board",
        "nearest_prior_id": "V6492-P10",
        "reason": "The donor-pool and placebo mechanism already has two frozen instances.",
    },
    {
        "candidate": "Accessible accordion audit",
        "nearest_prior_id": "V6456-P08",
        "reason": "The details-summary disclosure surface was too close to justify a new core proposal.",
    },
    {
        "candidate": "GMUT Kugo-Ojima BRST quartet board",
        "nearest_prior_id": "V6458-P02",
        "reason": "BRST nilpotency and cohomological obligations were already frozen; the candidate was quarantined.",
    },
    {
        "candidate": "GMUT Noether second-theorem board",
        "nearest_prior_id": "V6452-P02",
        "reason": "Noether identities and dependent gauge constraints were already frozen.",
    },
]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6504-X1-N01",
        "category": "broad_worktree_listing",
        "failed": "A broad worktree listing exceeded the display window and earned no completeness credit.",
        "recovery": "Use exact named-path and branch probes for source and owner lanes.",
        "passing": "Exact bounded probes established the source and owner lane identities without mutation.",
        "recurrence_guard": "Do not use an unbounded worktree inventory as proof of one named lane.",
    },
    {
        "negative_id": "V6504-X1-N02",
        "category": "baton_read_budget",
        "failed": "A direct full activation-baton read exceeded the output budget and was not counted as complete.",
        "recovery": "Read the committed baton in bounded line-addressed chunks through the exact final line.",
        "passing": "Four bounded chunks covered every line through end of file.",
        "recurrence_guard": "Chunk long authoritative files and record explicit end-of-file coverage.",
    },
    {
        "negative_id": "V6504-X1-N03",
        "category": "fast_forward_summary_budget",
        "failed": "The fast-forward change summary exceeded the display budget and earned no path-inventory credit.",
        "recovery": "Verify exact head, ancestry, status, and remote equality with bounded post-operation probes.",
        "passing": "The owner lane reached the exact source head, stayed clean, and was pushed four-way equal.",
        "recurrence_guard": "Treat verbose Git summaries as diagnostics, never as exact state receipts.",
    },
    {
        "negative_id": "V6504-X1-N04",
        "category": "frozen_index_schema",
        "failed": "The first collision query assumed a nonexistent proposals key and therefore searched zero records.",
        "recovery": "Decode and concatenate prior_proposals with new_proposals, then assert the combined count is 800.",
        "passing": "The corrected collision screen covered all 800 frozen proposal records.",
        "recurrence_guard": "Inspect exact JSON keys and assert corpus cardinality before semantic screening.",
    },
    {
        "negative_id": "V6504-X1-N05",
        "category": "similarity_sweep_timeout",
        "failed": "One broad PowerShell similarity sweep timed out after fifteen of twenty candidates and earned no complete-audit credit.",
        "recovery": "Run bounded candidate batches and preserve the same tokenization and threshold.",
        "passing": "The recovered batches scored all twenty candidates; every maximum was below 0.50.",
        "recurrence_guard": "Batch quadratic lexical scans and require an exact candidate count in the receipt.",
    },
]


def safe_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        pid = proposal["proposal_id"]
        rows.extend(
            [
                {
                    "item_id": f"V6504-SAFE-{len(rows) + 1:02d}",
                    "title": f"Build the bounded {proposal['slug']} contract and explicit refusal boundary",
                    "proposal_id": pid,
                    "approval_class": "safe_now_owner_scoped",
                    "execution_lane": "x2_bounded_owner_local",
                    "origin": "orin_v650_v4_new",
                    "x1_state": "frozen_not_executed",
                    "acceptance_gate": "Emit a schema-valid contract with all protected gates and no outcome promotion.",
                },
                {
                    "item_id": f"V6504-SAFE-{len(rows) + 2:02d}",
                    "title": f"Build five rejecting {proposal['slug']} mutations with retained witnesses",
                    "proposal_id": pid,
                    "approval_class": "safe_now_owner_scoped",
                    "execution_lane": "x2_disposable_synthetic",
                    "origin": "orin_v650_v4_new",
                    "x1_state": "frozen_not_executed",
                    "acceptance_gate": "Reject every preregistered mutation and retain its identifier.",
                },
            ]
        )
    return rows


def candidate_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        rows.append(
            {
                "item_id": f"V6504-CAND-{len(rows) + 1:02d}",
                "title": f"Prototype a deterministic {proposal['slug']} accepting and rejecting evaluator",
                "proposal_id": proposal["proposal_id"],
                "approval_class": "candidate_bounded_prototype",
                "execution_lane": "x2_disposable_synthetic",
                "origin": "orin_v650_v4_new",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "One declared valid fixture passes and one declared invalid fixture fails closed.",
            }
        )
    for proposal in PROPOSALS[:10]:
        rows.append(
            {
                "item_id": f"V6504-CAND-{len(rows) + 1:02d}",
                "title": f"Prototype {proposal['slug']} rollback and evidence-credit isolation",
                "proposal_id": proposal["proposal_id"],
                "approval_class": "candidate_bounded_prototype",
                "execution_lane": "x2_owner_local_no_external_state",
                "origin": "orin_v650_v4_new",
                "x1_state": "frozen_not_executed",
                "acceptance_gate": "A failed fixture receives zero promotion credit and leaves external state unchanged.",
            }
        )
    return rows


def cleanup_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        rows.extend(
            [
                {
                    "item_id": f"V6504-CFR-{len(rows) + 1:02d}",
                    "title": f"CLEAN {proposal['slug']} generated-path and UTF-8 normalization",
                    "proposal_id": proposal["proposal_id"],
                    "class": "CLEAN",
                    "approval_class": "safe_now_additive_non_destructive",
                    "x1_state": "frozen_not_executed",
                    "acceptance_gate": "Owner paths remain normalized; no user or sibling material is deleted.",
                },
                {
                    "item_id": f"V6504-CFR-{len(rows) + 2:02d}",
                    "title": f"REFINE {proposal['slug']} evidence label and gate visibility",
                    "proposal_id": proposal["proposal_id"],
                    "class": "REFINE",
                    "approval_class": "safe_now_additive_non_destructive",
                    "x1_state": "frozen_not_executed",
                    "acceptance_gate": "Every receipt names its evidence class, rollback, and protected gates.",
                },
            ]
        )
    return rows


def mutation_plan() -> list[dict]:
    mutation_names = [
        "missing_required_obligation",
        "wrong_domain_or_type",
        "unsupported_promotion_attempt",
        "resource_or_iteration_budget_exceeded",
        "negative_or_gate_erasure_attempt",
    ]
    rows = []
    for proposal in PROPOSALS:
        for name in mutation_names:
            rows.append(
                {
                    "mutation_id": f"V6504-MUT-{len(rows) + 1:03d}",
                    "proposal_id": proposal["proposal_id"],
                    "mutation": name,
                    "expected": "rejected_or_quarantined",
                    "x1_state": "preregistered_not_executed",
                    "completion_credit": False,
                }
            )
    return rows
