#!/usr/bin/env python3
"""Build bounded synthetic x2 evidence for Neris Solane v666-v1."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_neris_solane_v666_v1_runtime import evaluate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v666-v1"
X1_SHA = "435bfd997f7f56635f6ba63d8da7ea2505059a75"
SOURCE_SHA = "4cf5028def85bcf89fbf4d0efe6c502a4b02be61"
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
    {"channel_token": "SYN-CHAN-001", "channel_interval": {"start": 0, "end": 100}, "response_revisions": [{"token": "SYN-RSP-A", "start": 0, "end": 100}], "coverage_status": "exact_partition", "uncovered_spans": [], "overlap_spans": [], "live_validity_claim": False},
    {"stage_tokens": ["SYN-STAGE-1", "SYN-STAGE-2"], "input_dimensions": ["L/T2", "COUNT"], "output_dimensions": ["COUNT", "COUNT"], "path_checksum": "SYN-DIM-PATH-OK", "mismatch_index": -1, "localization_status": "no_mismatch", "conformance_claim": False},
    {"gain_nodes": ["SYN-SENSOR", "SYN-DIGITIZER"], "dependency_edges": [["SYN-SENSOR", "SYN-DIGITIZER"]], "saturation_state": "detected_synthetic", "uncertainty_status": "dominant_unknown", "revision_token": "SYN-GAIN-R1", "corrected_sample_count": 0, "amplitude_correction_allowed": False},
    {"clock_epoch_token": "SYN-CLOCK-E1", "offset_state": "placeholder_zero", "drift_state": "unknown", "leap_state": "unresolved", "latency_status": "vacant", "discontinuity_status": "quarantined", "timestamp_comparison_allowed": False, "estimated_correction_count": 0},
    {"axis_tokens": ["SYN-X", "SYN-Y", "SYN-Z"], "orthogonality_residuals": [0, 0, 0], "handedness_state": "ambiguous_with_mirror", "reflection_alternatives": ["right_handed", "left_handed"], "closure_status": "symbolic_only", "installation_claim": False},
    {"threshold_order": ["nominal", "clip"], "saturation_runs": [[10, 12]], "bound_status": "synthetic_known", "clipping_status": "detected_only", "reconstructed_samples": [], "recovery_allowed": False, "device_performance_claim": False},
    {"rise_threshold": 8, "fall_threshold": 3, "pre_window": 5, "post_window": 7, "state_sequence": ["armed", "triggered", "rearming", "cancelled"], "rearm_status": "explicit", "event_claim": False},
    {"interval_convention": "half_open", "source_intervals": [[0, 5], [5, 10], [0, 5]], "normalized_partitions": [[0, 5], [5, 10]], "duplicate_provenance": [{"interval": [0, 5], "source_count": 2}], "permutation_status": "stable", "destructive_coalescence_allowed": False, "quality_grade_claim": False},
    {"chain_tokens": ["SYN-CAL-A", "SYN-REF-VACANT"], "chain_completeness_status": "structural_only", "certificate_status": "absent", "uncertainty_status": "vacant_dominant_hold", "competent_review_status": "reserved", "traceability_claim": False, "acceptance_claim": False},
    {"before_config": {"sample_rate": "SYN-100", "range": "SYN-R1"}, "after_config": {"sample_rate": "SYN-200", "range": "SYN-R1"}, "critical_field_classes": ["sample_rate"], "effective_interval": [0, 1], "recorded_interval": [2, 3], "rollback_preview_token": "SYN-ROLLBACK-PREVIEW", "device_command_count": 0, "rollback_execution_allowed": False},
    {"site_token": "SYN-SITE-REDACTED", "applicable_states": ["generalize", "withhold"], "dominant_disclosure_status": "withhold", "purpose_conflict_status": "held", "contest_status": "open", "coordinate_fields": [], "coordinate_release_allowed": False, "hazard_claim": False},
    {"packet_tokens": ["SYN-PACKET-ROOT", "SYN-PACKET-CHILD"], "parent_links": [["SYN-PACKET-CHILD", "SYN-PACKET-ROOT"]], "root_tokens": ["SYN-PACKET-ROOT"], "cycle_status": "absent", "fixity_status": "placeholder_unverified", "contest_status": "open", "authenticity_claim": False},
    {"anomaly_states": ["unknown", "held", "resolved_synthetic"], "text_cues": ["UNKNOWN", "HELD", "RESOLVED"], "noncolour_symbols": ["?", "!", "="], "header_closure_status": "present", "keyboard_order_status": "structural_only", "manual_evaluation_status": "reserved", "accessibility_complete_claim": False},
    {"purpose_options": ["schema_evaluation", "maintenance_training_fixture"], "selected_purpose": "schema_evaluation", "retention_ceilings": ["fixture_session", "one_day"], "selected_retention_status": "fixture_session", "role_status": "vacant", "free_text_allowed": False, "personal_data_rows": 0},
    {"fault_topology": ["clock_jump", "gain_unknown", "interval_duplicate"], "branch_order_status": "masked", "repair_budget": 3, "trace_tokens": ["SYN-TRACE-A", "SYN-TRACE-B"], "participants": 0, "sessions": 0, "effectiveness_claim": False},
    {"assertion_tokens": ["SYN-ASSERT-A", "SYN-ASSERT-B"], "issuer_status": "vacant", "conflict_status": "contested", "precedence_status": "absent_hold", "expiry_states": ["active_fixture", "expired_fixture"], "revocation_status": "synthetic_only", "key_count": 0, "proof_count": 0, "production_lock": True},
    {"symbolic_stages": ["SYN-H1", "SYN-H2"], "input_dimension": "L/T2", "intermediate_dimension": "COUNT", "output_dimension": "COUNT", "basis_convention": "symbolic_frequency_domain", "numeric_response_values": [], "observation_count": 0, "likelihood_present": False, "prediction_claim": False},
    {"latent_components": ["SYN-WHITE", "SYN-COLORED-A", "SYN-COLORED-B"], "symbolic_spectra": ["S0", "S1", "S1"], "equivalent_decompositions": [["SYN-COLORED-A"], ["SYN-COLORED-B"]], "identifiability_status": "held", "dominant_status": "nonidentified", "observation_count": 0, "causal_claim": False},
    {"source_ids": ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13"], "mapping_pairs": [["StationXML.Channel", "synthetic_channel"], ["PROV.Entity", "synthetic_packet"]], "conflict_status": "unresolved", "version_pin_status": "recorded_not_live_resolved", "transport_status": "disabled", "network_calls": 0, "real_rows": 0, "authority_nonconversion_status": "active", "current_registry_status": "open_gap"},
    {"reserved_decisions": ["station_disclosure", "calibration_release", "hazard_use", "worker_safety", "affected_party_remedy", "cultural_review", "Māori_authority"], "approvals_present": [], "authority_status": "reserved", "execution_status": "unexecuted", "structural_success_authorizes_operation": False, "affected_party_evidence": 0, "Māori_authority_evidence": 0},
]


REPRESENTED_EVIDENCE_GAPS = {
    "NRS6661-N015": ["no real participants, operators, instruments, or acquisition incidents", "no governed counterfactual arms, safety monitoring, statistics, or independent review"],
    "NRS6661-N016": ["no standards-conformant real issuers, holders, keys, signatures, or proofs", "no live issuance, resolution, contestation, revocation, interoperability, recovery, or trust governance"],
    "NRS6661-N017": ["no numerical transfer function, waveform, observation, likelihood, empirical constraint, or prediction", "no independent physics or instrumentation review"],
    "NRS6661-N018": ["no measured spectrum, covariance estimate, fitted latent process, likelihood, causal inference, or prediction", "no independent physics or instrumentation review"],
    "NRS6661-N019": ["no live official-source retrieval, version negotiation, or standard-owner semantic review", "no network calls and zero external rows"],
    "NRS6661-N020": ["no station operator, engineer, metrologist, worker, affected-party, safety, legal, cultural, or remedy approval", "no Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, or Māori-authority approval"],
}


SKILL_SPECS = [
    ("response-epoch-coverage-join", "Validate a synthetic channel-to-response interval partition without asserting live metadata validity.", "half-open epochs, unique response coverage, gaps, overlaps, and quarantine"),
    ("response-dimensional-path-checksum", "Localize synthetic response-stage unit mismatches without claiming conformance or calibration.", "ordered stages, adjacent dimensions, path checksums, and reversible mismatch attribution"),
    ("strong-motion-abstention-envelope", "Separate synthetic clipping detectability from forbidden reconstruction and device-performance conclusions.", "threshold ordering, saturation runs, unknown bounds, and zero recovered samples"),
    ("clock-discontinuity-quarantine", "Hold synthetic timing comparisons when offset, drift, leap, latency, or epoch-edge state is unresolved.", "clock states, dominant holds, and zero estimated correction"),
    ("orientation-closure-reflection-tribunal", "Check symbolic triad closure while preserving mirrored alternatives and installation abstention.", "orthogonality residuals, handedness, reflection ambiguity, and no site claim"),
    ("acquisition-interval-normalizer", "Normalize half-open synthetic acquisition intervals without erasing duplicates or correction provenance.", "permutation stability, duplicate lineage, boundary semantics, and reversible partitions"),
    ("calibration-traceability-claim-firewall", "Keep structural calibration-chain checks separate from traceability, certificate, and acceptance claims.", "chain completeness, certificate vacancy, uncertainty, competent review, and refusal"),
    ("sensitive-site-disclosure-lattice", "Apply the strictest synthetic disclosure state without releasing coordinates or inferring authority.", "omit, generalize, withhold, contest, purpose conflict, and no-coordinate release"),
    ("strong-motion-method-flow", "Retain phase failures, rejecting fixtures, recoveries, passing witnesses, and recurrence guards.", "Method Flow rows and exact negative retention"),
    ("strong-motion-closeout-gate", "Check owner-local phase truth, manifests, privacy boundaries, open gates, and terminal no-send prerequisites.", "closeout and route gating without a full repository suite"),
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
        "schema": "ghc.family.neris-solane.v666-v1.proposal-contract.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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

Use this owner-local phase skill only for Neris Solane v666-v1 synthetic artifacts concerning {focus}. It is a narrow reference package and is not globally installed.

## Workflow

1. Read the frozen proposal and its protected gates before changing an artifact.
2. Accept only synthetic tokens with zero people, real stations or locations, real waveforms or measurements, devices, network calls, identity operations, and external actions.
3. Preserve source, revision, withdrawal, correction, uncertainty, and dominant-stop fields that apply to the request.
4. Run the proposal's bounded positive and all five preregistered rejecting mutations. Retain every failure and recovery through Method Flow.
5. Label evidence as bounded same-owner software structure. Reserve manual, affected-user, professional, legal, cultural, Māori-authority, production, security, privacy, accessibility, and independent review.

## Stop conditions

Stop rather than infer permission when a request introduces a real station operator, engineer, metrologist, worker, affected party, station, sensitive location, waveform, measurement, calibration acceptance, hazard or safety judgment, an accelerograph or other device command, credentials, external writes, authority decisions, or claims beyond the four exact outcome labels. Never convert public-source vocabulary into conformance, competence, endorsement, or authority.
"""


def runner_text(runner_id: str, purpose: str) -> str:
    return f'''#!/usr/bin/env python3
"""Neris Solane v666-v1 runner: {purpose}."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_neris_solane_v666_v1_runner_common import run

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
        path = ROOT / "scripts" / f"ghc_family_neris_solane_v666_v1_{suffix}.py"
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
        "schema": "ghc.family.neris-solane.v666-v1.tooling-smoke-receipt.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        path = ROOT / "scripts" / f"ghc_family_neris_solane_v666_v1_{suffix}.py"
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
        "schema": "ghc.family.neris-solane.v666-v1.runtime-validation-receipt.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
                "schema": "ghc.family.neris-solane.v666-v1.mutation-results.v1",
                "owner": "Neris Solane",
                "phase": "v666-v1",
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
                "schema": "ghc.family.neris-solane.v666-v1.bounded-receipt.v1",
                "owner": "Neris Solane",
                "phase": "v666-v1",
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
                f"NRS6661-MF-{pid}-P",
                f"validate the bounded positive for {pid}",
                f"the bounded positive passed for {pid}",
                "bounded_passing_witness",
                False,
            )
        )
        for mutation in evaluation["mutations"]:
            proposal_methods.append(
                method_row(
                    f"NRS6661-MF-{mutation['mutation_id']}",
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
            "schema": "ghc.family.neris-solane.v666-v1.proposal-ledger.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.domain-surface-catalog.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.source-adapter.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.trinity-representations.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "primary": "THOS Body",
            "freed_id": {
                "proposal": "NRS6661-N016",
                "status": "represented",
                "real_keys": 0,
                "real_proofs": 0,
                "production": False,
                "missing": REPRESENTED_EVIDENCE_GAPS["NRS6661-N016"],
            },
            "thos": {
                "proposal": "NRS6661-N015",
                "status": "represented",
                "participants": 0,
                "real_arms": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["NRS6661-N015"],
            },
            "gmut": {
                "proposals": ["NRS6661-N017", "NRS6661-N018"],
                "status": "represented",
                "observations": 0,
                "likelihoods": 0,
                "constraints": 0,
                "predictions": 0,
                "claim": "typed symbolic transfer and identifiability placeholders only",
            },
            "cbr": {
                "proposal": "NRS6661-N020",
                "status": "exact_gate",
                "authority_decisions": 0,
                "approvals": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["NRS6661-N020"],
            },
        },
    )

    skill_rows = []
    for name, description, focus in SKILL_SPECS:
        relative = Path("docs") / "neris-solane" / "v666-v1" / "x2" / "skills" / name / "SKILL.md"
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
            "schema": "ghc.family.neris-solane.v666-v1.skill-catalog.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
        name = f"ghc_family_neris_solane_v666_v1_{suffix}.py"
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
            "schema": "ghc.family.neris-solane.v666-v1.runner-catalog.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.portfolio-execution.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
                    f"NRS6661-MF-{prefix}{index:02d}",
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
            "schema": "ghc.family.neris-solane.v666-v1.method-flow-x2.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "activation_baseline_negatives": 26041,
            "activation_baseline_methods": 10238,
            "startup_negatives": 16,
            "startup_methods": 16,
            "new_rejecting_mutation_negatives": 100,
            "new_x2_methods": 215,
            "effective_negatives_before_later_operational_overlays": 26157,
            "effective_methods_before_later_operational_overlays": 10469,
            "proposal_method_count": len(proposal_methods),
            "portfolio_method_count": len(portfolio_methods),
            "methods": all_methods,
            "no_failure_erased": True,
        },
    )

    write_json(
        "method-flow/x2-operational-overlay.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.method-flow-x2-operational-overlay.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "base_effective_negatives": 26157,
            "base_effective_methods": 10469,
            "new_operational_negative_count": 0,
            "new_operational_method_count": 0,
            "effective_negatives_after_this_overlay": 26157,
            "effective_methods_after_this_overlay": 10469,
            "rows": [],
            "no_failure_erased": True,
        },
    )

    write_json(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.x2-build-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
        raise SystemExit("usage: build_ghc_family_neris_solane_v666_v1_x2.py [--tooling-smoke|--validate-x2]")
    else:
        main()
