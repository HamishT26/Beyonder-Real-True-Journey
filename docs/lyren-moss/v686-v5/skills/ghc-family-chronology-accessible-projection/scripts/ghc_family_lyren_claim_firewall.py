"""Refuse evidence and authority promotion for Lyren's synthetic clock records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EVIDENCE_CLASSES = {"synthetic", "bounded_software"}
GATED_CLAIMS = {"production_identity", "professional", "cultural", "consciousness"}
GAP_CLAIMS = {"empirical", "independent_reproduction"}


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_member")
        result[key] = value
    return result


def read_strict(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def evidence_class(data: dict[str, Any]) -> Any:
    if data.get("external_action") is True:
        return {"error": "external_action_refused"}
    if data.get("external_action") is not False:
        return {"error": "invalid_external_action"}
    evidence = data.get("evidence_class")
    if evidence not in EVIDENCE_CLASSES:
        return {"error": "unknown_evidence_class"}
    claim = data.get("claim")
    if claim == "local_software":
        return "local_workflow_only"
    if claim in GAP_CLAIMS:
        return "open_gap"
    if claim in GATED_CLAIMS:
        return "exact_gate"
    return {"error": "unknown_claim"}


def _reservation(data: dict[str, Any], outcome: str) -> Any:
    if data.get("external_action") is not False:
        return {"error": "external_action_refused"}
    if data.get("evidence") is not None or data.get("authority") is not None:
        return {"error": "unverified_external_binding"}
    if not isinstance(data.get("obligation"), str) or not data["obligation"]:
        return {"error": "invalid_obligation"}
    return outcome


def thos_schedule_readback(data: dict[str, Any]) -> Any:
    return _reservation(data, "represented")


def gmut_clock_evidence_gap(data: dict[str, Any]) -> Any:
    return _reservation(data, "open_gap")


def cbr_time_authority_gate(data: dict[str, Any]) -> Any:
    return _reservation(data, "exact_gate")


OPERATIONS = {
    "evidence_class": evidence_class,
    "thos_schedule_readback": thos_schedule_readback,
    "gmut_clock_evidence_gap": gmut_clock_evidence_gap,
    "cbr_time_authority_gate": cbr_time_authority_gate,
}


def run(operation: str, data: Any) -> Any:
    if operation not in OPERATIONS:
        return {"error": "unknown_operation"}
    if not isinstance(data, dict):
        return {"error": "invalid_input"}
    return OPERATIONS[operation](data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("output exists; exclusive-write refusal")
    try:
        payload = read_strict(args.input)
        result = run(payload.get("operation"), payload.get("input")) if isinstance(payload, dict) else {"error": "invalid_input"}
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        result = {"error": "invalid_json"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
