"""
freed_id_registry.py
====================

Minimal in-memory Freed ID registry implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid

from did_webvh import DidWebVHError, DidWebvh

from freed_id_minimum_disclosure import (
    MinimumDisclosurePolicy,
    build_minimum_disclosure_presentation,
)


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

    def __init__(self, authority: str, data_dir: str) -> None:
        self.authority = authority
        self.webvh = DidWebvh(authority, data_dir)




    async def register(self, doc: DIDDocument) -> str:
        try:
            return await self.webvh.create(doc.to_dict())
        except DidWebVHError as e:
            raise ValueError(f"Failed to register DID: {e}") from e



    async def resolve(self, did: str) -> Optional[DIDDocument]:
        try:
            doc = await self.webvh.resolve(did)
            if doc:
                return DIDDocument(
                    did=doc["id"],
                    controller=doc["controller"],
                    verification_methods=doc.get("verificationMethod", []),
                    services=doc.get("service", []),
                    revoked=doc.get("revoked", False),
                )
            return None
        except DidWebVHError as e:
            raise ValueError(f"Failed to resolve DID: {e}") from e



    async def update(self, did: str, new_doc: DIDDocument) -> None:
        try:
            await self.webvh.update(did, new_doc.to_dict())
        except DidWebVHError as e:
            raise ValueError(f"Failed to update DID: {e}") from e



    async def revoke(self, did: str) -> None:
        try:
            await self.webvh.revoke(did)
        except DidWebVHError as e:
            raise ValueError(f"Failed to revoke DID: {e}") from e



    async def list_active(self) -> List[str]:
        # This is not directly supported by did-webvh, as it's a decentralized protocol.
        # We could implement a caching layer to support this, but for now we'll return an empty list.
        return []



    async def issue_credential(self, did: str, credential: Dict[str, object]) -> None:
        doc = await self.resolve(did)
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
        await self.update(did, doc)

    async def verify_credential(self, did: str, credential_id: str) -> bool:
        doc = await self.resolve(did)
        if not doc or doc.revoked:
            return False
        return any(s.get("id") == credential_id for s in doc.services)

    async def build_credential_presentation(
        self,
        did: str,
        credential_id: str,
        requested_fields: List[str],
        policy: MinimumDisclosurePolicy,
    ) -> Dict[str, object]:
        doc = await self.resolve(did)
        if not doc:
            raise KeyError(f"DID not found: {did}")

        credential_service = next(
            (s for s in doc.services if s.get("id") == credential_id), None
        )
        if not credential_service:
            raise KeyError(f"Credential not found: {credential_id}")

        claims = credential_service.get("credential", {})

        if not isinstance(claims, dict):
            raise TypeError("claims must be a dict")

        return build_minimum_disclosure_presentation(
            subject_did=did,
            credential_id=credential_id,
            claims=claims,
            requested_fields=requested_fields,
            policy=policy,
        )



        



        
