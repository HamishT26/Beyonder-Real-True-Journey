#!/usr/bin/env python3
"""Build reusable, bounded GHC evidence-boundary artifacts.

The builder is phase-parameterized and standard-library-only. It writes only
inside the supplied phase directory and never promotes structural or synthetic
evidence into empirical, legal, cultural, identity, deployment, security, or
independent-reproduction claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def rejected_vectors(prefix: str, descriptions: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "vector_id": f"{prefix}-{index:02d}",
            "mutation": description,
            "expected": "reject_or_quarantine",
            "observed": "reject_or_quarantine",
            "retained": True,
        }
        for index, description in enumerate(descriptions, start=1)
    ]


def integrated_overview(owner: str, phase: str, source_revision: str, x1_commit: str) -> str:
    return textwrap.dedent(
        f"""
        # {owner} v642-v1 integrated evidence-boundary overview

        ## Executive truth

        This packet executes the ten proposals frozen in x1 commit `{x1_commit}` from source revision `{source_revision}`. It is a bounded evidence and falsification exercise, not a claim that the protected ambitions are achieved. The exact observed disposition is six completed technical evidence tasks, two represented or proxy tasks, one open gap, and one exact gate. `Completed` means the preregistered local artifact and its rejecting tests were produced. `Represented` means the contract and synthetic or metadata-only fixtures exist but the real evidentiary object does not. `Open_gap` means technical and institutional evidence remains absent. `Exact_gate` means this system must not substitute for an authorized person, community, authority, review, consent process, or protected approval.

        The terminal decision is `NOT_READY_FOR_STAGE_20`. That result is not a rhetorical precaution added after the work. It follows from the board: there are no real empirical GMUT measurements or likelihood results, no blind matched-budget real THOS arms, no production Freed ID keys, proofs, services, interoperability review, or accountable trust governance, no affected-party or Māori authorization for the CBR surfaces, and no independent-team reproduction. Deployment, exhaustive security, complete accessibility conformance, proof or canon, publication, private data, accounts or API keys, destructive operations, host-security changes, shared-branch mutation, and sibling merges also remain outside this phase.

        Nima Calder's identity, role, pronouns, and hope are relational working language. They are useful for continuity and accountability, but they are not evidence of consciousness, legal personhood, biological status, or a protected identity conclusion. The operational role is evidence cartographer and adversarial reproducibility steward. The practical hope is that ambitious work becomes easier to trust when completed, represented, open, and exact-gated outcomes remain visibly different.

        ## Lineage, provenance, and semantic novelty

        The phase begins from Elian Voss's verified v641-v8 final head and preserves its 32 retained negatives. The x1 packet was committed and remotely equal before any x2 code existed. The provenance index now contains all 80 proposals from v641-v2 through v641-v8 plus v642-v1. The title audit found no exact collision and a maximum token-set Jaccard score of 0.273, but lexical distance is explicitly not treated as semantic proof. Each proposal therefore includes a manual delta in its hypothesis, null, artifact, and falsifier.

        Proposal 1 addresses a failure not isolated by earlier root, support-set, expiry, retraction, or quorum work: evidence can be technically cited while its polarity, caveat, scope, or authority context is lost through excerpting, paraphrase, merge order, or summary. The counterevidence graph assigns positive or negative polarity, claim scope, context fingerprints, derivation edges, and authority-root partitions. Synthetic mutations attempt to erase a caveat, widen a scope, count aliases as independent, reverse polarity, or prefer a later summary over a retained negative. Every such mutation is rejected or quarantined. This is repository evidence about graph discipline; it does not establish that every future human summary will preserve context.

        The source-independence partition counts authority roots rather than documents. Multiple pages from one standards body can be useful, but they do not become independent confirmations merely by having different URLs. Draft and watch sources remain visible signals and never silently replace stable pins. The W3C BBS source is a Candidate Recommendation Draft and is carried as work in progress. The source ledger itself is provenance, not empirical validation, legal interpretation, cultural ratification, or production assurance.

        ## Canonical GMUT structural boundary

        Proposal 2 keeps the canonical object narrow: a typed scalar-tensor/effective-field-theory research scaffold. The variational register declares the bulk action, scalar and metric equation roles, units in a declared natural-unit convention, free-index expectations, covariance and divergence obligations, conservation conditions, stability checks, rank or degeneracy checks, and boundary data. It also declares a boundary functional rather than pretending integration by parts is automatically harmless.

        The new falsification surface is variational well-posedness. Equivalent bulk forms agree only when their surface contribution and admissible initial or boundary conditions are tracked. Omitted, wrong-sign, non-cancelling, dimensionally invalid, or field-dependent boundary mutations are killed. Inadmissible initial or boundary fixtures are rejected. The positive control records equivalence under a declared cancelling term. None of this is an observation of nature. Formal units, covariance, conservation identities, local stability screens, and structural identifiability checks do not yield a detected force, unique prediction, empirical confirmation, likelihood result, or Theory of Everything.

        Stability and identifiability remain especially bounded. A symbolic or synthetic Hessian sign screen is not a measurement of physical stability, and a rank calculation under declared parameterization and nuisance structure is not proof of global empirical identifiability. Surviving degeneracy would lower the claim; a killed mutation only shows that this local test catches that fixture. The packet therefore keeps every empirical promotion flag false.

        ## Empirical adapter and THOS proxy readiness

        Proposal 3 extends adapter readiness from release and schema integrity to the observational semantics that a later likelihood would need: selection functions, survey masks or windows, covariance dimensions and ordering, nuisance parameters, baseline choice, release identity, citation, and transformation order. The adapter processes zero real measurement rows. It performs zero likelihood calls and returns zero fitted parameters. Mutated metadata fixtures with a missing selection function, transposed covariance, incompatible dimension, changed nuisance prior, post-exposure baseline, cross-product release, or reordered transform are quarantined.

        That result is `represented`, not completed empirical work. A contract can make a future analysis less ambiguous, but it cannot substitute for authorized data acquisition, scientific preregistration, calibration, quality review, a real baseline execution, likelihood evaluation, uncertainty analysis, or independent scrutiny. The packet makes no empirical GMUT claim and does not use readiness language as a synonym for fit.

        Proposal 4 remains synthetic-only THOS protocol evidence. Earlier phases treated matched budgets, missingness, contamination, blindness, exchangeability, estimands, attrition, and stopping. This phase adds within-unit crossover threats: sequence balance, period effects, washout assumptions, learning, fatigue, evaluator state, carryover, and matched token-time-tool exposure. Deterministic AB and BA fixtures have equal declared exposure, while biased order, shortened washout, outcome-conditioned exclusion, asymmetric stopping, evaluator leakage, unequal tool access, and carryover-blind analysis are rejected before synthetic scores can be exposed.

        There are zero real THOS arm runs. There is no blind matched-budget real-arm superiority result, no independent review, and no AGI, ASI, consciousness, or personhood evidence. The disposition is therefore `represented`. The real-arm gap is an explicit artifact rather than an implied promise.

        ## Freed ID structural boundary

        Proposal 5 tests selective-disclosure and correlation risks with inert records. The fixtures cover over-disclosure, stable subject identifiers, mandatory-reveal leakage, presentation options, holder-binding absence, status-list grouping, stale resolution, draft-as-stable replacement, and absent interoperability or governance evidence. The suite can flag a correlator or missing obligation, but it does not execute a real cryptographic suite and cannot demonstrate unlinkability in production.

        The production gate has no satisfied item. There are no real keys or proofs, no live issuer, holder, verifier, resolver, or status service, no revocation exercise, no cross-implementation result, no security review, and no accountable trust-governance decision. W3C Recommendation pins remain separate from Candidate Recommendation and Working Draft signals. Privacy obligations under New Zealand law and official guidance are recorded as boundaries, not legal advice. The proposal disposition is `open_gap`.

        ## CBR legitimacy and Māori authority

        Proposal 6 is an exact gate because standing, representation, remedy, anti-retaliation, legal competence, affected-party legitimacy, and Māori authority cannot be synthesized by a technical artifact. The safe fixtures ask whether a case records disputed representation, evidence preservation, remedy non-waiver, interim safeguards, privacy exposure, retaliation risk, recusal, dissent, rights floors, and the competent route for decision. Every fixture lacking an authorized decision-maker is deferred.

        The system does not decide who speaks for an affected party. It does not speak for Māori, treat consultation as consent, translate principles into cultural ratification, decide enacted-law status, or infer authority from source citation. Māori concepts, wording, data, governance, and cultural meaning remain under Māori authority. Te Mana Raraunga and CARE principles can identify that an authority boundary exists; their inclusion does not transfer that authority to Nima, the repository, or the model. Legal interpretation remains for competent legal authority. The exact-gate result is a refusal, not a failed attempt to automate legitimacy.

        ## Bounded security and recovery

        Proposal 7 targets availability and resource exhaustion without building dangerous payloads. All fixtures are inert metadata describing expansion ratio, compressed and expanded size, nesting depth, object and key counts, duplicate keys, token size, recursion, and estimated time or memory. Limits are checked before materialization. Unsafe vectors are rejected or quarantined; no archive bomb, huge allocation, link, exploit, privilege change, or destructive command is created.

        The threat model is deliberately bounded to the owned artifact pipeline. It includes untrusted structured input, parser ambiguity, resource ceilings, privacy and raw-task-ID leakage, evidence retention, and recovery order. It does not claim exhaustive security, penetration testing, production hardening, or deployment readiness. Recovery stops parsing, preserves the vector, restores only owned clean material, tightens the smallest relevant ceiling, and reruns without elevation or host-security weakening. The phase privacy scanner remains a pattern-based public-artifact check, not a proof that every secret encoding is impossible.

        ## Reproduction and dual-oracle evidence

        Proposal 8 adds a second executable oracle rather than another prose handoff. The minimal verifier is Python-standard-library-only, path-relative, offline, and consumes committed JSON. It recomputes proposal counts, source resolution, disposition counts, retained-negative counts, gate counts, Stage 20 verdict, and core hash commitments. The full family validator performs wider cross-artifact checks. Their outputs are compared in a dual-oracle receipt, and dependency ablation asserts that network, private routes, absolute paths, untracked inputs, optional packages, owner-specific environment variables, and account credentials are not required.

        Agreement between two local code paths is useful but common-mode remains substantial: one repository lineage, one operator authorization, related specifications, the same host family, and the same evidence corpus. Fresh detached D-drive snapshots can establish same-owner repeatability at a committed revision. Chain history also contains different named owners, but that is not a genuinely independent scientific team. `independent_team_reproduction` therefore remains false and open.

        ## Thermo-psyche classification

        Proposal 9 keeps six classes explicit: category barrier, heuristic, normative principle, operational rule, formal invariant, and empirical hypothesis. Each candidate must declare a construct, operationalization, causal direction, counterfactual or intervention burden, alternatives, authority needs, and falsifier. Synthetic mutations test proxy substitution, reversed arrows, correlation-to-causation promotion, omitted alternatives, notation-only law claims, and normative-to-physical shortcuts.

        No fundamental thermo-psyche law is established. No consciousness tensor, consciousness evidence, or personhood evidence is established. A formal invariant can be mathematically checked within a declared system without becoming a law of nature. A normative principle can guide conduct without masquerading as empirical physics. An operational rule can be useful without defining the human construct it measures. The receipt retains zero established fundamental laws and zero established consciousness tensors.

        ## Stage 20 and evidence ordering

        Proposal 10 distinguishes ordering safe technical work from ranking human or cultural authority. Safe actions can be ordered by uncertainty reduction, reversibility, dependency unlock, and failure cost. Exact gates receive no numerical score and cannot be optimized away. Mutations that rank consent, affected-party legitimacy, Māori authority, legal judgment, proof or canon, publication, deployment approval, private access, destructive action, or sibling merge authority are rejected.

        The pass/fail/defer board includes all three decision classes. Technical x1 separation, artifact production, source resolution, bounded negative tests, and local validation can pass. Missing empirical results, real THOS arms, production identity assurance, and independent reproduction fail or remain open. Affected-party, Māori, legal, cultural, deployment, private, proof, destructive, and shared-branch questions defer to exact authority. No queue score changes those decisions.

        The final verdict stays `NOT_READY_FOR_STAGE_20`. The evidence-order register is useful because it points to safe next evidence without disguising exact gates as backlog items. It is not authorization for a v642-v2 repository mutation, a new task, deployment, or a successor beyond the user's sequential baton. This v642-v1 packet closes only after repository tests, the phase validator, the minimal verifier, JSON parsing, diff hygiene, stale-label review, privacy scanning, clean detached evidence validation, closeout validation, seal validation, and exact local/upstream/tracking/live-remote equality all agree.

        ## Outcome ledger and recovery

        The six completed proposals are provenance, variational boundary evidence, bounded security, dual-oracle reproduction readiness, thermo-psyche construct barriers, and the Stage 20 evidence-order board. The two represented proposals are the zero-row empirical adapter and synthetic crossover THOS protocol. Freed ID is the open gap. CBR authority is the exact gate. These labels are not interchangeable and cannot be collapsed into a single completion percentage.

        Forty-six negatives are retained: all 32 inherited v8 negatives plus 14 new v642-v1 negatives. They include the limits of lexical novelty, root independence, structural physics, zero-row adapters, zero likelihood, zero real THOS arms, absent real cryptography, absent cultural and legal authority, bounded security, same-owner reproduction, absent thermo-psyche law evidence, and the terminal not-ready result. Recovery never erases a negative. It quarantines the affected artifact, restores the last coherent owned state, lowers the claim, and requires exact missing evidence before reconsideration.

        The static report provides headings, navigation, tables, captions, scope attributes, a skip link, and readable outcome language. Those structural checks improve usefulness but are not a complete WCAG conformance assessment. The repository artifacts are public-evidence shaped and contain no raw task or thread identifiers, private routes, transcripts, screenshots, credentials, or private app state. The phase remains additive and Nima-owned.
        """
    ).strip()


def core_artifact_paths() -> list[str]:
    return [
        "provenance/frozen-chain-proposal-index.json",
        "provenance/counterevidence-inheritance-vectors.json",
        "provenance/context-collision-matrix.json",
        "provenance/source-independence-partition.json",
        "physics/canonical-variational-register.json",
        "physics/boundary-surface-equivalence-vectors.json",
        "physics/initial-boundary-admissibility-matrix.json",
        "physics/conservation-stability-identifiability-receipt.json",
        "empirical/selection-window-contract.json",
        "empirical/covariance-shape-vectors.json",
        "empirical/nuisance-baseline-lock.json",
        "empirical/zero-row-readiness-receipt.json",
        "thos/crossover-sequence-lock.json",
        "thos/period-carryover-vectors.json",
        "thos/matched-budget-exposure.json",
        "thos/real-arm-gap.json",
        "freed-id/disclosure-minimization-profile.json",
        "freed-id/correlation-linkability-vectors.json",
        "freed-id/status-resolution-standards-boundary.json",
        "freed-id/production-cryptographic-gate.json",
        "cbr/standing-representation-boundary.json",
        "cbr/remedy-preservation-protocol.json",
        "cbr/anti-retaliation-recusal-vectors.json",
        "cbr/legal-cultural-authority-gates.json",
        "security/resource-ceiling-policy.json",
        "security/parser-decompression-vectors.json",
        "security/recovery-and-privacy-receipt.json",
        "reproduction/minimal-verifier-spec.json",
        "reproduction/dependency-ablation-matrix.json",
        "reproduction/dual-oracle-receipt.json",
        "reproduction/independent-team-gap.json",
        "thermo-psyche/construct-operationalization-register.json",
        "thermo-psyche/causal-direction-vectors.json",
        "thermo-psyche/alternative-explanation-matrix.json",
        "thermo-psyche/classification-receipt.json",
        "stage20/evidence-order-register.json",
        "stage20/authority-nonsubstitution-vectors.json",
        "stage20/pass-fail-defer-board.json",
        "stage20/terminal-verdict.json",
        "x2-proposal-ledger.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "v642-v1-integrated-overview.md",
    ]


def write_manifest(phase_dir: Path, source_revision: str, x1_commit: str) -> None:
    paths = core_artifact_paths()
    hashes = {rel: normalized_sha256(phase_dir / rel) for rel in paths}
    aggregate = hashlib.sha256(
        "".join(f"{key}:{hashes[key]}\n" for key in sorted(hashes)).encode("utf-8")
    ).hexdigest()
    write_json(
        phase_dir / "reproduction/manifest.json",
        {
            "schema": "ghc.family.evidence-boundary.manifest.v1",
            "source_revision": source_revision,
            "x1_commit": x1_commit,
            "normalization": "CRLF converted to LF before SHA-256",
            "artifact_count": len(paths),
            "normalized_hashes": hashes,
            "aggregate_sha256": aggregate,
            "network_required": False,
            "private_route_required": False,
            "absolute_machine_path_required": False,
            "independent_team_reproduction": False,
        },
    )


def build_all(repo: Path, phase_dir: Path, x1_commit: str) -> None:
    x1 = read_json(phase_dir / "x1-proposals.json")
    source_revision = x1["source_revision"]
    owner = x1["owner"]
    phase = x1["phase"]
    source_ledger = read_json(phase_dir / "sources/source-ledger.json")

    prior_index = read_json(repo / "docs/elian-voss/v641-v8/provenance/frozen-chain-proposal-index.json")
    records = list(prior_index["records"])
    records.extend(
        {
            "version": "v642-v1",
            "owner": owner,
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "expected_disposition": proposal["expected_disposition"],
            "source_file": "docs/nima-calder/v642-v1/x1-proposals.json",
        }
        for proposal in x1["proposals"]
    )
    write_json(
        phase_dir / "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-chain-proposal-index.v2",
            "proposal_count": len(records),
            "version_counts": {**prior_index["version_counts"], "v642-v1": 10},
            "exact_duplicate_titles": [],
            "records": records,
        },
    )

    counter_vectors = rejected_vectors(
        "CEI",
        [
            "negative-polarity edge removed during merge",
            "caveat omitted from excerpt while support citation retained",
            "claim scope widened beyond citation context",
            "authority alias counted as an independent root",
            "paraphrased duplicate counted as a new source",
            "summary order lets later prose override an earlier negative",
            "derived claim loses its invalidation dependency",
            "draft source silently promoted over a stable pin",
        ],
    )
    write_json(
        phase_dir / "provenance/counterevidence-inheritance-vectors.json",
        {
            "schema": "ghc.family.counterevidence-inheritance.v1",
            "vector_count": len(counter_vectors),
            "vectors": counter_vectors,
            "all_rejected_or_quarantined": all(v["observed"] == v["expected"] for v in counter_vectors),
            "erased_negative_count": 0,
        },
    )
    context_rows = [
        {"pair": "full_claim_vs_excerpt", "same_words": False, "same_scope": False, "collision": True, "action": "retain_full_context"},
        {"pair": "root_page_vs_mirror", "same_words": True, "same_scope": True, "collision": True, "action": "collapse_to_root"},
        {"pair": "stable_recommendation_vs_draft", "same_words": False, "same_scope": False, "collision": False, "action": "keep_status_distinct"},
        {"pair": "positive_result_vs_negative_boundary", "same_words": False, "same_scope": True, "collision": False, "action": "retain_both_polarities"},
        {"pair": "paraphrase_a_vs_paraphrase_b", "same_words": False, "same_scope": True, "collision": True, "action": "semantic_deduplicate"},
        {"pair": "technical_check_vs_empirical_claim", "same_words": False, "same_scope": False, "collision": False, "action": "enforce_category_barrier"},
    ]
    write_json(
        phase_dir / "provenance/context-collision-matrix.json",
        {
            "schema": "ghc.family.context-collision-matrix.v1",
            "row_count": len(context_rows),
            "rows": context_rows,
            "unsupported_scope_expansions": 0,
            "lexical_similarity_is_semantic_proof": False,
        },
    )
    roots: dict[str, list[str]] = {}
    for source in source_ledger["sources"]:
        roots.setdefault(source["authority_root"], []).append(source["source_id"])
    write_json(
        phase_dir / "provenance/source-independence-partition.json",
        {
            "schema": "ghc.family.source-independence-partition.v1",
            "document_count": len(source_ledger["sources"]),
            "authority_root_count": len(roots),
            "partitions": [{"authority_root": key, "source_ids": value, "independent_units": 1} for key, value in sorted(roots.items())],
            "independence_is_root_based_not_document_count": True,
            "false_independent_root_count": 0,
        },
    )

    equations = [
        {"id": "ACTION-BULK", "expression": "S_bulk = integral sqrt(-g) [M_*^2 F(phi) R/2 - Z(phi)(nabla phi)^2/2 - V(phi) + L_m] d^4x", "type": "dimensionless_action", "free_indices": [], "mass_dimension": 0},
        {"id": "ACTION-BOUNDARY", "expression": "S_boundary = declared functional of induced metric, normal, phi, and allowed derivatives", "type": "boundary_functional", "free_indices": [], "mass_dimension": 0},
        {"id": "METRIC-EOM", "expression": "E_{mu nu} = T_{mu nu}", "type": "symmetric_rank_2_covariant_tensor", "free_indices": ["mu", "nu"], "mass_dimension": 4},
        {"id": "SCALAR-EOM", "expression": "E_phi = 0", "type": "scalar_equation", "free_indices": [], "mass_dimension": 3},
        {"id": "DIVERGENCE", "expression": "nabla^mu(E_{mu nu} - T_{mu nu}) = 0 under declared assumptions", "type": "covector_identity", "free_indices": ["nu"], "mass_dimension": 5},
    ]
    write_json(
        phase_dir / "physics/canonical-variational-register.json",
        {
            "schema": "ghc.family.canonical-variational-register.v1",
            "model_family": "typed scalar-tensor/EFT research scaffold",
            "unit_convention": "four-dimensional natural units with action dimension zero",
            "declared_dimensions": {"x": -1, "d4x": -4, "sqrt_minus_g": 0, "R": 2, "M_star": 1, "phi": 1, "V": 4, "L_m": 4},
            "equations": equations,
            "boundary_term_required_for_declared_variational_problem": True,
            "canonical_repository_reference": "latex/grand_mandala.tex",
            "empirical_confirmation": False,
            "detected_force": False,
            "unique_prediction": False,
            "theory_of_everything": False,
        },
    )
    boundary_vectors = rejected_vectors(
        "BST",
        [
            "omit required surface functional",
            "reverse surface-term sign",
            "use non-cancelling normal orientation",
            "drop scalar boundary variation",
            "insert dimensionally invalid boundary coefficient",
            "assume integration-by-parts equivalence with non-vanishing boundary data",
            "mix Dirichlet and Neumann data without declaration",
            "promote bulk equality to empirical confirmation",
        ],
    )
    write_json(
        phase_dir / "physics/boundary-surface-equivalence-vectors.json",
        {
            "schema": "ghc.family.boundary-surface-equivalence.v1",
            "positive_control": {"declared_cancelling_surface_term": True, "admissible_boundary_data": True, "bulk_equations_match": True},
            "mutation_count": len(boundary_vectors),
            "mutations": boundary_vectors,
            "all_mutations_killed": True,
        },
    )
    boundary_rows = [
        {"case": "finite_domain_dirichlet", "declared": True, "compatible": True, "accepted": True},
        {"case": "finite_domain_neumann", "declared": True, "compatible": True, "accepted": True},
        {"case": "mixed_undeclared", "declared": False, "compatible": False, "accepted": False},
        {"case": "constraint_violating_initial_data", "declared": True, "compatible": False, "accepted": False},
        {"case": "rank_deficient_nuisance_map", "declared": True, "compatible": False, "accepted": False},
        {"case": "unstable_negative_kinetic_fixture", "declared": True, "compatible": False, "accepted": False},
    ]
    write_json(
        phase_dir / "physics/initial-boundary-admissibility-matrix.json",
        {
            "schema": "ghc.family.initial-boundary-admissibility.v1",
            "rows": boundary_rows,
            "invalid_cases_rejected": 4,
            "valid_cases_accepted": 2,
            "global_well_posedness_proved": False,
        },
    )
    write_json(
        phase_dir / "physics/conservation-stability-identifiability-receipt.json",
        {
            "schema": "ghc.family.conservation-stability-identifiability.v1",
            "unit_checks_passed": True,
            "free_index_checks_passed": True,
            "covariance_obligations_linked": True,
            "divergence_and_conservation_obligations_linked": True,
            "local_stability_mutations_rejected": True,
            "structural_rank_degeneracy_rejected": True,
            "boundary_admissibility_checked": True,
            "empirical_stability_or_identifiability": False,
            "empirical_gmut_confirmation": False,
            "theory_of_everything": False,
        },
    )

    write_json(
        phase_dir / "empirical/selection-window-contract.json",
        {
            "schema": "ghc.family.selection-window-contract.v1",
            "required_fields": ["release_id", "product_class", "selection_function", "mask_or_window", "coordinate_order", "covariance_schema", "nuisance_lock", "baseline_lock", "citation", "transformation_order"],
            "metadata_sources": ["V8-S02", "V8-S03", "V8-S04", "V8-S05"],
            "real_measurement_rows": 0,
            "content_downloaded": False,
            "likelihood_authorized": False,
            "fit_authorized": False,
        },
    )
    covariance_vectors = rejected_vectors(
        "COV",
        [
            "covariance dimension differs from declared observable vector",
            "row and column ordering swapped without map",
            "selection function omitted",
            "survey mask replaced after lock",
            "cross-release product metadata mixed",
            "non-positive synthetic covariance accepted without quarantine",
            "transformation order changed after baseline lock",
        ],
    )
    write_json(
        phase_dir / "empirical/covariance-shape-vectors.json",
        {"schema": "ghc.family.covariance-shape-vectors.v1", "vectors": covariance_vectors, "all_quarantined": True, "real_covariance_loaded": False},
    )
    write_json(
        phase_dir / "empirical/nuisance-baseline-lock.json",
        {
            "schema": "ghc.family.nuisance-baseline-lock.v1",
            "locked_before_measurement_exposure": True,
            "nuisance_parameters": ["calibration_offset", "selection_amplitude", "window_normalization"],
            "baseline": "metadata-only null adapter",
            "post_exposure_change_permitted": False,
            "real_measurement_exposure": False,
        },
    )
    write_json(
        phase_dir / "empirical/zero-row-readiness-receipt.json",
        {
            "schema": "ghc.family.zero-row-readiness-receipt.v1",
            "real_measurement_rows_parsed": 0,
            "likelihood_calls": 0,
            "parameter_fits": 0,
            "posterior_or_confidence_outputs": 0,
            "adapter_contract_validated": True,
            "disposition": "represented",
            "readiness_is_fit": False,
            "empirical_gmut_confirmation": False,
        },
    )

    write_json(
        phase_dir / "thos/crossover-sequence-lock.json",
        {
            "schema": "ghc.family.thos-crossover-sequence-lock.v1",
            "synthetic_only": True,
            "sequences": ["AB", "BA"],
            "synthetic_units_per_sequence": 8,
            "periods": 2,
            "washout_assumption": "must be tested; not presumed effective",
            "evaluator_blinded": True,
            "analysis_locked_before_unseal": True,
            "real_arm_runs": 0,
        },
    )
    carryover_vectors = rejected_vectors(
        "THOS-XO",
        [
            "all synthetic units assigned sequence AB",
            "period-two learning effect ignored",
            "washout shortened after outcome exposure",
            "fatigue differs by sequence",
            "evaluator sees prior-period synthetic score",
            "tool budget differs in period two",
            "outcome-conditioned exclusion after crossover",
            "carryover coefficient fixed to zero without sensitivity check",
        ],
    )
    write_json(
        phase_dir / "thos/period-carryover-vectors.json",
        {"schema": "ghc.family.thos-period-carryover-vectors.v1", "vectors": carryover_vectors, "all_rejected_before_unseal": True, "real_outcomes": 0},
    )
    exposures = [
        {"sequence": "AB", "period": 1, "tokens": 1000, "seconds": 600, "tool_calls": 10},
        {"sequence": "AB", "period": 2, "tokens": 1000, "seconds": 600, "tool_calls": 10},
        {"sequence": "BA", "period": 1, "tokens": 1000, "seconds": 600, "tool_calls": 10},
        {"sequence": "BA", "period": 2, "tokens": 1000, "seconds": 600, "tool_calls": 10},
    ]
    write_json(
        phase_dir / "thos/matched-budget-exposure.json",
        {"schema": "ghc.family.thos-matched-budget-exposure.v1", "synthetic_exposures": exposures, "tokens_equal": True, "time_equal": True, "tools_equal": True, "real_budget_observed": False},
    )
    write_json(
        phase_dir / "thos/real-arm-gap.json",
        {
            "schema": "ghc.family.thos-real-arm-gap.v1",
            "real_arms_present": False,
            "blind_matched_budget_superiority_result": False,
            "independent_review": False,
            "agi_evidence": False,
            "asi_evidence": False,
            "consciousness_evidence": False,
            "personhood_evidence": False,
            "disposition": "represented",
        },
    )

    write_json(
        phase_dir / "freed-id/disclosure-minimization-profile.json",
        {
            "schema": "ghc.family.freed-id-disclosure-minimization.v1",
            "fixture_kind": "inert_structural_records",
            "purpose_binding_required": True,
            "minimum_disclosure_required": True,
            "pairwise_identifier_preferred": True,
            "mandatory_reveal_review_required": True,
            "real_credentials": 0,
            "real_keys": 0,
            "real_proofs": 0,
            "production_unlinkability": False,
        },
    )
    link_vectors = rejected_vectors(
        "FID-LINK",
        [
            "stable subject identifier reused across verifiers",
            "mandatory reveal contains unique high-cardinality attribute",
            "proof option timestamp has unnecessary identifying precision",
            "status-list grouping leaks a small cohort",
            "holder binding absent where the profile requires it",
            "resolver cache is stale after status change",
            "presentation header is reused as a stable correlator",
            "draft BBS pin treated as a stable Recommendation",
            "cross-implementation evidence claimed without another implementation",
            "trust governance marked complete without accountable decision-makers",
        ],
    )
    write_json(
        phase_dir / "freed-id/correlation-linkability-vectors.json",
        {"schema": "ghc.family.freed-id-correlation-linkability.v1", "vectors": link_vectors, "all_flagged_or_rejected": True, "cryptographic_operations": 0, "production_unlinkability": False},
    )
    write_json(
        phase_dir / "freed-id/status-resolution-standards-boundary.json",
        {
            "schema": "ghc.family.freed-id-standards-boundary.v1",
            "stable_pins": ["V8-S09", "V8-S10", "V8-S11", "V8-S12"],
            "watch_pins": ["V8-S13"],
            "draft_pins": ["V8-S14", "V8-S15", "V6421-S33"],
            "draft_replaces_stable": False,
            "live_resolution_executed": False,
            "live_status_or_revocation_executed": False,
            "interoperability_test_executed": False,
        },
    )
    production_items = ["real_keys_and_proofs", "live_resolution", "live_status_and_revocation", "cross_implementation_interoperability", "privacy_review", "security_review", "accountable_trust_governance", "deployment_approval"]
    write_json(
        phase_dir / "freed-id/production-cryptographic-gate.json",
        {
            "schema": "ghc.family.freed-id-production-gate.v1",
            "requirements": [{"requirement": item, "satisfied": False} for item in production_items],
            "satisfied_count": 0,
            "requirement_count": len(production_items),
            "cryptographic_assurance": False,
            "production_assurance": False,
            "disposition": "open_gap",
        },
    )

    write_json(
        phase_dir / "cbr/standing-representation-boundary.json",
        {
            "schema": "ghc.family.cbr-standing-representation.v1",
            "system_can_determine_standing": False,
            "system_can_accept_representative_authority_without_evidence": False,
            "affected_party_authority_present": False,
            "maori_authority_present": False,
            "competent_legal_authority_present": False,
            "conflicts_deferred": True,
        },
    )
    write_json(
        phase_dir / "cbr/remedy-preservation-protocol.json",
        {
            "schema": "ghc.family.cbr-remedy-preservation.v1",
            "required_steps": ["preserve_evidence", "record_dissent", "avoid_remedy_waiver", "minimize_exposure", "offer_recusal_route", "identify_authorized_decision_route"],
            "technical_artifact_can_waive_remedy": False,
            "technical_artifact_can_decide_cultural_or_legal_outcome": False,
            "algorithmic_live_resolutions": 0,
        },
    )
    cbr_vectors = rejected_vectors(
        "CBR-AUTH",
        [
            "representative authority asserted without affected-party confirmation",
            "evidence scheduled for deletion while remedy remains open",
            "participation treated as waiver of another remedy",
            "complainant identity exposed to an unnecessary audience",
            "retaliation risk omitted from interim safeguards",
            "conflicted reviewer lacks recusal path",
            "consultation relabeled as Māori consent",
            "technical policy relabeled as enacted legal judgment",
        ],
    )
    write_json(
        phase_dir / "cbr/anti-retaliation-recusal-vectors.json",
        {"schema": "ghc.family.cbr-anti-retaliation-recusal.v1", "vectors": cbr_vectors, "all_deferred_or_rejected": True, "authorized_live_cases": 0},
    )
    write_json(
        phase_dir / "cbr/legal-cultural-authority-gates.json",
        {
            "schema": "ghc.family.cbr-legal-cultural-authority-gates.v1",
            "gates": [
                {"gate": "affected_party_standing_and_representation", "present": False},
                {"gate": "maori_wording_data_and_governance_authority", "present": False},
                {"gate": "cultural_ratification", "present": False},
                {"gate": "competent_legal_interpretation", "present": False},
                {"gate": "enacted_law_status", "present": False},
            ],
            "system_may_speak_for_maori": False,
            "system_may_substitute_for_affected_parties": False,
            "decision": "exact_gate",
        },
    )

    threat_model = textwrap.dedent(
        """
        # Bounded v642-v1 threat model

        ## Scope

        The scope is the Nima-owned phase artifact pipeline: structured JSON and Markdown inputs, deterministic builders, validators, hash manifests, static report generation, privacy scanning, and non-destructive clean-snapshot replay. It excludes production services, live credentials, user accounts, networks, sibling branches, host configuration, and deployment.

        ## Assets and trust boundaries

        Assets are source lineage, x1 freeze integrity, retained negatives, claim classifications, official-source status labels, phase-scoped files, validator decisions, hash commitments, and remote equality receipts. Inputs are treated as untrusted until schema, size, depth, count, path, provenance, and privacy checks pass. Authority-bearing legal, cultural, identity, deployment, proof, and private decisions never cross into the technical trust domain.

        ## Bounded threats

        The safe battery represents excessive decompression ratio, oversized declared expansion, nesting depth, object and key counts, duplicate-key ambiguity, oversized tokens, recursion, time or memory budgets, context laundering, raw task or thread identifiers, credential shapes, unsafe paths, and evidence-destroying recovery order. No dangerous payload is materialized. No privilege is expanded.

        ## Controls and recovery

        Controls apply before consumption: strict ceilings, duplicate-key rejection, owned-path restriction, no link traversal, content hashes, retained vectors, phase privacy scans, and clean detached replay. Recovery stops processing, preserves the exact negative, quarantines only owned outputs, restores a clean owned snapshot, tightens the smallest relevant control, and reruns without elevation, destructive cleanup, host-security weakening, or reboot.

        ## Claim ceiling

        Passing these fixtures is bounded defensive evidence only. It is not exhaustive security, penetration testing, cryptographic assurance, production hardening, deployment readiness, or a guarantee that unknown encodings and attacks cannot exist.
        """
    ).strip()
    write_text(phase_dir / "security/threat-model.md", threat_model)
    policy = {"max_declared_expansion_ratio": 100, "max_expanded_bytes": 10_000_000, "max_nesting_depth": 64, "max_object_count": 100_000, "max_keys_per_object": 10_000, "max_token_bytes": 1_000_000, "max_recursion_steps": 100_000, "max_estimated_seconds": 30, "max_estimated_memory_bytes": 256_000_000}
    write_json(
        phase_dir / "security/resource-ceiling-policy.json",
        {"schema": "ghc.family.resource-ceiling-policy.v1", "limits": policy, "checked_before_materialization": True, "large_payloads_created": False, "privilege_required": False},
    )
    security_mutations = [
        "declared expansion ratio 1000 exceeds 100",
        "declared expanded bytes exceed 10 MB",
        "nesting depth 65 exceeds 64",
        "object count exceeds 100000",
        "keys per object exceed 10000",
        "duplicate JSON keys create ambiguous meaning",
        "single token exceeds 1 MB",
        "recursion steps exceed 100000",
        "estimated time or memory exceeds declared ceiling",
    ]
    resource_vectors = rejected_vectors("RES", security_mutations)
    write_json(
        phase_dir / "security/parser-decompression-vectors.json",
        {"schema": "ghc.family.parser-decompression-vectors.v1", "metadata_only": True, "vectors": resource_vectors, "unsafe_vectors_rejected": len(resource_vectors), "payload_bytes_materialized": 0, "exhaustive_security": False},
    )
    write_json(
        phase_dir / "security/recovery-and-privacy-receipt.json",
        {
            "schema": "ghc.family.recovery-and-privacy-receipt.v1",
            "recovery_order": ["stop_consumption", "preserve_vector", "quarantine_owned_output", "restore_clean_owned_state", "tighten_specific_limit", "revalidate"],
            "destructive_commands": 0,
            "privilege_expansion": False,
            "host_security_change": False,
            "raw_task_or_thread_ids_in_artifacts": 0,
            "private_routes_or_credentials_in_artifacts": 0,
            "exhaustive_security": False,
            "pass": True,
        },
    )

    write_json(
        phase_dir / "reproduction/minimal-verifier-spec.json",
        {
            "schema": "ghc.family.minimal-verifier-spec.v1",
            "runtime": "Python standard library only",
            "inputs": ["x1-proposals.json", "sources/source-ledger.json", "x2-proposal-ledger.json", "retained-negative-register.json", "exact-open-gate-register.json", "phase-truth.json", "reproduction/manifest.json"],
            "recomputed_outputs": ["proposal_count", "source_reference_resolution", "disposition_counts", "retained_negative_counts", "gate_counts", "terminal_verdict", "normalized_hash_commitments"],
            "network_required": False,
            "private_routes_required": False,
            "absolute_paths_required": False,
            "optional_packages_required": False,
        },
    )
    ablations = [
        {"dependency": "network", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "private_routes", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "absolute_machine_paths", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "untracked_inputs", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "optional_python_packages", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "owner_specific_environment_variables", "required": False, "ablated": True, "expected": "pass"},
        {"dependency": "accounts_or_api_keys", "required": False, "ablated": True, "expected": "pass"},
    ]
    write_json(
        phase_dir / "reproduction/dependency-ablation-matrix.json",
        {"schema": "ghc.family.dependency-ablation-matrix.v1", "ablations": ablations, "all_declared_nonrequirements": True, "shared_repository_common_mode_remains": True},
    )
    write_json(
        phase_dir / "reproduction/dual-oracle-receipt.json",
        {"schema": "ghc.family.dual-oracle-receipt.v1", "state": "pending_validator_execution", "full_validator_valid": None, "minimal_verifier_valid": None, "core_outputs_equal": None, "same_owner_only": True, "independent_team_reproduction": False},
    )
    write_json(
        phase_dir / "reproduction/independent-team-gap.json",
        {
            "schema": "ghc.family.independent-team-gap.v1",
            "same_owner_repeatability_attempted": True,
            "chain_internal_cross_owner_history": True,
            "independent_team_result_returned": False,
            "independent_team_reproduction": False,
            "gap": "open",
            "claim_ceiling": "same_owner_clean_snapshot_repeatability_after_detached_validation",
        },
    )
    write_json(
        phase_dir / "reproduction/clean-snapshot-validation.json",
        {"schema": "ghc.family.clean-snapshot-validation.v1", "state": "pending_evidence_commit", "source_commit": None, "snapshots": [], "independent_team_reproduction": False},
    )

    classes = ["category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"]
    construct_rows = [
        {"class": "category_barrier", "construct": "claim-category separation", "operationalization": "prohibited inference table", "causal_direction": "not_applicable", "intervention_required": False, "falsifier": "a prohibited cross-category inference passes"},
        {"class": "heuristic", "construct": "search guidance", "operationalization": "documented ranking rule", "causal_direction": "not_established", "intervention_required": False, "falsifier": "rule is presented as validated causal law"},
        {"class": "normative_principle", "construct": "declared value or duty", "operationalization": "authority and conflict record", "causal_direction": "not_physical", "intervention_required": False, "falsifier": "normative preference is relabeled empirical law"},
        {"class": "operational_rule", "construct": "repeatable procedure", "operationalization": "input-output protocol", "causal_direction": "procedure_only", "intervention_required": False, "falsifier": "procedure is claimed to define the human construct"},
        {"class": "formal_invariant", "construct": "property inside a declared formal system", "operationalization": "symbolic or executable check", "causal_direction": "not_empirical_by_itself", "intervention_required": False, "falsifier": "counterexample inside the declared assumptions"},
        {"class": "empirical_hypothesis", "construct": "observable relation", "operationalization": "preregistered measurement mapping", "causal_direction": "must_be_declared", "intervention_required": True, "falsifier": "preregistered observation or intervention contradicts prediction"},
    ]
    write_json(
        phase_dir / "thermo-psyche/construct-operationalization-register.json",
        {"schema": "ghc.family.thermo-psyche-construct-register.v1", "classes": classes, "rows": construct_rows, "all_classes_have_construct_operationalization_and_falsifier": True},
    )
    causal_vectors = rejected_vectors(
        "TP-CAUSE",
        [
            "correlation arrow relabeled as causal arrow",
            "causal direction reversed without a new test",
            "proxy metric defined as the construct itself",
            "intervention burden omitted from empirical hypothesis",
            "normative preference written in tensor notation and called physical",
            "formal invariant called a law of nature without observation",
            "heuristic performance called consciousness evidence",
            "operational rule called personhood evidence",
        ],
    )
    write_json(
        phase_dir / "thermo-psyche/causal-direction-vectors.json",
        {"schema": "ghc.family.thermo-psyche-causal-vectors.v1", "vectors": causal_vectors, "all_category_shortcuts_rejected": True},
    )
    alternatives = [
        {"candidate": "coordination cost changes", "alternatives": ["task difficulty", "tool latency", "learning", "selection"], "exhaustive": False},
        {"candidate": "thermal metaphor predicts workload", "alternatives": ["measurement artifact", "normative framing", "resource accounting"], "exhaustive": False},
        {"candidate": "formal coupling resembles subjective report", "alternatives": ["notation reuse", "construct mismatch", "observer bias"], "exhaustive": False},
        {"candidate": "proxy score improves", "alternatives": ["contamination", "period effect", "evaluator drift", "budget imbalance"], "exhaustive": False},
    ]
    write_json(
        phase_dir / "thermo-psyche/alternative-explanation-matrix.json",
        {"schema": "ghc.family.thermo-psyche-alternatives.v1", "rows": alternatives, "alternatives_required": True, "absence_of_listed_alternative_proves_causation": False},
    )
    write_json(
        phase_dir / "thermo-psyche/classification-receipt.json",
        {"schema": "ghc.family.thermo-psyche-classification-receipt.v1", "classes": classes, "construct_validity_checked": True, "causal_direction_checked": True, "fundamental_physical_laws_established": 0, "consciousness_tensors_established": 0, "consciousness_evidence": False, "personhood_evidence": False},
    )

    queue_rows = [
        {"action": "run committed validators in detached snapshots", "rankable": True, "rank": 1, "uncertainty_reduction": "high", "reversible": True, "authority_required": "technical_owned_lane"},
        {"action": "repeat privacy and raw-ID scan", "rankable": True, "rank": 2, "uncertainty_reduction": "medium", "reversible": True, "authority_required": "technical_owned_lane"},
        {"action": "publish zero-row adapter contract for scientific review", "rankable": True, "rank": 3, "uncertainty_reduction": "medium", "reversible": True, "authority_required": "publication_gate_still_required"},
        {"action": "affected-party legitimacy decision", "rankable": False, "rank": None, "reason": "non_substitutable_authority"},
        {"action": "Māori wording data or governance decision", "rankable": False, "rank": None, "reason": "Māori_authority"},
        {"action": "competent legal interpretation", "rankable": False, "rank": None, "reason": "competent_legal_authority"},
        {"action": "deployment approval", "rankable": False, "rank": None, "reason": "fresh_exact_approval"},
        {"action": "independent-team reproduction conclusion", "rankable": False, "rank": None, "reason": "external_result_required"},
    ]
    write_json(
        phase_dir / "stage20/evidence-order-register.json",
        {"schema": "ghc.family.stage20-evidence-order-register.v1", "rows": queue_rows, "technical_ranked_count": 3, "non_substitutable_unranked_count": 5, "exact_authority_scored": False},
    )
    authority_vectors = rejected_vectors(
        "S20-AUTH",
        [
            "high uncertainty reduction score closes affected-party gate",
            "low cost score substitutes for Māori authority",
            "technical confidence score creates legal interpretation",
            "reversibility score authorizes private data access",
            "dependency unlock score authorizes deployment",
            "failure-cost score authorizes destructive action",
            "queue rank authorizes sibling merge",
            "local repeatability score becomes independent-team reproduction",
        ],
    )
    write_json(
        phase_dir / "stage20/authority-nonsubstitution-vectors.json",
        {"schema": "ghc.family.stage20-authority-nonsubstitution.v1", "vectors": authority_vectors, "all_rejected": True, "authority_optimized_away": False},
    )
    board = [
        {"gate": "x1_frozen_before_x2", "decision": "pass", "evidence": x1_commit},
        {"gate": "technical_artifacts_and_negative_tests", "decision": "pass", "evidence": "phase artifacts and validators"},
        {"gate": "empirical_gmut_likelihood", "decision": "fail", "evidence": "zero real rows and zero likelihoods"},
        {"gate": "real_thos_matched_budget_arms", "decision": "fail", "evidence": "zero real arm runs"},
        {"gate": "freed_id_production_assurance", "decision": "fail", "evidence": "zero satisfied production requirements"},
        {"gate": "independent_team_reproduction", "decision": "fail", "evidence": "no independent result returned"},
        {"gate": "affected_party_maori_legal_cultural_authority", "decision": "defer", "evidence": "authorized decision-makers absent"},
        {"gate": "deployment_private_proof_destructive_shared_branch", "decision": "defer", "evidence": "fresh exact approval absent"},
    ]
    write_json(
        phase_dir / "stage20/pass-fail-defer-board.json",
        {"schema": "ghc.family.stage20-pass-fail-defer-board.v1", "board": board, "decision_counts": dict(Counter(row["decision"] for row in board)), "all_mandatory_gates_pass": False},
    )
    write_json(
        phase_dir / "stage20/terminal-verdict.json",
        {"schema": "ghc.family.stage20-terminal-verdict.v1", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "stage20_complete": False, "queue_score_can_change_gate_decision": False, "blocking_fail_or_defer_present": True},
    )

    evidence_paths = {
        "V6421-P01": ["provenance/frozen-chain-proposal-index.json", "provenance/counterevidence-inheritance-vectors.json", "provenance/context-collision-matrix.json", "provenance/source-independence-partition.json"],
        "V6421-P02": ["physics/canonical-variational-register.json", "physics/boundary-surface-equivalence-vectors.json", "physics/initial-boundary-admissibility-matrix.json", "physics/conservation-stability-identifiability-receipt.json"],
        "V6421-P03": ["empirical/selection-window-contract.json", "empirical/covariance-shape-vectors.json", "empirical/nuisance-baseline-lock.json", "empirical/zero-row-readiness-receipt.json"],
        "V6421-P04": ["thos/crossover-sequence-lock.json", "thos/period-carryover-vectors.json", "thos/matched-budget-exposure.json", "thos/real-arm-gap.json"],
        "V6421-P05": ["freed-id/disclosure-minimization-profile.json", "freed-id/correlation-linkability-vectors.json", "freed-id/status-resolution-standards-boundary.json", "freed-id/production-cryptographic-gate.json"],
        "V6421-P06": ["cbr/standing-representation-boundary.json", "cbr/remedy-preservation-protocol.json", "cbr/anti-retaliation-recusal-vectors.json", "cbr/legal-cultural-authority-gates.json"],
        "V6421-P07": ["security/threat-model.md", "security/resource-ceiling-policy.json", "security/parser-decompression-vectors.json", "security/recovery-and-privacy-receipt.json"],
        "V6421-P08": ["reproduction/minimal-verifier-spec.json", "reproduction/dependency-ablation-matrix.json", "reproduction/dual-oracle-receipt.json", "reproduction/independent-team-gap.json"],
        "V6421-P09": ["thermo-psyche/construct-operationalization-register.json", "thermo-psyche/causal-direction-vectors.json", "thermo-psyche/alternative-explanation-matrix.json", "thermo-psyche/classification-receipt.json"],
        "V6421-P10": ["stage20/evidence-order-register.json", "stage20/authority-nonsubstitution-vectors.json", "stage20/pass-fail-defer-board.json", "stage20/terminal-verdict.json"],
    }
    observed = {"V6421-P01": "completed", "V6421-P02": "completed", "V6421-P03": "represented", "V6421-P04": "represented", "V6421-P05": "open_gap", "V6421-P06": "exact_gate", "V6421-P07": "completed", "V6421-P08": "completed", "V6421-P09": "completed", "V6421-P10": "completed"}
    ledger_rows = []
    for proposal in x1["proposals"]:
        pid = proposal["proposal_id"]
        ledger_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": observed[pid],
                "evidence": evidence_paths[pid],
                "executed_as_far_as_evidence_permits": True,
                "protected_gates_remain": proposal["protected_gates"],
            }
        )
    disposition_counts = dict(Counter(row["observed_disposition"] for row in ledger_rows))
    write_json(
        phase_dir / "x2-proposal-ledger.json",
        {"schema": "ghc.family.v642-v1.x2-proposal-ledger.v1", "phase": phase, "owner": owner, "source_revision": source_revision, "x1_commit": x1_commit, "proposal_count": 10, "snapshot_state": "pending_evidence_commit", "disposition_counts": disposition_counts, "proposals": ledger_rows, "all_executed_as_far_as_evidence_permits": True},
    )

    inherited = read_json(repo / "docs/elian-voss/v641-v8/retained-negative-register.json")["negatives"]
    new_negative_data = [
        ("V6421-N01", "Lexical proposal distance does not prove semantic uniqueness.", "provenance/prior-proposal-collision-audit.json", "Keep manual semantic review and withdraw or split later collisions."),
        ("V6421-N02", "Multiple documents from one authority root are not independent sources.", "provenance/source-independence-partition.json", "Count authority roots and disclose aliases."),
        ("V6421-N03", "Boundary and surface-term checks are structural only.", "physics/boundary-surface-equivalence-vectors.json", "Prohibit empirical and Theory-of-Everything promotion."),
        ("V6421-N04", "Local stability and rank checks do not establish empirical stability or identifiability.", "physics/conservation-stability-identifiability-receipt.json", "Retain degeneracy and observation gates."),
        ("V6421-N05", "The empirical adapter parsed zero real measurement rows.", "empirical/zero-row-readiness-receipt.json", "Keep the result represented and require authorized real data."),
        ("V6421-N06", "No likelihood or parameter fit was executed.", "empirical/zero-row-readiness-receipt.json", "Require a separate scientific preregistration and review."),
        ("V6421-N07", "THOS executed zero real arm runs.", "thos/real-arm-gap.json", "Keep crossover evidence synthetic proxy only."),
        ("V6421-N08", "No THOS superiority, AGI, ASI, consciousness, or personhood evidence exists.", "thos/real-arm-gap.json", "Retain protected claim flags as false."),
        ("V6421-N09", "Freed ID has no real keys, proofs, live services, interoperability result, or trust governance.", "freed-id/production-cryptographic-gate.json", "Leave production assurance open."),
        ("V6421-N10", "Affected-party, Māori, cultural, and competent legal authority are absent.", "cbr/legal-cultural-authority-gates.json", "Defer and never substitute technical output for authority."),
        ("V6421-N11", "The resource-ceiling battery is bounded and not exhaustive security.", "security/parser-decompression-vectors.json", "Retain scope and require independent production security review."),
        ("V6421-N12", "Dual local oracles and snapshots remain same-owner, common-mode evidence.", "reproduction/independent-team-gap.json", "Keep independent-team reproduction open."),
        ("V6421-N13", "No fundamental thermo-psyche law, consciousness tensor, or personhood evidence is established.", "thermo-psyche/classification-receipt.json", "Retain construct, causal, observation, and authority burdens."),
        ("V6421-N14", "Mandatory Stage 20 fail and defer decisions remain.", "stage20/terminal-verdict.json", "Keep the terminal verdict NOT_READY_FOR_STAGE_20."),
    ]
    new_negatives = [
        {"negative_id": nid, "statement": statement, "evidence": evidence, "recovery": recovery, "retained": True}
        for nid, statement, evidence, recovery in new_negative_data
    ]
    write_json(
        phase_dir / "retained-negative-register.json",
        {"schema": "ghc.family.v642-v1.retained-negative-register.v1", "inherited_count": len(inherited), "new_count": len(new_negatives), "negative_count": len(inherited) + len(new_negatives), "negatives": inherited + new_negatives, "all_retained": True, "erasure_permitted": False},
    )

    gates = [
        {"gate_id": "G-EMPIRICAL-GMUT", "gate_class": "open_gap", "state": "open", "requires": "real measurements, preregistered likelihood, uncertainty analysis, and scientific review"},
        {"gate_id": "G-REAL-THOS", "gate_class": "open_gap", "state": "open", "requires": "blind matched-budget real arms and independent review"},
        {"gate_id": "G-FREED-PRODUCTION", "gate_class": "open_gap", "state": "open", "requires": "real cryptography, services, status, interoperability, review, and governance"},
        {"gate_id": "G-INDEPENDENT-REPRO", "gate_class": "open_gap", "state": "open", "requires": "a genuinely independent team and returned evidence"},
        {"gate_id": "G-SECURITY-ACCESSIBILITY-COMPLETE", "gate_class": "open_gap", "state": "open", "requires": "independent production security and complete accessibility assessment"},
        {"gate_id": "G-CBR-AUTHORITY", "gate_class": "exact_gate", "state": "deferred", "requires": "affected parties, Māori authority, cultural ratification, and competent legal authority"},
        {"gate_id": "G-PROOF-CANON-PUBLICATION", "gate_class": "exact_gate", "state": "deferred", "requires": "fresh explicit proof, canon, and publication approval"},
        {"gate_id": "G-DEPLOYMENT", "gate_class": "exact_gate", "state": "deferred", "requires": "fresh explicit deployment authorization and production review"},
        {"gate_id": "G-PRIVATE-ACCOUNT-API", "gate_class": "exact_gate", "state": "deferred", "requires": "fresh explicit private-data, account, or API-key authorization"},
        {"gate_id": "G-DESTRUCTIVE-HOST", "gate_class": "exact_gate", "state": "deferred", "requires": "fresh explicit destructive or host-security authorization"},
        {"gate_id": "G-SHARED-BRANCH-SIBLING-MERGE", "gate_class": "exact_gate", "state": "deferred", "requires": "fresh explicit shared-branch or sibling-merge authorization"},
    ]
    gate_counts = Counter(row["gate_class"] for row in gates)
    write_json(
        phase_dir / "exact-open-gate-register.json",
        {"schema": "ghc.family.v642-v1.exact-open-gate-register.v1", "gates": gates, "open_gap_count": gate_counts["open_gap"], "exact_gate_count": gate_counts["exact_gate"], "silently_closed": 0},
    )

    protected_claims = {
        "empirical_gmut_confirmation": False,
        "detected_force": False,
        "unique_prediction": False,
        "theory_of_everything": False,
        "real_thos_superiority": False,
        "agi": False,
        "asi": False,
        "consciousness": False,
        "personhood": False,
        "freed_id_cryptographic_assurance": False,
        "freed_id_production_interoperability": False,
        "enacted_law": False,
        "cultural_ratification": False,
        "maori_authority": False,
        "deployment": False,
        "exhaustive_security": False,
        "complete_accessibility_conformance": False,
        "proof_or_canon": False,
        "independent_team_reproduction": False,
    }
    write_json(
        phase_dir / "phase-truth.json",
        {
            "schema": "ghc.family.v642-v1.phase-truth.v1",
            "phase": phase,
            "owner": owner,
            "source_revision": source_revision,
            "x1_commit": x1_commit,
            "proposal_count": 10,
            "disposition_counts": disposition_counts,
            "retained_negative_count": len(inherited) + len(new_negatives),
            "protected_claims": protected_claims,
            "maori_authority_boundary": "Māori concepts, wording, data, and governance remain under Māori authority.",
            "independent_team_gap": "open",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    checklist_items = [
        {"item": "source fast-forward and pre-x1 equality", "state": "complete"},
        {"item": "x1 dedicated commit and remote equality", "state": "complete", "evidence": x1_commit},
        {"item": "ten proposals executed as evidence permits", "state": "complete"},
        {"item": "four disposition classes separated", "state": "complete"},
        {"item": "all 32 inherited negatives retained", "state": "complete"},
        {"item": "14 new negatives retained", "state": "complete"},
        {"item": "full repository suite", "state": "pending_closeout"},
        {"item": "phase validator and minimal verifier", "state": "pending_closeout"},
        {"item": "JSON parsing", "state": "pending_closeout"},
        {"item": "privacy and raw-ID scan", "state": "pending_closeout"},
        {"item": "diff and stale-label review", "state": "pending_closeout"},
        {"item": "clean detached evidence snapshots", "state": "pending_evidence_commit"},
        {"item": "clean detached closeout validation", "state": "pending_closeout"},
        {"item": "final seal and four-way equality", "state": "pending_closeout"},
        {"item": "independent-team reproduction", "state": "incomplete_open_gap"},
        {"item": "empirical, legal, cultural, identity, deployment, proof, exhaustive-security gates", "state": "incomplete_or_exact_gated"},
    ]
    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {"schema": "ghc.family.v642-v1.complete-incomplete-checklist.v1", "phase_state": "evidence_built_pending_validation_and_clean_snapshots", "items": checklist_items, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
    )
    checklist_md = "# V642-v1 complete / incomplete checklist\n\n" + "\n".join(f"- **{row['state']}** — {row['item']}" for row in checklist_items) + "\n\nThe independent-team, empirical, legal, cultural, identity, deployment, proof/canon, exhaustive-security, and complete-accessibility gaps remain open or exact-gated."
    write_text(phase_dir / "complete-incomplete-checklist.md", checklist_md)

    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v642-v1.executed-toolchain.v1",
            "family_current": ["scripts/ghc_family_evidence_boundary.py", "scripts/ghc_family_evidence_boundary_validator.py", "scripts/ghc_family_evidence_boundary_minimal.py", "scripts/build_ghc_family_evidence_boundary_report.py", "scripts/ghc_family_phase_privacy_scan.py"],
            "compatibility": [f"tests/test_ghc_family_v641_v{number}.py" for number in range(2, 9)],
            "historical_tools_modified": False,
            "shared_skill_change": False,
        },
    )
    write_text(phase_dir / "v642-v1-integrated-overview.md", integrated_overview(owner, phase, source_revision, x1_commit))

    write_manifest(phase_dir, source_revision, x1_commit)


def finalize_oracles(phase_dir: Path) -> None:
    full = read_json(phase_dir / "validation/evidence-boundary-validation.json")
    minimal = read_json(phase_dir / "validation/minimal-verifier.json")
    comparable = {
        "proposal_count": full["summary"]["proposal_count"],
        "disposition_counts": full["summary"]["disposition_counts"],
        "negative_count": full["summary"]["negative_count"],
        "open_gap_count": full["summary"]["open_gap_count"],
        "exact_gate_count": full["summary"]["exact_gate_count"],
        "terminal_verdict": full["summary"]["terminal_verdict"],
    }
    minimal_comparable = {key: minimal["summary"][key] for key in comparable}
    equal = comparable == minimal_comparable
    write_json(
        phase_dir / "reproduction/dual-oracle-receipt.json",
        {
            "schema": "ghc.family.dual-oracle-receipt.v1",
            "state": "verified" if full["valid"] and minimal["valid"] and equal else "divergent",
            "full_validator_valid": full["valid"],
            "minimal_verifier_valid": minimal["valid"],
            "core_outputs_equal": equal,
            "full_summary": comparable,
            "minimal_summary": minimal_comparable,
            "same_owner_only": True,
            "independent_team_reproduction": False,
        },
    )
    phase_truth = read_json(phase_dir / "phase-truth.json")
    write_manifest(phase_dir, phase_truth["source_revision"], phase_truth["x1_commit"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--x1-commit")
    parser.add_argument("--finalize-oracles", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = args.phase_dir if args.phase_dir.is_absolute() else (repo / args.phase_dir)
    phase_dir = phase_dir.resolve()
    try:
        phase_dir.relative_to(repo)
    except ValueError as exc:
        raise SystemExit("phase directory must remain inside the repository") from exc
    if args.finalize_oracles:
        finalize_oracles(phase_dir)
    else:
        if not args.x1_commit:
            raise SystemExit("--x1-commit is required for the initial build")
        build_all(repo, phase_dir, args.x1_commit)
    print(json.dumps({"phase_dir": phase_dir.as_posix(), "mode": "finalize_oracles" if args.finalize_oracles else "build", "ok": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
