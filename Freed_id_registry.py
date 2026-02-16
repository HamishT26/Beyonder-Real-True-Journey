"""
freed_id_registry.py
====================

Minimal in-memory Freed ID registry implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


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

    def __init__(self) -> None:
        self._store: Dict[str, DIDDocument] = {}

    def _generate_did(self) -> str:
        return f"did:freed:{uuid.uuid4().hex}"

    def register(self, doc: DIDDocument) -> str:
        did = doc.did or self._generate_did()
        if did in self._store and not self._store[did].revoked:
            raise ValueError(f"DID {did} already exists and is active")
        doc.did = did
        self._store[did] = doc
        return did

    def resolve(self, did: str) -> Optional[DIDDocument]:
        return self._store.get(did)

    def update(self, did: str, new_doc: DIDDocument) -> None:
        if did not in self._store or self._store[did].revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        if did != new_doc.did:
            raise ValueError("DID mismatch in update")
        self._store[did] = new_doc

    def revoke(self, did: str) -> None:
        doc = self._store.get(did)
        if not doc:
            raise KeyError(f"DID {did} does not exist")
        doc.revoked = True

    def list_active(self) -> List[str]:
        return [did for did, doc in self._store.items() if not doc.revoked]

    def issue_credential(self, did: str, credential: Dict[str, object]) -> None:
        doc = self._store.get(did)
        if not doc or doc.revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        doc.services.append(
            {
                "id": f"{did}#cred-{len(doc.services)}",
                "type": "FreedIDCredential",
                "credential": credential,
            }
        )

    def verify_credential(self, did: str, credential_id: str) -> bool:
        doc = self._store.get(did)
        if not doc or doc.revoked:
            return False
        return any(service.get("id") == credential_id for service in doc.services)
