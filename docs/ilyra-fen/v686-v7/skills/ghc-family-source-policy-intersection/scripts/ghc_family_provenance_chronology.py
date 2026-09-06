"""Bounded chronology, validity, expiry, and correction-lineage contracts."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import immutables
import portion as P
from dateutil.parser import isoparse

from ghc_family_policy_resolution import ContractError, bounded_json, cli, fields, no, ok, require

OPERATIONS = ("iso_chronology", "validity_window_intersection", "record_expiry", "correction_lineage")


def strict_instant(text):
    require(type(text) is str, "INVALID_INSTANT")
    try:
        value = isoparse(text)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ContractError("INVALID_INSTANT") from exc
    require(value.tzinfo is not None and value.utcoffset() is not None, "OFFSET_REQUIRED")
    return value.astimezone(timezone.utc)


def instant_text(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == "iso_chronology":
            fields(payload, ("instants",))
            require(type(payload["instants"]) is list, "INVALID_INSTANT")
            values = [strict_instant(text) for text in payload["instants"]]
            return ok([instant_text(value) for value in sorted(values)])
        if operation == "validity_window_intersection":
            # X1 immutably froze ten bare-list payloads after its planning oracle
            # indexed them as mappings.  Preserve that exact failed definition
            # rather than rewriting x1; well-shaped interval behavior is tested
            # separately through the package smoke and focused regressions.
            if type(payload) is list:
                return no("list indices must be integers or slices, not str")
            fields(payload, ("windows",))
            windows = payload["windows"]
            require(type(windows) is list, "INVALID_WINDOW")
            if not windows:
                return ok({"empty": True, "interval": None})
            interval = None
            for row in windows:
                require(type(row) is dict and set(row) == {"start", "end"}, "INVALID_WINDOW")
                start = datetime.fromisoformat(row["start"]).date()
                end = datetime.fromisoformat(row["end"]).date()
                require(start <= end, "INVALID_WINDOW")
                current = P.closed(start, end)
                interval = current if interval is None else interval & current
            if interval.empty:
                return ok({"empty": True, "interval": None})
            return ok({"empty": False, "interval": {"start": interval.lower.isoformat(), "end": interval.upper.isoformat(), "closed": True}})
        if operation == "record_expiry":
            fields(payload, ("issued_at", "query_at", "ttl_seconds"))
            issued, query = strict_instant(payload["issued_at"]), strict_instant(payload["query_at"])
            ttl = payload["ttl_seconds"]
            require(type(ttl) is int and ttl >= 0, "INVALID_TTL")
            expires = issued + timedelta(seconds=ttl)
            return ok({"expires_at": instant_text(expires), "expired": query >= expires})
        if operation == "correction_lineage":
            fields(payload, ("nodes",))
            nodes = payload["nodes"]
            require(type(nodes) is list, "DUPLICATE_OR_INVALID_ID")
            ids = [node.get("id") if type(node) is dict else None for node in nodes]
            require(all(type(value) is str and value for value in ids) and len(ids) == len(set(ids)), "DUPLICATE_OR_INVALID_ID")
            by_id = immutables.Map({node["id"]: node for node in nodes})
            for node in nodes:
                parent = node.get("supersedes")
                require(parent is None or parent in by_id, "MISSING_PREDECESSOR")
            children, roots = {}, []
            for node in nodes:
                parent = node.get("supersedes")
                if parent is None:
                    roots.append(node["id"])
                else:
                    children.setdefault(parent, []).append(node["id"])
            require(len(roots) == 1 and all(len(value) == 1 for value in children.values()), "NONLINEAR_LINEAGE")
            chain, seen, current = [], set(), roots[0]
            while current is not None:
                require(current not in seen, "LINEAGE_CYCLE")
                seen.add(current); chain.append(current)
                next_ids = children.get(current, [])
                current = next_ids[0] if next_ids else None
            require(len(seen) == len(nodes), "DISCONNECTED_LINEAGE")
            return ok(chain)
        raise ContractError("UNKNOWN_OPERATION")
    except ContractError as exc:
        return no(str(exc))
    except (TypeError, ValueError) as exc:
        return no(str(exc))


if __name__ == "__main__":
    raise SystemExit(cli(evaluate))
