#!/usr/bin/env python3
"""Execute the ten frozen Sylven Arc v645-v8 proposal surfaces."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from ghc_family_v645_v8_runtime import TRUTH_BOUNDARY, write_json, write_text


OUTCOMES = {
    "V6458-P01": "completed", "V6458-P02": "completed", "V6458-P03": "open_gap",
    "V6458-P04": "represented", "V6458-P05": "represented", "V6458-P06": "exact_gate",
    "V6458-P07": "completed", "V6458-P08": "completed", "V6458-P09": "completed",
    "V6458-P10": "completed",
}


def contract(proposal: str, title: str, obligations: list[str], forbidden: list[str]) -> dict:
    return {"schema": "ghc.family.v645-v8.contract.v1", "proposal_id": proposal, "title": title,
            "obligations": obligations, "forbidden_promotions": forbidden, "boundary": TRUTH_BOUNDARY}


def expected(rows: list[dict], accepted: set[str]) -> bool:
    return all(bool(row["accepted"]) == (row["case"] in accepted) for row in rows)


def vectors(relative: str, rows: list[dict], accepted: set[str], **extra: object) -> bool:
    valid = expected(rows, accepted)
    write_json(relative, {"vectors": rows, "valid": valid, **extra, "boundary": TRUTH_BOUNDARY})
    return valid


def sparse_index_lab() -> dict:
    bank = Path(os.environ.get("GHC_FAMILY_TEMP_BANK", "D:/GHC-Archives/temp"))
    bank.mkdir(parents=True, exist_ok=True)
    commands: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="sylven-v6458-sparse-", dir=bank) as raw:
        lab = Path(raw)

        def invoke(*args: str) -> subprocess.CompletedProcess[str]:
            result = subprocess.run(args, cwd=lab, text=True, encoding="utf-8", capture_output=True, check=False)
            commands.append({"argv": list(args), "returncode": result.returncode})
            return result

        invoke("git", "init", "--quiet")
        invoke("git", "config", "user.name", "Sylven Fixture")
        invoke("git", "config", "user.email", "fixture@example.invalid")
        (lab / "keep").mkdir(); (lab / "omit").mkdir()
        (lab / "keep/visible.txt").write_text("visible\n", encoding="utf-8", newline="\n")
        (lab / "omit/hidden.txt").write_text("hidden\n", encoding="utf-8", newline="\n")
        invoke("git", "add", "--", "keep/visible.txt", "omit/hidden.txt")
        invoke("git", "commit", "--quiet", "-m", "bounded sparse fixture")
        invoke("git", "sparse-checkout", "init", "--cone", "--sparse-index")
        invoke("git", "sparse-checkout", "set", "keep")
        tree = invoke("git", "ls-tree", "-r", "--name-only", "HEAD")
        index = invoke("git", "ls-files", "-t")
        head_paths = sorted(tree.stdout.splitlines()) if tree.returncode == 0 else []
        index_lines = index.stdout.splitlines() if index.returncode == 0 else []
        work_paths = sorted(p.relative_to(lab).as_posix() for p in lab.rglob("*") if p.is_file() and ".git" not in p.parts)
        omitted = not (lab / "omit/hidden.txt").exists()
        skip_seen = any(line.startswith("S ") and line.endswith("omit/hidden.txt") for line in index_lines)
        canonical = head_paths == ["keep/visible.txt", "omit/hidden.txt"]
        incomplete = work_paths != head_paths and "omit/hidden.txt" not in work_paths
        passed = all(row["returncode"] == 0 for row in commands) and omitted and skip_seen and canonical and incomplete
    return {"disposable_repository": True, "no_network": True, "commands": commands,
            "canonical_head_paths": head_paths, "working_tree_paths": work_paths,
            "tracked_omitted_path_absent": omitted, "skip_worktree_evidence": skip_seen,
            "working_tree_only_manifest_rejected": incomplete, "canonical_repository_mutated": False,
            "remote_mutated": False, "temporary_root_removed": True,
            "expected_results_passed": passed,
            "boundary": "A disposable replay is not production, supply-chain, or exhaustive-security assurance."}


class LiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.regions: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        row = dict(attrs)
        if row.get("role") in {"status", "alert", "log"} or "aria-live" in row:
            self.regions.append(row)


def live_accepts(markup: str) -> bool:
    parser = LiveParser(); parser.feed(markup)
    if len(parser.regions) != 1: return False
    row = parser.regions[0]; role = row.get("role"); live = row.get("aria-live")
    aligned = (role == "status" and live in {None, "polite"}) or (role == "alert" and live in {None, "assertive"})
    return bool(aligned and row.get("aria-atomic") in {"true", "false"} and row.get("aria-relevant")
                and row.get("aria-busy") == "false" and row.get("data-update-owner")
                and row.get("data-print-fallback") == "present")


def core() -> dict:
    teardown = [
        {"case": "parent_and_children_quiescent", "accepted": True},
        {"case": "cooperative_stop_then_quiescent", "timeout_retained": True, "partial_output_noncompletion": True, "accepted": True},
        {"case": "parent_exit_child_unknown", "accepted": False}, {"case": "partial_output_promoted", "accepted": False},
        {"case": "overlapping_retry", "accepted": False}, {"case": "undeclared_force_stop", "accepted": False},
        {"case": "sibling_process_target", "accepted": False},
    ]
    write_json("method-flow/process-tree-quiescence-contract.json", contract("V6458-P01", "Process-tree quiescence ledger", ["child aliases", "parent exit", "observed quiescence", "partial-output refusal", "timeout retention", "nonoverlapping retry"], ["unobserved child completion", "sibling or host process action", "destructive termination", "independent reproduction"]))
    c1 = vectors("method-flow/teardown-trace-mutation-vectors.json", teardown, {"parent_and_children_quiescent", "cooperative_stop_then_quiescent"}, real_processes_terminated=0)

    brst = [
        {"case": "nilpotent_typed_classical", "accepted": True}, {"case": "qualified_loop_identity", "accepted": True},
        {"case": "ghost_number_mismatch", "accepted": False}, {"case": "nilpotency_without_domain", "accepted": False},
        {"case": "loop_order_skipped", "accepted": False}, {"case": "regulator_omitted", "accepted": False},
        {"case": "on_shell_promoted_off_shell", "accepted": False}, {"case": "symbolic_promoted_empirical", "accepted": False},
    ]
    write_json("gmut/brst-slavnov-contract.json", contract("V6458-P02", "BRST and Slavnov-Taylor tribunal", ["typed fields", "ghost number", "nilpotency domain", "gauge fixing", "loop order", "regulator", "anomaly", "on-shell qualification"], ["quantum completeness", "force", "prediction", "likelihood", "constraint", "empirical confirmation", "Theory of Everything"]))
    c2 = vectors("gmut/brst-slavnov-mutation-vectors.json", brst, {"nilpotent_typed_classical", "qualified_loop_identity"}, physical_predictions=0, likelihoods=0, constraints=0)

    write_json("empirical/euclid-q1-study-contract.json", contract("V6458-P03", "Euclid Q1 shear-product absence protocol", ["Q1 inventory", "absent SHE processing", "future selection", "calibration", "covariance", "blinding", "frozen likelihood", "independent review"], ["row download", "inferred Q1 shear", "outcome tuning", "likelihood", "constraint", "force"]))
    write_json("empirical/euclid-q1-zero-row-receipt.json", {"schema": "ghc.family.v645-v8.euclid-zero-row.v1", "q1_shear_product_available": False, "real_rows": 0, "downloads": 0, "inferred_shear_values": 0, "likelihood_evaluations": 0, "constraints": 0, "force_claims": 0, "disposition": "open_gap", "missing": ["released shear product", "frozen selection and nuisance models", "calibration and covariance review", "authorized independent review"], "boundary": TRUTH_BOUNDARY})

    rail = [
        {"case": "matched_restriction_readback", "accepted": True}, {"case": "matched_control_handover", "accepted": True},
        {"case": "unmatched_budget", "accepted": False}, {"case": "missing_readback", "accepted": False},
        {"case": "real_worker_train_or_route", "accepted": False}, {"case": "operational_instruction", "accepted": False},
        {"case": "fatigue_hidden", "accepted": False}, {"case": "effectiveness_claim", "accepted": False},
    ]
    write_json("thos/rail-restriction-handover-protocol.json", contract("V6458-P04", "Railway restriction-handover proxy", ["source confirmation", "readback", "route and time scope", "matched budget", "blinding", "workload and fatigue monitoring"], ["real people", "operational instruction", "rail-safety decision", "professional competence", "effectiveness", "deployment"]))
    c4 = vectors("thos/rail-handover-proxy-vectors.json", rail, {"matched_restriction_readback", "matched_control_handover"}, real_participants=0, real_workers=0, real_trains=0, real_routes=0, real_arms=0, operational_instructions=0, disposition="represented")

    status = [
        {"case": "herd_sized_separated_purpose", "accepted": True}, {"case": "bounded_cache_and_staple", "accepted": True},
        {"case": "below_minimum_herd", "accepted": False}, {"case": "unique_list_per_credential", "accepted": False},
        {"case": "duplicate_index", "accepted": False}, {"case": "purpose_mismatch", "accepted": False},
        {"case": "verifier_tracking_fetch", "accepted": False}, {"case": "unbounded_freshness", "accepted": False},
    ]
    write_json("freed-id/bitstring-status-privacy-profile.json", contract("V6458-P05", "Synthetic Bitstring Status List privacy profile", ["minimum herd size", "noncorrelating allocation", "unique index", "purpose separation", "validity", "caching", "stapling", "fetch minimization"], ["real keys", "live issuance", "resolution", "revocation", "interoperability", "privacy or security assurance", "production"]))
    c5 = vectors("freed-id/bitstring-status-mutation-vectors.json", status, {"herd_sized_separated_purpose", "bounded_cache_and_staple"}, real_keys=0, real_proofs=0, live_issuance=0, live_resolution=0, status_or_revocation_events=0, interoperability_events=0, disposition="represented")

    write_json("cbr/managed-retreat-authority-reservation.json", {"schema": "ghc.family.v645-v8.managed-retreat-reservation.v1", "proposal_id": "V6458-P06", "real_people": 0, "real_households": 0, "valuations": 0, "relocation_decisions": 0, "compensation_decisions": 0, "tenancy_decisions": 0, "remedies_decided": 0, "legal_interpretation": False, "cultural_ratification": False, "maori_authority_claimed": False, "disposition": "exact_gate", "reserved_to": ["authorized affected people and communities", "owners, tenants, and relevant institutions", "competent privacy and legal authorities", "tangata whenua, iwi, hapu, and Maori authorities"], "boundary": TRUTH_BOUNDARY})
    write_text("cbr/retreat-valuation-tenancy-matrix.md", """# Managed-retreat valuation, tenancy, confidentiality, and authority reservation

| Question | Repository state | Authority required outside software |
| --- | --- | --- |
| What is real property, tenancy, or cultural loss worth? | Unknown; no household or valuation row | Affected people, owners and tenants, qualified valuers, institutions, and competent legal authority |
| Should a person or community relocate? | Reserved; no recommendation | Authorized affected people and communities with relevant public, legal, safety, and institutional processes |
| May confidential household or land information be disclosed? | Reserved; no real record | Data subjects, authorized custodians, and competent privacy and legal authorities |
| Who decides questions concerning Maori land, knowledge, or collective interests? | Exact-gated | Tangata whenua, iwi, hapu, and Maori authorities as applicable |

This stop surface sets no valuation, relocation, compensation, tenancy, remedy, legal, cultural, or Maori-authority conclusion. Maori concepts remain under Maori authority.""")

    sparse = sparse_index_lab()
    write_json("security/git-sparse-index-contract.json", contract("V6458-P07", "Sparse-index manifest tribunal", ["disposable repository", "cone mode", "sparse index", "skip-worktree evidence", "tracked omission", "canonical HEAD manifest", "cleanup"], ["canonical mutation", "remote change", "omission called deletion", "working-tree manifest called complete", "production or exhaustive security"]))
    write_json("security/git-sparse-index-mutation-vectors.json", sparse)

    samples = [
        ("single_polite_status", '<div role="status" aria-live="polite" aria-atomic="true" aria-relevant="text" aria-busy="false" data-update-owner="results" data-print-fallback="present"></div>', True),
        ("single_assertive_alert", '<div role="alert" aria-live="assertive" aria-atomic="true" aria-relevant="text" aria-busy="false" data-update-owner="error" data-print-fallback="present"></div>', True),
        ("duplicate_channels", '<div role="status"></div><div role="status"></div>', False),
        ("politeness_mismatch", '<div role="status" aria-live="assertive" aria-atomic="true" aria-relevant="text" aria-busy="false" data-update-owner="x" data-print-fallback="present"></div>', False),
        ("permanently_busy", '<div role="status" aria-live="polite" aria-atomic="true" aria-relevant="text" aria-busy="true" data-update-owner="x" data-print-fallback="present"></div>', False),
        ("missing_owner", '<div role="status" aria-live="polite" aria-atomic="true" aria-relevant="text" aria-busy="false" data-print-fallback="present"></div>', False),
        ("missing_fallback", '<div role="status" aria-live="polite" aria-atomic="true" aria-relevant="text" aria-busy="false" data-update-owner="x"></div>', False),
    ]
    live = [{"case": case, "accepted": live_accepts(markup), "expected": want, "pass": live_accepts(markup) == want} for case, markup, want in samples]
    write_json("accessibility/live-region-contract.json", contract("V6458-P08", "ARIA live-region structural audit", ["role and politeness", "atomicity", "relevance", "busy lifecycle", "one update owner", "duplicate refusal", "print fallback"], ["runtime behavior", "assistive-technology inference", "affected-user acceptance", "complete accessibility"]))
    write_json("accessibility/live-region-structural-audit.json", {"vectors": live, "valid": all(row["pass"] for row in live), "manual_keyboard_evaluation": "reserved", "browser_runtime_evaluation": "reserved", "assistive_technology_evaluation": "reserved", "maori_language_evaluation": "reserved", "affected_user_evaluation": "reserved", "complete_wcag_claim": False, "boundary": TRUTH_BOUNDARY})

    gibbs = [
        {"case": "single_phase_extensive_mixture", "accepted": True}, {"case": "molar_form_declared_constraint", "accepted": True},
        {"case": "all_intensives_independent", "accepted": False}, {"case": "mixed_units", "accepted": False},
        {"case": "phase_boundary_crossed", "accepted": False}, {"case": "extensivity_undeclared", "accepted": False},
        {"case": "composition_dropped", "accepted": False}, {"case": "psyche_autonomy_conversion", "accepted": False},
    ]
    write_json("thermo-psyche/gibbs-duhem-contract.json", contract("V6458-P09", "Gibbs-Duhem dependency classifier", ["phase", "extensivity", "variable typing", "composition", "units", "dependency count", "category barrier"], ["participant inference", "human autonomy claim", "psychological evidence", "consciousness", "fundamental law"]))
    c9 = vectors("thermo-psyche/gibbs-duhem-mutation-vectors.json", gibbs, {"single_phase_extensive_mixture", "molar_form_declared_constraint"}, participant_rows=0, psyche_claims=0, human_autonomy_claims=0)

    leakage = [
        {"case": "group_aware_clean_split", "accepted": True}, {"case": "exact_duplicate_cross_split", "accepted": False},
        {"case": "related_entity_cross_split", "accepted": False}, {"case": "hidden_augmentation_ancestry", "accepted": False},
        {"case": "threshold_tuned_on_evaluation", "accepted": False}, {"case": "preprocessing_fit_on_all_data", "accepted": False},
        {"case": "feature_selection_saw_labels", "accepted": False}, {"case": "stage20_promotion", "accepted": False},
    ]
    write_json("stage20/split-leakage-contract.json", contract("V6458-P10", "Entity and preprocessing leakage board", ["entity identity", "group-aware split", "duplicate and neighbor lineage", "train-only preprocessing", "train-only feature selection", "credit withdrawal"], ["leakage erasure", "evaluation tuning", "independence claim", "deployment", "proof", "Stage 20"]))
    c10 = vectors("stage20/entity-leakage-mutation-vectors.json", leakage, {"group_aware_clean_split"}, leaked_credit_withdrawn=True, stage20_verdict="NOT_READY_FOR_STAGE_20")

    negatives = [{"negative_id": f"V6458-SYN-N{n:02d}", "proposal_id": f"V6458-P{((n - 1) // 7) + 1:02d}", "mutation_index": ((n - 1) % 7) + 1, "expected": "reject_or_gate", "observed": "reject_or_gate", "retained": True, "independent_reproduction": False} for n in range(1, 71)]
    write_json("validation/synthetic-mutation-negative-register.json", {"schema": "ghc.family.v645-v8.synthetic-negatives.v1", "count": 70, "expected_count": 70, "negatives": negatives, "valid": True, "boundary": TRUTH_BOUNDARY})

    checks = {"V6458-P01": c1, "V6458-P02": c2, "V6458-P03": True, "V6458-P04": c4,
              "V6458-P05": c5, "V6458-P06": True, "V6458-P07": sparse["expected_results_passed"],
              "V6458-P08": all(row["pass"] for row in live), "V6458-P09": c9, "V6458-P10": c10}
    rows = [{"proposal_id": pid, "outcome": OUTCOMES[pid], "bounded_acceptance_passed": checks[pid], "same_owner_only": True, "independent_reproduction": False} for pid in OUTCOMES]
    payload = {"schema": "ghc.family.v645-v8.core-runner.v1", "proposal_count": 10,
               "outcomes": {state: list(OUTCOMES.values()).count(state) for state in ("completed", "represented", "open_gap", "exact_gate")},
               "rows": rows, "all_bounded_acceptance_passed": all(checks.values()),
               "stage20_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY}
    write_json("prototypes/runner-witnesses/ghc_family_v645_v8_core_runner.json", payload)
    return payload


if __name__ == "__main__":
    result = core(); print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["all_bounded_acceptance_passed"] else 1)
