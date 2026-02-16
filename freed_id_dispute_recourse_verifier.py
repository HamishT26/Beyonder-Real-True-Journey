"""
freed_id_dispute_recourse_verifier.py
-------------------------------------

Reproducible governance check for GOV-004:
dispute/recourse protocol workflow and transition enforcement.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from freed_id_dispute_recourse import open_dispute_case, transition_case


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _pass(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="PASS", detail=detail)


def _fail(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="FAIL", detail=detail)


def _validate_schema_contract(case_payload: Dict[str, object], schema: Dict[str, object]) -> List[CheckResult]:
    results: List[CheckResult] = []
    required_fields = schema.get("required", [])
    if not isinstance(required_fields, list):
        return [_fail("schema_required_fields", "schema required field list missing or malformed")]

    missing = [field for field in required_fields if field not in case_payload]
    if missing:
        results.append(_fail("schema_required_fields", f"missing={missing}"))
    else:
        results.append(_pass("schema_required_fields", "all required case fields present"))

    properties = schema.get("properties", {})
    status_enum = properties.get("status", {}).get("enum", []) if isinstance(properties, dict) else []
    case_status = str(case_payload.get("status", ""))
    if isinstance(status_enum, list) and case_status in status_enum:
        results.append(_pass("schema_status_enum", f"status={case_status}"))
    else:
        results.append(_fail("schema_status_enum", f"status={case_status} not in enum"))

    defs = schema.get("$defs", {})
    event_enum = []
    if isinstance(defs, dict):
        event_props = defs.get("dispute_event", {}).get("properties", {})
        if isinstance(event_props, dict):
            event_enum = event_props.get("to_status", {}).get("enum", [])

    history = case_payload.get("history", [])
    if isinstance(history, list) and history:
        invalid = [
            str(event.get("to_status", ""))
            for event in history
            if str(event.get("to_status", "")) not in event_enum
        ]
        if invalid:
            results.append(_fail("schema_event_status_enum", f"invalid_to_status={invalid}"))
        else:
            results.append(_pass("schema_event_status_enum", f"history_entries={len(history)}"))
    else:
        results.append(_fail("schema_event_status_enum", "history missing or empty"))
    return results


def _run_verification(schema_path: Path) -> Tuple[List[CheckResult], Dict[str, object]]:
    checks: List[CheckResult] = []

    case = open_dispute_case(
        case_id="case-gov004-0001",
        subject_did="did:freed:subject-001",
        credential_id="did:freed:subject-001#cred-0",
        opened_by="did:freed:ombuds-1",
        reason="presentation denial dispute",
        evidence_refs=["evidence://submission/1"],
    )
    checks.append(_pass("open_case", f"status={case.status}"))

    try:
        transition_case(
            case,
            to_status="resolved",
            actor="did:freed:ombuds-1",
            note="invalid direct resolve should fail",
        )
        checks.append(_fail("reject_invalid_transition", "opened->resolved unexpectedly accepted"))
    except ValueError:
        checks.append(_pass("reject_invalid_transition", "opened->resolved rejected"))

    transition_plan = [
        ("to_review", "review", "did:freed:reviewer-1", "intake accepted"),
        ("to_escalated", "escalated", "did:freed:reviewer-1", "needs council review"),
        ("escalation_back_to_review", "review", "did:freed:council-1", "returned with findings"),
        ("resolve_case", "resolved", "did:freed:reviewer-1", "credential update ordered"),
        ("reopen_case", "reopened", "did:freed:subject-001", "appeal on remediation scope"),
        ("reopened_to_review", "review", "did:freed:reviewer-2", "appeal accepted"),
        ("close_as_dismissed", "dismissed", "did:freed:reviewer-2", "appeal concluded"),
    ]
    for check_name, to_status, actor, note in transition_plan:
        try:
            transition_case(case, to_status=to_status, actor=actor, note=note)
            checks.append(_pass(check_name, f"status={case.status}"))
        except ValueError as exc:
            checks.append(_fail(check_name, str(exc)))

    case_payload = case.to_dict()

    history_len = len(case_payload.get("history", [])) if isinstance(case_payload.get("history"), list) else 0
    if history_len >= 8:
        checks.append(_pass("history_depth", f"events={history_len}"))
    else:
        checks.append(_fail("history_depth", f"events={history_len}, expected>=8"))

    if str(case_payload.get("status", "")) == "dismissed":
        checks.append(_pass("final_status", "dismissed"))
    else:
        checks.append(_fail("final_status", f"status={case_payload.get('status')}"))

    if schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        checks.extend(_validate_schema_contract(case_payload, schema))
    else:
        checks.append(_fail("schema_available", f"missing schema: {schema_path}"))

    return checks, case_payload


def _build_markdown(generated_utc: str, overall_status: str, checks: List[CheckResult], final_case: Dict[str, object]) -> str:
    lines = [
        "# Freed ID Dispute/Recourse Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        "- control_id: `GOV-004`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for result in checks:
        lines.append(f"| {result.check} | {result.status} | {result.detail} |")

    lines.extend(
        [
            "",
            "## Final case snapshot",
            "```json",
            json.dumps(final_case, indent=2),
            "```",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GOV-004 dispute/recourse verification.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs")
    parser.add_argument(
        "--schema",
        default="docs/freed-id-dispute-case-schema-v0.json",
        help="Schema path used for minimal contract checks.",
    )
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-dispute-recourse-latest.json",
        help="Path for latest JSON artifact.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-dispute-recourse-latest.md",
        help="Path for latest markdown artifact.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    checks, final_case = _run_verification(Path(args.schema))
    overall_status = "PASS" if all(item.status == "PASS" for item in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-004",
        "overall_status": overall_status,
        "checks": [asdict(item) for item in checks],
        "final_case": final_case,
    }
    markdown = _build_markdown(generated_utc, overall_status, checks, final_case)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-freedid-dispute-recourse-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-dispute-recourse-check.md"
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
