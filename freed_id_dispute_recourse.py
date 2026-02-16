"""
freed_id_dispute_recourse.py
----------------------------

Minimal dispute/recourse workflow scaffold for Freed ID governance control GOV-004.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Set


ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    "opened": {"review", "dismissed"},
    "review": {"resolved", "dismissed", "escalated"},
    "escalated": {"review", "resolved"},
    "resolved": {"reopened"},
    "dismissed": {"reopened"},
    "reopened": {"review"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class DisputeEvent:
    at_utc: str
    actor: str
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
) -> DisputeCase:
    allowed = ALLOWED_TRANSITIONS.get(case.status, set())
    if to_status not in allowed:
        raise ValueError(f"Invalid transition: {case.status} -> {to_status}")

    event = DisputeEvent(
        at_utc=_utc_now(),
        actor=actor,
        from_status=case.status,
        to_status=to_status,
        note=note,
        evidence_refs=list(evidence_refs or []),
    )
    case.history.append(event)
    case.status = to_status
    return case
