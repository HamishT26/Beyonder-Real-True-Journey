"""Bounded CBR authority, GMUT evidence, and THOS operational reservations."""

from __future__ import annotations

from ghc_family_policy_resolution import ContractError, bounded_json, cli, fields, no, ok, require

OPERATIONS = ("cbr_authority_gate", "gmut_evidence_gap", "thos_operational_readback")

AUTHORITY = {
    "disclosure": "affected_party_consent",
    "correction": "competent_correction_authority",
    "retention": "governance_authority",
    "credential": "credential_owner_authority",
    "accessibility": "affected_user_accessibility_review",
    "professional": "qualified_professional_review",
    "legal": "competent_legal_authority",
    "maori_language": "maori_language_authority",
    "iwi_data": "iwi_authority",
    "hapu_stewardship": "hapu_authority",
}
EVIDENCE = {
    "apparatus": "independent_apparatus_observation",
    "calibration": "traceable_calibration_evidence",
    "units": "validated_measurement_model",
    "sampling": "observed_sampling_protocol",
    "missingness": "missingness_evidence",
    "covariance": "measured_uncertainty_covariance",
    "blind_comparator": "blind_matched_comparator",
    "causality": "causal_identification_evidence",
    "reproduction": "independent_reproduction",
    "discrimination": "empirical_model_discrimination",
}
OPERATIONAL = {
    "cutover": "authorized_operator_execution",
    "rollback": "real_recovery_observation",
    "parallel": "live_matched_comparison",
    "capacity": "measured_capacity_under_load",
    "notice": "affected_recipient_delivery",
    "checkpoint": "competent_operational_acceptance",
    "freeze": "authorized_service_state",
    "archive": "retention_owner_decision",
    "dependencies": "production_review",
    "handover": "operator_acknowledgement",
}


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        fields(payload, ("topic",))
        topic = payload["topic"]
        require(type(topic) is str, "INVALID_TOPIC")
        if operation == "cbr_authority_gate":
            require(topic in AUTHORITY, "UNKNOWN_TOPIC")
            return ok({"authorized": False, "gate_open": True, "required_authority": [AUTHORITY[topic]]})
        if operation == "gmut_evidence_gap":
            require(topic in EVIDENCE, "UNKNOWN_TOPIC")
            return ok({"empirical": False, "gate_open": True, "missing": [EVIDENCE[topic]]})
        if operation == "thos_operational_readback":
            require(topic in OPERATIONAL, "UNKNOWN_TOPIC")
            return ok({"production": False, "execution_authorized": False, "missing": [OPERATIONAL[topic]]})
        raise ContractError("UNKNOWN_OPERATION")
    except ContractError as exc:
        return no(str(exc))


if __name__ == "__main__":
    raise SystemExit(cli(evaluate))
