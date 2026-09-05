"""Fail-closed THOS, GMUT, and CBR configuration obligation projection."""

from __future__ import annotations

from typing import Any

from ghc_family_config_toml import canonical, check_json, cli_main


ALLOWED = {"represented", "open_gap", "exact_gate"}


def evaluate(operation: str, data: dict[str, Any]) -> Any:
    original = canonical(data)
    if operation != "obligation":
        result: Any = {"error": "unknown_operation"}
    elif set(data) != {"obligation", "evidence", "authority", "external_action", "expected_disposition"}:
        result = {"error": "invalid_obligation"}
    elif not isinstance(data.get("obligation"), str) or not data["obligation"].strip():
        result = {"error": "invalid_obligation"}
    elif data.get("external_action") is not False:
        result = {"error": "unsupported_promotion"}
    elif data.get("evidence") is not None or data.get("authority") is not None:
        result = {"error": "unsupported_promotion"}
    elif data.get("expected_disposition") not in ALLOWED:
        result = {"error": "invalid_disposition"}
    else:
        result = data["expected_disposition"]
    if canonical(data) != original:
        raise AssertionError("input_mutated")
    check_json(result)
    return result


if __name__ == "__main__":
    raise SystemExit(cli_main(evaluate))
