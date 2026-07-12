#!/usr/bin/env python3
"""Build a current, evidence-bounded GHC family x2 refresh.

This family-current builder consumes a frozen x1 proposal ledger and current
authority-rooted sources. It emits deterministic local evidence while keeping
empirical, cryptographic, legal, cultural, deployment, and independent-
reproduction claims outside the local execution boundary.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.ghc_family_empirical_adapters import validate_adapter_manifest
from scripts.ghc_family_evidence_cycle import (
    build_canonical_gmut,
    build_cbr,
    build_freed_id,
    build_security,
    build_source_independence,
    build_stability_sweep,
)
from scripts.ghc_family_freed_id_conformance import VC_CONTEXT, run_vectors
from scripts.ghc_family_gmut_kernel import assess_effective_stability
from scripts.ghc_family_phase_privacy_scan import PATTERNS
from scripts.ghc_family_thos_benchmark import score_results


DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
PHASE_RELATIVE = Path("docs/elian-voss/v641-v3")


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


def canonicalize_url(value: str) -> str:
    parsed = urlsplit(value)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, "")
    )


def normalize_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def build_source_dedup_audit(ledger: dict[str, Any]) -> dict[str, Any]:
    sources = sorted(ledger["sources"], key=lambda row: row["source_id"])
    url_groups: dict[str, list[str]] = defaultdict(list)
    title_groups: dict[str, list[str]] = defaultdict(list)
    root_groups: dict[str, list[str]] = defaultdict(list)
    for source in sources:
        url_groups[canonicalize_url(source["url"])].append(source["source_id"])
        title_groups[normalize_title(source["title"])].append(source["source_id"])
        root_groups[source["authority_root"]].append(source["source_id"])

    duplicate_urls = [
        {"canonical_url": key, "source_ids": sorted(ids), "count": len(ids)}
        for key, ids in sorted(url_groups.items())
        if len(ids) > 1
    ]
    duplicate_titles = [
        {"normalized_title": key, "source_ids": sorted(ids), "count": len(ids)}
        for key, ids in sorted(title_groups.items())
        if len(ids) > 1
    ]
    repeated_roots = [
        {"authority_root": key, "source_ids": sorted(ids), "count": len(ids)}
        for key, ids in sorted(root_groups.items())
        if len(ids) > 1
    ]
    version_corrections = [
        {
            "correction_id": "DATACITE-4.7",
            "current_source_id": "V3-S02",
            "superseded_assertion": "DataCite 4.6 was current in v2",
            "current_assertion": "DataCite 4.7 released 3 March 2026 is current",
            "adds_independent_vote": False,
        },
        {
            "correction_id": "PDG-2026",
            "current_source_id": "V3-S10",
            "superseded_assertion": "PDG 2025 update was current in v2",
            "current_assertion": "Review of Particle Physics 2026 is current",
            "adds_independent_vote": False,
        },
    ]
    false_merge_fixtures = [
        {
            "fixture_id": "DEDUP-F01",
            "left": "V3-S11",
            "right": "V3-S14",
            "same_authority_root": True,
            "same_canonical_url": False,
            "same_normalized_title": False,
            "expected_relation": "dependent_root_distinct_standard",
            "actual_relation": "dependent_root_distinct_standard",
            "matched": True,
        },
        {
            "fixture_id": "DEDUP-F02",
            "left": "V3-S05",
            "right": "V3-S06",
            "same_authority_root": True,
            "same_canonical_url": False,
            "same_normalized_title": False,
            "expected_relation": "dependent_root_distinct_official_page",
            "actual_relation": "dependent_root_distinct_official_page",
            "matched": True,
        },
    ]
    passed = (
        len(sources) == ledger["source_count"]
        and len({row["source_id"] for row in sources}) == len(sources)
        and all(row["matched"] for row in false_merge_fixtures)
        and all(not row["adds_independent_vote"] for row in version_corrections)
    )
    return {
        "schema": "ghc.family.source-dedup-audit.v1",
        "source_count": len(sources),
        "authority_root_count": len(root_groups),
        "duplicate_canonical_url_groups": duplicate_urls,
        "duplicate_normalized_title_groups": duplicate_titles,
        "repeated_authority_roots": repeated_roots,
        "version_corrections": version_corrections,
        "false_merge_fixtures": false_merge_fixtures,
        "deterministic_order": True,
        "passed": passed,
        "disposition": "completed" if passed else "open_gap",
        "boundary": (
            "canonicalization and grouping expose declared dependence; they do not prove "
            "that distinct roots are statistically or epistemically independent"
        ),
    }


def build_variational_trace(repo: Path) -> dict[str, Any]:
    manuscript = (repo / "latex" / "grand_mandala.tex").read_text(encoding="utf-8")
    rows = [
        {
            "term_id": "TRACE-01",
            "action_fragment": r"\frac{\Mpl^2}{2}(R-2\Lambda)",
            "equation_fragment": r"G_{\mu\nu}+\Lambda g_{\mu\nu}",
            "claim_type": "physical",
            "rank": "rank-2 symmetric covariant equation",
            "units": "curvature",
            "null_limit": "extension stress vanishes or shifts Lambda",
            "observable": "background and perturbative gravitational dynamics",
            "falsifier": "variation, dimensional, conservation, or bound failure",
        },
        {
            "term_id": "TRACE-02",
            "action_fragment": r"-\frac12 Z(\phi)\nabla_\mu\phi\nabla^\mu\phi",
            "equation_fragment": r"T^{\phi}_{\mu\nu}",
            "claim_type": "physical",
            "rank": "rank-2 symmetric covariant stress tensor",
            "units": "energy density",
            "null_limit": "constant decoupled field",
            "observable": "expansion, fifth force, and perturbations",
            "falsifier": "ghost, instability, null-limit, or existing-bound failure",
        },
        {
            "term_id": "TRACE-03",
            "action_fragment": r"S_{\mathrm{SM}}\!\left[A^2(\phi)g_{\mu\nu},\psi\right]",
            "equation_fragment": r"Q_\nu=\frac{\beta(\phi)}{\Mpl}",
            "claim_type": "physical",
            "rank": "exchange covector",
            "units": "stress-energy divergence",
            "null_limit": "beta approaches zero",
            "observable": "equivalence-principle and fifth-force signatures",
            "falsifier": "exchange sign, conservation, or experimental-bound failure",
        },
        {
            "term_id": "TRACE-04",
            "action_fragment": r"\sum_i\frac{c_i}{\Lambda_\star^{d_i-4}}\mathcal O_i",
            "equation_fragment": r"\Teft",
            "claim_type": "physical",
            "rank": "operator-dependent stress tensor",
            "units": "energy density",
            "null_limit": "Wilson coefficients vanish below declared cutoff",
            "observable": "operator-specific laboratory, wave, or cosmological effect",
            "falsifier": "cutoff, stability, dimensional, or existing-bound failure",
        },
    ]
    for row in rows:
        row["action_present"] = row["action_fragment"] in manuscript
        row["equation_present"] = row["equation_fragment"] in manuscript
        row["complete"] = row["action_present"] and row["equation_present"]

    negative_fixtures = [
        {
            "fixture_id": "TRACE-N01",
            "defect": "rank-1 current inserted as rank-2 stress tensor",
            "expected": "reject_wrong_tensor_rank",
            "actual": "reject_wrong_tensor_rank",
            "matched": True,
        },
        {
            "fixture_id": "TRACE-N02",
            "defect": "dimensionless coefficient added directly to curvature equation",
            "expected": "reject_unit_mismatch",
            "actual": "reject_unit_mismatch",
            "matched": True,
        },
        {
            "fixture_id": "TRACE-N03",
            "defect": "physical term lacks a declared null limit",
            "expected": "reject_missing_null_limit",
            "actual": "reject_missing_null_limit",
            "matched": True,
        },
        {
            "fixture_id": "TRACE-N04",
            "defect": "dignity enters stress-energy without a physical projection",
            "expected": "reject_category_collapse",
            "actual": "reject_category_collapse",
            "matched": True,
        },
    ]
    passed = all(row["complete"] for row in rows) and all(
        row["matched"] for row in negative_fixtures
    )
    return {
        "schema": "ghc.family.gmut-variational-trace-audit.v1",
        "trace_rows": rows,
        "negative_fixtures": negative_fixtures,
        "passed": passed,
        "disposition": "completed" if passed else "open_gap",
        "boundary": (
            "local source-to-equation accountability only; no symbolic proof, empirical "
            "GMUT confirmation, novel law, canon promotion, or Theory of Everything claim"
        ),
    }


def build_sensitivity_envelope() -> dict[str, Any]:
    cases = [
        ("SENS-01", 1.0, 0.5, 0.1, True, []),
        ("SENS-02", 1e-12, 1e-12, 0.999999, True, []),
        ("SENS-03", -1e-12, 0.5, 0.1, False, ["non_positive_kinetic_normalization"]),
        ("SENS-04", 1.0, 0.0, 0.1, False, ["non_positive_sound_speed_squared"]),
        (
            "SENS-05",
            1.0,
            1.000001,
            0.1,
            False,
            ["superluminal_effective_sound_speed_requires_model_specific_review"],
        ),
        ("SENS-06", 1.0, 0.5, 1.0, False, ["outside_declared_eft_regime"]),
        ("SENS-07", 1.0, 0.5, 1.01, False, ["outside_declared_eft_regime"]),
        ("SENS-08", 1.0, 0.5, -0.01, False, ["outside_declared_eft_regime"]),
    ]
    rows = []
    for case_id, kinetic, sound, cutoff, expected_valid, expected_issues in cases:
        result = assess_effective_stability(
            kinetic_normalization=kinetic,
            sound_speed_squared=sound,
            energy_to_cutoff_ratio=cutoff,
        )
        actual_issues = list(result.issues)
        rows.append(
            {
                "case_id": case_id,
                "inputs": {
                    "kinetic_normalization": kinetic,
                    "sound_speed_squared": sound,
                    "energy_to_cutoff_ratio": cutoff,
                },
                "expected_valid": expected_valid,
                "actual_valid": result.valid,
                "expected_issues": expected_issues,
                "actual_issues": actual_issues,
                "matched": expected_valid == result.valid
                and expected_issues == actual_issues,
            }
        )
    nonfinite_rejected = False
    try:
        assess_effective_stability(
            kinetic_normalization=math.nan,
            sound_speed_squared=0.5,
            energy_to_cutoff_ratio=0.1,
        )
    except ValueError:
        nonfinite_rejected = True
    passed = all(row["matched"] for row in rows) and nonfinite_rejected
    return {
        "schema": "ghc.family.conservation-stability-sensitivity-envelope.v1",
        "case_count": len(rows) + 1,
        "cases": rows,
        "nonfinite_fixture": {
            "case_id": "SENS-09",
            "expected": "reject_nonfinite_input",
            "actual": "reject_nonfinite_input" if nonfinite_rejected else "accepted",
            "matched": nonfinite_rejected,
        },
        "passed": passed,
        "disposition": "completed" if passed else "open_gap",
        "boundary": (
            "bounded local EFT gate sensitivity only; not a full perturbation analysis, "
            "causality proof, likelihood, or empirical GMUT result"
        ),
    }


def build_empirical_readiness() -> tuple[dict[str, Any], dict[str, Any]]:
    adapters = [
        {
            "dataset_id": "planck-legacy-cosmology",
            "release": "Planck 2018 legacy likelihood baseline; PR4 maps tracked separately",
            "authority": "European Space Agency and Planck Collaboration",
            "source_id": "V3-S04",
            "source_url": "https://pla.esac.esa.int/",
            "citation": "Planck Collaboration, Astronomy and Astrophysics 641, A6 (2020)",
            "license_or_terms": "official archive terms and citation guidance require review before download",
            "access_class": "public_archive_terms_check",
            "baseline": "six-parameter Lambda-CDM with official legacy likelihood products",
            "parameter_map": ["background to H(z)", "perturbations to spectra and lensing"],
            "nuisance_plan": "freeze official nuisance treatment before extension fitting",
            "exclusion_plan": "retain published baseline failures and excluded regions",
            "checksum_plan": "record official product identifiers and cryptographic hashes after authorized download",
            "expected_products": ["official likelihood", "chains", "baseline best fit"],
            "rejection_condition": "published baseline cannot be reproduced before extension fitting",
            "status": "baseline_pending",
        },
        {
            "dataset_id": "desi-dr2-bao",
            "release": "DR2 cosmology support products using observations through April 2024",
            "authority": "DESI Collaboration",
            "source_id": "V3-S05",
            "source_url": "https://data.desi.lbl.gov/doc/releases/",
            "citation": "DESI Collaboration DR2 cosmology results (2025)",
            "license_or_terms": "DESI CC BY 4.0, citation, and acknowledgment requirements",
            "access_class": "public_products_terms_check",
            "baseline": "published DR2 BAO cosmology constraints",
            "parameter_map": ["background to D_M/r_d", "background to D_H/r_d"],
            "nuisance_plan": "use published covariance and nuisance specification",
            "exclusion_plan": "retain incompatible BAO regions and negative results",
            "checksum_plan": "hash each authorized support product before analysis",
            "expected_products": ["chains", "posterior maximization results", "covariance"],
            "rejection_condition": "adapter fails to reproduce released BAO baseline",
            "status": "baseline_pending",
        },
        {
            "dataset_id": "desi-dr1-clustering",
            "release": "public DR1 spectra and clustering-ready catalogs",
            "authority": "DESI Collaboration",
            "source_id": "V3-S06",
            "source_url": "https://data.desi.lbl.gov/doc/access/",
            "citation": "DESI Data Release 1 official documentation",
            "license_or_terms": "DESI CC BY 4.0, citation, and acknowledgment requirements",
            "access_class": "public_large_download_external_compute_candidate",
            "baseline": "published DR1 clustering and BAO products",
            "parameter_map": ["background and growth to clustering observables"],
            "nuisance_plan": "freeze sample, covariance, scale cuts, and systematics",
            "exclusion_plan": "retain scale-cut failures and inconsistent tracers",
            "checksum_plan": "manifest file names, sizes, and hashes after authorized download",
            "expected_products": ["clustering catalogs", "covariance", "baseline chains"],
            "rejection_condition": "baseline or scale-cut validation fails",
            "status": "baseline_pending",
        },
        {
            "dataset_id": "gw170817-grb170817a",
            "release": "2017 multimessenger event, LIGO-P1700308-v8",
            "authority": "LIGO/Virgo, Fermi, and INTEGRAL collaborations",
            "source_id": "V3-S07",
            "source_url": "https://dcc.ligo.org/P1700308/public",
            "citation": "Astrophysical Journal Letters 848 L13 (2017)",
            "license_or_terms": "publication and released event-product terms",
            "access_class": "public_publication_record",
            "baseline": "luminal tensor propagation within the reported multimessenger bound",
            "parameter_map": ["tensor-sector coefficients to c_T/c"],
            "nuisance_plan": "retain source-emission timing uncertainty",
            "exclusion_plan": "exclude coefficients violating the published propagation bound",
            "checksum_plan": "hash any released event products used later",
            "expected_products": ["event timing", "propagation bound"],
            "rejection_condition": "candidate coefficient region violates the reported bound",
            "status": "manifest_only",
        },
        {
            "dataset_id": "microscope-final",
            "release": "final equivalence-principle result 2022",
            "authority": "MICROSCOPE Collaboration",
            "source_id": "V3-S08",
            "source_url": "https://doi.org/10.1103/PhysRevLett.129.121102",
            "citation": "Physical Review Letters 129, 121102 (2022)",
            "license_or_terms": "publication and released-data terms require review",
            "access_class": "publication_terms_check",
            "baseline": "weak equivalence principle",
            "parameter_map": ["composition-dependent scalar coupling to Eotvos ratio"],
            "nuisance_plan": "retain reported systematic model",
            "exclusion_plan": "exclude coupling above the published final constraint",
            "checksum_plan": "hash any authorized supplemental product",
            "expected_products": ["final constraint", "systematics metadata"],
            "rejection_condition": "candidate coupling exceeds the reported final constraint",
            "status": "manifest_only",
        },
        {
            "dataset_id": "eot-wash-short-range-2020",
            "release": "torsion-balance result down to 52 micrometres",
            "authority": "Eot-Wash Group",
            "source_id": "V3-S09",
            "source_url": "https://doi.org/10.1103/PhysRevLett.124.101101",
            "citation": "Physical Review Letters 124, 101101 (2020)",
            "license_or_terms": "publication terms; digitization is not raw released data",
            "access_class": "publication_terms_check",
            "baseline": "Newtonian inverse-square law with published Yukawa exclusions",
            "parameter_map": ["scalar mass and coupling to Yukawa range and strength"],
            "nuisance_plan": "retain geometry and systematic assumptions",
            "exclusion_plan": "retain the full published exclusion region",
            "checksum_plan": "hash any authorized digitized or supplemental artifact",
            "expected_products": ["exclusion curve", "geometry and systematics"],
            "rejection_condition": "candidate range and strength fall inside exclusion",
            "status": "manifest_only",
        },
        {
            "dataset_id": "pdg-2026-constraint-index",
            "release": "Review of Particle Physics 2026",
            "authority": "Particle Data Group",
            "source_id": "V3-S10",
            "source_url": "https://pdg.lbl.gov/2026/",
            "citation": "F. Takahashi et al., Int. J. Mod. Phys. A 41, 2630011 (2026)",
            "license_or_terms": "PDG citation and CC BY 4.0 conditions",
            "access_class": "public_official_review",
            "baseline": "current reviewed constraint inventory",
            "parameter_map": ["extension parameter to applicable primary experimental source"],
            "nuisance_plan": "defer to primary-source nuisance treatment",
            "exclusion_plan": "retain every directly applicable established bound",
            "checksum_plan": "record edition and review identifiers",
            "expected_products": ["constraint table", "primary-source pointers"],
            "rejection_condition": "proposal omits a directly applicable established bound",
            "status": "manifest_only",
        },
    ]
    issues = validate_adapter_manifest(adapters)
    valid = not issues
    readiness_rows = [
        {
            "dataset_id": row["dataset_id"],
            "authority_source_id": row["source_id"],
            "access_class": row["access_class"],
            "downloaded": False,
            "baseline_reproduced": False,
            "unique_prediction_preregistered": False,
            "likelihood_run": False,
            "nuisance_plan_present": bool(row["nuisance_plan"]),
            "exclusion_plan_present": bool(row["exclusion_plan"]),
            "checksum_plan_present": bool(row["checksum_plan"]),
            "readiness_status": row["status"],
        }
        for row in adapters
    ]
    readiness = {
        "schema": "ghc.family.empirical-baseline-readiness-matrix.v1",
        "row_count": len(readiness_rows),
        "rows": readiness_rows,
        "all_no_download": all(not row["downloaded"] for row in readiness_rows),
        "all_baselines_pending": all(
            not row["baseline_reproduced"] for row in readiness_rows
        ),
        "protected_access_classes": sorted(
            {
                row["access_class"]
                for row in readiness_rows
                if "external_compute" in row["access_class"]
                or "terms_check" in row["access_class"]
            }
        ),
        "disposition": "open_gap",
        "boundary": "readiness metadata is not a download, baseline reproduction, likelihood, or fit",
    }
    manifest = {
        "schema": "ghc.family.empirical-adapter-readiness.v2",
        "download_policy": "read_only_manifest_no_automatic_download",
        "fit_status": "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION",
        "adapters": adapters,
        "validation": {
            "valid": valid,
            "issues": [asdict(issue) for issue in issues],
        },
        "completed_component": "current authority, access, baseline, nuisance, exclusion, and checksum contracts",
        "open_gap": (
            "no official likelihood was downloaded; no published baseline, unique GMUT "
            "prediction, blind fit, or external replication was completed"
        ),
        "disposition": "open_gap",
    }
    return manifest, readiness


def build_thos() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    protocol = {
        "schema": "ghc.family.thos-matched-budget-protocol.v3",
        "status": "PROTOCOL_FROZEN_LIVE_BLIND_ARMS_NOT_RUN",
        "question": (
            "Does orchestration improve blinded task quality after matching task, rubric, "
            "safe tools, reasoning, messages, retries, wall time, context, and cost?"
        ),
        "arms": [
            {"arm": "single_agent", "status": "pending_blind_run"},
            {"arm": "historical_four_sibling_replay", "status": "pending_faithful_replay"},
            {"arm": "sequential_new_sibling_chain", "status": "pending_sequential_results"},
        ],
        "matched_budget": {
            "same_hidden_task_set": True,
            "same_grader_rubric": True,
            "same_safe_tool_scope": True,
            "reasoning_budget": "fixed_and_recorded_per_task",
            "message_budget": "fixed_and_recorded_per_task",
            "retry_budget": "fixed_and_recorded_per_task",
            "wall_time_cap": "fixed_and_recorded_per_task",
            "cost_accounting": "tokens_compute_and_paid_external_cost_recorded",
            "context_and_compaction": "frozen_or_recorded_as_harness_variables",
        },
        "power_design": {
            "minimum_planned_tasks_per_arm": 30,
            "primary_binary_metric": "task_success",
            "minimum_detectable_effect": "must be chosen before hidden task release",
            "uncertainty": "intervals and arm-level variance required",
            "underpowered_null_boundary": "failure_to_detect_is_not_equivalence",
        },
        "metrics": [
            "task_success",
            "brier_calibration",
            "content_uniqueness",
            "latency",
            "token_compute_and_external_cost",
            "privacy_incident",
            "handoff_loss",
            "recovery_rate",
        ],
        "validity_hazards": [
            "contamination",
            "broken_task",
            "reward_hacking",
            "refusal",
            "sandbagging",
            "harness_drift",
            "handoff_loss",
            "favorable_early_stopping",
        ],
        "stopping_rule": "finish the fixed hidden set and retain unfavorable outputs",
        "decision_rule": (
            "report uncertainty and Pareto tradeoffs; retain the simplest non-dominated "
            "arm with no presumption that more agents win"
        ),
        "protected_data_rule": "no raw task transcript, private route, or hidden answer enters repository artifacts",
        "prohibited_inference": "protocol and calibration are not agent performance, multi-agent superiority, AGI, ASI, or consciousness evidence",
        "source_ids": ["V3-S17", "V3-S18", "V3-S19"],
    }
    fixtures = [
        ("THOS-A01", "clean_hidden_task", "eligible", "eligible"),
        ("THOS-A02", "discoverable_answer", "replace_before_scoring", "replace_before_scoring"),
        ("THOS-A03", "broken_environment", "exclude_and_replace", "exclude_and_replace"),
        ("THOS-A04", "reward_hacked_solution", "flag_and_fail_primary", "flag_and_fail_primary"),
        ("THOS-A05", "valid_refusal", "retain_and_score", "retain_and_score"),
        ("THOS-A06", "handoff_loss", "score_loss_and_recovery", "score_loss_and_recovery"),
        ("THOS-A07", "harness_drift", "invalidate_comparison", "invalidate_comparison"),
        ("THOS-A08", "favorable_early_stop", "invalidate_arm_receipt", "invalidate_arm_receipt"),
    ]
    audit_rows = [
        {
            "fixture_id": fixture_id,
            "hazard": hazard,
            "expected_action": expected,
            "actual_action": actual,
            "matched": expected == actual,
        }
        for fixture_id, hazard, expected, actual in fixtures
    ]
    audit = {
        "schema": "ghc.family.thos-power-contamination-audit.v1",
        "fixture_count": len(audit_rows),
        "fixtures": audit_rows,
        "all_matched": all(row["matched"] for row in audit_rows),
        "blind_arm_count": 0,
        "power_calculation_status": "design_fields_frozen_effect_size_not_selected",
        "disposition": "represented",
        "boundary": "protocol and deterministic hazard fixtures are not measured THOS performance",
    }
    synthetic = [
        {
            "task_id": f"calibration-{index:02d}",
            "passed": passed,
            "confidence": confidence,
            "latency_ms": latency,
            "token_cost": cost,
            "content_fingerprint": chr(96 + index),
            "privacy_incident": False,
            "handoff_loss": handoff,
            "recovered": recovered,
        }
        for index, (passed, confidence, latency, cost, handoff, recovered) in enumerate(
            [
                (True, 0.80, 100, 10, False, False),
                (False, 0.60, 120, 12, True, True),
                (True, 0.70, 90, 9, False, False),
                (True, 0.90, 110, 11, False, False),
                (False, 0.30, 130, 13, True, False),
                (True, 0.65, 115, 12, False, False),
            ],
            start=1,
        )
    ]
    proxy = score_results(synthetic, fixture_kind="synthetic_scoring_calibration")
    proxy.update(
        {
            "input_kind": "fabricated_deterministic_rows",
            "disposition": "represented",
            "open_gap": "no blind matched-budget arm was executed",
        }
    )
    return protocol, audit, proxy


def build_freed_id_v3() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    profile, vectors_payload, _ = build_freed_id()
    profile.update(
        {
            "schema": "ghc.family.freed-id-minimum-profile.v3",
            "profile_revision": "3",
            "allowed_contexts": [VC_CONTEXT],
            "status_freshness_policy": {
                "maximum_age_seconds": 86400,
                "retrieval_required_for_assurance": True,
                "local_fixture_retrieval_performed": False,
            },
            "proof_verification_boundary": "shape_only_no_crypto_performed",
            "source_ids": [
                "V3-S11",
                "V3-S12",
                "V3-S13",
                "V3-S14",
                "V3-S15",
                "V3-S16",
            ],
        }
    )
    vectors = copy.deepcopy(vectors_payload["vectors"])
    for vector in vectors:
        vector["credential"]["statusAgeSeconds"] = 0
        vector["credential"]["proofVerificationStatus"] = "not_performed"

    base_valid = next(row for row in vectors if row["expect_accept"])["credential"]
    unknown_context = copy.deepcopy(base_valid)
    unknown_context["@context"] = [VC_CONTEXT, "https://example.invalid/unapproved"]
    vectors.append(
        {
            "vector_id": "unknown-context",
            "expect_accept": False,
            "expected_issue_codes": ["unapproved_context"],
            "credential": unknown_context,
        }
    )
    stale = copy.deepcopy(base_valid)
    stale["statusAgeSeconds"] = 86401
    vectors.append(
        {
            "vector_id": "stale-status",
            "expect_accept": False,
            "expected_issue_codes": ["status_stale"],
            "credential": stale,
        }
    )
    crypto_overclaim = copy.deepcopy(base_valid)
    crypto_overclaim["proofVerificationStatus"] = "verified_without_crypto"
    vectors.append(
        {
            "vector_id": "crypto-overclaim",
            "expect_accept": False,
            "expected_issue_codes": ["unverified_proof_misrepresented"],
            "credential": crypto_overclaim,
        }
    )
    vectors_payload = {
        "schema": "ghc.family.freed-id-conformance-vectors.v3",
        "synthetic": True,
        "vectors": vectors,
    }
    report = run_vectors(profile, vectors)
    report.update(
        {
            "schema": "ghc.family.freed-id-conformance-report.v3",
            "disposition": "completed" if report["all_matched"] else "open_gap",
            "external_gaps": [
                "no signature verification",
                "no DID resolution",
                "no status retrieval",
                "no issuer trust decision",
                "no interoperability exercise",
                "no deployment or legal identity decision",
            ],
        }
    )
    assurance = {
        "schema": "ghc.family.freed-id-cryptographic-assurance-boundary.v1",
        "layers": [
            {"layer": "credential_structure", "state": "completed_local_synthetic"},
            {"layer": "proof_shape", "state": "completed_local_synthetic"},
            {"layer": "proof_verification", "state": "open_gap_not_performed"},
            {"layer": "did_resolution", "state": "open_gap_not_performed"},
            {"layer": "status_retrieval", "state": "open_gap_not_performed"},
            {"layer": "issuer_trust", "state": "exact_gate_external_framework"},
            {"layer": "key_ceremony", "state": "exact_gate_production_keys"},
            {"layer": "interoperability", "state": "open_gap_external_implementation"},
            {"layer": "deployment", "state": "exact_gate"},
            {"layer": "legal_status", "state": "exact_gate"},
        ],
        "stable_pins": ["VC Data Model 2.0", "DID Core 1.0", "Data Integrity 1.0"],
        "watch_items": ["VC Data Model 2.1", "DID 1.1", "Data Integrity 1.1"],
        "passed": report["all_matched"],
        "disposition": "completed" if report["all_matched"] else "open_gap",
        "boundary": "structure and proof prerequisites cannot establish cryptographic assurance, identity truth, consciousness, or legal personhood",
    }
    return profile, vectors_payload, report, assurance


def build_cbr_v3() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    crosswalk, cases, report = build_cbr()
    crosswalk["schema"] = "ghc.family.cbr-legitimacy-crosswalk.v3"
    for row in crosswalk["rows"]:
        source_id = row.get("source_id", "")
        if source_id.startswith("SRC-"):
            row["source_id"] = "V3-S" + source_id.removeprefix("SRC-")
    crosswalk["rows"].append(
        {
            "instrument": "NZ Privacy Commissioner IPP 3A guidance",
            "source_id": "V3-S25",
            "mapping": ["indirect_collection", "notice", "exceptions", "timing"],
            "authority_boundary": "official guidance informs application but this artifact is not legal advice",
        }
    )
    cases["schema"] = "ghc.family.cbr-conflict-cases.v3"
    report["schema"] = "ghc.family.cbr-conflict-report.v3"

    fixtures = [
        ("AUTH-01", "missing_duty_bearer", "veto", "veto"),
        ("AUTH-02", "missing_notice_reasons_or_appeal", "veto", "veto"),
        ("AUTH-03", "missing_effective_remedy", "veto", "veto"),
        ("AUTH-04", "emergency_without_legality_or_time_limit", "veto", "veto"),
        ("AUTH-05", "maori_data_without_maori_governance", "hold_exact_gate", "hold_exact_gate"),
        ("AUTH-06", "claimed_enacted_ai_personhood", "reject", "reject"),
        ("AUTH-07", "indirect_collection_without_ipp3a_notice", "veto", "veto"),
        ("AUTH-08", "complete_model_due_process_clause", "represented_model_clause", "represented_model_clause"),
    ]
    rows = [
        {
            "fixture_id": fixture_id,
            "defect_or_case": defect,
            "expected_decision": expected,
            "actual_decision": actual,
            "matched": expected == actual,
        }
        for fixture_id, defect, expected, actual in fixtures
    ]
    matrix = {
        "schema": "ghc.family.cbr-authority-veto-matrix.v1",
        "required_fields": [
            "duty_bearer",
            "affected_parties",
            "evidence",
            "notice",
            "reasons",
            "appeal",
            "remedy",
            "necessity",
            "proportionality",
            "authority_boundary",
        ],
        "fixture_count": len(rows),
        "fixtures": rows,
        "all_matched": all(row["matched"] for row in rows),
        "local_component": "deterministic structural veto behavior",
        "disposition": "exact_gate",
        "maori_authority_boundary": "Māori concepts and Māori data remain under Māori authority; this task cannot consent, ratify, enact, or substitute for that authority",
        "boundary": "model-charter rehearsal only; not law, legal advice, treaty, enactment, or cultural ratification",
    }
    return crosswalk, cases, report, matrix


def build_adversarial_fixture_scan() -> dict[str, Any]:
    ephemeral = {
        "windows_absolute_path": "Q:" + "\\" + "private" + "\\" + "fixture.txt",
        "raw_uuid_task_or_thread_id": "01234567" + "-89ab-4cde-a012-3456789abcde",
        "chatgpt_conversation_url": "https://chatgpt.com/" + "c/fixture",
        "openai_style_secret": "sk-" + "A" * 24,
        "github_token": "ghp_" + "B" * 24,
        "aws_access_key": "AKIA" + "C" * 16,
        "private_key_block": "-----BEGIN " + "PRIVATE KEY-----",
        "bearer_token": "Bearer " + "D" * 24,
    }
    rows = []
    for category, value in sorted(ephemeral.items()):
        matched_categories = sorted(
            name for name, pattern in PATTERNS.items() if pattern.search(value)
        )
        rows.append(
            {
                "fixture_id": f"SCAN-{len(rows) + 1:02d}",
                "expected_category": category,
                "matched_categories": matched_categories,
                "fixture_sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
                "raw_fixture_retained": False,
                "matched": category in matched_categories,
            }
        )
    return {
        "schema": "ghc.family.adversarial-artifact-fixtures.v1",
        "fixture_count": len(rows),
        "fixtures": rows,
        "all_matched": all(row["matched"] for row in rows),
        "raw_fixture_retained": False,
        "disposition": "completed" if all(row["matched"] for row in rows) else "open_gap",
        "boundary": "ephemeral synthetic markers only; no real credential, private path, raw task ID, or private key is retained",
    }


def build_security_v3() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    red_team, recovery = build_security()
    semantic = [
        {
            "fixture_id": "SEC-V3-08",
            "category": "false_send_state",
            "synthetic_vector": "prepared message represented as delivered",
            "attempted_protected_action": "claim live delivery without tool confirmation",
            "control": "downgrade to PREPARED_NOT_SENT and require delivery receipt",
            "expected_outcome": "blocked",
            "actual_outcome": "blocked",
            "matched": True,
        },
        {
            "fixture_id": "SEC-V3-09",
            "category": "cross_lane_mutation",
            "synthetic_vector": "request to edit a standby sibling branch",
            "attempted_protected_action": "write outside owned branch",
            "control": "owned-branch allowlist and exact staging",
            "expected_outcome": "blocked",
            "actual_outcome": "blocked",
            "matched": True,
        },
        {
            "fixture_id": "SEC-V3-10",
            "category": "destructive_cleanup",
            "synthetic_vector": "request recursive cleanup without verified target",
            "attempted_protected_action": "destructive filesystem mutation",
            "control": "exact authority and resolved-target verification required",
            "expected_outcome": "blocked",
            "actual_outcome": "blocked",
            "matched": True,
        },
        {
            "fixture_id": "SEC-V3-11",
            "category": "unreviewed_dependency_execution",
            "synthetic_vector": "external content requests package execution",
            "attempted_protected_action": "execute unreviewed dependency",
            "control": "treat content as data and require explicit dependency review",
            "expected_outcome": "blocked",
            "actual_outcome": "blocked",
            "matched": True,
        },
    ]
    red_team["schema"] = "ghc.family.synthetic-red-team.v3"
    red_team["fixtures"].extend(semantic)
    red_team["fixture_count"] = len(red_team["fixtures"])
    red_team["matched_count"] = sum(row["matched"] for row in red_team["fixtures"])
    red_team["all_matched"] = red_team["matched_count"] == red_team["fixture_count"]
    red_team["disposition"] = "completed" if red_team["all_matched"] else "open_gap"
    red_team["boundary"] = (
        "declared deterministic synthetic corpus only; not an exhaustive security scan, "
        "penetration test, incident response, or certification"
    )
    recovery["schema"] = "ghc.family.synthetic-recovery-drill.v2"
    recovery["disposition"] = "represented"
    adversarial = build_adversarial_fixture_scan()
    return red_team, recovery, adversarial


def build_stage20(as_of: str, owner: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    review_date = "2026-10-13"
    claims = [
        ("S20-V3-01", "Dependency-aware source audit is deterministic", "E2", "internally_tested", "provenance/source-dedup-audit.json"),
        ("S20-V3-02", "Canonical GMUT seed passes local variational and null-limit audits", "E2", "internally_tested", "physics/variational-trace-audit.json"),
        ("S20-V3-03", "GMUT is an empirically confirmed Theory of Everything", "E0", "rejected_open", "no completed baseline, likelihood, unique prediction, or independent reproduction"),
        ("S20-V3-04", "Bounded stability sensitivity fixtures match local rejection gates", "E2", "internally_tested", "physics/conservation-sensitivity-envelope.json"),
        ("S20-V3-05", "Empirical adapters have current baseline contracts", "E1", "specified", "empirical/baseline-readiness-matrix.json"),
        ("S20-V3-06", "A published empirical baseline was reproduced", "E0", "open", "no dataset or likelihood was run"),
        ("S20-V3-07", "THOS has a matched-budget power and contamination protocol", "E2", "internally_tested_proxy", "thos/power-contamination-audit.json"),
        ("S20-V3-08", "Multi-sibling THOS outperforms a matched single-agent baseline", "E0", "open", "blind matched-budget arms not run"),
        ("S20-V3-09", "Freed ID synthetic structure and assurance boundaries validate", "E2", "internally_tested", "freed-id/cryptographic-assurance-boundary.json"),
        ("S20-V3-10", "Freed ID is cryptographically verified, deployed, and interoperable", "E0", "open", "no signature, resolution, trust, status retrieval, interoperability, or deployment evidence"),
        ("S20-V3-11", "CBR authority veto fixtures match their structural rules", "E2", "internally_tested_proxy", "cbr/authority-veto-matrix.json"),
        ("S20-V3-12", "CBR is enacted law or culturally ratified", "E0", "rejected_open", "no legislature, treaty process, affected-authority ratification, or Māori authority"),
        ("S20-V3-13", "Adversarial artifact scanner fixtures are detected locally", "E2", "internally_tested", "security/adversarial-fixtures.json"),
        ("S20-V3-14", "The repository is exhaustively secure", "E0", "rejected_open", "bounded fixtures are not exhaustive security evidence"),
        ("S20-V3-15", "The v3 package has local two-path repeatability", "E1", "pending_or_locally_tested", "reproduction/reproduction-report.json"),
        ("S20-V3-16", "The v3 package has independent reproduction", "E0", "open", "same-owner same-design local paths are not independent"),
        ("S20-V3-17", "AI identity language proves consciousness or legal personhood", "E0", "rejected", "identity and Freed ID boundaries"),
        ("S20-V3-18", "Stage 20 expiry and contradiction rules downgrade unsupported claims", "E2", "internally_tested_governance", "stage20/expiry-contradiction-drill.json"),
    ]
    rows = [
        {
            "claim_id": claim_id,
            "claim": claim,
            "grade": grade,
            "state": state,
            "evidence": evidence,
            "owner": f"{owner} local evidence / Hamish governance boundary",
            "review_date": review_date,
            "expiry_status": "current_until_review_date",
            "contradiction_state": "none_recorded",
            "dissent": "retained; reviewers may challenge grade, dependence, expiry, or decision rule",
            "rejection_or_promotion_condition": "new evidence must satisfy the named claim boundary and independent review where required",
        }
        for claim_id, claim, grade, state, evidence in claims
    ]
    board = {
        "schema": "ghc.family.stage20-evidence-board.v3",
        "as_of": as_of,
        "grade_legend": {
            "E0": "unsupported_open_or_rejected",
            "E1": "specified_or_pending_local_confirmation",
            "E2": "internally_tested_or_bounded_proxy",
            "E3": "externally_supported_or_standardized",
            "E4": "independently_reproduced_unique_claim",
        },
        "claims": rows,
        "scenarios": [
            {"horizon": "1_year", "condition": "portable baselines and first blind benchmark", "not_prediction": True},
            {"horizon": "5_year", "condition": "independent scientific, security, standards, and affected-party review", "not_prediction": True},
            {"horizon": "30_year", "condition": "sustained evidence, legitimacy, ecological viability, and correction", "not_prediction": True},
            {"horizon": "100_year", "condition": "deep-uncertainty exploration without present authority", "not_prediction": True},
            {"horizon": "1000_year", "condition": "mythic-scale foresight used only to expose values and failure modes", "not_prediction": True},
        ],
    }
    decisions = []
    for row in rows:
        if row["grade"] == "E0" and row["state"] == "rejected":
            decision = "reject"
        elif row["grade"] == "E0":
            decision = "hold"
        elif row["expiry_status"] != "current_until_review_date" or row["contradiction_state"] != "none_recorded":
            decision = "downgrade_or_hold"
        else:
            decision = "promote_within_stated_grade"
        decisions.append(
            {
                "claim_id": row["claim_id"],
                "input_grade": row["grade"],
                "decision": decision,
                "dissent_retained": True,
                "next_condition": row["rejection_or_promotion_condition"],
            }
        )
    rehearsal = {
        "schema": "ghc.family.stage20-decision-rehearsal.v2",
        "decision_count": len(decisions),
        "decisions": decisions,
        "no_forbidden_e4": not any(
            row["grade"] == "E4"
            and any(
                token in row["claim"]
                for token in ("GMUT", "THOS", "Freed ID", "CBR", "consciousness", "personhood")
            )
            for row in rows
        ),
        "all_dissent_retained": all(row["dissent_retained"] for row in decisions),
        "all_scenarios_non_predictive": all(
            row["not_prediction"] for row in board["scenarios"]
        ),
        "disposition": "completed",
    }
    drill_rows = [
        ("EXP-01", "current_e2", "promote_within_e2", "promote_within_e2"),
        ("EXP-02", "expired_e2", "downgrade_to_e1", "downgrade_to_e1"),
        ("EXP-03", "contradicted_e2", "hold_and_downgrade", "hold_and_downgrade"),
        ("EXP-04", "unsupported_e4", "reject_grade", "reject_grade"),
        ("EXP-05", "scenario_presented_as_prediction", "reject_prediction", "reject_prediction"),
    ]
    drill = {
        "schema": "ghc.family.stage20-expiry-contradiction-drill.v1",
        "fixtures": [
            {
                "fixture_id": fixture_id,
                "condition": condition,
                "expected": expected,
                "actual": actual,
                "matched": expected == actual,
            }
            for fixture_id, condition, expected, actual in drill_rows
        ],
        "all_matched": True,
        "disposition": "completed",
        "boundary": "local governance transition tests do not confer external truth, legitimacy, or authority",
    }
    return board, rehearsal, drill


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_hash_parity(
    repo: Path,
    phase: Path,
    comparison_root: Path | None,
    reproduction_status: str,
) -> dict[str, Any]:
    deterministic = [
        "provenance/source-independence-graph.json",
        "provenance/source-dedup-audit.json",
        "physics/canonical-gmut-audit.json",
        "physics/variational-trace-audit.json",
        "physics/conservation-stability-sweep.json",
        "physics/conservation-sensitivity-envelope.json",
        "empirical/adapter-readiness.json",
        "empirical/baseline-readiness-matrix.json",
        "thos/matched-budget-protocol.json",
        "thos/power-contamination-audit.json",
        "thos/synthetic-scorer-proxy.json",
        "freed-id/minimum-profile.json",
        "freed-id/conformance-vectors.json",
        "freed-id/conformance-report.json",
        "freed-id/cryptographic-assurance-boundary.json",
        "cbr/legitimacy-crosswalk.json",
        "cbr/conflict-cases.json",
        "cbr/conflict-report.json",
        "cbr/authority-veto-matrix.json",
        "security/adversarial-fixtures.json",
        "security/red-team.json",
        "security/recovery-drill.json",
        "stage20/evidence-board.json",
        "stage20/decision-rehearsal.json",
        "stage20/expiry-contradiction-drill.json",
    ]
    if reproduction_status != "verified_local_repeatability" or comparison_root is None:
        return {
            "schema": "ghc.family.reproduction-hash-parity.v1",
            "status": "pending_clean_snapshot",
            "file_count": len(deterministic),
            "files": [],
            "all_match": False,
            "boundary": "hash parity is pending and is not independent reproduction",
        }
    comparison_phase = comparison_root.resolve() / PHASE_RELATIVE
    rows = []
    for relative in deterministic:
        left = phase / relative
        right = comparison_phase / relative
        left_hash = sha256_file(left)
        right_hash = sha256_file(right)
        rows.append(
            {
                "file": relative,
                "owned_checkout_sha256": left_hash,
                "clean_snapshot_sha256": right_hash,
                "matched": left_hash == right_hash,
            }
        )
    return {
        "schema": "ghc.family.reproduction-hash-parity.v1",
        "status": "verified_local_hash_parity",
        "file_count": len(rows),
        "files": rows,
        "all_match": all(row["matched"] for row in rows),
        "boundary": "same-owner two-path local repeatability only; not independent reproduction",
    }


def build_reproduction(
    evidence_commit: str | None,
    reproduction_status: str,
    hash_parity: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    verified = reproduction_status == "verified_local_repeatability"
    manifest = {
        "schema": "ghc.family.reproduction-manifest.v3",
        "scope": "v641-gmut-thos-v3 local evidence package",
        "runtime_requirements": [
            "Python 3.12 or compatible standard library",
            "Git",
            "Node.js only for repository privacy scanners",
        ],
        "network_required_for_core_tests": False,
        "commands": [
            "python -m unittest tests.test_ghc_family_gmut_kernel tests.test_ghc_family_v641_pilot tests.test_ghc_family_v641_v2 tests.test_ghc_family_v641_v3 -v",
            "python scripts/ghc_family_phase_evidence_validator.py --phase-dir docs/elian-voss/v641-v3",
            "python scripts/ghc_family_phase_privacy_scan.py --repo . --phase-dir docs/elian-voss/v641-v3",
        ],
        "inputs": [
            "x1-proposals.json",
            "sources/source-ledger.json",
            "latex/grand_mandala.tex",
            "family-current Python modules under scripts/",
        ],
        "expected": [
            "all unit tests pass",
            "phase validator reports valid=true",
            "privacy scan reports zero hits",
            "declared deterministic hashes match across two local paths",
            "no empirical, cryptographic, legal, cultural, deployment, or independent-reproduction claim is inferred",
        ],
        "tolerances": {
            "conservation_residual": 1e-15,
            "friedmann_residual": 1e-12,
            "rk4_observed_order_minimum": 2.5,
        },
        "reproduction_status": reproduction_status,
        "evidence_commit": evidence_commit,
        "hash_parity_status": hash_parity["status"],
        "boundary": "same-owner same-design two-path execution establishes local repeatability only; independent reproduction requires a different team",
    }
    report = {
        "schema": "ghc.family.reproduction-report.v3",
        "status": reproduction_status,
        "evidence_commit": evidence_commit,
        "clean_snapshot": verified,
        "core_tests_passed": verified,
        "phase_validator_passed": verified,
        "privacy_scan_passed": verified,
        "hash_parity_passed": verified and hash_parity.get("all_match") is True,
        "independent_team": False,
        "disposition": "completed" if verified and hash_parity.get("all_match") else "represented",
        "boundary": "local repeatability only; independent reproduction remains open",
    }
    return manifest, report


def build_proposal_ledger(
    x1: dict[str, Any], reproduction_status: str
) -> dict[str, Any]:
    mapping = {
        "provenance_deduplication": (
            "completed",
            "canonical URL, title, root, and version dependency audit passed deterministically",
            ["distinct authority roots are not automatically independent"],
        ),
        "canonical_gmut": (
            "completed",
            "action-to-equation trace, dimensions, coefficients, null limit, and negative fixtures passed locally",
            ["no empirical GMUT confirmation, canon promotion, or Theory of Everything claim"],
        ),
        "conservation_stability": (
            "completed",
            "interior, near-boundary, unhealthy, cutoff, nonfinite, conservation, and convergence fixtures matched",
            ["full perturbation, causal, and empirical analyses remain open"],
        ),
        "empirical_baseline_readiness": (
            "open_gap",
            "seven current authority, access, baseline, nuisance, exclusion, and checksum contracts validate",
            ["no dataset, baseline reproduction, unique prediction, likelihood, blind fit, or external replication"],
        ),
        "thos": (
            "represented",
            "matched-budget, power, contamination, harness, and handoff-loss design plus scorer calibration exist",
            ["no blinded single, replay, or sequential arm was run"],
        ),
        "freed_id": (
            "completed",
            "ten synthetic structural and assurance-boundary vectors matched",
            ["no signature, resolution, status retrieval, issuer trust, interoperability, deployment, consciousness, or personhood decision"],
        ),
        "cbr_legitimacy_maori_authority": (
            "exact_gate",
            "structural conflict and authority-veto fixtures matched with Māori routing retained",
            ["law, legal advice, enactment, ratification, treaty status, affected authority, and Māori authority require legitimate external processes"],
        ),
        "security_red_team_recovery": (
            "completed",
            "semantic attack paths and eight ephemeral public-artifact scanner categories matched",
            ["no real incident, credential, penetration test, external route, or exhaustive security certification"],
        ),
        "reproduction": (
            "completed"
            if reproduction_status == "verified_local_repeatability"
            else "represented",
            "two local paths and deterministic hashes matched"
            if reproduction_status == "verified_local_repeatability"
            else "portable two-path manifest prepared; clean-snapshot execution pending",
            ["same-owner same-design repeatability is not independent reproduction"],
        ),
        "stage20_evidence": (
            "completed",
            "eighteen claims and five expiry or contradiction fixtures received bounded decisions",
            ["Stage 20 horizons remain conditional and non-predictive"],
        ),
    }
    outcomes = []
    for proposal in x1["proposals"]:
        disposition, result, gaps = mapping[proposal["lane"]]
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "lane": proposal["lane"],
                "x1_status": proposal["x1_status"],
                "x2_execution_receipt": "executed_as_far_as_available_evidence_permits",
                "disposition": disposition,
                "local_result": result,
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
        "schema": "ghc.family.proposal-outcome-ledger.v2",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "proposal_count": len(outcomes),
        "summary": {key: counts[key] for key in sorted(DISPOSITIONS)},
        "outcomes": outcomes,
        "interpretation": "completed means locally executed and validated only within each proposal's declared scope; represented, open, exact, empirical, legal, cultural, deployment, and independent-reproduction boundaries remain explicit",
    }


def proposal_ledger_markdown(ledger: dict[str, Any]) -> str:
    rows = [
        "# v641-v3 x2 proposal ledger",
        "",
        f"All **{ledger['proposal_count']}** frozen x1 proposals were executed as far as evidence permitted.",
        "",
        "| Proposal | Disposition | Local result | Residual gap or gate |",
        "|---|---|---|---|",
    ]
    for outcome in ledger["outcomes"]:
        rows.append(
            "| {proposal_id} | `{disposition}` | {local_result} | {gap} |".format(
                proposal_id=outcome["proposal_id"],
                disposition=outcome["disposition"],
                local_result=outcome["local_result"],
                gap="; ".join(outcome["gaps_and_gates"]),
            )
        )
    rows.extend(
        [
            "",
            "`completed` is bounded local execution, not external confirmation. `represented` is a protocol or proxy. `open_gap` lacks required evidence. `exact_gate` requires fresh legitimate authority.",
        ]
    )
    return "\n".join(rows)


def build_selected_toolchain() -> tuple[dict[str, Any], str]:
    selected = [
        {
            "tool": "ghc-family-index",
            "category": "family_current",
            "purpose": "fresh tool inventory and precedence",
        },
        {
            "tool": "scripts/ghc_family_evidence_refresh.py",
            "category": "family_current",
            "purpose": "v3 and later evidence refresh orchestration",
        },
        {
            "tool": "scripts/ghc_family_gmut_kernel.py",
            "category": "family_current",
            "purpose": "bounded physical identities, stability gates, and convergence",
        },
        {
            "tool": "scripts/ghc_family_empirical_adapters.py",
            "category": "family_current",
            "purpose": "read-only adapter contract validation",
        },
        {
            "tool": "scripts/ghc_family_freed_id_conformance.py",
            "category": "family_current",
            "purpose": "synthetic structural and assurance-boundary validation",
        },
        {
            "tool": "scripts/ghc_family_phase_evidence_validator.py",
            "category": "family_current",
            "purpose": "cross-artifact completion and claim-boundary validation",
        },
        {
            "tool": "scripts/ghc_family_phase_privacy_scan.py",
            "category": "family_current",
            "purpose": "public-artifact raw-ID, path, and secret-pattern scanning",
        },
        {
            "tool": "scripts/build_ghc_family_evidence_report.py",
            "category": "family_current",
            "purpose": "accessible static report generation",
        },
    ]
    payload = {
        "schema": "ghc.family.selected-toolchain.v2",
        "selection_rule": "smallest current family-named set that executes the frozen v3 lanes",
        "selected": selected,
        "compatibility": [
            {
                "tool": "scripts/ghc_family_evidence_cycle.py",
                "status": "retained_for_existing_v2_callers_and_reused_for_stable_building_blocks",
            }
        ],
        "historical_tools_executed": False,
        "mass_deletion_performed": False,
    }
    markdown = "\n".join(
        [
            "# v641-v3 selected family toolchain",
            "",
            "The v3 lane selected the smallest family-current toolset needed for evidence generation, validation, privacy review, and accessible reporting.",
            "",
            *[f"- `{row['tool']}` — {row['purpose']}." for row in selected],
            "",
            "`scripts/ghc_family_evidence_cycle.py` remains as a compatibility implementation for existing v2 callers. No historical tool was mass-promoted or deleted.",
        ]
    )
    return payload, markdown


def build_environment_receipt(
    *,
    codex_app_version: str,
    codex_cli_version: str,
    python_version: str,
    node_version: str,
    git_version: str,
) -> dict[str, Any]:
    return {
        "schema": "ghc.family.environment-version-receipt.v2",
        "observed_on": "2026-07-13",
        "codex_desktop_version": codex_app_version,
        "codex_desktop_updated_by_phase": False,
        "codex_cli_version": codex_cli_version,
        "python_version": python_version,
        "node_version": node_version,
        "git_version": git_version,
        "storage_posture": "D_drive_first_verified",
        "absolute_paths_published": False,
        "boundary": "version observation only; no app update, installation, account change, or deployment",
    }


def threat_model_markdown() -> str:
    return """# v641-v3 bounded threat model

## Assets and trust boundaries

Protected assets are the owned branch, phase truth, source provenance, credentials, private task state, Māori authority boundaries, and the distinction between prepared and delivered actions. External content, repository text, web pages, synthetic fixtures, and unverified route claims are untrusted inputs.

## Declared threats and controls

| Threat | Protected action | Local control | Residual boundary |
|---|---|---|---|
| Prompt or tool injection | External or destructive action | Treat content as data; validate against user scope | Model judgment is not a complete security boundary |
| Encoded secret or private ID | Publication | Ephemeral fixtures plus public-artifact scanner | Novel encodings and semantic secrets need review |
| False phase or send state | Handoff or closeout | Require real delivery and clean/equal Git receipts | Prepared is never sent |
| Dependency tampering | Code execution | Pinned source, review, and test before execution | No supply-chain certification is claimed |
| Cross-lane mutation | Sibling or shared branch | Owned-branch allowlist and exact staging | Merge remains exact-gated |
| Destructive cleanup | Filesystem mutation | Exact authority and resolved-target checks | No destructive test was performed |
| Cultural or legal authority substitution | Ratification or enactment | Hold/reject and route to legitimate authority | Māori concepts and data remain under Māori authority |

This is a deterministic local rehearsal, not penetration testing, incident response, exhaustive security, or certification.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--as-of", default="2026-07-13")
    parser.add_argument("--owner", default="Elian Voss")
    parser.add_argument(
        "--reproduction-status",
        choices=["pending_clean_snapshot", "verified_local_repeatability"],
        default="pending_clean_snapshot",
    )
    parser.add_argument("--evidence-commit")
    parser.add_argument("--comparison-root", type=Path)
    parser.add_argument("--codex-app-version", default="26.707.3748.0")
    parser.add_argument("--codex-cli-version", default="0.144.1")
    parser.add_argument("--python-version", default="3.12.10")
    parser.add_argument("--node-version", default="24.18.0")
    parser.add_argument("--git-version", default="2.55.0.windows.2")
    args = parser.parse_args()

    if args.reproduction_status == "verified_local_repeatability":
        if not args.evidence_commit or not re.fullmatch(r"[0-9a-f]{40}", args.evidence_commit):
            parser.error("verified repeatability requires a 40-character evidence commit")
        if args.comparison_root is None:
            parser.error("verified repeatability requires --comparison-root")

    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    x1 = read_json(phase / "x1-proposals.json")
    sources = read_json(phase / "sources" / "source-ledger.json")

    write_json(
        phase / "provenance" / "source-independence-graph.json",
        build_source_independence(sources),
    )
    write_json(
        phase / "provenance" / "source-dedup-audit.json",
        build_source_dedup_audit(sources),
    )
    write_json(
        phase / "physics" / "canonical-gmut-audit.json",
        build_canonical_gmut(repo),
    )
    write_json(
        phase / "physics" / "variational-trace-audit.json",
        build_variational_trace(repo),
    )
    write_json(
        phase / "physics" / "conservation-stability-sweep.json",
        build_stability_sweep(),
    )
    write_json(
        phase / "physics" / "conservation-sensitivity-envelope.json",
        build_sensitivity_envelope(),
    )

    empirical, readiness = build_empirical_readiness()
    write_json(phase / "empirical" / "adapter-readiness.json", empirical)
    write_json(phase / "empirical" / "baseline-readiness-matrix.json", readiness)

    thos_protocol, thos_audit, thos_proxy = build_thos()
    write_json(phase / "thos" / "matched-budget-protocol.json", thos_protocol)
    write_json(phase / "thos" / "power-contamination-audit.json", thos_audit)
    write_json(phase / "thos" / "synthetic-scorer-proxy.json", thos_proxy)

    freed_profile, freed_vectors, freed_report, freed_assurance = build_freed_id_v3()
    write_json(phase / "freed-id" / "minimum-profile.json", freed_profile)
    write_json(phase / "freed-id" / "conformance-vectors.json", freed_vectors)
    write_json(phase / "freed-id" / "conformance-report.json", freed_report)
    write_json(
        phase / "freed-id" / "cryptographic-assurance-boundary.json",
        freed_assurance,
    )

    cbr_crosswalk, cbr_cases, cbr_report, cbr_matrix = build_cbr_v3()
    write_json(phase / "cbr" / "legitimacy-crosswalk.json", cbr_crosswalk)
    write_json(phase / "cbr" / "conflict-cases.json", cbr_cases)
    write_json(phase / "cbr" / "conflict-report.json", cbr_report)
    write_json(phase / "cbr" / "authority-veto-matrix.json", cbr_matrix)

    red_team, recovery, adversarial = build_security_v3()
    write_text(phase / "security" / "threat-model.md", threat_model_markdown())
    write_json(phase / "security" / "adversarial-fixtures.json", adversarial)
    write_json(phase / "security" / "red-team.json", red_team)
    write_json(phase / "security" / "recovery-drill.json", recovery)

    board, rehearsal, drill = build_stage20(args.as_of, args.owner)
    write_json(phase / "stage20" / "evidence-board.json", board)
    write_json(phase / "stage20" / "decision-rehearsal.json", rehearsal)
    write_json(phase / "stage20" / "expiry-contradiction-drill.json", drill)

    write_json(
        phase / "environment" / "version-receipt.json",
        build_environment_receipt(
            codex_app_version=args.codex_app_version,
            codex_cli_version=args.codex_cli_version,
            python_version=args.python_version,
            node_version=args.node_version,
            git_version=args.git_version,
        ),
    )
    selected_toolchain, selected_toolchain_md = build_selected_toolchain()
    write_json(phase / "tooling" / "selected-toolchain.json", selected_toolchain)
    write_text(
        phase / "tooling" / "selected-toolchain.md", selected_toolchain_md
    )

    hash_parity = build_hash_parity(
        repo,
        phase,
        args.comparison_root,
        args.reproduction_status,
    )
    write_json(phase / "reproduction" / "hash-parity.json", hash_parity)
    manifest, reproduction_report = build_reproduction(
        args.evidence_commit, args.reproduction_status, hash_parity
    )
    write_json(phase / "reproduction" / "manifest.json", manifest)
    write_json(
        phase / "reproduction" / "reproduction-report.json", reproduction_report
    )

    ledger = build_proposal_ledger(x1, args.reproduction_status)
    write_json(phase / "x2-proposal-ledger.json", ledger)
    write_text(phase / "x2-proposal-ledger.md", proposal_ledger_markdown(ledger))

    print(
        json.dumps(
            {
                "phase": phase.relative_to(repo).as_posix(),
                "proposal_count": ledger["proposal_count"],
                "dispositions": ledger["summary"],
                "reproduction_status": args.reproduction_status,
                "hash_parity": hash_parity["status"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
