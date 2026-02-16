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


@dataclass
class DisputeEvent:
    at_utc: str
    actor: str
    actor_role: str
    from_status: str
    to_status: str
    note: str
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
            at_utc=case.opened_utc,
            actor=opened_by,
            actor_role=_infer_actor_role(opened_by),
            from_status="none",
            to_status="opened",
            note="case opened",
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
) -> DisputeCase:
    allowed = ALLOWED_TRANSITIONS.get(case.status, set())
    if to_status not in allowed:
        raise ValueError(f"Invalid transition: {case.status} -> {to_status}")

    resolved_role = _normalize_actor_role(actor_role, actor)
    if enforce_actor_policy:
        allowed_roles = ALLOWED_ROLES_BY_TRANSITION.get((case.status, to_status), set())
        if resolved_role not in allowed_roles:
            raise PermissionError(
                f"Unauthorized transition actor role: role={resolved_role} transition={case.status}->{to_status}"
            )

    event = DisputeEvent(
        at_utc=_utc_now(),
        actor=actor,
        actor_role=resolved_role,
        from_status=case.status,
        to_status=to_status,
        note=note,
        evidence_refs=list(evidence_refs or []),
    )
    case.history.append(event)
    case.status = to_status
    return case
