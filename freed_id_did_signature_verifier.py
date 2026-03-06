"""
freed_id_did_signature_verifier.py
----------------------------------

GOV-004 utilities for DID-method signature verification.
"""

from __future__ import annotations

import base64
import binascii
from typing import TYPE_CHECKING, Callable, Dict

if TYPE_CHECKING:
    from freed_id_registry import FreedIDRegistry

REQUIRED_AUTH_PROOF_FIELDS = {"proof_id", "signer_did", "signature_ref", "issued_at_utc"}
ED25519_METHOD_TYPES = {"Ed25519VerificationKey2020", "Ed25519VerificationKey2018"}
SignatureVerifier = Callable[[str, Dict[str, str]], bool]


def build_canonical_payload(auth_proof: Dict[str, str]) -> bytes:
    """
    Build the canonical signed payload (v0) for GOV-004 auth proofs.

    Contract: proof_id + newline + signer_did + newline + issued_at_utc (UTF-8).
    """

    return (
        auth_proof["proof_id"].encode("utf-8")
        + b"\n"
        + auth_proof["signer_did"].encode("utf-8")
        + b"\n"
        + auth_proof["issued_at_utc"].encode("utf-8")
    )


def verify_ed25519_signature_ref(payload: bytes, signature_value: str, public_key_hex: str) -> bool:
    """Verify an Ed25519 signature encoded as hex or base64url."""

    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        return False

    try:
        key_bytes = bytes.fromhex(public_key_hex)
    except (TypeError, ValueError):
        return False
    if len(key_bytes) != 32:
        return False

    try:
        if len(signature_value) == 128 and all(char in "0123456789abcdefABCDEF" for char in signature_value):
            signature_bytes = bytes.fromhex(signature_value)
        else:
            padded = signature_value + ("=" * ((4 - len(signature_value) % 4) % 4))
            signature_bytes = base64.urlsafe_b64decode(padded.encode("ascii"))
    except (ValueError, binascii.Error):
        return False
    if len(signature_bytes) != 64:
        return False

    try:
        public_key = Ed25519PublicKey.from_public_bytes(key_bytes)
        public_key.verify(signature_bytes, payload)
        return True
    except Exception:
        return False


def build_did_method_signature_verifier(registry: "FreedIDRegistry") -> SignatureVerifier:
    """
    Return a SignatureVerifier that resolves verification methods from the Freed ID registry.

    This verifier currently supports Ed25519 verification methods and uses the v0
    canonical auth-proof payload defined in the GOV-004 scaffold doc.
    """

    def verifier(actor: str, auth_proof: Dict[str, str]) -> bool:
        if not auth_proof:
            return False
        missing = [field for field in REQUIRED_AUTH_PROOF_FIELDS if not str(auth_proof.get(field, "")).strip()]
        if missing:
            return False

        signer_did = str(auth_proof["signer_did"]).strip()
        if signer_did != actor:
            return False

        doc = registry.resolve(signer_did)
        if doc is None or doc.revoked:
            return False

        signature_value = str(auth_proof.get("signature_hex") or auth_proof.get("signature_ref") or "").strip()
        if not signature_value:
            return False

        payload = build_canonical_payload(auth_proof)
        for method in doc.verification_methods:
            if not isinstance(method, dict):
                continue
            method_type = str(method.get("type", "")).strip()
            if method_type not in ED25519_METHOD_TYPES:
                continue
            public_key_hex = str(method.get("publicKeyHex", "")).strip()
            if public_key_hex and verify_ed25519_signature_ref(payload, signature_value, public_key_hex):
                return True
        return False

    return verifier
