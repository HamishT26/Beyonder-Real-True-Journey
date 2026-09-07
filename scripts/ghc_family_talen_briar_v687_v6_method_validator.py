#!/usr/bin/env python3
"""Maintain an append-only GHC Family method-flow ledger."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SCHEMA = "ghc.family.method-flow-state.v1"
STATES = ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]
RESULTS = ["pass", "fail"]
TRANSITIONS = {
    "observed": {"candidate", "deprecated"},
    "candidate": {"validated", "deprecated"},
    "validated": {"preferred", "superseded", "deprecated"},
    "preferred": {"superseded", "deprecated"},
    "superseded": set(),
    "deprecated": set(),
}
METHOD_FIELDS = {
    "method_id",
    "title",
    "failure_signature",
    "trigger_preconditions",
    "privacy_class",
    "approval_class",
    "candidate_workaround",
    "validation_witness_ids",
    "recurrence_guard",
    "rollback",
    "recommendation_state",
    "supersedes",
    "protected_gates",
    "retained_negative_ids",
    "scope_boundary",
}
WITNESS_FIELDS = {
    "witness_id",
    "method_id",
    "procedure",
    "scope",
    "expected",
    "observed",
    "result",
    "same_owner_only",
    "independent_reproduction",
    "retained_negative_ids",
    "boundary",
}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE),
    "private_uri": re.compile(r"\b(?:app|plugin)://", re.IGNORECASE),
    "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.IGNORECASE),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"
    ),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def refresh_counts(ledger: dict[str, Any]) -> None:
    states = Counter(row.get("recommendation_state") for row in ledger.get("methods", []))
    results = Counter(row.get("result") for row in ledger.get("witnesses", []))
    ledger["counts"] = {
        "methods": len(ledger.get("methods", [])),
        "witnesses": len(ledger.get("witnesses", [])),
        "state_events": len(ledger.get("state_events", [])),
        "recommendations": len(ledger.get("recommendations", [])),
        "states": {state: states.get(state, 0) for state in STATES},
        "witness_results": {result: results.get(result, 0) for result in RESULTS},
    }


def new_ledger(phase: str, owner: str) -> dict[str, Any]:
    ledger = {
        "schema": SCHEMA,
        "phase": phase,
        "owner": owner,
        "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, or authority evidence.",
        "methods": [],
        "witnesses": [],
        "state_events": [],
        "recommendations": [],
        "counts": {},
        "boundary": "This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.",
    }
    refresh_counts(ledger)
    return ledger


def method_map(ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["method_id"]: row for row in ledger.get("methods", [])}


def passing_witnesses(ledger: dict[str, Any], method_id: str) -> list[dict[str, Any]]:
    return [
        row
        for row in ledger.get("witnesses", [])
        if row.get("method_id") == method_id and row.get("result") == "pass"
    ]


def append_event(
    ledger: dict[str, Any],
    method_id: str,
    before: str | None,
    after: str,
    reason: str,
    witness_id: str | None = None,
) -> None:
    ledger["state_events"].append(
        {
            "event_index": len(ledger["state_events"]) + 1,
            "method_id": method_id,
            "before": before,
            "after": after,
            "reason": reason,
            "witness_id": witness_id,
        }
    )


def validate_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    top_fields = {
        "schema",
        "phase",
        "owner",
        "identity_boundary",
        "methods",
        "witnesses",
        "state_events",
        "recommendations",
        "counts",
        "boundary",
    }
    if not top_fields.issubset(ledger):
        issues.append("missing top-level fields")
    if ledger.get("schema") != SCHEMA:
        issues.append("unexpected schema")

    methods = ledger.get("methods", [])
    witnesses = ledger.get("witnesses", [])
    ids = [row.get("method_id") for row in methods]
    witness_ids = [row.get("witness_id") for row in witnesses]
    if None in ids or len(ids) != len(set(ids)):
        issues.append("method identifiers missing or duplicated")
    if None in witness_ids or len(witness_ids) != len(set(witness_ids)):
        issues.append("witness identifiers missing or duplicated")
    by_id = method_map(ledger)

    for row in methods:
        method_id = row.get("method_id", "<missing>")
        if not METHOD_FIELDS.issubset(row):
            issues.append(f"{method_id}: missing method fields")
        if row.get("recommendation_state") not in STATES:
            issues.append(f"{method_id}: invalid recommendation state")
        for field in ("trigger_preconditions", "protected_gates", "retained_negative_ids"):
            if not isinstance(row.get(field), list) or not row.get(field):
                issues.append(f"{method_id}: {field} must be a non-empty list")
        if not isinstance(row.get("validation_witness_ids"), list):
            issues.append(f"{method_id}: validation_witness_ids must be a list")
        if not isinstance(row.get("supersedes"), list):
            issues.append(f"{method_id}: supersedes must be a list")
        if row.get("recommendation_state") == "preferred" and not passing_witnesses(ledger, method_id):
            issues.append(f"{method_id}: preferred without a passing witness")
        if row.get("recommendation_state") == "superseded":
            successors = row.get("supersedes") or []
            if not successors:
                issues.append(f"{method_id}: superseded without successor")
            for successor in successors:
                successor_row = by_id.get(successor)
                if not successor_row or successor_row.get("recommendation_state") not in {"validated", "preferred"}:
                    issues.append(f"{method_id}: successor {successor} is not validated")

    for witness in witnesses:
        witness_id = witness.get("witness_id", "<missing>")
        if not WITNESS_FIELDS.issubset(witness):
            issues.append(f"{witness_id}: missing witness fields")
        if witness.get("method_id") not in by_id:
            issues.append(f"{witness_id}: unknown method")
        if witness.get("result") not in RESULTS:
            issues.append(f"{witness_id}: invalid result")
        if witness.get("independent_reproduction") is not False:
            issues.append(f"{witness_id}: independent reproduction may not be promoted by this runner")
        method = by_id.get(witness.get("method_id"))
        if method and witness_id not in method.get("validation_witness_ids", []):
            issues.append(f"{witness_id}: missing method backlink")

    serialized = json.dumps(ledger, ensure_ascii=False)
    privacy_hits = [
        {"pattern_class": label}
        for label, pattern in PRIVATE_PATTERNS.items()
        if pattern.search(serialized)
    ]
    if privacy_hits:
        issues.append("privacy exclusion pattern hit")

    expected_counts = dict(ledger.get("counts") or {})
    refreshed = json.loads(json.dumps(ledger))
    refresh_counts(refreshed)
    if expected_counts != refreshed["counts"]:
        issues.append("derived counts are stale")

    return {
        "schema": "ghc.family.method-flow-state.validation.v1",
        "phase": ledger.get("phase"),
        "owner": ledger.get("owner"),
        "method_count": len(methods),
        "witness_count": len(witnesses),
        "state_event_count": len(ledger.get("state_events", [])),
        "recommendation_count": len(ledger.get("recommendations", [])),
        "privacy_pattern_classes": sorted(PRIVATE_PATTERNS),
        "privacy_hits": privacy_hits,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Validation covers the ledger schema and bounded method evidence only; it is not independent reproduction or broader assurance.",
    }


def render_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# GHC Family Method Flow State",
        "",
        f"- Phase: {ledger['phase']}",
        f"- Owner: {ledger['owner']}",
        f"- Methods: {ledger['counts']['methods']}",
        f"- Passing witnesses: {ledger['counts']['witness_results']['pass']}",
        f"- Failed witnesses retained: {ledger['counts']['witness_results']['fail']}",
        "",
        "## Preferred methods",
        "",
    ]
    preferred = [row for row in ledger["methods"] if row["recommendation_state"] == "preferred"]
    if not preferred:
        lines.append("- None.")
    for row in preferred:
        lines.extend(
            [
                f"### {row['method_id']} — {row['title']}",
                "",
                f"- Trigger: {'; '.join(row['trigger_preconditions'])}",
                f"- Method: {row['candidate_workaround']}",
                f"- Recurrence guard: {row['recurrence_guard']}",
                f"- Rollback: {row['rollback']}",
                f"- Witnesses: {', '.join(row['validation_witness_ids'])}",
                "",
            ]
        )
    lines.extend(["## Retained boundary", "", ledger["boundary"], ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--ledger", type=Path, required=True)
    init.add_argument("--phase", required=True)
    init.add_argument("--owner", required=True)

    record = sub.add_parser("record")
    record.add_argument("--ledger", type=Path, required=True)
    record.add_argument("--record-file", type=Path, required=True)

    witness = sub.add_parser("witness")
    witness.add_argument("--ledger", type=Path, required=True)
    witness.add_argument("--witness-file", type=Path, required=True)

    set_state = sub.add_parser("set-state")
    set_state.add_argument("--ledger", type=Path, required=True)
    set_state.add_argument("--method-id", required=True)
    set_state.add_argument("--state", choices=STATES, required=True)
    set_state.add_argument("--note", required=True)
    set_state.add_argument("--successor")

    validate = sub.add_parser("validate")
    validate.add_argument("--ledger", type=Path, required=True)
    validate.add_argument("--receipt", type=Path)

    summarize = sub.add_parser("summarize")
    summarize.add_argument("--ledger", type=Path, required=True)
    summarize.add_argument("--json-output", type=Path)
    summarize.add_argument("--markdown-output", type=Path)

    args = parser.parse_args()

    if args.command == "init":
        if args.ledger.exists():
            raise SystemExit("ledger already exists")
        ledger = new_ledger(args.phase, args.owner)
        write_json(args.ledger, ledger)
        print(json.dumps({"created": True, "ledger": args.ledger.name, "valid": True}))
        return

    ledger = read_json(args.ledger)
    if args.command == "record":
        row = read_json(args.record_file)
        missing = METHOD_FIELDS - set(row)
        if missing:
            raise SystemExit(f"record missing fields: {sorted(missing)}")
        if row["method_id"] in method_map(ledger):
            raise SystemExit("method identifier already exists")
        if row["recommendation_state"] not in {"observed", "candidate"}:
            raise SystemExit("new methods must begin observed or candidate")
        ledger["methods"].append(row)
        append_event(
            ledger,
            row["method_id"],
            None,
            row["recommendation_state"],
            "method recorded with retained negative linkage",
        )
        refresh_counts(ledger)
        write_json(args.ledger, ledger)
        print(json.dumps({"recorded": row["method_id"], "state": row["recommendation_state"]}))
        return

    if args.command == "witness":
        row = read_json(args.witness_file)
        missing = WITNESS_FIELDS - set(row)
        if missing:
            raise SystemExit(f"witness missing fields: {sorted(missing)}")
        if row["witness_id"] in {item["witness_id"] for item in ledger["witnesses"]}:
            raise SystemExit("witness identifier already exists")
        methods = method_map(ledger)
        if row["method_id"] not in methods:
            raise SystemExit("witness method does not exist")
        if row["result"] not in RESULTS:
            raise SystemExit("witness result must be pass or fail")
        if row["independent_reproduction"] is not False:
            raise SystemExit("this runner cannot claim independent reproduction")
        ledger["witnesses"].append(row)
        method = methods[row["method_id"]]
        method["validation_witness_ids"].append(row["witness_id"])
        if row["result"] == "pass" and method["recommendation_state"] in {"observed", "candidate"}:
            before = method["recommendation_state"]
            method["recommendation_state"] = "validated"
            append_event(
                ledger,
                method["method_id"],
                before,
                "validated",
                "bounded witness passed",
                row["witness_id"],
            )
        refresh_counts(ledger)
        write_json(args.ledger, ledger)
        print(json.dumps({"witness": row["witness_id"], "result": row["result"], "method_state": method["recommendation_state"]}))
        return

    if args.command == "set-state":
        methods = method_map(ledger)
        if args.method_id not in methods:
            raise SystemExit("method does not exist")
        method = methods[args.method_id]
        before = method["recommendation_state"]
        if args.state not in TRANSITIONS.get(before, set()):
            raise SystemExit(f"invalid transition {before} -> {args.state}")
        if args.state == "preferred" and not passing_witnesses(ledger, args.method_id):
            raise SystemExit("preferred requires a passing witness")
        if args.state == "superseded":
            if not args.successor:
                raise SystemExit("superseded requires --successor")
            successor = methods.get(args.successor)
            if not successor or successor["recommendation_state"] not in {"validated", "preferred"}:
                raise SystemExit("successor must already be validated or preferred")
            method["supersedes"].append(args.successor)
        method["recommendation_state"] = args.state
        append_event(ledger, args.method_id, before, args.state, args.note)
        if args.state == "preferred":
            ledger["recommendations"].append(
                {
                    "recommendation_index": len(ledger["recommendations"]) + 1,
                    "method_id": args.method_id,
                    "preconditions": method["trigger_preconditions"],
                    "method": method["candidate_workaround"],
                    "witness_ids": method["validation_witness_ids"],
                    "recurrence_guard": method["recurrence_guard"],
                    "rollback": method["rollback"],
                    "scope_boundary": method["scope_boundary"],
                }
            )
        refresh_counts(ledger)
        write_json(args.ledger, ledger)
        print(json.dumps({"method": args.method_id, "before": before, "after": args.state}))
        return

    receipt = validate_ledger(ledger)
    if args.command == "validate":
        if args.receipt:
            write_json(args.receipt, receipt)
        print(json.dumps(receipt, ensure_ascii=False))
        raise SystemExit(0 if receipt["valid"] else 1)

    if args.command == "summarize":
        payload = {
            "schema": "ghc.family.method-flow-state.summary.v1",
            "phase": ledger["phase"],
            "owner": ledger["owner"],
            "counts": ledger["counts"],
            "preferred_methods": [
                {
                    "method_id": row["method_id"],
                    "title": row["title"],
                    "trigger_preconditions": row["trigger_preconditions"],
                    "candidate_workaround": row["candidate_workaround"],
                    "validation_witness_ids": row["validation_witness_ids"],
                    "recurrence_guard": row["recurrence_guard"],
                    "rollback": row["rollback"],
                    "scope_boundary": row["scope_boundary"],
                }
                for row in ledger["methods"]
                if row["recommendation_state"] == "preferred"
            ],
            "retained_failed_witnesses": [
                row["witness_id"] for row in ledger["witnesses"] if row["result"] == "fail"
            ],
            "valid": receipt["valid"],
            "boundary": ledger["boundary"],
        }
        if args.json_output:
            write_json(args.json_output, payload)
        if args.markdown_output:
            args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
            args.markdown_output.write_text(render_markdown(ledger), encoding="utf-8", newline="\n")
        print(json.dumps(payload, ensure_ascii=False))
        raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()
