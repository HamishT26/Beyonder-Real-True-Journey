"""
freed_id_did_signature_verifier.py
----------------------------------

GOV-004 scaffold: build a SignatureVerifier that resolves the signer's DID via the
Freed ID registry and verifies the signature_ref cryptographically against the DID
Document's verification methods (Ed25519 when cryptography is available).
"""

from __future__ import annotations

import base64
import binascii
from typing import TYPE_CHECKING, Callable, Dict, Optional

if TYPE_CHECKING:
    from Freed_id_registry import FreedIDRegistry

REQUIRED_AUTH_PROOF_FIELDS = {"proof_id", "signer_did", "signature_ref", "issued_at_utc"}
SignatureVerifier = Callable[[str, Dict[str, str]], bool]

# Optional Ed25519: use cryptography if present so we don't force a dependency.
def _verify_ed25519(payload: bytes, signature_ref: str, public_key_hex: str) -> bool:
    """Verify Ed25519 signature over payload. Returns False if crypto unavailable or invalid."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        return False
    try:
        key_bytes = bytes.fromhex(public_key_hex)
    except (ValueError, TypeError):
        return False
    if len(key_bytes) != 32:
        return False
    try:
        sig_bytes: Optional[bytes] = None
        if len(signature_ref) == 128 and all(c in "0123456789abcdefABCDEF" for c in signature_ref):
            sig_bytes = bytes.fromhex(signature_ref)
        else:
            padded = signature_ref + "==" if len(signature_ref) % 4 else signature_ref
            sig_bytes = base64.urlsafe_b64decode(padded)
        if not sig_bytes or len(sig_bytes) != 64:
            return False
    except (ValueError, binascii.Error):
        return False
    try:
        pub = Ed25519PublicKey.from_public_bytes(key_bytes)
        pub.verify(sig_bytes, payload)
        return True
    except Exception:
        return False


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
        signature_ref = str(auth_proof.get("signature_ref", "")).strip()
        if not signature_ref:
            return False
        for vm in doc.verification_methods:
            if not isinstance(vm, dict):
                continue
            vm_type = str(vm.get("type") or "").strip()
            pub_hex = (vm.get("publicKeyHex") or "").strip()
            if vm_type == "Ed25519VerificationKey2020" and pub_hex:
                if len(pub_hex) == 64 and all(c in "0123456789abcdefABCDEF" for c in pub_hex):
                    if _verify_ed25519(payload_bytes, signature_ref, pub_hex):
                        return True
        return False

    return verifier
