"""Bounded provenance conflict, coverage, negative-index, and missingness contracts."""

from __future__ import annotations

from ghc_family_policy_resolution import ContractError, bounded_json, canonical, cli, fields, no, ok, require

OPERATIONS = ("provenance_branch_conflict", "coverage_abstention", "negative_evidence_index", "missingness_class")


def evaluate(operation, payload):
    try:
        bounded_json(payload)
        if operation == "provenance_branch_conflict":
            fields(payload, ("observations",))
            rows = payload["observations"]
            require(type(rows) is list, "INVALID_OBSERVATION")
            grouped = {}
            for row in rows:
                require(type(row) is dict and all(type(row.get(key)) is str for key in ("field", "source")) and "value" in row, "INVALID_OBSERVATION")
                grouped.setdefault(row["field"], []).append(row)
            conflicts = []
            for field, values in sorted(grouped.items()):
                distinct = {canonical(row["value"]).decode("utf-8") for row in values}
                if len(distinct) > 1:
                    conflicts.append({"field": field, "sources": sorted(row["source"] for row in values), "winner": None})
            return ok({"conflict": bool(conflicts), "conflicts": conflicts})
        if operation == "coverage_abstention":
            fields(payload, ("outputs", "declared_sources", "links"))
            outputs, sources, links = payload["outputs"], payload["declared_sources"], payload["links"]
            require(type(outputs) is list and type(sources) is list and type(links) is list, "INVALID_COVERAGE_INPUT")
            require(len(outputs) == len(set(outputs)), "DUPLICATE_OUTPUT")
            by_output = {}
            for link in links:
                require(type(link) is dict and set(link) == {"output", "sources"}, "INVALID_COVERAGE_INPUT")
                require(link["output"] not in by_output, "DUPLICATE_LINK")
                by_output[link["output"]] = link["sources"]
            orphan = sorted(set(by_output) - set(outputs))
            unknown = sorted({source for values in by_output.values() for source in values if source not in sources})
            covered = sorted(output for output in outputs if by_output.get(output) and all(source in sources for source in by_output[output]))
            uncovered = sorted(set(outputs) - set(covered))
            return ok({"complete": not orphan and not unknown and not uncovered, "covered": covered, "uncovered": uncovered, "orphan_links": orphan, "unknown_sources": unknown})
        if operation == "negative_evidence_index":
            fields(payload, ("failures",))
            rows = payload["failures"]
            require(type(rows) is list, "DUPLICATE_OR_INVALID_FAILURE_ID")
            ids = [row.get("id") if type(row) is dict else None for row in rows]
            require(all(type(value) is str and value for value in ids) and len(ids) == len(set(ids)), "DUPLICATE_OR_INVALID_FAILURE_ID")
            grouped = {}
            for row in rows:
                signature = row.get("signature")
                require(type(signature) is str and signature, "INVALID_SIGNATURE")
                grouped.setdefault(signature, []).append(row["id"])
            return ok([{"signature": key, "witness_ids": sorted(value)} for key, value in sorted(grouped.items())])
        if operation == "missingness_class":
            fields(payload, ("record", "field", "redacted_fields"))
            record, field, redacted = payload["record"], payload["field"], payload["redacted_fields"]
            require(type(record) is dict and type(field) is str and type(redacted) is list, "INVALID_MISSINGNESS_INPUT")
            if field in redacted:
                kind = "redacted"
            elif field not in record:
                kind = "absent"
            elif record[field] is None:
                kind = "explicit_null"
            elif type(record[field]) is dict and record[field] == {"unknown": True}:
                kind = "unknown"
            else:
                kind = "value"
            return ok({"field": field, "class": kind})
        raise ContractError("UNKNOWN_OPERATION")
    except ContractError as exc:
        return no(str(exc))


if __name__ == "__main__":
    raise SystemExit(cli(evaluate))
