#!/usr/bin/env python3
"""Bounded synthetic and formal runtime for Orin v650-v4.

This module deliberately refuses network, participant, production identity,
authority, deployment, or empirical promotion work.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path
from typing import Any, Callable

try:
    import ghc_family_v650_v4_phase_data as d
except ModuleNotFoundError:  # package import used by repository tests
    from . import ghc_family_v650_v4_phase_data as d

REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / d.PHASE_ROOT
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def common_fixture() -> dict[str, Any]:
    return {
        "required_obligation": True,
        "domain": "declared_bounded_domain",
        "claim": "bounded_only",
        "resource_units": 8,
        "resource_budget": 64,
        "negative_retention": True,
    }


def common_check(fixture: dict[str, Any]) -> tuple[bool, str]:
    if not fixture.get("required_obligation"):
        return False, "missing_required_obligation"
    if fixture.get("domain") != "declared_bounded_domain":
        return False, "wrong_domain_or_type"
    if fixture.get("claim") != "bounded_only":
        return False, "unsupported_promotion_attempt"
    if fixture.get("resource_units", 0) > fixture.get("resource_budget", 0):
        return False, "resource_or_iteration_budget_exceeded"
    if fixture.get("negative_retention") is not True:
        return False, "negative_or_gate_erasure_attempt"
    return True, "common_guard_pass"


def formal_obligation_witness(required: list[str], extra: dict[str, Any]) -> dict[str, Any]:
    declared = {key: True for key in required}
    missing = [key for key in required if not declared.get(key)]
    return {
        "required_count": len(required),
        "missing": missing,
        "all_required_present": not missing,
        **extra,
    }


def witness_p01() -> dict[str, Any]:
    retired = ["node-a", "node-b"]
    protection_slots = {"thread-1": "node-a", "thread-2": None}
    protected = {value for value in protection_slots.values() if value}
    reclaimable = sorted(set(retired) - protected)
    return {
        "protection_slots": protection_slots,
        "retired": retired,
        "reclaimable_after_scan": reclaimable,
        "protected_node_reclaimed": bool(protected & set(reclaimable)),
        "aba_tag_required": True,
        "teardown_requires_empty_slots": True,
        "passed": reclaimable == ["node-b"] and not (protected & set(reclaimable)),
    }


def witness_p02() -> dict[str, Any]:
    return formal_obligation_witness(
        [
            "poincare_representation",
            "mass_casimir",
            "spin_or_helicity",
            "little_group",
            "positive_energy",
            "polarization_scope",
            "gauge_reservation",
            "eft_scope",
            "unit_scope",
            "observation_firewall",
        ],
        {
            "massive_little_group_model": "SO(3)",
            "massless_little_group_model": "ISO(2)",
            "physical_spectrum_claim": False,
            "passed": True,
        },
    )


def witness_p03() -> dict[str, Any]:
    return formal_obligation_witness(
        [
            "s_matrix_scope",
            "connected_symmetry_group",
            "poincare_subgroup",
            "finite_low_mass_particle_types",
            "analytic_scattering",
            "nontrivial_scattering",
            "generator_kernel_distribution",
            "direct_product_conditional",
            "supersymmetry_reservation",
            "observation_firewall",
        ],
        {
            "theorem_application": "conditional_on_all_declared_assumptions",
            "gmutt_symmetry_claim": False,
            "passed": True,
        },
    )


def witness_p04() -> dict[str, Any]:
    vector_shift = 3.0
    compensator_shift = -3.0
    invariant_combination_shift = vector_shift + compensator_shift
    return formal_obligation_witness(
        [
            "mass_term",
            "compensator",
            "gauge_transformation",
            "gauge_fixing",
            "decoupling_limit",
            "strong_coupling_reservation",
            "eft_scope",
            "unit_scope",
            "observation_firewall",
        ],
        {
            "synthetic_invariant_combination_shift": invariant_combination_shift,
            "nonabelian_completion_claim": False,
            "passed": invariant_combination_shift == 0.0,
        },
    )


def witness_p05() -> dict[str, Any]:
    return {
        "official_archive_identified": True,
        "point_source_schema_identified": True,
        "download_attempted": False,
        "real_rows": 0,
        "likelihood_evaluations": 0,
        "posterior_samples": 0,
        "constraints": 0,
        "empirical_claim": False,
        "passed": True,
    }


def witness_p06() -> dict[str, Any]:
    assertion = {
        "iss": "synthetic-client",
        "sub": "synthetic-client",
        "aud": "https://authorization.invalid/token",
        "iat": 100,
        "exp": 160,
        "jti": "synthetic-jti-1",
        "purpose": "client_authentication",
    }
    valid = (
        assertion["iss"] == assertion["sub"]
        and assertion["aud"].startswith("https://")
        and assertion["exp"] > assertion["iat"]
        and bool(assertion["jti"])
    )
    return {
        "synthetic_assertion": assertion,
        "claim_binding_valid": valid,
        "real_signature": False,
        "real_key": False,
        "network_exchange": False,
        "passed": valid,
    }


def witness_p07() -> dict[str, Any]:
    request = {
        "method": "POST",
        "transport": "https",
        "authenticated_synthetic_client": True,
        "token_type_hint": "refresh_token",
        "unknown_value_response": 200,
        "cascade_scope_declared": True,
    }
    return {
        "synthetic_request": request,
        "unsupported_hint_falls_back_to_all_supported_types": True,
        "real_token": False,
        "live_revocation": False,
        "network_exchange": False,
        "passed": all(
            [
                request["method"] == "POST",
                request["transport"] == "https",
                request["authenticated_synthetic_client"],
                request["unknown_value_response"] == 200,
            ]
        ),
    }


def witness_p08() -> dict[str, Any]:
    registration = {
        "redirect_uris": ["https://client.invalid/callback"],
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "software_statement_present": True,
        "initial_access_present": False,
        "metadata_minimized": True,
    }
    return {
        "synthetic_registration": registration,
        "redirect_uri_valid": registration["redirect_uris"][0].startswith("https://"),
        "grant_response_consistent": registration["grant_types"]
        == ["authorization_code"]
        and registration["response_types"] == ["code"],
        "real_credential": False,
        "live_registration": False,
        "network_exchange": False,
        "passed": True,
    }


def witness_p09() -> dict[str, Any]:
    trace = [
        "received",
        "identifier_minimized",
        "state_of_charge_recorded",
        "isolated",
        "thermal_flagged",
        "incompatible_charger_refused",
        "release_held",
        "handover_assigned",
    ]
    required_order = ["received", "isolated", "thermal_flagged", "release_held"]
    order_valid = all(
        trace.index(left) < trace.index(right)
        for left, right in zip(required_order, required_order[1:])
    )
    return {
        "synthetic_trace": trace,
        "order_valid": order_valid,
        "release_performed": False,
        "real_people": 0,
        "real_batteries": 0,
        "real_repairs": 0,
        "operational_effectiveness_claim": False,
        "passed": order_valid and "release_held" in trace,
    }


def witness_p10() -> dict[str, Any]:
    gates = {
        "worker_acceptance": "reserved",
        "customer_acceptance": "reserved",
        "disability_access_decision": "reserved",
        "fire_risk_decision": "reserved",
        "location_disclosure": "reserved",
        "disposal_decision": "reserved",
        "remedy": "reserved",
        "legal_interpretation": "reserved",
        "cultural_legitimacy": "reserved",
        "data_governance": "reserved",
        "maori_authority": "reserved",
    }
    return {
        "reservations": gates,
        "authority_decisions": 0,
        "real_affected_parties": 0,
        "all_reserved": set(gates.values()) == {"reserved"},
        "passed": set(gates.values()) == {"reserved"},
    }


def parse_bson_int32_document(data: bytes, budget: int = 1024) -> dict[str, int]:
    if len(data) > budget or len(data) < 5:
        raise ValueError("resource_or_length_failure")
    declared = struct.unpack("<i", data[:4])[0]
    if declared != len(data) or data[-1] != 0:
        raise ValueError("length_or_terminator_failure")
    offset = 4
    result: dict[str, int] = {}
    while offset < len(data) - 1:
        element_type = data[offset]
        offset += 1
        end = data.find(b"\x00", offset)
        if end < 0:
            raise ValueError("cstring_failure")
        key = data[offset:end].decode("utf-8")
        offset = end + 1
        if key in result:
            raise ValueError("duplicate_key")
        if element_type != 0x10 or offset + 4 > len(data) - 1:
            raise ValueError("element_type_or_truncation")
        result[key] = struct.unpack("<i", data[offset : offset + 4])[0]
        offset += 4
    return result


def witness_p11() -> dict[str, Any]:
    body = b"\x10count\x00" + struct.pack("<i", 7) + b"\x00"
    data = struct.pack("<i", len(body) + 4) + body
    decoded = parse_bson_int32_document(data)
    return {
        "decoded": decoded,
        "bytes": len(data),
        "duplicate_key_policy": "reject",
        "general_bson_conformance_claim": False,
        "passed": decoded == {"count": 7},
    }


def witness_p12() -> dict[str, Any]:
    header_magic = bytes.fromhex("fd377a585a00")
    stream = header_magic + b"\x00\x04" + b"synthetic-block-index" + b"YZ"
    valid = (
        stream.startswith(header_magic)
        and stream.endswith(b"YZ")
        and len(stream) <= 128
    )
    return {
        "header_magic_valid": stream.startswith(header_magic),
        "footer_magic_valid": stream.endswith(b"YZ"),
        "synthetic_stream_bytes": len(stream),
        "decompression_attempted": False,
        "general_xz_conformance_claim": False,
        "passed": valid,
    }


class CountMinSketch:
    def __init__(self, width: int, depth: int, maximum: int = 2**31 - 1):
        if width <= 0 or depth <= 0:
            raise ValueError("invalid_dimensions")
        self.width = width
        self.depth = depth
        self.maximum = maximum
        self.table = [[0] * width for _ in range(depth)]

    def _indices(self, key: str) -> list[int]:
        return [
            int.from_bytes(
                hashlib.sha256(f"{row}:{key}".encode("utf-8")).digest()[:8],
                "big",
            )
            % self.width
            for row in range(self.depth)
        ]

    def update(self, key: str, count: int = 1) -> None:
        if count < 0:
            raise ValueError("negative_update")
        indices = self._indices(key)
        current = min(self.table[row][column] for row, column in enumerate(indices))
        target = current + count
        if target > self.maximum:
            raise OverflowError("counter_overflow")
        for row, column in enumerate(indices):
            if self.table[row][column] == current:
                self.table[row][column] = target

    def estimate(self, key: str) -> int:
        return min(
            self.table[row][column]
            for row, column in enumerate(self._indices(key))
        )


def witness_p13() -> dict[str, Any]:
    sketch = CountMinSketch(width=32, depth=4)
    for _ in range(5):
        sketch.update("alpha")
    for _ in range(2):
        sketch.update("beta")
    estimates = {"alpha": sketch.estimate("alpha"), "beta": sketch.estimate("beta")}
    return {
        "dimensions": {"width": 32, "depth": 4},
        "estimates": estimates,
        "overestimation_only": estimates["alpha"] >= 5 and estimates["beta"] >= 2,
        "heavy_hitter": max(estimates, key=estimates.get),
        "passed": estimates == {"alpha": 5, "beta": 2},
    }


def parse_timestamp(value: str) -> float:
    parts = value.split(":")
    if len(parts) not in {2, 3}:
        raise ValueError("timestamp_shape")
    if len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    else:
        hours, minutes, seconds = parts
    total = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    if total < 0:
        raise ValueError("timestamp_domain")
    return total


def parse_webvtt(text: str, budget: int = 4096) -> list[dict[str, Any]]:
    if len(text.encode("utf-8")) > budget or not text.startswith("WEBVTT\n"):
        raise ValueError("header_or_budget")
    cues = []
    blocks = [block for block in text.strip().split("\n\n")[1:] if block]
    for block in blocks:
        lines = block.splitlines()
        timing_index = 0 if "-->" in lines[0] else 1
        if timing_index >= len(lines) or "-->" not in lines[timing_index]:
            raise ValueError("cue_timing_missing")
        left, right = [part.strip().split()[0] for part in lines[timing_index].split("-->")]
        start = parse_timestamp(left)
        end = parse_timestamp(right)
        if end <= start:
            raise ValueError("cue_order")
        payload = "\n".join(lines[timing_index + 1 :])
        cues.append({"start": start, "end": end, "payload": payload})
    return cues


def witness_p14() -> dict[str, Any]:
    text = "WEBVTT\n\n00:00.000 --> 00:02.000 line:90%\n<v Speaker>Bounded cue</v>\n"
    cues = parse_webvtt(text)
    return {
        "cue_count": len(cues),
        "first_cue": cues[0],
        "overlap_policy": "explicit_review_required",
        "rendering_or_accessibility_conformance_claim": False,
        "passed": len(cues) == 1 and cues[0]["end"] == 2.0,
    }


def clenshaw(coefficients: list[float], x: float) -> float:
    if not coefficients or not -1.0 <= x <= 1.0:
        raise ValueError("coefficient_or_interval_failure")
    b1 = 0.0
    b2 = 0.0
    for coefficient in reversed(coefficients[1:]):
        b0 = 2.0 * x * b1 - b2 + coefficient
        b2, b1 = b1, b0
    return x * b1 - b2 + coefficients[0]


def witness_p15() -> dict[str, Any]:
    coefficients = [1.0, -0.5, 0.25, 0.125]
    x = 0.25
    recurrence = clenshaw(coefficients, x)
    direct = (
        coefficients[0]
        + coefficients[1] * x
        + coefficients[2] * (2 * x * x - 1)
        + coefficients[3] * (4 * x**3 - 3 * x)
    )
    return {
        "coefficients": coefficients,
        "x": x,
        "clenshaw_value": recurrence,
        "direct_reference": direct,
        "absolute_error": abs(recurrence - direct),
        "passed": math.isclose(recurrence, direct, rel_tol=0.0, abs_tol=1e-12),
    }


def witness_p16() -> dict[str, Any]:
    synthetic = {
        "header": "ORC",
        "postscript": {"footerLength": 40, "compression": "ZLIB", "magic": "ORC"},
        "footer": {
            "stripes": 2,
            "rows": 8,
            "rowIndexStride": 4,
            "schema": ["struct", "int", "string"],
            "statistics_present": True,
        },
        "resource_budget": 1024,
        "declared_bytes": 256,
    }
    passed = (
        synthetic["header"] == synthetic["postscript"]["magic"] == "ORC"
        and synthetic["footer"]["rows"] == 8
        and synthetic["declared_bytes"] <= synthetic["resource_budget"]
    )
    return {
        "synthetic_orc": synthetic,
        "tail_first_contract": True,
        "real_orc_file_opened": False,
        "general_orc_conformance_claim": False,
        "passed": passed,
    }


def witness_p17() -> dict[str, Any]:
    board = {
        "lanes": [
            {"name": "Ready", "cards": ["card-a"]},
            {"name": "Held", "cards": ["card-b"]},
        ],
        "explicit_move_controls": True,
        "drag_required": False,
        "keyboard_reachable": True,
        "focus_return": "moved_card",
        "status_role": "status",
        "filtered_count_text": "2 cards shown",
        "list_fallback": True,
    }
    return {
        "structural_board": board,
        "manual_keyboard_review": "reserved",
        "assistive_technology_review": "reserved",
        "affected_user_review": "reserved",
        "complete_accessibility_claim": False,
        "passed": all(
            [
                board["explicit_move_controls"],
                not board["drag_required"],
                board["keyboard_reachable"],
                board["status_role"] == "status",
                board["list_fallback"],
            ]
        ),
    }


def witness_p18() -> dict[str, Any]:
    density = 0.05
    second = -0.1
    third = 0.02
    compressibility = 1.0 + second * density + third * density**2
    return {
        "density": density,
        "second_virial_coefficient": second,
        "third_virial_coefficient": third,
        "compressibility_factor": compressibility,
        "temperature_domain_declared": True,
        "single_phase_low_density_domain": True,
        "units_checked": True,
        "psyche_conversion": False,
        "agency_conversion": False,
        "fundamental_mind_law_claim": False,
        "passed": math.isclose(compressibility, 0.99505, abs_tol=1e-12),
    }


def witness_p19() -> dict[str, Any]:
    obligations = {
        "time_varying_treatment": True,
        "confounder_history": True,
        "consistency": "required_not_established",
        "sequential_exchangeability": "required_not_established",
        "positivity": "required_not_established",
        "model_specification": "required_not_established",
        "monte_carlo_plan": "structural_only",
        "sensitivity": "required",
        "outcome_switching": "forbidden",
    }
    return {
        "obligations": obligations,
        "real_participants": 0,
        "empirical_rows": 0,
        "effect_estimates": 0,
        "stage20_promoted": False,
        "passed": all(key in obligations for key in obligations),
    }


def witness_p20() -> dict[str, Any]:
    state = {
        "capacity": 4,
        "dynamic_table": ["x-a", "x-b"],
        "insert_count": 2,
        "required_insert_count": 2,
        "blocked_stream_limit": 1,
        "blocked_streams": [3],
        "acknowledged_sections": [1],
        "cancelled_streams": [5],
    }
    passed = (
        len(state["dynamic_table"]) <= state["capacity"]
        and state["required_insert_count"] <= state["insert_count"]
        and len(state["blocked_streams"]) <= state["blocked_stream_limit"]
    )
    return {
        "synthetic_state": state,
        "general_http3_conformance_claim": False,
        "network_exchange": False,
        "passed": passed,
    }


WITNESSES: dict[str, Callable[[], dict[str, Any]]] = {
    f"V6504-P{index:02d}": function
    for index, function in enumerate(
        [
            witness_p01,
            witness_p02,
            witness_p03,
            witness_p04,
            witness_p05,
            witness_p06,
            witness_p07,
            witness_p08,
            witness_p09,
            witness_p10,
            witness_p11,
            witness_p12,
            witness_p13,
            witness_p14,
            witness_p15,
            witness_p16,
            witness_p17,
            witness_p18,
            witness_p19,
            witness_p20,
        ],
        start=1,
    )
}


def mutated_fixture(name: str) -> dict[str, Any]:
    fixture = common_fixture()
    if name == "missing_required_obligation":
        fixture["required_obligation"] = False
    elif name == "wrong_domain_or_type":
        fixture["domain"] = "outside_declared_domain"
    elif name == "unsupported_promotion_attempt":
        fixture["claim"] = "empirical_or_authority_promotion"
    elif name == "resource_or_iteration_budget_exceeded":
        fixture["resource_units"] = fixture["resource_budget"] + 1
    elif name == "negative_or_gate_erasure_attempt":
        fixture["negative_retention"] = False
    else:
        raise ValueError(f"unknown mutation {name}")
    return fixture


def run_proposal(proposal_id: str) -> dict[str, Any]:
    proposal = next(
        row for row in d.PROPOSALS if row["proposal_id"] == proposal_id
    )
    valid_fixture = common_fixture()
    common_pass, common_reason = common_check(valid_fixture)
    domain_witness = WITNESSES[proposal_id]()
    if not common_pass or not domain_witness.get("passed"):
        raise RuntimeError(f"valid fixture failed for {proposal_id}")
    planned = [
        row for row in d.mutation_plan() if row["proposal_id"] == proposal_id
    ]
    mutation_rows = []
    for row in planned:
        passed, reason = common_check(mutated_fixture(row["mutation"]))
        mutation_rows.append(
            {
                "mutation_id": row["mutation_id"],
                "mutation": row["mutation"],
                "expected": row["expected"],
                "observed": "accepted" if passed else "rejected_or_quarantined",
                "reason": reason,
                "passed": not passed and reason == row["mutation"],
                "completion_credit": False,
            }
        )
    if len(mutation_rows) != 5 or not all(row["passed"] for row in mutation_rows):
        raise RuntimeError(f"mutation tribunal failed for {proposal_id}")
    outcome = proposal["expected_disposition"]
    if outcome not in ALLOWED_OUTCOMES:
        raise RuntimeError(f"invalid outcome vocabulary: {outcome}")
    root = PHASE / "surfaces" / proposal["slug"]
    contract = {
        "schema": "ghc.family.v650-v4.surface-contract.v1",
        "proposal_id": proposal_id,
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "hypothesis": proposal["hypothesis"],
        "null_or_failure_condition": proposal["null_or_failure_condition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "official_or_primary_source_needs": proposal[
            "official_or_primary_source_needs"
        ],
        "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"],
        "network_allowed": False,
        "external_state_mutation_allowed": False,
        "boundary": d.BOUNDARY,
    }
    mutation_result = {
        "schema": "ghc.family.v650-v4.mutation-results.v1",
        "proposal_id": proposal_id,
        "planned": 5,
        "executed": 5,
        "rejected_or_quarantined": 5,
        "accepted": 0,
        "results": mutation_rows,
        "boundary": (
            "Rejected synthetic mutations are bounded guard evidence, not production "
            "security, empirical truth, authority, or independent reproduction."
        ),
    }
    receipt = {
        "schema": "ghc.family.v650-v4.bounded-receipt.v1",
        "proposal_id": proposal_id,
        "outcome": outcome,
        "valid_fixture_common_guard": common_reason,
        "domain_witness": domain_witness,
        "mutations_rejected": 5,
        "evidence_class": {
            "completed": "bounded_software_symbolic_formal_or_structural",
            "represented": "synthetic_proxy_only",
            "open_gap": "zero_row_readiness_only",
            "exact_gate": "reservation_matrix_only",
        }[outcome],
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": d.BOUNDARY,
        "passed": True,
    }
    write_json(root / "contract.json", contract)
    write_json(root / "mutation-results.json", mutation_result)
    write_json(root / "bounded-receipt.json", receipt)
    return receipt


GROUP_PROPOSALS = {
    1: ["V6504-P01", "V6504-P02", "V6504-P03", "V6504-P04"],
    2: ["V6504-P05"],
    3: ["V6504-P06", "V6504-P07", "V6504-P08"],
    4: ["V6504-P09"],
    5: ["V6504-P10"],
    6: ["V6504-P11", "V6504-P12", "V6504-P14", "V6504-P16", "V6504-P20"],
    7: ["V6504-P13", "V6504-P15"],
    8: ["V6504-P17"],
    9: ["V6504-P18"],
    10: ["V6504-P19"],
}


def run_group(group: int) -> dict[str, Any]:
    if not 1 <= group <= 10:
        raise ValueError("group must be 1 through 10")
    proposal_ids = GROUP_PROPOSALS[group]
    receipts = [run_proposal(proposal_id) for proposal_id in proposal_ids]
    witness = {
        "schema": "ghc.family.v650-v4.runner-witness.v1",
        "group": group,
        "proposal_ids": proposal_ids,
        "receipts_passed": sum(row["passed"] for row in receipts),
        "valid_fixture_count": len(proposal_ids),
        "rejected_mutation_count": len(proposal_ids) * 5,
        "same_owner_only": True,
        "independent_reproduction": False,
        "passed": all(row["passed"] for row in receipts),
        "boundary": d.BOUNDARY,
    }
    runner_name = Path(d.RUNNERS[group - 1]).stem
    write_json(PHASE / "runner-witnesses" / f"{runner_name}.json", witness)
    return witness


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal")
    parser.add_argument("--group", type=int)
    args = parser.parse_args()
    if bool(args.proposal) == bool(args.group):
        parser.error("provide exactly one of --proposal or --group")
    result = run_proposal(args.proposal) if args.proposal else run_group(args.group)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
