"""
freed_id_dispute_recourse_adversarial_verifier.py
-------------------------------------------------

Adversarial checks for GOV-004 dispute/recourse workflow:
- replayed auth proof rejection,
- signer mismatch rejection,
- event-order and event-sequence tamper detection.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
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
    proof_id = str(proof.get("proof_id", "")).strip()
    signer = str(proof.get("signer_did", "")).strip()
    signature_ref = str(proof.get("signature_ref", "")).strip()
    return signer == actor and signature_ref == f"sig://{proof_id}"


def _run_verification() -> Tuple[List[CheckResult], Dict[str, object]]:
    checks: List[CheckResult] = []
    case = open_dispute_case(
        case_id="case-gov004-adversarial-0001",
        subject_did="did:freed:subject-adv-001",
        credential_id="did:freed:subject-adv-001#cred-0",
        opened_by="did:freed:ombuds-1",
        reason="adversarial transition checks",
        evidence_refs=["evidence://adversarial/seed"],
    )
    checks.append(_pass("open_case", f"status={case.status}"))

    transition_case(
        case,
        to_status="review",
        actor="did:freed:reviewer-1",
        note="baseline review transition",
        enforce_actor_policy=True,
        auth_proof=_proof("adv-proof-1", "did:freed:reviewer-1"),
        require_auth_proof=True,
        enforce_signature_verification=True,
        signature_verifier=_signature_verifier,
        reject_replayed_proof=True,
    )
    checks.append(_pass("baseline_to_review", f"status={case.status}"))

    try:
        transition_case(
            case,
            to_status="escalated",
            actor="did:freed:reviewer-1",
            note="replay proof attack",
            enforce_actor_policy=True,
            auth_proof=_proof("adv-proof-1", "did:freed:reviewer-1"),
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_replayed_proof", "replayed proof accepted"))
    except PermissionError:
        checks.append(_pass("reject_replayed_proof", "replayed proof rejected"))

    try:
        transition_case(
            case,
            to_status="escalated",
            actor="did:freed:reviewer-1",
            note="signer mismatch attack",
            enforce_actor_policy=True,
            auth_proof=_proof("adv-proof-2", "did:freed:council-1"),
            require_auth_proof=True,
            enforce_signer_match=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_signer_mismatch", "mismatched signer accepted"))
    except PermissionError:
        checks.append(_pass("reject_signer_mismatch", "mismatched signer rejected"))

    bad_sig = _proof("adv-proof-bad-signature", "did:freed:reviewer-1")
    bad_sig["signature_ref"] = "bad://adv-proof-bad-signature"
    try:
        transition_case(
            case,
            to_status="escalated",
            actor="did:freed:reviewer-1",
            note="invalid signature reference attack",
            enforce_actor_policy=True,
            auth_proof=bad_sig,
            require_auth_proof=True,
            enforce_signature_verification=True,
            signature_verifier=_signature_verifier,
            reject_replayed_proof=True,
        )
        checks.append(_fail("reject_invalid_signature_ref", "invalid signature reference accepted"))
    except PermissionError:
        checks.append(_pass("reject_invalid_signature_ref", "invalid signature reference rejected"))

    transition_case(
        case,
        to_status="escalated",
        actor="did:freed:reviewer-1",
        note="valid escalation",
        enforce_actor_policy=True,
        auth_proof=_proof("adv-proof-3", "did:freed:reviewer-1"),
        require_auth_proof=True,
        enforce_signature_verification=True,
        signature_verifier=_signature_verifier,
        reject_replayed_proof=True,
    )
    transition_case(
        case,
        to_status="review",
        actor="did:freed:council-1",
        note="valid escalation return",
        enforce_actor_policy=True,
        auth_proof=_proof("adv-proof-4", "did:freed:council-1"),
        require_auth_proof=True,
        enforce_signature_verification=True,
        signature_verifier=_signature_verifier,
        reject_replayed_proof=True,
    )
    transition_case(
        case,
        to_status="resolved",
        actor="did:freed:council-1",
        note="valid resolution",
        enforce_actor_policy=True,
        auth_proof=_proof("adv-proof-5", "did:freed:council-1"),
        require_auth_proof=True,
        enforce_signature_verification=True,
        signature_verifier=_signature_verifier,
        reject_replayed_proof=True,
    )
    checks.append(_pass("baseline_progression", f"status={case.status}"))

    ok, errors = verify_case_history_integrity(case)
    if ok:
        checks.append(_pass("baseline_history_integrity", "integrity checks passed"))
    else:
        checks.append(_fail("baseline_history_integrity", "; ".join(errors[:3])))

    tampered_order = deepcopy(case)
    if len(tampered_order.history) >= 4:
        tampered_order.history[2], tampered_order.history[3] = (
            tampered_order.history[3],
            tampered_order.history[2],
        )
    order_ok, order_errors = verify_case_history_integrity(tampered_order)
    if not order_ok:
        checks.append(_pass("detect_order_tamper", "; ".join(order_errors[:2])))
    else:
        checks.append(_fail("detect_order_tamper", "order tamper was not detected"))

    tampered_seq = deepcopy(case)
    if len(tampered_seq.history) >= 2:
        tampered_seq.history[1].event_seq = 99
    seq_ok, seq_errors = verify_case_history_integrity(tampered_seq)
    if not seq_ok:
        checks.append(_pass("detect_sequence_tamper", "; ".join(seq_errors[:2])))
    else:
        checks.append(_fail("detect_sequence_tamper", "sequence tamper was not detected"))

    payload = {
        "final_status": case.status,
        "history_length": len(case.history),
        "used_auth_proof_ids": list(case.used_auth_proof_ids),
        "sample_case": case.to_dict(),
    }
    return checks, payload


def _build_markdown(generated_utc: str, overall_status: str, checks: List[CheckResult], details: Dict[str, object]) -> str:
    lines = [
        "# Freed ID Dispute/Recourse Adversarial Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        "- control_id: `GOV-004`",
        f"- mode: `adversarial`",
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
            "## Detail snapshot",
            "```json",
            json.dumps(details, indent=2),
            "```",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run adversarial GOV-004 dispute/recourse checks.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs")
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-dispute-recourse-adversarial-latest.json",
        help="Path for latest JSON artifact.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-dispute-recourse-adversarial-latest.md",
        help="Path for latest markdown artifact.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    checks, detail_payload = _run_verification()
    overall_status = "PASS" if all(item.status == "PASS" for item in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-004",
        "mode": "adversarial",
        "overall_status": overall_status,
        "checks": [asdict(item) for item in checks],
        "detail": detail_payload,
    }
    markdown = _build_markdown(generated_utc, overall_status, checks, detail_payload)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-freedid-dispute-recourse-adversarial-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-dispute-recourse-adversarial-check.md"
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
