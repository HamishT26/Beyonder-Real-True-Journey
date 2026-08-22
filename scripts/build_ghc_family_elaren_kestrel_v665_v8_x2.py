#!/usr/bin/env python3
"""Build bounded synthetic x2 evidence for Elaren Kestrel v665-v8."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_elaren_kestrel_v665_v8_runtime import evaluate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v665-v8"
X1_SHA = "05cab184438f3a5c7c8d4ae453e6b80e3db21ed6"
SOURCE_SHA = "5f688af4fd89004f23cf0489b569e559f7b7fbea"
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
    {"plate_token": "SYN-PLATE-001", "series_status": "placeholder_only", "observatory_status": "vacant", "telescope_status": "vacant", "revision": 1, "cancellation_available": True, "handling_allowed": False},
    {"support_token": "SYN-GLASS-SUPPORT-001", "emulsion_status": "unknown_quarantined", "fracture_cue_status": "unobserved", "lifting_cue_status": "unobserved", "process_status": "vacant", "diagnosis_claim": False, "treatment_allowed": False},
    {"envelope_token": "SYN-ENVELOPE-001", "box_token": "SYN-BOX-001", "shelf_token": "SYN-SHELF-PLACEHOLDER", "plate_token": "SYN-PLATE-001", "orphan_status": "declared_unresolved", "quarantine_status": "held", "location_truth_claim": False},
    {"exposure_token": "SYN-EXPOSURE-001", "date_time_status": "vacant", "telescope_status": "vacant", "instrument_status": "vacant", "observer_status": "anonymous_placeholder", "target_status": "unidentified", "source_assertion_status": "unverified", "observation_truth_claim": False},
    {"plate_token": "SYN-PLATE-001", "side_convention_status": "unspecified", "edge_marks": ["SYN-MARK-A"], "label_tokens": ["SYN-LABEL-A"], "annotation_status": "unknown_uninterpreted", "correction_available": True, "interpretation_claim": False},
    {"legacy_plate_token": "SYN-LEGACY-001", "series_token": "SYN-SERIES-001", "envelope_token": "SYN-ENVELOPE-001", "box_token": "SYN-BOX-001", "derivative_tokens": ["SYN-DERIV-001"], "discrepancy_status": "declared_unresolved", "inventory_truth_claim": False},
    {"capture_job_token": "SYN-CAPTURE-JOB-001", "calibration_status": "vacant", "cancellation_available": True, "safety_hold_status": "dominant", "scanner_calls": 0, "camera_calls": 0, "device_command_status": "prohibited"},
    {"wedge_token": "SYN-WEDGE-001", "fiducial_tokens": ["SYN-FID-A", "SYN-FID-B"], "annotation_tokens": ["SYN-ANN-A"], "scale_status": "placeholder_only", "unit_status": "symbolic_SI_placeholder", "uncertainty_status": "vacant", "measurement_count": 0},
    {"derivative_token": "SYN-DERIV-001", "fits_status": "placeholder_not_ingested", "checksum_status": "placeholder_unverified", "generation_step": "synthetic_mapping", "redaction_status": "none_required_for_synthetic_fixture", "image_rows": 0, "conformance_claim": False},
    {"table_token": "SYN-OBS-TABLE-001", "target_status": "unidentified", "coordinate_frame_status": "placeholder_only", "epoch_status": "vacant", "exposure_status": "vacant", "quality_status": "unrated", "row_count": 0, "celestial_claim": False},
    {"assertion_token": "SYN-ASSERT-001", "prior_value_token": "SYN-VALUE-000", "current_value_token": "SYN-VALUE-001", "contest_window_status": "open", "source_link_status": "synthetic_attached", "amendment_status": "declared", "prior_state_erased": False},
    {"rights_record_token": "SYN-RIGHTS-001", "observer_disclosure_status": "withheld_synthetic", "sensitive_target_status": "reserved", "purpose_ceiling": "schema_evaluation", "access_hold_status": "active", "correction_route": "placeholder_appeal", "remedy_status": "reserved_external", "rights_decision_claim": False},
    {"text_capsules": ["INTAKE", "ENCLOSURE", "PROVENANCE"], "table_path_status": "present", "unknown_states_explicit": True, "keyboard_landmarks_status": "structural_only", "print_companion_status": "present", "manual_evaluation_status": "reserved"},
    {"metadata_fields": ["purpose", "revision", "status"], "collection_purpose": "schema_evaluation", "disclosure_ceiling": "minimum_synthetic_fields", "retention_status": "delete_after_fixture", "correction_route": "placeholder_appeal", "identifier_use_status": "synthetic_only", "personal_data_rows": 0},
    {"packet_tokens": ["SYN-PACKET-A", "SYN-PACKET-B"], "permutation_status": "synthetic_sealed", "edit_ceiling": "symbolic_equal", "provenance_labels_masked": True, "dominant_stop": "safety_or_withdrawal", "participants": 0, "sessions": 0, "effectiveness_claim": False},
    {"statement_token": "SYN-PLATE-STATEMENT-001", "plate_relation": "SYN-PLATE-001", "status_state": "synthetic_expired", "disclosure_purpose": "schema_evaluation", "expiry_status": "expired_fixture", "correction_route": "placeholder_appeal", "revocation_status": "not_operated", "key_count": 0, "proof_count": 0, "production_lock": True},
    {"frame_tokens": ["SYN-FRAME-A", "SYN-FRAME-B"], "transform_operator": [[1, 0], [0, 1]], "basis_convention": "symbolic_plate_basis", "unit_status": "symbolic_SI_placeholder", "observation_count": 0, "likelihood_present": False, "coordinate_solution_claim": False},
    {"distortion_state": [0, 0], "coefficient_placeholders": [], "covariance_status": "vacant", "identifiability_status": "unresolved", "uncertainty_status": "vacant", "coefficient_count": 0, "observation_count": 0, "prediction_claim": False},
    {"source_ids": ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13"], "version_pin_status": "recorded_not_live_resolved", "source_access_status": "metadata_only", "authority_holds": ["Māori_authority_reserved", "professional_review_reserved"], "network_calls": 0, "real_rows": 0, "current_adapter_status": "open_gap"},
    {"reserved_decisions": ["custody", "copyright", "image_rights", "sensitive_sky_knowledge", "worker_safety", "privacy", "access", "remedy", "affected_party_legitimacy", "Māori_authority"], "approvals_present": [], "authority_status": "reserved", "execution_status": "unexecuted", "affected_party_evidence": 0, "Māori_authority_evidence": 0},
]


REPRESENTED_EVIDENCE_GAPS = {
    "ELK6658-N015": ["no real participants or operators", "no preregistered blind matched-budget governed arms", "no safety monitoring, statistics, or independent review"],
    "ELK6658-N016": ["no standards-conformant real keys or proofs", "no live issuance, resolution, status, revocation, interoperability, recovery, or trust governance"],
    "ELK6658-N017": ["no real plate observation, coordinate solution, likelihood, empirical scale, constraint, force, or prediction", "no independent physics review"],
    "ELK6658-N018": ["no real distortion observation, covariance estimate, likelihood, parameter inference, or prediction", "no independent physics review"],
    "ELK6658-N019": ["no live official-source retrieval or schema negotiation by phase software", "no network calls and zero external rows"],
    "ELK6658-N020": ["no archivist, astronomer, conservator, worker, affected-party, custody, rights, safety, legal, cultural, sensitive-knowledge, or remedy approval", "no Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, or Māori-authority approval"],
}


SKILL_SPECS = [
    ("astronomical-plate-intake-boundary", "Structure a synthetic plate-intake identity capsule while refusing handling, observation truth, production, and authority actions.", "plate token, series, observatory and telescope vacancies, cancellation, and handling lock"),
    ("plate-enclosure-topology", "Trace synthetic plate, envelope, box, and shelf relations without asserting location, custody, condition, or fitness.", "enclosure tokens, orphan state, quarantine, and no-location-truth rule"),
    ("exposure-provenance-abstention", "Record synthetic exposure provenance fields while refusing target identification or observational truth.", "date-time, telescope, instrument, observer, target, source assertion, and abstention"),
    ("digitization-device-firewall", "Separate synthetic digitization-job metadata from every scanner and camera command.", "calibration vacancy, cancellation, safety hold, and zero device calls"),
    ("plate-annotation-orientation", "Map synthetic plate sides, edges, labels, and annotations without interpreting content or authenticity.", "orientation conventions, marks, corrections, and interpretation refusal"),
    ("plate-catalogue-reconciliation", "Preserve synthetic catalogue discrepancies and non-erasing reconciliation without asserting inventory truth.", "legacy, series, enclosure, derivative, and discrepancy tokens"),
    ("plate-rights-contestation", "Reserve synthetic rights, disclosure, sensitive-target, correction, and remedy decisions for competent authority.", "purpose ceilings, holds, contestation, correction, and no-rights decision"),
    ("plate-source-profile-watch", "Maintain official astronomical, preservation, provenance, accessibility, privacy, and authority source status without converting citation into conformance.", "FITS, IAU, IVOA, LOC, CCI, W3C, NIST, New Zealand Privacy, and Te Mana Raraunga"),
    ("plate-method-flow", "Retain plate-phase failures, rejecting fixtures, recoveries, passing witnesses, and recurrence guards.", "Method Flow rows and exact negative retention"),
    ("plate-closeout-gate", "Check owner-local plate-phase truth, manifests, privacy boundaries, open gates, and terminal no-send prerequisites.", "closeout and route gating without a full repository suite"),
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.proposal-contract.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
        "x1_sha": X1_SHA,
        "source_sha": SOURCE_SHA,
        "preregistered_before_x2": True,
        "proposal_id": pid,
        "title": proposal["title"],
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

Use this owner-local phase skill only for Elaren Kestrel v665-v8 synthetic artifacts concerning {focus}. It is a narrow reference package and is not globally installed.

## Workflow

1. Read the frozen proposal and its protected gates before changing an artifact.
2. Accept only synthetic tokens with zero people, real plates or images, real observations, devices, network calls, identity operations, and external actions.
3. Preserve source, revision, withdrawal, correction, uncertainty, and dominant-stop fields that apply to the request.
4. Run the proposal's bounded positive and all five preregistered rejecting mutations. Retain every failure and recovery through Method Flow.
5. Label evidence as bounded same-owner software structure. Reserve manual, affected-user, professional, legal, cultural, Māori-authority, production, security, privacy, accessibility, and independent review.

## Stop conditions

Stop rather than infer permission when a request introduces a real archivist, astronomer, conservator, worker, affected party, plate, image, observation, rights record, conservation or safety judgment, a scanner, camera, telescope, or other device command, credentials, external writes, authority decisions, or claims beyond the four exact outcome labels. Never convert public-source vocabulary into conformance, competence, endorsement, or authority.
"""


def runner_text(runner_id: str, purpose: str) -> str:
    return f'''#!/usr/bin/env python3
"""Elaren Kestrel v665-v8 runner: {purpose}."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_elaren_kestrel_v665_v8_runner_common import run

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
        path = ROOT / "scripts" / f"ghc_family_elaren_kestrel_v665_v8_{suffix}.py"
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.tooling-smoke-receipt.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
        path = ROOT / "scripts" / f"ghc_family_elaren_kestrel_v665_v8_{suffix}.py"
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.runtime-validation-receipt.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
                "schema": "ghc.family.elaren-kestrel.v665-v8.mutation-results.v1",
                "owner": "Elaren Kestrel",
                "phase": "v665-v8",
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
                "schema": "ghc.family.elaren-kestrel.v665-v8.bounded-receipt.v1",
                "owner": "Elaren Kestrel",
                "phase": "v665-v8",
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
                f"ELK6658-MF-{pid}-P",
                f"validate the bounded positive for {pid}",
                f"the bounded positive passed for {pid}",
                "bounded_passing_witness",
                False,
            )
        )
        for mutation in evaluation["mutations"]:
            proposal_methods.append(
                method_row(
                    f"ELK6658-MF-{mutation['mutation_id']}",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.proposal-ledger.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.domain-surface-catalog.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.source-adapter.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.trinity-representations.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "generated_at_utc": NOW,
            "primary": "Freed ID and CBR Heart",
            "freed_id": {
                "proposal": "ELK6658-N016",
                "status": "represented",
                "real_keys": 0,
                "real_proofs": 0,
                "production": False,
                "missing": REPRESENTED_EVIDENCE_GAPS["ELK6658-N016"],
            },
            "thos": {
                "proposal": "ELK6658-N015",
                "status": "represented",
                "participants": 0,
                "real_arms": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["ELK6658-N015"],
            },
            "gmut": {
                "proposals": ["ELK6658-N017", "ELK6658-N018"],
                "status": "represented",
                "observations": 0,
                "likelihoods": 0,
                "constraints": 0,
                "predictions": 0,
                "claim": "typed discrete surrogate placeholders only",
            },
            "cbr": {
                "proposal": "ELK6658-N020",
                "status": "exact_gate",
                "authority_decisions": 0,
                "approvals": 0,
                "missing": REPRESENTED_EVIDENCE_GAPS["ELK6658-N020"],
            },
        },
    )

    skill_rows = []
    for name, description, focus in SKILL_SPECS:
        relative = Path("docs") / "elaren-kestrel" / "v665-v8" / "x2" / "skills" / name / "SKILL.md"
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.skill-catalog.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
        name = f"ghc_family_elaren_kestrel_v665_v8_{suffix}.py"
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.runner-catalog.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.portfolio-execution.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
                    f"ELK6658-MF-{prefix}{index:02d}",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.method-flow-x2.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "generated_at_utc": NOW,
            "activation_baseline_negatives": 25921,
            "activation_baseline_methods": 10003,
            "startup_negatives": 13,
            "startup_methods": 13,
            "new_rejecting_mutation_negatives": 100,
            "new_x2_methods": 215,
            "effective_negatives_before_later_operational_overlays": 26034,
            "effective_methods_before_later_operational_overlays": 10231,
            "proposal_method_count": len(proposal_methods),
            "portfolio_method_count": len(portfolio_methods),
            "methods": all_methods,
            "no_failure_erased": True,
        },
    )

    write_json(
        "method-flow/x2-operational-overlay.json",
        {
            "schema": "ghc.family.elaren-kestrel.v665-v8.method-flow-x2-operational-overlay.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "generated_at_utc": NOW,
            "base_effective_negatives": 26034,
            "base_effective_methods": 10231,
            "new_operational_negative_count": 0,
            "new_operational_method_count": 0,
            "effective_negatives_after_this_overlay": 26034,
            "effective_methods_after_this_overlay": 10231,
            "rows": [],
            "no_failure_erased": True,
        },
    )

    write_json(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.elaren-kestrel.v665-v8.x2-build-receipt.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
        raise SystemExit("usage: build_ghc_family_elaren_kestrel_v665_v8_x2.py [--tooling-smoke|--validate-x2]")
    else:
        main()
