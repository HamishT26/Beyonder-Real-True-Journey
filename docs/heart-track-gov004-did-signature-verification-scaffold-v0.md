# GOV-004 DID-Method Signature Verification Scaffold v0 (Heart Track)

Purpose: define the **contract and integration path** for replacing callback-level signature checks with **DID-method cryptographic verification** against the Freed ID registry, so GOV-004 transitions can require proof that the actor holds the private key for their DID.

---

## Current state

- `freed_id_dispute_recourse.apply_transition(..., signature_verifier=...)` accepts a `SignatureVerifier` callback: `(actor: str, auth_proof: Dict[str, str]) -> bool`.
- Auth proof must include: `proof_id`, `signer_did`, `signature_ref`, `issued_at_utc`.
- Existing verifiers (in dispute_recourse_verifier.py and adversarial_verifier.py) use **callback-level** checks (e.g. signer_did == actor). The control matrix next action is: *Replace callback-level checks with DID-method cryptographic signature verification against registry verification methods.*

---

## Target contract (DID-method verifier)

A **DID-method signature verifier** should:

1. **Resolve** `signer_did` (from `auth_proof`) via the Freed ID registry → obtain DID Document.
2. **Obtain** the verification method (e.g. public key or verificationMaterial) from the DID Document’s `verificationMethod` (or equivalent).
3. **Verify** that `signature_ref` (in `auth_proof`) is a valid signature over a canonical payload (e.g. `proof_id` + `issued_at_utc` + transition context) using the resolved verification method.
4. **Return** `True` only if resolution succeeds, verification method is present, and the cryptographic verification passes. Return `False` otherwise (e.g. DID not found, no verification method, or signature invalid).

Payload canonicalization (what is signed) should be specified and stable so that all parties can reproduce it (e.g. `proof_id || issued_at_utc` or a small JSON canonical form).

---

## Integration point

- **Module:** `freed_id_did_signature_verifier.py` (new).
- **Export:** `build_did_method_signature_verifier(registry)` → returns a `SignatureVerifier` that uses `registry.resolve(signer_did)` and, when crypto is implemented, verifies `signature_ref` against the DID Document’s verification method.
- **Usage:** Callers (e.g. dispute workflow or Heart verifiers) pass this verifier when they want DID-method enforcement:  
  `apply_transition(..., signature_verifier=build_did_method_signature_verifier(registry), enforce_signature_verification=True)`.

---

## Implementation status (scaffold)

- **Done:** Design doc (this file); stub module that resolves the DID via registry and has a clear placeholder for cryptographic verification.
- **TODO:** Define canonical signed payload format; implement verification of `signature_ref` using `verification_methods` (e.g. Ed25519 or JWS); add tests that pass real signatures and fail on invalid ones; wire into Heart verifiers and require PASS when DID-method verifier is used.

---

## References

- `freed_id_dispute_recourse.py`: `SignatureVerifier`, `_resolve_auth_proof`, `apply_transition`.
- `freed_id_spec.md`: DID method, resolution, verification.
- `docs/freedid-cosmic-control-matrix-v0.md`: GOV-004 next action.

---

*Caelis · Session 3 · 2026-02-17 · Heart track advancement*
