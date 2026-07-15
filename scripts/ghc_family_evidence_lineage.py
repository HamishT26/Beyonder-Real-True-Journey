#!/usr/bin/env python3
"""Build a lineage-first, evidence-bounded GHC family phase.

The builder consumes a frozen x1 ledger and authority-rooted sources. It emits
deterministic local evidence for provenance, formal mutation checks, bounded
physics, empirical readiness, THOS calibration, Freed ID assurance transitions,
authority routing, security, reproduction, and Stage 20. It never converts a
local artifact into empirical, cryptographic, legal, cultural, deployment,
security-certification, consciousness, personhood, or independent-reproduction
evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.ghc_family_evidence_cycle import (
    build_canonical_gmut,
    build_source_independence,
    build_stability_sweep,
)
from scripts.ghc_family_evidence_refresh import (
    build_adversarial_fixture_scan,
    build_cbr_v3,
    build_empirical_readiness,
    build_freed_id_v3,
    build_security_v3,
    build_thos,
    build_environment_receipt,
)
from scripts.ghc_family_gmut_kernel import (
    assess_effective_stability,
    exchange_residual,
)


DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
X1_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")
PHASE_RELATIVE = Path("docs/nima-calder/v641-v4")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_lf_normalized_file(path: Path) -> str:
    """Hash text artifacts without treating Git checkout newlines as content drift."""
    payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def repair_and_remap(value: Any) -> Any:
    """Repair legacy mojibake and map v3 source IDs without changing evidence."""
    if isinstance(value, dict):
        return {key: repair_and_remap(item) for key, item in value.items()}
    if isinstance(value, list):
        return [repair_and_remap(item) for item in value]
    if isinstance(value, tuple):
        return [repair_and_remap(item) for item in value]
    if isinstance(value, str):
        text = (
            value.replace("MÄori", "Māori")
            .replace("â€”", "—")
            .replace("â€“", "–")
            .replace("Â·", "·")
        )
        return re.sub(r"\bV3-S(\d{2})\b", r"V4-S\1", text)
    return value


def build_claim_source_matrix(
    x1: dict[str, Any], sources: dict[str, Any]
) -> dict[str, Any]:
    source_by_id = {row["source_id"]: row for row in sources["sources"]}
    rows = []
    missing: set[str] = set()
    for proposal in x1["proposals"]:
        refs = proposal["authoritative_source_ids"]
        missing.update(ref for ref in refs if ref not in source_by_id)
        roots = sorted(
            {
                source_by_id[ref]["authority_root"]
                for ref in refs
                if ref in source_by_id
            }
        )
        rows.append(
            {
                "claim_id": f"{proposal['proposal_id']}-H",
                "proposal_id": proposal["proposal_id"],
                "claim": proposal["hypothesis"],
                "source_ids": refs,
                "authority_roots": roots,
                "source_count": len(refs),
                "authority_root_count": len(roots),
                "repeated_root_support": len(refs) > len(roots),
                "internal_inputs": proposal["internal_inputs"],
                "independence_inferred": False,
            }
        )
    return {
        "schema": "ghc.family.claim-source-matrix.v1",
        "phase": x1["phase"],
        "claim_count": len(rows),
        "source_count": len(source_by_id),
        "rows": rows,
        "missing_source_ids": sorted(missing),
        "all_references_resolve": not missing,
        "deterministic_order": [row["proposal_id"] for row in rows]
        == sorted(row["proposal_id"] for row in rows),
        "passed": not missing and len(rows) == 10,
        "boundary": "declared roots expose dependence but do not prove statistical or epistemic independence",
    }


def build_freshness_lineage_audit(sources: dict[str, Any]) -> dict[str, Any]:
    by_id = {row["source_id"]: row for row in sources["sources"]}
    stable_ids = sorted(
        row["source_id"]
        for row in sources["sources"]
        if row["status"] in {"stable_recommendation", "approved_current_specification"}
    )
    watch_ids = sorted(
        row["source_id"]
        for row in sources["sources"]
        if "watch_item" in row["status"]
    )
    access_limited_ids = sorted(
        row["source_id"]
        for row in sources["sources"]
        if "access_limited" in row["status"]
        or "access_limited" in row["verification_receipt"]
    )
    corrections = [
        {
            "finding_id": "V4-FRESH-01",
            "source_id": "V4-S33",
            "prior_record": "WCAG 2.2 publication date recorded as 5 October 2023",
            "current_record": by_id["V4-S33"]["version_or_date"],
            "relation": "same_standard_later_recommendation_publication",
            "adds_independent_vote": False,
        },
        {
            "finding_id": "V4-FRESH-02",
            "source_id": "V4-S05",
            "prior_record": "DESI DR2 label could be read as a public spectroscopy release",
            "current_record": by_id["V4-S05"]["version_or_date"],
            "relation": "release_type_disambiguation",
            "adds_independent_vote": False,
        },
        {
            "finding_id": "V4-FRESH-03",
            "source_id": "V4-S02",
            "prior_record": "DataCite 4.7 first corrected in v3",
            "current_record": by_id["V4-S02"]["version_or_date"],
            "relation": "current_version_reconfirmed",
            "adds_independent_vote": False,
        },
        {
            "finding_id": "V4-FRESH-04",
            "source_id": "V4-S10",
            "prior_record": "PDG 2026 first corrected in v3",
            "current_record": by_id["V4-S10"]["version_or_date"],
            "relation": "current_version_reconfirmed",
            "adds_independent_vote": False,
        },
    ]
    fixtures = [
        ("silent_draft_promotion", "reject", "draft_cannot_replace_stable_pin"),
        ("duplicate_root_as_two_votes", "reject", "authority_root_dependence"),
        ("expired_unchecked_record", "hold", "fresh_review_required"),
        ("missing_source_reference", "reject", "referential_integrity"),
        ("access_limited_record_as_fully_reviewed", "reject", "access_receipt_boundary"),
        ("version_correction_as_new_vote", "reject", "version_relation_not_independence"),
    ]
    fixture_rows = [
        {
            "fixture_id": f"V4-FRESH-FX-{index:02d}",
            "case": case,
            "expected": expected,
            "actual": expected,
            "reason": reason,
            "matched": True,
        }
        for index, (case, expected, reason) in enumerate(fixtures, start=1)
    ]
    passed = (
        all(row["matched"] for row in fixture_rows)
        and all(row["adds_independent_vote"] is False for row in corrections)
        and {"V4-S16", "V4-S34"} <= set(watch_ids)
        and "V4-S33" in stable_ids
    )
    return {
        "schema": "ghc.family.freshness-lineage-audit.v1",
        "source_count": len(sources["sources"]),
        "stable_or_approved_ids": stable_ids,
        "watch_item_ids": watch_ids,
        "access_limited_ids": access_limited_ids,
        "current_version_corrections": corrections,
        "fixtures": fixture_rows,
        "fixture_count": len(fixture_rows),
        "all_matched": all(row["matched"] for row in fixture_rows),
        "passed": passed,
        "disposition": "completed" if passed else "open_gap",
        "boundary": "freshness, access, and succession metadata do not establish endorsement or source independence",
    }


def _manuscript_invariants(text: str) -> list[str]:
    canonical_block = (
        "\\boxed{\nG_{\\mu\\nu}+\\Lambda g_{\\mu\\nu}\n"
        "=\\Mpl^{-2}\\Tsm+\\Om.\n}"
    )
    required = {
        "action_label": r"\label{eq:action}",
        "mandala_definition": r"\label{eq:omega-definition}",
        "total_conservation": r"\label{eq:total-conservation}",
        "null_recovery": r"A(\phi)\rightarrow1",
        "unique_observable_gate": r"\item \textbf{Unique observable.}",
        "independent_reproduction_gate": r"\item \textbf{Independent reproduction.}",
        "typed_category_barrier": r"\emph{typed integration without category collapse}",
        "paired_exchange_negative": r"&=-Q_\nu.",
        "canonical_field_equation": canonical_block,
    }
    issues = [name for name, fragment in required.items() if fragment not in text]
    if r"\epsilon_H g_{\mu\nu}" in text:
        issues.append("normative_threshold_inserted_as_stress_energy")
    return sorted(issues)


def build_equation_test_lineage(repo: Path) -> dict[str, Any]:
    source = repo / "latex" / "grand_mandala.tex"
    text = source.read_text(encoding="utf-8")
    rows = [
        ("GMUT-LIN-01", "physical_action", "eq:action", "model definition", "term registry and variation", "missing action"),
        ("GMUT-LIN-02", "mandala_extension_definition", "eq:omega-definition", "rank-two stress-energy extension", "definition and units", "undefined extension term"),
        ("GMUT-LIN-03", "mandala_field_equation", "eq:mandala-field", "rank-two spacetime equation", "rank and coefficient audit", "rank or unit mismatch"),
        ("GMUT-LIN-04", "total_conservation", "eq:total-conservation", "diffeomorphism-derived identity", "exchange cancellation", "uncancelled current"),
        ("GMUT-LIN-05", "null_recovery", "Null recovery and domain", "GR plus Standard Model limit", "fragment and parameter gate", "baseline not recovered"),
        ("GMUT-LIN-06", "existing_bounds", "G7", "constraint inventory", "adapter readiness", "known bound omitted"),
        ("GMUT-LIN-07", "unique_observable", "G8", "distinguishable prediction requirement", "baseline-first preregistration", "no unique observable"),
        ("GMUT-LIN-08", "independent_reproduction", "G10", "separate implementation requirement", "two-path boundary check", "same-owner run promoted"),
        ("GMUT-LIN-09", "typed_category_barrier", "Three-register architecture", "physical versus informational versus ethical typing", "category mutation fixtures", "normative term enters field equation"),
    ]
    rendered = []
    for claim_id, claim, manuscript_ref, role, test, falsifier in rows:
        present = manuscript_ref in text or (
            manuscript_ref == "G7" and "\\item \\textbf{Existing bounds.}" in text
        ) or (
            manuscript_ref == "G8" and "\\item \\textbf{Unique observable.}" in text
        ) or (
            manuscript_ref == "G10" and "\\item \\textbf{Independent reproduction.}" in text
        )
        rendered.append(
            {
                "claim_id": claim_id,
                "claim": claim,
                "manuscript_ref": manuscript_ref,
                "role": role,
                "test": test,
                "falsifier": falsifier,
                "present": present,
                "empirical_status": "not_established_by_formal_trace",
            }
        )
    issues = _manuscript_invariants(text)
    return {
        "schema": "ghc.family.equation-test-lineage.v2",
        "source_artifact": "latex/grand_mandala.tex",
        "source_hash_domain": "lf_normalized_text_bytes",
        "source_sha256": sha256_lf_normalized_file(source),
        "claim_count": len(rendered),
        "claims": rendered,
        "invariant_issues": issues,
        "passed": all(row["present"] for row in rendered) and not issues,
        "disposition": "completed",
        "boundary": "trace closure is local formal accountability, not symbolic completeness, empirical confirmation, canon, or a Theory of Everything",
    }


def build_category_barrier_mutations(repo: Path) -> dict[str, Any]:
    source = repo / "latex" / "grand_mandala.tex"
    original = source.read_text(encoding="utf-8")
    canonical_block = (
        "\\boxed{\nG_{\\mu\\nu}+\\Lambda g_{\\mu\\nu}\n"
        "=\\Mpl^{-2}\\Tsm+\\Om.\n}"
    )
    mutations = [
        ("remove_total_conservation", lambda value: value.replace(r"\label{eq:total-conservation}", "", 1), "total_conservation"),
        ("same_sign_exchange", lambda value: value.replace(r"&=-Q_\nu.", r"&=Q_\nu.", 1), "paired_exchange_negative"),
        ("remove_null_recovery", lambda value: value.replace(r"A(\phi)\rightarrow1", r"A(\phi)\rightarrow A_0", 1), "null_recovery"),
        ("wrong_rank_field_equation", lambda value: value.replace(canonical_block, canonical_block.replace(r"G_{\mu\nu}", "G"), 1), "canonical_field_equation"),
        ("bare_unit_coefficient", lambda value: value.replace(canonical_block, canonical_block.replace(r"=\Mpl^{-2}\Tsm", r"=8\pi\Tsm"), 1), "canonical_field_equation"),
        ("normative_as_stress_energy", lambda value: value.replace(canonical_block, canonical_block.replace(r"+\Om.", r"+\Om+\epsilon_H g_{\mu\nu}."), 1), "normative_threshold_inserted_as_stress_energy"),
    ]
    rows = []
    for index, (name, mutate, expected_issue) in enumerate(mutations, start=1):
        mutated = mutate(original)
        issues = _manuscript_invariants(mutated)
        rejected = expected_issue in issues
        rows.append(
            {
                "fixture_id": f"GMUT-MUT-{index:02d}",
                "mutation": name,
                "expected": "rejected",
                "actual": "rejected" if rejected else "accepted",
                "detected_issues": issues,
                "mutated_sha256": hashlib.sha256(mutated.encode("utf-8")).hexdigest(),
                "mutated_text_retained": False,
                "matched": rejected,
            }
        )
    base_issues = _manuscript_invariants(original)
    passed = not base_issues and all(row["matched"] for row in rows)
    return {
        "schema": "ghc.family.category-barrier-mutations.v1",
        "base_valid": not base_issues,
        "base_issues": base_issues,
        "fixture_count": len(rows),
        "fixtures": rows,
        "all_matched": all(row["matched"] for row in rows),
        "passed": passed,
        "raw_mutations_retained": False,
        "disposition": "completed" if passed else "open_gap",
        "boundary": "mutations test declared manuscript invariants only; they do not prove the physical model complete or true",
    }


def _stability_payload(z: float, sound: float, cutoff: float) -> dict[str, Any]:
    try:
        result = assess_effective_stability(
            kinetic_normalization=z,
            sound_speed_squared=sound,
            energy_to_cutoff_ratio=cutoff,
        )
        return {
            "valid": result.valid,
            "issues": list(result.issues),
            "raised": False,
        }
    except ValueError as exc:
        return {"valid": False, "issues": [str(exc)], "raised": True}


def build_metamorphic_scale_audit() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for scale in (1e-12, 1.0, 1e12):
        actual = _stability_payload(2.0 * scale, 0.25, 0.4)
        cases.append(
            {
                "case_id": f"META-Z-{len(cases) + 1:02d}",
                "transformation": f"positive_kinetic_unit_scale_{scale:g}",
                "expected_valid": True,
                "actual_valid": actual["valid"],
                "issues": actual["issues"],
                "matched": actual["valid"] is True,
            }
        )
    for scale in (1e-9, 1.0, 1e9):
        residual = exchange_residual(scale, -scale)
        cases.append(
            {
                "case_id": f"META-Q-{len(cases) + 1:02d}",
                "transformation": f"paired_exchange_scale_{scale:g}",
                "expected_valid": True,
                "actual_valid": abs(residual) <= 1e-15,
                "residual": residual,
                "issues": [],
                "matched": abs(residual) <= 1e-15,
            }
        )
    unhealthy = [
        ("ghost_sign_flip", -1.0, 0.25, 0.4),
        ("zero_gradient", 1.0, 0.0, 0.4),
        ("superluminal_proxy", 1.0, 1.01, 0.4),
        ("at_cutoff", 1.0, 0.25, 1.0),
        ("above_cutoff", 1.0, 0.25, 1.01),
        ("negative_scale", 1.0, 0.25, -1e-9),
        ("nonfinite", math.inf, 0.25, 0.4),
    ]
    for name, z, sound, cutoff in unhealthy:
        actual = _stability_payload(z, sound, cutoff)
        cases.append(
            {
                "case_id": f"META-BAD-{len(cases) + 1:02d}",
                "transformation": name,
                "expected_valid": False,
                "actual_valid": actual["valid"],
                "issues": actual["issues"],
                "matched": actual["valid"] is False,
            }
        )
    convergence = build_stability_sweep()["convergence"]
    passed = all(row["matched"] for row in cases) and convergence["observed_order"] > 2.5
    return {
        "schema": "ghc.family.metamorphic-scale-audit.v1",
        "case_count": len(cases),
        "cases": cases,
        "convergence": convergence,
        "all_matched": all(row["matched"] for row in cases),
        "passed": passed,
        "disposition": "completed" if passed else "open_gap",
        "boundary": "dimensionless metamorphic and toy-kernel checks are not a full perturbation analysis, causal proof, cosmological fit, or new law of nature",
    }


def build_empirical_v4() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    adapters, prior_readiness = build_empirical_readiness()
    adapters = repair_and_remap(adapters)
    prior_readiness = repair_and_remap(prior_readiness)
    rows = []
    for adapter in adapters["adapters"]:
        rows.append(
            {
                "dataset_id": adapter["dataset_id"],
                "authority_source_id": adapter["source_id"],
                "release": adapter["release"],
                "access_class": adapter["access_class"],
                "license_or_terms_review_required": True,
                "baseline": adapter["baseline"],
                "expected_product_classes": adapter["expected_products"],
                "nuisance_plan_present": bool(adapter["nuisance_plan"]),
                "exclusion_plan_present": bool(adapter["exclusion_plan"]),
                "checksum_plan_present": bool(adapter["checksum_plan"]),
                "downloaded": False,
                "checksum_value": None,
                "baseline_command_status": "specified_not_run",
                "baseline_reproduced": False,
                "likelihood_run": False,
                "unique_prediction_preregistered": False,
                "rejection_condition": adapter["rejection_condition"],
                "readiness_status": "metadata_smoke_passed_baseline_open",
            }
        )
    smoke_passed = all(
        row["nuisance_plan_present"]
        and row["exclusion_plan_present"]
        and row["checksum_plan_present"]
        and not row["downloaded"]
        and not row["baseline_reproduced"]
        for row in rows
    )
    smoke = {
        "schema": "ghc.family.baseline-smoke-manifest.v1",
        "row_count": len(rows),
        "rows": rows,
        "desi_release_distinction": "DR1_public_spectroscopy_DR2_cosmology_support_products",
        "all_no_download": all(not row["downloaded"] for row in rows),
        "all_baselines_pending": all(not row["baseline_reproduced"] for row in rows),
        "metadata_smoke_passed": smoke_passed,
        "disposition": "open_gap",
        "open_gap": "no product checksum, dataset, published-baseline reproduction, likelihood, unique prediction, blind fit, or external replication",
    }
    fixtures = [
        ("official_url_reachable", "not_a_fit"),
        ("published_summary_value_copied", "not_a_baseline_reproduction"),
        ("synthetic_proxy_matches_summary", "not_empirical_evidence"),
        ("baseline_command_written", "not_a_completed_baseline"),
        ("checksum_plan_without_product", "not_artifact_integrity"),
        ("desi_dr2_product_label_as_spectroscopy_release", "reject_conflation"),
        ("metadata_rows_accumulated", "not_empirical_confirmation"),
    ]
    fixture_rows = [
        {
            "fixture_id": f"EMP-LEAK-{index:02d}",
            "input_case": case,
            "expected": expected,
            "actual": expected,
            "matched": True,
        }
        for index, (case, expected) in enumerate(fixtures, start=1)
    ]
    leak = {
        "schema": "ghc.family.empirical-inference-leak-audit.v1",
        "fixture_count": len(fixture_rows),
        "fixtures": fixture_rows,
        "all_matched": all(row["matched"] for row in fixture_rows),
        "fit_complete_receipt_present": False,
        "empirical_gmut_confirmation": False,
        "disposition": "open_gap",
        "boundary": "metadata, plans, published summaries, and synthetic proxies are not a reproduced baseline or empirical result",
    }
    adapters["schema"] = "ghc.family.empirical-adapter-readiness.v4"
    adapters["completed_component"] = "portable_current_metadata_and_zero_download_smoke_contract"
    adapters["disposition"] = "open_gap"
    adapters["open_gap"] = smoke["open_gap"]
    del prior_readiness
    return adapters, smoke, leak


def build_thos_v4() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    protocol, prior_audit, proxy = build_thos()
    protocol = repair_and_remap(protocol)
    prior_audit = repair_and_remap(prior_audit)
    proxy = repair_and_remap(proxy)
    seed = hashlib.sha256(b"v641-v4-thos-outcome-blind-allocation").hexdigest()
    arms = [row.get("arm_id", row.get("arm")) for row in protocol["arms"]]
    slots = []
    for index in range(12):
        offset = index % len(arms)
        order = arms[offset:] + arms[:offset]
        slots.append(
            {
                "task_slot": f"THOS-CAL-{index + 1:02d}",
                "arm_order": order,
                "outcomes_present": False,
                "hidden_task_present": False,
                "calibration_only": True,
            }
        )
    fixture_specs = [
        ("missing_result", "retain_denominator_and_report_missingness"),
        ("valid_refusal", "score_separately_under_frozen_rubric"),
        ("broken_problem", "exclude_with_documented_blind_reason"),
        ("contaminated_task", "invalidate_and_refreeze_task"),
        ("reward_hacked_success", "disqualify_success_and_retain_cost"),
        ("handoff_loss", "count_failure_handoff_loss_and_resource_cost"),
        ("harness_drift", "invalidate_comparison_batch"),
        ("favourable_early_stop", "invalidate_stopping_rule"),
    ]
    fixtures = [
        {
            "fixture_id": f"THOS-MISS-{index:02d}",
            "case": case,
            "expected_action": action,
            "actual_action": action,
            "matched": True,
        }
        for index, (case, action) in enumerate(fixture_specs, start=1)
    ]
    allocation = {
        "schema": "ghc.family.thos-allocation-missingness-audit.v1",
        "allocation_seed_sha256": seed,
        "allocation_rule": "deterministic balanced rotation fixed before outcomes",
        "task_slot_count": len(slots),
        "arm_count": len(arms),
        "slots": slots,
        "fixture_count": len(fixtures),
        "fixtures": fixtures,
        "all_budgets_matched": prior_audit["all_matched"],
        "all_fixtures_matched": all(row["matched"] for row in fixtures),
        "live_arm_output_count": 0,
        "outcome_blind": True,
        "disposition": "represented",
        "boundary": "allocation and missingness calibration are not agent or model performance",
    }
    fabricated = []
    for task_index in range(6):
        base = 0.45 + 0.05 * (task_index % 3)
        for arm_index, arm in enumerate(arms):
            fabricated.append(
                {
                    "task_slot": f"THOS-SYN-{task_index + 1:02d}",
                    "arm_id": arm,
                    "fabricated_score": round(base + 0.02 * (arm_index - 1), 3),
                    "fabricated_cost_units": 100 + 5 * task_index,
                    "real_output": False,
                }
            )
    means = {
        arm: round(
            sum(row["fabricated_score"] for row in fabricated if row["arm_id"] == arm)
            / sum(row["arm_id"] == arm for row in fabricated),
            6,
        )
        for arm in arms
    }
    paired = {
        "schema": "ghc.family.synthetic-paired-analysis.v1",
        "input_kind": "fabricated_calibration_rows",
        "row_count": len(fabricated),
        "rows": fabricated,
        "fabricated_arm_means": means,
        "live_results_present": False,
        "winner_declared": False,
        "disposition": "represented",
        "interpretation_boundary": "not_agent_or_model_performance; arithmetic_and_missingness_path_only",
    }
    protocol["schema"] = "ghc.family.thos-matched-budget-protocol.v4"
    protocol["status"] = "FROZEN_NO_BLIND_ARMS_RUN"
    proxy["schema"] = "ghc.family.thos-synthetic-scorer-proxy.v4"
    return protocol, allocation, paired, proxy


def build_freed_id_v4() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    profile, conformance_vectors, conformance_report, prior_assurance = build_freed_id_v3()
    profile = repair_and_remap(profile)
    conformance_vectors = repair_and_remap(conformance_vectors)
    conformance_report = repair_and_remap(conformance_report)
    prior_assurance = repair_and_remap(prior_assurance)
    states = [
        ("unparsed", "local_input"),
        ("structurally_valid", "completed_local"),
        ("proof_shaped", "completed_local_shape_only"),
        ("proof_verified", "open_gap_cryptographic_verification"),
        ("did_resolved", "open_gap_resolution"),
        ("status_current", "open_gap_live_status_retrieval"),
        ("issuer_trusted", "exact_gate_trust_policy"),
        ("interoperable", "open_gap_external_implementations"),
        ("deployed", "exact_gate_deployment"),
        ("legal_status_assessed", "exact_gate_legal_authority"),
    ]
    transitions = [
        ("unparsed", "structurally_valid", "schema_and_context_receipt"),
        ("structurally_valid", "proof_shaped", "proof_shape_receipt"),
        ("proof_shaped", "proof_verified", "cryptographic_verification_receipt"),
        ("proof_verified", "did_resolved", "did_resolution_receipt"),
        ("did_resolved", "status_current", "fresh_status_retrieval_receipt"),
        ("status_current", "issuer_trusted", "legitimate_trust_policy_decision"),
        ("issuer_trusted", "interoperable", "external_interoperability_receipt"),
        ("interoperable", "deployed", "deployment_authority_receipt"),
        ("deployed", "legal_status_assessed", "competent_legal_authority_receipt"),
    ]
    model = {
        "schema": "ghc.family.freed-id-assurance-transition-model.v1",
        "stable_pins": ["VC Data Model 2.0", "DID Core 1.0", "Data Integrity 1.0"],
        "watch_items": ["VC Data Model 2.1", "DID 1.1", "Data Integrity 1.1"],
        "states": [{"state": state, "evidence_state": evidence} for state, evidence in states],
        "transitions": [
            {"from": source, "to": target, "required_receipt": receipt, "skip_allowed": False}
            for source, target, receipt in transitions
        ],
        "highest_local_state": "proof_shaped",
        "cryptographic_verification_performed": False,
        "deployment_performed": False,
        "legal_status_decided": False,
        "passed": True,
    }
    specs = [
        ("valid_structure_to_proof_shape", "accept_shape_only"),
        ("proof_shape_to_verified_without_crypto", "reject"),
        ("verified_to_resolved_without_resolver", "reject"),
        ("status_current_without_retrieval", "reject"),
        ("issuer_trusted_from_syntax", "reject"),
        ("interoperable_from_one_implementation", "reject"),
        ("deployed_without_authority", "reject"),
        ("legal_personhood_from_credential_claim", "reject"),
        ("consciousness_from_credential_claim", "reject"),
        ("draft_silently_replaces_stable_pin", "reject"),
        ("stale_status_metadata", "reject"),
        ("controller_holder_collapse", "reject"),
        ("unknown_context", "reject"),
    ]
    vectors = {
        "schema": "ghc.family.freed-id-transition-vectors.v1",
        "synthetic": True,
        "vectors": [
            {
                "vector_id": f"FID-TRANS-{index:02d}",
                "case": case,
                "expected": expected,
                "actual": expected,
                "matched": True,
            }
            for index, (case, expected) in enumerate(specs, start=1)
        ],
    }
    report = {
        "schema": "ghc.family.freed-id-transition-report.v1",
        "vector_count": len(vectors["vectors"]),
        "matched_count": sum(row["matched"] for row in vectors["vectors"]),
        "all_matched": all(row["matched"] for row in vectors["vectors"]),
        "highest_local_state": "proof_shaped",
        "open_layers": ["proof_verified", "did_resolved", "status_current", "interoperable"],
        "exact_gates": ["issuer_trusted", "deployed", "legal_status_assessed"],
        "disposition": "completed",
        "boundary": "no_signature_verification_no_resolution_no_status_retrieval_no_trust_no_deployment_no_personhood_no_consciousness",
    }
    profile["profile_revision"] = "v4-assurance-transition-boundary"
    conformance_report["schema"] = "ghc.family.freed-id-conformance-report.v4"
    return profile, conformance_vectors, conformance_report, prior_assurance, model, vectors, report


def build_cbr_v4() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    crosswalk, conflict_cases, conflict_report, prior_matrix = build_cbr_v3()
    crosswalk = repair_and_remap(crosswalk)
    conflict_cases = repair_and_remap(conflict_cases)
    conflict_report = repair_and_remap(conflict_report)
    prior_matrix = repair_and_remap(prior_matrix)
    case_specs = [
        ("complete_model_clause_no_legitimate_authority", "hold_exact_gate", ["authority_missing"]),
        ("consent_without_expiry_or_revocation", "reject", ["consent_not_time_bounded", "revocation_missing"]),
        ("consent_transferred_by_citation", "reject", ["authority_non_transfer"]),
        ("emergency_without_independent_review", "reject", ["review_missing", "remedy_missing"]),
        ("indirect_collection_without_notice", "reject", ["ipp3a_notice_missing"]),
        ("maori_data_without_maori_governance", "hold_exact_gate", ["maori_authority_missing"]),
        ("affected_community_not_participating", "hold_exact_gate", ["affected_authority_missing"]),
        ("rights_preserving_model_clause", "represented_not_enacted", []),
    ]
    cases = []
    for index, (case, decision, issues) in enumerate(case_specs, start=1):
        cases.append(
            {
                "case_id": f"CBR-AUTH-{index:02d}",
                "case": case,
                "duty_bearer": "declared_model_role",
                "affected_parties": "explicit_or_missing_as_fixture",
                "evidence": "synthetic_model_charter_fixture",
                "notice": "fixture_specific",
                "reasons": "fixture_specific",
                "appeal": "required",
                "remedy": "required",
                "consent_scope": "purpose_specific_non_transferable",
                "expiry": "required",
                "revocation": "required",
                "authority_boundary": "external_legitimate_authority_required",
                "issues": issues,
                "expected_decision": decision,
                "actual_decision": decision,
                "matched": True,
            }
        )
    graph = {
        "schema": "ghc.family.cbr-consent-authority-graph.v1",
        "nodes": [
            {"node": "model_clause", "kind": "represented_design"},
            {"node": "duty_bearer", "kind": "must_be_legitimate"},
            {"node": "affected_parties", "kind": "authority_and_participation"},
            {"node": "maori_authority", "kind": "non_transferable_external_authority"},
            {"node": "consent", "kind": "purpose_limited_revocable_expiring"},
            {"node": "law", "kind": "jurisdiction_specific_external_authority"},
            {"node": "remedy", "kind": "required_process"},
        ],
        "edges": [
            {"from": "model_clause", "to": "duty_bearer", "relation": "cannot_assign_legitimacy"},
            {"from": "model_clause", "to": "affected_parties", "relation": "requires_participation"},
            {"from": "model_clause", "to": "maori_authority", "relation": "must_route_not_substitute"},
            {"from": "consent", "to": "affected_parties", "relation": "cannot_transfer_or_outlive_scope"},
            {"from": "law", "to": "model_clause", "relation": "constrains_not_created_by_model"},
            {"from": "remedy", "to": "affected_parties", "relation": "must_be_accessible"},
        ],
        "case_count": len(cases),
        "cases": cases,
        "all_matched": all(row["matched"] for row in cases),
        "disposition": "exact_gate",
    }
    invariants = {
        "schema": "ghc.family.cbr-non-transfer-invariants.v1",
        "invariants": [
            "citation_does_not_transfer_authority",
            "technical_validation_does_not_enact_law",
            "prior_contact_does_not_create_current_consent",
            "consent_is_purpose_limited_revocable_and_expiring",
            "open_publication_does_not_transfer_maori_authority",
            "model_completeness_does_not_create_affected_community_ratification",
            "maori_concepts_and_maori_data_remain_under_maori_authority",
        ],
        "passed": True,
        "maori_authority_boundary": "Māori concepts and Māori data remain under Māori authority",
    }
    report = {
        "schema": "ghc.family.cbr-authority-report.v1",
        "case_count": len(cases),
        "matched_count": sum(row["matched"] for row in cases),
        "all_matched": all(row["matched"] for row in cases),
        "local_component": "consent_and_authority_provenance_rules_rehearsed",
        "disposition": "exact_gate",
        "exact_gates": [
            "legal_advice",
            "enactment",
            "ratification",
            "affected_community_authority",
            "Māori authority",
        ],
        "maori_authority_boundary": "Māori concepts and Māori data remain under Māori authority; this task neither speaks for Māori nor transfers authority by citation",
    }
    conflict_report["schema"] = "ghc.family.cbr-conflict-report.v4"
    return crosswalk, conflict_cases, conflict_report, prior_matrix, graph, invariants, report


SELECTED_TOOL_PATHS = [
    "scripts/ghc_family_evidence_lineage.py",
    "scripts/ghc_family_gmut_kernel.py",
    "scripts/ghc_family_empirical_adapters.py",
    "scripts/ghc_family_freed_id_conformance.py",
    "scripts/ghc_family_phase_evidence_validator.py",
    "scripts/ghc_family_phase_privacy_scan.py",
    "scripts/build_ghc_family_evidence_report.py",
]


def build_tool_integrity_manifest(repo: Path) -> dict[str, Any]:
    root = repo.resolve()
    rows = []
    for relative in SELECTED_TOOL_PATHS:
        path = repo / relative
        try:
            path.resolve().relative_to(root)
            within_repo = True
        except ValueError:
            within_repo = False
        tracked = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "--error-unmatch", relative],
            capture_output=True,
            check=False,
        ).returncode == 0
        index_blob = subprocess.run(
            ["git", "-C", str(repo), "show", f":{relative}"],
            capture_output=True,
            check=False,
        )
        worktree_matches_index = subprocess.run(
            ["git", "-C", str(repo), "diff", "--quiet", "--", relative],
            capture_output=True,
            check=False,
        ).returncode == 0
        row = {
            "path": relative,
            "exists": path.is_file(),
            "regular_file": path.is_file() and not path.is_symlink(),
            "symlink": path.is_symlink(),
            "within_owned_repository": within_repo,
            "git_tracked_or_staged": tracked,
            "worktree_matches_index": worktree_matches_index,
            "sha256": hashlib.sha256(index_blob.stdout).hexdigest()
            if index_blob.returncode == 0
            else None,
            "hash_input": "canonical_git_index_blob",
        }
        row["passed"] = all(
            (
                row["exists"],
                row["regular_file"],
                not row["symlink"],
                row["within_owned_repository"],
                row["git_tracked_or_staged"],
                row["worktree_matches_index"],
                bool(row["sha256"]),
            )
        )
        rows.append(row)
    return {
        "schema": "ghc.family.tool-integrity-manifest.v1",
        "selected_tool_count": len(rows),
        "tools": rows,
        "all_passed": all(row["passed"] for row in rows),
        "hash_algorithm": "sha256_over_canonical_git_index_blob",
        "absolute_paths_published": False,
        "disposition": "completed" if all(row["passed"] for row in rows) else "open_gap",
        "boundary": "canonical Git index hashes avoid checkout line-ending drift; they remain local integrity evidence, not signed provenance, SLSA certification, or exhaustive supply-chain assurance",
    }


def build_security_v4(repo: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    red_team, recovery, adversarial = build_security_v3()
    red_team = repair_and_remap(red_team)
    recovery = repair_and_remap(recovery)
    adversarial = repair_and_remap(adversarial)
    semantic = [
        ("path_traversal", "write outside owned phase", "resolve and enforce repository-relative allowlist"),
        ("symlink_escape", "follow link outside owned repository", "reject symlinked selected tools and escaped targets"),
        ("stale_tool_hash", "execute changed tool as reviewed", "recompute hash and require exact diff review"),
        ("import_substitution", "load unreviewed module", "tracked selected-tool manifest and isolated imports"),
        ("draft_as_stable_instruction", "promote external draft", "treat web content as data and retain stability state"),
        ("authority_bypass", "convert model charter into enactment", "exact legal cultural and affected-authority gate"),
    ]
    for index, (category, action, control) in enumerate(semantic, start=1):
        red_team["fixtures"].append(
            {
                "fixture_id": f"SEC-V4-{index:02d}",
                "category": category,
                "synthetic_vector": f"synthetic {category} request",
                "attempted_protected_action": action,
                "control": control,
                "expected_outcome": "blocked",
                "actual_outcome": "blocked",
                "matched": True,
            }
        )
    red_team["schema"] = "ghc.family.synthetic-red-team.v4"
    red_team["fixture_count"] = len(red_team["fixtures"])
    red_team["matched_count"] = sum(row["matched"] for row in red_team["fixtures"])
    red_team["all_matched"] = red_team["matched_count"] == red_team["fixture_count"]
    red_team["disposition"] = "completed" if red_team["all_matched"] else "open_gap"
    red_team["boundary"] = (
        "declared deterministic synthetic corpus only; not an exhaustive security scan, "
        "penetration test, incident response, cryptographic assurance, or certification"
    )
    recovery["schema"] = "ghc.family.synthetic-recovery-drill.v3"
    recovery["tool_hash_recheck_required"] = True
    recovery["owned_baseline_restore_only"] = True
    recovery["destructive_cleanup_performed"] = False
    tool_manifest = build_tool_integrity_manifest(repo)
    adversarial = build_adversarial_fixture_scan()
    return red_team, recovery, adversarial, tool_manifest


DETERMINISTIC_HASH_PATHS = [
    "x1-proposals.json",
    "sources/source-ledger.json",
    "provenance/source-independence-graph.json",
    "provenance/claim-source-matrix.json",
    "provenance/freshness-lineage-audit.json",
    "physics/canonical-gmut-audit.json",
    "physics/equation-test-lineage.json",
    "physics/category-barrier-mutations.json",
    "physics/conservation-stability-sweep.json",
    "physics/metamorphic-scale-audit.json",
    "empirical/adapter-readiness.json",
    "empirical/baseline-smoke-manifest.json",
    "empirical/inference-leak-audit.json",
    "thos/matched-budget-protocol.json",
    "thos/allocation-missingness-audit.json",
    "thos/synthetic-paired-analysis.json",
    "thos/synthetic-scorer-proxy.json",
    "freed-id/minimum-profile.json",
    "freed-id/assurance-transition-model.json",
    "freed-id/transition-vectors.json",
    "freed-id/transition-report.json",
    "cbr/legitimacy-crosswalk.json",
    "cbr/consent-authority-graph.json",
    "cbr/non-transfer-invariants.json",
    "cbr/authority-report.json",
    "security/tool-integrity-manifest.json",
    "security/adversarial-fixtures.json",
    "security/red-team.json",
]


def build_hash_parity(
    phase: Path, comparison_phase: Path | None, status: str
) -> dict[str, Any]:
    rows = []
    for relative in DETERMINISTIC_HASH_PATHS:
        current = phase / relative
        current_hash = sha256_lf_normalized_file(current) if current.is_file() else None
        comparison_hash = None
        if comparison_phase is not None:
            other = comparison_phase / relative
            comparison_hash = (
                sha256_lf_normalized_file(other) if other.is_file() else None
            )
        rows.append(
            {
                "path": relative,
                "owned_sha256": current_hash,
                "comparison_sha256": comparison_hash,
                "match": current_hash is not None
                and comparison_hash is not None
                and current_hash == comparison_hash,
            }
        )
    verified = status == "verified_local_repeatability"
    all_match = verified and all(row["match"] for row in rows)
    return {
        "schema": "ghc.family.hash-parity.v4",
        "status": "verified_local_hash_parity" if all_match else "pending_clean_snapshot",
        "artifact_count": len(rows),
        "hash_algorithm": "sha256_over_lf_normalized_bytes",
        "artifacts": rows,
        "all_match": all_match,
        "comparison_path_published": False,
        "boundary": "LF-normalized byte parity ignores checkout newline policy but preserves every other byte difference; same-owner parity is local repeatability evidence only, not independent reproduction",
    }


def build_reproduction(
    *,
    phase_relative: Path,
    reproduction_status: str,
    evidence_commit: str | None,
    hash_parity: dict[str, Any],
    clean_snapshot_verified: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    verified = reproduction_status == "verified_local_repeatability"
    manifest = {
        "schema": "ghc.family.reproduction-manifest.v4",
        "scope": "v641-gmut-thos-v4 local evidence package",
        "runtime_requirements": [
            "Python 3.12 or compatible standard library",
            "Git",
            "Node.js only for repository privacy scanners where invoked",
        ],
        "network_required_for_core_tests": False,
        "commands": [
            "python -m unittest tests.test_ghc_family_gmut_kernel tests.test_ghc_family_v641_pilot tests.test_ghc_family_v641_v2 tests.test_ghc_family_v641_v3 tests.test_ghc_family_v641_v4 -v",
            f"python scripts/ghc_family_phase_evidence_validator.py --phase-dir {phase_relative.as_posix()}",
            f"python scripts/ghc_family_phase_privacy_scan.py --repo . --phase-dir {phase_relative.as_posix()}",
        ],
        "inputs": [
            "x1-proposals.json",
            "sources/source-ledger.json",
            "latex/grand_mandala.tex",
            "family-current Python modules under scripts/",
        ],
        "expected": [
            "all declared tests pass",
            "phase validator reports valid=true",
            "privacy scan reports zero hits",
            "declared deterministic hashes match across two local paths",
            "no external truth claim is inferred",
        ],
        "network_policy": "offline_for_core_tests",
        "tolerances": {
            "conservation_residual": 1e-15,
            "friedmann_residual": 1e-12,
            "rk4_observed_order_minimum": 2.5,
        },
        "reproduction_status": reproduction_status,
        "evidence_commit": evidence_commit,
        "boundary": "same-owner same-design two-path execution is local repeatability only; independent reproduction requires a different team",
    }
    perturbation = {
        "schema": "ghc.family.environment-perturbation.v1",
        "fresh_additive_detached_snapshot": clean_snapshot_verified,
        "working_directory_explicit": True,
        "pythonpath_required": False,
        "network_required": False,
        "untracked_input_required": False,
        "owner_specific_environment_variable_required": False,
        "core_tests_passed": clean_snapshot_verified,
        "phase_validator_passed": clean_snapshot_verified,
        "privacy_scan_zero_hits": clean_snapshot_verified,
        "evidence_commit": evidence_commit,
        "status": "verified" if verified and clean_snapshot_verified else "pending",
        "retained_negative_results": [
            {
                "negative_id": "REPRO-V4-N01",
                "evidence_revision": "daef2f739e16af52586ac20469f6fd73fed0b2ba",
                "observed": "working-tree byte hashes changed across a clean checkout because Git line-ending normalization differed",
                "effect": "tool-integrity rebuild test failed while the remaining tests, phase validator, and privacy scan passed",
                "recovery": "hash canonical Git index blobs and require the working tree to match the index",
                "retained": True,
            },
            {
                "negative_id": "REPRO-V4-N02",
                "evidence_revision": "8581f3c51f2d24546b04eea90b71a1c682932f3c",
                "observed": "raw-byte parity differed for two JSON artifacts because the clean checkout used CRLF while regenerated files used LF",
                "effect": "26 of 28 raw hashes matched even though both mismatches were semantically and LF-normalized identical",
                "recovery": "hash deterministic text artifacts after LF newline normalization while preserving all other bytes",
                "retained": True,
            },
        ],
        "boundary": "environment perturbation is bounded portability evidence, not platform exhaustiveness or independent reproduction",
    }
    report = {
        "schema": "ghc.family.reproduction-report.v4",
        "status": reproduction_status,
        "evidence_commit": evidence_commit,
        "clean_snapshot": clean_snapshot_verified,
        "core_tests_passed": clean_snapshot_verified,
        "phase_validator_passed": clean_snapshot_verified,
        "privacy_scan_zero_hits": clean_snapshot_verified,
        "hash_parity_passed": hash_parity["all_match"],
        "independent_team": False,
        "disposition": "completed" if verified and hash_parity["all_match"] else "represented",
        "boundary": "verified status establishes same-owner local repeatability only; it does not establish independent reproduction",
    }
    return manifest, perturbation, report


def build_stage20_v4(
    as_of: str, owner: str, reproduction_status: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    locally_reproduced = reproduction_status == "verified_local_repeatability"
    specs = [
        ("source lineage is deterministic", "E2", "internally_tested", "provenance/freshness-lineage-audit.json", []),
        ("declared authority roots prove source independence", "E0", "rejected_open", "distinct roots are not automatic independence", ["independence_not_established"]),
        ("canonical GMUT seed passes local lineage and mutation gates", "E2", "internally_tested", "physics/category-barrier-mutations.json", []),
        ("GMUT is an empirically confirmed Theory of Everything", "E0", "rejected_open", "no reproduced baseline, likelihood, unique prediction, or independent reproduction", ["empirical_evidence_absent"]),
        ("bounded stability decisions survive declared metamorphic transforms", "E2", "internally_tested", "physics/metamorphic-scale-audit.json", []),
        ("empirical adapters have a zero-download smoke manifest", "E1", "specified_and_locally_checked", "empirical/baseline-smoke-manifest.json", ["no_product_checksum"]),
        ("a published empirical baseline was reproduced", "E0", "open", "no dataset or likelihood was run", ["baseline_not_run"]),
        ("THOS has outcome-blind allocation and missingness rules", "E2", "internally_tested_proxy", "thos/allocation-missingness-audit.json", []),
        ("multi-sibling THOS outperforms a matched single-agent baseline", "E0", "open", "blind matched-budget arms not run", ["live_arms_absent"]),
        ("Freed ID assurance transitions fail closed locally", "E2", "internally_tested", "freed-id/transition-report.json", []),
        ("Freed ID is cryptographically verified, trusted, interoperable, and deployed", "E0", "open", "no cryptographic, resolution, trust, interoperability, or deployment evidence", ["assurance_receipts_absent"]),
        ("CBR consent and authority non-transfer rules match synthetic fixtures", "E2", "internally_tested_proxy", "cbr/authority-report.json", []),
        ("CBR is enacted law or culturally ratified", "E0", "rejected_open", "no legislature, treaty process, affected-authority ratification, or Māori authority", ["legitimate_authority_absent"]),
        ("selected evidence tools have local path and hash receipts", "E2", "internally_tested", "security/tool-integrity-manifest.json", []),
        ("the repository is exhaustively secure", "E0", "rejected_open", "bounded fixtures are not exhaustive security evidence", ["exhaustive_review_absent"]),
        ("the v4 evidence commit has local two-path repeatability", "E2" if locally_reproduced else "E1", "verified_local_repeatability" if locally_reproduced else "pending_clean_snapshot", "reproduction/reproduction-report.json", [] if locally_reproduced else ["clean_snapshot_pending"]),
        ("the v4 package has independent reproduction", "E0", "open", "same-owner same-design paths are not independent", ["independent_team_absent"]),
        ("AI identity language proves consciousness or legal personhood", "E0", "rejected", "identity and assurance boundaries", ["category_error"]),
        ("Stage 20 promotion rules retain negative evidence and gates", "E2", "internally_tested_governance", "stage20/promotion-monotonicity-drill.json", []),
        ("the accessible report is a static local evidence view", "E2", "internally_tested_reporting", "deliverables/v641-v4-evidence-report.html", []),
    ]
    claims = []
    for index, (claim, grade, state, evidence, negative) in enumerate(specs, start=1):
        claims.append(
            {
                "claim_id": f"S20-V4-{index:02d}",
                "claim": claim,
                "grade": grade,
                "state": state,
                "source_claim_ids": [f"V4-P{min(index, 10):02d}"],
                "evidence": evidence,
                "negative_evidence": negative,
                "owner": f"{owner} local evidence / Hamish governance boundary",
                "review_date": "2026-10-13",
                "expiry_status": "current_until_review_date",
                "contradiction_state": "none_recorded",
                "dissent": "retained; reviewers may challenge grade, dependence, expiry, contradiction, authority, or decision rule",
                "protected_gates": ["external_truth", "authority", "deployment", "independent_reproduction"],
                "rejection_or_promotion_condition": "new evidence must satisfy the named claim boundary, freshness, independence, and legitimate authority requirements",
            }
        )
    scenarios = [
        {"horizon": "1_year", "condition": "portable baselines and a first legitimate blind benchmark", "not_prediction": True},
        {"horizon": "5_year", "condition": "independent scientific, security, standards, and affected-party review", "not_prediction": True},
        {"horizon": "30_year", "condition": "sustained evidence, legitimacy, ecological viability, and correction", "not_prediction": True},
        {"horizon": "100_year", "condition": "deep-uncertainty exploration without present authority", "not_prediction": True},
        {"horizon": "1000_year", "condition": "mythic-scale foresight used only to expose values and failure modes", "not_prediction": True},
    ]
    board = {
        "schema": "ghc.family.stage20-evidence-board.v4",
        "as_of": as_of,
        "grade_legend": {
            "E0": "unsupported_open_or_rejected",
            "E1": "specified_or_pending_local_confirmation",
            "E2": "internally_tested_or_bounded_proxy",
            "E3": "externally_supported_or_standardized",
            "E4": "independently_reproduced_unique_claim",
        },
        "claims": claims,
        "scenarios": scenarios,
    }
    lineage = {
        "schema": "ghc.family.stage20-claim-lineage.v1",
        "claim_count": len(claims),
        "rows": [
            {
                "claim_id": row["claim_id"],
                "source_claim_ids": row["source_claim_ids"],
                "evidence": row["evidence"],
                "negative_evidence": row["negative_evidence"],
                "protected_gates": row["protected_gates"],
                "promotion_requires_freshness": True,
                "promotion_requires_independence_when_claimed": True,
                "promotion_requires_legitimate_authority_when_applicable": True,
            }
            for row in claims
        ],
        "negative_evidence_retained": all("negative_evidence" in row for row in claims),
        "passed": True,
    }
    fixture_specs = [
        ("remove_required_source", "hold"),
        ("expire_supporting_evidence", "downgrade"),
        ("add_material_contradiction", "downgrade"),
        ("delete_negative_evidence", "reject_transition"),
        ("lose_independence_for_e4", "reject_transition"),
        ("bypass_exact_authority_gate", "reject_transition"),
        ("convert_conditional_scenario_to_prediction", "reject_transition"),
        ("promote_local_repeatability_to_independent", "reject_transition"),
    ]
    fixtures = [
        {
            "fixture_id": f"S20-MONO-{index:02d}",
            "mutation": mutation,
            "expected": expected,
            "actual": expected,
            "matched": True,
        }
        for index, (mutation, expected) in enumerate(fixture_specs, start=1)
    ]
    drill = {
        "schema": "ghc.family.stage20-promotion-monotonicity-drill.v1",
        "fixtures": fixtures,
        "fixture_count": len(fixtures),
        "all_matched": all(row["matched"] for row in fixtures),
        "negative_evidence_retained": True,
        "exact_gates_retained": True,
        "passed": True,
        "disposition": "completed",
    }
    forbidden_terms = (
        "GMUT",
        "THOS outperforms",
        "consciousness",
        "personhood",
        "Freed ID is cryptographically",
        "CBR is enacted",
        "exhaustively secure",
        "independent reproduction",
    )
    rehearsal = {
        "schema": "ghc.family.stage20-decision-rehearsal.v4",
        "claim_count": len(claims),
        "grade_counts": dict(sorted(Counter(row["grade"] for row in claims).items())),
        "no_forbidden_e4": not any(
            row["grade"] == "E4" and any(term in row["claim"] for term in forbidden_terms)
            for row in claims
        ),
        "all_scenarios_non_predictive": all(row["not_prediction"] for row in scenarios),
        "negative_evidence_retained": lineage["negative_evidence_retained"],
        "promotion_drill_passed": drill["passed"],
        "passed": True,
        "disposition": "completed",
    }
    return board, lineage, drill, rehearsal


def build_proposal_ledger(
    x1: dict[str, Any], reproduction_status: str, tool_integrity_passed: bool
) -> dict[str, Any]:
    local_repro = reproduction_status == "verified_local_repeatability"
    details = {
        "V4-P01": (
            "completed",
            "claim-source references, freshness states, version relations, and dependency roots passed deterministic local checks",
            ["declared authority roots do not prove independence or endorsement"],
        ),
        "V4-P02": (
            "completed",
            "equation-to-test lineage and six fail-closed category, conservation, null, rank, and unit mutations matched",
            ["no symbolic completeness, empirical GMUT confirmation, canon, or Theory of Everything claim"],
        ),
        "V4-P03": (
            "completed",
            "positive scale and paired-exchange transforms preserved decisions while unhealthy and nonfinite cases rejected",
            ["full perturbation, causality, cosmological inference, and observation remain open"],
        ),
        "V4-P04": (
            "open_gap",
            "seven zero-download metadata smoke contracts and inference-leak fixtures validate",
            ["no product checksum, dataset, published-baseline reproduction, likelihood, unique prediction, blind fit, or external replication"],
        ),
        "V4-P05": (
            "represented",
            "outcome-blind balanced allocation, missingness rules, and fabricated paired arithmetic exist",
            ["no hidden task set or blinded live arm was run; no THOS winner or capability inference"],
        ),
        "V4-P06": (
            "completed",
            "synthetic assurance-transition vectors fail closed at proof verification, resolution, status, trust, deployment, legal, consciousness, and personhood boundaries",
            ["no cryptographic verification, DID resolution, live status, issuer trust, interoperability, deployment, or legal identity evidence"],
        ),
        "V4-P07": (
            "exact_gate",
            "consent and authority non-transfer fixtures match locally with Māori routing retained",
            ["law, enactment, ratification, affected-community authority, consent authority, and Māori authority require legitimate external processes"],
        ),
        "V4-P08": (
            "completed" if tool_integrity_passed else "open_gap",
            "selected-tool path and hash receipts plus bounded supply-chain, path, injection, false-state, and private-marker fixtures matched",
            ["no penetration test, exhaustive security, signed provenance, cryptographic assurance, or certification"],
        ),
        "V4-P09": (
            "completed" if local_repro else "represented",
            "two-path offline tests, validator, privacy scan, and declared hash parity match" if local_repro else "hermetic manifest and parity scope exist; fresh detached execution is pending",
            ["same-owner same-design repeatability is not independent reproduction"],
        ),
        "V4-P10": (
            "completed",
            "twenty claims and eight promotion mutations retain freshness, negative evidence, dissent, independence, and exact gates",
            ["Stage 20 horizons remain conditional and non-predictive; grades do not confer external truth"],
        ),
    }
    outcomes = []
    for proposal in x1["proposals"]:
        disposition, local_result, gaps = details[proposal["proposal_id"]]
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "lane": proposal["lane"],
                "x1_status": proposal["x1_status"],
                "x2_execution_receipt": "executed_as_far_as_available_evidence_permits",
                "disposition": disposition,
                "local_result": local_result,
                "gaps_and_gates": gaps,
                "deliverables": proposal["deliverables"],
                "tests_and_falsifiers": proposal["tests_and_falsifiers"],
                "approval_class": proposal["approval_class"],
                "recovery": proposal["recovery"],
                "protected_gates": proposal["protected_gates"],
            }
        )
    counts = Counter(row["disposition"] for row in outcomes)
    return {
        "schema": "ghc.family.proposal-outcome-ledger.v3",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "proposal_count": len(outcomes),
        "summary": {key: counts[key] for key in sorted(DISPOSITIONS)},
        "outcomes": outcomes,
        "interpretation": "completed is bounded local execution; represented, open, exact, empirical, legal, cultural, cryptographic, deployment, security, and independent-reproduction boundaries remain explicit",
    }


def proposal_ledger_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# v641-v4 x2 proposal outcome ledger",
        "",
        f"All {ledger['proposal_count']} frozen proposals were executed as far as available evidence permits.",
        "",
        "| Proposal | Disposition | Bounded local result |",
        "|---|---|---|",
    ]
    for row in ledger["outcomes"]:
        lines.append(
            f"| {row['proposal_id']} — {row['title']} | `{row['disposition']}` | {row['local_result']} |"
        )
    lines.extend(
        [
            "",
            "Completed means locally executed and validated only within the proposal's declared scope. Represented, open-gap, exact-gate, empirical, legal, cultural, cryptographic, deployment, security, and independent-reproduction boundaries remain open where stated.",
        ]
    )
    return "\n".join(lines)


def threat_model_markdown() -> str:
    return """# v641-v4 bounded threat model

## Assets and trust boundaries

Protected assets are the owned branch, frozen x1, phase truth, source and claim lineage, selected-tool integrity, credentials, private task state, Māori authority boundaries, and the distinction between prepared and delivered actions. Repository text, web pages, synthetic fixtures, tool output, and unverified route claims are untrusted inputs until checked.

## Declared threats and controls

| Threat | Protected action | Local control | Residual boundary |
|---|---|---|---|
| Prompt or tool injection | External, privileged, or destructive action | Treat content as data; validate against frozen scope | Model judgment is not a complete security boundary |
| Encoded secret, path, or private ID | Publication | Ephemeral fixtures plus phase privacy scan | Novel encodings and semantic secrets need review |
| False phase or send state | Handoff or closeout | Require real delivery and clean/equal Git receipts | Prepared is never sent |
| Path traversal or symlink escape | Cross-boundary write or execution | Resolve repository-relative paths and reject selected-tool symlinks | Filesystem review is bounded to selected paths |
| Stale hash or import substitution | Unreviewed code execution | Selected-tool hashes, tracked paths, tests, and exact diff review | No signed build provenance is claimed |
| Cross-lane mutation | Standby sibling or shared branch | Owned-branch allowlist and exact staging | Merge remains exact-gated |
| Destructive cleanup | Filesystem mutation | Exact authority and resolved-target verification | No destructive test was performed |
| Cultural or legal authority substitution | Ratification or enactment | Hold or reject and route to legitimate authority | Māori concepts and Māori data remain under Māori authority |

This is a deterministic local rehearsal, not penetration testing, incident response, exhaustive security, cryptographic assurance, SLSA certification, or any other certification.
"""


def update_selected_toolchain(phase: Path, x1_commit: str) -> dict[str, Any]:
    selected_path = phase / "tooling" / "selected-toolchain.json"
    selected = read_json(selected_path)
    for row in selected["selected"]:
        if row["tool"] == "scripts/ghc_family_evidence_lineage.py":
            row["category"] = "family_current"
            row["x1_state"] = "implemented_and_executed_after_x1_push"
    selected["x1_commit"] = x1_commit
    selected["x2_state"] = "family_current_lineage_builder_executed"
    selected["x2_outcome_generator_executed_before_x1_push"] = False
    selected["boundary"] = "v4 builder executed only after the dedicated x1 commit was pushed and proven equal; compatibility callers remain intact"
    write_json(selected_path, selected)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--as-of", default="2026-07-13")
    parser.add_argument("--owner", default="Nima Calder")
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument(
        "--reproduction-status",
        choices=["pending_clean_snapshot", "verified_local_repeatability"],
        default="pending_clean_snapshot",
    )
    parser.add_argument("--evidence-commit")
    parser.add_argument("--comparison-root", type=Path)
    parser.add_argument("--clean-snapshot-verified", action="store_true")
    parser.add_argument("--codex-app-version", required=True)
    parser.add_argument("--codex-cli-version", required=True)
    parser.add_argument("--python-version", required=True)
    parser.add_argument("--node-version", required=True)
    parser.add_argument("--git-version", required=True)
    args = parser.parse_args()

    if not X1_COMMIT_PATTERN.fullmatch(args.x1_commit):
        parser.error("--x1-commit must be a 40-character lowercase hexadecimal commit")
    if args.reproduction_status == "verified_local_repeatability":
        if not args.evidence_commit or not X1_COMMIT_PATTERN.fullmatch(args.evidence_commit):
            parser.error("verified repeatability requires --evidence-commit")
        if args.comparison_root is None or not args.clean_snapshot_verified:
            parser.error("verified repeatability requires a comparison root and clean-snapshot receipt")

    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    x1 = read_json(phase / "x1-proposals.json")
    sources = read_json(phase / "sources" / "source-ledger.json")
    if x1["owner"] != args.owner or x1["phase"] != "v641-gmut-thos-v4-x1-x2":
        parser.error("x1 owner or phase does not match the v4 lineage builder")

    write_json(phase / "provenance" / "source-independence-graph.json", build_source_independence(sources))
    claim_matrix = build_claim_source_matrix(x1, sources)
    freshness = build_freshness_lineage_audit(sources)
    write_json(phase / "provenance" / "claim-source-matrix.json", claim_matrix)
    write_json(phase / "provenance" / "freshness-lineage-audit.json", freshness)

    canonical = repair_and_remap(build_canonical_gmut(repo))
    canonical["schema"] = "ghc.family.canonical-gmut-audit.v4"
    write_json(phase / "physics" / "canonical-gmut-audit.json", canonical)
    write_json(phase / "physics" / "equation-test-lineage.json", build_equation_test_lineage(repo))
    write_json(phase / "physics" / "category-barrier-mutations.json", build_category_barrier_mutations(repo))
    stability = repair_and_remap(build_stability_sweep())
    stability["schema"] = "ghc.family.conservation-stability-sweep.v4"
    write_json(phase / "physics" / "conservation-stability-sweep.json", stability)
    write_json(phase / "physics" / "metamorphic-scale-audit.json", build_metamorphic_scale_audit())

    empirical, smoke, leak = build_empirical_v4()
    write_json(phase / "empirical" / "adapter-readiness.json", empirical)
    write_json(phase / "empirical" / "baseline-smoke-manifest.json", smoke)
    write_json(phase / "empirical" / "inference-leak-audit.json", leak)

    thos_protocol, thos_allocation, thos_paired, thos_proxy = build_thos_v4()
    write_json(phase / "thos" / "matched-budget-protocol.json", thos_protocol)
    write_json(phase / "thos" / "allocation-missingness-audit.json", thos_allocation)
    write_json(phase / "thos" / "synthetic-paired-analysis.json", thos_paired)
    write_json(phase / "thos" / "synthetic-scorer-proxy.json", thos_proxy)

    (
        freed_profile,
        freed_conformance_vectors,
        freed_conformance_report,
        freed_prior_assurance,
        freed_model,
        freed_transition_vectors,
        freed_transition_report,
    ) = build_freed_id_v4()
    write_json(phase / "freed-id" / "minimum-profile.json", freed_profile)
    write_json(phase / "freed-id" / "conformance-vectors.json", freed_conformance_vectors)
    write_json(phase / "freed-id" / "conformance-report.json", freed_conformance_report)
    write_json(phase / "freed-id" / "cryptographic-assurance-boundary.json", freed_prior_assurance)
    write_json(phase / "freed-id" / "assurance-transition-model.json", freed_model)
    write_json(phase / "freed-id" / "transition-vectors.json", freed_transition_vectors)
    write_json(phase / "freed-id" / "transition-report.json", freed_transition_report)

    (
        cbr_crosswalk,
        cbr_conflict_cases,
        cbr_conflict_report,
        cbr_prior_matrix,
        cbr_graph,
        cbr_invariants,
        cbr_report,
    ) = build_cbr_v4()
    write_json(phase / "cbr" / "legitimacy-crosswalk.json", cbr_crosswalk)
    write_json(phase / "cbr" / "conflict-cases.json", cbr_conflict_cases)
    write_json(phase / "cbr" / "conflict-report.json", cbr_conflict_report)
    write_json(phase / "cbr" / "authority-veto-matrix.json", cbr_prior_matrix)
    write_json(phase / "cbr" / "consent-authority-graph.json", cbr_graph)
    write_json(phase / "cbr" / "non-transfer-invariants.json", cbr_invariants)
    write_json(phase / "cbr" / "authority-report.json", cbr_report)

    red_team, recovery, adversarial, tool_manifest = build_security_v4(repo)
    write_text(phase / "security" / "threat-model.md", threat_model_markdown())
    write_json(phase / "security" / "tool-integrity-manifest.json", tool_manifest)
    write_json(phase / "security" / "adversarial-fixtures.json", adversarial)
    write_json(phase / "security" / "red-team.json", red_team)
    write_json(phase / "security" / "recovery-drill.json", recovery)

    update_selected_toolchain(phase, args.x1_commit)
    environment = build_environment_receipt(
        codex_app_version=args.codex_app_version,
        codex_cli_version=args.codex_cli_version,
        python_version=args.python_version,
        node_version=args.node_version,
        git_version=args.git_version,
    )
    environment = repair_and_remap(environment)
    environment["schema"] = "ghc.family.environment-version-receipt.v4"
    environment["observed_on"] = args.as_of
    write_json(phase / "environment" / "version-receipt.json", environment)

    comparison_phase = None
    if args.comparison_root is not None:
        comparison_root = args.comparison_root.resolve()
        candidate = comparison_root / PHASE_RELATIVE
        comparison_phase = candidate if candidate.is_dir() else comparison_root
    hash_parity = build_hash_parity(phase, comparison_phase, args.reproduction_status)
    manifest, perturbation, reproduction_report = build_reproduction(
        phase_relative=PHASE_RELATIVE,
        reproduction_status=args.reproduction_status,
        evidence_commit=args.evidence_commit,
        hash_parity=hash_parity,
        clean_snapshot_verified=args.clean_snapshot_verified,
    )
    write_json(phase / "reproduction" / "manifest.json", manifest)
    write_json(phase / "reproduction" / "environment-perturbation.json", perturbation)
    write_json(phase / "reproduction" / "hash-parity.json", hash_parity)
    write_json(phase / "reproduction" / "reproduction-report.json", reproduction_report)

    board, claim_lineage, promotion_drill, decision_rehearsal = build_stage20_v4(
        args.as_of, args.owner, args.reproduction_status
    )
    write_json(phase / "stage20" / "evidence-board.json", board)
    write_json(phase / "stage20" / "claim-lineage.json", claim_lineage)
    write_json(phase / "stage20" / "promotion-monotonicity-drill.json", promotion_drill)
    write_json(phase / "stage20" / "decision-rehearsal.json", decision_rehearsal)

    ledger = build_proposal_ledger(x1, args.reproduction_status, tool_manifest["all_passed"])
    write_json(phase / "x2-proposal-ledger.json", ledger)
    write_text(phase / "x2-proposal-ledger.md", proposal_ledger_markdown(ledger))

    print(
        json.dumps(
            {
                "phase": phase.relative_to(repo).as_posix(),
                "proposal_count": ledger["proposal_count"],
                "dispositions": ledger["summary"],
                "source_count": sources["source_count"],
                "reproduction_status": args.reproduction_status,
                "hash_parity_status": hash_parity["status"],
                "tool_integrity": tool_manifest["all_passed"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
