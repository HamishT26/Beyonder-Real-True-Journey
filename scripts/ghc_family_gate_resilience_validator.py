#!/usr/bin/env python3
"""Validate a bounded GHC family gate-resilience evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


REQUIRED_FILES = [
    "x1-proposals.json", "x1-preregistration.md", "x2-proposal-ledger.json", "x2-proposal-ledger.md",
    "sources/source-ledger.json", "provenance/frozen-chain-proposal-index.json", "provenance/authority-liveness-quorum.json",
    "provenance/source-retraction-replay.json", "provenance/semantic-novelty-audit.json",
    "physics/canonical-gmut-obligation-matrix.json", "physics/tensor-unit-covariance-mutations.json",
    "physics/stability-identifiability-kill-matrix.json", "physics/assumption-trace.json",
    "empirical/dataset-integrity-manifest.json", "empirical/schema-license-drift-vectors.json",
    "empirical/adapter-zero-fit-receipt.json", "empirical/baseline-readiness-docket.json",
    "thos/estimand-lock.json", "thos/matched-budget-accounting.json", "thos/attrition-missingness-vectors.json", "thos/real-arm-gap.json",
    "freed-id/lifecycle-product-automaton.json", "freed-id/resolver-freshness-cache-vectors.json",
    "freed-id/status-privacy-interoperability-matrix.json", "freed-id/production-trust-gate.json",
    "cbr/contestability-remedy-protocol.json", "cbr/recusal-authority-nonsubstitution.json",
    "cbr/maori-authority-boundary.json", "cbr/legal-cultural-exact-gates.json",
    "security/threat-model.md", "security/manifest-swap-toctou-vectors.json", "security/link-reparse-boundary.json",
    "security/recovery-rto-drill.json", "security/privacy-raw-id-controls.json",
    "reproduction/external-executor-protocol.json", "reproduction/blinded-output-commitment.json",
    "reproduction/common-mode-dependency-split.json", "reproduction/clean-snapshot-validation.json", "reproduction/independent-team-gap.json",
    "thermo-psyche/promotion-state-machine.json", "thermo-psyche/evidence-burden-matrix.json",
    "thermo-psyche/prohibited-transition-vectors.json", "thermo-psyche/classification-register.json",
    "stage20/gate-dependency-graph.json", "stage20/minimal-blocking-cutsets.json", "stage20/stop-rule-mutations.json",
    "stage20/terminal-evidence-board.json", "retained-negative-register.json", "exact-open-gate-register.json",
    "phase-truth.json", "phase-truth.md", "complete-incomplete-checklist.json", "complete-incomplete-checklist.md",
    "environment/version-receipt.json", "tooling/executed-toolchain.json", "v641-v8-integrated-overview.md",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(phase: Path, allow_pending: bool = False, require_report: bool = False, output: Path | None = None) -> dict:
    issues: list[str] = []
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            issues.append(message)

    phase = phase.resolve()
    for rel in REQUIRED_FILES:
        check((phase / rel).is_file(), f"missing required file: {rel}")
    if issues:
        report = {"schema": "ghc.family.v641-v8.validation.v1", "valid": False, "checks": checks, "issues": issues}
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return report

    parsed: dict[str, dict] = {}
    for path in phase.rglob("*.json"):
        rel = path.relative_to(phase).as_posix()
        try:
            parsed[rel] = load(path)
        except Exception as exc:  # pragma: no cover - diagnostic path
            issues.append(f"JSON parse failed for {rel}: {exc}")
    check(not any("JSON parse failed" in issue for issue in issues), "one or more JSON files failed to parse")

    x1 = parsed["x1-proposals.json"]
    required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "expected_disposition", "novelty_against_prior_chain"}
    check(x1.get("proposal_count") == 10 and len(x1.get("proposals", [])) == 10, "x1 must contain exactly ten proposals")
    check(len({row.get("proposal_id") for row in x1["proposals"]}) == 10, "x1 proposal IDs must be unique")
    check(all(required <= set(row) for row in x1["proposals"]), "x1 proposal fields are incomplete")
    check(x1.get("source_revision") == "008fb47054eb313a439999d5a5b4ddc2e863e187", "x1 source revision mismatch")

    source = parsed["sources/source-ledger.json"]
    check(source.get("source_count") == 31 and len(source.get("sources", [])) == 31, "source ledger count mismatch")
    check(Counter(row["status_class"] for row in source["sources"]) == Counter(source["status_counts"]), "source status counts mismatch")
    source_ids = {row["source_id"] for row in source["sources"]}
    check(not ({ref for row in x1["proposals"] for ref in row["authoritative_source_needs"]} - source_ids), "unresolved proposal source reference")

    chain = parsed["provenance/frozen-chain-proposal-index.json"]
    check(chain.get("proposal_count") == 70, "frozen chain must contain 70 proposals")
    check(chain.get("version_counts") == {f"v{n}": 10 for n in range(2, 9)}, "frozen chain version counts mismatch")
    check(chain.get("exact_duplicate_titles") == [], "frozen chain contains exact duplicate titles")
    novelty = parsed["provenance/semantic-novelty-audit.json"]
    check(novelty.get("prior_proposals_reviewed") == 60 and novelty.get("all_distinct") is True, "semantic novelty audit failed")
    quorum = parsed["provenance/authority-liveness-quorum.json"]
    check(quorum.get("all_quorums_current") is True and quorum.get("independence_is_root_based_not_document_count") is True, "authority quorum invariant failed")
    replay = parsed["provenance/source-retraction-replay.json"]
    check(replay.get("mutation_count") == 8 and replay.get("all_required_downgrades_observed") is True and replay.get("silently_retained_strength") == 0, "source retraction replay failed")

    gmut = parsed["physics/canonical-gmut-obligation-matrix.json"]
    check(gmut.get("equations") == ["G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}", "Omega_{mu nu} = M_Pl^{-2} (T^phi_{mu nu} + T^{EFT}_{mu nu})"], "canonical GMUT equations changed")
    check(gmut.get("coverage") == {"declared": 8, "linked_to_assumption": 8, "linked_to_rejecting_test": 8}, "GMUT obligation coverage incomplete")
    check(not gmut.get("empirical_confirmation") and not gmut.get("theory_of_everything"), "GMUT protected claims inflated")
    tensor_mut = parsed["physics/tensor-unit-covariance-mutations.json"]
    stability_mut = parsed["physics/stability-identifiability-kill-matrix.json"]
    check(tensor_mut.get("all_killed") is True and stability_mut.get("all_killed") is True, "one or more GMUT mutations survived")
    check(stability_mut.get("mutation_score") == 1.0 and not stability_mut.get("empirical_stability_or_identifiability"), "GMUT mutation score or boundary invalid")
    check(parsed["physics/assumption-trace.json"].get("unlinked_obligations") == [], "GMUT assumption trace has unlinked obligations")

    empirical = parsed["empirical/adapter-zero-fit-receipt.json"]
    check(empirical.get("real_measurement_rows_parsed") == 0 and not empirical.get("likelihood_executed") and not empirical.get("parameter_fit_executed"), "empirical zero-fit boundary failed")
    check(parsed["empirical/schema-license-drift-vectors.json"].get("all_quarantined") is True, "adapter drift vector escaped quarantine")
    check(parsed["empirical/baseline-readiness-docket.json"].get("promotion_allowed") is False, "baseline docket permits unsupported promotion")

    estimand = parsed["thos/estimand-lock.json"]
    budget = parsed["thos/matched-budget-accounting.json"]
    check(estimand.get("synthetic_only") is True and estimand.get("real_arm_runs") == 0 and not estimand.get("superiority_result"), "THOS proxy boundary failed")
    check(budget.get("declared_budgets_equal") is True and not budget.get("real_cost_observation"), "THOS budget accounting invalid")
    check(parsed["thos/attrition-missingness-vectors.json"].get("all_rejected_before_unseal") is True, "THOS attrition mutation escaped")
    check(parsed["thos/real-arm-gap.json"].get("real_arms_present") is False, "THOS real-arm gap was silently closed")

    lifecycle = parsed["freed-id/lifecycle-product-automaton.json"]
    check(lifecycle.get("all_invalid_rejected") is True and lifecycle.get("real_credentials") == 0, "Freed ID lifecycle invariant failed")
    check(parsed["freed-id/resolver-freshness-cache-vectors.json"].get("all_rejected") is True, "Freed ID resolver freshness vector escaped")
    trust = parsed["freed-id/production-trust-gate.json"]
    check(trust.get("satisfied_count") == 0 and trust.get("disposition") == "open_gap" and not trust.get("deployment_authorized"), "Freed ID production gate inflated")

    cbr = parsed["cbr/contestability-remedy-protocol.json"]
    maori = parsed["cbr/maori-authority-boundary.json"]
    check(cbr.get("algorithmic_live_resolutions") == 0 and cbr.get("all_conflicts_deferred") is True, "CBR conflict was algorithmically resolved")
    check(not maori.get("Māori_authority_present") and not maori.get("system_may_speak_for_Māori") and maori.get("decision") == "exact_gate", "Māori authority boundary failed")
    check(parsed["cbr/legal-cultural-exact-gates.json"].get("satisfied") == [], "legal or cultural exact gate silently closed")

    toctou = parsed["security/manifest-swap-toctou-vectors.json"]
    links = parsed["security/link-reparse-boundary.json"]
    recovery = parsed["security/recovery-rto-drill.json"]
    check(toctou.get("all_detected") is True and not toctou.get("exhaustive_security"), "TOCTOU boundary or detections invalid")
    check(links.get("actual_links_created") is False and links.get("unsafe_vectors_rejected") == 4, "link-boundary fixture invalid")
    check(recovery.get("pass") is True and recovery.get("destructive_commands") == 0 and not recovery.get("privilege_expansion"), "recovery drill unsafe")

    commitment = parsed["reproduction/blinded-output-commitment.json"]
    current_hashes = {rel: normalized_sha256(phase / rel) for rel in commitment["normalized_hashes"]}
    check(current_hashes == commitment["normalized_hashes"], "core artifact commitment hash mismatch")
    aggregate = hashlib.sha256("".join(f"{key}:{current_hashes[key]}\n" for key in sorted(current_hashes)).encode()).hexdigest()
    check(aggregate == commitment.get("aggregate_sha256") and commitment.get("artifact_count") == len(current_hashes), "aggregate commitment mismatch")
    protocol_text = json.dumps(parsed["reproduction/external-executor-protocol.json"], ensure_ascii=False)
    check(not re.search(r"[A-Za-z]:[\\/]", protocol_text) and not re.search(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}\b", protocol_text), "external protocol leaks a private path or raw UUID")
    snap = parsed["reproduction/clean-snapshot-validation.json"]
    check(snap.get("state") in {"pending", "verified"}, "snapshot state invalid")
    if not allow_pending:
        check(snap.get("state") == "verified" and snap.get("verified_snapshots") == 2 and snap.get("same_owner_repeatability") is True, "clean snapshot verification is incomplete")
    check(parsed["reproduction/independent-team-gap.json"].get("gap") == "open" and not parsed["reproduction/common-mode-dependency-split.json"].get("independent_team_reproduction"), "independent-team gap was silently closed")

    promotion = parsed["thermo-psyche/promotion-state-machine.json"]
    expected_classes = {"category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"}
    check(set(promotion.get("classes", [])) == expected_classes and promotion.get("every_promotion_adds_burden") is True, "thermo-psyche promotion state machine invalid")
    check(parsed["thermo-psyche/prohibited-transition-vectors.json"].get("all_rejected") is True, "prohibited thermo-psyche transition escaped")
    classification = parsed["thermo-psyche/classification-register.json"]
    check(classification.get("fundamental_physical_laws_established") == 0 and classification.get("consciousness_tensors_established") == 0, "thermo-psyche protected claim inflated")

    board = parsed["stage20/terminal-evidence-board.json"]
    check(set(row["decision"] for row in board.get("board", [])) == {"pass", "fail", "defer"}, "Stage 20 board lacks exact decision classes")
    check(board.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20" and board.get("stage20_complete") is False, "Stage 20 terminal verdict inflated")
    check(parsed["stage20/minimal-blocking-cutsets.json"].get("cutset_count") == 6 and parsed["stage20/minimal-blocking-cutsets.json"].get("every_cutset_blocks_ready") is True, "Stage 20 cut-set audit failed")
    check(parsed["stage20/stop-rule-mutations.json"].get("all_rejected") is True, "Stage 20 stop-rule mutation escaped")

    negatives = parsed["retained-negative-register.json"]
    check(negatives.get("inherited_count") == 20 and negatives.get("new_count") == 12 and negatives.get("negative_count") == 32, "retained negative counts mismatch")
    check(negatives.get("all_retained") is True and all(row.get("retained") for row in negatives.get("negatives", [])), "a negative was not retained")
    gates = parsed["exact-open-gate-register.json"]
    check(gates.get("open_gap_count") == 5 and gates.get("exact_gate_count") == 2 and gates.get("silently_closed") == 0, "open/exact gate counts invalid")

    ledger = parsed["x2-proposal-ledger.json"]
    check(ledger.get("proposal_count") == 10 and ledger.get("disposition_counts") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "x2 disposition counts invalid")
    check(ledger.get("x1_commit") == "4bbfbcc069894f60a9392799bb0fb15c03e6c954" and ledger.get("all_executed_as_far_as_evidence_permits") is True, "x1/x2 continuity invalid")
    truth = parsed["phase-truth.json"]
    check(truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20" and not any(truth.get("protected_claims", {}).values()), "phase truth protected claim or terminal verdict invalid")
    check(truth.get("independent_team_reproduction") is False, "phase truth overclaims independent reproduction")

    overview = (phase / "v641-v8-integrated-overview.md").read_text(encoding="utf-8")
    check(len(re.findall(r"\b\w+\b", overview)) >= 1800, "integrated overview is shorter than the three-page-equivalent floor")
    check("NOT_READY_FOR_STAGE_20" in overview and "Māori authority" in overview, "overview omits terminal or Māori authority boundary")
    checklist = parsed["complete-incomplete-checklist.json"]
    if not allow_pending:
        check(checklist.get("terminal_closeout_ready") is True and checklist.get("snapshot_verified") is True, "checklist is not closeout-ready")

    if require_report:
        report_path = phase / "deliverables/v641-v8-gate-resilience-report.html"
        check(report_path.is_file(), "static report is missing")
        if report_path.is_file():
            report_text = report_path.read_text(encoding="utf-8")
            for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
                check(token in report_text, f"static report missing structural token {token}")
            check("not a complete WCAG conformance assessment" in report_text, "static report omits accessibility boundary")

    report = {
        "schema": "ghc.family.v641-v8.validation.v1",
        "valid": not issues,
        "checks": checks,
        "issues": issues,
        "snapshot_state": snap.get("state"),
        "json_files_parsed": len(parsed),
        "required_file_count": len(REQUIRED_FILES),
        "terminal_verdict": board.get("terminal_verdict"),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate(args.phase_dir, allow_pending=args.allow_pending, require_report=args.require_report, output=args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
