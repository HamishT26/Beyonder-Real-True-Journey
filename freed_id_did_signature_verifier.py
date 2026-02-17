"""
freed_id_did_signature_verifier.py
----------------------------------

GOV-004 scaffold: build a SignatureVerifier that resolves the signer's DID via the
Freed ID registry and (when implemented) verifies the signature_ref cryptographically
against the DID Document's verification methods.

Current: stub that resolves the DID and returns False (crypto verification not yet
implemented). Integration point for DID-method signature verification.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict

if TYPE_CHECKING:
    from Freed_id_registry import FreedIDRegistry

REQUIRED_AUTH_PROOF_FIELDS = {"proof_id", "signer_did", "signature_ref", "issued_at_utc"}
SignatureVerifier = Callable[[str, Dict[str, str]], bool]


def build_canonical_payload(auth_proof: Dict[str, str]) -> bytes:
    """
    Build the canonical signed payload (v0) for GOV-004 auth proofs.

    Contract: proof_id + newline + signer_did + newline + issued_at_utc (UTF-8).
    See docs/heart-track-gov004-did-signature-verification-scaffold-v0.md.
    """
    return (
        auth_proof["proof_id"].encode("utf-8")
        + b"\n"
        + auth_proof["signer_did"].encode("utf-8")
        + b"\n"
        + auth_proof["issued_at_utc"].encode("utf-8")
    )


def build_did_method_signature_verifier(registry: "FreedIDRegistry") -> SignatureVerifier:
    """
    Return a SignatureVerifier that uses the registry to resolve the signer's DID.

    Contract (see docs/heart-track-gov004-did-signature-verification-scaffold-v0.md):
    1. Resolve signer_did (from auth_proof) via registry.resolve(signer_did).
    2. Obtain verification method from the DID Document.
    3. Verify signature_ref against a canonical payload using that method.

    Current implementation: resolves the DID; if not found or revoked, returns False.
    If found, crypto verification is not yet implemented (returns False) so that
    callers can wire this in and the next step is to add real verification.
    """

    def verifier(actor: str, auth_proof: Dict[str, str]) -> bool:
        if not auth_proof:
            return False
        missing = [f for f in REQUIRED_AUTH_PROOF_FIELDS if not str(auth_proof.get(f, "")).strip()]
        if missing:
            return False
        signer_did = str(auth_proof["signer_did"]).strip()
        if signer_did != actor:
            return False
        doc = registry.resolve(signer_did)
        if doc is None or doc.revoked:
            return False
        if not doc.verification_methods:
            return False
        payload_bytes = build_canonical_payload(auth_proof)
        # TODO (GOV-004): Verify auth_proof["signature_ref"] over payload_bytes using
        # doc.verification_methods (e.g. Ed25519). See Ed25519 test vector v0 in
        # docs/heart-track-gov004-did-signature-verification-scaffold-v0.md.
        _ = payload_bytes  # used when crypto is implemented
        return False

    return verifier
