"""
freed_id_registry.py
====================

Minimal in-memory Freed ID registry implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid

from freed_id_audit_log import FreedIDAuditLedger


@dataclass
class DIDDocument:
    """A simplified representation of a Freed ID DID Document."""

    did: str
    controller: str
    verification_methods: List[Dict[str, str]] = field(default_factory=list)
    services: List[Dict[str, str]] = field(default_factory=list)
    revoked: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "@context": "https://www.w3.org/ns/did/v1",
            "id": self.did,
            "controller": self.controller,
            "verificationMethod": self.verification_methods,
            "service": self.services,
            "revoked": self.revoked,
        }


class FreedIDRegistry:
    """A simple in-memory registry for Freed ID DID Documents."""

    def __init__(self, audit_ledger_path: Optional[str] = None) -> None:
        self._store: Dict[str, DIDDocument] = {}
        self._audit_ledger = (
            FreedIDAuditLedger(audit_ledger_path) if audit_ledger_path else None
        )

    def _audit(self, action: str, did: str, details: Optional[Dict[str, object]] = None) -> None:
        if self._audit_ledger is None:
            return
        self._audit_ledger.append(action=action, did=did, details=details or {})

    def _generate_did(self) -> str:
        return f"did:freed:{uuid.uuid4().hex}"

    def register(self, doc: DIDDocument) -> str:
        did = doc.did or self._generate_did()
        if did in self._store and not self._store[did].revoked:
            raise ValueError(f"DID {did} already exists and is active")
        doc.did = did
        self._store[did] = doc
        self._audit(
            "register",
            did,
            {
                "controller": doc.controller,
                "verification_method_count": len(doc.verification_methods),
                "service_count": len(doc.services),
            },
        )
        return did

    def resolve(self, did: str) -> Optional[DIDDocument]:
        return self._store.get(did)

    def update(self, did: str, new_doc: DIDDocument) -> None:
        if did not in self._store or self._store[did].revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        if did != new_doc.did:
            raise ValueError("DID mismatch in update")
        self._store[did] = new_doc
        self._audit(
            "update",
            did,
            {
                "verification_method_count": len(new_doc.verification_methods),
                "service_count": len(new_doc.services),
            },
        )

    def revoke(self, did: str) -> None:
        doc = self._store.get(did)
        if not doc:
            raise KeyError(f"DID {did} does not exist")
        doc.revoked = True
        self._audit("revoke", did, {"revoked": True})

    def list_active(self) -> List[str]:
        return [did for did, doc in self._store.items() if not doc.revoked]

    def issue_credential(self, did: str, credential: Dict[str, object]) -> None:
        doc = self._store.get(did)
        if not doc or doc.revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        credential_id = f"{did}#cred-{len(doc.services)}"
        doc.services.append(
            {
                "id": credential_id,
                "type": "FreedIDCredential",
                "credential": credential,
            }
        )
        self._audit(
            "issue_credential",
            did,
            {
                "credential_id": credential_id,
                "credential_keys": sorted(str(key) for key in credential.keys()),
            },
        )

    def verify_credential(self, did: str, credential_id: str) -> bool:
        doc = self._store.get(did)
        if not doc or doc.revoked:
            return False
        return any(service.get("id") == credential_id for service in doc.services)
