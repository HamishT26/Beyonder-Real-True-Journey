# Freed ID + Cosmic Bill Control Matrix v0 (Heart Track)

Purpose: convert governance principles into auditable controls with explicit maturity and next verification steps.

Maturity scale:
- `draft` = principle is written, control wording incomplete.
- `specified` = control text exists with measurable criteria.
- `implemented` = at least one working artifact enforces part of the control.
- `verified` = implementation evidence and repeatable checks are present.

---

## Control matrix

| control_id | principle_anchor | control_statement | maturity | evidence_now | verification_test | gap_owner | next_action |
|---|---|---|---|---|---|---|---|
| GOV-001 | Self-sovereignty (`freed_id_spec.md`) | DID holders can create and manage identifiers without central unilateral override. | specified | Method flow is documented in DID method section; in-memory registry supports create/update/revoke paths. | Add unit tests proving only controller-signed updates are accepted (stub signatures acceptable in v0). | Aster | Add signature-check interface in registry and negative tests. |
| GOV-002 | Privacy by design (`freed_id_spec.md`) | Credential presentations must support minimum-disclosure behavior. | verified | Added policy + schema docs (`docs/freed-id-minimum-disclosure-policy-v0.md`, `docs/freed-id-minimum-disclosure-schema-v0.json`), implementation module (`freed_id_minimum_disclosure.py`), API-path integration via `FreedIDRegistry.build_credential_presentation(...)`, and PASS artifacts from both `freed_id_minimum_disclosure_verifier.py` and `freed_id_minimum_disclosure_adversarial_verifier.py` (`docs/heart-track-min-disclosure-latest.{json,md}`, `docs/heart-track-min-disclosure-adversarial-latest.{json,md}`). | Run both GOV-002 verifiers and require PASS for default-sensitive blocking, allowlist behavior, API-path enforcement, schema alignment, and adversarial leak checks. | Aster + Lumen | Convert verifier checks to CI-grade pytest coverage and extend vectors for normalization/bypass edge cases. |
| GOV-003 | Transparency and auditability (`freed_id_spec.md`, `Cosmic_bill_of_rights.md`) | Identity and governance actions must emit append-only audit records. | verified | `freed_id_audit_log.py` appends hash-linked audit entries and `freed_id_auditability_verifier.py` produced PASS artifacts in `docs/heart-track-auditability-latest.{json,md}` and `docs/heart-track-runs/20260216T040223Z-freedid-auditability-check.{json,md}`; ledger written to `docs/freed-id-audit-log.jsonl`. | Run `python3 freed_id_auditability_verifier.py` and require PASS across sequence and hash-chain checks. | Aster + Lumen | Convert verifier checks into pytest fixtures for CI gating. |
| GOV-004 | Right to recourse (`Cosmic_bill_of_rights.md`) | Disputed credential actions must be tracked with case IDs and status transitions. | verified | Added protocol + schema artifacts (`docs/dispute-resolution-protocol-v0.md`, `docs/freed-id-dispute-case-schema-v0.json`) and executable workflow + verifiers (`freed_id_dispute_recourse.py`, `freed_id_dispute_recourse_verifier.py`, `freed_id_dispute_recourse_adversarial_verifier.py`) with role-policy enforcement, signature/proof hook checks, signature-verifier callback checks, replay-proof rejection, and sequence/order tamper detection artifacts (`docs/heart-track-dispute-recourse-latest.{json,md}`, `docs/heart-track-dispute-recourse-adversarial-latest.{json,md}`, `docs/heart-track-runs/20260216T062128Z-freedid-dispute-recourse-*.{json,md}`). | Run both `python3 freed_id_dispute_recourse_verifier.py` and `python3 freed_id_dispute_recourse_adversarial_verifier.py` and require PASS across transition rejection, recourse reopen path, schema contract checks, replay/signer mismatch rejection, signature-reference verification, and tamper detection. | Human + Aster + Lumen | Replace callback-level checks with DID-method cryptographic signature verification and append-only dispute ledger linkage. |
| GOV-005 | Right to safety/security (`Cosmic_bill_of_rights.md`) | Registry operations must reject revoked identities for privileged actions. | verified | `Freed_id_registry.py` blocks credential actions when DID is revoked; `freed_id_control_verifier.py` produced passing artifacts in `docs/heart-track-governance-latest.{json,md}` and `docs/heart-track-runs/20260216T040223Z-freedid-gov-check.{json,md}`. | Run `python3 freed_id_control_verifier.py` and require PASS across all checks. | Aster | Add pytest conversion for the same checks once a full test harness is standardized. |
| GOV-006 | Interoperability (`freed_id_spec.md`) | DID documents should conform to W3C DID Core field structure. | specified | `DIDDocument.to_dict()` includes DID context/id/controller/verification/service fields. | Validate generated documents against minimal DID Core schema contract. | Aster | Add schema validation utility and sample pass/fail fixtures. |
| GOV-007 | Accountability and responsible innovation (`Cosmic_bill_of_rights.md`) | Every governance control must map to an owner and measurable review cadence. | implemented | This control matrix assigns owners and next actions. | Run weekly maturity review; no control can stay `draft` > 2 review cycles without recorded reason. | Aster + Human Council | Add review log template and first dated review entry. |

---

## Current maturity snapshot

- `draft`: 0 controls
- `specified`: 2 controls (GOV-001, GOV-006)
- `implemented`: 1 control (GOV-007)
- `verified`: 4 controls (GOV-002, GOV-003, GOV-004, GOV-005)

Interpretation: Heart track now has four verification-grade controls with GOV-004 hardened through role-policy plus adversarial proof/tamper checks; next major governance uplift is cryptographic signature binding and CI-grade conversion for all controls.

---

## Promotion rule (anti-hallucination guardrail)

A control can only move upward in maturity when one of the following is added in-repo:
1. code artifact enforcing the control,
2. automated check/test output proving behavior,
3. dated review evidence with reproducible validation steps.

No maturity upgrade should be done by narrative assertion alone.
