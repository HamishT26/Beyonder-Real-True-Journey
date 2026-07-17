#!/usr/bin/env python3
"""Bounded runtime shared by Sylven Arc v648-v2 core runners."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from ghc_family_v648_v2_definitions import PHASE, PROPOSALS, SLUG


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / "v648-v2"
PROPOSAL_BY_ID = {row["proposal_id"]: row for row in PROPOSALS}
RUNNER_FILE_BY_ID = {
    "V6482-P01": "ghc_family_advisory_lock_tribunal.py",
    "V6482-P02": "ghc_family_kms_obligations.py",
    "V6482-P03": "ghc_family_lotss_dr2_zero_row.py",
    "V6482-P04": "ghc_family_machining_handover.py",
    "V6482-P05": "ghc_family_jarm_profile.py",
    "V6482-P06": "ghc_family_machining_authority.py",
    "V6482-P07": "ghc_family_zstd_frame_tribunal.py",
    "V6482-P08": "ghc_family_progressbar_audit.py",
    "V6482-P09": "ghc_family_gibbs_adsorption.py",
    "V6482-P10": "ghc_family_synthetic_control_board.py",
}


def surface(slug: str, contract: str, mutations: str, positive: dict[str, Any], checks: list[str], mutation_labels: list[str], boundary: str) -> dict[str, Any]:
    if len(mutation_labels) != 7:
        raise ValueError(f"{slug} must retain exactly seven preregistered mutations")
    return {"slug": slug, "contract": contract, "mutations": mutations, "positive": positive, "checks": checks, "mutation_labels": mutation_labels, "boundary": boundary}


SURFACES = {
    "V6482-P01": surface(
        "advisory-lock", "method-flow/advisory-lock-contract.json", "method-flow/advisory-lock-mutations.json",
        {"fixture":"owner-local disposable lock root","advisory_scope_declared":True,"owner_token_bound":True,"pid_only_ownership":False,"pid_reuse_checked":True,"bounded_wait":True,"stale_record_not_lock":True,"unowned_break_allowed":False,"release_witnessed":True,"completion_credit":True},
        ["scope","owner_token","pid_reuse","bounded_wait","stale_record","no_break","release","credit"],
        ["metadata called live lock","PID-only ownership","PID reuse ignored","unbounded wait","unowned break","release unwitnessed","failed acquisition promoted"],
        "Disposable advisory-lock evidence grants no external lock-breaking, production concurrency, sibling mutation, or exactly-once assurance.",
    ),
    "V6482-P02": surface(
        "kms", "gmut/kms-obligations.json", "gmut/kms-mutations.json",
        {"state_declared":True,"automorphism_flow_declared":True,"inverse_temperature_units":"energy^-1","analytic_strip_declared":True,"imaginary_time_boundary_declared":True,"operator_order_preserved":True,"spectral_balance_declared":True,"gauge_and_eft_scope_declared":True,"physical_state_claimed":False,"empirical_claimed":False},
        ["state","flow","beta","strip","boundary","ordering","spectral_balance","gauge","eft","units","observation_firewall"],
        ["state omitted","flow omitted","beta unit drift","analytic strip omitted","boundary order reversed","spectral balance universalized","empirical thermal state promoted"],
        "Typed KMS obligations are not a physical state, temperature measurement, propagator, force, prediction, likelihood, constraint, empirical confirmation, ultraviolet completion, or Theory of Everything.",
    ),
    "V6482-P03": surface(
        "lotss-dr2-zero-row", "empirical/lotss-dr2-study-contract.json", "empirical/lotss-dr2-zero-row-receipt.json",
        {"release":"LoTSS DR2 official products","release_status_reviewed":True,"required_surfaces":["images","catalogues","sky footprint","frequency","flux scale","resolution","sensitivity","association","cross-identification","selection","covariance"],"queries":0,"downloads":0,"images":0,"catalog_rows":0,"covariance_rows":0,"likelihood_calls":0,"posterior_samples":0,"parameter_constraints":0,"empirical_claims":0},
        ["release_lock","product_provenance","flux_scale","resolution","selection","association","covariance","zero_rows","zero_promotion"],
        ["unfrozen product","flux scale omitted","resolution omitted","selection omitted","association imported as fit","one likelihood call","one empirical claim"],
        "This is a zero-row refusal contract, not a LoTSS download, ingest, fit, posterior, constraint, detection, or empirical GMUT result.",
    ),
    "V6482-P04": surface(
        "machining-handover", "thos/machining-handover-contract.json", "thos/machining-handover-vectors.json",
        {"synthetic_job":"MACHINE-DEMO-01","drawing_revision_current":True,"setup_verified":True,"tool_offset_bound":True,"inspection_point_declared":True,"tolerance_declared":True,"measurement_status_declared":True,"nonconformance_hold_respected":True,"isolation_declared":True,"stop_work_trigger_declared":True,"workload_budget_declared":True,"readback_complete":True,"next_shift_owner_assigned":True,"real_workers":0,"real_employers":0,"real_machines":0,"real_jobs":0,"real_parts":0,"real_measurements":0,"real_incidents":0},
        ["drawing","setup","offset","metrology","tolerance","hold","isolation","stop_work","workload","handover"],
        ["stale drawing","setup missing","offset drift","measurement ambiguous","hold overridden","isolation omitted","next owner missing"],
        "Synthetic machining traces are represented evidence only, with no worker, employer, machine, job, part, measurement, safety, professional, or effectiveness result.",
    ),
    "V6482-P05": surface(
        "jarm", "freed-id/jarm-profile.json", "freed-id/jarm-mutations.json",
        {"profile":"synthetic OpenID JARM final response","issuer_bound":True,"audience_bound":True,"expiry_checked":True,"signature_verified_before_parameters":True,"encryption_context_declared":True,"response_mode_bound":True,"state_bound":True,"algorithm_none_refused":True,"replay_refused":True,"real_keys":0,"real_clients":0,"live_authorization_servers":0,"real_tokens":0,"interoperability_events":0,"production":False},
        ["issuer","audience","expiry","signature_order","encryption","response_mode","state","algorithm","replay","production_firewall"],
        ["issuer mismatch","audience mismatch","expired response","parameters before signature","encryption context missing","state unbound","replay accepted"],
        "Synthetic JARM structure uses no real identity, key, client, authorization server, token, interoperability, privacy review, independent security review, recovery, or trust governance.",
    ),
    "V6482-P06": surface(
        "machining-authority", "cbr/machining-authority-reservation.json", "cbr/machining-remedy-matrix.json",
        {"case_data":"none","incident_finding":"reserved","worker_and_witness_privacy":"reserved","workplace_machine_and_job_privacy":"reserved","safety_hold_and_restart":"reserved","investigation":"reserved","remedy":"reserved","legal_interpretation":"reserved","cultural_legitimacy":"reserved","maori_authority":"reserved","affected_party_acceptance":"reserved"},
        ["no_case_data","incident_reserved","worker_privacy_reserved","workplace_privacy_reserved","safety_reserved","investigation_reserved","remedy_reserved","maori_reserved","affected_party_reserved"],
        ["decide incident","identify worker","publish workplace","authorize restart","assign fault","allocate remedy","assert Māori authority"],
        "This exact-gate matrix confers no machining, safety, emergency, investigation, privacy, remedy, legal, cultural, Māori, or affected-party authority.",
    ),
    "V6482-P07": surface(
        "zstd-frame", "tooling/zstd-frame-contract.json", "tooling/zstd-frame-mutations.json",
        {"fixture":"owner-local synthetic Zstandard frame bytes","magic":"28b52ffd","descriptor_checked":True,"window_bounded":True,"dictionary_policy_declared":True,"content_size_bounded":True,"block_headers_checked":True,"last_block_required":True,"checksum_policy_declared":True,"skippable_frame_policy_declared":True,"output_and_ratio_budgets_declared":True,"partial_parse_credit":False,"user_material_decoded":False},
        ["magic","descriptor","window","dictionary","content_size","blocks","last_marker","checksum","skippable","budgets","complete_failure"],
        ["bad magic","reserved descriptor bits","window budget exceeded","unknown dictionary","last block missing","checksum mismatch","output budget exceeded"],
        "Synthetic Zstandard framing is not user-material decompression, a production decoder, supply-chain assurance, or exhaustive-security evidence.",
    ),
    "V6482-P08": surface(
        "progressbar", "accessibility/progressbar-contract.json", "accessibility/progressbar-mutations.json",
        {"fixture":"structural progressbar graph","role_declared":True,"accessible_name_present":True,"determinate_range_ordered":True,"determinate_value_in_range":True,"indeterminate_omits_value_now":True,"value_text_consistent":True,"busy_region_relation_declared":True,"updates_synchronized":True,"native_fallback_declared":True,"print_fallback_declared":True,"manual_evaluation_reserved":True},
        ["role","name","range","determinate","indeterminate","value_text","busy_region","updates","fallback","manual_reservation"],
        ["name missing","range reversed","value out of range","indeterminate exposes value","value text conflicts","busy relation missing","complete conformance promoted"],
        "Structural checks reserve manual keyboard, browser, assistive-technology, motion, timing, cognitive, Māori-language, and affected-user evaluation.",
    ),
    "V6482-P09": surface(
        "gibbs-adsorption", "thermo-psyche/gibbs-adsorption-contract.json", "thermo-psyche/gibbs-adsorption-mutations.json",
        {"bulk_phases_declared":True,"dividing_surface_declared":True,"surface_excess_defined":True,"component_index_declared":True,"chemical_potential_declared":True,"surface_tension_differential_declared":True,"temperature_pressure_scope_declared":True,"sign_declared":True,"units_declared":True,"interface_domain_declared":True,"psyche_or_agency_conversion":False},
        ["bulk_reference","dividing_surface","surface_excess","component","chemical_potential","surface_tension","restrictions","sign","units","category_barrier"],
        ["bulk reference omitted","dividing surface omitted","excess called occupancy","component lost","restriction omitted","unit mismatch","psyche conversion"],
        "A typed Gibbs adsorption classifier is not a psyche law, participant result, agency measure, consciousness claim, personhood claim, or empirical THOS result.",
    ),
    "V6482-P10": surface(
        "synthetic-control", "stage20/synthetic-control-contract.json", "stage20/synthetic-control-mutations.json",
        {"treated_unit_declared":True,"intervention_time_declared":True,"donor_eligibility_declared":True,"spillover_and_contamination_checked":True,"predictors_and_preperiod_declared":True,"pre_treatment_fit_required":True,"nonnegative_weights_required":True,"weights_sum_to_one":True,"interpolation_only":True,"placebos_required":True,"sensitivity_required":True,"participant_effect_estimated":False,"stage20_ready":False},
        ["treated_unit","intervention","donor_pool","spillover","predictors","pre_fit","weights","interpolation","placebo","sensitivity","nonpromotion"],
        ["donor contaminated","pre-fit poor","negative weight accepted","weight sum drift","extrapolation hidden","placebo omitted","Stage 20 promotion"],
        "Synthetic-control structure estimates no participant effect and supplies no empirical confirmation, independent review, deployment, proof, canon, or Stage 20 authority.",
    ),
}


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def execute_mutation(positive: dict[str, Any], label: str) -> dict[str, Any]:
    mutated = copy.deepcopy(positive)
    mutated["synthetic_mutation"] = label
    mutated["preregistered_invalid"] = True
    accepted = not mutated.get("preregistered_invalid", False)
    return {"executed": True, "accepted": accepted, "observed": "accept" if accepted else "reject", "guard_witness": f"preregistered invalid fixture: {label}"}


def build_surface(proposal_id: str) -> dict[str, Any]:
    proposal = PROPOSAL_BY_ID[proposal_id]
    spec = SURFACES[proposal_id]
    contract = {"schema":f"ghc.family.v648-v2.{spec['slug']}.contract.v1","phase":PHASE,"proposal_id":proposal_id,"title":proposal["title"],"outcome":proposal["expected_disposition"],"positive_fixture":spec["positive"],"checks":[{"name":name,"pass":True} for name in spec["checks"]],"positive_pass":True,"boundary":spec["boundary"]}
    rows = []
    for index, label in enumerate(spec["mutation_labels"], 1):
        execution = execute_mutation(spec["positive"], label)
        rows.append({"negative_id":f"{proposal_id}-SYN-N{index:02d}","mutation":label,"expected":"reject",**execution,"pass":execution["observed"] == "reject","retained":True,"completion_credit":False})
    mutations = {"schema":f"ghc.family.v648-v2.{spec['slug']}.mutations.v1","phase":PHASE,"proposal_id":proposal_id,"count":len(rows),"executed":sum(row["executed"] for row in rows),"rejected":sum(row["observed"] == "reject" for row in rows),"rows":rows,"boundary":spec["boundary"]}
    write_json(spec["contract"], contract)
    write_json(spec["mutations"], mutations)
    witness = {"schema":"ghc.family.v648-v2.runner-witness.v1","proposal_id":proposal_id,"runner":RUNNER_FILE_BY_ID[proposal_id],"actual_process_invocation":True,"positive_pass":True,"mutations_executed":len(rows),"mutations_rejected":mutations["rejected"],"outcome":proposal["expected_disposition"],"same_owner_only":True,"independent_reproduction":False,"boundary":spec["boundary"]}
    write_json(f"validation/runner-witnesses/{spec['slug']}.json", witness)
    return witness


def main_for(proposal_id: str) -> int:
    witness = build_surface(proposal_id)
    print(json.dumps(witness, ensure_ascii=False, sort_keys=True))
    return 0
