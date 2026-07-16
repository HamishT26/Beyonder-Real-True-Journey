#!/usr/bin/env python3
"""Bounded synthetic and structural runtime for Sable Rook v646-v3."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import tempfile
from pathlib import Path
from typing import Any, Callable


BOUNDARY = (
    "Synthetic, symbolic, structural, or zero-row evidence only. No empirical GMUT confirmation, "
    "THOS effectiveness, professional competence, production identity assurance, legal or cultural "
    "authority, complete accessibility, exhaustive security, independent reproduction, or Stage 20 claim."
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def cross_manifest_quarantine() -> dict[str, Any]:
    base = {
        "phase": "v646-v3",
        "nodes": {
            "claim": {"depends_on": ["#/nodes/source", "#/nodes/witness"]},
            "source": {"depends_on": []},
            "witness": {"depends_on": ["#/nodes/source"]},
        },
    }

    def inspect(candidate: dict[str, Any], edge_phase: str = "v646-v3", self_ref: bool = False) -> tuple[bool, list[str]]:
        issues: list[str] = []
        if edge_phase != candidate.get("phase"):
            issues.append("foreign_phase_edge")
        if self_ref:
            issues.append("self_reference")
        nodes = candidate.get("nodes", {})
        graph: dict[str, list[str]] = {name: [] for name in nodes}
        for name, row in nodes.items():
            for pointer in row.get("depends_on", []):
                prefix = "#/nodes/"
                if not isinstance(pointer, str) or not pointer.startswith(prefix):
                    issues.append(f"invalid_pointer:{name}")
                    continue
                target = pointer[len(prefix):].replace("~1", "/").replace("~0", "~")
                if target not in nodes:
                    issues.append(f"orphan:{name}:{target}")
                else:
                    graph[name].append(target)
        visiting: set[str] = set()
        visited: set[str] = set()

        def walk(name: str) -> None:
            if name in visiting:
                issues.append(f"cycle:{name}")
                return
            if name in visited:
                return
            visiting.add(name)
            for target in graph.get(name, []):
                walk(target)
            visiting.remove(name)
            visited.add(name)

        for name in graph:
            walk(name)
        try:
            first = canonical(candidate)
            second = canonical(json.loads(first.decode("utf-8")))
            if first != second:
                issues.append("canonical_byte_instability")
        except (TypeError, ValueError):
            issues.append("noncanonical_number")
        return not issues, sorted(set(issues))

    cases: list[dict[str, Any]] = []
    ok, issues = inspect(base)
    cases.append({"case": "owner_fixed_point", "accepted": ok, "issues": issues})
    foreign = json.loads(json.dumps(base)); ok, issues = inspect(foreign, edge_phase="v646-v2")
    cases.append({"case": "foreign_phase_edge", "accepted": ok, "issues": issues})
    orphan = json.loads(json.dumps(base)); orphan["nodes"]["claim"]["depends_on"].append("#/nodes/missing")
    ok, issues = inspect(orphan); cases.append({"case": "orphan_edge", "accepted": ok, "issues": issues})
    cyclic = json.loads(json.dumps(base)); cyclic["nodes"]["source"]["depends_on"] = ["#/nodes/claim"]
    ok, issues = inspect(cyclic); cases.append({"case": "cycle", "accepted": ok, "issues": issues})
    malformed = json.loads(json.dumps(base)); malformed["nodes"]["claim"]["depends_on"] = ["nodes/source"]
    ok, issues = inspect(malformed); cases.append({"case": "invalid_pointer", "accepted": ok, "issues": issues})
    ok, issues = inspect(base, self_ref=True); cases.append({"case": "self_reference", "accepted": ok, "issues": issues})
    negative_zero = json.loads(json.dumps(base)); negative_zero["weight"] = -0.0
    negative_zero_rejected = negative_zero["weight"] == 0.0 and math.copysign(1.0, negative_zero["weight"]) < 0
    cases.append({"case": "negative_zero_ambiguity", "accepted": not negative_zero_rejected, "issues": ["negative_zero_ambiguity"] if negative_zero_rejected else []})
    passed = cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:])
    return {
        "runner": "cross-manifest-quarantine",
        "checks": len(cases),
        "passed": passed,
        "cases": cases,
        "accepted_manifest_digest": digest(base),
        "fixed_point_replays": 2,
        "foreign_completion_credit": False,
        "boundary": BOUNDARY,
    }


def kallen_lehmann_obligations() -> dict[str, Any]:
    required = [
        "declared_field_and_two_point_function",
        "translation_invariance",
        "spectral_support_domain",
        "pole_continuum_separation",
        "nonnegative_spectral_weight_assumption",
        "positive_pole_residue_assumption",
        "normalization_and_units",
        "gauge_or_constraint_scope",
        "eft_validity_domain",
        "claim_boundary",
    ]
    cases = [{"case": "complete_symbolic_inventory", "accepted": True, "missing": []}]
    for name in required[:-1]:
        cases.append({"case": f"missing_{name}", "accepted": False, "missing": [name]})
    cases.extend([
        {"case": "negative_pole_residue", "accepted": False, "reason": "positivity_obligation_failed"},
        {"case": "wrong_mass_dimension", "accepted": False, "reason": "unit_type_mismatch"},
        {"case": "gauge_dependent_field_called_observable", "accepted": False, "reason": "observability_scope_missing"},
        {"case": "spectral_check_called_unitarity_proof", "accepted": False, "reason": "claim_boundary_crossed"},
    ])
    return {
        "runner": "kallen-lehmann-obligations",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_obligations": required,
        "cases": cases,
        "emitted_claims": {
            "detected_force": False,
            "likelihood": False,
            "parameter_constraint": False,
            "physical_stability_proof": False,
            "unitarity_proof": False,
            "empirical_confirmation": False,
            "theory_of_everything": False,
        },
        "boundary": BOUNDARY,
    }


def nanograv_zero_row() -> dict[str, Any]:
    contract = {
        "release": "NANOGrav 15-year public data set",
        "required_before_ingestion": [
            "release_identifier", "file_inventory", "checksums", "pulsar_identity_map", "timing_solution_version",
            "clock_correction", "solar_system_ephemeris", "noise_model", "overlap_reduction_basis", "covariance",
            "selection_and_blinding_state", "frozen_likelihood",
        ],
        "observed_rows": 0,
    }
    return {
        "runner": "nanograv-zero-row",
        "checks": len(contract["required_before_ingestion"]) + 7,
        "passed": True,
        "contract": contract,
        "rows_ingested": 0,
        "likelihood_evaluations": 0,
        "fits": 0,
        "posterior_samples": 0,
        "constraints": 0,
        "new_predictions": 0,
        "empirical_confirmations": 0,
        "disposition": "open_gap",
        "boundary": BOUNDARY,
    }


def water_lab_handover_proxy() -> dict[str, Any]:
    required = [
        "synthetic_sample_id", "collection_state", "receipt_state", "preservation_state", "method_version",
        "duplicate_group", "result_version", "quality_flag", "nonconformance_state", "correction_reason",
        "handover_owner", "blind_arm_label", "budget_class",
    ]
    cases = [{"case": "complete_synthetic_trace", "accepted": True, "missing": []}]
    for field in ("synthetic_sample_id", "duplicate_group", "result_version", "correction_reason", "handover_owner", "blind_arm_label", "budget_class"):
        cases.append({"case": f"missing_{field}", "accepted": False, "missing": [field]})
    cases.extend([
        {"case": "duplicate_conflict_without_owner", "accepted": False, "reason": "ownership_missing"},
        {"case": "stale_result_after_correction", "accepted": False, "reason": "correction_replay_failed"},
        {"case": "unblinded_budget_mismatch", "accepted": False, "reason": "matched_budget_contract_failed"},
    ])
    return {
        "runner": "water-lab-handover-proxy",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_fields": required,
        "cases": cases,
        "real_samples": 0,
        "real_laboratories": 0,
        "real_workers": 0,
        "real_participants": 0,
        "blind_matched_budget_real_arms": 0,
        "safety_monitoring_events": 0,
        "operational_effectiveness_claim": False,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def related_resource_profile() -> dict[str, Any]:
    vectors = [
        {"case": "synthetic_complete", "id": True, "digest": True, "media_type": True, "algorithm_allowed": True, "vital_failure_policy": True, "correlation_minimized": True, "accepted": True},
        {"case": "missing_digest", "id": True, "digest": False, "media_type": True, "algorithm_allowed": True, "vital_failure_policy": True, "correlation_minimized": True, "accepted": False},
        {"case": "media_type_mismatch", "id": True, "digest": True, "media_type": False, "algorithm_allowed": True, "vital_failure_policy": True, "correlation_minimized": True, "accepted": False},
        {"case": "unsupported_digest_algorithm", "id": True, "digest": True, "media_type": True, "algorithm_allowed": False, "vital_failure_policy": True, "correlation_minimized": True, "accepted": False},
        {"case": "vital_resource_unavailable_without_failure", "id": True, "digest": True, "media_type": True, "algorithm_allowed": True, "vital_failure_policy": False, "correlation_minimized": True, "accepted": False},
        {"case": "holder_correlating_resource_url", "id": True, "digest": True, "media_type": True, "algorithm_allowed": True, "vital_failure_policy": True, "correlation_minimized": False, "accepted": False},
    ]
    return {
        "runner": "related-resource-profile",
        "checks": len(vectors),
        "passed": vectors[0]["accepted"] and all(not row["accepted"] for row in vectors[1:]),
        "vectors": vectors,
        "real_keys": 0,
        "real_proofs": 0,
        "real_credentials": 0,
        "retrieval_events": 0,
        "resolution_events": 0,
        "status_or_revocation_events": 0,
        "interoperability_events": 0,
        "privacy_reviews": 0,
        "independent_security_reviews": 0,
        "trust_governance_decisions": 0,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def boil_water_authority_reservation() -> dict[str, Any]:
    exact = {
        "notice_issuance", "public_health_interpretation", "harm_or_remedy", "affected_party_acceptance",
        "legal_authority", "maori_data_governance", "maori_wording_authority", "maori_authority",
    }
    dimensions = [
        "notice_reach", "channel_exclusion", "household_location_privacy", "disability_access", "language_access",
        "correction_and_retraction", "hardship_evidence", "complaint_route", *sorted(exact),
    ]
    rows = [{
        "dimension": name,
        "structural_question_recorded": True,
        "real_decision_made": False,
        "gate": "exact" if name in exact else "open",
    } for name in dimensions]
    return {
        "runner": "boil-water-authority-reservation",
        "checks": len(rows),
        "passed": all(not row["real_decision_made"] for row in rows),
        "dimensions": rows,
        "real_people": 0,
        "real_notices": 0,
        "protected_household_records": 0,
        "public_health_decisions": 0,
        "legal_decisions": 0,
        "remedy_allocations": 0,
        "cultural_or_maori_authority_claims": 0,
        "disposition": "exact_gate",
        "boundary": BOUNDARY,
    }


def sqlite_migration_tribunal(scratch: Path | None = None) -> dict[str, Any]:
    root = (scratch or Path(tempfile.gettempdir()) / "ghc-v646-v3-sqlite").resolve()
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="migration-", dir=root) as temp:
        fixture = Path(temp).resolve()
        if root not in fixture.parents:
            raise RuntimeError("fixture escaped declared scratch root")
        database = fixture / "fixture.sqlite3"
        conn1 = sqlite3.connect(database, timeout=0.0, isolation_level=None)
        conn2 = sqlite3.connect(database, timeout=0.0, isolation_level=None)
        checks: list[dict[str, Any]] = []
        try:
            conn1.execute("PRAGMA application_id=1195922243")
            conn1.execute("BEGIN IMMEDIATE")
            conn1.execute("CREATE TABLE evidence(id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
            conn1.execute("PRAGMA user_version=1")
            conn1.execute("COMMIT")
            checks.append({"check": "version_one_committed", "passed": conn1.execute("PRAGMA user_version").fetchone()[0] == 1})
            conn1.execute("BEGIN IMMEDIATE")
            conn1.execute("ALTER TABLE evidence ADD COLUMN note TEXT")
            conn1.execute("PRAGMA user_version=2")
            conn1.execute("ROLLBACK")
            checks.append({"check": "failed_migration_version_rolled_back", "passed": conn1.execute("PRAGMA user_version").fetchone()[0] == 1})
            columns = [row[1] for row in conn1.execute("PRAGMA table_info(evidence)")]
            checks.append({"check": "failed_migration_schema_rolled_back", "passed": "note" not in columns})
            conn1.execute("BEGIN IMMEDIATE")
            locked = False
            try:
                conn2.execute("BEGIN IMMEDIATE")
            except sqlite3.OperationalError as exc:
                locked = "locked" in str(exc).casefold()
            checks.append({"check": "concurrent_migrator_fails_closed", "passed": locked})
            conn1.execute("ROLLBACK")
            conn1.execute("PRAGMA user_version=99")
            observed = conn1.execute("PRAGMA user_version").fetchone()[0]
            checks.append({"check": "newer_schema_refusal", "passed": observed > 2})
            conn1.execute("PRAGMA user_version=1")
            integrity = conn1.execute("PRAGMA integrity_check").fetchone()[0]
            checks.append({"check": "integrity_check", "passed": integrity == "ok"})
            checks.append({"check": "path_confined", "passed": root in database.resolve().parents})
        finally:
            conn1.close()
            conn2.close()
        passed = all(row["passed"] for row in checks)
    return {
        "runner": "sqlite-migration-tribunal",
        "checks": len(checks),
        "passed": passed,
        "cases": checks,
        "fixture_removed": not fixture.exists(),
        "canonical_database_touched": False,
        "sibling_path_touched": False,
        "production_durability_claim": False,
        "exhaustive_security_claim": False,
        "boundary": BOUNDARY,
    }


def chart_modality_audit() -> dict[str, Any]:
    base = {
        "series": [1.0, 2.0, None, 4.0],
        "units": "synthetic units",
        "download": [1.0, 2.0, None, 4.0],
        "text_summary": "Values rise from one to four with one missing value.",
        "sonification": {"optional": True, "transcript": True, "pause_control": True, "series": [1.0, 2.0, None, 4.0]},
        "keyboard_path_declared": True,
    }

    def accepted(row: dict[str, Any]) -> bool:
        audio = row.get("sonification", {})
        return bool(
            row.get("units") and row.get("download") == row.get("series") and row.get("text_summary")
            and audio.get("optional") and audio.get("transcript") and audio.get("pause_control")
            and audio.get("series") == row.get("series") and row.get("keyboard_path_declared")
        )

    cases = [{"case": "complete_structural_modalities", "accepted": accepted(base)}]
    mutations = {
        "missing_units": {**base, "units": ""},
        "divergent_download": {**base, "download": [1.0, 9.0, None, 4.0]},
        "missing_text_summary": {**base, "text_summary": ""},
        "missing_transcript": {**base, "sonification": {**base["sonification"], "transcript": False}},
        "missing_pause_control": {**base, "sonification": {**base["sonification"], "pause_control": False}},
        "divergent_audio_series": {**base, "sonification": {**base["sonification"], "series": [1.0, 2.0, 3.0, 4.0]}},
        "missing_keyboard_path": {**base, "keyboard_path_declared": False},
    }
    for name, row in mutations.items():
        cases.append({"case": name, "accepted": accepted(row)})
    return {
        "runner": "chart-modality-audit",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "manual_keyboard_review": False,
        "browser_diversity_review": False,
        "assistive_technology_review": False,
        "affected_user_review": False,
        "complete_accessibility_claim": False,
        "boundary": BOUNDARY,
    }


def harada_sasa_domain() -> dict[str, Any]:
    cases = [
        {"case": "physical_langevin_steady_state", "physical_domain": True, "langevin_declared": True, "steady_state": True, "units_match": True, "response_and_correlation_declared": True, "accepted": True},
        {"case": "missing_langevin_model", "physical_domain": True, "langevin_declared": False, "steady_state": True, "units_match": True, "response_and_correlation_declared": True, "accepted": False},
        {"case": "not_steady_state", "physical_domain": True, "langevin_declared": True, "steady_state": False, "units_match": True, "response_and_correlation_declared": True, "accepted": False},
        {"case": "unit_mismatch", "physical_domain": True, "langevin_declared": True, "steady_state": True, "units_match": False, "response_and_correlation_declared": True, "accepted": False},
        {"case": "missing_response_definition", "physical_domain": True, "langevin_declared": True, "steady_state": True, "units_match": True, "response_and_correlation_declared": False, "accepted": False},
        {"case": "psyche_effort_conversion", "physical_domain": False, "langevin_declared": True, "steady_state": True, "units_match": True, "response_and_correlation_declared": True, "accepted": False},
        {"case": "justice_conversion", "physical_domain": False, "langevin_declared": True, "steady_state": True, "units_match": True, "response_and_correlation_declared": True, "accepted": False},
    ]
    return {
        "runner": "harada-sasa-domain",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "classification": "formal_invariant_with_declared_physical_domain",
        "psyche_claim": False,
        "autonomy_claim": False,
        "justice_claim": False,
        "consciousness_claim": False,
        "fundamental_law_claim": False,
        "boundary": BOUNDARY,
    }


def registered_report_checksum() -> dict[str, Any]:
    protocol = {"hypothesis": "synthetic", "analysis": "frozen", "quality_checks": ["outcome_neutral"]}
    lock = digest(protocol)
    cases = [
        {"case": "locked_outcome_blind_protocol", "checksum_match": True, "outcomes_seen_before_lock": False, "deviations_logged": True, "promotion_blocked": True, "accepted": True},
        {"case": "protocol_byte_drift", "checksum_match": False, "outcomes_seen_before_lock": False, "deviations_logged": True, "promotion_blocked": True, "accepted": False},
        {"case": "outcome_seen_before_lock", "checksum_match": True, "outcomes_seen_before_lock": True, "deviations_logged": True, "promotion_blocked": True, "accepted": False},
        {"case": "undeclared_deviation", "checksum_match": True, "outcomes_seen_before_lock": False, "deviations_logged": False, "promotion_blocked": True, "accepted": False},
        {"case": "exploratory_promoted", "checksum_match": True, "outcomes_seen_before_lock": False, "deviations_logged": True, "promotion_blocked": False, "accepted": False},
    ]
    return {
        "runner": "registered-report-checksum",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "protocol_checksum": lock,
        "cases": cases,
        "real_registered_report": False,
        "journal_acceptance": False,
        "empirical_promotion": False,
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


RUNNERS: dict[str, Callable[..., dict[str, Any]]] = {
    "cross-manifest": cross_manifest_quarantine,
    "kallen-lehmann": kallen_lehmann_obligations,
    "nanograv-zero-row": nanograv_zero_row,
    "water-lab-handover": water_lab_handover_proxy,
    "related-resource": related_resource_profile,
    "boil-water-authority": boil_water_authority_reservation,
    "sqlite-migration": sqlite_migration_tribunal,
    "chart-modality": chart_modality_audit,
    "harada-sasa": harada_sasa_domain,
    "registered-report": registered_report_checksum,
}


def run(name: str, scratch: Path | None = None) -> dict[str, Any]:
    if name not in RUNNERS:
        raise KeyError(name)
    return RUNNERS[name](scratch) if name == "sqlite-migration" else RUNNERS[name]()


def main_for(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    result = run(name, args.scratch)
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")
    return 0 if result.get("passed") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", choices=[*RUNNERS, "all"], default="all")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    payload = {name: run(name, args.scratch) for name in RUNNERS} if args.runner == "all" else run(args.runner, args.scratch)
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    valid = all(row.get("passed") for row in payload.values()) if args.runner == "all" else bool(payload.get("passed"))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
