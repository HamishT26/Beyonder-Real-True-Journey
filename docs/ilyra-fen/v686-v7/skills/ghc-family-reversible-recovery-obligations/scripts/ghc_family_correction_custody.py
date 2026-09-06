"""Bounded difference, number, revocation, custody, and recovery contracts."""

from __future__ import annotations

import copy
import re
from decimal import Decimal, InvalidOperation

from ghc_family_policy_resolution import ContractError, bounded_json, cli, fields, no, ok, require

OPERATIONS = ("accessible_diff", "canonical_number_policy", "revocation_projection", "custody_chain", "recovery_obligation")


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == "accessible_diff":
            fields(payload, ("before", "after"))
            before, after = payload["before"], payload["after"]
            require(type(before) is dict and type(after) is dict, "MAPPING_REQUIRED")
            changes = []
            for key in sorted(set(before) | set(after)):
                if key not in before:
                    changes.append({"field": key, "kind": "added", "after": after[key]})
                elif key not in after:
                    changes.append({"field": key, "kind": "removed", "before": before[key]})
                elif type(before[key]) is not type(after[key]):
                    changes.append({"field": key, "kind": "type_changed", "before_type": type(before[key]).__name__, "after_type": type(after[key]).__name__})
                elif before[key] != after[key]:
                    changes.append({"field": key, "kind": "value_changed", "before": before[key], "after": after[key]})
            return ok(changes)
        if operation == "canonical_number_policy":
            fields(payload, ("text",))
            text = payload["text"]
            require(type(text) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", text), "NONCANONICAL_NUMBER")
            require(not text.startswith("-0") and not ("." in text and text.endswith("0")), "NONCANONICAL_NUMBER")
            try:
                value = Decimal(text)
            except InvalidOperation as exc:
                raise ContractError("NONCANONICAL_NUMBER") from exc
            return ok({"canonical": text, "finite": value.is_finite()})
        if operation == "revocation_projection":
            fields(payload, ("records",))
            rows = payload["records"]
            require(type(rows) is list and all(type(row) is dict for row in rows), "DUPLICATE_OR_INVALID_ID")
            ids = [row.get("id") for row in rows]
            require(all(type(value) is str for value in ids) and len(ids) == len(set(ids)), "DUPLICATE_OR_INVALID_ID")
            require(all(row.get("status") in {"active", "revoked", "expired", "held"} for row in rows), "INVALID_STATUS")
            active = [copy.deepcopy(row) for row in rows if row["status"] == "active"]
            omitted = [{"id": row["id"], "reason": row["status"]} for row in rows if row["status"] != "active"]
            return ok({"active": active, "omitted": omitted})
        if operation == "custody_chain":
            fields(payload, ("events",))
            events = payload["events"]
            require(type(events) is list and all(type(event) is dict for event in events), "NONCONTIGUOUS_SEQUENCE")
            require([event.get("sequence") for event in events] == list(range(1, len(events) + 1)), "NONCONTIGUOUS_SEQUENCE")
            require(all(type(event.get("actor")) is str and event["actor"] and type(event.get("action")) is str and event["action"] for event in events), "INCOMPLETE_CUSTODY_EVENT")
            return ok({"complete": True, "events": len(events)})
        if operation == "recovery_obligation":
            require(type(payload) is dict and set(payload).issubset({"reversible", "preimage"}), "INVALID_FIELDS")
            reversible = payload.get("reversible")
            require(type(reversible) is bool, "INVALID_REVERSIBILITY_FLAG")
            if not reversible:
                return ok({"eligible": False, "missing": ["reversible_contract"]})
            if "preimage" not in payload:
                return ok({"eligible": False, "missing": ["retained_preimage"]})
            return ok({"eligible": True, "missing": []})
        raise ContractError("UNKNOWN_OPERATION")
    except ContractError as exc:
        return no(str(exc))


if __name__ == "__main__":
    raise SystemExit(cli(evaluate))
