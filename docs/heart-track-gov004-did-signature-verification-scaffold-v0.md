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
  `transition_case(..., signature_verifier=build_did_method_signature_verifier(registry), enforce_signature_verification=True)`.

---

## Integration example (wire into dispute flow)

To use the DID-method verifier in a dispute transition (e.g. in a Heart verifier or service that holds a registry):

```python
from Freed_id_registry import FreedIDRegistry
from freed_id_dispute_recourse import transition_case, open_dispute_case
from freed_id_did_signature_verifier import build_did_method_signature_verifier

registry = FreedIDRegistry(audit_ledger_path="docs/freed-id-audit-log.jsonl")
did_verifier = build_did_method_signature_verifier(registry)

# When applying a transition that must be DID-verified:
transition_case(
    case=case,
    new_status="review",
    actor="did:freed:reviewer-abc",
    auth_proof={"proof_id": "...", "signer_did": "did:freed:reviewer-abc", "signature_ref": "...", "issued_at_utc": "..."},
    require_auth_proof=True,
    enforce_signer_match=True,
    enforce_signature_verification=True,
    signature_verifier=did_verifier,
    reject_replayed_proof=True,
)
```

Until crypto is implemented in the stub, `did_verifier` will return `False`, so transitions with `enforce_signature_verification=True` will raise `PermissionError`. Use the existing callback verifier in tests until the stub is replaced with real verification.

---

## Canonical signed payload (v0)

So that signers and verifiers agree on the exact bytes to sign, the **canonical payload** for GOV-004 auth proofs is defined as follows.

**Source fields (from `auth_proof`):** `proof_id`, `signer_did`, `issued_at_utc`. All must be non-empty strings.

**Construction (deterministic):**

1. Take the three values in order: `proof_id`, `signer_did`, `issued_at_utc`.
2. Encode each as UTF-8. Concatenate with a single newline `\n` (U+000A) between them, no trailing newline.
3. **Payload bytes** = `proof_id_utf8 + b"\n" + signer_did_utf8 + b"\n" + issued_at_utc_utf8`.

**Example (Python):**

```python
payload_bytes = (
    auth_proof["proof_id"].encode("utf-8") + b"\n" +
    auth_proof["signer_did"].encode("utf-8") + b"\n" +
    auth_proof["issued_at_utc"].encode("utf-8")
)
# Sign payload_bytes with the private key corresponding to the DID's verification method.
# signature_ref = base64url(signature) or hex(signature) per verification method type.
```

**Verifier:** Recompute `payload_bytes` from `auth_proof` using the same construction; resolve `signer_did` to get the verification method; verify that the value in `signature_ref` is a valid signature over `payload_bytes` for that method (e.g. Ed25519). Accept only if verification succeeds.

**Stability:** This format is v0. Future versions may add optional fields (e.g. `case_id`, `from_status`, `to_status`) with a version prefix; the verifier must use the same version as the signer.

---

## Ed25519 test vector (v0)

Implementers may use the following deterministic payload and (when crypto is added) verify that a signature over it is accepted when the DID Document’s verification method contains the corresponding public key.

**Canonical payload example:**

| Field         | Value                    |
|---------------|--------------------------|
| `proof_id`    | `gov004-test-001`        |
| `signer_did`  | `did:freed:test-key-001` |
| `issued_at_utc` | `2026-02-17T05:45:00Z` |

**Payload bytes (UTF-8, newline-separated):**  
`gov004-test-001\ndid:freed:test-key-001\n2026-02-17T05:45:00Z`

**Payload hex (for test vectors):**  
`676f763030342d746573742d3030310a6469643a66726565643a746573742d6b65792d3030310a323032362d30322d31375430353a34353a30305a`

**Verifier contract:** When a verification method has type `Ed25519VerificationKey2020` (or equivalent) and provides a 32-byte public key, the verifier must recompute the canonical payload with `build_canonical_payload(auth_proof)` (see `freed_id_did_signature_verifier`), decode `signature_ref` as 64-byte Ed25519 signature (e.g. hex or base64url), and accept only if the signature is valid over the payload. Use RFC 8032 test vectors for algorithm conformance; this vector defines the GOV-004 payload shape for one known-good case.

---

## Implementation status (scaffold)

- **Done:** Design doc (this file); stub module that resolves the DID via registry; integration example; **canonical signed payload format (v0)**; **Ed25519 test vector v0** (payload hex + verifier contract); **canonical payload builder** in `freed_id_did_signature_verifier.build_canonical_payload`.
- **TODO:** Implement verification of `signature_ref` over the canonical payload using `verification_methods` (e.g. Ed25519); add tests that pass real signatures and fail on invalid ones; wire into Heart verifiers and require PASS when DID-method verifier is used.

---

## References

- `freed_id_dispute_recourse.py`: `SignatureVerifier`, `_resolve_auth_proof`, `apply_transition`.
- `freed_id_spec.md`: DID method, resolution, verification.
- `docs/freedid-cosmic-control-matrix-v0.md`: GOV-004 next action.

---

*Caelis · Session 3 (scaffold) · Session 6 (integration example) · Session 8 (canonical payload v0) · Session 12 (Ed25519 test vector v0 + canonical payload helper) · 2026-02-17 · Heart track advancement*
