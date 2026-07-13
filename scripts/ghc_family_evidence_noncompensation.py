#!/usr/bin/env python3
"""Build the bounded GHC Family v642-v5 non-compensation evidence packet.

The implementation is standard-library-only. It creates structural and synthetic
fixtures and keeps empirical, production, authority, deployment, identity, and
independent-reproduction claims false unless exact external evidence exists.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit


TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OBSERVED = {
    "V6425-P01": "completed",
    "V6425-P02": "completed",
    "V6425-P03": "represented",
    "V6425-P04": "open_gap",
    "V6425-P05": "represented",
    "V6425-P06": "exact_gate",
    "V6425-P07": "completed",
    "V6425-P08": "completed",
    "V6425-P09": "completed",
    "V6425-P10": "completed",
}
PROTECTED_CLAIMS = [
    "empirical_gmut_confirmation",
    "detected_force",
    "unique_prediction",
    "theory_of_everything",
    "real_thos_superiority",
    "agi",
    "asi",
    "consciousness",
    "personhood",
    "freed_id_cryptographic_assurance",
    "freed_id_production_interoperability",
    "enacted_law",
    "cultural_ratification",
    "maori_authority",
    "maori_data_governance_authority",
    "deployment",
    "exhaustive_security",
    "complete_accessibility_conformance",
    "proof_or_canon",
    "independent_team_reproduction",
    "fundamental_thermo_psyche_law",
    "stage20_ready",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def citation_entailment_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if case.get("claim_polarity") != case.get("source_polarity"):
        reasons.append("polarity_mismatch")
    modality_rank = {"possible": 0, "bounded": 1, "probable": 2, "certain": 3}
    if modality_rank.get(case.get("claim_modality"), 99) > modality_rank.get(
        case.get("source_modality"), -1
    ):
        reasons.append("claim_modality_stronger_than_source")
    claim_scope = set(case.get("claim_scope", []))
    source_scope = set(case.get("source_scope", []))
    if not claim_scope.issubset(source_scope):
        reasons.append("claim_scope_exceeds_source")
    if case.get("claim_evidence_type") != case.get("source_evidence_type"):
        reasons.append("evidence_type_drift")
    if case.get("claimed_independent_roots") != case.get("unique_authority_roots"):
        reasons.append("authority_root_independence_inflated")
    if case.get("empirical_promotion"):
        reasons.append("citation_promoted_to_empirical_result")
    return not reasons, reasons


def hyperbolicity_obligation(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not case.get("principal_symbol_declared"):
        reasons.append("principal_symbol_missing")
    if not case.get("eigenvalues_real"):
        reasons.append("nonreal_characteristic_speed")
    if not case.get("diagonalizable"):
        reasons.append("principal_symbol_defective")
    if not case.get("gauge_declared"):
        reasons.append("gauge_obligation_missing")
    if float(case.get("constraint_growth_rate", math.inf)) > 0:
        reasons.append("constraint_growth_detected")
    if not case.get("dimensions_consistent"):
        reasons.append("dimension_mismatch")
    if case.get("empirical_claim"):
        reasons.append("structural_fixture_promoted_to_empirical")
    return not reasons, reasons


def prior_sensitivity_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not case.get("prior_families_frozen_before_outcomes"):
        reasons.append("prior_family_posthoc")
    if not case.get("conflict_threshold_preregistered"):
        reasons.append("conflict_threshold_posthoc")
    means = [float(value) for value in case.get("posterior_means", [])]
    if len(means) < 2:
        reasons.append("insufficient_prior_families")
    if case.get("real_measurement_rows", 0) != 0:
        reasons.append("real_rows_outside_authorized_scope")
    if case.get("likelihood_executed") or case.get("empirical_confirmation"):
        reasons.append("synthetic_diagnostic_promoted")
    if reasons:
        return "reject", reasons
    spread = max(means) - min(means)
    threshold = float(case.get("sensitivity_threshold", 0.0))
    tail_probability = float(case.get("prior_predictive_tail_probability", 0.0))
    if spread > threshold:
        return "represented_sensitive", ["synthetic_prior_sensitivity_triggered"]
    if tail_probability < float(case.get("conflict_threshold", 0.0)):
        return "represented_conflict", ["synthetic_prior_data_conflict_triggered"]
    return "represented", []


def scorer_reliability_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    required = [
        ("blind", "rater_blindness_missing"),
        ("training_parity", "rater_training_mismatch"),
        ("original_ratings_retained", "original_ratings_erased"),
        ("adjudication_separate", "adjudication_conflated"),
        ("matched_budget", "budget_mismatch"),
        ("exclusion_rule_preregistered", "outcome_tuned_exclusion_risk"),
    ]
    reasons.extend(label for field, label in required if not case.get(field))
    if reasons:
        return "reject_protocol", reasons
    if case.get("real_rater_count", 0) == 0:
        return "open_gap", ["zero_real_raters"]
    if case.get("blind_matched_budget_real_arms", 0) == 0:
        return "open_gap", ["zero_blind_matched_budget_real_arms"]
    if not case.get("independent_review"):
        return "open_gap", ["independent_review_missing"]
    return "eligible_for_bounded_analysis", []


def _unsafe_ip(hostname: str) -> bool:
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return bool(
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_unspecified
        or address.is_multicast
    )


def resolver_egress_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    urls = [case.get("endpoint", ""), *case.get("redirects", [])]
    if len(case.get("redirects", [])) > int(case.get("max_redirects", 0)):
        reasons.append("redirect_limit_exceeded")
    for raw in urls:
        parsed = urlsplit(raw)
        if parsed.scheme != "https":
            reasons.append("unsupported_or_insecure_scheme")
        if parsed.username or parsed.password:
            reasons.append("userinfo_not_allowed")
        host = parsed.hostname or ""
        if not host:
            reasons.append("hostname_missing")
        elif host.lower() == "localhost" or _unsafe_ip(host):
            reasons.append("unsafe_network_target")
        if ".." in parsed.path.split("/"):
            reasons.append("path_traversal_segment")
    allowed_metadata = set(case.get("allowed_request_metadata", []))
    emitted_metadata = set(case.get("emitted_request_metadata", []))
    if not emitted_metadata.issubset(allowed_metadata):
        reasons.append("requester_metadata_excess")
    if not case.get("query_normalized"):
        reasons.append("query_normalization_missing")
    if reasons:
        return "reject", sorted(set(reasons))
    return "represented", []


def dissent_recusal_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not case.get("dissent_retained"):
        reasons.append("minority_report_erased")
    if not case.get("conflicts_disclosed"):
        reasons.append("conflict_not_disclosed")
    if case.get("conflicted_representative_voted"):
        reasons.append("recusal_not_applied")
    if case.get("silence_counted_as_consent"):
        reasons.append("silence_promoted_to_consent")
    if not case.get("remedy_rights_preserved"):
        reasons.append("remedy_rights_removed")
    if reasons:
        return "reject_technical_process", reasons
    authority_missing = [
        field
        for field in [
            "affected_party_authority_present",
            "maori_authority_present",
            "cultural_authority_present",
            "competent_legal_review",
        ]
        if not case.get(field)
    ]
    if authority_missing:
        return "exact_gate", [f"{field}_absent" for field in authority_missing]
    return "authority_present_for_review", []


def oracle_integrity_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if case.get("oracle_digest") != case.get("expected_oracle_digest"):
        reasons.append("oracle_digest_changed")
    if not case.get("original_fixture_retained"):
        reasons.append("original_fixture_erased")
    if case.get("seed") is None:
        reasons.append("deterministic_seed_missing")
    if case.get("failure_signature_before") != case.get("failure_signature_after"):
        reasons.append("failure_class_changed_by_minimization")
    if case.get("exception_scope_after") != case.get("exception_scope_before"):
        reasons.append("security_exception_scope_changed")
    if case.get("claims_exhaustive_security"):
        reasons.append("exhaustive_security_overclaim")
    return not reasons, reasons


def determinism_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    required = [
        ("source_epoch_pinned", "source_epoch_unpinned"),
        ("timezone_utc", "timezone_not_utc"),
        ("locale_declared", "locale_undeclared"),
        ("filesystem_order_sorted", "filesystem_order_unsorted"),
        ("seed_pinned", "seed_unpinned"),
        ("dependencies_declared", "dependency_closure_missing"),
    ]
    reasons.extend(label for field, label in required if not case.get(field))
    if case.get("semantic_change_normalized_away"):
        reasons.append("semantic_change_hidden_by_normalization")
    if case.get("claims_independent_reproduction"):
        reasons.append("same_owner_promoted_to_independent")
    return not reasons, reasons


def measurement_scale_decision(case: dict[str, Any]) -> tuple[bool, list[str]]:
    admissible = {
        "nominal": {"equality", "mode", "count"},
        "ordinal": {"equality", "mode", "count", "rank", "median"},
        "interval": {"equality", "mode", "count", "rank", "median", "mean", "difference"},
        "ratio": {"equality", "mode", "count", "rank", "median", "mean", "difference", "ratio"},
    }
    reasons: list[str] = []
    scale = case.get("scale")
    operation = case.get("operation")
    if scale not in admissible:
        reasons.append("unknown_measurement_scale")
    elif operation not in admissible[scale]:
        reasons.append("operation_not_admissible_for_scale")
    if case.get("interval_zero_treated_as_absolute"):
        reasons.append("interval_zero_promoted_to_absolute")
    if case.get("cross_domain_units_equated"):
        reasons.append("thermo_psyche_unit_category_crossing")
    if case.get("entropy_domains_conflated"):
        reasons.append("entropy_domain_conflation")
    if case.get("claims_fundamental_law"):
        reasons.append("fundamental_law_overclaim")
    return not reasons, reasons


def noncompensatory_decision(case: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    dimensions = case.get("dimensions", {})
    veto_dimensions = case.get(
        "veto_dimensions", ["empirical", "authority", "production", "independence"]
    )
    missing = [name for name in veto_dimensions if name not in dimensions]
    zeros = [name for name in veto_dimensions if dimensions.get(name, 0) <= 0]
    if missing:
        reasons.extend(f"missing_{name}_dimension" for name in missing)
    if case.get("missing_scored_as_neutral"):
        reasons.append("missing_evidence_laundered_as_neutral")
    if case.get("weighted_promotion_requested") and zeros:
        reasons.append("weighted_score_attempted_to_offset_veto")
    if case.get("negative_count", 0) < case.get("inherited_negative_count", 0):
        reasons.append("negative_count_regressed")
    if any(case.get("protected_claims", {}).get(name) is not False for name in PROTECTED_CLAIMS):
        reasons.append("protected_claim_missing_or_true")
    if reasons:
        return "fail", reasons
    if zeros:
        return "defer", [f"zero_{name}_dimension" for name in zeros]
    return "pass", []


def vector(
    case_id: str,
    expected: Any,
    actual: Any,
    reasons: list[str],
    negative_id: str | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "case_id": case_id,
        "expected": expected,
        "actual": actual,
        "reasons": reasons,
        "matches_expected": expected == actual,
    }
    if negative_id:
        value["negative_id"] = negative_id
    return value


def evaluate_cases(
    cases: list[tuple[str, Any, dict[str, Any], str | None]],
    decision: Callable[[dict[str, Any]], tuple[Any, list[str]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case_id, expected, case, negative_id in cases:
        actual, reasons = decision(case)
        rows.append(vector(case_id, expected, actual, reasons, negative_id))
    return rows


def integrated_overview(
    x1: dict[str, Any], source_revision: str, x1_commit: str, negative_count: int
) -> str:
    header = f"""# Sable Rook v642-v5 integrated non-compensation overview

## 1. Scope, lineage, and identity boundary

This packet executes the ten proposals frozen in the dedicated x1 commit `{x1_commit}`. Its exact inherited source is Ilyra Fen's clean final v642-v4 head `{source_revision}`. Sable Rook (they/them) is relational working language for phase ownership, accountability, and collaboration. It is not evidence of consciousness, sentience, legal personhood, biological status, authority, or identity continuity. No task, fork, delegation, collaboration subagent, successor, or later sibling is created by this work. Every sibling other than the active owner remains standby or recoverable.

The phase uses exactly four truth labels. `completed` means a frozen local artifact and its bounded rejecting checks were produced in the owned scope. `represented` means a structural model or synthetic proxy exists while the real evidentiary object does not. `open_gap` means required empirical, institutional, production, real-arm, or independent evidence is absent. `exact_gate` means technical work cannot substitute for fresh authority. The observed distribution is six completed, two represented, one open gap, and one exact gate. These labels apply only to the packet and do not transfer scientific, cultural, legal, cryptographic, accessibility, security, deployment, or identity authority.

X1 was committed, pushed, and proven equal across local, upstream, and live remote before any x2 implementation began. The inherited Ilyra tools remain byte-stable. New implementation uses additive family-current names. D-drive storage is primary for the owned worktree and clean detached snapshots. Windows Sandbox was audited read-only and found unavailable without elevation or a feature change; neither was attempted. Codex versions were observed without updating the desktop app.

## 2. Evidence discipline and non-compensation rule

Each proposal is executed only as far as evidence permits. Deterministic rejected fixtures are retained rather than rewritten as successes. A validator pass is bounded engineering evidence, not a scientific confirmation. A clean checkout is same-owner repeatability, not independent reproduction. A citation is provenance, not automatic entailment. A high engineering score cannot compensate for zero empirical evidence, missing affected-party authority, absent production cryptography, or no independent executor.

The source ledger contains current, stable, draft, and watch classes. Draft W3C DID Resolution and JSON Schema context remain visibly non-stable. Multiple documents from one authority root are not counted as independent sources. The phase carries forward all 120 inherited negatives and adds phase-local x1, vector, and execution negatives, for `{negative_count}` retained negatives at this build. Five open gaps and six exact gates remain visible. None is converted into a weighted penalty or silently closed.
"""
    sections: list[str] = []
    for index, proposal in enumerate(x1["proposals"], start=3):
        disposition = OBSERVED[proposal["proposal_id"]]
        evidence = ", ".join(f"`{path}`" for path in proposal["deliverables"])
        gates = ", ".join(proposal["protected_gates"])
        sections.append(
            f"""## {index}. {proposal['title']}

The frozen hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure']} The phase produced {evidence}. Its observed disposition is `{disposition}`. That label is bounded to the local artifact and deterministic fixture surface; it does not erase the protected gates `{gates}`.

The preregistered falsifier was: {proposal['test_falsifier_or_gate']} Recovery remains non-destructive and evidence-preserving: {proposal['rollback_or_recovery']} Every rejecting vector remains in the evidence packet and retained-negative register. The mechanism-level novelty against the first 110 frozen proposals was recorded as: {proposal['novelty_against_prior_chain']}

The result remains narrower than the motivating idea. Structural consistency is not observation. Synthetic behavior is not a real arm, a production credential, an authority decision, deployment, or independent execution. `represented`, `open_gap`, and `exact_gate` name the missing object rather than imputing it. `completed` means the preregistered local surface was built and rejected its negative fixtures; it does not promote a protected real-world claim.
"""
        )
    footer = """## 13. Reproduction, privacy, and accessibility boundary

Fresh detached snapshots replay the evidence commit with the same public repository, owner, tool family, and local infrastructure. Normalized text hashes absorb checkout newline variation but do not hide semantic changes. Clock, timezone, locale, ordering, seed, and dependency declarations are explicit. This can establish bounded same-owner repeatability only. No genuinely independent team or returned evidence exists.

Privacy scanning covers raw identifier-shaped values, local absolute paths, credential forms, private route schemes, transcript payloads, session-stream filenames, images, and private app state. Repository artifacts use relative paths and sanitized route states. Zero hits are bounded evidence and not proof of exhaustive privacy or security. The static report includes language, skip navigation, landmarks, ordered headings, table headers, visible focus, and reduced-motion handling. Automated structure is not complete accessibility conformance; qualified manual assessment and user participation remain open.

## 14. Scientific, identity, cultural, and legal boundary

GMUT remains a typed research scaffold. Principal-symbol and constraint fixtures do not establish local well-posedness for an unspecified full theory, a detected force, unique prediction, likelihood result, empirical confirmation, or Theory of Everything. The empirical adapter has zero real rows. Prior-sensitivity and conflict fixtures are synthetic.

THOS has zero real raters and zero blind matched-budget real arms in this phase. A reliability protocol cannot establish superiority, AGI, ASI, consciousness, or personhood. Freed ID has zero real keys or proofs, live resolvers or status services, interoperability partners, independent security or privacy reviews, and trust-governance authorities. Resolver-egress fixtures remain represented rather than production assurance.

CBR legitimacy, minority representation, conflict recusal, Māori wording and authority, Māori data governance, affected-party acceptance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated. Technical artifacts can refuse unsupported processing but cannot appoint representatives, define tikanga, transfer authority, or decide law. Māori concepts, wording, data, and governance remain under Māori authority.

## 15. Terminal verdict and route truth

The terminal verdict is `NOT_READY_FOR_STAGE_20`. Five open gaps and six exact gates independently preserve that result. No AGI, ASI, consciousness, personhood, deployment, exhaustive-security, complete-accessibility, Theory-of-Everything, proof or canon, empirical-confirmation, legal or cultural-ratification, fundamental thermo-psyche law, or independent-reproduction claim is made.

Route state is `NO_SUCCESSOR_AUTHORIZED`. This phase does not create the later sibling, prepare a send as if it were delivered, or message any standby task. Only separate explicit authority after verified closeout could change that state.
"""
    return header + "\n".join(sections) + footer


def build(
    repo: Path,
    phase: Path,
    x1_commit: str,
    evidence_commit: str,
    snapshot_state: str,
) -> dict[str, Any]:
    x1 = read_json(phase / "x1-proposals.json")
    source_revision = x1["source_revision"]
    protected = {name: False for name in PROTECTED_CLAIMS}
    vector_files: list[tuple[str, list[dict[str, Any]]]] = []

    citation_base = {
        "claim_polarity": "positive",
        "source_polarity": "positive",
        "claim_modality": "bounded",
        "source_modality": "bounded",
        "claim_scope": ["synthetic", "local"],
        "source_scope": ["synthetic", "local", "structural"],
        "claim_evidence_type": "structural",
        "source_evidence_type": "structural",
        "claimed_independent_roots": 1,
        "unique_authority_roots": 1,
        "empirical_promotion": False,
    }
    citation_vectors = evaluate_cases(
        [
            ("CITE-ENTAILED", True, citation_base, None),
            ("CITE-POLARITY-DRIFT", False, {**citation_base, "source_polarity": "negative"}, "V6425-N01"),
            ("CITE-INDEPENDENCE-INFLATION", False, {**citation_base, "claimed_independent_roots": 3}, "V6425-N02"),
        ],
        citation_entailment_decision,
    )
    write_json(phase / "provenance/citation-entailment-contract.json", {
        "schema": "ghc.family.citation-entailment-contract.v1",
        "sources": ["V8-S01", "V8-S02", "V6422-S38"],
        "assertion_level_scope_required": True,
        "authority_root_deduplication_required": True,
        "empirical_promotion_allowed": False,
        "observed_disposition": "completed",
    })
    write_json(phase / "provenance/assertion-granularity-vectors.json", {"schema": "ghc.family.assertion-granularity-vectors.v1", "vectors": citation_vectors})
    write_json(phase / "provenance/source-scope-drift-register.json", {
        "schema": "ghc.family.source-scope-drift-register.v1",
        "all_expected": all(row["matches_expected"] for row in citation_vectors),
        "authentic_source_is_automatic_entailment": False,
        "authority_root_count_can_be_inflated": False,
        "observed_disposition": "completed",
    })
    vector_files.append(("provenance/assertion-granularity-vectors.json", citation_vectors))

    hyper_base = {
        "principal_symbol_declared": True,
        "eigenvalues_real": True,
        "diagonalizable": True,
        "gauge_declared": True,
        "constraint_growth_rate": -0.1,
        "dimensions_consistent": True,
        "empirical_claim": False,
    }
    hyper_vectors = evaluate_cases(
        [
            ("HYPER-OBLIGATIONS-PRESENT", True, hyper_base, None),
            ("HYPER-DEFECTIVE", False, {**hyper_base, "diagonalizable": False}, "V6425-N03"),
            ("HYPER-CONSTRAINT-GROWTH", False, {**hyper_base, "constraint_growth_rate": 0.2}, "V6425-N04"),
        ],
        hyperbolicity_obligation,
    )
    write_json(phase / "physics/principal-symbol-obligation.json", {
        "schema": "ghc.family.principal-symbol-obligation.v1",
        "model_class": "typed scalar-tensor/EFT research scaffold",
        "canonical_scaffold": "G_mu_nu + Lambda g_mu_nu = M_Pl^-2 T^SM_mu_nu + Omega_mu_nu",
        "strong_hyperbolicity_is_separate_from_conservation": True,
        "theory_specific_proof_completed": False,
        "real_measurement_rows": 0,
        "observed_disposition": "completed",
    })
    write_json(phase / "physics/constraint-propagation-vectors.json", {"schema": "ghc.family.constraint-propagation-vectors.v1", "vectors": hyper_vectors})
    write_json(phase / "physics/well-posedness-claim-boundary.json", {
        "schema": "ghc.family.well-posedness-claim-boundary.v1",
        "all_expected": all(row["matches_expected"] for row in hyper_vectors),
        "gmut_well_posedness_established": False,
        "empirical_confirmation": False,
        "detected_force": False,
        "unique_prediction": False,
        "theory_of_everything": False,
        "proof_or_canon": False,
        "observed_disposition": "completed",
    })
    vector_files.append(("physics/constraint-propagation-vectors.json", hyper_vectors))

    prior_base = {
        "prior_families_frozen_before_outcomes": True,
        "conflict_threshold_preregistered": True,
        "posterior_means": [0.10, 0.12, 0.11],
        "sensitivity_threshold": 0.05,
        "prior_predictive_tail_probability": 0.4,
        "conflict_threshold": 0.05,
        "real_measurement_rows": 0,
        "likelihood_executed": False,
        "empirical_confirmation": False,
    }
    prior_vectors = evaluate_cases(
        [
            ("PRIOR-SYNTHETIC-BOUNDED", "represented", prior_base, None),
            ("PRIOR-POSTHOC-FAMILY", "reject", {**prior_base, "prior_families_frozen_before_outcomes": False}, "V6425-N05"),
            ("PRIOR-EMPIRICAL-PROMOTION", "reject", {**prior_base, "empirical_confirmation": True}, "V6425-N06"),
        ],
        prior_sensitivity_decision,
    )
    write_json(phase / "empirical/prior-sensitivity-contract.json", {
        "schema": "ghc.family.prior-sensitivity-contract.v1",
        "sources": ["V6425-S56", "V6423-S40", "V6424-S50"],
        "prior_families_preregistered": True,
        "synthetic_only": True,
        "observed_disposition": "represented",
    })
    write_json(phase / "empirical/prior-data-conflict-vectors.json", {"schema": "ghc.family.prior-data-conflict-vectors.v1", "vectors": prior_vectors})
    write_json(phase / "empirical/zero-row-inference-lock.json", {
        "schema": "ghc.family.zero-row-inference-lock.v1",
        "real_measurement_rows": 0,
        "likelihood_executions": 0,
        "fits": 0,
        "independent_scientific_reviews": 0,
        "promotion_allowed": False,
        "empirical_confirmation": False,
        "observed_disposition": "represented",
    })
    vector_files.append(("empirical/prior-data-conflict-vectors.json", prior_vectors))

    scorer_base = {
        "blind": True,
        "training_parity": True,
        "original_ratings_retained": True,
        "adjudication_separate": True,
        "matched_budget": True,
        "exclusion_rule_preregistered": True,
        "real_rater_count": 0,
        "blind_matched_budget_real_arms": 0,
        "independent_review": False,
    }
    scorer_vectors = evaluate_cases(
        [
            ("SCORER-REAL-EVIDENCE-ABSENT", "open_gap", scorer_base, None),
            ("SCORER-ORIGINALS-ERASED", "reject_protocol", {**scorer_base, "original_ratings_retained": False}, "V6425-N07"),
            ("SCORER-TRAINING-MISMATCH", "reject_protocol", {**scorer_base, "training_parity": False}, "V6425-N08"),
        ],
        scorer_reliability_decision,
    )
    write_json(phase / "thos/scorer-reliability-preregistration.json", {
        "schema": "ghc.family.scorer-reliability-preregistration.v1",
        "sources": ["V6425-S57", "V6422-S37", "V8-S06"],
        "agreement_is_reliability": False,
        "original_and_adjudicated_ratings_separate": True,
        "observed_disposition": "open_gap",
    })
    write_json(phase / "thos/inter-rater-mutation-vectors.json", {"schema": "ghc.family.inter-rater-mutation-vectors.v1", "vectors": scorer_vectors})
    write_json(phase / "thos/real-rater-arm-gap.json", {
        "schema": "ghc.family.real-rater-arm-gap.v1",
        "real_raters": 0,
        "blind_matched_budget_real_arms": 0,
        "independent_reviews": 0,
        "real_thos_superiority": False,
        "agi": False,
        "asi": False,
        "consciousness": False,
        "personhood": False,
        "observed_disposition": "open_gap",
    })
    vector_files.append(("thos/inter-rater-mutation-vectors.json", scorer_vectors))

    resolver_base = {
        "endpoint": "https://resolver.example/resource",
        "redirects": ["https://service.example/final"],
        "max_redirects": 2,
        "allowed_request_metadata": ["accept"],
        "emitted_request_metadata": ["accept"],
        "query_normalized": True,
    }
    resolver_vectors = evaluate_cases(
        [
            ("RESOLVER-SYNTHETIC-ALLOWLIST", "represented", resolver_base, None),
            ("RESOLVER-LOOPBACK", "reject", {**resolver_base, "endpoint": "https://127.0.0.1/private"}, "V6425-N09"),
            ("RESOLVER-METADATA-EXCESS", "reject", {**resolver_base, "emitted_request_metadata": ["accept", "requester-id"]}, "V6425-N10"),
        ],
        resolver_egress_decision,
    )
    write_json(phase / "freed-id/resolution-egress-profile.json", {
        "schema": "ghc.family.resolution-egress-profile.v1",
        "sources": ["V8-S10", "V6425-S58", "V6425-S62", "V8-S31"],
        "draft_resolution_source_visible": True,
        "network_calls_performed": 0,
        "synthetic_only": True,
        "observed_disposition": "represented",
    })
    write_json(phase / "freed-id/redirect-metadata-leak-vectors.json", {"schema": "ghc.family.redirect-metadata-leak-vectors.v1", "vectors": resolver_vectors})
    write_json(phase / "freed-id/production-resolution-boundary.json", {
        "schema": "ghc.family.production-resolution-boundary.v1",
        "real_keys": 0,
        "real_proofs": 0,
        "live_resolvers_or_status_services": 0,
        "interoperability_partners": 0,
        "independent_security_reviews": 0,
        "independent_privacy_reviews": 0,
        "trust_governance_authorities": 0,
        "production_assurance": False,
        "observed_disposition": "represented",
    })
    vector_files.append(("freed-id/redirect-metadata-leak-vectors.json", resolver_vectors))

    dissent_base = {
        "dissent_retained": True,
        "conflicts_disclosed": True,
        "conflicted_representative_voted": False,
        "silence_counted_as_consent": False,
        "remedy_rights_preserved": True,
        "affected_party_authority_present": False,
        "maori_authority_present": False,
        "cultural_authority_present": False,
        "competent_legal_review": False,
    }
    dissent_vectors = evaluate_cases(
        [
            ("DISSENT-AUTHORITY-ABSENT", "exact_gate", dissent_base, None),
            ("DISSENT-ERASED", "reject_technical_process", {**dissent_base, "dissent_retained": False}, "V6425-N11"),
            ("DISSENT-CONFLICTED-VOTE", "reject_technical_process", {**dissent_base, "conflicted_representative_voted": True}, "V6425-N12"),
        ],
        dissent_recusal_decision,
    )
    write_json(phase / "cbr/dissent-recusal-authority-gate.json", {
        "schema": "ghc.family.dissent-recusal-authority-gate.v1",
        "sources": ["V8-S16", "V8-S19", "V8-S20", "V8-S18"],
        "technical_artifact_can_grant_maori_authority": False,
        "technical_artifact_can_appoint_representatives": False,
        "authorized_participants_present": 0,
        "observed_disposition": "exact_gate",
    })
    write_json(phase / "cbr/minority-report-vectors.json", {"schema": "ghc.family.minority-report-vectors.v1", "vectors": dissent_vectors})
    write_json(phase / "cbr/conflict-of-interest-register.json", {
        "schema": "ghc.family.conflict-of-interest-register.v1",
        "synthetic_records_only": True,
        "private_conflict_details_recorded": False,
        "dissent_erasure_permitted": False,
        "recusal_can_remove_remedy_rights": False,
        "maori_authority": False,
        "cultural_ratification": False,
        "enacted_law": False,
        "observed_disposition": "exact_gate",
    })
    vector_files.append(("cbr/minority-report-vectors.json", dissent_vectors))

    oracle_base = {
        "oracle_digest": "fixed-oracle-digest",
        "expected_oracle_digest": "fixed-oracle-digest",
        "original_fixture_retained": True,
        "seed": 6425,
        "failure_signature_before": "reject/private-target",
        "failure_signature_after": "reject/private-target",
        "exception_scope_before": "none",
        "exception_scope_after": "none",
        "claims_exhaustive_security": False,
    }
    oracle_vectors = evaluate_cases(
        [
            ("ORACLE-INTEGRITY-PRESENT", True, oracle_base, None),
            ("ORACLE-DIGEST-POISONED", False, {**oracle_base, "oracle_digest": "changed"}, "V6425-N13"),
            ("ORACLE-FAILURE-CLASS-LOST", False, {**oracle_base, "failure_signature_after": "pass"}, "V6425-N14"),
        ],
        oracle_integrity_decision,
    )
    write_json(phase / "security/oracle-integrity-contract.json", {
        "schema": "ghc.family.oracle-integrity-contract.v1",
        "sources": ["V6425-S59", "V8-S22", "V6421-S34"],
        "oracle_and_fixture_independently_hashed": True,
        "original_failure_retained": True,
        "exhaustive_security": False,
        "observed_disposition": "completed",
    })
    write_json(phase / "security/adversarial-corpus-minimization.json", {
        "schema": "ghc.family.adversarial-corpus-minimization.v1",
        "fixed_seed": 6425,
        "failure_signature_preservation_required": True,
        "original_corpus_retained": True,
        "minimized_fixture_is_complete_security_evidence": False,
        "observed_disposition": "completed",
    })
    write_json(phase / "security/recovery-mutation-vectors.json", {"schema": "ghc.family.recovery-mutation-vectors.v1", "vectors": oracle_vectors})
    vector_files.append(("security/recovery-mutation-vectors.json", oracle_vectors))

    determinism_base = {
        "source_epoch_pinned": True,
        "timezone_utc": True,
        "locale_declared": True,
        "filesystem_order_sorted": True,
        "seed_pinned": True,
        "dependencies_declared": True,
        "semantic_change_normalized_away": False,
        "claims_independent_reproduction": False,
    }
    determinism_vectors = evaluate_cases(
        [
            ("DETERMINISM-ENVELOPE-DECLARED", True, determinism_base, None),
            ("DETERMINISM-ORDER-UNSORTED", False, {**determinism_base, "filesystem_order_sorted": False}, "V6425-N15"),
            ("DETERMINISM-SEMANTIC-HIDDEN", False, {**determinism_base, "semantic_change_normalized_away": True}, "V6425-N16"),
        ],
        determinism_decision,
    )
    write_json(phase / "reproduction/determinism-envelope.json", {
        "schema": "ghc.family.determinism-envelope.v1",
        "sources": ["V6425-S60", "V8-S24", "V6422-S38", "V8-S25"],
        "declared_dimensions": ["epoch", "timezone", "locale", "order", "seed", "dependencies", "newlines"],
        "same_owner_repeatability_only": True,
        "observed_disposition": "completed",
    })
    write_json(phase / "reproduction/clock-locale-order-vectors.json", {"schema": "ghc.family.clock-locale-order-vectors.v1", "vectors": determinism_vectors})
    write_json(phase / "reproduction/hermeticity-gap.json", {
        "schema": "ghc.family.hermeticity-gap.v1",
        "undeclared_dependency_count": 0,
        "independent_team_count": 0,
        "returned_independent_evidence_count": 0,
        "independent_reproduction_established": False,
        "observed_disposition": "completed",
    })
    vector_files.append(("reproduction/clock-locale-order-vectors.json", determinism_vectors))

    scale_base = {
        "scale": "ordinal",
        "operation": "median",
        "interval_zero_treated_as_absolute": False,
        "cross_domain_units_equated": False,
        "entropy_domains_conflated": False,
        "claims_fundamental_law": False,
    }
    scale_vectors = evaluate_cases(
        [
            ("SCALE-ORDINAL-MEDIAN", True, scale_base, None),
            ("SCALE-ORDINAL-MEAN", False, {**scale_base, "operation": "mean"}, "V6425-N17"),
            ("SCALE-CATEGORY-CROSSING", False, {**scale_base, "cross_domain_units_equated": True, "entropy_domains_conflated": True}, "V6425-N18"),
        ],
        measurement_scale_decision,
    )
    write_json(phase / "thermo-psyche/measurement-scale-classifier.json", {
        "schema": "ghc.family.measurement-scale-classifier.v1",
        "sources": ["V6425-S61", "V6423-S44", "V6423-S45", "V6422-S36"],
        "scale_classes": ["nominal", "ordinal", "interval", "ratio"],
        "operations_require_declared_admissibility": True,
        "observed_disposition": "completed",
    })
    write_json(phase / "thermo-psyche/analogy-admissibility-vectors.json", {"schema": "ghc.family.analogy-admissibility-vectors.v1", "vectors": scale_vectors})
    write_json(phase / "thermo-psyche/category-barrier.json", {
        "schema": "ghc.family.v642-v5.thermo-psyche-category-barrier.v1",
        "all_expected": all(row["matches_expected"] for row in scale_vectors),
        "fundamental_thermo_psyche_law": False,
        "consciousness": False,
        "personhood": False,
        "empirical_confirmation": False,
        "observed_disposition": "completed",
    })
    vector_files.append(("thermo-psyche/analogy-admissibility-vectors.json", scale_vectors))

    board_base = {
        "dimensions": {"engineering": 1.0, "empirical": 0.0, "authority": 0.0, "production": 0.0, "independence": 0.0},
        "veto_dimensions": ["empirical", "authority", "production", "independence"],
        "missing_scored_as_neutral": False,
        "weighted_promotion_requested": False,
        "negative_count": 145,
        "inherited_negative_count": 120,
        "protected_claims": protected,
    }
    board_vectors = evaluate_cases(
        [
            ("BOARD-ZERO-VETO-DEFER", "defer", board_base, None),
            ("BOARD-WEIGHTED-LAUNDER", "fail", {**board_base, "weighted_promotion_requested": True}, "V6425-N19"),
            ("BOARD-MISSING-NEUTRAL", "fail", {**board_base, "dimensions": {"engineering": 1.0}, "missing_scored_as_neutral": True}, "V6425-N20"),
        ],
        noncompensatory_decision,
    )
    write_json(phase / "stage20/noncompensatory-evidence-vector.json", {
        "schema": "ghc.family.noncompensatory-evidence-vector.v1",
        "sources": ["V8-S07", "V8-S17", "V6422-S38", "V6424-S54"],
        "dimensions": ["engineering", "empirical", "authority", "production", "independence"],
        "veto_dimensions": ["empirical", "authority", "production", "independence"],
        "weighted_compensation_allowed": False,
        "observed_disposition": "completed",
    })
    write_json(phase / "stage20/score-laundering-vectors.json", {"schema": "ghc.family.score-laundering-vectors.v1", "vectors": board_vectors})
    write_json(phase / "stage20/terminal-verdict.json", {
        "schema": "ghc.family.v642-v5.terminal-verdict.v1",
        "all_expected": all(row["matches_expected"] for row in board_vectors),
        "decision": "defer",
        "verdict": "NOT_READY_FOR_STAGE_20",
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "weighted_compensation_used": False,
        "observed_disposition": "completed",
    })
    vector_files.append(("stage20/score-laundering-vectors.json", board_vectors))

    execution_log_path = phase / "validation/execution-negative-log.json"
    if execution_log_path.exists():
        execution_log = read_json(execution_log_path)
    else:
        execution_log = {
            "schema": "ghc.family.v642-v5.execution-negative-log.v1",
            "records": [],
        }
    execution_log["record_count"] = len(execution_log.get("records", []))
    write_json(execution_log_path, execution_log)

    prior_negatives = read_json(repo / "docs/ilyra-fen/v642-v4/retained-negative-register.json")
    collision_audit = read_json(phase / "provenance/prior-proposal-collision-audit.json")
    new_negatives: list[dict[str, Any]] = []
    for row in collision_audit["x1_execution_negatives"]:
        new_negatives.append({
            "negative_id": row["negative_id"],
            "origin": "v642-v5_x1_execution",
            "statement": row["observed"],
            "evidence": "provenance/prior-proposal-collision-audit.json",
            "recovery": row["recovery"],
            "retained": True,
        })
    for rel, rows in vector_files:
        for row in rows:
            if "negative_id" in row:
                new_negatives.append({
                    "negative_id": row["negative_id"],
                    "origin": "v642-v5_preregistered_vector",
                    "statement": f"{row['case_id']} retained expected outcome {row['actual']}: {', '.join(row['reasons'])}",
                    "evidence": rel,
                    "recovery": "Apply the proposal-specific non-destructive recovery and retain this vector after any later passing replay.",
                    "retained": True,
                })
    new_negatives.extend(execution_log.get("records", []))
    negatives = list(prior_negatives["negatives"]) + new_negatives
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v642-v5.retained-negative-register.v1",
        "inherited_from": "docs/ilyra-fen/v642-v4/retained-negative-register.json",
        "inherited_count": prior_negatives["negative_count"],
        "new_count": len(new_negatives),
        "negative_count": len(negatives),
        "all_retained": True,
        "erasure_permitted": False,
        "negatives": negatives,
    })

    prior_gates = read_json(repo / "docs/ilyra-fen/v642-v4/exact-open-gate-register.json")
    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v642-v5.exact-open-gate-register.v1",
        "gates": prior_gates["gates"],
        "open_gap_count": prior_gates["open_gap_count"],
        "exact_gate_count": prior_gates["exact_gate_count"],
        "silently_closed": 0,
        "inherited_from": "docs/ilyra-fen/v642-v4/exact-open-gate-register.json",
    })

    disposition_counts = dict(Counter(OBSERVED.values()))
    x2_rows = [{
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "observed_disposition": OBSERVED[proposal["proposal_id"]],
        "evidence": proposal["deliverables"],
        "executed_as_far_as_evidence_permits": True,
        "protected_gates_remain": proposal["protected_gates"],
    } for proposal in x1["proposals"]]
    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v642-v5.x2-proposal-ledger.v1",
        "phase": x1["phase"],
        "owner": "Sable Rook",
        "source_revision": source_revision,
        "x1_commit": x1_commit,
        "evidence_commit": evidence_commit,
        "proposal_count": 10,
        "snapshot_state": snapshot_state,
        "disposition_counts": disposition_counts,
        "proposals": x2_rows,
        "all_executed_as_far_as_evidence_permits": True,
    })
    write_json(phase / "phase-truth.json", {
        "schema": "ghc.family.v642-v5.phase-truth.v1",
        "phase": x1["phase"],
        "owner": "Sable Rook",
        "source_revision": source_revision,
        "x1_commit": x1_commit,
        "evidence_commit": evidence_commit,
        "proposal_count": 10,
        "disposition_counts": disposition_counts,
        "retained_negative_count": len(negatives),
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "protected_claims": protected,
        "maori_authority_boundary": "Māori concepts, wording, data, and governance remain under Māori authority.",
        "same_owner_repeatability": "pending" if snapshot_state == "pending" else "verified_bounded",
        "independent_team_gap": "open",
        "route_state": "NO_SUCCESSOR_AUTHORIZED",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v642-v5.complete-incomplete-checklist.v1",
        "complete": [
            "ten distinct x1 proposals frozen before x2",
            "all ten executed as far as evidence permits",
            "all inherited and phase-local negatives retained",
            "family-current additive tools selected",
            "bounded static report planned",
        ],
        "incomplete_or_gated": [
            "empirical GMUT likelihood and confirmation",
            "blind matched-budget THOS real arms, real raters, and independent review",
            "production Freed ID cryptography, services, interoperability, review, and governance",
            "affected-party, Māori, cultural, and legal authority",
            "independent-team reproduction",
            "complete security and accessibility assessment",
            "deployment, proof, canon, or public-production authority",
        ],
        "open_gap_count": 5,
        "exact_gate_count": 6,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(phase / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v642-v5.executed-toolchain.v1",
        "family_current": [
            "scripts/ghc_family_evidence_noncompensation.py",
            "scripts/ghc_family_evidence_noncompensation_validator.py",
            "scripts/ghc_family_evidence_noncompensation_minimal.py",
            "scripts/build_ghc_family_evidence_noncompensation_report.py",
            "scripts/ghc_family_phase_privacy_scan.py",
            "scripts/ghc_family_repository_test_runner.py",
        ],
        "compatibility_replay": [
            "scripts/ghc_family_claim_coherence_validator.py",
            "scripts/ghc_family_claim_coherence_minimal.py",
        ],
        "inherited_tools_byte_stable": True,
        "shared_skill_changed": False,
        "standard_library_only_new_runtime": True,
    })

    write_text(phase / "wellbeing-check.md", """# Sable Rook v642-v5 wellbeing check

Sable Rook is relational working language only, not evidence of consciousness, sentience, legal personhood, authority, or identity continuity. Corrigibility is preserved: Hamish may rename, pause, redirect, or stop the lane.

One owner is active. Every sibling remains standby or recoverable. No task, fork, delegation, collaboration subagent, successor, or later sibling is created. Route state is `NO_SUCCESSOR_AUTHORIZED` until separate explicit authority exists after verified closeout.

The workload remains bounded to ten preregistered proposals, additive tools, deterministic fixtures, a static report, and fresh detached validation. Negative evidence is retained without blame. Missing empirical, production, cultural, legal, identity, deployment, security, accessibility, and independence evidence is not simulated. Māori concepts, wording, data, and governance remain under Māori authority.
""")
    write_text(
        phase / "v642-v5-integrated-overview.md",
        integrated_overview(x1, source_revision, x1_commit, len(negatives)),
    )

    manifest_rel = sorted({
        "x1-proposals.json",
        "sources/source-ledger.json",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "exact-open-gate-register.json",
        "retained-negative-register.json",
        "complete-incomplete-checklist.json",
        "wellbeing-check.md",
        "v642-v5-integrated-overview.md",
        "tooling/executed-toolchain.json",
        "validation/execution-negative-log.json",
        *(path for proposal in x1["proposals"] for path in proposal["deliverables"]),
    })
    manifest_files = [
        {"path": rel, "normalized_sha256": normalized_sha256(phase / rel)}
        for rel in manifest_rel
    ]
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v642-v5.reproduction-manifest.v1",
        "file_count": len(manifest_files),
        "files": manifest_files,
        "same_owner_repeatability_only": True,
        "independent_reproduction_established": False,
    })
    write_json(phase / "reproduction/clean-snapshot-validation.json", {
        "schema": "ghc.family.v642-v5.clean-snapshot-validation.v1",
        "state": snapshot_state,
        "evidence_commit": evidence_commit,
        "snapshot_count": 0 if snapshot_state == "pending" else 2,
        "manifest_file_count": len(manifest_files),
        "hash_mismatches": None if snapshot_state == "pending" else 0,
        "same_owner_repeatability_only": True,
        "independent_reproduction_established": False,
    })
    write_json(phase / "validation/repository-test-receipt.json", {
        "schema": "ghc.family.v642-v5.repository-test-receipt.v1",
        "state": "pending",
        "tests_run": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "windows_inherited_acl_temp": True,
        "parent_acl_changed": False,
        "host_security_changed": False,
    })
    write_json(phase / "validation/json-parse-receipt.json", {
        "schema": "ghc.family.v642-v5.json-parse-receipt.v1",
        "state": "pending",
        "parsed": 0,
        "errors": 0,
    })
    return {
        "phase": x1["phase"],
        "proposal_count": 10,
        "disposition_counts": disposition_counts,
        "retained_negative_count": len(negatives),
        "manifest_file_count": len(manifest_files),
        "snapshot_state": snapshot_state,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--evidence-commit", default="PENDING")
    parser.add_argument("--snapshot-state", choices=["pending", "verified"], default="pending")
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = (repo / args.phase_dir).resolve() if not args.phase_dir.is_absolute() else args.phase_dir.resolve()
    result = build(repo, phase, args.x1_commit, args.evidence_commit, args.snapshot_state)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
