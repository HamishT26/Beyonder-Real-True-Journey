"""Typed synthetic Noether/symplectic obligation board for Ilyra v670-v2.

This module validates structure only. It does not solve field equations, ingest
observations, fit parameters, or establish any physical claim.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

REQUIRED = {
    "board_id",
    "lagrangian",
    "fields",
    "variation",
    "symmetry_generator",
    "euler_lagrange",
    "symplectic_potential",
    "symplectic_current",
    "noether_current",
    "constraint_term",
    "boundary_term",
    "units",
    "domain",
    "truncation",
    "observation_firewall",
    "real_rows",
    "likelihood_calls",
    "external_actions",
}


class ObligationError(ValueError):
    """Raised when a bounded obligation is absent or promoted."""


def positive_fixture() -> dict[str, Any]:
    return {
        "board_id": "synthetic-noether-board-01",
        "lagrangian": {"symbol": "L", "form_degree": "n", "status": "declared_not_solved"},
        "fields": [{"symbol": "phi", "domain": "formal_configuration_space"}],
        "variation": {"identity": "delta_L_equals_E_delta_phi_plus_d_theta", "proved_here": False},
        "symmetry_generator": {"symbol": "xi", "field_dependent": "reserved"},
        "euler_lagrange": {"symbol": "E", "on_shell_conversion": "prohibited"},
        "symplectic_potential": {"symbol": "theta", "ambiguity": "exact_form_reserved"},
        "symplectic_current": {"symbol": "omega", "antisymmetric": True, "flux": "reserved"},
        "noether_current": {"symbol": "J_xi", "decomposition": "constraint_plus_exact_reserved"},
        "constraint_term": {"symbol": "C_xi", "surface": "declared_not_solved"},
        "boundary_term": {"symbol": "Q_xi", "integrability": "unproved"},
        "units": {"system": "SI_when_dimensionful", "dimensionless_symbols_declared": True},
        "domain": {"model": "typed_scalar_tensor_EFT_research_family", "physical_solution": False},
        "truncation": {"order": "declared_symbolic", "regulator": "reserved", "closure": "unproved"},
        "observation_firewall": {
            "symbolic_is_not_empirical": True,
            "prediction": False,
            "parameter_constraint": False,
            "theory_of_everything": False,
            "stage20": False,
        },
        "real_rows": 0,
        "likelihood_calls": 0,
        "external_actions": 0,
    }


def validate_board(board: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(board, dict):
        raise ObligationError("board must be an object")
    missing = sorted(REQUIRED - board.keys())
    if missing:
        raise ObligationError(f"missing obligations: {missing}")
    if not board["fields"]:
        raise ObligationError("at least one formal field declaration is required")
    if board["symplectic_current"].get("antisymmetric") is not True:
        raise ObligationError("symplectic antisymmetry obligation is missing")
    if board["boundary_term"].get("integrability") not in {"unproved", "refused", "reserved"}:
        raise ObligationError("integrability cannot be promoted")
    firewall = board["observation_firewall"]
    if firewall.get("symbolic_is_not_empirical") is not True:
        raise ObligationError("symbolic-to-empirical firewall is missing")
    if any(firewall.get(key) is not False for key in ("prediction", "parameter_constraint", "theory_of_everything", "stage20")):
        raise ObligationError("observation or promotion claim is prohibited")
    if any(board[key] != 0 for key in ("real_rows", "likelihood_calls", "external_actions")):
        raise ObligationError("real rows, likelihood calls, and external actions must remain zero")
    return {
        "accepted": True,
        "board_id": board["board_id"],
        "obligation_count": len(REQUIRED),
        "integrability": board["boundary_term"]["integrability"],
        "physical_claim": False,
        "boundary": "typed symbolic obligation evidence only",
    }


def rejecting_fixtures() -> list[dict[str, Any]]:
    fixtures = []
    for mutator in (
        lambda row: row.pop("domain"),
        lambda row: row["observation_firewall"].update({"prediction": True}),
        lambda row: row.update({"real_rows": 1}),
        lambda row: row["boundary_term"].update({"integrability": "proved"}),
    ):
        row = deepcopy(positive_fixture())
        mutator(row)
        fixtures.append(row)
    return fixtures
