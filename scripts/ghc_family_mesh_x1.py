"""Bounded exact one-dimensional grid and finite-difference operations.

The module reads no frozen proposal table. It evaluates explicit synthetic
payloads with rational arithmetic and keeps empirical and authority claims out
of the result surface.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import pairwise


class ContractError(ValueError):
    """Typed refusal for the bounded public contract."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ContractError(code)


def scalar(value: object) -> Fraction:
    require(type(value) in (int, str), "E_SCALAR")
    if type(value) is int:
        require(abs(value) <= 1_000_000, "E_SCALAR")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ContractError("E_SCALAR") from None
    require(abs(result) <= 1_000_000, "E_SCALAR")
    return result


def integer(value: object, minimum: int = 0, maximum: int = 64) -> int:
    require(type(value) is int and minimum <= value <= maximum, "E_INTEGER")
    return value


def fstr(value: Fraction | int) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fields(payload: object, names: list[str]) -> dict:
    require(type(payload) is dict, "E_PAYLOAD")
    require(set(payload) == set(names), "E_PAYLOAD_FIELDS")
    return payload


def values(value: object, minimum: int = 2) -> list[Fraction]:
    require(type(value) is list and minimum <= len(value) <= 65, "E_VECTOR")
    return [scalar(item) for item in value]


def positive_spacing(payload: dict) -> Fraction:
    spacing = scalar(payload["h"])
    require(spacing > 0, "E_SPACING")
    return spacing


SCHEMA = {
    "uniform_grid": ["start", "stop", "intervals"],
    "cell_widths": ["nodes"],
    "linear_interpolate": ["x0", "x1", "y0", "y1", "x"],
    "forward_difference": ["values", "h"],
    "backward_difference": ["values", "h"],
    "central_difference": ["values", "h"],
    "second_difference": ["values", "h"],
    "trapezoid_integral": ["values", "h"],
    "l1_grid_error": ["approx", "exact"],
    "observed_order": ["errors", "refinement_ratio"],
}


def compute(operation: str, payload: dict) -> object:
    if operation == "uniform_grid":
        start, stop = scalar(payload["start"]), scalar(payload["stop"])
        intervals = integer(payload["intervals"], 1, 64)
        require(stop > start, "E_INTERVAL")
        width = (stop - start) / intervals
        return [fstr(start + index * width) for index in range(intervals + 1)]
    if operation == "cell_widths":
        nodes = values(payload["nodes"])
        widths = [b - a for a, b in pairwise(nodes)]
        require(all(width > 0 for width in widths), "E_MONOTONE")
        return [width.numerator if width.denominator == 1 else fstr(width) for width in widths]
    if operation == "linear_interpolate":
        x0, x1 = scalar(payload["x0"]), scalar(payload["x1"])
        y0, y1, x = scalar(payload["y0"]), scalar(payload["y1"]), scalar(payload["x"])
        require(x1 > x0 and x0 <= x <= x1, "E_INTERPOLATION_DOMAIN")
        return fstr(y0 + (x - x0) * (y1 - y0) / (x1 - x0))
    if operation in {"forward_difference", "backward_difference", "central_difference", "second_difference", "trapezoid_integral"}:
        row = values(payload["values"], 3 if operation in {"central_difference", "second_difference"} else 2)
        spacing = positive_spacing(payload)
        if operation == "forward_difference":
            return [fstr((b - a) / spacing) for a, b in pairwise(row)]
        if operation == "backward_difference":
            return [fstr((row[index] - row[index - 1]) / spacing) for index in range(1, len(row))]
        if operation == "central_difference":
            return [fstr((row[index + 1] - row[index - 1]) / (2 * spacing)) for index in range(1, len(row) - 1)]
        if operation == "second_difference":
            return [fstr((row[index - 1] - 2 * row[index] + row[index + 1]) / (spacing * spacing)) for index in range(1, len(row) - 1)]
        return fstr(spacing * (row[0] / 2 + sum(row[1:-1], Fraction()) + row[-1] / 2))
    if operation == "l1_grid_error":
        approx, exact = values(payload["approx"]), values(payload["exact"])
        require(len(approx) == len(exact), "E_VECTOR_LENGTH")
        return fstr(sum((abs(a - b) for a, b in zip(approx, exact)), Fraction()) / len(exact))
    require(operation == "observed_order", "E_OPERATION")
    errors = values(payload["errors"], 3)
    require(len(errors) == 3 and all(error > 0 for error in errors), "E_ERRORS")
    ratio = scalar(payload["refinement_ratio"])
    require(ratio > 1, "E_REFINEMENT_RATIO")
    error_ratios = [errors[0] / errors[1], errors[1] / errors[2]]
    orders = []
    for observed in error_ratios:
        order = next((candidate for candidate in range(1, 9) if ratio ** candidate == observed), None)
        require(order is not None, "E_ORDER_EXACT")
        orders.append(fstr(order))
    return {"error_ratios": [fstr(item) for item in error_ratios], "orders": orders}


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
