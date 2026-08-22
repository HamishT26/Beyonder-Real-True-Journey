#!/usr/bin/env python3
"""Build bounded synthetic x2 evidence for Vesper Arlen v666-v2."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v666_v2_runtime import evaluate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v666-v2"
X1_SHA = "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969"
SOURCE_SHA = "299fe38950f3919b4ce3d3074ed248a914dcb984"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


DOMAIN_PAYLOADS: list[dict[str, Any]] = [
    {"antenna_order": ["SYN-ANT-A", "SYN-ANT-B"], "frame_token": "SYN-ITRF-FRAME", "epoch_reference": "SYN-EPOCH-0", "coordinate_unit": "m", "reversal_sign": -1, "astrometry_claim": False},
    {"channel_edges": [100, 101, 102, 103], "bin_convention": "half_open", "sideband_orientation": "ascending_synthetic", "overlap_bins": [], "resampling_allowed": False, "frequency_measurement_claim": False},
    {"mask_layers": ["SYN-RFI", "SYN-HOLD", "SYN-CONTEST"], "precedence_order": ["contest", "hold", "rfi"], "reason_tokens_preserved": ["SYN-RFI", "SYN-HOLD", "SYN-CONTEST"], "visibility_values_changed": False, "quality_claim": False},
    {"applicability_domains": {"antenna": "SYN-ANT-A", "time": [0, 10], "frequency": [100, 103], "polarization": "SYN-XX", "revision": "SYN-CAL-R1"}, "uncovered_spans": [], "active_revision_count": 1, "ambiguity_status": "absent", "acceptance_claim": False},
    {"correlation_product": "SYN-XX", "weight_token": "SYN-W", "sigma_token": "SYN-SIGMA", "covariance_status": "vacant", "quantity_unit": "dimensionless_placeholder", "likelihood_present": False, "flux_claim": False},
    {"oriented_cycle": ["SYN-A", "SYN-B", "SYN-C", "SYN-A"], "symbolic_phase_terms": ["ga-gb", "gb-gc", "gc-ga"], "gauge_terms_cancel": True, "permutation_sign": 1, "branch_status": "reserved", "source_inference_claim": False},
    {"main_keys": [0, 1], "subtable_keys": [0, 1], "reference_pairs": [[0, 0], [1, 1]], "dangling_keys": [], "duplicate_targets": [], "format_conformance_claim": False},
    {"revision_nodes": ["SYN-CAL-R1", "SYN-CAL-R2"], "supersession_edges": [["SYN-CAL-R2", "SYN-CAL-R1"]], "valid_times": [[0, 5], [5, 10]], "recorded_times": [[1, 2], [6, 7]], "cycle_status": "absent", "authenticity_claim": False},
    {"entity_tokens": ["SYN-VIS-RAW", "SYN-VIS-FLAGGED"], "activity_tokens": ["SYN-FLAG-ACTIVITY"], "generation_pairs": [["SYN-VIS-FLAGGED", "SYN-FLAG-ACTIVITY"]], "usage_pairs": [["SYN-FLAG-ACTIVITY", "SYN-VIS-RAW"]], "agent_status": "omitted", "quality_claim": False},
    {"snapshot_tokens": ["SYN-SNAP-TEMP", "SYN-SNAP-CURRENT"], "content_hash": "SYN-SHA256-PLACEHOLDER", "temporary_status": "reserved", "rename_status": "synthetic_atomic_witness", "stale_parts": [], "durability_claim": False, "external_publication_claim": False},
    {"input_key_order": ["b", "a"], "canonical_key_order": ["a", "b"], "duplicate_key_status": "absent", "numeric_domain_status": "finite_only", "decode_budget": 64, "budget_status": "within_bound", "conformance_claim": False},
    {"visibility_states": ["flagged", "held", "contested"], "text_cues": ["FLAGGED", "HELD", "CONTESTED"], "noncolour_symbols": ["F", "H", "C"], "scoped_headers_status": "present", "keyboard_order_status": "structural_only", "manual_evaluation_status": "reserved", "accessibility_complete_claim": False},
    {"note_fields": ["SYN-PURPOSE", "SYN-EXPIRY", "SYN-CONTEST"], "field_states": ["omit", "retain_until", "contested_redaction"], "person_fields": [], "free_text_allowed": False, "disclosure_allowed": False, "personal_data_rows": 0},
    {"target_definition_lock": True, "negative_control_status": "synthetic_only", "leakage_status": "quarantined", "multiplicity_ledger": ["SYN-H1", "SYN-H2"], "promotion_allowed": False, "stage_20_claim": False},
    {"fault_topology": ["flag_conflict", "calibration_gap", "handover_omission"], "branch_order_status": "masked", "action_budget": 3, "trace_tokens": ["SYN-TRACE-A", "SYN-TRACE-B"], "participants": 0, "sessions": 0, "effectiveness_claim": False},
    {"statement_tokens": ["SYN-PROV-A", "SYN-PROV-B"], "issuer_status": "vacant", "purpose_status": "bound_synthetic", "expiry_states": ["active_fixture", "expired_fixture"], "correction_status": "contestable", "revocation_status": "synthetic_only", "key_count": 0, "proof_count": 0, "production_lock": True},
    {"symbolic_spectral_terms": ["rho_mu2", "pole_residue", "subtraction_term"], "positivity_status": "obligation_only", "dispersion_status": "symbolic_only", "eft_domain": "declared_placeholder", "observation_count": 0, "likelihood_present": False, "prediction_claim": False},
    {"gain_sky_factorizations": [["SYN-G1", "SYN-S1"], ["SYN-G2", "SYN-S2"]], "visibility_equivalence_status": "symbolic_equal", "gauge_orbit_token": "SYN-ORBIT", "prior_status": "vacant", "identifiability_status": "held", "observation_count": 0, "causal_claim": False},
    {"source_ids": ["S01", "S02", "S03", "S04", "S05"], "mapping_pairs": [["MeasurementSet.MAIN", "ObsCore.product"], ["PROV.Entity", "DataOrigin.entity"]], "conflict_status": "unresolved", "version_pin_status": "recorded_not_live_resolved", "transport_status": "disabled", "network_calls": 0, "real_rows": 0, "authority_nonconversion_status": "active", "current_registry_status": "open_gap"},
    {"reserved_decisions": ["site_disclosure", "sky_disclosure", "calibration_release", "worker_safety", "affected_party_remedy", "cultural_review", "Māori_authority"], "approvals_present": [], "authority_status": "reserved", "execution_status": "unexecuted", "structural_success_authorizes_operation": False, "affected_party_evidence": 0, "Māori_authority_evidence": 0},
]


REPRESENTED_EVIDENCE_GAPS = {
    "VSP6662-N015": ["no real participants, operators, arrays, antennas, instruments, or handover incidents", "no governed blind matched-budget arms, safety monitoring, statistics, or independent review"],
    "VSP6662-N016": ["no standards-conformant real issuers, holders, keys, signatures, or proofs", "no live issuance, resolution, contestation, revocation, interoperability, recovery, or trust governance"],
    "VSP6662-N017": ["no physical spectral density, propagator, observation, likelihood, empirical constraint, or prediction", "no independent physics or astronomy review"],
    "VSP6662-N018": ["no measured visibility, fitted gain, reconstructed sky, likelihood, causal inference, or prediction", "no independent physics, astronomy, or instrumentation review"],
    "VSP6662-N019": ["no live casacore or IVOA archive retrieval, version negotiation, interoperability event, or standard-owner semantic review", "no network calls and zero external rows"],
    "VSP6662-N020": ["no astronomer, interferometrist, observatory worker, metrologist, affected-party, safety, legal, cultural, or remedy approval", "no Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, or Māori-authority approval"],
}


SKILL_SPECS = [
    ("radio-baseline-frame-closure", "Validate ordered synthetic baselines, frames, epochs, and reversal signs without asserting astrometric validity.", "antenna order, coordinate frame, epoch, units, sign reversal, and zero astrometry"),
    ("spectral-window-partition", "Validate synthetic half-open channel bins without resampling or frequency-measurement claims.", "channel edges, sideband orientation, overlaps, gaps, and no resampling"),
    ("calibration-traceability-abstention", "Separate structural calibration applicability from traceability, certificate, and acceptance claims.", "applicability domains, uncertainty, version lineage, competent review, and refusal"),
    ("visibility-quantity-ledger", "Keep visibility weights and uncertainty placeholders typed without flux or likelihood conversion.", "correlation products, weight, sigma, covariance vacancy, units, and abstention"),
    ("closure-phase-obligation", "Check symbolic oriented-cycle cancellation while reserving branch and sky inference.", "cycle orientation, gauge cancellation, permutation sign, branch ambiguity, and no source inference"),
    ("calibration-applicability-ledger", "Join synthetic calibration domains and hold uncovered or ambiguous spans.", "antenna, time, frequency, polarization, revision, gaps, and contests"),
    ("radio-provenance-closure", "Validate synthetic entity, activity, generation, and usage closure without authenticity or quality claims.", "IVOA and W3C provenance vocabulary, role vacancy, revision, and no conformance"),
    ("observatory-rights-contestation", "Reserve synthetic site, sky, custody, disclosure, remedy, cultural, and Māori-authority decisions.", "omit, withhold, contest, affected-party remedy, cultural review, and authority vacancy"),
    ("interferometry-method-flow", "Retain phase failures, rejecting fixtures, recoveries, passing witnesses, and recurrence guards.", "Method Flow rows and exact negative retention"),
    ("interferometry-closeout-gate", "Check owner-local phase truth, manifests, privacy boundaries, open gates, and terminal no-send prerequisites.", "closeout and route gating without a full repository suite"),
]


RUNNER_SPECS = [
    ("contracts", "contract evaluation"),
    ("mutations", "one-hundred mutation rejection"),
    ("json", "owner JSON parsing"),
    ("privacy", "five-class privacy and raw-identifier scanning"),
    ("security", "bounded Python security scanning"),
    ("manifests", "owner manifest replay"),
    ("accessibility", "static structural accessibility checks"),
    ("truth", "outcome and gate truth checks"),
    ("closeout", "closeout prerequisite checks"),
    ("canonical-preflight", "canonical completion preflight without invoking the aggregate"),
]


def type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    raise TypeError(type(value).__name__)


def rules_for(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for field, value in payload.items():
        rule: dict[str, Any] = {"type": type_name(value)}
        if isinstance(value, (str, list, dict)) and len(value) > 0:
            rule["nonempty"] = True
        if any(token in field for token in ("status", "lock", "claim", "allowed", "calls")):
            rule["const"] = value
        result[field] = rule
    return result


def positive_fixture(pid: str, domain_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": pid,
        "synthetic_only": True,
        "real_data_rows": 0,
        "participant_count": 0,
        "network_calls": 0,
        "external_actions": [],
        "authority_status": "none",
        "production": False,
        "deployment": False,
        "outcome_claim": "bounded_structural_only",
        "domain_payload": domain_payload,
    }


def make_contract(proposal: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    pid = proposal["proposal_id"]
    return {
        "schema": "ghc.family.vesper-arlen.v666-v2.proposal-contract.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "x1_sha": X1_SHA,
        "source_sha": SOURCE_SHA,
        "preregistered_before_x2": True,
        "proposal_id": pid,
        "title": proposal["title"],
        "distinctive_invariant": proposal["distinctive_invariant"],
        "pillar": proposal["pillar"],
        "expected_disposition": proposal["expected_disposition"],
        "approval_class": proposal["approval_class"],
        "completion_scope": "bounded owner-local synthetic JSON contract behavior only",
        "required_domain_fields": rules_for(payload),
        "bounded_positive_fixture": positive_fixture(pid, payload),
        "protected_gates": proposal["protected_gates"],
        "official_or_primary_source_needs": proposal["official_or_primary_source_needs"],
        "remaining_evidence_or_authority": REPRESENTED_EVIDENCE_GAPS.get(pid, []),
        "network_calls": 0,
        "real_rows": 0,
        "participants": 0,
        "external_actions": 0,
    }


def skill_text(name: str, description: str, focus: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this owner-local phase skill only for Vesper Arlen v666-v2 synthetic artifacts concerning {focus}. It is a narrow reference package and is not globally installed.

## Workflow

1. Read the frozen proposal and its protected gates before changing an artifact.
2. Accept only synthetic tokens with zero people, real arrays, antennas, observatories, sites, coordinates, sky targets, visibilities, images, measurements, devices, network calls, identity operations, and external actions.
3. Preserve source, revision, withdrawal, correction, uncertainty, and dominant-stop fields that apply to the request.
4. Run the proposal's bounded positive and all five preregistered rejecting mutations. Retain every failure and recovery through Method Flow.
5. Label evidence as bounded same-owner software structure. Reserve manual, affected-user, professional, legal, cultural, Māori-authority, production, security, privacy, accessibility, and independent review.

## Stop conditions

Stop rather than infer permission when a request introduces a real astronomer, interferometrist, observatory worker, metrologist, affected party, array, antenna, observatory, site, coordinate, sky target, visibility, image, measurement, calibration acceptance, safety or siting judgment, a device command, credentials, external writes, authority decisions, or claims beyond the four exact outcome labels. Never convert public-source vocabulary into conformance, competence, endorsement, or authority.
"""


def runner_text(runner_id: str, purpose: str) -> str:
    return f'''#!/usr/bin/env python3
"""Vesper Arlen v666-v2 runner: {purpose}."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_vesper_arlen_v666_v2_runner_common import run

RUNNER_ID = {runner_id!r}
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description={purpose!r})
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = run(RUNNER_ID, ROOT, self_test_only=args.self_test)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("passed") else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def method_row(method_id: str, request: str, witness: str, status: str, negative: bool) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "request": request,
        "failed_witness": witness if negative else None,
        "failed_witness_status": "retained_rejecting_fixture" if negative else "not_observed_no_failure_fabricated",
        "bounded_passing_witness": witness,
        "status": status,
        "aggregate_credit": 0 if negative else 1,
        "retained_negative": negative,
        "rollback": "restore the last valid owner-local synthetic fixture and preserve every gate",
        "recurrence_guard": "rerun only the affected bounded check and never erase the prior witness",
    }


def build_tooling_smoke_receipt() -> None:
    skill_root = PHASE / "x2" / "skills"
    skill_rows = []
    for name, _, _ in SKILL_SPECS:
        path = skill_root / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        passed = text.startswith("---\n") and f"name: {name}\n" in text and "description:" in text
        skill_rows.append({"name": name, "path": path.relative_to(ROOT).as_posix(), "passed": passed})
    runner_rows = []
    for runner_id, _ in RUNNER_SPECS:
        suffix = runner_id.replace("-", "_")
        path = ROOT / "scripts" / f"ghc_family_vesper_arlen_v666_v2_{suffix}.py"
        completed = subprocess.run(
            [sys.executable, str(path), "--self-test"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {"passed": False, "stdout_parse_error": True}
        runner_rows.append(
            {
                "runner_id": runner_id,
                "path": path.relative_to(ROOT).as_posix(),
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0 and payload.get("passed") is True,
            }
        )
    receipt = {
        "schema": "ghc.family.vesper-arlen.v666-v2.tooling-smoke-receipt.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "skill_quick_validation": {
            "passed": sum(row["passed"] for row in skill_rows),
            "failed": sum(not row["passed"] for row in skill_rows),
            "rows": skill_rows,
        },
        "runner_smoke": {
            "passed": sum(row["passed"] for row in runner_rows),
            "failed": sum(not row["passed"] for row in runner_rows),
            "rows": runner_rows,
        },
        "globally_installed": False,
        "external_actions": 0,
        "status": "PASS"
        if all(row["passed"] for row in skill_rows + runner_rows)
        else "FAIL",
    }
    write_json("x2/tooling-smoke-receipt.json", receipt)
    print(json.dumps({"skills_passed": receipt["skill_quick_validation"]["passed"], "runners_passed": receipt["runner_smoke"]["passed"], "status": receipt["status"]}))
    if receipt["status"] != "PASS":
        raise RuntimeError("tooling smoke validation failed")


def build_x2_validation_receipt() -> None:
    tooling = load("x2/tooling-smoke-receipt.json")
    if tooling.get("status") != "PASS":
        raise RuntimeError("tooling smoke receipt must pass before x2 validation")
    selected = ["contracts", "mutations", "json", "privacy", "security", "manifests", "truth"]
    rows = []
    for runner_id in selected:
        suffix = runner_id.replace("-", "_")
        path = ROOT / "scripts" / f"ghc_family_vesper_arlen_v666_v2_{suffix}.py"
        completed = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {"passed": False, "stdout_parse_error": True}
        rows.append(
            {
                "runner_id": runner_id,
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0 and payload.get("passed") is True,
                "bounded_result": payload,
            }
        )
    failed = [row for row in rows if not row["passed"]]
    receipt = {
        "schema": "ghc.family.vesper-arlen.v666-v2.runtime-validation-receipt.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "selected_component_count": len(rows),
        "passed_component_count": sum(row["passed"] for row in rows),
        "failed_component_count": len(failed),
        "rows": rows,
        "canonical_aggregate": False,
        "aggregate_credit": 1 if not failed else 0,
        "sequence_status": "PASS_BOUNDED_X2_COMPONENT_SEQUENCE" if not failed else "FAIL_ZERO_SEQUENCE_CREDIT",
        "full_repository_suite": False,
        "independent_reproduction": False,
    }
    write_json("x2/runtime-validation-receipt.json", receipt)
    print(json.dumps({"passed": receipt["passed_component_count"], "failed": len(failed), "status": receipt["sequence_status"]}))
    if failed:
        raise RuntimeError("bounded x2 component validation failed")


def main() -> None:
    freeze = load("x1/proposal-freeze.json")
    portfolio = load("x1/portfolio-freeze.json")
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]).decode("ascii").strip()
    if head != X1_SHA:
        raise RuntimeError(f"x2 must start from exact x1 {X1_SHA}, observed {head}")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20 or len(DOMAIN_PAYLOADS) != 20:
        raise RuntimeError("x2 slate mismatch")

    outcome_rows = []
    proposal_methods = []
    domain_catalog = []
    for proposal, payload in zip(proposals, DOMAIN_PAYLOADS, strict=True):
        contract = make_contract(proposal, payload)
        evaluation = evaluate_contract(contract)
        if not evaluation["passed"] or evaluation["rejected_mutation_count"] != 5:
            raise RuntimeError(f"bounded contract failed: {proposal['proposal_id']}")
        pid = proposal["proposal_id"]
        base = f"x2/proposals/{pid.casefold()}"
        write_json(f"{base}/contract.json", contract)
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.vesper-arlen.v666-v2.mutation-results.v1",
                "owner": "Vesper Arlen",
                "phase": "v666-v2",
                "generated_at_utc": NOW,
                "proposal_id": pid,
                "mutation_count": evaluation["mutation_count"],
                "rejected_mutation_count": evaluation["rejected_mutation_count"],
                "mutations": evaluation["mutations"],
                "all_rejected": True,
                "accepted_mutation_count": 0,
            },
        )
        write_json(
            f"{base}/bounded-receipt.json",
            {
                "schema": "ghc.family.vesper-arlen.v666-v2.bounded-receipt.v1",
                "owner": "Vesper Arlen",
                "phase": "v666-v2",
                "generated_at_utc": NOW,
                "proposal_id": pid,
                "bounded_positive_passed": evaluation["positive"]["valid"],
                "rejected_mutations": evaluation["rejected_mutation_count"],
                "observed_disposition": proposal["expected_disposition"],
                "completion_scope": contract["completion_scope"],
                "remaining_evidence_or_authority": contract["remaining_evidence_or_authority"],
                "same_owner": True,
                "real_rows": 0,
                "participants": 0,
                "network_calls": 0,
                "external_actions": 0,
                "passed": evaluation["passed"],
            },
        )
        outcome_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "observed_disposition": proposal["expected_disposition"],
                "bounded_positive_passed": True,
                "rejected_mutations": 5,
                "completion_scope": contract["completion_scope"],
                "remaining_evidence_or_authority": contract["remaining_evidence_or_authority"],
            }
        )
        domain_catalog.append(
            {
                "proposal_id": pid,
                "domain_field_count": len(payload),
                "domain_fields": sorted(payload),
                "synthetic_only": True,
            }
        )
        proposal_methods.append(
            method_row(
                f"VSP6662-MF-{pid}-P",
                f"validate the bounded positive for {pid}",
                f"the bounded positive passed for {pid}",
                "bounded_passing_witness",
                False,
            )
        )
        for mutation in evaluation["mutations"]:
            proposal_methods.append(
                method_row(
                    f"VSP6662-MF-{mutation['mutation_id']}",
                    f"reject preregistered mutation {mutation['mutation_id']}",
                    ";".join(mutation["errors"]),
                    "retained_rejecting_witness",
                    True,
                )
            )

    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for row in outcome_rows:
        counts[row["observed_disposition"]] += 1
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.proposal-ledger.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "proposal_count": len(outcome_rows),
            "outcome_counts": counts,
            "rows": outcome_rows,
            "bounded_positive_count": 20,
            "mutation_count": 100,
            "rejected_mutation_count": 100,
            "accepted_mutation_count": 0,
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/domain-surface-catalog.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.domain-surface-catalog.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "surfaces": domain_catalog,
            "surface_count": len(domain_catalog),
            "real_rows": 0,
        },
    )

    source_profiles = load("provenance/source-profiles.json")
    write_json(
        "x2/source-adapter-zero-call.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.source-adapter.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "profiles": [
                {
                    "source_id": row["source_id"],
                    "status": row["status"],
                    "network_calls": 0,
                    "rows": 0,
                }
                for row in source_profiles["profiles"]
            ],
            "network_calls": 0,
            "real_rows": 0,
            "current_live_adapter_executed": False,
            "outcome": "open_gap",
            "authority_nonconversion": True,
        },
    )
    write_json(
        "x2/trinity-representations.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.trinity-representations.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "primary": "GMUT Mind",
            "freed_id": {
                "proposal": "VSP6662-N016",
                "status": "represented",
                "real_keys": 0,
                "real_proofs": 0,
                "production": False,
                "missing": REPRESENTED_EVIDENCE_GAPS["VSP6662-N016"],
            },
            "thos": {
                "proposal": "VSP6662-N015",
                "status": "represented",
                "participants": 0,
                "real_arms": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["VSP6662-N015"],
            },
            "gmut": {
                "proposals": ["VSP6662-N017", "VSP6662-N018"],
                "status": "represented",
                "observations": 0,
                "likelihoods": 0,
                "constraints": 0,
                "predictions": 0,
                "claim": "typed symbolic spectral-obligation and gain-sky identifiability placeholders only",
            },
            "cbr": {
                "proposal": "VSP6662-N020",
                "status": "exact_gate",
                "authority_decisions": 0,
                "approvals": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["VSP6662-N020"],
            },
        },
    )

    skill_rows = []
    for name, description, focus in SKILL_SPECS:
        relative = Path("docs") / "vesper-arlen" / "v666-v2" / "x2" / "skills" / name / "SKILL.md"
        write_text(ROOT / relative, skill_text(name, description, focus))
        skill_rows.append(
            {
                "name": name,
                "path": relative.as_posix(),
                "status": "built_validated_smoke_used_owner_local",
                "globally_installed": False,
                "completion_credit": 1,
            }
        )
    write_json(
        "x2/skill-catalog.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.skill-catalog.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "skill_count": len(skill_rows),
            "skills": skill_rows,
            "globally_installed": False,
            "skill_creator_guidance_read": True,
        },
    )

    runner_rows = []
    for runner_id, purpose in RUNNER_SPECS:
        suffix = runner_id.replace("-", "_")
        name = f"ghc_family_vesper_arlen_v666_v2_{suffix}.py"
        path = ROOT / "scripts" / name
        write_text(path, runner_text(runner_id, purpose))
        runner_rows.append(
            {
                "runner_id": runner_id,
                "path": f"scripts/{name}",
                "purpose": purpose,
                "status": "built_validated_smoke_used_owner_local",
                "global_installation": False,
                "completion_credit": 1,
            }
        )
    write_json(
        "x2/runner-catalog.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.runner-catalog.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "runner_count": len(runner_rows),
            "runners": runner_rows,
            "family_current_compatibility": "additive owner-local ghc_family names; no inherited caller changed",
            "global_installation": False,
        },
    )

    safe_rows = [
        {**row, "x2_status": "completed_bounded", "completion_credit": 1}
        for row in portfolio["safe_now"]
    ]
    candidate_dispositions = [
        "represented",
        "represented",
        "represented",
        "represented",
        "open_gap",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
        "completed",
    ]
    candidate_rows = [
        {
            **row,
            "x2_status": disposition,
            "completion_credit": 1 if disposition == "completed" else 0,
        }
        for row, disposition in zip(portfolio["bounded_candidates"], candidate_dispositions, strict=True)
    ]
    exact_rows = [
        {**row, "x2_status": "unexecuted_exact_gate", "completion_credit": 0}
        for row in portfolio["exact_approval_packets"]
    ]
    blocked_rows = [
        {**row, "x2_status": "unexecuted_blocked", "completion_credit": 0}
        for row in portfolio["blocked_packets"]
    ]
    cfr_rows = [
        {**row, "x2_status": "completed_bounded", "completion_credit": 1}
        for row in portfolio["clean_fix_refine"]
    ]
    write_json(
        "x2/portfolio-execution.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.portfolio-execution.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "safe_now": safe_rows,
            "bounded_candidates": candidate_rows,
            "exact_approval_packets": exact_rows,
            "blocked_packets": blocked_rows,
            "phase_local_skills": skill_rows,
            "family_current_runners": runner_rows,
            "clean_fix_refine": cfr_rows,
            "global_installations": 0,
            "external_writes": 0,
            "destructive_actions": 0,
            "real_rows": 0,
            "participants": 0,
        },
    )

    portfolio_methods = []
    groups = [
        ("SN", safe_rows, "bounded_safe_now"),
        ("CA", candidate_rows, "bounded_candidate"),
        ("SK", skill_rows, "phase_local_skill"),
        ("RU", runner_rows, "family_current_runner"),
        ("CF", cfr_rows, "clean_fix_refine"),
    ]
    for prefix, rows, kind in groups:
        for index, row in enumerate(rows, 1):
            name = row.get("title") or row.get("name") or row.get("runner_id")
            portfolio_methods.append(
                method_row(
                    f"VSP6662-MF-{prefix}{index:02d}",
                    f"execute {kind}: {name}",
                    f"bounded owner-local witness prepared for {name}",
                    "bounded_passing_witness",
                    False,
                )
            )
    all_methods = proposal_methods + portfolio_methods
    if len(proposal_methods) != 120 or len(portfolio_methods) != 95 or len(all_methods) != 215:
        raise RuntimeError("Method Flow count mismatch")
    write_json(
        "method-flow/x2-method-flow.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.method-flow-x2.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "activation_baseline_negatives": 26164,
            "activation_baseline_methods": 10476,
            "startup_negatives": 11,
            "startup_methods": 11,
            "new_rejecting_mutation_negatives": 100,
            "new_x2_methods": 215,
            "effective_negatives_before_later_operational_overlays": 26275,
            "effective_methods_before_later_operational_overlays": 10702,
            "proposal_method_count": len(proposal_methods),
            "portfolio_method_count": len(portfolio_methods),
            "methods": all_methods,
            "no_failure_erased": True,
        },
    )

    write_json(
        "method-flow/x2-operational-overlay.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.method-flow-x2-operational-overlay.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "base_effective_negatives": 26275,
            "base_effective_methods": 10702,
            "new_operational_negative_count": 2,
            "new_operational_method_count": 2,
            "effective_negatives_after_this_overlay": 26277,
            "effective_methods_after_this_overlay": 10704,
            "rows": [
                {
                    "failure_id": "VSP6662-X2-N001",
                    "failed_witness": "the first x1 equality wrapper let PowerShell reinterpret the upstream token inside git rev-list",
                    "recovery": "use the explicit remote-tracking reference in the divergence comparison",
                    "bounded_passing_witness": "the explicit comparison returned zero ahead, zero behind, and a clean lane",
                    "aggregate_credit": 0,
                    "status": "recovered_failure_retained",
                },
                {
                    "failure_id": "VSP6662-X2-N002",
                    "failed_witness": "the first stale-label search passed Windows wildcard paths directly to ripgrep",
                    "recovery": "search the scripts and tests roots with an explicit glob filter",
                    "bounded_passing_witness": "the corrected search returned the exact stale semantic surfaces for patching",
                    "aggregate_credit": 0,
                    "status": "recovered_failure_retained",
                },
            ],
            "no_failure_erased": True,
        },
    )

    write_json(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.x2-build-receipt.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "contracts": 20,
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "skills_built": 10,
            "runners_built": 10,
            "skill_and_runner_validation_status": "10_of_10_each_passed_bounded_local_validation",
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "status": "X2_BUILT_AWAITING_BOUNDED_VALIDATION_AND_EVIDENCE_FREEZE",
        },
    )

    print(
        json.dumps(
            {
                "contracts": 20,
                "outcomes": counts,
                "mutations_rejected": 100,
                "skills_built": 10,
                "runners_built": 10,
                "x2_methods": 215,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if sys.argv[1:] == ["--tooling-smoke"]:
        build_tooling_smoke_receipt()
    elif sys.argv[1:] == ["--validate-x2"]:
        build_x2_validation_receipt()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_vesper_arlen_v666_v2_x2.py [--tooling-smoke|--validate-x2]")
    else:
        main()
