"""
freed_id_dispute_recourse.py
----------------------------

Dispute/recourse workflow scaffold for Freed ID governance control GOV-004.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple


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

    if case.status != case.history[-1].to_status:
        errors.append(f"case.status mismatch: case.status={case.status} history_last={case.history[-1].to_status}")

    proof_history_sorted = sorted(seen_proof_ids)
    proof_case_sorted = sorted(case.used_auth_proof_ids)
    if proof_history_sorted != proof_case_sorted:
        errors.append("used_auth_proof_ids does not match proof IDs present in history")

    return len(errors) == 0, errors
