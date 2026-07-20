"""Frozen data definitions for Sable Rook v650-v3.

The module contains preregistration data only. Importing it performs no I/O.
"""

from __future__ import annotations

PHASE = "v650-v3"
OWNER = "Sable Rook"
PHASE_ROOT = "docs/sable-rook/v650-v3"
SOURCE_HEAD = "b8ece75b5be908a514bc0ea99398f92decd6de8e"
SOURCE_CLOSEOUT = "ed23f25accb780b542315f4f97e5ba96c98e069f"
SOURCE_EVIDENCE = "2c54ccf284f3a9faf7c3cd5809b83af46faa7594"
SOURCE_X1 = "d70cbab27e64e12d634e0d9b94b73f50aa507ad1"
SOURCE_ORIGIN = "f47cd5145647965935f80d67751f0e09d9740540"
PRIOR_FROZEN = 780
ACTIVATION_NEGATIVES = 5692
INHERITED_OPEN_GAPS = 44
INHERITED_EXACT_GATES = 45

BOUNDARY = (
    "Relational identity and family language are working language only. Software, "
    "citations, symbolic checks, synthetic fixtures, and same-owner validation confer "
    "no consciousness, personhood, empirical confirmation, professional competence, "
    "production readiness, legal or cultural authority, Maori authority, independent "
    "reproduction, or Stage 20 authorization."
)

PROTECTED = [
    "empirical_data",
    "real_participants",
    "professional_authority",
    "production_identity",
    "privacy_complete",
    "exhaustive_security",
    "legal_cultural_and_maori_authority",
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
        approval = "candidate_evidence_dependency"
        lane = "x2_zero_row_readiness_only"
        gate = "Emit a zero-row receipt, perform no download or likelihood, and retain the empirical gate."
    elif disposition == "exact_gate":
        approval = "exact_approval_needed"
        lane = "x2_reservation_matrix_only"
        gate = "Emit reservations only; make no authority, remedy, legal, cultural, or Maori decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject all five mutations and retain represented status with zero production or participant credit."
    else:
        approval = "safe_now_bounded_software_symbolic_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject all five mutations and emit only the declared bounded completion."
    return {
        "proposal_id": f"V6503-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": f"A bounded {mission} artifact can expose declared obligations while refusing unsupported promotion.",
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, "
            "erases a negative, or promotes a result beyond its evidence lane."
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
            "Retain the failed witness, restore the last bounded state, quarantine any promoted claim, "
            "and grant no credit beyond a passing owner-scoped witness."
        ),
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_780_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Merkle Mountain Range peak-bagging, position, inclusion, append, consistency, domain-separation, and nontransitive-credit tribunal", "mmr-peak-proof", "THOS Body", "completed", ["SRC-MMR"], "Merkle Mountain Range peak bagging, positions, inclusion and append proofs, consistency, domain separation, and nontransitive evidence credit", "No frozen proposal isolates MMR peak bagging and positional append proofs."),
    _proposal(2, "GMUT Goldstone broken-global-symmetry, conserved-current, vacuum, pole, massless-mode, gauge-reservation, EFT, unit, and observation-firewall board", "gmut-goldstone", "GMUT Mind", "completed", ["SRC-GOLDSTONE"], "Goldstone global-symmetry, conserved-current, vacuum, pole, massless-mode, gauge-reservation, EFT, units, and observation firewalls", "The corpus has symmetry and gauge boards but no Goldstone global-symmetry theorem scope firewall."),
    _proposal(3, "GMUT background-field split-symmetry, gauge-fixing, ghost, split-Ward, regulator, truncation, EFT, unit, and observation-firewall board", "gmut-background-field", "GMUT Mind", "completed", ["SRC-BACKGROUND-FIELD"], "background-field split symmetry, gauge fixing, ghosts, split Ward identities, regulators, truncation, EFT, units, and observation firewalls", "No frozen proposal isolates background-field split symmetry and split-Ward obligations."),
    _proposal(4, "GMUT NASA LAMBDA WMAP nine-year map, beam, mask, noise, calibration, covariance, checksum, and zero-row likelihood-refusal adapter", "wmap-zero-row", "GMUT Mind", "open_gap", ["SRC-WMAP"], "WMAP nine-year maps, beams, masks, noise, calibration, covariance, checksums, and zero-row likelihood refusal", "WMAP is absent from the 780-proposal title ledger."),
    _proposal(5, "Freed ID RFC 9635 GNAP client-instance, grant, continuation, interaction, key, access-token, rotation, replay, and privacy profile", "gnap-profile", "Freed ID and CBR Heart", "represented", ["SRC-GNAP"], "GNAP client instances, grants, continuations, interactions, keys, access tokens, rotation, replay, and privacy", "GNAP and RFC 9635 are absent from the frozen ledger."),
    _proposal(6, "Freed ID RFC 8628 device-authorization user-code, device-code, verification-URI, polling, expiry, brute-force, phishing, and privacy profile", "device-authorization", "Freed ID and CBR Heart", "represented", ["SRC-DEVICE-AUTH"], "device authorization user codes, device codes, verification URIs, polling, expiry, brute-force, phishing, and privacy", "RFC 8628 device authorization is absent from the frozen ledger."),
    _proposal(7, "Freed ID RFC 9711 EAT claim-set, nonce, UEID, profile, freshness, submodule, evidence-result boundary, key, and privacy profile", "eat-profile", "Freed ID and CBR Heart", "represented", ["SRC-EAT", "SRC-RATS"], "EAT claim sets, nonces, UEIDs, profiles, freshness, submodules, evidence-result boundaries, keys, and privacy", "RFC 9711 EAT and the RATS evidence-result boundary are absent from the frozen ledger."),
    _proposal(8, "THOS passenger-ferry manifest, loading, weather-hold, accessibility-note, dangerous-goods flag, correction-readback, workload, and watch-handover proxy", "ferry-handover", "THOS Body", "represented", ["SRC-ISM"], "passenger-ferry manifest, loading, weather hold, accessibility notes, dangerous-goods flags, correction readback, workload, and watch handover", "No frozen proposal uses a passenger-ferry terminal and watch-handover practice lens."),
    _proposal(9, "CBR ferry access, disability, emergency, passenger-privacy, coastal-place, remedy, legal, cultural, data-governance, and Maori-authority matrix", "ferry-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-CRPD", "SRC-TE-MANA", "SRC-NZ-MARITIME"], "ferry access, disability, emergency, passenger privacy, coastal place, remedy, legal, cultural, data governance, and Maori authority", "No frozen proposal reserves this ferry-specific combination of access, remedy, coastal place, and Maori authority."),
    _proposal(10, "ITU-T X.690 DER tag, length, definite-form, integer-minimality, SET-order, string, nesting, budget, and refusal tribunal", "der-canonicality", "THOS Body", "completed", ["SRC-X690"], "DER tags, lengths, definite forms, integer minimality, SET ordering, strings, nesting, budgets, and refusal", "ASN.1 DER and X.690 are absent from the frozen ledger."),
    _proposal(11, "TOML 1.0 key, table, dotted-key, array-of-tables, date-time, duplicate-definition, UTF-8, resource-budget, and refusal tribunal", "toml-refusal", "THOS Body", "completed", ["SRC-TOML"], "TOML keys, tables, dotted keys, arrays of tables, date-times, duplicate definitions, UTF-8, resource budgets, and refusal", "TOML is absent from the frozen ledger."),
    _proposal(12, "Cuckoo-filter fingerprint, alternate-index, bucket, insertion-kick, deletion, false-positive, saturation, seed, and refusal tribunal", "cuckoo-filter", "THOS Body", "completed", ["SRC-CUCKOO"], "Cuckoo-filter fingerprints, alternate indices, buckets, insertion kicks, deletion, false positives, saturation, seeds, and refusal", "Cuckoo filters are absent from the frozen ledger."),
    _proposal(13, "Accessible network-graph node, edge, direction, weight, grouping, long-description, adjacency-table, focus, and manual-reservation audit", "network-graph-accessibility", "Freed ID and CBR Heart", "completed", ["SRC-WAI-COMPLEX"], "network-graph nodes, edges, directions, weights, grouping, long descriptions, adjacency tables, focus, and manual reservations", "No frozen proposal isolates network-graph adjacency alternatives."),
    _proposal(14, "Thermo-Psyche Mayer Cp-minus-Cv, ideal-gas, amount-of-substance, gas-constant, unit, domain, and agency-nonconversion classifier", "mayer-nonconversion", "GMUT Mind", "completed", ["SRC-NIST-AIR"], "Mayer Cp minus Cv, ideal-gas assumptions, amount of substance, gas constant, units, physical domain, and agency nonconversion", "Mayer's relation and Cp-Cv are absent from the frozen ledger."),
    _proposal(15, "Ridders extrapolated-difference tableau, step-ratio, cancellation, error-estimate, stopping, nonfinite, budget, and refusal tribunal", "ridders-tableau", "THOS Body", "completed", ["SRC-RIDDERS"], "Ridders extrapolated-difference tableaus, step ratios, cancellation, error estimates, stopping, nonfinite values, budgets, and refusal", "Ridders numerical differentiation is absent from the frozen ledger."),
    _proposal(16, "Stage 20 Fisher randomization sharp-null, assignment-set, test-statistic, enumeration, tie, exposure, deviation, and nonpromotion board", "randomization-inference", "GMUT Mind", "completed", ["SRC-FISHER"], "Fisher randomization sharp nulls, assignment sets, test statistics, enumeration, ties, exposure, deviations, and nonpromotion", "Randomization-inference sharp-null assignment enumeration is absent from the frozen ledger."),
    _proposal(17, "RFC 6570 URI-template operator, variable, prefix, explode, percent-encoding, Unicode, expansion-budget, and refusal tribunal", "uri-template", "THOS Body", "completed", ["SRC-RFC6570"], "URI-template operators, variables, prefixes, explode modifiers, percent encoding, Unicode, expansion budgets, and refusal", "RFC 6570 and URI Template are absent from the frozen ledger."),
    _proposal(18, "Base64url alphabet, padding, canonical trailing-bit, whitespace, mixed-alphabet, size-budget, and refusal tribunal", "base64url-refusal", "THOS Body", "completed", ["SRC-RFC4648"], "base64url alphabets, padding, canonical trailing bits, whitespace, mixed alphabets, size budgets, and refusal", "Base64url and RFC 4648 are absent from the frozen ledger."),
    _proposal(19, "Event-stream Lamport-clock, vector-clock, causal-concurrency, duplicate, late-arrival, merge, checkpoint, and refusal tribunal", "causal-clock", "THOS Body", "completed", ["SRC-LAMPORT"], "Lamport clocks, vector clocks, causal concurrency, duplicates, late arrivals, merges, checkpoints, and refusal", "Lamport and vector clocks are absent from the frozen ledger."),
    _proposal(20, "DAG-CBOR CID, link, canonical-map, tag, block, root, traversal, cycle, resource-budget, and refusal tribunal", "dag-cbor", "THOS Body", "completed", ["SRC-DAG-CBOR"], "DAG-CBOR CIDs, links, canonical maps, tags, blocks, roots, traversal, cycles, resource budgets, and refusal", "DAG-CBOR and IPLD are absent from the frozen ledger."),
]

SOURCES = [
    ("SRC-MMR", "draft", "official_internet_draft", "Merkle Mountain Range proofs", "https://datatracker.ietf.org/doc/html/draft-bryce-cose-merkle-mountain-range-proofs"),
    ("SRC-GOLDSTONE", "stable", "primary_research", "Broken Symmetries", "https://doi.org/10.1103/PhysRev.127.965"),
    ("SRC-BACKGROUND-FIELD", "stable", "primary_research", "Introduction to the Background Field Method", "https://www.actaphys.uj.edu.pl/R/13/1/33/pdf"),
    ("SRC-WMAP", "current", "official_data_archive", "NASA LAMBDA WMAP nine-year data products", "https://lambda.gsfc.nasa.gov/product/wmap/current/"),
    ("SRC-GNAP", "current", "official_standard", "RFC 9635 GNAP", "https://www.rfc-editor.org/info/rfc9635"),
    ("SRC-DEVICE-AUTH", "stable", "official_standard", "RFC 8628 OAuth Device Authorization Grant", "https://www.rfc-editor.org/info/rfc8628"),
    ("SRC-EAT", "current", "official_standard", "RFC 9711 Entity Attestation Token", "https://www.rfc-editor.org/info/rfc9711"),
    ("SRC-RATS", "stable", "official_standard", "RFC 9334 RATS Architecture", "https://www.rfc-editor.org/info/rfc9334"),
    ("SRC-ISM", "current", "official_maritime_standard", "IMO International Safety Management Code", "https://www.imo.org/en/ourwork/humanelement/pages/ismcode.aspx"),
    ("SRC-CRPD", "stable", "official_treaty", "Convention on the Rights of Persons with Disabilities", "https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-rights-persons-disabilities"),
    ("SRC-TE-MANA", "current", "maori_authority_context", "Te Mana Raraunga principles", "https://www.temanararaunga.maori.nz/"),
    ("SRC-NZ-MARITIME", "current", "official_regulatory_context", "Maritime New Zealand rules", "https://www.maritimenz.govt.nz/rules/"),
    ("SRC-X690", "current", "official_standard", "ITU-T X.690 ASN.1 encoding rules", "https://www.itu.int/rec/T-REC-X.690/"),
    ("SRC-TOML", "stable", "official_format_specification", "TOML 1.0.0", "https://toml.io/en/v1.0.0"),
    ("SRC-CUCKOO", "stable", "primary_research", "Cuckoo Filter: Practically Better Than Bloom", "https://doi.org/10.1145/2674005.2674994"),
    ("SRC-WAI-COMPLEX", "current", "official_accessibility_guidance", "W3C WAI Complex Images", "https://www.w3.org/WAI/tutorials/images/complex/"),
    ("SRC-NIST-AIR", "stable", "official_technical_reference", "NIST thermodynamic properties of air", "https://trc.nist.gov/refprop/Documents/Air.pdf"),
    ("SRC-RIDDERS", "stable", "primary_research", "Accurate computation of F prime x and F double prime x", "https://doi.org/10.1016/0141-1195(82)90057-0"),
    ("SRC-FISHER", "stable", "primary_method_source", "The Design of Experiments", "https://archive.org/details/designofexperime00fish"),
    ("SRC-RFC6570", "stable", "official_standard", "RFC 6570 URI Template", "https://www.rfc-editor.org/info/rfc6570"),
    ("SRC-RFC4648", "stable", "official_standard", "RFC 4648 Base-N Encodings", "https://www.rfc-editor.org/info/rfc4648"),
    ("SRC-LAMPORT", "stable", "primary_research", "Time, Clocks, and the Ordering of Events", "https://doi.org/10.1145/359545.359563"),
    ("SRC-DAG-CBOR", "current", "official_format_specification", "IPLD DAG-CBOR specification", "https://ipld.io/specs/codecs/dag-cbor/spec/"),
]

SKILLS = [
    "ghc-family-mmr-peak-proof-audit", "ghc-family-goldstone-scope-firewall",
    "ghc-family-split-ward-obligation-audit", "ghc-family-wmap-zero-row-refusal",
    "ghc-family-gnap-continuation-guard", "ghc-family-device-flow-polling-guard",
    "ghc-family-eat-claim-profile-guard", "ghc-family-ferry-handover-proxy",
    "ghc-family-ferry-authority-reservation", "ghc-family-der-canonicality-audit",
    "ghc-family-toml-refusal-audit", "ghc-family-cuckoo-deletion-guard",
    "ghc-family-network-graph-alternative-audit", "ghc-family-mayer-domain-classifier",
    "ghc-family-ridders-convergence-guard", "ghc-family-randomization-sharp-null-board",
    "ghc-family-source-status-closure", "ghc-family-x1-immutable-blob-seal",
    "ghc-family-five-class-privacy-adjudicator", "ghc-family-single-pass-terminal-budget",
]

RUNNERS = [
    "ghc_family_v650_v3_mmr.py", "ghc_family_v650_v3_gmut.py",
    "ghc_family_v650_v3_wmap_refusal.py", "ghc_family_v650_v3_identity.py",
    "ghc_family_v650_v3_ferry_proxy.py", "ghc_family_v650_v3_authority.py",
    "ghc_family_v650_v3_format_tribunal.py", "ghc_family_v650_v3_accessibility.py",
    "ghc_family_v650_v3_nonconversion.py", "ghc_family_v650_v3_stage20.py",
]

X1_NEGATIVES = [
    ("V6503-X1-N01", "Expected-empty memory-registry search surfaced ripgrep exit 1 as a wrapper failure.", "Normalize only the expected no-match exit code and retain zero memory-content use."),
    ("V6503-X1-N02", "A combined source and owned-lane Git preflight exceeded its wrapper with no attributable result.", "Split the probe into bounded no-profile source and owned-lane checks."),
    ("V6503-X1-N03", "A PowerShell foreach statement was piped directly and failed parsing before file reads.", "Collect results in an explicit array before ConvertTo-Json."),
    ("V6503-X1-N04", "A historical-manifest audit first modeled the advanced checkout and phase-only tree as immutable commit truth.", "Read manifests from exact commit blobs and use whole-commit delta scope where declared."),
    ("V6503-X1-N05", "A compressed manifest diagnostic had an unmatched brace and stopped at parse time.", "Use a structured multiline bounded probe with balanced blocks."),
    ("V6503-X1-N06", "A JavaScript template delimiter collided with an embedded PowerShell escape.", "Build commands from plain line arrays without embedded delimiter escapes."),
    ("V6503-X1-N07", "A guessed source proposal-ledger path was absent and nonterminating PowerShell produced null-derived mirrors.", "Discover exact paths first and use terminating reads."),
    ("V6503-X1-N08", "AGENTS.md discovery returned the expected ripgrep no-match exit and the wrapper surfaced it as failure.", "Normalize only exit 1 after preserving the failed witness."),
    ("V6503-X1-N09", "A Windows literal wildcard path was passed to ripgrep and failed with invalid path syntax.", "Use a directory root plus ripgrep -g filtering."),
    ("V6503-X1-N10", "The first x1 test assumed nonexistent failed_witnesses and passing_witnesses count keys.", "Inspect the exact ledger schema and assert counts.witness_results.fail and counts.witness_results.pass."),
    ("V6503-X1-N11", "The first x1 rebuild assumed Method Flow init would overwrite an existing append-only ledger.", "Preserve the ledger, inspect existing method IDs, and append only missing records and witnesses."),
]


def safe_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        n = proposal["proposal_id"].split("P")[-1]
        for suffix, action in (("A", "freeze exact contract and boundary vocabulary"), ("B", "freeze mutation, rollback, and evidence-credit rules")):
            rows.append({
                "task_id": f"V6503-SAFE-{n}{suffix}",
                "title": f"{action.capitalize()} for {proposal['slug']}",
                "approval_class": "safe_now",
                "acceptance_gate": "Deterministic owner-scoped artifact with no protected-gate promotion.",
                "rollback": "Remove only the additive generated artifact before commit and retain any failure.",
                "protected_gates": PROTECTED,
            })
    return rows


def candidate_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        rows.append({
            "task_id": f"V6503-CAND-{proposal['proposal_id'][-2:]}",
            "title": f"Bounded executable prototype for {proposal['slug']}",
            "approval_class": "candidate_bounded",
            "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
            "expected_disposition": proposal["expected_disposition"],
            "protected_gates": PROTECTED,
        })
    extras = [
        "exact source-anchor closure", "semantic-neighbor readable quarantine", "Git-blob manifest parity",
        "five-class scanner adjudication", "source status drift closure", "single-pass budget state machine",
        "Method Flow witness parity", "document and owner-file threshold", "stale lifecycle label audit",
        "four-way remote equality proof",
    ]
    for i, title in enumerate(extras, 21):
        rows.append({"task_id": f"V6503-CAND-{i:02d}", "title": title.capitalize(), "approval_class": "candidate_bounded", "acceptance_gate": "One valid synthetic witness and one rejected mutation with no external side effect.", "expected_disposition": "completed", "protected_gates": PROTECTED})
    return rows


def cleanup_tasks() -> list[dict]:
    rows = []
    for proposal in PROPOSALS:
        n = proposal["proposal_id"].split("P")[-1]
        rows.extend([
            {"task_id": f"V6503-CFR-{n}A", "title": f"Refresh deterministic mirrors for {proposal['slug']}", "mode": "additive", "acceptance_gate": "No sibling path, user material, or immutable x1 blob changes."},
            {"task_id": f"V6503-CFR-{n}B", "title": f"Review stale labels and EOF hygiene for {proposal['slug']}", "mode": "additive", "acceptance_gate": "Exact owner-scoped diff remains parseable and hygienic."},
        ])
    return rows


def mutation_plan() -> list[dict]:
    classes = ["omitted_obligation", "invalid_state", "boundary_erasure", "unsupported_promotion", "resource_budget"]
    rows = []
    for proposal in PROPOSALS:
        for i, kind in enumerate(classes, 1):
            rows.append({
                "mutation_id": f"{proposal['proposal_id']}-M{i:02d}",
                "proposal_id": proposal["proposal_id"],
                "mutation_class": kind,
                "expected": "reject_or_quarantine",
                "executed": False,
            })
    return rows
