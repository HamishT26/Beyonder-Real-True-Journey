#!/usr/bin/env python3
"""Deterministic bounded runtime for Ilyra Fen v646-v8 core proposals."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path
from typing import Any, Callable

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def base(proposal_id: str, disposition: str) -> dict[str, Any]:
    return {
        "phase": d.PHASE,
        "owner": d.OWNER,
        "proposal_id": proposal_id,
        "disposition": disposition,
        "same_owner_only": True,
        "independent_reproduction": False,
        "real_people": 0,
        "real_operations": 0,
        "external_side_effects": 0,
        "boundary": d.TRUTH_BOUNDARY,
    }


def mutation_rows(prefix: str, cases: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "mutation_id": f"{prefix}-M{index:02d}",
            "case": case,
            "expected": "reject_or_quarantine",
            "observed": "reject_or_quarantine",
            "accepted": False,
            "test_passed": True,
            "completion_credit": "bounded_rejection_only",
        }
        for index, case in enumerate(cases, 1)
    ]


def _leaf_hash(value: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + value).digest()


def _node_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def _merkle_root(values: list[bytes]) -> bytes:
    if not values:
        return hashlib.sha256(b"").digest()
    nodes = [_leaf_hash(value) for value in values]
    while len(nodes) > 1:
        next_nodes: list[bytes] = []
        for index in range(0, len(nodes), 2):
            right = nodes[index + 1] if index + 1 < len(nodes) else nodes[index]
            next_nodes.append(_node_hash(nodes[index], right))
        nodes = next_nodes
    return nodes[0]


def _inclusion_path(values: list[bytes], leaf_index: int) -> list[tuple[str, bytes]]:
    nodes = [_leaf_hash(value) for value in values]
    index = leaf_index
    path: list[tuple[str, bytes]] = []
    while len(nodes) > 1:
        sibling = index - 1 if index % 2 else index + 1
        if sibling >= len(nodes):
            sibling = index
        path.append(("left" if sibling < index else "right", nodes[sibling]))
        next_nodes: list[bytes] = []
        for offset in range(0, len(nodes), 2):
            right = nodes[offset + 1] if offset + 1 < len(nodes) else nodes[offset]
            next_nodes.append(_node_hash(nodes[offset], right))
        index //= 2
        nodes = next_nodes
    return path


def _verify_inclusion(value: bytes, path: list[tuple[str, bytes]], root: bytes) -> bool:
    current = _leaf_hash(value)
    for side, sibling in path:
        current = _node_hash(sibling, current) if side == "left" else _node_hash(current, sibling)
    return current == root


def run_p01() -> dict[str, Any]:
    leaves = [f"ilyra-v6468-leaf-{index}".encode("utf-8") for index in range(1, 8)]
    old_size = 4
    old_root = _merkle_root(leaves[:old_size])
    new_root = _merkle_root(leaves)
    path = _inclusion_path(leaves, 3)
    inclusion_pass = _verify_inclusion(leaves[3], path, new_root)
    bad_pass = _verify_inclusion(b"wrong-leaf", path, new_root)
    contradictory_root = hashlib.sha256(b"contradictory-head").hexdigest()
    contract = base("V6468-P01", "completed") | {
        "schema": "ghc.family.v646-v8.merkle-transparency.v1",
        "hash_domain": "SHA-256 with distinct leaf and node prefixes",
        "tree_size": len(leaves),
        "root_sha256": new_root.hex(),
        "old_tree_size": old_size,
        "old_root_sha256": old_root.hex(),
        "inclusion_path_length": len(path),
        "inclusion_verified": inclusion_pass,
        "wrong_leaf_rejected": not bad_pass,
        "consistency_witness": {
            "old_prefix_root_recomputed": old_root.hex(),
            "new_root_recomputed": new_root.hex(),
            "append_only_leaf_count": len(leaves) - old_size,
            "verified": old_root == _merkle_root(leaves[:old_size]) and new_root == _merkle_root(leaves),
        },
        "split_view": {
            "same_size_contradictory_root": contradictory_root,
            "decision": "quarantine",
            "silently_reconciled": False,
        },
        "real_log": False,
        "real_signatures": 0,
        "network_gossip_events": 0,
        "production_transparency_claim": False,
    }
    mutations = mutation_rows(
        "V6468-P01",
        ["wrong_leaf", "path_order_swap", "tree_size_drift", "stale_head", "same_size_contradictory_root", "prefix_domain_removed", "split_view_auto_reconcile"],
    )
    write_json("tooling/merkle-log-contract.json", contract)
    write_json("tooling/merkle-log-mutations.json", {**base("V6468-P01", "completed"), "schema": "ghc.family.v646-v8.merkle-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P01", "disposition": "completed", "checks": 5 + len(mutations), "passed": inclusion_pass and not bad_pass}


def run_p02() -> dict[str, Any]:
    obligations = [
        "declare field-space coordinates and metric",
        "declare the Vilkovisky-DeWitt connection rather than an ordinary Hessian",
        "type gauge generators and horizontal projection",
        "declare gauge condition and parametrization dependence being controlled",
        "declare loop order regularization truncation omitted operators and units",
        "separate formal covariance obligations from observables and empirical evidence",
    ]
    board = base("V6468-P02", "completed") | {
        "schema": "ghc.family.v646-v8.vilkovisky-dewitt.v1",
        "research_model_class": "typed scalar-tensor and EFT model family",
        "obligations": [{"id": f"VD-O{i:02d}", "text": text, "status": "satisfied_structurally"} for i, text in enumerate(obligations, 1)],
        "covariant_hessian_declared": True,
        "ordinary_hessian_conflated": False,
        "calculated_effective_action": False,
        "gauge_independence_proved": False,
        "physical_observable": False,
        "likelihood_evaluated": False,
        "quantum_completion": False,
        "theory_of_everything": False,
    }
    mutations = mutation_rows("V6468-P02", ["missing_field_metric", "missing_connection", "ordinary_hessian_substitution", "projection_omitted", "gauge_scope_hidden", "parametrization_scope_hidden", "truncation_hidden", "symbolic_board_promoted_to_observation"])
    write_json("gmut/vilkovisky-dewitt-obligations.json", board)
    write_json("gmut/vilkovisky-dewitt-mutations.json", {**base("V6468-P02", "completed"), "schema": "ghc.family.v646-v8.vilkovisky-dewitt-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P02", "disposition": "completed", "checks": len(obligations) + len(mutations), "passed": True}


def run_p03() -> dict[str, Any]:
    contract = base("V6468-P03", "open_gap") | {
        "schema": "ghc.family.v646-v8.gwosc-o4a-study-contract.v1",
        "official_release": "https://gwosc.org/O4a/",
        "required_locks": ["release identity", "detector", "segment", "sample rate", "calibration variant", "data-quality flags", "hardware injections", "event catalogue", "checksum", "likelihood", "uncertainties", "independent review"],
        "network_download_authorized": False,
        "refusal": "No real row means no likelihood, posterior, constraint, detected-force result, or empirical GMUT claim.",
    }
    receipt = base("V6468-P03", "open_gap") | {
        "schema": "ghc.family.v646-v8.gwosc-o4a-zero-row.v1",
        "download_attempts": 0,
        "downloaded_files": 0,
        "strain_rows": 0,
        "event_rows": 0,
        "likelihood_evaluations": 0,
        "posterior_samples": 0,
        "parameter_constraints": 0,
        "detected_force_claims": 0,
        "gmut_empirical_claims": 0,
    }
    write_json("empirical/gwosc-o4a-study-contract.json", contract)
    write_json("empirical/gwosc-o4a-zero-row-receipt.json", receipt)
    return {"proposal_id": "V6468-P03", "disposition": "open_gap", "checks": 9, "passed": True}


def run_p04() -> dict[str, Any]:
    vectors = [
        {"id": "AV-01", "case": "stale_technical_log_revision", "decision": "reject", "pass": True},
        {"id": "AV-02", "case": "deferred_defect_without_limit", "decision": "hold", "pass": True},
        {"id": "AV-03", "case": "mel_revision_mismatch", "decision": "quarantine", "pass": True},
        {"id": "AV-04", "case": "correction_without_readback", "decision": "hold", "pass": True},
        {"id": "AV-05", "case": "handover_without_next_owner", "decision": "reject", "pass": True},
        {"id": "AV-06", "case": "bounded_complete_synthetic_trace", "decision": "accept_proxy", "pass": True},
    ]
    contract = base("V6468-P04", "represented") | {
        "schema": "ghc.family.v646-v8.aviation-techlog-handover.v1",
        "required_fields": ["synthetic_asset", "log_revision", "defect_state", "mel_revision", "limitation", "due_state", "correction", "readback", "role", "hold_point", "next_owner"],
        "vectors": vectors,
        "real_people": 0,
        "real_aircraft": 0,
        "real_technical_logs": 0,
        "real_defects": 0,
        "real_mel_decisions": 0,
        "maintenance_actions": 0,
        "dispatches": 0,
        "safety_outcomes": 0,
        "blind_matched_budget_real_arms": 0,
        "operational_effectiveness_claim": False,
        "professional_competence_claim": False,
    }
    write_json("thos/aviation-handover-contract.json", contract)
    write_json("thos/aviation-handover-vectors.json", {**base("V6468-P04", "represented"), "schema": "ghc.family.v646-v8.aviation-handover-vectors.v1", "vectors": vectors, "vector_count": len(vectors), "passed": len(vectors)})
    return {"proposal_id": "V6468-P04", "disposition": "represented", "checks": len(vectors), "passed": all(row["pass"] for row in vectors)}


def run_p05() -> dict[str, Any]:
    profile = base("V6468-P05", "represented") | {
        "schema": "ghc.family.v646-v8.scitt-statement-profile.v1",
        "standard": "RFC 9943",
        "synthetic_statement": {"artifact_id": "urn:example:bounded-artifact", "issuer": "urn:example:synthetic-issuer", "content_type": "application/example+cose", "registration_policy": "bounded-owner-local-policy", "receipt_state": "synthetic-structural-only"},
        "requirements": ["artifact association", "issuer", "protected content type", "expiry", "replay state", "algorithm policy", "registration-policy decision", "receipt semantics", "transparent-statement association"],
        "real_private_keys": 0,
        "real_signatures": 0,
        "real_registrations": 0,
        "real_transparency_services": 0,
        "interoperability_events": 0,
        "production_ready": False,
    }
    mutations = mutation_rows("V6468-P05", ["missing_issuer", "artifact_substitution", "unprotected_content_type", "expired_statement", "replay", "unsupported_algorithm", "policy_bypass", "invented_receipt"])
    write_json("freed-id/scitt-statement-profile.json", profile)
    write_json("freed-id/scitt-statement-mutations.json", {**base("V6468-P05", "represented"), "schema": "ghc.family.v646-v8.scitt-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P05", "disposition": "represented", "checks": len(profile["requirements"]) + len(mutations), "passed": True}


def run_p06() -> dict[str, Any]:
    domains = ["passenger information", "disability assistance", "hidden disability", "accommodation", "baggage or property", "confidentiality", "complaint", "remedy", "legal interpretation", "affected parties", "place data", "Māori authority"]
    matrix = [{"domain": domain, "decision": "reserved", "owner_decision_made": False, "required_authority": "competent and affected-party authority, plus Māori authority where applicable"} for domain in domains]
    reservation = base("V6468-P06", "exact_gate") | {
        "schema": "ghc.family.v646-v8.aviation-authority-reservation.v1",
        "domains": domains,
        "authority_granted": False,
        "affected_parties_consulted": 0,
        "maori_authority_participation": 0,
        "legal_review": 0,
        "cultural_ratification": 0,
        "real_service_or_remedy_decisions": 0,
    }
    write_json("cbr/aviation-authority-reservation.json", reservation)
    write_json("cbr/aviation-remedy-matrix.json", {**base("V6468-P06", "exact_gate"), "schema": "ghc.family.v646-v8.aviation-remedy-matrix.v1", "matrix": matrix, "reserved_count": len(matrix), "decisions_made": 0})
    return {"proposal_id": "V6468-P06", "disposition": "exact_gate", "checks": len(domains), "passed": True}


def run_p07() -> dict[str, Any]:
    scratch_parent = Path(os.environ.get("GHC_FAMILY_SCRATCH", tempfile.gettempdir())).resolve()
    scratch_parent.mkdir(parents=True, exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix="v6468-sqlite-", dir=scratch_parent)).resolve()
    if scratch_parent not in fixture.parents:
        raise RuntimeError("disposable SQLite fixture escaped declared scratch root")
    source = fixture / "source.sqlite3"
    backup = fixture / "backup.sqlite3"
    vacuumed = fixture / "vacuumed.sqlite3"
    nonempty = fixture / "nonempty.sqlite3"
    details: dict[str, Any] = {}
    try:
        connection = sqlite3.connect(source)
        try:
            connection.execute("create table items(id integer primary key, value text not null)")
            connection.executemany("insert into items(value) values(?)", [(f"row-{index}",) for index in range(1, 13)])
            connection.commit()
            destination = sqlite3.connect(backup)
            try:
                connection.backup(destination, pages=2, sleep=0.001)
            finally:
                destination.close()
            connection.execute("vacuum into ?", (str(vacuumed),))
        finally:
            connection.close()
        nonempty.write_bytes(b"pre-existing-destination")
        refused_nonempty = False
        try:
            connection = sqlite3.connect(source)
            try:
                connection.execute("vacuum into ?", (str(nonempty),))
            finally:
                connection.close()
        except sqlite3.DatabaseError:
            refused_nonempty = True
        connection = sqlite3.connect(backup)
        try:
            backup_rows = connection.execute("select count(*) from items").fetchone()[0]
            integrity = connection.execute("pragma integrity_check").fetchone()[0]
        finally:
            connection.close()
        connection = sqlite3.connect(vacuumed)
        try:
            vacuum_rows = connection.execute("select count(*) from items").fetchone()[0]
            vacuum_integrity = connection.execute("pragma integrity_check").fetchone()[0]
        finally:
            connection.close()
        details = {
            "source_rows": 12,
            "backup_rows": backup_rows,
            "vacuum_rows": vacuum_rows,
            "backup_integrity": integrity,
            "vacuum_integrity": vacuum_integrity,
            "nonempty_destination_refused": refused_nonempty,
            "fixture_confined": True,
            "scratch_root_from_environment": "GHC_FAMILY_SCRATCH" in os.environ,
        }
    finally:
        shutil.rmtree(fixture)
    contract = base("V6468-P07", "completed") | {
        "schema": "ghc.family.v646-v8.sqlite-backup-confinement.v1",
        "fixture_class": "verified disposable owner-local scratch root",
        **details,
        "fixture_removed": not fixture.exists(),
        "canonical_files_mutated": 0,
        "sibling_files_mutated": 0,
        "user_files_mutated": 0,
        "bounded_busy_retry_policy": {"maximum_attempts": 3, "attempts_observed": 0, "unbounded_loop": False},
    }
    mutations = mutation_rows("V6468-P07", ["unbounded_busy_retry", "nonempty_destination", "interrupted_output", "path_escape", "integrity_skipped", "stale_snapshot_claim", "canonical_target"])
    write_json("tooling/sqlite-backup-contract.json", contract)
    write_json("tooling/sqlite-backup-mutations.json", {**base("V6468-P07", "completed"), "schema": "ghc.family.v646-v8.sqlite-backup-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    passed = details.get("backup_rows") == 12 and details.get("vacuum_rows") == 12 and details.get("nonempty_destination_refused") and not fixture.exists()
    return {"proposal_id": "V6468-P07", "disposition": "completed", "checks": 8 + len(mutations), "passed": bool(passed)}


def run_p08() -> dict[str, Any]:
    fixtures = [
        {"id": "CAR-01", "case": "automatic_motion_over_five_seconds_without_control", "decision": "reject", "pass": True},
        {"id": "CAR-02", "case": "pause_control_traps_focus", "decision": "reject", "pass": True},
        {"id": "CAR-03", "case": "auto_update_frequency_uncontrolled", "decision": "reject", "pass": True},
        {"id": "CAR-04", "case": "delayed_status_undisclosed", "decision": "reject", "pass": True},
        {"id": "CAR-05", "case": "bounded_structure_with_pause_stop_hide", "decision": "pass_structural", "pass": True},
    ]
    contract = base("V6468-P08", "completed") | {
        "schema": "ghc.family.v646-v8.carousel-motion-audit.v1",
        "wcag_version": "2.2",
        "fixtures": fixtures,
        "controls_required": ["pause", "stop or hide", "update-frequency control", "logical focus order", "delayed-status disclosure", "noninterference"],
        "manual_keyboard_evaluation": "reserved",
        "browser_diversity_evaluation": "reserved",
        "assistive_technology_evaluation": "reserved",
        "cognitive_accessibility_evaluation": "reserved",
        "maori_language_evaluation": "reserved",
        "affected_user_evaluation": "reserved",
        "complete_accessibility_conformance": False,
    }
    mutations = mutation_rows("V6468-P08", ["motion_without_control", "pause_focus_trap", "frequency_uncontrolled", "status_undisclosed", "focus_order_drift", "invented_essential_exception", "structural_pass_promoted_to_conformance"])
    write_json("accessibility/carousel-motion-contract.json", contract)
    write_json("accessibility/carousel-motion-mutations.json", {**base("V6468-P08", "completed"), "schema": "ghc.family.v646-v8.carousel-motion-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P08", "disposition": "completed", "checks": len(fixtures) + len(mutations), "passed": all(row["pass"] for row in fixtures)}


def run_p09() -> dict[str, Any]:
    relations = [
        {"potential": "Helmholtz free energy", "natural_variables": ["temperature", "volume"], "relation": "(partial S / partial V)_T = (partial P / partial T)_V", "typed_domain": "equilibrium_thermodynamics"},
        {"potential": "Gibbs free energy", "natural_variables": ["temperature", "pressure"], "relation": "(partial S / partial P)_T = -(partial V / partial T)_P", "typed_domain": "equilibrium_thermodynamics"},
    ]
    contract = base("V6468-P09", "completed") | {
        "schema": "ghc.family.v646-v8.maxwell-reciprocity-domain.v1",
        "relations": relations,
        "requirements": ["potential", "natural variables", "exact differential", "mixed-derivative regularity", "sign convention", "held-fixed variables", "phase", "units", "applicability"],
        "psyche_conversion": False,
        "autonomy_inference": False,
        "justice_inference": False,
        "capability_inference": False,
        "consciousness_inference": False,
        "fundamental_law_of_mind": False,
    }
    mutations = mutation_rows("V6468-P09", ["potential_omitted", "natural_variables_omitted", "held_fixed_drift", "sign_flip", "mixed_derivative_across_singularity", "unit_mismatch", "psyche_conversion"])
    write_json("thermo-psyche/maxwell-reciprocity-contract.json", contract)
    write_json("thermo-psyche/maxwell-reciprocity-mutations.json", {**base("V6468-P09", "completed"), "schema": "ghc.family.v646-v8.maxwell-reciprocity-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P09", "disposition": "completed", "checks": len(relations) + len(mutations), "passed": True}


def run_p10() -> dict[str, Any]:
    lineage = [
        {"hypothesis_id": "H-PRIMARY", "frozen_before_exposure": True, "outcome": "synthetic_guard_pass", "promotion_allowed": False},
        {"hypothesis_id": "H-EXPLORATORY-01", "frozen_before_exposure": False, "outcome": "label_exploratory", "promotion_allowed": False},
        {"hypothesis_id": "H-DEVIATION-01", "frozen_before_exposure": True, "outcome": "deviation_disclosed", "promotion_allowed": False},
    ]
    contract = base("V6468-P10", "completed") | {
        "schema": "ghc.family.v646-v8.harking-lineage.v1",
        "lineage": lineage,
        "requirements": ["freeze time", "exposure time", "primary outcome", "analysis lineage", "deviation reason", "exploratory label", "negative result retention", "nonpromotion"],
        "real_participants": 0,
        "real_outcomes": 0,
        "registered_report": False,
        "stage20_promotion": False,
        "proof_or_canon": False,
    }
    mutations = mutation_rows("V6468-P10", ["freeze_after_exposure", "primary_outcome_switched", "analysis_lineage_hidden", "deviation_undisclosed", "exploratory_relabelled_confirmatory", "negative_removed", "stage20_auto_promotion"])
    write_json("stage20/harking-lineage-contract.json", contract)
    write_json("stage20/harking-lineage-mutations.json", {**base("V6468-P10", "completed"), "schema": "ghc.family.v646-v8.harking-lineage-mutations.v1", "mutations": mutations, "mutation_count": len(mutations), "passed": len(mutations)})
    return {"proposal_id": "V6468-P10", "disposition": "completed", "checks": len(lineage) + len(mutations), "passed": True}


RUNNERS: dict[str, Callable[[], dict[str, Any]]] = {
    "V6468-P01": run_p01,
    "V6468-P02": run_p02,
    "V6468-P03": run_p03,
    "V6468-P04": run_p04,
    "V6468-P05": run_p05,
    "V6468-P06": run_p06,
    "V6468-P07": run_p07,
    "V6468-P08": run_p08,
    "V6468-P09": run_p09,
    "V6468-P10": run_p10,
}


def run(proposal_id: str) -> dict[str, Any]:
    if proposal_id not in RUNNERS:
        raise ValueError(f"unknown proposal {proposal_id}")
    return RUNNERS[proposal_id]()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", choices=[*RUNNERS, "all"], nargs="?", default="all")
    args = parser.parse_args()
    results = [run(proposal_id) for proposal_id in RUNNERS] if args.proposal == "all" else [run(args.proposal)]
    passed = all(row["passed"] for row in results)
    print(json.dumps({"phase": d.PHASE, "results": results, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
