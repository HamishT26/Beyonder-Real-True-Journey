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

from freed_id_dispute_recourse import open_dispute_case, transition_case, verify_case_history_integrity


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _pass(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="PASS", detail=detail)


def _fail(check: str, detail: str) -> CheckResult:
    return CheckResult(check=check, status="FAIL", detail=detail)


def _proof(proof_id: str, signer_did: str) -> Dict[str, str]:
    return {
        "proof_id": proof_id,
        "signer_did": signer_did,
        "signature_ref": f"sig://{proof_id}",
        "issued_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def _signature_verifier(actor: str, proof: Dict[str, str]) -> bool:
    """
    v0 verifier hook: requires signer match + sig:// URI with proof_id suffix.
    """
    proof_id = str(proof.get("proof_id", "")).strip()
    signer = str(proof.get("signer_did", "")).strip()
    signature_ref = str(proof.get("signature_ref", "")).strip()
    return signer == actor and signature_ref == f"sig://{proof_id}"


def _as_nonempty_text(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return ""


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
    actor_role_enum = []
    if isinstance(defs, dict):
        event_props = defs.get("dispute_event", {}).get("properties", {})
        if isinstance(event_props, dict):
            event_enum = event_props.get("to_status", {}).get("enum", [])
            actor_role_enum = event_props.get("actor_role", {}).get("enum", [])

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

        invalid_roles = [
            str(event.get("actor_role", ""))
            for event in history
            if str(event.get("actor_role", "")) not in actor_role_enum
        ]
        if invalid_roles:
            results.append(_fail("schema_event_actor_role_enum", f"invalid_actor_role={invalid_roles}"))
        else:
            results.append(_pass("schema_event_actor_role_enum", f"history_entries={len(history)}"))

        bad_sequences: List[int] = []
        bad_ids: List[str] = []
        for idx, event in enumerate(history):
            if int(event.get("event_seq", -1)) != idx:
                bad_sequences.append(idx)
            expected_id = f"{case_payload.get('case_id', 'case')}:event:{idx:04d}"
            if str(event.get("event_id", "")) != expected_id:
                bad_ids.append(str(event.get("event_id", "")))
        if bad_sequences:
            results.append(_fail("schema_event_sequence", f"bad_indices={bad_sequences}"))
        else:
            results.append(_pass("schema_event_sequence", f"history_entries={len(history)}"))
        if bad_ids:
            results.append(_fail("schema_event_id_pattern", f"invalid_event_ids={bad_ids[:3]}"))
        else:
            results.append(_pass("schema_event_id_pattern", f"history_entries={len(history)}"))
    else:
        results.append(_fail("schema_event_status_enum", "history missing or empty"))
        results.append(_fail("schema_event_actor_role_enum", "history missing or empty"))
        results.append(_fail("schema_event_sequence", "history missing or empty"))
        results.append(_fail("schema_event_id_pattern", "history missing or empty"))
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

    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:reviewer-1",
            note="proof-required transition should fail without auth proof",
            enforce_actor_policy=True,
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
        )
        checks.append(_fail("reject_missing_auth_proof", "missing proof opened->review unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_missing_auth_proof", "missing proof opened->review rejected"))

    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:reviewer-1",
            note="signature verification required should fail without verifier",
            enforce_actor_policy=True,
            auth_proof=_proof("proof-no-verifier", "did:freed:reviewer-1"),
            require_auth_proof=True,
            enforce_signature_verification=True,
        )
        checks.append(_fail("reject_missing_signature_verifier", "missing signature_verifier unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_missing_signature_verifier", "missing signature_verifier rejected"))

    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:subject-001",
            note="subject should not be allowed to move opened->review",
            enforce_actor_policy=True,
            auth_proof=_proof("proof-unauthorized-subject", "did:freed:subject-001"),
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_unauthorized_actor_role", "subject opened->review unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_unauthorized_actor_role", "subject opened->review rejected"))

    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:robot-1",
            note="unknown actor role should be rejected",
            enforce_actor_policy=True,
            auth_proof=_proof("proof-unknown-role", "did:freed:robot-1"),
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_unknown_actor_role", "unknown role opened->review unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_unknown_actor_role", "unknown role opened->review rejected"))

    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:reviewer-1",
            note="mismatched signer should fail",
            enforce_actor_policy=True,
            auth_proof=_proof("proof-signer-mismatch", "did:freed:council-1"),
            require_auth_proof=True,
            enforce_signer_match=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_signer_mismatch", "signer mismatch opened->review unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_signer_mismatch", "signer mismatch opened->review rejected"))

    used_proofs: List[str] = []

    def proof_for(actor: str, suffix: str) -> Dict[str, str]:
        proof_id = f"proof-{suffix}"
        used_proofs.append(proof_id)
        return _proof(proof_id, actor)

    bad_signature_proof = _proof("proof-bad-signature-ref", "did:freed:reviewer-1")
    bad_signature_proof["signature_ref"] = "invalid://proof-bad-signature-ref"
    try:
        transition_case(
            case,
            to_status="review",
            actor="did:freed:reviewer-1",
            note="invalid signature reference should fail",
            enforce_actor_policy=True,
            auth_proof=bad_signature_proof,
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_invalid_signature_ref", "invalid signature_ref unexpectedly accepted"))
    except PermissionError:
        checks.append(_pass("reject_invalid_signature_ref", "invalid signature_ref rejected"))

    transition_plan = [
        ("to_review", "review", "did:freed:reviewer-1", "intake accepted"),
        ("to_escalated", "escalated", "did:freed:reviewer-1", "needs council review"),
        ("reject_replayed_proof", "review", "did:freed:council-1", "replay should fail"),
        ("escalation_back_to_review", "review", "did:freed:council-1", "returned with findings"),
        ("resolve_case", "resolved", "did:freed:reviewer-1", "credential update ordered"),
        ("reopen_case", "reopened", "did:freed:subject-001", "appeal on remediation scope"),
        ("reopened_to_review", "review", "did:freed:reviewer-2", "appeal accepted"),
        ("close_as_dismissed", "dismissed", "did:freed:reviewer-2", "appeal concluded"),
    ]
    for check_name, to_status, actor, note in transition_plan:
        if check_name == "reject_replayed_proof":
            replay_id = used_proofs[-1] if used_proofs else "proof-missing"
            replay_proof = _proof(replay_id, actor)
            try:
                transition_case(
                    case,
                    to_status=to_status,
                    actor=actor,
                    note=note,
                    enforce_actor_policy=True,
                    auth_proof=replay_proof,
                    require_auth_proof=True,
                    enforce_signature_verification=True,
                    signature_verifier=_signature_verifier,
                    reject_replayed_proof=True,
                )
                checks.append(_fail(check_name, f"replayed proof accepted: {replay_id}"))
            except PermissionError:
                checks.append(_pass(check_name, f"replayed proof rejected: {replay_id}"))
            continue

        try:
            transition_case(
                case,
                to_status=to_status,
                actor=actor,
                note=note,
                enforce_actor_policy=True,
                auth_proof=proof_for(actor, check_name),
                require_auth_proof=True,
                enforce_signature_verification=True,
                signature_verifier=_signature_verifier,
                reject_replayed_proof=True,
            )
            checks.append(_pass(check_name, f"status={case.status}"))
        except (ValueError, PermissionError) as exc:
            checks.append(_fail(check_name, str(exc)))

    case_payload = case.to_dict()
    chain_ok, chain_errors = verify_case_history_integrity(case)
    if chain_ok:
        checks.append(_pass("history_integrity_chain", "event sequence and status chain verified"))
    else:
        checks.append(_fail("history_integrity_chain", "; ".join(chain_errors[:3])))

    history_len = len(case_payload.get("history", [])) if isinstance(case_payload.get("history"), list) else 0
    if history_len >= 8:
        checks.append(_pass("history_depth", f"events={history_len}"))
    else:
        checks.append(_fail("history_depth", f"events={history_len}, expected>=8"))

    if str(case_payload.get("status", "")) == "dismissed":
        checks.append(_pass("final_status", "dismissed"))
    else:
        checks.append(_fail("final_status", f"status={case_payload.get('status')}"))

    history = case_payload.get("history", [])
    if isinstance(history, list):
        missing_auth = [
            idx
            for idx, event in enumerate(history[1:], start=1)
            if not str(event.get("auth_proof_id", "")).strip()
        ]
        if missing_auth:
            checks.append(_fail("auth_proof_presence", f"missing_indices={missing_auth}"))
        else:
            checks.append(_pass("auth_proof_presence", "all transition events include auth_proof_id"))

        proof_ids_history = sorted(
            _as_nonempty_text(event.get("auth_proof_id"))
            for event in history
            if _as_nonempty_text(event.get("auth_proof_id"))
        )
        proof_ids_registry = sorted(
            _as_nonempty_text(proof_id)
            for proof_id in case_payload.get("used_auth_proof_ids", [])
            if _as_nonempty_text(proof_id)
        )
        if proof_ids_history == proof_ids_registry and len(proof_ids_registry) == len(set(proof_ids_registry)):
            checks.append(_pass("auth_proof_registry_consistency", f"proof_count={len(proof_ids_registry)}"))
        else:
            checks.append(
                _fail(
                    "auth_proof_registry_consistency",
                    f"history={len(proof_ids_history)} registry={len(proof_ids_registry)}",
                )
            )
    else:
        checks.append(_fail("auth_proof_presence", "history missing"))
        checks.append(_fail("auth_proof_registry_consistency", "history missing"))

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
