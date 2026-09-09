"""Bounded exact refinement, diffusion, and evidence operations for Neris x2."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import pairwise

from ghc_family_mesh_x1 import ContractError, fields, fstr, integer, require, scalar, values

SCHEMA = {
    "poisson_dirichlet_1d": ["intervals", "forcing", "left", "right"],
    "poisson_residual": ["values", "forcing"],
    "flux_balance": ["values", "h"],
    "richardson_extrapolate": ["coarse", "fine", "order", "refinement_ratio"],
    "adaptive_split": ["intervals", "errors", "threshold"],
    "cfl_number": ["speed", "dt", "dx"],
    "heat_step": ["values", "alpha", "fixed_boundary"],
    "discrete_energy": ["values"],
    "provenance_binding": ["record", "declared_digest"],
    "claim_reservation": ["requested_scope", "evidence_class", "execute"],
}


def tridiagonal_solution(intervals: int, forcing: Fraction, left: Fraction, right: Fraction) -> list[Fraction]:
    count = intervals - 1
    if count == 0:
        return [left, right]
    diagonal = [Fraction(2) for _ in range(count)]
    upper = [Fraction(-1) for _ in range(max(0, count - 1))]
    lower = [Fraction(-1) for _ in range(max(0, count - 1))]
    rhs = [forcing for _ in range(count)]
    rhs[0] += left
    rhs[-1] += right
    for index in range(1, count):
        factor = lower[index - 1] / diagonal[index - 1]
        diagonal[index] -= factor * upper[index - 1]
        rhs[index] -= factor * rhs[index - 1]
    solution = [Fraction() for _ in range(count)]
    solution[-1] = rhs[-1] / diagonal[-1]
    for index in range(count - 2, -1, -1):
        solution[index] = (rhs[index] - upper[index] * solution[index + 1]) / diagonal[index]
    return [left, *solution, right]


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def compute(operation: str, payload: dict) -> object:
    if operation == "poisson_dirichlet_1d":
        intervals = integer(payload["intervals"], 1, 64)
        forcing, left, right = scalar(payload["forcing"]), scalar(payload["left"]), scalar(payload["right"])
        return [fstr(item) for item in tridiagonal_solution(intervals, forcing, left, right)]
    if operation == "poisson_residual":
        row = values(payload["values"], 3)
        forcing = scalar(payload["forcing"])
        return [fstr(2 * row[index] - row[index - 1] - row[index + 1] - forcing) for index in range(1, len(row) - 1)]
    if operation == "flux_balance":
        row = values(payload["values"], 3)
        spacing = scalar(payload["h"])
        require(spacing > 0, "E_SPACING")
        flux = [(b - a) / spacing for a, b in pairwise(row)]
        interior = sum((b - a for a, b in pairwise(flux)), Fraction())
        boundary = flux[-1] - flux[0]
        return {"interior_divergence_sum": fstr(interior), "boundary_flux_difference": fstr(boundary)}
    if operation == "richardson_extrapolate":
        coarse, fine = scalar(payload["coarse"]), scalar(payload["fine"])
        order = integer(payload["order"], 1, 8)
        ratio = scalar(payload["refinement_ratio"])
        require(ratio > 1, "E_REFINEMENT_RATIO")
        factor = ratio**order
        return fstr((factor * fine - coarse) / (factor - 1))
    if operation == "adaptive_split":
        intervals = payload["intervals"]
        errors = payload["errors"]
        threshold = scalar(payload["threshold"])
        require(type(intervals) is list and type(errors) is list and 1 <= len(intervals) == len(errors) <= 64, "E_INTERVALS")
        require(threshold >= 0, "E_THRESHOLD")
        parsed = []
        previous = None
        for interval in intervals:
            require(type(interval) is list and len(interval) == 2, "E_INTERVALS")
            a, b = scalar(interval[0]), scalar(interval[1])
            require(a < b and (previous is None or a >= previous), "E_INTERVALS")
            parsed.append((a, b))
            previous = b
        indicators = [scalar(item) for item in errors]
        require(all(item >= 0 for item in indicators), "E_ERRORS")
        result = []
        for (a, b), indicator in zip(parsed, indicators):
            if indicator > threshold:
                midpoint = (a + b) / 2
                result.extend([[fstr(a), fstr(midpoint)], [fstr(midpoint), fstr(b)]])
            else:
                result.append([fstr(a), fstr(b)])
        return result
    if operation == "cfl_number":
        speed, timestep, spacing = scalar(payload["speed"]), scalar(payload["dt"]), scalar(payload["dx"])
        require(timestep >= 0 and spacing > 0, "E_CFL_DOMAIN")
        cfl = abs(speed) * timestep / spacing
        return {"cfl": fstr(cfl), "stable_under_selected_bound": cfl <= 1}
    if operation == "heat_step":
        row = values(payload["values"], 3)
        alpha = scalar(payload["alpha"])
        require(payload["fixed_boundary"] is True, "E_BOUNDARY_POLICY")
        require(0 <= alpha <= Fraction(1, 2), "E_ALPHA")
        updated = [row[0], *[row[index] + alpha * (row[index - 1] - 2 * row[index] + row[index + 1]) for index in range(1, len(row) - 1)], row[-1]]
        return [fstr(item) for item in updated]
    if operation == "discrete_energy":
        row = values(payload["values"])
        return fstr(sum(((b - a) ** 2 for a, b in pairwise(row)), Fraction()) / 2)
    if operation == "provenance_binding":
        require(type(payload["record"]) is dict, "E_RECORD")
        declared = payload["declared_digest"]
        require(type(declared) is str and len(declared) == 64 and all(char in "0123456789abcdef" for char in declared), "E_DIGEST")
        observed = canonical_digest(payload["record"])
        return {"observed_digest": observed, "matches": observed == declared, "authority_transferred": False}
    require(operation == "claim_reservation", "E_OPERATION")
    represented = {"software_example", "numerical_identity", "synthetic_mesh", "local_test", "documentation"}
    gated = {"physical_law", "credential_issuance", "public_policy", "maori_authority", "stage20"}
    scope = payload["requested_scope"]
    require(type(scope) is str and scope in represented | gated, "E_SCOPE")
    require(payload["evidence_class"] == "synthetic", "E_EVIDENCE_CLASS")
    require(payload["execute"] is False, "E_EXECUTION_RESERVED")
    return {"scope": scope, "executed": False, "disposition": "represented" if scope in represented else "exact_gate"}


def evaluate(request: object) -> dict:
    try:
        require(type(request) is dict and set(request) == {"op", "payload", "synthetic"}, "E_FIELDS")
        require(request["synthetic"] is True, "E_SYNTHETIC")
        operation = request["op"]
        require(type(operation) is str and operation in SCHEMA, "E_OPERATION")
        payload = fields(request["payload"], SCHEMA[operation])
        return {"ok": True, "value": compute(operation, payload), "error": None}
    except ContractError as error:
        return {"ok": False, "value": None, "error": str(error)}
