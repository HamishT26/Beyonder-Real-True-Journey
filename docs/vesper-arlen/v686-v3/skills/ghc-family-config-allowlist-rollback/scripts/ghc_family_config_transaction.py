"""Atomic synthetic configuration transactions, allowlists, rollback, and diffs."""

from __future__ import annotations

import copy
from typing import Any

from ghc_family_config_toml import canonical, check_json, cli_main, sha


def _parts(path: str) -> list[str]:
    if not isinstance(path, str) or not path or path.startswith(".") or path.endswith(".") or ".." in path:
        raise ValueError("invalid_path")
    parts = path.split(".")
    if any(not part or not part.replace("_", "a").isalnum() for part in parts):
        raise ValueError("invalid_path")
    return parts


def _set(document: dict[str, Any], path: str, value: Any) -> None:
    parts = _parts(path)
    node: Any = document
    for part in parts[:-1]:
        if not isinstance(node, dict) or part not in node:
            raise KeyError("missing_target")
        node = node[part]
    if not isinstance(node, dict):
        raise KeyError("scalar_traversal")
    node[parts[-1]] = copy.deepcopy(value)


def _changed(before: Any, after: Any, prefix: str = "") -> list[str]:
    if type(before) is not type(after):
        return [prefix]
    if isinstance(before, dict):
        paths: list[str] = []
        for key in sorted(set(before) | set(after)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in before or key not in after:
                paths.append(path)
            else:
                paths.extend(_changed(before[key], after[key], path))
        return paths
    if isinstance(before, list):
        if len(before) != len(after):
            return [prefix]
        paths = []
        for index, (left, right) in enumerate(zip(before, after, strict=True)):
            paths.extend(_changed(left, right, f"{prefix}[{index}]"))
        return paths
    return [] if before == after else [prefix]


def evaluate(operation: str, data: dict[str, Any]) -> Any:
    original = canonical(data)
    try:
        if operation == "apply":
            document = data.get("document")
            changes = data.get("changes")
            if not isinstance(document, dict) or not isinstance(changes, list) or len(changes) > 500:
                return {"error": "invalid_changes"}
            working = copy.deepcopy(document)
            for change in changes:
                if not isinstance(change, dict) or set(change) != {"op", "path", "value"} or change["op"] != "set":
                    return {"error": "invalid_change"}
                _set(working, change["path"], change["value"])
            result = working
        elif operation == "authorize":
            allowed = data.get("allowed")
            paths = data.get("paths")
            if not isinstance(allowed, list) or not isinstance(paths, list) or not allowed or any(not isinstance(item, str) for item in allowed + paths):
                return {"error": "invalid_permissions"}
            allowed_tokens = [_parts(item) for item in allowed]
            requested = [_parts(item) for item in paths]
            if not all(any(parts[: len(prefix)] == prefix for prefix in allowed_tokens) for parts in requested):
                return {"error": "path_not_allowed"}
            result = {"authorized": True, "paths": copy.deepcopy(paths)}
        elif operation == "chain":
            snapshots = data.get("snapshots")
            links = data.get("links")
            if not isinstance(snapshots, list) or not snapshots or not isinstance(links, list) or len(links) != len(snapshots) - 1:
                return {"error": "link_count_mismatch"}
            for index, link in enumerate(links, 1):
                if not isinstance(link, dict) or link.get("ordinal") != index or link.get("parent_sha256") != sha(snapshots[index - 1]) or link.get("child_sha256") != sha(snapshots[index]) or not isinstance(link.get("reason"), str) or not link["reason"].strip():
                    return {"error": "lineage_mismatch"}
            result = {"links": len(links), "tip_sha256": sha(snapshots[-1]), "rollback_sha256": sha(snapshots[0])}
        elif operation == "diff":
            before = data.get("before")
            after = data.get("after")
            prefixes = data.get("breaking_prefixes")
            if not isinstance(prefixes, list) or any(not isinstance(item, str) for item in prefixes):
                return {"error": "invalid_diff_policy"}
            paths = _changed(before, after)
            breaking = any(any(path == prefix or path.startswith(prefix + ".") or path.startswith(prefix + "[") for prefix in prefixes) for path in paths)
            result = {"paths": paths, "classification": "breaking" if breaking else "nonbreaking"}
        else:
            result = {"error": "unknown_operation"}
    except (KeyError, ValueError, TypeError):
        result = {"error": "transaction_refused"}
    if canonical(data) != original:
        raise AssertionError("input_mutated")
    check_json(result)
    return result


if __name__ == "__main__":
    raise SystemExit(cli_main(evaluate))
