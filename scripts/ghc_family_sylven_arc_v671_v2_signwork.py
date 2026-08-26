"""Bounded owner-local helpers for Sylven Arc v671-v2.

This module validates wholly synthetic signwriting-documentation fixtures.  It
never performs a network call, touches a real sign or person, issues an
identity credential, makes a professional decision, or exercises authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sylven Arc"
PHASE = "v671-v2"
PREFIX = "SA6712"
SOURCE_FINAL = "ebbd2ea41873c12287d94b0ec2b64dc22a87c07d"
X1_COMMIT = "26c88fefc685b48965a1418d07204cc91f6580a0"
SOURCE_CHAIN = 5590
CHAIN_AFTER = 5630
OWNER_ROOT = Path("docs/sylven-arc/v671-v2")
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

INHERITED = {
    "effective_negatives": 33525,
    "methods": 19842,
    "failed_witnesses": 5346,
    "passing_witnesses": 6881,
    "open_gaps": 257,
    "exact_gates": 252,
}

PROTECTED_GATES = [
    "real_people_participants_or_personal_records",
    "real_signs_sites_land_objects_materials_tools_or_workplaces",
    "real_measurements_observations_treatments_installations_or_safety_actions",
    "professional_signwriting_conservation_engineering_or_workplace_decision",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_accessibility_complete_or_exhaustive_security_claim",
    "ownership_custody_authorship_recording_access_legal_or_remedy_decision",
    "cultural_interpretation_traditional_knowledge_or_affected_party_legitimacy",
    "Maori_wording_concepts_data_governance_or_authority",
    "empirical_GMUT_final_physics_or_Theory_of_Everything_claim",
    "THOS_operational_effectiveness_AGI_or_ASI_claim",
    "consciousness_personhood_or_identity_continuity_claim",
    "independent_reproduction_production_deployment_canon_or_Stage_20_claim",
]

BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite evidence "
    "is not empirical confirmation, participant evidence, professional or scientific "
    "authority, production readiness, legal or cultural ratification, Maori authority, "
    "affected-party approval, complete privacy or accessibility assurance, exhaustive "
    "security, independent reproduction, AGI/ASI, consciousness or personhood evidence, "
    "Theory-of-Everything proof, canon, or Stage 20 authority."
)

RUNNER_BINDINGS = [
    ("ghc-family-signwork-project-identity", "ghc_family_signwork_project_identity", "SA6712-N001"),
    ("ghc-family-signboard-topology", "ghc_family_signboard_topology", "SA6712-N002"),
    ("ghc-family-letter-layout-relations", "ghc_family_letter_layout_relations", "SA6712-N003"),
    ("ghc-family-paint-layer-vacancy", "ghc_family_paint_layer_vacancy", "SA6712-N004"),
    ("ghc-family-signwork-orientation-variant-firewall", "ghc_family_signwork_measurement_vacancy", "SA6712-N005"),
    ("ghc-family-signwork-custody-abstention", "ghc_family_coating_safety_abstention", "SA6712-N006"),
    ("ghc-family-sign-condition-diagnosis-firewall", "ghc_family_signwork_privacy_quarantine", "SA6712-N007"),
    ("ghc-family-signwork-measurement-vacancy", "ghc_family_signwork_accessible_status", "SA6712-N008"),
    ("ghc-family-signwork-command-observation-split", "ghc_family_signwork_correction_readback", "SA6712-N009"),
    ("ghc-family-brush-coating-material-hold", "ghc_family_signwork_workload_handover", "SA6712-N010"),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slugify(value: str) -> str:
    return "-".join(re.findall(r"[a-z0-9]+", value.lower()))[:96].strip("-")


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    payload = load_json(repo / OWNER_ROOT / "x1/new-proposal-freeze.json")
    rows = payload["rows"]
    if len(rows) != 40:
        raise ValueError(f"expected 40 frozen proposals, found {len(rows)}")
    return rows


def contract_for(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.synthetic-signwork-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "title": row["title"],
        "semantic_slug": slugify(row["title"]),
        "outcome": row["expected_disposition"],
        "synthetic_only": True,
        "authoritative": False,
        "source_status": row["official_or_primary_source_needs"],
        "typed_state": "documented_synthetic_fixture",
        "zero_counters": {
            "real_people": 0,
            "real_signs_or_objects": 0,
            "real_measurements": 0,
            "network_calls": 0,
            "external_actions": 0,
            "identity_lifecycle_actions": 0,
            "authority_actions": 0,
        },
        "vacancies": [
            "real_observation",
            "real_measurement",
            "professional_interpretation",
            "affected_party_authority",
            "legal_and_cultural_authority",
        ],
        "protected_gates": PROTECTED_GATES,
        "rollback": row["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


def validate_contract(payload: dict[str, Any], expected_proposal_id: str | None = None) -> dict[str, Any]:
    failures: list[str] = []
    required = {
        "schema", "owner", "phase", "proposal_id", "title", "semantic_slug", "outcome",
        "synthetic_only", "authoritative", "source_status", "zero_counters", "vacancies",
        "protected_gates", "rollback", "terminal_verdict", "boundary",
    }
    missing = sorted(required - payload.keys())
    if missing:
        failures.append("missing_required_fields:" + ",".join(missing))
    if payload.get("schema") != "ghc.family.synthetic-signwork-contract.v1":
        failures.append("schema_mismatch")
    if payload.get("owner") != OWNER or payload.get("phase") != PHASE:
        failures.append("owner_or_phase_mismatch")
    if expected_proposal_id and payload.get("proposal_id") != expected_proposal_id:
        failures.append("proposal_id_mismatch")
    if payload.get("outcome") not in CORE_LABELS:
        failures.append("invalid_outcome")
    if payload.get("synthetic_only") is not True or payload.get("authoritative") is not False:
        failures.append("synthetic_or_authority_boundary_broken")
    counters = payload.get("zero_counters")
    if not isinstance(counters, dict) or not counters or any(value != 0 for value in counters.values()):
        failures.append("nonzero_or_missing_real_world_counter")
    gates = payload.get("protected_gates")
    if not isinstance(gates, list) or set(gates) != set(PROTECTED_GATES):
        failures.append("protected_gate_set_mismatch")
    if payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        failures.append("stage20_boundary_broken")
    if payload.get("boundary") != BOUNDARY:
        failures.append("claim_boundary_mismatch")
    return {
        "schema": "ghc.family.synthetic-contract-validation.v1",
        "proposal_id": payload.get("proposal_id"),
        "passed": not failures,
        "failures": failures,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def rejecting_mutations(base: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    variants: list[tuple[str, dict[str, Any]]] = []
    first = copy.deepcopy(base)
    first["zero_counters"]["real_people"] = 1
    variants.append(("real_person_counter_nonzero", first))
    second = copy.deepcopy(base)
    second["authoritative"] = True
    variants.append(("authority_promotion", second))
    third = copy.deepcopy(base)
    third["terminal_verdict"] = "READY_FOR_STAGE_20"
    variants.append(("stage20_promotion", third))
    fourth = copy.deepcopy(base)
    fourth["protected_gates"] = fourth["protected_gates"][:-1]
    variants.append(("missing_protected_gate", fourth))
    return variants


def portfolio_execution(rows: Iterable[dict[str, Any]], state: str, credit: int) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "x2_state": state,
            "completion_credit": credit,
            "same_owner_only": True,
            "external_actions": 0,
        }
        for row in rows
    ]


def git_blob(repo: Path, spec: str) -> bytes:
    return subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout


def normalized_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def runner_main(expected_proposal_id: str) -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: runner <synthetic-contract.json>")
    path = Path(sys.argv[1])
    try:
        payload = load_json(path)
        result = validate_contract(payload, expected_proposal_id)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"passed": False, "failures": [type(exc).__name__], "proposal_id": None}
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result.get("passed") else 1)
