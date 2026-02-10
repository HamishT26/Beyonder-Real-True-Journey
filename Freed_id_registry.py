"""
freed_id_registry.py
====================

This module implements a minimal Freed ID registry service for managing self‑sovereign
identifiers and associated DID Documents.  It is designed to accompany the Freed ID
specification and demonstrate how identifiers can be stored, resolved and revoked
within the Trinity Hybrid‑AI framework.  The registry is intentionally simple: it
uses in‑memory data structures and does not persist data to disk or a blockchain.

Usage
-----

```
from freed_id_registry import FreedIDRegistry, DIDDocument

registry = FreedIDRegistry()
doc = DIDDocument(
    did="did:freed:example:1234", controller="did:freed:example:1234",
    verification_methods=[{"id": "did:freed:example:1234#keys-1", "type": "Ed25519VerificationKey2018", "publicKeyBase58": "GfH2..."}],
    services=[{"id": "did:freed:example:1234#cred", "type": "FreedIDCredentialRegistry", "serviceEndpoint": "https://..."}]
)

registry.register(doc)
fetched = registry.resolve("did:freed:example:1234")
print(fetched)
```

The registry can be integrated into the Trinity orchestrator to authenticate agents
and to manage credentials under the Cosmic Bill of Rights.
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
    """
    A simple in‑memory registry for Freed ID DID Documents.

    The registry provides methods to register, resolve, update and revoke
    identifiers.  In a production system, this would be backed by a
    distributed ledger or database and include cryptographic
    verification.
    """

    def __init__(self):
        self._store: Dict[str, DIDDocument] = {}

    def _generate_did(self) -> str:
        """Generate a new unique Freed DID using UUID4."""
        return f"did:freed:{uuid.uuid4().hex}"

    def register(self, doc: DIDDocument) -> str:
        """
        Register a new DID Document.

        If the DID is None or empty, a new DID will be generated.  If the
        DID already exists and is not revoked, registration will raise an
        error.

        Args:
            doc (DIDDocument): Document to register.

        Returns:
            str: The DID assigned to the document.
        """
        did = doc.did or self._generate_did()
        if did in self._store and not self._store[did].revoked:
            raise ValueError(f"DID {did} already exists and is active")
        doc.did = did
        self._store[did] = doc
        return did

    def resolve(self, did: str) -> Optional[DIDDocument]:
        """
        Retrieve a DID Document by its identifier.

        Args:
            did (str): Identifier to resolve.

        Returns:
            Optional[DIDDocument]: The document if it exists, None otherwise.
        """
        return self._store.get(did)

    def update(self, did: str, new_doc: DIDDocument) -> None:
        """
        Update an existing DID Document.  The DID in new_doc must match the
        DID parameter.  The previous document must exist and not be revoked.

        Args:
            did (str): The identifier to update.
            new_doc (DIDDocument): New document data.
        """
        if did not in self._store or self._store[did].revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        if did != new_doc.did:
            raise ValueError("DID mismatch in update")
        self._store[did] = new_doc

    def revoke(self, did: str) -> None:
        """
        Revoke an existing DID Document.  After revocation, the DID cannot
        be updated or re‑registered and will be marked as revoked.

        Args:
            did (str): The identifier to revoke.
        """
        doc = self._store.get(did)
        if not doc:
            raise KeyError(f"DID {did} does not exist")
        doc.revoked = True

    def list_active(self) -> List[str]:
        """Return a list of all active (non‑revoked) DIDs."""
        return [did for did, doc in self._store.items() if not doc.revoked]

    def issue_credential(self, did: str, credential: Dict[str, object]) -> None:
        """
        Add a verifiable credential to the service endpoints of the DID Document.
        In a real system, credentials would be cryptographically signed and
        referenced externally.  Here we simply append to the service list.

        Args:
            did (str): DID to which the credential applies.
            credential (Dict[str, object]): Credential data.
        """
        doc = self._store.get(did)
        if not doc or doc.revoked:
            raise KeyError(f"DID {did} does not exist or is revoked")
        doc.services.append({
            "id": f"{did}#cred-{len(doc.services)}",
            "type": "FreedIDCredential",
            "credential": credential
        })

    def verify_credential(self, did: str, credential_id: str) -> bool:
        """
        Verify that a credential exists for a given DID.

        Args:
            did (str): Identifier of the document.
            credential_id (str): Identifier of the credential to verify.

        Returns:
            bool: True if credential exists and DID is active, False otherwise.
        """
        doc = self._store.get(did)
        if not doc or doc.revoked:
            return False
        return any(service.get("id") == credential_id for service in doc.services)
