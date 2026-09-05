"""Bounded TOML contracts and shared Vesper v686-v3 evidence helpers."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import math
import tomllib
from pathlib import Path
from typing import Any, Callable


HASH_DOMAIN = "sorted compact UTF-8 JSON with exact JSON types"
MAX_DEPTH = 64
MAX_NODES = 10_000
MAX_TEXT_BYTES = 65_536


class Refusal(ValueError):
    """Bounded input refusal."""


def check_json(value: Any, depth: int = 0, counter: list[int] | None = None) -> None:
    if counter is None:
        counter = [0]
    counter[0] += 1
    if counter[0] > MAX_NODES:
        raise Refusal("node_budget")
    if depth > MAX_DEPTH:
        raise Refusal("depth_budget")
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise Refusal("nonfinite_number")
        return
    if isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise Refusal("invalid_unicode") from exc
        return
    if isinstance(value, list):
        for item in value:
            check_json(item, depth + 1, counter)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise Refusal("nonstring_key")
            check_json(key, depth + 1, counter)
            check_json(item, depth + 1, counter)
        return
    raise Refusal("unsupported_json_type")


def canonical(value: Any) -> bytes:
    check_json(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_load(text: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise Refusal("duplicate_json_member")
            out[key] = value
        return out

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_constant=lambda _value: (_ for _ in ()).throw(Refusal("nonfinite_number")),
        )
    except Refusal:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise Refusal("invalid_json") from exc
    check_json(value)
    return value


def json_safe(value: Any) -> Any:
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return value


def _flatten_shape(value: Any, prefix: str = "") -> tuple[list[str], int]:
    paths: list[str] = []
    tables = 0
    if isinstance(value, dict):
        if prefix:
            tables += 1
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else key
            child_paths, child_tables = _flatten_shape(value[key], path)
            paths.extend(child_paths)
            tables += child_tables
        if not value and prefix:
            paths.append(prefix)
    elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
        for index, item in enumerate(value):
            child_paths, child_tables = _flatten_shape(item, f"{prefix}[{index}]")
            paths.extend(child_paths)
            tables += child_tables
    else:
        paths.append(prefix)
    return paths, tables


def _set_path(document: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".") if path else []
    if not parts:
        raise Refusal("invalid_path")
    node: Any = document
    for part in parts[:-1]:
        if not isinstance(node, dict) or part not in node:
            raise Refusal("missing_target")
        node = node[part]
    if not isinstance(node, dict):
        raise Refusal("scalar_traversal")
    node[parts[-1]] = copy.deepcopy(value)


def evaluate(operation: str, data: dict[str, Any]) -> Any:
    original = canonical(data)
    try:
        if operation == "parse":
            text = data.get("text")
            budget = data.get("byte_budget")
            if not isinstance(text, str) or isinstance(budget, bool) or not isinstance(budget, int) or budget < 0 or budget > MAX_TEXT_BYTES:
                return {"error": "invalid_toml"}
            if len(text.encode("utf-8")) > budget:
                return {"error": "text_budget"}
            try:
                result = json_safe(tomllib.loads(text))
                check_json(result)
            except (tomllib.TOMLDecodeError, Refusal, ValueError, TypeError, UnicodeError):
                result = {"error": "invalid_toml"}
        elif operation == "roundtrip":
            text = data.get("text")
            path = data.get("path")
            marker = data.get("marker")
            if not all(isinstance(item, str) for item in (text, path, marker)):
                return {"error": "invalid_roundtrip"}
            try:
                parsed = json_safe(tomllib.loads(text))
                _set_path(parsed, path, data.get("value"))
            except (tomllib.TOMLDecodeError, Refusal, ValueError, TypeError):
                return {"error": "invalid_roundtrip"}
            result = {"marker_preserved": marker in text, "updated_value": copy.deepcopy(data.get("value"))}
        elif operation == "shape":
            text = data.get("text")
            if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_TEXT_BYTES:
                return {"error": "invalid_toml"}
            try:
                parsed = json_safe(tomllib.loads(text))
            except (tomllib.TOMLDecodeError, ValueError, TypeError):
                return {"error": "invalid_toml"}
            paths, table_count = _flatten_shape(parsed)
            result = {"paths": sorted(paths), "table_count": table_count}
        else:
            result = {"error": "unknown_operation"}
    finally:
        if canonical(data) != original:
            raise AssertionError("input_mutated")
    check_json(result)
    return result


def envelope(row: dict[str, Any], result: Any) -> dict[str, Any]:
    return {
        "proposal_id": row["proposal_id"],
        "definition_sha256": row["definition_sha256"],
        "input_sha256": sha(row["input"]),
        "result": copy.deepcopy(result),
        "result_sha256": sha(result),
        "hash_domain": HASH_DOMAIN,
        "disposition": row["expected_execution_disposition"],
        "empirical": False,
        "authority": False,
        "same_owner_only": True,
    }


def verify_envelope(
    row: dict[str, Any],
    record: dict[str, Any],
    evaluator: Callable[[str, dict[str, Any]], Any],
) -> dict[str, Any]:
    issues: list[str] = []
    allowed = {
        "proposal_id",
        "definition_sha256",
        "input_sha256",
        "result",
        "result_sha256",
        "hash_domain",
        "disposition",
        "empirical",
        "authority",
        "same_owner_only",
    }
    if set(record) != allowed:
        issues.append("envelope_shape")
    if record.get("proposal_id") != row["proposal_id"]:
        issues.append("proposal_id")
    if record.get("definition_sha256") != row["definition_sha256"]:
        issues.append("definition_digest")
    if record.get("input_sha256") != sha(row["input"]):
        issues.append("input_digest")
    try:
        expected = evaluator(row["operation"], copy.deepcopy(row["input"]))
    except Exception:
        expected = {"error": "evaluation_failure"}
    if canonical(record.get("result")) != canonical(expected):
        issues.append("result_value")
    if record.get("result_sha256") != sha(record.get("result")):
        issues.append("result_digest")
    if record.get("hash_domain") != HASH_DOMAIN:
        issues.append("hash_domain")
    if record.get("disposition") != row["expected_execution_disposition"]:
        issues.append("disposition")
    if record.get("empirical") is not False:
        issues.append("empirical_promotion")
    if record.get("authority") is not False:
        issues.append("authority_promotion")
    if record.get("same_owner_only") is not True:
        issues.append("same_owner_scope")
    return {"accepted": not issues, "issues": issues}


def cli_main(evaluator: Callable[[str, dict[str, Any]], Any]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        data = strict_load(args.input.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise Refusal("input_not_object")
        result = evaluator(args.operation, data)
    except (OSError, Refusal, UnicodeError) as exc:
        result = {"error": exc.args[0] if exc.args else "input_refused"}
    payload = {"result": result, "same_owner_only": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    return 2 if isinstance(result, dict) and set(result) == {"error"} else 0


if __name__ == "__main__":
    raise SystemExit(cli_main(evaluate))
