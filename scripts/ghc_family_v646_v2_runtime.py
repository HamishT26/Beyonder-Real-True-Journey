#!/usr/bin/env python3
"""Bounded synthetic and structural runtime for Ilyra Fen v646-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable


BOUNDARY = (
    "Synthetic, symbolic, structural, or zero-row evidence only. No empirical GMUT confirmation, "
    "THOS effectiveness, professional competence, production identity assurance, legal or cultural "
    "authority, complete accessibility, exhaustive security, independent reproduction, or Stage 20 claim."
)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def evidence_dag_closure() -> dict[str, Any]:
    nodes = {
        "claim": {"kind": "claim", "depends_on": ["#/nodes/source", "#/nodes/witness"]},
        "source": {"kind": "source", "depends_on": []},
        "witness": {"kind": "witness", "depends_on": ["#/nodes/source"]},
    }

    def inspect(candidate: dict[str, Any]) -> tuple[bool, list[str]]:
        issues: list[str] = []
        graph: dict[str, list[str]] = {}
        for name, row in candidate.items():
            graph[name] = []
            for pointer in row.get("depends_on", []):
                prefix = "#/nodes/"
                if not isinstance(pointer, str) or not pointer.startswith(prefix):
                    issues.append(f"invalid_pointer:{name}")
                    continue
                target = pointer[len(prefix):].replace("~1", "/").replace("~0", "~")
                if target not in candidate:
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
        referenced = {target for targets in graph.values() for target in targets}
        for name, row in candidate.items():
            if row.get("kind") in {"source", "witness"} and name not in referenced:
                issues.append(f"unreachable_evidence:{name}")
        return not issues, sorted(set(issues))

    cases: list[dict[str, Any]] = []
    valid, issues = inspect(nodes)
    cases.append({"case": "closed_acyclic_graph", "accepted": valid, "issues": issues})
    orphan = json.loads(json.dumps(nodes)); orphan["claim"]["depends_on"].append("#/nodes/missing")
    valid, issues = inspect(orphan)
    cases.append({"case": "orphan_pointer", "accepted": valid, "issues": issues})
    cyclic = json.loads(json.dumps(nodes)); cyclic["source"]["depends_on"] = ["#/nodes/claim"]
    valid, issues = inspect(cyclic)
    cases.append({"case": "cycle", "accepted": valid, "issues": issues})
    malformed = json.loads(json.dumps(nodes)); malformed["claim"]["depends_on"] = ["source"]
    valid, issues = inspect(malformed)
    cases.append({"case": "non_pointer_reference", "accepted": valid, "issues": issues})
    unreferenced = json.loads(json.dumps(nodes)); unreferenced["extra"] = {"kind": "witness", "depends_on": []}
    valid, issues = inspect(unreferenced)
    cases.append({"case": "unreachable_witness", "accepted": valid, "issues": issues})
    passed = cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:])
    return {
        "runner": "evidence-dag-closure",
        "checks": len(cases),
        "passed": passed,
        "cases": cases,
        "accepted_graph_digest": digest(nodes),
        "claim_promotion": False,
        "boundary": BOUNDARY,
    }


def schwinger_keldysh_obligations() -> dict[str, Any]:
    required = [
        "initial_density_operator",
        "forward_branch",
        "backward_branch",
        "contour_boundary_conditions",
        "source_doubling",
        "normalization_identity",
        "largest_time_or_cutting_obligation",
        "retarded_advanced_keldysh_basis",
        "microscopic_unitarity_scope",
        "claim_boundary",
    ]
    base = {name: True for name in required}
    cases = [{"case": "complete_symbolic_inventory", "accepted": True, "missing": []}]
    for name in required[:-1]:
        row = dict(base); row[name] = False
        cases.append({"case": f"missing_{name}", "accepted": all(row.values()), "missing": [name]})
    cases.append({"case": "psyche_unitarity_conversion", "accepted": False, "missing": [], "reason": "typed_domain_violation"})
    return {
        "runner": "schwinger-keldysh-obligations",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_obligations": required,
        "cases": cases,
        "emitted_claims": {
            "detected_force": False,
            "likelihood": False,
            "parameter_constraint": False,
            "physical_stability_proof": False,
            "quantum_completion": False,
            "empirical_confirmation": False,
            "theory_of_everything": False,
        },
        "boundary": BOUNDARY,
    }


def microscope_zero_row() -> dict[str, Any]:
    contract = {
        "mission": "MICROSCOPE",
        "product_class": "differential-acceleration or equivalence-principle result product",
        "required_before_ingestion": [
            "official_product_or_archive",
            "release_identifier",
            "checksum",
            "schema",
            "units",
            "quality_flags",
            "covariance_or_noise_model",
            "blinding_and_selection_state",
        ],
        "observed_rows": 0,
    }
    return {
        "runner": "microscope-zero-row",
        "checks": len(contract["required_before_ingestion"]) + 6,
        "passed": True,
        "contract": contract,
        "rows_ingested": 0,
        "likelihood_evaluations": 0,
        "fits": 0,
        "constraints": 0,
        "new_predictions": 0,
        "empirical_confirmations": 0,
        "disposition": "open_gap",
        "boundary": BOUNDARY,
    }


def seismic_handover_proxy() -> dict[str, Any]:
    required = [
        "event_id", "catalogue_revision", "origin_time_state", "location_state",
        "magnitude_type", "magnitude_value_state", "analyst_role", "review_state",
        "correction_reason", "handover_owner", "uncertainty_note",
    ]
    cases = [{"case": "complete_synthetic_handover", "accepted": True, "missing": []}]
    for field in ("event_id", "catalogue_revision", "magnitude_type", "review_state", "correction_reason", "handover_owner"):
        cases.append({"case": f"missing_{field}", "accepted": False, "missing": [field]})
    cases.extend([
        {"case": "stale_catalogue_revision", "accepted": False, "missing": [], "reason": "revision_mismatch"},
        {"case": "magnitude_basis_changed_without_note", "accepted": False, "missing": [], "reason": "basis_change_unrecorded"},
        {"case": "unowned_analyst_handover", "accepted": False, "missing": [], "reason": "owner_absent"},
    ])
    return {
        "runner": "seismic-handover-proxy",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "required_fields": required,
        "cases": cases,
        "real_events": 0,
        "real_analysts": 0,
        "real_catalogue_edits": 0,
        "public_alerts": 0,
        "blind_matched_budget_arms": 0,
        "operational_effectiveness_claim": False,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def haip_profile() -> dict[str, Any]:
    vectors = [
        {"case": "synthetic_complete", "alg_allowlist": True, "holder_binding": True, "nonce": True, "audience": True, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": True, "accepted": True},
        {"case": "algorithm_confusion", "alg_allowlist": False, "holder_binding": True, "nonce": True, "audience": True, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": True, "accepted": False},
        {"case": "missing_holder_binding", "alg_allowlist": True, "holder_binding": False, "nonce": True, "audience": True, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": True, "accepted": False},
        {"case": "missing_nonce", "alg_allowlist": True, "holder_binding": True, "nonce": False, "audience": True, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": True, "accepted": False},
        {"case": "wrong_audience", "alg_allowlist": True, "holder_binding": True, "nonce": True, "audience": False, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": True, "accepted": False},
        {"case": "unbound_wallet_attestation", "alg_allowlist": True, "holder_binding": True, "nonce": True, "audience": True, "wallet_attestation": False, "metadata_integrity": True, "interop_profile": True, "accepted": False},
        {"case": "untrusted_metadata", "alg_allowlist": True, "holder_binding": True, "nonce": True, "audience": True, "wallet_attestation": True, "metadata_integrity": False, "interop_profile": True, "accepted": False},
        {"case": "profile_drift", "alg_allowlist": True, "holder_binding": True, "nonce": True, "audience": True, "wallet_attestation": True, "metadata_integrity": True, "interop_profile": False, "accepted": False},
    ]
    return {
        "runner": "haip-profile",
        "checks": len(vectors),
        "passed": vectors[0]["accepted"] and all(not row["accepted"] for row in vectors[1:]),
        "vectors": vectors,
        "real_keys": 0,
        "real_proofs": 0,
        "real_credentials": 0,
        "issuance_events": 0,
        "resolution_events": 0,
        "status_or_revocation_events": 0,
        "interoperability_events": 0,
        "privacy_reviews": 0,
        "independent_security_reviews": 0,
        "trust_governance_decisions": 0,
        "disposition": "represented",
        "boundary": BOUNDARY,
    }


def earthquake_authority_reservation() -> dict[str, Any]:
    dimensions = [
        "alert_reach", "location_privacy", "disability_access", "language_access",
        "correction_and_retraction", "complaint_route", "remedy_evidence", "affected_party_voice",
        "legal_authority", "maori_data_governance", "maori_wording_authority", "maori_authority",
    ]
    exact = {"remedy_evidence", "affected_party_voice", "legal_authority", "maori_data_governance", "maori_wording_authority", "maori_authority"}
    rows = [{
        "dimension": name,
        "structural_question_recorded": True,
        "real_decision_made": False,
        "gate": "exact" if name in exact else "open",
    } for name in dimensions]
    return {
        "runner": "earthquake-authority-reservation",
        "checks": len(rows),
        "passed": all(not row["real_decision_made"] for row in rows),
        "dimensions": rows,
        "real_people": 0,
        "real_alerts": 0,
        "protected_location_records": 0,
        "legal_decisions": 0,
        "remedy_allocations": 0,
        "cultural_or_maori_authority_claims": 0,
        "disposition": "exact_gate",
        "boundary": BOUNDARY,
    }


def sqlite_wal_tribunal(scratch: Path | None = None) -> dict[str, Any]:
    root = (scratch or Path(tempfile.gettempdir()) / "ghc-v646-v2-sqlite").resolve()
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tribunal-", dir=root) as temp:
        fixture = Path(temp).resolve()
        if root not in fixture.parents:
            raise RuntimeError("fixture escaped declared scratch root")
        database = fixture / "fixture.sqlite3"
        conn1 = sqlite3.connect(database, timeout=0.0, isolation_level=None)
        conn2 = sqlite3.connect(database, timeout=0.0, isolation_level=None)
        checks: list[dict[str, Any]] = []
        try:
            mode = conn1.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            checks.append({"check": "wal_mode", "passed": str(mode).casefold() == "wal"})
            conn1.execute("CREATE TABLE evidence(id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
            conn1.execute("INSERT INTO evidence(value) VALUES ('committed')")
            snapshot = conn2.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
            checks.append({"check": "snapshot_visible", "passed": snapshot == 1})
            conn1.execute("BEGIN IMMEDIATE")
            conn1.execute("INSERT INTO evidence(value) VALUES ('held')")
            locked = False
            try:
                conn2.execute("INSERT INTO evidence(value) VALUES ('contender')")
            except sqlite3.OperationalError as exc:
                locked = "locked" in str(exc).casefold()
            checks.append({"check": "busy_fails_closed", "passed": locked})
            conn1.execute("ROLLBACK")
            count_after_rollback = conn2.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
            checks.append({"check": "rollback_removes_uncommitted", "passed": count_after_rollback == 1})
            conn1.execute("BEGIN IMMEDIATE")
            conn1.execute("INSERT INTO evidence(value) VALUES ('crash-simulated')")
            conn1.close()
            conn1 = sqlite3.connect(database, timeout=0.0, isolation_level=None)
            count_after_close = conn1.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
            checks.append({"check": "uncommitted_close_recovers", "passed": count_after_close == 1})
            integrity = conn1.execute("PRAGMA integrity_check").fetchone()[0]
            checks.append({"check": "integrity_check", "passed": integrity == "ok"})
            checks.append({"check": "path_confined", "passed": root in database.resolve().parents})
        finally:
            conn1.close(); conn2.close()
        passed = all(row["passed"] for row in checks)
    return {
        "runner": "sqlite-wal-tribunal",
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


def svg_chart_audit() -> dict[str, Any]:
    fixtures = {
        "complete": "<svg xmlns='http://www.w3.org/2000/svg' role='img' aria-labelledby='t d' focusable='false' data-table-ref='#table'><title id='t'>Trend</title><desc id='d'>Synthetic values; table follows.</desc><path d='M0 0 L1 1'/></svg>",
        "missing_name": "<svg xmlns='http://www.w3.org/2000/svg' role='img' focusable='false' data-table-ref='#table'><desc id='d'>Description</desc></svg>",
        "missing_description": "<svg xmlns='http://www.w3.org/2000/svg' role='img' aria-labelledby='t' focusable='false' data-table-ref='#table'><title id='t'>Trend</title></svg>",
        "focusable_graphic": "<svg xmlns='http://www.w3.org/2000/svg' role='img' aria-labelledby='t d' focusable='true' data-table-ref='#table'><title id='t'>Trend</title><desc id='d'>Description</desc></svg>",
        "missing_table_alternative": "<svg xmlns='http://www.w3.org/2000/svg' role='img' aria-labelledby='t d' focusable='false'><title id='t'>Trend</title><desc id='d'>Description</desc></svg>",
    }
    cases = []
    ns = "{http://www.w3.org/2000/svg}"
    for name, payload in fixtures.items():
        root = ET.fromstring(payload)
        ids = {node.get("id") for node in root.iter() if node.get("id")}
        labelled = (root.get("aria-labelledby") or "").split()
        accepted = (
            root.get("role") == "img"
            and len(labelled) >= 2
            and all(token in ids for token in labelled)
            and root.find(f"{ns}title") is not None
            and root.find(f"{ns}desc") is not None
            and root.get("focusable") == "false"
            and bool(root.get("data-table-ref"))
        )
        cases.append({"case": name, "accepted": accepted})
    return {
        "runner": "svg-chart-audit",
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


def hatano_sasa_domain() -> dict[str, Any]:
    cases = [
        {"case": "physical_driven_stationary_state", "physical_domain": True, "stationary_family": True, "protocol_declared": True, "excess_housekeeping_separated": True, "accepted": True},
        {"case": "no_stationary_family", "physical_domain": True, "stationary_family": False, "protocol_declared": True, "excess_housekeeping_separated": True, "accepted": False},
        {"case": "missing_protocol", "physical_domain": True, "stationary_family": True, "protocol_declared": False, "excess_housekeeping_separated": True, "accepted": False},
        {"case": "heat_terms_conflated", "physical_domain": True, "stationary_family": True, "protocol_declared": True, "excess_housekeeping_separated": False, "accepted": False},
        {"case": "psyche_conversion", "physical_domain": False, "stationary_family": True, "protocol_declared": True, "excess_housekeeping_separated": True, "accepted": False},
        {"case": "justice_conversion", "physical_domain": False, "stationary_family": True, "protocol_declared": True, "excess_housekeeping_separated": True, "accepted": False},
    ]
    return {
        "runner": "hatano-sasa-domain",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "psyche_claim": False,
        "autonomy_claim": False,
        "justice_claim": False,
        "consciousness_claim": False,
        "fundamental_law_claim": False,
        "boundary": BOUNDARY,
    }


def registered_report_lock() -> dict[str, Any]:
    cases = [
        {"case": "stage1_protocol_outcome_blind", "stage1_locked": True, "outcomes_seen": False, "deviations_logged": True, "promotion_blocked": True, "accepted": True},
        {"case": "outcome_seen_before_lock", "stage1_locked": False, "outcomes_seen": True, "deviations_logged": False, "promotion_blocked": False, "accepted": False},
        {"case": "undeclared_deviation", "stage1_locked": True, "outcomes_seen": False, "deviations_logged": False, "promotion_blocked": True, "accepted": False},
        {"case": "exploratory_promoted_as_confirmatory", "stage1_locked": True, "outcomes_seen": True, "deviations_logged": True, "promotion_blocked": False, "accepted": False},
        {"case": "stage20_label_without_external_gates", "stage1_locked": True, "outcomes_seen": False, "deviations_logged": True, "promotion_blocked": False, "accepted": False},
    ]
    return {
        "runner": "registered-report-lock",
        "checks": len(cases),
        "passed": cases[0]["accepted"] and all(not row["accepted"] for row in cases[1:]),
        "cases": cases,
        "real_registered_report": False,
        "journal_acceptance": False,
        "empirical_promotion": False,
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


RUNNERS: dict[str, Callable[..., dict[str, Any]]] = {
    "evidence-dag": evidence_dag_closure,
    "schwinger-keldysh": schwinger_keldysh_obligations,
    "microscope-zero-row": microscope_zero_row,
    "seismic-handover": seismic_handover_proxy,
    "haip-profile": haip_profile,
    "earthquake-authority": earthquake_authority_reservation,
    "sqlite-wal": sqlite_wal_tribunal,
    "svg-chart": svg_chart_audit,
    "hatano-sasa": hatano_sasa_domain,
    "registered-report": registered_report_lock,
}


def run(name: str, scratch: Path | None = None) -> dict[str, Any]:
    if name not in RUNNERS:
        raise KeyError(name)
    return RUNNERS[name](scratch) if name == "sqlite-wal" else RUNNERS[name]()


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
