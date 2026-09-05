"""Synthetic configuration assurance, schema, receipt, and accessibility contracts."""

from __future__ import annotations

import re
from typing import Any

from ghc_family_config_toml import canonical, check_json, cli_main


PLACEHOLDERS = {
    "PLACEHOLDER_API_KEY",
    "REDACTED_TOKEN",
    "EXAMPLE_ONLY",
    "ENV_REFERENCE",
    "VAULT_REFERENCE",
    "EMPTY_VALUE",
    "LOCAL_FIXTURE",
    "TEST_SENTINEL",
    "DOCUMENTED_ABSENT",
}


def _bool_text(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def _type_matches(value: Any, kind: str) -> bool:
    if kind == "string":
        return isinstance(value, str)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "array":
        return isinstance(value, list)
    if kind == "object":
        return isinstance(value, dict)
    return False


def evaluate(operation: str, data: dict[str, Any]) -> Any:
    original = canonical(data)
    try:
        if operation == "update_ini":
            text = data.get("text")
            section = data.get("section")
            option = data.get("option")
            value = data.get("value")
            marker = data.get("marker")
            if not all(isinstance(item, str) for item in (text, section, option, value, marker)) or len(text.encode("utf-8")) > 65_536:
                return {"error": "invalid_ini"}
            section_match = re.search(rf"(?m)^\[{re.escape(section)}\]\s*$", text)
            option_match = re.search(rf"(?m)^{re.escape(option)}\s*=", text)
            if not section_match or not option_match:
                return {"error": "missing_target"}
            result = {"marker_preserved": marker in text, "option": option, "value": value}
        elif operation == "secret_guard":
            marker = data.get("marker")
            if not isinstance(marker, str):
                return {"error": "invalid_marker"}
            result = {"accepted_placeholder": marker in PLACEHOLDERS, "real_secret_used": False}
        elif operation == "env_overlay":
            values = data.get("values")
            schema = data.get("schema")
            allowed = data.get("allowed")
            if not isinstance(values, dict) or not isinstance(schema, dict) or not isinstance(allowed, list) or set(values) - set(allowed):
                return {"error": "environment_not_allowed"}
            result: dict[str, Any] = {}
            for key, raw in values.items():
                kind = schema.get(key)
                if not isinstance(raw, str):
                    return {"error": "invalid_environment_value"}
                if kind == "integer" and re.fullmatch(r"-?(?:0|[1-9][0-9]*)", raw):
                    result[key] = int(raw)
                elif kind == "boolean" and raw in {"true", "false"}:
                    result[key] = raw == "true"
                elif kind == "string":
                    result[key] = raw
                else:
                    return {"error": "environment_type"}
        elif operation == "schema":
            config = data.get("config")
            schema = data.get("schema")
            if not isinstance(config, dict) or not isinstance(schema, dict):
                return {"error": "invalid_schema"}
            required = schema.get("required")
            types = schema.get("types")
            additional = schema.get("additional")
            if not isinstance(required, list) or not isinstance(types, dict) or not isinstance(additional, bool):
                return {"error": "invalid_schema"}
            if any(key not in config for key in required):
                return {"error": "missing_required"}
            if not additional and set(config) - set(types):
                return {"error": "unknown_field"}
            if any(key in config and not _type_matches(config[key], kind) for key, kind in types.items()):
                return {"error": "type_mismatch"}
            result = True
        elif operation == "receipt":
            expected = data.get("expected")
            receipt = data.get("receipt")
            required = {"owner", "phase", "source", "candidate", "same_owner_only", "authority"}
            result = True if isinstance(expected, dict) and isinstance(receipt, dict) and set(expected) == set(receipt) == required and canonical(expected) == canonical(receipt) and expected["same_owner_only"] is True and expected["authority"] is False else {"error": "scope_mismatch"}
        elif operation == "summary":
            changes = data.get("changes")
            language = data.get("language")
            if not isinstance(changes, list) or language != "en-NZ" or len(changes) > 100:
                return {"error": "invalid_summary"}
            rows = []
            for change in changes:
                if not isinstance(change, dict) or set(change) != {"path", "before", "after"} or not isinstance(change["path"], str):
                    return {"error": "invalid_change"}
                rows.append(f"{change['path']}: {_bool_text(change['before'])} → {_bool_text(change['after'])}")
            result = {"heading": "Synthetic configuration changes", "rows": rows, "manual_review_reserved": True}
        else:
            result = {"error": "unknown_operation"}
    except (TypeError, ValueError, re.error):
        result = {"error": "assurance_refused"}
    if canonical(data) != original:
        raise AssertionError("input_mutated")
    check_json(result)
    return result


if __name__ == "__main__":
    raise SystemExit(cli_main(evaluate))
