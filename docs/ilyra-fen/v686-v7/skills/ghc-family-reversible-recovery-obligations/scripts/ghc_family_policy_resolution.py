"""Bounded policy decisions plus shared Ilyra JSON and CLI contracts."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys

OPERATIONS = (
    "policy_decision_intersection",
    "scope_conjunction",
    "revocation_precedence",
    "authority_abstention",
)
HASH_DOMAIN = "compact UTF-8 sorted-key finite JSON"


class ContractError(ValueError):
    """A deliberate bounded refusal."""


def require(condition, reason):
    if not condition:
        raise ContractError(reason)


def canonical(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def bounded_json(value, max_depth=16, max_nodes=2000, max_bytes=65536):
    stack = [(value, 1)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        require(depth <= max_depth and count <= max_nodes, "INPUT_BUDGET")
        if type(item) is dict:
            require(all(type(k) is str for k in item), "NON_TEXT_KEY")
            stack.extend((v, depth + 1) for v in item.values())
        elif type(item) is list:
            stack.extend((v, depth + 1) for v in item)
        else:
            require(item is None or type(item) in (str, bool, int, float), "NON_JSON_VALUE")
            require(type(item) is not float or math.isfinite(item), "NONFINITE_VALUE")
    require(len(canonical(value)) <= max_bytes, "INPUT_BUDGET")


def fields(payload, names):
    require(type(payload) is dict and set(payload) == set(names), "INVALID_FIELDS")


def ok(value):
    bounded_json(value)
    return {"ok": True, "value": copy.deepcopy(value)}


def no(reason):
    return {"ok": False, "reason": reason}


def strict_loads(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, "DUPLICATE_KEY")
            result[key] = value
        return result

    def constant(_value):
        raise ContractError("INVALID_JSON")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ContractError("INVALID_JSON") from exc


def make_report(proposal, result, context):
    fields(context, ("owner", "phase", "source", "x1"))
    definition = dict(proposal)
    claimed = definition.pop("definition_sha256")
    require(digest(definition) == claimed, "INVALID_DEFINITION_BINDING")
    bounded_json(result)
    report = {
        "schema": "ghc.family.policy-report.v1",
        **context,
        "proposal_id": proposal["proposal_id"],
        "operation": proposal["operation"],
        "runner": proposal["runner"],
        "definition_sha256": claimed,
        "input_sha256": digest(proposal["input"]),
        "result": copy.deepcopy(result),
        "result_sha256": digest(result),
        "disposition": proposal["expected_execution_disposition"],
        "hash_domain": HASH_DOMAIN,
        "synthetic": True,
        "empirical": False,
        "authority": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    report["report_sha256"] = digest(report)
    return report


def verify_report(proposal, report, context):
    try:
        bounded_json(report)
        return canonical(report) == canonical(make_report(proposal, proposal["expected_result"], context))
    except (ContractError, KeyError, TypeError, ValueError, UnicodeError):
        return False


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == "policy_decision_intersection":
            fields(payload, ("decisions",))
            decisions = payload["decisions"]
            require(type(decisions) is list, "INVALID_DECISION")
            require(all(x in {"allow", "deny", "abstain"} for x in decisions), "INVALID_DECISION")
            decision = "deny" if "deny" in decisions else "allow" if decisions and set(decisions) == {"allow"} else "abstain"
            return ok({"decision": decision, "inputs": decisions})
        if operation == "scope_conjunction":
            fields(payload, ("scopes",))
            scopes = payload["scopes"]
            require(type(scopes) is list, "INVALID_SCOPE_SET")
            require(all(type(row) is list and all(type(item) is str for item in row) for row in scopes), "INVALID_SCOPE_SET")
            shared = set(scopes[0]) if scopes else set()
            for row in scopes[1:]:
                shared &= set(row)
            return ok(sorted(shared))
        if operation == "revocation_precedence":
            fields(payload, ("grants", "revoked"))
            grants, revoked = payload["grants"], payload["revoked"]
            require(type(grants) is list and type(revoked) is list, "INVALID_SCOPE")
            require(all(type(item) is str for item in grants + revoked), "INVALID_SCOPE")
            return ok({"active": sorted(set(grants) - set(revoked)), "revoked": sorted(set(grants) & set(revoked))})
        if operation == "authority_abstention":
            fields(payload, ("requirements",))
            requirements = payload["requirements"]
            require(type(requirements) is list, "INVALID_AUTHORITY_STATUS")
            require(all(type(row) is dict and set(row) == {"name", "status"} and row["status"] in {"verified", "missing", "contested"} for row in requirements), "INVALID_AUTHORITY_STATUS")
            missing = [row["name"] for row in requirements if row["status"] != "verified"]
            return ok({"authorized": bool(requirements) and not missing, "abstain_on": missing})
        raise ContractError("UNKNOWN_OPERATION")
    except ContractError as exc:
        return no(str(exc))


def cli(evaluator):
    try:
        raw = sys.stdin.buffer.read(262145)
        require(len(raw) <= 262144, "INPUT_BUDGET")
        request = strict_loads(raw)
        if type(request) is dict and set(request) == {"requests"}:
            rows = request["requests"]
            require(type(rows) is list and len(rows) <= 200, "INVALID_BATCH")
        else:
            rows = [request]
        results = []
        for row in rows:
            fields(row, ("operation", "input"))
            before = canonical(row["input"])
            result = evaluator(row["operation"], row["input"])
            require(before == canonical(row["input"]), "INPUT_MUTATED")
            results.append({"operation": row["operation"], "result": result, "input_unchanged": True})
        output, code = {"results": results}, 0
    except ContractError as exc:
        output, code = no(str(exc)), 2
    sys.stdout.buffer.write(canonical(output) + b"\n")
    return code


if __name__ == "__main__":
    raise SystemExit(cli(evaluate))
