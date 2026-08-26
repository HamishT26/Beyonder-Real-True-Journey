"""Bounded synthetic seed-library contracts for Eiren Kestrel v671-v4."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

OWNER = "Eiren Kestrel"
PHASE = "v671-v4"
OWNER_ROOT = Path("docs/eiren-kestrel/v671-v4")
X1_COMMIT = "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26"
CHAIN_AFTER = 5710
CORE_LABELS = ("completed", "represented", "open_gap", "exact_gate")
PROTECTED_GATES = (
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "legal",
    "cultural",
    "affected_party",
    "Maori_authority",
    "AGI_ASI",
    "consciousness_personhood",
    "Theory_of_Everything",
    "proof_canon",
    "Stage_20",
)
ZERO_COUNTER_KEYS = (
    "real_people",
    "real_seed_libraries_or_genebanks",
    "real_seeds_plants_or_samples",
    "real_accessions_packets_or_records",
    "real_storage_germination_or_regeneration_events",
    "real_biosafety_or_phytosanitary_actions",
    "real_measurements",
    "real_media_or_records",
    "network_calls",
    "downloads",
    "external_writes",
    "identity_lifecycle_events",
    "professional_actions",
    "authority_acts",
)
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Maori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI or ASI evidence, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or "
    "canon, or Stage 20 authority."
)

RUNNER_BINDINGS = (
    ("ghc-family-seed-accession-identity", "ghc_family_seed_accession_identity", "EK6714-N001"),
    ("ghc-family-seed-lot-lineage", "ghc_family_seed_lot_lineage", "EK6714-N003"),
    ("ghc-family-seed-packet-topology", "ghc_family_seed_packet_topology", "EK6714-N004"),
    ("ghc-family-seed-taxonomy-vacancy", "ghc_family_seed_taxonomy_vacancy", "EK6714-N005"),
    ("ghc-family-seed-measurement-vacancy", "ghc_family_seed_measurement_vacancy", "EK6714-N008"),
    ("ghc-family-seed-biosafety-abstention", "ghc_family_seed_biosafety_abstention", "EK6714-N013"),
    ("ghc-family-seed-sensitive-data-quarantine", "ghc_family_seed_sensitive_data_quarantine", "EK6714-N020"),
    ("ghc-family-seed-correction-handover", "ghc_family_seed_correction_handover", "EK6714-N024"),
    ("ghc-family-seed-rights-vacancy", "ghc_family_seed_rights_vacancy", "EK6714-N027"),
    ("ghc-family-seed-accessible-status", "ghc_family_seed_accessible_status", "EK6714-N022"),
)


def load_json(path: Path) -> Any:
    """Load one UTF-8 JSON document."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write one deterministic UTF-8 JSON document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    """Write deterministic UTF-8 text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    """Return the immutable x1 proposal rows."""
    payload = load_json(repo / OWNER_ROOT / "x1/proposals.json")
    rows = payload["rows"]
    if len(rows) != 40:
        raise ValueError("expected exactly forty frozen proposal rows")
    return rows


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return list(dict.fromkeys(words))[:12]


def contract_for(row: dict[str, Any]) -> dict[str, Any]:
    """Build one synthetic, non-authoritative contract from a frozen row."""
    disposition = row["expected_disposition"]
    state = {
        "completed": "bounded_synthetic_structure_passed",
        "represented": "bounded_representation_only",
        "open_gap": "unclosed_real_evidence_gap",
        "exact_gate": "unexecuted_exact_authority_gate",
    }[disposition]
    return {
        "schema": "ghc.family.seed-library-synthetic-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "title": row["title"],
        "hypothesis": row["hypothesis"],
        "expected_disposition": disposition,
        "observed_disposition": disposition,
        "evidence_state": state,
        "completion_credit": 1 if disposition == "completed" else 0,
        "synthetic_only": True,
        "authoritative": False,
        "primary_pillar": "Freed ID and CBR Heart",
        "protected_pillars": ["GMUT Mind", "THOS Body"],
        "bounded_practice": "synthetic community seed-library and genebank documentation only",
        "structural_witness": {
            "proposal_tokens": _tokens(row["title"]),
            "input_class": "synthetic_or_reported_placeholder",
            "output_class": "bounded_documentation_state",
            "acceptance_gate": row["falsifier_or_acceptance_gate"],
            "null_condition": row["null_or_failure_condition"],
            "rollback": row["rollback_or_recovery"],
            "source_needs": row["official_or_primary_source_needs"],
            "concrete_artifacts": row["concrete_artifacts"],
            "deterministic": True,
        },
        "state_transitions": [
            {"from": "declared", "to": "quarantined", "reversible": True},
            {"from": "quarantined", "to": state, "reversible": True},
        ],
        "vacancy_state": {
            "real_evidence_missing": disposition in {"open_gap", "exact_gate"},
            "exact_authority_missing": disposition == "exact_gate",
            "representation_is_completion": False,
        },
        "zero_counters": {key: 0 for key in ZERO_COUNTER_KEYS},
        "protected_gates": list(PROTECTED_GATES),
        "claims_not_made": [
            "real measurement or observation",
            "seed conservation taxonomy biosafety or phytosanitary competence",
            "production or deployment readiness",
            "identity issuance or verification",
            "legal cultural affected-party or Maori authority",
            "empirical GMUT or operational THOS evidence",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


def validate_contract(
    payload: dict[str, Any], expected_row: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Validate structural and authority invariants for one contract."""
    failures: list[str] = []
    if payload.get("schema") != "ghc.family.seed-library-synthetic-contract.v1":
        failures.append("schema")
    if expected_row is not None:
        for key in ("proposal_id", "title"):
            if payload.get(key) != expected_row.get(key):
                failures.append(f"frozen_{key}")
        if payload.get("expected_disposition") != expected_row.get(
            "expected_disposition"
        ):
            failures.append("frozen_expected_disposition")
    disposition = payload.get("observed_disposition")
    if disposition not in CORE_LABELS:
        failures.append("core_disposition")
    if payload.get("expected_disposition") != disposition:
        failures.append("expected_observed_disposition")
    if payload.get("synthetic_only") is not True:
        failures.append("synthetic_only")
    if payload.get("authoritative") is not False:
        failures.append("authoritative")
    counters = payload.get("zero_counters")
    if not isinstance(counters, dict) or set(counters) != set(ZERO_COUNTER_KEYS):
        failures.append("zero_counter_shape")
    elif any(type(value) is not int or value != 0 for value in counters.values()):
        failures.append("zero_counter_value")
    if set(payload.get("protected_gates", [])) != set(PROTECTED_GATES):
        failures.append("protected_gates")
    witness = payload.get("structural_witness")
    if not isinstance(witness, dict) or not witness.get("deterministic"):
        failures.append("structural_witness")
    elif not witness.get("proposal_tokens") or not witness.get("concrete_artifacts"):
        failures.append("proposal_specific_structure")
    transitions = payload.get("state_transitions")
    if not isinstance(transitions, list) or len(transitions) != 2:
        failures.append("state_transitions")
    elif not all(item.get("reversible") is True for item in transitions):
        failures.append("reversibility")
    expected_credit = 1 if disposition == "completed" else 0
    if payload.get("completion_credit") != expected_credit:
        failures.append("completion_credit")
    vacancy = payload.get("vacancy_state", {})
    if disposition == "represented" and vacancy.get("representation_is_completion"):
        failures.append("representation_laundering")
    if disposition == "open_gap" and not vacancy.get("real_evidence_missing"):
        failures.append("open_gap_erasure")
    if disposition == "exact_gate" and not vacancy.get("exact_authority_missing"):
        failures.append("exact_gate_erasure")
    if payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        failures.append("terminal_verdict")
    if payload.get("boundary") != BOUNDARY:
        failures.append("boundary")
    return {"passed": not failures, "failures": sorted(set(failures))}


def rejecting_mutations(
    contract: dict[str, Any],
) -> list[tuple[str, dict[str, Any]]]:
    """Return four preregistered invalid variants without mutating the source."""
    people = copy.deepcopy(contract)
    people["zero_counters"]["real_people"] = 1
    authority = copy.deepcopy(contract)
    authority["authoritative"] = True
    stage = copy.deepcopy(contract)
    stage["terminal_verdict"] = "READY_FOR_STAGE_20"
    gate = copy.deepcopy(contract)
    gate["protected_gates"].remove("Maori_authority")
    return [
        ("real_person_counter_promotion", people),
        ("authority_promotion", authority),
        ("stage20_promotion", stage),
        ("protected_gate_removal", gate),
    ]


def runner_main(expected_proposal_id: str) -> None:
    """CLI entry point shared by the ten family-current wrappers."""
    if len(sys.argv) != 2:
        print(json.dumps({"passed": False, "failures": ["one_contract_path_required"]}))
        raise SystemExit(2)
    path = Path(sys.argv[1])
    try:
        payload = load_json(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "failures": [type(exc).__name__]}))
        raise SystemExit(1)
    if payload.get("proposal_id") != expected_proposal_id:
        result = {"passed": False, "failures": ["runner_proposal_binding"]}
    else:
        result = validate_contract(payload)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
