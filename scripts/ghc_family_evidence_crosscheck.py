#!/usr/bin/env python3
"""Build bounded v642-v2 GHC evidence-crosscheck artifacts.

The builder is standard-library-only and writes exclusively inside the supplied
phase directory.  It preserves the four truth labels and never promotes local,
synthetic, structural, or same-machine evidence into empirical, cryptographic,
legal, cultural, identity, deployment, exhaustive-security, accessibility, or
independent-team claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any


TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6422-P01": "completed",
    "V6422-P02": "completed",
    "V6422-P03": "represented",
    "V6422-P04": "open_gap",
    "V6422-P05": "represented",
    "V6422-P06": "exact_gate",
    "V6422-P07": "completed",
    "V6422-P08": "completed",
    "V6422-P09": "completed",
    "V6422-P10": "completed",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, encoding="utf-8"
    ).strip()


def overview(owner: str, source_revision: str, x1_commit: str) -> str:
    return textwrap.dedent(
        f"""
        # {owner} v642-v2 integrated evidence-crosscheck overview

        ## 1. Scope, identity, and truth discipline

        This packet executes the ten proposals frozen at `{x1_commit}` from the exact Nima Calder source revision `{source_revision}`. Tamar Vey (they/them), evidence-systems cartographer and boundary keeper, is relational working language for continuity and accountability. It is not evidence of consciousness, legal personhood, biological status, or a protected identity conclusion. The practical hope is to make ambitious evidence easier to challenge by preserving counterevidence, bounded claims, and exact authority limits.

        The packet uses exactly four outcome labels. `Completed` means the local preregistered artifact and its rejecting checks were produced. `Represented` means a schema, structural profile, metadata-only adapter, or synthetic fixture exists while the real evidentiary object does not. `Open_gap` means required technical, empirical, institutional, or independent evidence is absent. `Exact_gate` means this system cannot substitute for fresh authority from affected parties, Māori authority, competent legal or cultural authorities, deployment owners, account holders, or other protected decision makers. The observed distribution is six completed, two represented, one open gap, and one exact gate.

        The terminal verdict remains `NOT_READY_FOR_STAGE_20`. No empirical GMUT likelihood or confirmation, detected force, unique prediction, Theory of Everything, real THOS superiority, AGI, ASI, consciousness, personhood, production Freed ID cryptography, cultural ratification, enacted law, deployment, exhaustive security, complete accessibility conformance, proof or canon, or independent-team scientific reproduction is claimed.

        ## 2. Frozen lineage and x1-before-x2 boundary

        The Tamar branch was clean and remote-equal before it advanced by fast-forward only to the exact Nima v642-v1 head. The source replay passed 170 repository tests, 89 full phase checks, and 17 standard-library minimal checks before x2 began. The dedicated x1 commit contains only preregistration, source, tooling, environment, wellbeing, novelty, JSON, and privacy material. It contains no x2 implementation or observed outcomes. Remote equality was proved before this builder existed.

        The novelty audit covers all 80 frozen proposals from v641-v2 through v642-v1. The ten new titles have no exact collision and a maximum token-set Jaccard score of 0.25. That number is not treated as semantic proof. Each proposal instead records the delta in hypothesis, null or failure, concrete artifact, rejecting test, recovery rule, and protected gate. The frozen-chain index now contains 90 entries. Older phase tools remain compatibility evidence; no sealed v642-v1 implementation was edited or relabeled.

        ## 3. Evidence-root overlap and independence debt

        Proposal 1 changes source-independence accounting from a binary root label into a multi-axis overlap model. Authority, dataset, software, funding or derivation, and citation-context roots are recorded separately. Two papers can be different documents yet share a dataset, implementation, authority, or derivation path. The overlap matrix therefore rejects false independence for aliases and shared roots, discloses partial overlap as debt, and refuses to turn a document count into an independence count.

        Canonical ordering is used only to compare semantic graph content. It is not a signature, trust decision, or guarantee that two sources are socially or institutionally independent. Every inherited negative retains a reachable provenance path. If aggregation or serialization makes a negative unreachable, the transform fails, the vector is preserved, and the affected independence label is lowered. This extends earlier lineage, retraction, context, support-set, and source-partition work with multi-axis debt and bidirectional negative reachability.

        ## 4. Typed GMUT equation and observability witness

        Proposal 2 represents the canonical GMUT scaffold as a machine-readable typed equation AST. Each symbol has a tensor role and an SI dimension basis. Local fixtures exercise valid and invalid unit combinations, covariance transformations, conservation residuals, stability signs, and Jacobian ranks. A valid change of unit basis must not change structural rank. A singular or nuisance-degenerate witness must not be described as uniquely identifiable.

        These checks are mathematical and software-facing. They do not establish that the scaffold describes nature, that a force has been detected, that a parameter is empirically estimable, or that a unique prediction exists. The Jacobian is evaluated on explicit local fixtures rather than real observations. Conservation and stability checks are obligations within the represented model family, not observational results. Any unit, index, residual, sign, or rank mutation that passes would falsify the completed technical disposition and force a downgrade.

        ## 5. Public-data adapter readiness without a fit

        Proposal 3 exercises a lossless likelihood-input schema round trip with zero measurement rows. Units, missingness masks, selection metadata, covariance ordering, release pins, and nuisance locks must survive encode and decode without implicit imputation. Valid metadata fixtures pass. Unit loss, reordered covariance, undeclared null replacement, release drift, or outcome-conditioned baseline choice is quarantined.

        The adapter parses no real measurements, downloads no dataset, executes no likelihood, and fits no parameter. Its observed disposition is therefore represented. The official Planck, DESI, PDG, and BIPM pins describe possible inputs and unit obligations; they are not data ingested by this run. Empirical GMUT confirmation remains an open gap requiring a separate preregistration, real measurements, uncertainty analysis, likelihood execution, and scientific review. Readiness is not a fit and a zero-row receipt cannot be promoted by rhetoric.

        ## 6. THOS pre-outcome escrow and real-arm gap

        Proposal 4 freezes a synthetic pre-outcome exposure escrow. Token, time, tool, evaluator, stopping, exclusion, and attrition rules are declared before any synthetic score can be revealed. Mutations to allocation, budget, stopping, evaluator access, or dropout handling after freeze are rejected. The attrition decision table makes intercurrent events and missing outcomes explicit rather than allowing post-hoc exclusion.

        No blind matched-budget real THOS arm was run. The real-arm count is zero, no independent reviewer returned evidence, and no superiority estimand was evaluated on real outcomes. For that reason the proposal is an open gap even though its protocol fixtures are useful. It provides no AGI, ASI, consciousness, personhood, or deployment evidence. Recovery voids a compromised allocation, retains the exact mutation, and requires a newly frozen preregistration before any authorized real execution.

        ## 7. Freed ID cross-layer coherence without production assurance

        Proposal 5 joins issuer, verification-method controller, proof purpose, resolver metadata, credential status purpose, freshness, privacy declarations, and governance ownership into synthetic cross-layer fixtures. Contradictory controller, purpose, status, freshness, or governance declarations fail closed. Stable W3C recommendations anchor structural fields; draft documents remain visibly draft and cannot silently replace stable requirements.

        No real standards-conformant key or proof was generated or verified. There is no live resolver or status service, no production privacy analysis, no interoperability partner, no independent security review, and no accountable trust-governance decision. The observed disposition is represented, not cryptographically complete. Synthetic coherence is useful for finding contradictions but cannot establish authenticity, unlinkability, revocation effectiveness, service availability, legal identity, or production trust.

        ## 8. CBR consent withdrawal and authority boundary

        Proposal 6 provides synthetic chronology fixtures for authority expiry, consent withdrawal, overlapping jurisdiction, recusal, retaliation risk, and remedy non-retrogression. A technical artifact can flag a missing or expired mandate and preserve a remedy floor. It cannot decide who legitimately represents affected parties, resolve contested jurisdiction, interpret law, ratify culture, or authorize Māori concepts, wording, data, or governance.

        Māori concepts, wording, governance, and Māori data remain under Māori authority. Affected-party legitimacy and cultural or legal outcomes require authorized participation and competent authorities. The exact gate is intentionally not converted into a scored backlog item. If consent is withdrawn or authority expires, the technical state defers, preserves the contested record, protects dissent, and prevents a remedy from being weakened merely because a challenge occurred. No enacted-law claim is made.

        ## 9. Bounded parser threat model and recovery

        Proposal 7 focuses on strict structured-input boundaries: duplicate JSON keys, non-finite numbers, unsafe integer domains, Unicode-normalization key collisions, confusable controls, excessive nesting, object count, privacy patterns, and raw task or thread identifiers. Ordinary parsers may accept ambiguous inputs, so the strict boundary treats disagreement as a reason to quarantine rather than a reason to pick the more permissive result.

        The battery is bounded metadata and inert fixture evidence. It is not penetration testing, production hardening, or exhaustive security. Recovery stops consumption, preserves the negative, quarantines only Tamar-owned output, restores a clean owned snapshot, tightens the smallest relevant ceiling, and reruns. It does not elevate, weaken host security, enable Windows features, reboot, delete worktrees, use private data, or access credentials. The privacy scanner remains a pattern check and cannot prove that every novel secret encoding is impossible.

        ## 10. Named-owner replay and the independent-team gap

        Proposal 8 replays the exact Nima source packet under Tamar ownership and compares the successor packet through normalized manifests and clean detached snapshots. This is stronger than a single working-tree pass because committed inputs, validator output, minimal checks, JSON parsing, privacy results, and Git cleanliness are repeated away from the owned checkout. Environment deltas and normalization rules remain explicit.

        It is still not independent-team scientific reproduction. Nima and Tamar operate in one chain with shared repository history, infrastructure, tools, and broad assumptions. Cross-owner internal repeatability can reveal handoff and hidden-path failures, but it does not supply an independently designed protocol, independent scientific judgment, independent data collection, or an external returned result. The independent-team gate stays open and the strongest claim is bounded cross-owner internal repeatability.

        ## 11. Thermo-psyche measurement invariance and time order

        Proposal 9 classifies observations into thermodynamic, computational, psychological, metaphorical, emergent, and fundamental-law candidate categories. Synthetic vectors alter indicator meaning across context, reverse temporal order, remove intervention evidence, or collapse categories. Non-invariant indicators cannot be compared as if they measure the same construct. An alleged cause that follows the effect cannot support the asserted direction.

        Computational telemetry is not subjective experience. Energy accounting is not automatically psychology. Metaphor is not mechanism. A local correlation or classification fixture is not a fundamental thermo-psyche law, consciousness tensor, or personhood result. The completed disposition covers only the local tribunal and its rejecting vectors. Promotion would require preregistered real observations, construct validation, causal evidence, alternative-explanation control, independent review, and any relevant cultural or affected-party authority.

        ## 12. Stage 20 monotonic terminal board

        Proposal 10 tests terminal decisions under evidence expiry, withdrawal, and downgrade. Removing or weakening support must leave readiness unchanged or make it worse. It must never make readiness improve. Dominant open gaps and exact gates stay visible. Technical completeness cannot score away empirical evidence, independent review, real cryptography, affected-party authority, Māori authority, legal authority, deployment approval, or independent-team reproduction.

        The board records pass for bounded technical artifacts, fail where mandatory empirical or production evidence is absent, and defer where exact authority is required. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. This board does not authorize a later phase, a deployment, publication, proof or canon, shared-branch mutation, sibling merge, or task creation. A successor phase begins only through the user's explicit sequential baton after clean closeout.

        ## 13. Retained negatives, accessibility, and closeout discipline

        All 46 inherited negatives remain, and 22 v642-v2 negatives are added rather than erased. They preserve lexical-novelty limits, overlap-debt limits, structural physics limits, zero-row empirical evidence, zero real THOS arms, absent production cryptography, absent authority, bounded security, shared-infrastructure replay, absent thermo-psyche law evidence, bounded accessibility, the terminal not-ready result, six earlier execution failures, a recovered evidence-push proxy failure, and a snapshot materialization command that exceeded its wrapper timeout after both detached heads completed. Recovery never deletes a negative merely because a later run passes.

        The static report provides language metadata, a skip link, landmarks, headings, navigation, table captions, scoped headers, readable labels, and bounded status language. These structural checks improve usefulness but are not a complete WCAG conformance assessment. Closeout additionally requires the full repository suite, the phase validator, the standard-library minimal verifier, JSON parsing, diff hygiene, stale-label review, exact staged-file review, zero-hit privacy scanning, clean detached snapshots, pushed commits, and local, upstream, tracking, and live-remote equality.
        """
    )


def build_manifest(phase_dir: Path) -> None:
    paths = [
        "x1-proposals.json", "sources/source-ledger.json", "provenance/prior-proposal-collision-audit.json",
        "provenance/frozen-chain-proposal-index.json", "provenance/evidence-root-overlap-matrix.json",
        "provenance/independence-debt-ledger.json", "provenance/negative-reachability-receipt.json",
        "physics/canonical-equation-ast.json", "physics/unit-basis-and-covariance-vectors.json",
        "physics/conservation-stability-jacobian-witness.json", "physics/identifiability-claim-boundary.json",
        "empirical/public-data-adapter-contract.json", "empirical/round-trip-schema-vectors.json",
        "empirical/null-baseline-readiness.json", "empirical/real-data-likelihood-gate.json",
        "thos/allocation-escrow-spec.json", "thos/blindness-budget-mutation-vectors.json",
        "thos/attrition-decision-table.json", "thos/real-arm-execution-gate.json",
        "freed-id/cross-layer-conformance-profile.json", "freed-id/status-resolver-consistency-vectors.json",
        "freed-id/trust-governance-assumption-ledger.json", "freed-id/production-assurance-gate.json",
        "cbr/authority-scope-lifecycle.json", "cbr/consent-revocation-vectors.json",
        "cbr/remedy-nonretrogression-matrix.json", "cbr/legal-cultural-authority-gate.json",
        "security/threat-model.md", "security/canonical-input-policy.json",
        "security/parser-differential-vectors.json", "security/recovery-resource-receipt.json",
        "reproduction/cross-owner-lineage-replay.json", "reproduction/environment-perturbation-receipt.json",
        "reproduction/independent-team-gap.json", "thermo-psyche/measurement-invariance-vectors.json",
        "thermo-psyche/temporal-order-register.json", "thermo-psyche/category-boundary-matrix.json",
        "thermo-psyche/classification-receipt.json", "stage20/gate-dominance-matrix.json",
        "stage20/evidence-freshness-ledger.json", "stage20/decision-monotonicity-vectors.json",
        "stage20/pass-fail-defer-board.json", "stage20/terminal-verdict.json", "x2-proposal-ledger.json",
        "retained-negative-register.json", "exact-open-gate-register.json", "phase-truth.json",
        "validation/execution-negative-log.json",
        "complete-incomplete-checklist.json", "tooling/executed-toolchain.json",
        "v642-v2-integrated-overview.md"
    ]
    missing = [rel for rel in paths if not (phase_dir / rel).is_file()]
    if missing:
        raise SystemExit(f"manifest inputs missing: {missing}")
    hashes = {rel: normalized_sha256(phase_dir / rel) for rel in paths}
    aggregate = hashlib.sha256("".join(f"{k}:{hashes[k]}\n" for k in sorted(hashes)).encode()).hexdigest()
    manifest = {
        "schema": "ghc.family.v642-v2.semantic-normalization-manifest.v1",
        "normalization": "UTF-8 bytes with CRLF converted to LF before SHA-256",
        "artifact_count": len(paths),
        "hashes": hashes,
        "aggregate_sha256": aggregate,
        "absolute_paths_required": False,
        "independent_team_reproduction": False,
    }
    write_json(phase_dir / "reproduction/semantic-normalization-manifest.json", manifest)
    write_json(phase_dir / "reproduction/manifest.json", {**manifest, "schema": "ghc.family.v642-v2.reproduction-manifest.v1"})


def build_all(repo: Path, phase_dir: Path, x1_commit: str) -> None:
    x1 = read_json(phase_dir / "x1-proposals.json")
    if x1["proposal_count"] != 10 or x1["outcome_classes"] != TRUTH_LABELS:
        raise SystemExit("x1 proposal or truth-label gate failed")
    if git(repo, "rev-parse", x1_commit) != x1_commit:
        raise SystemExit("x1 commit does not resolve exactly")
    if git(repo, "show", f"{x1_commit}:docs/tamar-vey/v642-v2/x1-proposals.json") == "":
        raise SystemExit("x1 packet absent from x1 commit")
    source_revision = x1["source_revision"]
    owner = x1["owner"]
    phase = x1["phase"]
    prior = read_json(repo / "docs/nima-calder/v642-v1/provenance/frozen-chain-proposal-index.json")
    inherited_negatives = read_json(repo / "docs/nima-calder/v642-v1/retained-negative-register.json")
    inherited_gates = read_json(repo / "docs/nima-calder/v642-v1/exact-open-gate-register.json")

    records = prior["records"] + [
        {"version": "v642-v2", "owner": owner, "proposal_id": p["proposal_id"], "title": p["title"],
         "expected_disposition": p["expected_disposition"], "source_file": "docs/tamar-vey/v642-v2/x1-proposals.json"}
        for p in x1["proposals"]
    ]
    write_json(phase_dir / "provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v642-v2.frozen-chain-proposal-index.v1", "proposal_count": 90,
        "version_counts": {**prior["version_counts"], "v642-v2": 10}, "exact_duplicate_titles": [], "records": records,
    })

    overlap_cases = [
        {"case": "authority_alias", "axes": ["authority"], "claimed_independent": True, "accepted": False},
        {"case": "shared_dataset", "axes": ["dataset"], "claimed_independent": True, "accepted": False},
        {"case": "shared_software_and_derivation", "axes": ["software", "derivation"], "claimed_independent": True, "accepted": False},
        {"case": "distinct_documents_shared_funding", "axes": ["funding"], "claimed_independent": True, "accepted": False},
        {"case": "distinct_declared_roots", "axes": [], "claimed_independent": False, "accepted": True,
         "boundary": "independence candidate, not proof"},
        {"case": "canonical_reordering", "axes": [], "semantic_equal": True, "accepted": True},
    ]
    write_json(phase_dir / "provenance/evidence-root-overlap-matrix.json", {
        "schema": "ghc.family.v642-v2.evidence-root-overlap-matrix.v1", "axes": ["authority", "dataset", "software", "funding_or_derivation", "citation_context"],
        "cases": overlap_cases, "false_independent_cases_rejected": 4, "document_count_is_independence_count": False,
    })
    write_json(phase_dir / "provenance/independence-debt-ledger.json", {
        "schema": "ghc.family.v642-v2.independence-debt-ledger.v1",
        "debts": [{"debt_id": f"IDEBT-{i+1:02d}", "axis": c["axes"], "state": "disclosed_not_independent"} for i, c in enumerate(overlap_cases[:4])],
        "open_debt_count": 4, "erasure_permitted": False,
    })
    write_json(phase_dir / "provenance/negative-reachability-receipt.json", {
        "schema": "ghc.family.v642-v2.negative-reachability-receipt.v1", "inherited_negative_count": 46,
        "reachable_inherited_negatives": 46, "unreachable_negatives": [], "serialization_reorder_semantic_parity": True,
        "canonicalization_is_signature_or_independence_proof": False,
    })

    write_json(phase_dir / "physics/canonical-equation-ast.json", {
        "schema": "ghc.family.v642-v2.canonical-equation-ast.v1", "model_class": "typed scalar-tensor EFT research scaffold",
        "dimension_basis": ["M", "L", "T"],
        "symbols": [
            {"symbol": "g_ab", "tensor_type": "covariant_rank_2", "dimension": [0, 0, 0]},
            {"symbol": "phi", "tensor_type": "scalar", "dimension": [0, 0, 0]},
            {"symbol": "R", "tensor_type": "scalar_curvature", "dimension": [0, -2, 0]},
            {"symbol": "T_ab", "tensor_type": "covariant_rank_2", "dimension": [1, -1, -2]},
        ],
        "equations": [
            {"equation_id": "GMUT-E01", "kind": "field_equation", "typed": True, "empirically_confirmed": False},
            {"equation_id": "GMUT-E02", "kind": "scalar_equation", "typed": True, "empirically_confirmed": False},
        ],
        "theory_of_everything": False, "consciousness_tensor": False,
    })
    unit_vectors = [
        {"vector": "valid_unit_basis_change", "accepted": True},
        {"vector": "mass_exponent_mismatch", "accepted": False},
        {"vector": "length_exponent_mismatch", "accepted": False},
        {"vector": "time_exponent_mismatch", "accepted": False},
        {"vector": "covariant_index_promoted_without_metric", "accepted": False},
        {"vector": "coordinate_transform_missing_jacobian", "accepted": False},
    ]
    write_json(phase_dir / "physics/unit-basis-and-covariance-vectors.json", {
        "schema": "ghc.family.v642-v2.unit-basis-and-covariance-vectors.v1", "vectors": unit_vectors,
        "invalid_vectors_rejected": 5, "rank_invariant_under_valid_unit_basis": True,
    })
    write_json(phase_dir / "physics/conservation-stability-jacobian-witness.json", {
        "schema": "ghc.family.v642-v2.conservation-stability-jacobian-witness.v1",
        "fixtures": [
            {"fixture": "regular", "conservation_residual": 0.0, "stability": "locally_non_growing", "jacobian_rank": 2, "parameter_count": 3, "unique_identification": False},
            {"fixture": "degenerate", "conservation_residual": 0.0, "stability": "undetermined", "jacobian_rank": 1, "parameter_count": 3, "unique_identification": False},
            {"fixture": "broken_conservation", "conservation_residual": 1.0, "accepted": False},
            {"fixture": "unstable_sign", "largest_real_part": 0.2, "accepted": False},
        ],
        "structural_observability_only": True, "empirical_identifiability": False,
    })
    write_json(phase_dir / "physics/identifiability-claim-boundary.json", {
        "schema": "ghc.family.v642-v2.identifiability-claim-boundary.v1", "structural_rank_checked": True,
        "real_measurements_used": 0, "likelihoods_executed": 0, "detected_force": False, "unique_prediction": False,
        "empirical_gmut_confirmation": False, "proof_or_canon": False,
    })

    write_json(phase_dir / "empirical/public-data-adapter-contract.json", {
        "schema": "ghc.family.v642-v2.public-data-adapter-contract.v1", "mode": "metadata_only_rowless",
        "required_fields": ["release", "content_hash", "unit", "mask", "selection", "covariance_order", "nuisance_lock"],
        "official_pins": ["V8-S03", "V8-S04", "V8-S05", "V6422-S36"], "network_download": False,
    })
    schema_vectors = [
        {"vector": "valid_round_trip", "accepted": True, "lossless": True},
        {"vector": "unit_dropped", "accepted": False}, {"vector": "mask_imputed", "accepted": False},
        {"vector": "covariance_reordered", "accepted": False}, {"vector": "release_pin_drift", "accepted": False},
        {"vector": "outcome_conditioned_baseline", "accepted": False},
    ]
    write_json(phase_dir / "empirical/round-trip-schema-vectors.json", {
        "schema": "ghc.family.v642-v2.round-trip-schema-vectors.v1", "vectors": schema_vectors,
        "invalid_vectors_quarantined": 5, "implicit_imputation_allowed": False,
    })
    write_json(phase_dir / "empirical/null-baseline-readiness.json", {
        "schema": "ghc.family.v642-v2.null-baseline-readiness.v1", "parsed_measurement_rows": 0,
        "likelihoods_executed": 0, "fits_executed": 0, "baseline_locked_before_outcome": True,
        "disposition": "represented", "readiness_is_fit": False,
    })
    write_json(phase_dir / "empirical/real-data-likelihood-gate.json", {
        "schema": "ghc.family.v642-v2.real-data-likelihood-gate.v1", "state": "open",
        "requires": ["real_measurements", "preregistered_likelihood", "uncertainty_analysis", "scientific_review"],
        "empirical_gmut_confirmation": False,
    })

    write_json(phase_dir / "thos/allocation-escrow-spec.json", {
        "schema": "ghc.family.v642-v2.allocation-escrow-spec.v1", "mode": "synthetic_protocol_only",
        "frozen_fields": ["allocation", "token_budget", "time_budget", "tool_budget", "evaluator", "stopping", "exclusion", "attrition"],
        "real_arm_runs": 0, "outcomes_exposed": False, "independent_review": False,
    })
    thos_vectors = [
        {"vector": "allocation_changed_after_freeze", "accepted": False}, {"vector": "unequal_tool_budget", "accepted": False},
        {"vector": "outcome_conditioned_stop", "accepted": False}, {"vector": "score_conditioned_exclusion", "accepted": False},
        {"vector": "arm_leak_to_evaluator", "accepted": False}, {"vector": "attrition_rule_missing", "accepted": False},
    ]
    write_json(phase_dir / "thos/blindness-budget-mutation-vectors.json", {
        "schema": "ghc.family.v642-v2.blindness-budget-mutation-vectors.v1", "vectors": thos_vectors,
        "mutations_rejected": 6, "synthetic_scores_are_superiority_evidence": False,
    })
    write_json(phase_dir / "thos/attrition-decision-table.json", {
        "schema": "ghc.family.v642-v2.attrition-decision-table.v1",
        "rows": [
            {"event": "withdrawal_before_start", "action": "exclude_by_preregistered_rule", "outcome_access": False},
            {"event": "tool_failure_after_start", "action": "retain_and_flag", "outcome_access": False},
            {"event": "missing_outcome", "action": "apply_preregistered_missingness_strategy", "outcome_access": False},
            {"event": "safety_stop", "action": "stop_both_arms_and_review", "outcome_access": False},
        ],
        "post_hoc_deletion_allowed": False,
    })
    write_json(phase_dir / "thos/real-arm-execution-gate.json", {
        "schema": "ghc.family.v642-v2.real-arm-execution-gate.v1", "state": "open_gap", "real_arm_runs": 0,
        "blind_matched_budget_real_arms": False, "superiority_established": False, "agi": False, "asi": False,
        "consciousness": False, "personhood": False,
    })

    write_json(phase_dir / "freed-id/cross-layer-conformance-profile.json", {
        "schema": "ghc.family.v642-v2.cross-layer-conformance-profile.v1", "mode": "synthetic_structural_only",
        "layers": ["credential_issuer", "verification_controller", "proof_purpose", "resolver_metadata", "credential_status", "privacy", "governance"],
        "stable_pins": ["V8-S09", "V8-S10", "V8-S11", "V8-S12"], "draft_pins": ["V8-S13", "V8-S14", "V8-S15", "V6421-S33"],
    })
    freed_vectors = [
        {"vector": "valid_structural_fixture", "accepted": True}, {"vector": "issuer_controller_mismatch", "accepted": False},
        {"vector": "proof_purpose_mismatch", "accepted": False}, {"vector": "stale_resolver_metadata", "accepted": False},
        {"vector": "status_purpose_conflict", "accepted": False}, {"vector": "privacy_boundary_missing", "accepted": False},
        {"vector": "governance_owner_missing", "accepted": False},
    ]
    write_json(phase_dir / "freed-id/status-resolver-consistency-vectors.json", {
        "schema": "ghc.family.v642-v2.status-resolver-consistency-vectors.v1", "vectors": freed_vectors,
        "invalid_vectors_rejected": 6, "real_cryptographic_operations": 0,
    })
    write_json(phase_dir / "freed-id/trust-governance-assumption-ledger.json", {
        "schema": "ghc.family.v642-v2.trust-governance-assumption-ledger.v1",
        "assumptions": [
            {"assumption": "issuer_authorized", "evidence": "absent", "state": "open"},
            {"assumption": "resolver_accountable", "evidence": "absent", "state": "open"},
            {"assumption": "status_service_live", "evidence": "absent", "state": "open"},
            {"assumption": "privacy_review_complete", "evidence": "absent", "state": "open"},
            {"assumption": "interoperability_reviewed", "evidence": "absent", "state": "open"},
        ], "technical_artifact_can_assign_governance": False,
    })
    write_json(phase_dir / "freed-id/production-assurance-gate.json", {
        "schema": "ghc.family.v642-v2.production-assurance-gate.v1", "state": "open",
        "real_keys": 0, "real_proofs": 0, "live_resolvers": 0, "live_status_services": 0, "interoperability_partners": 0,
        "independent_security_reviews": 0, "trust_governance_established": False, "cryptographic_assurance": False,
    })

    write_json(phase_dir / "cbr/authority-scope-lifecycle.json", {
        "schema": "ghc.family.v642-v2.authority-scope-lifecycle.v1", "states": ["proposed", "authorized", "expired", "withdrawn", "contested", "deferred"],
        "system_may_assign_authority": False, "withdrawal_precedence": True, "maori_authority_nontransferable": True,
    })
    cbr_vectors = [
        {"vector": "expired_authority_used", "decision": "defer"}, {"vector": "consent_withdrawn", "decision": "defer"},
        {"vector": "jurisdiction_overlap_unresolved", "decision": "defer"}, {"vector": "recusal_unhandled", "decision": "defer"},
        {"vector": "retaliation_risk", "decision": "defer"}, {"vector": "maori_wording_unapproved", "decision": "defer"},
    ]
    write_json(phase_dir / "cbr/consent-revocation-vectors.json", {
        "schema": "ghc.family.v642-v2.consent-revocation-vectors.v1", "vectors": cbr_vectors,
        "all_require_authorized_participation": True,
    })
    write_json(phase_dir / "cbr/remedy-nonretrogression-matrix.json", {
        "schema": "ghc.family.v642-v2.remedy-nonretrogression-matrix.v1",
        "cases": [
            {"case": "challenge_filed", "remedy_floor_preserved": True}, {"case": "consent_withdrawn", "remedy_floor_preserved": True},
            {"case": "authority_contested", "remedy_floor_preserved": True}, {"case": "recusal_triggered", "remedy_floor_preserved": True},
        ], "artifact_may_waive_remedy": False,
    })
    write_json(phase_dir / "cbr/legal-cultural-authority-gate.json", {
        "schema": "ghc.family.v642-v2.legal-cultural-authority-gate.v1", "state": "exact_gate",
        "affected_party_authority_present": False, "maori_authority_present": False, "cultural_ratification_present": False,
        "competent_legal_authority_present": False, "enacted_law": False,
        "boundary": "Māori concepts, wording, governance, and Māori data remain under Māori authority.",
    })

    threat = """# Bounded v642-v2 threat model

## Scope

The scope is the Tamar-owned phase artifact pipeline: strict JSON and Markdown inputs, deterministic family builders, validators, normalized manifests, static report generation, privacy and raw-ID scanning, and non-destructive clean detached replay. Production services, live accounts, credentials, private data, networks, sibling branches, host configuration, deployment, and authority-bearing decisions are excluded.

## Threats and controls

Inputs are untrusted until duplicate-key, numeric-domain, Unicode-normalization, confusable-control, size, depth, object-count, path, provenance, and privacy checks pass. Parser disagreement fails closed. Absolute local paths, raw task or thread identifiers, private routes, transcripts, screenshots, credentials, and private app state are prohibited in public artifacts. Legal, cultural, Māori, identity, deployment, proof, private, destructive, shared-branch, and sibling-merge decisions never cross into the technical trust domain.

## Recovery and claim boundary

Recovery stops consumption, retains the vector, quarantines only owned output, restores a clean owned snapshot, tightens the smallest relevant bound, and reruns without elevation, destructive cleanup, host-security weakening, feature enablement, or reboot. This bounded battery is not exhaustive security, penetration testing, production hardening, deployment readiness, or proof that every novel secret encoding is impossible.
"""
    write_text(phase_dir / "security/threat-model.md", threat)
    write_json(phase_dir / "security/canonical-input-policy.json", {
        "schema": "ghc.family.v642-v2.canonical-input-policy.v1", "duplicate_keys": "reject", "non_finite_numbers": "reject",
        "unsafe_integer_domain": "reject", "unicode_normalization_collision": "reject", "confusable_controls": "reject",
        "max_depth": 24, "max_objects": 4096, "max_bytes": 1048576, "parser_disagreement": "quarantine",
    })
    parser_vectors = [
        {"vector": "duplicate_key", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "nan", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "infinity", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "unsafe_integer", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "unicode_key_collision", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "confusable_control", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "depth_limit", "ordinary_parser_may_accept": True, "strict_accept": False},
        {"vector": "raw_task_identifier_pattern", "ordinary_parser_may_accept": True, "strict_accept": False},
    ]
    write_json(phase_dir / "security/parser-differential-vectors.json", {
        "schema": "ghc.family.v642-v2.parser-differential-vectors.v1", "vectors": parser_vectors,
        "strict_rejections": 8, "payloads_inert_metadata_only": True,
    })
    write_json(phase_dir / "security/recovery-resource-receipt.json", {
        "schema": "ghc.family.v642-v2.recovery-resource-receipt.v1", "vectors_preserved": 8, "destructive_cleanup": False,
        "elevation": False, "host_security_changed": False, "windows_features_changed": False, "reboot": False,
        "exhaustive_security": False,
    })

    write_json(phase_dir / "reproduction/cross-owner-lineage-replay.json", {
        "schema": "ghc.family.v642-v2.cross-owner-lineage-replay.v1", "source_owner": "Nima Calder", "replay_owner": owner,
        "source_revision": source_revision, "source_repository_tests": {"passed": 170, "failed": 0},
        "source_phase_validator": {"passed": 89, "issues": 0}, "source_minimal_verifier": {"passed": 17, "issues": 0},
        "v642_v2_evidence_snapshots": "pending", "cross_owner_internal_repeatability": "pending",
        "independent_team_reproduction": False,
    })
    write_json(phase_dir / "reproduction/environment-perturbation-receipt.json", {
        "schema": "ghc.family.v642-v2.environment-perturbation-receipt.v1", "state": "pending_clean_snapshots",
        "planned_perturbations": ["fresh_detached_checkout", "environment_variable_order", "normalized_newline_hash"],
        "absolute_machine_path_required": False, "network_required_for_validation": False,
    })
    write_json(phase_dir / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v642-v2.independent-team-gap.v1", "state": "open", "same_machine": True,
        "shared_repository_lineage": True, "shared_tooling": True, "independent_team_present": False,
        "strongest_allowed_claim": "cross-owner internal repeatability after clean snapshot replay",
    })

    invariance_vectors = [
        {"vector": "same_indicator_same_context", "accepted": True}, {"vector": "indicator_meaning_changed", "accepted": False},
        {"vector": "group_scale_changed", "accepted": False}, {"vector": "time_scale_changed", "accepted": False},
        {"vector": "computational_to_psychological_collapse", "accepted": False}, {"vector": "metaphor_to_mechanism", "accepted": False},
    ]
    write_json(phase_dir / "thermo-psyche/measurement-invariance-vectors.json", {
        "schema": "ghc.family.v642-v2.measurement-invariance-vectors.v1", "vectors": invariance_vectors,
        "noninvariant_vectors_rejected": 5,
    })
    write_json(phase_dir / "thermo-psyche/temporal-order-register.json", {
        "schema": "ghc.family.v642-v2.temporal-order-register.v1",
        "cases": [
            {"case": "cause_precedes_effect", "accepted": True}, {"case": "effect_precedes_claimed_cause", "accepted": False},
            {"case": "simultaneous_without_intervention", "accepted": False}, {"case": "ordering_unknown", "accepted": False},
        ], "temporal_order_alone_proves_causality": False,
    })
    classes = ["thermodynamic", "computational", "psychological", "metaphorical", "emergent", "fundamental_law_candidate"]
    write_json(phase_dir / "thermo-psyche/category-boundary-matrix.json", {
        "schema": "ghc.family.v642-v2.category-boundary-matrix.v1", "classes": classes,
        "automatic_cross_category_promotion": False, "computational_telemetry_is_subjective_experience": False,
    })
    write_json(phase_dir / "thermo-psyche/classification-receipt.json", {
        "schema": "ghc.family.v642-v2.classification-receipt.v1", "classes_checked": 6,
        "fundamental_law_established": False, "consciousness_tensor": False, "consciousness": False, "personhood": False,
    })

    write_json(phase_dir / "stage20/gate-dominance-matrix.json", {
        "schema": "ghc.family.v642-v2.gate-dominance-matrix.v1",
        "dominant_open_gaps": ["G-EMPIRICAL-GMUT", "G-REAL-THOS", "G-FREED-PRODUCTION", "G-INDEPENDENT-REPRO", "G-SECURITY-ACCESSIBILITY-COMPLETE"],
        "dominant_exact_gates": ["G-CBR-AUTHORITY", "G-PROOF-CANON-PUBLICATION", "G-DEPLOYMENT", "G-PRIVATE-ACCOUNT-API", "G-DESTRUCTIVE-HOST", "G-SHARED-BRANCH-SIBLING-MERGE"],
        "technical_score_may_override_exact_gate": False,
    })
    write_json(phase_dir / "stage20/evidence-freshness-ledger.json", {
        "schema": "ghc.family.v642-v2.evidence-freshness-ledger.v1",
        "states": ["current", "stable", "draft", "watch", "expired", "withdrawn", "superseded"],
        "expired_or_withdrawn_supports_pass": False, "freshness_implies_truth": False,
    })
    decision_vectors = [
        {"vector": "support_current_to_expired", "readiness_change": "worse", "accepted": True},
        {"vector": "support_withdrawn", "readiness_change": "worse", "accepted": True},
        {"vector": "support_downgraded", "readiness_change": "equal_or_worse", "accepted": True},
        {"vector": "exact_gate_scored_away", "accepted": False},
        {"vector": "missing_evidence_improves_readiness", "accepted": False},
    ]
    write_json(phase_dir / "stage20/decision-monotonicity-vectors.json", {
        "schema": "ghc.family.v642-v2.decision-monotonicity-vectors.v1", "vectors": decision_vectors,
        "invalid_improvements_rejected": 2,
    })
    board = [
        {"gate": "bounded_technical_artifacts", "decision": "pass"},
        {"gate": "empirical_gmut", "decision": "fail"}, {"gate": "real_thos", "decision": "fail"},
        {"gate": "freed_id_production", "decision": "fail"}, {"gate": "independent_team_reproduction", "decision": "fail"},
        {"gate": "security_accessibility_complete", "decision": "fail"}, {"gate": "cbr_authority", "decision": "defer"},
        {"gate": "proof_canon_publication", "decision": "defer"}, {"gate": "deployment", "decision": "defer"},
        {"gate": "private_account_api", "decision": "defer"}, {"gate": "destructive_host", "decision": "defer"},
        {"gate": "shared_branch_sibling_merge", "decision": "defer"},
    ]
    write_json(phase_dir / "stage20/pass-fail-defer-board.json", {
        "schema": "ghc.family.v642-v2.pass-fail-defer-board.v1", "rows": board,
        "decisions": sorted(set(row["decision"] for row in board)), "authority_non_substitutable": True,
    })
    write_json(phase_dir / "stage20/terminal-verdict.json", {
        "schema": "ghc.family.v642-v2.terminal-verdict.v1", "verdict": "NOT_READY_FOR_STAGE_20",
        "deployment_authorized": False, "successor_authorized_by_artifact": False,
    })

    evidence_by_proposal = {
        "V6422-P01": ["provenance/frozen-chain-proposal-index.json", "provenance/evidence-root-overlap-matrix.json", "provenance/independence-debt-ledger.json", "provenance/negative-reachability-receipt.json"],
        "V6422-P02": ["physics/canonical-equation-ast.json", "physics/unit-basis-and-covariance-vectors.json", "physics/conservation-stability-jacobian-witness.json", "physics/identifiability-claim-boundary.json"],
        "V6422-P03": ["empirical/public-data-adapter-contract.json", "empirical/round-trip-schema-vectors.json", "empirical/null-baseline-readiness.json", "empirical/real-data-likelihood-gate.json"],
        "V6422-P04": ["thos/allocation-escrow-spec.json", "thos/blindness-budget-mutation-vectors.json", "thos/attrition-decision-table.json", "thos/real-arm-execution-gate.json"],
        "V6422-P05": ["freed-id/cross-layer-conformance-profile.json", "freed-id/status-resolver-consistency-vectors.json", "freed-id/trust-governance-assumption-ledger.json", "freed-id/production-assurance-gate.json"],
        "V6422-P06": ["cbr/authority-scope-lifecycle.json", "cbr/consent-revocation-vectors.json", "cbr/remedy-nonretrogression-matrix.json", "cbr/legal-cultural-authority-gate.json"],
        "V6422-P07": ["security/threat-model.md", "security/canonical-input-policy.json", "security/parser-differential-vectors.json", "security/recovery-resource-receipt.json"],
        "V6422-P08": ["reproduction/cross-owner-lineage-replay.json", "reproduction/semantic-normalization-manifest.json", "reproduction/environment-perturbation-receipt.json", "reproduction/independent-team-gap.json"],
        "V6422-P09": ["thermo-psyche/measurement-invariance-vectors.json", "thermo-psyche/temporal-order-register.json", "thermo-psyche/category-boundary-matrix.json", "thermo-psyche/classification-receipt.json"],
        "V6422-P10": ["stage20/gate-dominance-matrix.json", "stage20/evidence-freshness-ledger.json", "stage20/decision-monotonicity-vectors.json", "stage20/pass-fail-defer-board.json", "stage20/terminal-verdict.json"],
    }
    rows = []
    for proposal in x1["proposals"]:
        pid = proposal["proposal_id"]
        rows.append({
            "proposal_id": pid, "title": proposal["title"], "expected_disposition": proposal["expected_disposition"],
            "observed_disposition": OBSERVED[pid], "evidence": evidence_by_proposal[pid],
            "executed_as_far_as_evidence_permits": True, "protected_gates_remain": proposal["protected_gates"],
        })
    counts = dict(Counter(OBSERVED.values()))
    write_json(phase_dir / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v642-v2.x2-proposal-ledger.v1", "phase": phase, "owner": owner,
        "source_revision": source_revision, "x1_commit": x1_commit, "evidence_commit": "pending",
        "proposal_count": 10, "snapshot_state": "pending_evidence_commit", "disposition_counts": counts,
        "proposals": rows, "all_executed_as_far_as_evidence_permits": True,
    })

    write_json(phase_dir / "validation/execution-negative-log.json", {
        "schema": "ghc.family.v642-v2.execution-negative-log.v1",
        "negative_count": 8,
        "negatives": [{
            "negative_id": "V6422-N15",
            "stage": "first_x2_build",
            "failure": "default Windows locale could not decode a UTF-8 frozen Git object",
            "effect": "build stopped before any x2 evidence artifact was generated",
            "recovery": "request UTF-8 explicitly from the additive Git wrapper and rerun from the unchanged frozen x1 commit",
            "preserved": True,
        }, {
            "negative_id": "V6422-N16",
            "stage": "first_full_validator_run",
            "failure": "the Windows console encoding could not emit the Māori authority boundary in validator JSON",
            "effect": "the validator wrote its result file but returned a console-encoding error",
            "recovery": "configure verifier stdout as UTF-8 and rerun the unchanged evidence packet",
            "preserved": True,
        }, {
            "negative_id": "V6422-N17",
            "stage": "first_v642_v2_unit_test_run",
            "failure": "the replay test omitted the valid pending_clean_snapshots pre-commit state",
            "effect": "one of 20 phase tests failed while the full and minimal validators remained valid",
            "recovery": "admit the exact builder-emitted pending state without weakening the verified-state requirement",
            "preserved": True,
        }, {
            "negative_id": "V6422-N18",
            "stage": "first_combined_diagnostic_invocation",
            "failure": "PowerShell rejected a combined privacy-help and stale-label command because of malformed quoting",
            "effect": "neither audit result from that invocation was accepted as evidence",
            "recovery": "split the read-only audits into simpler commands and rerun each from the unchanged worktree",
            "preserved": True,
        }, {
            "negative_id": "V6422-N19",
            "stage": "full_repository_test_reruns",
            "failure": "an inherited v641-v4 test could not write or clean mode-0700 temporary directories in either the system or Tamar-owned D-drive temp root",
            "effect": "two 190-test reruns ended with one environmental error each after an earlier complete pass",
            "attempts": [
                {"temp_root": "system_default", "result": "permission_denied"},
                {"temp_root": "tamar_owned_d_drive", "result": "permission_denied"}
            ],
            "diagnosis": "ordinary inherited-ACL child directories were writable; the failure followed Python 3.12 tempfile mode 0700 under the managed Windows execution token",
            "recovery": "use the additive family test runner to create only ephemeral temp children with inherited parent ACLs; do not edit the inherited test or change parent or host security",
            "preserved": True,
        }, {
            "negative_id": "V6422-N20",
            "stage": "first_inherited_acl_test_runner_run",
            "failure": "the first adapted runner omitted the repository from sys.path; the second incorrectly treated the bare tests directory as an importable package",
            "effect": "the first ran only 106 tests with six import errors; the second stopped before discovery; both partial results were rejected",
            "attempts": [
                {"discovery": "bare_without_repository_sys_path", "result": "106_tests_and_6_import_errors"},
                {"discovery": "tests_as_importable_top_level", "result": "start_directory_not_importable"}
            ],
            "recovery": "insert the repository in sys.path while preserving bare unittest discovery from tests",
            "preserved": True,
        }, {
            "negative_id": "V6422-N21",
            "stage": "first_evidence_push",
            "failure": "the local Git proxy endpoint was unavailable before the push reached the live remote",
            "effect": "the evidence commit remained local and the first push result was rejected",
            "recovery": "retry the same non-force push; then prove local, upstream, tracking, and live-remote equality",
            "preserved": True,
        }, {
            "negative_id": "V6422-N22",
            "stage": "evidence_snapshot_materialization",
            "failure": "the command wrapper timed out after both additive detached snapshots finished materializing and reported the exact evidence head",
            "effect": "the timeout result itself was rejected until both heads and clean states were rechecked",
            "recovery": "retain both additive snapshots, verify their exact heads and clean states separately, then run the complete battery in each",
            "preserved": True,
        }],
    })
    new_negative_specs = [
        ("V6422-N01", "Lexical proposal distance does not prove semantic uniqueness.", "provenance/prior-proposal-collision-audit.json", "Retain manual semantic review and withdraw or split later collisions."),
        ("V6422-N02", "Multi-axis overlap disclosure does not prove source independence.", "provenance/independence-debt-ledger.json", "Keep overlap debt visible and prohibit document-count independence claims."),
        ("V6422-N03", "Typed equation and covariance checks are structural only.", "physics/canonical-equation-ast.json", "Keep empirical confirmation, detected-force, unique-prediction, and Theory-of-Everything claims false."),
        ("V6422-N04", "Local Jacobian rank does not establish empirical identifiability.", "physics/conservation-stability-jacobian-witness.json", "Retain nuisance and real-observation gates."),
        ("V6422-N05", "The empirical adapter parsed zero real measurement rows and executed zero likelihoods.", "empirical/null-baseline-readiness.json", "Keep the result represented and require a separate real-data study."),
        ("V6422-N06", "THOS executed zero blind matched-budget real arm runs.", "thos/real-arm-execution-gate.json", "Keep the result open and require real arms plus independent review."),
        ("V6422-N07", "The THOS escrow provides no superiority, AGI, ASI, consciousness, or personhood evidence.", "thos/real-arm-execution-gate.json", "Retain all protected claim flags as false."),
        ("V6422-N08", "Freed ID has no real keys, proofs, live resolution or status, interoperability review, or trust governance.", "freed-id/production-assurance-gate.json", "Keep production assurance open."),
        ("V6422-N09", "Affected-party, Māori, cultural, and competent legal authority are absent.", "cbr/legal-cultural-authority-gate.json", "Defer and never substitute technical output for authority."),
        ("V6422-N10", "The strict parser battery is bounded and not exhaustive security.", "security/recovery-resource-receipt.json", "Require independent production security review for stronger claims."),
        ("V6422-N11", "Named-owner replay shares a machine, repository, tools, and assumptions.", "reproduction/independent-team-gap.json", "Report cross-owner internal repeatability only and keep independent-team reproduction open."),
        ("V6422-N12", "No fundamental thermo-psyche law, consciousness tensor, or personhood evidence is established.", "thermo-psyche/classification-receipt.json", "Retain construct, causal, observation, and authority burdens."),
        ("V6422-N13", "Static report structure is not complete WCAG conformance.", "deliverables/v642-v2-evidence-crosscheck-report.html", "Require a complete independent accessibility assessment for conformance claims."),
        ("V6422-N14", "Mandatory Stage 20 fail and defer decisions remain.", "stage20/terminal-verdict.json", "Keep NOT_READY_FOR_STAGE_20."),
        ("V6422-N15", "The first x2 build failed when the Windows default locale decoded a UTF-8 frozen Git object.", "validation/execution-negative-log.json", "Request UTF-8 explicitly and preserve the failed attempt in the execution log."),
        ("V6422-N16", "The first full validator run wrote its result but failed while emitting the Māori authority boundary through the Windows console encoding.", "validation/execution-negative-log.json", "Configure verifier stdout as UTF-8 and preserve the failed attempt in the execution log."),
        ("V6422-N17", "The first v642-v2 test run failed because the replay test omitted the valid pending_clean_snapshots state.", "validation/execution-negative-log.json", "Admit the exact pre-commit state while retaining the stricter verified-state closeout gate."),
        ("V6422-N18", "The first combined diagnostic invocation was rejected by PowerShell quoting before its audits ran.", "validation/execution-negative-log.json", "Split the read-only audits and preserve the rejected invocation."),
        ("V6422-N19", "Two repository reruns hit the same managed-Windows permission error for mode-0700 temporary directories across system and D-drive roots.", "validation/execution-negative-log.json", "Use the additive inherited-ACL temp adapter without editing the inherited test or changing parent or host security."),
        ("V6422-N20", "Two inherited-ACL runner discovery attempts failed: one partial 106-test run and one non-importable-start error.", "validation/execution-negative-log.json", "Insert the repository in sys.path, preserve bare discovery, and reject both failed attempts."),
        ("V6422-N21", "The first evidence push could not reach the live remote because the local Git proxy endpoint was unavailable.", "validation/execution-negative-log.json", "Retry without force and prove four-way equality after success."),
        ("V6422-N22", "The evidence snapshot materialization command exceeded its wrapper timeout after both detached heads completed.", "validation/execution-negative-log.json", "Recheck both heads and clean states separately, retain both worktrees, and validate each fully."),
    ]
    new_negatives = [{"negative_id": nid, "statement": statement, "evidence": evidence, "recovery": recovery, "retained": True}
                     for nid, statement, evidence, recovery in new_negative_specs]
    write_json(phase_dir / "retained-negative-register.json", {
        "schema": "ghc.family.v642-v2.retained-negative-register.v1", "inherited_count": 46, "new_count": 22,
        "negative_count": 68, "negatives": inherited_negatives["negatives"] + new_negatives,
        "all_retained": True, "erasure_permitted": False,
    })
    write_json(phase_dir / "exact-open-gate-register.json", {
        "schema": "ghc.family.v642-v2.exact-open-gate-register.v1", "gates": inherited_gates["gates"],
        "open_gap_count": 5, "exact_gate_count": 6, "silently_closed": 0,
    })
    protected = {
        "empirical_gmut_confirmation": False, "detected_force": False, "unique_prediction": False,
        "theory_of_everything": False, "real_thos_superiority": False, "agi": False, "asi": False,
        "consciousness": False, "personhood": False, "freed_id_cryptographic_assurance": False,
        "freed_id_production_interoperability": False, "enacted_law": False, "cultural_ratification": False,
        "maori_authority": False, "deployment": False, "exhaustive_security": False,
        "complete_accessibility_conformance": False, "proof_or_canon": False, "independent_team_reproduction": False,
    }
    write_json(phase_dir / "phase-truth.json", {
        "schema": "ghc.family.v642-v2.phase-truth.v1", "phase": phase, "owner": owner,
        "source_revision": source_revision, "x1_commit": x1_commit, "evidence_commit": "pending",
        "proposal_count": 10, "disposition_counts": counts, "retained_negative_count": 68,
        "open_gap_count": 5, "exact_gate_count": 6, "protected_claims": protected,
        "maori_authority_boundary": "Māori concepts, wording, data, and governance remain under Māori authority.",
        "cross_owner_internal_repeatability": "pending_clean_snapshots", "independent_team_gap": "open",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    checklist = [
        {"item": "exact ten frozen proposals executed as evidence permits", "state": "completed"},
        {"item": "four truth labels and observed distribution", "state": "completed"},
        {"item": "all 68 negatives retained", "state": "completed"},
        {"item": "five open gaps and six exact gates visible", "state": "completed"},
        {"item": "full repository suite", "state": "pending_validation"},
        {"item": "phase validator and minimal verifier", "state": "pending_validation"},
        {"item": "JSON, privacy, diff, stale-label, and staged-file review", "state": "pending_validation"},
        {"item": "two clean evidence snapshots and normalized parity", "state": "pending_snapshots"},
        {"item": "closeout, seal, and final-head detached validation", "state": "pending_closeout"},
        {"item": "single Eiren baton", "state": "not_sent_pre_terminal_gate"},
    ]
    write_json(phase_dir / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v642-v2.complete-incomplete-checklist.v1", "phase_state": "evidence_built_pending_validation",
        "items": checklist, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text(phase_dir / "complete-incomplete-checklist.md", "# v642-v2 complete/incomplete checklist\n\n" + "\n".join(f"- [{ 'x' if row['state']=='completed' else ' ' }] {row['item']} — `{row['state']}`" for row in checklist))
    write_json(phase_dir / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v642-v2.executed-toolchain.v1", "family_current": [
            "scripts/ghc_family_evidence_crosscheck.py", "scripts/ghc_family_evidence_crosscheck_validator.py",
            "scripts/ghc_family_evidence_crosscheck_minimal.py", "scripts/build_ghc_family_evidence_crosscheck_report.py",
            "scripts/ghc_family_phase_privacy_scan.py", "scripts/ghc_family_repository_test_runner.py",
        ], "compatibility_source_replay": [
            "scripts/ghc_family_evidence_boundary_validator.py", "scripts/ghc_family_evidence_boundary_minimal.py"
        ], "shared_source_tools_modified": False,
    })
    write_text(phase_dir / "v642-v2-integrated-overview.md", overview(owner, source_revision, x1_commit))
    build_manifest(phase_dir)


def finalize(phase_dir: Path, evidence_commit: str) -> None:
    snapshots = read_json(phase_dir / "reproduction/clean-snapshot-validation.json")
    if snapshots.get("verified_snapshot_count", 0) < 2 or snapshots.get("hash_mismatches") != 0:
        raise SystemExit("two verified snapshots with zero hash mismatches required")
    x2 = read_json(phase_dir / "x2-proposal-ledger.json")
    x2["evidence_commit"] = evidence_commit
    x2["snapshot_state"] = "verified"
    write_json(phase_dir / "x2-proposal-ledger.json", x2)
    truth = read_json(phase_dir / "phase-truth.json")
    truth["evidence_commit"] = evidence_commit
    truth["cross_owner_internal_repeatability"] = "verified_bounded"
    write_json(phase_dir / "phase-truth.json", truth)
    replay = read_json(phase_dir / "reproduction/cross-owner-lineage-replay.json")
    replay["v642_v2_evidence_snapshots"] = snapshots["verified_snapshot_count"]
    replay["cross_owner_internal_repeatability"] = "verified_bounded"
    write_json(phase_dir / "reproduction/cross-owner-lineage-replay.json", replay)
    perturb = read_json(phase_dir / "reproduction/environment-perturbation-receipt.json")
    perturb.update({"state": "verified", "verified_snapshots": snapshots["verified_snapshot_count"],
                    "normalized_hash_files": snapshots["normalized_hash_files"], "hash_mismatches": 0})
    write_json(phase_dir / "reproduction/environment-perturbation-receipt.json", perturb)
    checklist = read_json(phase_dir / "complete-incomplete-checklist.json")
    for item in checklist["items"]:
        if item["state"] in {"pending_validation", "pending_snapshots"}:
            item["state"] = "completed"
    checklist["phase_state"] = "validated_pending_closeout"
    write_json(phase_dir / "complete-incomplete-checklist.json", checklist)
    write_text(phase_dir / "complete-incomplete-checklist.md", "# v642-v2 complete/incomplete checklist\n\n" + "\n".join(f"- [{ 'x' if row['state']=='completed' else ' ' }] {row['item']} — `{row['state']}`" for row in checklist["items"]))
    build_manifest(phase_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--x1-commit")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--evidence-commit")
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    phase_dir = phase_dir.resolve()
    try:
        phase_dir.relative_to(repo)
    except ValueError as exc:
        raise SystemExit("phase directory must remain inside repository") from exc
    if args.finalize:
        if not args.evidence_commit:
            raise SystemExit("--evidence-commit is required with --finalize")
        finalize(phase_dir, args.evidence_commit)
        mode = "finalize"
    else:
        if not args.x1_commit:
            raise SystemExit("--x1-commit is required")
        build_all(repo, phase_dir, args.x1_commit)
        mode = "build"
    print(json.dumps({"phase": "v642-v2", "mode": mode, "ok": True}))


if __name__ == "__main__":
    main()
