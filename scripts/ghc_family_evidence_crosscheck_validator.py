#!/usr/bin/env python3
"""Validate bounded v642-v2 GHC evidence-crosscheck artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_COUNTS = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(phase: Path, allow_pending_snapshot: bool, require_report: bool) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "pass": bool(condition), "detail": detail})

    required = [
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
        "security/threat-model.md", "security/canonical-input-policy.json", "security/parser-differential-vectors.json",
        "security/recovery-resource-receipt.json", "reproduction/cross-owner-lineage-replay.json",
        "reproduction/semantic-normalization-manifest.json", "reproduction/manifest.json",
        "reproduction/environment-perturbation-receipt.json", "reproduction/independent-team-gap.json",
        "thermo-psyche/measurement-invariance-vectors.json", "thermo-psyche/temporal-order-register.json",
        "thermo-psyche/category-boundary-matrix.json", "thermo-psyche/classification-receipt.json",
        "stage20/gate-dominance-matrix.json", "stage20/evidence-freshness-ledger.json",
        "stage20/decision-monotonicity-vectors.json", "stage20/pass-fail-defer-board.json",
        "stage20/terminal-verdict.json", "x2-proposal-ledger.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "phase-truth.json", "complete-incomplete-checklist.json",
        "tooling/executed-toolchain.json", "validation/execution-negative-log.json",
        "v642-v2-integrated-overview.md",
    ]
    for rel in required:
        check(f"required artifact exists: {rel}", (phase / rel).is_file())
    if not all((phase / rel).is_file() for rel in required):
        issues = [row for row in checks if not row["pass"]]
        return {"schema": "ghc.family.evidence-crosscheck-validation.v1", "valid": False,
                "check_count": len(checks), "pass_count": len(checks) - len(issues), "issue_count": len(issues),
                "issues": issues, "checks": checks}

    x1 = load(phase / "x1-proposals.json")
    source = load(phase / "sources/source-ledger.json")
    collision = load(phase / "provenance/prior-proposal-collision-audit.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    overlap = load(phase / "provenance/evidence-root-overlap-matrix.json")
    debt = load(phase / "provenance/independence-debt-ledger.json")
    reach = load(phase / "provenance/negative-reachability-receipt.json")
    ast = load(phase / "physics/canonical-equation-ast.json")
    units = load(phase / "physics/unit-basis-and-covariance-vectors.json")
    witness = load(phase / "physics/conservation-stability-jacobian-witness.json")
    id_boundary = load(phase / "physics/identifiability-claim-boundary.json")
    adapter = load(phase / "empirical/public-data-adapter-contract.json")
    schema_vectors = load(phase / "empirical/round-trip-schema-vectors.json")
    readiness = load(phase / "empirical/null-baseline-readiness.json")
    empirical_gate = load(phase / "empirical/real-data-likelihood-gate.json")
    escrow = load(phase / "thos/allocation-escrow-spec.json")
    thos_vectors = load(phase / "thos/blindness-budget-mutation-vectors.json")
    attrition = load(phase / "thos/attrition-decision-table.json")
    thos_gate = load(phase / "thos/real-arm-execution-gate.json")
    freed_profile = load(phase / "freed-id/cross-layer-conformance-profile.json")
    freed_vectors = load(phase / "freed-id/status-resolver-consistency-vectors.json")
    trust = load(phase / "freed-id/trust-governance-assumption-ledger.json")
    freed_gate = load(phase / "freed-id/production-assurance-gate.json")
    authority = load(phase / "cbr/authority-scope-lifecycle.json")
    consent = load(phase / "cbr/consent-revocation-vectors.json")
    remedy = load(phase / "cbr/remedy-nonretrogression-matrix.json")
    cbr_gate = load(phase / "cbr/legal-cultural-authority-gate.json")
    policy = load(phase / "security/canonical-input-policy.json")
    parser_vectors = load(phase / "security/parser-differential-vectors.json")
    recovery = load(phase / "security/recovery-resource-receipt.json")
    replay = load(phase / "reproduction/cross-owner-lineage-replay.json")
    perturb = load(phase / "reproduction/environment-perturbation-receipt.json")
    independent = load(phase / "reproduction/independent-team-gap.json")
    invariance = load(phase / "thermo-psyche/measurement-invariance-vectors.json")
    temporal = load(phase / "thermo-psyche/temporal-order-register.json")
    categories = load(phase / "thermo-psyche/category-boundary-matrix.json")
    classification = load(phase / "thermo-psyche/classification-receipt.json")
    dominance = load(phase / "stage20/gate-dominance-matrix.json")
    freshness = load(phase / "stage20/evidence-freshness-ledger.json")
    monotonic = load(phase / "stage20/decision-monotonicity-vectors.json")
    board = load(phase / "stage20/pass-fail-defer-board.json")
    verdict = load(phase / "stage20/terminal-verdict.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    manifest = load(phase / "reproduction/semantic-normalization-manifest.json")
    execution_negatives = load(phase / "validation/execution-negative-log.json")

    required_fields = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs",
                       "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates",
                       "expected_disposition", "novelty_against_prior_chain"}
    check("x1 proposal count is ten", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("x1 ids unique", len({p["proposal_id"] for p in x1["proposals"]}) == 10)
    check("x1 fields complete", all(required_fields <= set(p) for p in x1["proposals"]))
    check("truth labels exact", x1["outcome_classes"] == TRUTH_LABELS)
    check("x1 expected counts exact", dict(Counter(p["expected_disposition"] for p in x1["proposals"])) == EXPECTED_COUNTS)
    check("expected counts are not results", x1["expected_counts_are_results"] is False)
    check("x2 proposal count ten", x2["proposal_count"] == len(x2["proposals"]) == 10)
    check("x2 observed counts exact", x2["disposition_counts"] == EXPECTED_COUNTS)
    check("x2 expected and observed remain explicit", all("expected_disposition" in p and "observed_disposition" in p for p in x2["proposals"]))
    check("all proposals executed as evidence permits", x2["all_executed_as_far_as_evidence_permits"] is True and all(p["executed_as_far_as_evidence_permits"] for p in x2["proposals"]))

    source_ids = {s["source_id"] for s in source["sources"]}
    check("source count 38", source["source_count"] == len(source["sources"]) == 38)
    check("source ids unique", len(source_ids) == 38)
    check("source statuses exact", dict(Counter(s["status_class"] for s in source["sources"])) == {"current": 20, "stable": 14, "draft": 3, "watch": 1})
    check("source references close", not {sid for p in x1["proposals"] for sid in p["authoritative_source_needs"] if sid not in source_ids})
    check("draft pins remain draft", all(s["status_class"] == "draft" for s in source["sources"] if s["source_id"] in {"V8-S14", "V8-S15", "V6421-S33"}))
    check("collision audit prior 80", collision["prior_phase_counts"]["total"] == 80)
    check("collision audit ten candidates", collision["candidate_count"] == 10)
    check("zero exact title collisions", collision["exact_title_collisions"] == 0)
    check("semantic delta review passed", collision["semantic_delta_review_passed"] is True)
    check("lexical score not semantic proof", collision["method"]["lexical_score_is_semantic_proof"] is False)
    check("frozen chain count 90", chain["proposal_count"] == len(chain["records"]) == 90)
    check("frozen chain version counts", chain["version_counts"].get("v642-v2") == 10 and sum(chain["version_counts"].values()) == 90)
    check("frozen titles unique", len({r["title"] for r in chain["records"]}) == 90)

    check("provenance axes complete", overlap["axes"] == ["authority", "dataset", "software", "funding_or_derivation", "citation_context"])
    check("false independence rejected", overlap["false_independent_cases_rejected"] == 4)
    check("document count not independence", overlap["document_count_is_independence_count"] is False)
    check("independence debt retained", debt["open_debt_count"] == len(debt["debts"]) == 4 and debt["erasure_permitted"] is False)
    check("all inherited negatives reachable", reach["reachable_inherited_negatives"] == reach["inherited_negative_count"] == 46 and not reach["unreachable_negatives"])
    check("canonicalization not signature", reach["canonicalization_is_signature_or_independence_proof"] is False)

    check("typed model class bounded", ast["model_class"] == "typed scalar-tensor EFT research scaffold")
    check("SI dimension basis complete", ast["dimension_basis"] == ["M", "L", "T"])
    check("equations typed", all(e["typed"] for e in ast["equations"]))
    check("equations not empirically confirmed", not any(e["empirically_confirmed"] for e in ast["equations"]))
    check("invalid unit vectors rejected", units["invalid_vectors_rejected"] == 5)
    check("rank invariant under unit basis", units["rank_invariant_under_valid_unit_basis"] is True)
    check("Jacobian fixtures preserve degeneracy", any(f.get("jacobian_rank", 99) < f.get("parameter_count", 0) for f in witness["fixtures"]))
    check("Jacobian evidence structural only", witness["structural_observability_only"] is True and witness["empirical_identifiability"] is False)
    check("physics protected claims false", not any(id_boundary[k] for k in ["detected_force", "unique_prediction", "empirical_gmut_confirmation", "proof_or_canon"]))

    check("adapter metadata only", adapter["mode"] == "metadata_only_rowless" and adapter["network_download"] is False)
    check("schema invalid vectors quarantined", schema_vectors["invalid_vectors_quarantined"] == 5)
    check("no implicit imputation", schema_vectors["implicit_imputation_allowed"] is False)
    check("zero-row empirical boundary", readiness["parsed_measurement_rows"] == readiness["likelihoods_executed"] == readiness["fits_executed"] == 0)
    check("empirical disposition represented", readiness["disposition"] == "represented" and readiness["readiness_is_fit"] is False)
    check("real-data gate open", empirical_gate["state"] == "open" and empirical_gate["empirical_gmut_confirmation"] is False)

    check("THOS escrow synthetic", escrow["mode"] == "synthetic_protocol_only")
    check("THOS zero real arms", escrow["real_arm_runs"] == thos_gate["real_arm_runs"] == 0)
    check("THOS mutations rejected", thos_vectors["mutations_rejected"] == len(thos_vectors["vectors"]) == 6)
    check("THOS post-hoc deletion forbidden", attrition["post_hoc_deletion_allowed"] is False)
    check("THOS observed disposition open", thos_gate["state"] == "open_gap")
    check("THOS protected claims false", not any(thos_gate[k] for k in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))

    check("Freed profile structural only", freed_profile["mode"] == "synthetic_structural_only")
    check("Freed invalid vectors rejected", freed_vectors["invalid_vectors_rejected"] == 6 and freed_vectors["real_cryptographic_operations"] == 0)
    check("Freed trust assumptions open", all(a["state"] == "open" for a in trust["assumptions"]))
    check("Freed governance not assigned", trust["technical_artifact_can_assign_governance"] is False)
    check("Freed production evidence absent", all(freed_gate[k] == 0 for k in ["real_keys", "real_proofs", "live_resolvers", "live_status_services", "interoperability_partners", "independent_security_reviews"]))
    check("Freed assurance false", freed_gate["trust_governance_established"] is False and freed_gate["cryptographic_assurance"] is False)

    check("CBR authority not system-assigned", authority["system_may_assign_authority"] is False)
    check("CBR withdrawal precedence", authority["withdrawal_precedence"] is True)
    check("Māori authority nontransferable", authority["maori_authority_nontransferable"] is True)
    check("CBR vectors all defer", all(v["decision"] == "defer" for v in consent["vectors"]))
    check("CBR remedy floor preserved", all(c["remedy_floor_preserved"] for c in remedy["cases"]) and remedy["artifact_may_waive_remedy"] is False)
    check("CBR exact gate", cbr_gate["state"] == "exact_gate")
    check("CBR authority absent", not any(cbr_gate[k] for k in ["affected_party_authority_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))
    check("CBR exact Māori boundary", "Māori authority" in cbr_gate["boundary"])

    check("strict duplicate keys", policy["duplicate_keys"] == "reject")
    check("strict non-finite numbers", policy["non_finite_numbers"] == "reject")
    check("strict unsafe integers", policy["unsafe_integer_domain"] == "reject")
    check("strict Unicode collisions", policy["unicode_normalization_collision"] == "reject")
    check("parser disagreement quarantined", policy["parser_disagreement"] == "quarantine")
    check("parser vectors all rejected", parser_vectors["strict_rejections"] == len(parser_vectors["vectors"]) == 8 and not any(v["strict_accept"] for v in parser_vectors["vectors"]))
    check("security recovery non-destructive", recovery["destructive_cleanup"] is False and recovery["elevation"] is False)
    check("host state unchanged", recovery["host_security_changed"] is False and recovery["windows_features_changed"] is False and recovery["reboot"] is False)
    check("security not exhaustive", recovery["exhaustive_security"] is False)

    check("source replay tests exact", replay["source_repository_tests"] == {"passed": 170, "failed": 0})
    check("source replay validator exact", replay["source_phase_validator"] == {"passed": 89, "issues": 0})
    check("source replay minimal exact", replay["source_minimal_verifier"] == {"passed": 17, "issues": 0})
    snapshot_ok = x2["snapshot_state"] == "verified" and replay["cross_owner_internal_repeatability"] == "verified_bounded" and perturb["state"] == "verified"
    check("snapshot state acceptable", snapshot_ok or allow_pending_snapshot, x2["snapshot_state"])
    check("independent team remains absent", independent["independent_team_present"] is False and replay["independent_team_reproduction"] is False)
    check("strongest replay claim bounded", "cross-owner internal repeatability" in independent["strongest_allowed_claim"])

    check("measurement invalid vectors rejected", invariance["noninvariant_vectors_rejected"] == 5)
    check("temporal reversal rejected", any(c["case"] == "effect_precedes_claimed_cause" and c["accepted"] is False for c in temporal["cases"]))
    check("temporal order not causality proof", temporal["temporal_order_alone_proves_causality"] is False)
    check("thermo psyche six classes exact", categories["classes"] == ["thermodynamic", "computational", "psychological", "metaphorical", "emergent", "fundamental_law_candidate"])
    check("category promotion forbidden", categories["automatic_cross_category_promotion"] is False and categories["computational_telemetry_is_subjective_experience"] is False)
    check("thermo psyche protected claims false", not any(classification[k] for k in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood"]))

    check("five dominant open gaps", len(dominance["dominant_open_gaps"]) == 5)
    check("six dominant exact gates", len(dominance["dominant_exact_gates"]) == 6)
    check("technical score cannot override exact gate", dominance["technical_score_may_override_exact_gate"] is False)
    check("expired support cannot pass", freshness["expired_or_withdrawn_supports_pass"] is False)
    check("freshness not truth", freshness["freshness_implies_truth"] is False)
    check("monotonic invalid improvements rejected", monotonic["invalid_improvements_rejected"] == 2)
    check("board uses pass fail defer", set(board["decisions"]) == {"pass", "fail", "defer"})
    check("board authority non-substitutable", board["authority_non_substitutable"] is True)
    check("terminal verdict exact", verdict["verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("terminal deployment false", verdict["deployment_authorized"] is False and verdict["successor_authorized_by_artifact"] is False)

    check("negative count 66", negatives["negative_count"] == len(negatives["negatives"]) == 66)
    check("negative inheritance 46 plus 20", negatives["inherited_count"] == 46 and negatives["new_count"] == 20)
    check("all negatives retained", negatives["all_retained"] is True and all(n["retained"] for n in negatives["negatives"]))
    check("negative erasure forbidden", negatives["erasure_permitted"] is False)
    check("execution failures retained", execution_negatives["negative_count"] == 6 and [row["negative_id"] for row in execution_negatives["negatives"]] == ["V6422-N15", "V6422-N16", "V6422-N17", "V6422-N18", "V6422-N19", "V6422-N20"] and all(row["preserved"] for row in execution_negatives["negatives"]))
    check("gate counts exact", gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6)
    check("no gates silently closed", gates["silently_closed"] == 0 and all(g["state"] in {"open", "deferred"} for g in gates["gates"]))
    check("phase truth counts exact", truth["disposition_counts"] == EXPECTED_COUNTS)
    check("phase truth negative count", truth["retained_negative_count"] == 66)
    check("all protected claims false", not any(truth["protected_claims"].values()))
    check("independent team gap open", truth["independent_team_gap"] == "open")

    check("manifest artifact count matches", manifest["artifact_count"] == len(manifest["hashes"]))
    mismatches = [rel for rel, digest in manifest["hashes"].items() if not (phase / rel).is_file() or normalized_sha256(phase / rel) != digest]
    check("manifest normalized hashes match", not mismatches, mismatches)
    aggregate = hashlib.sha256("".join(f"{k}:{manifest['hashes'][k]}\n" for k in sorted(manifest["hashes"])).encode()).hexdigest()
    check("manifest aggregate matches", aggregate == manifest["aggregate_sha256"])
    check("manifest has no absolute path dependency", manifest["absolute_paths_required"] is False)
    check("manifest preserves independent gap", manifest["independent_team_reproduction"] is False)

    overview = (phase / "v642-v2-integrated-overview.md").read_text(encoding="utf-8")
    words = len(re.findall(r"\b\w+[\w'-]*\b", overview))
    check("overview is three-page equivalent", words >= 1800, words)
    for phrase in ["NOT_READY_FOR_STAGE_20", "Māori authority", "cross-owner internal repeatability", "zero measurement rows", "not a complete WCAG conformance assessment"]:
        check(f"overview contains boundary: {phrase}", phrase in overview)

    report = phase / "deliverables/v642-v2-evidence-crosscheck-report.html"
    check("static report exists when required", report.is_file() or not require_report)
    if report.is_file():
        html = report.read_text(encoding="utf-8")
        for phrase in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            check(f"report contains {phrase}", phrase in html)
        check("report accessibility claim bounded", "not a complete WCAG conformance assessment" in html)

    issues = [row for row in checks if not row["pass"]]
    return {
        "schema": "ghc.family.evidence-crosscheck-validation.v1", "valid": not issues,
        "check_count": len(checks), "pass_count": len(checks) - len(issues), "issue_count": len(issues),
        "issues": issues,
        "summary": {"proposal_count": 10, "disposition_counts": EXPECTED_COUNTS, "negative_count": 66,
                    "open_gap_count": 5, "exact_gate_count": 6, "manifest_files": manifest["artifact_count"],
                    "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
        "checks": checks,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    result = validate(phase, args.allow_pending_snapshot, args.require_report)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else phase / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
