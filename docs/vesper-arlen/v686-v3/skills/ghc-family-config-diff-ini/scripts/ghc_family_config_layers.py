"""Synthetic configuration layer, origin, and immutable-snapshot contracts."""

from __future__ import annotations

import copy
from typing import Any

from ghc_family_config_toml import canonical, check_json, cli_main


def _merge(layers: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for layer in layers:
        if not isinstance(layer, dict):
            raise ValueError("invalid_layer")
        for key, value in layer.items():
            if isinstance(value, dict) and isinstance(out.get(key), dict):
                out[key] = _merge([out[key], value])
            else:
                out[key] = copy.deepcopy(value)
    return out


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(value, dict):
        return {prefix: copy.deepcopy(value)}
    out: dict[str, Any] = {}
    for key in sorted(value):
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value[key], dict):
            out.update(_flatten(value[key], path))
        else:
            out[path] = copy.deepcopy(value[key])
    return out


def evaluate(operation: str, data: dict[str, Any]) -> Any:
    original = canonical(data)
    try:
        if operation == "merge":
            layers = data.get("layers")
            precedence = data.get("precedence")
            if not isinstance(layers, list) or not isinstance(precedence, list) or len(layers) != len(precedence) or len(layers) > 32:
                return {"error": "invalid_layers"}
            result = _merge(layers)
        elif operation == "origins":
            layers = data.get("layers")
            if not isinstance(layers, list) or len(layers) > 32:
                return {"error": "invalid_layers"}
            result: dict[str, dict[str, Any]] = {}
            for layer in layers:
                if not isinstance(layer, dict) or not isinstance(layer.get("name"), str) or not isinstance(layer.get("values"), dict):
                    return {"error": "invalid_layer"}
                for path, value in _flatten(layer["values"]).items():
                    result[path] = {"value": value, "origin": layer["name"]}
        elif operation == "snapshot":
            base = data.get("base")
            changes = data.get("set")
            if not isinstance(base, dict) or not isinstance(changes, dict):
                return {"error": "invalid_snapshot"}
            before = copy.deepcopy(base)
            derived = copy.deepcopy(base)
            for key, value in changes.items():
                derived[key] = copy.deepcopy(value)
            result = {"base": before, "derived": derived, "base_unchanged": canonical(base) == canonical(before)}
        else:
            result = {"error": "unknown_operation"}
    except (ValueError, TypeError):
        result = {"error": "invalid_layers"}
    if canonical(data) != original:
        raise AssertionError("input_mutated")
    check_json(result)
    return result


if __name__ == "__main__":
    raise SystemExit(cli_main(evaluate))
