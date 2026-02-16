"""
freed_id_dispute_recourse.py
----------------------------

Dispute/recourse workflow scaffold for Freed ID governance control GOV-004.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Set, Tuple


ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    "opened": {"review", "dismissed"},
    "review": {"resolved", "dismissed", "escalated"},
    "escalated": {"review", "resolved"},
    "resolved": {"reopened"},
    "dismissed": {"reopened"},
    "reopened": {"review"},
}

ROLE_TOKENS = {"subject", "reviewer", "council", "ombuds", "system", "unknown"}
REQUIRED_AUTH_PROOF_FIELDS = {"proof_id", "signer_did", "signature_ref", "issued_at_utc"}
REQUIRED_SIGNATURE_FIELDS = {"verification_method_id", "payload_sha256", "signature_hex"}

# v0.1 role policy: role-prefix checks before cryptographic actor binding is added.
ALLOWED_ROLES_BY_TRANSITION: Dict[Tuple[str, str], Set[str]] = {
    ("opened", "review"): {"reviewer", "ombuds"},
    ("opened", "dismissed"): {"reviewer", "ombuds"},
    ("review", "resolved"): {"reviewer", "council"},
    ("review", "dismissed"): {"reviewer", "council"},
    ("review", "escalated"): {"reviewer", "ombuds"},
    ("escalated", "review"): {"council", "ombuds"},
    ("escalated", "resolved"): {"council"},
    ("resolved", "reopened"): {"subject", "ombuds"},
    ("dismissed", "reopened"): {"subject", "ombuds"},
    ("reopened", "review"): {"reviewer", "ombuds"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _infer_actor_role(actor: str) -> str:
    """
    Infer actor role from DID suffix convention: did:freed:<role>-<id>.
    """
    tail = actor.rsplit(":", maxsplit=1)[-1]
    token = tail.split("-", maxsplit=1)[0].lower()
    if token in ROLE_TOKENS:
        return token
    return "unknown"


def _normalize_actor_role(actor_role: str | None, actor: str) -> str:
    if actor_role is None:
        return _infer_actor_role(actor)
    normalized = actor_role.strip().lower()
    if normalized in ROLE_TOKENS:
        return normalized
    return "unknown"


def _resolve_auth_proof(
    auth_proof: Dict[str, str] | None,
    *,
    actor: str,
    require_auth_proof: bool,
    enforce_signer_match: bool,
) -> Tuple[str | None, str | None]:
    if auth_proof is None:
        if require_auth_proof:
            raise PermissionError("Missing auth proof for transition.")
        return None, None

    missing = sorted(
        field for field in REQUIRED_AUTH_PROOF_FIELDS if not str(auth_proof.get(field, "")).strip()
    )
    if missing:
        raise PermissionError(f"Auth proof missing required fields: {missing}")

    proof_id = str(auth_proof["proof_id"]).strip()
    signer_did = str(auth_proof["signer_did"]).strip()
    if enforce_signer_match and signer_did != actor:
        raise PermissionError(f"Auth signer mismatch: signer={signer_did} actor={actor}")
    return proof_id, signer_did


def _build_transition_payload(
    case: "DisputeCase",
    *,
    event_seq: int,
    actor: str,
    to_status: str,
    note: str,
) -> str:
    payload = {
        "actor": actor,
        "case_id": case.case_id,
        "credential_id": case.credential_id,
        "event_seq": event_seq,
        "from_status": case.status,
        "note": note,
        "subject_did": case.subject_did,
        "to_status": to_status,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sign_payload_hmac(payload: str, secret_key_hex: str) -> str:
    try:
        secret = bytes.fromhex(secret_key_hex)
    except ValueError as exc:  # pragma: no cover - defensive
        raise PermissionError("Invalid secretKeyHex for verification method.") from exc
    if not secret:
        raise PermissionError("Empty secretKeyHex for verification method.")
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def build_hmac_transition_auth_proof(
    case: "DisputeCase",
    *,
    proof_id: str,
    actor: str,
    to_status: str,
    note: str,
    verification_method_id: str,
    secret_key_hex: str,
    signer_did: str | None = None,
    signature_ref: str | None = None,
    issued_at_utc: str | None = None,
    event_seq: int | None = None,
) -> Dict[str, str]:
    resolved_signer = signer_did or actor
    resolved_event_seq = len(case.history) if event_seq is None else event_seq
    payload = _build_transition_payload(
        case,
        event_seq=resolved_event_seq,
        actor=actor,
        to_status=to_status,
        note=note,
    )
    payload_sha256 = _sha256_hex(payload)
    signature_hex = _sign_payload_hmac(payload, secret_key_hex)
    return {
        "proof_id": proof_id,
        "signer_did": resolved_signer,
        "signature_ref": signature_ref or f"sig://{proof_id}",
        "issued_at_utc": issued_at_utc or _utc_now(),
        "verification_method_id": verification_method_id,
        "payload_sha256": payload_sha256,
        "signature_hex": signature_hex,
        "signature_algorithm": "hmac-sha256-v1",
    }


def _verify_transition_signature(
    case: "DisputeCase",
    *,
    event_seq: int,
    actor: str,
    signer_did: str,
    to_status: str,
    note: str,
    auth_proof: Dict[str, str] | None,
    verification_method_resolver: Callable[[str, str], Dict[str, object] | None] | None,
) -> Tuple[str, str]:
    if auth_proof is None:
        raise PermissionError("Missing auth proof for signature verification.")
    if verification_method_resolver is None:
        raise PermissionError("Missing verification method resolver.")

    missing = sorted(field for field in REQUIRED_SIGNATURE_FIELDS if not str(auth_proof.get(field, "")).strip())
    if missing:
        raise PermissionError(f"Auth proof missing signature fields: {missing}")

    verification_method_id = str(auth_proof["verification_method_id"]).strip()
    verification_method = verification_method_resolver(signer_did, verification_method_id)
    if not isinstance(verification_method, dict):
        raise PermissionError(
            f"Unknown verification method for signer: signer={signer_did} method={verification_method_id}"
        )

    method_id = str(verification_method.get("id", "")).strip()
    if method_id != verification_method_id:
        raise PermissionError("Verification method id mismatch.")
    controller = str(verification_method.get("controller", signer_did)).strip()
    if controller and controller != signer_did:
        raise PermissionError(f"Verification method controller mismatch: controller={controller} signer={signer_did}")

    method_type = str(verification_method.get("type", "")).strip().lower()
    if method_type not in {"hmacsha256verificationkey2026", "hmac-sha256-verification-key-2026"}:
        raise PermissionError(f"Unsupported verification method type: {verification_method.get('type')}")
    secret_key_hex = str(verification_method.get("secretKeyHex", "")).strip()
    if not secret_key_hex:
        raise PermissionError("Verification method missing secretKeyHex.")

    payload = _build_transition_payload(
        case,
        event_seq=event_seq,
        actor=actor,
        to_status=to_status,
        note=note,
    )
    payload_sha256 = _sha256_hex(payload)
    claimed_payload_sha = str(auth_proof["payload_sha256"]).strip().lower()
    if payload_sha256 != claimed_payload_sha:
        raise PermissionError("Auth proof payload digest mismatch.")

    expected_signature = _sign_payload_hmac(payload, secret_key_hex)
    provided_signature = str(auth_proof["signature_hex"]).strip().lower()
    if not hmac.compare_digest(expected_signature, provided_signature):
        raise PermissionError("Invalid auth proof signature.")
    return verification_method_id, payload_sha256


@dataclass
class DisputeEvent:
    event_id: str
    event_seq: int
    at_utc: str
    actor: str
    actor_role: str
    from_status: str
    to_status: str
    note: str
    auth_proof_id: str | None = None
    auth_signer_did: str | None = None
    verification_method_id: str | None = None
    payload_sha256: str | None = None
    signature_verified: bool = False
    evidence_refs: List[str] = field(default_factory=list)


@dataclass
class DisputeCase:
    case_id: str
    subject_did: str
    credential_id: str
    reason: str
    opened_utc: str
    opened_by: str
    status: str = "opened"
    evidence_refs: List[str] = field(default_factory=list)
    history: List[DisputeEvent] = field(default_factory=list)
    used_auth_proof_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "case_id": self.case_id,
            "subject_did": self.subject_did,
            "credential_id": self.credential_id,
            "reason": self.reason,
            "opened_utc": self.opened_utc,
            "opened_by": self.opened_by,
            "status": self.status,
            "evidence_refs": list(self.evidence_refs),
            "used_auth_proof_ids": list(self.used_auth_proof_ids),
            "history": [asdict(event) for event in self.history],
        }


def open_dispute_case(
    *,
    case_id: str,
    subject_did: str,
    credential_id: str,
    opened_by: str,
    reason: str,
    evidence_refs: List[str] | None = None,
) -> DisputeCase:
    case = DisputeCase(
        case_id=case_id,
        subject_did=subject_did,
        credential_id=credential_id,
        reason=reason,
        opened_utc=_utc_now(),
        opened_by=opened_by,
        evidence_refs=list(evidence_refs or []),
    )
    case.history.append(
        DisputeEvent(
            event_id=f"{case.case_id}:event:0000",
            event_seq=0,
            at_utc=case.opened_utc,
            actor=opened_by,
            actor_role=_infer_actor_role(opened_by),
            from_status="none",
            to_status="opened",
            note="case opened",
            auth_proof_id=None,
            auth_signer_did=opened_by,
            verification_method_id=None,
            payload_sha256=None,
            signature_verified=False,
            evidence_refs=list(evidence_refs or []),
        )
    )
    return case


def transition_case(
    case: DisputeCase,
    *,
    to_status: str,
    actor: str,
    note: str,
    evidence_refs: List[str] | None = None,
    actor_role: str | None = None,
    enforce_actor_policy: bool = False,
    auth_proof: Dict[str, str] | None = None,
    require_auth_proof: bool = False,
    enforce_signer_match: bool = True,
    reject_replayed_proof: bool = False,
    verification_method_resolver: Callable[[str, str], Dict[str, object] | None] | None = None,
    require_signature_verification: bool = False,
) -> DisputeCase:
    allowed = ALLOWED_TRANSITIONS.get(case.status, set())
    if to_status not in allowed:
        raise ValueError(f"Invalid transition: {case.status} -> {to_status}")

    resolved_role = _normalize_actor_role(actor_role, actor)
    proof_id, signer_did = _resolve_auth_proof(
        auth_proof,
        actor=actor,
        require_auth_proof=require_auth_proof,
        enforce_signer_match=enforce_signer_match,
    )
    if enforce_actor_policy:
        allowed_roles = ALLOWED_ROLES_BY_TRANSITION.get((case.status, to_status), set())
        if resolved_role not in allowed_roles:
            raise PermissionError(
                f"Unauthorized transition actor role: role={resolved_role} transition={case.status}->{to_status}"
            )
    if reject_replayed_proof and proof_id is not None and proof_id in case.used_auth_proof_ids:
        raise PermissionError(f"Replay auth proof detected: proof_id={proof_id}")

    event_seq = len(case.history)
    verification_method_id: str | None = None
    payload_sha256: str | None = None
    signature_verified = False
    if require_signature_verification:
        if signer_did is None:
            raise PermissionError("Signer DID is required for signature verification.")
        verification_method_id, payload_sha256 = _verify_transition_signature(
            case,
            event_seq=event_seq,
            actor=actor,
            signer_did=signer_did,
            to_status=to_status,
            note=note,
            auth_proof=auth_proof,
            verification_method_resolver=verification_method_resolver,
        )
        signature_verified = True

    event = DisputeEvent(
        event_id=f"{case.case_id}:event:{event_seq:04d}",
        event_seq=event_seq,
        at_utc=_utc_now(),
        actor=actor,
        actor_role=resolved_role,
        from_status=case.status,
        to_status=to_status,
        note=note,
        auth_proof_id=proof_id,
        auth_signer_did=signer_did,
        verification_method_id=verification_method_id,
        payload_sha256=payload_sha256,
        signature_verified=signature_verified,
        evidence_refs=list(evidence_refs or []),
    )
    case.history.append(event)
    if proof_id is not None:
        case.used_auth_proof_ids.append(proof_id)
    case.status = to_status
    return case


def verify_case_history_integrity(case: DisputeCase) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not case.history:
        return False, ["history is empty"]

    seen_proof_ids: Set[str] = set()
    for index, event in enumerate(case.history):
        expected_event_id = f"{case.case_id}:event:{index:04d}"
        if event.event_seq != index:
            errors.append(f"event_seq mismatch at index={index}: got={event.event_seq}")
        if event.event_id != expected_event_id:
            errors.append(f"event_id mismatch at index={index}: got={event.event_id}")

        if index == 0:
            if event.from_status != "none" or event.to_status != "opened":
                errors.append("first event must be none->opened")
        else:
            prev = case.history[index - 1]
            if event.from_status != prev.to_status:
                errors.append(
                    f"status chain mismatch at index={index}: from={event.from_status} prev_to={prev.to_status}"
                )
            if event.at_utc < prev.at_utc:
                errors.append(f"timestamp order mismatch at index={index}")

        if event.auth_proof_id:
            if event.auth_proof_id in seen_proof_ids:
                errors.append(f"duplicate auth_proof_id in history: {event.auth_proof_id}")
            seen_proof_ids.add(event.auth_proof_id)
            if not event.signature_verified:
                errors.append(f"signature_verified=false for proof event at index={index}")
            if not event.verification_method_id:
                errors.append(f"missing verification_method_id for proof event at index={index}")
            if not event.payload_sha256:
                errors.append(f"missing payload_sha256 for proof event at index={index}")

    if case.status != case.history[-1].to_status:
        errors.append(f"case.status mismatch: case.status={case.status} history_last={case.history[-1].to_status}")

    proof_history_sorted = sorted(seen_proof_ids)
    proof_case_sorted = sorted(case.used_auth_proof_ids)
    if proof_history_sorted != proof_case_sorted:
        errors.append("used_auth_proof_ids does not match proof IDs present in history")

    return len(errors) == 0, errors
